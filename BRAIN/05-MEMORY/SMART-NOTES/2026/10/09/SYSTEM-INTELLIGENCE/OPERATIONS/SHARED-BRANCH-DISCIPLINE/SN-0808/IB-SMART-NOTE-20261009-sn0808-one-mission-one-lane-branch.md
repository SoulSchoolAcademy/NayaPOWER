# One Mission, One Lane Branch — Claim Before You Commit, Halt on the Second Branch

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0808-one-mission-one-lane-branch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6086995387 (2026-10-09).
**Provenance:** #1354 6086995387 (STEWARD UPDATE — design-gate reconciliation VERDICT, 2026-10-09T18:36:37Z) — naya5/ship-design-gate-repairs4 vs naya5/ship-design-gate-repairs5 collision; roster notes recorded on the verdict. Related: SN-0671 (strict-superset lane races), SN-0493 (a decision expires when the tip moves).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two parallel seats fixed the same design gate at the same time on two different branches — and each branch held unique work the other lacked. Repairs4 passed every battery but missed two round-5 holes (comment-trick in unquoted url(), > inside quoted attributes); repairs5 closed exactly those two holes but was missing most of the round-4 repairs and crashed on malformed input. Merging either as-is would have silently lost real fixes. The reconciliation verdict: keep repairs4 as the lane, port repairs5's two fixes into it file-by-file (a squash had broken the ancestry, so no git merge was possible), re-run all four batteries, park repairs5 as the record — no deletion. The contributing cause was a roster failure: the repairs5 seat branched from the live tip and pushed a new branch name without ever posting on #1354, while the round-4 fixer was finalizing via local squash + force-push, so "the branch" was a moving target with no claim marker. Four roster rules were recorded: one mission = one lane branch claimed on #1354 before the first commit; a second branch name for the same mission = instant halt, reconcile, then continue on one branch; no pushes to the lane branch during final-head validation; no force-push squashes as the delivery mechanism on shared lanes.

## 🩷 HUMAN NOTE

Shawn — today two of our mechanics fixed the same machine at the same time, and each one fixed things the other didn't. If we'd merged either version, real fixes would have been lost silently — the good branch was missing two small blind spots, and the other branch fixed those blind spots but had lost most of the earlier repairs. We didn't merge either. We kept the strong branch, bolted the other branch's two fixes onto it, re-tested everything. The deeper fix is a rule we recorded: one job = one branch, claimed on the board before the first commit. A second branch for the same job means everyone stops, we sort it out, then continue on one branch. No more two mechanics unknowingly rebuilding the same engine.

## 👶 CHILD NOTE

Imagine two friends both build you a toy car — and each car has a part the other one is missing. If you keep only one car, you lose the other one's special part. So instead you take the best car and move the other car's special parts onto it, then test the whole thing. And the rule from now on: if two people are going to build the same thing, they raise their hand FIRST so everyone knows — nobody builds in secret.

## 👵 GRANDMA NOTE

Honey, it's like two grandkids both fixing the fence — one replaces the rotten posts, the other mends the broken gate. You don't throw either one's work away; you walk the fence together and keep both repairs. And from now on, whoever starts a chore shouts it out at the kitchen table first, so we don't end up with two people painting the same room two different colors.

## 🤖 NAYA NOTE

When lanes risk building the same mission in parallel:

1. **Claim before you commit.** One mission = one lane branch, and the claim is posted on the board BEFORE the first commit. A build with no prior claim is a protocol violation, not a fait accompli.
2. **Second branch = instant halt.** A second branch name for the same mission stops both lanes: reconcile first (decide the carrier, port the unique work), then continue on one branch. Never race to the merge.
3. **Freeze during final-head validation.** No pushes to the lane branch while a validator holds a SHA. The validator freezes a SHA; the lane freezes until the verdict.
4. **No force-push squashes on shared lanes.** History replacement orphans parallel work and erases the chain others built on — it makes "the branch" a moving target with no claim marker.
5. **Reconcile by unique work, not by branch age.** Compare exact heads on exact bytes. If each branch has unique work, neither merges as-is: pick the carrier (the one holding on every battery), port the donor's unique fixes file-by-file (when ancestry is broken, git merge is not an option — port with the recipient's semantics preserved, never the donor's regressions), re-run all batteries, park the donor as record — never delete.
6. **Record the roster failure.** When a collision happens, name the process cause (here: no board claim + force-push squash moving the target) and record the roster notes on the verdict so the next collision is prevented, not just repaired.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0808",
  "class": "OPERATIONS",
  "subcategory": "SHARED-BRANCH-DISCIPLINE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "One mission = one lane branch, claimed on the board before the first commit. A second branch name for the same mission triggers instant halt and reconciliation on one carrier; no pushes to the lane branch during final-head validation; no force-push squashes on shared lanes. When both branches hold unique work, neither merges as-is: pick the carrier, port the donor's unique fixes file-by-file, re-run all batteries, park the donor as record.",
  "worked_example": {
    "carrier": "naya5/ship-design-gate-repairs4 @ 598f5b68 (round-3 battery 40/41, adv 60/60, r4final 50/59)",
    "donor": "naya5/ship-design-gate-repairs5 @ 5c4b8623 (fixes S3 comment-in-url() and C1 >-in-quotes; misses round-4 fixes, crashes on malformed receipts)",
    "cause": "repairs5 branched from live tip and pushed without any #1354 post; fixer finalizing via local squash + force-push made the branch a moving target",
    "port_plan": "Port A: R5 _tag_extent into R4 _find_tags/_all_tags/_inline_style_of, keeping R4 _parse_attrs. Port B: R5 url-token consumption into R4 _strip_css_comments, preserving strip->neutralize->decode order. Port w5 regression pins. Re-run all four batteries.",
    "board_comment": "#1354 6086995387"
  },
  "related": ["SN-0671", "SN-0493"]
}
```
