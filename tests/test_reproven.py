from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from reproven.cli.main import main
from reproven.domain.utils import canonical_json, safe_path
from reproven.manifest.loader import ManifestError, load_manifest
from reproven.reports import to_json, to_junit, to_markdown, to_sarif
from reproven.verify import verify


def make_manifest(root: Path, expected: str, artifact: str = "artifact.txt") -> Path:
    path = root / "manifest.yaml"
    path.write_text(
        f"""schema_version: '1'
artifact:
  path: {artifact}
  sha256: {expected}
  kind: file
source:
  path: source.txt
build:
  command: [python, -c, "from pathlib import Path; Path('artifact.txt').write_text('stable artifact'+chr(10))"]
  cwd: .
  timeout_seconds: 10
  network: false
  isolation: local
policy:
  require_provenance: false
  require_isolation: false
  allow_network: false
""",
        encoding="utf-8",
    )
    return path


def test_reproduced(tmp_path: Path) -> None:
    (tmp_path / "source.txt").write_text("source\n")
    expected = hashlib.sha256(b"stable artifact\n").hexdigest()
    manifest, manifest_sha = load_manifest(make_manifest(tmp_path, expected))
    evidence = verify(manifest, manifest_sha, tmp_path)
    assert evidence.verdict.value == "reproduced"
    assert "digest_match" in [item.value for item in evidence.reason_codes]
    assert to_json(evidence).endswith("\n")
    assert "ReProven verification" in to_markdown(evidence)
    assert '"version": "2.1.0"' in to_sarif(evidence)
    assert "<testsuite" in to_junit(evidence)


def test_mismatch(tmp_path: Path) -> None:
    (tmp_path / "source.txt").write_text("source\n")
    expected = hashlib.sha256(b"not the output\n").hexdigest()
    manifest, manifest_sha = load_manifest(make_manifest(tmp_path, expected))
    evidence = verify(manifest, manifest_sha, tmp_path)
    assert evidence.verdict.value == "mismatch"


def test_missing_source(tmp_path: Path) -> None:
    expected = hashlib.sha256(b"stable artifact\n").hexdigest()
    manifest, manifest_sha = load_manifest(make_manifest(tmp_path, expected))
    evidence = verify(manifest, manifest_sha, tmp_path)
    assert evidence.verdict.value == "not_reproducible"
    assert evidence.reason_codes[0].value == "source_missing"


def test_safe_path_rejects_escape(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        safe_path(tmp_path, "../outside")


def test_manifest_rejects_invalid_digest(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("artifact:\n  path: a\n  sha256: nope\nsource:\n  path: s\nbuild:\n  command: [echo, ok]\n")
    with pytest.raises(ManifestError):
        load_manifest(path)


def test_canonical_json_is_stable() -> None:
    assert canonical_json({"b": 1, "a": 2}) == canonical_json({"a": 2, "b": 1})


def test_runner_failure_and_cli_outputs(tmp_path: Path) -> None:
    (tmp_path / "source.txt").write_text("source\n")
    manifest_path = tmp_path / "failure.yaml"
    manifest_path.write_text(
        "artifact:\n  path: artifact.txt\n  sha256: "
        + hashlib.sha256(b"x").hexdigest()
        + "\nsource:\n  path: source.txt\nbuild:\n  command: [missing-reproven-command]\n"
    )
    assert main(["verify", str(manifest_path), "--workspace", str(tmp_path), "--format", "json"]) == 12


def test_cli_invalid_manifest(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("not: a manifest\n")
    assert main(["verify", str(bad), "--workspace", str(tmp_path)]) == 20



def test_evidence_is_sealed_and_can_be_verified(tmp_path: Path) -> None:
    (tmp_path / "source.txt").write_text("source\n")
    expected = hashlib.sha256(b"stable artifact\n").hexdigest()
    manifest, manifest_sha = load_manifest(make_manifest(tmp_path, expected))
    evidence = verify(manifest, manifest_sha, tmp_path)
    assert evidence.evidence_sha256
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_text(to_json(evidence), encoding="utf-8")
    assert main(["verify-evidence", str(evidence_path)]) == 0
    assert main(["inspect", str(evidence_path)]) == 0


def test_tampered_evidence_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "source.txt").write_text("source\n")
    expected = hashlib.sha256(b"stable artifact\n").hexdigest()
    manifest, manifest_sha = load_manifest(make_manifest(tmp_path, expected))
    evidence = verify(manifest, manifest_sha, tmp_path)
    payload = evidence.model_dump(mode="json")
    payload["verdict"] = "mismatch"
    path = tmp_path / "tampered.json"
    import json
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert main(["verify-evidence", str(path)]) == 21


def test_missing_artifact_is_distinct_from_build_failure(tmp_path: Path) -> None:
    (tmp_path / "source.txt").write_text("source\n")
    expected = hashlib.sha256(b"stable artifact\n").hexdigest()
    path = make_manifest(tmp_path, expected)
    path.write_text(path.read_text().replace("Path('artifact.txt').write_text('stable artifact'+chr(10))", "pass"), encoding="utf-8")
    manifest, manifest_sha = load_manifest(path)
    evidence = verify(manifest, manifest_sha, tmp_path)
    assert evidence.reason_codes[0].value == "artifact_missing"


def test_invalid_evidence_json_and_missing_file(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("[]", encoding="utf-8")
    assert main(["verify-evidence", str(bad)]) == 21
    assert main(["verify-evidence", str(tmp_path / "missing.json")]) == 20
