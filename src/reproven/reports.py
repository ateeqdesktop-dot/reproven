from __future__ import annotations

import json
from xml.etree.ElementTree import Element, SubElement, tostring

from reproven.domain.models import Evidence, Verdict


def to_json(evidence: Evidence) -> str:
    return json.dumps(evidence.model_dump(mode="json"), sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def to_markdown(evidence: Evidence) -> str:
    rows = "\n".join(f"| {key} | {value or '-'} |" for key, value in [
        ("Run ID", evidence.run_id),
        ("Verdict", evidence.verdict.value),
        ("Reasons", ", ".join(item.value for item in evidence.reason_codes)),
        ("Expected SHA-256", evidence.expected_sha256),
        ("Actual SHA-256", evidence.actual_sha256),
    ])
    return f"# ReProven verification\n\n| Field | Value |\n|---|---|\n{rows}\n"


def to_sarif(evidence: Evidence) -> str:
    level = "note" if evidence.verdict == Verdict.REPRODUCED else "error"
    result = {"ruleId": "reproven/verdict", "level": level, "message": {"text": evidence.verdict.value}}
    payload = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": [{"tool": {"driver": {"name": "ReProven", "version": "0.2.0"}}, "results": [result]}]}
    return json.dumps(payload, sort_keys=True, indent=2) + "\n"


def to_junit(evidence: Evidence) -> str:
    suite = Element("testsuite", name="reproven", tests="1", failures="0" if evidence.verdict == Verdict.REPRODUCED else "1")
    case = SubElement(suite, "testcase", name=evidence.verdict.value)
    if evidence.verdict != Verdict.REPRODUCED:
        failure = SubElement(case, "failure", message=", ".join(item.value for item in evidence.reason_codes))
        failure.text = to_markdown(evidence)
    return tostring(suite, encoding="unicode") + "\n"
