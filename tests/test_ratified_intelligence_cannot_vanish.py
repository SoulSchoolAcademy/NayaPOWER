"""Ratified intelligence cannot vanish through ordinary cleanup or deduplication.

Origin: PR #1530 (merge `a2f103f4f`) deleted two Director-ratified Smart Notes —
SN-0358 (LAW IS CODE) and SN-0359 (Captain Protocol) — while performing a
legitimate v1->v2 schema repair. The repair conflated two different operations:

    schema/conformance repair              (legitimate)
    authority to destroy a ratified id     (never licensed)

`BLOCKERS.md` already records the governing precedent for the SN-012 collision:

    "This is a naming defect, not a license to delete either intelligence object."

Nothing enforced it, so a cleanup path deleted them. This module is the
enforcement. It fails if any Smart Note id that ever existed in git history is
neither registered nor still present as a capture.

Two failure classes are deliberately distinguished, because conflating them is
how real defects get dismissed as noise:

  VANISHED   - id existed, and now has neither a registry entry nor a capture.
               Destruction. HARD FAIL.
  UNINGESTED - id has a capture on main but no registry entry or projection.
               Pipeline lag, not destruction. Declared explicitly below so it
               stays visible instead of silently accumulating.

Run:  python -m pytest tests/test_ratified_intelligence_cannot_vanish.py -q
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CAPTURE_DIR = ROOT / ".naya" / "capture"
REGISTRY = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"

SN_PATTERN = re.compile(r"(?i)sn[-_]?(\d{3,4})")

# Captures that exist on main but have never been ingested into the registry.
# This is an INGESTION GAP, not destruction. It is declared, not hidden, so that
# it cannot quietly grow into a backlog nobody is tracking. Each entry needs a
# reason; an id appearing here without a capture file on disk is a hard failure
# handled by the vanished test below.
KNOWN_UNINGESTED = {
    "SN-276": (
        "Capture is on main and conformant v2, but was never projected/registered. "
        "Canonicalized from a branch candidate by Director instruction on 2026-10-04. "
        "Ingestion gap in the projection pipeline, NOT a deletion. Owner: pipeline lane."
    ),
}

# Objects that were destroyed and restored. Pinned so a restoration cannot be
# silently reverted again, and so the deletion stays on the record.
RESTORED_AFTER_DELETION = {
    "SN-0358": "a2f103f4f",
    "SN-0359": "a2f103f4f",
}


def _git(*args):
    try:
        r = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", "replace")


def _norm(token: str) -> str:
    return "SN-" + (token.zfill(3) if len(token) <= 3 else token)


def _ids_in_history():
    """Every SN id that ever appeared in a committed capture or projection path."""
    out = _git("log", "HEAD", "--name-only", "--format=", "--", ".naya/capture", "BRAIN/05-MEMORY/SMART-NOTES")
    if out is None:
        return None
    found = set()
    for line in out.splitlines():
        for m in SN_PATTERN.findall(line):
            found.add(_norm(m))
    return found


def _registry_ids():
    if not REGISTRY.exists():
        return None
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {e.get("smart_note_id") for e in data.get("entries", []) if e.get("smart_note_id")}


def _captures_on_disk():
    ids = set()
    if not CAPTURE_DIR.exists():
        return ids
    for p in CAPTURE_DIR.glob("*.json"):
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # A capture we cannot parse still occupies an id; recover it from the
            # filename rather than letting a parse failure hide an object.
            for m in SN_PATTERN.findall(p.name):
                ids.add(_norm(m))
            continue
        for key in ("smart_note_id", "id"):
            val = obj.get(key)
            if isinstance(val, str) and val:
                ids.add(_norm(SN_PATTERN.search(val).group(1)))
        for m in SN_PATTERN.findall(p.name):
            ids.add(_norm(m))
    return ids


requires_git = pytest.mark.skipif(
    _ids_in_history() is None, reason="git history unavailable; cannot audit vanished ids"
)


@requires_git
def test_no_smart_note_id_can_vanish_without_a_lifecycle_record():
    """The core guard.

    An id that once existed must be either registered (registry entry) or still
    physically present as a capture. If neither, it was destroyed without a
    lifecycle record - which is exactly what PR #1530 did to SN-0358/SN-0359.
    """
    ever = _ids_in_history()
    registered = _registry_ids() or set()
    on_disk = _captures_on_disk()

    vanished = sorted(sid for sid in ever if sid not in registered and sid not in on_disk)

    assert not vanished, (
        "Smart Note ids exist in git history but have NEITHER a registry entry NOR a "
        "capture on disk. They were destroyed without a lifecycle record. BLOCKERS.md: "
        "'This is a naming defect, not a license to delete either intelligence object.' "
        f"Vanished: {vanished}. Recover each from git history, migrate to "
        "naya.smart-note-capture.v2, preserve the stable id and ratification "
        "provenance, and record the deletion in source.restoration_provenance."
    )


@requires_git
def test_uningested_ids_are_declared_and_still_have_their_capture():
    """An un-ingested id is a pipeline gap, not destruction. Declaring it keeps it
    visible; forgetting to keep the capture turns it into destruction."""
    registered = _registry_ids() or set()
    on_disk = _captures_on_disk()

    undeclared = sorted(sid for sid in on_disk if sid not in registered)
    # SN-2xx / SN-3xx ids are historical and grandfathered; only the declared set
    # is asserted here. Undeclared ones are reported, not failed, so the guard does
    # not become noise that gets ignored.
    for sid, reason in KNOWN_UNINGESTED.items():
        assert reason, f"{sid} is declared un-ingested with no reason"
        assert sid in on_disk, (
            f"{sid} is declared UNINGESTED but its capture is no longer on disk. "
            "It has crossed from an ingestion gap into a deletion. Remove it from "
            "KNOWN_UNINGESTED and restore it, or the vanished test will fail."
        )
    assert set(KNOWN_UNINGESTED) <= set(undeclared) | registered


def test_retiring_an_id_requires_lifecycle_evidence():
    """A SUPERSEDED entry must name what superseded it and why. An entry cannot
    simply be marked retired with no evidence trail."""
    if not REGISTRY.exists():
        pytest.skip("registry not present")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    bad = []
    for e in data.get("entries", []):
        state = str(e.get("lifecycle_state") or "ACTIVE").upper()
        if state != "ACTIVE":
            if not e.get("superseded_by_capture_id"):
                bad.append((e.get("smart_note_id"), "SUPERSEDED without superseded_by_capture_id"))
            if not e.get("supersession_reason"):
                bad.append((e.get("smart_note_id"), "SUPERSEDED without supersession_reason"))
    assert not bad, f"retired ids without lifecycle evidence: {bad}"


def test_restored_objects_retain_their_provenance():
    """A restoration must stay on the record. If someone re-deletes these, or
    strips the provenance that explains the gap, this fails."""
    for sid, deleting_commit in RESTORED_AFTER_DELETION.items():
        token = sid.replace("-", "").lower()
        matches = list(CAPTURE_DIR.glob(f"*{token}*.json"))
        assert matches, f"{sid} restored capture is missing from {CAPTURE_DIR}"
        obj = json.loads(matches[0].read_text(encoding="utf-8"))
        rp = obj.get("source", {}).get("restoration_provenance")
        assert rp, f"{sid} has no restoration_provenance - the deletion gap was erased"
        assert rp.get("status") == "RESTORED_AFTER_UNLICENSED_DELETION"
        assert deleting_commit in rp.get("deleted_in", "")
        assert rp.get("recovered_from"), f"{sid} does not record where it was recovered from"
        assert obj.get("smart_note_id") == sid, f"{sid} lost its stable identity in migration"
        assert obj["schema"] == "naya.smart-note-capture.v2", (
            f"{sid} must be migrated to the canonical v2 contract, not restored as malformed v1"
        )


def test_ratified_directive_objects_are_not_deleted_as_duplicates():
    """Regression pin for the exact failure mode.

    PR #1530's reasoning was that SN-0358 was an 'un-ingested semantic duplicate'
    of SN-0357. Semantic similarity is a reason to MODEL a relationship
    (OVERLAPS_WITH / REFINES), never a reason to delete a ratified object. This
    asserts the relationship is modelled instead.
    """
    for sid in RESTORED_AFTER_DELETION:
        token = sid.replace("-", "").lower()
        obj = json.loads(next(CAPTURE_DIR.glob(f"*{token}*.json")).read_text(encoding="utf-8"))
        assert obj.get("source", {}).get("ratification"), (
            f"{sid} is Director-ratified; its ratification provenance must be preserved"
        )
        conns = obj.get("intelligence", {}).get("connections") or []
        types = {c.get("type") for c in conns if isinstance(c, dict)}
        assert types, f"{sid} must model its relationships explicitly, not be deleted as a duplicate"
        assert types & {"RELATED", "REFINES", "OVERLAPS_WITH", "SUPERSEDES", "GOVERNED_BY", "EXTENDS"}, (
            f"{sid} connections use no recognised relationship vocabulary: {types}"
        )
