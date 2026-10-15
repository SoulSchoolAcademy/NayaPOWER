# SMART NOTE — Verify the Final Artifact, Not the Intermediate — A Check Is a Snapshot Verdict

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01365-verify-the-final-artifact-not-the-intermediate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

---

## ✦ IN A NUTSHELL

**A check verdict binds to the exact state snapshot it ran against — any mutation after the check silently voids the verdict.** CONNECT driver run 2026-10-14 ~21:08 PDT: the branch's brain-index regen ran, `regenerate_brain_index.py --check` passed OK, and *then* a cherry-pick overlay landed on top and the branch was pushed. CI on the new head caught index drift the local check had missed. Byte-level root cause (verified, not inferred): the branch tree's registry file was blob `79661f69` (the cherry-picked 1-line entrypoint fix) while the committed index recorded `cc5f5559` (the tip's pre-cherry-pick blob) — the check had validated a state that no longer existed at push time. The repair: regenerate in place against the final committed tree (commit `297370e64e`), re-run `--check` (OK, 1259 files) + `pytest tests/test_brain_index_freshness.py` (13/13 PASS) on that final tree, push `ce1873c2`. The sequencing rule: **mutate → commit → check → push — the check is the last step before the artifact ships, or the old verdict is void.** "Already done" triggers a byte check — on the artifact that ships, not the one that was checked.

---

## 🩷 HUMAN NOTE

A car passes its inspection, gets the sticker — and then the mechanic swaps the engine in the parking lot. The sticker is honest: it describes the car as it stood at inspection time. But what ships to the customer is not that car anymore. Nobody forged the inspection; the *ordering* broke it. That's what happened here: the freshness check passed on the intermediate tree, then a cherry-pick changed the tree underneath it, and CI was the first one to look at the shipped car. The fix wasn't a better check — it was moving the check to after the last wrench turned. Every verification is a photograph, not a promise: the moment the subject moves, the photo is history. (Related: SN-077's install-then-report rule for restoration; SN-0533's fingerprint-before-proof. This note is the ordering corollary — *when* the fingerprint is taken matters as much as what it covers.)

---

## 🟣 CHILD NOTE

Your teacher checks your homework page and says "all correct!" — and then you scribble in three more answers after she walks away. When the teacher collects the page, those new answers were never checked. You didn't cheat; you just did things in the wrong order. The rule: **check comes last.** If you change anything after the check, the check doesn't count anymore — do it again. That's the whole lesson: finish everything first, *then* check, *then* hand it in.

---

## 🔵 GRANDMA NOTE

It's like weighing your ingredients on the kitchen scale, getting the perfect reading — and then pouring in more flour after you put the bowl on the counter. The scale told the truth about the bowl *at that moment*. It can't tell you anything about the bowl after you added more. This is a note about doing things in the right order: finish the mixing, *then* weigh, *then* bake. A measurement only describes what was there when you took it.

---

## 🟠 NAYA NOTE

1. **A check is a snapshot verdict, not a forward promise.** `regenerate_brain_index.py --check` consumes tree state; its OK verdict binds to that tree. A cherry-pick, rebase, amend, or overlay after the check changes the state the verdict was about. The verdict has no reach forward in time.
2. **The signature of this defect class:** `--check` OK on the intermediate + CI red at the pushed head. When you see it, don't re-run the check on the same state — look for what mutated *after* the check. Here: regen ran before the cherry-pick overlay landed; CI caught the drift the local run missed.
3. **Sequencing rule for every generated artifact** (brain index, migrations, docs, wiring): mutate → commit → check → push. The check is the last step before ship. After ANY post-check change, the old verdict is void: re-run the checker on the final committed tree and re-pin head/sha everywhere (PR body `## Evidence`, receipts, board posts).
4. **Byte-check the final artifact, not the checked one.** The forensics: branch tree registry file `79661f69` (cherry-picked fix) vs committed index `cc5f5559` (pre-cherry-pick). The tip itself was self-consistent — the drift lived only on the branch, invisible until CI looked at the final bytes.
5. **Boundary:** this does not apply when the check itself is broken, or when the red is transient infra (quota 403s, rate-limit bodies) — classify first (content vs transient vs environmental), then fix the sequencing. A broken clock and a moved subject are different failures.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn01365-verify-the-final-artifact-not-the-intermediate",
  "epistemic_state": "CANDIDATE",
  "capture_type": "SEQUENCING_DEFECT / VERIFICATION_ORDERING",
  "rule": [
    "mutate -> commit -> check -> push: the checker runs against the FINAL committed tree, never an intermediate",
    "any mutation after a check (cherry-pick, rebase, amend, overlay) voids the verdict; re-run the checker on the final tree and re-pin head/sha everywhere",
    "defect signature: local --check OK + CI red at pushed head -> look for post-check mutations, not a broken checker",
    "boundary: classify failures first (content vs transient vs environmental); this rule covers content-drift-after-check, not broken checkers or quota 403s"
  ],
  "evidence": {
    "finding": "hidden_files/connect-driver-run-20261014-2108-log/run-log.md (CONNECT driver, 2026-10-14 ~21:08-21:30 PDT)",
    "pr": "#2528 branch naya4/connect-seam-residual-20261013: head 58f349e5 -> repair commit 297370e64e -> ce1873c2",
    "byte_forensics": "branch tree registry file = blob 79661f69 (cherry-picked 1-line entrypoint fix); committed index recorded cc5f5559 (pre-cherry-pick blob); tip itself self-consistent (cc5f5559 in both) - drift lived only on the branch",
    "re_verification": "regenerate_brain_index.py --check -> OK (1259 files); pytest tests/test_brain_index_freshness.py -> 13/13 PASS, both run against the FINAL committed tree; merge-cleanliness at tip ba626387 confirmed (0 conflict markers)"
  },
  "mechanism": "verification consumes a state snapshot (tree hash, file blobs); a post-check mutation changes the state the verdict described, so the verdict cannot hold for the new state - a verdict has no reach forward in time",
  "falsifiability": "would be refuted by byte evidence that a --check verdict survived a subsequent mutation that provably altered the checked artifact (not merely by a passing re-check, which is the remedy, not a refutation); boundary case that does NOT falsify: checkers that are themselves broken or failures caused by transient infra",
  "decision_change": "when a seat regenerates a generated artifact and then applies any overlay/edit/amend, they must re-run the checker on the final committed tree before push/merge - never trust a check that predates the last mutation",
  "related": ["SN-077 false-green-restoration (install-then-report)", "SN-0533 fingerprint the bytes before you prove them", "tick-40 already-done-triggers-a-byte-check mechanism"],
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION"
}
```
