from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Verdict(str, Enum):
    REPRODUCED = "reproduced"
    MISMATCH = "mismatch"
    NOT_REPRODUCIBLE = "not_reproducible"
    INCONCLUSIVE = "inconclusive"
    INVALID_MANIFEST = "invalid_manifest"


class ReasonCode(str, Enum):
    DIGEST_MATCH = "digest_match"
    DIGEST_MISMATCH = "digest_mismatch"
    BUILD_FAILED = "build_failed"
    BUILD_TIMEOUT = "build_timeout"
    SOURCE_MISSING = "source_missing"
    TOOL_MISSING = "tool_missing"
    PROVENANCE_MISMATCH = "provenance_mismatch"
    INVALID_PATH = "invalid_path"
    INVALID_COMMAND = "invalid_command"
    OPTIONAL_CHECK_SKIPPED = "optional_check_skipped"
    ARTIFACT_MISSING = "artifact_missing"
    EVIDENCE_VERIFIED = "evidence_verified"
    EVIDENCE_TAMPERED = "evidence_tampered"


class ArtifactSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    kind: str = "file"


class SourceSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path: str
    revision: str | None = None


class BuildSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    command: list[str] = Field(min_length=1)
    cwd: str = "."
    timeout_seconds: int = Field(default=120, ge=1, le=3600)
    network: bool = False
    isolation: str = Field(default="local", pattern=r"^(local|container)$")


class PolicySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    require_provenance: bool = False
    require_isolation: bool = False
    allow_network: bool = False
    max_output_bytes: int = Field(default=1_000_000, ge=1024, le=10_000_000)


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: str = Field(default="1", pattern=r"^1$")
    artifact: ArtifactSpec
    source: SourceSpec
    build: BuildSpec
    provenance: dict[str, Any] | None = None
    policy: PolicySpec = Field(default_factory=PolicySpec)


class ExecutionResult(BaseModel):
    command: list[str]
    returncode: int | None
    duration_ms: int
    stdout: str
    stderr: str
    timed_out: bool = False
    tool_missing: bool = False


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: str = "1"
    verifier_version: str = "0.2.0"
    run_id: str
    verdict: Verdict
    reason_codes: list[ReasonCode]
    manifest_sha256: str
    expected_sha256: str
    actual_sha256: str | None = None
    source_sha256: str | None = None
    evidence_sha256: str | None = None
    execution: ExecutionResult | None = None
    provenance: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
