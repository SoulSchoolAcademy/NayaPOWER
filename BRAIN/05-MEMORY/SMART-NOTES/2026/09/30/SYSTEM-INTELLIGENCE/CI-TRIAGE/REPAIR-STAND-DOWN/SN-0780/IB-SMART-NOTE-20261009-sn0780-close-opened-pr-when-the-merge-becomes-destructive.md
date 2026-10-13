# Close the Opened PR When the Merge Becomes the Destructive Act — Byte-Verified Supersession

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0780-close-opened-pr-when-the-merge-becomes-destructive
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6082386099 ([NAYA 4 — DRIVE LOOP] #1854 closed as superseded + 3-link finding for brain-build, 2026-10-09T13:57:19Z) + closing comment 6082374458 — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-0508 sets the stand-down bar at pushed-vs-unpushed: an unpushed repair costs nothing to abandon. The #1854 case closes the harder case — an **already opened, unmerged PR**. Naya 4's registry-repair PR #1854 was open and legitimate at open time. Byte-verification on tip `9f2e3db5` showed the owning lane's canonical ingestion (#1959/#1961) had since restructured 18 of the PR's 21 target entries (`smart_link: null`, ACTIVE). Merging #1854 would no longer heal — it would **revert the owning lane's canonical artifact**. The lesson: a repair that would revert the owner's canonical state is not a repair; closing unmerged is the repair. The same byte-verification discipline that justified the PR at open time now justified its closure — re-verify target state at action time (SN-0493). She closed it unmerged, and converted the repair into a witnessed finding for the owning lane: 3 entries remain SUPERSEDED with genuinely broken self-dir links, with byte-verified successors on `9f2e3db5` (SN-0360 → SN-0608, SN-0522 → SN-0614, SN-346 → SN-0589) — flagged only, never absorbed, because the index is brain-build's canonical artifact.

Why this is brain-grade: lanes racing the same seam will sometimes publish before the seam moves under them. The temptation is to merge the published work anyway ("it's already open, it's my repair"). This note names the inversion: once the owner's canonical artifact changes the targets, **the merge itself becomes the destructive act** — and the most expensive thing you can do is merge a fix that unfixes. Closing unmerged costs nothing; merging a reverter breaks canonical state and poisons another lane's heal path.

Rule for a cold successor: **re-verify your open repair PR's targets against the live tip at action time; if the owning lane's canonical artifact has changed them, close the PR unmerged — the merge is now the destructive act. Convert the repair into a witnessed finding (exact successors, byte-verified) for the owning lane.** Pairs with SN-0508 (which covers the unpushed case) and SN-0236 (one repair per RED class).

## 🩷 HUMAN NOTE

Shawn — your lanes keep doing the hard right thing. Naya 4 had an open registry-repair PR (#1854), fully legitimate when opened. Then the owning lane's canonical work restructured 18 of its 21 targets. She byte-verified this on the live tip — and instead of merging her already-open PR, she closed it unmerged, because merging it now would have reverted the owner's canonical artifact. The merge itself had become the destructive act. She converted the effort into a finding instead: the 3 entries that genuinely still need healing, with exact successor links byte-verified on the tip, flagged to the owning lane. Rule: an open PR is not a commitment to merge — when the targets move, closing unmerged is the repair.

## 🟣 CHILD NOTE

Imagine you're halfway through fixing a puzzle, and while you're working, someone else fixes it a different, better way — and your remaining pieces would actually undo their fix. The smart move isn't to jam your pieces in anyway because you already started. It's to put your pieces down and point at the three spots that still need help. That's what happened: the PR was already open (like pieces already on the table), but merging it would have broken the good fix. So she closed it and just pointed at what still needed help. Closing isn't losing — merging a breaker is losing.

## 👵 GRANDMA NOTE

Grandma, think of two people tidying the same room. One of them had a plan written on a notecard and was halfway through it. The other finished the room in a better arrangement. The first person checked carefully — and instead of finishing her old plan (which would have messed up the new arrangement), she threw the notecard away and just wrote down the three things that still needed doing, handing that list to the person who owns the room. The lesson: a plan that was right yesterday can become wrong today — when it would undo someone's good work, you cancel the plan, not the good work.

## 🟣 NAYA NOTE

Operational rule, extending SN-0508 to the published case: (1) before ANY merge of a repair PR, re-verify its targets against the live tip — never trust open-time state (SN-0493); (2) if the owning lane's canonical artifact has restructured the targets, CLOSE the PR unmerged — merging it would revert canonical state and is now the destructive act; (3) convert the repair into a witnessed finding: exact successor paths, byte-verified on the tip, flagged to the owning lane; (4) never absorb another lane's canonical artifact — flag, don't fix. An open PR is a proposal, never a commitment. Closing unmerged costs nothing; merging a reverter breaks the seam and the owning lane's trust.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0780",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-STAND-DOWN",
  "doctrine": "close-opened-pr-when-the-merge-becomes-destructive",
  "rule": "Re-verify an open repair PR's targets against the live tip at action time; if the owning lane's canonical artifact has changed them, close the PR unmerged — the merge itself is now the destructive act. Convert the repair into a witnessed, byte-verified finding for the owning lane.",
  "failure_mode": "merging an already-open repair PR after the seam moved, reverting the owning lane's canonical artifact; treating an open PR as a commitment to merge",
  "checks": [
    "repair PR targets re-verified against live tip before any merge action",
    "if targets restructured by owning lane, PR closed unmerged (not merged)",
    "witnessed finding delivered: exact successor paths, byte-verified on tip",
    "owning lane's canonical artifact never absorbed or reverted"
  ],
  "pairs_with": ["SN-0508", "SN-0236", "SN-0493"],
  "provenance": {
    "board": "#1354",
    "comment_ids": [6082386099, 6082374458],
    "author": "SoulSchoolAcademy",
    "seat": "Naya 4",
    "timestamp": "2026-10-09T13:57Z"
  }
}
