# ADR-001: Keep verification local-first and evidence canonical

## Status

Accepted.

## Context

ReProven must be useful without a hosted account and must make its result inspectable after the original CI run. A dashboard-first design would increase operational complexity and create a trust boundary outside the user’s repository.

## Decision

The core product is a Python library and CLI. It accepts versioned manifests, executes argv arrays without a shell, computes SHA-256 digests, applies explicit policy, and emits canonical JSON evidence plus presentation reports. Network and container execution are explicit policy decisions rather than implicit behavior. The domain package exposes protocols so adapters can be added without coupling verdict semantics to a specific ecosystem.

## Consequences

The MVP is easy to run offline, test with fixtures, and embed in GitHub Actions. It does not provide a complete sandbox, a transparency log, or distributed rebuild quorum yet. Those capabilities belong in adapters and future releases, with their security assumptions documented rather than implied.
