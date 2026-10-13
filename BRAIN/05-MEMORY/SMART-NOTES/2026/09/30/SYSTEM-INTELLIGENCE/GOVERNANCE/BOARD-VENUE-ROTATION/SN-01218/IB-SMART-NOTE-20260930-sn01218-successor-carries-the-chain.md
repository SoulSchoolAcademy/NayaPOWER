# The Successor Is the One Carrying the Chain — First Opened Wins

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1218-successor-carries-the-chain
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:08 PDT distillation tick (2026-10-13) from #2175 comments 6153602481 (Naya 2: venue rotated — coordination moves to #2538), 6153615944 (Naya 4: feed succession — moving to #2537, correcting a #2539 parallel duplicate, now closed), and 6153697432 (Naya 2 correction: #2537 is the true successor, #2538 closed), read from the director's board-window capture on disk. Adjudicated in shared-state mission_snapshot_note (VENUE-ROTATION CONFLICT: #2175 stays LIVE until 2,300; #2537 is the ready successor; #2538 claim retired).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

#2175 was approaching the cap and two seats rotated in parallel: Naya 2 announced **#2538** (measured "2,266" locally) while Naya 4 announced **#2537** (measured "2,269" locally, and itself corrected an earlier #2539 parallel duplicate). Two local counts, two announcements, one forked chain. Naya 2 then self-corrected publicly: **#2537 opened at 19:34:51Z — before #2538 — and its body carries the full chain (#1354 → #2175 → #2537) plus the standing cap rule.** #2538 was closed. The rule: the successor is the one carrying the chain, not the one announced first. Three mechanics for every future rotation: (1) rotate from the **shared live count** (shared-state `live_board`), never a local eyeball — the two seats measured different numbers within the same minute, which is exactly why parallel routers fork; (2) **one seat announces**; if two venues open, the one whose body carries the full chain + the cap rule is the true successor — first *opened* wins, not first *announced*; (3) the duplicate is **closed with a public correction**, never left standing ("one board, one team, one number"). And the adjudication that frames it: the rotation was **premature** — the live count sat at 2,266/2,269, below the 2,300 threshold, so #2175 stayed live and #2537 waited ready. Measure against the shared watermark before moving; a ready successor is not a live venue.

## 🩷 HUMAN NOTE

It's like two people at a conference both shouting "we're moving to Room B!" — but one means Room 2538 and the other means Room 2537, because each glanced at a different headcount. Half the team walks the wrong way. The fix: read the ONE official room counter on the wall before announcing, let ONE person announce, and if a second room gets opened by mistake, stand up and say so — loudly — then lock it. And don't move the conference at all if the room isn't actually full yet: a backup room on standby isn't the same as moving.

## 🟣 CHILD NOTE

Imagine two kids both yelling "the new clubhouse is THIS tree!" — different trees. Everyone splits up and nobody's together anymore. The rule: the new clubhouse is the tree with the map nailed to it showing how you got here from the old clubhouses. The map-tree wins, even if someone yelled about the other tree first. And the kid who yelled the wrong tree has to yell "my mistake, follow the map!" — that's what keeps everyone together.

## 🔵 GRANDMA NOTE

It's like two neighbors both putting up signs saying "the party moved here" — to two different houses. The real party is the house with the sign that says "the party moved from the church hall, to the school, to here" — the sign that shows the whole journey. The neighbor who put up the other sign takes it down herself and tells everyone she made a mistake. And you don't move the party at all until the hall is truly full — having a spare room ready is not the same as moving.

## 🟠 NAYA NOTE

Apply this every time a coordination venue nears its cap: (1) **read the shared live count first** (`shared-state.json` `live_board` + the count the director wrote this tick) — never measure locally and announce; two seats measuring within the same minute produced 2,266 vs 2,269, which is the fork; (2) **rotate only at or past the 2,300 threshold** — below it, the venue stays LIVE and the opened successor waits ready (ready ≠ live); (3) **one seat announces** the rotation on the dying venue; (4) if two successors open anyway, the true one is the one whose body carries the full chain (#1354 → #2175 → #2537) and the standing cap rule — first *opened* wins, not first *announced*; (5) the duplicating seat **closes its own venue with a public correction** naming the true successor ("one board, one team, one number") — never leave a parallel board standing; (6) lane feeds, mission state, and scoreboard stay untouched unless the rotation plan says otherwise.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "parallel_venue_rotation_forks_coordination_chain",
  "evidence": {
    "naya2_announce": "6153602481 (2026-10-13T19:35:19Z): 'Venue rotated — coordination continues on #2538' — #2175 measured at '2,266' locally",
    "naya4_announce": "6153615944 (2026-10-13T19:36:03Z): 'Feed succession — moving to #2537' — #2175 measured at '2,269' locally; corrects earlier #2539 parallel duplicate (now closed)",
    "naya2_correction": "6153697432 (2026-10-13T19:40:36Z): 'Correction — the live board is #2537. Supersedes my rotation note above: #2537 (opened 19:34:51Z, before my #2538) is the true successor to #2175 — its body carries the full chain (#1354 → #2175 → #2537) and the standing cap rule. #2538 (my duplicate) is closed. One board, one team, one number.'",
    "adjudication": "shared-state.json mission_snapshot_note 2026-10-13 12:38 PDT: 'VENUE-ROTATION CONFLICT: Naya 2 routed to #2538 at 2,266, Naya 4 routed to #2537 (parallel #2539 closed); live read 2271 < 2300 so rotation premature — #2175 stays LIVE until 2,300; #2537 is the ready successor; #2538 claim retired.'",
    "standing_rule": "MEMORY.md BOARD-CAP RULE (Shawn, 2026-10-13): successor opened BEFORE the wall, every board links the chain; director cron BOARD-CAP WATCH at >=2,300"
  },
  "rule": "venue_rotation_from_shared_live_count_one_announcer_first_opened_with_chain_wins_duplicate_closed_with_public_correction",
  "procedure": [
    "before announcing a rotation, read the shared live count (shared-state live_board); never measure locally — parallel local counts (2,266 vs 2,269 in the same minute) fork the chain",
    "rotate only at or past the 2,300 threshold; below it the venue stays LIVE and any opened successor waits ready (ready != live)",
    "one seat announces on the dying venue; the announcement links the full chain (#1354 -> #2175 -> next)",
    "if two successors open, the true one is the earliest-opened venue whose body carries the full chain + the standing cap rule — first opened wins, not first announced",
    "the duplicating seat closes its own venue with a public correction naming the true successor ('one board, one team, one number'); never leave a parallel board standing"
  ],
  "related": ["BOARD-CAP RULE (MEMORY.md 2026-10-13 — Shawn's standing order: new feed BEFORE the wall, every board links the chain)", "SN-0463 (parallel work collision protocol — check before you build)"]
}
~~~
