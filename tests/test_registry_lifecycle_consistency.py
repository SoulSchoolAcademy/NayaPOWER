"""Lifecycle self-contradiction ratchet (TRUTH seat).

An entry whose own title/topic/subtopic declares it SUPERSEDED or RETIRED
while its lifecycle_state is ACTIVE is a false liveness claim: retrieval
treats ACTIVE entries as live candidates, so a retired fixture stamped
ACTIVE can take retrieval down (2026-11-12: SN-9998/SN-9999, INDEX_CORRUPT,
retrieve() down at the live tip; the backing captures themselves declare
lifecycle_state ACTIVE for a retirement record).

Ratchet, mirroring test_smart_note_registry_drift.py: the count may never
grow past the pinned baseline, and no NEW contradictory id may appear.
Pinned at 2 (the two known fixtures). The cure (re-stamp ACTIVE ->
SUPERSEDED/RETIRED, the inactive states in smart_note_v2) drives the count
to 0 and the test keeps passing. A third supersede repeating the defect
fails the build.

The retirement declaration is read from STRUCTURED fields only -- the
topic/subtopic taxonomy, or the "(lifecycle record)" title marker. A bare
word match on the free-text title was tried first and REJECTED: it flags
SN-0337 ("...Close the Duplicate as SUPERSEDED"), a live lesson ABOUT
superseding, whose taxonomy (SYSTEM-INTELLIGENCE / GOVERNANCE) correctly
says it is not itself superseded. The rule must never flag a lesson for
discussing retirement.
"""

import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path(os.environ.get(
    "TRUTH_REGISTRY_PATH",
    ROOT / ".naya" / "memory" / "smart-notes" / "index.json",
))

RETIREMENT_WORDS = ("superseded", "retired")

# The two known contradictions at pin time (2026-11-12, tip dafc1845).
# Cure removes them; the ratchet passes at 0, 1, or 2 -- but only for
# THESE ids. Any other id failing the rule fails the test.
PINNED_CONTRADICTORY_IDS = frozenset({
    "IB-SMART-NOTE-20261022-sn9998-live-fire-test-lifecycle",
    "IB-SMART-NOTE-20261022-sn9999-live-fire-test-lifecycle",
})
PINNED_MAX = len(PINNED_CONTRADICTORY_IDS)


def _declares_retirement(entry):
    taxonomy = " ".join(
        str(entry.get(k) or "") for k in ("topic", "subtopic")
    ).lower()
    if any(word in taxonomy for word in RETIREMENT_WORDS):
        return True
    return "(lifecycle record)" in str(entry.get("title") or "").lower()


def contradictory_entries(entries):
    """Entries claiming ACTIVE liveness while declaring retirement."""
    return [
        entry for entry in entries
        if str(entry.get("lifecycle_state", "ACTIVE")).upper() == "ACTIVE"
        and _declares_retirement(entry)
    ]


def _load_entries():
    data = json.loads(REGISTRY.read_text())
    if isinstance(data, list):
        return data
    return data.get("entries", [])


def test_live_registry_lifecycle_contradictions_never_grow():
    bad = contradictory_entries(_load_entries())
    ids = [entry.get("intelligent_block_id") for entry in bad]
    assert len(bad) <= PINNED_MAX, (
        f"lifecycle contradictions grew: {PINNED_MAX} -> {len(bad)}: {ids}"
    )
    unknown = sorted(set(ids) - PINNED_CONTRADICTORY_IDS)
    assert not unknown, f"new lifecycle contradictions: {unknown}"


# --- unit shape: the rule itself, no registry IO -------------------------


def _entry(block_id, lifecycle="ACTIVE", title="", topic="", subtopic=""):
    return {
        "intelligent_block_id": block_id,
        "lifecycle_state": lifecycle,
        "title": title,
        "topic": topic,
        "subtopic": subtopic,
    }


def test_retired_title_with_active_lifecycle_is_contradictory():
    entry = _entry("X1", title="SN-9999 — retired test fixture, superseded",
                   subtopic="TEST-FIXTURE-SUPERSEDED")
    assert contradictory_entries([entry]) == [entry]


def test_retired_title_with_superseded_lifecycle_is_clean():
    entry = _entry("X2", lifecycle="SUPERSEDED",
                   title="SN-9999 — retired test fixture, superseded",
                   subtopic="TEST-FIXTURE-SUPERSEDED")
    assert contradictory_entries([entry]) == []


def test_retired_title_with_retired_lifecycle_is_clean():
    entry = _entry("X3", lifecycle="RETIRED",
                   title="SN-9999 — retired test fixture, superseded")
    assert contradictory_entries([entry]) == []


def test_active_lifecycle_with_ordinary_title_is_clean():
    entry = _entry("X4", title="The Discipline Is the Machine",
                   topic="SYSTEM")
    assert contradictory_entries([entry]) == []


def test_lesson_about_superseding_is_clean():
    # SN-0337 shape: a live lesson whose TITLE discusses superseding.
    # Free-text title matching would flag it; the structured taxonomy
    # (SYSTEM-INTELLIGENCE / GOVERNANCE) correctly says it is live.
    entry = _entry("X4b",
                   title="When Lanes Converge: First-Qualifying Repair "
                         "Owns the Class — Close the Duplicate as SUPERSEDED",
                   topic="SYSTEM-INTELLIGENCE", subtopic="GOVERNANCE")
    assert contradictory_entries([entry]) == []


def test_active_unprojected_private_entry_is_clean():
    # ACTIVE + null projection_path alone is NOT a contradiction: a
    # legitimately unprojected PRIVATE note has no projection path.
    # Only the entry's own retirement declaration contradicts ACTIVE.
    entry = _entry("X5", title="Private working note", topic="SYSTEM")
    entry["projection_path"] = None
    assert contradictory_entries([entry]) == []


def test_missing_lifecycle_defaults_active_and_is_flagged():
    entry = _entry("X6", title="Old note, retired",
                   subtopic="TEST-FIXTURE-SUPERSEDED")
    del entry["lifecycle_state"]
    assert contradictory_entries([entry]) == [entry]
