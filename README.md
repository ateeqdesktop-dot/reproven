# ReProven

> **Independent proof that a release is what its source says it is.**

ReProven is a local-first, explainable verifier for software release reproducibility. It independently runs a declared build recipe, hashes the resulting artifact, compares it with the release digest, and emits a portable evidence capsule that a maintainer, reviewer, or downstream consumer can verify later without rebuilding or trusting a hosted dashboard.

## The problem

A signed artifact can prove who signed it. Provenance can describe how a builder claims to have produced it. An SBOM can describe what is inside it. None of those claims alone answers the practical maintainer question: **does this exact downloadable artifact match the source and build recipe that were reviewed?** ReProven closes that loop with an explicit, fail-closed comparison.

## What makes it different

| Property | ReProven behavior |
|---|---|
| Local-first | No account, hosted service, model call, database, or hidden upload is required. |
| Deterministic | Versioned manifests, argv-only commands, canonical JSON, SHA-256 digests, stable reason codes. |
| Explainable | A verdict includes the expected/observed digest, source digest, bounded execution result, and machine-readable reasons. |
| CI-native | JSON, Markdown, SARIF, JUnit, exit codes, and a composite GitHub Action are included. |
| Fail-closed | Unsafe paths, disallowed network, missing isolation, missing artifacts, and malformed manifests cannot silently become success. |
| Portable | Evidence can be inspected and verified offline after the original build has finished. |

## Five-minute demo

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
reproven verify examples/reproduced/manifest.yaml \
  --workspace examples/reproduced \
  --format markdown
```

A successful run returns exit code `0`. A digest mismatch returns `10`, a failed or timed-out build returns `11`, an inconclusive verification returns `12`, invalid input returns `20`, and invalid/tampered evidence returns `21`.

To verify an evidence capsule without executing a build:

```bash
reproven verify-evidence reproven-results/evidence.json
```

## Manifest

```yaml
schema_version: '1'
artifact:
  path: dist/package.whl
  sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
  kind: python-wheel
source:
  path: .
build:
  command: [python, -m, build, --wheel, --no-isolation]
  cwd: .
  timeout_seconds: 300
  network: false
  isolation: local
policy:
  require_provenance: false
  require_isolation: false
  allow_network: false
```

Commands are argv arrays and never pass through a shell. Workspace-relative paths are resolved and checked for escape. Network access is denied unless both the build and policy explicitly allow it. A requested container isolation mode is not silently downgraded.

## GitHub Action

```yaml
- name: Verify release reproducibility
  uses: ateeqdesktop-dot/reproven@main
  with:
    manifest: .reproven/release.yaml
    workspace: .
```

The action writes JSON evidence, SARIF, and JUnit artifacts to `reproven-results/`, then uploads them for review. Pin a release tag or commit SHA in production workflows.

## Architecture

The system is divided into a typed domain layer, manifest and path resolution, a bounded local runner, artifact inspection, evidence sealing, reporting, and CI integration. The core verdict is independent of presentation formats. See [`docs/architecture.md`](docs/architecture.md) and [`docs/adr-001-core-boundaries.md`](docs/adr-001-core-boundaries.md).

## Security boundary

ReProven is a policy-aware verifier, not a complete hostile-build sandbox. Local execution is appropriate for trusted or reviewable recipes. For untrusted builds, use the planned container/external-sandbox adapter and treat `isolation: local` as insufficient. ReProven never claims that reproducibility proves the producer is trustworthy, that dependencies are safe, or that an artifact contains no vulnerability.

Please report vulnerabilities privately according to [`SECURITY.md`](SECURITY.md).

## Development

```bash
pip install -e '.[dev]'
pytest
ruff check .
mypy src
python -m build
```

The test suite includes fixture-based reproduced and mismatch cases, path traversal defenses, malformed manifests, command failures, missing artifacts, evidence tampering, and evidence-only verification. The project targets Python 3.11+ and is released under Apache-2.0.

## Roadmap

The next releases will add container-backed execution with explicit runtime guarantees, SLSA/in-toto provenance adapters, Sigstore verification hooks, reproducibility-drift diagnostics, and ecosystem inspectors for Python wheels, npm tarballs, Cargo packages, Go modules, and OCI images. A remote rebuild quorum and transparency-log integration are intentionally optional layers rather than dependencies of the local core.

## Contributing

Contributions are welcome. Start with [`CONTRIBUTING.md`](CONTRIBUTING.md), reproduce the behavior with a fixture, add a regression test, and keep security assumptions explicit in documentation and release notes.

## License

Apache-2.0. Copyright © 2026 ReProven Contributors.
