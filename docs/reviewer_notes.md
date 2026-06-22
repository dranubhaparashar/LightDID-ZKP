# Reviewer notes

## Implemented scope

The repository reflects the implemented scope of the manuscript:

- BBS selective-disclosure presentations.
- AnonCreds credential-backed predicate presentations.
- CAPS-ZK policy/resource selector.

## Non-claims

This repository does not claim:

- LightDID-ZKP is a new ZKP scheme.
- LightDID-ZKP is cryptographically stronger than BBS or AnonCreds.
- BBS universally outperforms AnonCreds.
- AnonCreds universally outperforms BBS.
- Bulletproofs were implemented or benchmarked.
- Results establish Android, Raspberry Pi, microcontroller, energy, or physical IoT-device performance.

## Why cost-first selection is unsafe

The `experiments/ablation_study.py` script demonstrates the main selector-safety point. A resource-only selector may choose BBS for a credential-backed predicate request because BBS is smaller for the measured selective-disclosure workload. CAPS-ZK blocks this because BBS is semantically invalid for hidden credential-backed predicate policies unless the predicate was already issuer-certified as a signed disclosed claim.
