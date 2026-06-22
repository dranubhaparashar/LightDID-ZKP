from __future__ import annotations

import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_PATH))
sys.path.insert(0, str(ROOT_PATH / "src"))

import pandas as pd

from lightdid_zkp.policy_parser import load_policy
from lightdid_zkp.registry import default_backend_registry, load_backend_metrics
from lightdid_zkp.selector import CAPSZKSelector
from lightdid_zkp.types import CredentialMetadata, DeviceProfile
from experiments._paths import CONFIGS, RESULTS, SUMMARY


def main() -> None:
    metrics = load_backend_metrics(SUMMARY)
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
    policies = [load_policy(p) for p in sorted((CONFIGS / "policies").glob("p*.json"))]
    memory_budgets = [160, 220, 300, 400]
    vp_budgets = [1000, 5000, 20000, 50000]
    rows = []
    for mem in memory_budgets:
        for vp in vp_budgets:
            device = DeviceProfile(
                name=f"grid_rss{mem}_vp{vp}",
                max_prove_ms=500,
                max_verify_ms=300,
                max_vp_bytes=vp,
                max_rss_mb=mem,
            )
            for policy in policies:
                attrs = int(policy.resource_budget.get("attributes", 16))
                result = selector.select(policy, device, attrs)
                rows.append(
                    {
                        "device": device.name,
                        "rss_budget_mb": mem,
                        "vp_budget_bytes": vp,
                        "policy_id": policy.policy_id,
                        "accepted": result.accepted,
                        "selected_backend": result.selected_backend or "REJECT",
                        "reason": result.reason,
                    }
                )
    out = pd.DataFrame(rows)
    (RESULTS / "resource_sensitivity").mkdir(parents=True, exist_ok=True)
    out.to_csv(RESULTS / "resource_sensitivity" / "resource_grid.csv", index=False)
    print("Wrote resource sensitivity grid.")


if __name__ == "__main__":
    main()
