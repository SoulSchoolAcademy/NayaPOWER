"""Cold-retrieve drill bank — behavioral regression gate.

The drill bank (tools/cold_retrieve_drill/drill_bank.json) is the measured
behavioral contract for the KNOW path: a cold query must return the exact
expected Smart Note against the live corpus. These tests pin the contract
so a scoring regression fails in CI instead of silently degrading retrieval.

Evidence: 2026-10-08 drill run on main 77e86701 — 4/4 exact-ID hits,
4/4 application grades PASS, boundary checks green
(tools/cold_retrieve_drill/drill_log.jsonl).
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRILL_DIR = ROOT / "tools" / "cold_retrieve_drill"


def _load_retrieve():
    # Mirror script execution: tools/ must be importable for sibling modules
    # (truth_state_guard, etc.) that smart_note_v2.py imports.
    tools_dir = str(ROOT / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    spec = importlib.util.spec_from_file_location(
        "smart_note_v2", ROOT / "tools" / "smart_note_v2.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.retrieve


retrieve = _load_retrieve()


def _bank_items():
    bank = json.loads((DRILL_DIR / "drill_bank.json").read_text(encoding="utf-8"))
    return [i for i in bank["items"] if not i.get("retired")]


BANK = _bank_items()
assert BANK, "drill bank must not be empty"


@pytest.mark.parametrize("item", BANK, ids=[i["id"] for i in BANK])
def test_drill_bank_query_retrieves_expected_note(item):
    """Exact-ID hit: the cold query must return the bank's expected note."""
    result = retrieve(item["query"])
    got = result["retrieved"].get("smart_note_id")
    assert got == item["note_id"], (
        f"drill {item['id']}: query {item['query']!r} retrieved {got}, "
        f"expected {item['note_id']}"
    )
    assert result["retrieved"].get("projection_path"), "retrieved entry needs a path"


@pytest.mark.parametrize("item", BANK, ids=[i["id"] for i in BANK])
def test_drill_bank_retrieval_never_returns_dead_note(item):
    """Servability: retrieval must not surface SUPERSEDED/ARCHIVED/REVOKED notes."""
    result = retrieve(item["query"])
    state = str(result["retrieved"].get("lifecycle_state", "ACTIVE")).upper()
    assert state not in {"SUPERSEDED", "ARCHIVED", "REVOKED"}, (
        f"drill {item['id']}: retrieved dead note in state {state}"
    )


def test_relevance_dominates_authority_compounding_proof():
    """Boundary (falsified 2026-10-06): an additive authority bonus once
    promoted SN-016 (Judgment Rule, RATIFIED) over the relevant note for the
    query "compounding proof". Relevance must win; authority only breaks ties.

    Corpus evolution (2026-10-08): the #1229 consolidation (commit 29afae46c)
    added SN-0531 ("The Falsifiability Battery"), whose nutshell carries the
    exact phrase "compounding proof". It now outranks SN-041 on pure
    relevance — a CANDIDATE winning on relevance alone IS the boundary
    working, not breaking. So this test pins the boundary mechanism, not a
    stale exact ID: (1) the high-authority decoy SN-016 must not win; (2) the
    winner must carry the query's relevance signal in a scored field. If an
    authority bonus ever returns and promotes SN-016 (whose text has no
    "compounding proof" signal), this test fires.
    """
    result = retrieve("compounding proof")
    got = result["retrieved"].get("smart_note_id")
    assert got != "SN-016", (
        "authority regression: SN-016 (RATIFIED) promoted over the relevant note"
    )
    evidence = " ".join([
        str(result["retrieved"].get("title") or ""),
        str(result.get("explanation") or ""),
    ]).lower()
    assert "compounding proof" in evidence, (
        f"winner {got} carries no relevance signal for the query"
    )


def test_zero_relevance_query_fails_closed():
    """Fail-closed: a query matching zero terms must raise
    NO_RELEVANT_INTELLIGENCE, never return a best-effort guess."""
    with pytest.raises(SystemExit) as exc:
        retrieve("zebra xylophone quantum pancake")
    assert "NO_RELEVANT_INTELLIGENCE" in str(exc.value.code)


def test_drill_log_records_latest_run():
    """The drill log is append-only evidence: the latest entry must record a
    real run (week, drill id, corpus SHA, verdict)."""
    log_path = DRILL_DIR / "drill_log.jsonl"
    assert log_path.exists(), "drill_log.jsonl must exist once the drill has run"
    lines = [ln for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert lines, "drill log must not be empty"
    latest = json.loads(lines[-1])
    for key in ("week", "drill_id", "corpus_sha", "retrieved_note_id", "verdict"):
        assert key in latest, f"drill log entry missing {key}"
    assert latest["verdict"] in {"PASS", "FAIL"}
