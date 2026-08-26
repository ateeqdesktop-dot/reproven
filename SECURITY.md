# Security Policy

ReProven executes commands declared in a manifest. Treat every manifest and source tree as untrusted. The default runner uses `shell=False`, does not grant network access through ReProven policy, bounds captured output, and rejects workspace path escapes. Local execution is not a security sandbox.

For stronger isolation, use a container runner in an environment configured with a non-root user, read-only source mounts, no network, resource limits, and a separate output directory. ReProven will never silently downgrade a requested container isolation mode.

Please do not disclose a suspected vulnerability in a public issue. Open a private security report through GitHub Security Advisories when enabled, or contact the maintainers through the repository profile. Include a minimal reproduction, affected version, impact, and mitigation if known.
