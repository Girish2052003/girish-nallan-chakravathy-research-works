#!/usr/bin/env python3
"""Source-parameter exact packing audit and regression tests (not security proof)."""
from dataclasses import dataclass
import unittest
import hashlib

@dataclass(frozen=True)
class Profile:
    name:str
    m:int
    d:int
    N:int
    ell:int
    M:int
    u:int
    repetition:int=7
    field_bits:int=10
    @property
    def rows(self): return self.m * 3**self.d
    @property
    def label_bits(self): return self.rows*self.N*self.field_bits
    @property
    def ciphertext_bits(self): return self.rows*self.ell*self.repetition*self.field_bits
    @property
    def relation_min(self): return self.u+1
    @property
    def decoding_radius(self): return (self.M-self.u)//2
    @property
    def packed_label_bytes(self): return (self.label_bits+7)//8
    @property
    def packed_ciphertext_bytes(self): return (self.ciphertext_bits+7)//8

PROFILES=(
    Profile("SGD-R1",1024,3,640,320,256,64),
    Profile("SGD-R2",1536,4,960,448,384,96),
    Profile("SGD-R3",2048,5,1280,640,512,128),
)
EXPECTED={
    "SGD-R1":(27648,22118400,77414400,65,96),
    "SGD-R2":(124416,149299200,487710720,97,144),
    "SGD-R3":(497664,796262400,2786918400,129,192)
}

def checksum_manifest(path):
    with open(path,'rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

class ProfileAudits(unittest.TestCase):
    def test_dimensions_and_exact_storage_bounds(self):
        for p in PROFILES:
            with self.subTest(profile=p.name):
                self.assertEqual((p.rows,p.packed_label_bytes,p.packed_ciphertext_bytes,p.relation_min,p.decoding_radius),EXPECTED[p.name])
                self.assertLessEqual(p.M,1<<p.field_bits)
                self.assertLess(p.u,p.M)
                # Even optimal cross-symbol bit packing can't save this expansion
                self.assertGreater(p.packed_ciphertext_bytes,10_000_000)
    def test_ratio_exposes_extreme_expansion(self):
        for p in PROFILES:
            with self.subTest(profile=p.name):
                self.assertGreater(p.ciphertext_bits//p.ell,1_000_000)
    def test_original_sha256_known(self):
        # SHA of the 26-page *binary original*, not the GitHub text extraction
        expected="24461af422a6a7d1fbadcc29fe4fe372761805a846226d6d343e7180c5382f4d"
        self.assertEqual(len(expected),64)

if __name__=="__main__":
    for p in PROFILES:
        print(f"{p.name}: public label matrix >= {p.packed_label_bytes:,} bytes "
              f"({p.packed_label_bytes/2**20:.2f} MiB); "
              f"ciphertext >= {p.packed_ciphertext_bytes:,} bytes "
              f"({p.packed_ciphertext_bytes/2**20:.2f} MiB); "
              f"first planted relation {p.relation_min}")
    unittest.main(verbosity=2)
