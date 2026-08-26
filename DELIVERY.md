# ReProven delivery report

## Delivered repository

The project is published at https://github.com/ateeqdesktop-dot/reproven as a public GitHub repository on the `main` branch. Release `v0.1.0` is available at https://github.com/ateeqdesktop-dot/reproven/releases/tag/v0.1.0 with a wheel and source distribution attached.

## Product decision

ReProven was selected after auditing the account’s existing concentration in AI-agent governance, MCP, trace evidence, and observability. The project adds a distinct release-engineering and software-supply-chain capability: it independently verifies whether a declared artifact can be reproduced from a declared source and build command, then emits an explainable verdict and portable evidence.

## Implemented MVP

The repository contains strict YAML/JSON manifests, SHA-256 artifact verification, a local argv-based runner with timeout and bounded output, fail-closed policy checks, workspace path traversal defense, deterministic JSON evidence, Markdown/SARIF/JUnit reports, stable exit codes, a reusable GitHub Action, Python 3.11–3.13 CI configuration, architecture/security/contribution documentation, and reproduced/mismatch fixtures.

## Verification

The local quality gate passed with 8 tests and 86.81% coverage. Ruff passed, mypy passed after adding official PyYAML stubs, and `python -m build` produced `reproven-0.1.0-py3-none-any.whl` and `reproven-0.1.0.tar.gz`. The README smoke test returned verdict `reproduced` with reason `digest_match` and exit code 0.

The manually dispatched GitHub Actions run was accepted and remained queued during the final observation window; the local quality gate is green, and the workflow is present in the public repository with a `workflow_dispatch` trigger for subsequent execution.

## Intentional MVP limits

Container execution, package-specific inspection beyond the generic file contract, cryptographic signing, transparency logs, and distributed rebuild quorum are explicitly roadmap items. The project does not claim that local subprocess execution is a complete sandbox; this is stated in SECURITY.md and the ADR.
