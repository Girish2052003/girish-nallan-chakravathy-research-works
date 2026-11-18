"""Raw ML-KEM adapter for the Node WebCrypto/OpenSSL provider."""
from pathlib import Path
import subprocess


_PROVIDER = Path(__file__).with_name("reviewed_provider.mjs")
_WIDTHS = {
    512: (800, 768),
    768: (1184, 1088),
    1024: (1568, 1568),
}


class MLKEM:
    """API returns (public, secret_seed) and (ciphertext, shared_key)."""

    private_bytes = 64
    key_bytes = 32

    def __init__(self, profile):
        if type(profile) is not int or profile not in _WIDTHS:
            raise ValueError("expected an ML-KEM profile of 512, 768 or 1024")
        self.profile = profile
        self.public_bytes, self.ciphertext_bytes = _WIDTHS[profile]
        self.suite = f"ML-KEM-{profile}".encode("ascii")

    def _run(self, operation, data, expected_size):
        result = subprocess.run(
            ["node", str(_PROVIDER), operation, str(self.profile)],
            input=data, capture_output=True, check=False,
        )
        if result.returncode == 2:
            raise ValueError("the ML-KEM provider rejected the key encoding")
        if result.returncode or len(result.stdout) != expected_size:
            raise RuntimeError(f"Node WebCrypto ML-KEM {operation} failed")
        return result.stdout

    def keygen(self):
        result = self._run("keygen", b"", self.public_bytes + self.private_bytes)
        return result[:self.public_bytes], result[self.public_bytes:]

    def public_from_private(self, private):
        self._check_private(private)
        return self._run("public", private, self.public_bytes)

    def encaps(self, public):
        if type(public) is not bytes or len(public) != self.public_bytes:
            raise ValueError("incorrect ML-KEM public key length")
        result = self._run("encaps", public, self.ciphertext_bytes + self.key_bytes)
        return result[:self.ciphertext_bytes], result[self.ciphertext_bytes:]

    def decaps(self, private, ciphertext):
        self._check_private(private)
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        return self._run("decaps", private + ciphertext, self.key_bytes)

    def _check_private(self, private):
        if type(private) is not bytes or len(private) != self.private_bytes:
            raise ValueError("incorrect ML-KEM private seed length")
