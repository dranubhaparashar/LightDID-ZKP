from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_PATH))
sys.path.insert(0, str(ROOT_PATH / "src"))

import pandas as pd

from lightdid_zkp.policy_parser import load_device_profile, load_policy
from lightdid_zkp.registry import default_backend_registry, load_backend_metrics
from lightdid_zkp.selector import CAPSZKSelector
from lightdid_zkp.types import CredentialMetadata
from experiments._paths import CONFIGS, RESULTS, SUMMARY


def main() -> None:
    metrics = load_backend_metrics(SUMMARY)
    registry = default_backend_registry(status_path_configured=False)
    meta = CredentialMetadata(
        credential_id="cred-lightdid-demo",
        issuer_id="did:example:issuer",
        available_backends=["BBS", "AnonCreds"],
        issuer_public_material_valid=True,
        status_path_configured=False,
        signed_claims=["name", "role", "membership"],
    )
    selector = CAPSZKSelector(registry, metrics, meta)
    device = load_device_profile(CONFIGS / "devices" / "container_baseline.json")

    rows = []
    for policy_path in sorted((CONFIGS / "policies").glob("p*.json")):
        policy = load_policy(policy_path)
        attributes = int(policy.resource_budget.get("attributes", 16))
        result = selector.select(policy, device, attributes)
        rows.append(
            {
                "policy_id": policy.policy_id,
                "policy_name": policy.name,
                "semantics": policy.semantics,
                "attributes": attributes,
                "accepted": result.accepted,
                "selected_backend": result.selected_backend or "REJECT",
                "score": result.score,
                "reason": result.reason,
                "candidates": ";".join(result.candidates),
                "rejected": json.dumps(result.rejected, sort_keys=True),
                "policy_hash": result.policy_hash,
            }
        )
    out = pd.DataFrame(rows)
    (RESULTS / "selector").mkdir(parents=True, exist_ok=True)
    out.to_csv(RESULTS / "selector" / "selector_decisions.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
