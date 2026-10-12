"""Battery for the L244 breach-post watchdog (tools/breach_post_watch.py).

The negative-control matrix from B-24:
  breach event WITH a posted flag   -> no flag
  breach event WITHOUT a post       -> flag fires
  ~17 prior silent instances        -> the flag must still fire
                                      (the normalization-of-deviance case
                                      is itself the regression test)
  API down                          -> "unable to verify", explicit, exit 1

Plus: the watchdog's own re-scan with its posted markers -> zero flags
(idempotency), and exception-marked merges -> no flag.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import breach_post_watch as bpw  # noqa: E402


def pr(number, title="Some fix", body="## Evidence\n- x", author="naya2",
       comments_text="", sha="a" * 40):
    return {"number": number, "title": title, "body": body,
            "merged_at": "2026-10-12T00:00:00Z",
            "merge_commit_sha": sha, "author": author,
            "comments_text": comments_text}


# --- invalid-authority --------------------------------------------------------

def test_revert_naming_invalid_authority_flags_original_pr():
    p = pr(2459, title="Revert #2455 — invalid delegated-merge-authority "
                       "invocation (LAW verdict: 0/5 gates)")
    evs = bpw.classify_pr(p)
    keys = {e["key"] for e in evs}
    assert "invalid-authority:2455" in keys


def test_revert_without_invalid_word_is_not_an_authority_event():
    p = pr(2400, title="Revert #2399 — broken test")
    evs = bpw.classify_pr(p)
    assert not any(e["kind"] == "invalid-authority" for e in evs)


def test_merged_pr_with_adjudication_flags_itself():
    p = pr(2455, title="Some merge",
           body="LAW verdict: 0/5 gates — invalid merge authority")
    evs = bpw.classify_pr(p)
    assert "invalid-authority:2455" in {e["key"] for e in evs}


def test_invalid_authority_with_posted_marker_stays_silent():
    p = pr(2459, title="Revert #2455 — invalid delegated-merge-authority "
                       "invocation")
    evs = bpw.classify_pr(p)
    flagged, _ = bpw.scan(evs, {"invalid-authority:2455"})
    assert flagged == []


def test_invalid_authority_without_marker_fires():
    p = pr(2459, title="Revert #2455 — invalid delegated-merge-authority "
                       "invocation")
    evs = bpw.classify_pr(p)
    flagged, _ = bpw.scan(evs, set())
    assert [e["key"] for e in flagged] == ["invalid-authority:2455"]


# --- protocol-breach (missing ## Evidence) ------------------------------------

def test_pr_with_evidence_section_is_clean():
    evs = bpw.classify_pr(pr(2471))
    assert not any(e["kind"] == "protocol-breach" for e in evs)


def test_pr_without_evidence_and_no_exception_fires():
    evs = bpw.classify_pr(pr(2471, body="Did the thing. Merged."))
    flagged, _ = bpw.scan(evs, set())
    assert [e["key"] for e in flagged] == ["protocol-breach:2471"]


def test_exception_marker_suppresses_the_flag():
    body = ("Did the thing. Merged under Shawn's explicit word: "
            "9.5-bar exception.")
    evs = bpw.classify_pr(pr(2325, body=body))
    assert not any(e["kind"] == "protocol-breach" for e in evs)


def test_exception_in_comments_suppresses_the_flag():
    evs = bpw.classify_pr(pr(2325, body="Did the thing.",
                             comments_text="director's word: 9.5-bar "
                                           "exception recorded"))
    assert not any(e["kind"] == "protocol-breach" for e in evs)


def test_bare_shawns_word_without_number_flags():
    # L22: no exception without his explicit real-numbered word.
    # A bare "Shawn's word" is the #2325 fraud pattern, not an exception.
    evs = bpw.classify_pr(pr(2401, body="Merged on Shawn's word."))
    flagged, _ = bpw.scan(evs, set())
    assert "protocol-breach:2401" in {e["key"] for e in flagged}


def test_bare_exception_claim_without_attribution_flags():
    evs = bpw.classify_pr(pr(2402, body="Merged. 9.5-bar exception."))
    flagged, _ = bpw.scan(evs, set())
    assert "protocol-breach:2402" in {e["key"] for e in flagged}


def test_negated_exception_flags():
    # "Per Shawn's word, this is not a 9.5-bar exception" denies the
    # exception — the negation must not suppress the flag.
    evs = bpw.classify_pr(
        pr(2403, body="Per Shawn's word, this is not a 9.5-bar exception."))
    flagged, _ = bpw.scan(evs, set())
    assert "protocol-breach:2403" in {e["key"] for e in flagged}


def test_denied_exception_flags():
    # Adversarial prose: attribution present, the "exception" explicitly
    # denied, no real number anywhere near the attribution.
    evs = bpw.classify_pr(
        pr(2404, body="Shawn's word: the exception was explicitly denied."))
    flagged, _ = bpw.scan(evs, set())
    assert "protocol-breach:2404" in {e["key"] for e in flagged}


def test_approved_by_shawn_with_number_suppresses():
    evs = bpw.classify_pr(
        pr(2405, body="Approved by Shawn, scored 9.6, exception recorded."))
    assert not any(e["kind"] == "protocol-breach" for e in evs)


def test_distant_number_does_not_launder_claim():
    # A real number 200+ chars from the attribution cannot launder the
    # claim — the evidence must sit near the attribution.
    body = "Merged on Shawn's word. " + "x" * 200 + " See run 9.7 for details."
    evs = bpw.classify_pr(pr(2406, body=body))
    flagged, _ = bpw.scan(evs, set())
    assert "protocol-breach:2406" in {e["key"] for e in flagged}


def test_evidence_grammar_is_exact():
    # "##Evidence" without the space, or "### Evidence", is not the section.
    evs = bpw.classify_pr(pr(2471, body="##Evidence\n- x"))
    kinds = {e["kind"] for e in evs}
    assert "protocol-breach" in kinds


# --- normalization-of-deviance regression: 17 silent merges -------------------

SILENT_MERGES = [
    (2423, "Relay merge-watch skip"),
    (2401, "Director click 1"), (2402, "Director click 2"),
    (2403, "Director click 3"), (2404, "Director click 4"),
    (2405, "Director click 5"), (2406, "Director click 6"),
    (2407, "Director click 7"), (2408, "Director click 8"),
    (2409, "Director click 9"), (2410, "Director click 10"),
    (2411, "Director click 11"), (2412, "Director click 12"),
    (2413, "Director click 13"), (2414, "Director click 14"),
    (2415, "Director click 15"), (2416, "Director click 16"),
]


def test_seventeen_prior_silent_merges_all_fire():
    """The normalization-of-deviance class is the regression test.

    Seventeen synthetic merges modeled on the silent-merge class
    (no ## Evidence, no exception, no post) must ALL still fire —
    the watchdog does not learn to tolerate them.
    """
    events = []
    for n, title in SILENT_MERGES:
        events.extend(bpw.classify_pr(
            pr(n, title=title, body="Merged per director click.")))
    flagged, _ = bpw.scan(events, set())
    flagged_keys = {e["key"] for e in flagged}
    for n, _ in SILENT_MERGES:
        assert f"protocol-breach:{n}" in flagged_keys, n
    assert len(flagged) == 17


# --- silent-override (direct push) --------------------------------------------

def test_direct_push_commit_fires():
    c = {"oid": "d" * 40, "message": "hotfix: adjust timeout",
         "date": "2026-10-12T00:00:00Z"}
    ev = bpw.classify_commit(c, pr_merge_oids=set())
    assert ev is not None
    assert ev["key"] == "silent-override:" + "d" * 12


def test_pr_merge_commits_do_not_fire():
    sha = "e" * 40
    cases = [
        {"oid": sha, "message": "Some title (#2471)"},          # squash
        {"oid": "f" * 40,
         "message": "Merge pull request #2472 from naya2/x"},  # merge
        {"oid": "0" * 40, "message": "Rebased title"},          # in PR set
    ]
    oids = {sha, "0" * 40}
    for c in cases:
        assert bpw.classify_commit(c, oids) is None, c["message"]


# --- idempotency ----------------------------------------------------------------

def test_watchdog_rescan_after_its_own_post_is_silent():
    p = pr(2471, body="Merged.")
    events = bpw.classify_pr(p)
    flagged, _ = bpw.scan(events, set())
    assert len(flagged) == 1
    body = bpw.render_body(flagged, [], 7, 1, 0)
    posted = bpw.extract_marker_keys([body])
    flagged2, _ = bpw.scan(events, posted)
    assert flagged2 == []


def test_duplicate_keys_collapse_to_one_flag():
    p = pr(2455, title="Revert #2455 — invalid delegated-merge-authority "
                       "invocation",
           body="LAW verdict on the invalid merge authority")
    events = bpw.classify_pr(p)
    # the revert names #2455 and the adjudication names #2455: one key
    flagged, _ = bpw.scan(events, set())
    keys = [e["key"] for e in flagged]
    assert keys.count("invalid-authority:2455") == 1


# --- marker extraction -------------------------------------------------------------

def test_extract_marker_keys_covers_all_three_formats():
    bodies = ["<!-- breach-post:invalid-authority:2455 -->",
              "<!-- breach-post:protocol-breach:2471 -->",
              "<!-- breach-post:silent-override:abc123def456 -->"]
    keys = bpw.extract_marker_keys(bodies)
    assert keys == {"invalid-authority:2455",
                    "protocol-breach:2471",
                    "silent-override:abc123def456"}


# --- report upsert ---------------------------------------------------------------

def test_find_marker_comment_searches_all_pages(monkeypatch):
    page1 = [{"id": i, "body": f"comment {i}"} for i in range(100)]
    page2 = [{"id": 101, "body": "<!-- breach-post-watch -->\nold"}]
    calls = []

    def fake_req(path, method="GET", data=None, graphql=False):
        calls.append(path)
        return page1 if "&page=1" in path else page2

    monkeypatch.setattr(bpw, "_req", fake_req)
    assert bpw.find_marker_comment("o", "n") == 101
    assert any("&page=2" in c for c in calls)


def test_find_marker_comment_returns_none_when_absent(monkeypatch):
    def fake_req(path, method="GET", data=None, graphql=False):
        return [{"id": 1, "body": "nothing here"}]

    monkeypatch.setattr(bpw, "_req", fake_req)
    assert bpw.find_marker_comment("o", "n") is None


# --- end-to-end --------------------------------------------------------------------

def test_main_end_to_end_flags_missing_post_and_upserts(monkeypatch):
    """Scripted run of the real job: fetch -> classify -> scan -> upsert.

    One merged PR with no ## Evidence, one attributable main commit,
    #2175's marker search crossing a page boundary (exercises pagination).
    Asserts the upsert body carries the breach marker and exactly one
    upsert happens.
    """
    pr_node = {
        "number": 2471, "title": "T", "body": "merged without evidence",
        "mergedAt": "2026-10-12T15:00:00Z", "baseRefName": "main",
        "author": {"login": "x"}, "mergeCommit": {"oid": "a" * 40},
        "comments": {"nodes": []},
    }
    commit_nodes = [{"oid": "a" * 40, "message": "T (#2471)",
                     "committedDate": "2026-10-12T15:00:00Z"}]
    page1 = [{"id": i, "body": f"c{i}"} for i in range(100)]
    upserts = []

    def fake_req(path, method="GET", data=None, graphql=False):
        if graphql:
            q = (data or {}).get("query", "")
            if "search(" in q:
                return {"data": {"search": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "nodes": [pr_node]}}}
            return {"data": {"repository": {"object": {"history": {
                "pageInfo": {"hasNextPage": False, "endCursor": None},
                "nodes": commit_nodes}}}}}
        if method == "POST" and "issues/2175/comments" in path:
            upserts.append(("POST", data["body"]))
            return {}
        if method == "PATCH":
            upserts.append(("PATCH", data["body"]))
            return {}
        if "&page=1" in path:
            return page1
        return []  # page 2: short page -> pagination stops

    monkeypatch.setattr(bpw, "_req", fake_req)
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/n")
    monkeypatch.setenv("GH_TOKEN", "x")
    bpw.main()
    assert len(upserts) == 1
    method, body = upserts[0]
    assert method == "POST"  # no prior marker comment -> first post
    assert "breach-post:protocol-breach:2471" in body
    assert "All clear" not in body


def test_main_patches_existing_report_comment(monkeypatch):
    """Second run: the marker comment already exists -> PATCH, not POST."""
    marker_comment = {"id": 999,
                      "body": "<!-- breach-post-watch -->\nold report"}
    upserts = []

    def fake_req(path, method="GET", data=None, graphql=False):
        if graphql:
            q = (data or {}).get("query", "")
            if "search(" in q:
                return {"data": {"search": {
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                    "nodes": []}}}
            return {"data": {"repository": {"object": {"history": {
                "pageInfo": {"hasNextPage": False, "endCursor": None},
                "nodes": []}}}}}
        if method == "POST" and "issues/2175/comments" in path:
            upserts.append(("POST", data["body"]))
            return {}
        if method == "PATCH":
            upserts.append(("PATCH", data["body"]))
            return {}
        return [marker_comment]  # short page -> pagination stops

    monkeypatch.setattr(bpw, "_req", fake_req)
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/n")
    monkeypatch.setenv("GH_TOKEN", "x")
    bpw.main()
    assert len(upserts) == 1
    method, body = upserts[0]
    assert method == "PATCH"
    assert "All clear" in body


# --- fail-closed -----------------------------------------------------------------

def test_api_failure_is_unable_to_verify_never_silent(capsys, monkeypatch):
    import urllib.error

    def boom(*a, **k):
        raise urllib.error.URLError("boom")
    monkeypatch.setattr(bpw, "fetch_merged_prs", boom)
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/n")
    with pytest.raises(SystemExit) as ei:
        bpw.main()
    assert ei.value.code == 1
    out = capsys.readouterr().out
    assert "unable to verify" in out
