from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict, List, Tuple

from .cost import normalized_cost
from .registry import nearest_metric
from .types import BackendCapability, BackendMetrics, CredentialMetadata, DeviceProfile, Policy


@dataclass(frozen=True)
class SelectionResult:
    accepted: bool
    selected_backend: str | None
    reason: str
    score: float | None
    candidates: List[str]
    rejected: Dict[str, List[str]]
    policy_hash: str


class CAPSZKSelector:
    """CAPS-ZK policy- and resource-aware backend selector."""

    def __init__(
        self,
        registry: Dict[str, BackendCapability],
        metrics: Dict[Tuple[str, int], BackendMetrics],
        credential_metadata: CredentialMetadata,
    ) -> None:
        self.registry = registry
        self.metrics = metrics
        self.credential_metadata = credential_metadata

    @staticmethod
    def policy_hash(policy: Policy) -> str:
        payload = "|".join(
            [
                policy.policy_id,
                policy.semantics,
                ",".join(policy.revealed_attributes),
                ",".join(policy.hidden_attributes),
                str([(p.claim, p.op, p.value, p.credential_backed) for p in policy.predicates]),
                str(policy.min_privacy_level),
                policy.nonce,
                policy.domain,
            ]
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def select(self, policy: Policy, device: DeviceProfile, attributes: int) -> SelectionResult:
        rejected: Dict[str, List[str]] = {}
        candidates: List[str] = []
        scores: Dict[str, float] = {}

        if not policy.nonce or not policy.domain:
            return SelectionResult(False, None, "freshness/domain binding failed", None, [], {}, self.policy_hash(policy))

        for backend, cap in self.registry.items():
            reasons = self._check_backend(backend, cap, policy, device, attributes)
            if reasons:
                rejected[backend] = reasons
                continue
            metric = nearest_metric(self.metrics, backend, attributes)
            candidates.append(backend)
            scores[backend] = normalized_cost(metric, device)

        if not candidates:
            return SelectionResult(False, None, "no semantically safe and resource-feasible backend", None, [], rejected, self.policy_hash(policy))

        selected_backend = min(candidates, key=lambda b: scores[b])
        return SelectionResult(
            accepted=True,
            selected_backend=selected_backend,
            reason="selected after semantic, privacy, status, issuer-binding, freshness, and resource filters",
            score=scores[selected_backend],
            candidates=candidates,
            rejected=rejected,
            policy_hash=self.policy_hash(policy),
        )

    def _check_backend(
        self,
        backend: str,
        cap: BackendCapability,
        policy: Policy,
        device: DeviceProfile,
        attributes: int,
    ) -> List[str]:
        reasons: List[str] = []
        meta = self.credential_metadata

        if not cap.implemented:
            reasons.append("backend not implemented")
        if backend not in meta.available_backends:
            reasons.append("credential material unavailable for backend")
        if not meta.issuer_public_material_valid or not cap.supports_issuer_binding:
            reasons.append("issuer/credential binding unavailable")
        if policy.semantics not in cap.supported_semantics:
            reasons.append(f"semantic mismatch: policy requires {policy.semantics}")
        if policy.revealed_attributes and not cap.supports_selective_disclosure:
            reasons.append("selective disclosure unsupported")
        if policy.unlinkability_required and not cap.supports_unlinkability:
            reasons.append("unlinkability unsupported")
        if cap.privacy_level < policy.min_privacy_level:
            reasons.append(f"privacy downgrade blocked: {cap.privacy_level} < {policy.min_privacy_level}")
        if policy.status_required and not (cap.supports_status_policy and meta.status_path_configured):
            reasons.append("status/revocation policy path not configured")

        # Predicate safety: BBS must not satisfy hidden credential-backed predicates unless
        # the predicate is certified as a signed disclosed claim.
        if policy.requires_predicate:
            if not cap.supports_predicates:
                safe_disclosed = all(
                    (not p.credential_backed) or p.issuer_certified_as_signed_claim
                    for p in policy.predicates
                )
                if not safe_disclosed:
                    reasons.append("credential-backed predicate unsupported; unsafe fallback blocked")

        if not reasons:
            m = nearest_metric(self.metrics, backend, attributes)
            if m.prove_or_present_ms_mean > min(device.max_prove_ms, policy.resource_budget.get("max_prove_ms", device.max_prove_ms)):
                reasons.append("prove/present latency exceeds budget")
            if m.verify_ms_mean > min(device.max_verify_ms, policy.resource_budget.get("max_verify_ms", device.max_verify_ms)):
                reasons.append("verify latency exceeds budget")
            if m.vp_bytes > min(device.max_vp_bytes, policy.resource_budget.get("max_vp_bytes", device.max_vp_bytes)):
                reasons.append("VP size exceeds budget")
            if m.peak_rss_mb > min(device.max_rss_mb, policy.resource_budget.get("max_rss_mb", device.max_rss_mb)):
                reasons.append("RSS memory exceeds budget")

        return reasons
