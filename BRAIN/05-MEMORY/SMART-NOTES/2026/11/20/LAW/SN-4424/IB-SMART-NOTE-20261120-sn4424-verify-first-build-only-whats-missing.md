# SN-4424 — Verify First, Build Only What's Missing

**Category:** LAW — check what's there before building; 2026-11-20 ~19:42–19:45 MST

*Paired Naya Note: NN-20261120-verify-first-build-only-whats-missing — the record of two rounds in the daily log.*

**Filed:** SN-4424 — Intelligence Loop run 440, 2026-11-20. Personal Round 4 + Dashboard sidebar-match, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Verify first. Build only what's missing. Two rounds proved it the same evening — one built a single item out of five, the other built nothing at all.

## The Lesson

Personal Round 4 (coordinator `77afab61`, takeover): the old coordinator's tip was unchanged and its message already claimed all five items done. The takeover maker verified first — and built only what was genuinely missing: one item, R3-5 pin to PERSONAL, +5/−5 lines, the only diff in the 52,322-line file. The other four were verified present, no change. Checker: 114 checks, 0 fail.

Dashboard sidebar-match (coordinator `25b72a18`): leaderboards were INVESTIGATED ONLY. The view already exists in the Hub file (LeaderboardsRoom, six boards, real ledger call, points map) — the follow-on is a data build, not a view build. Nothing built. The round's value was the investigation, not a build.

The lesson in both: the file is the truth, not the last report. A report that claims five done is checked against the bytes; a brief that asks for a view is checked against the file. What is already there is not built again.

## Why It Matters

Building what already exists is the doubling-up he corrects all week — two copies of the same thing, two places to maintain, two truths that drift apart. Verifying first is also faster than building: the Personal takeover landed a 10-line diff instead of a rebuild, and the Dashboard round spent its effort on the real gap (the data) instead of a duplicate view. And a claim that is not verified — five items "done" in a message, a tip unchanged — is how a round reports done while the page still misses an item.

## How to Use It

Before any build, verify against the file: grep the claim, read the bytes, count the lines. Build only the items the file does not have. When a brief asks for a view, check whether the view already exists — investigate before you build, and say plainly when the answer is "it already exists, the follow-on is data." Never take a prior report's word for done.

## His Order, As Recorded

> No direct dictation — the lesson is from the rounds themselves, recorded in the daily log 2026-11-20: the takeover maker "verified first and built only what was genuinely missing — one item," and leaderboards were "INVESTIGATED ONLY."

## Owed from This Dictation

- Personal Round 4 follow-on: pin lands in PERSONAL but does not yet render the note pinned at the top of the feed (isPinned 0, togglePin 0) — a follow-on build, not part of this round.
- Dashboard leaderboards follow-on is a data build, not a view build.
