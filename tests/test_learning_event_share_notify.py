"""Tests for the #2244 req 3 -> req 4 consumer seam: SHARED transition hands
the event to the worker notification outbox (tools/notify_outbox.py).

The seam is: every SHARED transition best-effort publishes one notification
(dedup_key = the deterministic event id); anything else never publishes; a
missing or broken outbox never breaks the transition.

The real outbox lives on PR #2303 (unmerged), so these tests pin the seam
against a recording stub that enforces the outbox's documented contract
(severity set, audience, title, dedup, TTL bound). One integration test is
gated on the real module and activates when #2303 merges.
"""

import json
import sys
import types

import pytest

from tools.learning_event_envelope import (
    _notify_shared,
    get_event,
    issue_event,
    main,
    transition,
)

SHA = "b" * 40
FEED_URL = "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2235"

# The outbox contract, per tools/notify_outbox.py on PR #2303.
OUTBOX_SEVERITIES = ("info", "attention", "urgent", "blocker")


def _fields(**over):
    base = {
        "event_type": "failure",
        "severity": "HIGH",
        "title": "promotion wait-step died on skipped check",
        "source_artifact": "tools/promote.py",
        "source_sha": SHA,
        "expected": "wait step tolerates skipped placeholder checks",
        "actual": "wait step failed fast on skipped == failed",
        "owner": "naya-2",
        "impacted_teams": ["learn", "verify"],
        "next_action": "record event, share in specialty feed",
    }
    base.update(over)
    return base


def _make_stub(fail_publish=False):
    """A recording stand-in for tools/notify_outbox.

    Enforces the documented publish contract and dedups on dedup_key like
    the real outbox, so the seam tests prove the payload would be accepted.
    """
    mod = types.ModuleType("notify_outbox")
    mod.SEVERITIES = OUTBOX_SEVERITIES
    mod.records = []
    mod.calls = 0

    def _validate(payload):
        assert isinstance(payload, dict)
        assert payload.get("severity") in OUTBOX_SEVERITIES, payload.get("severity")
        aud = payload.get("audience")
        assert aud and isinstance(aud, list) and all(isinstance(a, str) and a for a in aud)
        assert payload.get("title") and isinstance(payload["title"], str)
        assert payload.get("dedup_key") and isinstance(payload["dedup_key"], str)
        ttl = payload.get("ttl_hours")
        assert isinstance(ttl, (int, float)) and 0 < ttl <= 168
        src = payload.get("source")
        if src is not None:
            assert isinstance(src, dict) and src.get("artifact")

    def publish(payload):
        mod.calls += 1
        if fail_publish:
            raise RuntimeError("boom")
        _validate(payload)
        for r in mod.records:
            if r["dedup_key"] == payload["dedup_key"]:
                return r["id"]  # idempotent, like the real outbox
        rid = f"notif-{len(mod.records):04d}"
        mod.records.append({"id": rid, **payload})
        return rid

    mod.publish = publish
    return mod


@pytest.fixture()
def ledger(tmp_path):
    return tmp_path / "events.json"


@pytest.fixture()
def outbox_stub(monkeypatch):
    """Inject the recording stub as both importable names the seam tries."""
    stub = _make_stub()
    monkeypatch.setitem(sys.modules, "notify_outbox", stub)
    monkeypatch.setitem(sys.modules, "tools.notify_outbox", stub)
    return stub


def _issued(ledger, **over):
    env, _ = issue_event(_fields(**over), ledger_path=ledger, issued_by="naya-2")
    return env["event_id"]


# ---------------------------------------------------------------- happy path


def test_shared_publishes_exactly_one_notification(ledger, outbox_stub):
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    assert len(outbox_stub.records) == 1
    rec = outbox_stub.records[0]
    assert rec["type"] == "learning-event"
    assert rec["severity"] == "urgent"  # HIGH -> urgent
    assert rec["audience"] == ["all", "learn", "verify"]
    assert "promotion wait-step" in rec["title"]
    assert FEED_URL in rec["body"]
    assert rec["dedup_key"] == f"learning-event:{eid}"
    assert rec["source"] == {"artifact": "tools/promote.py", "sha": SHA}
    assert rec["publisher"] == "learning-event-envelope:naya-2"
    # The receipt rides on the envelope.
    receipt = env["share_notification"]
    assert receipt["outbox_event_id"] == rec["id"]
    assert receipt["dedup_key"] == rec["dedup_key"]
    assert "skipped" not in receipt


@pytest.mark.parametrize("envelope_sev,outbox_sev", [
    ("INFO", "info"),
    ("NOTICE", "attention"),
    ("WARNING", "attention"),
    ("HIGH", "urgent"),
    ("CRITICAL", "blocker"),
])
def test_severity_mapping_all_levels(ledger, outbox_stub, envelope_sev, outbox_sev):
    eid = _issued(ledger, severity=envelope_sev, title=f"sev {envelope_sev}")
    transition(eid, "SHARED", actor="naya-2", ledger_path=ledger, feed_url=FEED_URL)
    assert outbox_stub.records[-1]["severity"] == outbox_sev


def test_non_shared_transitions_publish_nothing(ledger, outbox_stub):
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    receipt_at_share = dict(env["share_notification"])
    assert len(outbox_stub.records) == 1
    transition(eid, "ACKNOWLEDGED", actor="naya-4", ledger_path=ledger)
    transition(eid, "RESOLVED", actor="naya-4", ledger_path=ledger,
               no_lesson_reason="one-off, no reusable lesson")
    assert len(outbox_stub.records) == 1  # still exactly one
    # The seam fires once, at SHARED: no re-publish on later transitions,
    # and the share receipt is never rewritten.
    assert outbox_stub.calls == 1
    env = get_event(eid, ledger_path=ledger)
    assert env["share_notification"] == receipt_at_share


def test_duplicate_issue_still_one_notification(ledger, outbox_stub):
    # #2244 acceptance: one material failure -> one event -> one notification.
    env1, dup1 = issue_event(_fields(), ledger_path=ledger)
    env2, dup2 = issue_event(_fields(), ledger_path=ledger)
    assert dup2 is True
    transition(env1["event_id"], "SHARED", actor="naya-2", ledger_path=ledger,
               feed_url=FEED_URL)
    assert len(outbox_stub.records) == 1
    assert outbox_stub.records[0]["dedup_key"] == f"learning-event:{env1['event_id']}"


def test_reshare_attempt_dedups_to_same_notification(ledger, outbox_stub):
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    first_id = env["share_notification"]["outbox_event_id"]
    # A second share attempt for the same event (e.g. operator retry) must
    # not create a second notification.
    again = _notify_shared(env, "naya-2")
    assert again["outbox_event_id"] == first_id
    assert len(outbox_stub.records) == 1


def test_cli_transition_surfaces_share_notification(ledger, outbox_stub, capsys):
    eid = _issued(ledger)
    rc = main(["--ledger", str(ledger), "transition", eid, "--to", "SHARED",
               "--actor", "naya-2", "--feed-url", FEED_URL])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["lifecycle_state"] == "SHARED"
    assert out["share_notification"]["outbox_event_id"] == outbox_stub.records[0]["id"]
    assert len(outbox_stub.records) == 1


# ---------------------------------------------------------------- fail-safe: the seam never breaks the transition


def test_outbox_absent_transition_still_succeeds(ledger, monkeypatch):
    # Simulate a tree where PR #2303 has not merged: both import names fail.
    monkeypatch.setitem(sys.modules, "notify_outbox", None)
    monkeypatch.setitem(sys.modules, "tools.notify_outbox", None)
    # Composition note (#2244-E): when another test module already imported
    # the real outbox, `from tools import notify_outbox` resolves through the
    # parent package's attribute and never consults sys.modules -- so the
    # absence simulation must also drop that attribute binding.
    pkg = sys.modules.get("tools")
    if pkg is not None:
        monkeypatch.delattr(pkg, "notify_outbox", raising=False)
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    assert env["lifecycle_state"] == "SHARED"  # the transition itself succeeded
    assert env["share_notification"]["skipped"] == "notify_outbox unavailable on this tree"


def test_publish_failure_never_breaks_transition(ledger, monkeypatch):
    stub = _make_stub(fail_publish=True)
    monkeypatch.setitem(sys.modules, "notify_outbox", stub)
    monkeypatch.setitem(sys.modules, "tools.notify_outbox", stub)
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    assert env["lifecycle_state"] == "SHARED"
    assert env["share_notification"]["skipped"] == "publish failed: RuntimeError"


def test_broken_outbox_import_never_breaks_transition(ledger, monkeypatch):
    # F1 regression (2026-10-11): a present-but-broken outbox module raising
    # at IMPORT time (not an ImportError) must degrade to a recorded skip,
    # per the seam's NEVER-raises contract — it must not break the transition.
    class _BrokenOutboxFinder:
        def find_spec(self, name, path=None, target=None):
            if name in ("notify_outbox", "tools.notify_outbox"):
                raise RuntimeError("simulated broken outbox at import time")
            return None

    monkeypatch.delitem(sys.modules, "notify_outbox", raising=False)
    monkeypatch.delitem(sys.modules, "tools.notify_outbox", raising=False)
    monkeypatch.setattr(sys, "meta_path", [_BrokenOutboxFinder()] + sys.meta_path)
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    assert env["lifecycle_state"] == "SHARED"
    assert env["share_notification"]["skipped"] == "notify_outbox import failed: RuntimeError"


def test_kill_switch_disables_notify(ledger, outbox_stub, monkeypatch):
    monkeypatch.setenv("NAYA_EVENT_SHARE_NOTIFY", "0")
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    assert env["lifecycle_state"] == "SHARED"
    assert len(outbox_stub.records) == 0
    assert env["share_notification"]["skipped"] == "disabled by NAYA_EVENT_SHARE_NOTIFY"


def test_share_notification_survives_ledger_round_trip(ledger, outbox_stub):
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    data = json.loads(ledger.read_text(encoding="utf-8"))
    assert data["events"][eid]["share_notification"] == env["share_notification"]


# ---------------------------------------------------------------- real-outbox integration (activates when #2303 merges)


def test_real_outbox_integration(ledger, tmp_path, monkeypatch):
    """End-to-end against the real tools/notify_outbox.

    Skipped until PR #2303 merges (the module is absent on this branch).
    When it runs, it proves the seam's payload passes the real validation
    and the notification is retrievable via the outbox's own API.
    """
    notify_outbox = pytest.importorskip("tools.notify_outbox")
    monkeypatch.setenv("NAYA_NOTIFY_ROOT", str(tmp_path / "outbox-state"))
    eid = _issued(ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url=FEED_URL)
    receipt = env["share_notification"]
    assert "outbox_event_id" in receipt
    found = notify_outbox.find_by_dedup_key(f"learning-event:{eid}")
    assert found is not None
    assert found["id"] == receipt["outbox_event_id"]
    pending = notify_outbox.pending("all")
    assert [e["id"] for e in pending] == [receipt["outbox_event_id"]]
