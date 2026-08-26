# ReProven

**Local-first, explainable release reproducibility verification.**

ReProven helps maintainers and consumers answer a concrete question: *can this released artifact be reproduced from the declared source and build recipe?* It turns the answer into a deterministic verdict, reason codes, and CI-friendly evidence instead of an opaque pass/fail signal.

## Why ReProven?

Provenance explains how an artifact claims to have been built. ReProven independently runs the declared build, hashes the result, and distinguishes `reproduced`, `mismatch`, `not_reproducible`, `inconclusive`, and `invalid_manifest`. It is intentionally local-first and does not require an account, hosted service, model call, or hidden upload.

## Five-minute demo

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
reproven verify examples/reproduced/manifest.yaml --workspace examples/reproduced --format markdown
```

A successful run returns exit code `0`. A digest mismatch returns `10`, an unsuccessful build returns `11`, an inconclusive verification returns `12`, and invalid input returns `20`.

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

The canonical command form is an argv array. ReProven never evaluates it through a shell. Network access is denied by policy unless explicitly allowed, and requested container isolation is never silently downgraded.

## Architecture

The domain layer owns immutable models, verdict semantics, and reason codes. Adapters handle manifests, source resolution, build execution, artifact inspection, provenance, comparison, evidence, and reports. This keeps the core library testable with fakes and makes ecosystem adapters additive.

## Status

The current MVP implements strict manifests, local execution, exact digest verification, deterministic JSON evidence, Markdown/SARIF/JUnit reports, path defense, bounded output, and a tested CLI. Container execution, package-specific inspectors, signatures, and richer provenance adapters are planned as incremental extensions rather than hidden claims in the MVP.

## Development

```bash
pytest
ruff check .
mypy src
```

ReProven is released under the Apache-2.0 license. Contributions are welcome through issues and pull requests; see `CONTRIBUTING.md` and `SECURITY.md`.
