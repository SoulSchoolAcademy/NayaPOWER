# The Merge Can Discard the Branch's Re-Stamp — Verify the Merged Tree Against Both Parents

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01445-the-merge-discarded-the-branch-re-stamp
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 19:38 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/gap-t0032-bisect-evidence-20261015.md` (Naya Clarity Narzan, Lane 10 Librarian, 2026-10-15 ~19:17–19:35 PDT) — independent second-seat re-run of parent t0032's five-commit drift-attribution check, detached worktrees at exact full SHAs.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The heal branch #2448's index re-stamp was verified green at the branch head — and it did not survive the merge. The second-seat bisect ran `tools/regenerate_brain_index.py --check` at five exact-SHA worktrees: `d998cac4` (#2437) exit 0, `bf16b098` (#2444) exit 0, `715bce27` (#2446) DRIFT, `6a5aaed46` (#2448 merge) DRIFT, live tip `9f80e8ec` exit 0. So #2446 introduced the drift (its diff: `BRAIN/CURRENT-MISSION-STATE.md` +34/−6 plus ledger files, zero index files touched), and the #2448 merge — the supposed heal — inherited it. The byte proof: `git rev-parse <merge>:<path>` for `BRAIN/REAL-TREE.json`, `BRAIN/REAL-TREE.md`, and `BRAIN/NAYAPOWER-BRAIN-INDEX.json` → merge tree == first parent, ≠ second parent, on all three; first-parent diff `715bce27..6a5aaed46` over `BRAIN/` → empty. The merge resolved the index paths to first-parent bytes, byte-identically discarding the branch's own re-stamp. Green at the branch head proved the branch; it said nothing about what the merge kept.

## 🩷 HUMAN NOTE

A branch is a rehearsal; the merge is the show. Imagine your team rehearses a play perfectly — then on opening night the stage manager hands the actors the script from the old production instead of the revised one. The rehearsal being flawless doesn't mean the audience saw it. The check that matters is on what's actually on stage: after every merge, you have to look at what merged — not what the branch proved in rehearsal.

## 🟣 CHILD NOTE

Imagine you wrote a beautiful book report, and your teacher said it was perfect. But when she staples your report to the class wall, she accidentally staples the rough draft instead. Your perfect report is real — it just never made it to the wall. The lesson: always check what's actually hanging on the wall, not just what the teacher praised.

## 🔵 GRANDMA NOTE

It's like getting a haircut you're happy with in the mirror, and then the photo your friend posts shows the old hair. The photo is what everyone else sees — the mirror doesn't travel. After a merge, the merge commit is the photo; the branch was only the mirror. Always check the photo.

## 🟠 NAYA NOTE

Apply this every time an index-layer heal branch merges: (1) never accept branch-head CI green as proof the re-stamp survived — the merge commit is a different object; (2) run the check tool AT the merge commit (detached worktree at the exact merge SHA, commit-exact bytes); (3) compare the merged tree's index bytes against BOTH parents with `git rev-parse <commit>:<path>` — merge == p1 / ≠ p2 on a path the branch touched means the re-stamp was discarded in content resolution; (4) a first-parent diff over the index paths that comes back empty at a merge is the signature of the discard; (5) the bisected attribution matters too: five-commit 0/0/1/1 exit patterns name the introducing commit (#2446 here), not the healing commit.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "merge_discards_branch_re_stamp",
  "evidence": {
    "bisect_bundle": "hidden_files/gap-t0032-bisect-evidence-20261015.md (Naya Clarity Narzan, Lane 10, 2026-10-15 ~19:17-19:35 PDT; detached worktrees at exact full SHAs; second-seat independent re-run)",
    "exit_pattern": "d998cac4 (#2437) exit 0; bf16b098 (#2444) exit 0; 715bce27 (#2446) DRIFT; 6a5aaed46 (#2448 merge) DRIFT; 9f80e8ec (live tip) exit 0 — identical to parent t0032",
    "introducing_commit": "#2446 diff bf16b0987..715bce27d: BRAIN/CURRENT-MISSION-STATE.md +34/-6, LEDGER files, zero index files touched — drift introduced here",
    "merge_discard_proof": "git rev-parse <merge>:<path> for BRAIN/REAL-TREE.json, BRAIN/REAL-TREE.md, BRAIN/NAYAPOWER-BRAIN-INDEX.json: merge == first parent (916b9271b), != second parent (d5015eb7) on all three; first-parent diff 715bce27d..6a5aaed463 over BRAIN/ -> empty",
    "confirmation": "parent t0032's verdict and mechanism independently re-derived on exact bytes — CONFIRMED, gap CLOSED"
  },
  "rule": "the_merge_can_discard_the_branch_re_stamp_verify_merged_tree_vs_both_parents",
  "procedure": [
    "after an index-layer heal branch merges, run the check tool AT the exact merge SHA in a detached worktree, never trust branch-head green",
    "compare merged-tree index bytes against both parents with git rev-parse <commit>:<path>",
    "treat merge == p1 / != p2 on a branch-touched index path as a discarded re-stamp and re-open the heal",
    "bisect attribution across the commit range with 0/0/1/1 exit patterns to name the introducing commit separately from the healing commit"
  ],
  "decision_change": "the next time an index re-stamp branch merges, the default acceptance check runs on the merge commit and byte-compares the index layer against both parents — a green branch head is no longer accepted as proof the re-stamp survived",
  "falsifiability": "if a future merge's index bytes equal the second parent's bytes (re-stamp survived), the claim is bounded to this instance; if drift at the merge is re-attributed to a different mechanism on byte proof, the finding is falsified",
  "mechanism": "git content-merge resolved the index paths to first-parent bytes: the branch's re-stamp edits did not survive merge content resolution, so the merged tree's index layer is the pre-heal first-parent layer byte-identically. Head-level proof cannot transfer across a merge that changes the bytes",
  "related": ["SN-01184 (FM#44 merge-commit receipt-blindness — certify the merge commit, not the PR head)", "CANDIDATE 402 (pin everything you compare against)"]
}
~~~
