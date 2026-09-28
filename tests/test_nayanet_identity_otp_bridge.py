from pathlib import Path

IDENTITY = Path("NAYANET BRIDGE INDENITY CODE.html")


def test_identity_uses_existing_user_otp_not_anonymous_auth():
    html = IDENTITY.read_text(encoding="utf-8")
    assert "signInWithOtp" in html
    assert "shouldCreateUser: false" in html
    assert "verifyOtp" in html
    assert "signInAnonymously" not in html


def test_identity_transfers_authenticated_session_without_query_tokens():
    html = IDENTITY.read_text(encoding="utf-8")
    assert "#access_token=" in html
    assert "&refresh_token=" in html
    assert "access_token=" not in html.split("#access_token=", 1)[0]


def test_identity_keeps_canonical_owner_fail_closed():
    html = IDENTITY.read_text(encoding="utf-8")
    assert "shouldCreateUser: false" in html
    assert "Do not change the Intelligent Block owner" in html
