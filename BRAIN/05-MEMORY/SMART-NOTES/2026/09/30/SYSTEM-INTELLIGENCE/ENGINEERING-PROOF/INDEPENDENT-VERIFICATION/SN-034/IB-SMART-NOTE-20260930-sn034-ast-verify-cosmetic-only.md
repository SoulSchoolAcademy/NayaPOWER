# "Cosmetic-Only" Is a Claim, Not a Fact — Verify with AST, and Gate Status Promotions with Honesty Tests

**Intelligent Block:** IB-SMART-NOTE-20260930-sn034-ast-verify-cosmetic-only
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

During the nine-node VERIFY lane's 22:52 PDT run (board comment 5925653492, 2026-10-01 05:58 UTC), three new HARDEN commits landed on `naya4/nine-node-kernel-v1` (→ `31864c25d4`) carrying what the author called docstring additions only. The verifier did not take that at face value: all 8 changed node source files were independently checked AST-IDENTICAL to the prior watermark `94340120ad` after stripping docstrings — a mechanical strip-and-compare, not a diff-eyeball. The verdict (457/457 node tests, 964/3 repo suite) followed from the proof, not the claim. The second durable move in the same run: the `manifest.json` status flip `SCAFFOLD` → `CANDIDATE` arrived guarded by 7 new `test_manifest_state.py` tests asserting the CANDIDATE status carries the NOT RATIFIED / NOT MERGED banner — the evidence-law honesty banner, enforced in code rather than promised in prose. Two rules for a cold successor: (1) "no behavioral change" is a claim that must be PROVED — AST strip-and-compare (or the equivalent mechanical check for the artifact type) is the minimum evidence; a green suite alone does not distinguish docstring-only from behavior-preserving-refactor-only; (2) status promotions (SCAFFOLD → CANDIDATE → …) are claims about the honesty of the label itself — gate them with tests that assert the banner, so a future reader can never see the status without seeing the caveat. All code remains CANDIDATE — not ratified, not merged, not deployed.

## 🩷 HUMAN NOTE

Someone said "I only changed the comments" — and instead of believing them, the verifier took the code, stripped the comments, and compared what was left mechanically. Identical. That's the standard: a claim of "nothing changed" gets proved, not trusted. And when the project status was upgraded, the upgrade came with tests that make sure the new label always shows its warning banner — honesty that can't be accidentally deleted.

## 🟣 CHILD NOTE

If your friend says "I didn't touch your LEGO castle, I just put labels on the bricks" — you don't take their word for it, you check: take the labels off and see if the castle is the same. Same bricks, same shape? Then the claim was true. And when the castle gets a new name tag, the tag has to say "not finished yet" in big letters — and you check every time that the letters are still there.

## 🔵 GRANDMA NOTE

"Trust, but verify" — except here it's verify first, and the verification has to be mechanical, not a glance. Like counting the silverware after a dinner guest helps with the dishes: the claim is "everything's back," the proof is the count. And if you change the label on a folder from "draft" to "final," you staple the warning to it so nobody reads the label without the warning.

## 🟠 NAYA NOTE

Adopt two verification habits permanently: (1) for every "cosmetic-only / no-behavioral-change" commit, run the mechanical no-change proof appropriate to the artifact — for Python, AST strip-and-compare against the prior watermark (docstrings/comments stripped), independent of the author's diff; pair it with the suite green, never substitute it; (2) for every status promotion in a manifest (SCAFFOLD → CANDIDATE → beyond), ship guard tests that assert the honesty banner travels with the status — NOT RATIFIED / NOT MERGED must be machine-checked, not human-promised. The verifier's lane also modeled scope hygiene: an ephemeral `/tmp` worktree at the exact SHA (clean fetch, read-only, removed after), a lane-claim re-confirmed before re-verifying, and the explicit "no newer kernel branch announced" freshness check. A verify run that cannot name its exact SHA, its watermark, and its freshness basis is a status update, not a verification.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": [
    {"board": "5925653492", "lane": "naya2-nine-node-verify", "when": "2026-10-01T05:58:09Z", "branch": "naya4/nine-node-kernel-v1", "sha": "31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194", "watermark": "94340120ad", "method": "AST strip-and-compare (docstrings stripped), independently checked — 8 changed node files AST-identical", "claim_proved": "3 HARDEN commits are docstring additions only; Kernel.decide() 13-edge topology unchanged", "suite": "tests/test_nodes 457/457; repo 964 passed, 3 skipped (4 uncollectible on missing pglast, pre-existing, unrelated)", "env": "ephemeral /tmp worktree at exact SHA, read-only, removed after"},
    {"board": "5925653492", "status_promotion": "manifest.json SCAFFOLD -> CANDIDATE", "guard": "7 new test_manifest_state.py tests asserting CANDIDATE status carries NOT RATIFIED / NOT MERGED banner", "evidence_law": "honesty banner machine-enforced, not prose-promised"}
  ],
  "rule": "mechanical_no_change_proof + banner_gated_status_promotion",
  "protocol": [
    "\"cosmetic-only / no-behavioral-change\" is a claim: prove with AST strip-and-compare (or artifact-equivalent mechanical check) against the prior watermark, independent of the author's diff",
    "suite green is required but not sufficient — it does not distinguish docstring-only from behavior-preserving-refactor",
    "every manifest status promotion ships guard tests asserting the honesty banner (NOT RATIFIED / NOT MERGED) travels with the status",
    "every verify run names: exact SHA, prior watermark, freshness basis (no newer branch announced), ephemeral read-only worktree disposed after"
  ],
  "related": ["SN-027 (amendment premise verification)", "SN-030 (phantom citation tokens — independent premise checking)", "SN-017 (asserted != verified)"]
}
~~~
