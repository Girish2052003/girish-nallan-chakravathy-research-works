# Parameter budgets and wire sizes

The 128, 192 and 256 rows are design targets. The tables show what the scheme costs under explicit choices and how strong its decoding assumptions would have to be. The smallest row already has an 18.88 TB public key (decimal units). No concrete security level has been established for any row.

## Wire convention

Parameters and the outer-code identifier are agreed out of band. All table entries for serialized objects are **bytes**. Let $B(a)=\lceil\log_{256} a\rceil$ for $a\ge1$ and $W(v,j)=\binom{v}{j}2^j$. Let $t$ be the outer-code length in trits, $N=m+t$, and $d=h+n(n+1)/2$. Write $u$ for the transmitted nonce width in bytes and $\sigma$ for the body sampler's slack in bits.

| Object | Exact reference-format width |
|---|---:|
| Encapsulation key, one row-major ternary matrix | $B(3^{dN})$ |
| Private part, ordered signed supports | $S=\sum_{i=0}^{t-1}B(W(m-iw,w))$ |
| Standalone decapsulation key | $B(3^{dN})+S$ |
| PKE body | $B(3^N)$ |
| KEM ciphertext | $u+B(3^N)$ |
| Internal PKE randomness tape per encryption | $B(3^{h+n}W(N,z))+\lceil\sigma/8\rceil$ |
| Shared key | 32 |

The dense matrix and body each use one canonical base-three rank. Their widths are minimal for fixed-width, lossless serialization of all ternary strings of the corresponding dimension. The honest public matrices have additional structure, so this observation proves no lower bound on the size of every possible public-key representation. Each signed support has its own fixed-width rank on the remaining positions. The standalone recipient key includes the public matrix because FO re-encryption requires it. The internal tape is expanded locally by the hash function. The KEM ciphertext contains only the nonce and body.

For an executable scale check, take an eight-bit message, $h=3,n=2,m=80,w=z=2$, 32 slack bits, an eight-byte nonce and RS encoding. Here $t=14$, $d=6$ and $N=94$. The dense format has a 112-byte public key, 28 bytes of secret supports, a 140-byte standalone decapsulation key, a 27-byte ciphertext and a seven-byte body tape. The entire message space has only 256 elements. This tiny row exercises the wire format and decoder.

## Illustrative choices

For a row indexed by $b$, set message length $\ell=2b+128$, nonce bits $8u=4b+128$, sampling slack $\sigma=b+128$, $n=b$, $w=z=6b$, $m=2tw$ and $h=\lfloor m/3\rfloor$. These choices give the disjoint supports half the original positions. They leave a residual key-decoding challenge of length $r=m-(t-1)w$ with $d<r$, and a noisy-codeword challenge of dimension $h<N$. Choosing $w,z$, or dimensions proportional to $b$ does not establish exponential security. The ciphertext-noise experiment samples its generator iid, as in the base proof.

The Reed–Solomon code uses the smallest $s$ such that $k=\lceil \ell/\log_2(3^s)\rceil$ and $L=k+2z\le3^s$; its length in trits is $t=sL$. Its distance $2z+1$ permits perfect correction of $z$ residual trit errors. The code and evaluation points are public.

| Target $b$ | Message bits | Nonce bytes | $w=z$ | RS $(s,k,L)$ | $t$ | $m$ | $h$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 128 | 384 | 80 | 768 | (7, 35, 1571) | 10,997 | 16,891,392 | 5,630,464 |
| 192 | 512 | 112 | 1,152 | (8, 41, 2345) | 18,760 | 43,223,040 | 14,407,680 |
| 256 | 640 | 144 | 1,536 | (8, 51, 3123) | 24,984 | 76,750,848 | 25,583,616 |

| Target $b$ | Key-syndrome rows $d$ | Remaining key coordinates $r$ | Ciphertext length $N$ in trits | Noise-syndrome rows $N-h$ |
|---:|---:|---:|---:|---:|
| 128 | 5,638,720 | 8,446,464 | 16,902,389 | 11,271,925 |
| 192 | 14,426,208 | 21,612,672 | 43,241,800 | 28,834,120 |
| 256 | 25,616,512 | 38,376,960 | 76,775,832 | 51,192,216 |

One elementary geometry check uses the fraction of weight-$j$ supports contained in a fixed set of $v$ out of $a$ positions, $p(a,v,j)=\binom vj/\binom aj$. For the key experiment take $(a,v,j)=(r,d,w)$, and for the noise syndrome take $(N,N-h,z)$. The respective values of $-\log_2 p$ (rounded) are 447.75 / 448.90, 671.85 / 673.53 and 895.77 / 898.15 for the three rows. These values describe support-containment probabilities in a basic information-set calculation. They supply no lower bound on the cost of distinguishing either distribution. The complete proof would need upper bounds on all adversaries' distinguishing advantages.

| Target $b$ | Public key | Private supports | Standalone private key | KEM ciphertext | Internal body tape |
|---:|---:|---:|---:|---:|---:|
| 128 | 18,882,418,835,572 | 17,336,974 | 18,882,436,172,546 | 3,348,787 | 1,117,186 |
| 192 | 123,590,462,639,307 | 46,446,613 | 123,590,509,085,920 | 8,567,191 | 2,857,072 |
| 256 | 389,648,968,566,839 | 84,459,566 | 389,649,053,026,405 | 15,210,996 | 5,072,198 |

## Effect of the outer code and shared parameters

As a comparison, repeat each message bit $2z+1$ times, and recompute $t,m,h,d,N$ from the same rules. The resulting public keys appear below. The RS width saving includes its consequent reduction in $m$ and $h$. A distinct setup variant samples the iid $d\times m$ matrix $A$ once as common public randomness. In a single-user experiment, providing that matrix separately leaves its joint distribution with the rest of the public key unchanged. Counting the shared matrix separately then leaves $d\times t$ trits per public key. Its delivery and storage still matter. The reference implementation uses a self-contained key. Replacing $A$ by the output of a short public seed would require a new argument for the resulting distribution. Multi-user reuse likewise requires its own analysis.

| Target $b$ | Repetition baseline public key | Shared $A$ in RS setup | Per-key RS public payload with shared $A$ |
|---:|---:|---:|---:|
| 128 | 54,311,885,724,562,578 | 18,870,133,592,348 | 12,285,243,225 |
| 192 | 488,485,653,736,732,306 | 123,536,844,217,338 | 53,618,421,970 |
| 256 | 2,411,480,107,537,889,529 | 389,522,170,985,138 | 126,797,581,701 |

The byte counts use integer rank cardinalities and outward-rounded logarithm bounds. They require no allocation of a full matrix. Small reference instances exercise the actual serializer. No generation time, memory or bandwidth measurement at a target row is claimed.

## Per-recipient seed format

A separate variant derives the base matrix per recipient from a 32-byte public seed and a dedicated hash domain. The encapsulation key consists of that seed followed by the $d\times t$ syndrome matrix. The decapsulation key consists of the same seed followed by the secret supports. The holder can recompute the public syndrome columns from the seed and the supports during re-encryption. Both savings trade stored or transmitted bytes for computation. The expanded matrix still has $dm$ entries. The reference dense and seeded formats have the same ciphertext width for a given nonce width.

| Target $b$ | Matrix slack in bits | Seeded public key | Seeded standalone private key | KEM ciphertext |
|---:|---:|---:|---:|---:|
| 128 | 448 | 12,285,243,257 | 17,337,006 | 3,348,787 |
| 192 | 576 | 53,618,422,002 | 46,446,645 | 8,567,191 |
| 256 | 704 | 126,797,581,733 | 84,459,598 | 15,210,996 |

This proof models the matrix expander as an independent random oracle. With $2b+192$ excess bits per row the distance from iid rows in the single-key comparison is at most $\delta_A=d2^{-(2b+192)}$. For raw two-message gaps include the corresponding $2\delta_A$ in the base-PKE bound, with the oracle simulation costs specified by the seeded proof. A fixed deployed SHAKE implementation requires the additional concrete-hash modeling assumption. Compression alone establishes no security rating.

The [private-seed storage variant](PRIVATE_SEED.md) further reduces standalone decapsulation keys to 80, 96 and 112 bytes. It regenerates the supports using a separate secret-seed expansion and adds its own quantified security term.

## What a concrete security proof would require

For an illustrative query budget $Q=2^b$, suppose $d_Q\le q_G+q_H\le Q$ and $q_D\le Q$, where $d_Q$ is quantum hash depth. Substituting the table's message and nonce lengths into the single-user raw-gap bound shows that its message and spread terms total at most $272\cdot 2^{-64}$. The base-PKE term is bounded by $1/4$ if $\epsilon\le 2^{-b-11}$ because $8\sqrt{2Q\epsilon}\le1/4$. The optional prechallenge correction adds at most $2Q/2^\ell$. These numerical choices illustrate a conditional constant-advantage exclusion. A different desired advantage calls for a different budget.

In particular, sufficient bounds on the two **iid-matrix** decisional advantages would be $\epsilon_1\le 2^{-b-14}/t$ for the signed private-check syndrome and $\epsilon_2\le 2^{-b-14}$ for the noisy codeword. Together with $\nu\le 2^{-(b+128)}$ for the body sampler they give $\epsilon\le 2t\epsilon_1+2\epsilon_2+2\nu\le2^{-b-11}$. A formulation via a full-rank noise syndrome must account for rank conditioning as in the base proof. These inequalities need to hold for the reductions' actual time and quantum memory, including hash simulation. The code dimensions and a count of hash queries alone do not bound either advantage. For example, the 192 row's budget includes $2^{191}$ queries, but the displayed inequalities provide no empirical or unconditional $2^{191}$ work estimate.

The proof applies to one honestly generated recipient. Extending an estimate to many public keys or target ciphertexts requires stating that game, its number of targets, and the resulting loss. Treating quantum query counts as classical operations or NIST security categories would also require a separate cost model. See the [base proof](BASE_PROOF.md), [FO theorem and security model](CCA_PROOF.md), and [NIST security evaluation criteria](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/evaluation-criteria/security-%28evaluation-criteria%29).

Recompute the tables from this directory with `python3 parameters.py`.

## A sufficient condition at the requested $2^{191}$ budget

Consider the 192 target in its [two-seed private format](PRIVATE_SEED.md), a single honestly generated recipient, and the four separately framed ideal hash domains. A challenger flips a fair coin and gives the adversary either the genuine shared key or an independent uniform key. It also supplies the challenge ciphertext. Write $\Delta$ for the absolute difference in acceptance probabilities between those cases. The adversary's excess chance of guessing the coin over one half is $\Delta/2$. Adaptive classical decapsulation is allowed under the [CCA game's challenge restriction](CCA_PROOF.md). Setting the decapsulation budget to zero gives the CPA guarantee.

Set $Q=2^{191}$. Allow $q_G+q_H\le Q$, $q_D\le Q$, and $q_{\rm priv}\le Q$ for the FO hashes, decapsulations, and private-seed hash queries respectively. Count quantum matrix-oracle queries, all computation, and memory in the resources of the reductions. The next two rows give **sufficient assumptions**, each imposed on both decoding distinguishing gaps $\epsilon_1,\epsilon_2$ for the generated distributions at those resources.

| Hypothetical upper bound on each decoding gap | Consequence for guessing the fair coin |
|---|---|
| $2^{-224}$ | Success below $51.6\%$ |
| $2^{-280}$ | Success below $1/2+2^{-33}$ |

**Derivation.** Write $D=14{,}426{,}208$ for matrix rows and $t=18{,}760$ for check columns. Applying the [base reduction with seeded rows](SEEDED_MATRIX.md), if each decoding gap is at most $2^{-a}$ then the raw PKE gap obeys
$$
\epsilon\le (2t+2)2^{-a}+2\cdot2^{-320}+2D\cdot2^{-576}.
$$
For $a=224$ this is below $2^{-208}$, and for $a=280$ it is below $2^{-264}$. The leading FO term is bounded by $8\sqrt{2Q\epsilon}$, giving respectively $2^{-5}$ and $2^{-33}$ as strict upper bounds.

The message and private-seed widths are 512 bits, the nonce width is 896 bits, and the private support sampler has 576 bits of slack. The remaining raw-gap terms, including the optional prechallenge correction, sum to at most
$$
16(2Q)2^{-256}+48Q(5Q)2^{-448}+2Q2^{-512}
+4Q2^{-256}+2t2^{-576}<2^{-57}.
$$
The first two terms are the FO message and nonce costs, the third allows earlier decapsulation queries, and the final two come from the private-seed format. Adding these costs and halving the raw gap yields the table. An [exact rational-arithmetic test](test_parameters.py) checks both inequalities against the profile dimensions.

The calculation quantifies the remaining hardness premise. Establishing either row as an actual security claim requires bounding the two decoding gaps under a stated time and memory budget, including the cost of simulating the ideal oracles. The number of oracle calls alone cannot justify a lower bound of $2^{191}$ elementary operations. The scope here is the mathematical single-recipient game; a concrete implementation also needs to uphold its execution assumptions.
