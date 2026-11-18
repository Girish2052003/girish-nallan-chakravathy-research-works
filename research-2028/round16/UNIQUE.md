# Unique witnesses on the complete public input

One question about the matched distribution has an unconditional answer. With overwhelming probability over the public matrix, **every** error of the prescribed weight has a different syndrome. Thus an honest challenge determines one sparse vector, and consequently one full cubic collision witness in the canonical encoding. This proposition allows an observer to see the entire matrix and syndrome. It describes what the public data determines, independently of the time needed to find the answer.

Let $B$ have $d$ rows and $r$ columns sampled independently and uniformly over the ternary field. There are $W=2^w\binom{r}{w}$ signed weight-$w$ vectors. For two distinct such vectors $s,u$, the difference $s-u$ has a nonzero coordinate. A uniform row of $B$ therefore has a uniform scalar product with $s-u$. Independence of the rows gives $\Pr_B[Bs=Bu]=3^{-d}$. A union bound on the unordered pairs gives
$$
\Pr_B[\text{some two weight-}w\text{ vectors have the same syndrome}]
\le {W(W-1)\over 2\,3^d}.
$$
For any fixed matrix the image of these vectors has at most $W$ elements. A fresh independent uniform comparison syndrome has a valid weight-$w$ witness with probability at most $W/3^d$, exactly $W/3^d$ if the restriction is injective. These claims concern iid matrices in the underlying hardness experiment. The KEM proof separately handles the seeded wire distribution.

| Matched target | $k$ with $2^{k-1}\le W<2^k$ | Probability any pair collides, below | Uniform comparison syndrome has a witness, below |
|---:|---:|---:|---:|
| 128 | 12,149 | $2^{-8,650,276}$ | $2^{-8,662,424}$ |
| 192 | 18,872 | $2^{-19,151,326}$ | $2^{-19,170,197}$ |
| 256 | 25,787 | $2^{-33,828,555}$ | $2^{-33,854,341}$ |

The figures follow by exact integer arithmetic. Compute $k$ as the bit length of $W$, and use $3^{12}>2^{19}$ to lower-bound $3^d$ by $2^{\lfloor 19d/12\rfloor}$. An unbounded observer can distinguish almost perfectly by checking existence. Establishing a bound on efficient observers is a separate computational question. No work factor follows from uniqueness or rarity.
