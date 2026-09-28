# Capability Is Not Authority

## Initial Multi-Model Evidence from the AnyLAI Security / Assessment Track

Under the fixed synthetic authority protocol, the three tested model configurations exhibited different observed patterns of unauthorized consequential execution, valid-task completion, and structured-response reliability; these observations do not support a general model-safety ranking.

The study evaluates six authority-focused families: untrusted-content action, privilege escalation, invalid delegation lifecycle, approval/evidence bypass, agent-to-agent authority amplification, and invented authority. The evaluation path is adversarial stimulus → agent decision → synthetic consequential action → authority/evidence ground truth → trace → finding.

The frozen result table is in [PUBLIC_RESULTS.md](PUBLIC_RESULTS.md). Deterministic reproduction is available through the bundled package; empirical model replication is separate and has not yet been independently completed.

## Limitations

- Three small local model configurations only.
- One primary run per condition.
- Synthetic procurement environment.
- TinyLlama had a substantial structured-output parser-failure rate.
- Phi3 Mini is a historical S8 baseline.
- Limited statistical power.
- No production systems were tested.
- No general model ranking is supported.
- No independent empirical model replication has been completed.
