"""
Ultimate Strategy Plan, best-of-best, as code.

Sources, in order of authority:
  1. Shawn Vibert, director, in chat 2026-10-24: done today, test immediately,
     maximum verified value per action/moment/output, think first, compose
     from existing pieces, AAA finish, no verbatim copying, scorecard then rewrite.
  2. Naya Power V1 + V2 self-scorecard (7.5/10, Loop 1 author review).
  3. Naya Resolve V2 scorecard (8.0/10 for Power V2) + rewrite, three tongues,
     2026-10-24: disposition clock, interim merge lane, standing-red baseline,
     resource budget, owners+gates, #3028 audit gates, kill criteria,
     sized verification lane, Shawn's items in-queue, front door, verdict SLA.

Status: LAW, approved by Shawn Vibert, director, in chat 2026-10-24 ~09:03 PDT.
This code is now operating law for this seat. Repo merge still follows the
normal road: different-seat scorecard at the exact final head, then merge.
It never merges itself, never writes production data, never touches a ruleset.

Design contract, also law, same approval:
  Everything elevated, clean, crisp. Nothing below high level. Exactly
  what's needed, in the most elegant, beautiful, intelligent way.
  High-contrast text, nicest fonts, perfect place and spacing, awe-inspiring
  yet easy, logical, sensible, push-button simple. Shop from our own shop:
  use approved elements, do not reinvent, do not invent diamonds.
  Design parents are the live Life with Naya page and the certificate /
  Smart Identity Activation page. Live pages win over repo files.

Corrections applied in this best-of-best, with live verification 2026-10-24:
  - Merge-gate hole is ruleset 24858146 "main-protection": pull_request
    required_approving_review_count = 0, dismiss_stale_reviews_on_push = False,
    no required_status_checks rule. Ruleset 23853581 "Naya Execution
    Governance" carries deletion + non_fast_forward only, no review/check
    rules, and bypass_actors = none listed at repo level for both rulesets
    (live read 2026-10-24). Resolve's draft attributed the hole to 23853581
    with bypass actors existing; that attribution is NOT carried forward.
  - Ambassador earning terms (50%, automatic Wednesday payout, pricing ladder)
    were ruled by Shawn in chat 2026-10-24. In this code they are carried as
    "ruled in chat, pending confirmation in the open before payout code
    prices on them", adopting Resolve's caution without erasing Shawn's ruling.
    Payout wiring stays behind the money gate in any case.
  - Front door is a THRESHOLD, not a Join button inside member navigation:
    unactivated visitors route to certificate -> Welcome; members inside the
    Hub never see a Join button. This preserves Shawn's 2026-10-24 correction.
  - PR #3036 (head f88edf88...) and PR #3037 (head 7dc4c4b6...) verified
    open, not draft, by live read 2026-10-24. Their 9.5 scorecards are
    Resolve-reported; this seat has NOT independently re-verified those
    scorecards in this pass, and the code marks them as such.

Pure functions only. No network, no database, no file writes in this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

LAND_THRESHOLD = 9.0
WIP_CAP_TEAM = 5
DISPOSITION_SLA_HOURS = 2
DISPOSITION_WEAKEST_HOURS = 4
WAKEUPS_CEILING_PER_DAY = 800
WAKEUPS_TARGET_LOW = 225
WAKEUPS_TARGET_HIGH = 250
RATIO_BAR = 60  # effort per verified outcome, must be < 60:1 by 2026-10-30

WEIGHTS = {"journey": 10, "system": 5, "fix": 1}

# Standing-red baseline, Resolve-reported 2026-10-24, heads e0cd4c24 + f7b0388e.
# Re-measure at the new head before claiming any burn-down. A failure NOT in
# this set blocks landing, mechanically.
STANDING_RED = {
    "retrieval_page_hash_mismatch": 14,
    "brain_index": 3,
    "factory": 2,
    "migration_baseline_missing_ledger_entry": 1,
    "vanish_sn_0842": 1,
    "report_generator_pin": 1,
}
STANDING_RED_TOTAL = sum(STANDING_RED.values())  # 22


@dataclass
class QueueItem:
    key: str
    priority: int
    owner: str
    gate: str
    tier: str = "system"  # journey | system | fix
    state: str = "queued"  # queued | claimed | verified | landed | blocked | thinking
    builder: str = ""
    scorer: str = ""
    verifier_login: str = ""
    builder_login: str = ""
    score: float = 0.0
    verified_at: datetime | None = None
    failures_same_way: int = 0
    failures_total: int = 0


def aaa_check(aligned: bool, authenticated: bool, actionable: bool) -> tuple[bool, list[str]]:
    """AAA finish: all three required. Two of three is NOT finished."""
    missing = []
    if not aligned:
        missing.append("ALIGNED")
    if not authenticated:
        missing.append("AUTHENTICATED")
    if not actionable:
        missing.append("ACTIONABLE")
    return (not missing, missing)


def can_claim(item: QueueItem, seat: str, team_wip: int) -> tuple[bool, str]:
    """Claim is the lock. One seat per item, team WIP cap 5, scorer/verifier
    must be named at build start (blank roster blocks start)."""
    if item.state == "claimed":
        return False, f"{item.key} already claimed by {item.builder}"
    if team_wip >= WIP_CAP_TEAM:
        return False, f"team WIP cap {WIP_CAP_TEAM} reached"
    if not item.scorer or not item.verifier_login:
        return False, f"{item.key} has blank scorer or verifier: start blocked"
    if item.scorer == seat:
        return False, "scorer must differ from builder"
    item.state = "claimed"
    item.builder = seat
    return True, "claimed"


def can_land(item: QueueItem, failures: list[str]) -> tuple[bool, str]:
    """Land only at >= 9.0, different-seat scorecard, different-login live
    verification, and no failure outside the enumerated standing-red set."""
    if item.score < LAND_THRESHOLD:
        return False, f"score {item.score} below land threshold {LAND_THRESHOLD}"
    if not item.scorer or item.scorer == item.builder:
        return False, "scorecard must be by a different seat than the builder"
    if not item.verifier_login or item.verifier_login == item.builder_login:
        return False, "verification must be by a different login than the builder"
    new_red = [f for f in failures if f not in STANDING_RED]
    if new_red:
        return False, f"new red blocks landing: {new_red}"
    return True, "landable"


def disposition_status(item: QueueItem, now: datetime) -> str:
    """Disposition clock, starts at verification >= 9.0.
    +2h unlanded -> escalate to Integrator. +4h -> named weakest point."""
    if item.state == "landed":
        return "LANDED"
    if item.verified_at is None or item.score < LAND_THRESHOLD:
        return "NOT_VERIFIED"
    age = now - item.verified_at
    if age >= timedelta(hours=DISPOSITION_WEAKEST_HOURS):
        return "WEAKEST_POINT"
    if age >= timedelta(hours=DISPOSITION_SLA_HOURS):
        return "ESCALATE_INTEGRATOR"
    return "WITHIN_SLA"


def kill_decision(item: QueueItem) -> str:
    """Kill criteria: same cure fails twice same way -> change mechanism.
    Third failure -> return to THINK, re-think from the whole."""
    if item.failures_same_way >= 2:
        return "CHANGE_MECHANISM"
    if item.failures_total >= 3:
        return "RETURN_TO_THINK"
    return "CONTINUE_SAME_PASS"


def verification_lane_action(build_queue_len: int, verify_queue_len: int) -> str:
    """Verification is a priced lane. If verify queue outgrows build queue,
    builders rotate to verifying (chameleon law). Proven work never waits
    for a scarce verifier while builders start new work."""
    if verify_queue_len > build_queue_len:
        return "ROTATE_BUILDERS_TO_VERIFY"
    return "NORMAL_FLOW"


def verdict_sla_ok(cleared_per_day: int, filings_per_day: int) -> bool:
    """Learning verdict SLA: cleared/day must be >= filings/day."""
    return cleared_per_day >= filings_per_day


def resource_budget_ok(wakeups_today: int, weighted_value_today: int) -> tuple[bool, str]:
    """Ceiling 800/day. If the budget binds, stop low-value work before
    adding agents. Stopping is a first-class queue action, not a failure."""
    if wakeups_today > WAKEUPS_CEILING_PER_DAY:
        return False, f"wakeups {wakeups_today} over ceiling {WAKEUPS_CEILING_PER_DAY}: stop low-value work"
    if wakeups_today > 0 and weighted_value_today == 0:
        return False, "wakeups spent with zero weighted verified value: stop and re-rank"
    return True, "within budget"


def front_door_route(visitor_has_identity: bool) -> str:
    """Threshold, not a nav button. Unactivated visitors route to the
    certificate -> Welcome door from outside. Members inside the Hub
    never get a Join button, because joining is behind them."""
    if visitor_has_identity:
        return "HUB"
    return "CERTIFICATE_WELCOME"


def weighted_value(landed_tiers: list[str]) -> int:
    """Journey 10, system 5, fix 1. Raw item count is not value."""
    return sum(WEIGHTS.get(t, 0) for t in landed_tiers)


def scoreboard(pct_done_proven: float, parts_at_9plus: int, parts_total: int,
               ratio_today: float, sync_health_pct: float, gates: dict,
               weakest_point: str, top_priorities: list[str],
               director_packets: list[str]) -> dict:
    """Five numbers + three lists, derived from the record, never typed.
    A cold reader must answer: what is true, what is mine, what is next."""
    return {
        "numbers": {
            "pct_done_proven": pct_done_proven,
            "parts_at_9plus": f"{parts_at_9plus}/{parts_total}",
            "ratio_today": ratio_today,
            "sync_health_pct": sync_health_pct,
            "gates": gates,
        },
        "lists": {
            "weakest_point": weakest_point,
            "top_priorities_with_owners": top_priorities,
            "director_packets": director_packets,
        },
    }


def thirty_second_test(knows_true: bool, knows_mine: bool, knows_next: bool) -> bool:
    """Shawn's screen test: all three yes, or the screen fails."""
    return bool(knows_true and knows_mine and knows_next)


def design_check(elevated: bool, clean: bool, crisp: bool,
                 high_contrast: bool, perfect_spacing: bool,
                 exactly_needed: bool, push_button_simple: bool,
                 approved_elements_only: bool) -> tuple[bool, list[str]]:
    """Design contract, machine law. Every element must pass. A page below
    this standard fails before it reaches Shawn, even if its function works.
    Approved elements only means: no invented diamonds, no reinvented
    elements where an approved Life with Naya / certificate element exists."""
    checks = {
        "ELEVATED": elevated,
        "CLEAN": clean,
        "CRISP": crisp,
        "HIGH_CONTRAST": high_contrast,
        "PERFECT_SPACING": perfect_spacing,
        "EXACTLY_NEEDED": exactly_needed,
        "PUSH_BUTTON_SIMPLE": push_button_simple,
        "APPROVED_ELEMENTS_ONLY": approved_elements_only,
    }
    failed = [name for name, ok in checks.items() if not ok]
    return (not failed, failed)


# Today's first queue, best-of-best order (Resolve queue + Power V2 queue,
# merged, duplicates removed). Owners and gates are start preconditions.
# PR #3036/#3037 existence + heads verified live 2026-10-24; their 9.5
# scorecards are Resolve-reported, marked as such in the machine JSON.
TODAY_QUEUE: list[QueueItem] = [
    QueueItem(key="land-pr-3036-3037", priority=10000, owner="merge lane",
              gate="already verified 9.5 (Resolve-reported, not re-verified here)",
              tier="system"),
    QueueItem(key="build-welcome-flow", priority=9999, owner="Nitro + Power",
              gate="#3028 audit 1: no-fork journey, cold walk, zero undeclared hand assist",
              tier="journey"),
    QueueItem(key="prove-privacy-two-owner", priority=9500, owner="Power",
              gate="#3028 audits 2, 3, 5; until pass state = SPECIFIED",
              tier="system"),
    QueueItem(key="public-front-door-threshold", priority=9400, owner="Nitro",
              gate="cold walk by non-builder seat; any builder-hand step = NOT LIVE",
              tier="system"),
    QueueItem(key="build-ambassador-system", priority=9000, owner="Power",
              gate="earning terms ruled in chat, pending confirmation in the open before payout pricing",
              tier="system"),
    QueueItem(key="face-pulse-today", priority=7000, owner="Power (named debt)",
              gate="page numbers reconcile with census record, clicked live",
              tier="fix"),
    QueueItem(key="project-list-states-note-pages", priority=6500, owner="Nitro",
              gate="list shows per-item state; /s/ note opens standalone",
              tier="fix"),
    QueueItem(key="gt-039-production-packet", priority=6000, owner="Resolve (packet); Nitro/security lane (blocker)",
              gate="fitted per-table policies land, then one consolidated director tap",
              tier="system"),
    QueueItem(key="director-items-in-queue", priority=5900, owner="Shawn",
              gate="ruleset tap packet + rollback prepared; seven Welcome answers in his own session only",
              tier="system"),
    QueueItem(key="stuck-review-verdicts", priority=5800, owner="Resolve (main seat)",
              gate="verdict SLA: cleared/day >= filings/day, starting today",
              tier="system"),
]
