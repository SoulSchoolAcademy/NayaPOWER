"""Receipt URL checks must distinguish dead links from temporary outages."""
import io
import sys
from pathlib import Path
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_pr_receipt  # noqa: E402


class Response:
    status = 200
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, size=-1):
        return b"x"


def http_error(code):
    return urllib.error.HTTPError(
        "https://example.test/evidence", code, "error", {}, io.BytesIO(b"{}")
    )


def test_confirmed_404_is_dead_evidence():
    check_pr_receipt.URL_CHECK_RESULTS.clear()
    with patch("urllib.request.urlopen", side_effect=[http_error(404), http_error(404)]):
        assert not check_pr_receipt.check_url("https://example.test/evidence")
    assert check_pr_receipt.URL_CHECK_RESULTS["https://example.test/evidence"]["state"] == "DEAD"


def test_network_outage_is_not_misreported_as_dead_evidence():
    check_pr_receipt.URL_CHECK_RESULTS.clear()
    outage = urllib.error.URLError("temporary DNS outage")
    with patch("urllib.request.urlopen", side_effect=[outage, outage]):
        assert not check_pr_receipt.check_url("https://example.test/evidence")
    assert check_pr_receipt.URL_CHECK_RESULTS["https://example.test/evidence"]["state"] == "UNAVAILABLE"


def test_forbidden_url_is_unavailable_not_dead():
    check_pr_receipt.URL_CHECK_RESULTS.clear()
    with patch("urllib.request.urlopen", side_effect=[http_error(403), http_error(403)]):
        assert not check_pr_receipt.check_url("https://example.test/private-evidence")
    assert check_pr_receipt.URL_CHECK_RESULTS["https://example.test/private-evidence"]["state"] == "UNAVAILABLE"


def test_head_rejected_but_get_works_is_live():
    check_pr_receipt.URL_CHECK_RESULTS.clear()
    with patch("urllib.request.urlopen", side_effect=[http_error(405), Response()]):
        assert check_pr_receipt.check_url("https://example.test/evidence")
    assert check_pr_receipt.URL_CHECK_RESULTS["https://example.test/evidence"]["state"] == "LIVE"
