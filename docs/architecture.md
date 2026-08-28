# ReProven Architecture

## Product contract

ReProven is a local-first verification engine. Given a versioned manifest, it resolves an explicit workspace, validates paths and policy, executes a build command as an argument vector, hashes the declared artifact, compares it with the expected release digest, and emits a canonical evidence capsule. The same capsule can be verified later without rebuilding, provided the referenced evidence and artifact are available.

## Layered design

| Layer | Responsibility | Security boundary |
|---|---|---|
| Manifest/domain | Typed schema, defaults, verdicts, reason codes, policy semantics | Reject malformed or ambiguous input before execution |
| Resolution | Resolve workspace-relative paths and normalize command cwd | Prevent traversal, absolute-path escape, and accidental host writes |
| Runner | Execute argv without a shell, enforce timeout and output bounds | No shell interpolation; explicit network/isolation policy; bounded subprocess |
| Inspection | Hash artifact and inspect known package formats | Never infer trust from filename alone; report unsupported checks explicitly |
| Evidence | Canonical JSON, digests, run metadata, reason codes | Stable serialization supports independent verification |
| Reporting | JSON, Markdown, SARIF, JUnit | Presentation cannot alter domain verdict |
| Integration | CLI and GitHub Action | CI receives deterministic exit semantics and uploadable artifacts |

## Evidence model

An evidence capsule contains schema version, verifier version, manifest digest, policy digest, source declaration, build declaration, expected artifact digest, observed artifact digest, verdict, reason codes, bounded build output digest, timestamps only when explicitly marked non-deterministic metadata, and optional signature metadata. Canonical fields are stable; volatile fields are isolated so consumers can choose reproducibility-sensitive comparison.

## Security model

The default posture is fail closed. Commands are argv arrays and never pass through a shell. Manifest paths must remain inside the declared workspace. The runner applies a timeout and bounded stdout/stderr capture. Network access is denied by policy unless explicitly enabled. A requested isolation mode that cannot be honored must return `inconclusive` or `invalid_manifest`, never silently downgrade to local execution. Verification never executes a command when validating an existing evidence capsule.

The MVP does not claim to be a complete OS sandbox. Documentation will distinguish policy checks from kernel-level isolation and will require a container or external sandbox adapter for hostile build recipes.

## Data and error flow

```text
manifest.yaml
    -> parse + schema validation
    -> path/policy validation
    -> build runner (or evidence-only verifier)
    -> artifact digest + inspector
    -> deterministic verdict + reason codes
    -> canonical evidence capsule
    -> JSON / Markdown / SARIF / JUnit / GitHub Action
```

All expected domain failures become structured verdicts. Programmer errors and unexpected operating-system failures remain visible and are never converted into a false success.

## MVP delivery

The flagship implementation will harden the current MVP with a complete public API, evidence-only verification, deterministic run IDs, provenance and signature hooks, package inspectors for Python wheels and npm tarballs, policy diagnostics, secure report generation, richer fixtures, security regression tests, GitHub Action annotations, release automation, and maintainer documentation.

## Advanced roadmap

1. Container-backed execution with an explicit runtime contract.
2. SLSA/in-toto provenance adapters and Sigstore verification.
3. Rebuild quorum orchestration across independent workers.
4. Reproducibility diagnostics that classify timestamp, path, ordering, and environment drift.
5. Adapters for Cargo, Go modules, OCI images, and generic archives.
6. Optional transparency-log integration that remains separable from the local core.

## Non-goals

ReProven is not a vulnerability database, package registry, hosted build service, generic CI orchestrator, or replacement for cryptographic signing. It complements those systems by independently comparing the release artifact with a fresh build and making the decision reviewable.

