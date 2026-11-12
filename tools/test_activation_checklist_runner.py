"""Tests for tools/activation_checklist_runner.py (GT-015 family).

All providers are fakes — no network, no real gate subprocess.
Negative controls (required):
  * boot-gate pin failure -> the receipt's FIRST line is RED naming the
    failure, and the verdict is FAIL (reported, never hidden);
  * stale operating state -> FAIL; venue pointer at the retired board
    (2765) -> FAIL; absent daily-law registry -> tune-in-laws FAIL with
    the GT-010 cure; a single named law -> FAIL (checklist requires >= 2).
Plus: the all-green path, the real repo checklist loads and classifies
(12 checks across 6 steps), design checks NA without --design.
"""
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import activation_checklist_runner as runner  # noqa: E402

NOW = 1_800_000_000.0  # fixed clock for fixtures
TIP = "a" * 40


def iso(ts):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_repo(tmp_path, registry=True, manifest=True, mech=True):
    root = tmp_path / "repo"
    (root / "BRAIN/00-ACTIVATION").mkdir(parents=True)
    (root / "BRAIN/01-GOVERNANCE").mkdir(parents=True)
    (root / "tools").mkdir()
    (root / ".naya/project-intelligence").mkdir(parents=True)
    real = Path(__file__).resolve().parent.parent / "BRAIN/00-ACTIVATION/activation-checklist.json"
    (root / "BRAIN/00-ACTIVATION/activation-checklist.json").write_text(real.read_text())
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# fixture law\n")
    if registry:
        (root / "BRAIN/01-GOVERNANCE/DAILY-LAW-REGISTRY.machine.json").write_text(json.dumps({
            "generated_from": {"daily_law_source": {
                "sha256": hashlib.sha256(agents.read_bytes()).hexdigest(),
                "path_label": "~/AGENTS.md"}}}))
    if manifest:
        (root / ".naya/project-intelligence/MANIFEST.json").write_text(
            json.dumps({"projects": [{"project_id": "fixture"}]}))
    if mech:
        (root / "tools/mechanism-registry.json").write_text(json.dumps({"mechanisms": [1, 2]}))
    return root, agents


def make_args(agents, **over):
    class A:
        pass
    a = A()
    a.agent_id = "test-seat"
    a.agents_md = str(agents)
    a.design = False
    a.outcome = "the director sees the activation proven, not promised"
    a.laws = "Prime Judgment Law, The Lesson Law"
    a.proof = "he opens the receipt file and reads the first line"
    a.memory_note = "preference: plain words first; commitment: report done, not doing"
    a.brief = "build the mechanical activation checklist runner"
    a.lane_note = "board scan: no conflicting lane"
    a.tools_note = "official mechanism named: the protocol gate itself"
    a.design_note = None
    a.project_id = "fixture"
    a.no_project_intelligence = False
    for k, v in over.items():
        setattr(a, k, v)
    return a


def green_providers():
    state = {
        "STATE-CORE.json": {"venue": {"live": 2793}},
        "OPERATING-STATE.json": {"generated_at": iso(NOW - 600), "tip": TIP},
        "QUEUE-CONTRACT.json": {"generated_at": iso(NOW - 600), "prs": [{}, {}]},
    }
    return {
        "tip": lambda: TIP,
        "state": lambda name: state.get(name),
        "prs": lambda: [{"number": 1, "title": "x"}],
        "gate": lambda root, agent: {"pass": True, "checks": [{}, {}, {}], "failures": []},
        "delta": lambda root: (True, "OK: delta in sync"),
        "ancestry": lambda a, b: True,
    }


def by_name(receipt):
    return {c["check"]: c for c in receipt["checks"]}


def test_all_green(tmp_path):
    root, agents = make_repo(tmp_path)
    r = runner.Runner(root, make_args(agents), providers=green_providers(), now=NOW).run()
    assert r["verdict"] == "PASS"
    assert r["boot_gate"]["first_line"].startswith("BOOT GATE: GREEN")
    text = runner.render_text(r)
    assert text.split("\n")[0] == r["boot_gate"]["first_line"]
    assert r["counts"].get("FAIL", 0) == 0


def test_pin_failure_is_first_red_line(tmp_path):
    # NEGATIVE CONTROL: the gate's protocol_pin failure must headline the receipt.
    root, agents = make_repo(tmp_path)
    prov = green_providers()
    prov["gate"] = lambda root, agent: {
        "pass": False, "checks": [],
        "failures": [{"name": "protocol_pin", "pass": False,
                      "detail": "PROTOCOL.md bytes differ from the pinned fingerprint"}]}
    r = runner.Runner(root, make_args(agents), providers=prov, now=NOW).run()
    first = runner.render_text(r).split("\n")[0]
    assert first.startswith("BOOT GATE: RED")
    assert "protocol_pin" in first
    assert "reported, not hidden" in first
    assert r["verdict"] == "FAIL"


def test_stale_operating_state_fails(tmp_path):
    root, agents = make_repo(tmp_path)
    prov = green_providers()
    base = prov["state"]
    prov["state"] = lambda name: (
        {"generated_at": iso(NOW - 3 * 3600), "tip": TIP} if name == "OPERATING-STATE.json"
        else base(name))
    r = runner.Runner(root, make_args(agents), providers=prov, now=NOW).run()
    row = by_name(r)["operating state published + fresh"]
    assert row["status"] == "FAIL" and "age" in row["evidence"]
    assert r["verdict"] == "FAIL"


def test_retired_venue_pointer_fails(tmp_path):
    root, agents = make_repo(tmp_path)
    prov = green_providers()
    base = prov["state"]
    prov["state"] = lambda name: (
        {"venue": {"live": 2765}} if name == "STATE-CORE.json" else base(name))
    r = runner.Runner(root, make_args(agents), providers=prov, now=NOW).run()
    row = by_name(r)["venue pointer resolves (STATE-CORE)"]
    assert row["status"] == "FAIL" and "2765" in row["evidence"]


def test_state_tip_ancestor_passes_diverged_fails(tmp_path):
    root, agents = make_repo(tmp_path)
    # state tip behind live tip but in-history -> PASS (hourly cadence)
    prov = green_providers()
    base = prov["state"]
    prov["state"] = lambda name: (
        {"generated_at": iso(NOW - 600), "tip": "b" * 40} if name == "OPERATING-STATE.json"
        else base(name))
    r = runner.Runner(root, make_args(agents), providers=prov, now=NOW).run()
    assert by_name(r)["operating state published + fresh"]["status"] == "PASS"
    # NEGATIVE CONTROL: state tip outside main's history -> FAIL
    prov["ancestry"] = lambda a, b: False
    r = runner.Runner(root, make_args(agents), providers=prov, now=NOW).run()
    assert by_name(r)["operating state published + fresh"]["status"] == "FAIL"


def test_missing_registry_fails_with_gt010_cure(tmp_path):
    root, agents = make_repo(tmp_path, registry=False)
    r = runner.Runner(root, make_args(agents), providers=green_providers(), now=NOW).run()
    row = by_name(r)["AGENTS.md read at current main tip"]
    assert row["status"] == "FAIL" and "GT-010" in row["cure"]


def test_single_law_fails_two_pass(tmp_path):
    root, agents = make_repo(tmp_path)
    r = runner.Runner(root, make_args(agents, laws="Only One Law"),
                      providers=green_providers(), now=NOW).run()
    assert by_name(r)["governing laws named"]["status"] == "FAIL"
    assert r["verdict"] == "FAIL"


def test_missing_attestations_fail_not_pass(tmp_path):
    root, agents = make_repo(tmp_path)
    r = runner.Runner(root, make_args(agents, outcome=None, proof=None, brief=None),
                      providers=green_providers(), now=NOW).run()
    rows = by_name(r)
    assert rows["outcome sentence written"]["status"] == "FAIL"
    assert rows["verification method named"]["status"] == "FAIL"
    assert rows["task brief read in full"]["status"] == "FAIL"
    assert r["verdict"] == "FAIL"


def test_design_checks_na_without_design(tmp_path):
    root, agents = make_repo(tmp_path)
    r = runner.Runner(root, make_args(agents), providers=green_providers(), now=NOW).run()
    rows = by_name(r)
    assert rows["design work: design laws loaded"]["status"] == "NA"
    assert rows["block catalog consulted for design work"]["status"] == "NA"


def test_real_checklist_shape(tmp_path):
    # the runner must classify every check of the REAL contract: 12 checks, 6 steps
    root, agents = make_repo(tmp_path)
    r = runner.Runner(root, make_args(agents), providers=green_providers(), now=NOW).run()
    checklist_rows = [c for c in r["checks"] if c["step"] != "published-state"]
    assert len(checklist_rows) == 12
    assert len({c["step"] for c in checklist_rows}) == 6
    assert r["checklist_schema"] == "naya.activation.checklist.v1"


def test_tampered_agents_fails_with_real_fingerprint(tmp_path):
    # REGRESSION (runner read a nonexistent registry key, so every real
    # activation false-failed with fingerprint "None"): with the real
    # GT-010 registry schema, a tampered AGENTS.md must FAIL naming the
    # registry's actual fingerprint — never None.
    root, agents = make_repo(tmp_path)
    want = hashlib.sha256(agents.read_bytes()).hexdigest()
    agents.write_text("# fixture law\n# tampered line\n")
    r = runner.Runner(root, make_args(agents), providers=green_providers(), now=NOW).run()
    row = by_name(r)["AGENTS.md read at current main tip"]
    assert row["status"] == "FAIL"
    assert want[:16] in row["evidence"]
    assert "None" not in row["evidence"]
    assert r["verdict"] == "FAIL"


def test_legacy_wrong_key_registry_does_not_pass(tmp_path):
    # NEGATIVE CONTROL: a registry carrying only the retired wrong key
    # (generated_from.agents_md_sha256) must NOT satisfy the leg — the
    # runner reads the schema the GT-010 generator actually emits.
    root, agents = make_repo(tmp_path)
    (root / "BRAIN/01-GOVERNANCE/DAILY-LAW-REGISTRY.machine.json").write_text(json.dumps({
        "generated_from": {"agents_md_sha256": hashlib.sha256(agents.read_bytes()).hexdigest()}}))
    r = runner.Runner(root, make_args(agents), providers=green_providers(), now=NOW).run()
    row = by_name(r)["AGENTS.md read at current main tip"]
    assert row["status"] == "FAIL"
