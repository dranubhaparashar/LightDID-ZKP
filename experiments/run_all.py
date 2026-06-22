from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "experiments/reproduce_tables.py",
    "experiments/selector_demo.py",
    "experiments/ablation_study.py",
    "experiments/resource_sensitivity.py",
    "experiments/generate_synthetic_raw_runs.py",
    "experiments/make_figures.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(ROOT / script)], check=True)
    print("\nAll LightDID-ZKP experiments completed.")


if __name__ == "__main__":
    main()
