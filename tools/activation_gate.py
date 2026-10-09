#!/usr/bin/env python3
"""
Unified Activation Gate — ONE receipt schema, ONE protected truth provider.

Unification (Naya 1, 2026-10-09): the activation lane had three checkers
drifting apart — PR #1979 `drink_first_gate.py` (v1 schema, six fail-open
defects), PR #1974 `activation_receipt_consistency.mjs` (v2 QA falsifier,
JS), and `tools/design_gate.py::check_activation` (structural layer,
delegates deep verification). This module is the single pre-delivery
enforcement point:

  ONE schema ........... naya.activation.receipt.v2 (v1 is retired)
  ONE truth provider ... resolve_truth(): the protected runner resolves
                         repository, current main SHA, and canonical source
                         fingerprints ITSELF from the runner context and the
                         live GitHub API. No caller flag may supply truth.
  ONE predicate ........ check(): pure function, no I/O, no network.

Retirement map:
  drink_first_gate.py (PR #1979, v1) ......... SUPERSEDED by this module
      (defects fixed: full-40-hex + exact main equality; trusted repo
       binding + wrong-repo replay; protected tip resolution; citation
       always required; closed-world source fingerprints; honest labels)
  activation_receipt_consistency.mjs (#1974) .. STAYS as Naya 3's V2 QA
      consistency falsifier lane (deconflicted: #1974 owns QA, this
      module owns pre-delivery enforcement). Same v2 schema, same
      marker format, same 4h TTL — one language, two seats.
  design_gate.py::check_activation ........... STAYS as the structural
      layer (marker presence/format/freshness/repo-digest). Deep truth
      verification belongs here.

ARCHITECTURAL LAW (non-negotiable): a builder cannot establish authenticity
by writing a plausible JSON file. Any input the builder supplies about the
truth being checked is untrusted by construction. In protected mode the only
trusted inputs are the runner context (GITHUB_REPOSITORY, GITHUB_TOKEN) and
the live GitHub API. A self-served truth (--mode local) can never produce a
PASS verdict — only an honestly labeled CANDIDATE-LOCAL-* verdict.

Acceptance table (every row must hold in real CI):
  authentic fresh receipt, exact repo, full current main SHA ... PASS
  fabricated / self-asserted receipt ...................... REJECT
  stale activation / changed commit (tip moved) ........... REJECT
  wrong repository identity .............................. REJECT
  missing / abbreviated / mismatched commit SHA .......... REJECT
  missing / tampered receipt ............................. REJECT
  unregistered source in `loaded` (closed-world) ......... REJECT
  alternate route bypassing the gate ..................... REJECT
      (self-minted truth yields CANDIDATE-LOCAL-*, never PASS;
       the delivery workflow gates shipment on a protected PASS)

Closed-world source rule: receipt.loaded must be an object whose keys are
EXACTLY the CANONICAL_SOURCES registry below, each a 40-hex blob SHA equal
to the blob's SHA in the live main tree. A new source is not a new key in a
receipt — it is a code change to CANONICAL_SOURCES plus its contract, or CI
fails.

Exit codes: 0 = PASS (protected) | 1 = REJECT | 2 = tool error
(including "cannot resolve trusted truth" — fail closed).
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

SCHEMA = "naya.activation.receipt.v2"
RECEIPT_TTL = timedelta(hours=4)
FUTURE_SKEW = timedelta(minutes=2)

SHA40_RE = re.compile(r"^[a-fA-F0-9]{40}$")
SHA64_RE = re.compile(r"^[a-fA-F0-9]{64}$")
RECEIPT_MARKER_RE = re.compile(
    r"<!--\s*NAYA-ACTIVATION-RECEIPT-SHA256:([a-fA-F0-9]{64})\s*-->")

# Closed-world registry of canonical activation sources.
# Logical name -> path in the repository at main. The protected runner binds
# each to its live blob SHA; the receipt must cite exactly these.
CANONICAL_SOURCES = {
    "design_contract": "BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md",
    "blocks_catalog": "BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json",
}

IDENTITY_FIELDS = ("session_id", "naya_identity", "human_authority",
                   "repository", "job", "proof_plan")

API_HOST = "https://api.github.com"


def _normalize_repo(name):
    if not isinstance(name, str):
        return ""
    return name.strip().lower().rstrip("/")


def check(receipt_bytes, deliverable_text, truth):
    """Pure predicate: (verdict, violations). No I/O, no network.

    receipt_bytes .... exact bytes of the receipt file (digest-bound)
    deliverable_text . text of the shipped artifact (must cite the receipt)
    truth ............ {"repository", "main_sha", "source_blobs", "now"}
    """
    violations = []

    if not isinstance(receipt_bytes, (bytes, bytearray)) or not receipt_bytes:
        return "REJECT", ["RECEIPT_MISSING_OR_EMPTY"]
    try:
        receipt = json.loads(receipt_bytes)
    except (ValueError, UnicodeDecodeError) as e:
        return "REJECT", ["RECEIPT_UNTAMPERED_UNREADABLE: %s" % e]
    if not isinstance(receipt, dict):
        return "REJECT", ["RECEIPT_NOT_AN_OBJECT"]

    # --- schema: one schema, v2 ---
    if receipt.get("schema") != SCHEMA:
        violations.append("WRONG_SCHEMA: expected %r" % SCHEMA)
    if receipt.get("status") != "ACTIVATED":
        violations.append("NOT_ACTIVATED: status is %r"
                          % (receipt.get("status"),))

    # --- identity ---
    for field in IDENTITY_FIELDS:
        if not receipt.get(field):
            violations.append("IDENTITY_INCOMPLETE: missing %s" % field)
    gates = receipt.get("gates")
    if not isinstance(gates, list) or not gates:
        violations.append("IDENTITY_INCOMPLETE: gates names no governing gates")

    # --- trusted repository binding (defect 2) ---
    want_repo = _normalize_repo((truth or {}).get("repository", ""))
    got_repo = _normalize_repo(receipt.get("repository", ""))
    if not want_repo:
        violations.append("TRUTH_UNTRUSTED: no trusted repository")
    elif got_repo != want_repo:
        violations.append("WRONG_REPOSITORY: receipt is for %r, gated repository is %r"
                          % (got_repo, want_repo))

    # --- full 40-hex SHA, exact equality vs independently resolved main (defect 1) ---
    main_sha = receipt.get("main_sha", "")
    live_sha = (truth or {}).get("main_sha", "")
    if not isinstance(main_sha, str) or not SHA40_RE.match(main_sha):
        violations.append("SHA_MALFORMED: main_sha is not a full 40-hex SHA")
    elif not isinstance(live_sha, str) or not SHA40_RE.match(live_sha):
        violations.append("TRUTH_UNTRUSTED: live main SHA unavailable")
    elif main_sha.lower() != live_sha.lower():
        violations.append("TIP_MOVED: receipt cites %s, live main is %s"
                          % (main_sha[:12], live_sha[:12]))

    # --- closed-world source fingerprints (defect 5) ---
    trusted_blobs = (truth or {}).get("source_blobs") or {}
    loaded = receipt.get("loaded")
    if not isinstance(loaded, dict):
        violations.append("SOURCES_UNVERIFIED: loaded must be an object of "
                          "canonical source fingerprints")
    else:
        want_keys = set(CANONICAL_SOURCES)
        got_keys = set(loaded)
        for extra in sorted(got_keys - want_keys):
            violations.append("SOURCE_NOT_REGISTERED: %r is not a canonical "
                              "activation source (closed-world)" % extra)
        for missing in sorted(want_keys - got_keys):
            violations.append("SOURCE_MISSING: no fingerprint for canonical "
                              "source %r" % missing)
        for name in sorted(want_keys & got_keys):
            claimed = loaded.get(name)
            trusted = trusted_blobs.get(name)
            if not isinstance(claimed, str) or not SHA40_RE.match(claimed):
                violations.append("SOURCE_FINGERPRINT_MALFORMED: %s" % name)
            elif not isinstance(trusted, str) or not SHA40_RE.match(trusted):
                violations.append("TRUTH_UNTRUSTED: no trusted fingerprint for %s"
                                  % name)
            elif claimed.lower() != trusted.lower():
                violations.append("SOURCE_FINGERPRINT_MISMATCH: %s" % name)

    # --- freshness (defect: 4h TTL, no future) ---
    now = (truth or {}).get("now")
    if not isinstance(now, datetime):
        violations.append("TRUTH_UNTRUSTED: no trusted clock")
    else:
        raw_ts = receipt.get("activated_at", "")
        try:
            activated = datetime.fromisoformat(
                str(raw_ts).strip().replace("Z", "+00:00"))
            if activated.tzinfo is None:
                activated = activated.replace(tzinfo=timezone.utc)
        except ValueError:
            activated = None
        if activated is None:
            violations.append("TIMESTAMP_INVALID: activated_at unparseable")
        elif activated > now + FUTURE_SKEW:
            violations.append("FUTURE_ACTIVATION: activated_at is in the future")
        elif now - activated > RECEIPT_TTL:
            violations.append("ACTIVATION_EXPIRED: older than %s" % RECEIPT_TTL)

    # --- citation: always required, digest-bound to exact receipt bytes (defect 4) ---
    digest = hashlib.sha256(bytes(receipt_bytes)).hexdigest()
    if not isinstance(deliverable_text, str):
        violations.append("CITATION_MISSING: no deliverable text to check")
    else:
        m = RECEIPT_MARKER_RE.search(deliverable_text)
        if not m:
            violations.append(
                "CITATION_MISSING: deliverable carries no "
                "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> --> marker")
        elif m.group(1).lower() != digest:
            violations.append(
                "CITATION_DIGEST_MISMATCH: marker does not match sha256 of "
                "the exact receipt bytes (stale or forged citation)")

    if violations:
        return "REJECT", violations
    return "PASS", []


def _api(method, path, token, body=None):
    req = urllib.request.Request(
        API_HOST + path, data=json.dumps(body).encode() if body else None,
        method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError("GitHub API %s %s -> HTTP %s: %s"
                           % (method, path, e.code, e.read().decode()[:300]))


def resolve_truth():
    """Protected truth provider. Resolves repository identity, current main
    SHA, and canonical source blob SHAs ITSELF. Raises on any failure —
    the gate fails closed when trust cannot be established.

    Trusted inputs ONLY: GITHUB_REPOSITORY + GITHUB_TOKEN from the runner
    context, and the live GitHub API. There is deliberately no flag, env
    var, or file that lets the caller supply truth.
    """
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not repo or "/" not in repo:
        raise RuntimeError("cannot establish trusted repository identity "
                           "(GITHUB_REPOSITORY missing) — refusing")
    if not token:
        raise RuntimeError("cannot reach live state without GITHUB_TOKEN — refusing")

    ref = _api("GET", "/repos/%s/git/ref/heads/main" % repo, token)
    main_sha = ((ref.get("object") or {}).get("sha")) or ""
    if not SHA40_RE.match(main_sha):
        raise RuntimeError("live main SHA unresolvable — refusing")

    tree = _api("GET", "/repos/%s/git/trees/%s?recursive=1" % (repo, main_sha),
                token)
    blobs = {}
    by_path = {t.get("path"): t for t in tree.get("tree", [])
               if t.get("type") == "blob"}
    for name, path in CANONICAL_SOURCES.items():
        entry = by_path.get(path)
        sha = (entry or {}).get("sha", "")
        if not SHA40_RE.match(sha):
            raise RuntimeError(
                "canonical source %r not found in live main tree — "
                "trust cannot be established, refusing" % path)
        blobs[name] = sha

    return {"repository": repo, "main_sha": main_sha,
            "source_blobs": blobs, "now": datetime.now(timezone.utc)}


def load_local_truth(path):
    """Local rehearsal truth. The verdict is ALWAYS labeled CANDIDATE-LOCAL —
    a self-served truth can never produce PASS (architectural law)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    now = datetime.now(timezone.utc)
    raw_now = data.get("now")
    if raw_now:
        try:
            now = datetime.fromisoformat(str(raw_now).replace("Z", "+00:00"))
        except ValueError:
            pass
    return {"repository": data.get("repository", ""),
            "main_sha": data.get("main_sha", ""),
            "source_blobs": data.get("source_blobs", {}),
            "now": now}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Unified Activation Gate: fail closed on unactivated or "
                    "counterfeit activation.")
    ap.add_argument("--receipt", required=True, help="activation receipt JSON path")
    ap.add_argument("--deliverable", required=True,
                    help="shipped artifact path (must cite the receipt)")
    ap.add_argument("--mode", choices=("protected", "local"),
                    default="protected",
                    help="protected: resolve truth from the runner (default). "
                         "local: rehearsal only, verdict labeled CANDIDATE-LOCAL.")
    ap.add_argument("--truth", default=None,
                    help="local-mode truth JSON (ignored in protected mode)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        with open(args.receipt, "rb") as f:
            receipt_bytes = f.read()
    except OSError as e:
        return _emit("TOOL-ERROR", [str(e)], args, 2, local=False)
    try:
        with open(args.deliverable, encoding="utf-8") as f:
            deliverable_text = f.read()
    except OSError as e:
        return _emit("TOOL-ERROR", [str(e)], args, 2, local=False)

    local = args.mode == "local"
    try:
        if local:
            if not args.truth:
                return _emit("TOOL-ERROR", ["local mode requires --truth"],
                             args, 2, local=True)
            truth = load_local_truth(args.truth)
        else:
            truth = resolve_truth()
    except RuntimeError as e:
        return _emit("TOOL-ERROR", [str(e)], args, 2, local=local)

    verdict, violations = check(receipt_bytes, deliverable_text, truth)
    if local:
        verdict = "CANDIDATE-LOCAL-" + verdict  # never PASS (defect 6)
        code = 0 if verdict.endswith("PASS") else 1
    else:
        code = 0 if verdict == "PASS" else 1
    return _emit(verdict, violations, args, code, local=local)


def _emit(verdict, violations, args, code, local):
    if args.json:
        print(json.dumps({"verdict": verdict, "violations": violations,
                          "mode": "local" if local else "protected"}))
    else:
        print("%s: %s" % (verdict,
                          "; ".join(violations) if violations else "ok"))
    return code


if __name__ == "__main__":
    sys.exit(main())
