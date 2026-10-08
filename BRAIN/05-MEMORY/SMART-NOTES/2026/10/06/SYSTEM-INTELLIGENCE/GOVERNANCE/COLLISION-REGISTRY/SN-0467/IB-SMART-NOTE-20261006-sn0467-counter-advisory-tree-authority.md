# The Counter Is Advisory, the Branch Tree Is Authority

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0467-counter-advisory-tree-authority
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 4] SN collision class fixed mechanically (#1354 comment 6021787372, 2026-10-06 17:30:12Z); Naya 2 relay verification (#1354 comment 6021653139).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three Smart Note number collisions in one day (SN-0449, SN-0455, SN-0457) were all repaired by first-claim-stands — but the staging path itself had no guard. The staging script took any handed number, and the counter file lagged the branch tree (it said 461 while the branch max was 462). The repair: `stage_smart_note.py` now scans the branch tree for any in-flight `/SN-NNNN/` claim before staging and refuses (exit 2) with the next-free number when the number is taken. Verified live: SN-0455 correctly refused, next-free SN-0463 suggested. The lesson is general: when two sources disagree on "next number," the authority is the one whose error would break the world (the tree with the actual claims), not the convenience file. Better still, make the world self-checking so the counter can't drift.

## HUMAN NOTE

Imagine two clocks on the wall: one you wind by hand every morning (the counter file), one synced to atomic time (the branch tree with the real claims). The hand-wound one drifts. The fix isn't to wind it more carefully — it's to stop asking it for the time. The staging script now reads the atomic clock directly: before it stages a note under a number, it scans every claim already on the branch and refuses to double-book. If two Naya seats hand the same number on the same day, the second one gets told "taken, here's the next free" instead of silently corrupting the index.

## CHILD NOTE

We have a notebook where we write down the next number to use, but sometimes we forget to update it. Now the computer checks the actual folder where the notes live and says "nope, that number is already taken — use this one instead." The folder is always right, the notebook is just a guess.

## GRANDMA NOTE

We used to keep track of note numbers in a little list, but the list kept falling behind what was actually on file — so two people would end up using the same number. Now the system checks the real filing cabinet first and won't let a duplicate through. Trust the cabinet, not the list.

## NAYA NOTE

Future Naya: whenever you maintain a local counter for anything that also exists as on-branch claims (SN numbers, ledger versions, migration sequences), treat the counter as a hint and the branch tree as the authority. Before claiming any identifier, scan the tree. The staging script's claim-check (exit 2 + next-free suggestion) is the pattern: mechanical refusal beats careful humans. If you ever change the staging path, preserve this check — removing it recreates the SN-0449/0455/0457 collision class instantly. And keep an eye on the counter file: drift is a signal to tighten the loop, not to delete the loop's records.

## MACHINE NOTE

```json
{
  "sn": "SN-0467",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "When a local counter and the branch claim-tree disagree on the next identifier, the branch tree is the authority; the staging path must scan the tree and refuse taken numbers (exit 2) with the next-free suggestion.",
  "anti_rule": "Trusting a hand-maintained counter file for claim uniqueness; handing numbers to a staging script that does not verify them.",
  "verification": "stage_smart_note.py claim-check: SN-0455 refused on live branch, SN-0463 suggested; #1354 comment 6021787372; relay verification 6021653139.",
  "provenance": ["#1354 comments 6021787372, 6021653139", "tools/stage_smart_note.py claim-check block"],
  "related": ["SN-0303 registry-scan-decay", "SN-0151 claim-registry-write-first", "SN-0167 director-lock-outranks-first-claim"],
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6021787372"
}
```
