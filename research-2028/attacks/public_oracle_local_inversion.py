"""Public evaluation only inversion of source-form ternary MaxEnt maps.

For f(x)=A*u_L+g(u_R), (u_L,u_R)=B*x, with invertible A,B,
this randomized PUBLIC algorithm needs only an evaluation callable and
the public dimensions. It never receives A,B,g,Q,a or a planted witness.
The source case is g=Delta_a Q; the proof works for arbitrary g.

Let q=3^d. For S iid uniform input probes and T iid uniform shifts,
failure <= q*(1-1/q)^S + ((3^r-1)/2)*(1-2/(3q))^T.
The conservative implemented budgets give failure <= eta. The bound
concerns ideal independent uniform sampling; deterministic seeds below
are reproducibility fixtures, not proof of the probability bound.

This is a LOCAL right-inversion attack, not a global CSP solver or KEM.
"""
import math
from fractions import Fraction


def _add(a, b):
    return tuple((x + y) % 3 for x, y in zip(a, b))


def _sub(a, b):
    return tuple((x - y) % 3 for x, y in zip(a, b))


def _rank(rows):
    a = [list(row) for row in rows]
    p = 0
    for c in range(len(a[0]) if a else 0):
        j = next((i for i in range(p, len(a)) if a[i][c]), None)
        if j is None:
            continue
        a[p], a[j] = a[j], a[p]
        inv = pow(a[p][c], -1, 3)
        a[p] = [(v * inv) % 3 for v in a[p]]
        for i in range(p + 1, len(a)):
            factor = a[i][c]
            a[i] = [(x - factor * y) % 3 for x, y in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return p


def _solve_columns(columns, rhs):
    n = len(rhs)
    a = [[columns[j][i] for j in range(n)] + [rhs[i]] for i in range(n)]
    for c in range(n):
        j = next((i for i in range(c, n) if a[i][c]), None)
        if j is None:
            return None
        a[c], a[j] = a[j], a[c]
        inv = pow(a[c][c], -1, 3)
        a[c] = [(v * inv) % 3 for v in a[c]]
        for i in range(n):
            if i != c:
                factor = a[i][c]
                a[i] = [(x - factor * y) % 3 for x, y in zip(a[i], a[c])]
    return tuple(row[-1] for row in a)


def recover_public_right_inverse(evaluate, k, d, eta, rng):
    """Return a publicly recovered shift basis, or None if inconclusive.

    Returning None (including for an input outside the proved model)
    supplies no security evidence. Reuse of the same random probe set
    is sound: coverage of every hidden right-block input simultaneously
    makes every candidate filter exact, including adaptive candidates.
    """
    if not (1 <= d < k and 0 < eta < 1):
        raise ValueError("Require 1 <= d < k and 0 < eta < 1")
    r, q = k - d, 3**d
    # Avoid overflow in 2*q/eta for small, otherwise valid failure budgets.
    log_inverse_eta = -math.log(eta)
    probes_count = math.ceil(q * (math.log(2*q) + log_inverse_eta))
    shifts_count = math.ceil((3 * q / 2) *
                            (r * math.log(3) + math.log(2) + log_inverse_eta))
    # Exact rational tail checks make floating logarithms an initial budget
    # estimate only. Never let rounding weaken the stated failure bound.
    half_budget = Fraction(eta) / 2
    coverage_step = Fraction(q - 1, q)
    rank_step = Fraction(3*q - 2, 3*q)
    coverage_bound = q * coverage_step**probes_count
    rank_bound = ((3**r - 1)//2) * rank_step**shifts_count
    while coverage_bound > half_budget:
        probes_count += 1
        coverage_bound *= coverage_step
    while rank_bound > half_budget:
        shifts_count += 1
        rank_bound *= rank_step
    # Rounded upward for the compact diagnostic; exact tails establish it.
    failure_bound = math.nextafter(float(coverage_bound + rank_bound), math.inf)
    query_bound = 1 + probes_count + shifts_count * (1 + probes_count)
    sample = lambda: tuple(rng.randrange(3) for _ in range(k))
    f0 = tuple(evaluate((0,) * k))
    if len(f0) != r:
        raise ValueError("Public output dimension disagrees with k-d")
    probes = [sample() for _ in range(probes_count)]
    values = [tuple(evaluate(x)) for x in probes]
    shifts, increments = [], []
    for attempt in range(shifts_count):
        h = sample()
        increment = _sub(evaluate(h), f0)
        if _rank(increments + [increment]) == len(increments):
            continue
        if not all(_sub(evaluate(_add(x, h)), fx) == increment
                   for x, fx in zip(probes, values)):
            continue
        shifts.append(h)
        increments.append(increment)
        if len(increments) == r:
            return {"k": k, "r": r, "f0": f0,
                    "shifts": shifts, "increments": increments,
                    "probe_count": probes_count, "shift_limit": shifts_count,
                    "shifts_tried": attempt + 1, "query_bound": query_bound,
                    "failure_bound": failure_bound}
    return None


def invert_target(evaluate, basis, target):
    """Return a verified target preimage, or None if verification fails."""
    coeff = _solve_columns(basis["increments"], _sub(target, basis["f0"]))
    if coeff is None:
        return None
    x = tuple(sum(c * h[i] for c, h in zip(coeff, basis["shifts"])) % 3
              for i in range(basis["k"]))
    return x if tuple(evaluate(x)) == tuple(target) else None


def project_to_target_fiber(evaluate, basis, target, z):
    """Return z+H(target-f(z)), checking the final public predicate.

    With a sound basis, H is a linear section of the public increment
    map, so this projection is exactly 3^r-to-1 onto the target fiber.
    An invalid sampled basis can yield None, never an unverified point.
    """
    coeff = _solve_columns(basis["increments"], _sub(target, evaluate(z)))
    if coeff is None:
        return None
    out = tuple((z[i] + sum(c * h[i] for c, h in zip(coeff, basis["shifts"]))) % 3
                for i in range(basis["k"]))
    return out if tuple(evaluate(out)) == tuple(target) else None


def sample_target_fiber(evaluate, basis, target, rng):
    """Uniformly sample the fiber when the recovered basis is sound."""
    z = tuple(rng.randrange(3) for _ in range(basis["k"]))
    return project_to_target_fiber(evaluate, basis, target, z)
