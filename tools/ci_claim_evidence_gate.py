"""CI caller for the anti-citogenesis claim-evidence gate.

WHAT THIS IS
------------
The enforcement activation for tools/check_claim_evidence.py (merged as
PR #2325). It runs in CI on pull_request_target -- the workflow file and
tools/ come from BASE, so the PR being judged cannot edit its judge
(see .github/workflows/claim-evidence-gate.yml header). The PR head is
checked out as DATA for test-path existence checks.

It fetches the PR body via the GitHub API, extracts verification
attestations with the gate's own find_attestations (never reimplemented),
gathers evidence the gate accepts, and fails closed (exit 1) when any
attestation stands on nothing admissible. A body with no attestations
passes vacuously -- PRs that make no verification claims are not punished.

Evidence gathered (the caller owns provenance -- the gate adjudicates):
  test        -- .py test paths named in the body, existence checked
                 against the PR head checkout. Named-but-missing paths are
                 INCLUDED so the gate fails them closed ("does not exist")
                 instead of silently skipping them.
  ci_run      -- completed+successful check runs on the PR head. (The gate
                 itself would accept any ci_run id; this caller is stricter:
                 only green runs count.)
  seat_review -- submitted, non-dismissed PR reviews whose body carries a
                 "Seat: ..." tag. Compared against the PR body's declared
                 seat via the gate's normalize_seat.

Notes and commits are NOT gathered: per the gate spec they can never be
independent evidence, so they cannot change the verdict.

WHAT THIS DOES NOT DO (D32 honesty -- read before trusting this gate)
---------------------------------------------------------------------
1. Pooled evidence (inherited from the gate): one admissible item covers
   EVERY attestation in the body. Per-attestation linkage is future work.
2. Seat tags are parsed TEXT, not identity. All GitHub activity shares one
   login; anyone can write "Seat: Naya 4" in a review body and this caller
   trusts it. Tag spoofing is not detected.
3. Review STATE is not adjudicated (beyond excluding DISMISSED). An
   APPROVED, COMMENTED, or CHANGES_REQUESTED review from a different seat
   counts the same. A changes-requested review is scrutiny, not
   verification -- the gate does not distinguish. Tightening this is a
   spec change to check_claim_evidence.py, not a caller tweak.
4. CI runs: a green run proves the machines ran green, not WHAT they
   verified. Only the run's existence + success is checked.
5. Test paths are extracted heuristically from body text. A path that looks
   like a test but isn't one is still checked for existence; existence is
   all the gate claims.
6. Missing author seat tag: when the body declares no "Seat:", the gate
   treats ANY seated review as independent (normalize_seat("") matches
   nothing, so seat != author is vacuously true). Bodies should declare
   their seat; without it, a same-seat review can pass as independent.
7. Only the first 100 reviews and first 100 check runs are considered
   (API pagination cap). PRs beyond that are out of scope.
8. Infrastructure failure (API unreachable, body unfetchable) fails CLOSED
   (exit 1, GATE_BLIND). A gate that passes when blind is theater.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_claim_evidence import (  # noqa: E402
    Evidence,
    adjudicate,
    find_attestations,
)

# ---------------------------------------------------------------------------
# Pure functions (unit-tested in tests/test_ci_claim_evidence_gate.py)
# ---------------------------------------------------------------------------

_SEAT_TAG_RE = re.compile(r"^[ \t]*seat[ \t]*:[ \t]*(.+?)[ \t]*$", re.IGNORECASE | re.MULTILINE)


def parse_seat_tag(text: str) -> str:
    """Return the raw seat string from the first 'Seat: ...' line, else ''.

    Convention: PR bodies and review bodies carry 'Seat: Naya N'. Only the
    first tag is read; later tags are ignored (documented, not silent).
    """
    if not text:
        return ""
    m = _SEAT_TAG_RE.search(text)
    return m.group(1).strip() if m else ""


_PY_PATH_RE = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9_./-]+\.py)(?![A-Za-z0-9_])")


def extract_test_paths(body: str) -> list:
    """Heuristically extract test-file paths named in prose.

    Keeps .py paths whose basename starts with 'test_' or that live under a
    tests/ directory. Order-preserving dedupe. This is a heuristic, not a
    parser -- see limitation 5 above.
    """
    seen: list = []
    for m in _PY_PATH_RE.finditer(body or ""):
        p = m.group(1).lstrip("./")
        base = p.rsplit("/", 1)[-1]
        if not (base.startswith("test_") or "/tests/" in p or p.startswith("tests/")):
            continue
        if p not in seen:
            seen.append(p)
    return seen


def resolve_test_path(path: str, path_exists) -> str | None:
    """Resolve a named test path to an existing one, else None.

    Checks the path as written first; falls back to tests/<basename> for
    bare test filenames. Returns None when nothing exists -- the caller
    still records the as-written ref so the gate fails it closed.
    """
    if path_exists(path):
        return path
    base = path.rsplit("/", 1)[-1]
    if base.startswith("test_"):
        cand = "tests/" + base
        if cand != path and path_exists(cand):
            return cand
    return None


def build_evidence(body, reviews, check_runs, path_exists) -> list:
    """Assemble the evidence list the gate adjudicates.

    reviews: list of dicts with 'id', 'state', 'body'.
    check_runs: list of dicts with 'id', 'status', 'conclusion'.
    path_exists: callable(relative_path) -> bool, rooted at the PR head.

    Note: the author's seat is NOT needed here -- seat comparison happens
    inside the gate's adjudicate(), which receives the author seat
    separately. Keeping it out avoids a dead parameter that implies a
    check this function does not perform.
    """
    evidence: list = []

    for p in extract_test_paths(body):
        resolved = resolve_test_path(p, path_exists)
        # Unresolved refs are kept as-written: the gate reports
        # "does not exist" and fails closed. Never silently dropped.
        evidence.append(Evidence(kind="test", ref=resolved or p, seat=""))

    for cr in check_runs or []:
        if cr.get("status") == "completed" and cr.get("conclusion") == "success":
            evidence.append(Evidence(kind="ci_run", ref=str(cr.get("id")), seat=""))
    # Anything not completed+successful (failed, in progress, cancelled,
    # including this gate's own in-progress run) contributes nothing.

    for rv in reviews or []:
        if rv.get("state") == "DISMISSED":
            continue  # retracted reviews are not reviews
        seat = parse_seat_tag(rv.get("body") or "")
        evidence.append(Evidence(kind="seat_review", seat=seat, ref=f"review-{rv.get('id')}"))
    # Reviews without a parseable seat tag are kept with seat="": the gate
    # marks them unattributable (inadmissible). Reviews from the author's
    # own seat are kept too: the gate marks them self-attestation.

    return evidence


def render_report(pr_number, head_sha, author_seat, attestations, evidence, result) -> str:
    """Human-readable verdict report for the CI log."""
    lines = [
        "CLAIM-EVIDENCE GATE",
        f"PR #{pr_number} @ {head_sha}",
        f"Author seat: {author_seat or '(not declared -- see limitation 6)'}",
        f"Attestations found: {len(attestations)}",
    ]
    for a in attestations:
        lines.append(f'  - "{a.text}"')
    lines.append(f"Evidence gathered: {len(evidence)}")
    for e in evidence:
        seat = f" seat={e.seat}" if e.seat else ""
        lines.append(f"  - {e.kind}:{e.ref}{seat}")
    lines.append("Verdicts:")
    for v in result["verdicts"]:
        mark = "PASS" if v.admissible else "FAIL"
        lines.append(f'  [{mark}] "{v.attestation.text}"')
        for r in v.reasons:
            lines.append(f"    - {r}")
    lines.append(f"GATE: {'PASS' if result['pass'] else 'FAIL'}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# IO (GitHub API + process boundary)
# ---------------------------------------------------------------------------

_API = "https://api.github.com"

# Retry parity with the consensus gate (packet 1, design infra-asks-t0754).
# Same tuning constants as tools/check_merge_consensus.py — parity, not a new policy.
_API_MAX_ATTEMPTS = 5
_API_BACKOFF_BASE_S = 1
_API_MAX_WAIT_S = 120


def _classify_http_error(e):
    """Classify an HTTPError as ('rate_limit'|'permission'|'error', detail,
    retry_after_seconds_or_None, header_dict). Semantics verbatim from
    check_merge_consensus._classify_http_error; header snapshot is the
    packet-1 addition (per-call x-ratelimit-*/Retry-After on every attempt)."""
    try:
        raw = e.read() or b""
    except Exception:
        raw = b""
    try:
        body_text = raw.decode("utf-8", "replace")
    except Exception:
        body_text = ""
    try:
        msg = json.loads(body_text).get("message", "") if body_text else ""
    except Exception:
        msg = body_text[:200]
    headers = e.headers if e.headers else {}
    retry_after = None
    try:
        ra = headers.get("Retry-After")
        retry_after = int(ra) if ra else None
    except (TypeError, ValueError):
        retry_after = None
    snap = {
        "remaining": headers.get("X-RateLimit-Remaining", "none"),
        "reset": headers.get("X-RateLimit-Reset", "none"),
        "retry_after": headers.get("Retry-After", "none"),
    }
    low = f"{msg} {body_text}".lower()
    if e.code == 429 or (e.code == 403
                         and ("rate limit" in low or retry_after is not None)):
        return "rate_limit", msg or "rate limited", retry_after, snap
    if e.code == 403 and "resource not accessible" in low:
        return "permission", msg or "forbidden", None, snap
    return "error", msg or f"HTTP {e.code}", None, snap


def _fetch_api(path: str, token: str):
    """GET one API path with consensus-gate retry parity.

    Transient rate limits (403/429) retry up to _API_MAX_ATTEMPTS: server's
    Retry-After (capped at _API_MAX_WAIT_S) else exponential backoff
    _API_BACKOFF_BASE_S * 2^(attempt-1). Permission 403s and other failures
    raise immediately. Each retry logs its headers so the next adjudication
    never has to guess rate-limit vs permission. Raises GateAPIError-style
    tuple info bundled into the raised exceptions below.
    """
    req = urllib.request.Request(
        _API + path,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "nayapower-claim-evidence-gate",
        },
    )
    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            kind, detail, retry_after, snap = _classify_http_error(e)
            if kind == "rate_limit" and attempt < _API_MAX_ATTEMPTS:
                wait = retry_after if retry_after else \
                    _API_BACKOFF_BASE_S * (2 ** (attempt - 1))
                wait = max(1, min(wait, _API_MAX_WAIT_S))
                print(f"CLAIM-EVIDENCE GATE: api retry -- HTTP {e.code} "
                      f"(rate-limited), waiting {wait}s "
                      f"(attempt {attempt}/{_API_MAX_ATTEMPTS}) "
                      f"[x-ratelimit-remaining={snap['remaining']}, "
                      f"x-ratelimit-reset={snap['reset']}, "
                      f"retry-after={snap['retry_after']}]",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            # Exhausted or fail-fast: carry a structured blind cause upward.
            raise _BlindCause(path, attempt, e.code, kind, detail, snap)


class _BlindCause(Exception):
    """Transport-blind failure after the retry policy ran its course.

    NOT a packet-3 GATE_BLIND marker change: the vocabulary and exit-code
    contract (packet 3) live on their own branch; this class only carries
    the retry outcome so the existing GateBlind path can render it.
    """
    def __init__(self, path, attempts, code, kind, detail, snap):
        super().__init__(path, attempts, code, kind, detail, snap)
        self.path = path
        self.attempts = attempts
        self.code = code
        self.kind = kind
        self.detail = detail
        self.snap = snap


def api_get(path: str, token: str):
    """GET a GitHub API path. Raises GateBlind on any failure (fail closed).

    Retry parity with the consensus gate: transient 403/429 get 5 attempts;
    the verdict after exhaustion is still fail-closed (exit code unchanged).
    """
    try:
        return _fetch_api(path, token)
    except _BlindCause as bc:
        raise GateBlind(
            f"GET {bc.path} failed after {bc.attempts} attempts: "
            f"{bc.kind} (HTTP {bc.code}, {bc.detail}, "
            f"x-ratelimit-remaining={bc.snap['remaining']})"
        ) from bc
    except Exception as exc:  # noqa: BLE001 -- any IO failure blinds the gate
        raise GateBlind(f"GET {path} failed: {exc}") from exc


class GateBlind(Exception):
    """The gate could not see what it must judge. Fail closed."""


def run_gate(repo: str, pr_number: str, head_sha: str, head_dir: str, token: str) -> int:
    """Full gate run. Returns process exit code (0 pass, 1 fail)."""
    pr = api_get(f"/repos/{repo}/pulls/{pr_number}", token)
    body = pr.get("body") or ""
    author_seat = parse_seat_tag(body)

    attestations = find_attestations(body)
    if not attestations:
        print("CLAIM-EVIDENCE GATE: PASS (no attestations in PR body -- nothing claimed)")
        return 0

    reviews = api_get(f"/repos/{repo}/pulls/{pr_number}/reviews?per_page=100", token)
    check_runs = api_get(
        f"/repos/{repo}/commits/{head_sha}/check-runs?per_page=100", token
    ).get("check_runs", [])

    root = Path(head_dir)
    exists = lambda p: (root / p).is_file()  # noqa: E731

    evidence = build_evidence(body, reviews, check_runs, exists)
    result = adjudicate(body, author_seat, evidence, path_exists=exists)

    print(render_report(pr_number, head_sha, author_seat, attestations, evidence, result))
    return 0 if result["pass"] else 1


def main() -> int:
    try:
        repo = os.environ["GITHUB_REPOSITORY"]
        pr_number = os.environ["PR_NUMBER"]
        head_sha = os.environ["PR_HEAD_SHA"]
        head_dir = os.environ.get("PR_HEAD_DIR", "pr-head")
        token = os.environ["GITHUB_TOKEN"]
    except KeyError as exc:
        print(f"CLAIM-EVIDENCE GATE: FAIL -- missing env {exc} (GATE_BLIND)")
        return 1
    try:
        return run_gate(repo, pr_number, head_sha, head_dir, token)
    except GateBlind as exc:
        print(f"CLAIM-EVIDENCE GATE: FAIL -- {exc} (GATE_BLIND)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
