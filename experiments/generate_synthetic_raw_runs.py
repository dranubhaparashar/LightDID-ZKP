from __future__ import annotations

import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_PATH))
sys.path.insert(0, str(ROOT_PATH / "src"))

from lightdid_zkp.registry import load_backend_metrics
from lightdid_zkp.synthetic_benchmarks import generate_synthetic_raw_runs
from experiments._paths import RESULTS, SUMMARY


def main() -> None:
    metrics = load_backend_metrics(SUMMARY)
    out = RESULTS / "synthetic_raw_runs" / "synthetic_raw_runs_from_summary_seed20260622.csv"
    df = generate_synthetic_raw_runs(metrics, out)
    print(f"Wrote {len(df)} synthetic run rows to {out}")


if __name__ == "__main__":
    main()
