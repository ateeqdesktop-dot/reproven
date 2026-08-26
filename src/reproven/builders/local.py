from __future__ import annotations

import subprocess
import time
from pathlib import Path

from reproven.domain.models import BuildSpec, ExecutionResult


def run_local(spec: BuildSpec, workspace: Path, max_output_bytes: int) -> ExecutionResult:
    cwd = (workspace / spec.cwd).resolve()
    if workspace.resolve() not in cwd.parents and cwd != workspace.resolve():
        raise ValueError("build cwd escapes workspace")
    started = time.monotonic()
    try:
        completed = subprocess.run(
            spec.command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=spec.timeout_seconds,
            check=False,
            shell=False,
        )
        out = completed.stdout[:max_output_bytes]
        err = completed.stderr[:max_output_bytes]
        return ExecutionResult(
            command=spec.command,
            returncode=completed.returncode,
            duration_ms=round((time.monotonic() - started) * 1000),
            stdout=out,
            stderr=err,
        )
    except subprocess.TimeoutExpired as exc:
        return ExecutionResult(
            command=spec.command,
            returncode=None,
            duration_ms=round((time.monotonic() - started) * 1000),
            stdout=str(exc.stdout or "")[:max_output_bytes],
            stderr=str(exc.stderr or "")[:max_output_bytes],
            timed_out=True,
        )
    except FileNotFoundError:
        return ExecutionResult(
            command=spec.command,
            returncode=None,
            duration_ms=round((time.monotonic() - started) * 1000),
            stdout="",
            stderr="command not found",
            tool_missing=True,
        )
