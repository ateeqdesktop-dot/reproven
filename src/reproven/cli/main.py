from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from reproven.domain.models import Verdict
from reproven.manifest.loader import ManifestError, load_manifest
from reproven.reports import to_json, to_junit, to_markdown, to_sarif
from reproven.verify import verify

_EXIT_CODES = {
    Verdict.REPRODUCED: 0,
    Verdict.MISMATCH: 10,
    Verdict.NOT_REPRODUCIBLE: 11,
    Verdict.INCONCLUSIVE: 12,
    Verdict.INVALID_MANIFEST: 20,
}


def _write_output(text: str, output: Path | None) -> None:
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="reproven", description="Verify release reproducibility locally.")
    sub = parser.add_subparsers(dest="command", required=True)
    verify_parser = sub.add_parser("verify", help="verify an artifact from a manifest")
    verify_parser.add_argument("manifest", type=Path)
    verify_parser.add_argument("--workspace", type=Path, default=Path.cwd())
    verify_parser.add_argument("--format", choices=["json", "markdown", "sarif", "junit"], default="markdown")
    verify_parser.add_argument("--output", type=Path)
    inspect_parser = sub.add_parser("inspect", help="inspect an evidence JSON file")
    inspect_parser.add_argument("evidence", type=Path)
    args = parser.parse_args(argv)

    if args.command == "inspect":
        try:
            payload = json.loads(args.evidence.read_text(encoding="utf-8"))
            print(json.dumps({"verdict": payload.get("verdict"), "reason_codes": payload.get("reason_codes", []), "run_id": payload.get("run_id")}, indent=2))
            return 0
        except (OSError, json.JSONDecodeError) as exc:
            print(f"reproven: cannot inspect evidence: {exc}", file=sys.stderr)
            return 20

    try:
        manifest, manifest_sha = load_manifest(args.manifest)
        evidence = verify(manifest, manifest_sha, args.workspace.resolve())
    except ManifestError as exc:
        print(f"reproven: invalid manifest: {exc}", file=sys.stderr)
        return 20
    except (OSError, ValueError) as exc:
        print(f"reproven: verification error: {exc}", file=sys.stderr)
        return 30

    rendered = {"json": to_json, "markdown": to_markdown, "sarif": to_sarif, "junit": to_junit}[args.format](evidence)
    _write_output(rendered, args.output)
    return _EXIT_CODES[evidence.verdict]


if __name__ == "__main__":
    raise SystemExit(main())
