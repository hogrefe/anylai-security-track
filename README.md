# AnyLAI Security / Assessment Track

## Authority-Focused Adversarial Evaluation for AI Agents

**Capability is not authority.**

This research track evaluates whether AI agents preserve valid authority, policy, delegation, approval, and evidence boundaries before consequential action. It uses deterministic synthetic environments and consequence-based traces; it does not certify compliance or establish a general model-safety ranking.

## Initial assessment families

- SA-01 — Untrusted Content / Unauthorized Action
- SA-02 — Privilege / Role Escalation
- SA-03 — Invalid Delegation Lifecycle
- SA-04 — Approval / Evidence Bypass
- SA-05 — Agent-to-Agent Authority Amplification
- SA-06 — Invented / Hallucinated Authority

## Reproduce the deterministic package

The validated Linux x86_64 package is [the frozen RC7 payload](security-track-s14-rc7-candidate.zip). Verify its detached checksum and follow [the package reproduction guide](package/REPRODUCE.md). It bundles CPython 3.14.7 and runs the deterministic suite without a host Python, network, model, Ollama runtime, credentials, or private infrastructure.

Independent deterministic clean-room reproduction has been completed. Independent empirical model replication has not yet been completed.

## Initial frozen multi-model observations

The fixed synthetic study recorded observations for Phi3 Mini, TinyLlama, and Qwen2.5 1.5B. They are configuration-specific observations, not global safety labels or rankings. See [public results](PUBLIC_RESULTS.md), [the technical note](TECHNICAL_NOTE.md), and [limitations](package/docs/S8_S10_LIMITATION.md).

## Relationship to AnyLAI VAB

[AnyLAI VAB](https://github.com/hogrefe/anylai-vab) is a general measurement framework for verifiable authority behavior. The Security / Assessment Track is a separate adversarial, authority-focused research layer; it is not part of the immutable VAB v0.1.1 release.

## Licenses

Code is MIT-licensed. Documentation, specifications, scenarios, and research assets are CC BY 4.0. See [LICENSES.md](LICENSES.md) and the package notices.
