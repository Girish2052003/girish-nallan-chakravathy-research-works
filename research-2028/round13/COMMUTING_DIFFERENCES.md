# Agreement from two finite differences over the ternary field

Let $V=\mathbb F_3^n$, $W=\mathbb F_3^m$, and let $P:V\to W$ be a public function. Define $(\tau_hP)(x)=P(x+h)$ and $\Delta_hP=\tau_hP-P$. A receiver who knows a private shift can apply it to the sender's public differential. The sender can do the same with the shifts reversed. This yields exact shared-key agreement. We give two results about what an observer can compute from the public information.

## Algorithms and correctness

The setup fixes one reduced polynomial map $P$ of total degree $d=2$ or $3$ for the reference implementation. Both $n$ and $m$ are positive. The receiver samples $b$ uniformly in $V$, publishes $B=\Delta_bP$ and privately stores $b$. The sender samples an independent uniform $a\in V$, sends $A=\Delta_aP$, and computes $v=B(a)-B(0)$. The receiver computes $v'=A(b)-A(0)$. Both values equal

$$D(a,b)=P(a+b)-P(a)-P(b)+P(0).$$

This follows by expanding the four evaluations. Applying the same KDF to this vector and public context therefore gives perfect agreement on every honestly generated ciphertext, even if the shifts or the double difference are zero. The receiver can reconstruct its public bytes from $b$ and the common setup. If exact recovery of a sender-selected bit string is desired, an additional ciphertext field can carry that string XOR a same-length pad derived from $D(a,b)$ and the original public transcript. Any observer who computes $D(a,b)$ can also remove the pad. The bare construction establishes agreement on $D(a,b)$ and makes no claim that decapsulation recovers the random shift $a$.

In the reference encoding, monomials have each exponent at most two. Order them by total degree and then lexicographically by the sorted tuple of repeated variable indices. Flatten the dense coordinate lists in output-major order, and interpret the trits as one base-three integer with first trit most significant. Store it as a fixed-width big-endian byte string. Both $B$ and $A$ have total degree at most $d-1$. Setup binds the label `SG-DIFRA/R13/commuting/setup/v1`, the two dimensions as eight-byte big-endian integers, $d$ as one byte, and the encoding of $P$. Each field receives an eight-byte big-endian length prefix. The setup identifier is the first 32 output bytes of SHAKE256 on this framing. The KDF applies the same framing to `SG-DIFRA/R13/commuting/kem/v1`, this identifier, the public-key bytes, the ciphertext bytes and the $m$ packed shared trits, and returns 32 SHAKE256 bytes. Decapsulation rejects malformed encodings. The mathematical results concern honest keys and ciphertexts, so they do not depend on how other canonical coefficient strings are handled.

Write $M(n,t)$ for the number of reduced monomials of total degree at most $t$, and $w(u)=\lceil u\log_2(3)/8\rceil$. The public setup coefficients require $w(mM(n,d))$ bytes once, each public key and ciphertext uses $w(mM(n,d-1))$ bytes, and the private shift uses $w(n)$ bytes. Here $M(n,1)=n+1$, $M(n,2)=\binom{n+2}2$, and $M(n,3)=\binom{n+3}3-n$. These counts concern the defined encoding. Theorems below preclude positive security ratings for the proposed KEM.

For example, take $P(u,v)=u^2v$, $b=(1,0)$, and $a=(0,1)$. The public polynomials are $B(u,v)=(2u+1)v$ and $A(u,v)=u^2$. The sender obtains $B(0,1)-B(0,0)=1$. The receiver obtains $A(1,0)-A(0,0)=1$. This example has a single output trit and illustrates only agreement.

## Exact public recovery with a bounded coefficient representation

**Theorem 1.** Suppose the printed coefficients belong to an explicitly represented, polynomial-dimensional space of vector-valued functions closed under translations by each coordinate unit vector. Suppose these translations, equality, and linear algebra on coefficient lists are polynomial-time operations. An observer can recover the entire function $\Delta_a\Delta_b P$ for every pair $a,b$ using $P,A,B$ and no secret. This holds in particular for the reference layout.

**Proof.** In that coefficient space, the span of the translates of $P$ has a basis of actual translates $\tau_{u_j}P$ with known $u_j$. Start with $P$, retain independent translates and close the evolving span under the $n$ coordinate-unit translations. At stabilization all ternary translations preserve the span, since the coordinate units generate $V$. Its dimension bounds the number of independent additions, and every stored basis function retains the shift that produced it. The zero space is allowed for $P=0$.

Now express the known function $P+B$ in this basis as $\sum_j t_j\tau_{u_j}P$. Because $P+B=\tau_bP$, linearity and commutation of translations give

$$\tau_{a+b}P=\sum_j t_j\tau_{u_j}(P+A).$$

Subtract $P+A$ and $P+B$ and add $P$ to recover the entire double difference. All work is polynomial in the stated coefficient-space dimension and input size. For dense reduced degree at most $d$ the ambient dimension is $mM(n,d)$. For a sparse explicit polynomial, its downward-closed monomial set also suffices, since translation cannot increase individual exponents. For fixed degree this closure has polynomial size. The method is an instance of linear decomposition in a linear group action. [Myasnikov and Roman’kov, 2015](https://arxiv.org/abs/1412.6401)

Thus a passive observer computes the exact KDF input for every honest encapsulation. With a $\kappa$-bit shared key, comparing the result against the offered key has raw real-versus-independent-uniform probability gap $1-2^{-\kappa}$. This equality holds for a concrete deterministic public KDF, including the implementation specified above. A full-size public inversion timing is unnecessary for this asymptotic conclusion.

## Quantum prediction at the public anchor for any efficiently evaluable map

Replacing the printed coefficient lists by short public circuits could enlarge the translation span exponentially. For the specified anchored agreement and a uniform ephemeral shift, a separate result covers this possibility. The oracle access used below can be implemented reversibly from public polynomial-time classical evaluators. Only the *public* functions are queried coherently.

**Theorem 2.** Let $P$ be any publicly efficiently evaluable function from $V$ to $W$. Assume the public-key representation permits efficient evaluation of $B(x)$, and the ciphertext permits efficient evaluation of $A(x)$. For $0<\eta,\delta<1$, a quantum computation using polynomial resources in $n,m,1/\eta,\log(1/\delta)$ and the public evaluation costs predicts $D(a,b)$ with probability at least $1-\delta-3\eta$ for every fixed $P,b$ and a fresh uniform $a$. Thus this anchored KEM fails IND-CPA also with succinct public evaluation. No bound on the algebraic degree, translate separation, stabilizer, or fiber size of $P$ is required.

**Proof.** Write $N=3^n$ and $\omega=e^{2\pi i/3}$. Form the vector-valued Fourier coefficients of the basis-state function $x\mapsto |P(x)\rangle$ by

$$|v_y\rangle=N^{-1}\sum_{x\in V}\omega^{-x\cdot y}|P(x)\rangle,\qquad p_y=\|v_y\|^2.$$

Parseval gives $\sum_y p_y=1$. A uniformly superposed control bit $j$ and point $x$ allow evaluation into a clean output register of $P(x)$ for $j=0$ and $P(x)+B(x)=P(x+b)$ for $j=1$. Uncompute all scratch registers. After the negative-sign Fourier transform of $x$, the joint state is

$$\sum_y |y\rangle\,\frac{|0\rangle+\omega^{b\cdot y}|1\rangle}{\sqrt 2}\,|v_y\rangle.$$

Measuring $y$ therefore samples the distribution $p$. For its control qubit use the three-outcome measurement with operators $E_k=\tfrac23 |w_k\rangle\langle w_k|$, where $|w_k\rangle=(|0\rangle-\omega^k|1\rangle)/\sqrt2$, $k\in\mathbb F_3$. The sum of the operators is the identity. The probability of $k=b\cdot y$ is zero and the other two probabilities are each $1/2$. Exact constant-dimensional gates can be used in the mathematical model. Equivalently, choose a uniformly random $k$ and project onto $|w_k\rangle$, keeping successful projections. This accepts with probability $1/2$ independently of $y$. Approximating the Fourier and measurement gates within total trace error $\xi$ changes overall success by at most $\xi$. To retain the displayed bound for arbitrary target errors, run the ideal calculation with $\eta/2,\delta/2$ and reserve the remaining slack for gate synthesis. Its logarithmic precision cost preserves the stated resource bound.

Let $h=n+n(n+1)/2$. For candidate $l\in V$ and homogeneous quadratic form $Q$, collect the following linear constraints in their $h$ unknown coefficients:

$$Q(y)+k(l\cdot y)+k^2=1\quad\text{in }\mathbb F_3.$$

The true pair $l=b$, $Q(y)=(b\cdot y)^2$ always satisfies them, since $(b\cdot y-k)^2=1$ for either allowed $k$ and $-2=1$ modulo three. Use $L=\lceil(h\ln3+\ln(1/\delta))/\eta\rceil$ independent samples and choose any solution by linear algebra. An implementation can return a fixed prediction on an inconsistent transcript, which cannot occur with the ideal measurement. A fixed pair with fresh-example failure probability greater than $\eta$ satisfies all $L$ samples with probability at most $e^{-\eta L}$. At most $3^h$ pairs exist. The union bound implies that, except with probability $\delta$, every consistent choice has fresh-example failure probability at most $\eta$.

On any $y$ with $(l-b)\cdot y\ne0$, subtract the true constraint from the candidate one. The residual is an affine expression in $k$ with nonzero linear coefficient. Of the two uniformly allowed values of $k$, at most one makes this residual zero. Hence on the good sample event

$$\Pr_{y\sim p}[(l-b)\cdot y\ne0]\le 2\eta.$$

For $e=l-b$, orthogonality of Fourier characters gives the autocorrelation identity

$$\Pr_{x\gets V}[P(x+e)=P(x)] = \sum_y p_y\operatorname{Re}(\omega^{e\cdot y}).$$

Indeed the left side is the mean scalar product of the two basis labels, and Fourier translation multiplies each coefficient by its character. The real part equals one at $e\cdot y=0$ and $-1/2$ otherwise. Thus the disagreement probability of the two translated functions is at most $3\eta$. This reasoning remains valid for a constant $P$, an arbitrary image distribution or any unknown period.

The learner uses only the setup and receiver's public key, so its $l$ is independent of the subsequent uniform $a$. Estimate $P(a+b)$ by $P(a+l)=P(l)+A(l)$. The estimate is correct with probability at least $1-3\eta$ on the good sample event. The remaining terms in $D(a,b)$ are known exactly from $P(0),A(0),B(0)$. This proves the claimed probability. Comparing a KDF output on the predicted value against the supplied key gives raw gap at least $1-\delta-3\eta-2^{-\kappa}$. For instance $\delta=\eta=1/64$ already gives gap at least $15/16-2^{-\kappa}$, up to circuit gate approximation error. There are no private-oracle queries.

This theorem predicts one anchored session value on a fresh uniform shift. It need not recover the exact shift, identify the full double-difference polynomial, or approximate that polynomial in a canonical encoding. It applies to any fixed public anchor by translating the argument. The uniformity and independence used in the final step are part of the construction. More generally, if the fresh independent shift law satisfies $\Pr[a=t]\le K/3^n$ at every $t$, the error bound becomes $\delta+3K\eta$. This follows by bounding each term in the disagreement event by $K$ times its uniform probability. Friedl, Ivanyos, Magniez, Santha and Sen use Fourier sampling and low-degree constraints for exact hidden translation over elementary abelian groups. Gavinsky, Roetteler and Roland relate exact Boolean hidden shift to the distribution of Fourier weight. Gharibi studies reducing noninjective hidden shifts to injective instances under conditions on the functions. The approximate ternary statement above follows the displayed proof; worldwide priority has not been assessed. [Friedl et al.](https://arxiv.org/abs/quant-ph/0211091) · [Gavinsky et al.](https://arxiv.org/abs/1103.3017) · [Gharibi](https://arxiv.org/abs/1207.4537)
