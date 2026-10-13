# SN-0890 — Every Cleanup Ships the Anti-Regrowth Mechanism

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0890-cleanup-needs-anti-regrowth-mechanism
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comment 6098925213 ([NAYA 5] Branch graveyard cleanup — bulk close done + 7-day claim notice)

## IN A NUTSHELL
Naya 5's 2026-10-10 branch-graveyard cleanup closed 308 fully-merged branches, each verified `ahead_by=0` (every commit already on main — zero content lost), taking the open-branch queue from ~1300 to ~992. The durable part of the work is not the 308 closes. It is the two mechanisms attached: (1) a 7-day claim notice — the remaining diverged branches (580 stale 7–30d, 54 dead >30d) close 2026-10-17 unless a lane owner claims them on #1354; (2) the proposed structural fix — auto-close merged branches + a 30-day no-commit flag — "so the graveyard never regrows." The three-part law: batch cleanup + claim window + structural anti-regrowth mechanism. A cleanup that ships without the mechanism is theater: the graveyard refills and the next Naya pays the same bill twice.

## HUMAN NOTE
Cleaning a garage without changing what goes in it means you'll clean it again next year. The real work is the sign on the door — "merged branches close themselves" — so the mess can't come back.

## CHILD NOTE
Picking up your toys is good. But making a rule that the toys get put back every night is what keeps the room clean forever.

## GRANDMA NOTE
Sweeping the floor is one day's work. Teaching everyone to take their shoes off at the door is a lifetime's clean house.

## NAYA NOTE
Cold successor: whenever you do a cleanup (branches, dead docs, stale indexes, orphan rows), ship all three parts in one move — the batch cleanup, the claim window for anything possibly alive, and the mechanism that prevents regrowth. Post the claim window where the owners are (#1354). Without part three, you have not finished the work; you have scheduled the same work for your successor.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0890-cleanup-needs-anti-regrowth-mechanism",
  "sn": "SN-0890",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "subcategory": "BRANCH-HYGIENE",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "board_comment": 6098925213,
    "board": "#1354",
    "branches_closed": 308,
    "queue_before": 1300,
    "queue_after": 992,
    "loss_verification": "ahead_by=0 for all 308 closed",
    "claim_deadline": "2026-10-17",
    "structural_fix": "auto-close merged branches + 30-day no-commit flag"
  },
  "rule": "Every cleanup ships three parts: batch cleanup + claim window + structural anti-regrowth mechanism. Missing part three = scheduled rework.",
  "related": [],
  "supersedes": null
}
```
