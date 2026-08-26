from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from reproven.domain.models import Manifest
from reproven.domain.utils import canonical_json, sha256_bytes


class ManifestError(ValueError):
    pass


def load_manifest(path: Path) -> tuple[Manifest, str]:
    try:
        raw = path.read_text(encoding="utf-8")
        data: Any = json.loads(raw) if path.suffix.lower() == ".json" else yaml.safe_load(raw)
        manifest = Manifest.model_validate(data)
    except (OSError, json.JSONDecodeError, yaml.YAMLError, ValidationError, TypeError) as exc:
        raise ManifestError(str(exc)) from exc
    canonical = canonical_json(manifest.model_dump(mode="json"))
    return manifest, sha256_bytes(canonical)
