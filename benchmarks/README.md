# Optional real-backend benchmark scripts

This directory contains optional benchmark entry points for users who want to rerun actual cryptographic backends.

The main repository does not require these dependencies for selector reproduction. The included `results/summary/*.csv` files are sufficient to rerun the selector, tables, ablations, and figures.

## BBS

```bash
cd benchmarks/bbs_mattr
npm install
node bench_bbs_mattr.js --attrs 4 --runs 50 --warmup 5
```

## AnonCreds

```bash
python benchmarks/anoncreds_python/bench_anoncreds_optional.py --attrs 4 --runs 50 --warmup 5
```

These scripts write CSVs to stdout by default. Copy validated output into `results/summary/` or a separate `results/raw_real/` folder with environment notes.
