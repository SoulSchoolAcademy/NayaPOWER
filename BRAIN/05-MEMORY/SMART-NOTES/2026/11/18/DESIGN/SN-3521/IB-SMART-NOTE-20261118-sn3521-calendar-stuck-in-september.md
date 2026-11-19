# SN-3521 — The Calendar Is Stuck in September — One Date, the Right Date, Everywhere

**Filed:** Intelligence Loop run 336, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3521; filed as SN-3521 under its draft number.

**Filed by:** Intelligence Loop run 336, 2026-11-18 — Shawn's ultimate calendar review, ~23:57–23:58Z: 10 screenshots + live voice, walked image by image by the captain. Filed as the captain's review `~/workspace/team-nitro/calendar-ultimate-20261118/CAPTAIN-REVIEW-ULTIMATE-CALENDAR-20261118.md`.

**Paired Naya Note:** NN-20261118-calendar-stuck-in-september

## The teaching, in his words (verbatim)

"how do we make it the ultimate? 10 out of 10? What's missing? What needs refining? More elegant? More beautiful?"

"is that the best feature for that page? How can I make that feature 10 times better, that page 10 times better, in usefulness?"

## The understanding

The headline finding is proven by date math, not opinion: the calendar body is living in September while the top bar says November 18. Nov 1, 2026 is a Sunday; the month grid puts the 1 under Tuesday with two leading blanks — that is September 2026's layout exactly (Sept 1 = Tuesday, 30 days). Nov 18 lands under Friday in the grid; the real Nov 18 is a Wednesday. The hero says "Friday, September 18th 2026". The portal card says "September 26, Friday" — September 26 is a Saturday, so the card is wrong twice: wrong month AND wrong weekday for its own date. The data is Nov 18's (3 appointments, matching the month view) — so this is a display/state bug: the viewed date is stale. The code has `var startDay = first.getDay()`; `first` / the viewed date is stale (September). This SUPERSEDES the old queued "hero-date" defect: it was never one wrong label — the whole body is on the wrong month. The fix: the grid, the hero and the portal card all follow the actual viewed day — Nov 1 Sunday, 0 leading blanks, 5 rows, Nov 18 under Wednesday, hero "Wednesday, November 18th 2026". One date, the right date, everywhere. The 6th row is entirely empty — dead space, it goes. His scorecard for the whole calendar: 6/10. The frame holds (7/10); the month view 6/10; the day blocks 5/10 — right shapes, but narrow islands in empty dark space, dead features, overlapping nav, wrong dates. The 10/10 bar: the right day, the right month, the right colours, every feature alive, nothing overlapping, everything elegant — a royal high-tech interface with the day laid out in the simplest most beautiful way. And the law that governs the round: every feature made 10x better in usefulness — for every page and every feature, ask whether it is the best feature for that page and how to make it ten times better. A board of dead ends is not a feature: Local / Provincial / Global news, Weather, Horoscope all say "Not connected yet" — wire them, or the board waits until it is live. Same for Your Worlds: Smart Mail / Messages / Connections say "Not connected yet" — wire them or hold the board. Half a board of dead rows is not a board. The always-current news feed exists in the system — wire it. The best board of the set is Notifications — three cards filling the width, ADD SOURCE clear, the "0" digit tile right — and even there the outer board has wide empty margins and the "NOT CONNECTED YET" pills shout instead of staying quiet. The Nov 17 wisdom bar in gold is the standard: one clean bar, Hz + date + wisdom + source, gold rim, everything in one line, nothing fighting. Every board should read that clean.

## The law

One date, the right date, everywhere — the grid, the hero and the portal card all follow the actual viewed day; the viewed date is never stale. Every feature made 10x better in usefulness: for every page and every feature, ask whether it is the best feature for that page and how to make it ten times better. No dead rows: wire a feature, or hold the board until it is live — a board of "not connected yet" is not a feature. The Nov 17 gold wisdom bar is the standard of cleanliness every board reads to.

## Owed from this dictation

This review is the NEXT round on the same calendar file, after the border eye-fix round finishes first (coordinator 0b796295, already running). It absorbs the queued defects follow-on (hero date, timeline cut-off, scrollbar — now expanded by the September finding and everything in the review). One checklist, one file, one round. Staged only, no PR/merge/live. The eye proves every item on the final staged bytes; Shawn's eye is the final gate. Frame quality at max rides the frame-fix round (item 5, already sent to its coordinator).

**One date, the right date, everywhere — and every feature ten times better, or it waits.**
