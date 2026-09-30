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


def test_identity_otp_request_uses_a_non_consuming_verify_page_redirect():
    html = IDENTITY.read_text(encoding='utf-8')
    assert 'emailRedirectTo' in html
    assert 'verify=1' in html


def test_identity_verify_page_is_explicitly_ready_for_code_entry():
    html = IDENTITY.read_text(encoding='utf-8')
    assert 'NAYA_VERIFY_PAGE' in html
    assert 'Enter the six digits from the newest NayaNET email.' in html


def test_email_template_contains_both_otp_and_plain_navigation_link():
    template = Path('supabase/templates/nayanet_magic_link.html').read_text(encoding='utf-8')
    assert '{{ .Token }}' in template
    assert '{{ .RedirectTo }}' in template
    assert '{{ .ConfirmationURL }}' not in template
    assert 'OPEN NAYANET & ENTER CODE' in template
