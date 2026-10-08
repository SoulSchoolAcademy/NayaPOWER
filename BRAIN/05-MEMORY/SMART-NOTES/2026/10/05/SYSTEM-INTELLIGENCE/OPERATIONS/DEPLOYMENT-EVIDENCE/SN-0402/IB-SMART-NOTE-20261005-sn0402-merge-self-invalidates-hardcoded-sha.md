# A Merge Self-Invalidates Hardcoded "Current Main" SHAs — Embedded SHAs Are Snapshots, Never Currency

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0402-merge-self-invalidates-hardcoded-sha
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6005125441 ([NAYA][MAIN FREEZE + TORCH] — independent reread caught one more subtle projection defect after #1523, 2026-10-05T23:11:18Z / 16:11 PDT).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An independent reread caught one more subtle projection defect after #1523 merged: a file merged into `main` cannot truthfully hardcode the previous `main` SHA as "current" — its own merge changes the tip. Any document landed on main that names "current main" as an embedded SHA is self-invalidating at birth: it was accurate at author time and false at merge time. The repair (PR #1524, merged → `5dd9178b`) rewrote the backlog's SHA references: embedded SHAs are evidence snapshots only — frozen context for what the author saw when they wrote it — and live references must be resolved at decision time, never read off a stored constant. The backlog no longer self-invalidates its own "current main" claim. The durable rule: **never write "current" as a constant; resolve currency at read time.**

## HUMAN NOTE

Here's a trap we caught just in time: a document was merged into the codebase that said "the current main version is X" — with X written in the text. But the act of merging it *changed* the current version. So the document was wrong the instant it landed. The fix (PR #1524): any version number written inside a document is a snapshot — "this is what I saw when I wrote this" — not a live claim. Anything that needs the *actual* current version must look it up fresh at the moment of decision, not copy it from a document. That one change removed a whole class of "the record says we're here, but we're actually there" confusion.

## CHILD NOTE

Imagine a sign nailed to a door that says "the door is painted red" — but the nail gun painted the door blue when you nailed it. The sign can't be true because putting it up changed the door. Same thing happened here: a file said "this is the current version," but merging the file changed the current version. Now the rule is: signs are allowed to say "this is what I saw when I hung the sign," but if you need to know the color of the door *right now*, you go look at the door.

## GRANDMA NOTE

A document that says "as of now, the current version is X" and then becomes part of the version history is lying to itself — because its own arrival creates version X+1. We caught this on the backlog: it embedded the old main SHA as "current," and the merge of that very fix moved main. The repair made every embedded SHA an evidence snapshot ("this is what the author saw, at this time") and made currency a lookup, not a constant. Nothing in the repo may claim "current" by copying a number — "current" is always resolved fresh, at the moment someone needs it.

## NAYA NOTE

This is the write-direction defect's twin — the read-direction defect. Even with projections that never write sources (SN-0401), a projection that *names* currency as a constant self-invalidates: author-time truth becomes merge-time falsehood because the merge renames the tip. Two safe forms only: (a) snapshot — an embedded SHA pinned to an author-time observation with its timestamp, explicitly labeled as evidence, never as "current"; (b) live resolution — a query/fetch that returns the tip at decision time. Anything labeled "current" that is neither a snapshot nor a live lookup is a latent lie. Apply this to receipts, scorecards, handoffs, and status docs: every "current main is X" statement must carry either a timestamped snapshot label or a live-resolution pointer.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0402",
  "intelligent_block": "IB-SMART-NOTE-20261005-sn0402-merge-self-invalidates-hardcoded-sha",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-05",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "never write 'current' as a constant; resolve currency at read time",
  "mechanism": "a merge changes the tip, so a document merged to main that hardcodes the previous tip's SHA as 'current' self-invalidates at birth",
  "two_safe_forms": {"snapshot": "embedded SHA + author timestamp, labeled evidence snapshot", "live_resolution": "tip resolved at decision time"},
  "repair": {"pr": "#1524", "merged": "5dd9178b", "effect": "embedded SHAs are snapshots; backlog no longer self-invalidates"},
  "evidence": {"board": "#1354 6005125441 (2026-10-05T23:11:18Z)", "freeze_sha": "5dd9178bb324f5be9727830cf009073af9f203bc"},
  "cousins": ["SN-0395", "SN-0393", "SN-0401", "SN-0388"]
}
```
