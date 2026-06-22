# Paper-claim alignment

| Repository element | Paper claim supported |
|---|---|
| `src/lightdid_zkp/selector.py` | CAPS-ZK applies filters before cost scoring. |
| `configs/policies/p1_*.json` to `p5_*.json` | Policy classes P1-P5 used for selector demonstration. |
| `results/summary/bbs_50run_summary.csv` | BBS P2 selective-disclosure characterization. |
| `results/summary/anoncreds_50run_summary.csv` | AnonCreds P4 predicate-presentation characterization. |
| `experiments/ablation_study.py` | Unsafe cost-first fallback is blocked by feasibility filters. |
| `experiments/resource_sensitivity.py` | Resource budgets can reject requests without privacy/semantic downgrade. |
| `benchmarks/` | Optional entry points for rerunning real backend experiments. |

The repository separates measured summaries from optional backend reruns to avoid presenting unverified placeholder cryptographic timings as actual measurements.
