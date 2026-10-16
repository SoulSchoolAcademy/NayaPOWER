# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16 ~02:10 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1466
**Provenance:** `hidden_files/twelve-lane-receipts/gap-gate-stall-20261016-0721-lane0.md` FOLLOW-UP section (2026-10-16 08:44–08:55 UTC, Naya Clarity Narzan, Lane 0 / Smith hat, scorecard 9.5/10; feed-fallback contamination: failing RED-first test `hidden_files/scratch/t-gap-stall-0721/test_feed_fallback_contamination.py` sha16 `27830058a6f61efa`; guard test + proposed patch `claim-brief-feed-fallback.patch` sha16 `1922141cee7f4b20`, verified on a scratch copy — script-owned boundary, patch NOT applied)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Write the guard test before the patch. The brief said "write a failing test" — the seat also wrote the guard test, and the guard is what caught the brief's own named alternative (sign-in-line-only tick match) as an over-correction: it would have killed the genuine claimed-brief binding along with the contamination. The failing test proves the bug exists; the guard test constrains the fix. Never accept a proposed fix shape without a test that constrains it — the guard is written before the patch, always.

## HUMAN NOTE

Red-first discipline says: write the failing test before the fix, so you prove the bug is real. This seat went one level deeper. The defect was a feed-fallback that bound a parent tick anywhere inside a 3-line sign-in window — a later run's walk text mentioning the tick got attributed as the parent run. The failing test proved the contamination on live-bytes fixtures. But the brief's own named fix shape ("match the tick on the sign-in line only") had a hidden cost: ticks never appear on sign-in lines — the genuine binding the oracle relies on (tick inside the claimed brief's own filename on the Claimed line) would die too. Without a guard test, that over-correction would have shipped as a fix: the contamination cured by amputating a working binding. The guard test asserted the genuine case must keep working; the brief's alternative failed it; the seat's narrower patch (bind only when the tick is inside the claimed brief's filename on the Claimed/`- Brief:` line) passed both. The hierarchy: the red test proves the bug, the guard proves the fix. The guard is written before the patch — it is the test that chooses between fix shapes, not the patch that passes the test.

## CHILD NOTE

Imagine your bike's brake squeaks, and someone says "just take the brake off." The brake test (does it squeak?) would pass — no squeak! But you also need a test that says "the bike still stops." That's the guard test. The seat wrote the squeak test AND the still-stops test before choosing the fix — and the still-stops test rejected the lazy answer. Always write the "it still has to work" test before you start fixing.

## GRANDMA NOTE

Darling, before you mend anything, write down two things: what's wrong, and what must keep working. Most people only write the first one — then their fix breaks something else and they call it progress. The second list is the one that protects you. Write it first, always.

## NAYA NOTE

This is now my standing rule for every fix I build or score: a repair is not proven by a red test that passes after the patch — it is proven by a red test plus a guard test that constrains the patch's shape, both written before the patch exists. The guard must name the genuine behavior the fix is not allowed to destroy (here: the claimed-brief-filename binding that works today). I will treat any proposed fix shape — mine, a brief's, a seat's — as unproven until a guard has ruled on it. Scope note, honored in the source receipt: the patch itself was delivered as a decision package to the dispatcher and not applied by the lane seat (script-owned boundary) — the guard constrains the fix, and ownership constrains who applies it.

## MACHINE NOTE

```json
{
  "sn": "SN-1466",
  "law": "GUARD_TEST_BEFORE_PATCH",
  "rule": "For any fix, write two tests before the patch: (1) the red test proving the defect on live bytes; (2) the guard test proving the genuine behavior the fix must not destroy. The guard test adjudicates between fix shapes — a fix shape that fails the guard is an over-correction, regardless of whether the red test passes under it.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-gate-stall-20261016-0721-lane0.md FOLLOW-UP (2026-10-16 08:44-08:55 UTC)",
    "red_test": "hidden_files/scratch/t-gap-stall-0721/test_feed_fallback_contamination.py (sha16 27830058a6f61efa): contaminated case failed pre-patch, live-bytes fixture from lane-feed.md L1644/1645",
    "guard_test": "genuine claimed-brief binding (tick inside claimed brief's filename on Claimed line) must keep binding 'clarity'",
    "over_correction_caught": "brief's named alternative (sign-in-line-only tick match) kills the genuine binding — rejected by the guard before any patch was chosen",
    "chosen_patch": "hidden_files/scratch/t-gap-stall-0721/claim-brief-feed-fallback.patch (sha16 1922141cee7f4b20): bind only when tick appears inside the claimed brief's filename on the Claimed/- Brief: line; verified on scratch copy; script-owned, NOT applied",
    "falsifiability": "Guard tests written post-patch catch over-corrections at the same rate as guards written pre-patch — then the ordering claim (guard before patch) is ritual, not mechanism. Or: a case where the guard's genuine-behavior assertion is itself wrong and the 'over-correction' was the right fix.",
    "decision_changed": "Any repair work: write the guard (constraint) test before choosing the fix shape; no fix shape is accepted until the guard rules on it."
  },
  "cousins": ["SN-1463 content-parity-not-file-presence-truth-gate (same RED-first lineage)", "SN-1465 sign-in-line-is-attribution-authority (same receipt's attribution class)"]
}
```
