"""Exact size comparisons and finite ternary outer-code lower bounds."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round14"))
from parameters import illustration, mixed_rank_bytes
from differential_pke import Params
from projected_kem import ProjectedKEM, research_profile


def outer_length_floor(bits, errors):
    """Singleton and all prefix shortenings of the ternary Plotkin bound."""
    if type(bits) is not int or bits < 1 or type(errors) is not int or errors < 0:
        raise ValueError("positive message width and nonnegative radius required")
    messages = 1 << bits
    distance = 2 * errors + 1
    prefix = 0
    prefixes = 1
    floor = 0
    while prefixes <= messages:
        fiber = (messages + prefixes - 1) // prefixes
        numerator = 3 * distance * (fiber - 1)
        denominator = 2 * fiber
        floor = max(floor, prefix + (numerator + denominator - 1) // denominator)
        prefix += 1
        prefixes *= 3
    # 2**bits cannot be a power of 3 when bits > 0, so prefix is ceil(log_3 M).
    return max(floor, prefix + distance - 1)


def limits_for_profile(target):
    kem = research_profile(target)
    source = kem.source
    t_floor = outer_length_floor(source.bits, source.z)
    r = source.m - (source.t - 1) * source.w
    minimum_base = r + (t_floor - 1) * source.w
    return dict(t=t_floor, r=r, public=32 + mixed_rank_bytes(source.d*t_floor),
                ciphertext=kem.nonce_bytes + mixed_rank_bytes(minimum_base + t_floor))


def rebalanced_example(target):
    """Change the source decoding dimensions; the original hypotheses no longer suffice."""
    previous = illustration(target)
    checks = research_profile(target).t
    base = 2 * checks * previous.w
    source_base = base + (previous.t - checks) * previous.w
    source = Params(previous.bits, base//3, previous.n, source_base, previous.w,
                    previous.z, previous.slack, outer="rs")
    return ProjectedKEM(source, previous.nonce_bytes)


def engineering_example():
    """A full 256-bit-message experiment with deliberately small check weight."""
    source = Params(bits=256, h=512, n=8, m=6440, w=4, z=64, slack=192, outer="rs")
    return ProjectedKEM(source, nonce_bytes=64)


if __name__ == "__main__":
    for target in (128, 192, 256):
        compact = research_profile(target)
        example = rebalanced_example(target)
        print(target, "projected", compact.public_bytes, compact.private_bytes,
              compact.ciphertext_bytes, "outer floor", limits_for_profile(target),
              "rebalanced", example.public_bytes, example.private_bytes, example.ciphertext_bytes)
