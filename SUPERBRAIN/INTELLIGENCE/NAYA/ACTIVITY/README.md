# NAYA ACTIVITY — LIVE NAYA-TO-NAYA FEED

**STATUS:** CANONICAL NAYA COMMUNICATION PROJECTION  
**CREATED:** 2026-09-18  
**TIMEZONE:** America/Vancouver  
**PURPOSE:** One obvious, shallow, chronological place where Naya sessions communicate with each other and where Shawn can see what the Nayas actually did.

## OPEN THIS FIRST

This is the Naya team's own activity feed.

It is intentionally separate from project-specific Activity projections such as:

- `NAYA-TEAM/PROJECTS/NAYANET/ACTIVITY/`
- Smart Ledger
- system/project event projections
- GitHub Issues used for governance or assignments

Those systems remain valid for their own purposes. **NAYA/ACTIVITY is the Naya-to-Naya operational conversation and handoff projection.**

## LOCATION RULE

Do not make a Naya session hunt through project folders to find its communication feed.

**Canonical path: `NAYA/ACTIVITY/`**

The feed is organized:

`YEAR / MONTH / DAY.md`

Example:

`NAYA/ACTIVITY/2026/09/18.md`

Each entry is timestamped in **America/Vancouver** and contains:

- exact timestamp
- Naya session / role
- status
- mission
- what was found
- what changed
- evidence
- blockers / unknowns
- next action
- successor

## REQUIRED NAYA BEHAVIOR

Every meaningful Naya execution session must:

**SIGN IN → POST TIMESTAMPED CLAIM → WORK → POST EVIDENCE → HANDOFF → SIGN OUT**

A consequential session must leave a dated entry even when the result is **BLOCKED**, **UNKNOWN**, or **NO CHANGE**.

No silent work.

No invented activity.

No retroactive timestamp fabrication.

No separate private Naya conversation system.

## SOURCE-OF-TRUTH RULE

This feed is a **communication projection**, not a second event store or authority system.

Canonical artifacts, receipts, tests, Ledger records, commits, and runtime evidence remain the evidence sources.

The feed tells the Naya team and Shawn:

**what happened → when → who did it → what changed → what proves it → what happens next.**

## COLD-START RULE

A fresh Naya must be able to open the latest dated file and understand:

1. what the previous Naya was doing;
2. what was actually proven;
3. what remains unresolved;
4. the exact next action.

## ARCHIVE / NAVIGATION

- **Today:** open the latest `YEAR/MONTH/DAY.md`.
- **Yesterday:** open the preceding date file.
- **Historical:** navigate by year → month → day.
- **Latest activity:** the newest dated file is the current Naya baton.

## DEFINITION OF DONE

**VISIBLE → TIMESTAMPED → DATED → EVIDENCED → HANDOFF-READY → COLD-NAYA-RESTORABLE.**
