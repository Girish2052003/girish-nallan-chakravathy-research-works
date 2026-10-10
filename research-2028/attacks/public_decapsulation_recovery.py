#!/usr/bin/env python3
"""Round 5: public decryption and session-key recovery on archived SG-DIFRA-MDS.

The published GF(1024) fixed-field GRS frame can be recovered in asymptotic
PPT under polynomial public-key sizes and N=Omega(lambda). Then a public
information-set decoder simulates SECRET bit-decapsulation for EVERY ciphertext.
This is NOT a feasible attack on the three frozen profiles. No new NCSG-only
secure KEM is being proposed or proved by this script.

Imports the real Round-3 finite-field implementation, not a mock cipher.
The toy FO-style deterministic re-encryption fixture is not a QROM proof.
"""
import hashlib
import itertools
import math
import random
import unittest

from fixed_field_mds_hbce_ppt_break import (
    Q, gf_mul, gf_rank, gframe, make_plant, find_low_rank_subset
)

def field_pow(a,n):
    z=1
    while n:
        if n&1:z=gf_mul(z,a)
        a=gf_mul(a,a); n>>=1
    return z

def dot(a,b):
    out=0
    for x,y in zip(a,b):out^=gf_mul(x,y)
    return out

def solve(A,b):
    n=len(b)
    t=[list(row)+[v] for row,v in zip(A,b)]
    for k in range(n):
        j=next((j for j in range(k,n) if t[j][k]),None)
        if j is None:return None
        t[k],t[j]=t[j],t[k]
        inv=field_pow(t[k][k],Q-2)
        t[k]=[gf_mul(inv,x) for x in t[k]]
        for h in range(n):
            if h!=k and t[h][k]:
                mult=t[h][k]
                t[h]=[x^gf_mul(mult,y) for x,y in zip(t[h],t[k])]
    return [row[-1] for row in t]

def public_recover_good_rows(H,u):
    # Round 3: enumerate public (u+1)-row dependencies.
    found=find_low_rank_subset(H,u)
    if found is None:return None
    W=[H[i] for i in found[:u]]
    if gf_rank(W)!=u:return None
    # A random decoy lies in planted W with negligible probability
    # in growing ambient dimension N.
    return tuple(i for i,row in enumerate(H) if gf_rank(W+[row])==u)

def code_coefficients(rows,u):
    # Express every recovered planted row in one PUBLIC u-row basis.
    basis=rows[:u]
    chosen=[]
    for col in range(len(basis[0])):
        trial=chosen+[col]
        if gf_rank([[row[k] for k in trial] for row in basis])==len(trial):
            chosen=trial
        if len(chosen)==u:break
    assert len(chosen)==u
    linear=[[basis[j][col] for j in range(u)] for col in chosen]
    coeff=[]
    for row in rows:
        a=solve(linear,[row[col] for col in chosen])
        assert a is not None
        assert all(dot(a,[basis[j][col] for j in range(u)])==v
                   for col,v in enumerate(row))
        coeff.append(a)
    return coeff

def public_bounded_distance_decision(generator,received,u):
    M=len(generator)
    threshold=(M-u)//2
    # Every u rows of this hidden-GRS-derived code are independent.
    # Enumerating u information sets exactly matches GRS accept/reject
    # for ALL received words (not just ciphertexts honestly generated).
    for J in itertools.combinations(range(M),u):
        a=solve([generator[j] for j in J],[received[j] for j in J])
        if a is None:continue
        if sum(dot(row,a)!=symbol
               for row,symbol in zip(generator,received))<=threshold:
            return 0
    return 1

def encrypt_bit(H,bit,rng):
    q=len(H)
    if bit:return tuple(rng.randrange(Q) for _ in range(q))
    t=[rng.randrange(Q) for _ in range(len(H[0]))]
    ciphertext=[]
    for row in H:
        symbol=dot(row,t)
        if rng.randrange(16)<3:
            symbol^=rng.randrange(1,Q)
        ciphertext.append(symbol)
    return tuple(ciphertext)

def encrypt_message(H,msg,seed):
    rng=random.Random(seed)
    return tuple(encrypt_bit(H,int(bit),rng)
                 for bit in msg for _ in range(3))

def decrypt_message(H,indices,u,C,secret_order=False):
    if secret_order:
        generator=gframe(len(indices),u)
    else:
        generator=code_coefficients([H[i] for i in indices],u)
    result=[]
    for k in range(0,len(C),3):
        decisions=[public_bounded_distance_decision(
            generator,[v[i] for i in indices],u) for v in C[k:k+3]]
        result.append('1' if sum(decisions)>=2 else '0')
    return ''.join(result)

def test_coin(msg):
    return int.from_bytes(hashlib.sha256(
        b'ROUND5-TOY-COINS'+msg.encode()).digest(),'big')

def test_key(msg,C):
    return hashlib.sha256(
        b'ROUND5-TOY-KEY'+msg.encode()+repr(C).encode()).hexdigest()

class PublicKeyRecoveryTests(unittest.TestCase):
    def test_all_selected_rows_and_bit_decisions(self):
        q,N,M,u=16,6,9,2
        for seed in range(12):
            H,secret=make_plant(q,N,M,u,seed+800)
            found=public_recover_good_rows(H,u)
            self.assertEqual(set(found),set(secret))
            for bit in (0,1):
                for sample in range(4):
                    v=encrypt_bit(H,bit,random.Random(seed*132+sample*3+bit))
                    secret_result=public_bounded_distance_decision(
                        gframe(M,u),[v[i] for i in secret],u)
                    public_result=public_bounded_distance_decision(
                        code_coefficients([H[i] for i in found],u),
                        [v[i] for i in found],u)
                    self.assertEqual(secret_result,public_result)
        print("Round 5: 12/12 recovered planted row sets, "
              "96/96 private-public bit decision matches")

    def test_end_to_end_toy_deterministic_kem_key_recovery(self):
        # Tiny fixture faithfully reproduces the linear channel, exact
        # independent 3/16 noise flags, repetition, and re-encryption check.
        # Uses a toy hash domain, NOT the archival full encoding/QROM.
        H,secret=make_plant(16,6,9,2,202806)
        recovered=public_recover_good_rows(H,2)
        self.assertEqual(set(recovered),set(secret))
        rng=random.Random(23052)
        recovered_keys=0
        for _ in range(10):
            mu=''.join(str(rng.randrange(2)) for j in range(8))
            C=encrypt_message(H,mu,test_coin(mu))
            real_mu=decrypt_message(H,secret,2,C,secret_order=True)
            attacker_mu=decrypt_message(H,recovered,2,C)
            self.assertEqual(real_mu,attacker_mu)
            accepts=(encrypt_message(H,real_mu,test_coin(real_mu))==C)
            attacker_accepts=(
                encrypt_message(H,attacker_mu,test_coin(attacker_mu))==C)
            self.assertEqual(accepts,attacker_accepts)
            if accepts:
                self.assertEqual(attacker_mu,mu)
                self.assertEqual(test_key(attacker_mu,C),test_key(mu,C))
                recovered_keys+=1
        self.assertGreaterEqual(recovered_keys,6)
        print("Round 5: exact public/secret decapsulation agreement "
              "on 10/10 toy ciphertexts; recovered real keys",
              recovered_keys,"/10")

    def test_frozen_profile_upper_work_budgets(self):
        for name,q,M,u in (("R1",27648,256,64),
                           ("R2",124416,384,96),
                           ("R3",497664,512,128)):
            discover=math.log2(math.comb(q,u+1))
            decode=math.log2(math.comb(M,u))
            self.assertGreater(discover,600)
            self.assertGreater(decode,200)
            print(name,"finite exhaustive log2 search",round(discover,2),
                  "public decode log2 combinations",round(decode,2))

if __name__=="__main__":
    unittest.main(verbosity=2)
