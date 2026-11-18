# A finite resource baseline for the generated ternary problem

The middle layout gives a full public input to a ternary syndrome problem with $d=12{,}119{,}412$ rows, $r=18{,}161{,}280$ columns and weight $w=1{,}152$. For the classical Prange baseline, the reciprocal of the one-trial favorable mass is about $2^{673.108}$. Its ideal quantum square-root scale is $2^{336.554}$. These are counts of trials or coherent predicate evaluations for one published method. They are compatible with a $2^{191}$ target considered in isolation. They give no lower bound on competing methods or the cost of distinguishing KEM keys. A separate calculation below identifies a quantitative limitation of the proof route through search.

## Which resources do the numbers count?

The matrix is iid uniform over $\mathbb F_3$. The syndrome equals $Be$ for an independent uniformly signed vector of weight $w$. This general search distribution also appears in [Loyer, *Quantum security analysis of Wave*, Problem 1](https://eprint.iacr.org/2023/1263.pdf). Its parameter values here belong to SG-DIFRA. The baseline counts subsets of $d$ matrix columns that contain the planted support and are independent. The containment mass is $u=\binom{d}{w}/\binom{r}{w}$. For a fixed subset the relevant square has full rank with probability $a_d=\prod_{i=1}^d(1-3^{-i})$, independently of the support. Thus $p=u a_d$ is the one-trial probability, averaged over honest inputs. The signs place no additional condition. A favorable square determines its supported solution uniquely by elementary linear algebra. [Kachigar and Tillich, *Quantum Information Set Decoding Algorithms*, §3](https://arxiv.org/abs/1703.00263)

| Target | $-\log_2 u$ | $-\log_2 p$ | $-\tfrac12\log_2 p$ | Packed iid matrix alone, decimal TB |
|---:|---:|---:|---:|---:|
| 128 | 448.081 | 448.917 | 224.459 | 8.911 |
| 192 | 672.271 | 673.108 | 336.554 | 43.607 |
| 256 | 896.464 | 897.300 | 448.650 | 135.944 |

Packing uses $dr\log_2(3)/8$ bytes before rounding up. The middle matrix contains exactly 220,104,034,767,360 trits, plus $d$ syndrome trits for the public challenge. The seeded KEM public key has a different representation. For classical sampling with fixed per-input favorable mass $p_B$, the probability of at least one favorable event in $K$ independent trials is $1-(1-p_B)^K$. A fixed-input constant-success budget is of order $1/p_B$. Quantum amplitude amplification uses order $1/\sqrt{p_B}$ coherent evaluations and their inverses for constant success, with unit cost assigned to each evaluation. The high-probability statements below and [Round 16 uniqueness](../round16/UNIQUE.md) justify these exponents for typical inputs, up to constant factors. Physical quantum costs also include reversible algebra, data access, state preparation, uncomputation, gates, depth and memory. The table does not assign unit cost to those operations in a physical resource estimate. [Brassard et al., *Quantum Amplitude Amplification and Estimation*](https://arxiv.org/abs/quant-ph/0005055)

## Why the average describes a typical public matrix

Fix a planted support of size $w$. For each iid $B$ let $X$ be the fraction of the $d$-subsets **containing that support** for which the square is invertible. Then $p_B=uX$ and $\mathbb E_B X=a_d$. For two independent such subsets whose intersection has size $j$, put $L_j=\prod_{i=0}^{j-1}(1-3^{i-d})$. The shared columns must be independent, an event of probability $L_j$. Conditional on their independence, either subset extends them to a basis with probability $a_d/L_j$. The two extensions use independent new columns. Consequently

$$\operatorname{Var}(X)/a_d^2=\mathbb E_j[1/L_j-1].$$

If $d-j\ge128$, the union bound on the rank-product factors gives $1-L_j<3^{-128}/2$ and $1/L_j-1<3^{-128}$. Always $L_j\ge a_d>1/2$. The exceptional probability $\Pr(d-j<128)$ equals

$$\frac{\sum_{i=0}^{127}\binom{r-d}{i}\binom{d-w}{i}}{\binom{r-w}{d-w}}.$$

Across the three rows, $r<2^{25}$ and $(r-w)/(d-w)>\sqrt{2}$. The numerator is at most $128r^{254}$. The denominator is at least $((r-w)/(d-w))^{d-w}>2^{(d-w)/2}$ by the product formula for binomial coefficients. Their ratio is below $2^{-1{,}000{,}000}$. Chebyshev's inequality therefore gives

$$\Pr\bigl(|X-a_d|>a_d/16\bigr)\le256(3^{-128}+2^{-1{,}000{,}000})<2^{-194}.$$

This controls the fixed-input favorable mass before repeating trials or applying amplitude amplification. Averaging the reciprocal of a one-trial success probability without handling input variability would not establish such a claim.

## A limit on the strong search-only certificate

Round 16's Fourier reduction implies $P_{\rm search}\ge4\eta^2/9$ for the corresponding tester and resources. To deduce $\eta\le2^{-280}$ solely by upper-bounding *all* search success via this inequality, a sufficient ceiling is $(4/9)2^{-560}$. That ceiling already falls below a classical lower bound on achievable search success in the following explicit unit-cost model. This addresses the proposed use of the Fourier inequality. The direct decisional assumption is a different statement.

Use random-access words large enough to address the whole dense input, with unit costs for word arithmetic, a load, a store and a fresh uniform integer below a word-sized bound. Charge one operation to read each input trit once, allow storage for the input and an additional dense $d$-square, and budget $2^{191}$ word operations. A deliberately loose upper budget for one ordinary dense baseline trial is $128(d+1)^3$ operations on these dimensions. For example, a cubic elimination on an augmented array needs at most $(d+1)^3$ elementary entry updates, each using a fixed row offset, at most four indexed reads/writes, two ternary arithmetic operations, and loop/address arithmetic. Pivot searches, row normalization, row swaps, and a final weight check contribute quadratic terms. Copying the square uses $O(d^2)$ word operations and selecting the subset by a word-array shuffle uses $O(r)$. Charging 32 operations per loop iteration to each of the cubic update pass, the setup and the quadratic passes stays within the displayed allowance since $r<2d$ and $d>10^7$. This is an abstract classical RAM convention. A reversible quantum circuit or a physical machine requires its own cost model.

At the middle dimensions $K=2^{113}$ independent trials fit because $K\cdot128(d+1)^3+dr+r+d<2^{191}$. Exact counts give $2^{-673}<u<2^{-672}$ and $a_d>11/20$. On the good set of matrices from the previous section, $p_B\ge(15/16)a_d u$ and $Kp_B\le Ku<1/8$. Inclusion–exclusion gives $1-(1-p_B)^K\ge Kp_B(1-Kp_B/2)\ge(15/16)Kp_B$. The good set has probability greater than $15/16$. Thus achievable planted search success in this model exceeds

$$ (15/16)^3(11/20)2^{-560}>(4/9)2^{-560}. $$

This small success probability can coexist with a very high cost for constant-success searches. It rules out that particular sufficient **uniform search ceiling** in this RAM budget. It does not demonstrate a common decision gap above $2^{-280}$ or a KEM distinguisher, or transfer that comparison to an independently specified physical gate budget. Quantitative IND-CCA security remains conditional on bounding the decision advantage at all resources used by the reduction. [Round 16 proof and numerical thresholds](../round16/MATCHED_PROOF.md)

`python3 baseline.py` reproduces the numerical table from the registered dimensions. It computes binomial coefficients as exact integers and encloses the rank probability using its first 48 factors and the geometric tail. The corresponding finite tests check the small-matrix second moment exhaustively, the large-profile arithmetic, the exceptional-event bounds and the search-ceiling comparison. The calculation processes dimensions only and does not build a matrix or solve an instance.
