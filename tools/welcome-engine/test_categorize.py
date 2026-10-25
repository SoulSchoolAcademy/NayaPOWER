#!/usr/bin/env python3
"""Auto-Categorization tests (B7, SN-0845 build 4).

Pins the filing half of the auto-organizer to the engine and to the
privacy law: a public project announcement files with its space, with
reasons; a public mail thread files with Smart Mail; a below-bar item
is UNFILED with the reason named, never force-filed; and a private
item is REFUSED before any scoring — proven by monkeypatching the
scorer to explode: a private item carrying a perfect-overlap topic
set that WOULD file at top score still never reaches it.
"""
import corpus as c
import categorize as z

STORE = c.build_corpus()

POST_ANNOUNCEMENT = {
    "id": "post-factory-1", "kind": "post", "visibility": "public",
    "topics": ["app creation", "templates"],
    "title": "App creation: new templates are live",
    "body": "Template to live app in minutes, building apps for citizens",
}
MAIL_THREAD = {
    "id": "mail-1", "kind": "mail", "visibility": "public",
    "subject": "Messaging and scheduling update",
    "body": "Compose anywhere send on time, delivery for all citizens",
}
SINGLE_SIGNAL = {
    "id": "post-voice-1", "kind": "post", "visibility": "public",
    "topics": ["voice"],
}
# Perfect overlap with space-smart-factory on topics AND its exact
# goal phrase: if this were ever scored, it would file. It is private.
PRIVATE_PERFECT = {
    "id": "mail-secret-1", "kind": "mail", "visibility": "private",
    "topics": ["apps", "building", "creation", "design", "templates"],
    "subject": "app creation templates building",
    "body": "Template to live app in minutes",
}


def test_public_post_files_to_its_space_with_reasons():
    r = z.categorize(POST_ANNOUNCEMENT, STORE)
    assert r["status"] == "filed"
    assert r["alias"] == "space-smart-factory" and r["kind"] == "space"
    assert r["item_id"] == "post-factory-1" and r["item_kind"] == "post"
    assert isinstance(r["score"], int) and r["score"] > 0
    assert r["reasons"] and r["signal_coverage_percent"] > 0
    assert r["calibrated"] is True
    assert len(r["signals"]) >= 2  # the engine's surfacing bar


def test_public_mail_files_to_smart_mail():
    r = z.categorize(MAIL_THREAD, STORE)
    assert r["status"] == "filed"
    assert r["alias"] == "space-smart-mail" and r["kind"] == "space"
    assert r["item_kind"] == "mail" and r["reasons"]


def test_below_bar_item_is_unfiled_with_named_reason():
    r = z.categorize(SINGLE_SIGNAL, STORE)
    assert r["status"] == "unfiled"
    assert "single-signal" in r["reason"]
    assert r["best_alias"] == "space-voice" and r["best_score"] > 0
    assert "alias" not in r  # unfiled carries no filing


def test_no_overlap_item_is_unfiled_not_force_filed():
    item = {"id": "post-none", "kind": "post", "visibility": "public",
            "topics": ["underwater basket weaving"]}
    r = z.categorize(item, STORE)
    assert r["status"] == "unfiled" and r["reason"]
    assert r["best_score"] == 0


def test_item_with_no_topics_is_unfiled_no_candidate():
    item = {"id": "post-empty", "kind": "post", "visibility": "public"}
    r = z.categorize(item, STORE)
    assert r["status"] == "unfiled"
    assert r["reason"].startswith("no candidate")
    assert r["best_alias"] is None and r["best_score"] is None


def test_private_item_is_refused_and_provably_unscored(monkeypatch):
    def explode(*a, **k):
        raise AssertionError("private content reached the scorer")

    monkeypatch.setattr(z, "score", explode)
    r = z.categorize(PRIVATE_PERFECT, STORE)
    assert r["status"] == "refused"
    assert r["reason"].startswith("privacy")
    assert "score" not in r and "alias" not in r  # nothing was scored


def test_unflagged_item_defaults_to_refused(monkeypatch):
    def explode(*a, **k):
        raise AssertionError("unflagged content reached the scorer")

    monkeypatch.setattr(z, "score", explode)
    item = dict(POST_ANNOUNCEMENT)
    del item["visibility"]
    r = z.categorize(item, STORE)
    assert r["status"] == "refused" and "privacy" in r["reason"]


def test_vector_builder_itself_refuses_private():
    try:
        z.item_vector(PRIVATE_PERFECT)
    except ValueError as e:
        assert "privacy" in str(e)
    else:
        raise AssertionError("item_vector vectorized a private item")


def test_mail_body_topics_only_count_when_public():
    # The same mail text files when public (above) and refuses when
    # the flag flips — subject/body derivation never runs pre-gate.
    item = dict(MAIL_THREAD, visibility="private")
    r = z.categorize(item, STORE)
    assert r["status"] == "refused"


def test_batch_keeps_filed_unfiled_refused_separate_and_complete():
    items = [POST_ANNOUNCEMENT, MAIL_THREAD, SINGLE_SIGNAL, PRIVATE_PERFECT]
    out = z.categorize_many(items, STORE)
    assert [r["item_id"] for r in out["filed"]] == ["post-factory-1", "mail-1"]
    assert [r["item_id"] for r in out["unfiled"]] == ["post-voice-1"]
    assert [r["item_id"] for r in out["refused"]] == ["mail-secret-1"]
    total = sum(len(v) for v in out.values())
    assert total == len(items)  # every item accounted for, none dropped


def test_only_spaces_and_projects_are_filed_with():
    # A citizen-shaped overlap must not file content with a person:
    # nitro's topics (testing/evidence) in an item file with a space
    # or not at all — citizens are never candidates.
    item = {"id": "post-evidence", "kind": "post", "visibility": "public",
            "topics": ["testing", "evidence", "validation"],
            "body": "Prove outcomes, test everything"}
    r = z.categorize(item, STORE)
    if r["status"] == "filed":
        assert r["kind"] in ("space", "project")
        assert r["alias"] not in {"nitro", "resolve", "naya-power"}


def test_deterministic_repeat_filing():
    a = z.categorize(POST_ANNOUNCEMENT, STORE)
    b = z.categorize(POST_ANNOUNCEMENT, c.build_corpus())
    assert a == b
