# Replay Canonical Selection at the Pinned selection_now — the Stale-Eligible-Block Forgery

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0556-selection-replay-at-pinned-selection-now
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6043318985 ([NAYA] P0 learning activation — EXACT-CURRENT SOURCE ACCEPTANCE GREEN, 2026-10-07T17:35:09Z); PR #1743 exact head `b112c8e93e114505cf359db92253fd6f9202e837`; durable full acceptance receipt: #1724 comment 6043312808

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A cold verifier found a real hole in the earlier P0 learning source: a **coherently forged KNOW receipt** could point to a *real older eligible block* with matching provenance and evidence, even when canonical KNOW would have selected a *newer* block — and earlier ACT accepted it. Provenance and evidence checks pass because the block is genuinely eligible; only the *selection* is wrong. The fix: ACT now replays canonical `selectKnowContext()` + CONNECT selection at the receipt's pinned `selection_now` and requires an exact match. The same attack is now **BLOCKED / KNOW_SELECTION_REPLAY_MISMATCH**, with a committed regression.

Why this is brain-grade and genuinely new: SN-0458 (second-source rule) says a single check is a hypothesis — this is not about the number of checks but about *what* is checked. Provenance-verification and selection-verification are two different gates on the same receipt, and the forged receipt passes the first while failing the second. An attacker doesn't need to forge evidence; they only need to smuggle in a worse-but-valid *choice*. The general rule: whenever an authority decision is validated against a receipt, validate not just the receipt's authenticity (provenance, evidence) but the *selection that produced it* — replay canonical selection at the receipt's pinned inputs and compare outputs. Authenticity of the artifact ≠ correctness of the choice.

## 🩷 HUMAN NOTE

Shawn — the learning seam's security story got stronger today, and the lesson generalizes. An independent verifier proved a forged receipt could have slipped past the old checks: not by faking evidence, but by pointing at a *real* older knowledge block when the newest one should have been chosen. The old checks asked "is this block real?" — they never asked "was this the block we would have actually picked?" Now the system replays the original selection logic at the moment the receipt claims to be from, and rejects anything that doesn't match. The takeaway for everything we build: don't just verify that a record is authentic — verify that the *decision* it records was the right one, by replaying the decision at its original inputs.

## 🟣 CHILD NOTE

Imagine the teacher asks you to pick the best apple from the basket, and you bring her a rotten-but-real apple. She checks: is it an apple? Yes. Did it come from the basket? Yes. But she never asked: was it the *best* one? You could keep bringing bad apples forever and pass every check. The new rule: the teacher goes back to the basket herself, picks what she would have picked, and compares. If yours doesn't match, you're caught.

## 👵 GRANDMA NOTE

A receipt shows a purchase happened — but a receipt can be for the wrong item and still be a genuine receipt. If a clerk hands you a real receipt for a cheaper product than the one you bought, checking that the receipt is authentic tells you nothing about whether you got what you paid for. You have to replay the transaction: what *should* the receipt have been? Our systems now do exactly that — they replay the original decision at the moment it was claimed to happen, and any receipt that doesn't match gets rejected.

## 🧠 NAYA NOTE

Cold successor: whenever you validate a receipt that drove an authority decision, add the selection-replay gate after the authenticity gate. (1) Pin the receipt's claimed selection inputs (here: `selection_now`). (2) Run the canonical selector at those inputs exactly (`selectKnowContext()` + CONNECT selection). (3) Require exact match with the receipt's claim; mismatch → hard block (`KNOW_SELECTION_REPLAY_MISMATCH`), never a soft warning. (4) Commit a regression for every forged-receipt class you block — the regression is the lesson's proof, not the comment. (5) Template: #1743's CONTROL/TREATMENT pair — control `APPLY_BASELINE_WITHOUT_RETAINED_STEERING`, treatment `PRESERVE_PROVENANCE_BEFORE_APPLY` — proves stale intelligence does not steer the same decision a second time.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0556",
  "title": "Replay Canonical Selection at the Pinned selection_now — the Stale-Eligible-Block Forgery",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "KERNEL-CONTRACT-SEAMS"],
  "cousins": ["SN-0458"],
  "evidence": {
    "board": ["#1354 6043318985 ([NAYA] P0 learning activation — EXACT-CURRENT SOURCE ACCEPTANCE GREEN, 2026-10-07T17:35:09Z)"],
    "acceptance_receipt": "#1724 comment 6043312808 (durable full acceptance receipt)",
    "head": "PR #1743 exact head b112c8e93e114505cf359db92253fd6f9202e837; main 78f2c568757698a29b4d4b97551cff085d8396b3",
    "attack": "coherently forged KNOW receipt pointing to a real older eligible block with matching provenance/evidence, where canonical KNOW would select a newer block — earlier ACT accepted it",
    "defense": "ACT replays canonical selectKnowContext() + CONNECT selection at the receipt's pinned selection_now; mismatch -> BLOCKED / KNOW_SELECTION_REPLAY_MISMATCH; regression committed",
    "corroboration": "exact-head evidence: independent verifier PASS; focused Node 50/50; full Node 551/551; focused Python 6/6; typecheck + guard 12/12; Brain index PASS 235 files; Kernel Tests PASS; Ratified Guard PASS; Spec Integrity PASS; Chain Readiness PASS"
  },
  "doctrine": {
    "principle": "authenticity of the artifact is not correctness of the choice — validate the selection that produced the receipt, not just the receipt's provenance and evidence",
    "mechanism": "replay canonical selection at the receipt's pinned inputs and require exact match",
    "verdict": "KNOW_SELECTION_REPLAY_MISMATCH is a hard block, never a soft warning",
    "regression_law": "every blocked forged-receipt class ships a committed regression — the regression is the lesson's proof"
  },
  "rule": "whenever an authority decision is validated against a receipt, replay the canonical selection at the receipt's pinned inputs and compare — an authentic receipt for the wrong choice is still a forgery"
}
```
