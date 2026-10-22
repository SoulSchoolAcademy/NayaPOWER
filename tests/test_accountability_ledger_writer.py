"""Tests for tools/accountability_ledger_writer.py — the first writer of
system actions into the one Smart Ledger.

Covered:
- the genesis day (2026-10-22 value-density audit) builds 56 chained
  entries whose hashes verify (mirror of nayanet_smart_ledger_hash);
- efficiency is computed FROM the entries: 8,986 actions / 52 verified
  outcomes / ratio 173 — engagement never counts as an outcome;
- TAMPER NEGATIVE CONTROL: mutating any hashed field, or breaking a chain
  link, makes verify_chain fail;
- shape validation: unverified outcomes, float payloads, and
  self-verification are rejected;
- the rendered SQL calls nayanet_record_ledger_event only — never a direct
  INSERT — one call per entry, owner left as the substitution token;
- no schema change sneaks in: the writer package creates no tables.

The shipped genesis artifacts are built with the owner substitution token
(the real system-owner uuid is assigned in the gated application step);
build_entries is deterministic, so the reviewing seat rebuilds with the
real owner id to verify the post-application read-back.
"""
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITER_PATH = ROOT / "tools" / "accountability_ledger_writer.py"
GENESIS_RECORD = ROOT / "tools" / "accountability_ledger" / "genesis_day_record_2026-10-22.json"
GENESIS_ENTRIES = ROOT / "tools" / "accountability_ledger" / "genesis_entries_2026-10-22.json"
GENESIS_SQL = ROOT / "tools" / "accountability_ledger" / "genesis_writes_2026-10-22.sql"

spec = importlib.util.spec_from_file_location("accountability_ledger_writer", WRITER_PATH)
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)

OWNER = writer.OWNER_TOKEN


def _genesis_record():
    return json.loads(GENESIS_RECORD.read_text(encoding="utf-8"))


def _genesis_entries(owner=OWNER):
    return writer.build_entries(_genesis_record(), owner)


def test_genesis_builds_56_entries_and_chain_verifies():
    entries = _genesis_entries()
    assert len(entries) == 56
    types = {}
    for e in entries:
        types[e["event_type"]] = types.get(e["event_type"], 0) + 1
    assert types == {"outcome_verified": 52, "loop_flagged_zero_output": 3, "run_census": 1}
    assert entries[0]["previous_chain_hash"] is None
    assert writer.verify_chain(entries, OWNER) is True
    # the same construction verifies under any concrete owner identity
    uuid_entries = _genesis_entries("11111111-2222-3333-4444-555555555555")
    assert writer.verify_chain(uuid_entries, "11111111-2222-3333-4444-555555555555") is True
    # shipped artifact is exactly this construction
    shipped = json.loads(GENESIS_ENTRIES.read_text(encoding="utf-8"))
    assert [json.dumps(e, sort_keys=True) for e in shipped] == \
           [json.dumps(e, sort_keys=True) for e in entries]


def test_efficiency_is_computed_from_entries():
    eff = writer.compute_efficiency(_genesis_entries())
    assert eff["day"] == "2026-10-22"
    assert eff["actions"] == 8986
    assert eff["verified_outcomes"] == 52
    assert round(eff["ratio_actions_per_outcome"]) == 173
    assert eff["outcomes_by_mechanism"] == {"pr-flow": 36, "decision-closures-and-deliverables": 16}
    assert eff["flagged_mechanisms"] == ["learning-bridge", "lesson-tools", "nine-node-verification-watch"]


def test_engagement_is_never_an_outcome():
    record = _genesis_record()
    record["outcomes_verified"] = []
    entries = writer.build_entries(record, OWNER)
    eff = writer.compute_efficiency(entries)
    assert eff["actions"] == 8986  # activity is fully present...
    assert eff["verified_outcomes"] == 0  # ...and counts for nothing
    assert eff["ratio_actions_per_outcome"] is None


def test_tamper_control_any_hashed_field_breaks_the_chain():
    entries = _genesis_entries()
    victim = 10
    mutations = []

    e = copy.deepcopy(entries); e[victim]["metadata"]["lane"] = "forged-lane"; mutations.append(e)
    e = copy.deepcopy(entries); e[victim]["evidence_refs"] = []; mutations.append(e)
    e = copy.deepcopy(entries); e[victim]["event_type"] = "closure_on_proof"; mutations.append(e)
    e = copy.deepcopy(entries); e[victim]["event_at"] = "2026-10-22T17:30:01Z"; mutations.append(e)
    e = copy.deepcopy(entries); e[victim]["source_id"] = "outcome:forged"; mutations.append(e)
    e = copy.deepcopy(entries); e[victim]["previous_chain_hash"] = "0" * 64; mutations.append(e)
    e = copy.deepcopy(entries); e[victim], e[victim + 1] = e[victim + 1], e[victim]; mutations.append(e)
    e = copy.deepcopy(entries); e[-1]["metadata"]["activity_units"] = 1; mutations.append(e)

    for i, mutated in enumerate(mutations):
        assert writer.verify_chain(mutated, OWNER) is False, f"mutation {i} went undetected"


def test_shape_validation_rejects_unverified_and_self_verified_outcomes():
    record = _genesis_record()

    bad = copy.deepcopy(record)
    bad["outcomes_verified"][0]["verifier"] = ""
    try:
        writer.build_entries(bad, OWNER)
        raised = False
    except ValueError:
        raised = True
    assert raised, "empty verifier accepted"

    bad = copy.deepcopy(record)
    bad["outcomes_verified"] = []
    bad["closures_on_proof"] = [{
        "source_table": "github_issues", "object_ref": "2599",
        "basis": "closed after verification", "closed_by": "lane-x",
        "verifier": "lane-x",
        "evidence_url": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793"}]
    try:
        writer.build_entries(bad, OWNER)
        raised = False
    except ValueError:
        raised = True
    assert raised, "closure whose verifier equals its closer accepted"


def test_float_payloads_are_rejected():
    entry = {"event_type": "run_census", "status": "RECORDED",
             "privacy_classification": "PUBLIC", "source_table": "accountability_census",
             "source_id": "census:x:y", "event_at": "2026-10-22T17:30:00Z",
             "evidence_refs": [], "verification": {}, "value": {}, "outcome": {},
             "learning_refs": [],
             "metadata": {"actor": "a", "actor_kind": "system", "day": "2026-10-22",
                          "window_start": "s", "window_end": "e", "actions_runs": 1,
                          "board_comments": 0, "activity_units": 1, "prs_opened": 0,
                          "prs_merged": 0, "prs_closed_unmerged": 0,
                          "outcomes_verified_total": 0,
                          "merged_without_individual_verification": 0,
                          "ratio": 1.5}}
    try:
        writer.validate_entry(entry)
        raised = False
    except ValueError:
        raised = True
    assert raised, "float in metadata accepted by validate_entry"

    record = _genesis_record()
    record["activity"] = dict(record["activity"], actions_runs=8449.5)
    try:
        writer.build_entries(record, OWNER)
        raised = False
    except ValueError:
        raised = True
    assert raised, "float census count accepted by build_entries"


def test_rendered_sql_calls_the_record_function_only():
    entries = _genesis_entries()
    sql = writer.render_sql(entries)
    assert "insert into" not in sql.lower()
    assert sql.count("nayanet_record_ledger_event(") == len(entries) == 56
    assert writer.OWNER_TOKEN in sql
    shipped = GENESIS_SQL.read_text(encoding="utf-8")
    assert shipped == sql


def test_idempotency_keys_are_unique():
    entries = _genesis_entries()
    keys = [(e["source_table"], e["source_id"]) for e in entries]
    assert len(keys) == len(set(keys))


def test_writer_package_creates_no_schema():
    assert "create table" not in WRITER_PATH.read_text(encoding="utf-8").lower()
    assert "create table" not in GENESIS_SQL.read_text(encoding="utf-8").lower()
