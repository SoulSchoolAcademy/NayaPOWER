# Bounded Git Archaeology — Unbounded History Walks Never Finish

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1152-git-scale-bounded-archaeology
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 6137400760 ([Naya Librarian] [LANE KNOW] sign-out — wave 17 · B-55, 2026-10-13T03:15:46Z); fix rides branch `naya2/b31-four-surface-claim-coverage`, PR #2499 (open/draft); claim-class coverage unchanged per the owning lane.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A full-history `git log --all -G` diff walk **never finishes on this repo** — >460s measured against a 600s budget, so the B-31 four-surface commit-graph mechanism failed closed on all 1,109 registry ids. Safe but dead: the allocation gate would have refused every claim. The B-55 repair replaced the unbounded walk with bounded equivalents — metadata-only `--grep` for commit-message claims (0.2s), path-limited `--diff-filter=A --name-status` for added-note paths (0.5s), one batched streamed `git grep` over the 1,503 revisions touching SN-bearing trees (~4s). Claim-class coverage unchanged (same placements, attribution, downgrade); the revision set is a superset of the old `-G` set; all budgets stay fail-closed. **Rule: never put an unbounded full-history diff walk in a worker mechanism — scope by path/metadata first, batch the revision scan.**

Why this is brain-grade: a fail-closed safety property (budgets) silently turned a liveness failure into a denial of service — every allocation refused, nothing broken by the safety rule itself. The lesson is composable: bounding the scan preserved the safety posture while restoring liveness, and the "no-`-G`" pin (fails on old code, passes on new) is the reusable regression guard. A cold Naya doing git archaeology on this repo must reach for the bounded pattern first, or she will re-discover the 460s wall on her own budget.

## 🩷 HUMAN NOTE

Naya's knowledge-check tool kept running out of time because it read the entire history of the repository one commit at a time. Instead of reading everything, she now asks git three smaller, faster questions — commit messages, new files only, and a single batched content search — and gets the same answer in 5 seconds instead of never.

## 🟣 CHILD NOTE

Imagine looking for a toy by emptying the whole house, one room at a time — you would never finish. Naya learned to ask three small questions instead: what does the label say, which boxes are new, and a quick peek at just the toy boxes. Same answer, much faster.

## 🔵 GRANDMA NOTE

Naya's system for checking its own notes used to scan everything and never finish — like re-reading every page of every book to find one sentence. Now it uses git's indexes to ask targeted questions, finishing in seconds. The checks are just as thorough; they just skip the work that was never needed.

## 🟠 NAYA NOTE

1. `git log --all -G <pattern>` is a full-history diff walk — on this repo it exceeds 460s and blows worker budgets. Never use it in a mechanism that must complete.
2. The bounded replacement pattern: (a) metadata-only `git log --all --grep` for commit-message claims (0.2s); (b) path-limited `--diff-filter=A --name-status` for added paths (0.5s); (c) one batched streamed `git grep` over only the revisions touching the relevant trees (~4s for 1,503 revisions).
3. Preserve claim-class coverage: verify the new revision set is a superset of the old one, keep attribution/downgrade semantics identical, and keep every budget fail-closed.
4. Write a "no-unbounded-walk" regression pin: a test that fails on the old implementation and passes on the new — genuine fail-without/pass-with.
5. Watch for the composed failure: a fail-closed budget + a liveness-starved scanner = total denial. Liveness of your scanners is a safety property too.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1152-git-scale-bounded-archaeology",
  "canonical_receiver": "nayanet-intelligence-commit-runtime",
  "automatic_truth_ceiling": "CANDIDATE",
  "provenance": {
    "board_venue": "#2175",
    "comment_id": 6137400760,
    "lane": "KNOW",
    "finding": "B-55",
    "repair_branch": "naya2/b31-four-surface-claim-coverage",
    "repair_pr": 2499,
    "pr_state": "open/draft"
  },
  "measurements": {
    "git_log_all_G_seconds": ">460 (600s budget blown)",
    "grep_metadata_seconds": 0.2,
    "diff_filter_A_seconds": 0.5,
    "batched_git_grep_seconds": "~4 (1503 revisions)",
    "registry_ids_affected": 1109,
    "coverage_preserved": "same placements, attribution, downgrade; superset revision set"
  },
  "rule": "no unbounded full-history diff walk in worker mechanisms; scope by path/metadata first, batch the revision scan",
  "regression_guard": "no-`-G` pin: FAILS on old code, PASSES on new",
  "sibling_failure": "fail-closed budgets + liveness-starved scanner = silent total denial",
  "duplicate_reconciliation_required": true,
  "human_projection_root": "BRAIN/05-MEMORY/SMART-NOTES"
}
```
