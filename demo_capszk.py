from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from lightdid_zkp.policy_parser import load_device_profile, load_policy
from lightdid_zkp.registry import default_backend_registry, load_backend_metrics
from lightdid_zkp.selector import CAPSZKSelector
from lightdid_zkp.types import CredentialMetadata

ROOT = Path(__file__).resolve().parent

metrics = load_backend_metrics(ROOT / "results" / "summary")
selector = CAPSZKSelector(
    default_backend_registry(status_path_configured=False),
    metrics,
    CredentialMetadata(
        credential_id="cred-demo",
        issuer_id="did:example:issuer",
        available_backends=["BBS", "AnonCreds"],
        issuer_public_material_valid=True,
        status_path_configured=False,
    ),
)
device = load_device_profile(ROOT / "configs" / "devices" / "container_baseline.json")

for policy_path in sorted((ROOT / "configs" / "policies").glob("p*.json")):
    policy = load_policy(policy_path)
    attrs = int(policy.resource_budget.get("attributes", 16))
    result = selector.select(policy, device, attrs)
    print(f"{policy.policy_id}: {policy.name} -> {result.selected_backend or 'REJECT'} ({result.reason})")
