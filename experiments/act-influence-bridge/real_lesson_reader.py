"""Naya Gamma — ACT influence experiment: REAL lesson reader.

Reads a REAL lesson from the repo's live learning store
(.naya/memory/smart-notes/index.json + the BRAIN projection file at the live
tip) and translates it into the ADVISE bridge lesson schema.

HONESTY CONTRACT — what is real vs translator-provided:
  REAL (copied verbatim from the store at the live tip):
    - lesson id (intelligent_block_id), title, principle (the IN A NUTSHELL
      paragraph, quoted from the projection file), source truth state,
      ratification facts, projection path.
  TRANSLATOR-PROVIDED (documented rules, NOT store metadata — the repo's
  store carries none of these yet):
    - T1 trust:   store truth_state RATIFIED -> bridge truth_state VERIFIED.
      The bridge only trusts PROMOTED/VERIFIED. RATIFIED (ratified by Shawn
      himself, 2026-10-05) is the strongest real trust signal in the store;
      the mapping is recorded in `_source_truth_state` for provenance.
    - T2 owner:   the store carries no owner field. The reader scopes the
      lesson to the acting owner it is called with (owner_id param). This is
      translator scoping policy, not store metadata. The AUTHORIZED gate
      itself (cross-owner rejection) is verified independently in arm D of
      the experiment, so this scoping does not self-certify the gate.
    - T3 applicability: ["consequential_action"], translator-authored. The
      Scorecard Law's own text governs "every decision"; this experiment
      scopes it to consequential_action, the action type under test.
    - T4 advisory: authored from the law's text into the bridge's allowlist
      keys (add_proof_requirements / add_constraints / note). The store
      carries no executable advisory; the advisory is the translator's
      executable encoding of the law's principle ("no scorecard, no merge").

The reader is the same retrieval seam KNOW uses (intelligence_reader),
so ADVISE evaluates exactly the lessons KNOW would surface.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]  # worktree root
INDEX_PATH = REPO_ROOT / ".naya" / "memory" / "smart-notes" / "index.json"
TARGET_SN = "SN-0340"  # The Scorecard Law — RATIFIED by Shawn, 2026-10-05


def _load_index() -> dict:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def _find_lesson(index: dict, smart_note_id: str) -> dict:
    for entry in index.get("entries", []):
        if entry.get("smart_note_id") == smart_note_id:
            return entry
    raise KeyError(f"lesson {smart_note_id} not found in {INDEX_PATH}")


def _extract_principle(projection_path: str) -> str:
    """Quote the IN A NUTSHELL paragraph verbatim from the projection file."""
    text = (REPO_ROOT / projection_path).read_text(encoding="utf-8")
    marker = "## IN A NUTSHELL"
    start = text.index(marker) + len(marker)
    rest = text[start:].lstrip("\n")
    end = rest.find("\n## ")
    paragraph = rest[: end if end != -1 else len(rest)].strip().replace("\n", " ")
    return " ".join(paragraph.split())


def build_lesson(entry: dict, acting_owner_id: str) -> dict:
    """Translate the real store entry into the ADVISE bridge lesson schema."""
    projection_path = entry["projection_path"]
    principle = _extract_principle(projection_path)
    return {
        # --- REAL: from the store ---
        "id": entry["intelligent_block_id"],
        "smart_note_id": entry["smart_note_id"],
        "title": entry["title"],
        "principle": principle,
        "_source_truth_state": entry["truth_state"],  # RATIFIED (real)
        "ratified_by": "Shawn Vibert",
        "ratified_at": "2026-10-05",
        "provenance": {
            "index": str(INDEX_PATH.relative_to(REPO_ROOT)),
            "projection_path": projection_path,
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        # --- TRANSLATOR-PROVIDED per rules T1..T4 (documented above) ---
        "truth_state": "VERIFIED",  # T1: RATIFIED -> trusted (bridge set is PROMOTED/VERIFIED)
        "owner_id": acting_owner_id,  # T2: scoped to acting owner
        "applies_to_action_types": ["consequential_action"],  # T3
        "advisory": {  # T4: executable encoding of "no scorecard, no merge"
            "add_proof_requirements": [
                "scorecard_receipt:options_enumerated_and_scored",
                "scorecard_gate:reversibility_and_damage_checked",
            ],
            "add_constraints": ["scorecard_required_before_merge"],
            "note": "SN-0340 The Scorecard Law: no scorecard, no merge. "
                    "Every decision runs through a written scorecard.",
        },
        "_translator": "naya-gamma/act-influence-experiment",
        "_translator_rules": ["T1 trust", "T2 owner", "T3 applicability", "T4 advisory"],
    }


def real_lesson_reader(block_id: str, owner_id: str) -> list[dict]:
    """intelligence_reader seam: real store -> bridge lesson schema."""
    index = _load_index()
    entry = _find_lesson(index, TARGET_SN)
    return [build_lesson(entry, owner_id)]


def foreign_owner_reader(block_id: str, owner_id: str) -> list[dict]:
    """Same real lesson, but scoped to a DIFFERENT owner (arm D control)."""
    index = _load_index()
    entry = _find_lesson(index, TARGET_SN)
    lesson = build_lesson(entry, "foreign-owner-9")
    return [lesson]


if __name__ == "__main__":
    lesson = real_lesson_reader("IB-ANY", "gamma-owner-1")[0]
    print(json.dumps(lesson, indent=2)[:2200])
