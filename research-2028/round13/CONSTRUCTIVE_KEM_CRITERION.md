# A sufficient condition for a secure SG-DIFRA permutation KEM

The aim is for only the receiver to recover the secret used by encapsulation. For the existing permutation wrapper, one constructive way to prove this uses two public-key distributions. Only the first distribution is used by a sender or receiver. The second exists for the proof. This is an application of the lossy trapdoor function idea of Peikert and Waters to the [SG-DIFRA transform](../round11/TRANSFORM.md). It specifies a sufficient design criterion. A concrete SG-DIFRA sampler satisfying all its premises remains open. [Peikert and Waters](https://people.csail.mit.edu/cpeikert/pubs/lossy_tdf.pdf)

## The construction to instantiate

Fix a dimension $n$, a domain $D=\mathbb F_3^n$ with $N=3^n$ elements, and a shared key length of 256 bits.

1. **Key generation.** Generate a public key $k$ and a private key $s$. The public map $F_k:D\to D$ must be a permutation. An efficient private procedure must return its unique inverse on every output. Both parties must be able to obtain identical canonical public-key bytes.
2. **Encapsulation.** Draw $X$ uniformly from $D$. Send the canonical encoding of $F_k(X)$ and derive the shared key by hashing the protocol label, suite, dimension, public key and encoded $X$ with the existing unambiguous framing.
3. **Decapsulation.** Reject a malformed ciphertext. On a canonical point, apply the private inverse and hash the recovered input with the same framing. Exact private inversion implies perfect honest agreement.

For the proof, specify a second sampler emitting keys of the same format and dimension with the same public evaluation algorithm. Its maps can have collisions. Assume their expected number of distinct outputs is at most $M$. Assume also that, for the resources being claimed, the difference between a tester's acceptance probabilities on the two public-key distributions is at most $\epsilon$. Key generation is independent of the ideal hash. In the quantum experiment this mode-hiding premise must hold even with the independent auxiliary ideal quantum function used by the simulator. The tester's resource budget must include the reduction, public evaluation and exact input comparison.

## Why hiding the key distribution suffices

Suppose an inverter succeeds with probability $p$ on fresh real keys and uniform encapsulation inputs. A tester samples $X$, runs that inverter on $(k,F_k(X))$, and accepts exactly when the answer equals its original $X$. On real keys this tester succeeds with probability $p$.

Fix a key from the second sampler and any one of its image points $y$. For all inputs $x$ mapping to $y$, the inverter receives the same public information. Its probabilities of returning those distinct $x$ therefore sum to at most one. Summing over $y$ and dividing by $N$ bounds its exact-input success by $|\operatorname{im}F_k|/N$. This works for quantum inverters returning a classical answer and for unequal fiber sizes. For example, a map taking 27 equally likely inputs to three distinct outputs allows exact recovery with probability at most $3/27=1/9$, even with unlimited computation. Averaging over the second sampler and applying mode hiding gives

$$p\le \epsilon+M/N.$$

The existing single-user, one-stage IND-CCA reduction now gives the following raw distinguishing gaps:

$$
\Delta_{\rm classical}\le\min(1,\epsilon+M/N),\qquad
\Delta_{\rm quantum}\le\min(1,2q_H\sqrt{\epsilon+M/N}).
$$

Each inequality uses the mode-hiding bound for the corresponding type and resources of tester. Here $q_H\ge1$ counts quantum hash queries. The quantum game uses classical decapsulation queries. The one-stage gap is zero with no hash queries. In the two-stage convention of Round 11, add $2q_{\rm pre}/N$ before clipping at one. IND-CPA follows by giving the adversary no decapsulation oracle. To establish asymptotic security by these bounds, both the hiding gap and the image ratio must be negligible against the named efficient adversaries. The ideal-hash proof and the concrete SHAKE256 reference implementation have distinct evidentiary scopes.

## Meaning of a concrete work target

As an illustration, set $q_H=2^{191}$ and ask this particular one-stage quantum bound to certify a raw gap of at most $1/2$. It suffices to prove $\epsilon\le2^{-387}$ for the full tester budget and $M/N\le2^{-387}$. Their sum is at most $2^{-386}$, so the displayed bound is at most $1/2$. For ternary domains, losing 245 trits in the sense $M/N\le3^{-245}$ meets the second inequality. This arithmetic imposes no estimate on the unknown mode-hiding gap. A count of hash queries alone does not specify total computation, quantum gates, memory, time, or a NIST security category. [Parameter definitions and cost models](PROFILE_BOUNDS.md)

For SG-DIFRA, the open design problem is to generate real keys with private exact inversion and proof-mode keys with a small image, then justify that their public descriptions are indistinguishable under an independently defined computational assumption. The [Round 12 collision compiler](../round12/GENERATED_DIFFERENTIAL_REDUCTION.md) expresses real-key inversion as a generated cubic differential witness when the external evaluation map has a suitable public circuit. Worst-case hardness of the unrestricted universal decision problem supplies no mode-hiding bound. Once a new construction satisfies the premises, actual reductions, byte sizes and running costs can be evaluated at the three proposed profiles.
