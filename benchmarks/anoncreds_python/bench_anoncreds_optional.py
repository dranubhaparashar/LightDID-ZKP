#!/usr/bin/env python3
"""Optional AnonCreds benchmark entry point.

This script provides a safe harness skeleton. It exits clearly if anoncreds is not
installed. Fill in the credential issuance/presentation calls according to the
installed libanoncreds Python wrapper version before reporting new measurements.
"""
from __future__ import annotations

import argparse
import csv
import sys
import time


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attrs", type=int, default=16)
    parser.add_argument("--runs", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=5)
    args = parser.parse_args()

    try:
        import anoncreds  # noqa: F401
    except Exception:
        print("Missing anoncreds/libanoncreds Python wrapper. Install it before running real backend benchmarks.", file=sys.stderr)
        raise SystemExit(2)

    writer = csv.DictWriter(sys.stdout, fieldnames=["run", "attributes", "present_ms", "verify_ms"])
    writer.writeheader()
    for i in range(args.warmup + args.runs):
        t0 = time.perf_counter()
        # Replace with actual anoncreds presentation creation for the installed wrapper.
        time.sleep(0)
        present_ms = (time.perf_counter() - t0) * 1000

        t1 = time.perf_counter()
        # Replace with actual anoncreds verification for the installed wrapper.
        time.sleep(0)
        verify_ms = (time.perf_counter() - t1) * 1000

        if i >= args.warmup:
            writer.writerow({"run": i - args.warmup + 1, "attributes": args.attrs, "present_ms": present_ms, "verify_ms": verify_ms})


if __name__ == "__main__":
    main()
