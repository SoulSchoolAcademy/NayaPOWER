# Projections Must Never Write the Canonical Source — the Display Seam Defect

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0401-projections-must-never-write-source
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6004790753 ([NAYA][FOUNDATION FINDING] Feed/backlog UX is right; current write seam needs correction, 2026-10-05T22:50:18Z / 15:50 PDT).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A foundation finding with two evidence-based defects in the Feed/Backlog implementation: (1) `.github/workflows/activity-feed.yml` ran every 15 minutes and **committed/pushed ACTIVITY-FEED.md to main** whenever activity changed — the exact main SHA moved on a display schedule, continuously recreating parity drift and stale exact-SHA proof targets; (2) `BACKLOG.md` declared itself "the canonical shared to-do list" while `BRAIN/90-OPERATIONS/0001-MAX-10-EXECUTION-QUEUE-V1.md`, Issues/PRs, and live current-truth evidence already carry work authority — without an explicit authority relationship this recreates split continuity. The repair: preserve the feature, fix the seam. The target law: `CANONICAL EVENT / ISSUE / PR / RECEIPT → PROJECTION → HUB`. Never: `ACTIVITY DISPLAY → NEW CANONICAL SOURCE COMMIT`. The backlog becomes a human-readable projection/index of authoritative work state; the activity feed becomes projection-only and updates without moving main.

## HUMAN NOTE

We built the new Activity Feed and Backlog, and the UX direction is right — Shawn's direction stands. But the plumbing had two real defects, caught and classified as P0 (#1519): the feed's update robot was committing its own display file to the main branch every 15 minutes, which means the "current version" of the entire codebase kept moving every time the display refreshed — that silently broke every exact-version proof the team runs. And the backlog document claimed to be THE official to-do list while other places already hold that job, which creates two competing "official" lists. Both were repaired: the feed no longer writes to main, the backlog is now explicitly a projection — a readable window onto the real sources of truth, not a second one.

## CHILD NOTE

Imagine the scoreboard at a game painting over the referee's rulebook every time the score changes. That's what the activity feed was doing — it repainted the whole book every 15 minutes just to update a display. Now the rulebook stays still, and the scoreboard just shows what's in it. Same with the backlog list: it doesn't get to call itself "the boss" when there are already bosses — it's now a window that looks at the real bosses. Displays show; sources decide.

## GRANDMA NOTE

The lesson is simple and it will outlive this project: a picture of something must never redraw the thing it pictures. We had a system that refreshed its own activity display by writing a new file into the official record every fifteen minutes — so the official record never stayed still, and every check that needed an exact, unmoving record kept failing for no good reason. We also had a to-do list that announced itself as the one true list when other true lists already existed. Both are fixed by one rule: displays look, they never touch. The activity feed shows state without moving it; the backlog reflects the real work authority instead of competing with it.

## NAYA NOTE

Two defects, one doctrine. (1) Write-direction: a projection pipeline that commits to the canonical source turns every render cycle into a source mutation — parity drift becomes a schedule, not an accident. Rule: projections are read-only artifact output; authority to move main belongs to governed work commits only. (2) Authority claims: a document that declares itself canonical while other surfaces already carry work authority recreates split truth silently — no malice required. Rule: exactly one owner per authority domain, with explicit projection relationships (owner → projection → Hub). The target law `CANONICAL EVENT / ISSUE / PR / RECEIPT → PROJECTION → HUB` is the forward direction; the reverse is a defect by definition, however useful the display feels.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0401",
  "intelligent_block": "IB-SMART-NOTE-20261005-sn0401-projections-must-never-write-source",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-05",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "defects": [
    {"id": 1, "seam": "activity-feed.yml self-writing main every 15 min", "effect": "continuous exact-SHA parity drift, stale proof targets"},
    {"id": 2, "seam": "BACKLOG.md claiming canonical to-do authority", "effect": "split continuity vs execution queue / Issues / PRs / live truth"}
  ],
  "target_law": "CANONICAL EVENT / ISSUE / PR / RECEIPT → PROJECTION → HUB",
  "forbidden": "ACTIVITY DISPLAY → NEW CANONICAL SOURCE COMMIT",
  "repair": {"issue": "#1519 (P0)", "feed": "projection-only, no main writes", "backlog": "explicit projection/index, not truth owner"},
  "evidence": {"board": "#1354 6004790753 (2026-10-05T22:50:18Z)"},
  "cousins": ["SN-0191", "SN-0388", "SN-0395", "SN-0392"]
}
```
