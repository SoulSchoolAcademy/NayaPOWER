"""Regression: V2.1 executable integrity must be checkout-line-ending stable.

A Windows/core.autocrlf checkout may materialize the ratified LF blob as CRLF.
The runtime must verify the same canonical git-blob content that the ratified
pin names; line-ending conversion alone must not look like tampering.
"""

from naya_kernel.node_base import _git_blob_sha


def test_git_blob_sha_is_crlf_stable():
    lf = b"alpha\nbeta\ngamma\n"
    crlf = lf.replace(b"\n", b"\r\n")
    assert _git_blob_sha(lf) == _git_blob_sha(crlf)


def test_git_blob_sha_still_detects_semantic_change():
    original = b"alpha\nbeta\ngamma\n"
    changed = b"alpha\nbeta\nGAMMA\n"
    assert _git_blob_sha(original) != _git_blob_sha(changed)
