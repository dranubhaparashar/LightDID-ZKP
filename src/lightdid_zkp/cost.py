from __future__ import annotations

from .types import BackendMetrics, DeviceProfile


def normalized_cost(metrics: BackendMetrics, device: DeviceProfile) -> float:
    """Compute a normalized resource score after feasibility filtering.

    Cost is meaningful only among semantically valid candidates. It must not be
    used to bypass predicate/privacy/resource constraints.
    """
    latency_ratio = (metrics.prove_or_present_ms_mean + metrics.verify_ms_mean) / max(
        device.max_prove_ms + device.max_verify_ms, 1e-9
    )
    size_ratio = metrics.vp_bytes / max(device.max_vp_bytes, 1e-9)
    memory_ratio = metrics.peak_rss_mb / max(device.max_rss_mb, 1e-9)
    w = device.weights
    return (
        float(w.get("latency", 0.45)) * latency_ratio
        + float(w.get("size", 0.35)) * size_ratio
        + float(w.get("memory", 0.20)) * memory_ratio
    )
