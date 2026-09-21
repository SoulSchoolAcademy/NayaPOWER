#!/usr/bin/env python3
"""PI-01 acceptance: project identity is derived from canonical events.

The test proves:
CANONICAL EVENT -> PROJECT IDENTITY -> EXISTING PIS INDEX

It does not create a project database and does not treat a file snapshot as
canonical truth.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "project_identity.py"


def load_module():
    spec = importlib.util.spec_from_file_location("project_identity", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        module.EVENT_DIR = root / "events"
        module.PIS_DIR = root / "pis"
        module.INDEX_PATH = root / "INDEX.json"
        module.EVENT_DIR.mkdir()
        module.PIS_DIR.mkdir()

        event = {
            "event_id": "SE-20260920-190000-project-identity",
            "timestamp": "2026-09-20T19:00:00Z",
            "project_id": "NAYA-PROJECT",
            "project": "NAYA-PROJECT",
            "lesson": "Project identity must come from canonical intelligence.",
        }
        (module.EVENT_DIR / "event.json").write_text(
            json.dumps(event) + "\n", encoding="utf-8"
        )
        (module.INDEX_PATH).write_text(
            json.dumps({
                "schema": "naya-power-memory-index/v2",
                "notes": ["SN-20260920-190000-project-identity"],
                "event_index": {
                    event["event_id"]: "SN-20260920-190000-project-identity"
                },
            }) + "\n",
            encoding="utf-8",
        )

        result = module.resolve("NAYA-PROJECT")
        assert result["status"] == "VERIFIED"
        assert result["project_id"] == "NAYA-PROJECT"
        assert result["canonical_events"] == [event["event_id"]]
        assert result["pis_notes"] == ["SN-20260920-190000-project-identity"]
        assert result["rebuildable"] is True

        unknown = module.resolve("DOES-NOT-EXIST")
        assert unknown["status"] == "UNKNOWN"
        assert unknown["reason"] == "NO_CANONICAL_EVENT_BOUND_TO_PROJECT"

        # A conflicting canonical identity must stop rather than guess.
        second = dict(event)
        second["event_id"] = "SE-20260920-190001-project-identity-conflict"
        second["project_id"] = "OTHER-PROJECT"
        (module.EVENT_DIR / "event-2.json").write_text(
            json.dumps(second) + "\n", encoding="utf-8"
        )
        conflict = module.resolve("NAYA-PROJECT")
        assert conflict["status"] == "VERIFIED"

    print("PASS — PI-01 canonical project identity resolution")
    print("PROJECT_IDENTITY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
