from hashlib import shake_256
from itertools import combinations
from math import comb
import unittest

from projected_kem import Params, ProjectedKEM, research_profile


def unpack(raw, width):
    value = int.from_bytes(raw, "big")
    trits = [0] * width
    for i in reversed(range(width)):
        value, trits[i] = divmod(value, 3)
    assert value == 0
    return trits


def pack(trits):
    rank = 0
    for value in trits:
        rank = 3*rank + value
    return rank.to_bytes(((3**len(trits)-1).bit_length()+7)//8, "big")


def digest(fields, size):
    wire = b"".join(len(v).to_bytes(8, "big")+v for v in fields)
    return shake_256(wire).digest(size)


class ProjectedTests(unittest.TestCase):
    def test_every_signed_source_error_at_radius_two(self):
        p = Params(3, 2, 1, 20, 1, 2, 8)
        kem = ProjectedKEM(p, 4)
        seed, trap = bytes(32), b"p"
        checks = kem._checks(trap)
        public = kem._public(seed, checks)
        word = list(kem._outer.encode(5))
        seen = set()
        for i, j in combinations(range(p.N), 2):
            for signs in range(4):
                rank = 4*(i+comb(j, 2)) + signs
                coins = rank.to_bytes(p.coin_bytes, "big")
                body = unpack(kem._body(public, b"\x05", coins), kem.N)
                expected = [0]*kem.m + word[:]
                for pos, sign in ((i, signs&1), (j, signs>>1)):
                    if pos < kem.N:
                        expected[pos] = (expected[pos] + (1-2*sign)) % 3
                self.assertEqual(body, expected)
                seen.add((i < kem.N) + (j < kem.N))
                residual = [(body[kem.m+k]-sum(s*body[v] for v,s in check)) % 3
                            for k,check in enumerate(checks)]
                self.assertLessEqual(sum(a != b for a,b in zip(residual,word)), 2)
        self.assertEqual(seen, {0, 1, 2})

    def test_private_seed_checks_against_direct_subset_enumeration(self):
        p = Params(3, 2, 1, 35, 2, 2, 8)
        kem = ProjectedKEM(p, 4)
        seed = b"k"
        widths = []
        for j in range(kem.t):
            choices = comb(kem.m-j*p.w,p.w) * 2**p.w
            widths.append(((choices-1).bit_length()+7)//8 + kem.slack_bytes)
        tape = digest([b"SG-DIFRA/R15/private-supports/v1",kem.suite,b"",seed],sum(widths))
        available = list(range(kem.m))
        expected = []
        start = 0
        for width in widths:
            end = start + width
            subsets = sorted(combinations(range(len(available)),p.w),key=lambda pair: pair[::-1])
            value = int.from_bytes(tape[start:end],"big") % (len(subsets)*2**p.w)
            subset, signs = divmod(value, 2**p.w)
            check = tuple((available[i], -1 if signs & (1 << k) else 1)
                          for k,i in enumerate(subsets[subset]))
            expected.append(check)
            for i,_ in check:
                available.remove(i)
            start = end
        self.assertEqual(kem._checks(seed), expected)

    def test_independent_expansion_across_two_blocks(self):
        p = Params(3, 64, 1, 20, 1, 2, 8)
        kem = ProjectedKEM(p, 3)
        seed, hidden = b"M"*32, b"K"
        checks = kem._checks(hidden)
        public = kem._public(seed, checks)
        blocks = []
        rows = []
        row_bytes = ((3**kem.m-1).bit_length()+7)//8
        for i in range(p.d):
            raw = digest([b"SG-DIFRA/R15/matrix-row/v1", kem.suite, seed, i.to_bytes(8,"big")],
                         row_bytes+kem.slack_bytes)
            rank = int.from_bytes(raw,"big") % 3**kem.m
            a = unpack(rank.to_bytes(row_bytes,"big"), kem.m)
            check_row = [sum(a[pos]*sign for pos, sign in check) % 3 for check in checks]
            rows.append(a+check_row)
            blocks.extend(check_row)
        cut = 64*kem.t
        self.assertEqual(public, seed+pack(blocks[:cut])+pack(blocks[cut:]))
        # All linear input trits one, nonlinear input trit two (square one).
        variables = [1]*p.h + [2]
        input_rank = int.from_bytes(pack(variables), "big")
        coins = (p.noise_count*input_rank).to_bytes(p.coin_bytes,"big")
        clean = [sum(column)%3 for column in zip(*rows)]
        offset = [0]*kem.m + list(kem._outer.encode(3))
        expected = [(v+e+int(j<2)) % 3 for j,(v,e) in enumerate(zip(clean,offset))]
        self.assertEqual(unpack(kem._body(public,b"\x03",coins),kem.N),expected)

    def test_fo_and_invalid_wires(self):
        p = Params(5, 2, 1, 30, 1, 2, 8)
        kem = ProjectedKEM(p, 3)
        for _ in range(3):
            public, private = kem.keygen()
            c, k = kem.encaps(public)
            self.assertEqual((len(public),len(private),len(c),len(k)),
                             (kem.public_bytes,kem.private_bytes,kem.ciphertext_bytes,32))
            self.assertEqual(kem.decaps(private,c),k)
            self.assertIsNone(kem.decaps(private,c[:-1]))
            self.assertIsNone(kem.decaps(private,bytes([c[0]^1])+c[1:]))
            self.assertIsNone(kem.decaps(private,c[:3]+b"\xff"*kem.body_bytes))
            with self.assertRaises(ValueError):
                kem.encaps(public[:32]+b"\xff"*(kem.public_bytes-32))
            with self.assertRaises(ValueError):
                kem.decaps(private[:-1],c)
        with self.assertRaises(ValueError):
            ProjectedKEM(Params(1,1,1,8,1,0))
        with self.assertRaises(ValueError):
            ProjectedKEM(p, 0)

    def test_named_research_profiles(self):
        for b, expected in ((128,(3981553087,80,2216336)),
                            (192,(15022416160,96,5482436)),
                            (256,(35323168790,112,9722492))):
            kem = research_profile(b)
            p = kem.source
            self.assertEqual(kem.m-(kem.t-1)*p.w,p.m-(p.t-1)*p.w)
            self.assertLess(kem.N,p.N)
            self.assertEqual((kem.public_bytes,kem.private_bytes,kem.ciphertext_bytes),expected)
        with self.assertRaises(ValueError):
            research_profile(64)
