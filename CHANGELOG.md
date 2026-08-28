# Changelog

## [0.2.0] — 2026-08-28

### Added

- Self-referential-free canonical evidence fingerprints for offline verification.
- `reproven verify-evidence` for validating an evidence capsule without executing a build.
- `inspect` now rejects missing or tampered evidence instead of displaying unverified fields.
- Distinct `artifact_missing`, `evidence_verified`, and `evidence_tampered` reason vocabulary.
- Production-oriented architecture documentation and a flagship product positioning guide.
- GitHub Action installation from `${{ github.action_path }}`, SARIF upload, evidence verification output, and uploaded artifacts.
- Regression tests for sealed evidence, tampering, missing artifacts, invalid JSON, and missing files.
- Python 3.11–3.13 CI matrix remains protected by pytest, Ruff, mypy, and package build gates.

### Changed

- Evidence emitted by `verify` is now sealed with a SHA-256 fingerprint.
- Artifact absence is reported separately from a non-zero build exit.
- Development dependencies include PyYAML type stubs and the PEP 517 build frontend.
- README now describes the security boundary, non-goals, CI integration, and roadmap.

## [0.1.0] — 2026-08-26

### Added

- Versioned YAML/JSON manifests with strict schema validation.
- Local argv-based build runner with timeout and bounded output capture.
- SHA-256 artifact verification and stable verdict/exit-code semantics.
- Deterministic JSON evidence and Markdown, SARIF, and JUnit reports.
- Workspace path traversal defense and explicit network/isolation policy checks.
- Reusable GitHub Action, CI matrix, architecture decision record, security policy, and fixture-based tests.
