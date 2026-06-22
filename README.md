# LightDID-ZKP

**Policy- and Resource-Aware Selection of BBS and AnonCreds Presentations for Privacy-Preserving Decentralized Identity**

This repository contains the reproducible code package for the LightDID-ZKP paper.  The repository is intentionally scoped to the implemented prototype described in the manuscript:

- **BBS** for unlinkable selective-disclosure presentations.
- **AnonCreds** for credential-backed hidden predicate presentations.
- **CAPS-ZK** as the policy- and resource-aware holder-side backend selector.

LightDID-ZKP is **not** a new cryptographic primitive. It is an orchestration and selection layer that decides which existing presentation backend is semantically safe and resource-feasible for a verifier policy.

## Repository contents

```text
LightDID-ZKP/
├── src/lightdid_zkp/          # CAPS-ZK selector, policy model, cost model, verifier guards
├── experiments/              # Scripts to reproduce tables, selector demo, ablations, figures
├── configs/                  # Policy classes P1-P5 and device profiles
├── results/                  # Included benchmark summaries, derived tables, and plots
├── benchmarks/               # Optional real-backend benchmark entry points
├── tests/                    # Basic pytest tests for selector safety
└── docs/                     # GitHub upload notes, reviewer notes, protocol notes
```

## What is included

The repository includes:

1. A runnable Python implementation of the CAPS-ZK selector.
2. Policy classes P1-P5 used in the paper.
3. Container-baseline benchmark summaries for 4, 8, 16, 32, and 64 attributes.
4. Derived scaling ratios and per-attribute growth tables.
5. Selector demonstration outputs.
6. Ablation showing why unsafe cost-first selection is invalid.
7. Resource-sensitivity experiments.
8. Figure generation scripts.
9. Optional real-backend benchmark scripts for environments where BBS and AnonCreds dependencies are installed.

## Important reviewer-safe claim boundary

This package does not claim that LightDID-ZKP outperforms BBS or AnonCreds. BBS and AnonCreds solve different policy semantics. The benchmark results characterize backend behavior for selector parameterization:

- BBS is evaluated for **P2 unlinkable selective disclosure**.
- AnonCreds is evaluated for **P4 credential-backed predicate presentation**.
- CAPS-ZK applies feasibility filters before cost scoring, so a low-cost backend is never selected when it is semantically insufficient.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python experiments/run_all.py
pytest
```

Generated outputs are written under `results/`.

## Reproduce included tables and plots

```bash
python experiments/reproduce_tables.py
python experiments/selector_demo.py
python experiments/ablation_study.py
python experiments/resource_sensitivity.py
python experiments/make_figures.py
```

## Optional real-backend benchmarks

The `benchmarks/` folder contains optional scripts for rerunning real cryptographic backends when dependencies are available. These are not required for the selector demonstration.

- `benchmarks/bbs_mattr/bench_bbs_mattr.js` expects Node.js and `@mattrglobal/bbs-signatures`.
- `benchmarks/anoncreds_python/bench_anoncreds_optional.py` expects a working `anoncreds` Python/libanoncreds installation.

If these dependencies are unavailable, use the included measured summary CSVs under `results/summary/` and rerun the selector/analysis code.

## Main commands for GitHub users

```bash
git init
git add .
git commit -m "Initial LightDID-ZKP reproducibility package"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

## Citation

See `CITATION.cff`.
