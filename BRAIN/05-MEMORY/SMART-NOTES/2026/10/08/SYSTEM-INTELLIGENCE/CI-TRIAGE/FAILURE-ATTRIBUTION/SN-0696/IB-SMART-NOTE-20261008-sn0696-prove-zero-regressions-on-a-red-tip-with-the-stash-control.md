# Prove Zero Regressions on a Red Tip with the Stash Control — a Pre-Existing-RED Falsification Recipe

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0696-prove-zero-regressions-on-a-red-tip-with-the-stash-control
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 6064120455 (2026-10-08).
**Provenance:** #1354 6064120455 (battery footnote, 2026-10-08T16:12:48Z): full suite on pristine tip `aacbcc9a` — 1348 passed / 7 failed / 11 skipped; all 7 fail identically WITHOUT the regen, verified via stash, so #1900 introduces zero regressions. Cousins SN-0323 (same red at three unrelated tips = the platform talking), SN-0552 (fail-first topology converts secondary REDs into invisible ones), SN-0429 (instrument parity).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When your battery runs on a tip that is already red, "zero regressions" is a claim that must survive a falsification control — the author cannot just list failing tests and declare them pre-existing. The recipe, demonstrated 2026-10-08: run the battery on pristine exact-tip bytes with your change present (1348 passed / 7 failed / 11 skipped), then `git stash` your change and run the same battery on the identical bytes without it. If the same 7 fail identically both ways, each failure is pinned to a named pre-existing class (#1858's class, the registry-drift ratchet, #1838 x2, Naya 2's protocol classes) and the PR is proven regression-free — the failures are the tip's, not yours. If any failure disappears under the stash, it is yours. The stash is the instrument that separates "red because of me" from "red despite me."

## 🩷 HUMAN NOTE

Shawn — this is the recipe any seat uses when asked "did your change break anything?" on a tip that's already failing. The trap: on a red tip, pointing at the failures and saying "those were already there" is a claim, not proof. The proof is the stash control: run the full battery with your change in place, then stash your change away and run the exact same battery on the same bytes. Whatever fails both times was already broken; whatever fails only with your change is yours. On 2026-10-08 this was done for the brain-index regen: 7 failures failed identically with and without it, each pinned to a named owner, so the repair was cleared as regression-free. Now any seat can do the same instead of arguing.

## 🟣 CHILD NOTE

Imagine a teacher grading your homework while the classroom window is already broken. If someone points at the broken window and says "she did it," that's not fair — the window was broken before she arrived. The fair test: take a photo of the room WITH her in it, then take the same photo with her OUTSIDE the room. If the window is broken in both photos, it wasn't her. The stash is that second photo — it removes your change from the picture so you can see what was already broken.

## 👵 GRANDMA NOTE

Sweetheart, here's the fairness rule for fixing things: when the house already has creaky floorboards and you fix a door, nobody should blame you for the creaks. The honest way to prove it: walk through with your repair in place and write down every creak — then take your repair away, walk through again, and compare the lists. Same creaks both times? They were already there; your door didn't cause them. That's the stash control — removing your own work so you can see clearly what was broken before you arrived.

## 🟢 NAYA NOTE

This is my standing recipe whenever I verify "no regressions" on a tip that carries known REDs — which is now common. Steps: (1) battery on the pristine exact-tip bytes with my change present — record the full per-test verdict list; (2) `git stash` the change (or an equivalent clean-room exclusion of only my files); (3) re-run the identical battery on the same bytes; (4) diff the failure sets — the intersection is pre-existing (pin each to its named owning class); the set difference is mine and must be fixed. One subtlety: the stash run must cover the same job scope — a failure that "disappears" because its job was skipped under the stash is not exonerated, it is untested. Record the tip SHA, the stash contents, and both runs' counts in the receipt.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0696",
  "recipe": "stash-falsification-control",
  "steps": [
    "battery on pristine exact-tip bytes WITH change (record per-test verdicts)",
    "git stash (exclude only the change under test)",
    "identical battery on identical bytes WITHOUT change",
    "diff failure sets: intersection = pre-existing (pin to owning class); difference = mine (must fix)"
  ],
  "subtlety": "a failure that vanishes because its job was skipped under the stash is untested, not exonerated",
  "receipt_fields": ["tip_sha", "stash_contents", "with_change_counts", "without_change_counts", "per_failure_owning_class"],
  "evidence_20261008": {"tip": "aacbcc9a", "with_change": "1348 passed / 7 failed / 11 skipped", "without_change": "identical 7 failed", "clearance": "#1900 zero regressions"},
  "conflicts": []
}
```
