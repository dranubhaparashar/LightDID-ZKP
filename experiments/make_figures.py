from __future__ import annotations

import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_PATH))
sys.path.insert(0, str(ROOT_PATH / "src"))

import matplotlib.pyplot as plt
import pandas as pd

from experiments._paths import FIGURES, RESULTS, SUMMARY


def save_line(df: pd.DataFrame, y: str, ylabel: str, title: str, out_name: str) -> None:
    fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=180)
    for backend, g in df.groupby("backend"):
        g = g.sort_values("attributes")
        ax.plot(g["attributes"], g[y], marker="o", label=backend)
    ax.set_xlabel("Attribute count")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, linewidth=0.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / out_name)
    plt.close(fig)


def main() -> None:
    bbs = pd.read_csv(SUMMARY / "bbs_50run_summary.csv")
    bbs["backend"] = "BBS"
    anon = pd.read_csv(SUMMARY / "anoncreds_50run_summary.csv")
    anon["backend"] = "AnonCreds"
    df = pd.concat([bbs, anon], ignore_index=True)

    save_line(df, "prove_or_present_ms_mean", "Prove/present latency (ms)", "Presentation generation latency", "latency_present.png")
    save_line(df, "verify_ms_mean", "Verify latency (ms)", "Verification latency", "latency_verify.png")
    save_line(df, "vp_bytes", "VP size (bytes)", "Presentation size", "vp_size.png")
    save_line(df, "peak_rss_mb", "Peak RSS (MB)", "Peak resident memory", "peak_rss.png")

    # Selector decisions bar-like plot.
    decisions_path = RESULTS / "selector" / "selector_decisions.csv"
    if decisions_path.exists():
        dec = pd.read_csv(decisions_path)
        mapping = {"REJECT": 0, "BBS": 1, "AnonCreds": 2}
        fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=180)
        ax.bar(dec["policy_id"], [mapping.get(x, 0) for x in dec["selected_backend"]])
        ax.set_yticks([0, 1, 2], ["Reject", "BBS", "AnonCreds"])
        ax.set_xlabel("Policy class")
        ax.set_title("CAPS-ZK selector decisions")
        ax.grid(True, axis="y", linewidth=0.3)
        fig.tight_layout()
        fig.savefig(FIGURES / "selector_decisions.png")
        plt.close(fig)

    print(f"Wrote figures to {FIGURES}")


if __name__ == "__main__":
    main()
