from pathlib import Path

from lightdid_zkp.policy_parser import load_device_profile, load_policy
from lightdid_zkp.registry import default_backend_registry, load_backend_metrics
from lightdid_zkp.selector import CAPSZKSelector
from lightdid_zkp.types import CredentialMetadata

ROOT = Path(__file__).resolve().parents[1]


def make_selector():
    return CAPSZKSelector(
        default_backend_registry(status_path_configured=False),
        load_backend_metrics(ROOT / "results" / "summary"),
        CredentialMetadata(
            credential_id="cred-test",
            issuer_id="did:example:issuer",
            available_backends=["BBS", "AnonCreds"],
            issuer_public_material_valid=True,
            status_path_configured=False,
        ),
    )


def test_p2_selects_bbs():
    selector = make_selector()
    policy = load_policy(ROOT / "configs" / "policies" / "p2_unlinkable_selective_disclosure.json")
    device = load_device_profile(ROOT / "configs" / "devices" / "container_baseline.json")
    result = selector.select(policy, device, 16)
    assert result.accepted
    assert result.selected_backend == "BBS"


def test_p4_predicate_does_not_fallback_to_bbs():
    selector = make_selector()
    policy = load_policy(ROOT / "configs" / "policies" / "p4_predicate_hidden_attributes.json")
    device = load_device_profile(ROOT / "configs" / "devices" / "container_baseline.json")
    result = selector.select(policy, device, 16)
    assert result.accepted
    assert result.selected_backend == "AnonCreds"
    assert "BBS" in result.rejected
    assert any("unsafe fallback" in x for x in result.rejected["BBS"])


def test_p5_rejects():
    selector = make_selector()
    policy = load_policy(ROOT / "configs" / "policies" / "p5_unsupported_or_resource_exceeding.json")
    device = load_device_profile(ROOT / "configs" / "devices" / "container_baseline.json")
    result = selector.select(policy, device, 64)
    assert not result.accepted
    assert result.selected_backend is None
