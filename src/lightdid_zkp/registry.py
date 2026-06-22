from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd

from .types import BackendCapability, BackendMetrics


BBS = "BBS"
ANONCREDS = "AnonCreds"


def default_backend_registry(status_path_configured: bool = False) -> Dict[str, BackendCapability]:
    """Return the implemented backend capability registry used by CAPS-ZK.

    BBS supports unlinkable selective disclosure. It does not support hidden
    credential-backed predicates unless such predicates are already certified as
    signed claims and disclosed. AnonCreds supports the evaluated predicate
    presentation path.
    """
    return {
        BBS: BackendCapability(
            backend=BBS,
            supports_selective_disclosure=True,
            supports_predicates=False,
            supports_unlinkability=True,
            supports_issuer_binding=True,
            supports_status_policy=status_path_configured,
            privacy_level=2,
            supported_semantics=["selective_disclosure", "unlinkable_selective_disclosure"],
        ),
        ANONCREDS: BackendCapability(
            backend=ANONCREDS,
            supports_selective_disclosure=True,
            supports_predicates=True,
            supports_unlinkability=True,
            supports_issuer_binding=True,
            supports_status_policy=status_path_configured,
            privacy_level=3,
            supported_semantics=["credential_backed_predicate", "predicate_hidden_attributes"],
        ),
    }


def load_backend_metrics(results_dir: str | Path) -> Dict[Tuple[str, int], BackendMetrics]:
    """Load included measured summary tables from results/summary."""
    results_dir = Path(results_dir)
    bbs = pd.read_csv(results_dir / "bbs_50run_summary.csv")
    anon = pd.read_csv(results_dir / "anoncreds_50run_summary.csv")
    rows = []
    for backend, df in [(BBS, bbs), (ANONCREDS, anon)]:
        for _, r in df.iterrows():
            rows.append(
                BackendMetrics(
                    backend=backend,
                    attributes=int(r["attributes"]),
                    prove_or_present_ms_mean=float(r["prove_or_present_ms_mean"]),
                    prove_or_present_ms_std=float(r["prove_or_present_ms_std"]),
                    verify_ms_mean=float(r["verify_ms_mean"]),
                    verify_ms_std=float(r["verify_ms_std"]),
                    proof_bytes=float(r["proof_bytes"]),
                    vp_bytes=float(r["vp_bytes"]),
                    peak_rss_mb=float(r["peak_rss_mb"]),
                    runs=int(r.get("runs", 50)),
                )
            )
    return {(m.backend, m.attributes): m for m in rows}


def nearest_metric(metrics: Dict[Tuple[str, int], BackendMetrics], backend: str, attributes: int) -> BackendMetrics:
    """Return exact metric when available; otherwise nearest attribute-count metric."""
    if (backend, attributes) in metrics:
        return metrics[(backend, attributes)]
    candidates = [m for (b, _), m in metrics.items() if b == backend]
    if not candidates:
        raise KeyError(f"No metrics available for backend={backend}")
    return min(candidates, key=lambda m: abs(m.attributes - attributes))
