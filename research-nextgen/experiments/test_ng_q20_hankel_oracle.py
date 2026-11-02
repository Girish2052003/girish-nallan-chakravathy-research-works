"""Independent exhaustive/seeded checks for NG-Q20 finite-field Hankel method."""
from itertools import product
from random import Random
from fractions import Fraction
import unittest
from ng_q20_hankel_oracle import (evaluate,reconstruct,exploratory_hankel_basis,all_words,
   mod_matmul,rank,inverse,needle,needle_word_reconstruction_success_limit)

class TestHankel(unittest.TestCase):
    def test_binary_needle_hankel_anti_diagonal(self):
        u=('a','b','a','b')
        alpha,A,beta=needle(u,2)
        f=lambda w:evaluate(alpha,A,beta,2,w)
        P=tuple(u[:j] for j in range(5))
        S=tuple(u[j:] for j in range(5))
        H=tuple(tuple(f(x+y) for y in S) for x in P)
        self.assertEqual(H,tuple(tuple(int(i==j) for j in range(5)) for i in range(5)))
        self.assertEqual(rank(H,2),5)
        out=reconstruct(f,('a','b'),2,P,S)
        self.assertTrue(all(evaluate(out['alpha'],out['M'],out['beta'],2,w)==f(w) for w in all_words(('a','b'),7)))
        self.assertLessEqual(out['oracle_calls'],(2+1)*25+10)

    def test_all_2_letter_needles_length_4(self):
        for u in product(('a','b'),repeat=4):
            alpha,A,beta=needle(u,3,alphabet=('a','b'))
            f=lambda w:evaluate(alpha,A,beta,3,w)
            P=tuple(u[:j] for j in range(5))
            S=tuple(u[j:] for j in range(5))
            result=reconstruct(f,('a','b'),3,P,S)
            self.assertEqual(result['dimension'],5)
            for w in all_words(('a','b'),5):
                self.assertEqual(evaluate(result['alpha'],result['M'],result['beta'],3,w),int(w==u))

    def test_random_hidden_noncommutative_representations(self):
        rng=Random(20261102)
        for p,d,alphabet in ((2,2,('a','b')),(3,3,('a','b')),(7,3,('a','b','c')),(11,4,('a','b'))):
            for seed in range(9):
                for attempt in range(100):
                    alpha=tuple(rng.randrange(p) for _ in range(d))
                    beta=tuple(rng.randrange(p) for _ in range(d))
                    A={a:tuple(tuple(rng.randrange(p) for _ in range(d)) for _ in range(d)) for a in alphabet}
                    f=lambda w:evaluate(alpha,A,beta,p,w)
                    try:P,S=exploratory_hankel_basis(f,alphabet,p,d);break
                    except ValueError:continue
                else:self.fail('did not find minimal random automaton')
                out=reconstruct(f,alphabet,p,P,S)
                self.assertEqual(out['dimension'],d)
                self.assertLessEqual(out['oracle_calls'],(len(alphabet)+1)*d*d+2*d)
                for w in all_words(alphabet,5):
                    self.assertEqual(evaluate(out['alpha'],out['M'],out['beta'],p,w),f(w),(p,d,seed,w))

    def test_noncommuting_hidden_matrices_remain_noncommuting(self):
        p=5;alpha=(1,0);beta=(1,2)
        A={'a':((1,1),(0,1)),'b':((1,0),(1,1))}
        self.assertNotEqual(mod_matmul(A['a'],A['b'],p),mod_matmul(A['b'],A['a'],p))
        f=lambda w:evaluate(alpha,A,beta,p,w)
        P,S=exploratory_hankel_basis(f,('a','b'),p,2)
        out=reconstruct(f,('a','b'),p,P,S)
        self.assertNotEqual(mod_matmul(out['M']['a'],out['M']['b'],p),mod_matmul(out['M']['b'],out['M']['a'],p))
        self.assertTrue(all(evaluate(out['alpha'],out['M'],out['beta'],p,w)==f(w) for w in all_words(('a','b'),8)))

    def test_wrong_basis_rejected(self):
        alpha,A,beta=needle(('a','b','a'),3)
        f=lambda w:evaluate(alpha,A,beta,3,w)
        with self.assertRaises(ValueError):reconstruct(f,('a','b'),3,[(),('a',)],[(),('b',)])
        with self.assertRaises(ValueError):reconstruct(f,('a','b'),3,[(),()],[(),('b',)])
        with self.assertRaises(ValueError):reconstruct(f,('a','b'),4,[()],[()])

    def test_invalid_oracle_output_rejected(self):
        with self.assertRaises(ValueError):reconstruct(lambda w:3,('a',),3,[()],[()])

    def test_no_hit_transcripts_identical_for_all_needle_words(self):
        alphabet=('a','b');L=5
        queries=[(),('a',),('b',)*3,('a',)*5,('b',)*5]
        for u in product(alphabet,repeat=L):
            if u in queries:continue
            alpha,A,beta=needle(u,2,alphabet=('a','b'))
            self.assertEqual([evaluate(alpha,A,beta,2,w) for w in queries],[0]*len(queries))

    def test_membership_only_exact_success_bound(self):
        self.assertEqual(needle_word_reconstruction_success_limit(2,8,20),Fraction(21,256))
        self.assertEqual(needle_word_reconstruction_success_limit(3,3,8),Fraction(1,3))
        with self.assertRaises(ValueError):needle_word_reconstruction_success_limit(2,4,16)

    def test_rank_d_needle_prefix_suffix_bound(self):
        for L in range(1,7):
            u=tuple('a' if i%2==0 else 'b' for i in range(L))
            alpha,A,beta=needle(u,3,alphabet=('a','b'))
            f=lambda w:evaluate(alpha,A,beta,3,w)
            P=tuple(u[:i] for i in range(L+1));S=tuple(u[i:] for i in range(L+1))
            H=tuple(tuple(f(x+y) for y in S) for x in P)
            self.assertEqual(rank(H,3),L+1)
            self.assertLessEqual(max(len(x)+1+len(y) for x in P for y in S),2*(L+1)-1)

    def test_empty_automaton_word_evaluation(self):
        self.assertEqual(evaluate((2,),{'a':((4,),)},(3,),5,()),1)
        self.assertEqual(evaluate((2,),{'a':((4,),)},(3,),5,('a',)),4)
        with self.assertRaises(ValueError):evaluate((2,),{'a':((4,),)},(3,),5,('b',))

if __name__=='__main__':unittest.main(verbosity=2)
