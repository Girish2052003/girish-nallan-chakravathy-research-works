# Reproducing the local collision results

The complete Round 10 suite runs with the Python standard library. The recorded local run used CPython 3.12.14 on 18 November 2026. From the repository root run

```sh
python3 -m unittest discover -s research-2028/round10 -p 'test_*.py' -v
```

The run completed **22 test methods with zero failures, errors or skips**. These finite checks exercise the construction and proofs on small inputs. No timing measurement enters a complexity theorem.

| Checks | What was compared |
| --- | --- |
| Quadratic compiler | Four one-bit circuits, 144 complete challenges across the fixtures, nine local response pairs per challenge and 1,296 comparisons of actual polynomial outputs at the two shifted points. Across those four circuits the test also compared all 2,916 pairs of complete ternary tables with direct graph conditions. Further fixtures covered aliased gate inputs, two-bit addresses, malformed traces, changed helpers and deletion of the sole linear term. |
| Cubic compiler | For a two-gate graph, exhaustive enumeration of 81 ternary challenges, all nine color pairs, and all 729 pairs of local tables gave 54 winning pairs including unconstrained nonbinary entries. On four Boolean vertices, enumeration of 81 common color assignments gave zero wins for the complete graph and 18 for the complete bipartite graph with sides of size two. Tests compared raw evaluations, corrupted individual helper values, checked the five-term and square-free conditions, and separately removed each exceptional term. |
| Affine relation algorithm | All 512 subsets of the nine-point ternary plane were compared with direct affine closure. The empty set and 22 nonempty affine sets matched the algorithm's classification. Brute force checked all 529 ordered pairs of parallel affine constraints, 1,296 transport-labeled rectangles and 240 seeded mixed networks. |
| Shortest refuting lists | Path distances were checked at widths two, three and four, with additional even-distance, identical-endpoint and disconnected examples. At width two an independent enumeration of 6,561 pairs of table assignments on Boolean addresses verifies that every pair of challenge effects is jointly satisfiable while a specified triple is inconsistent. |
| Fully local quadratic upper bound | Checked 81 bi-affine interpolation examples, all 729 quadratic coefficient choices for a two-dimensional unseen block, and 152 small policy systems by comparing the interpolation/subspace test with exhaustive policy search. Of these systems, 131 had no policy. Each extracted refuting list was checked independently by brute force. |

The compilers emit sparse coordinate monomials. The tests evaluate their coefficients and factors directly at $z$ and $z+h_c$. In the lower-bound compilers the helper assignments are triangular, so for fixed local answers and a challenge their stationary helper values are uniquely determined; the moving base coordinates cancel. The test for the upper bound explicitly materializes small graphs. The polynomial-space proof describes how to generate their edges without storing an exponential graph.

The typeset note includes the main proof, both certificate-size proofs and the comparison with published work. Rebuild it from the four Markdown sources using Pandoc 3, XeLaTeX and the Latin Modern fonts.

```sh
python3 research-2028/round10/build_paper.py
```

The companion baseline can be reproduced separately with

```sh
python3 research-2028/round9/verify_round9.py --output-dir /tmp/sg-difra-round9
```

The local baseline run passed the 21 Round 9 methods. Written derivations were also checked in separate AI-assisted reviews, including the two deletion certificates, the observation assumptions, and the interpolation argument. No external referee or proof-assistant certification is recorded here.

[Main proof](README.md) · [Shortest refuting list](OBSTRUCTION.md) · [Two-view bound](TWO_VIEW_BOUND.md) · [Literature and priority](RELATED_WORK.md)
