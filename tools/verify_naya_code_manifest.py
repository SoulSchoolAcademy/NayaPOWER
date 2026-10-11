#!/usr/bin/env python3
"""Static Naya Code entrypoint checker: not a moral or production runtime proof."""
import json
import sys
from pathlib import Path

REL = "NAYA-ACTIVATION/CONSTITUTION/NAYA-CODE-V1.machine.json"
CANONICAL = ("law_of_one", "operating_code", "operating_law", "value_calculus",
             "value_engine", "act_pipeline", "cold_activation",
             "thinking_curriculum", "mission")
FORMS = ("human_form", "ai_form")


def _file(root, name):
    if not isinstance(name, str) or not name or name.startswith("/") or "\\" in name:
        raise ValueError("unsafe source path")
    target = (root / name).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("source escapes repository")
    return target


def validate(root: Path):
    root = root.resolve()
    try:
        data = json.loads(_file(root, REL).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"manifest invalid: {exc}"]
    failures = []
    if data.get("schema") != "naya.code.entrypoint.v1" or data.get("code_id") != "NAYA-CODE-V1":
        failures.append("incorrect identity")
    if data.get("status") != "DRAFT_NOT_RUNTIME_ENFORCED":
        failures.append("unsupported enforcement claim")
    if data.get("truth_states", {}).get("boot_consumption") != "UNVERIFIED":
        failures.append("boot claims must remain unverified in draft")
    for key in FORMS:
        try:
            path = _file(root, data[key])
            if not path.is_file() or "The Naya Code" not in path.read_text(encoding="utf-8"):
                failures.append(f"missing or incorrect {key}")
        except (KeyError, OSError, ValueError):
            failures.append(f"invalid {key}")
    for key in CANONICAL:
        try:
            if not _file(root, data["canonical_sources"][key]).is_file():
                failures.append(f"missing canonical source: {key}")
        except (KeyError, ValueError):
            failures.append(f"invalid canonical source: {key}")
    doctrines = data.get("doctrine", [])
    if len(doctrines) != 12 or len(set(doctrines)) != len(doctrines):
        failures.append("expected twelve distinct principles")
    if not data.get("hard_boundaries") or len(set(data["hard_boundaries"])) != len(data["hard_boundaries"]):
        failures.append("missing or duplicate hard boundaries")
    if data.get("routing", {}).get("current_board") != "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175":
        failures.append("stale coordination board")
    return failures


if __name__ == "__main__":
    repo = Path(__file__).resolve().parent.parent
    errors = validate(repo)
    if errors:
        for error in errors:
            print("NAYA-CODE FAIL:", error)
        sys.exit(1)
    print("NAYA-CODE STATIC REFERENCES PASS; runtime enforcement NOT PROVEN")
