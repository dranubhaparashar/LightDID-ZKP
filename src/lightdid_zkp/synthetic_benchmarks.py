from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd

from .types import BackendMetrics


def generate_synthetic_raw_runs(
    metrics: Dict[Tuple[str, int], BackendMetrics],
    out_path: str | Path,
    seed: int = 20260622,
) -> pd.DataFrame:
    """Generate labeled synthetic raw runs from published summary statistics.

    The included manuscript tables provide summary statistics rather than raw run
    traces. This function creates synthetic traces for code testing and plotting.
    They must not be presented as original raw cryptographic measurements.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for (_, _), m in sorted(metrics.items(), key=lambda x: (x[0][0], x[0][1])):
        for run in range(1, m.runs + 1):
            present = max(0.0, rng.normal(m.prove_or_present_ms_mean, m.prove_or_present_ms_std))
            verify = max(0.0, rng.normal(m.verify_ms_mean, m.verify_ms_std))
            rows.append(
                {
                    "backend": m.backend,
                    "attributes": m.attributes,
                    "run": run,
                    "prove_or_present_ms": present,
                    "verify_ms": verify,
                    "proof_bytes": m.proof_bytes,
                    "vp_bytes": m.vp_bytes,
                    "peak_rss_mb": m.peak_rss_mb,
                    "synthetic_from_summary": True,
                }
            )
    df = pd.DataFrame(rows)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return df
