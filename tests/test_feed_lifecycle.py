"""Tests for tools/feed_lifecycle.py — #2244 requirement 2 (specialty-feed lifecycle).

Includes negative controls AND sabotage checks: the tests must fail if the
mechanism they guard is broken, not just when the code is absent.
"""

import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from feed_lifecycle import (
    FeedRegistryError,
    IllegalTransitionError,
    RegistryCorruptError,
    RegistryNotInitializedError,
    StandingFeedProtectedError,
    UnknownFeedError,
    ValidationError,
    close_feed,
    create_focused_feed,
    get_feed,
    init_registry,
    link_event,
    link_issue,
    list_feeds,
    load_registry,
    match,
    reopen_feed,
    resolve_feed,
    save_registry,
    STANDING_FEEDS,
)

TOOL = os.path.join(os.path.dirname(__file__), "..", "tools", "feed_lifecycle.py")
JUST = ("A focused feed for the promotion-chain proof work: failures need one "
        "persistent venue so the repair, the evidence, and the lesson stay together.")


@pytest.fixture()
def root(tmp_path):
    return str(tmp_path)


@pytest.fixture()
def seeded(root):
    init_registry(root=root, actor="test")
    return root


# --- init ---------------------------------------------------------------

def test_init_seeds_nine_standing_feeds_open(root):
    out = init_registry(root=root, actor="test")
    assert out["added"] and len(out["added"]) == 9
    feeds = list_feeds(root=root)
    assert len(feeds) == 9
    assert {f["feed_id"] for f in feeds} == {f"feed-{n}" for n, _ in STANDING_FEEDS}
    assert all(f["kind"] == "standing" and f["status"] == "OPEN" for f in feeds)
    assert all(f["issue_url"].endswith(f"/issues/{f['issue_number']}") for f in feeds)


def test_init_idempotent_never_duplicates(seeded):
    before = list_feeds(root=seeded)
    out = init_registry(root=seeded, actor="test")
    assert out["added"] == []
    assert list_feeds(root=seeded) == before


def test_load_uninitialized_fails_closed(root):
    with pytest.raises(RegistryNotInitializedError):
        load_registry(root=root)


def test_load_corrupt_fails_closed(root):
    p = os.path.join(root, "feed-registry.json")
    os.makedirs(root, exist_ok=True)
    with open(p, "w") as f:
        f.write("{not json")
    with pytest.raises(RegistryCorruptError):
        load_registry(root=root)


def test_load_wrong_schema_fails_closed(root):
    p = os.path.join(root, "feed-registry.json")
    os.makedirs(root, exist_ok=True)
    with open(p, "w") as f:
        json.dump({"schema": "something.else.v9", "feeds": []}, f)
    with pytest.raises(RegistryCorruptError):
        load_registry(root=root)


def test_load_duplicate_feed_id_fails_closed(root):
    init_registry(root=root, actor="test")
    doc = load_registry(root=root)
    doc["feeds"].append(dict(doc["feeds"][0]))
    save_registry(doc, root=root)
    with pytest.raises(RegistryCorruptError):
        load_registry(root=root)


# --- create --------------------------------------------------------------

def test_create_focused_feed_happy_path(seeded):
    out = create_focused_feed(
        title="Promotion Chain Proof Failures",
        owner="naya2",
        material_justification=JUST,
        parent_feed="feed-1868",
        root=seeded,
    )
    assert out["duplicate"] is False
    feed = out["feed"]
    assert feed["kind"] == "focused"
    assert feed["status"] == "OPEN"
    assert feed["parent_feed"] == "feed-1868"
    assert feed["feed_id"].startswith("feed-promotion-chain-proof-failures-")


def test_create_idempotent_on_title_parent_while_open(seeded):
    a = create_focused_feed("Proof Failures", "naya2", JUST, "feed-1868", root=seeded)
    b = create_focused_feed("  proof   FAILURES ", "naya2", JUST, "feed-1868", root=seeded)
    assert b["duplicate"] is True
    assert b["feed_id"] == a["feed_id"]
    assert len(list_feeds(kind="focused", root=seeded)) == 1


def test_create_rejects_short_justification(seeded):
    with pytest.raises(ValidationError):
        create_focused_feed("X", "naya2", "misc stuff", "feed-1868", root=seeded)


def test_create_rejects_missing_justification(seeded):
    with pytest.raises(ValidationError):
        create_focused_feed("X", "naya2", "   ", "feed-1868", root=seeded)


def test_create_rejects_unknown_parent(seeded):
    with pytest.raises(UnknownFeedError):
        create_focused_feed("X", "naya2", JUST, "feed-9999", root=seeded)


def test_create_rejects_focused_parent(seeded):
    a = create_focused_feed("Parent", "naya2", JUST, "feed-1868", root=seeded)
    with pytest.raises(ValidationError):
        create_focused_feed("Child", "naya2", JUST, a["feed_id"], root=seeded)


def test_create_rejects_empty_title(seeded):
    with pytest.raises(ValidationError):
        create_focused_feed("  ", "naya2", JUST, "feed-1868", root=seeded)


def test_create_rejects_empty_owner(seeded):
    with pytest.raises(ValidationError):
        create_focused_feed("X", "", JUST, "feed-1868", root=seeded)


# --- lifecycle ------------------------------------------------------------

def _focused(seeded, title="Proof Failures"):
    return create_focused_feed(title, "naya2", JUST, "feed-1868", root=seeded)["feed_id"]


def test_resolve_requires_receipt_fields(seeded):
    fid = _focused(seeded)
    with pytest.raises(ValidationError):
        resolve_feed(fid, "short", "SN-1234",
                     "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1",
                     root=seeded)
    with pytest.raises(ValidationError):
        resolve_feed(fid, "A proper outcome description of what happened here.",
                     "not-a-note",
                     "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1",
                     root=seeded)
    with pytest.raises(ValidationError):
        resolve_feed(fid, "A proper outcome description of what happened here.",
                     "SN-1234", "notaurl", root=seeded)
    assert get_feed(fid, root=seeded)["status"] == "OPEN"  # still open


def test_resolve_happy_path_then_close(seeded):
    fid = _focused(seeded)
    r = resolve_feed(
        fid,
        outcome="Promotion proof chain unblocked; three dispatch failures root-caused.",
        smart_note_id="SN-1234",
        smart_note_link="https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175",
        evidence_refs=["run 37352372748"],
        actor="naya2",
        root=seeded,
    )
    assert r["status"] == "RESOLVED"
    assert r["resolution"]["smart_note_id"] == "SN-1234"
    c = close_feed(fid, actor="naya2", root=seeded)
    assert c["status"] == "CLOSED"
    assert get_feed(fid, root=seeded)["status"] == "CLOSED"


def test_open_to_closed_is_illegal(seeded):
    fid = _focused(seeded)
    with pytest.raises(IllegalTransitionError):
        close_feed(fid, root=seeded)


def test_resolve_twice_is_illegal(seeded):
    fid = _focused(seeded)
    kw = dict(outcome="A proper outcome description of what happened here, at length.",
              smart_note_id="SN-1234",
              smart_note_link="https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1",
              root=seeded)
    resolve_feed(fid, **kw)
    with pytest.raises(IllegalTransitionError):
        resolve_feed(fid, **kw)


def test_reopen_keeps_resolution_history(seeded):
    fid = _focused(seeded)
    resolve_feed(fid, "A proper outcome description of what happened here, at length.",
                 "SN-1234", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1",
                 root=seeded)
    reopen_feed(fid, reason="Regression appeared in the next cycle; reopening.", root=seeded)
    feed = get_feed(fid, root=seeded)
    assert feed["status"] == "OPEN"
    assert feed["resolution"] is None
    assert len(feed["resolution_history"]) == 1
    assert feed["resolution_history"][0]["smart_note_id"] == "SN-1234"


def test_reopen_from_open_is_illegal(seeded):
    fid = _focused(seeded)
    with pytest.raises(IllegalTransitionError):
        reopen_feed(fid, reason="nope", root=seeded)


def test_standing_feeds_are_protected(seeded):
    kw = dict(outcome="A proper outcome description of what happened here, at length.",
              smart_note_id="SN-1234",
              smart_note_link="https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1",
              root=seeded)
    with pytest.raises(StandingFeedProtectedError):
        resolve_feed("feed-1868", **kw)
    with pytest.raises(StandingFeedProtectedError):
        close_feed("feed-1868", root=seeded)
    with pytest.raises(StandingFeedProtectedError):
        reopen_feed("feed-1868", reason="x", root=seeded)
    assert get_feed("feed-1868", root=seeded)["status"] == "OPEN"


def test_unknown_feed_raises(seeded):
    with pytest.raises(UnknownFeedError):
        get_feed("feed-nope", root=seeded)
    with pytest.raises(UnknownFeedError):
        link_event("feed-nope", "evt-1", root=seeded)


# --- link_issue / link_event / match ---------------------------------------

def test_link_issue_binds_venue(seeded):
    fid = _focused(seeded)
    out = link_issue(fid, 9999, root=seeded)
    assert out["issue_url"] == "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/9999"
    assert get_feed(fid, root=seeded)["issue_number"] == 9999


def test_link_issue_rejects_bad_number(seeded):
    fid = _focused(seeded)
    with pytest.raises(ValidationError):
        link_issue(fid, -3, root=seeded)


def test_link_event_dedupes(seeded):
    fid = _focused(seeded)
    a = link_event(fid, "evt-abc", root=seeded)
    b = link_event(fid, "evt-abc", root=seeded)
    assert a["linked"] is True and b["linked"] is False
    assert get_feed(fid, root=seeded)["linked_events"] == ["evt-abc"]


def test_link_event_on_standing_feed_allowed(seeded):
    out = link_event("feed-1865", "evt-abc", root=seeded)
    assert out["linked"] is True


def test_match_by_id_number_and_url(seeded):
    assert match("feed-1868", root=seeded)["issue_number"] == 1868
    assert match("1868", root=seeded)["feed_id"] == "feed-1868"
    assert match("#1868", root=seeded)["feed_id"] == "feed-1868"
    assert match("https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1868",
                root=seeded)["feed_id"] == "feed-1868"


def test_match_unknown_raises(seeded):
    with pytest.raises(UnknownFeedError):
        match("feed-0000", root=seeded)


def test_list_filters(seeded):
    _focused(seeded, title="A")
    assert len(list_feeds(status="OPEN", root=seeded)) == 10
    assert len(list_feeds(kind="focused", root=seeded)) == 1
    assert len(list_feeds(status="CLOSED", root=seeded)) == 0


# --- sabotage checks: the tests must catch a broken mechanism ---------------

def test_sabotage_short_justification_would_be_caught(seeded):
    """If the justification-length gate were removed, this test must FAIL."""
    import feed_lifecycle as fl
    src = open(TOOL).read()
    # The gate exists: MIN_JUSTIFICATION compared against justification length.
    assert "MIN_JUSTIFICATION" in src and "material_justification" in src
    # Behavioral proof the gate is live, not decorative:
    with pytest.raises(ValidationError):
        fl.create_focused_feed("X", "naya2", "x" * 39, "feed-1868", root=seeded)
    ok = fl.create_focused_feed("X", "naya2", "x" * 40, "feed-1868", root=seeded)
    assert ok["duplicate"] is False


def test_sabotage_standing_protection_would_be_caught(seeded):
    """If standing-feed protection were removed, resolve would succeed — test guards it."""
    import feed_lifecycle as fl
    assert "StandingFeedProtectedError" in open(TOOL).read()
    with pytest.raises(FeedRegistryError):
        fl.resolve_feed(
            "feed-1865", "A proper outcome description of what happened here.",
            "SN-1234", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1",
            root=seeded)


def test_sabotage_skip_receipt_would_be_caught(seeded):
    """OPEN -> CLOSED must stay illegal; the receipt is the whole point."""
    fid = _focused(seeded)
    with pytest.raises(IllegalTransitionError):
        close_feed(fid, root=seeded)
    assert get_feed(fid, root=seeded)["status"] == "OPEN"


# --- CLI end-to-end ----------------------------------------------------------

def test_cli_end_to_end(tmp_path):
    root = str(tmp_path)

    def run(*args):
        r = subprocess.run([sys.executable, TOOL, "--root", root, *args],
                           capture_output=True, text=True)
        return r

    assert run("init").returncode == 0
    r = run("create", "--title", "CLI Feed", "--owner", "naya2",
            "--justification", JUST, "--parent", "feed-1872")
    assert r.returncode == 0, r.stderr
    fid = json.loads(r.stdout)["feed_id"]

    r = run("create", "--title", "CLI Feed", "--owner", "naya2",
            "--justification", JUST, "--parent", "feed-1872")
    assert json.loads(r.stdout)["duplicate"] is True

    assert run("link-issue", "--feed", fid, "--issue", "9991").returncode == 0
    assert run("link-event", "--feed", fid, "--event", "evt-1").returncode == 0

    # resolve without a note link -> refused, exit 2, feed still OPEN
    r = run("resolve", "--feed", fid, "--outcome", "x",
            "--smart-note-id", "SN-1", "--smart-note-link", "notaurl")
    assert r.returncode == 2
    assert "FEED_LIFECYCLE_REFUSED" in r.stderr

    r = run("resolve", "--feed", fid,
            "--outcome", "CLI run proved the lifecycle end to end, honestly.",
            "--smart-note-id", "SN-9999",
            "--smart-note-link", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1",
            "--actor", "naya2")
    assert r.returncode == 0, r.stderr
    assert run("close", "--feed", fid).returncode == 0

    r = run("match", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1872")
    assert json.loads(r.stdout)["feed_id"] == "feed-1872"

    r = run("list", "--status", "CLOSED")
    assert fid in [f["feed_id"] for f in json.loads(r.stdout)["feeds"]]


def test_cli_unknown_command_refused(tmp_path):
    r = subprocess.run([sys.executable, TOOL, "--root", str(tmp_path),
                        "resolve", "--feed", "feed-nope", "--outcome", "x" * 30,
                        "--smart-note-id", "SN-12",
                        "--smart-note-link", "https://example.com/1"],
                       capture_output=True, text=True)
    assert r.returncode == 2
    assert "FEED_LIFECYCLE_REFUSED" in r.stderr
