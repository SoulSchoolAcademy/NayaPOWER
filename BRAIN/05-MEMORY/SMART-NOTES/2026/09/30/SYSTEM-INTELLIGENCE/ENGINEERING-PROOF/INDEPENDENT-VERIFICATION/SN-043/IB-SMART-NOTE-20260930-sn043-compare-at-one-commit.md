# Compare at ONE Commit — Resolve Both Sides of a Cross-State Claim at Their Own Refs

**Intelligent Block:** IB-SMART-NOTE-20260930-sn043-compare-at-one-commit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:15 PDT distillation tick (2026-10-01) from #554 comment 5927430220 ([NAYA 2][BUILD-LOOP] — #1224 `test` red: false premise corrected + repair go-ahead). Extends SN-038 (regeneration encodes intent) in the pin-drift family; AGENTS.md already carries the standing rule.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two of Naya 4's three "#1224 `test` red" root-cause findings were wrong, and both failed the same way: one side of each comparison was resolved at the wrong ref. The pin drift (27 vs 36) was real — but "stale vs main" was not: main `a726a837` holds pin `EXPECTED_DOMAIN_COUNTS["03-KERNEL"] = 28` with a recursive blob count of 28, so `--check` is green on main; the "27 vs 28" comparison had measured the branch's pin against main's tree — a cross-commit. And the `0005` Ultimate-Lock file was never removed on the branch: it 404s at base `507d3421` AND head `19abcf2f` but exists on current main — main-side drift from one of 88 post-base merges, not a branch deletion. The branch delta vs its own base is purely +9 (0006 scorecard + 8× `0002-MASTER-SPEC`), so 27 + 9 = 36 with no −1 and no removal to investigate. Naya 2's verdict: "compare at ONE commit — evaluate both sides with `git ls-tree` at the ref, never branch-tree vs current-main." This is the second wild instance of the standing rule; the repair pin must be **36 now** and **37 only after the rebase** — do not pre-bump, or `--check` stays red.

## 🩷 HUMAN NOTE

Imagine proofreading a manuscript: you compare the draft in your hands against the published book and flag "this chapter is missing" — but the chapter was added to the book after the draft was made. You compared two different editions and invented a disappearance. The fix is the same in both cases: hold one edition in your hands at a time. Every claim about "X is stale" or "Y was deleted" must resolve both sides at the same commit, or it manufactures findings.

## 🟣 CHILD NOTE

If you're checking whether your puzzle still has all its pieces, don't count your box and compare it to your friend's finished puzzle on the table — compare your box to what your box had yesterday. Different piles, different answers.

## 🔵 GRANDMA NOTE

It's like checking a grocery list: the store has 28 kinds of jam today, your list from last week says 27. That doesn't mean a jam went missing from the list — it means the store changed after the list was written. Check the list against the list's own date, not against today's shelves.

## 🟠 NAYA NOTE

Install the one-commit rule as the first gate of every cross-state claim (drift, deletion, staleness, pin mismatch): (1) state the claim's two refs explicitly — which commit supplies the "expected" side, which supplies the "actual" side; (2) resolve BOTH sides with `git ls-tree`/tree reads at those refs, never branch-tree vs current-main tip; (3) when a delta surprises you (a missing −1, an unexpected 28), check the base-relative delta and the main-side drift before theorizing — main moves under branches constantly; (4) for repair pins: set the pin to match the tree it currently guards, and document the post-rebase value as a separate, later step — pre-bumping is a red gate you gave yourself. The two false findings here both cost a full investigation cycle each; the rule costs one line of ref hygiene.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "cross_commit_comparison_false_finding",
  "evidence": {
    "board_comment": "5927430220 — [NAYA 2][BUILD-LOOP] #1224 test red: false premise corrected + repair go-ahead (2026-10-01 ~01:10 PDT), verified live via gh-api with each side resolved at its own ref",
    "false_finding_1": "pin 'stale vs main' — branch pin 27 was compared against main's tree 28; main a726a837 pin=28, blob count=28, --check green; no action needed on main",
    "false_finding_2": "'0005 removed on branch' — 404 at base 507d3421 AND head 19abcf2f, exists on main a726a837; main-side drift, not a branch deletion; branch delta vs own base = +9 (0006 + 8x 0002), 27+9=36, no -1",
    "repair": "pin 27->36 now (match current tree), 37 only at rebase (28+9); repair approved as amendment commit on PR #1232, branch owner's lane; CI gate only, merge gate (#1224, Shawn) and 8 qualify blockers unchanged"
  },
  "rule": "compare_at_one_commit",
  "procedure": [
    "name both refs of any cross-state claim (expected-side ref, actual-side ref)",
    "resolve both sides with git ls-tree at those refs — never branch-tree vs current-main tip",
    "check the base-relative delta and main-side drift before theorizing about a surprising delta",
    "set repair pins to the tree they currently guard; post-rebase values are separate later steps — do not pre-bump"
  ],
  "related": ["SN-038 (regeneration encodes intent — same pin-drift family)", "SN-028 (clean-room verification)", "SN-033 (collision-registry first-claim protocol)"]
}
~~~
