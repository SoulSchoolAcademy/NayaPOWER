#!/usr/bin/env python3
"""#2244 step E: one complete failure -> notification -> specialty
collaboration -> canonical Smart Note -> cold-successor reuse chain.

Executable proof that the four #2244 mechanisms compose into one living
loop:

    req 3 envelope (learning_event_envelope.py)
  + req 4 outbox   (notify_outbox.py)
  + req 2 feeds    (feed_lifecycle.py)
  + step D wire    (worker_event_wire.py, exercised via the SHARED handoff)

The chain under test (all synthetic, all in temp dirs):

    synthetic failure
      -> DETECTED  (idempotent issuance; duplicate -> same id)
      -> SHARED    (specialty-feed URL required; outbox handoff fires;
                    affected worker receives a delivery digest + receipt)
      -> ACKNOWLEDGED (collaboration recorded on the feed)
      -> RESOLVED  (regression evidence + canonical Smart Note required)
      -> PRESERVED (Smart Note bound)
      -> REUSED    (a COLD successor -- fresh subprocess, fresh env, no
                    shared memory -- retrieves the lesson and applies it)
      -> BEHAVIORALLY_VERIFIED (behavior proof required)

Honest boundaries (what this does NOT claim):
  - Synthetic throughout: the failure, the feed venue, the Smart Note,
    and the successor are fixtures. This proves the machinery composes;
    it does not prove production delivery, real GitHub posting, or that
    a human would find the lesson useful.
  - The "specialty collaboration" is the feed-lifecycle registry's
    link/ack record, not a live GitHub issue thread.
  - The cold successor applies the lesson's machine repair block; a real
    successor would need richer lesson-application. The point proven is
    that the preserved lesson is retrievable and actionable by a party
    that shares nothing with the originator but the ledger path.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent / "tools"
ENVELOPE = [sys.executable, str(TOOLS / "learning_event_envelope.py")]

SHA40 = "0123456789abcdef0123456789abcdef01234567"
SN_ID = "SN-0001"
SN_LINK = "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/SN-0001.md"

sys.path.insert(0, str(TOOLS))


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------

@pytest.fixture()
def chain(tmp_path, monkeypatch):
    """Isolated #2244 world: ledger, outbox root, feed registry, scenario."""
    ledger = tmp_path / "events" / "learning-events.json"
    outbox_root = tmp_path / "outbox"
    feed_root = tmp_path / "feeds"
    scenario = tmp_path / "scenario.json"
    for d in (ledger.parent, outbox_root, feed_root):
        d.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("NAYA_EVENT_LEDGER", str(ledger))
    monkeypatch.setenv("NAYA_NOTIFY_ROOT", str(outbox_root))
    # fresh import state per test (module-level roots are env-driven at call)
    import notify_outbox, feed_lifecycle  # noqa: F401
    feed_lifecycle.init_registry(root=str(feed_root), actor="chain-proof")
    return {
        "ledger": str(ledger),
        "outbox_root": str(outbox_root),
        "feed_root": str(feed_root),
        "scenario": str(scenario),
        "tmp": tmp_path,
    }


def cli(*args, ledger):
    """Run the envelope CLI; return (exit_code, stdout, stderr)."""
    p = subprocess.run(
        ENVELOPE + ["--ledger", ledger, *args],
        capture_output=True, text=True, cwd=TOOLS.parent,
    )
    return p.returncode, p.stdout, p.stderr


def issue_failure(chain, title="gate threshold misconfigured"):
    code, out, err = cli(
        "issue", "--type", "failure", "--severity", "HIGH",
        "--title", title,
        "--artifact", "scenario/deploy_gate.py", "--sha", SHA40,
        "--expected", "gate_threshold == 10",
        "--actual", "gate_threshold == 0 (gate never trips; deploys unguarded)",
        "--owner", "naya-2", "--teams", "build",
        "--next", ("Repair: set gate_threshold to 10. "
                   "REPAIR_JSON={\"gate_threshold\": 10}"),
        ledger=chain["ledger"],
    )
    assert code == 0, err
    return json.loads(out)


def gate_check(scenario_path):
    """The synthetic material check: passes iff gate_threshold == 10."""
    cfg = json.loads(Path(scenario_path).read_text())
    ok = cfg.get("gate_threshold") == 10
    return ok, f"gate_threshold={cfg.get('gate_threshold')}"


SUCCESSOR_SCRIPT = textwrap.dedent('''\
    """Cold successor: retrieve the PRESERVED lesson and apply it.

    Shares NOTHING with the originator except the ledger path (argv).
    Refuses lessons that are not PRESERVED -- an unpreserved qualification
    must never be republished as authority (the D35 spirit).
    """
    import json, subprocess, sys
    from pathlib import Path

    ledger, event_id, scenario_path, tools_dir = sys.argv[1:5]
    r = subprocess.run(
        [sys.executable, str(Path(tools_dir) / "learning_event_envelope.py"),
         "--ledger", ledger, "get", event_id],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"SUCCESSOR-FAIL: cannot retrieve lesson: {r.stderr.strip()}")
        sys.exit(10)
    lesson = json.loads(r.stdout)
    if lesson["lifecycle_state"] != "PRESERVED":
        print(f"SUCCESSOR-FAIL: lesson not PRESERVED "
              f"(state={lesson['lifecycle_state']}); refusing to apply")
        sys.exit(11)
    nxt = lesson.get("next_action", "")
    marker = "REPAIR_JSON="
    if marker not in nxt:
        print("SUCCESSOR-FAIL: lesson carries no machine repair block")
        sys.exit(12)
    repair = json.loads(nxt.split(marker, 1)[1].strip().rstrip(")"))
    cfg_path = Path(scenario_path)
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
    cfg.update(repair)
    cfg_path.write_text(json.dumps(cfg))
    ok = cfg.get("gate_threshold") == 10
    if not ok:
        print(f"SUCCESSOR-FAIL: repair applied but gate still failing: {cfg}")
        sys.exit(13)
    print(f"SUCCESSOR-OK: applied lesson {event_id}; gate now passing; "
          f"smart_note={lesson.get('smart_note_id')}")
    sys.exit(0)
''')


def run_cold_successor(chain, event_id, fresh_scenario=True):
    """Run the successor in a scrubbed env; return (exit_code, output)."""
    import notify_outbox  # noqa: F401  (ensure importable; env is scrubbed below)
    tmp = chain["tmp"]
    script = tmp / "successor.py"
    script.write_text(SUCCESSOR_SCRIPT)
    scenario = tmp / ("successor-scenario.json" if fresh_scenario else "scenario.json")
    if fresh_scenario:
        scenario.write_text(json.dumps({"gate_threshold": 0}))
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": os.environ.get("HOME", "/tmp"),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
    }
    # NOTE: deliberately NOT passing NAYA_EVENT_LEDGER / NAYA_NOTIFY_ROOT.
    # The successor gets the ledger path as an explicit argument -- the
    # same way a real cold worker would be handed a location, not state.
    p = subprocess.run(
        [sys.executable, str(script), chain["ledger"], event_id,
         str(scenario), str(TOOLS)],
        capture_output=True, text=True, env=env, cwd=TOOLS.parent,
    )
    return p.returncode, (p.stdout + p.stderr).strip()


# ---------------------------------------------------------------------------
# the chain
# ---------------------------------------------------------------------------

def test_full_chain_failure_to_behaviorally_verified(chain):
    import notify_outbox
    import feed_lifecycle

    # 1. FAILURE -> DETECTED (idempotent)
    broken = chain["scenario"]
    Path(broken).write_text(json.dumps({"gate_threshold": 0}))
    ok, detail = gate_check(broken)
    assert not ok, "fixture must start broken"
    first = issue_failure(chain)
    assert first["lifecycle_state"] == "DETECTED"
    event_id = first["event_id"]
    second = issue_failure(chain)
    assert second["event_id"] == event_id and second["duplicate"] is True

    # 2. Specialty feed for the collaboration (req 2), under [TEAM FEED] Learning
    feed = feed_lifecycle.create_focused_feed(
        title="chain-proof: gate threshold failure",
        owner="naya-2",
        material_justification=(
            "Proving the #2244-E chain end to end: a misconfigured deploy "
            "gate is a material failure whose lesson must reach every worker."
        ),
        parent_feed="feed-1865",
        issue_number=999999,
        root=chain["feed_root"],
    )
    feed_url = feed["feed"]["issue_url"]
    assert feed_url.startswith("https://")

    # 3. DETECTED -> SHARED: feed URL mandatory; the outbox handoff fires
    code, out, err = cli("transition", event_id, "--to", "SHARED",
                         "--actor", "naya-2", "--feed-url", feed_url,
                         ledger=chain["ledger"])
    assert code == 0, err
    env = json.loads(cli("get", event_id, ledger=chain["ledger"])[1])
    assert env["lifecycle_state"] == "SHARED"
    assert env["specialty_feed_url"] == feed_url
    share_note = env.get("share_notification", {})
    assert not share_note.get("skipped"), f"notify handoff skipped: {share_note}"

    # 4. NOTIFICATION: the affected worker actually receives awareness
    pending = notify_outbox.pending("build")
    notif = next((e for e in pending
                  if e.get("dedup_key") == f"learning-event:{event_id}"), None)
    assert notif is not None, \
        "shared event never reached the outbox for the affected audience"
    digest = notify_outbox.deliver_pending("build", "chain-proof-worker")
    assert digest and event_id in digest or title_in_digest(digest, "gate threshold"), \
        f"delivery digest missing the event: {digest!r}"
    # delivery receipt recorded (auditable) against the notification id
    deliveries = (Path(chain["outbox_root"]) / "deliveries.jsonl").read_text()
    assert notif["id"] in deliveries

    # 5. COLLABORATION -> ACKNOWLEDGED
    feed_lifecycle.link_event(feed["feed_id"], event_id, root=chain["feed_root"])
    got = feed_lifecycle.get_feed(feed["feed_id"], root=chain["feed_root"])
    assert event_id in got["linked_events"]
    code, out, err = cli("transition", event_id, "--to", "ACKNOWLEDGED",
                         "--actor", "naya-2", "--note", "build lane ack; repair agreed",
                         ledger=chain["ledger"])
    assert code == 0, err

    # 6. RESOLVED: regression evidence + canonical Smart Note are mandatory
    Path(broken).write_text(json.dumps({"gate_threshold": 10}))
    ok, detail = gate_check(broken)
    assert ok, "repair must make the check pass before claiming resolution"
    code, out, err = cli(
        "transition", event_id, "--to", "RESOLVED", "--actor", "naya-2",
        "--regression-evidence", f"deploy gate re-run green: {detail}",
        "--smart-note-id", SN_ID, "--smart-note-link", SN_LINK,
        ledger=chain["ledger"])
    assert code == 0, err

    # 7. PRESERVED
    code, out, err = cli("transition", event_id, "--to", "PRESERVED",
                         "--actor", "naya-2", ledger=chain["ledger"])
    assert code == 0, err

    # 8. COLD SUCCESSOR retrieves the lesson and applies it (fresh process,
    #    fresh env, fresh broken scenario -- only the ledger path is shared)
    code, successor_out = run_cold_successor(chain, event_id)
    assert code == 0, f"cold successor failed: {successor_out}"
    assert "SUCCESSOR-OK" in successor_out

    # 9. REUSED -> BEHAVIORALLY_VERIFIED, each step demanding its evidence
    code, out, err = cli("transition", event_id, "--to", "REUSED",
                         "--actor", "naya-2",
                         "--reuse-evidence", successor_out,
                         ledger=chain["ledger"])
    assert code == 0, err
    code, out, err = cli("transition", event_id, "--to", "BEHAVIORALLY_VERIFIED",
                         "--actor", "naya-2",
                         "--behavior-proof",
                         f"cold successor (fresh env) applied {event_id} and "
                         f"the gate passed: {successor_out}",
                         ledger=chain["ledger"])
    assert code == 0, err
    final = json.loads(cli("get", event_id, ledger=chain["ledger"])[1])
    assert final["lifecycle_state"] == "BEHAVIORALLY_VERIFIED"
    assert final["lesson_status"] == "VERIFIED"
    assert final["smart_note_id"] == SN_ID
    # the full history is an auditable chain, in order
    states = [h["to"] for h in final["history"] if h["to"]]
    assert states == ["SHARED", "ACKNOWLEDGED", "RESOLVED", "PRESERVED",
                      "REUSED", "BEHAVIORALLY_VERIFIED"], states


def title_in_digest(digest, needle):
    return bool(digest) and needle in digest


# ---------------------------------------------------------------------------
# negative controls: if these don't fail, the chain is theater
# ---------------------------------------------------------------------------

def test_chain_rejects_share_without_feed(chain):
    """The notification step cannot be skipped: SHARED without a specialty
    feed URL is rejected, so no event can reach workers silently."""
    evt = issue_failure(chain)
    code, out, err = cli("transition", evt["event_id"], "--to", "SHARED",
                         "--actor", "naya-2", ledger=chain["ledger"])
    assert code == 2, f"expected rejection, got {code}: {out} {err}"
    assert "MISSING_FEED_URL" in err


def test_chain_rejects_out_of_order_transition(chain):
    """DETECTED -> RESOLVED is illegal: resolution requires the collaboration
    and evidence steps in between."""
    evt = issue_failure(chain)
    code, out, err = cli(
        "transition", evt["event_id"], "--to", "RESOLVED", "--actor", "naya-2",
        "--regression-evidence", "x", "--smart-note-id", SN_ID,
        "--smart-note-link", SN_LINK, ledger=chain["ledger"])
    assert code == 2, f"expected rejection, got {code}: {out} {err}"
    assert "ILLEGAL_TRANSITION" in err


def test_chain_rejects_resolve_without_evidence(chain):
    """RESOLVED without regression evidence and without a Smart Note is
    rejected -- a claim of resolution with no proof cannot enter the chain."""
    import feed_lifecycle
    evt = issue_failure(chain)
    feed_lifecycle.init_registry(root=chain["feed_root"], actor="t")
    feed = feed_lifecycle.create_focused_feed(
        title="chain-proof: negative control feed", owner="naya-2",
        material_justification="Negative control: resolution must carry proof.",
        parent_feed="feed-1865", issue_number=999998, root=chain["feed_root"])
    code, _, _ = cli("transition", evt["event_id"], "--to", "SHARED",
                     "--actor", "naya-2",
                     "--feed-url", feed["feed"]["issue_url"],
                     ledger=chain["ledger"])
    assert code == 0
    code, out, err = cli("transition", evt["event_id"], "--to", "ACKNOWLEDGED",
                         "--actor", "naya-2", ledger=chain["ledger"])
    assert code == 0
    code, out, err = cli("transition", evt["event_id"], "--to", "RESOLVED",
                         "--actor", "naya-2", ledger=chain["ledger"])
    assert code == 2, f"expected rejection, got {code}: {out} {err}"
    assert "MISSING_RESOLUTION" in err or "MISSING_REGRESSION_EVIDENCE" in err


def test_cold_successor_without_lesson_cannot_reuse(chain):
    """Control arm: a successor with no preserved lesson faces the same
    broken scenario and fails. The lesson -- not the harness -- is what
    makes reuse succeed."""
    code, out = run_cold_successor(chain, "evt-does-not-exist-0000")
    assert code != 0, "successor must fail when the lesson is unretrievable"
    assert "SUCCESSOR-FAIL" in out


def test_cold_successor_refuses_unpreserved_lesson(chain):
    """A lesson stuck at DETECTED (never preserved) must not be applied as
    authority: the successor refuses, so unqualified claims can't masquerade
    as verified learning."""
    evt = issue_failure(chain, title="unpreserved failure")
    code, out = run_cold_successor(chain, evt["event_id"])
    assert code != 0, "successor must refuse an unpreserved lesson"
    assert "not PRESERVED" in out


def test_idempotency_is_identity_based(chain):
    """Two DIFFERENT failures produce two events: idempotency keys on the
    failure's identity, it never collapses distinct failures into one."""
    a = issue_failure(chain, title="failure alpha")
    b = issue_failure(chain, title="failure beta")
    assert a["event_id"] != b["event_id"]
    assert a["duplicate"] is False and b["duplicate"] is False
