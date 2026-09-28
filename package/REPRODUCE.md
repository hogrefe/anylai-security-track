# Deterministic reproduction
Supported platform: Linux x86_64 with a Docker-compatible runtime is required only to build this candidate; reproduction uses the bundled CPython 3.14.7 filesystem runtime and needs no host Python, network, model, Ollama service, credentials, or private repository.

From the extracted candidate directory run `./reproduce.sh`. It verifies the complete package manifest and hashes, runs the deterministic public test suite, produces `../rc7-output/reproduction-output.json`, and fails closed on a verification or test error.

S8 and S10 are historical context only. This package does not reproduce, verify, or make empirical claims about their unavailable artifact sets.
