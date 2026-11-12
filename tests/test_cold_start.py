"""Cold-start contract for the weekly cold-retrieve drill (retrieval lane).

A cold successor has zero warm state: no drill log, no caches, no ambient
environment. These tests pin that the drill/retrieve path fires cold and
fails LOUD (never silent-pass) when its preconditions are gone.

Covers:
  C1 drill.py pick() on an all-retired/empty bank -> SystemExit BANK_EMPTY
     (was: cryptic ZeroDivisionError).
  C2 drill.py --show with a missing bank -> non-zero exit, loud error.
  C3 drill.py --show from a pristine CWD, scrubbed env, no drill log ->
     valid drill JSON (drill_id, expected_note_id, know_query,
     application_question).
  C4 smart_note_v2.py retrieve for the week's KNOW query, env scrubbed to
     PATH+HOME only -> exact expected note_id (no ambient-state dependence).
  C5 zero-relevance query in a scrubbed env -> NO_RELEVANT_INTELLIGENCE
     fail-closed.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRILL = ROOT / "tools" / "cold_retrieve_drill" / "drill.py"
BANK = ROOT / "tools" / "cold_retrieve_drill" / "drill_bank.json"
RETRIEVE = ROOT / "tools" / "smart_note_v2.py"
WEEK = 41  # seeded rotation week; deterministic


def load_drill_module():
    spec = importlib.util.spec_from_file_location("cold_drill", DRILL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scrubbed_env():
    home = tempfile.mkdtemp(prefix="cold-test-home-")
    return {"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": home}


def test_pick_empty_bank_raises_bank_empty_loud(tmp_path):
    """C1: all-retired bank must announce BANK_EMPTY, never crash cryptically.

    The real seam is load_bank (filters retired) -> pick: when every item
    is retired the weekly cron must say BANK_EMPTY, not ZeroDivisionError.
    """
    mod = load_drill_module()
    with pytest.raises(SystemExit) as ei:
        mod.pick([], WEEK)
    assert str(ei.value.code) == "BANK_EMPTY"
    retired_bank = tmp_path / "retired_bank.json"
    retired_bank.write_text(json.dumps({"items": [{"id": "x", "retired": True}]}))
    _, items = mod.load_bank(str(retired_bank))
    assert items == []
    with pytest.raises(SystemExit) as ei2:
        mod.pick(items, WEEK)
    assert str(ei2.value.code) == "BANK_EMPTY"


def test_pick_still_round_robins_active_items():
    # pick() operates on the load_bank-filtered list (retired already out).
    mod = load_drill_module()
    items = [{"id": "a"}, {"id": "b"}]
    assert mod.pick(items, 0)["id"] == "a"
    assert mod.pick(items, 1)["id"] == "b"
    assert mod.pick(items, 2)["id"] == "a"


def test_show_missing_bank_fails_loud_not_silent(tmp_path):
    """C2: missing bank -> non-zero exit; a pass it never earned is forbidden."""
    r = subprocess.run(
        [sys.executable, str(DRILL), "--bank", str(tmp_path / "nope.json"), "--show"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode != 0
    assert "FileNotFoundError" in r.stderr or "No such file" in r.stderr


def test_show_cold_pristine_cwd_scrubbed_env_no_log():
    """C3: --show needs no drill log, no warm state, no ambient environment."""
    cold_cwd = tempfile.mkdtemp(prefix="cold-test-cwd-")
    # --show must not read any drill log: the contract holds whether or not
    # one exists (a cold successor has never run a drill).
    r = subprocess.run(
        [sys.executable, str(DRILL), "--bank", str(BANK), "--week", str(WEEK), "--show"],
        cwd=cold_cwd, env=scrubbed_env(), capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, r.stderr[:300]
    d = json.loads(r.stdout)
    for k in ("drill_id", "expected_note_id", "know_query", "application_question"):
        assert d.get(k), f"missing {k}"


def test_retrieve_cold_scrubbed_env_hits_exact_note():
    """C4: scrubbed env (PATH+HOME only) still retrieves the exact expected note."""
    bank = json.loads(BANK.read_text())
    items = [i for i in bank["items"] if not i.get("retired")]
    item = items[WEEK % len(items)]
    r = subprocess.run(
        [sys.executable, str(RETRIEVE), "retrieve", "--query", item["query"]],
        cwd=tempfile.mkdtemp(prefix="cold-test-cwd-"),
        env=scrubbed_env(), capture_output=True, text=True, timeout=300,
    )
    assert r.returncode == 0, (r.stdout + r.stderr)[:300]
    got = json.loads(r.stdout)["retrieved"]["smart_note_id"]
    assert got == item["note_id"], f"got {got}, expected {item['note_id']}"


def test_zero_relevance_fails_closed_when_cold():
    """C5: a query whose tokens match nothing -> NO_RELEVANT_INTELLIGENCE.

    Tokens are pure nonsense: an earlier draft used "no/such/concept" and
    legitimately matched a note — those are real words, not zero relevance.
    """
    r = subprocess.run(
        [sys.executable, str(RETRIEVE), "retrieve",
         "--query", "xqzqw wibblzqrk zzzqqq kkkvvv"],
        cwd=tempfile.mkdtemp(prefix="cold-test-cwd-"),
        env=scrubbed_env(), capture_output=True, text=True, timeout=300,
    )
    assert r.returncode != 0
    assert "NO_RELEVANT_INTELLIGENCE" in (r.stdout + r.stderr)
