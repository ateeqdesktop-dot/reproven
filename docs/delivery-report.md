# ReProven Flagship Delivery Report

## Executive decision

The GitHub audit showed a portfolio with strong but highly concentrated work in AI-agent governance, MCP, telemetry, deterministic evidence, CI analysis, and Arabic AI/OCR quality. The account had 60 public repositories, zero followers, and almost no external adoption signals. The strategic gap was not another adjacent prototype; it was a single understandable, durable, developer-facing flagship with a credible release lifecycle.

The selected foundation was the existing `reproven` repository. It already had the right core idea and could be strengthened without creating another duplicate. Its final product promise is: **independent proof that a release is what its source says it is**.

## Research basis

SLSA describes supply-chain security as incrementally adoptable guidance for producers, consumers, and infrastructure providers, while explicitly identifying code quality, producer trust, and transitive dependency trust as separate concerns [1]. The competitive scan found mature tools for provenance, signing, SBOM/SCA, reproducible builds, and agent governance, but fewer portable repository-level workflows that independently rebuild a declared artifact and produce reviewable evidence for both CI and downstream consumers. Microsoft’s Agent Governance Toolkit demonstrates the adoption potential of a mature multi-language governance product, but its scope is runtime agent control rather than general release reproducibility [2].

## Delivered product

| Area | Delivered outcome |
|---|---|
| Domain model | Strict manifests, explicit verdicts, reason codes, policy fields, and versioned evidence. |
| Security | argv-only subprocess execution, workspace path defense, timeout and output bounds, explicit network/isolation semantics, and no silent downgrade. |
| Evidence | Canonical SHA-256 fingerprint that excludes its own self-reference, plus offline verification through `verify-evidence`. |
| CLI | `verify`, `verify-evidence`, and verified `inspect` flows with JSON, Markdown, SARIF, and JUnit outputs. |
| CI | Python 3.11–3.13 matrix, pytest coverage gate, Ruff, mypy, package build, and action smoke test. |
| GitHub Action | Installs from `github.action_path`, publishes SARIF, uploads evidence artifacts, and records evidence-only verification output. |
| Documentation | Product README, architecture document, ADR, security boundary, roadmap, changelog, and this delivery report. |
| Release | GitHub `v0.2.0` release with wheel and source distribution assets. |

## Verification results

The local release check passed with **12 tests**, **90.35% total coverage**, Ruff clean, mypy clean, and successful wheel/sdist builds. The GitHub Actions run `33170123385` passed all four jobs: quality on Python 3.11, 3.12, and 3.13, plus the action smoke test. The repository working tree is clean after publication.

## Key files

- [`README.md`](../README.md) — product entry point and quick start.
- [`docs/architecture.md`](architecture.md) — system boundaries, security model, flows, and roadmap.
- [`action.yml`](../action.yml) — reusable GitHub Action.
- [`src/reproven/evidence/__init__.py`](../src/reproven/evidence/__init__.py) — evidence sealing and offline verification.
- [`tests/test_reproven.py`](../tests/test_reproven.py) — regression and security-oriented tests.
- [`CHANGELOG.md`](../CHANGELOG.md) — release history.

## Published links

- Repository: https://github.com/ateeqdesktop-dot/reproven
- Release: https://github.com/ateeqdesktop-dot/reproven/releases/tag/v0.2.0
- CI run: https://github.com/ateeqdesktop-dot/reproven/actions/runs/33170123385

## Next maintainer priorities

The next high-value additions are container-backed execution with explicit runtime guarantees, SLSA/in-toto and Sigstore adapters, reproducibility-drift diagnostics, and ecosystem inspectors. These should be introduced as additive adapters behind the stable evidence contract. The project should then seek real users through a small number of focused examples, issue labels, and a tagged-action adoption guide rather than immediately expanding into a hosted control plane.

## References

[1]: https://slsa.dev/spec/v1.0/about "SLSA About"
[2]: https://github.com/microsoft/agent-governance-toolkit "Microsoft Agent Governance Toolkit"
[3]: https://github.com/systempromptio/awesome-ai-agent-governance "Awesome AI Agent Governance"

