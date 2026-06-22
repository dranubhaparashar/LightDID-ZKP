from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Predicate:
    """A verifier predicate over issuer-certified claims."""

    claim: str
    op: str
    value: Any
    credential_backed: bool = True
    issuer_certified_as_signed_claim: bool = False


@dataclass(frozen=True)
class Policy:
    """Verifier policy P = (A_R, A_H, Phi, L, R, tau, d, kappa, lambda)."""

    policy_id: str
    name: str
    semantics: str
    revealed_attributes: List[str]
    hidden_attributes: List[str]
    predicates: List[Predicate]
    unlinkability_required: bool
    min_privacy_level: int
    status_required: bool
    nonce: str
    domain: str
    resource_budget: Dict[str, float]
    notes: str = ""

    @property
    def requires_predicate(self) -> bool:
        return bool(self.predicates)


@dataclass(frozen=True)
class DeviceProfile:
    """Resource constraint vector D."""

    name: str
    max_prove_ms: float
    max_verify_ms: float
    max_vp_bytes: float
    max_rss_mb: float
    weights: Dict[str, float] = field(
        default_factory=lambda: {"latency": 0.45, "size": 0.35, "memory": 0.20}
    )


@dataclass(frozen=True)
class BackendCapability:
    """Backend capability vector Cap(b)."""

    backend: str
    supports_selective_disclosure: bool
    supports_predicates: bool
    supports_unlinkability: bool
    supports_issuer_binding: bool
    supports_status_policy: bool
    privacy_level: int
    supported_semantics: List[str]
    implemented: bool = True


@dataclass(frozen=True)
class BackendMetrics:
    """Measured resource vector for one backend at one attribute count."""

    backend: str
    attributes: int
    prove_or_present_ms_mean: float
    prove_or_present_ms_std: float
    verify_ms_mean: float
    verify_ms_std: float
    proof_bytes: float
    vp_bytes: float
    peak_rss_mb: float
    runs: int = 50

    @property
    def total_latency_ms(self) -> float:
        return self.prove_or_present_ms_mean + self.verify_ms_mean


@dataclass(frozen=True)
class CredentialMetadata:
    """Holder-side metadata about available credential material."""

    credential_id: str
    issuer_id: str
    available_backends: List[str]
    issuer_public_material_valid: bool = True
    status_path_configured: bool = False
    signed_claims: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class VerificationMetadata:
    """Verifier-side metadata included with a presentation."""

    backend: str
    policy_hash: str
    nonce: str
    domain: str
    disclosed_attributes: List[str]
    hidden_attribute_count: int
    proof_or_presentation_bytes: float
    contains_raw_credential: bool = False
    contains_link_secret: bool = False
