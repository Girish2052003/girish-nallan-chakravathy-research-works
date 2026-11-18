"""Exact capacity and serialization accounting for the Round 11 public control."""

from dataclasses import dataclass
import json


CAPACITY_TARGETS = (128, 192, 256)
SHARED_KEY_BYTES = 32


@dataclass(frozen=True)
class ProfileSize:
    capacity_target_bits: int
    trits: int
    domain_size: int
    packed_vector_bytes: int

    @property
    def mean_blind_guesses(self):
        """Uniform preimage, enumerated once in fixed order until it is found."""
        return (self.domain_size + 1) // 2

    def as_record(self):
        return {
            "capacity_target_bits": self.capacity_target_bits,
            "trits": self.trits,
            "domain_size": self.domain_size,
            "mean_blind_guesses": self.mean_blind_guesses,
            "control_public_key_bytes": self.packed_vector_bytes,
            "control_private_key_bytes": self.packed_vector_bytes,
            "control_ciphertext_bytes": self.packed_vector_bytes,
            "shared_key_bytes": SHARED_KEY_BYTES,
            "control_has_public_inverse": True,
        }


def profile_size(capacity_target_bits):
    """Find the smallest n with 3**n >= 2**target using integer comparisons."""
    if type(capacity_target_bits) is not int or capacity_target_bits < 1:
        raise ValueError("capacity target must be a positive integer")
    required_size = 1 << capacity_target_bits
    trits = 0
    domain_size = 1
    while domain_size < required_size:
        trits += 1
        domain_size *= 3
    width = ((domain_size - 1).bit_length() + 7) // 8
    return ProfileSize(capacity_target_bits, trits, domain_size, width)


if __name__ == "__main__":
    print(json.dumps([profile_size(bits).as_record() for bits in CAPACITY_TARGETS], indent=2))
