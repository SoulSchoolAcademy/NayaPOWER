#!/usr/bin/env python3
"""
Unified Activation Gate — ONE receipt schema, ONE protected truth provider.

Unification (Naya 1, 2026-10-09): the activation lane had three checkers
drifting apart — PR #1979 `drink_first_gate.py` (v1 schema, six fail-open
defects), PR #1974 `activation_receipt_consistency.mjs` (v2 QA falsifier,
JS), and `tools/design_gate.py::check_activation` (structural layer).
This module is the single pre-delivery enforcement point:

  ONE schema ........... naya.activation.receipt.v2 (v1 is retired)
  ONE truth provider ... resolve_truth(): the protected runner resolves
                         repository, current main SHA, and canonical source
                         fingerprints ITSELF from the runner context and the
                         live GitHub API. No caller flag may supply truth.
  ONE predicate ........ check(): pure function, no I/O, no network.

ROUND-2 HARDENING (independent attack, 2026-10-09 — four bypasses closed):
  1. THE GATE GUARDED NOTHING. The CI workflow trigger was avoidable by
     path and no required status check existed. The workflow now triggers
     on EVERY pull_request_target to main (no paths filter) and every push
     to main. The required status check is documented as the authority
     step needing Shawn's word — until it is set, the gate says so.
  2. PR-EDITABLE TRUST ROOT. resolve_truth() read GITHUB_REPOSITORY from a
     plain env var and the workflow executed the PR's own gate code — the
     builder graded their own exam. Now: the repository identity is read
     from the runner-written event payload (GITHUB_EVENT_PATH) and
     cross-checked against the env; ANY disagreement refuses. The CI
     workflow runs on pull_request_target (workflow + gate code pinned to
     the BASE ref; the PR's code is checked out separately and only ever
     READ as text, never executed).
  3. UNDOCUMENTED COMPONENTS PASSED SILENTLY. The gate now
     delegates-and-verifies: in protected mode it runs the design gate
     (tools/design_gate.py) resolved from the PROTECTED base ref against
     the deliverable and folds its verdict in. If the design gate is
     absent from the base ref, the verdict is BLOCKED-DESIGN-GATE-ABSENT
     — never a silent PASS. No pass-through, ever.
  4. RECEIPT TRANSPLANT. A receipt for one job could ship another
     deliverable. The receipt is now bound to the deliverable:
     deliverable_sha256 (sha256 of the canonical deliverable bytes, marker
     stripped) is REQUIRED for PASS, and when the runner supplies the
     delivery job context, receipt.job must match it exactly.

ARCHITECTURAL LAW (non-negotiable): a builder cannot establish authenticity
by writing a plausible JSON file. Any input the builder supplies about the
truth being checked is untrusted by construction. In protected mode the only
trusted inputs are the runner context (event payload + GITHUB_TOKEN) and the
live GitHub API. A self-served truth (--mode local) can never produce a
PASS verdict — only honestly labeled CANDIDATE-LOCAL-* verdicts.

Verdicts: PASS | REJECT | BLOCKED-DESIGN-GATE-ABSENT | TOOL-ERROR.
Local-mode verdicts never contain the substring "PASS".
Exit codes: 0 = PASS and ONLY PASS | 1 = any non-PASS verdict | 2 = tool error.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
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


def canonical_deliverable_bytes(deliverable_text):
    """Bytes the receipt's deliverable_sha256 binds to: the deliverable with
    the receipt marker stripped (the marker cites the receipt, so it cannot
    be part of what the receipt binds — otherwise minting is circular)."""
    if not isinstance(deliverable_text, str):
        return None
    return RECEIPT_MARKER_RE.sub("", deliverable_text).encode("utf-8")


def check(receipt_bytes, deliverable_text, truth, delivery=None):
    """Pure predicate: (verdict, violations). No I/O, no network.

    receipt_bytes .... exact bytes of the receipt file (digest-bound)
    deliverable_text . text of the shipped artifact (must cite the receipt)
    truth ............ {"repository", "main_sha", "source_blobs", "now"}
    delivery ......... None, or {"job": str, "deliverable_sha256": str}
                       supplied by the PROTECTED runner (never the builder).
                       Binds the receipt to THIS deliverable: a receipt
                       minted for another job/deliverable cannot PASS here.
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

    # --- trusted repository binding ---
    want_repo = _normalize_repo((truth or {}).get("repository", ""))
    got_repo = _normalize_repo(receipt.get("repository", ""))
    if not want_repo:
        violations.append("TRUTH_UNTRUSTED: no trusted repository")
    elif got_repo != want_repo:
        violations.append("WRONG_REPOSITORY: receipt is for %r, gated repository is %r"
                          % (got_repo, want_repo))

    # --- full 40-hex SHA, exact equality vs independently resolved main ---
    main_sha = receipt.get("main_sha", "")
    live_sha = (truth or {}).get("main_sha", "")
    if not isinstance(main_sha, str) or not SHA40_RE.match(main_sha):
        violations.append("SHA_MALFORMED: main_sha is not a full 40-hex SHA")
    elif not isinstance(live_sha, str) or not SHA40_RE.match(live_sha):
        violations.append("TRUTH_UNTRUSTED: live main SHA unavailable")
    elif main_sha.lower() != live_sha.lower():
        violations.append("TIP_MOVED: receipt cites %s, live main is %s"
                          % (main_sha[:12], live_sha[:12]))

    # --- closed-world source fingerprints ---
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

    # --- freshness: 4h TTL, no future ---
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

    # --- citation: always required, digest-bound to exact receipt bytes ---
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

    # --- deliverable binding (round-2, hole 4: receipt transplant) ---
    bound = receipt.get("deliverable_sha256", "")
    if not isinstance(bound, str) or not SHA64_RE.match(bound):
        violations.append(
            "RECEIPT_UNBOUND: receipt carries no deliverable_sha256 binding — "
            "an unbound receipt could be transplanted onto another deliverable")
    else:
        canon = canonical_deliverable_bytes(deliverable_text)
        if canon is None:
            violations.append("CITATION_MISSING: no deliverable text to bind")
        elif hashlib.sha256(canon).hexdigest() != bound.lower():
            violations.append(
                "DELIVERABLE_DIGEST_MISMATCH: this receipt was minted for a "
                "different deliverable (transplant rejected)")

    # --- job binding (when the protected runner supplies delivery context) ---
    if delivery is not None:
        want_job = delivery.get("job")
        if isinstance(want_job, str) and want_job:
            if receipt.get("job") != want_job:
                violations.append(
                    "RECEIPT_JOB_MISMATCH: receipt job %r != delivery job %r"
                    % (receipt.get("job"), want_job))

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


def _repo_from_event_payload():
    """Repository identity from the runner-written event payload.

    GITHUB_EVENT_PATH is written by the GitHub runner before any workflow
    step executes. Under pull_request_target the workflow definition comes
    from the BASE ref, so a PR cannot forge this file. Returns "" when the
    payload is unavailable (local rehearsal)."""
    path = os.environ.get("GITHUB_EVENT_PATH", "").strip()
    if not path or not os.path.isfile(path):
        return ""
    try:
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
        repo = ((payload.get("repository") or {}).get("full_name")) or ""
        return repo.strip()
    except (ValueError, OSError, AttributeError):
        return ""


def resolve_truth():
    """Protected truth provider. Resolves repository identity, current main
    SHA, and canonical source blob SHAs ITSELF. Raises on any failure —
    the gate fails closed when trust cannot be established.

    Trust root (round-2, hole 2): the repository identity comes from the
    RUNNER-WRITTEN EVENT PAYLOAD, cross-checked against GITHUB_REPOSITORY.
    A step-level `env: GITHUB_REPOSITORY: evil/x` override — or any other
    caller-supplied identity — is REFUSED. There is deliberately no flag,
    env var, or file that lets the caller supply truth.
    """
    payload_repo = _repo_from_event_payload()
    env_repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if not payload_repo:
        # No runner-written event payload: there is no trusted identity
        # source at all. GITHUB_REPOSITORY alone is builder-suppliable and
        # therefore untrusted by construction. Fail closed; --mode local
        # exists for rehearsal.
        raise RuntimeError(
            "no runner event payload (GITHUB_EVENT_PATH) — protected mode "
            "requires the CI runner context; refusing")
    if env_repo and _normalize_repo(payload_repo) != _normalize_repo(env_repo):
        raise RuntimeError(
            "repository identity conflict: event payload says %r but "
            "environment says %r — refusing (possible trust-root override)"
            % (payload_repo, env_repo))
    repo = payload_repo
    token = os.environ.get("GITHUB_TOKEN", "").strip()
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


def run_design_gate(deliverable_path, design_gate_path, manifest_path):
    """Delegate-and-verify (round-2, hole 3): run the design gate resolved
    from the PROTECTED base ref against the deliverable. Returns a list of
    violation strings (empty = the design gate passed).

    The design gate enforces the structural closed-world rule the unified
    gate cannot see: no freestyle components, every Naya-prefixed class in
    the manifest, black root, dark scheme, self-contained, mobile viewport.
    """
    if not design_gate_path or not os.path.isfile(design_gate_path):
        return ["DESIGN_GATE_ABSENT"]
    if not manifest_path or not os.path.isfile(manifest_path):
        return ["DESIGN_GATE_ABSENT: manifest unavailable"]
    try:
        p = subprocess.run(
            [sys.executable, design_gate_path, deliverable_path,
             manifest_path],
            capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return ["DESIGN_GATE_TOOL_ERROR: %s" % e]
    if p.returncode == 0:
        return []
    violations = []
    for line in (p.stdout + "\n" + p.stderr).splitlines():
        line = line.strip()
        if not line:
            continue
        # design_gate prints "  ✕ <VIOLATION>" lines; keep them verbatim.
        if "✕" in line:
            violations.append("DESIGN_GATE: " + line.split("✕", 1)[1].strip())
    if not violations:
        violations.append("DESIGN_GATE: failed with exit %d (no parsed "
                          "violations)" % p.returncode)
    return violations


def default_design_gate_paths():
    """Design gate + manifest resolved from the PROTECTED ref.

    The gate module executes from the base-pinned checkout (the CI workflow
    runs on pull_request_target), so these paths are base code by
    construction — never the PR's. Returns (gate_path, manifest_path) with
    "" for whichever is absent."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gp = os.path.join(root, "tools", "design_gate.py")
    mp = os.path.join(root, "smart-blocks", "manifest.json")
    return (gp if os.path.isfile(gp) else "",
            mp if os.path.isfile(mp) else "")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Unified Activation Gate: fail closed on unactivated, "
                    "counterfeit, transplanted, or structurally unlawful "
                    "deliverables.")
    ap.add_argument("--receipt", required=True, help="activation receipt JSON path")
    ap.add_argument("--deliverable", required=True,
                    help="shipped artifact path (must cite the receipt)")
    ap.add_argument("--mode", choices=("protected", "local"),
                    default="protected",
                    help="protected: resolve truth from the runner (default). "
                         "local: rehearsal only, verdict labeled CANDIDATE-LOCAL.")
    ap.add_argument("--truth", default=None,
                    help="local-mode truth JSON (ignored in protected mode)")
    ap.add_argument("--job", default=None,
                    help="delivery job context (protected runner supplies this; "
                         "receipt.job must match it exactly)")
    ap.add_argument("--design-gate", default=None,
                    help="explicit design_gate.py to delegate to (the CI "
                         "workflow pins the reviewed design-gate commit here; "
                         "default resolves from the protected base ref via "
                         "default_design_gate_paths).")
    ap.add_argument("--design-manifest", default=None,
                    help="explicit manifest for the design gate.")
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

    # Deliverable binding context: the protected runner supplies the job.
    # The deliverable digest is always recomputed inside check() from the
    # presented deliverable bytes — the runner never asserts it.
    delivery = {"job": args.job}

    verdict, violations = check(receipt_bytes, deliverable_text, truth,
                                delivery=delivery)

    # Design-gate delegation (round-2, hole 3): structural closed-world.
    # Never silent: absent gate => BLOCKED, never PASS.
    if args.design_gate is not None or args.design_manifest is not None:
        dg_path = args.design_gate or ""
        dg_manifest = args.design_manifest or ""
    else:
        dg_path, dg_manifest = default_design_gate_paths()
    dg_violations = run_design_gate(args.deliverable, dg_path, dg_manifest)
    if dg_violations == ["DESIGN_GATE_ABSENT"] or dg_violations == [
            "DESIGN_GATE_ABSENT: manifest unavailable"]:
        # Fail closed and honest: without the structural gate the component
        # closed-world row cannot be evaluated, so PASS is not issuable.
        return _emit("BLOCKED-DESIGN-GATE-ABSENT",
                     ["component closed-world unverifiable: the design gate "
                      "is absent from the protected ref — no silent "
                      "pass-through"] + violations, args, 1, local=local)
    violations = violations + dg_violations
    if violations:
        verdict = "REJECT"

    if local:
        # Local-mode labels never contain the substring "PASS" (round-2 fix):
        # a naive `"PASS" in verdict` check must not confuse them.
        verdict = ("CANDIDATE-LOCAL-CLEAN" if verdict == "PASS"
                   else "CANDIDATE-LOCAL-REJECTED")
    # Exit discipline: 0 if and ONLY if verdict == "PASS" exactly.
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
