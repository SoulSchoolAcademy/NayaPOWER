from urllib.parse import parse_qs, urlparse

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
