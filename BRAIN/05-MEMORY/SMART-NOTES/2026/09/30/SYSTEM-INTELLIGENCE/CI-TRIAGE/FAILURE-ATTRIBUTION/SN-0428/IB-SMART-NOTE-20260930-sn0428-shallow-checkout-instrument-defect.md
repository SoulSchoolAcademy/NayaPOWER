# The Shallow Checkout Lies — a git-log Scan Instrument Is Checkout-Shape-Sensitive, So PR-Only CI Reds Are Instrument Defects, Not Content

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0428-shallow-checkout-instrument-defect
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6008665626 (Naya 4 drive-loop 20:13 PDT tick, 2026-10-06T03:21:40Z — RED classification) + 6008731516 (Naya 2 relay, 2026-10-06T03:28:14Z — independent live-bytes confirmation); SoulSchoolAcademy/NayaPOWER PR #1229 Kernel Tests.

## ✦ IN A NUTSHELL

PR #1229's Kernel Tests fail 2 provenance tests that pass on every main push — not because the tree is broken, but because the instrument measures the checkout shape, not the tree. Both tests scan `git log HEAD --name-only -- .naya/capture BRAIN/05-MEMORY/SMART-NOTES`. PR CI checks out a shallow (depth-1) merge ref; on a shallow merge, `git log --name-only` emits the ENTIRE tree (30 + 423 files) instead of the tip commit's diff (30 + 41 files on main push). Same tests, same tree content — different measurement. The ~380 "vanished" ids the failure text reports as destroyed are actually historical BRAIN markdown docs never projected into `.naya/capture/*.json` or the 39-entry registry: UNINGESTED (pipeline lag), not VANISHED. Classification: instrument defect, platform class — not fixable from PR content. Correct posture: freeze the merge pipeline (Scorecard Law — no merge without green), decline absorbing the anomaly (no bulk-registering ~340 ids to silence the tripwire, per SN-0420), and route the repair propose-first to the owning lane — the guards live in `.github/workflows/`, a human-only gate (Shawn's 2026-10-05 batch).

## HUMAN NOTE

Shawn: two red checks on #1229 are lying to us. The tests scan the git history for Smart Note provenance, but CI on pull requests checks out only a shallow snapshot — one layer deep. On a shallow snapshot the scan tool reports the whole filing cabinet as "changed," so ~380 old documents look like they vanished. They didn't vanish — they were just never filed into the registry (the filing backlog, not a fire). Naya 4 proved this by running the same scan locally: shallow checkout = 453 files listed, full push checkout = 71. Same content, different ruler. The fix has to go in the ruler itself — make it detect real deletions (`--diff-filter=D`) or count what's actually on disk — and that ruler belongs to your 10-05 guards batch, so nobody touches it without your word. Until then, every open PR stays frozen by design: no merge without green.

## CHILD NOTE

Imagine counting how many pages changed in a book by looking at the bookmarks. If someone hands you the whole book (every page bookmarked), you count 453. If someone hands you just the last chapter, you count 71. The book is exactly the same — you were just handed different-sized piles. Always check which pile you got before deciding the book is broken.

## GRANDMA NOTE

It's like weighing yourself on two different scales. The new scale is off by 30 pounds — not because you gained weight, but because the scale is broken. The tests didn't weigh the actual code; they weighed the shape of the box it arrived in. Fix the scale; the code was fine.

## NAYA NOTE

Sisters: this is the FAILURE-ATTRIBUTION family's newest member — SN-0341 taught us the harness lies about disk, SN-0329 taught us to reproduce in the target environment, and now SN-0428 teaches us the CI checkout lies about the tree. The exact trap: a test that passes on every push and fails on every PR is almost never a content bug — it is a checkout-shape bug. The reproduction recipe is one line: run the same scan on a depth-1 merge checkout vs the push checkout and compare the file counts (453 vs 71 here). The posture discipline matters more than the diagnosis: Naya 4 declined three wrong repairs in the same tick — bulk-registering ~340 un-ingested ids to make the numbers agree (SN-0420's "never absorb the anomaly to silence the tripwire"), editing Shawn's 10-05 guard batch unilaterally, merging red. Naya 2 independently confirmed the classification on live bytes and confirmed the freeze stays clean. A cold Naya seeing "PR red, main green" on any `git log`-shaped test should reach for this note before touching any content.

## MACHINE NOTE

```json
{
  "sn": "SN-0428",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "taxonomy": "SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION",
  "extends": ["SN-0329", "SN-0341", "SN-0420"],
  "lesson": "A git-log-scan instrument is checkout-shape-sensitive: on a shallow depth-1 merge checkout, `git log HEAD --name-only` emits the entire tree, inflating provenance/drift counts. Same tree, same tests, different measurement — classify as instrument defect (platform class), not content defect. Under the Scorecard Law this freezes every open PR merge by design; repair the instrument propose-first via the owning lane, never absorb the anomaly.",
  "evidence": {
    "board": "#1354 comment 6008665626 (Naya 4 20:13 PDT tick, 2026-10-06T03:21:40Z) + comment 6008731516 (Naya 2 relay, 2026-10-06T03:28:14Z)",
    "failing_tests": [
      "test_no_smart_note_id_can_vanish_without_a_lifecycle_record (~380 ids 'vanished')",
      "test_live_repository_drift_never_grows_per_class (published_pages_without_registry_entry 1 -> 383)"
    ],
    "pr": "SoulSchoolAcademy/NayaPOWER#1229 (draft, head 683bfae8)",
    "mechanism": {
      "scan": "git log HEAD --name-only -- .naya/capture BRAIN/05-MEMORY/SMART-NOTES",
      "shallow_merge_checkout": "30 + 423 files emitted (entire tree)",
      "main_push_checkout": "30 + 41 files emitted (tip diff only)"
    },
    "true_state_of_ids": "UNINGESTED (pipeline lag — historical BRAIN .md never projected into .naya/capture/*.json or the 39-entry registry), not VANISHED"
  },
  "gate": "When a test passes on pushes and fails on PRs: (1) re-run the instrument on both checkout shapes before touching content; (2) classify instrument-vs-content FIRST — code changes never precede classification; (3) if the instrument is checkout-shape-sensitive, freeze merges (Scorecard Law) and route propose-first to the owning lane; (4) declined repairs: bulk-registration to silence the count (SN-0420), unilateral guard edits, merging red.",
  "proposed_repair": "Make the scan checkout-shape-independent: detect real deletions via `git log --diff-filter=D`, count BRAIN .md presence as 'on disk', or pin the drift baseline per checkout shape. Owning lane: Shawn's 2026-10-05 guards batch (.github/workflows/) — human-only gate.",
  "ratification": "NOT_RATIFIED — only Shawn ratifies"
}
```
