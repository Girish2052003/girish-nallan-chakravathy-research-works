# Single-recipient seeded matrix profile

The encapsulation key is a 32-byte public seed followed by the packed syndrome columns. The decapsulation key is the same seed followed by the packed private signed supports. The receiver regenerates the matrix and the syndrome columns for FO re-encryption. Each encapsulation and decapsulation therefore depends on the same authenticated public matrix without transmitting it in full.

## Expansion and protocol binding

Let $A$ have $d$ rows and $m$ columns. For matrix sampling slack $s$, each row takes $D=8(\lceil m\log_{256}3\rceil+\lceil s/8\rceil)$ random bits. Interpret these bits as a big-endian integer, reduce modulo $C=3^m$, and unpack the result into $m$ ternary entries, most significant trit first. The implementation uses a separate framed SHAKE256 domain for row sampling. Each input binds the complete base-suite configuration, the seeded-profile identifier, $s$, the public seed, and the canonical row number. Each of the two FO hashes binds the seeded profile, the seed and the reconstructed full public matrix. This also distinguishes two wire keys whose seeds happen to generate the same matrix. The nonce and body use the existing FO ciphertext layout.

## Reduction for the seeded profile

Model row sampling as an independent public random oracle $T$ with $D$ output bits on each row address, available in superposition, in addition to independent FO oracles $G,H$. Classical-only access is a special case. The matrix seed is public. The single-recipient theorem imposes no computational assumption on hiding it.

**Theorem.** Suppose the two iid-matrix decisional bounds in the [base proof](BASE_PROOF.md) hold with the added independent oracle resources and simulation costs below. For the implemented PKE's two-message raw IND-CPA gap, a valid bound is

$$\epsilon_{\rm seed}\le\min\{1,\ 2t\epsilon_1+2\epsilon_2+2\nu+2d\,2^{-s}\},$$

where $\nu$ bounds the total variation of the separate encryption tape from ideal encryption coins. The [FO theorem](CCA_PROOF.md) applies with this base bound, the existing message and nonce lengths, and the same perfect correctness and spread. Concrete SHAKE256 instantiates the independent ideal oracles heuristically.

**Proof.** Choose the target seed before invoking the adversary. Put $Q=2^D$. Compare the actual oracle to one that assigns a uniform ternary rank $a$ to each of the $d$ target rows, then samples the oracle output uniformly among $a,a+C,a+2C,\ldots<Q$. Every other address keeps its original independent random output. If $e=Q\bmod C$, the single-row statistical distance from a uniform $D$-bit string is precisely $e(C-e)/(QC)$. Indeed, in each residue class both laws are uniform conditioned on membership, while $e$ classes have $\lceil Q/C\rceil$ representatives and the rest have $\lfloor Q/C\rfloor$. This distance is at most $C/Q\le 2^{-s}$. By coupling all $d$ rows, the probability that the two *entire oracle tables* differ is at most $d2^{-s}$. Any quantum distinguisher's acceptance probabilities in these games consequently differ by at most that amount, irrespective of query count. The raw gap uses two message experiments or twice the excess guessing probability, giving the displayed factor of two. If an ideal XOF is exposed, keep a fresh independent suffix after each lifted prefix so all output lengths agree.

In the lifted game the $d$ target ranks are exactly iid uniform. Run the usual hybrid embedding: for the public-key syndrome experiment build $A$ using the prescribed embedded columns and sample the complementary columns. In the noisy-codeword experiment use the first $k$ rows supplied by that challenge for the $A$ portion and sample the other rows. In both cases all $d$ rows of $A$ are marginally iid. Once $A$ is available, sample the $d$ conditional lifts above independently and answer target row queries from them. Forward all other addresses to an independent oracle. This rule is fixed before the adversary starts and has exactly the lifted game's joint distribution with the key and candidate challenge. The simulator can implement it on superpositions by reversible comparison, lookup and uncomputation. It pays for $d$ lifts and the reversible lookups at the distinguisher's query lengths. The seed field, suite and all public expansions can be supplied to the adversary and to the FO reduction. The remaining hybrid transitions incur $2t\epsilon_1+2\epsilon_2$ in raw gap as before, plus $2\nu$ for encryption sampling. This proves the bound.

The statistical comparison changes the joint law of the public seed, its entire oracle slice and all other addresses coherently. No step replaces a short, visible standard-model PRG seed by an independent iid matrix. The conclusion averages over an honestly generated single recipient with access to the separate ideal oracle. Reuse, multiple recipients and a concrete cost bound for quantum random-decoding at these dimensions require their own analyses.

## Serialized sizes

The three rows use $s=2b+192$ bits, which equals the default message length plus 64 bits in these layouts. Counts below are exact bytes. The costs and the unestablished concrete security levels of the [parameter experiments](PARAMETERS.md) still apply.

| Target label $b$ | Sender public key | Receiver private key | Ciphertext |
|---:|---:|---:|---:|
| 128 | 12,285,243,257 | 17,337,006 | 3,348,787 |
| 192 | 53,618,422,002 | 46,446,645 | 8,567,191 |
| 256 | 126,797,581,733 | 84,459,598 | 15,210,996 |

The formulas are $32+\lceil dt\log_{256}3\rceil$ public bytes and $32+S$ private bytes for the private-support width $S$. Each shared key has 32 bytes. Expansion still processes $dm$ trits per full regeneration. The reference materializes the matrix, and the table describes wire lengths rather than measured execution at target dimensions. [Implementation](seeded_matrix.py) and [finite checks](test_seeded_matrix.py).
