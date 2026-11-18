# Published classical cost estimates for the three generated ternary instances

We evaluated the three nonbinary decoding cost models in CryptographicEstimators 2.1.1 on the exact registered input sizes. For the 192 target, the smallest time exponent returned without a memory limit was **700.68**, with a memory exponent of **95.72**. A time exponent measures a modeled number of additions in the field of three elements. A memory exponent measures storage in field elements. These estimates describe classical search on the public syndrome problem. The concrete quantum KEM security level remains open. [Estimator paper, §4.1 and Table 2](https://eprint.iacr.org/2023/589.pdf) · [Pinned estimator source](https://github.com/Crypto-TII/CryptographicEstimators/tree/071cce7a942af423422cb0c6d6af55778c72e4d1/cryptographic_estimators/SDFqEstimator)

## Inputs and units

The estimator takes code length $n$, code dimension $k$, Hamming weight $w$ and field size $q$. For the [matched SG-DIFRA distribution](../round16/MATCHED_PROOF.md) the matrix has $d$ parity-check rows and $n$ columns, so $k=n-d$. The experiment plants a uniformly chosen weight-$w$ ternary vector and publishes its syndrome. We used a log solution count of zero (one planted answer), the estimate for a nonzero syndrome, and $q=3$. For a fixed nonzero planted vector and an iid matrix the syndrome is zero with probability $3^{-d}$. Additional equal-weight answers occur with the extremely small probabilities bounded in [the uniqueness proof](../round16/UNIQUE.md). The probability that the matrix falls short of full row rank is less than $3^{-k}/2$ by a union bound on dependent rows. These choices model the overwhelmingly typical planted instance.

| Target label | $n$ | $k$ | $w$ |
|---:|---:|---:|---:|
| 128 | 8,209,152 | 2,730,474 | 768 |
| 192 | 18,161,280 | 6,041,868 | 1,152 |
| 256 | 32,067,072 | 10,669,096 | 1,536 |

Each entry below is **(log₂ modeled ternary additions, log₂ field elements stored)** rounded to two decimals. We used the published choices of internal search ranges and a constant-cost memory-access model. The Stern implementation searches a finite neighborhood of its heuristic parameter choices. The output covers the package's implemented choices. The first three columns use no memory cap. The last column limits stored field elements to $2^{50}$, or about 223 TB if packed ideally. Both of the other methods retained the same figures under that cap. These are analytic cost evaluations with large integers. No large matrix was allocated or decoded in these runs.

| Target | Prange | Lee–Brickell | Stern | Stern with memory cap |
|---:|---:|---:|---:|---:|
| 128 | (513.81, 45.35) | (499.24, 44.35) | (476.53, 91.08) | (500.08, 48.67) |
| 192 | (741.44, 47.65) | (725.69, 46.64) | (700.68, 95.72) | (742.86, 47.65) |
| 256 | (968.09, 49.29) | (951.52, 48.28) | (924.87, 99.06) | (969.52, 49.29) |

With the stated memory limit, Lee–Brickell gives the smallest modeled time at all three sizes. For example, at the middle size it gives exponents 725.69 for time and 46.64 for memory. The difference between this result and unrestricted Stern illustrates how memory assumptions affect estimates. The suite uses its own operation and storage accounting for each method, including its treatment of the matrix. Physical costs would also depend on input layout, memory access, arithmetic implementation and parallelism.

The [support-probability baseline](BASELINE.md) counts trials and coherent predicate evaluations for one method. The full classical estimator adds modeled work within each trial. Neither calculation supplies a universal lower bound. The application needs a bound on **distinguishing advantage** for the specified resources and proof loss. A cost estimate for typical successful **search** does not bound that advantage. In particular, halving a classical additions exponent gives no quantum gate or depth estimate. Esser et al. report material quantum width and time tradeoffs for binary decoding. Loyer sets out the same random-matrix, planted-weight definition for arbitrary finite fields in §2.2 and evaluates Wave's parameters. Elbro and Weger study further nonbinary methods outside the released three-model suite. [Quantum resource models](https://eprint.iacr.org/2022/964) · [Loyer, §2.2](https://eprint.iacr.org/2023/1263.pdf) · [Elbro and Weger](https://eprint.iacr.org/2025/1402)

## Reproduce the modeled costs

Use a separate Python environment with `cryptographic-estimators==2.1.1`. The input and estimator versions are pinned. All three classes support `time_complexity()` and `memory_complexity()`. The calls below only evaluate published formulas. Leaving the bundled search ranges at their defaults reproduces the table. The optional `bit_complexities=1` setting adds $\log_2(\log_2(3))$ to the reported exponents. The table uses `0`. [PyPI release and source provenance](https://pypi.org/project/cryptographic-estimators/2.1.1/)

```python
from math import inf
from cryptographic_estimators.SDFqEstimator import SDFqProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Prange, LeeBrickell, Stern

profiles = [(8_209_152, 2_730_474, 768), (18_161_280, 6_041_868, 1152),
            (32_067_072, 10_669_096, 1536)]
for n, k, w in profiles:
    for cap in (inf, 50):
        problem = SDFqProblem(n, k, w, 3, nsolutions=0, is_syndrome_zero=False,
                              memory_bound=cap)
        for model in (Prange, LeeBrickell, Stern):
            estimate = model(problem, bit_complexities=0, memory_access=0)
            print(n, cap, model.__name__, round(estimate.time_complexity(), 2),
                  round(estimate.memory_complexity(), 2))
```

As a small reproduction check, the same configuration with $(n,k,w,q)=(100,50,10,3)$ gives Prange (28.65, 12.32), Lee–Brickell (24.22, 12.29) and Stern (22.89, 20.68). The published source and the distributed wheel agree on the small case and all nine uncapped target estimates at the precision reported.
