"""Shared 403 classifier for every fail-closed gate.

WHY THIS EXISTS (gr-w257-eta-gate403-class)
-------------------------------------------
GitHub answers HTTP 403 for two unrelated reasons:

  quota      -- rate/quota limit exceeded (transient). The run's token is
               spent, not broken. A retry after backoff can succeed, so a
               quota 403 must NEVER fail the PR: the gate reports
               INCONCLUSIVE/RETRY instead of FAIL.
  permission -- "Resource not accessible ..." (final). Retries cannot help;
               fail closed, fail fast.
  unknown    -- anything else. Fail closed, exactly as before.

Before this module, fail-closed gates read only the status code:
ci_claim_evidence_gate.py raised GATE_BLIND on ANY API error and
activation_gate.py raised RuntimeError -- so a quota 403 under merge-burst
pressure produced a red gate that cost a full diagnosis (the #2635 class).
The response BODY carries the distinction; every gate that judges a 403
must read it. Precedent: check_merge_consensus.py::_classify_http_error
already classified this way for its own retry loop; this module is the one
shared mechanism, so the fix is a decision, not a bandage.

CONTRACT
--------
classify_403_body(body) -> "quota" | "permission" | "unknown".
Pure function; never raises. Bodies it cannot read classify "unknown" --
a gate that cannot see WHY it was refused stays fail-closed.

QuotaExhausted is raised when an API call 403s on quota. It subclasses
RuntimeError so call sites that catch RuntimeError broadly stay fail-closed
at sites not yet wired for INCONCLUSIVE. Wired sites catch QuotaExhausted
FIRST and report INCONCLUSIVE/RETRY, carrying the server's message and its
Retry-After (seconds) when the server sent one.
"""

from __future__ import annotations

import json
import urllib.error

# Substrings of GitHub's 403 message bodies (lowercased before matching).
# Quota bodies look like: "API rate limit exceeded for user ID ...",
# "You have exceeded a secondary rate limit ...",
# "API rate limit exceeded for installation ID ...".
_QUOTA_SIGNALS = ("rate limit",)

# Permission bodies look like: "Resource not accessible by personal access
# token.", "Resource not accessible by integration.",
# "Must have admin rights to Repository."
_PERMISSION_SIGNALS = ("resource not accessible", "must have admin")


def classify_403_body(body) -> str:
    """Classify a 403 response body: "quota" | "permission" | "unknown".

    Accepts bytes, bytearray, or str (anything else -> "unknown").
    Never raises.
    """
    try:
        if isinstance(body, (bytes, bytearray)):
            text = bytes(body).decode("utf-8", "replace")
        else:
            text = str(body or "")
    except Exception:  # noqa: BLE001 -- hostile input still classifies
        return "unknown"
    low = text.lower()
    # Quota first: a spent token must never be mislabeled a permission fault.
    if any(s in low for s in _QUOTA_SIGNALS) or ("quota" in low and "exceed" in low):
        return "quota"
    if any(s in low for s in _PERMISSION_SIGNALS):
        return "permission"
    return "unknown"


def read_error_body(exc: urllib.error.HTTPError) -> bytes:
    """Read an HTTPError's response body. Never raises; b"" when unreadable."""
    try:
        return exc.read() or b""
    except Exception:  # noqa: BLE001 -- an unreadable body is "unknown"
        return b""


def error_message(body: bytes) -> str:
    """GitHub's JSON "message" from a response body, else the raw text head."""
    try:
        text = body.decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return ""
    try:
        msg = json.loads(text).get("message", "")
        if msg:
            return str(msg)
    except Exception:  # noqa: BLE001 -- not JSON; fall through to raw text
        pass
    return text[:200]


def retry_after_seconds(exc: urllib.error.HTTPError):
    """The server's Retry-After header in seconds, or None. Never raises."""
    try:
        headers = exc.headers
        ra = headers.get("Retry-After") if headers else None
        return int(ra) if ra else None
    except (TypeError, ValueError):
        return None


class QuotaExhausted(RuntimeError):
    """A GitHub API call 403'd on quota, not permission.

    The gate must NOT report FAIL. Report INCONCLUSIVE/RETRY: the gate
    could not judge, and a retry after backoff may succeed.
    Carries retry_after (seconds) when the server sent a Retry-After header.
    """

    def __init__(self, message: str = "", retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after

    @classmethod
    def for_http_error(cls, context: str, exc: urllib.error.HTTPError, body: bytes = None):
        """Build from a 403 HTTPError. Pass the already-read body to avoid
        a second read of a consumed stream. Never raises."""
        if body is None:
            body = read_error_body(exc)
        msg = error_message(body) or "quota 403"
        ra = retry_after_seconds(exc)
        detail = "%s: %s" % (context, msg)
        if ra is not None:
            detail += " (server asked Retry-After: %ds)" % ra
        return cls(detail, retry_after=ra)
