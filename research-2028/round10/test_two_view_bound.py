"""Finite checks of the two-view interpolation and refuting-list theorem."""

import itertools
import random
import unittest

FIELD = (0, 1, 2)
ADDRESSES = tuple(itertools.product(FIELD, repeat=2))
POLICIES = tuple(itertools.product(FIELD, repeat=3))
COEFFICIENTS = tuple(itertools.product(FIELD, repeat=4))


def left(row, a, b, u):
    constant, x, xx, xy, _, _, k, ka, kb, _, _, _ = row
    return (constant + x*a + xx*a*a + xy*a*b + (k + ka*a + kb*b)*u) % 3


def right(row, a, b, v):
    _, _, _, _, y, yy, _, _, _, k, ka, kb = row
    return (y*b + yy*b*b + (k + ka*a + kb*b)*v) % 3


def q_value(coefficients, a, b):
    constant, x, y, xy = coefficients
    return (constant + x*a + y*b + xy*a*b) % 3


def interpolant(frame_values):
    v00, v01, v10, v11 = frame_values
    return (v00, (v10-v00) % 3, (v01-v00) % 3, (v11-v01-v10+v00) % 3)


def direct_policy(row, addresses):
    allowed = {
        (a, b): {(u, v) for u, v in ADDRESSES
                 if (left(row, a, b, u) + right(row, a, b, v)) % 3 == 0}
        for a, b in addresses
    }
    for f, g in itertools.product(POLICIES, repeat=2):
        if all((f[a], g[b]) in pairs for (a, b), pairs in allowed.items()):
            return f, g
    return None


def projected_sets(row):
    """Explicitly project attainable frame pairs, then test Q on each frame."""
    result = []
    for a in FIELD:
        reachable = {(left(row, a, 0, u), left(row, a, 1, u)) for u in FIELD}
        allowed_q = {q for q in COEFFICIENTS if (q_value(q, a, 0), q_value(q, a, 1)) in reachable}
        result.append(("left", a, allowed_q))
    for b in FIELD:
        reachable = {((-right(row, 0, b, v)) % 3, (-right(row, 1, b, v)) % 3) for v in FIELD}
        allowed_q = {q for q in COEFFICIENTS if (q_value(q, 0, b), q_value(q, 1, b)) in reachable}
        result.append(("right", b, allowed_q))
    return result


class TwoViewTests(unittest.TestCase):
    def test_biaffine_interpolation(self):
        for q in COEFFICIENTS:
            frame = [q_value(q, a, b) for a, b in itertools.product((0, 1), repeat=2)]
            self.assertEqual(interpolant(frame), q)

    def test_unseen_quadratic_probe_interpolation(self):
        # The six probes interpolate all 729 bivariate ternary quadratics.
        for coefficients in itertools.product(FIELD, repeat=6):
            def evaluate(i, j):
                c, x, y, xx, yy, xy = coefficients
                return (c + x*i + y*j + xx*i*i + yy*j*j + xy*i*j) % 3
            c, u, v, s, t, mixed = [evaluate(i, j) for i, j in
                                     ((0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1))]
            recovered = (c, 2*(u-s), 2*(v-t), 2*(u+s-2*c),
                         2*(v+t-2*c), mixed-u-v+c)
            self.assertEqual(tuple(k % 3 for k in recovered), coefficients)

    def test_projected_spaces_and_actual_refuting_subsets(self):
        rng = random.Random(1025)
        samples = [tuple(rng.randrange(3) for _ in range(12)) for _ in range(150)]
        # Include an identity and a contradictory constant row.
        samples.extend([(0,)*12, (1,) + (0,)*11])
        yes = no = smaller = 0
        for row in samples:
            policy = direct_policy(row, ADDRESSES)
            candidates = set(COEFFICIENTS)
            selected = []
            for side, address, allowed in projected_sets(row):
                narrowed = candidates & allowed
                if narrowed != candidates:
                    selected.append((side, address))
                    candidates = narrowed
                if not candidates:
                    break
            self.assertEqual(bool(candidates), policy is not None)
            if policy is not None:
                yes += 1
                values = [left(row, a, b, policy[0][a])
                          for a, b in itertools.product((0, 1), repeat=2)]
                q = interpolant(values)
                self.assertIn(q, candidates)
                for a, b in ADDRESSES:
                    self.assertEqual(left(row, a, b, policy[0][a]), q_value(q, a, b))
                continue
            no += 1
            self.assertLessEqual(len(selected), 5)  # D = 4.
            probes = set(itertools.product((0, 1), repeat=2))
            for side, address in selected:
                for base in (0, 1):
                    probes.add((address, base) if side == "left" else (base, address))
            self.assertIsNone(direct_policy(row, probes))
            smaller += len(probes) < len(ADDRESSES)
        self.assertGreater(yes, 1)
        self.assertGreater(no, 1)
        self.assertGreater(smaller, 1)


if __name__ == "__main__":
    unittest.main()
