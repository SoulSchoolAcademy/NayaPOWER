# Main Tip Is Not the Line With the Work — Verify the Base Branch Carries the Subtree

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1579-main-tip-is-not-the-line-with-the-work
**Smart Note:** SN-1579
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** lesson-broadcast.md [2026-10-17T23:22Z] MIRROR t0798-lane12 (Naya Clarity Narzan, Lane 12 Herald, self-scored 9.5/10) — near-miss owned: branched from main tip to build breaker #3, but the smart-builder subtree lived ONLY on the `design-library-canonical` line; caught on `ls`, re-based cleanly, no residue.

## IN A NUTSHELL

Before building, check that the branch you branched from actually contains the code you're about to work on. `git ls-tree <base> <subtree>` at branch creation. "Main tip" is a moving pointer, not a guarantee the work is there.

## HUMAN NOTE

The near-miss: a builder branched off main's latest commit assuming it was the freshest, best base — but the target subtree (smart-builder) existed only on a different line (`design-library-canonical`). The mistake was caught by listing the directory before writing code, and the branch was re-based cleanly with no residue.

The rule going forward: at branch creation, run `git ls-tree <base> <subtree>` for the subtree you intend to build in. If it returns nothing, the base is wrong — stop and pick the right line. This takes five seconds and prevents building against a phantom tree, which otherwise surfaces as missing files, false "not implemented" verdicts, or work done on the wrong line that must be re-done.

This is a different check from SN-395 (regen reads the commit, not the worktree) — that one is about reads; this one is about branch-creation base selection.

## CHILD NOTE

When you make a new branch to do work, first check that the branch has the folder you need. Use `git ls-tree <base> <subtree>` — if the folder isn't listed, you're on the wrong branch and you need to start from the right one before you write any code.

## GRANDMA NOTE

Before starting a new project off a shared plan, open the drawer and check the tools are actually in it. Don't assume the newest copy has everything — verify the pieces exist where you'll be working.

## NAYA NOTE

Branch creation is a claim about the world: "this line carries the work." Make that claim verifiable at creation time. `git ls-tree <base> <subtree>` before the first build action, recorded in the build receipt's branch line. A build receipt whose branch line lacks the subtree-presence check is a receipt hole — the lane-scorer treats it the same as any other missing verification.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1579",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-17",
  "applies_when": [
    ["branch", "base-selection"],
    ["build", "branch-creation"]
  ],
  "enforcement": "Named verification step: at branch creation, run `git ls-tree <base> <subtree>` for the intended subtree before any build action; record the presence check on the build receipt's branch line. Gap-lane-scorer verifies build receipts for this line; a missing line is a receipt hole. Tripwire: any 'target subtree not found after branching' incident after adoption falsifies the habit.",
  "decision_change": "Which base branch a work branch is created from — the check moves the decision from 'newest tip' to 'the line that carries the subtree'.",
  "falsifier": "If branch-creation incidents of class 'base lacks subtree' do not drop after the check is enforced, or a builder verifies the subtree and still loses work to a wrong base, the lesson is wrong.",
  "mechanism": "git branch creation inherits the base's tree verbatim; build work targets files that must exist in that tree. 'Main tip' is a moving pointer across a line that may never have merged the subtree. A five-second ls-tree at creation time binds the claim to the bytes.",
  "evidence": "lesson-broadcast.md 2026-10-17T23:22Z MIRROR t0798-lane12 (Naya Clarity Narzan, Lane 12 Herald, 9.5/10): near-miss — branched from main tip, smart-builder subtree lived only on design-library-canonical; caught on `ls`, re-based cleanly, no residue."
}
~~~
