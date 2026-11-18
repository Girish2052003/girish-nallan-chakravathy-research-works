# Shared-matrix public-key encoding

The setup authority samples a matrix $A$ uniformly from all ternary $d$-by-$m$ matrices. Both parties receive the same authenticated matrix and suite parameters. The reference packs the matrix into one base-three integer, most significant trit first, in row-major order. Independently rounding each of two transmitted blocks to whole bytes can cost one byte compared with packing both jointly.

Alice samples the usual signed disjoint supports and sends only the $d$-by-$t$ matrix of check columns. Bob interleaves its rows with the public setup rows, reconstructing the full canonical encapsulation key. For decapsulation Alice independently reconstructs these same columns from her private supports and her copy of the setup. Consequently her per-user secret consists entirely of the signed support ranks. Provisioning and authenticating the setup is an external cost. Private storage trades against recomputation during decapsulation. Neither party can discard access to the matrix.

**Single-user equivalence.** In a fresh honestly generated setup, the joint distribution of the split key is precisely that of the two blocks in the original public matrix. A reduction splits its original challenge public key to simulate the setup and recipient key for the adversary. The adversary sees both simultaneously, or can perform local preprocessing on the matrix before reading the recipient key. It forwards the unchanged challenge ciphertext and permitted decapsulation queries between games. The full hash input contains the original authenticated public matrix and syndrome columns, so every ciphertext, shared key, and rejection has the original distribution. The same argument in the opposite direction recombines the blocks. Both transformations take time linear in the matrix representation apart from base-conversion costs. The single-user IND-CPA and IND-CCA advantages therefore coincide up to encoding time. This experiment averages over the honest setup; a malicious setup or a security claim conditioned on every particular matrix would require another argument.

The adapter uses the full KEM’s suite identifier and ciphertext format. It is a reversible public-key encoding with external setup; the interface distinguishes the setup and compact key arguments. The entire matrix stays public. The theorem covers the single-user security game. No concrete multi-user, amortized preprocessing or short-seed security estimate is asserted here.

| Layout label | Shared matrix bytes | Per-user public bytes | Per-user secret bytes | Ciphertext bytes |
|---|---:|---:|---:|---:|
| 128 target | 18,870,133,592,348 | 12,285,243,225 | 17,336,974 | 3,348,787 |
| 192 target | 123,536,844,217,338 | 53,618,421,970 | 46,446,613 | 8,567,191 |
| 256 target | 389,522,170,985,138 | 126,797,581,701 | 84,459,566 | 15,210,996 |

These counts use the polynomial-evaluation outer code in [the parameter analysis](PARAMETERS.md). A distinct authenticated channel or cached setup accounts for the second column. All wire counts exclude external framing, signatures, and protocol suite identifiers. If every recipient has to obtain a fresh copy of the setup, the first two size columns both contribute to initial per-recipient public data. Shared keys occupy 32 bytes in every layout.

The [implementation](matrix_setup.py) supplies `generate_setup` and `SharedMatrixKEM`. [Tests](test_matrix_setup.py) enumerate all nine setup matrices and both supports at a tiny parameter point, check both wire formats against each other, and exercise rejection.
