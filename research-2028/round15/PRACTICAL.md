# Standard ML-KEM provider

The `MLKEM` adapter runs all three FIPS 203 parameter sets using Node's native WebCrypto ML-KEM implementation. It supplies a runnable, compact reference and can provide the independently analyzed component of a combined KEM. ML-KEM uses module lattices. Its confidentiality assumption is distinct from the ternary SG-DIFRA decoding assumptions.

| Suite | NIST category | Public key | Stored private seed | FIPS 203 expanded private key | Ciphertext | Shared key |
|---|---:|---:|---:|---:|---:|---:|
| ML-KEM-512 | 1 | 800 | 64 | 1,632 | 768 | 32 |
| ML-KEM-768 | 3 | 1,184 | 64 | 2,400 | 1,088 | 32 |
| ML-KEM-1024 | 5 | 1,568 | 64 | 3,168 | 1,568 | 32 |

All widths are bytes. The 64-byte private serialization is the ordered pair of secret 32-byte seeds $d,z$. Import regenerates the private key. FIPS 203 Table 3 specifies the expanded private-key widths. The test suite generated keys at full size, serialized and reimported them, and ran an actual encapsulation and decapsulation for each profile. [FIPS 203, §§3.3, 7 and 8](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)

**Confidentiality and agreement.** FIPS 203 describes ML-KEM as believed to provide IND-CCA2 security under its module-lattice assumptions and cryptographic transformation. The CPA game follows by allowing the adversary zero decapsulation queries. A fixed-width invalid ciphertext produces a pseudorandom fallback secret by implicit rejection. Syntactically incorrect lengths yield a distinct framing error. FIPS 203 Table 1 gives an estimated honest decapsulation failure probability of $2^{-138.8}$, $2^{-164.8}$ and $2^{-174.8}$ for the three profiles respectively, under its hash/XOF modeling assumptions. NIST's categories express comparison goals. They supply no exact classical or quantum work bound of $2^{191}$ operations. The Python adapter and its Node bridge have not undergone formal certification or independent implementation audit. [FIPS 203, §§3.1 and 8](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) · [NIST SP 800-227](https://csrc.nist.gov/pubs/sp/800/227/final)

## Run an exchange

Use Node v24.22.3 and Python 3. The tested Node binary reported OpenSSL 3.5.9. The JavaScript module uses only `node:crypto`, `node:fs` and `node:url`. It delegates key generation, public-key derivation, key parsing, encapsulation, decapsulation and random sampling to Node's provider. The Python adapter exchanges bytes with that process using stdin/stdout pipes. The synchronous Python subprocess overhead is part of this research interface; applications using JavaScript can import the async functions directly. [Node's version-pinned WebCrypto API](https://github.com/nodejs/node/blob/v24.22.3/doc/api/webcrypto.md) · [OpenSSL ML-KEM key types](https://docs.openssl.org/3.5/man7/EVP_PKEY-ML-KEM/)

From this directory:

```sh
python3 - <<'PY'
from reviewed_kem import MLKEM
kem = MLKEM(768)
public, private_seed = kem.keygen()
ciphertext, sender_key = kem.encaps(public)
assert kem.decaps(private_seed, ciphertext) == sender_key
print(len(public), len(private_seed), len(ciphertext), len(sender_key))
PY
python3 -m unittest discover -s . -p 'test_reviewed_kem.py' -v
```

The example prints `1184 64 1088 32`. The shared secret is not printed. The suite identifier is selected out of band and the recipient public key must be authenticated by its protocol.

## Independent verification data

The [offline fixtures](reviewed_vectors.json) contain two test cases per parameter set. First, `d || z` from NIST ACVP key-generation cases 1, 26 and 51 must produce the SHA-256 digest of the published encapsulation key. Second, seed and valid ciphertext from the general FIPS 203 group of Wycheproof case 2 must give its 32-byte expected secret by decapsulation. The fixture encodes the published ciphertext in base64 to keep the six cases compact. The tests also check the FIPS 203 fallback formula, invalid public-key rejection and actual encapsulation with fresh provider randomness. [NIST ACVP source, pinned revision](https://github.com/usnistgov/ACVP-Server/blob/ad33b3d9504491767f1aa76382464f3b3fa2359e/gen-val/json-files/ML-KEM-keyGen-FIPS203/internalProjection.json) · [Wycheproof vectors, pinned revision](https://github.com/C2SP/wycheproof/tree/3fa63dd0344abb611f1fb1d77e119938603ea230/testvectors_v1)

A separate interoperability run used the PQClean-backed Python package `pqcrypto==0.3.4`. For each of the three ACVP seed/expanded-key pairs, the Node provider recovered a PQClean encapsulation, and PQClean recovered a Node encapsulation. The portable known-answer suite requires neither PQClean nor network access.
