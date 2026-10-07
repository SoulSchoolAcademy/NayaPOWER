#!/usr/bin/env python3
"""
Unified Activation Gate — ROUND 2. ONE receipt schema, ONE protected truth
provider, ONE locked door.

Round-1 (branch naya5/unified-activation-gate) was independently attacked:
verdict STILL-LEAKING, 5.5/10. Four reproduced bypasses, all closed here:

  BYPASS 1 (ROW 8 — the gate guarded nothing): the CI workflow's `paths:`
      filter meant deliverable PRs avoiding 3 files never triggered it, and
      no required status check existed. CLOSED: new workflow
      `.github/workflows/activation-delivery-gate.yml` runs on
      `pull_request_target` for PRs to main touching deliverable paths, and
      the delivery job fails closed when a changed deliverable has no valid
      bound receipt. (Marking the check *required* in branch protection is an
      authority change — needs Shawn/admin; named in the report, not done
      silently.)
  BYPASS 2 (PR-EDITABLE TRUST ROOT): `resolve_truth()` read
      GITHUB_REPOSITORY from a plain env var (proven: it queried
      `evil-corp/stolen-repo`), and `pull_request` + PR-supplied code meant
      the gate ran the PR's own judge. CLOSED: repository identity now comes
      from the runner-written event payload (GITHUB_EVENT_PATH), cross-
      checked against the GITHUB_REPOSITORY env — any disagreement fails
      closed. The delivery workflow is `pull_request_target`: the workflow
      file and the gate code come from BASE, never from the PR. The PR's
      bytes are data, verified, never executed as the judge.
  BYPASS 3 (ROW 7 — freestyle component): an undocumented component class +
      freestyle CSS passed with a valid receipt. The component/structural
      closed-world belongs to the design lane (tools/design_gate.py, PR
      #1996, branch naya5/ship-design-gate) — this gate does NOT reimplement
      it. DELEGATE-AND-VERIFY: in delivery mode the workflow fetches the
      design gate + manifest at the PINNED reviewed commit DESIGN_GATE_PIN
      (content-addressed, immutable — the PR cannot change its judge) and
      the gate folds its verdict into every HTML deliverable. No design gate
      available -> DESIGN_GATE_UNAVAILABLE -> REJECT (fail closed, never a
      silent pass). Coordination note: PR #1994 (gate fusion) is the
      reconciliation vehicle to watch so three gates don't become permanent.
  BYPASS 4 (RECEIPT TRANSPLANT): a receipt minted for one job shipped a
      different deliverable — job/proof_plan/session_id were unchecked free
      text. CLOSED: the receipt must bind every deliverable it covers via
      `deliverables: [{path, sha256}]`, and the gate recomputes the hash
      from the actual bytes. A receipt minted for page A cannot ship page B.
      job/proof_plan/session_id remain descriptive claims about the
      activation session — the ENFORCED binding is the deliverable hash.

  PLUS: local-mode label `CANDIDATE-LOCAL-PASS` contained the substring
      "PASS" and exited 0. CLOSED: local verdicts are
      `LOCAL-REHEARSAL-UNVERIFIED` / `LOCAL-REHEARSAL-REJECTED` (no "PASS"
      substring anywhere) and local mode ALWAYS exits 3 — distinct from
      0=PASS, 1=REJECT, 2=tool error.

ARCHITECTURAL LAW (non-negotiable): a builder cannot establish authenticity
by writing a plausible JSON file. Any input the builder supplies about the
truth being checked is untrusted by construction.

Round-3 settles the forgery question (attacker A1) explicitly: a receipt
with correct PUBLIC data (repo, live SHA, blob SHAs, fresh timestamp,
valid deliverables[] binding) but minted by NOBODY is still a forgery, and
public data was never the authenticity root. Authenticity == RUN-ATTESTED
ISSUANCE: the receipt must have been minted by the trusted mint workflow
(.github/workflows/activation-mint.yml, base code, trusted runner), and the
delivery gate verifies via the live API that the attested run exists in the
gated repository, ran the mint workflow to success via workflow_dispatch,
and its artifact's receipt.json is byte-identical to the presented receipt.
A self-minted receipt, however perfect its public data, FAILS issuance
verification: ISSUANCE_UNATTESTED / ISSUANCE_BYTES_MISMATCH.

What the gate enforces, precisely:
  (1) ISSUANCE — the receipt was minted by the trusted runner (delivery
      boundary only; the single-pair predicate tests consistency+binding).
  (2) CONSISTENCY — schema v2, ACTIVATED, identity fields, exact repo,
      full 40-hex live main SHA equality, closed-world source fingerprints,
      4h TTL, no future skew.
  (3) BINDING — two-way: deliverable cites sha256(exact receipt bytes);
      receipt's deliverables[] binds sha256(canonical deliverable bytes).
  (4) ROW 7 — the design lane's gate judges HTML deliverables on
      canonicalized bytes (D3/D4 quote-tolerant); absent design gate fails
      closed.
job/proof_plan/session_id remain DESCRIPTIVE claims about the activation
session — the enforced primitives are issuance, consistency, and binding.
In protected mode the only trusted inputs are the runner context (the
runner-written event payload + GITHUB_TOKEN) and the live GitHub API.
A self-served truth (--mode local) can never produce a PASS verdict — only
an honestly labeled LOCAL-REHEARSAL-* verdict with a distinct exit code.

Binding design (no circularity): the deliverable cites the receipt with
  <!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->
where <64hex> = sha256 of the EXACT receipt bytes. The receipt binds the
deliverable with deliverables[].sha256 = sha256 of the deliverable bytes
with ALL citation-marker comments stripped (canonical form). Mint order:
page -> hash -> receipt -> insert marker. The gate strips markers before
hashing, so minting converges in one pass.

Acceptance table (every row must hold in real CI):
  authentic fresh receipt, exact repo, full current main SHA,
    bound deliverable, RUN-ATTESTED issuance ........ PASS
  fabricated / self-asserted receipt .............. REJECT
  self-minted receipt, perfect public data (A1) ... REJECT (ISSUANCE_*)
  tampered attestation / foreign run / failed run . REJECT (ISSUANCE_*)
  stale activation / changed commit (tip moved) ... REJECT
  wrong repository identity ...................... REJECT
  env-tampered repository (event payload wins) .... TOOL-ERROR (fail closed)
  missing / abbreviated / mismatched commit SHA .. REJECT
  missing / tampered receipt ..................... REJECT
  transplanted receipt (wrong deliverable) ....... REJECT
  deleted deliverable with tombstone ............. PASS
  deleted deliverable without tombstone .......... REJECT
  unregistered component class (design lane) ..... REJECT (delegated)
  unquoted class=naya-evil (D3) .................. REJECT
  spaced class = "..." (D4) ...................... REJECT
  expired / future activation .................... REJECT
  alternate route bypassing the gate .............. LOCAL-REHEARSAL-*, never
      PASS, exit 3 (self-minted truth yields no passing verdict)

Closed-world source rule: receipt.loaded must be an object whose keys are
EXACTLY the CANONICAL_SOURCES registry below, each a 40-hex blob SHA equal
to the blob's SHA in the live main tree. A new source is not a new key in a
receipt — it is a code change to CANONICAL_SOURCES plus its contract, or CI
fails.

Exit codes: 0 = PASS (protected) | 1 = REJECT | 2 = tool error
(including "cannot resolve trusted truth" — fail closed) |
3 = local rehearsal (never a pass, never confusable with one).
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

# Deliverable scope: what the delivery gate guards. A file is a deliverable
# when it lives under a DELIVERABLE_ROOT or its name ends with a
# DELIVERABLE_SUFFIX. The workflow's paths: filter mirrors this list.
DELIVERABLE_ROOTS = ("smart-blocks/",)
DELIVERABLE_SUFFIXES = (".html",)

# Conventional receipt location inside the PR head (untrusted bytes —
# content is fully verified; the path is just where the gate looks).
RECEIPT_PATH = ".naya/activation/receipt.json"

IDENTITY_FIELDS = ("session_id", "naya_identity", "human_authority",
                   "repository", "job", "proof_plan")

API_HOST = "https://api.github.com"


def _normalize_repo(name):
    if not isinstance(name, str):
        return ""
    return name.strip().lower().rstrip("/")


def _safe_repo_path(p):
    """Repo-relative, no absolute paths, no parent escapes."""
    if not isinstance(p, str) or not p:
        return False
    if p.startswith("/") or p.startswith("\\"):
        return False
    parts = p.replace("\\", "/").split("/")
    if any(part in ("", ".", "..") for part in parts):
        return False
    norm = "/".join(parts)
    return norm == p


def _is_deliverable(path):
    if not isinstance(path, str):
        return False
    p = path.replace("\\", "/")
    if any(p == r.rstrip("/") or p.startswith(r) for r in DELIVERABLE_ROOTS):
        return True
    return any(p.lower().endswith(s) for s in DELIVERABLE_SUFFIXES)


def _canonical_deliverable_bytes(raw):
    """Deliverable bytes with ALL citation markers stripped — the canonical
    form the receipt's deliverables[].sha256 binds. Lets minting converge
    in one pass: page -> hash -> receipt -> insert marker."""
    if isinstance(raw, (bytes, bytearray)):
        text = bytes(raw).decode("utf-8", errors="replace")
    else:
        text = str(raw)
    return RECEIPT_MARKER_RE.sub("", text).encode("utf-8")


def _sha256_hex(data):
    return hashlib.sha256(bytes(data)).hexdigest()


def check_receipt(receipt_bytes, truth):
    """Receipt-side predicate: (receipt_dict_or_None, verdict, violations).
    Pure function, no I/O, no network. Covers everything except the
    deliverable binding and citation (see check_deliverable_binding)."""
    violations = []

    if not isinstance(receipt_bytes, (bytes, bytearray)) or not receipt_bytes:
        return None, "REJECT", ["RECEIPT_MISSING_OR_EMPTY"]
    try:
        receipt = json.loads(receipt_bytes)
    except (ValueError, UnicodeDecodeError) as e:
        return None, "REJECT", ["RECEIPT_UNTAMPERED_UNREADABLE: %s" % e]
    if not isinstance(receipt, dict):
        return None, "REJECT", ["RECEIPT_NOT_AN_OBJECT"]

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

    # --- trusted repository binding (bypass 2) ---
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

    # --- freshness (4h TTL, no future) ---
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

    # --- deliverables list shape (bypass 4: transplant defense) ---
    dlist = receipt.get("deliverables")
    if not isinstance(dlist, list) or not dlist:
        violations.append("DELIVERABLES_UNBOUND: receipt names no bound "
                          "deliverables (transplant risk)")
    else:
        for i, entry in enumerate(dlist):
            if not isinstance(entry, dict):
                violations.append("DELIVERABLES_UNBOUND: entry %d not an object" % i)
                continue
            if not _safe_repo_path(entry.get("path")):
                violations.append("DELIVERABLE_PATH_UNSAFE: entry %d path %r"
                                  % (i, entry.get("path")))
            if not isinstance(entry.get("sha256"), str) or not SHA64_RE.match(
                    entry.get("sha256", "")):
                violations.append("DELIVERABLE_SHA_MALFORMED: entry %d" % i)

    if violations:
        return receipt, "REJECT", violations
    return receipt, "PASS", []


def check_deliverable_binding(receipt_bytes, receipt, deliverable_bytes):
    """Two-way binding for ONE presented deliverable. Returns violations.

    deliverable -> receipt: the citation marker must equal sha256 of the
        EXACT receipt bytes (stale/forged citation impossible).
    receipt -> deliverable: some deliverables[] entry must equal sha256 of
        the canonical (marker-stripped) deliverable bytes — a receipt minted
        for page A cannot ship page B (transplant impossible).
    """
    violations = []
    if receipt is None:
        return ["RECEIPT_MISSING_OR_EMPTY"]
    if not isinstance(deliverable_bytes, (bytes, bytearray)):
        return ["CITATION_MISSING: no deliverable bytes to check"]

    digest = _sha256_hex(receipt_bytes)
    text = bytes(deliverable_bytes).decode("utf-8", errors="replace")
    m = RECEIPT_MARKER_RE.search(text)
    if not m:
        violations.append(
            "CITATION_MISSING: deliverable carries no "
            "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> --> marker")
    elif m.group(1).lower() != digest:
        violations.append(
            "CITATION_DIGEST_MISMATCH: marker does not match sha256 of "
            "the exact receipt bytes (stale or forged citation)")

    dhash = _sha256_hex(_canonical_deliverable_bytes(deliverable_bytes))
    bound = False
    for entry in receipt.get("deliverables") or []:
        if isinstance(entry, dict) and isinstance(entry.get("sha256"), str) \
                and entry["sha256"].lower() == dhash:
            bound = True
            break
    if not bound:
        violations.append(
            "DELIVERABLE_BINDING_MISMATCH: no deliverables[] entry matches "
            "sha256 of the presented deliverable — receipt was minted for "
            "different bytes (transplant)")
    return violations


def check(receipt_bytes, deliverable_text, truth):
    """Pure predicate: (verdict, violations). No I/O, no network.

    receipt_bytes .... exact bytes of the receipt file (digest-bound)
    deliverable_text . bytes or text of the shipped artifact
    truth ............ {"repository", "main_sha", "source_blobs", "now"}
    """
    receipt, verdict, violations = check_receipt(receipt_bytes, truth)
    if verdict == "REJECT" and receipt is None:
        return verdict, violations
    if isinstance(deliverable_text, str):
        deliverable_bytes = deliverable_text.encode("utf-8", errors="replace")
    else:
        deliverable_bytes = deliverable_text
    violations = violations + check_deliverable_binding(
        receipt_bytes, receipt, deliverable_bytes)
    if violations:
        return "REJECT", violations
    return "PASS", []


# ---------------------------------------------------------------------------
# ROW 7 — delegate-and-verify. The component/structural closed-world belongs
# to the design lane: tools/design_gate.py (PR #1996, branch
# naya5/ship-design-gate). This gate does NOT reimplement it. In delivery
# mode the CI workflow fetches the design gate + manifest at the PINNED
# reviewed commit DESIGN_GATE_PIN (content-addressed, immutable — the PR
# cannot change which code judges it) and this function runs it against each
# HTML deliverable, folding its verdict in. No design gate available ->
# DESIGN_GATE_UNAVAILABLE -> REJECT (fail closed, never a silent pass).
# When PR #1996 merges, the pin becomes tools/design_gate.py at base.
# ---------------------------------------------------------------------------

DESIGN_GATE_PIN = "3bfa8f64cafa482a17ed89790f7be02c2e320628"
DESIGN_GATE_FILE = "tools/design_gate.py"
DESIGN_MANIFEST_FILE = "smart-blocks/manifest.json"


# D3/D4 (round-3): the design lane's class regex only matches quoted
# `class="..."`. Unquoted (`class=naya-evil`) and spaced (`class = "..."`)
# forms evade it. This gate canonicalizes every class attribute to the
# quoted form BEFORE delegating, so the lane's logic judges every class the
# browser will see. Semantics-preserving: `class=x` == `class="x"` in HTML.
CLASS_ATTR_RE = re.compile(
    r'''\bclass\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))''', re.IGNORECASE)


def canonicalize_class_attributes(html_text):
    """Rewrite every class attribute to canonical `class="..."` form."""
    def _q(m):
        val = m.group(1) if m.group(1) is not None else (
            m.group(2) if m.group(2) is not None else (m.group(3) or ""))
        return 'class="%s"' % val
    return CLASS_ATTR_RE.sub(_q, html_text)


def _download_bytes(url, token):
    """Two-hop download: the API 302-redirects to a pre-signed blob URL that
    rejects the API bearer — take the Location and fetch it WITHOUT auth."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    opener = urllib.request.build_opener(NoRedirect())
    try:
        opener.open(req, timeout=30)
    except Redirected as r:
        loc = r.location
    else:
        raise RuntimeError("artifact download did not redirect — refusing")
    req2 = urllib.request.Request(loc)
    with urllib.request.urlopen(req2, timeout=60) as resp:
        return resp.read()


class Redirected(Exception):
    def __init__(self, location):
        super().__init__("redirect")
        self.location = location


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Redirected(newurl)


MINT_WORKFLOW_PATH = ".github/workflows/activation-mint.yml"
MINT_ARTIFACT_PREFIX = "activation-receipt-"


def verify_issuance(receipt, receipt_bytes, truth, token):
    """Run-attested trusted issuance (round-3, forgery A1).

    A receipt is authentic iff the trusted mint workflow minted THESE EXACT
    BYTES: the attested run must exist in this repo, have run the base mint
    workflow to success via workflow_dispatch, and its artifact's
    receipt.json must be byte-identical to the presented receipt. A
    fully self-minted receipt with correct PUBLIC data (repo, live SHA,
    blob SHAs, fresh timestamp, valid binding) FAILS here — public data was
    never the authenticity root; the runner's attested issuance is.
    Returns a list of violations (empty = issuance genuine).
    """
    att = receipt.get("attestation")
    if not isinstance(att, dict):
        return ["ISSUANCE_UNATTESTED: receipt carries no trusted-issuance "
                "attestation — a self-minted receipt, however plausible, "
                "cannot pass the delivery boundary (forgery A1)"]
    run_id = att.get("run_id")
    if not run_id:
        return ["ISSUANCE_UNATTESTED: attestation names no run"]
    repo = _normalize_repo((truth or {}).get("repository", ""))
    if not repo:
        return ["TRUTH_UNTRUSTED: no trusted repository for issuance check"]
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
    head_repo = _normalize_repo(
        ((run.get("head_repository") or {}).get("full_name")) or "")
    if head_repo != repo:
        return ["ISSUANCE_FOREIGN_RUN: attested run %s belongs to %r, not "
                "the gated repository" % (run_id, head_repo)]
    try:
        arts = _api("GET", "/repos/%s/actions/runs/%s/artifacts" % (repo, run_id),
                    token)
    except RuntimeError as e:
        return ["ISSUANCE_UNVERIFIABLE: attested run artifacts unreachable (%s)"
                % e]
    want_digest = _sha256_hex(receipt_bytes)
    saw_receipt_artifact = False
    for a in arts.get("artifacts", []) or []:
        if not str(a.get("name", "")).startswith(MINT_ARTIFACT_PREFIX):
            continue
        saw_receipt_artifact = True
        try:
            blob = _download_bytes(a.get("archive_download_url", ""), token)
        except RuntimeError as e:
            return ["ISSUANCE_UNVERIFIABLE: artifact download failed (%s)" % e]
        import io
        import zipfile
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
                "activation-receipt artifact" % run_id]
    return ["ISSUANCE_BYTES_MISMATCH: the presented receipt bytes are not "
            "byte-identical to the attested run's minted receipt — forged "
            "or tampered issuance (forgery A1)"]


def base_blob_bytes(repo, path, ref, token):
    """Bytes of a file at a base ref, via the live API (for tombstones)."""
    import base64
    meta = _api("GET", "/repos/%s/contents/%s?ref=%s" % (repo, path, ref), token)
    if meta.get("type") != "file" or not meta.get("sha"):
        raise RuntimeError("not a file at base ref")
    blob = _api("GET", "/repos/%s/git/blobs/%s" % (repo, meta["sha"]), token)
    content = blob.get("content", "")
    if blob.get("encoding") != "base64":
        raise RuntimeError("unexpected blob encoding")
    return base64.b64decode("".join(content.split()))


def run_design_gate(deliverable_path, design_gate_path, manifest_path):
    """Run the design lane's gate against one deliverable. Returns a list of
    violation strings (empty = the design gate passed)."""
    if not design_gate_path or not os.path.isfile(design_gate_path):
        return ["DESIGN_GATE_UNAVAILABLE: design gate not supplied — "
                "structural closed-world unverifiable, refusing"]
    if not manifest_path or not os.path.isfile(manifest_path):
        return ["DESIGN_GATE_UNAVAILABLE: design manifest not supplied — "
                "refusing"]
    import subprocess as _sp
    try:
        p = _sp.run([sys.executable, design_gate_path, deliverable_path,
                     manifest_path],
                    capture_output=True, text=True, timeout=120)
    except (OSError, _sp.SubprocessError) as e:
        return ["DESIGN_GATE_TOOL_ERROR: %s" % e]
    if p.returncode == 0:
        return []
    violations = []
    for line in (p.stdout + "\n" + p.stderr).splitlines():
        line = line.strip()
        if "✕" in line:
            violations.append(
                "DESIGN_GATE: " + line.split("✕", 1)[1].strip())
    if not violations:
        violations.append("DESIGN_GATE: failed with exit %d (no parsed "
                          "violations)" % p.returncode)
    return violations


def check_delivery(receipt_bytes, pr_head_dir, changed, truth,
                   design_gate_path="", design_manifest_path="",
                   base_sha="", token=""):
    """Delivery predicate for ONE pull request. Pure apart from reading the
    PR-head files from disk and the live API calls for issuance + tombstones
    (bytes the gate verifies, never trusts).

    Every changed deliverable must be bound by a RUN-ATTESTED receipt
    (issuance verified via the live API — forgery A1), by path + sha256 of
    PR-head bytes, and cite the receipt (marker = sha256 of exact receipt
    bytes). HTML deliverables additionally pass the design lane's gate on
    canonicalized bytes (D3/D4 quote-tolerant). Deleted deliverables travel
    the tombstone path: the receipt carries action:"delete" and the gate
    verifies the base blob. Returns (verdict, violations).

    `changed`: list of {"path", "status", "previous_filename"} — status in
    added/modified/removed/renamed (the PR files API vocabulary).
    """
    violations = []
    receipt, verdict, v = check_receipt(receipt_bytes, truth)
    violations.extend(v)
    if receipt is None:
        return "REJECT", violations

    # issuance FIRST: no attested issuance, no delivery — however plausible
    # the receipt's public data (forgery A1).
    violations.extend(verify_issuance(receipt, receipt_bytes, truth, token))
    if any(x.startswith("ISSUANCE_") or x.startswith("TRUTH_UNTRUSTED")
           for x in violations):
        return "REJECT", violations

    # expand renames into delete(old) + add(new)
    logical = []
    for c in changed or []:
        path = c.get("path", "")
        status = (c.get("status") or "modified").lower()
        prev = c.get("previous_filename")
        if status == "renamed" and prev and prev != path:
            logical.append({"path": prev, "status": "removed"})
            logical.append({"path": path, "status": "added"})
        else:
            logical.append({"path": path, "status": status})
    changed_deliverables = [c for c in logical if _is_deliverable(c["path"])]
    if not changed_deliverables:
        violations.append("DELIVERY_SCOPE_EMPTY: no changed deliverables — "
                          "nothing for the gate to bind (fail closed)")
        return "REJECT", violations

    entries = {}
    for entry in receipt.get("deliverables") or []:
        if isinstance(entry, dict) and _safe_repo_path(entry.get("path")):
            entries[entry["path"]] = entry

    repo = _normalize_repo((truth or {}).get("repository", ""))
    digest = _sha256_hex(receipt_bytes)

    for change in sorted(changed_deliverables, key=lambda c: c["path"]):
        path = change["path"]
        status = change["status"]
        entry = entries.get(path)
        if not _safe_repo_path(path):
            violations.append("DELIVERABLE_PATH_UNSAFE: %r" % path)
            continue
        disk_path = os.path.join(pr_head_dir, path)

        if status == "removed":
            # --- tombstone path (round-3c): legitimate deletions merge ---
            if entry is None or entry.get("action") != "delete":
                violations.append(
                    "DELETION_UNATTESTED: %r is removed in the PR but the "
                    "receipt carries no tombstone for it (action:\"delete\")"
                    % path)
                continue
            if os.path.isfile(disk_path):
                violations.append(
                    "DELETION_NOT_EFFECTIVE: %r attested deleted but still "
                    "present in the PR head" % path)
                continue
            ref = base_sha or (truth or {}).get("main_sha", "")
            try:
                base_raw = base_blob_bytes(repo, path, ref, token)
            except RuntimeError as e:
                violations.append(
                    "DELETION_UNVERIFIABLE: base bytes of %r unreachable (%s)"
                    % (path, e))
                continue
            if _sha256_hex(_canonical_deliverable_bytes(base_raw)) != \
                    str(entry.get("sha256", "")).lower():
                violations.append(
                    "DELETION_BINDING_MISMATCH: tombstone for %r does not "
                    "match the base bytes (wrong file)" % path)
            continue

        if entry is None:
            violations.append(
                "DELIVERABLE_NOT_BOUND: changed deliverable %r is not listed "
                "in receipt.deliverables" % path)
            continue

        if not os.path.isfile(disk_path):
            violations.append("DELIVERABLE_MISSING: %r not found in PR head "
                              "(not marked deleted — tombstone required)" % path)
            continue
        with open(disk_path, "rb") as f:
            raw = f.read()
        if _sha256_hex(_canonical_deliverable_bytes(raw)) != \
                str(entry.get("sha256", "")).lower():
            violations.append(
                "DELIVERABLE_BINDING_MISMATCH: PR-head bytes of %r do not "
                "match the receipt's bound sha256 (transplant or drift)" % path)
            continue
        # citation: deliverable -> receipt
        text = raw.decode("utf-8", errors="replace")
        m = RECEIPT_MARKER_RE.search(text)
        if not m:
            violations.append("CITATION_MISSING: %r carries no receipt marker" % path)
        elif m.group(1).lower() != digest:
            violations.append(
                "CITATION_DIGEST_MISMATCH: %r marker does not match sha256 of "
                "the exact receipt bytes" % path)
        # ROW 7 — delegate-and-verify on CANONICALIZED bytes (D3/D4): the
        # design lane's gate judges the structural closed-world; every class
        # attribute is first rewritten to the quoted form so unquoted/spaced
        # evasions cannot hide from its regex. Absent design gate fails
        # closed — never a silent pass.
        if path.lower().endswith(".html"):
            canon = canonicalize_class_attributes(text)
            if canon != text:
                fd, tmp = None, None
                try:
                    import tempfile
                    fd, tmp = tempfile.mkstemp(prefix="gate-canon-",
                                               suffix=".html")
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(canon)
                    delegate_path = tmp
                except OSError as e:
                    violations.append("TOOL-ERROR: canonicalization failed (%s)"
                                      % e)
                    delegate_path = disk_path
            else:
                tmp, delegate_path = None, disk_path
            try:
                violations.extend(
                    "[%s] %s" % (path, x)
                    for x in run_design_gate(delegate_path, design_gate_path,
                                             design_manifest_path))
            finally:
                if tmp:
                    try:
                        os.unlink(tmp)
                    except OSError:
                        pass

    if violations:
        return "REJECT", violations
    return "PASS", []


# ---------------------------------------------------------------------------
# Protected truth provider
# ---------------------------------------------------------------------------

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
    """Protected truth provider. Repository identity comes from the
    RUNNER-WRITTEN event payload (GITHUB_EVENT_PATH) — never from a plain
    env var a workflow step or a local shell could override (bypass 2:
    the attacker set GITHUB_REPOSITORY=evil-corp/stolen-repo and the old
    code obeyed). When the GITHUB_REPOSITORY env is present it must AGREE
    with the event payload; any disagreement fails closed. Raises on any
    failure — the gate fails closed when trust cannot be established.

    Trusted inputs ONLY: the runner event payload + GITHUB_TOKEN from the
    runner context, and the live GitHub API. There is deliberately no flag,
    env var, or file that lets the caller supply truth.
    """
    event_path = os.environ.get("GITHUB_EVENT_PATH", "").strip()
    if not event_path or not os.path.isfile(event_path):
        raise RuntimeError("cannot establish trusted repository identity "
                           "(no runner event context at GITHUB_EVENT_PATH) "
                           "— refusing")
    try:
        with open(event_path, encoding="utf-8") as f:
            event = json.load(f)
    except (ValueError, OSError) as e:
        raise RuntimeError("runner event payload unreadable (%s) — refusing" % e)
    repo = (((event.get("repository") or {}).get("full_name")) or "").strip()
    if not repo or "/" not in repo:
        raise RuntimeError("runner event carries no repository identity — refusing")
    env_repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if env_repo and _normalize_repo(env_repo) != _normalize_repo(repo):
        raise RuntimeError(
            "GITHUB_REPOSITORY %r disagrees with runner event payload %r — "
            "the env var is caller-editable and untrusted, refusing" % (env_repo, repo))
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


def pr_changed_files(repo, pr_number, token):
    """Changed files of a PR, via the live API (trusted). Returns a list of
    {"path", "status", "previous_filename"} in the PR files API vocabulary."""
    files = []
    page = 1
    while True:
        batch = _api("GET", "/repos/%s/pulls/%s/files?per_page=100&page=%d"
                     % (repo, pr_number, page), token)
        if not batch:
            break
        for f in batch:
            files.append({"path": f.get("filename", ""),
                          "status": (f.get("status") or "modified").lower(),
                          "previous_filename": f.get("previous_filename")})
        if len(batch) < 100:
            break
        page += 1
        if page > 40:
            raise RuntimeError("PR file list implausibly large — refusing")
    return files


def parse_changed_files(spec):
    """CLI override: 'path[:status],path[:status],...' (default modified)."""
    out = []
    for chunk in (spec or "").split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            path, status = chunk.rsplit(":", 1)
        else:
            path, status = chunk, "modified"
        out.append({"path": path.strip(), "status": status.strip().lower() or
                    "modified", "previous_filename": None})
    return out


def load_local_truth(path):
    """Local rehearsal truth. The verdict is ALWAYS labeled LOCAL-REHEARSAL —
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
        description="Unified Activation Gate (r2): fail closed on unactivated, "
                    "counterfeit, or transplanted activation.")
    ap.add_argument("--receipt", default=None,
                    help="activation receipt JSON path (single-pair mode)")
    ap.add_argument("--deliverable", default=None,
                    help="shipped artifact path (single-pair mode)")
    ap.add_argument("--delivery", action="store_true",
                    help="delivery mode: gate a whole PR (needs --pr-head, --pr)")
    ap.add_argument("--pr-head", default=None,
                    help="directory holding the PR head checkout (delivery mode)")
    ap.add_argument("--pr", default=None,
                    help="PR number (delivery mode; changed files via live API)")
    ap.add_argument("--changed-files", default=None,
                    help="comma-separated 'path[:status]' (delivery mode; "
                         "overrides the live API — for tests)")
    ap.add_argument("--base-sha", default="",
                    help="base ref SHA for tombstone verification (delivery "
                         "mode; defaults to the PR base / live main)")
    ap.add_argument("--design-gate", default="",
                    help="path to the design lane's gate script (delivery "
                         "mode; row-7 delegate-and-verify)")
    ap.add_argument("--design-manifest", default="",
                    help="path to the Smart Blocks manifest (delivery mode)")
    ap.add_argument("--mode", choices=("protected", "local"),
                    default="protected",
                    help="protected: resolve truth from the runner (default). "
                         "local: rehearsal only, verdict labeled LOCAL-REHEARSAL, "
                         "exit 3 (never a pass).")
    ap.add_argument("--truth", default=None,
                    help="local-mode truth JSON (ignored in protected mode)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.delivery and args.mode == "local":
        return _emit("TOOL-ERROR",
                     ["delivery mode requires protected truth (local cannot "
                      "establish the PR's live context)"],
                     args, 2, local=False)

    if args.delivery:
        return _run_delivery(args)

    if not args.receipt or not args.deliverable:
        return _emit("TOOL-ERROR",
                     ["single-pair mode requires --receipt and --deliverable"],
                     args, 2, local=False)

    try:
        with open(args.receipt, "rb") as f:
            receipt_bytes = f.read()
    except OSError as e:
        return _emit("TOOL-ERROR", [str(e)], args, 2, local=False)
    try:
        with open(args.deliverable, "rb") as f:
            deliverable_bytes = f.read()
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

    verdict, violations = check(receipt_bytes, deliverable_bytes, truth)
    if local:
        # Bypass-5 fix: no "PASS" substring anywhere; exit 3 always.
        verdict = ("LOCAL-REHEARSAL-UNVERIFIED" if verdict == "PASS"
                   else "LOCAL-REHEARSAL-REJECTED")
        return _emit(verdict, violations, args, 3, local=True)
    code = 0 if verdict == "PASS" else 1
    return _emit(verdict, violations, args, code, local=False)


def _run_delivery(args):
    if not args.pr_head or not os.path.isdir(args.pr_head):
        return _emit("TOOL-ERROR", ["delivery mode requires --pr-head DIR"],
                     args, 2, local=False)
    receipt_file = os.path.join(args.pr_head, RECEIPT_PATH)
    try:
        with open(receipt_file, "rb") as f:
            receipt_bytes = f.read()
    except OSError:
        return _emit("REJECT", ["RECEIPT_MISSING_OR_EMPTY: no receipt at %s "
                                "in the PR head — deliverables cannot ship "
                                "without bound activation (fail closed)"
                                % RECEIPT_PATH],
                     args, 1, local=False)
    try:
        truth = resolve_truth()
    except RuntimeError as e:
        return _emit("TOOL-ERROR", [str(e)], args, 2, local=False)

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    try:
        if args.changed_files is not None:
            changed = parse_changed_files(args.changed_files)
        else:
            if not args.pr:
                return _emit("TOOL-ERROR",
                             ["delivery mode needs --pr or --changed-files"],
                             args, 2, local=False)
            changed = pr_changed_files(truth["repository"], args.pr, token)
    except RuntimeError as e:
        return _emit("TOOL-ERROR", [str(e)], args, 2, local=False)

    base_sha = args.base_sha.strip() or ""
    if not base_sha and not args.changed_files:
        # live path: the PR's base SHA from the runner event payload
        try:
            with open(os.environ.get("GITHUB_EVENT_PATH", "")) as f:
                ev = json.load(f)
            base_sha = ((ev.get("pull_request") or {}).get("base") or {}).get("sha", "")
        except (OSError, ValueError):
            base_sha = ""

    verdict, violations = check_delivery(receipt_bytes, args.pr_head, changed,
                                         truth, args.design_gate,
                                         args.design_manifest,
                                         base_sha=base_sha, token=token)
    code = 0 if verdict == "PASS" else 1
    return _emit(verdict, violations, args, code, local=False)


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
