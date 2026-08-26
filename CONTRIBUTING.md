# Contributing to ReProven

Thank you for helping make release verification more understandable and reproducible. Before opening a pull request, run `pytest`, `ruff check .`, and `mypy src`. Changes to the manifest schema, verdict semantics, exit codes, or evidence format require an architecture note and a fixture-based regression test.

Keep the domain layer free from subprocess, network, and presentation dependencies. New package ecosystems should implement a small adapter protocol and include golden fixtures for reproduced, mismatch, and inconclusive outcomes. Please explain security assumptions and failure behavior in the pull request description.

By contributing, you agree that your contribution is provided under the Apache-2.0 license.
