"""Tests for the merge-consensus gate's paginated API reader.

tools/check_merge_consensus.py :: api_get must follow GitHub's
Link: rel="next" pagination at per_page=100, so reviews and scorecards on
busy PRs (>30 comments) stay gate-visible, while single-object endpoints
pass through untouched. Rate-limited responses (403/429) are retried with
exponential backoff instead of failing the gate.
"""
import io
import json
import sys
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_merge_consensus import api_get  # noqa: E402


class _FakeHeaders(dict):
    def get(self, key, default=None):
        return super().get(key, default)


class _FakeResponse:
    """Minimal stand-in for the urlopen context manager."""

    def __init__(self, payload, link=""):
        self._body = json.dumps(payload).encode("utf-8")
        self.headers = _FakeHeaders({"Link": link})

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self, *args):
        return self._body


def _http_error(code):
    return urllib.error.HTTPError(
        url="https://api.github.com/x", code=code,
        msg="rate limited", hdrs=None, fp=io.BytesIO(b"{}"))


def test_multi_page_list_concatenates():
    """Two pages of a list endpoint come back as one concatenated list,
    and the first request asks for the larger page size."""
    page1 = _FakeResponse(
        [{"id": 1}, {"id": 2}],
        link=('<https://api.github.com/repos/o/r/issues/1/comments?page=2>; rel="next", '
              '<https://api.github.com/repos/o/r/issues/1/comments?page=2>; rel="last"'),
    )
    page2 = _FakeResponse([{"id": 3}])
    with patch("urllib.request.urlopen") as m:
        m.side_effect = [page1, page2]
        result = api_get("/repos/o/r/issues/1/comments", "token")
    assert result == [{"id": 1}, {"id": 2}, {"id": 3}]
    assert m.call_count == 2
    first_url = m.call_args_list[0].args[0].full_url
    assert "per_page=100" in first_url
    # Second page URL is followed verbatim from the Link header.
    second_url = m.call_args_list[1].args[0].full_url
    assert "page=2" in second_url


def test_single_dict_passes_through():
    """Single-object endpoints (e.g. the PR itself) return the dict as-is,
    not wrapped in a list."""
    pr = _FakeResponse({"number": 2261, "user": {"login": "naya"}})
    with patch("urllib.request.urlopen", side_effect=[pr]):
        result = api_get("/repos/o/r/pulls/2261", "token")
    assert result == {"number": 2261, "user": {"login": "naya"}}


def test_empty_list_returns_empty():
    """A list endpoint with zero items returns [], not None."""
    empty = _FakeResponse([])
    with patch("urllib.request.urlopen", side_effect=[empty]):
        result = api_get("/repos/o/r/pulls/1/reviews", "token")
    assert result == []


def test_retry_on_429_then_succeeds():
    """A 429 rate-limit on the first attempt is retried (exponential
    backoff) and the eventual page is returned."""
    ok = _FakeResponse([{"id": 7}])
    with patch("urllib.request.urlopen",
               side_effect=[_http_error(429), ok]) as m, \
         patch("check_merge_consensus.time.sleep") as sleep_mock:
        result = api_get("/repos/o/r/issues/1/comments", "token")
    assert result == [{"id": 7}]
    assert m.call_count == 2
    sleep_mock.assert_called_once_with(1)  # 2**(1-1)


def test_non_retryable_error_raises():
    """A non-rate-limit failure (e.g. 404) is not retried: it propagates."""
    with patch("urllib.request.urlopen",
               side_effect=[_http_error(404)]) as m:
        try:
            api_get("/repos/o/r/pulls/999999", "token")
        except urllib.error.HTTPError as e:
            assert e.code == 404
        else:
            raise AssertionError("expected HTTPError to propagate")
    assert m.call_count == 1
