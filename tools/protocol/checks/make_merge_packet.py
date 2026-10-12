#!/usr/bin/env python3
"""make_merge_packet.py — assemble the Delegated-Merge-Authority merge packet.

The merge path (tools/protocol/checks/merge_gate.py, 2026-10-12) refuses
every main-ref update without a passing `--packet <json-file>`. This script
assembles that packet from what the merge lane already has: the #2154
intent / scorecard / IV post bodies (or their comment ids), the branch
name, the builder seat, the score, and the evidence links.

FAIL-CLOSED, same as the gate:
  * Explicit flags always win over derivation.
  * A field is DERIVED only from text the supplied post bodies state
    plainly, matched by conservative patterns, unambiguous. Anything the
    posts do not say in plain words is NOT guessed — it is REFUSED, with
    the missing field named (exit 1). Never fabricate a field.
  * The assembled packet is run through the REAL check
    (checks.merge_authority.check — the same function the gate calls). If
    the check fails, the producer refuses with the check's own reasons and
    names the input that fixes each one. A refused producer is not a broken
    producer; it is the gate doing its job one step earlier.
  * Some assertions can ONLY be made by the merging seat and are never
    derived: branch, seat, evidence_backed, value_calculus_run,
    report_planned. They have explicit flags and no defaults.

The nine required fields (the gate pins target="main" itself):
  branch, seat, tests_green, test_evidence,
  self_scorecard {score, evidence_backed, value_calculus_run},
  independent_validator, posted_to_1354, team_objections,
  post_merge_report_planned.

Usage:
    python3 make_merge_packet.py --branch <name> --seat "<seat>" \\
        --score 9.2 --tests-green --test-evidence "<ref>" \\
        --evidence-backed --value-calculus-run \\
        --independent-validator "<seat>" --feed-comment <id> \\
        --team-objections 0 --report-planned \\
        [--scorecard-body-file F] [--iv-body-file F] [--intent-body-file F]
        [--out packet.json]

Exit codes: 0 = packet emitted; 1 = refused (named missing/invalid fields);
2 = usage error.

What this does NOT claim (D32):
  * The producer assembles the CLAIM. It cannot verify that a cited
    --feed-comment id is real, on #2154, or says what the operator says it
    says; it cannot verify the green claim or the score happened. The
    packet makes the claim falsifiable (named posts, named seats,
    reference-shaped evidence); the independent validator, the team
    consensus on the live feed, and the #2154 receipts are what make it
    true. A packet is a form, not a proof.
  * Explicit operator assertions (--seat, --tests-green, --evidence-backed,
    --value-calculus-run, --report-planned, --team-objections) are the
    merging seat's word. The producer checks them against the real check's
    rules; it does not check them against reality.
  * Derivation is conservative on purpose: real posts often do NOT state a
    field plainly, and then the producer refuses and names the field. That
    refusal is the feature — the merge lane supplies the explicit flag.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Resolve the `checks` package (merge_authority.py) the same way merge_gate.py
# does: the repo copy sits beside this file; the live operator copy resolves
# the canonical clone; NAYAPOWER_REPO overrides everything.
_here = Path(__file__).resolve()


def _checks_roots():
    roots = []
    env = os.environ.get("NAYAPOWER_REPO")
    if env:
        roots.append(Path(env) / "tools" / "protocol")
    roots.append(Path.home() / "workspace" / "nayapower-work" / "tools" / "protocol")
    roots.append(_here.parents[1])  # tools/protocol when this file is checks/
    return roots


for _root in _checks_roots():
    if (_root / "checks" / "merge_authority.py").is_file():
        sys.path.insert(0, str(_root))
        break

try:
    from checks import merge_authority  # noqa: E402
except Exception as e:  # fail closed: without the check there is no producer
    print(f"make_merge_packet: cannot load checks.merge_authority ({e}); "
          "refusing — a producer that cannot verify its own packet is "
          "worse than no producer.", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Derivation patterns — conservative by design. A pattern fires only when
# the post states the fact in plain words. Ambiguity (two different
# candidates) is a refusal, not a guess.
# ---------------------------------------------------------------------------

# score: JSON-ish "score": 9.2, or 9.2/10. Derivation admits any plainly
# stated score; the REAL check enforces the 9.0 bar below, loudly. A
# derived sub-9.0 score is a refusal, not a fabrication — the packet is
# never assembled, so nothing slips through.
_SCORE_PATTERNS = (
    re.compile(r'"score"\s*:\s*(\d{1,2}(?:\.\d+)?)'),
    re.compile(r'\b(\d{1,2}(?:\.\d+)?)\s*/\s*10\b'),
)

# validator: the IV post names the seat that independently validated.
_VALIDATOR_PATTERNS = (
    re.compile(r'independent[ _-]?validator\s*[:=]\s*([^\n,;()]{1,60})', re.I),
    re.compile(r'\bvalidated by\s+([^\n,;()]{1,60})', re.I),
    # "IV seat: X" only — a bare "IV: <verdict text>" is not a seat claim.
    re.compile(r'\bIV\s+seat\s*[:=]\s*([^\n,;()]{1,60})', re.I),
    re.compile(r'different[ _-]?seat\s*[:=]\s*([^\n,;()]{1,60})', re.I),
    re.compile(r'\bvalidator\s*[:=]\s*([^\n,;()]{1,60})', re.I),
)

# A derived validator must look like a seat ("Naya Epsilon", "Naya 5",
# "Coda 1", "Codex") — otherwise a captured fragment like "VERDICT A"
# becomes a fabricated validator. Explicit --independent-validator values
# are the operator's own assertion and skip this shape check.
_SEAT_SHAPE = re.compile(r'^(?:naya|coda)\s+[a-z0-9]+$|^codex$', re.I)

# tests_green: an explicit green claim WITH counts, on one line. A bare
# "green" with no counts is a claim without proof — not enough to derive.
# Patterns stay line-local: a green claim in one sentence must not borrow
# counts from another.
_GREEN_PATTERNS = (
    re.compile(r'\b(\d+)\s*/\s*(\d+)\s+(?:tests?|suites?|probes?|checks?)\s+green\b', re.I),
    re.compile(r'\b(\d+)\s+passed\b[^\n]*\bgreen\b', re.I),
    re.compile(r'\bgreen\b[^\n]*\b(\d+)\s+passed\b', re.I),
)

# team_objections: plain-words "no objections" -> 0; an explicit count is
# honored as-is (a nonzero count refuses the whole packet below).
_NO_OBJECTIONS_PATTERNS = (
    re.compile(r'\bno\s+(?:team\s+)?objections?\b', re.I),
    re.compile(r'\bno\s+seat\s+objects?\b', re.I),
)
_OBJECTIONS_COUNT_PATTERN = re.compile(r'\bobjections?\s*[:=]\s*(\d+)\b', re.I)

_URL_PATTERN = re.compile(r'https?://\S+')


def _snip(text: str, n: int = 80) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1] + "…"


def _read_bodies(paths) -> list[tuple[str, str]]:
    """Return [(label, text)] for each readable body file."""
    out = []
    for label, path in paths:
        if not path:
            continue
        try:
            out.append((label, Path(path).read_text()))
        except Exception as e:
            print(f"make_merge_packet: cannot read {label} file {path}: {e}",
                  file=sys.stderr)
            sys.exit(2)
    return out


def _distinct(values: list[str]) -> list[str]:
    seen: list[str] = []
    for v in values:
        v = v.strip()
        if v and v not in seen:
            seen.append(v)
    return seen


class Refusal(Exception):
    """A named refusal: (field, plain-words reason, how to supply it)."""

    def __init__(self, field: str, reason: str, fix: str):
        self.field = field
        self.reason = reason
        self.fix = fix
        super().__init__(f"{field}: {reason}")


# ---------------------------------------------------------------------------
# Derivation — each returns (value, provenance) or raises Refusal.
# ---------------------------------------------------------------------------

def derive_score(explicit, bodies) -> tuple[float, str]:
    cands = _score_candidates(bodies)
    if explicit is not None:
        for c in cands:
            if abs(float(c) - explicit) > 1e-9:
                print(f"make_merge_packet: note: explicit --score {explicit} "
                      f"overrides post-body score {c} — confirm this is the "
                      f"builder's self-scorecard score", file=sys.stderr)
        return explicit, "explicit --score"
    if not cands:
        raise Refusal(
            "self_scorecard.score",
            "no score found in the supplied post bodies",
            "supply --score <9.0-10.0>, e.g. the builder's scorecard score",
        )
    if len(cands) > 1:
        raise Refusal(
            "self_scorecard.score",
            f"ambiguous scores in post bodies: {', '.join(cands)} — refusing to pick",
            "supply --score explicitly (the builder's self-scorecard score, not the IV's)",
        )
    try:
        value = float(cands[0])
    except ValueError:
        raise Refusal("self_scorecard.score",
                      f"unparseable score {cands[0]!r}",
                      "supply --score explicitly")
    return value, f"derived from post body ({cands[0]})"


def _score_candidates(bodies) -> list[str]:
    cands: list[str] = []
    # scorecard body first (the builder's own scorecard is authoritative),
    # then IV body, then intent body, then generic.
    order = {"scorecard": 0, "iv": 1, "intent": 2, "body": 3}
    for label, text in sorted(bodies, key=lambda b: order.get(b[0], 9)):
        for pat in _SCORE_PATTERNS:
            cands.extend(pat.findall(text))
    return _distinct(cands)


def derive_tests_green(explicit: bool, bodies) -> tuple[bool, str]:
    if explicit:
        return True, "explicit --tests-green"
    for label, text in bodies:
        for line in text.splitlines():
            if _FAIL_ON_SAME_LINE.search(line):
                # A line that also names failures is not a green line — the
                # green claim is ambiguous, so nothing is derived from it.
                continue
            for pat in _GREEN_PATTERNS:
                m = pat.search(line)
                if m:
                    return True, f"derived from {label} body ({_snip(m.group(0))})"
    raise Refusal(
        "tests_green",
        "no explicit green claim with test counts in the post bodies",
        "assert --tests-green yourself, or supply a post body stating "
        "counts (e.g. '15/15 tests green')",
    )


_FAIL_ON_SAME_LINE = re.compile(r"\b\d+\s+fail", re.I)


def derive_test_evidence(explicit, bodies) -> tuple[str, str]:
    if explicit:
        return explicit.strip(), "explicit --test-evidence"
    for label, text in bodies:
        m = _URL_PATTERN.search(text)
        if m:
            return m.group(0).rstrip(").,"), f"derived from {label} body (URL)"
    for label, text in bodies:
        for line in text.splitlines():
            line = line.strip()
            if len(line) > 10 and merge_authority._is_evidence_shaped(line):
                return line, f"derived from {label} body ({_snip(line)})"
    raise Refusal(
        "test_evidence",
        "no reference-shaped evidence (URL, run/job id, counts transcript, "
        "artifact path) in the post bodies",
        "supply --test-evidence with a CI run, command transcript, or "
        "artifact a validator can resolve",
    )


def derive_validator(explicit, seat: str, bodies) -> tuple[str, str]:
    cands = _validator_candidates(bodies)
    if explicit:
        name = explicit.strip()
        for c in cands:
            if (merge_authority._seat_key(c) != merge_authority._seat_key(name)
                    and merge_authority._seat_key(c) != merge_authority._seat_key(seat)):
                print(f"make_merge_packet: note: explicit --independent-validator "
                      f"{name!r} overrides post-body candidate {c!r} — confirm "
                      f"this is the seat that ran the IV", file=sys.stderr)
        prov = "explicit --independent-validator"
    else:
        if not cands:
            raise Refusal(
                "independent_validator",
                "no validator seat named in the post bodies",
                "supply --independent-validator <seat> (the different seat "
                "that ran the IV)",
            )
        if len(cands) > 1:
            raise Refusal(
                "independent_validator",
                f"ambiguous validator seats: {', '.join(cands)} — refusing to pick",
                "supply --independent-validator explicitly",
            )
        name, prov = cands[0], "derived from post body"
    if merge_authority._seat_key(name) == merge_authority._seat_key(seat):
        raise Refusal(
            "independent_validator",
            f"{name!r} normalizes to the same seat as {seat!r} — "
            "self-validation is not independent validation",
            "name the DIFFERENT seat that ran the independent validation",
        )
    return name, prov


def _validator_candidates(bodies) -> list[str]:
    cands: list[str] = []
    order = {"iv": 0, "scorecard": 1, "intent": 2, "body": 3}
    for label, text in sorted(bodies, key=lambda b: order.get(b[0], 9)):
        for pat in _VALIDATOR_PATTERNS:
            cands.extend(m.strip(" .") for m in pat.findall(text))
    # Derived candidates must be seat-shaped; anything else is not a
    # seat claim and is ignored rather than guessed at.
    return _distinct([c for c in cands
                      if len(c) >= 2 and _SEAT_SHAPE.match(c)])


def derive_team_objections(explicit, bodies) -> tuple[int, str]:
    if explicit is not None:
        n, prov = explicit, "explicit --team-objections"
    else:
        n, prov = None, ""
        for label, text in bodies:
            if any(p.search(text) for p in _NO_OBJECTIONS_PATTERNS):
                n, prov = 0, f"derived from {label} body (plain-words 'no objections')"
                break
        if n is None:
            for label, text in bodies:
                m = _OBJECTIONS_COUNT_PATTERN.search(text)
                if m:
                    n, prov = int(m.group(1)), f"derived from {label} body (explicit count)"
                    break
    if n is None:
        raise Refusal(
            "team_objections",
            "no objection count stated in the post bodies",
            "supply --team-objections 0 (after confirming no seat objects "
            "on the live feed)",
        )
    if n > 0:
        raise Refusal(
            "team_objections",
            f"{n} objection(s) on the record — no packet can authorize this "
            "merge; it still needs Shawn's word",
            "resolve the objections on the team feed first",
        )
    return n, prov


def derive_feed_comments(explicit_ids) -> tuple[list[str], str]:
    ids: list[str] = []
    for raw in explicit_ids or []:
        raw = raw.strip()
        m = re.search(r'issuecomment-(\d+)', raw)
        ids.append(m.group(1) if m else raw)
    ids = _distinct(ids)
    for raw in ids:
        if not re.search(r"\d", raw):
            raise Refusal(
                "posted_to_1354",
                f"feed-comment {raw!r} is not shaped like a comment id — "
                "the packet names claims a validator must be able to "
                "resolve",
                "supply --feed-comment <comment-id or its URL>",
            )
    if not ids:
        raise Refusal(
            "posted_to_1354",
            "no live-feed post cited — the delegation requires intent + "
            "scorecard + validation posted on the team feed",
            "supply --feed-comment <comment-id or URL> (repeatable; the "
            "IV verdict post at minimum)",
        )
    return ids, "explicit --feed-comment"


# ---------------------------------------------------------------------------
# Assembly + verification through the real check.
# ---------------------------------------------------------------------------

_MISSING_INPUT_FOR_REASON = (
    ("branch missing", "branch", "--branch <name>"),
    ("seat unnamed", "seat", "--seat \"<merging seat>\""),
    ("tests_green is not true", "tests_green", "--tests-green"),
    ("test_evidence missing", "test_evidence", "--test-evidence \"<ref>\""),
    ("is not reference-shaped", "test_evidence", "--test-evidence \"<ref>\""),
    ("self_scorecard missing", "self_scorecard",
     "--score <n> --evidence-backed --value-calculus-run"),
    ("self_scorecard.score", "self_scorecard.score", "--score <9.0-10.0>"),
    ("evidence_backed is not true", "self_scorecard.evidence_backed",
     "--evidence-backed"),
    ("value_calculus_run is not true", "self_scorecard.value_calculus_run",
     "--value-calculus-run"),
    ("independent_validator", "independent_validator",
     "--independent-validator \"<different seat>\""),
    ("posted_to_1354", "posted_to_1354", "--feed-comment <id>"),
    ("team_objections", "team_objections", "--team-objections 0"),
    ("post_merge_report_planned", "post_merge_report_planned",
     "--report-planned"),
)


def map_reason_to_input(reason: str) -> tuple[str, str]:
    for needle, field, fix in _MISSING_INPUT_FOR_REASON:
        if needle in reason:
            return field, fix
    return "packet", "--help"


def assemble(args) -> tuple[dict, list[str]]:
    """Assemble the packet. Returns (packet, receipt_lines).

    Raises Refusal naming the missing field — never fabricates one.
    """
    bodies = _read_bodies([
        ("scorecard", args.scorecard_body_file),
        ("iv", args.iv_body_file),
        ("intent", args.intent_body_file),
    ] + [("body", p) for p in args.body_file or []])

    receipt: list[str] = []
    missing: list[Refusal] = []

    branch = (args.branch or "").strip()
    if not branch:
        missing.append(Refusal("branch", "not supplied",
                               "supply --branch <branch-name>"))
    seat = (args.seat or "").strip()
    if not seat:
        missing.append(Refusal("seat", "merging seat not supplied",
                               "supply --seat \"<seat>\" (never derived — "
                               "posts may name several seats)"))

    # Each derivation is independent: collect ALL missing fields before
    # refusing, so one run names everything the operator must supply.
    results: dict = {}
    for field, fn, fargs in (
        ("tests_green", derive_tests_green, (args.tests_green, bodies)),
        ("test_evidence", derive_test_evidence, (args.test_evidence, bodies)),
        ("self_scorecard.score", derive_score, (args.score, bodies)),
        ("independent_validator", derive_validator,
         (args.independent_validator, seat or "?", bodies)),
        ("team_objections", derive_team_objections,
         (args.team_objections, bodies)),
        ("posted_to_1354", derive_feed_comments, (args.feed_comment,)),
    ):
        try:
            results[field] = fn(*fargs)
        except Refusal as r:
            missing.append(r)

    if not args.evidence_backed:
        missing.append(Refusal(
            "self_scorecard.evidence_backed",
            "not asserted — never derived from prose",
            "supply --evidence-backed (the merging seat asserts the "
            "scorecard is evidence-backed)"))
    if not args.value_calculus_run:
        missing.append(Refusal(
            "self_scorecard.value_calculus_run",
            "not asserted — never derived from prose",
            "supply --value-calculus-run (the merging seat asserts the "
            "value calculus was run)"))
    if not args.report_planned:
        missing.append(Refusal(
            "post_merge_report_planned",
            "not asserted",
            "supply --report-planned (the merging seat commits to the "
            "post-merge report)"))

    if missing:
        raise _MultiRefusal(missing)

    score, score_prov = results["self_scorecard.score"]
    tests_green, green_prov = results["tests_green"]
    test_evidence, ev_prov = results["test_evidence"]
    validator, val_prov = results["independent_validator"]
    objections, obj_prov = results["team_objections"]
    feed_ids, feed_prov = results["posted_to_1354"]

    packet = {
        # target is pinned by the gate itself (merge_gate.enforce sets it);
        # the producer writes the same value so the packet is truthful
        # standalone too.
        "target": "main",
        "branch": branch,
        "seat": seat,
        "tests_green": tests_green,
        "test_evidence": test_evidence,
        "self_scorecard": {
            "score": score,
            "evidence_backed": True,
            "value_calculus_run": True,
        },
        "independent_validator": validator,
        "posted_to_1354": True,
        "team_objections": objections,
        "post_merge_report_planned": True,
        # Extra provenance the check ignores but the merge lane and the
        # ledger can audit: which live-feed posts this packet rests on.
        "feed_comments": feed_ids,
    }

    receipt = [
        f"branch: {branch} (explicit --branch)",
        f"seat: {seat} (explicit --seat)",
        f"tests_green: true ({green_prov})",
        f"test_evidence: {_snip(test_evidence)} ({ev_prov})",
        f"self_scorecard.score: {score} ({score_prov})",
        "self_scorecard.evidence_backed: true (explicit --evidence-backed)",
        "self_scorecard.value_calculus_run: true (explicit --value-calculus-run)",
        f"independent_validator: {validator} ({val_prov})",
        f"posted_to_1354: true ({feed_prov}: {', '.join(feed_ids)})",
        f"team_objections: {objections} ({obj_prov})",
        "post_merge_report_planned: true (explicit --report-planned)",
    ]
    return packet, receipt


class _MultiRefusal(Exception):
    def __init__(self, refusals: list[Refusal]):
        self.refusals = refusals
        super().__init__("; ".join(f"{r.field}: {r.reason}" for r in refusals))


def parse_argv(argv):
    p = argparse.ArgumentParser(
        description="Assemble the Delegated-Merge-Authority merge packet, "
                    "fail-closed. Refuses (exit 1) with named missing fields "
                    "rather than fabricating any.")
    p.add_argument("--branch", help="branch about to merge to main")
    p.add_argument("--seat", help="merging seat (never derived)")
    p.add_argument("--score", type=float,
                   help="self-scorecard score 9.0-10.0 (or derived from "
                        "the scorecard post body)")
    p.add_argument("--tests-green", action="store_true",
                   help="assert tests are green")
    p.add_argument("--test-evidence",
                   help="reference-shaped proof (or derived from post bodies)")
    p.add_argument("--evidence-backed", action="store_true",
                   help="assert the scorecard is evidence-backed")
    p.add_argument("--value-calculus-run", action="store_true",
                   help="assert the value calculus was run")
    p.add_argument("--independent-validator",
                   help="the DIFFERENT seat that ran the IV (or derived "
                        "from the IV post body)")
    p.add_argument("--feed-comment", action="append", default=[],
                   help="live-feed (#2154) comment id or URL evidencing the "
                        "posted intent/scorecard/validation; repeatable")
    p.add_argument("--team-objections", type=int, default=None,
                   help="objection count on the live feed (0 required)")
    p.add_argument("--report-planned", action="store_true",
                   help="commit to the post-merge report")
    p.add_argument("--scorecard-body-file",
                   help="builder's scorecard post body (score source)")
    p.add_argument("--iv-body-file",
                   help="IV verdict post body (validator source)")
    p.add_argument("--intent-body-file",
                   help="intent post body")
    p.add_argument("--body-file", action="append", default=[],
                   help="any other post body; repeatable")
    p.add_argument("--out",
                   help="write the packet JSON here (default: stdout)")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_argv(sys.argv[1:] if argv is None else argv)
    try:
        packet, receipt = assemble(args)
    except _MultiRefusal as e:
        print("PACKET REFUSED — nothing assembled, nothing fabricated:",
              file=sys.stderr)
        for r in e.refusals:
            print(f"  - missing/invalid field: {r.field}", file=sys.stderr)
            print(f"      reason: {r.reason}", file=sys.stderr)
            print(f"      fix: {r.fix}", file=sys.stderr)
        return 1
    except Refusal as e:  # pragma: no cover — assemble wraps in _MultiRefusal
        print(f"PACKET REFUSED — {e.field}: {e.reason} (fix: {e.fix})",
              file=sys.stderr)
        return 1

    # The final word belongs to the real check — the same function the gate
    # calls. If the packet would not pass the gate, it does not leave here.
    res = merge_authority.check(packet)
    if not res.get("pass"):
        print("PACKET REFUSED — the assembled packet FAILS the real check:",
              file=sys.stderr)
        for reason in res.get("reasons", ["packet did not pass"]):
            field, fix = map_reason_to_input(reason)
            print(f"  - {reason}", file=sys.stderr)
            print(f"      field: {field} | fix: {fix}", file=sys.stderr)
        return 1

    out = json.dumps(packet, indent=2)
    if args.out:
        Path(args.out).write_text(out + "\n")
    else:
        print(out)
    print("packet assembled and PASSED the real check — provenance:",
          file=sys.stderr)
    for line in receipt:
        print(f"  - {line}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
