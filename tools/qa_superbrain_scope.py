#!/usr/bin/env python3
"""Guard the canonical NayaPOWER Superbrain repository scope."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "START-HERE.md"
RESOLUTION = ROOT / ".naya/NAYA-POWER-SUPERBRAIN-SCOPE-RESOLUTION.md"
BRIEFING = ROOT / ".naya/memory/NAYAPOWER-RUNTIME-BRIEFING.md"
LAW = ROOT / ".naya/NAYA-LAW-SYSTEM-PROTOCOL.md"


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    for path in (START, RESOLUTION, BRIEFING, LAW):
        if not path.is_file():
            return fail(f"missing required scope artifact: {path.relative_to(ROOT)}")

    start = START.read_text(encoding="utf-8")
    resolution = RESOLUTION.read_text(encoding="utf-8")
    briefing = BRIEFING.read_text(encoding="utf-8")
    law = LAW.read_text(encoding="utf-8")

    if "SoulSchoolAcademy/NayaPOWER" not in start:
        return fail("START-HERE does not establish NayaPOWER")
    if "MAXESS PRODUCT WORKSPACE" not in start or "SoulSchoolAcademy/MaxRESULTS" not in start:
        return fail("START-HERE does not distinguish MaxRESULTS as the MAXESS product workspace")
    if "NayaPOWER" not in briefing or "central SuperBrain" not in briefing:
        return fail("Runtime Briefing does not establish NayaPOWER as central SuperBrain")
    if "LEGACY SCOPE AMBIGUITY" not in resolution:
        return fail("scope resolution does not define legacy ambiguity handling")

    # Legacy law text may still contain the historical MaxRESULTS repository
    # declaration. It is acceptable only when the current scope resolution is
    # present and explicit; historical documents are not rewritten merely to
    # erase lineage.
    if "Canonical repository:" in law and "MaxRESULTS" in law and "NayaPOWER" not in law:
        print("WARN: legacy Naya Law contains a MaxRESULTS canonical-repository declaration; current scope resolution governs NayaPOWER Superbrain work without rewriting history.")

    print("PASS — NayaPOWER is the canonical Superbrain; MaxRESULTS is scoped to MAXESS product work; legacy scope ambiguity has an explicit current resolution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
