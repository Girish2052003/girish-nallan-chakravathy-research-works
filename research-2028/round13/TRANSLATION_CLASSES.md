# Recovering the class of a secret translation in an explicit potential

The proposed exchange lets the receiver keep a ternary shift $b$ and publish only the first difference of a fixed polynomial map $P$. A sender with a fresh shift $a$ can compute a shared second difference. This note proves perfect honest agreement. It also proves that the full published coefficients reveal everything required to compute that shared value from an honest ciphertext. The conclusion includes maps with many equivalent private keys.

## Shift-equivalence theorem

Let $F,G:\mathbb F_3^n\to\mathbb F_3^m$ be ordered vectors of reduced coordinate polynomials. Every exponent of a variable is at most two. Write $\tau_h F(x)=F(x+h)$ and $\Delta_hF=\tau_hF-F$. Write $D$ for the largest total degree in either map and $M$ for the number of distinct monomials in the downward closure of their combined support, including the constant. A monomial lies in this closure if it divides a listed monomial. Dimensions, variables, and output coordinates are explicit.

**Theorem.** There is a deterministic algorithm of cost polynomial in $n,m,D,M$ and the input length which returns either an empty set or a representative and basis for the entire affine space

$$\mathcal S(F,G)=\{h:\tau_hF=G\}.$$

In particular it returns the full linear subspace $\operatorname{Per}(F)=\mathcal S(F,F)$. This is polynomial in the dense coefficient encoding for any degree and in the ordinary sparse input size at bounded degree. A single high-degree monomial can have a large downward closure in a sparse encoding.

**Proof.** The reduced representation is unique, by the univariate root bound applied successively in each variable. Translation replaces each reduced monomial by itself plus terms of strictly lower total degree. It introduces only divisors of that monomial. Thus translation preserves our coefficient space and all its degree subspaces. Let $V_j$ be its vector-valued subspace of total degree at most $j$, with $V_{-1}=0$. Translation induces the identity on $V_j/V_{j-1}$. Denote the projection from $V_j$ to this quotient by $\pi_j$.

Start with $j=D$, a representative $v=0$, and $H=\mathbb F_3^n$. The current approximate solution set is

$$v+H=\{w:\tau_wF-G\in V_j\},\qquad H=\{u:\Delta_uF\in V_j\}.$$

Both equalities hold initially. On $H$ we have the map $L_j(u)=\pi_j(\Delta_uF)$. The cocycle identity $\Delta_{u+w}F=\Delta_uF+\tau_u\Delta_wF$ and triviality of translation on the quotient show that $L_j$ is additive. Since the scalar field is the prime field $\mathbb F_3$, it is linear there. For every $u\in H$,

$$\pi_j(\tau_{v+u}F-G)=\pi_j(\tau_vF-G)+L_j(u).$$

Compute $L_j$ on a basis of $H$ by substitution and coefficient extraction. Solve this *linear* equation for the right-hand side to vanish. Inconsistency proves the exact solution set is empty. If $u_0$ is one solution, the next representative is $v+u_0$, the next space is $\ker L_j$, and the two displayed invariants hold with $j-1$. After processing the constant grade $j=0$, congruence modulo $V_{-1}$ is exact equality. The resulting coset is the entire set of shifts. Its associated direction space is the period space of $F$.

There are at most $D+1$ grades. Expanding a translation of one monomial uses only its divisors, at most $M$ monomials, with coefficients obtained from the binomial formula. Computing the graded maps for at most $n$ basis elements and solving linear systems with at most $mM$ rows take polynomially many operations in the stated parameters. This argument does not require ordinary formal derivatives to detect the secret shift.

Shift equivalence and period computation have a published history. Grigoriev's Theorem 2 already gives a randomized algorithm over prime fields for reduced inputs, of cost $(p^D\binom{n+D}{D})^{O(1)}$, together with the affine-coset description. The proof above works directly with the graded coefficients of ternary functions and yields the deterministic bound for the stated representation. We use this argument for the differential key distribution. Global priority for the algorithm is unverified. [Grigoriev, *Testing shift-equivalence of polynomials by deterministic, probabilistic and quantum machines*, Theorem 2](https://logic.pdmi.ras.ru/~grigorev/pub/quantum2_tcs.pdf)

## Consequences for a private shift and for lossy keys

Suppose $P$ is public and $B=\Delta_bP$ is also public. Apply the theorem with $F=P$, $G=P+B$. It returns exactly $b+\operatorname{Per}(P)$. Given any representative $b'=b+h$ with $h\in\operatorname{Per}(P)$, one has $\Delta_{b'}P=\Delta_b P$. For every $a$, $\tau_h(\Delta_a P)=\Delta_a(\tau_h P)=\Delta_aP$. Hence

$$\Delta_{b'}(\Delta_aP)=\Delta_b(\Delta_aP)=\Delta_a(\Delta_bP)$$

as full polynomial functions. Therefore recovering the specific originally sampled $b$ is unnecessary even when many secrets produce the same public key. Any deterministic public calculation on that shared polynomial and the transcript, including evaluation at zero, agrees with the honest sender. This statement suffices on authentic ciphertexts. It requires no assumption about the private decoder on unrelated ciphertexts.

There is also a direct consequence for lossy map proposals. An injective $F$ has only the zero period. Every map of the form $x\mapsto C(Ax+t)$ with a singular linear input map $A$ has $\ker A\subseteq\operatorname{Per}(F)$, whatever $C$ does. Thus the public period dimension separates these two modes exactly for explicit polynomial encodings within the theorem's cost. The conclusion concerns loss introduced by an affine input projection. Other ways of introducing collisions may leave the period space trivial.

## Byte counts for the reference implementation

The [protocol specification](COMMUTING_DIFFERENCES.md) gives the field order, length framing and KDF inputs. These counts apply to its [quadratic and cubic implementation](commuting_kem.py). Write $d$ for the setup degree and $w(t)=\lceil t\log_2(3)/8\rceil$ for the canonical byte width of $t$ trits.

The public key and ciphertext each occupy $w(m\binom{n+d-1}{d-1})$ bytes because the transmitted degree is at most two. The private key uses $w(n)$ bytes. The degree-$d$ setup is separate. Its dense layout uses $w(m\binom{n+2}{2})$ bytes for $d=2$ or $w(m(\binom{n+3}{3}-n))$ for $d=3$. The following sizes illustrate $m=n$. They do not assign security bits.

| Dimension | Private key | Quadratic potential: public key or ciphertext | Cubic potential: public key or ciphertext |
| ---: | ---: | ---: | ---: |
| 81 | 17 B | 1,316 B | 54,611 B |
| 122 | 25 B | 2,973 B | 184,326 B |
| 162 | 33 B | 5,232 B | 428,989 B |

By the preceding theorem a passive observer recomputes the exact shared key for every honest transcript. Comparing the offered challenge key with that value gives raw IND-CPA gap $1-2^{-256}$. The same observation disproves IND-CCA. This holds independently of the number of periods, randomness used to generate $P$, or the computational properties of the KDF, provided the representation fits the calculation above and $P$ is public.

For a one-trit numerical check, let $P(x)=2x^2+x+1$, $b=2$ and $a=1$. Then $B(x)=1+2x$ and $C(x)=x$. Both sides obtain $t=2$. The packed public key, private key and ciphertext are `05`, `02` and `01` in hex. The [finite tests](test_commuting_kem.py) cover all 18 scalar quadratics with all nine ordered shift pairs, every shift pair for a two-output cubic fixture, explicit sets of equivalent private keys, independent packed polynomial evaluation, KDF framing and canonical parsing.
