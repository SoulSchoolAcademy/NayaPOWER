# In-PR Regen Evidence Expires at Merge — the Merge-Tip Regen Law

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0821-in-pr-regen-expires-at-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6089228800, 6089244710, 6089299519 (2026-10-09T21:04–21:09Z); merge scorecard 6089133219.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A PR can score merge-green with "index regenerated in-PR, bytes verified identical" and still land a stale brain index on the merge tip. The merge itself combines two index states — the base's committed index and the head's regenerated index — and if nobody re-runs the generator on the exact merge tip after resolution, the tip inherits a state the tool never produced. Observed twice: PR #2023's drift (tick 146) and PR #2056's drift (tick 151, tip `185c8beb`, Kernel Tests + Governed Production Promotion RED). The law: for generated-index artifacts, regen + `--check` must run on a clean worktree at the exact merge tip. In-PR regen evidence expires at merge. This refines SN-0395 (the generator reads the committed HEAD — so the HEAD it must read is the merge commit itself) and SN-0238 (recompute from the live tree, not the PR blobs).

## 🩷 HUMAN NOTE

Think of the brain index like a table of contents at the back of a book. PR #2056 added a chapter and reprinted the table of contents for its own draft — perfectly correct for the draft. But merging pastes the new chapter into the full book, and the table of contents at the back of the book still lists the old page numbers. The robots caught it: the nightly test that regenerates the table of contents from scratch and compares failed, twice — once for PR #2023, once for PR #2056. The scorecard that approved #2056 even claimed the index was regenerated and verified — it was, but on the draft, not on the merged book. The lesson: after every merge that touches an index file, re-run the index generator on the exact merged result and check it passes. A green check on the draft is not a green check on the book.

## 🟣 CHILD NOTE

You built a Lego set and counted all the pieces — everything's there, great. Then your friend added their Lego set on top of yours. The piece-count you did on YOUR set doesn't tell you the count of the combined set. You have to count again after combining. Merging two code changes is the same: count the pieces again after the merge, every time.

## 🔵 GRANDMA NOTE

A recipe tastes right when you test the final dish, dear, not just the ingredients. The index is the final dish — after the merge stirs everything together, taste it again. Test the merged result itself, not the pieces that went in.

## 🟠 NAYA NOTE

1. Generated artifacts (brain index, REAL-TREE.json/md) are functions of the exact commit tree. A merge creates a new tree; therefore any regen evidence from the PR head describes a tree that no longer exists as the tip. This is the SN-0493 expiry rule applied to generated artifacts: the decision (regen OK) expired when the tip moved (the merge).
2. The repair pattern, twice validated: run `tools/regenerate_brain_index.py` on a clean worktree at the exact merge tip, verify `--check` passes, land the result (PR #2057 did this with positive + negative controls: pytest 1931/0, node 579/0, `--check` OK on repaired bytes / DRIFT on unrepaired).
3. The tripwire works and must stay: the CI step "Verify generated Brain index has no drift" caught both incidents (PR #2023, PR #2056). SN-0240 holds — the repair lane does not touch another lane's merge; the owning lane lands the regen, watchers verify the next tip.
4. Scorecard discipline: "index regenerated in-PR, bytes verified identical" on a merge scorecard must name the tree it describes. If it names the head, it is stale evidence at merge time — score accordingly, or hold for the post-merge regen.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261009-sn0821-in-pr-regen-expires-at-merge",
  "automatic_truth_ceiling": "CANDIDATE",
  "captured": "2026-10-09",
  "rule": "merge_tip_regen_law",
  "statement": "regen_and_check_must_run_at_exact_merge_tip_for_generated_artifacts",
  "evidence": {
    "incidents": [
      {"pr": "#2023", "tick": 146, "caught_by": "ci_tripwire_verify_generated_brain_index_no_drift"},
      {"pr": "#2056", "tick": 151, "tip": "185c8beb", "red": ["Kernel Tests", "Governed Production Promotion (fail-closed behind it, SN-0438)"]}
    ],
    "board": ["#1354/6089228800", "#1354/6089244710", "#1354/6089299519"],
    "merge_scorecard": "#1354/6089133219 (claimed in-PR regen; merge still landed drift)",
    "repair_pr": "#2057 (regen at exact tip 185c8beb, --check OK)"
  },
  "procedure": {
    "worktree": "clean",
    "head": "exact_merge_commit_sha",
    "command": "python tools/regenerate_brain_index.py --check",
    "on_drift": "regenerate_at_tip_and_land_as_followup",
    "lane_boundary": "owning_lane_lands_regen__watchers_verify_next_tip__never_touch_another_lanes_merge_SN-0240"
  },
  "refines": ["SN-0395", "SN-0238"],
  "extends": "SN-0493 (decision expiry applied to generated-artifact evidence)"
}
~~~

## 🟢 LEARNING LESSON

Green evidence computed on a tree that no longer exists is not evidence about the current tree — it is a photograph of the past. Twice in one week, a green scorecard's in-PR regen claim was true about the head and false about the tip, and only the mechanical CI tripwire noticed. The fix is not more careful humans; it is a standing mechanical rule: the merge tip gets its own regen, every time, or the tip is RED until it does.

## 🟡 WHAT IT MEANS

Any merge touching generated-index artifacts must budget a post-merge regen run at the exact tip. Scorecards that cite in-PR regen for such merges cite expired evidence. The CI drift tripwire is the last line of defense and must never be weakened to make a red go away.

## 🟨 HOW TO APPLY / HOW TO USE

Merge lands touching BRAIN index files → check out the exact merge commit on a clean worktree → run `python tools/regenerate_brain_index.py --check` → if DRIFT: regenerate, verify `--check` passes, land as follow-up commit (owning lane) → watch the next tip for the regen landing before claiming green.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-0395 — regen reads the commit: the commit it must read is the merge commit
- **REFINES** → SN-0238 — recompute the index from the live tree, not the PR blobs
- **EXTENDS** → SN-0493 — a decision (regen OK) expires when the tip moves
- **SUPPORTS** → SN-0240 — never touch another lane's merge; the owning lane lands the regen
- **GOVERNS** → every merge of an index-touching PR

## 🧾 PROOF / PROVENANCE

- #1354 comment 6089228800 (2026-10-09T21:04:14Z, pipeline-monitor): NEW failure on main — Kernel Tests RED, brain index drift from PR #2056 merge; likely causes: regen ran on a pre-merge base, or the merge combined two index states without a fresh regen after resolution.
- #1354 comment 6089244710 (2026-10-09T21:05:17Z, Naya 4 PROVE-driver): classified PROCESS DEFECT, built minimal repair, opened PR #2057 (`naya4/prove-regen-brain-index-20261009`); independent recomputation on tip bytes: pytest 1931/0, node 579/0, `--check` OK on repaired bytes / DRIFT on unrepaired.
- #1354 comment 6089299519 (2026-10-09T21:09:12Z, Naya 4 CONNECT-driver): healed PR-introduced drift via mechanical `regenerate_brain_index.py`.
- #1354 comment 6089133219 (2026-10-09T20:57:41Z, merge scorecard): scored #2056 A(8.7) "merge now" with "index regenerated in-PR, bytes verified identical" — still landed drift.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: the mechanical law is twice-observed and the repair pattern is verified, but only the director ratifies. The law does not claim every merge needs a regen — only merges that touch generated-index artifacts. Whether the regen should be a blocking merge-time gate versus a follow-up convention is not decided here; the current standing is follow-up + CI tripwire as the backstop.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every seat merging an index-touching PR runs the regen at the exact merge tip and lands it before claiming green. Success is behavioral: the drift tripwire goes quiet not because it was silenced but because merges stop producing drift.
