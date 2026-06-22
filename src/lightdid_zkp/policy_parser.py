from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .types import DeviceProfile, Policy, Predicate


def load_policy(path: str | Path) -> Policy:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    predicates = [Predicate(**p) for p in data.get("predicates", [])]
    return Policy(
        policy_id=data["policy_id"],
        name=data["name"],
        semantics=data["semantics"],
        revealed_attributes=data.get("revealed_attributes", []),
        hidden_attributes=data.get("hidden_attributes", []),
        predicates=predicates,
        unlinkability_required=bool(data.get("unlinkability_required", False)),
        min_privacy_level=int(data.get("min_privacy_level", 1)),
        status_required=bool(data.get("status_required", False)),
        nonce=data.get("nonce", "nonce-demo"),
        domain=data.get("domain", "verifier.example"),
        resource_budget=data.get("resource_budget", {}),
        notes=data.get("notes", ""),
    )


def load_device_profile(path: str | Path) -> DeviceProfile:
    data: Dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    return DeviceProfile(
        name=data["name"],
        max_prove_ms=float(data["max_prove_ms"]),
        max_verify_ms=float(data["max_verify_ms"]),
        max_vp_bytes=float(data["max_vp_bytes"]),
        max_rss_mb=float(data["max_rss_mb"]),
        weights=data.get("weights", {"latency": 0.45, "size": 0.35, "memory": 0.20}),
    )
