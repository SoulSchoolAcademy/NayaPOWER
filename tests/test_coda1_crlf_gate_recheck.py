"""Coda 1 independent recheck at 71077670: CRLF normalization must not mask tampering.

Re-arms the CRLF finding that motivated node_base._git_blob_sha, and asserts the
normalize-on-read repair fails closed on any real content change.
"""
from naya_kernel.node_base import _git_blob_sha, v21_executable_status, \
    CALCULUS_V21_EXECUTABLE_HASH as PIN

LF = b"line one\nline two\n"
CRLF = b"line one\r\nline two\r\n"


def test_crlf_normalizes_to_lf():
    assert _git_blob_sha(CRLF) == _git_blob_sha(LF)


def test_real_content_change_still_detected_in_lf():
    assert _git_blob_sha(b"line one\nline TWO\n") != _git_blob_sha(LF)


def test_real_content_change_still_detected_in_crlf():
    assert _git_blob_sha(b"line one\r\nline TWO\r\n") != _git_blob_sha(CRLF)


def test_lone_cr_is_not_normalized():
    """Only CRLF is representation; a lone CR is a byte change."""
    assert _git_blob_sha(b"line one\rline two\n") != _git_blob_sha(LF)


def test_ratified_executable_matches_pin_on_this_checkout():
    st = v21_executable_status()
    assert st["match"] is True, st
    assert st["actual_blob_sha"] == PIN


def test_pinned_sha():
    assert PIN
