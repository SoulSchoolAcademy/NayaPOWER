# Verifiers Don't Self-Certify — Clean-Room Verification at the Exact SHA

**Intelligent Block:** IB-SMART-NOTE-20260930-sn028-clean-room-verification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Independent verification of a branch must happen in a clean-room the builder never touched: a fresh public clone at the exact pinned SHA, in an ephemeral scratch worktree, read-only, destroyed afterward. The verifier lane never trusts the builder's working tree, the branch's living head, or its own memory of what the code "should" be. Concrete case: the nine-node kernel verify (2026-09-30 ~21:55 PDT) cloned `naya4/nine-node-kernel-v1` at exact SHA `7e72b2737` into an ephemeral `/tmp` worktree, ran the full battery there, then removed the worktree. GREEN: `tests/test_nodes/` 450/450 (all nine nodes implemented-candidate, none a stub), kernel integration battery 22/22, full collectible suite 957 passed / 3 skipped — plus adversarial spot-review of two commits against the canonical graph seed. All code still CANDIDATE, not ratified, not merged, not deployed. The discipline, not the verdict, is the lesson: verification means nothing if it can read uncommitted state the evidence won't admit.

## 🩷 HUMAN NOTE

Here's the trap this kills: a builder verifies "their" branch from their own machine, and the checkout has uncommitted edits, a different head, a stale index — so the green tests prove a tree nobody else will ever see. The clean-room rule closes that gap mechanically. Clone fresh from the remote. Pin the exact SHA — not the branch name, which moves. Run read-only; nothing writes back into the clone. Delete the scratch when done, so no stale tree ever masquerades as a verification. Then report the SHA in the verdict, so anyone can reproduce the room. Naya 2's verify even pinned the two spot-reviewed commits by SHA and checked the 13 `REL-KERNEL-*` edge IDs 1:1 against the canonical seed — the same depth the discipline demands. Expensive? Minutes. Cheap compared to a green verdict that was lying about its subject.

## 🟣 CHILD NOTE

Imagine you and a friend build a LEGO castle, and your friend checks "did we follow the instructions?" — but they check by looking at a *photograph* of the castle instead of the castle itself. The photo might be old, or from the wrong angle, or Photoshopped. That's verifying from the builder's working tree: it might not match what everyone else sees. The clean-room rule says: your friend must go to the *actual* castle, with fresh eyes, in the room it really stands in. If it passes there, the castle is real.

## 🔵 GRANDMA NOTE

When someone checks important work, they should look at the real thing — not a copy that might be different, not the version in someone's head. Fresh eyes, the exact same materials, in a room where nothing can be quietly changed. That's how you know a "pass" is honest.

## 🟠 NAYA NOTE

This is the operational twin of the asserted-≠-verified doctrine (SN-020) pointed at the *subject* of verification rather than its *claim*. Asserted-≠-verified asks "did anyone prove it?"; clean-room asks "was the proof run against the thing it names?" Both matter; either one failing makes the verdict void. For the verify lane: the verifier never reviews from the builder's tree, never pins a branch name, never lets the scratch outlive the run. For cold successors: any "verified at SHA X" claim you inherit should name the clone source and SHA — if it doesn't, re-verify.

## 🟢 MACHINE NOTE

```json
{
  "block": "IB-SMART-NOTE-20260930-sn028-clean-room-verification",
  "truth_state": "CANDIDATE",
  "captured": "2026-09-30",
  "evidence": {
    "case": "#554 comment 5925107643 (2026-10-01T05:04:36Z, Naya 2 nine-node verify)",
    "subject": "naya4/nine-node-kernel-v1 @ 7e72b2737bb22956b3b83ca9a8a2acb1553ab216",
    "method": "ephemeral /tmp worktree; clean public clone at exact SHA; read-only; removed after",
    "verdict": "GREEN — tests/test_nodes 450/450 (SELF 37, LAW 27, ACT 32, KNOW 53, PROVE 34, CONNECT 49, VERIFY 75, LEARN 58, EVOLVE 63, none a stub); kernel nine-node integration 22/22; full collectible suite 957 passed, 3 skipped (4 files fail collection on undeclared pglast — pre-existing environment gap, unrelated)",
    "spot_review": "d86741b36: 13 REL-KERNEL-* edge IDs/types match BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json 1:1; LOCK_MINIMUM_ROUTES(11) enforced; GATE_REQUIREMENTS keep VERIFY on ACT+PROVE+CONNECT, EVOLVE on LAW+LEARN; ACT->KNOW and EVOLVE->SELF recorded as non-gate edges. 7e72b2737: KNOW reconciliation faithful to the Ultimate Lock (applicability exclusion -> non-steering note; epistemic assessment moved to PROVE via prove_receipt_ref naming NAYA-KERNEL-PROVE; truth_deltas -> state_deltas)"
  },
  "protocol": [
    "clone_fresh_from_remote_never_builder_tree",
    "pin_exact_sha_not_branch_name",
    "run_read_only_nothing_writes_back",
    "destroy_scratch_worktree_after_run",
    "report_sha_in_verdict_for_reproduction",
    "spot_review_commit_level_against_canonical_seeds"
  ],
  "failure_mode_killed": "green verdict proven against uncommitted or moved state that no one else will ever see",
  "twin_doctrine": "SN-020 asserted-not-verified (this note covers the subject, SN-020 covers the claim)",
  "lane": "verifier; builders do not self-certify"
}
```
