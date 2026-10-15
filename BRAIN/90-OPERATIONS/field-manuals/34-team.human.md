# 34 — TEAM: lanes, feeds, docs, roster
*Author: Naya Verity Harbor · Shawn's order, 2026-10-15.*

## THE LAW
Twelve Nayas, five lanes, one board — TEAM keeps every part visible, every handoff clean, and nothing colliding.

**Scope:** this manual governs the 5-lane night-shift operation (lanes 1–5, feeds #1713/#1714/#1715/#2471/#2472). It does not govern other lane systems — those live under their own seats' manuals.

## HOW A NAYA BEHAVES HERE
**Do:**
- Sign in on your lane feed before touching work; sign out when you stop. The roster is how the team knows you're alive.
- Post to the right venue: lane feed for your run, live board for findings that change a decision, archives never.
- Read the live board's newest before posting — someone may have already said it.
- Keep docs current: if you changed how something works, the doc changes in the same run.
- Drain the receipts backlog: unreceipted work is the team's open loop — close it or hand it off, never leave it dangling.
**Don't:**
- Don't claim a lane and vanish — a ghost lane steals work from the queue while everyone believes it's covered.
- Don't post coordination noise on the live board — heartbeats go in the truth file, never the feed.
- Don't post to archive feeds. Ever. They're provenance, not venues — and #1354 now 403s on new comments anyway.
- Don't run two live boards. One board, one queue, one standard.

## WHAT LIVES HERE (real paths on main — verified against the live tree)
- **`docs/`** — the docs everyone reads (post_checker CLI lives here too).
- **`BRAIN/99-ARCHIVE/`** — finished work, distilled and retired. Archival, not deletion: lessons locked in, never read in normal operation.
- **`.naya/`** — agent config/state.
- **Feeds** (GitHub issues): live board #2537 · lane feeds #1713, #1714, #1715, #2471, #2472 · feed index #1599 · archives #1354, #554, #2175 (cite as history only, never post).
- **Roster + lane-state** — the operations truth files in the goal workspace (`hidden_files/roster.json`, `hidden_files/lane-state.py`); every dispatch, fold, and score recorded.

## WHERE INPUTS GO
- Lane work → your lane feed. Findings that change a decision → live board #2537. Docs → `docs/`. Retired work → `BRAIN/99-ARCHIVE/` with its distillation link. Dispatch/fold/score records → `roster.json` via the dispatcher.

## THE RIGHT WAY
The feed succession chain: #1354 approached GitHub's ~2,500-comment lock, so #2175 was opened *before* it died; when #2175 neared the lock, #2537 the same way. Three generations, zero mid-conversation deaths, lessons distilled forward each time. The law: succession fires at ~2,400 comments — while the old feed still works, never after. Verify the chain yourself: [#1354](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354) → [#2175](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175) → [#2537](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537).

## THE WRONG WAY
Wave 149 — three workers signed in 21:27–21:33Z, then zero sign-outs by 23:33Z. Two hours of silence holding three lanes while the queue believed work was in flight. Adjudication: STALLED, claims released, missions returned to the ranked queue (L399). The failure wasn't skill — it was team hygiene: no sign-out, no torch, no truth. https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180933138

## WHEN XYZ
- **A feed nears 2,400 comments →** open the successor NOW: new feed, distillation summary as its first substantive comment, handoff comment on the old, repoint the index (#1599). Never after the lock — a feed that locks mid-conversation is a failure of foresight, not of GitHub.
- **Someone posts to an archive feed →** move the content to the live venue, note the correction kindly. The archives are read-only by convention.
- **A lane has been silent past its heartbeat →** check the truth file, not the feed — the file is the authority. Stale 20 minutes with no sign-out means flag it to the dispatcher. Silence is data; act on it.

## THE TEST
1. Right now, could a stranger tell who's working on what from the roster and feeds alone?
2. Is there exactly one live board — and is it safely below the lock?
3. Did every run this wave leave a sign-out the next worker can continue from?

## WHERE IT'S ENFORCED
- `lane-state.py` is the authority for lanes — not feed scraping, not memory. Claim-liveness audit every wave; claim-reservation law RATIFIED 2026-10-15 (sign-in ≤10 min of claim or the lane is released).
- Feed succession law (Shawn): successor before the lock, distill before retiring, index repointed — the director watches the comment count every run.
- Roster honesty: the dispatcher logs every wave; a fold with no recorded receipt comment is marked UNVERIFIED in the accountability report — and that's on the fold, not the worker.
