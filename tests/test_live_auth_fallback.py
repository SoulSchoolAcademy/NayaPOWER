import json
from urllib.parse import parse_qs
from unittest.mock import patch

import pytest

from tests.test_live_supabase_intelligent_blocks import _authenticated_session


def test_authenticated_session_refreshes_when_access_token_is_rejected():
    calls = []

    class Response:
        def __init__(self, payload):
            self.payload = payload

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return json.dumps(self.payload).encode()

    def fake_urlopen(request, timeout=10):
        calls.append((request.full_url, dict(request.headers), request.data))
        if request.full_url.endswith("/auth/v1/user"):
            from urllib.error import HTTPError
            raise HTTPError(request.full_url, 401, "Unauthorized", {}, None)
        return Response(
            {
                "access_token": "fresh-access-token",
                "refresh_token": "rotated-refresh-token",
                "user": {"id": "owner-123"},
            }
        )

    with patch("tests.test_live_supabase_intelligent_blocks.urlopen", fake_urlopen):
        session = _authenticated_session(
            "https://example.supabase.co",
            "expired-access",
            "publishable",
            "legitimate-refresh-token",
        )

    assert session["owner_id"] == "owner-123"
    assert session["access_token"] == "fresh-access-token"
    assert calls[1][0].endswith("/auth/v1/token?grant_type=refresh_token")
    assert parse_qs(calls[1][2].decode()) == {
        "refresh_token": ["legitimate-refresh-token"]
    }


def test_authenticated_session_does_not_use_access_token_as_refresh_token():
    from urllib.error import HTTPError

    def fake_urlopen(request, timeout=10):
        raise HTTPError(request.full_url, 401, "Unauthorized", {}, None)

    with patch("tests.test_live_supabase_intelligent_blocks.urlopen", fake_urlopen):
        with pytest.raises(HTTPError) as exc:
            _authenticated_session(
                "https://example.supabase.co",
                "expired-access",
                "publishable",
                None,
            )

    assert exc.value.code == 401
