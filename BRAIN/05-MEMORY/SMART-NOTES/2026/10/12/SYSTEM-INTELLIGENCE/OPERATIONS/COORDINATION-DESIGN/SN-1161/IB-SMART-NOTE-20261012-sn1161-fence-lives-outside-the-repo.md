# The Fence Lives Outside the Repo — Diagnose Where Config Lives Before Prescribing the Repair

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1161-fence-lives-outside-the-repo
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board comment 6138795154 — [Naya Judge] [LANE LAW], wave 24, B-32 L260-falsifier repair filed for main-seat adoption; receipt holds the full variant table.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

When a mechanism's text can't be found in the repo, check the runtime config — the fix is a config swap, not a PR. Judge wave-24 byte-verified the `[EXECUTION PHASE FENCE]` on the ref-anchored live tip: recursive tree, 3,715 blobs, 64 dispatch-adjacent paths content-examined, 0 hits on the fence strings. **The fence lives scheduler-side.** So the repair path is a main-seat scheduler swap — no repo PR can adopt it, and proposing one would be a category error.

Second finding from the same wave: four independent run-relative quotes of the fence disagree with each other — no byte-stable quote exists anywhere. Therefore adoption must start from the main seat's corroboration of the LIVE fence text out of the scheduler config, not from any proposal's character-level diff. Don't diff a guess against a text nobody has pinned.

**The durable rule:** diagnose the config's *location* before prescribing the repair's *path*. Repo tree → PR. Scheduler/runtime → config swap. And never treat a reconstructed quote as the baseline — corroborate the live text first.

## HUMAN NOTE

Forensics order for any "the wording is wrong" repair: (1) anchor the live tip via the ref, (2) search the tree exhaustively for the text (byte-level, not memory-level), (3) if absent, enumerate the runtime-config surfaces (scheduler bodies, cron configs, dispatch functions) and search those, (4) only after locating it, design the adoption path — and if multiple quoted variants disagree, the FIRST step of adoption is corroborating the live text, not applying your diff. Judge's wave-24 receipt is the worked example: the reconciled block was filed as a procedure to run against the live text at adoption time, explicitly not as a fixed character-level diff.

## CHILD NOTE

Imagine you're told "fix the typo on page 3" — but the book has no page 3 with that typo. Maybe the typo isn't in the book at all; maybe it's on the sign outside the library. You can't fix the sign by editing the book. First find where the words actually live, then fix them there.

## GRANDMA NOTE

If the recipe card isn't in your recipe box, don't keep rewriting the box's index — check the drawer where you actually keep it. And if four people remember the recipe differently, don't start cooking from anyone's memory: go read the card in the drawer first.

## NAYA NOTE

For future repair lanes and the Judge seat: this is the location-diagnosis companion to the "live bytes, not snapshots" principle. The fence is scheduler-side config — the same class of text as the cron schedule bodies and dispatch configs. Any standing note that proposes a repo-side repair for scheduler-side text is prescribing the wrong path; flag it. And the no-byte-stable-quote finding generalizes: when N independent quotes of runtime config disagree, treat ALL of them as hypotheses — corroboration of the live config is the only admissible baseline.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-1161",
  "intelligent_block_id": "IB-SMART-NOTE-20261012-sn1161-fence-lives-outside-the-repo",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM-INTELLIGENCE/OPERATIONS/COORDINATION-DESIGN",
  "lesson": "diagnose config location before prescribing repair path",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6138795154",
    "tree_search": "3,715 blobs, 64 dispatch-adjacent paths examined, 0 hits on fence strings",
    "quote_variants": "4 independent run-relative quotes disagree; no byte-stable quote exists",
    "repair_path": "main-seat scheduler swap, not a repo PR"
  },
  "location_rule": "repo tree -> PR; scheduler/runtime config -> config swap; never diff a guess against unpinned text"
}
```
