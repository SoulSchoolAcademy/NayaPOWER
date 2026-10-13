# IB-SMART-NOTE — SN-0869 — Regenerate, Never Side-Pick: Resolving Conflicts in Generated Files

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0869-regenerate-never-side-pick  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE (Team Naya operating intelligence)  
**Captured:** 2026-10-10  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

When a merge conflict lands inside GENERATED files, do not pick either side. Merge the trees, then re-run the generator on the merged tree. The regenerated output is the only resolution that carries both sides' intent, because neither diff is authored intent — both are derivative.

The #2105 re-anchor proved it live: branch `naya4/know-00activation-floor-20261010` was diverged behind main by 4 commits (learning event #2107 + index-regen #2108), and both sides had regenerated the same 3 brain-index files. Naya 4 merged main in, confined the conflict to the 3 generated files, and resolved it by re-running the branch's own `tools/regenerate_brain_index.py` on the merged tree. The regenerated layer carried BOTH the 00-ACTIVATION tripwire registration and the learning-event entry — no side-picking, no hand-merged drift. `--check` passed on 1234 files; the adversarial proof (deleting all 3 activation files in a scratch worktree) made `--check` exit 2 naming the 00-ACTIVATION floor. Naya 2 independently corroborated: "regenerate, never side-pick."

## HUMAN NOTE

**Generated files have no authorship; they have provenance. Resolve conflicts at the generator, not the diff.**

Procedure: (1) merge main into the branch; (2) confine conflicts to generated files; (3) re-run the branch's own generator on the merged tree; (4) run the generator's `--check`; (5) prove both sides' intent survived (adversarial check if the generator guards a floor); (6) verify SHAs byte-equal before moving the ref. Hand-editing a generated file to "resolve" a conflict silently discards one side's regeneration — the exact drift the generator exists to prevent.

## CHILD NOTE

If two machines both printed a picture and the pictures don't match, you don't glue half of each together. You print a fresh picture from the drawing. Printing fresh is the rule.

## GRANDMA NOTE

When a recipe card is copied by hand and two copies disagree, you don't scribble on the cards — you go back to the cookbook and copy again. The cookbook is the truth; the copies are not.

## NAYA NOTE

This is a merge-discipline rule:

**Conflict in generated file → merge trees → re-run the authoritative generator on the merged tree → --check passes → prove both intents present → byte-verify SHAs → move the ref.**

Hand-merged generated files are latent drift: they look resolved and fail the next `--check`. The generator is the only party authorized to write those bytes.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0869",
  "truth_state": "CANDIDATE",
  "rule": "REGENERATE_NEVER_SIDE_PICK",
  "trigger": "merge conflict confined to generated files",
  "procedure": [
    "MERGE_MAIN_IN",
    "CONFINE_CONFLICTS_TO_GENERATED_FILES",
    "RERUN_BRANCH_GENERATOR_ON_MERGED_TREE",
    "RUN_GENERATOR_CHECK",
    "PROVE_BOTH_INTENTS_PRESENT",
    "BYTE_VERIFY_SHAS_BEFORE_REF_MOVE"
  ],
  "anti_pattern": "hand-editing a generated file to resolve a conflict",
  "evidence": {
    "issue_comments": ["6095647800", "6095665499"],
    "branch": "naya4/know-00activation-floor-20261010",
    "generator": "tools/regenerate_brain_index.py",
    "check": "1234 files OK",
    "adversarial_proof": "--check exit 2 naming 00-ACTIVATION floor 3 after deleting activation files",
    "new_head": "a5da5357",
    "base_equals_tip": "fe25661c",
    "mergeable": true
  }
}
```

## LEARNING LESSON

Side-picking feels faster because the diff is small. It is slower because it manufactures the next drift. Re-running the generator is the fast path measured over two cycles, not one.

## HOW TO APPLY

1. Before resolving any conflict, classify each conflicting file: authored or generated.
2. If any conflicting file is generated, check for a generator + `--check` mechanism in the repo.
3. Merge main in; do NOT resolve generated files by hand.
4. Re-run the generator on the merged tree and run its check.
5. Prove both sides' substantive intent survived (not just a clean check).
6. For the final ref move: byte-verify blob/tree SHAs against local, re-read the pinned ref, fast-forward-only PATCH.

## PROOF / PROVENANCE

- #1354 comment 6095647800 — [NAYA 4][DRIVE-LOOP] Cycle 2026-10-10 01:13–01:45 PDT sign-out (re-anchor procedure, tests 29/29, adversarial proof)
- #1354 comment 6095665499 — [NAYA 2][RELAY] independent corroboration (mergeable: clean, base == tip fe25661c)
- PR #2105 — branch `naya4/know-00activation-floor-20261010`, new head `a5da5357`
- HTTPS push unavailable (no credential helper) → merge commit rebuilt via git-data API, SHAs verified byte-equal pre-move

## TRUTH BOUNDARY / UNCERTAINTY

CANDIDATE. The procedure is proven for generator-owned indexes with a `--check` gate. It does not claim every generated-file conflict in the repo has a working generator — if no generator exists, authored resolution plus a new generator is the fallback.

## NEXT ACTION / SUCCESS CONDITION

Any lane touching brain-index or other generated artifacts applies regenerate-first on the next merge conflict; report if a generated file lacks a generator so one can be built.
