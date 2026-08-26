from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from reproven.builders.local import run_local
from reproven.domain.models import Evidence, Manifest, ReasonCode, Verdict
from reproven.domain.utils import safe_path, sha256_file


def verify(manifest: Manifest, manifest_sha256: str, workspace: Path) -> Evidence:
    run_id = uuid4().hex
    reasons: list[ReasonCode] = []
    source_path = safe_path(workspace, manifest.source.path)
    artifact_path = safe_path(workspace, manifest.artifact.path)
    source_digest: str | None = None
    actual_digest: str | None = None
    execution = None

    if not source_path.exists():
        return Evidence(
            run_id=run_id,
            verdict=Verdict.NOT_REPRODUCIBLE,
            reason_codes=[ReasonCode.SOURCE_MISSING],
            manifest_sha256=manifest_sha256,
            expected_sha256=manifest.artifact.sha256,
        )
    source_digest = sha256_file(source_path) if source_path.is_file() else None

    if manifest.policy.require_isolation and manifest.build.isolation != "container":
        reasons.append(ReasonCode.OPTIONAL_CHECK_SKIPPED)
        return Evidence(
            run_id=run_id,
            verdict=Verdict.INCONCLUSIVE,
            reason_codes=reasons,
            manifest_sha256=manifest_sha256,
            expected_sha256=manifest.artifact.sha256,
            source_sha256=source_digest,
        )
    if manifest.build.network and not manifest.policy.allow_network:
        return Evidence(
            run_id=run_id,
            verdict=Verdict.INVALID_MANIFEST,
            reason_codes=[ReasonCode.INVALID_COMMAND],
            manifest_sha256=manifest_sha256,
            expected_sha256=manifest.artifact.sha256,
            source_sha256=source_digest,
        )

    execution = run_local(manifest.build, workspace, manifest.policy.max_output_bytes)
    if execution.tool_missing:
        verdict = Verdict.INCONCLUSIVE
        reasons.append(ReasonCode.TOOL_MISSING)
    elif execution.timed_out:
        verdict = Verdict.NOT_REPRODUCIBLE
        reasons.append(ReasonCode.BUILD_TIMEOUT)
    elif execution.returncode != 0 or not artifact_path.exists() or not artifact_path.is_file():
        verdict = Verdict.NOT_REPRODUCIBLE
        reasons.append(ReasonCode.BUILD_FAILED)
    else:
        actual_digest = sha256_file(artifact_path)
        if actual_digest == manifest.artifact.sha256:
            verdict = Verdict.REPRODUCED
            reasons.append(ReasonCode.DIGEST_MATCH)
        else:
            verdict = Verdict.MISMATCH
            reasons.append(ReasonCode.DIGEST_MISMATCH)

    if manifest.policy.require_provenance and manifest.provenance is None:
        verdict = Verdict.INCONCLUSIVE
        reasons.append(ReasonCode.PROVENANCE_MISMATCH)

    return Evidence(
        run_id=run_id,
        verdict=verdict,
        reason_codes=reasons,
        manifest_sha256=manifest_sha256,
        expected_sha256=manifest.artifact.sha256,
        actual_sha256=actual_digest,
        source_sha256=source_digest,
        execution=execution,
        provenance=manifest.provenance,
        metadata={"workspace": str(workspace), "artifact_kind": manifest.artifact.kind},
    )
