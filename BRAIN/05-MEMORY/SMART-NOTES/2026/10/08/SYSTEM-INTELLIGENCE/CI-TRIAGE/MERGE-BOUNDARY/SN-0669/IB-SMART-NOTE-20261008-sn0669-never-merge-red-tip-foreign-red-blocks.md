# Never Merge With Red CI — Even When the Red Isn't Yours

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0669-never-merge-red-tip-foreign-red-blocks
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6056167126 (2026-10-08).
**Provenance:** #1354 6056167126 ([NAYA 4] #1840 analysis — fix verified, 4 remaining failures belong to the wave, 2026-10-08T08:44:54Z). Related: SN-0552 (fail-first CI topology), SN-0240 (classify every CI red before healing), SN-0340 (Scorecard Law).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1840 fixed its own defect — `test_engineering_gates.py` 17/17 pass, the collection error gone on rebased head `7fd4942c`. The full suite still showed 4 failures — every one of them owned by other lanes' open PRs (Naya 5's kernel TypeError, #1838/#1844 registry drift ×2, the weights issue). Decision: **NOT merging.** The "never merge with red CI" boundary stands even when the red isn't from your changes: a PR's own green does not license merging into a red tip. Instead the merge order was documented on the record — #1837 + #1838/#1844 (registry) + Naya 5's kernel fix, *then* #1840 merges, *then* the tip is green. This is the fail-first topology working as designed: #1840's fix unblocked collection, which revealed the next layer of failures. Holding the line converts that revelation into an ordered path to green; merging through it would convert it into a tip you can't trust.

## 🩷 HUMAN NOTE

Shawn — the unglamorous decision that keeps the system honest: #1840's fix works (17/17 tests pass), but the lane held the merge anyway because four other lanes' failures were still on the tip. Merging a clean fix into a dirty tip would have made the tip dirtier. Instead there's a written merge order on the board: wave first, then #1840, then green. Discipline over momentum.

## 👶 CHILD NOTE

Imagine your team is building a tower and your block is perfect — but three blocks below it are still wobbly. You don't stack your perfect block on top anyway. You wait, fix the wobbly ones first, then place yours. Your perfect block doesn't make the wobbly tower stable.

## 👵 GRANDMA NOTE

Honey, it's like baking a wedding cake with a crooked bottom layer. Your top layer is beautiful, but you don't set it on the crooked one — the whole cake tips over. You straighten the bottom first, then place your layer. The rule is about the whole cake, not your layer.

## 🤖 NAYA NOTE

Before merging a PR when other failures exist on the tip:

1. **Attribute every failure.** Own vs. foreign-owned. The 4 remaining failures here were all wave-owned (#1838/#1844, Naya 5's kernel, weights) — none from #1840's changes.
2. **Hold the merge anyway.** A PR's own green does not override the tip's red. "Never merge with red CI" is a tip-level boundary, not a PR-level one.
3. **Write the path to green instead.** Document the merge order on the board (here: wave PRs → #1840 → green tip) so the hold is a plan, not a stall.
4. **Read the unmasking as signal.** Fixing a collection error reveals the next layer — that's fail-first topology (SN-0552) working, not a new emergency. Log the revealed layer, assign it to its owning lanes, keep your lane's evidence pinned to its own head SHA.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0669",
  "class": "CI-TRIAGE",
  "subcategory": "MERGE-BOUNDARY",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Never merge with red CI — even when the red isn't yours. A PR's own green does not license merging into a red tip; hold the merge, attribute the foreign failures, and document the ordered path to green instead.",
  "worked_example": {
    "pr": "PR #1840 (fix test_engineering_gates import)",
    "evidence": "17/17 pass on rebased head 7fd4942c; 4 remaining failures all wave-owned (#1837/#1838/#1844 registry, Naya 5 kernel TypeError, weights)",
    "decision": "no merge; written merge order: wave PRs -> #1840 -> green tip",
    "board_comment": "#1354 6056167126"
  },
  "related": ["SN-0552", "SN-0240", "SN-0340"]
}
```
