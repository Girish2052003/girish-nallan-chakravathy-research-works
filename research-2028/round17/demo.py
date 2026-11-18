"""Run a small SG-DIFRA exchange, or print the registered research sizes."""
import argparse
from time import perf_counter

from systematic_kem import SystematicKEM, research_profile
from matched_kem import MatchedKEM


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--sizes', action='store_true',
                       help='print fixed serialized sizes without generating the large keys')
    modes.add_argument('--timings', action='store_true',
                       help='time three fresh exchanges on a small-weight, 512-bit message fixture')
    args = parser.parse_args()
    if args.sizes:
        print('target  public_B  private_B  ciphertext_B  nonce_B')
        for target in (128, 192, 256):
            kem = research_profile(target)
            print(target, kem.public_bytes, kem.private_bytes,
                  kem.ciphertext_bytes, kem.nonce_bytes)
        return

    if args.timings:
        kem = SystematicKEM(MatchedKEM(512, 4, 2, slack=320, nonce_bytes=16), nonce_bytes=0)
        print('Engineering fixture, weight 2, timings in seconds')
        print('key_generation  encapsulation  decapsulation')
        for _ in range(3):
            start = perf_counter()
            public, private = kem.keygen()
            keyed = perf_counter()
            ciphertext, key = kem.encaps(public)
            sent = perf_counter()
            received = kem.decaps(private, ciphertext)
            done = perf_counter()
            if received != key:
                raise RuntimeError('full-radius key agreement failed')
            print(f'{keyed-start:.4f}  {sent-keyed:.4f}  {done-sent:.4f}')
        print(f'Serialized bytes (public, private, ciphertext, shared key): '
              f'{len(public)}, {len(private)}, {len(ciphertext)}, {len(key)}')
        return

    # The full-radius fixture makes this fresh exchange correct for every tape.
    kem = SystematicKEM(MatchedKEM(8, 1, 1, nonce_bytes=4), nonce_bytes=0)
    public, private = kem.keygen()
    ciphertext, sender_key = kem.encaps(public)
    receiver_key = kem.decaps(private, ciphertext)
    if receiver_key != sender_key:
        raise RuntimeError('full-radius key agreement failed')
    print('Small full-radius exchange with fresh keys')
    print(f'Public key {len(public)} B, private key {len(private)} B, '
          f'ciphertext {len(ciphertext)} B')
    print(f'Sender and receiver agreed on a {len(sender_key)}-byte key.')


if __name__ == '__main__':
    main()
