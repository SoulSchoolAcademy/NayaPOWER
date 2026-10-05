#!/usr/bin/env python3
"""Enforcement predicate for FULL-AUTO-MERGE-V1, authorized under the supreme
SCORECARD-LAW-V1 (Shawn Vibert, verbal ratification 2026-10-05 ~06:05 PDT,
recorded #1354 comment 5995131455): "my law that supersedes all laws you must
scorecard everything."

The receipt IS the law's five steps:
  1. ENUMERATE every option
  2. SCORE each on value, consequences (pros/cons), mission/vision alignment,
     situational awareness
  3. GATE — reversible? no major damage? positive forward effect? (hard stops)
  4. DECIDE — highest score + gates pass → act; winner, strongest alternative,
     falsifier
  5. RECEIPT — written and posted; no receipt, no merge

Usage:
    python3 tools/auto_merge_gate.py <pr_state.json>

Reads a pr_state JSON object (see BRAIN/01-GOVERNANCE/0003-FULL-AUTO-MERGE-V1.ai.md),
evaluates every precondition of the Full Auto-Merge Law, and prints a verdict.

Exit code 0: may auto-merge.  Exit code 1: must NOT auto-merge (reasons printed).
Exit code 2: usage / input error.

Fail-closed: any missing or unresolvable field fails its precondition. UNKNOWN != PASS.

Stdlib only.
"""

import json
import sys
from datetime import datetime, timezone

LAW_ID = "FULL-AUTO-MERGE-V1"

# Tunable only through the law's amendment path (authority-model change).
MAX_EVIDENCE_AGE_SECONDS = 900

PROTECTED_PATH_PREFIXES = (
    ".github/workflows/",
    "CONSTITUTION/",
    "BRAIN/01-GOVERNANCE/",
    "GOVERNANCE/",
    "NAYA-ACTIVATION/",
)

# The receipt IS the Scorecard Law's five steps. Top-level envelope fields plus
# the five step objects; the predicate validates each step mechanically.
REQUIRED_RECEIPT_FIELDS = (
    "decision_id",
    "engine",
    "decided_at",
    "decided_by",
    # Five steps (SCORECARD-LAW-V1, 2026-10-05):
    "step1_enumerate",
    "step2_score",
    "step3_gate",
    "step4_decide",
    "step5_receipt",
    # H1 anti-theater / rigor (Shawn hardening, 2026-10-04):
    "rigor_tier",
    # H4 scope fields:
    "lane",
    "owner_seat",
    "author_seat",
    "author_lane",
)

# Step 2 scoring dimensions — the law's four, in the law's words.
SCORE_DIMENSIONS = (
    "value",
    "consequences",
    "mission_vision_alignment",
    "situational_awareness",
)

# Step 3 hard stops — no score overrides a failed gate.
GATE_FIELDS = (
    "reversible",
    "no_major_damage",
    "positive_forward_effect",
)

FULL_TIER_EXTRA_FIELDS = (
    "named_risks",
    "rollback_plan",
    "second_seat_ack_comment_id",
)


def _parse_ts(value):
    """Parse an ISO-8601 timestamp; return aware datetime or None."""
    if not isinstance(value, str) or not value:
        return None
    try:
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def _now(evaluation_now):
    dt = _parse_ts(evaluation_now) if evaluation_now else None
    return dt or datetime.now(timezone.utc)


def _check_receipt(receipt, reasons):
    """Validate the scorecard receipt against the Scorecard Law's five steps.

    Returns rigor tier or None. Every step is checked mechanically:
      step 1 — >= 2 enumerated options, each with an id
      step 2 — every option scored on all four dimensions (0-10, numeric)
      step 3 — all three hard-stop gates true (no score overrides a failed gate)
      step 4 — winner matches an enumerated id AND holds the highest total
                among gate-passers; strongest alternative + falsifier substantive
      step 5 — receipt posted (comment id present); decided_at/decided_by set
    """
    if not isinstance(receipt, dict):
        reasons.append("P8: scorecard_receipt missing or not an object (no receipt, no merge)")
        return None
    for field in REQUIRED_RECEIPT_FIELDS:
        if field not in receipt or receipt[field] in (None, "", []):
            reasons.append(f"P8: scorecard_receipt missing required field '{field}'")

    # ---- Step 1: ENUMERATE
    option_ids = []
    s1 = receipt.get("step1_enumerate")
    if isinstance(s1, dict):
        options = s1.get("options")
        if isinstance(options, list):
            if len(options) < 2:
                reasons.append("step1: must enumerate >= 2 options")
            else:
                option_ids = [o.get("id") for o in options if isinstance(o, dict) and o.get("id")]
                if len(option_ids) < 2:
                    reasons.append("step1: each enumerated option needs an id")
        else:
            reasons.append("step1: step1_enumerate.options must be a list")
    else:
        reasons.append("step1: step1_enumerate missing or not an object")

    # ---- Step 2: SCORE — four dimensions, 0-10, numeric, every option.
    totals = {}
    s2 = receipt.get("step2_score")
    if isinstance(s2, dict):
        scores = s2.get("scores")
        if isinstance(scores, dict):
            for oid in option_ids:
                dims = scores.get(oid)
                if not isinstance(dims, dict):
                    reasons.append(f"step2: option '{oid}' has no score entry")
                    continue
                total = 0
                for dim in SCORE_DIMENSIONS:
                    v = dims.get(dim)
                    if not isinstance(v, (int, float)) or isinstance(v, bool):
                        reasons.append(f"step2: option '{oid}' dimension '{dim}' must be numeric 0-10")
                        break
                    if v < 0 or v > 10:
                        reasons.append(f"step2: option '{oid}' dimension '{dim}' out of range 0-10")
                        break
                    total += v
                else:
                    totals[oid] = total
        else:
            reasons.append("step2: step2_score.scores must be an object keyed by option id")
    else:
        reasons.append("step2: step2_score missing or not an object")

    # ---- Step 3: GATE — hard stops; no score overrides a failed gate.
    gates = receipt.get("step3_gate")
    gates_pass = True
    if isinstance(gates, dict):
        for g in GATE_FIELDS:
            if gates.get(g) is not True:
                reasons.append(f"step3: gate '{g}' is not true — hard stop, no score overrides it")
                gates_pass = False
    else:
        reasons.append("step3: step3_gate missing or not an object")
        gates_pass = False

    # ---- Step 4: DECIDE — winner is an enumerated id with the highest total.
    s4 = receipt.get("step4_decide")
    winner = None
    if isinstance(s4, dict):
        winner = s4.get("winner")
        if winner not in option_ids:
            reasons.append("step4: winner must match an enumerated option id")
            winner = None
        elif gates_pass and totals:
            best = max(totals.values())
            if totals.get(winner, -1) < best:
                reasons.append(
                    "step4: winner does not hold the highest total score "
                    f"({totals.get(winner)} < {best}) — the math decides, not the author"
                )
        # H1: anti-theater — strongest alternative + falsifier must be substantive.
        alt = s4.get("strongest_alternative")
        if not isinstance(alt, dict) or not alt.get("summary"):
            reasons.append("step4: strongest_alternative.summary is empty (theater check failed)")
        falsifier = s4.get("falsifier")
        if not isinstance(falsifier, str) or len(falsifier.strip()) < 20:
            reasons.append("step4: falsifier must state concrete evidence that would prove the decision wrong")
    else:
        reasons.append("step4: step4_decide missing or not an object")

    # ---- Step 5: RECEIPT — written AND posted.
    s5 = receipt.get("step5_receipt")
    if isinstance(s5, dict):
        if not isinstance(s5.get("receipt_posted_comment_id"), int):
            reasons.append("step5: receipt_posted_comment_id missing — a private scorecard is not a gate")
    else:
        reasons.append("step5: step5_receipt missing or not an object")

    tier = receipt.get("rigor_tier")
    if tier not in ("LIGHT", "FULL"):
        reasons.append("H1: rigor_tier must be LIGHT or FULL")
        return None
    if tier == "FULL":
        for field in FULL_TIER_EXTRA_FIELDS:
            if field not in receipt or receipt[field] in (None, "", []):
                reasons.append(f"H1: FULL rigor tier requires '{field}'")
        risks = receipt.get("named_risks")
        if isinstance(risks, list) and len(risks) == 0:
            reasons.append("H1: FULL rigor tier requires a non-empty named_risks list")
    # H4: scope creep — out-of-lane merge needs owning seat's acknowledgment.
    if receipt.get("lane") != receipt.get("author_lane"):
        if not receipt.get("owning_seat_ack_comment_id"):
            reasons.append(
                "H4: merge is outside the author's lane; "
                "owning_seat_ack_comment_id (owning seat's #554 acknowledgment) is required"
            )
    return tier


def may_auto_merge(pr_state):
    """Evaluate the Full Auto-Merge Law against a pr_state dict.

    Returns (allowed: bool, reasons: list[str]). allowed is True only when
    every precondition holds on live-verified, fresh evidence.
    """
    reasons = []
    if not isinstance(pr_state, dict):
        return False, ["pr_state must be an object"]

    get = pr_state.get
    now = _now(get("evaluation_now"))

    # ---- P9: evidence freshness (check first; stale evidence poisons everything)
    fetched = _parse_ts(get("evidence_fetched_at"))
    if fetched is None:
        reasons.append("P9: evidence_fetched_at missing or unparsable (stale evidence fails)")
    elif (now - fetched).total_seconds() > MAX_EVIDENCE_AGE_SECONDS:
        reasons.append(
            f"P9: evidence is stale ({int((now - fetched).total_seconds())}s old, "
            f"max {MAX_EVIDENCE_AGE_SECONDS}s); re-fetch, don't argue"
        )

    # ---- P1: checks green on the merge head
    if get("checks_green_on_head") is not True:
        reasons.append("P1: checks_green_on_head is not true (must be green on head_sha)")
    if not get("head_sha"):
        reasons.append("P1: head_sha missing")

    # ---- P2: head SHA verified against live state
    if get("head_sha_verified_live") is not True:
        reasons.append("P2: head_sha_verified_live is not true (local SHAs are claims, not measurements)")

    # ---- P3: no conflicts
    if get("mergeable") is not True or get("has_conflicts") is not False:
        reasons.append("P3: PR is not cleanly mergeable (mergeable must be true, has_conflicts false)")

    # ---- P4: branch current with main tip
    base_sha = get("base_sha")
    main_tip = get("main_tip_sha")
    if not base_sha or not main_tip:
        reasons.append("P4: base_sha/main_tip_sha missing (both must be re-fetched live)")
    elif base_sha != main_tip:
        reasons.append("P4: base_sha != main_tip_sha; branch is behind main — rebase and re-verify")

    # ---- P10 (H2): serialization — tip at merge time must equal the verified tip
    tip_at_merge = get("main_tip_at_merge")
    if not tip_at_merge:
        reasons.append(
            "H2: main_tip_at_merge missing — re-fetch the live main tip immediately before "
            "the merge call; no blind merges"
        )
    elif main_tip and tip_at_merge != main_tip:
        reasons.append(
            "H2: main tip moved since verification "
            f"(verified {main_tip}, now {tip_at_merge}); re-verify currency before merging"
        )

    # ---- P5: intent posted on #554
    intent_id = get("intent_comment_id")
    if not isinstance(intent_id, int):
        reasons.append("P5: intent_comment_id missing — intent must be posted to #554 before merging")

    # ---- P6: deconfliction re-fetch
    if _parse_ts(get("deconfliction_refetch_at")) is None:
        reasons.append("P6: deconfliction_refetch_at missing — re-fetch newest board state before merging")
    if get("same_topic_race") is not False:
        reasons.append("P6: same-topic race detected — stand down, do not merge")

    # ---- P7: revertable in one commit
    if get("revertable_one_commit") is not True:
        reasons.append("P7: not revertable in one commit (migrations/data changes -> human)")

    # ---- P8 + H1 + H4: scorecard receipt (the gate) — the five steps, validated
    # mechanically inside _check_receipt (step 5 covers posted-ness).
    _check_receipt(get("scorecard_receipt"), reasons)

    # ---- Human-only exclusions (any one forces the human gate)
    changed = get("changed_files") or []
    if not isinstance(changed, list):
        reasons.append("human-only: changed_files must be a list (cannot assess protected paths)")
        changed = []
    hit = sorted({p for f in changed for p in PROTECTED_PATH_PREFIXES if str(f).startswith(p)})
    if hit:
        # Narrow, evidence-bound exception: the supreme Scorecard Law's own
        # encoding may merge when the receipt proves the Human Director already
        # ratified the substance (the merge encodes ratified authority, it
        # creates none). Without that proof, protected paths never auto-merge.
        exc = (get("scorecard_receipt") or {}).get("supreme_law_exception")
        if (
            isinstance(exc, dict)
            and exc.get("ratified_by") == "Shawn Vibert"
            and isinstance(exc.get("ratification_evidence_comment_id"), int)
            and isinstance(exc.get("scope"), str)
            and len(exc["scope"].strip()) >= 20
        ):
            pass  # exception proven on the receipt; protected-path gate waived
        else:
            reasons.append(f"human-only: touches protected paths {hit} — never auto-merged")
    for flag, label in (
        ("is_production_deploy_or_dispatch", "production deploy/dispatch"),
        ("is_production_db_access", "production DB access"),
        ("touches_credentials_or_money", "credentials/money"),
        ("is_destructive_or_irreversible", "destructive/irreversible action"),
        ("is_constitutional_or_evolve_ratification", "constitutional/EVOLVE-charter ratification"),
    ):
        if get(flag) is not True and get(flag) is not False:
            reasons.append(f"human-only: '{flag}' unattested (missing flags fail closed as human-only)")
        elif get(flag) is True:
            reasons.append(f"human-only: {label} — never auto-merged")

    return (len(reasons) == 0, reasons)


def main(argv):
    if len(argv) != 2:
        print("usage: python3 tools/auto_merge_gate.py <pr_state.json>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], "r", encoding="utf-8") as fh:
            pr_state = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"law": LAW_ID, "allowed": False, "error": str(exc)}))
        return 2
    allowed, reasons = may_auto_merge(pr_state)
    print(json.dumps({"law": LAW_ID, "allowed": allowed, "reasons": reasons}, indent=2))
    return 0 if allowed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
