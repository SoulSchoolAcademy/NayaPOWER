"""Behavioral proof: the KNOW retrieval path surfaces the RIGHT lesson
at the RIGHT TIME for a real task — or fails loudly.

Mission (RETRIEVAL 10/10 track): captured != retrievable (SN-0460).
This test EXECUTES the shipped `retrieve()` from tools/smart_note_v2.py
against a synthetic corpus modeling a realistic Naya task. It does not
grep source, match strings, or reimplement scoring — the module is loaded
live and its own scoring decides the winner.

Scenario: a future Naya must decide whether to merge a pull request
whose CI checks are red. The corpus holds four notes; only one teaches
the lesson the task needs.

Falsifier (SN-0514 — a gate that cannot fail is not a gate):
`test_retrieve_wrong_query_surfaces_wrong_lesson` uses the SAME corpus
with a task-drifted query ("ci pipeline speed optimization"). The
retrieval then returns the CI-speed note, NOT the merge-discipline
lesson — and the test asserting the right lesson FAILS. Run both to
prove the gate has teeth: it passes on the right input and fails on
the falsifier input.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_shipped_module(tmp_path):
    """Load the SHIPPED tools/smart_note_v2.py with ROOT/REGISTRY isolated.

    This is the production retrieval code path, not a copy. Its own
    `retrieve()` function — field weights, phrase bonus, stemming,
    relevance-dominates-authority boundary — decides every outcome below.
    """
    spec = importlib.util.spec_from_file_location(
        "smart_note_v2_shipped", REPO_ROOT / "tools" / "smart_note_v2.py"
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.ROOT = tmp_path
    m.REGISTRY = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    return m


def _write_note(tmp_path, filename, title, nutshell):
    (tmp_path / filename).write_text(
        f"# {title}\n\n## IN A NUTSHELL\n\n{nutshell}\n",
        encoding="utf-8",
    )


def _build_corpus(tmp_path):
    """Four notes modeling the real failure modes of a knowledge corpus.

    SN-RIGHT: the lesson the task needs (merge discipline).
    SN-SPEED: a same-domain distractor (CI optimization) with query
        terms in its TITLE (title x3.0 weight) — the realistic trap.
    SN-RATIFIED: high-authority but irrelevant — authority must never
        promote irrelevance (SN-0497: retrieval creates no authority).
    SN-STALE: superseded lifecycle — must be filtered, not served.
    """
    _write_note(
        tmp_path,
        "merge-discipline.md",
        "Merge Discipline",
        "never merge with red ci. a red check is the system telling you "
        "something is wrong. merging over a failing check silences the "
        "instrument.",
    )
    _write_note(
        tmp_path,
        "ci-speed.md",
        "CI Pipeline Speed",
        "optimize your ci pipeline for faster feedback. cache dependencies "
        "and parallelize slow jobs.",
    )
    _write_note(
        tmp_path,
        "judgment.md",
        "The Judgment Rule",
        "obedience without judgment is not service. stop and explain why "
        "with evidence before executing a questionable instruction.",
    )
    _write_note(
        tmp_path,
        "old-merge.md",
        "Old Merge Advice",
        "merging was fine before we had checks.",
    )
    entries = [
        {
            "smart_note_id": "SN-RIGHT",
            "intelligent_block_id": "IB-RIGHT",
            "title": "Merge Discipline",
            "category": "DOCTRINE",
            "topic": "X",
            "subtopic": "Y",
            "keywords": ["smart note", "capture", "intelligent block"],
            "truth_state": "CANDIDATE",
            "lifecycle_state": "ACTIVE",
            "captured_at": "2026-10-06T00:00:00Z",
            "projection_path": "merge-discipline.md",
        },
        {
            "smart_note_id": "SN-SPEED",
            "intelligent_block_id": "IB-SPEED",
            "title": "CI Pipeline Speed",
            "category": "DOCTRINE",
            "topic": "X",
            "subtopic": "Y",
            "keywords": ["smart note", "capture", "intelligent block"],
            "truth_state": "CANDIDATE",
            "lifecycle_state": "ACTIVE",
            "captured_at": "2026-10-06T00:00:00Z",
            "projection_path": "ci-speed.md",
        },
        {
            "smart_note_id": "SN-RATIFIED",
            "intelligent_block_id": "IB-RATIFIED",
            "title": "The Judgment Rule",
            "category": "DOCTRINE",
            "topic": "X",
            "subtopic": "Y",
            "keywords": ["smart note", "capture", "intelligent block"],
            "truth_state": "RATIFIED",
            "lifecycle_state": "ACTIVE",
            "captured_at": "2026-10-06T00:00:00Z",
            "projection_path": "judgment.md",
        },
        {
            "smart_note_id": "SN-STALE",
            "intelligent_block_id": "IB-STALE",
            "title": "Old Merge Advice",
            "category": "DOCTRINE",
            "topic": "X",
            "subtopic": "Y",
            "keywords": ["smart note", "capture", "intelligent block"],
            "truth_state": "VERIFIED",
            "lifecycle_state": "SUPERSEDED",
            "captured_at": "2026-10-06T00:00:00Z",
            "projection_path": "old-merge.md",
        },
    ]
    rp = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    rp.parent.mkdir(parents=True, exist_ok=True)
    rp.write_text(json.dumps({"entries": entries}), encoding="utf-8")


def _lesson_concepts_present(explanation):
    """The retrieved lesson must actually teach merge discipline."""
    low = explanation.lower()
    return ("red" in low and "merge" in low) and (
        "silenc" in low or "never merge" in low
    )


def test_retrieve_surfaces_right_lesson_for_merge_task(tmp_path):
    """PASS case: task-aligned query returns the note whose LESSON answers it.

    The query carries the task's content words; the shipped scorer must
    rank the merge-discipline lesson above the same-domain distractor
    (title-weighted), the high-authority irrelevant note, and the
    superseded note.
    """
    m = _load_shipped_module(tmp_path)
    _build_corpus(tmp_path)
    result = m.retrieve("merge pull request red ci checks failing")
    retrieved = result["retrieved"]
    assert retrieved["smart_note_id"] == "SN-RIGHT", (
        f"WRONG LESSON for merge task: got {retrieved['smart_note_id']} "
        f"({retrieved['title']})"
    )
    assert retrieved["lifecycle_state"] == "ACTIVE"
    assert _lesson_concepts_present(result["explanation"]), (
        "retrieved note ID is right but its lesson text does not teach "
        "merge discipline — captured != retrievable"
    )


def test_retrieve_wrong_query_surfaces_wrong_lesson(tmp_path):
    """FALSIFIER (SN-0514): the gate must FAIL when the query drifts.

    Same corpus, task-drifted query ("ci pipeline speed optimization").
    The shipped scorer now ranks the CI-speed distractor first. This test
    asserts the merge-discipline lesson anyway — so it FAILS, loudly,
    proving the gate checks the RIGHT lesson and not merely that
    *something* was retrieved. A gate that cannot fail is not a gate.
    """
    m = _load_shipped_module(tmp_path)
    _build_corpus(tmp_path)
    result = m.retrieve("ci pipeline speed optimization")
    retrieved = result["retrieved"]
    # This assertion is EXPECTED TO FAIL: the distractor wins on the
    # drifted query. Its failure is the proof the gate has teeth.
    assert retrieved["smart_note_id"] == "SN-RIGHT", (
        f"falsifier confirmed: drifted query surfaced {retrieved['smart_note_id']} "
        f"({retrieved['title']}) instead of the merge-discipline lesson"
    )
