#!/usr/bin/env python3
"""Tests for tools/law_landing_receipt_scan.py — the Scorecard Law post-merge
tripwire. Pure core only: no network, no git, no GitHub. The live scan path is
covered by a stub-API integration test (local HTTP server).

Fail-closed bar: every malformed/ambiguous input must produce UNKNOWN or
"no receipt found", never a false CLEAN or a false VIOLATION.
"""

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from law_landing_receipt_scan import (  # noqa: E402
    classify,
    is_director_landing,
    receipt_predates,
    verdict_table,
)

MERGED_AT = "2026-10-08T13:58:42Z"


def comment(cid, body, created_at, author="SoulSchoolAcademy"):
    return {"id": cid, "body": body, "created_at": created_at,
            "user": {"login": author}}


def good_receipt(cid=6061497970):
    return comment(
        cid,
        "## [NAYA 4] SIGN OUT — scorecard receipt for #1864\n\n"
        "1. ENUMERATE: options A/B/C. 2. SCORE: 9/7/5. 3. GATE: reversible. "
        "4. DECIDE: A. 5. RECEIPT: posted here.",
        "2026-10-08T13:58:29Z")


# ----------------------------------------------- is_director_landing ---

def test_director_by_committer_github():
    # The empirical Director-merge signal (web/API merge as Shawn).
    assert is_director_landing("Shawn Vibert", "GitHub") is True


def test_director_by_name():
    assert is_director_landing("Shawn Vibert", "Shawn Vibert") is True


def test_seat_identity_is_not_director():
    # BUG-001: author Naya 4, committer Naya 4.
    assert is_director_landing("Naya 4", "Naya 4") is False


def test_missing_identities_fail_closed():
    # Unknown identities are NOT director landings (never a false exempt).
    assert is_director_landing(None, None) is False
    assert is_director_landing("", "") is False


# ------------------------------------------------------- receipt_predates ---

def test_receipt_found_before_merge():
    r = receipt_predates([good_receipt()], 1864, MERGED_AT)
    assert r is not None and r["comment_id"] == 6061497970


def test_receipt_after_merge_does_not_count():
    # A receipt posted AFTER the merge is not a pre-merge receipt.
    late = comment(1, "scorecard receipt for #1864", "2026-10-08T13:59:00Z")
    assert receipt_predates([late], 1864, MERGED_AT) is None


def test_receipt_for_other_pr_does_not_count():
    other = comment(2, "scorecard receipt for #1863", "2026-10-08T13:55:00Z")
    assert receipt_predates([other], 1864, MERGED_AT) is None


def test_scorecard_word_without_pr_reference_does_not_count():
    vague = comment(3, "here is my scorecard, looks good", "2026-10-08T13:00:00Z")
    assert receipt_predates([vague], 1864, MERGED_AT) is None


def test_pr_reference_without_receipt_word_does_not_count():
    plain = comment(4, "merged #1864 just now", "2026-10-08T13:50:00Z")
    assert receipt_predates([plain], 1864, MERGED_AT) is None


def test_bare_number_reference_counts():
    bare = comment(5, "scorecard for 1864: enumerate/score/gate/decide/receipt",
                   "2026-10-08T13:00:00Z")
    r = receipt_predates([bare], 1864, MERGED_AT)
    assert r is not None


def test_bare_number_must_be_standalone_token():
    # "#18640" must not match PR 1864 (no false positive).
    tricky = comment(6, "scorecard for #18640", "2026-10-08T13:00:00Z")
    assert receipt_predates([tricky], 1864, MERGED_AT) is None


def test_earliest_receipt_wins():
    c1 = comment(10, "scorecard #1864 v1", "2026-10-08T12:00:00Z")
    c2 = comment(11, "scorecard #1864 v2", "2026-10-08T13:00:00Z")
    r = receipt_predates([c2, c1], 1864, MERGED_AT)
    assert r["comment_id"] == 10


def test_malformed_comments_are_ignored_never_counted():
    junk = [{"no": "body"}, {"body": None, "created_at": "not-a-date"},
            {"body": "scorecard #1864", "created_at": None}]
    assert receipt_predates(junk, 1864, MERGED_AT) is None


def test_malformed_merged_at_never_matches():
    assert receipt_predates([good_receipt()], 1864, "not-a-date") is None
    assert receipt_predates([good_receipt()], 1864, None) is None


# ---------------------------------------------------------------- classify ---

def test_seat_landing_with_receipt_is_clean():
    assert classify("Naya 4", "Naya 4", {"comment_id": 1}) == "CLEAN"


def test_seat_landing_without_receipt_is_violation():
    # BUG-001 class.
    assert classify("Naya 4", "Naya 4", None) == "VIOLATION"


def test_director_landing_is_exempt_even_without_receipt():
    assert classify("Shawn Vibert", "GitHub", None) == "EXEMPT_DIRECTOR"


def test_receipt_beats_director_exemption():
    # A receipt on a director landing is CLEAN, not EXEMPT.
    assert classify("Shawn Vibert", "GitHub", {"comment_id": 1}) == "CLEAN"


def test_missing_identities_without_receipt_is_unknown():
    assert classify(None, None, None) == "UNKNOWN"
    assert classify("", "", None) == "UNKNOWN"


# ------------------------------------------------------------ verdict_table ---

def test_verdict_table_renders_rows():
    findings = [
        {"sha": "aca944b5" + "0" * 32, "pr": 1839, "author": "Naya 4",
         "committer": "Naya 4", "verdict": "VIOLATION", "receipt": None},
        {"sha": "b19b242f" + "0" * 32, "pr": 1864, "author": "Shawn Vibert",
         "committer": "GitHub", "verdict": "EXEMPT_DIRECTOR",
         "receipt": {"comment_id": 6061497970,
                     "created_at": "2026-10-08T13:58:29Z"}},
    ]
    t = verdict_table(findings)
    assert "**VIOLATION**" in t and "**EXEMPT_DIRECTOR**" in t
    assert "#1839" in t and "#1864" in t


# --------------------------------- stub-API integration (no real network) ---

PULLS_PAGE = [
    {"number": 1864, "merged": True, "merged_at": MERGED_AT,
     "updated_at": MERGED_AT, "merge_commit_sha": "a" * 40},
    {"number": 1863, "merged": True, "merged_at": "2026-10-08T13:55:27Z",
     "updated_at": "2026-10-08T13:55:27Z", "merge_commit_sha": "b" * 40},
    {"number": 1862, "merged": False, "merged_at": None,
     "updated_at": "2026-10-08T13:00:00Z", "merge_commit_sha": None},
]
COMMITS = {
    "a" * 40: {"commit": {"author": {"name": "Naya 4"},
                          "committer": {"name": "Naya 4"}}},
    "b" * 40: {"commit": {"author": {"name": "Shawn Vibert"},
                          "committer": {"name": "GitHub"}}},
}
COMMENTS = [
    {"id": 6061497970,
     "body": "scorecard receipt for #1864: enumerate/score/gate/decide/receipt",
     "created_at": "2026-10-08T13:58:29Z", "user": {"login": "x"}},
]


class Stub(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/repos/o/r/pulls?") or \
                self.path.startswith("/repos/o/r/pulls&"):
            payload = PULLS_PAGE
        elif "/pulls" in self.path:
            payload = PULLS_PAGE
        elif "/commits/" in self.path:
            sha = self.path.rsplit("/commits/", 1)[1].split("?")[0]
            payload = COMMITS[sha]
        elif "comments" in self.path:
            payload = COMMENTS
        else:
            payload = {}
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


def _stubbed(monkeypatch):
    import law_landing_receipt_scan as tool
    server = HTTPServer(("127.0.0.1", 0), Stub)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setenv("GITHUB_API_BASE",
                       f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setenv("GITHUB_TOKEN", "stub-token")
    # Route the tool at the stub's short repo path.
    monkeypatch.setattr(tool, "OWNER", "o")
    monkeypatch.setattr(tool, "REPO", "r")
    return tool, server


def test_end_to_end_scan_against_stub_api(monkeypatch):
    tool, server = _stubbed(monkeypatch)
    findings, any_unknown = tool.scan(24)
    server.shutdown()
    by_pr = {f["pr"]: f["verdict"] for f in findings}
    # 1864: seat landing + pre-merge receipt -> CLEAN
    assert by_pr[1864] == "CLEAN"
    # 1863: director landing -> EXEMPT_DIRECTOR
    assert by_pr[1863] == "EXEMPT_DIRECTOR"
    # 1862: not merged -> not judged at all
    assert 1862 not in by_pr
    assert not any_unknown


def test_end_to_end_violation_against_stub_api(monkeypatch):
    import law_landing_receipt_scan as tool2
    tool, server = _stubbed(monkeypatch)
    assert tool is tool2
    monkeypatch.setattr(tool, "feed_comments", lambda hours: [])  # empty feed
    findings, any_unknown = tool.scan(24)
    server.shutdown()
    by_pr = {f["pr"]: f["verdict"] for f in findings}
    # BUG-001 class: seat landing, no receipt -> VIOLATION
    assert by_pr[1864] == "VIOLATION"
    # Director landing stays exempt even with an empty feed.
    assert by_pr[1863] == "EXEMPT_DIRECTOR"
    assert not any_unknown
