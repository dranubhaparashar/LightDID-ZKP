from __future__ import annotations

import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_PATH))
sys.path.insert(0, str(ROOT_PATH / "src"))

import pandas as pd

from lightdid_zkp.registry import load_backend_metrics
from experiments._paths import RESULTS, SUMMARY


def main() -> None:
    metrics = load_backend_metrics(SUMMARY)
    rows = []
    for (backend, attributes), m in sorted(metrics.items(), key=lambda x: (x[0][0], x[0][1])):
        rows.append(
            {
                "backend": backend,
                "attributes": attributes,
                "runs": m.runs,
                "prove_or_present_ms_mean": m.prove_or_present_ms_mean,
                "prove_or_present_ms_std": m.prove_or_present_ms_std,
                "verify_ms_mean": m.verify_ms_mean,
                "verify_ms_std": m.verify_ms_std,
                "proof_bytes": m.proof_bytes,
                "vp_bytes": m.vp_bytes,
                "peak_rss_mb": m.peak_rss_mb,
                "cv_present_pct": round(100 * m.prove_or_present_ms_std / m.prove_or_present_ms_mean, 2),
                "cv_verify_pct": round(100 * m.verify_ms_std / m.verify_ms_mean, 2),
            }
        )
    out = pd.DataFrame(rows)
    (RESULTS / "tables").mkdir(parents=True, exist_ok=True)
    out.to_csv(RESULTS / "tables" / "combined_backend_summary.csv", index=False)

    # Derived scaling tables.
    derived = []
    growth = []
    for backend in sorted({r["backend"] for r in rows}):
        df = out[out.backend == backend].sort_values("attributes")
        first = df.iloc[0]
        last = df.iloc[-1]
        span = float(last.attributes - first.attributes)
        derived.append(
            {
                "backend": backend,
                "prove_or_present_ratio_4_to_64": round(last.prove_or_present_ms_mean / first.prove_or_present_ms_mean, 2),
                "verify_ratio_4_to_64": round(last.verify_ms_mean / first.verify_ms_mean, 2),
                "vp_size_ratio_4_to_64": round(last.vp_bytes / first.vp_bytes, 2),
                "rss_ratio_4_to_64": round(last.peak_rss_mb / first.peak_rss_mb, 2),
            }
        )
        growth.append(
            {
                "backend": backend,
                "prove_or_present_ms_per_attribute": round((last.prove_or_present_ms_mean - first.prove_or_present_ms_mean) / span, 2),
                "verify_ms_per_attribute": round((last.verify_ms_mean - first.verify_ms_mean) / span, 2),
                "vp_bytes_per_attribute": round((last.vp_bytes - first.vp_bytes) / span, 2),
            }
        )
    pd.DataFrame(derived).to_csv(SUMMARY / "scaling_ratios.csv", index=False)
    pd.DataFrame(growth).to_csv(SUMMARY / "per_attribute_growth.csv", index=False)
    print("Wrote combined backend summary and derived scaling tables.")


if __name__ == "__main__":
    main()
