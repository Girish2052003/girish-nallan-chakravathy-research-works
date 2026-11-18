# Round 9 reproducible finite evidence

Generated on 18 November 2026 by
`research-2028/round9/verify_round9.py --legacy` from the working tree based
on `b0a4288dbb9dbffa647cc9eed973f76e640aa7f7`.

- [Structured results and exact source SHA-256 hashes](results.json)
- [21 new tests: full log](round9-tests.log)
- Fifteen `legacy-*.log` files preserve the output of the existing
  prescribed research programs. Each returned exit code zero.
- [Interpretation and scope of these results](../../round9/VERIFICATION_REPORT.md)

Reproduce without overwriting the committed evidence:

```sh
python3 research-2028/round9/verify_round9.py --legacy --output-dir /tmp/sg-difra-round9
```

The JSON records the checkout HEAD separately from exact source hashes
because the evidence was generated before committing the new source files.
Timestamps and elapsed times will differ on reruns. The fixed input cases
and seeds are reproducible. This is finite regression evidence, not a
cryptographic hardness estimate or formal verification of the Python code.
