from urllib.parse import parse_qs, urlparse

import hashlib

import pytest

from tools import board_claim_scan as scanner


def fake_board(monkeypatch, count, *, final_count=None, truncate=False):
    calls = []
    metadata_reads = 0

    def get(method, path):
        nonlocal metadata_reads
        calls.append(path)
        if "/comments?" not in path:
            metadata_reads += 1
            return {"comments": final_count if metadata_reads > 1 and final_count is not None else count}
        page = int(parse_qs(urlparse(path).query)["page"][0])
        rows = [{"id": i, "body": "active-tail-work" if i == count else "unrelated"}
                for i in range((page - 1) * 100 + 1, min(page * 100, count) + 1)]
        return rows[:-1] if truncate else rows

    monkeypatch.setattr(scanner, "gh_api", get)
    return calls


@pytest.mark.parametrize("count", [0, 1, 100, 200, 201, 350, 800])
def test_board_tail_is_newest_window(monkeypatch, count):
    calls = fake_board(monkeypatch, count)
    rows = scanner.fetch_board_tail("1354")
    assert [r["id"] for r in rows] == list(range(max(1, count - 199), count + 1))
    if count:
        collisions, _ = scanner.scan("active-tail-work", rows)
        assert collisions[0][0]["id"] == count
    assert len([c for c in calls if "/comments?" in c]) <= 3


def test_moving_board_cannot_report_clear(monkeypatch):
    fake_board(monkeypatch, 350, final_count=351)
    with pytest.raises(RuntimeError, match="BOARD_CHANGED"):
        scanner.fetch_board_tail("1354")


def test_incomplete_board_cannot_report_clear(monkeypatch):
    fake_board(monkeypatch, 350, truncate=True)
    with pytest.raises(RuntimeError, match="BOARD_COVERAGE"):
        scanner.fetch_board_tail("1354")


@pytest.mark.parametrize("count", [None, -1, True, "350"])
def test_invalid_comment_count_is_unknown(monkeypatch, count):
    monkeypatch.setattr(scanner, "gh_api", lambda *args: {"comments": count})
    with pytest.raises(RuntimeError, match="BOARD_COMMENT_COUNT"):
        scanner.fetch_board_tail("1354")


@pytest.mark.parametrize("rows", [
    [{"id": 1, "body": "a"}, {"id": 1, "body": "b"}],
    [{"id": 2, "body": "a"}, {"id": 1, "body": "b"}],
    [{"id": 1, "body": None}, {"id": 2, "body": "b"}],
])
def test_invalid_page_cannot_hide_claims(monkeypatch, rows):
    monkeypatch.setattr(scanner, "gh_api", lambda method, path:
                        rows if "/comments?" in path else {"comments": 2})
    with pytest.raises(RuntimeError, match="BOARD_COVERAGE"):
        scanner.fetch_board_tail("1354")


def test_cli_reports_unknown_when_board_moves(monkeypatch, tmp_path, capsys):
    fake_board(monkeypatch, 350, final_count=351)
    prs = tmp_path / "prs.json"
    prs.write_text("[]")
    assert scanner.main(["--work", "active-tail-work", "--prs-json", str(prs)]) == 3
    output = capsys.readouterr().out
    assert "ENVIRONMENT FAILURE" in output
    assert "VERDICT: CLEAR" not in output


def fake_prs(monkeypatch, count, *, duplicate=False):
    calls = []

    def get(method, path):
        calls.append(path)
        page = int(parse_qs(urlparse(path).query).get("page", ["1"])[0])
        return [{"number": 1 if duplicate else i, "title": "active-pr-claim" if i == count else "unrelated",
                 "head": {"ref": f"branch-{i}"}}
                for i in range((page - 1) * 100 + 1, min(page * 100, count) + 1)]

    monkeypatch.setattr(scanner, "gh_api", get)
    return calls


@pytest.mark.parametrize("count", [0, 1, 100, 101, 200, 999])
def test_all_open_pr_pages_participate_in_scan(monkeypatch, count):
    fake_prs(monkeypatch, count)
    rows = scanner.fetch_open_prs()
    assert len(rows) == count
    if count:
        collisions, _ = scanner.scan("active-pr-claim", rows)
        assert collisions[0][0]["id"] == count


def test_full_pr_page_ceiling_is_unknown(monkeypatch):
    calls = fake_prs(monkeypatch, 1000)
    with pytest.raises(RuntimeError, match="PR_PAGINATION_LIMIT"):
        scanner.fetch_open_prs()
    assert len(calls) == 10


def test_duplicate_pr_page_is_unknown(monkeypatch):
    fake_prs(monkeypatch, 101, duplicate=True)
    with pytest.raises(RuntimeError, match="PR_COVERAGE"):
        scanner.fetch_open_prs()


@pytest.mark.parametrize("data", [{"message": "error"}, [None], [{"number": 1, "title": "missing head"}]])
def test_malformed_pr_response_is_unknown(monkeypatch, data):
    monkeypatch.setattr(scanner, "gh_api", lambda *args: data)
    with pytest.raises(RuntimeError, match="PR_COVERAGE"):
        scanner.fetch_open_prs()


def fake_board_long_body(monkeypatch, body):
    def get(method, path):
        if "/comments?" in path:
            return [{"id": 1, "body": body}]
        return {"comments": 1}
    monkeypatch.setattr(scanner, "gh_api", get)


class TestBoardClaimFullBody:
    """P0-F5 sibling (tools/board_claim_scan.py:154): the scan answered from
    body[:2000] while verdicting completeness. Shaped by the falsification
    spec in PR #2477 review 6128553449 — falsify a claim carried BEYOND
    character 2000. All three fail pre-fix, pass post-fix."""

    def test_claim_token_beyond_char_2000_is_detected(self, monkeypatch):
        token = "full-auto-merge-v1"
        body = "x " * 1100 + f"stand down: this seat already claimed the {token} workstream"
        assert body.index(token) > 2000  # the falsifier sits past the old cut
        fake_board_long_body(monkeypatch, body)
        rows = scanner.fetch_board_tail("1354")
        collisions, _ = scanner.scan("repair: duplicate of full-auto-merge-v1 workstream", rows)
        assert len(collisions) == 1
        assert collisions[0][0]["id"] == 1

    def test_unigram_cluster_beyond_char_2000_is_detected(self, monkeypatch):
        tail = "coordination note: zebra quark vortex lantern drift continues"
        body = "x " * 1100 + tail
        assert body.index("zebra") > 2000  # the falsifier sits past the old cut
        fake_board_long_body(monkeypatch, body)
        rows = scanner.fetch_board_tail("1354")
        collisions, _ = scanner.scan("repair: zebra quark vortex lantern drift", rows)
        assert len(collisions) == 1

    def test_stored_text_is_source_bound_to_full_body(self, monkeypatch):
        body = "x " * 1100 + "final line of a long comment"
        assert len(body) > 2000
        fake_board_long_body(monkeypatch, body)
        item = scanner.fetch_board_tail("1354")[0]
        assert item["text"] == body
        assert item["text_full_len"] == len(body)
        assert item["text_source"] == "FULL"
        assert item["text_sha12"] == hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
