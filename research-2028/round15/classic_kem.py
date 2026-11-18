"""Classic McEliece component using the system libmceliece.so.1 implementation.

Widths are those of the byte-aligned, unconfirmed Classic McEliece suites.
The Linux C ABI entries correspond to the public aliases in <mceliece.h>.
"""
import ctypes
from functools import cache


# Name, public-key bytes, private-key bytes, ciphertext bytes.
_PROFILES = {
    128: ("348864", 261120, 6492, 96),
    192: ("460896", 524160, 13608, 156),
    256: ("6688128", 1044992, 13932, 208),
}


@cache
def _library():
    try:
        return ctypes.CDLL("libmceliece.so.1")
    except OSError as exc:
        raise RuntimeError("Install the Linux libmceliece1 package and its dependencies") from exc


def _check_input(value, width, name):
    if type(value) is not bytes or len(value) != width:
        raise ValueError(f"invalid {name} type or byte length")


class ClassicMcEliece:
    """KeyGen, Encaps and Decaps for one of three fixed native-library suites."""
    key_bytes = 32

    def __init__(self, target):
        if type(target) is not int or target not in _PROFILES:
            raise ValueError("choose 128, 192 or 256 as the research layout label")
        name, self.public_bytes, self.private_bytes, self.ciphertext_bytes = _PROFILES[target]
        self.suite = ("Classic-McEliece/" + name + "/20221023").encode("ascii")
        lib = _library()
        prefix = "mceliece_kem_" + name
        self._keypair = getattr(lib, prefix + "_keypair")
        self._enc = getattr(lib, prefix + "_enc")
        self._dec = getattr(lib, prefix + "_dec")
        writable = ctypes.POINTER(ctypes.c_char)
        readonly = ctypes.c_char_p
        self._keypair.argtypes = (writable, writable)
        self._keypair.restype = None
        self._enc.argtypes = (writable, writable, readonly)
        self._enc.restype = ctypes.c_int
        self._dec.argtypes = (writable, readonly, readonly)
        self._dec.restype = ctypes.c_int

    def keygen(self):
        public = ctypes.create_string_buffer(self.public_bytes)
        private = ctypes.create_string_buffer(self.private_bytes)
        self._keypair(public, private)
        return public.raw, private.raw

    def encaps(self, public):
        _check_input(public, self.public_bytes, "Classic McEliece public key")
        ciphertext = ctypes.create_string_buffer(self.ciphertext_bytes)
        shared = ctypes.create_string_buffer(self.key_bytes)
        if self._enc(ciphertext, shared, public) != 0:
            raise ValueError("Classic McEliece provider rejected the public key")
        return ciphertext.raw, shared.raw

    def decaps(self, private, ciphertext):
        _check_input(private, self.private_bytes, "Classic McEliece private key")
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        shared = ctypes.create_string_buffer(self.key_bytes)
        if self._dec(shared, ciphertext, private) != 0:
            return None
        return shared.raw


def code_based_hybrid(target):
    """Combine Classic McEliece and the compact SG-DIFRA component."""
    from hybrid_kem import ParallelKEM
    return ParallelKEM(ClassicMcEliece(target), cache_public=True)
