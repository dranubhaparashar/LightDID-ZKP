# Experiment protocol

The included benchmark summaries use the following reported protocol:

- Environment type: container-baseline only.
- OS/platform: Linux x86_64 container environment.
- Runtime versions: Node.js v22.16.0 and Python 3.13.5.
- BBS library: `@mattrglobal/bbs-signatures` v2.0.0.
- AnonCreds library: `anoncreds` / libanoncreds via Python wrapper.
- Attribute counts: 4, 8, 16, 32, 64.
- Runs: 5 warmup runs and 50 measured runs per configuration.
- Metrics: prove/present latency, verify latency, proof/VP size, and peak RSS.

## Replacing included results

To add new physical-device results, create a new folder such as:

```text
results/device_raspberry_pi_5/
results/device_android_midrange/
results/workstation_cpu/
```

Each folder should include:

1. Raw per-run CSV.
2. Summary CSV.
3. Environment notes.
4. Exact dependency versions.
5. Whether CPU frequency scaling, containerization, and background services were controlled.

Do not overwrite the included container-baseline results unless rerunning the same environment.
