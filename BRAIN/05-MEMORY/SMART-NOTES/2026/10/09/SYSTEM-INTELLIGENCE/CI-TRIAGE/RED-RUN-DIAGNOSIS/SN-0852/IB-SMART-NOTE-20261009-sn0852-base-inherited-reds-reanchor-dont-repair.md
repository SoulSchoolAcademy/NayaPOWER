# Base-Inherited Reds Get Re-Anchored, Not Repaired — Prove Where the Red Lives First

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0852-base-inherited-reds-reanchor-dont-repair
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6092998750 (2026-10-10T02:51:18Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1980's old head (`928ae75a`, base `ec134159`) carried `test` + `spec-integrity` reds — but those reds were proven base-inherited, not introduced by the PR. The repair was not a code fix; it was a re-anchor: the head was moved onto the exact live tip (`9aa04ab8`), where it went 8/8 CI green with zero code changes — mergeable=true, mergeable_state=clean, backed by byte-parity proofs (blobs, tree, diff-intent). The rule: before repairing any CI red, prove whether it is base-inherited. An inherited red is not your branch's defect; re-anchor onto the green tip instead of "fixing" code that was never broken.

## 🩷 HUMAN NOTE

A student gets marked wrong for a question the textbook itself got wrong. You don't rewrite the student's correct answer — you fix the textbook, or grade against the corrected one. That's what happened with PR #1980: its test failures came from the old base it was built on, not from its own changes. Rebuilding the PR on top of the current, healthy code made everything green without changing a single line of the PR. Repairing "the PR" would have meant rewriting correct code to dodge somebody else's failure.

## 🟣 CHILD NOTE

If your homework was checked against an answer sheet that had a mistake, your answers look wrong even when they're right. Don't change your right answers — get the correct answer sheet and check again.

## 🔵 GRANDMA NOTE

Don't repaint a clean wall because the neighbor's fence fell on it, dear. Find out whose mess it is first — then fix the fence, not the wall.

## 🟠 NAYA NOTE

1. The order of operations for any CI red on a branch: (1) reproduce, (2) prove provenance — is the red introduced by this head or inherited from its base? — (3) if inherited, re-anchor the head onto the green live tip and re-verify; only repair code when the red is proven introduced. PR #1980's `test` + `spec-integrity` reds were proven inherited from base `ec134159`; the new head (`35cca990`) on exact tip `9aa04ab8` went 8/8 green with zero code change.
2. The anti-pattern is inherited-defect repair: "fixing" branch code to work around a base that was already broken. That fix is dead weight the moment the base heals — it becomes unexplained code carrying a rationale that no longer exists, and it pollutes the diff the reviewer must understand.
3. The evidence bar for "base-inherited": the red reproduces on the base without the branch's changes, and disappears when the unchanged branch head is re-anchored onto a green base. Byte-parity proofs (blobs, tree, diff-intent) on #1980 made the "no code change" claim checkable rather than asserted.
4. This is SN-0493 (a decision expires when the tip moves) applied to CI triage: the red belongs to a world that no longer exists once the base moves — the re-anchor moves the branch into the current world instead of patching the old one.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261009-sn0852-base-inherited-reds-reanchor-dont-repair",
  "automatic_truth_ceiling": "CANDIDATE",
  "captured": "2026-10-09",
  "rule": "red_provenance_before_repair",
  "statement": "prove_ci_red_is_introduced_not_base_inherited_before_repairing_inherited_reds_re_anchor_not_repair",
  "admissible_form": "reproduce → prove_provenance(introduced|base-inherited) → if_inherited: re-anchor_onto_green_tip + byte-parity_proof + re-verify",
  "inadmissible_form": "repair_branch_code_for_a_red_the_base_introduced",
  "evidence": {
    "note": "#1354/6092998750 (2026-10-10T02:51:18Z, Naya 4 VERIFY-driver)",
    "branch": "PR #1980 (replay-trial schema tolerance)",
    "old_head": "928ae75a on base ec134159 — test + spec-integrity reds proven base-inherited, not introduced",
    "new_head": "35cca990 on exact live tip 9aa04ab8 — 8/8 CI green, mergeable=true, mergeable_state=clean, zero code change; byte-parity proofs (blobs, tree, diff-intent) in receipt comment 6092987316",
    "boundary": "#2053 (authority-gov repair3) still HELD for Shawn's explicit word — protected gate, recorded not forced"
  },
  "applies_to": ["CI_triage", "PR_re_anchor", "any_red_on_a_branch_with_a_moved_base"]
}
~~~

## 🟢 LEARNING LESSON

The instinct when you see red on your branch is to open your files and start fixing. The discipline is to first ask "was this red already here when I built on this base?" — because the answer changes the whole job. #1980's reds were the base's, so the job wasn't repair at all; it was relocation. The cleanest repair is the one you never have to write, and you find it by proving provenance instead of assuming authorship.

## 🟡 WHAT IT MEANS

No branch code is edited for a red that isn't proven introduced. Every CI triage starts with provenance: reproduce on the base alone. Inherited reds are closed by re-anchor onto the green tip with byte-parity proof; introduced reds are repaired in code. The merge seat receives provenance with the green, not just the green.

## 🟨 HOW TO APPLY / HOW TO USE

CI red on your branch → check whether the red exists on the base without your changes → if yes (base-inherited): re-anchor head onto the exact live green tip, re-run CI, attach byte-parity proof that no code changed → if no (introduced): repair the code, re-verify on the exact tip. Never carry an inherited red into a code fix; never re-anchor to dodge an introduced red.

## 🔗 HOW IT CONNECTS

- **PAIRS** → SN-0851 — environment-only failures: prove the habitat before you touch anything (same discipline, different habitat)
- **EXTENDS** → SN-0493 — a decision expires when the tip moves: a red belongs to the world of its base; move the branch, don't patch the old world
- **GOVERNS** → PR review burden: diffs free of inherited-defect workarounds are reviewable diffs

## 🧾 PROOF / PROVENANCE

- #1354 comment 6092998750 (2026-10-10T02:51:18Z, Naya 4 VERIFY-driver): "Top hole filled: **PR #1980 (replay-trial schema tolerance) re-anchored onto the green tip and now fully green.** Old head `928ae75a` (base `ec134159`) had `test` + `spec-integrity` reds — proven base-inherited, not introduced. New head `35cca990` (base = exact live tip `9aa04ab8`): **8/8 CI green, mergeable=true, mergeable_state=clean**. Byte-parity proofs (blobs, tree, diff-intent) in the receipt."
- Receipt: comment 6092987316; #1723 sign-in/out: 6092997888. VERIFY 9.2 → 9.3.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: observed once with a clean provenance proof. The rule does not claim re-anchor always suffices — some reds are genuinely dual (base weakens, branch finishes). The claim is only the order of operations: prove provenance before choosing between repair and re-anchor, and treat an unproven choice as inadmissible.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every CI triage on a branch carries a provenance verdict (INTRODUCED / BASE-INHERITED) with evidence before any repair. Success is behavioral: no future branch is ever edited to work around a red its base brought along.
