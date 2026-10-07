# tree=head-tree Is a Claim About the Tree, Not a Merge — GitHub's "Merged" Can Disagree with the Tree

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0539-tree-head-tree-silent-merge-corruption
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6039639981 (NAYA 4 — REPAIR REPORT: I broke main's tree, I fixed it, 2026-10-07T14:03:42Z — repair commit 955b1996 on top of 46179105; verified remote tree SHA == local rebuild tree SHA 72f44ba2)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4's three git-data fallback merges (#1702/#1701/#1700) each used tree=head-tree. Because #1701's and #1700's heads predated the earlier merges, their trees silently dropped 34 files from main — including tools/note_bridge.py, scripts/gate-learning-compounding.py, the BRAIN index updates, and tests. GitHub showed all three PRs as merged; the tree disagreed. `mergeable_state=clean` means "no conflicts," NOT "head contains base" — and tree=head-tree is only valid when the head branch's tree already contains the base tip's tree (head strictly ahead of base in content). The repair: merged the three PR heads locally with git in order (no conflicts expected across lanes), applied the resulting tree via the API as base_tree=tip + change list, and verified remote tree SHA == local rebuild tree SHA byte-for-byte (72f44ba2) with the restored paths present and brain-index --check OK (231 files). Standing rule: never trust a git-data "merge" without diffing the result against a real local merge.

## 🩷 HUMAN NOTE

Shawn — a miss I owned this morning, worth one line in your mental model: when the merge endpoint 404s and I merge via the API fallback, the tree I hand it has to be computed honestly. I passed "tree = head tree" three times in a row, which quietly dropped 34 files off main even though GitHub showed all three PRs merged. Caught it the same hour, repaired it by merging the three PR heads properly and re-applying the correct tree — verified byte-for-byte (remote tree SHA matches the local rebuild exactly). Main is whole at 955b1996. The system rule that came out of it: "clean" only means "no conflicts" — it never means the head contains the base. No action needed from you; this is in the machine now.

## 🟣 CHILD NOTE

Imagine you're stacking three towers of blocks, but the second and third towers were built from yesterday's blueprint — they're missing blocks you added this morning. If you say "just use the third tower's picture," the missing blocks disappear from the final tower even though the picture says "complete." The fix: actually stack all three towers together in the right order, take a NEW picture of the real result, and compare the picture to the real tower block by block. "No conflicts" just means the blocks don't collide — it doesn't mean nothing is missing.

## 👵 GRANDMA NOTE

A stamp that says "merged" is only as honest as the paperwork underneath it. In this case the stamp went on three times, but the filing cabinet lost 34 folders — because each filing was copied from an older drawer. The lesson is an old one, wearing new clothes: trust the contents, not the stamp. Verify by laying the real contents next to the copy and checking they match exactly, folder for folder. And remember: "clean" means "nothing clashes" — it never means "nothing is missing."

## 💜 NAYA NOTE

Note to future me: the git-data fallback merge (used when POST /pulls/{n}/merge 404s) has a hard precondition — **tree=head-tree is valid ONLY when head strictly contains base in content** (head's tree already includes the base tip's tree). Test the precondition before every fallback merge: `git merge-base --is-ancestor base_tip head_tip` on a local clone, or merge the heads locally and diff. `mergeable_state=clean` is about conflicts, not containment — never read it as "safe to copy the tree." The repair pattern when the precondition was violated: (1) `git merge` the PR heads locally in order (no conflicts expected across lanes); (2) apply the resulting tree via the API as base_tree=<current tip> + change list (blobs already exist remotely); (3) verify remote tree SHA == local rebuild tree SHA byte-for-byte and spot-check the restored paths; (4) run the index/brain check --check after the repair. A decision computed on an older tip expires when the tip moves — re-anchor at action instant (SN-0493) — and a "merge" whose result was never diffed against a real merge is a claim, not a merge (SN-040). Never push a tree you haven't verified.

## ⚙️ MACHINE NOTE

{"sn": "SN-0539", "title": "tree=head-tree Is a Claim About the Tree, Not a Merge — GitHub's \"Merged\" Can Disagree with the Tree", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-07", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "AMENDMENT-VERIFICATION", "MERGE-DECISION-INTEGRITY"], "cousins": ["SN-039", "SN-040", "SN-0493", "SN-0508", "SN-0440"], "authority": "observed episode — Naya 4 repair report on own git-data fallback merges, CANDIDATE (auto-capture, not ratified); recorded in AGENTS.md as the CORRECTION entry 2026-10-07", "evidence": {"board": ["#1354 6039639981 (NAYA 4 — REPAIR REPORT: I broke main's tree, I fixed it, 2026-10-07T14:03:42Z — three git-data fallback merges #1702/#1701/#1700 used tree=head-tree; #1701/#1700 heads predated earlier merges; 34 files silently dropped incl. tools/note_bridge.py, scripts/gate-learning-compounding.py, BRAIN index updates, tests; GitHub showed all three PRs merged; tree disagreed; mergeable_state=clean != head contains base)"], "state": "repaired main at commit 955b1996 on top of 46179105; remote tree SHA == local rebuild tree SHA (72f44ba2); note_bridge.py + compounding gate + revised spec present at tip; brain-index --check OK (231 files)"}, "doctrine": {"precondition": "tree=head-tree is valid ONLY when head strictly contains base in content — check `git merge-base --is-ancestor base_tip head_tip` before any git-data fallback merge", "clean_is_not_containment": "mergeable_state=clean means no conflicts, never 'head contains base'", "repair_pattern": "real local `git merge` of PR heads in order → apply resulting tree via API as base_tree=<tip> + change list → verify remote tree SHA == local rebuild tree SHA byte-for-byte → spot-check restored paths → index --check", "never_diff_never_merge": "a git-data 'merge' never diffed against a real local merge is a claim, not a merge (SN-040); verify the instrument (SN-0341 family)"}}
