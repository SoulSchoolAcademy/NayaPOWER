"""
read_receipt_issuance.py — Machine law: run-attested issuance for read receipts.

The unkeyed SHA-256 in read_receipt.py proves INTEGRITY (the receipt was not
tampered with after minting). It does NOT prove ISSUANCE (who minted it) —
anyone can recompute the hash. This module closes that gap.

A read receipt is AUTHENTIC iff the trusted mint workflow
(.github/workflows/read-receipt-mint.yml) minted THESE EXACT BYTES: the
attested run must exist in the gated repository, have run the base mint
workflow to success via workflow_dispatch, and its artifact's receipt.json
must be byte-identical to the presented receipt. A fully self-minted receipt
with correct answers and a valid hash FAILS here — correct answers were never
the authenticity root; the runner's attested issuance is.

HONEST CAVEAT (documented, not hidden): run-attestation proves "the trusted
runner ran and graded THESE answers", not "which agent it ran for". The
agent_id in the receipt is caller-supplied. This narrows the identity gap
(the old receipt proved nothing about issuance at all) but does not fully
close it.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import urllib.request
import zipfile


MINT_WORKFLOW_PATH = ".github/workflows/read-receipt-mint.yml"
MINT_ARTIFACT_PREFIX = "read-receipt-"
SCHEMA = "naya/read-receipt-attested-v1"


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _api(method: str, path: str, token: str, body=None):
    """Minimal GitHub API client (same shape as tools/activation_gate.py)."""
    url = "https://api.github.com" + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError("GitHub API %s %s -> %s" % (method, path, e.code))
    except urllib.error.URLError as e:
        raise RuntimeError("GitHub API unreachable: %s" % e)


class _Redirected(Exception):
    def __init__(self, location):
        super().__init__("redirect")
        self.location = location


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise _Redirected(newurl)


def _download_bytes(url: str, token: str) -> bytes:
    """Two-hop download: the API 302-redirects to a pre-signed blob URL that
    rejects the API bearer — take the Location and fetch it WITHOUT auth."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        opener.open(req, timeout=30)
    except _Redirected as r:
        loc = r.location
    else:
        raise RuntimeError("artifact download did not redirect — refusing")
    req2 = urllib.request.Request(loc)
    with urllib.request.urlopen(req2, timeout=60) as resp:
        return resp.read()


def verify_issuance(envelope: dict, envelope_bytes: bytes, token: str,
                    repo: str) -> list:
    """Verify a read-receipt envelope was minted by the trusted runner.

    Returns a list of violations (empty = issuance genuine).
    """
    if not isinstance(envelope, dict):
        return ["ISSUANCE_MALFORMED: envelope is not an object"]
    if envelope.get("schema") != SCHEMA:
        return ["ISSUANCE_WRONG_SCHEMA: expected %r, got %r"
                % (SCHEMA, envelope.get("schema"))]
    receipt = envelope.get("receipt")
    if not isinstance(receipt, dict):
        return ["ISSUANCE_NO_RECEIPT: envelope carries no receipt object"]
    if not receipt.get("passed"):
        return ["ISSUANCE_NOT_PASSED: receipt did not pass grading"]
    att = envelope.get("attestation")
    if not isinstance(att, dict):
        return ["ISSUANCE_UNATTESTED: receipt carries no trusted-issuance "
                "attestation — a self-minted receipt, however plausible, "
                "cannot pass the boot boundary"]
    run_id = att.get("run_id")
    if not run_id:
        return ["ISSUANCE_UNATTESTED: attestation names no run"]
    if not repo:
        return ["TRUTH_UNTRUSTED: no trusted repository for issuance check"]
    if not token:
        return ["ISSUANCE_UNVERIFIABLE: no token to verify the attested run"]

    try:
        run = _api("GET", "/repos/%s/actions/runs/%s" % (repo, run_id), token)
    except RuntimeError as e:
        return ["ISSUANCE_UNVERIFIABLE: attested run %s unreachable (%s)"
                % (run_id, e)]
    if run.get("event") != "workflow_dispatch":
        return ["ISSUANCE_WRONG_EVENT: attested run %s event is %r, not "
                "workflow_dispatch" % (run_id, run.get("event"))]
    if run.get("path") != MINT_WORKFLOW_PATH:
        return ["ISSUANCE_WRONG_WORKFLOW: attested run %s ran %r, not the "
                "trusted mint workflow" % (run_id, run.get("path"))]
    if run.get("conclusion") != "success":
        return ["ISSUANCE_RUN_NOT_SUCCESS: attested run %s concluded %r"
                % (run_id, run.get("conclusion"))]
    head_repo = ((run.get("head_repository") or {}).get("full_name")) or ""
    if head_repo != repo:
        return ["ISSUANCE_FOREIGN_RUN: attested run %s belongs to %r, not "
                "the gated repository" % (run_id, head_repo)]

    try:
        arts = _api("GET", "/repos/%s/actions/runs/%s/artifacts" % (repo, run_id),
                    token)
    except RuntimeError as e:
        return ["ISSUANCE_UNVERIFIABLE: attested run artifacts unreachable (%s)"
                % e]
    want_digest = _sha256_hex(envelope_bytes)
    saw_receipt_artifact = False
    for a in arts.get("artifacts", []) or []:
        if not str(a.get("name", "")).startswith(MINT_ARTIFACT_PREFIX):
            continue
        saw_receipt_artifact = True
        try:
            blob = _download_bytes(a.get("archive_download_url", ""), token)
        except RuntimeError as e:
            return ["ISSUANCE_UNVERIFIABLE: artifact download failed (%s)" % e]
        try:
            z = zipfile.ZipFile(io.BytesIO(blob))
            names = [n for n in z.namelist()
                     if os.path.basename(n) == "receipt.json"]
            if not names:
                continue
            if _sha256_hex(z.read(names[0])) == want_digest:
                return []
        except zipfile.BadZipFile:
            continue
    if not saw_receipt_artifact:
        return ["ISSUANCE_ARTIFACT_MISSING: attested run %s carries no "
                "read-receipt artifact" % run_id]
    return ["ISSUANCE_BYTES_MISMATCH: the presented receipt bytes are not "
            "byte-identical to the attested run's minted receipt — forged "
            "or tampered issuance"]


def envelope_from_receipt(receipt_dict: dict, attestation: dict) -> tuple:
    """Build the canonical attested envelope bytes for a minted receipt.

    Used by the mint script path and by tests constructing fixtures.
    Returns (envelope_dict, envelope_bytes).
    """
    envelope = {
        "schema": SCHEMA,
        "receipt": receipt_dict,
        "attestation": attestation,
    }
    return envelope, json.dumps(envelope, sort_keys=True).encode()
