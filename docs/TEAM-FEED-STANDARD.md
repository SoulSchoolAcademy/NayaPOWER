# Team Feed Standard — the ultimate template for posting (Shawn, 2026-10-14)

Every post on the team coordination feed (#2537, the live board) follows this
template. Purpose: the next Naya must extract **who, what, why, what next,
and the numbers** in under 30 seconds. If she can't, the post failed.

## The rule

- **Roster names only.** Sign with your roster name (Naya Alpha … Naya Mu).
  A post signed by a non-roster name is flagged, not read. One shared login
  means names are self-asserted — the roster is the only identity that counts.
- **Numbers over adjectives.** SHAs, run IDs, comment IDs, PR numbers, honest
  scores. "Went well" is not a report.
- **One post per sign-in, one per sign-out.** No threads, no edits-as-updates.
- **30-second test.** If the next Naya can't get who/what/why/next in 30
  seconds, rewrite it.

## SIGN-IN

```
[Seat] sign-in — wave [N] [LANE X]
Seat: [roster name] · Lane: [1-5] · Wave: [N]
Mission: [one line — the single objective]
Bullseye: [what "done" looks like, one line]
Tip verified: [SHA, read live this step]
```

Example:

```
[Naya Gamma] sign-in — wave 108 [LANE 3]
Seat: Naya Gamma · Lane: 3 · Wave: 108
Mission: Five-gate re-audit of PR #2540 at the live tip.
Bullseye: every gate named green/red with the exact check-run ID.
Tip verified: 59e8a9af (ls-remote, this step)
```

## SIGN-OUT

```
[Seat] sign-out — wave [N] [LANE X]
Seat: [roster name] · Lane: [X] · Wave: [N]
Verdict: [DONE / HELD / BLOCKED — one line on what happened]
Did:
- [bullet 1]
- [bullet 2]
- [bullet 3 max]
Evidence: [SHAs, run IDs, comment IDs, PR numbers — the receipts]
Score: [honest x/10 — one line why]
Next: [the single next action + who owns it]
Win + why: [the mechanism that made it work, not the luck]
```

Example:

```
[Naya Gamma] sign-out — wave 108 [LANE 3]
Seat: Naya Gamma · Lane: 3 · Wave: 108
Verdict: HELD — 4/5 gates green; `test` red is trunk-inherited (freshness DRIFT at 59e8a9af), not this PR.
Did:
- Re-ran the five-gate audit at head a77610a9 (same-step reads)
- Confirmed test red matches the trunk signature, not the diff
- Posted the gate table to the dock thread
Evidence: check-run 115562353305 (test, FAILURE 21:59:57Z); PR #2540 head a77610a9
Score: 8.0/10 — audit is airtight; holding is correct, not a defect, but nothing moved.
Next: dock re-eval after the regen PR (#2560) lands — dock lane owns it.
Win + why: caught the inherited-vs-caused distinction by diffing the failure signature against the trunk log instead of re-firing blindly — one read beat three re-runs.
```

## What NOT to post

- Jargon walls. Internal codes (t0686, WP-57, L313) mean nothing to a cold
  reader — translate or link the definition.
- Unsigned claims. "The team agreed" with no seat, no link, no ID never happened.
- Vibe reports. "Went well," "looks good," "almost there" — delete and write numbers.
- Cross-posts. Lane sign-in/out belongs on the lane feed; the live board is
  for coordination (blockers, dock decisions, standards, lessons).

## Why this exists

A feed the next Naya can't read in 30 seconds is a feed that didn't happen.
This standard is the contract version of the sign-in/out convention — same
practice, now with teeth. Scored 6.0/10 before (practice without contract);
this is the 9.0 path. The final point is mechanization: a sign-out checker
that rejects posts missing the fields, the way the receipt gate rejects PRs
missing evidence.
