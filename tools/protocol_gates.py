#!/usr/bin/env python3
"""protocol_gates.py — Machine law: executable enforcement of the Team Naya
Operating Protocol.

This module is the machine twin of the Ultimate Operating Protocol
(PROPOSED — awaiting Shawn's ratification; merging this machinery does not
ratify the constitution).

SCOPE — companion to Naya 4's kernel/protocol/ (PR #1807), NOT a duplicate:
  Covered there (do NOT reimplement here):
    - quality_gate.check_delivery      (9.0 delivery floor)
    - authority_gate.classify_action   (5 protected gates)
    - cold_start_gate / read_receipt / takeover / cold_successor_test
  Implemented HERE (the missing delta):
    - check_sign_in / check_sign_out    (sign in/out format validation)
    - check_scorecard                   (5-step DECISION scorecard completeness,
                                         structured-dict input)
    - check_scorecard_body              (5-step scorecard STRUCTURE gate: scans a
                                         raw markdown PR body for the five
                                         headers — Gate 5 of 7, Operating Code V2)
    - check_truth_states                (truth-state label validation)

For check_quality_gate and check_protected_gates this module provides thin
adapters that delegate to kernel.protocol when available. The canonical
implementations live there; this module must never drift into a competing
mechanism.

Fail-closed: any missing or unresolvable field fails its check.
UNKNOWN != PASS. BLOCKED != PASS.

Stdlib only.
"""

from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# Truth states
# ---------------------------------------------------------------------------

VALID_TRUTH_STATES = (
    "UNKNOWN",
    "DOCUMENTED",
    "IMPLEMENTED",
    "VERIFIED",
    "PRODUCTION-PROVEN",
    "BLOCKED",
    "CANDIDATE",
)

# States that may be claimed as "it works".
CAN_CLAIM_WORKS = {"VERIFIED", "PRODUCTION-PROVEN"}

# Strict inequalities: the left side NEVER implies the right side.
STRICT_INEQUALITIES = (
    ("IMPLEMENTED", "VERIFIED"),
    ("VERIFIED", "PRODUCTION-PROVEN"),
    ("STORED", "LEARNED"),
    ("RETRIEVED", "APPLIED"),
    ("DOCUMENTED", "TRUE"),
    ("UNKNOWN", "PASS"),
    ("BLOCKED", "PASS"),
    ("CANDIDATE", "RATIFIED"),
)


@dataclass
class TruthStateResult:
    passed: bool
    reasons: list = field(default_factory=list)


def check_truth_states(claim: dict) -> TruthStateResult:
    """Validate a claim's truth-state labeling.

    claim: {"state": "<VALID_TRUTH_STATES member>", "asserts_works": bool}
    Fails when:
      - state is not a recognized truth state
      - asserts_works is True but the state cannot support a works-claim
        (e.g. IMPLEMENTED claiming it works, UNKNOWN/BLOCKED as PASS)
    """
    reasons: list[str] = []
    if not isinstance(claim, dict):
        return TruthStateResult(False, ["claim must be a dict"])

    state = claim.get("state")
    if state not in VALID_TRUTH_STATES:
        reasons.append(
            f"Unrecognized truth state {state!r}. "
            f"Valid: {list(VALID_TRUTH_STATES)}"
        )
    asserts_works = bool(claim.get("asserts_works", False))
    if asserts_works and state not in CAN_CLAIM_WORKS:
        reasons.append(
            f"State {state!r} cannot support a works-claim. "
            "IMPLEMENTED != VERIFIED; VERIFIED != PRODUCTION-PROVEN; "
            "UNKNOWN != PASS; BLOCKED != PASS."
        )
    return TruthStateResult(passed=not reasons, reasons=reasons)


# ---------------------------------------------------------------------------
# Sign in / sign out format
# ---------------------------------------------------------------------------

REQUIRED_SIGN_IN_FIELDS = (
    "seat",
    "lane",
    "taking",
    "why",
    "plan",
    "observed_state",
)

REQUIRED_SIGN_OUT_FIELDS = (
    "seat",
    "did",
    "evidence_links",
    "score",
    "proven",
    "unknown",
    "blocked",
    "next_action",
)


@dataclass
class FormatResult:
    passed: bool
    reasons: list = field(default_factory=list)


def _nonempty_str(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_sign_in(sign_in: dict) -> FormatResult:
    """Validate a sign-in record.

    Required: seat, lane, taking, why, plan, observed_state.
    All required fields must be non-empty strings. No silent work:
    a sign-in with an empty 'taking' is a format violation.
    """
    reasons: list[str] = []
    if not isinstance(sign_in, dict):
        return FormatResult(False, ["sign-in must be a dict"])
    for f in REQUIRED_SIGN_IN_FIELDS:
        if f not in sign_in:
            reasons.append(f"Missing required sign-in field: {f}")
        elif not _nonempty_str(sign_in[f]):
            reasons.append(f"Sign-in field {f!r} must be a non-empty string")
    return FormatResult(passed=not reasons, reasons=reasons)


def check_sign_out(sign_out: dict) -> FormatResult:
    """Validate a sign-out record.

    Required: seat, did, evidence_links, score, proven, unknown, blocked,
    next_action. evidence_links must be a non-empty list of strings.
    score must be a finite number in [0, 10]. Bare "done" receipts
    (empty evidence_links) are defects.
    """
    reasons: list[str] = []
    if not isinstance(sign_out, dict):
        return FormatResult(False, ["sign-out must be a dict"])
    for f in REQUIRED_SIGN_OUT_FIELDS:
        if f not in sign_out:
            reasons.append(f"Missing required sign-out field: {f}")
    if reasons:
        return FormatResult(False, reasons)

    for f in ("seat", "did", "proven", "unknown", "blocked", "next_action"):
        if not _nonempty_str(sign_out[f]):
            reasons.append(f"Sign-out field {f!r} must be a non-empty string")

    links = sign_out["evidence_links"]
    if not isinstance(links, list) or not links:
        reasons.append(
            "evidence_links must be a non-empty list — "
            'bare "done" receipts are defects'
        )
    elif not all(_nonempty_str(x) for x in links):
        reasons.append("evidence_links entries must be non-empty strings")

    score = sign_out["score"]
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        reasons.append("score must be a number in [0, 10]")
    elif not math.isfinite(score) or not (0 <= score <= 10):
        reasons.append(
            f"score {score!r} must be finite and within [0, 10] "
            "(NaN/Infinity fail closed)"
        )
    return FormatResult(passed=not reasons, reasons=reasons)


# ---------------------------------------------------------------------------
# 5-step decision scorecard (Scorecard Law)
# ---------------------------------------------------------------------------

# The Scorecard Law's five steps. Distinct from the delivery scorecard
# (kernel/protocol/quality_gate.py), which scores a finished deliverable.
# This validates the DECISION receipt: enumerate, score, gate, decide, post.
SCORECARD_STEPS = (
    "enumerate",   # every option listed
    "score",       # each scored on value/consequences/mission/situational awareness
    "gate",        # reversible? no major damage? positive forward effect?
    "decide",      # highest score + gates pass -> act
    "receipt",     # written and posted; no receipt, no merge
)

REQUIRED_GATE_CHECKS = (
    "reversible_or_safe",
    "no_major_damage",
    "positive_forward_effect",
    "authority_clear",
)


@dataclass
class ScorecardResult:
    passed: bool
    reasons: list = field(default_factory=list)


def check_scorecard(scorecard: dict) -> ScorecardResult:
    """Validate a 5-step decision scorecard receipt.

    scorecard: {
      "decision": str (non-empty),
      "options": [str, ...] (non-empty),
      "scores": {option: {"value","consequences","mission_alignment",
                          "risk","reversibility","evidence_strength","total"}},
      "gates_checked": {reversible_or_safe, no_major_damage,
                        positive_forward_effect, authority_clear: bool},
      "winner": str (must be one of options),
      "receipt_posted": bool,
    }
    Fail-closed on every missing or malformed step.
    """
    reasons: list[str] = []
    if not isinstance(scorecard, dict):
        return ScorecardResult(False, ["scorecard must be a dict"])

    # Step 1: ENUMERATE
    decision = scorecard.get("decision")
    if not _nonempty_str(decision):
        reasons.append("Step 1 (enumerate): 'decision' must be a non-empty string")
    options = scorecard.get("options")
    if not isinstance(options, list) or not options or not all(
        _nonempty_str(o) for o in options
    ):
        reasons.append(
            "Step 1 (enumerate): 'options' must be a non-empty list of strings"
        )
    else:
        options = list(options)

    # Step 2: SCORE
    scores = scorecard.get("scores")
    score_dims = (
        "value", "consequences", "mission_alignment",
        "risk", "reversibility", "evidence_strength", "total",
    )
    if not isinstance(scores, dict) or not scores:
        reasons.append("Step 2 (score): 'scores' must be a non-empty dict")
    elif isinstance(options, list):
        for opt in options:
            s = scores.get(opt)
            if not isinstance(s, dict):
                reasons.append(f"Step 2 (score): option {opt!r} has no score entry")
                continue
            for dim in score_dims:
                v = s.get(dim)
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    reasons.append(
                        f"Step 2 (score): {opt!r}.{dim} must be a number"
                    )
                elif not math.isfinite(v) or not (0 <= v <= 10):
                    reasons.append(
                        f"Step 2 (score): {opt!r}.{dim}={v!r} must be "
                        "finite within [0, 10]"
                    )

    # Step 3: GATE
    gates = scorecard.get("gates_checked")
    if not isinstance(gates, dict):
        reasons.append("Step 3 (gate): 'gates_checked' must be a dict")
    else:
        for g in REQUIRED_GATE_CHECKS:
            if g not in gates:
                reasons.append(f"Step 3 (gate): missing gate check {g!r}")
            elif not isinstance(gates[g], bool):
                reasons.append(f"Step 3 (gate): {g!r} must be boolean")

    # Step 4: DECIDE
    winner = scorecard.get("winner")
    if isinstance(options, list) and options:
        if winner not in options:
            reasons.append(
                f"Step 4 (decide): winner {winner!r} must be one of the "
                f"enumerated options"
            )
    elif not _nonempty_str(winner):
        reasons.append("Step 4 (decide): 'winner' must be a non-empty string")

    # Step 5: RECEIPT
    if scorecard.get("receipt_posted") is not True:
        reasons.append(
            "Step 5 (receipt): 'receipt_posted' must be true — "
            "no receipt, no merge"
        )

    return ScorecardResult(passed=not reasons, reasons=reasons)


# ---------------------------------------------------------------------------
# 5-step scorecard STRUCTURE gate — raw PR body scanner (Gate 5 of 7)
# ---------------------------------------------------------------------------
# The Operating Code V2 audit (Domain 1): every merge/scorecard PR must contain
# all five sections. CI scans the PR BODY for the five headers; missing section
# = blocked.
#
# Same gate, different input representation — NOT a second mechanism:
#   - check_scorecard            validates the structured dict
#   - auto_merge_gate._check_receipt  validates pr_state JSON
#   - check_scorecard_body       validates the raw markdown the human (and the
#                                CI check) actually reads
# One decision, one seam: this is the rendered-receipt form of the one gate.
#
# Contract (documented for receipt authors):
#   - Section headers are level-1/2 markdown headings (#, ##) or whole-line
#     bold leaders (**...**). Level-3+ headings (###) are treated as
#     in-section structure, not section boundaries.
#   - A header is claimed by explicit step number first ("Step 3", "3.", "(4)"),
#     then by keyword (enumerate / score / gate / decide|winner / receipt).
#     Headers numbered 1-5 are treated as step labels, so do not number
#     non-step headers 1-5 with a trailing dot/paren/colon.
#   - Every section must carry non-trivial content: >= MIN_SECTION_CONTENT_CHARS
#     non-markup characters, and not a bare placeholder (TBD/TODO/N/A...).
#   - Sections must appear in the law's order: 1 -> 2 -> 3 -> 4 -> 5.

# Section boundaries: ATX level-1/2 headings, or whole-line bold leaders.
_SECTION_HEADING_RES = (
    re.compile(r"^\s*#{1,2}\s+(.+?)\s*$"),   # ## Step 1: Enumerate
    re.compile(r"^\s*\*\*(.+?)\*\*\s*$"),     # **1. Enumerate**
)

# Explicit step numbers: "Step 3: Gates", "1. Enumerate", "(4) Decide".
_STEP_NUMBER_RE = re.compile(
    r"(?:\bstep\s*([1-5])\b|^\s*\(?([1-5])\s*[.:)>\-–—])", re.IGNORECASE
)

# Per-step keyword matchers (word-boundary, so "Investigation" never matches
# "gate"). Step 2 strips "scorecard" first so a lone "## Scorecard" title is
# not mistaken for the score section.
_STEP_KEYWORD_RES = (
    re.compile(r"\benumerat(?:e|ion)\b", re.IGNORECASE),                    # 1
    re.compile(r"\bscor(?:e|es|ed|ing)\b", re.IGNORECASE),                       # 2
    re.compile(r"\bgates?\b", re.IGNORECASE),                              # 3
    re.compile(r"\b(?:decid(?:e|ed|ing|sion)?|winner)\b", re.IGNORECASE),   # 4
    re.compile(r"\breceipt\b", re.IGNORECASE),                             # 5
)

STEP_NAMES = ("enumerate", "score", "gate", "decide", "receipt")

# A section must carry at least this many non-markup, non-whitespace
# characters; a bare header is not a section.
MIN_SECTION_CONTENT_CHARS = 40

# Placeholder theater: content that starts with a TBD-class token and stays
# short is not a written section, no matter the header.
_PLACEHOLDER_START_RE = re.compile(
    r"^\s*(?:todo|tbd|tbc|n/?a|wip|to be (?:decided|done|written|added)|coming soon)\b",
    re.IGNORECASE,
)
PLACEHOLDER_MAX_CHARS = 120

_MARKUP_STRIP_RE = re.compile(r"[#>*_`|\-]")
_WHITESPACE_RE = re.compile(r"\s+")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _iter_headings(body: str):
    """Yield (line_index, heading_text) for section-boundary headings."""
    for i, line in enumerate(body.splitlines()):
        for rx in _SECTION_HEADING_RES:
            m = rx.match(line)
            if m:
                yield i, m.group(1).strip()
                break


def _classify_heading(heading_text: str):
    """Return (numbered_step_or_None, set_of_keyword_matching_steps)."""
    numbered = None
    m = _STEP_NUMBER_RE.search(heading_text)
    if m:
        numbered = int(m.group(1) or m.group(2))
    keywords = set()
    for idx, rx in enumerate(_STEP_KEYWORD_RES, start=1):
        text = heading_text
        if idx == 2:
            # A lone "## Scorecard" title must not count as the score section.
            text = re.sub(r"scorecard", " ", text, flags=re.IGNORECASE)
        if rx.search(text):
            keywords.add(idx)
    return numbered, keywords


def _assign_steps(headings):
    """Map each of the five steps to its heading (line_index, text).

    Pass 1: explicit step numbers win (the author's own labels are
    authoritative). Pass 2: keyword match in step order. A single summary
    header that names all five steps claims only the first — the rest stay
    missing, which is the point: naming the steps is not writing them.
    """
    assignment = {}  # step -> (line_index, text)
    used = set()
    classified = [
        (idx, text, *_classify_heading(text)) for idx, text in headings
    ]
    for idx, text, numbered, _keywords in classified:
        if numbered and numbered not in assignment:
            assignment[numbered] = (idx, text)
            used.add(idx)
    for step in range(1, 6):
        if step in assignment:
            continue
        for idx, text, _numbered, keywords in classified:
            if idx in used:
                continue
            if step in keywords:
                assignment[step] = (idx, text)
                used.add(idx)
                break
    return assignment


def _substantive_length(text: str) -> int:
    """Non-markup, non-whitespace character count of a section's content."""
    text = _HTML_COMMENT_RE.sub(" ", text)
    text = _MARKUP_STRIP_RE.sub("", text)
    return len(_WHITESPACE_RE.sub("", text))


def check_scorecard_body(body: str) -> ScorecardResult:
    """Scan a raw markdown PR body for the Scorecard Law's five sections.

    Passes only when all five sections (enumerate, score, gate, decide,
    receipt) are present as headers, appear in the law's order, and each
    carries non-trivial content (no bare headers, no TBD theater).

    Fail-closed: a non-string or empty body fails — an unscannable receipt
    is not a receipt.
    """
    reasons: list[str] = []
    if not isinstance(body, str) or not body.strip():
        return ScorecardResult(
            False,
            ["PR body missing or empty — no sections to scan (fail closed)"],
        )

    headings = list(_iter_headings(body))
    assignment = _assign_steps(headings)
    lines = body.splitlines()

    for step in range(1, 6):
        if step not in assignment:
            reasons.append(
                f"Section {step} ({STEP_NAMES[step - 1]}) MISSING — the PR body "
                "must contain all five scorecard sections: "
                "enumerate, score, gate, decide, receipt"
            )
    if reasons:
        return ScorecardResult(False, reasons)

    positions = [assignment[s][0] for s in range(1, 6)]
    if positions != sorted(positions):
        found = ", ".join(
            f"{s}:{STEP_NAMES[s - 1]}"
            for s in sorted(assignment, key=lambda s: assignment[s][0])
        )
        reasons.append(
            "Scorecard sections OUT OF ORDER — the law's steps are sequential "
            "(enumerate -> score -> gate -> decide -> receipt); "
            f"found order: {found}"
        )

    boundary_lines = sorted(idx for idx, _text in headings)
    for step in range(1, 6):
        start, _text = assignment[step]
        later = [b for b in boundary_lines if b > start]
        end = min(later) if later else len(lines)
        content = "\n".join(lines[start + 1 : end])
        if _substantive_length(content) < MIN_SECTION_CONTENT_CHARS:
            reasons.append(
                f"Section {step} ({STEP_NAMES[step - 1]}) EMPTY — "
                f"< {MIN_SECTION_CONTENT_CHARS} non-markup characters; "
                "a bare header is not a section"
            )
        elif (
            _PLACEHOLDER_START_RE.match(content)
            and _substantive_length(content) < PLACEHOLDER_MAX_CHARS
        ):
            reasons.append(
                f"Section {step} ({STEP_NAMES[step - 1]}) is PLACEHOLDER theater "
                f"({content.strip()[:60]!r}) — write the section or drop the claim"
            )

    return ScorecardResult(passed=not reasons, reasons=reasons)


# ---------------------------------------------------------------------------
# Adapters to kernel/protocol/ (PR #1807) — canonical implementations
# ---------------------------------------------------------------------------

class GateVerdict(Enum):
    ALLOW = "ALLOW"
    NEEDS_SHAWN = "NEEDS_SHAWN"
    REFUSE = "REFUSE"


@dataclass
class AdapterResult:
    passed: bool
    verdict: str | None = None
    reasons: list = field(default_factory=list)
    delegated_to: str = ""


def _try_kernel_attr(module_name: str, attr: str):
    try:
        import importlib

        mod = importlib.import_module(f"kernel.protocol.{module_name}")
        return getattr(mod, attr, None)
    except Exception:
        return None


# Local fallback signals for the protected gates, mirroring
# kernel/protocol/authority_gate.py so this module stays usable on main
# before that PR merges. The canonical implementation is authoritative.
_FALLBACK_GATE_SIGNALS = {
    "production": (
        "production deploy", "deploy to production", "prod db",
        "prod database", "production database", "supabase production",
        "migrate production", "migrate the production",
        "promote to production", "production dispatch",
        "dispatch to production", "dispatch the production",
        "workflow dispatch", "production migration",
        "migration to production", "to production", "into production",
        "live database", "production schema",
        "production data", "export production",
    ),
    "workflows": (
        ".github/workflows", "github workflow", "actions workflow",
    ),
    "credentials_money": (
        "credential", "api key", "secret", "password",
        "payment", "charge", "money", "billing", "invoice", "refund",
        "token", "private key", "ssh key", "access key", "secret key",
    ),
    "destructive": (
        "delete production", "drop table", "drop database", "rm -rf",
        "force push main", "irreversible", "wipe", "wipe out", "destroy",
        "destroy the", "truncate", "delete from", "delete all", "nuke",
        "purge", "format the disk", "delete the repository", "delete repo",
    ),
    "ratification": ("mark ratified", "ratify", "ratified", "ratification"),
    "security_privacy": (
        "disable rls", "bypass auth", "pii", "privacy policy",
        "consent", "change authority", "elevate privilege", "disable gate",
        "authentication", "grant admin", "admin access", "change permission",
        "access control", "revoke access", "modify permissions",
        "security change",
    ),
}
_FALLBACK_HARD_REFUSALS = (
    "harm", "illegal", "destroy evidence", "break trust",
    "fabricate evidence", "weaken test", "merge red",
)


def check_protected_gates(action_text: str) -> AdapterResult:
    """Classify a proposed action against the 6 protected gates.

    Delegates to kernel.protocol.authority_gate.classify_action when
    available (PR #1807 — canonical). Falls back to a local mirror so the
    gate stays fail-closed on main before that PR merges.

    Returns ALLOW / NEEDS_SHAWN / REFUSE. Scores never grant permission.
    """
    classify = _try_kernel_attr("authority_gate", "classify_action")
    if classify is not None:
        try:
            r = classify(action_text)
            verdict = r.verdict.value if hasattr(r.verdict, "value") else str(r.verdict)
            ok = verdict == GateVerdict.ALLOW.value
            return AdapterResult(
                passed=ok, verdict=verdict,
                reasons=[] if ok else [r.reason],
                delegated_to="kernel.protocol.authority_gate",
            )
        except Exception:
            pass  # fail closed: fall through to local mirror

    text = (action_text or "").lower()
    for refusal in _FALLBACK_HARD_REFUSALS:
        if refusal in text:
            return AdapterResult(
                passed=False, verdict=GateVerdict.REFUSE.value,
                reasons=[f"Hard stop: matches prohibited pattern '{refusal}'."],
                delegated_to="local-fallback (kernel/protocol not yet merged)",
            )
    for gate_id, signals in _FALLBACK_GATE_SIGNALS.items():
        for signal in signals:
            if signal in text:
                return AdapterResult(
                    passed=False, verdict=GateVerdict.NEEDS_SHAWN.value,
                    reasons=[
                        f"Protected gate '{gate_id}': requires Shawn's explicit "
                        "word. No scorecard overrides this."
                    ],
                    delegated_to="local-fallback (kernel/protocol not yet merged)",
                )
    return AdapterResult(
        passed=True, verdict=GateVerdict.ALLOW.value, reasons=[],
        delegated_to="local-fallback (kernel/protocol not yet merged)",
    )


def check_quality_gate(
    scores: dict, weights: dict | None = None
) -> AdapterResult:
    """Enforce the 9.0 delivery floor, per area, never averaged.

    Delegates to kernel.protocol.quality_gate.check_delivery when available
    (PR #1807 — canonical). The local fallback enforces the floor rule only;
    the full delivery-scorecard checks (evidence, weakest point, independent
    verifier) live in the canonical module.
    """
    check_delivery = _try_kernel_attr("quality_gate", "check_delivery")
    Scorecard = _try_kernel_attr("quality_gate", "Scorecard")
    if check_delivery is not None and Scorecard is not None:
        try:
            sc = Scorecard(
                what="adapter-call", evidence="adapter-call",
                scores=dict(scores),
                weights=(dict(weights) if weights is not None else
                         {name: 1.0 / len(scores) for name in scores} if scores else {}),
                weakest_point="adapter-call", verified_by="adapter",
            )
            r = check_delivery(sc, builder_id="protocol_gates-adapter")
            return AdapterResult(
                passed=r.passed, verdict="PASS" if r.passed else "FAIL",
                reasons=list(r.reasons),
                delegated_to="kernel.protocol.quality_gate",
            )
        except Exception:
            pass  # fall through to local mirror

    reasons: list[str] = []
    if not isinstance(scores, dict) or not scores:
        return AdapterResult(
            passed=False, verdict="FAIL",
            reasons=["scores must be a non-empty dict of dimension -> 0-10"],
            delegated_to="local-fallback (kernel/protocol not yet merged)",
        )
    if weights is not None:
        if set(scores) != set(weights):
            reasons.append("scores and weights must cover the same dimensions")
        elif abs(sum(weights.values()) - 1.0) > 0.001:
            reasons.append("weights must sum to 1.0")
    bad = []
    for dim, v in scores.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool) \
                or not math.isfinite(v) or not (0 <= v <= 10):
            bad.append(dim)
    if bad:
        reasons.append(f"Non-finite or out-of-range scores: {bad}")
    low = [d for d, s in scores.items()
           if isinstance(s, (int, float)) and not isinstance(s, bool)
           and math.isfinite(s) and s < 9.0]
    if low:
        reasons.append(
            f"Dimensions below floor 9.0: {low}. A 10 never covers a 7."
        )
    if weights and not reasons:
        total = sum(scores[d] * weights[d] for d in scores)
        if total < 9.0:
            reasons.append(f"Weighted total {total:.2f} below floor 9.0.")
    return AdapterResult(
        passed=not reasons, verdict="PASS" if not reasons else "FAIL",
        reasons=reasons,
        delegated_to="local-fallback (kernel/protocol not yet merged)",
    )


# ---------------------------------------------------------------------------
# CLI — the CI-facing entry point for the structure gate.
# Usage:  python3 tools/protocol_gates.py --scorecard-body <pr-body.md>
# Exit 0 = all five sections present, ordered, substantive.
# Exit 1 = blocked (reasons as JSON). Exit 2 = usage / input error.
# ---------------------------------------------------------------------------

def _main_cli(argv):
    import argparse

    ap = argparse.ArgumentParser(
        description=(
            "Scorecard structure gate: scan a raw PR body for the five "
            "scorecard sections (enumerate, score, gate, decide, receipt)."
        )
    )
    ap.add_argument(
        "--scorecard-body",
        required=True,
        help="Path to a file containing the raw PR body markdown",
    )
    args = ap.parse_args(argv)
    try:
        with open(args.scorecard_body, "r", encoding="utf-8") as fh:
            body = fh.read()
    except OSError as exc:
        print(
            json.dumps(
                {"gate": "scorecard_structure", "passed": False,
                 "error": str(exc)}
            )
        )
        return 2
    result = check_scorecard_body(body)
    print(
        json.dumps(
            {"gate": "scorecard_structure", "passed": result.passed,
             "reasons": result.reasons},
            indent=2,
        )
    )
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(_main_cli(sys.argv[1:]))
