# SCORECARD — Hub 9-Circle Bar Overflow Fix (Area #8) — 2026-11-14

## Score: 9/10

| # | Check | Result |
|---|---|---|
| 1 | Defect reproduced first-hand (live /hub, settled state) | PASS — checker numbers exact to the pixel at 390/360; 0 errors |
| 2 | Fix choice scorecarded (fit vs scroll), one picked with reason | PASS — scroll + visible affordance; fit rejected as a redesign (labels unreadable) |
| 3 | Fix is bar-only; no worker/feed/entrance/modal/redesign | PASS — diff scoped to the one-bottom-bar block, verified line-by-line |
| 4 | At 390/360 every pill reachable + fully visible, visible affordance | PASS — › fade + chevron at rest; tap → last 5 whole (SL 208/238); ‹ returns; real touch swipe moves the row |
| 5 | At 1440 nothing changes | PASS — no chevrons/fades; pill positions identical to live (MAIL 382 … 10 APPS 1058) |
| 6 | Gems unregressed | PASS — 3, 27×27 at 390/360, SVGs 564/540/676 (checker's numbers exactly) |
| 7 | Note route + SN-2696 + feed unregressed | PASS — bot /s/sn2696 200 (14,635 B); note renders on staging (title, hook, nutshell); feed 1085 notes, cards visible |
| 8 | Template + repo byte-identical (the trap) | PASS — both sha `7d25f591…`, 5,003,256 B |
| 9 | Next-sync proof (sync's own function) | PASS — fix survives, +2 B (same artifact as the live leg) |
| 10 | Staged proof by eye, cold + direct, 390/360/1440, 0 errors | PASS — with the limits named below |

## Deduction (−1)

The staging worker — the fullest staged surface (note renders, feed
live) — was overwritten by another round between my deploy and the
checker's turn, so the checker cannot re-run the note walk there without
a re-deploy. The stable proof is the proof-host link (immutable branch
bytes) + my completed worker probe in the record. A shared-staging
process gap, not a defect in the fix — but the proof is weaker for it.

## What would make it 10

A re-deploy of the staging worker (after the other round's staging is
done) with the checker re-walking the note at 390 — closing the loop on
a surface the checker controls — plus Shawn's tap to live.
