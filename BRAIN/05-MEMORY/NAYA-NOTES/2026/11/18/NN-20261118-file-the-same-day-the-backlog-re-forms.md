# File the Same Day — The Backlog Re-Forms Overnight

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261118-file-the-same-day-the-backlog-re-forms.md · Naya Note · 2026-11-18 03:14Z**

**Category:** Operations — the filing loop

## What it is

The filing push finished, 03:14:30Z: 165 pairs filed, every one verified in-tree by blob sha, queue 165 → 0. The SN-3161 duplicate resolved — run 280's train-the-army keeps SN-3161, run 281's on-top-of-things moved to SN-3269, the old file deleted. And the queue had already refilled — runs 291–292, 22 pairs, not in this push. Filing has to keep up the same day, or the backlog re-forms.

- **THE LIVE CAVEAT, DELIVERED TO SHAWN WITH THE COUNT:** filed in GitHub + recorded for sync — NOT live on nayanet.app until the publication repair lands; do not claim any note live.
- **OPEN ITEMS:** the organize hook + build_index.py are still EPERM-blocked (INDEX.md is 0 bytes, regenerates deterministically); the next push's driver range must extend to 293.

## Why it matters

One hundred and sixty-five pairs is a day of teaching that was sitting in drafts, not in the system — captured and distilled, but not yet working in the live system, which is exactly the gap Shawn named at 01:50Z when he said the loop must close. The push closed it. And before the ink was dry the queue had refilled, because the loop keeps drafting faster than the filing keeps up. Filing is not a weekly chore, it is the same day's work, or the backlog re-forms overnight and the loop is open again. Filed in GitHub is also not live on the Hub — the publication repair still stands between the tree and nayanet.app, and no note is claimed live until that repair lands.

## How to use it

File the same day as drafting — the queue is worked to zero daily, never left to re-form. The next filing push extends its driver range to cover runs 291–293 and renumbers against the fresh tree max. No note is claimed live on nayanet.app until the publication repair lands and a fresh fetch proves it. The organize hook + index rebuild recovery runs when the EPERM flake clears — build_index first, then the hook — never a blind retry into the flake.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3308 — File the Same Day — The Backlog Re-Forms Overnight*
