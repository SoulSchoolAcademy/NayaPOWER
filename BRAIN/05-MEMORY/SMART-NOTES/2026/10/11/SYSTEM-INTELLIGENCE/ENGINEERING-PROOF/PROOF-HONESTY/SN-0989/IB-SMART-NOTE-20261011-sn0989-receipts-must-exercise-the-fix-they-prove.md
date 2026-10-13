# Receipts Must Exercise the Fix They Prove

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0989-receipts-must-exercise-the-fix-they-prove
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/PROOF-HONESTY

## IN A NUTSHELL

SN-0983 banked the finding that the receipt gate treated 40-char SHAs as live handles but could not resolve them inside its own depth-1 checkout. The fix (PR #2347, `naya2/receipt-gate-fetch-depth-fix` @ `e29be87477`, a one-line `fetch-depth: 0`) closed it — but the receipt that proves the fix is self-demonstrating: the PR body cites its own commit SHA as the live handle, so the fixed gate must resolve that exact SHA in CI for the receipt job to pass. If the fix were wrong, the receipt would fail on its own evidence. The receipt also names and scores the rejected alternatives — API-fallback 5/10 (auth/rate-limit flake), warn-don't-fail 3/10 (fail-open) — below the one-liner at 9.5/10.

The durable rule: **a repair's receipt should depend on the repair — route the receipt's own evidence through the fixed mechanism.** Cite handles (SHAs, paths, URLs) that only the fixed mechanism can resolve, so a broken fix fails its own receipt instead of passing on evidence gathered elsewhere. Asserting the fix works from outside the mechanism is a claim; making the receipt's validity conditional on the fix is proof. And name the rejected alternatives with their scores — a receipt that only shows the winner hides the reasoning the next repair will need when the winner stops working.

## HUMAN NOTE

Shawn — small proof-craft catch from the night shift worth keeping: the lane that fixed the receipt gate wrote its receipt so the fix has to prove itself — the PR body cites its own commit SHA as a live handle, so the fixed gate must actually resolve that SHA in CI for the receipt to go green. A broken fix would fail its own receipt. Lesson banked: make a repair's evidence pass through the repaired mechanism, and score the alternatives you rejected in the receipt so the reasoning survives.

## CHILD NOTE

If you fix a lock, don't just say "the lock works now" — lock the door with the new key and try to open it. That's what this lane did: the receipt itself uses the thing that was broken (a commit SHA the gate couldn't read before), so if the fix didn't work, the receipt would fail on its own evidence. Rule: make your proof use the thing you fixed — and write down the other ideas you said no to, so nobody has to guess why later.

## GRANDMA NOTE

It's like fixing a broken phone and then proving it works by calling someone *on that phone* — not by waving it in the air and saying "fixed." If the phone were still broken, the call itself would fail. The worker who fixed the receipt gate did exactly that: the proof uses the gate's own repaired machinery. And they wrote down the two ideas they rejected and why — so the next person doesn't re-try a bad idea.

## NAYA NOTE

When I ship a repair, I make the receipt depend on the repair. The receipt's evidence must pass through the fixed mechanism: I cite handles — SHAs, paths, URLs — that resolve only if the fix is real, so a broken fix fails its own receipt. Evidence gathered outside the mechanism proves nothing about the mechanism. I also score the rejected alternatives in the receipt itself (what they were, why they lost), because the next failure will ask "did we consider X?" and the receipt should already answer. A receipt that only shows the winner is a trophy; a receipt that shows the winner and the losers is a record.

## MACHINE NOTE

```json
{
  "sn": "SN-0989",
  "slug": "receipts-must-exercise-the-fix-they-prove",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "PROOF-HONESTY"],
  "authority": "distillation tick 2026-10-11 07:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board": "#2175 comment 6109653689 (BUILD lane sign-out 2026-10-11 ~13:50Z)",
    "pr": "PR #2347 (naya2/receipt-gate-fetch-depth-fix) @ e29be87477 — receipt job now checks out with fetch-depth: 0, same as the two sibling jobs",
    "self_demonstration": "PR body cites its own commit SHA as the live handle — the fixed gate must resolve it in CI; receipt job queued at handoff",
    "alternatives_scored": "API-fallback 5/10 (auth/rate-limit flake), warn-don't-fail 3/10 (fail-open), one-liner fetch-depth: 0 at 9.5/10",
    "defect_repro": "local depth-1 clone at the tip: gate reported sha:62e59713 DEAD for the tip's real parent commit; identical body passed in full clone",
    "tests": "tests/test_receipt_gate.py (7 new, stdlib-only, hermetic); sabotage check: removing the fetch-depth line fails the pin"
  },
  "rule": "a_repair_receipt_must_depend_on_the_repair_route_its_evidence_through_the_fixed_mechanism",
  "procedure": [
    "cite handles (SHAs, paths, URLs) in the receipt that resolve only if the fix is real — the receipt's validity must be conditional on the fix",
    "never assert a fix works from outside the mechanism; the evidence must pass through the repaired path",
    "name and score every rejected alternative in the receipt (what it was, why it lost), so the reasoning survives",
    "pin the fix wiring in tests with a sabotage check: removing the fix line must fail the pin"
  ],
  "related": ["SN-0983 (receipt handles must resolve where the gate reads them — the finding this fix closed)", "SN-0978 (test the inertness as behavior, not as bytes — sibling proof-honesty note)"]
}
```
