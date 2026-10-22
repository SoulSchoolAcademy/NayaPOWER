#!/usr/bin/env python3
"""Tests for the Evidence Scorer — Layer 4 of the Ultimate Decision Machine.

Every test constructs realistic fixtures (intent + options + world-model
cache) and verifies evidence-derived behavior: no guessed numbers, gates
as walls, UNKNOWN instead of fabrication.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import evidence_scorer as es

TOOL = Path(__file__).resolve().parent.parent / "tools" / "evidence_scorer.py"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def fresh_ts():
    return datetime.now(timezone.utc).timestamp()


def make_model(prs, tip_ok=True, mission_seq=()):
    sections = {
        "tip": {"status": "OK" if tip_ok else "UNKNOWN",
                "sha": "abc123", "as_of_utc": "now", "as_of_ts": fresh_ts()},
        "prs": {"status": "OK", "count": len(prs), "prs": prs,
                "as_of_utc": "now", "as_of_ts": fresh_ts()},
        "lanes": {"status": "OK", "lanes": {}, "as_of_utc": "now",
                  "as_of_ts": fresh_ts()},
        "mission": {"status": "OK", "sequencing": list(mission_seq),
                    "as_of_utc": "now", "as_of_ts": fresh_ts()},
    }
    return {"sections": sections}


def pr(number, **kw):
    base = {
        "number": number,
        "title": f"PR #{number}",
        "head_sha": "deadbeef",
        "head_branch": f"naya5/thing-{number}",
        "mergeable": True,
        "draft": False,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=2)).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "user": "SoulSchoolAcademy",
    }
    base.update(kw)
    return base


def make_intent(**kw):
    base = {
        "ok": True,
        "exit_hint": 0,
        "intent_type": "should_merge",
        "intent_description": "decide whether a PR should merge",
        "objective": "decide which PR should merge next",
        "constraints": ["CI green", "IV >= 9.5"],
        "decision_weight": "standard",
        "weight_reason": "reversible, medium stakes",
        "reversibility": "high",
        "stakes": "medium",
        "references": {},
        "grounded_references": {},
        "confidence": 0.9,
    }
    base.update(kw)
    return base


def make_option(oid, source_type, source, title, **kw):
    base = {
        "id": oid,
        "source_type": source_type,
        "source": source,
        "title": title,
        "relevance": 0.7,
        "why": "test option",
        "evidence_links": [],
        "freshness": "now",
    }
    base.update(kw)
    return base


def write_model(model):
    """Write a fixture world model to a temp file; return its path."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    Path(path).write_text(json.dumps(model))
    return path


# ---------------------------------------------------------------------------
# 1. Ranking: merge-ready > draft > user-added, all evidence-carrying
# ---------------------------------------------------------------------------

def test_ranking_merge_ready_beats_draft_beats_user_added():
    model = make_model([
        pr(2410, title="Consolidation", mergeable=True, draft=False),
        pr(2422, title="World model draft", mergeable=None, draft=True),
    ])
    intent = make_intent()
    options = [
        make_option("pr-2410", "pr", "PR #2410", "Merge PR #2410",
                    iv_score=9.5, tests_green=True, files_changed=3,
                    test_count=267),
        make_option("pr-2422", "pr", "PR #2422", "Merge PR #2422 draft",
                    files_changed=2),
        make_option("user-0", "user_added", "user suggestion",
                    "What about rewriting everything?", relevance=None),
    ]
    res = es.score_options(intent, options, model)
    assert res["ok"] and res["exit_hint"] == 0
    ranks = {o["id"]: o["rank"] for o in res["options"]}
    assert ranks["pr-2410"] == 1, ranks
    assert ranks["pr-2422"] == 2, ranks
    assert ranks["user-0"] == 3, ranks
    rec = res["recommendation"]
    assert rec["option_id"] == "pr-2410"
    # Every dimension on every option carries evidence — no bare numbers.
    for o in res["options"]:
        for name, d in o["dimensions"].items():
            if d["value"] is not None:
                assert d["evidence"], f"{o['id']}.{name} has value but no evidence"


# ---------------------------------------------------------------------------
# 2. Hard gates: protected actions are walls
# ---------------------------------------------------------------------------

def test_protected_gate_flags_requires_shawn():
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent(objective="deploy the new build to production tonight",
                         reversibility="low", stakes="consequential",
                         decision_weight="foundational")
    options = [make_option("pr-2400", "pr", "PR #2400", "Deploy to production")]
    res = es.score_options(intent, options, model)
    o = res["options"][0]
    assert o["gated"] is True
    assert o["gate_verdict"] == "REQUIRES_SHAWN"
    assert o["gate_reasons"], "gate must name its reason"
    assert o["rank"] is None, "gated option must never rank"
    assert res["recommendation"] is None, "no recommendation when all gated"
    assert any("HARD GATE" in n for n in res["notes"])


def test_gate_in_constraints_also_fires():
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent(constraints=["needs Shawn's word: production deploy"],
                         objective="ship it")
    options = [make_option("pr-2400", "pr", "PR #2400", "Ship the release")]
    res = es.score_options(intent, options, model)
    assert res["options"][0]["gated"] is True


def test_clean_option_not_gated():
    model = make_model([pr(2410, mergeable=True)])
    intent = make_intent()
    options = [make_option("pr-2410", "pr", "PR #2410", "Merge the consolidation",
                           iv_score=9.5, tests_green=True, files_changed=3)]
    res = es.score_options(intent, options, model)
    assert res["options"][0]["gated"] is False
    assert res["options"][0]["gate_verdict"] == "clear"


def test_prohibition_listing_is_not_a_gate():
    """Layer 2 lists protected gates as constraints ('no production
    deploys') — stating the law is the opposite of requesting the action."""
    model = make_model([pr(2410, mergeable=True)])
    intent = make_intent(constraints=[
        "Protected gates hold: no production deploys, DB writes, "
        "credential/money moves, destructive actions without Shawn's word"])
    options = [make_option("pr-2410", "pr", "PR #2410", "Merge PR #2410",
                           iv_score=9.5, tests_green=True, files_changed=3)]
    res = es.score_options(intent, options, model)
    o = res["options"][0]
    assert o["gated"] is False, o["gate_reasons"]
    assert res["recommendation"] is not None


def test_constraint_requesting_gate_fires():
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent(constraints=["this requires production deploy"],
                         objective="ship the release")
    options = [make_option("pr-2400", "pr", "PR #2400", "Ship the release")]
    res = es.score_options(intent, options, model)
    assert res["options"][0]["gated"] is True


def test_genuine_request_after_prohibition_sentence_fires():
    """A prohibition in one sentence must not silence a real request in
    the next — gates fail closed, never open."""
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent(
        constraints=["no production deploys without approval. "
                     "Deploy to production needs Shawn's word."],
        objective="ship the release")
    options = [make_option("pr-2400", "pr", "PR #2400", "Ship the release")]
    res = es.score_options(intent, options, model)
    assert res["options"][0]["gated"] is True


# ---------------------------------------------------------------------------
# 3. UNKNOWN instead of guessing
# ---------------------------------------------------------------------------

def test_unknown_mergeability_withholds_mission_value():
    model = make_model([pr(2422, mergeable=None, draft=False)])
    intent = make_intent()
    options = [make_option("pr-2422", "pr", "PR #2422", "Merge PR #2422",
                           files_changed=2)]
    res = es.score_options(intent, options, model)
    o = res["options"][0]
    assert o["dimensions"]["mission_value"]["value"] is None
    assert "mission_value" in o["unknown_dimensions"]
    assert o["total"] is not None, "other dimensions still combine"


def test_unknown_cost_never_guessed():
    model = make_model([pr(2410, mergeable=True)])
    intent = make_intent()
    options = [make_option("pr-2410", "pr", "PR #2410", "Merge PR #2410")]
    res = es.score_options(intent, options, model)
    cost = res["options"][0]["dimensions"]["cost"]
    assert cost["value"] is None
    assert any("refusing to guess" in e for e in cost["evidence"])


def test_no_world_model_exits_2():
    res = es.score_options(make_intent(),
                           [make_option("a", "pr", "PR #1", "x")], None)
    assert res["exit_hint"] == 2
    assert res["ok"] is False


def test_no_options_exits_2():
    res = es.score_options(make_intent(), [], make_model([]))
    assert res["exit_hint"] == 2


def test_bad_intent_exits_2():
    res = es.score_options({"ok": False, "exit_hint": 2}, [
        make_option("a", "pr", "PR #1", "x")], make_model([]))
    assert res["exit_hint"] == 2


# ---------------------------------------------------------------------------
# 4. Evidence strength is mechanical
# ---------------------------------------------------------------------------

def test_evidence_rewards_iv_and_punishes_draft():
    model = make_model([
        pr(2410, mergeable=True, draft=False),
        pr(2422, mergeable=True, draft=True),
    ])
    intent = make_intent()
    options = [
        make_option("pr-2410", "pr", "PR #2410", "Merge",
                    iv_score=9.5, tests_green=True, files_changed=3),
        make_option("pr-2422", "pr", "PR #2422", "Merge draft",
                    files_changed=2),
    ]
    res = es.score_options(intent, options, model)
    by_id = {o["id"]: o for o in res["options"]}
    e1 = by_id["pr-2410"]["dimensions"]["evidence"]
    e2 = by_id["pr-2422"]["dimensions"]["evidence"]
    assert e1["value"] > e2["value"], (e1, e2)
    assert any("9.5" in ev for ev in e1["evidence"])
    assert any("draft" in ev.lower() for ev in e2["evidence"])


def test_risk_rises_with_irreversibility():
    model = make_model([pr(2410, mergeable=True)])
    low_rev = make_intent(reversibility="low", decision_weight="foundational")
    high_rev = make_intent(reversibility="high", decision_weight="five-minute")
    opt = lambda: [make_option("pr-2410", "pr", "PR #2410", "Merge",
                               files_changed=25)]
    r_low = es.score_options(low_rev, opt(), model)["options"][0]["dimensions"]["risk"]
    r_high = es.score_options(high_rev, opt(), model)["options"][0]["dimensions"]["risk"]
    assert r_low["value"] > r_high["value"]
    assert any("low" in e for e in r_low["evidence"])


# ---------------------------------------------------------------------------
# 5. Urgency from sequencing + age
# ---------------------------------------------------------------------------

def test_urgency_blocks_others():
    model = make_model(
        [pr(2410, mergeable=True),
         pr(2411, mergeable=True)],
        mission_seq=[{"name": "sweep", "after": ["#2410"]}])
    intent = make_intent()
    options = [make_option("pr-2410", "pr", "PR #2410", "Merge",
                           files_changed=1),
               make_option("pr-2411", "pr", "PR #2411", "Merge",
                           files_changed=1)]
    res = es.score_options(intent, options, model)
    by_id = {o["id"]: o for o in res["options"]}
    u1 = by_id["pr-2410"]["dimensions"]["urgency"]
    u2 = by_id["pr-2411"]["dimensions"]["urgency"]
    assert u1["value"] > u2["value"], (u1, u2)
    assert any("blocks" in e for e in u1["evidence"])


def test_urgency_old_pr_more_urgent():
    old = pr(2400, mergeable=True,
             created_at=(datetime.now(timezone.utc) - timedelta(days=20)).strftime(
                 "%Y-%m-%dT%H:%M:%SZ"))
    new = pr(2420, mergeable=True)
    model = make_model([old, new])
    intent = make_intent()
    options = [make_option("pr-2400", "pr", "PR #2400", "Merge", files_changed=1),
               make_option("pr-2420", "pr", "PR #2420", "Merge", files_changed=1)]
    res = es.score_options(intent, options, model)
    by_id = {o["id"]: o for o in res["options"]}
    assert by_id["pr-2400"]["dimensions"]["urgency"]["value"] > \
        by_id["pr-2420"]["dimensions"]["urgency"]["value"]


# ---------------------------------------------------------------------------
# 6. Combination math + weight hook
# ---------------------------------------------------------------------------

def test_weights_dict_present_for_layer6():
    assert set(es.WEIGHTS) == {"mission_value", "evidence", "risk", "cost",
                               "urgency"}
    assert es.WEIGHTS["risk"] < 0 and es.WEIGHTS["cost"] < 0
    assert es.WEIGHTS["mission_value"] > 0
    assert es.WEIGHTS_SCHEMA_VERSION == 1
    src = Path(es.__file__).read_text()
    assert "LAYER 6 HOOK" in src


def test_combination_subtracts_risk_and_cost():
    dims = {
        "mission_value": {"value": 1.0, "evidence": ["e"], "confidence": 1.0},
        "evidence": {"value": 1.0, "evidence": ["e"], "confidence": 1.0},
        "risk": {"value": 0.0, "evidence": ["e"], "confidence": 1.0},
        "cost": {"value": 0.0, "evidence": ["e"], "confidence": 1.0},
        "urgency": {"value": 1.0, "evidence": ["e"], "confidence": 1.0},
    }
    t_safe, _ = es.combine(dims)
    dims["risk"]["value"] = 1.0
    dims["cost"]["value"] = 1.0
    t_risky, _ = es.combine(dims)
    assert t_risky < t_safe, (t_safe, t_risky)


def test_all_unknown_total_is_none():
    dims = {k: {"value": None, "evidence": ["e"], "confidence": 0.3}
            for k in es.WEIGHTS}
    total, conf = es.combine(dims)
    assert total is None
    assert conf == 0.0


def test_confidence_weighted_mean():
    dims = {
        "mission_value": {"value": 0.8, "evidence": ["e"], "confidence": 1.0},
        "evidence": {"value": 0.8, "evidence": ["e"], "confidence": 0.5},
        "risk": {"value": 0.2, "evidence": ["e"], "confidence": 1.0},
        "cost": {"value": None, "evidence": ["e"], "confidence": 0.3},
        "urgency": {"value": 0.4, "evidence": ["e"], "confidence": 1.0},
    }
    total, conf = es.combine(dims)
    assert total is not None
    assert 0.5 < conf < 1.0, conf


# ---------------------------------------------------------------------------
# 7. Freshness degrades confidence
# ---------------------------------------------------------------------------

def test_stale_cache_lowers_confidence():
    old_ts = (datetime.now(timezone.utc) - timedelta(hours=5)).timestamp()
    sections = {
        "tip": {"status": "OK", "sha": "x", "as_of_ts": fresh_ts()},
        "prs": {"status": "OK", "count": 1, "prs": [pr(2410, mergeable=True)],
                "as_of_ts": old_ts},  # 5h old, ttl 600s → stale
    }
    stale_model = {"sections": sections}
    fresh_model = make_model([pr(2410, mergeable=True)])
    intent = make_intent()
    opt = lambda: [make_option("pr-2410", "pr", "PR #2410", "Merge",
                               iv_score=9.5, tests_green=True, files_changed=3)]
    s = es.score_options(intent, opt(), stale_model)["options"][0]
    f = es.score_options(intent, opt(), fresh_model)["options"][0]
    assert s["total_confidence"] < f["total_confidence"], (
        s["total_confidence"], f["total_confidence"])


# ---------------------------------------------------------------------------
# 8. CLI behavior
# ---------------------------------------------------------------------------

def run_cli(payload=None, args=(), env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    inp = json.dumps(payload) if payload is not None else None
    return subprocess.run(
        [sys.executable, str(TOOL), "score", *args],
        input=inp, capture_output=True, text=True, env=env, timeout=30)


def test_cli_scores_end_to_end():
    model = make_model([pr(2410, mergeable=True)])
    path = write_model(model)
    payload = {
        "intent": make_intent(),
        "options": [make_option("pr-2410", "pr", "PR #2410", "Merge PR #2410",
                                iv_score=9.5, tests_green=True, files_changed=3,
                                test_count=267)],
    }
    try:
        r = run_cli(payload, args=["--stdin"], env_extra={"NAYA_WORLD_MODEL": path})
        assert r.returncode == 0, r.stderr
        out = json.loads(r.stdout)
        assert out["ok"] and out["recommendation"]["option_id"] == "pr-2410"
    finally:
        os.unlink(path)


def test_cli_plain_output():
    model = make_model([pr(2410, mergeable=True)])
    path = write_model(model)
    payload = {"intent": make_intent(),
               "options": [make_option("pr-2410", "pr", "PR #2410", "Merge",
                                       iv_score=9.5, files_changed=3)]}
    try:
        r = run_cli(payload, args=["--stdin", "--plain"],
                    env_extra={"NAYA_WORLD_MODEL": path})
        assert r.returncode == 0, r.stderr
        assert "Recommendation" in r.stdout
        assert "mission_value" in r.stdout
    finally:
        os.unlink(path)


def test_cli_bad_json_exits_2():
    r = subprocess.run([sys.executable, str(TOOL), "score", "--stdin"],
                       input="{not json", capture_output=True, text=True,
                       timeout=30)
    assert r.returncode == 2


def test_cli_no_world_model_exits_2():
    payload = {"intent": make_intent(), "options": [
        make_option("a", "pr", "PR #1", "x")]}
    r = run_cli(payload, args=["--stdin"],
                env_extra={"NAYA_WORLD_MODEL": "/tmp/does-not-exist-xyz.json"})
    assert r.returncode == 2
    assert "world model" in r.stdout.lower()


# ---------------------------------------------------------------------------
# 9. Cross-layer integration: real Layer 2 → Layer 3 → Layer 4
# ---------------------------------------------------------------------------

def _load_layer_modules():
    """Locate the real Layer 1/2/3 modules. Prefers the repo tools dir
    (post-merge), falls back to /tmp dev copies, else returns None."""
    import importlib.util
    found = {}
    repo_tools = Path(__file__).resolve().parent.parent / "tools"
    dev_copies = {  # module name -> dev path (this dev session)
        "intent_parser": Path("/tmp/intent_parser.py"),
        "option_miner": Path("/tmp/option_miner.py"),
    }
    for name, dev in dev_copies.items():
        path = repo_tools / f"{name}.py"
        if not path.exists():
            path = dev
        if not path.exists():
            return None
        spec = importlib.util.spec_from_file_location(
            f"layer_{name}", str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        found[name] = mod
    return found


def test_cross_layer_chain_end_to_end():
    layers = _load_layer_modules()
    if layers is None:
        import pytest
        pytest.skip("Layer 2/3 modules not available")
    ip, om = layers["intent_parser"], layers["option_miner"]

    model = make_model([
        pr(2410, title="Decision engine consolidation", mergeable=True,
           draft=False),
        pr(2422, title="World model", mergeable=None, draft=True),
    ])
    cache_path = write_model(model)
    real_cache = Path.home() / ".naya" / "world-model.json"
    had_real = real_cache.exists()
    backup = None
    try:
        # Point every layer at the fixture cache (monkeypatch, no real
        # file touched beyond a temp backup if one existed).
        from pathlib import Path as P
        if had_real:
            backup = real_cache.read_bytes()
        real_cache.parent.mkdir(parents=True, exist_ok=True)
        real_cache.write_text(json.dumps(model))
        ip.WORLD_MODEL_PATH = real_cache
        om.WORLD_MODEL_PATH = real_cache

        intent = ip.parse_intent("should we merge PR #2410 next?")
        assert intent.get("ok"), intent.get("clarifying_questions")
        assert intent["intent_type"] == "should_merge"

        mined = om.mine_options(intent)
        assert mined["ok"], mined["notes"]
        assert mined["options"], "Layer 3 mined zero options"

        result = es.score_options(intent, mined["options"], model)
        assert result["ok"], result["notes"]
        assert result["recommendation"], "Layer 4 recommended nothing"
        assert result["recommendation"]["option_id"] == "merge-pr-2410", \
            result["recommendation"]
        # No bare numbers anywhere in the chain output.
        for o in result["options"]:
            for name, d in o["dimensions"].items():
                if d["value"] is not None:
                    assert d["evidence"], f"{o['id']}.{name}"
    finally:
        os.unlink(cache_path)
        if had_real and backup is not None:
            real_cache.write_bytes(backup)
        elif not had_real and real_cache.exists():
            # Only remove what we created — and only if it's our fixture.
            try:
                if json.loads(real_cache.read_text()).get("sections", {}).get(
                        "tip", {}).get("sha") == "abc123":
                    real_cache.unlink()
            except (json.JSONDecodeError, OSError):
                pass


def test_zero_network_calls():
    # Word-boundary match: "_constraint_requests_gate" contains the
    # substring "requests" but is not the requests library.
    src = Path(es.__file__).read_text()
    for banned in ("urllib", "requests", "http.client", "socket", "gh-api"):
        assert not re.search(r"\b" + re.escape(banned) + r"\b", src), \
            f"network use? {banned}"
    assert "import urllib" not in src and "import requests" not in src


# ---------------------------------------------------------------------------
# 9. Gate-wall hardening — fix-pass tests (natural phrasings must trip the
#    wall; prohibition listings must not). The wall is a tripwire, not a
#    completeness proof — see HEURISTIC BOUNDARY in evidence_scorer.py.
# ---------------------------------------------------------------------------

def _gated_title(title):
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent()
    options = [make_option("opt-1", "pr", "PR #2400", title)]
    return es.score_options(intent, options, model)


def test_gate_delete_the_database_fires():
    """F1: article 'the' must not dodge the wall."""
    o = _gated_title("Delete the database before the migration")["options"][0]
    assert o["gated"] is True
    assert o["gate_verdict"] == "REQUIRES_SHAWN"
    assert o["rank"] is None


def test_gate_delete_the_branch_fires():
    o = _gated_title("Delete the branch naya5/stale")["options"][0]
    assert o["gated"] is True


def test_gate_write_to_the_db_fires():
    """F2: natural word order 'write to the db' must trip the wall."""
    o = _gated_title("Write to the db directly")["options"][0]
    assert o["gated"] is True
    assert o["gate_verdict"] == "REQUIRES_SHAWN"


def test_gate_write_straight_to_db_fires():
    o = _gated_title("Write straight to the db")["options"][0]
    assert o["gated"] is True


def test_gate_ship_it_to_prod_fires():
    """F3: colloquial prod-deploy synonyms must trip the wall."""
    o = _gated_title("Ship it to prod")["options"][0]
    assert o["gated"] is True
    assert o["gate_verdict"] == "REQUIRES_SHAWN"


def test_gate_push_to_production_fires():
    o = _gated_title("Push to production tonight")["options"][0]
    assert o["gated"] is True


def test_gate_drop_the_production_database_fires():
    o = _gated_title("Drop the production database")["options"][0]
    assert o["gated"] is True


def test_gate_send_money_fires():
    o = _gated_title("Send money to the vendor")["options"][0]
    assert o["gated"] is True


def test_gate_nuke_the_repo_fires():
    o = _gated_title("Nuke the repo")["options"][0]
    assert o["gated"] is True


def test_extended_prohibition_listing_still_not_a_gate():
    """Law listings with the new phrasings under prohibition language
    are still the law being stated, not the action being asked for."""
    model = make_model([pr(2410, mergeable=True)])
    intent = make_intent(constraints=[
        "Protected gates hold: no deleting the database, no shipping "
        "to prod, no db writes, no credential moves without Shawn's word"])
    options = [make_option("pr-2410", "pr", "PR #2410", "Merge PR #2410",
                           iv_score=9.5, tests_green=True, files_changed=3)]
    res = es.score_options(intent, options, model)
    o = res["options"][0]
    assert o["gated"] is False, o["gate_reasons"]
    assert res["recommendation"] is not None


def test_unknown_dimensions_listed_in_notes():
    """F5: total_confidence renormalizes over known dims only — the
    report must name the UNKNOWN dims so Layer 5 sees the gap."""
    model = make_model([pr(2422, mergeable=None, draft=False)])
    intent = make_intent()
    options = [make_option("u-1", "pr", "PR #2422", "World model draft",
                           iv_score=9.5, tests_green=True, files_changed=2)]
    res = es.score_options(intent, options, model)
    o = res["options"][0]
    assert o["unknown_dimensions"], "expected at least one UNKNOWN dimension"
    note = " ".join(res["notes"]).lower()
    for dim in o["unknown_dimensions"]:
        assert dim in note, f"UNKNOWN dim '{dim}' not named in notes"


def test_gated_option_still_never_ranks():
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent()
    options = [
        make_option("bad", "pr", "PR #2400", "Delete the database"),
        make_option("good", "pr", "PR #2401", "Merge PR #2401",
                    iv_score=9.5, tests_green=True, files_changed=3),
    ]
    res = es.score_options(intent, options, model)
    assert res["options"][0]["gated"] is True
    assert res["options"][0]["rank"] is None
    assert res["recommendation"]["option_id"] == "good"

def test_gate_delete_our_database_fires():
    """Same defect class as F1: possessive/article must not dodge the wall."""
    o = _gated_title("Delete our database now")["options"][0]
    assert o["gated"] is True


def test_gate_delete_a_branch_fires():
    o = _gated_title("Delete a branch after merge")["options"][0]
    assert o["gated"] is True


def test_gate_drop_our_production_database_fires():
    o = _gated_title("Drop our production database")["options"][0]
    assert o["gated"] is True


def test_gate_rm_rf_fires():
    """Re-IV gap: 'rm -rf' (any target) must trip the wall."""
    for title in ["rm -rf /", "rm -rf the repo", "rm -fr /tmp/data",
                  "Run rm -rf on the directory"]:
        o = _gated_title(title)["options"][0]
        assert o["gated"] is True, title
        assert o["gate_verdict"] == "REQUIRES_SHAWN"
        assert o["rank"] is None


def test_gate_rm_rf_variants_fire():
    o = _gated_title("rm -rfv old_build")["options"][0]
    assert o["gated"] is True


def test_gate_plain_rm_r_stays_out_of_scope():
    """Plain 'rm -r' (no force flag) is out of scope — must not gate."""
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent()
    options = [make_option("opt-1", "pr", "PR #2400", "rm -r old_cache")]
    res = es.score_options(intent, options, model)
    assert res["options"][0]["gated"] is False


def test_gate_kill_production_target_fires():
    """Re-IV gap: 'kill' + production/database/cluster target must trip."""
    for title in ["kill the production database", "kill the cluster",
                  "kill -9 the database", "Kill the db now"]:
        o = _gated_title(title)["options"][0]
        assert o["gated"] is True, title
        assert o["gate_verdict"] == "REQUIRES_SHAWN"
        assert o["rank"] is None


def test_gate_kill_process_stays_out_of_scope():
    """Plain 'kill the process' (no production/data target) stays out."""
    model = make_model([pr(2400, mergeable=True)])
    intent = make_intent()
    options = [make_option("opt-1", "pr", "PR #2400", "kill the process")]
    res = es.score_options(intent, options, model)
    assert res["options"][0]["gated"] is False


def test_gate_no_rm_rf_listing_stays_clean():
    """Law-listing 'no rm -rf' is the law being stated, not requested."""
    model = make_model([pr(2410, mergeable=True)])
    intent = make_intent(constraints=[
        "Protected gates hold: no rm -rf on production, no killing the "
        "cluster without Shawn's word"])
    options = [make_option("pr-2410", "pr", "PR #2410", "Merge PR #2410",
                           iv_score=9.5, tests_green=True, files_changed=3)]
    res = es.score_options(intent, options, model)
    o = res["options"][0]
    assert o["gated"] is False, o["gate_reasons"]
    assert res["recommendation"] is not None


def test_gate_title_prohibition_no_rm_rf_stays_clean():
    """Validator finding: prohibition scoping must apply to option TITLES,
    not just constraints. 'no rm -rf' in a title is the law being stated,
    not an action being requested — it must not gate."""
    o = _gated_title("no rm -rf in this repo")["options"][0]
    assert o["gated"] is False, o["gate_reasons"]
    # ...while the genuine request still gates.
    o2 = _gated_title("rm -rf the repo")["options"][0]
    assert o2["gated"] is True
    assert o2["gate_verdict"] == "REQUIRES_SHAWN"


def test_gate_title_prohibition_never_kill_stays_clean():
    """Validator finding: 'never kill the cluster' as a title is a
    prohibition listing — it must not gate."""
    o = _gated_title("never kill the cluster")["options"][0]
    assert o["gated"] is False, o["gate_reasons"]
    # ...while the genuine request still gates.
    o2 = _gated_title("kill the production database")["options"][0]
    assert o2["gated"] is True
    assert o2["gate_verdict"] == "REQUIRES_SHAWN"


def test_gate_title_prohibition_sentence_scoped():
    """Prohibition in one sentence does not silence a genuine request in
    the title's next sentence (sentence scoping preserved)."""
    o = _gated_title("No deploys without Shawn's word. rm -rf the repo now")["options"][0]
    assert o["gated"] is True, o["gate_reasons"]


def test_gate_threshold_substring_no_longer_exempts():
    """Validator finding (9.0 rejection): 'hold' as a substring prohibition
    marker fired inside 'threshold', silently exempting genuine gate
    mentions. 'hold' is now matched as a standalone word only."""
    o = _gated_title(
        "above the error threshold, drop the production database")["options"][0]
    assert o["gated"] is True, o["gate_reasons"]
    assert o["gate_verdict"] == "REQUIRES_SHAWN"
    o2 = _gated_title(
        "threshold exceeded: delete the database")["options"][0]
    assert o2["gated"] is True, o2["gate_reasons"]
    assert o2["gate_verdict"] == "REQUIRES_SHAWN"


def test_gate_holds_suffix_not_prohibition():
    """'holds' is not the standalone word 'hold': a genuine gate after
    'holds' still gates (the old substring code exempted it)."""
    o = _gated_title(
        "the release holds, deploy to production")["options"][0]
    assert o["gated"] is True, o["gate_reasons"]
    assert o["gate_verdict"] == "REQUIRES_SHAWN"


def test_gate_standalone_hold_still_prohibits():
    """The documented Layer-2 case still holds: standalone 'hold' remains a
    prohibition marker ('Protected gates hold: ...' is the law stated)."""
    o = _gated_title(
        "Protected gates hold: no production deploys")["options"][0]
    assert o["gated"] is False, o["gate_reasons"]
