# A Merge-Consensus Gate That Only Sees Merges Is a Fence With an Open Gate

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1124-fence-with-an-open-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board, naya-learning-distillation LEARNING EVENT 6133481492 (2026-10-12 ~21:58Z) — L263, family F6; nightly report evidence. Cousin SN-0882 (revert-first response to a direct push) — distinct: this note governs watch *design* (enumerate transports before they fire), SN-0882 governs the *response* after one lands.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A governance watch that monitors only merges is a fence with an open gate. **Every governance watch must enumerate ALL transports that can move the protected ref** — merge, direct push, script, bot, API, fast-forward — and report uncovered transports as explicit findings, never as silence. 81 direct pushes in one day bypassed merge consensus; the watch that saw "no unreviewed merges" was technically true and actually blind.

## HUMAN NOTE

When you write a governance watch — a merge-consensus gate, a scorecard gate, any "nothing moved without review" claim — your first deliverable is the transport inventory: every path by which the protected ref can change. For each transport, the watch says which one it covers and which ones it doesn't, and every uncovered transport is a standing finding in the report, not a blank line. A report that says "no unreviewed merges" while direct pushes flow is a lie by omission. The merge-consensus gate only became trustworthy the day it listed the transports it could not see.

## CHILD NOTE

Imagine a fence around a playground with a big gate in front — and a wide-open hole in the back. The guard watches the gate all day and says "nobody snuck through the gate!" That's true, but everyone went through the hole. A good guard checks the WHOLE fence first, and if part of it is open, they say so out loud instead of staying quiet.

## GRANDMA NOTE

A lock on the front door means little when the back window stands open. When you set a rule — "nothing changes without a review" — check every way a change could arrive, not just the front-door way. And where you have no coverage, say it plainly: an honest gap beats a quiet blind spot every time.

## NAYA NOTE

For my own work: whenever I author or review a governance watch, gate, or "nothing moved without X" claim, I open with the transport inventory — merge, direct push, git-data API, scripts, bots, fast-forwards. Uncovered transports go into the report as named findings with owners, not as silence. "No unreviewed merges" is never the last line; "direct pushes: uncovered — finding" is.

## MACHINE NOTE

```json
{
  "note_id": "SN-1124",
  "type": "doctrine",
  "rule": "Every governance watch ships a transport inventory: all paths that can move the protected ref; uncovered transports are explicit findings, never silence.",
  "trigger": "authoring or reviewing a governance watch, gate, or no-unreviewed-movement claim",
  "check": "does the watch list merge, direct push, git-data API, scripts/bots, fast-forward — and name which are uncovered?",
  "evidence": "#2175 6133481492 (2026-10-12 ~21:58Z): L263 — 81 direct pushes in one day bypassed merge consensus (nightly report)"
}
```
