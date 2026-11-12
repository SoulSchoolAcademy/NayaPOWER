# Post-Merge Guardian — operator notes

`tools/post_merge_guardian.py` · workflow `.github/workflows/post-merge-guardian.yml` · law `POST-MERGE-GUARDIAN-V1`

## Why it exists

The HOUSE-FIRE LAW (Shawn, 2026-10-21): a bad landing is unmerged and
made right immediately — never noted and watched. Before this tool, the
merge watch checked *protocol* (the relay's review + scorecard watch),
one merge route's *pre-move* tree (verify_gitdata_merge_tree.py), and
nothing checked the landing itself, prepared a revert, or kept the
defect log the balance gauge reads. This guardian is that missing
layer. It extends the existing watch; it replaces none of it.

## What it does, per push to main

For every landing in the push (PR merges of any shape; direct pushes
incl. note-door landings):

| Check | Question | Defect class |
|---|---|---|
| Faithfulness | merge commit an ancestor of the live tip? every changed blob identical at PR head / merge commit / tip (later-commit touches excused)? | `FAITHFULNESS_NOT_ANCESTOR`, `FAITHFULNESS_BLOB_DRIFT` |
| New red | a tip-failing check was **present and passing** at the parent commit (L636 derivation, per workflow)? | `NEW_RED` |
| Surface | for `HUB/**` landings: `https://nayanet.live/` answers 200 with the feed present? | `SURFACE_DOWN` |

Verdicts: `OK` · `PENDING` (checks unsettled inside the wait budget,
bytes unverifiable, or a red whose before-state derived UNKNOWN —
recorded with reasons, never silent, never charged) · `ESCAPE` ·
`ESCAPE_ON_REVERT`.

**The L636 derivation (new-red charges).** Set difference is not
attribution. For every check failing after a push, the guardian
derives its before-state at the parent commit: failing → `INHERITED`
(never charged); present and completed not-failing → `NEW_RED` (the
only chargeable shape); **absent — no check-run at the parent at all —
or still pending there → `UNKNOWN`: never a charge, never a revert
preparation, never a board alarm.** Absence is not evidence the check
was green; the b1e8d514 claim (voided, correction 6347895618) and the
PR #2936 claim 6351319337 (MISCHARGE) both came from treating absent
as passing. Every record's `checks` carries the derivation
(per-workflow before/after/verdict) and both failing-set counts, so
each charge — and each non-charge — is inspectable from the log.

## On a verified escape — one motion

1. Prepare the revert: branch `guardian/revert-<merge-sha-10>`, revert
   commit, PR titled `[GUARDIAN-REVERT] …`, labeled `GUARDIAN-REVERT`,
   body = the detection evidence (the safety action's scorecard
   substitute). **The guardian never merges the revert** — it lands on
   one different-seat scorecard through the normal protocol. If the
   revert conflicts, the alarm says so and names the manual cure.
2. Post the alarm + evidence + revert link to the live board (#2793).
3. Append the record to the guardian log.

A landing that is itself a `GUARDIAN-REVERT` is verified but never
revert-prepped (loop guard); an escape on one alarms only.

## The guardian log

One JSONL record per landing on branch **`live/guardian-log`**, file
`guardian-log.jsonl`: merge SHA, PR, tier (via `tools/pr_flow_tier.py`
when present), files, verdict, defect classes, before/after failing
sets, detection latency (landing commit → detection), cure (revert PR
when prepared). The balance gauge (Balanced Machine DESIGN.ai.md §6)
derives the post-merge escape rate from this log — escapes are counted
from records, never guessed.

## Run it by hand

```bash
python3 tools/post_merge_guardian.py \
  --before <tip-before> --after <tip-after> \
  --repo-path ~/workspace/naya/repo-tests [--no-act] [--wait-secs 1500]
```

`--no-act` = detect + log only (no revert PR, no board alarm).
Exit code is 1 iff a landing escaped — the workflow run going red is
part of the alarm surface; the guardian is not a required check and
can never block the flow it protects.

## Boundaries (drawn deliberately, flagged in the PR)

- **H3 self-heal is not the guardian's hand.** `tools/auto_merge_self_heal.py`
  actuates by direct ref move, covers only FULL-AUTO-MERGE-V1
  auto-merges still sitting at the tip, and nothing calls it. The
  guardian's hand is the revert PR, for every merge, because merges
  stay protocol. If H3's owners wire their hand for their program's
  merges, the two coexist by scope: H3 for that program's tip-still-tip
  auto-merges, the guardian for everything else.
- **Surface = liveness, not freshness.** A Hub fix not yet deployed is
  the deploy lane's freshness metric (gauge), not an escape. The
  guardian charges only a dead or feed-less surface after a Hub landing.
- **Latency.** Faithfulness + surface: inside the push run (~1–2 min).
  New-red: bounded by the tip's own checks settling (25-min poll),
  else `PENDING` on the record — the honest edge of "shortly after".
