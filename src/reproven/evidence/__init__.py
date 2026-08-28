from __future__ import annotations

import json
from hashlib import sha256
from typing import Any

from pydantic import ValidationError

from reproven.domain.models import Evidence
from reproven.domain.utils import canonical_json


def evidence_payload(evidence: Evidence) -> dict[str, Any]:
    """Return the stable, self-referential-free representation of an evidence capsule."""
    return evidence.model_dump(mode="json", exclude={"evidence_sha256"})


def evidence_fingerprint(evidence: Evidence) -> str:
    return sha256(canonical_json(evidence_payload(evidence))).hexdigest()


def seal_evidence(evidence: Evidence) -> Evidence:
    return evidence.model_copy(update={"evidence_sha256": evidence_fingerprint(evidence)})


def verify_evidence_payload(payload: dict[str, Any]) -> tuple[bool, str]:
    try:
        evidence = Evidence.model_validate(payload)
    except ValidationError as exc:
        return False, f"invalid evidence: {exc}"
    supplied = evidence.evidence_sha256
    if not supplied:
        return False, "evidence has no fingerprint"
    expected = evidence_fingerprint(evidence)
    if supplied != expected:
        return False, "evidence fingerprint mismatch"
    return True, expected


def load_and_verify(text: str) -> tuple[bool, Evidence | None, str]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return False, None, f"invalid JSON: {exc}"
    if not isinstance(payload, dict):
        return False, None, "evidence JSON must be an object"
    ok, detail = verify_evidence_payload(payload)
    if not ok:
        return False, None, detail
    return True, Evidence.model_validate(payload), detail
