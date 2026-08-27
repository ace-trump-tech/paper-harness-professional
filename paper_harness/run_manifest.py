"""Hash artifact files so a resumed CV run can detect external modification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_artifact_manifest(run_dir: Path, artifact_dir: Path, project_id: str) -> Path:
    entries = {path.name: _sha256(path) for path in sorted(Path(artifact_dir).glob("*.json"))}
    target = Path(run_dir) / "artifact-manifest.json"
    target.write_text(json.dumps({"project_id": project_id, "algorithm": "sha256", "artifacts": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def verify_artifact_manifest(run_dir: Path, artifact_dir: Path) -> Dict[str, object]:
    path = Path(run_dir) / "artifact-manifest.json"
    if not path.exists():
        return {"status": "missing"}
    data = json.loads(path.read_text(encoding="utf-8"))
    expected = data.get("artifacts", {})
    changed = [name for name, digest in expected.items() if not (Path(artifact_dir) / name).exists() or _sha256(Path(artifact_dir) / name) != digest]
    return {"status": "valid" if not changed else "changed", "changed": changed}
