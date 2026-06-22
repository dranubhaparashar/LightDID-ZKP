from __future__ import annotations

import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_PATH))
sys.path.insert(0, str(ROOT_PATH / "src"))

import pandas as pd

from lightdid_zkp.cost import normalized_cost
from lightdid_zkp.policy_parser import load_device_profile, load_policy
from lightdid_zkp.registry import default_backend_registry, load_backend_metrics, nearest_metric
from lightdid_zkp.selector import CAPSZKSelector
from lightdid_zkp.types import CredentialMetadata
from experiments._paths import CONFIGS, RESULTS, SUMMARY


def unsafe_cost_first(policy, device, metrics, attributes: int) -> str:
    """Deliberately unsafe baseline: chooses minimum resource score before filters."""
    backends = ["BBS", "AnonCreds"]
    return min(backends, key=lambda b: normalized_cost(nearest_metric(metrics, b, attributes), device))


def main() -> None:
    metrics = load_backend_metrics(SUMMARY)
    device = load_device_profile(CONFIGS / "devices" / "container_baseline.json")
    selector = CAPSZKSelector(
        default_backend_registry(status_path_configured=False),
        metrics,
        CredentialMetadata(
            credential_id="cred-lightdid-demo",
            issuer_id="did:example:issuer",
            available_backends=["BBS", "AnonCreds"],
            issuer_public_material_valid=True,
            status_path_configured=False,
        ),
    )

    rows = []
    for policy_path in sorted((CONFIGS / "policies").glob("p*.json")):
        policy = load_policy(policy_path)
        attrs = int(policy.resource_budget.get("attributes", 16))
        safe = selector.select(policy, device, attrs)
        unsafe = unsafe_cost_first(policy, device, metrics, attrs)
        violation = bool(policy.requires_predicate and unsafe == "BBS")
        rows.append(
            {
                "policy_id": policy.policy_id,
                "policy_name": policy.name,
                "safe_caps_zk": safe.selected_backend or "REJECT",
                "unsafe_cost_first": unsafe,
                "unsafe_semantic_violation": violation,
                "explanation": "cost-first selects BBS for a predicate policy" if violation else "no predicate downgrade in this row",
            }
        )
    out = pd.DataFrame(rows)
    (RESULTS / "ablation").mkdir(parents=True, exist_ok=True)
    out.to_csv(RESULTS / "ablation" / "unsafe_fallback_guard.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
