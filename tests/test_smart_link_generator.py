#!/usr/bin/env python3
"""Tests for the Smart-Link generator + gate (tools/smart_link.py).

All network access is faked via FakeVerifier. No test hits GitHub.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import smart_link as sl  # noqa: E402

GOOD_PATH = ("BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/"
             "TEST/SN-999/IB-SMART-NOTE-20261004-sn999-test.md")
GOOD_URL = ("https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/" + GOOD_PATH)


def make_index(entries):
    return {"entries": entries}


def entry(sid="SN-999", path=GOOD_PATH, url=GOOD_URL, status="ACTIVE",
          scope="PUBLIC"):
    return {"smart_note_id": sid, "projection_path": path,
            "smart_link": url, "smart_link_status": status, "scope": scope,
            "title": "Test", "truth_state": "CANDIDATE"}


# --- link building -----------------------------------------------------------

def test_emitted_link_is_main_only():
    url = sl.smart_link_for(GOOD_PATH)
    assert url == GOOD_URL
    assert "/blob/main/" in url


def test_branch_ref_in_path_refused():
    with pytest.raises(ValueError, match="REF_IN_PATH_REJECTED"):
        sl.smart_link_for("BRAIN/blob/naya4/x/SMART-NOTES/y.md")


def test_path_traversal_refused():
    with pytest.raises(ValueError, match="PATH_TRAVERSAL_REJECTED"):
        sl.smart_link_for("BRAIN/05-MEMORY/SMART-NOTES/../secret.md")


def test_non_smart_note_path_refused():
    with pytest.raises(ValueError, match="NOT_A_SMART_NOTE_PROJECTION"):
        sl.smart_link_for("HUB/app/index.html")


def test_non_markdown_refused():
    with pytest.raises(ValueError, match="NOT_MARKDOWN"):
        sl.smart_link_for("BRAIN/05-MEMORY/SMART-NOTES/x.wav")


def test_empty_path_refused_with_clear_error():
    with pytest.raises(ValueError, match="EMPTY_PROJECTION_PATH"):
        sl.smart_link_for("")


# --- generate -----------------------------------------------------------------

def test_generate_verifies_against_main():
    idx = make_index([])
    frag = sl.generate(GOOD_PATH, idx, verifier=sl.FakeVerifier({GOOD_PATH}),
                       rev="abc123")
    assert frag["smart_link"] == GOOD_URL
    # no index entry -> scope defaults to PRIVATE (fail closed on visibility)
    assert frag["smart_link_status"] == "ACTIVE_AUTH_GATED"
    assert frag["smart_link_verified_rev"] == "abc123"
    assert frag["smart_link_verified_at"]


def test_generate_public_scope_gets_active():
    idx = make_index([entry(scope="PUBLIC")])
    frag = sl.generate(GOOD_PATH, idx, verifier=sl.FakeVerifier({GOOD_PATH}))
    assert frag["smart_link_status"] == "ACTIVE"


def test_generate_refuses_path_missing_on_main():
    idx = make_index([])
    with pytest.raises(ValueError, match="NOT_ON_MAIN"):
        sl.generate(GOOD_PATH, idx, verifier=sl.FakeVerifier(set()))


def test_generate_private_scope_gets_auth_gated_status():
    idx = make_index([entry(scope="PRIVATE")])
    frag = sl.generate(GOOD_PATH, idx, verifier=sl.FakeVerifier({GOOD_PATH}))
    assert frag["smart_link_status"] == "ACTIVE_AUTH_GATED"


def test_generate_without_verifier_is_pending():
    frag = sl.generate(GOOD_PATH, make_index([]), verifier=None)
    assert frag["smart_link_status"] == "PENDING"
    assert frag["smart_link_verified_at"] == ""


def test_generate_refuses_collision():
    other = entry(sid="SN-998", path="OTHER/path.md", url=GOOD_URL)
    idx = make_index([other])
    with pytest.raises(ValueError, match="COLLISION"):
        sl.generate(GOOD_PATH, idx, verifier=sl.FakeVerifier({GOOD_PATH}))


def test_malformed_note_missing_projection_gives_clear_error_not_broken_link():
    idx = make_index([])
    with pytest.raises(ValueError) as ei:
        sl.generate("", idx, verifier=sl.FakeVerifier({GOOD_PATH}))
    assert "EMPTY_PROJECTION_PATH" in str(ei.value)
    # and no URL was ever produced
    assert not sl.validate_shape("")


# --- gate: shape ---------------------------------------------------------------

def test_shape_passes_main_only():
    assert sl.check_shape(make_index([entry()])) == []


def test_shape_fails_branch_url():
    bad = entry(url="https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya4/x/SMART-NOTES/y.md")
    v = sl.check_shape(make_index([bad]))
    assert len(v) == 1 and v[0].startswith("SHAPE")


def test_shape_fails_sha_url():
    bad = entry(url="https://github.com/SoulSchoolAcademy/NayaPOWER/blob/abc123/BRAIN/x.md")
    assert sl.check_shape(make_index([bad]))


# --- gate: resolves --------------------------------------------------------------

def test_resolves_passes_when_on_main():
    v = sl.check_resolves(make_index([entry()]), sl.FakeVerifier({GOOD_PATH}))
    assert v == []


def test_resolves_fails_when_missing_on_main():
    v = sl.check_resolves(make_index([entry()]), sl.FakeVerifier(set()))
    assert len(v) == 1 and v[0].startswith("RESOLVES")


def test_resolves_skips_non_active():
    v = sl.check_resolves(make_index([entry(status="PENDING")]),
                          sl.FakeVerifier(set()))
    assert v == []


# --- gate: unique -----------------------------------------------------------------

def test_unique_passes_distinct_links():
    idx = make_index([entry(sid="SN-1", url=GOOD_URL),
                      entry(sid="SN-2", url=GOOD_URL + "2")])
    assert sl.check_unique(idx) == []


def test_unique_fails_duplicate_link():
    idx = make_index([entry(sid="SN-1"), entry(sid="SN-2")])
    v = sl.check_unique(idx)
    assert len(v) == 1 and "SN-2" in v[0] and "SN-1" in v[0]


# --- gate: complete -----------------------------------------------------------------

def test_complete_passes_when_all_covered():
    idx = make_index([entry()])
    assert sl.check_complete(idx, [GOOD_PATH]) == []


def test_complete_fails_uncovered_projection():
    idx = make_index([])
    v = sl.check_complete(idx, [GOOD_PATH])
    assert len(v) == 1 and v[0].startswith("COMPLETE")


def test_complete_counts_superseded_tombstones_as_covered():
    e = entry()
    e["superseded_projections"] = [{"projection_path": "BRAIN/05-MEMORY/SMART-NOTES/old.md",
                                    "status": "SUPERSEDED_TOMBSTONE"}]
    idx = make_index([e])
    assert sl.check_complete(idx, [GOOD_PATH, "BRAIN/05-MEMORY/SMART-NOTES/old.md"]) == []


def test_complete_ignores_non_note_files():
    assert sl.check_complete(make_index([]), ["HUB/app/x.md"]) == []


# --- gate: no-branch-links ------------------------------------------------------------

def test_no_branch_links_passes_clean_diff():
    diff = "+see https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/x.md\n"
    assert sl.check_no_branch_links(diff) == []


def test_no_branch_links_fails_branch_url():
    diff = "+see https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya4/x/BRAIN/y.md\n"
    v = sl.check_no_branch_links(diff)
    assert len(v) == 1 and v[0].startswith("BRANCH_LINK")


# --- backfill --------------------------------------------------------------------------

def test_backfill_stamps_verified_entries():
    idx = make_index([entry(scope="PRIVATE"), entry(sid="SN-2", scope="PUBLIC")])
    rep = sl.backfill(idx, sl.FakeVerifier({GOOD_PATH}), rev="rev1")
    assert rep["stamped"] == 2 and rep["broken"] == []
    assert idx["entries"][0]["smart_link_verified_rev"] == "rev1"
    assert idx["entries"][0]["smart_link_verified_at"]
    assert idx["entries"][0]["smart_link_status"] == "ACTIVE_AUTH_GATED"
    assert idx["entries"][1]["smart_link_status"] == "ACTIVE"


def test_backfill_marks_missing_projection_broken():
    idx = make_index([entry()])
    rep = sl.backfill(idx, sl.FakeVerifier(set()), rev="rev1")
    assert rep["broken"] == ["SN-999"]
    assert idx["entries"][0]["smart_link_status"] == "BROKEN"


def test_backfill_dry_run_does_not_mutate():
    idx = make_index([entry()])
    before = idx["entries"][0].get("smart_link_verified_rev")
    sl.backfill(idx, sl.FakeVerifier({GOOD_PATH}), rev="rev1", dry_run=True)
    assert idx["entries"][0].get("smart_link_verified_rev") == before
