"""Wire: PR-body caller for the anti-citogenesis claim-evidence gate.

PR #2325 built the adjudicator (tools/check_claim_evidence.py) as pure
spec: claim text + structured evidence in, verdicts out. It deliberately
does NOT parse PR bodies -- "the caller owns provenance of the evidence
list" -- and it is NOT wired into CI. This module is that caller, and the
`claim-evidence-gate` workflow is that wiring.

Operating path: every pull_request event feeds the PR body through
extract_evidence() -> check_claim_evidence.adjudicate(). A verification
attestation ("independently verified", "proven", ...) with no admissible
independent evidence fails the check and blocks the merge path.

Exit codes (fail-closed):
  0 -- PASS: no attestations found, or every attestation has admissible
       independent evidence. Nothing claimed, nothing to prove.
  1 -- VIOLATION: at least one attestation rests on inadmissible evidence
       (self-attestation, repetition, phantom test path, bare claim).
  2 -- CALLER FAILURE: body unreadable, adjudicator unimportable, or an
       unexpected error. The gate goes red rather than silently green.

Evidence extraction is heuristic and documented as such: the adjudicator
remains the authority on admissibility. Anything the extractor cannot
classify is left out (never invented); the fail-closed rule then applies
to the attestation, which is the honest outcome for an unevidenced claim.

Limitations (caller's, not the adjudicator's):
  - `repeats` is not auto-detected; repetition chains across notes are the
    adjudicator's future work, noted in its docstring.
  - Seat identity comes from the PR body's `Seat:` line (all team PRs post
    under one GitHub account). A missing Seat line means self-attestation
    cannot be distinguished from cross-seat review for bare seat mentions;
    named seats still count, documented in the verdict reasons.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from check_claim_evidence import Evidence, adjudicate, find_attestations, normalize_seat
except ImportError as exc:  # fail-closed: no adjudicator, no silent pass
    print(f"claim-evidence-gate: FATAL -- cannot import adjudicator: {exc}", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

_SEAT_LINE = re.compile(r"^\s*seat\s*:\s*(naya|coda)\s*(\d+)", re.IGNORECASE | re.MULTILINE)
_SEAT_MENTION = re.compile(r"\b(naya|coda)\s*(\d+)\b", re.IGNORECASE)
_REVIEW_NEAR = re.compile(
    r"\b(review|reviewed|reviewer|audit|audited|scorecard|verified\s+by|independent\s+verification)\b",
    re.IGNORECASE,
)
_TEST_PATH = re.compile(r"(?<![\w\-./])([\w\-./]*test[\w\-]*\.py)")
_CI_RUN_ID = re.compile(r"\b(\d{9,})\b")
_CI_NEAR = re.compile(r"\b(run|runs|ci|check|workflow|action|actions)\b", re.IGNORECASE)
_COMMIT_SHA = re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b|\b[0-9a-f]{40}\b")
_NOTE_ID = re.compile(r"\bSN-(\d{2,})\b", re.IGNORECASE)

_PROXIMITY = 120  # chars: evidence must sit near its cue word


def _near(text: str, pos: int, cue: re.Pattern, window: int = _PROXIMITY) -> bool:
    lo = max(0, pos - window)
    hi = min(len(text), pos + window)
    return bool(cue.search(text[lo:hi]))


def extract_seat(body: str) -> str:
    """Author seat from the body's `Seat:` line, normalized. '' if absent."""
    m = _SEAT_LINE.search(body or "")
    if not m:
        return ""
    return normalize_seat(f"{m.group(1)} {m.group(2)}")


def extract_evidence(body: str) -> list:
    """Heuristic evidence items cited in PR prose. Never invents items."""
    body = body or ""
    items: list = []
    seen = set()

    def add(kind: str, ref: str, seat: str = "") -> None:
        key = (kind, ref, seat)
        if key not in seen:
            seen.add(key)
            items.append(Evidence(kind=kind, ref=ref, seat=seat))

    for m in _TEST_PATH.finditer(body):
        add("test", m.group(1))

    for m in _CI_RUN_ID.finditer(body):
        if _near(body, m.start(), _CI_NEAR):
            add("ci_run", m.group(1))

    for m in _SEAT_MENTION.finditer(body):
        # The author's own `Seat:` declaration line is not a review.
        line_start = body.rfind("\n", 0, m.start()) + 1
        line_end = body.find("\n", m.end())
        line = body[line_start:line_end if line_end != -1 else len(body)]
        if _SEAT_LINE.search(line):
            continue
        if _near(body, m.start(), _REVIEW_NEAR):
            add("seat_review", f"body@{m.start()}", seat=f"{m.group(1)} {m.group(2)}")

    for m in _COMMIT_SHA.finditer(body):
        add("commit", m.group(0))

    for m in _NOTE_ID.finditer(body):
        add("note", f"SN-{m.group(1)}")

    return items


# ---------------------------------------------------------------------------
# Gate entry point
# ---------------------------------------------------------------------------

def scan(body: str, author_seat: str = "", repo_root: str = ".") -> dict:
    """Run the full gate. Returns the adjudication dict plus extraction meta."""
    seat = author_seat or extract_seat(body)
    evidence = extract_evidence(body)

    def path_exists(ref: str) -> bool:
        return os.path.exists(os.path.join(repo_root, ref))

    try:
        result = adjudicate(body, seat, evidence, path_exists=path_exists)
    except Exception as exc:  # fail-closed: adjudication must not silently pass
        print(f"claim-evidence-gate: FATAL -- adjudication crashed: {exc}", file=sys.stderr)
        sys.exit(2)
    result["author_seat"] = seat
    result["evidence"] = evidence
    result["attestation_count"] = len(find_attestations(body))
    return result


def report(result: dict) -> int:
    """Print the verdict. Returns the process exit code."""
    verdicts = result["verdicts"]
    if not verdicts:
        print("claim-evidence-gate: PASS -- no verification attestations in PR body "
              "(nothing claimed, nothing to prove).")
        return 0
    if result["pass"]:
        print(f"claim-evidence-gate: PASS -- {len(verdicts)} attestation(s), "
              f"each with admissible independent evidence "
              f"(author seat: {result['author_seat'] or 'unknown'}).")
        for v in verdicts:
            ev = ", ".join(f"{e.kind}:{e.ref}" for e in v.admissible_evidence)
            print(f"  ok: \"{v.attestation.text}\" <- {ev}")
        return 0
    print(f"claim-evidence-gate: FAIL -- {sum(not v.admissible for v in verdicts)} of "
          f"{len(verdicts)} attestation(s) lack admissible independent evidence.")
    for v in verdicts:
        if v.admissible:
            continue
        print(f"  violation: \"{v.attestation.text}\"")
        for reason in v.reasons:
            print(f"    - {reason}")
    print("Remediation: cite executable evidence (an existing test path, a CI run id) "
          "or an independent seat review -- or soften the claim. "
          "Internal repetition is not independent corroboration.")
    return 1


def _read_body(args) -> str:
    if args.body_env:
        return os.environ.get(args.body_env, "")
    if args.body_file:
        try:
            with open(args.body_file, encoding="utf-8") as fh:
                return fh.read()
        except OSError as exc:
            print(f"claim-evidence-gate: FATAL -- cannot read body file: {exc}", file=sys.stderr)
            sys.exit(2)
    return args.body or ""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="PR-body caller for the claim-evidence gate.")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--body", default="", help="PR body text directly")
    src.add_argument("--body-file", help="path to a file holding the PR body")
    src.add_argument("--body-env", help="env var holding the PR body")
    parser.add_argument("--seat", default="", help="author seat override (e.g. 'Naya 5')")
    parser.add_argument("--repo", default=".", help="repo root for test-path existence checks")
    args = parser.parse_args(argv)

    body = _read_body(args)
    result = scan(body, author_seat=normalize_seat(args.seat), repo_root=args.repo)
    return report(result)


if __name__ == "__main__":
    sys.exit(main())
