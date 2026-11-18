"""Run the selected end-to-end KEM and report public sizes and agreement."""
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scheme", choices=("code-hybrid", "ml-hybrid", "ml-kem"))
    parser.add_argument("target", type=int, choices=(128, 192, 256))
    args = parser.parse_args()
    if args.scheme == "code-hybrid":
        from classic_kem import code_based_hybrid
        kem = code_based_hybrid(args.target)
    else:
        ml_profile = {128: 512, 192: 768, 256: 1024}[args.target]
        if args.scheme == "ml-hybrid":
            from hybrid_kem import HybridKEM
            kem = HybridKEM(ml_profile)
        else:
            from reviewed_kem import MLKEM
            kem = MLKEM(ml_profile)

    public, private = kem.keygen()
    ciphertext, sender = kem.encaps(public)
    agreed = kem.decaps(private, ciphertext) == sender
    print(json.dumps(dict(scheme=args.scheme, layout=args.target, public_bytes=len(public),
                          private_bytes=len(private), ciphertext_bytes=len(ciphertext),
                          shared_bytes=len(sender), agreed=agreed)))
    if not agreed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
