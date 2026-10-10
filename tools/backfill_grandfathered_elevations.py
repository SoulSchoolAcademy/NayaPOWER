#!/usr/bin/env python3
"""One-shot backfill: elevation_history for pre-guard Human-Director ratifications.

Why this exists (#1468 follow-through)
--------------------------------------
tools/truth_state_guard.py's read-side audit (audit_registry_semantics) flags
every elevated registry entry that carries no elevation history. On
2026-10-08 the audit found 8 RATIFIED entries with no history at all:
SN-016, SN-0340, SN-0399, SN-0400, SN-0408, SN-0459, SN-0522,
SN-NET-POWER-MAGIC-001.

Investigation (same run) established that all 8 are genuinely ratified: each
entry's provenance records direct ratification by the Human Director (Shawn
Vibert) before the guard existed (2026-10-06). They predate the machine
history format; nothing was hand-escalated. Leaving them history-less means
the CI-wired audit can never pass — or worse, teams learn to ignore it.

What this does
-------------
For each of the 8 entries it appends ONE history record:
  - authority: "Human Director" (the named constitutional authority; the
    audit's anonymous-authority check requires a real name, and this is the
    real one — it is recorded in each entry's provenance).
  - evidence: sha256 of the note's markdown file on main where it exists;
    otherwise sha256 of the recorded ratification statement in provenance.
    Nothing is invented: the hash is always of bytes that exist.
  - kind: "backfill" (never "elevation" — the guard's apply_elevation cannot
    produce CANDIDATE->RATIFIED; only the Human Director can, and did).
  - at: the historical ratification date from provenance (not today);
    recorded_at: today, so the backfill event itself is dated.

Idempotent: entries that already carry elevation_history are skipped.
Dry-run by default; --apply writes the registry. Run from repo root.

This file is a one-shot migration kept for the record, not a runtime tool.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"

# smart_note_id -> (ratification date, authority detail, note file or None)
BACKFILL = {
    "SN-016": ("2026-09-30",
               "Shawn Vibert — Prime 1 Judgment Rule, ratified operating law; lineage recorded in provenance",
               "BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/PRIME-JUDGMENT/SN-016/IB-SMART-NOTE-20260930-sn016-prime-judgment-rule.md"),
    "SN-0340": ("2026-10-05",
                "Shawn Vibert, verbal ratification in main chat 2026-10-05 (provenance: registration bookkeeping for already-ratified law; receipt #1605)",
                "BRAIN/05-MEMORY/SMART-NOTES/2026/10/05/SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-DOCTRINE/SN-0340/IB-SMART-NOTE-20261005-sn0340-the-scorecard-law.md"),
    "SN-0399": ("2026-10-05",
                'Shawn Vibert 2026-10-05: "this is how we roll... this is what is expected... this is the code we operate under" (provenance)',
                "BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-CODE/SN-0399/IB-SMART-NOTE-20261005-sn0399-self-directed-intelligence.md"),
    "SN-0400": ("2026-10-05",
                'Shawn Vibert 2026-10-05: "I don\'t ever want you to be reactive, I always want you to be proactive... make it law" (provenance)',
                "BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-CODE/SN-0400/IB-SMART-NOTE-20261005-sn0400-captain-directive-proactive-always.md"),
    "SN-0408": ("2026-10-05",
                'Shawn Vibert 2026-10-05: "you don\'t delete anything until you understand fully what it is" (provenance)',
                "BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-CODE/SN-0408/IB-SMART-NOTE-20261005-sn0408-deletion-discipline.md"),
    "SN-0459": ("2026-10-06",
                "Shawn Vibert (Human Director), DIRECT_TO_MAIN PR #1654, tip commit 1204519c (provenance)",
                "BRAIN/05-MEMORY/SMART-NOTES/2026/10/06/SYSTEM-INTELLIGENCE/EXECUTION/SN-0459/IB-SMART-NOTE-20261006-sn0459-parallel-execution-directive.md"),
    "SN-0522": ("2026-10-07",
                'Shawn Vibert 2026-10-07: "Make it so. Word." (provenance; PR #1727 registration). Note markdown file absent on main — evidence is the recorded ratification statement, not the note bytes.',
                None),
    "SN-NET-POWER-MAGIC-001": ("2026-10-05",
                "Human Director, DIRECT_TO_MAIN commit 2c34c6e1d 2026-10-05 (provenance)",
                "BRAIN/05-MEMORY/SMART-NOTES/2026/10/05/SYSTEM-INTELLIGENCE/NAYAPOWER-NAYANET-CORE-MAGIC/SN-NET-POWER-MAGIC-001/IB-SMART-NOTE-20261005-NET-POWER-MAGIC-001.md"),
}

CONSTITUTIONAL_BASIS = (
    "Human-Director direct ratification predates the truth-state guard "
    "(2026-10-06). Direct CANDIDATE->RATIFIED is the Human Director's "
    "constitutional prerogative; the guard governs machine paths and does "
    "not — and cannot — govern his word. Recorded so the read-side audit "
    "enforces uniformly on all future writes."
)


def _sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def build_record(entry: dict) -> tuple[dict | None, str]:
    sid = entry.get("smart_note_id")
    spec = BACKFILL.get(sid)
    if spec is None:
        return None, f"{sid}: not in backfill table; skipped"
    if entry.get("elevation_history"):
        return None, f"{sid}: already has elevation_history; skipped"
    state = str(entry.get("truth_state", "")).upper()
    if state != "RATIFIED":
        return None, f"{sid}: truth_state is {state}, not RATIFIED; skipped"
    ratified_at, authority_detail, note_rel = spec
    if note_rel:
        note_path = ROOT / note_rel
        if not note_path.exists():
            return None, f"{sid}: note file missing at {note_rel}; skipped (will not fabricate)"
        ev_hash = _sha256_file(note_path)
        ev_types = ["note-source"]
        ev_sources = [note_rel]
    else:
        prov_text = json.dumps(entry.get("provenance"), sort_keys=True)
        ev_hash = "sha256:" + hashlib.sha256(prov_text.encode("utf-8")).hexdigest()
        ev_types = ["ratification-record"]
        ev_sources = ["registry provenance note (note markdown absent on main)"]
    record = {
        "from": "CANDIDATE",
        "to": "RATIFIED",
        "authority": "Human Director",
        "authority_detail": authority_detail,
        "evidence_hashes": [ev_hash],
        "evidence_types": ev_types,
        "evidence_sources": ev_sources,
        "at": f"{ratified_at}T00:00:00+00:00",
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": "backfill",
        "constitutional_basis": CONSTITUTIONAL_BASIS,
    }
    return record, f"{sid}: backfill record built"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true",
                    help="Write the registry (default is dry-run).")
    ap.add_argument("--registry", default=str(REGISTRY))
    args = ap.parse_args(argv)
    reg_path = Path(args.registry)
    if not reg_path.exists():
        print(f"REGISTRY_NOT_FOUND: {reg_path}", file=sys.stderr)
        return 2
    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    entries = registry.get("entries", [])
    by_id = {str(e.get("smart_note_id")): e for e in entries if isinstance(e, dict)}
    changed = 0
    for sid in BACKFILL:
        entry = by_id.get(sid)
        if entry is None:
            print(f"{sid}: not found in registry; skipped")
            continue
        record, msg = build_record(entry)
        print(msg)
        if record is not None:
            if args.apply:
                entry.setdefault("elevation_history", []).append(record)
            changed += 1
    if args.apply and changed:
        backup = reg_path.with_suffix(".json.backfill-bak")
        backup.write_text(reg_path.read_text(encoding="utf-8"), encoding="utf-8")
        # Match the canonical file format exactly (verified 2026-10-10 against
        # the live registry: indent=2, raw UTF-8, trailing newline). Any other
        # serialization rewrites the whole file and buries the 8 records in
        # a 25k-line diff.
        reg_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print(f"wrote {changed} backfill record(s); backup at {backup.name}")
    else:
        print(f"dry-run: {changed} record(s) would be written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
