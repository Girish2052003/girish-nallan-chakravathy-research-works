#!/usr/bin/env python3
"""Domain-separated encoding and hybrid KDF *test harness*.

The SHAKE256 binding construction below is illustrative. It is NOT a
verified split-key PRF, full KEM, FIPS-validated module, or QROM security proof.
No toy implementation should be deployed.
"""
import hashlib, hmac, os, unittest

DOMAIN=b"SG-DIFRA-EUROCRYPT-2028-HYBRID-RESEARCH-V1\x00"
def encode_fields(*fields):
    if len(fields)>255: raise ValueError("too many fields")
    result=bytearray(bytes([len(fields)]))
    for part in fields:
        if not isinstance(part,bytes):raise TypeError("expected canonical byte strings")
        if len(part)>=2**32:raise ValueError("field too long")
        result += len(part).to_bytes(4,"big")+part
    return bytes(result)

def parse_fields(wire, number, limits):
    if not isinstance(wire,bytes) or len(wire)<1:raise ValueError("invalid wire")
    if wire[0]!=number or number!=len(limits):raise ValueError("field-count mismatch")
    idx=1;fields=[]
    for limit in limits:
        if len(wire)-idx<4:raise ValueError("truncated length")
        k=int.from_bytes(wire[idx:idx+4],"big");idx+=4
        if k>limit or len(wire)-idx<k:raise ValueError("invalid field size")
        fields.append(wire[idx:idx+k]);idx+=k
    if idx!=len(wire):raise ValueError("trailing bytes")
    return tuple(fields)

def research_only_combiner(ss_ml,ss_sg,ct_ml,ct_sg,ek_ml,ek_sg,context=b"",length=32):
    if not 16<=length<=64:raise ValueError("output length invalid")
    payload=encode_fields(ss_ml,ss_sg,ct_ml,ct_sg,ek_ml,ek_sg,context)
    return hashlib.shake_256(DOMAIN+payload).digest(length)

class CodecTests(unittest.TestCase):
    def test_encoding_roundtrip(self):
        fields=(b"a",b"",b"\x00\x01",os.urandom(40))
        self.assertEqual(parse_fields(encode_fields(*fields),4,[10,0,10,40]),fields)
    def test_rejects_malformed_frames(self):
        packet=encode_fields(b"abc",b"def")
        for bad in (packet[:-1],packet+b"x",packet[:2],b"\x01"+packet[1:]):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):parse_fields(bad,2,[3,3])
    def test_independent_field_binding(self):
        args=[os.urandom(32),os.urandom(32),os.urandom(16),os.urandom(21),
              os.urandom(64),os.urandom(72),b"label"]
        base=research_only_combiner(*args)
        self.assertTrue(hmac.compare_digest(base,research_only_combiner(*args)))
        for i,item in enumerate(args):
            modified=args[:]
            modified[i]=item+b"\x01"
            self.assertNotEqual(research_only_combiner(*modified),base)
    def test_public_ciphertext_binding_even_with_broken_sg_key(self):
        # sg shared secret deliberately set to a known, constant all-zero string.
        ml_secret=os.urandom(32)
        sg_broken=b"\0"*32
        a=research_only_combiner(ml_secret,sg_broken,b"ctML",b"ctSG",b"ekML",b"ekSG")
        b=research_only_combiner(ml_secret,sg_broken,b"ctML",b"ctS2",b"ekML",b"ekSG")
        self.assertNotEqual(a,b)
    def test_no_proof_claim_from_hash_kat(self):
        # Deterministic test vector, not evidence of quantum security.
        self.assertEqual(len(research_only_combiner(b"x"*32,b"y"*32,b"a",b"b",b"c",b"d")),32)
if __name__=="__main__":
    unittest.main(verbosity=2)
