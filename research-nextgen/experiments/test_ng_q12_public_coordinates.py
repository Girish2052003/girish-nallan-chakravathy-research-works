import unittest
from collections import Counter
from itertools import product
from random import Random
from fractions import Fraction
from ng_q12_public_coordinates import (
    POINTS2, POINTS3, F3, all_invertible_matrices, rank, matvec, invert,
    generate, recover_equivalent, fixed_basis_source_count,
    membership_false_positive_upper_bound)


class TestPublicCoordinates(unittest.TestCase):
    def test_full_11232_matrix_count_and_inverses(self):
        all_m=list(all_invertible_matrices())
        self.assertEqual(len(all_m),11232)
        self.assertEqual(len(set(all_m)),11232)
        for M in (all_m[:30] + all_m[5555:5570] + all_m[-10:]):
            self.assertEqual(rank(M),3)
            C=invert(M)
            for u in POINTS3:
                self.assertEqual(matvec(C,matvec(M,u)),u)

    def test_exact_image_kernel_for_all_19683_Q(self):
        count=Counter()
        for Qvalues in product(F3,repeat=9):
            Q=dict(zip(POINTS2,Qvalues))
            g=tuple((Q[((z+1)%3,w)]-Q[(z,w)])%3 for z,w in POINTS2)
            count[g]+=1
            for w in F3:
                self.assertEqual(sum(g[POINTS2.index((z,w))] for z in F3)%3,0)
        self.assertEqual(len(count),729)
        self.assertEqual(set(count.values()),{27})
        self.assertEqual(fixed_basis_source_count(),(729,27))

    def test_recover_equivalent_for_masked_source(self):
        rng=Random(20261101)
        matrix_list=list(all_invertible_matrices())
        for j in range(15):
            B=matrix_list[rng.randrange(len(matrix_list))]
            A=rng.choice((1,2))
            Q=dict(zip(POINTS2,(rng.randrange(3) for _ in POINTS2)))
            f=generate(B,A,Q)
            found=recover_equivalent(f)
            self.assertIsNotNone(found, f'instance {j}')
            self.assertEqual(generate(*found),f)

    def test_reject_nonsource_extremes_and_random(self):
        self.assertIsNone(recover_equivalent({x:0 for x in POINTS3}))
        rng=Random(9132)
        for _ in range(12):
            f={x:rng.randrange(3) for x in POINTS3}
            self.assertIsNone(recover_equivalent(f))

    def test_exact_upper_probability(self):
        self.assertEqual(membership_false_positive_upper_bound(),
                         Fraction(832,387420489))
        self.assertLess(membership_false_positive_upper_bound(),Fraction(1,400000))

    def test_invalid_table_rejected(self):
        with self.assertRaises(ValueError):recover_equivalent({})
        with self.assertRaises(ValueError):recover_equivalent({x:3 for x in POINTS3})


if __name__=='__main__':unittest.main(verbosity=2)
