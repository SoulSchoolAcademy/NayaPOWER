#!/usr/bin/env python3
"""
Activation Pre-Gate for the Naya Design Compliance Checker
============================================================
Gap-2 integration: the compliance checker must REFUSE to score a deliverable
when the builder cannot prove valid, current activation.

This is a Python port of Naya 3's activation receipt consistency falsifier
(PR #1974, tools/qa/activation_receipt_consistency.mjs). The logic is
faithful; the language is Python so the checker has zero new dependencies.

The law: ACTIVATION FIRST. No valid receipt = no score. Not a low score —
a refusal. The gate does not open without it.

Critical anti-forgery property (from Naya 3):
    The caller MUST independently fetch the GitHub state. Accepting
    builder-supplied "trusted" state is UNSAFE.

Violation codes (matching the .mjs source):
    RECEIPT_MISSING, TRUSTED_STATE_MISSING, WRONG_SCHEMA_OR_STATE,
    IDENTITY_INCOMPLETE, JOB_GATES_PROOF_MISSING, MAIN_STALE_OR_MISMATCH,
    DOC_MISMATCH_DESIGN_BLOB, DOC_MISMATCH_BLOCKS_BLOB,
    CONTEXT_MISMATCH_GOALS_DIGEST, CONTEXT_MISMATCH_FEED_DIGEST,
    TIMESTAMP_INVALID, FUTURE_ACTIVATION, ACTIVATION_EXPIRED,
    RECEIPT_DIGEST_UNTRUSTED_OR_MISSING, DELIVERABLE_RECEIPT_CITATION_MISSING,
    REPOSITORY_MISMATCH, TRUSTED_STATE_UNREACHABLE
"""

import hashlib
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

REPO = "SoulSchoolAcademy/NayaPOWER"
API_BASE = "https://api.github.com/repos/" + REPO
ACTIVATION_TTL_SECONDS = 4 * 60 * 60  # 4 hours, per Naya 3
FUTURE_SKEW_SECONDS = 120  # 2 minutes clock skew tolerance

SHA40_RE = re.compile(r"^[a-f0-9]{40}$", re.IGNORECASE)
SHA64_RE = re.compile(r"^[a-f0-9]{64}$", re.IGNORECASE)

# Canonical paths whose blob SHAs form the trusted "loaded" state
DESIGN_CATALOG_PATH = "BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json"
BLOCKS_INDEX_PATH = "BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json"


class ActivationRefused(Exception):
    """Raised when the pre-gate refuses to score. Carries violations."""
    def __init__(self, violations):
        self.violations = violations
        super().__init__(
            "ACTIVATION REFUSED: " + ", ".join(violations)
        )


def _api_get(path):
    """GET a GitHub API path. Returns parsed JSON. Raises on failure."""
    req = urllib.request.Request(
        API_BASE + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "naya-activation-pregate/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        raise ActivationRefused(["TRUSTED_STATE_UNREACHABLE"])


def fetch_trusted_state():
    """
    Independently fetch the trusted activation state from live GitHub.
    This is the state the receipt is checked AGAINST — never taken from
    the builder.
    """
    # 1. Live main tip SHA
    ref = _api_get("/git/refs/heads/main")
    main_sha = ref["object"]["sha"]

    # 2. Blob SHAs of the canonical design intelligence files at main
    design_info = _api_get(f"/contents/{DESIGN_CATALOG_PATH}?ref=main")
    blocks_info = _api_get(f"/contents/{BLOCKS_INDEX_PATH}?ref=main")

    # 3. Context digests: current team feed (latest #1354 comments) and
    #    current build-list goals state. These prove "current" loading.
    comments = _api_get("/issues/1354/comments?per_page=100")
    # Use the newest 20 comment ids+timestamps as the feed fingerprint
    feed_fp = json.dumps(
        [{"id": c["id"], "updated": c["updated_at"]} for c in comments[-20:]],
        sort_keys=True,
    )
    feed_digest = hashlib.sha256(feed_fp.encode()).hexdigest()

    # Goals digest: SHA256 of the open-issue count + newest issue/PR numbers
    # (observable, current, builder-independent)
    issues = _api_get("/issues?state=open&per_page=5&sort=created&direction=desc")
    pulls = _api_get("/pulls?state=open&per_page=5&sort=created&direction=desc")
    goals_fp = json.dumps(
        {
            "newest_issues": [i["number"] for i in issues],
            "newest_pulls": [p["number"] for p in pulls],
        },
        sort_keys=True,
    )
    goals_digest = hashlib.sha256(goals_fp.encode()).hexdigest()

    return {
        "main_sha": main_sha,
        "design_blob": design_info["sha"],
        "blocks_blob": blocks_info["sha"],
        "goals_digest": goals_digest,
        "feed_digest": feed_digest,
    }


def check_activation_receipt(receipt, trusted, work_product_html, now_iso=None):
    """
    Verify an activation receipt against independently-fetched trusted state.

    Args:
        receipt: dict parsed from the builder's receipt JSON file.
        trusted: dict from fetch_trusted_state() — NEVER builder-supplied.
        work_product_html: the deliverable HTML string (checked for citation).
        now_iso: ISO timestamp for "now" (defaults to current UTC).

    Returns:
        (ok: bool, violations: list[str], receipt_sha256: str|None)

    Raises:
        ActivationRefused if violations are found.
    """
    violations = []

    def sha40(v):
        return isinstance(v, str) and bool(SHA40_RE.match(v))

    def sha64(v):
        return isinstance(v, str) and bool(SHA64_RE.match(v))

    # --- Existence ---
    if not receipt or not isinstance(receipt, dict):
        violations.append("RECEIPT_MISSING")
        raise ActivationRefused(violations)
    if not trusted or not isinstance(trusted, dict):
        violations.append("TRUSTED_STATE_MISSING")
        raise ActivationRefused(violations)

    # --- Schema and state ---
    if receipt.get("schema") != "naya.activation.receipt.v2" \
            or receipt.get("status") != "ACTIVATED":
        violations.append("WRONG_SCHEMA_OR_STATE")

    # --- Identity ---
    for field in ("session_id", "naya_identity", "human_authority", "repository"):
        if not receipt.get(field):
            violations.append("IDENTITY_INCOMPLETE")
            break

    # --- Repository binding ---
    repo = receipt.get("repository", "")
    if repo and repo != REPO and repo != f"https://github.com/{REPO}":
        violations.append("REPOSITORY_MISMATCH")

    # --- Job, gates, proof plan ---
    if (not receipt.get("job")
            or not isinstance(receipt.get("gates"), list)
            or not receipt.get("gates")
            or not receipt.get("proof_plan")):
        violations.append("JOB_GATES_PROOF_MISSING")

    # --- Main SHA freshness ---
    if (not sha40(receipt.get("main_sha"))
            or not sha40(trusted.get("main_sha"))
            or receipt.get("main_sha") != trusted.get("main_sha")):
        violations.append("MAIN_STALE_OR_MISMATCH")

    # --- Loaded document digests ---
    loaded = receipt.get("loaded") or {}
    for key, vcode in (("design_blob", "DOC_MISMATCH_DESIGN_BLOB"),
                       ("blocks_blob", "DOC_MISMATCH_BLOCKS_BLOB")):
        if (not sha40(loaded.get(key))
                or not sha40(trusted.get(key))
                or loaded.get(key) != trusted.get(key)):
            violations.append(vcode)
    for key, vcode in (("goals_digest", "CONTEXT_MISMATCH_GOALS_DIGEST"),
                       ("feed_digest", "CONTEXT_MISMATCH_FEED_DIGEST")):
        if (not sha64(loaded.get(key))
                or not sha64(trusted.get(key))
                or loaded.get(key) != trusted.get(key)):
            violations.append(vcode)

    # --- Timestamp: valid, not future, not expired ---
    now_iso = now_iso or datetime.now(timezone.utc).isoformat()
    try:
        now = datetime.fromisoformat(now_iso.replace("Z", "+00:00")).timestamp()
        activated = datetime.fromisoformat(
            receipt.get("activated_at", "").replace("Z", "+00:00")
        ).timestamp()
    except (ValueError, TypeError, AttributeError):
        now, activated = None, None
    if now is None or activated is None:
        violations.append("TIMESTAMP_INVALID")
    elif activated > now + FUTURE_SKEW_SECONDS:
        violations.append("FUTURE_ACTIVATION")
    elif now - activated > ACTIVATION_TTL_SECONDS:
        violations.append("ACTIVATION_EXPIRED")

    # --- Receipt digest: computed from exact bytes, must be cited ---
    receipt_sha256 = None
    try:
        receipt_bytes = json.dumps(receipt, sort_keys=True).encode()
        receipt_sha256 = hashlib.sha256(receipt_bytes).hexdigest()
    except (TypeError, ValueError):
        pass
    if not receipt_sha256:
        violations.append("RECEIPT_DIGEST_UNTRUSTED_OR_MISSING")
    elif (not isinstance(work_product_html, str)
          or f"NAYA-ACTIVATION-RECEIPT-SHA256:{receipt_sha256}"
          not in work_product_html):
        violations.append("DELIVERABLE_RECEIPT_CITATION_MISSING")

    if violations:
        raise ActivationRefused(violations)
    return True, [], receipt_sha256


def gate_or_refuse(receipt_path, work_product_html):
    """
    Run the full pre-gate: load receipt, fetch trusted state, verify.
    Returns the receipt_sha256 on success. Raises ActivationRefused otherwise.
    """
    try:
        with open(receipt_path, encoding="utf-8") as f:
            receipt = json.load(f)
    except (OSError, json.JSONDecodeError):
        raise ActivationRefused(["RECEIPT_MISSING"])
    trusted = fetch_trusted_state()
    ok, _, digest = check_activation_receipt(receipt, trusted, work_product_html)
    return digest
