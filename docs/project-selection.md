# Why ReProven?

## Account fit

The account already demonstrates strong work in AI reliability, governance, MCP, trace evidence, privacy-safe artifacts, and CI-native developer tools. That profile is coherent, but it also makes another generic agent gateway, trace viewer, policy engine, or MCP scanner a low-increment choice. ReProven deliberately expands the portfolio into release engineering and software supply-chain verification while reusing the account’s strengths in deterministic evidence, fail-closed behavior, and maintainable Python tooling.

## Market gap

The official [Reproducible Builds tools catalogue](https://reproducible-builds.org/tools/) separates artifact comparison, nondeterminism diagnosis, rebuilding orchestration, backends, and verifiers. The official [SLSA security-level guidance](https://slsa.dev/spec/v1.0/levels) explains provenance and build-platform guarantees, but provenance is not the same as an independently reproduced artifact. ReProven is the small integration and explanation layer between those concerns: it lets a repository or consumer execute a declared build, compare the result, and preserve a portable verdict.

The project is not a replacement for `diffoscope`, `reprotest`, `rebuilderd`, SLSA, in-toto, Sigstore, or a package registry. Its value is the workflow contract around them: a versioned manifest, explicit policy, deterministic evidence, stable exit codes, and CI reports that tell a maintainer why verification succeeded or failed.

## Competitive signal

Large open-source projects such as Langfuse, Phoenix, OpenLLMetry, Helicone, Evidently, TensorZero, NVIDIA SkillSpector, Snyk agent-scan, and ToolHive show strong demand for AI observability and agent security. They also confirm that those categories are crowded and often platform-oriented. ReProven chooses a narrower, developer-first surface with no hosted account and a result that can be reviewed as a file in a pull request.

## Decision matrix

| Criterion | ReProven | DriftLens | AgentBench Relay | Context Provenance Graph | Maintainer Atlas 2 |
|---|---:|---:|---:|---:|---:|
| Originality | 9 | 7 | 7 | 7 | 5 |
| Technical depth | 9 | 8 | 9 | 9 | 6 |
| Real-world value | 10 | 9 | 8 | 8 | 7 |
| Open-source/community potential | 9 | 8 | 8 | 8 | 7 |
| Portfolio/recruiter value | 10 | 9 | 9 | 9 | 7 |
| Testing/CI potential | 10 | 10 | 10 | 8 | 9 |
| Extensibility/long-term value | 10 | 9 | 10 | 10 | 8 |
| **Selected weighted signal** | **67** | **60** | **61** | **59** | **49** |

The full 18-criterion scoring record is retained in the planning audit. ReProven was selected because it has the highest combined value while adding a genuinely different engineering category to the account.

## References

[1]: https://reproducible-builds.org/tools/ — Reproducible Builds, “Tools”.
[2]: https://slsa.dev/spec/v1.0/levels — SLSA, “Security levels”.
[3]: https://arxiv.org/html/2511.20920v1 — Errico, Ngiam, and Sojan, “Securing the Model Context Protocol: Risks, Controls, and Governance”.
