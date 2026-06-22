from __future__ import annotations

from .selector import CAPSZKSelector
from .types import Policy, VerificationMetadata


def verify_metadata_guard(policy: Policy, vp: VerificationMetadata) -> tuple[bool, str]:
    """Verifier-side metadata guard used by the paper's Algorithm 2.

    This is not a cryptographic verifier. It checks the orchestration metadata
    boundary: nonce/domain binding, policy hash, disclosure set, and absence of
    raw credentials/link secrets in the presentation object.
    """
    expected_hash = CAPSZKSelector.policy_hash(policy)
    if vp.nonce != policy.nonce or vp.domain != policy.domain:
        return False, "nonce/domain mismatch"
    if vp.policy_hash != expected_hash:
        return False, "policy hash mismatch"
    if vp.contains_raw_credential or vp.contains_link_secret:
        return False, "presentation leaks raw credential or link secret"
    if sorted(vp.disclosed_attributes) != sorted(policy.revealed_attributes):
        return False, "disclosed attributes do not match policy"
    return True, "metadata guard passed; run backend cryptographic verifier next"
