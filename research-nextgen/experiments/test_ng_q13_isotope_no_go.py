import unittest
from random import Random
from ng_q13_isotope_no_go import (
    random_isotope,public_principal_group, public_group_coordinates,
    group_sum, group_diff, recover_equivalent_isotope)


class TestIsotopeNoGo(unittest.TestCase):
    def test_publicly_normalized_law_is_group_and_recovered(self):
        for m,trials in ((1,10),(2,15),(3,10)):
            n=3**m
            for j in range(trials):
                T,alpha,beta,gamma=random_isotope(m,62000+100*m+j)
                x0=(3+j)%n;y0=(5+j)%n
                P,e=public_principal_group(T,n,x0,y0)
                self.assertEqual(e,T[x0,y0])
                inverse_gamma={g:i for i,g in enumerate(gamma)}
                for x in range(n):
                    for y in range(n):
                        self.assertEqual(P[x,y], inverse_gamma[group_diff(
                            group_sum(gamma[x],gamma[y],m),gamma[e],m)])
                coords=public_group_coordinates(P,n,e)
                self.assertEqual(len(set(coords.values())),n)
                for x in range(n):
                    for y in range(n):
                        self.assertEqual(coords[P[x,y]],tuple((a+b)%3 for a,b in
                                         zip(coords[x],coords[y])))

    def test_public_row_suffices_to_divide(self):
        T,*_=random_isotope(2,81231)
        for x in range(9):
            for z in range(9):
                ys=[y for y in range(9) if T[x,y]==z]
                self.assertEqual(len(ys),1)
                self.assertEqual(T[x,ys[0]],z)

    def test_recover_equivalent_hidden_isotopy_key(self):
        for m in (1,2,3):
            n=3**m
            T,_,_,_=random_isotope(m,1990+m)
            alpha,beta,gamma=recover_equivalent_isotope(T,n,1%n,2%n)
            self.assertEqual(set(alpha.values()),set(range(n)))
            self.assertEqual(set(beta.values()),set(range(n)))
            self.assertEqual(set(gamma.values()),set(range(n)))
            inverse_gamma={v:i for i,v in gamma.items()}
            for x in range(n):
                for y in range(n):
                    self.assertEqual(T[x,y],inverse_gamma[group_sum(alpha[x],beta[y],m)])

    def test_invalid_nonlatin_rejected(self):
        T={(x,y):0 for x in range(9) for y in range(9)}
        with self.assertRaises(ValueError): public_principal_group(T,9)

    def test_public_identity_different_from_original_group_zero(self):
        T,a,b,g=random_isotope(2,32498)
        P,e=public_principal_group(T,9,2,3)
        coords=public_group_coordinates(P,9,e)
        self.assertEqual(coords[e],(0,0))


if __name__=='__main__':unittest.main(verbosity=2)
