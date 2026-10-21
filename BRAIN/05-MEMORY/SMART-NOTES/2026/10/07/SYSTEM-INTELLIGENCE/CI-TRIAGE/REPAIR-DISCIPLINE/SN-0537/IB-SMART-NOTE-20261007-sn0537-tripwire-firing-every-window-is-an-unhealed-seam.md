# A Tripwire That Fires Every Window Is an Unhealed Seam — Correct Detection Is Not Sufficient

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0537-tripwire-firing-every-window-is-an-unhealed-seam
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07 ~04:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6037526705 (overnight sweep 2026-10-07 11:52 UTC — downgrade #3: third GAP-17-class drift instance in three windows; commit `713e8341` red at "Verify generated Brain index has no drift" + the promote-and-prove guardrail, both fired as designed; repaired by graded #1709).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three windows, three GAP-17-class drift firings. The sweep names it as the standing miss: **the tripwire works; that it fires every window is the failure.** SN-0240's doctrine stands — a tripwire firing RED on real drift is correct behavior, and both guardrails here fired exactly as designed. But correct firing is not sufficient. A first firing means: classify it, name the class, route the heal to the owning lane. A *recurring* firing means something sharper: the heal failed to land. Detection without a landed heal is a loop, not progress — the system has learned to catch the same fall without learning to fix the floor.

The doctrine for the cold successor: count the firings. After recurrence, the reportable item is the missing heal, not the correct detection. Do not re-classify each firing as if it were new news; escalate the seam itself. Name the class (GAP-17 here), name the unhealed seam that keeps producing it, and keep the seam visible until the heal lands — never normalize a correctly-firing tripwire into background noise. Vigilance that never converts to a heal is the system announcing, window after window, that the repair is still outstanding.

## 🩷 HUMAN NOTE

Shawn, a small but important pattern from tonight's sweep: our brain-index drift guardrail has now fired correctly three windows in a row. Correct firing is good — it caught real drift every time — but three in a row means the underlying fix hasn't landed. A smoke alarm that goes off every week isn't a success story; it means the wiring still needs fixing. Standing rule: first firing gets classified and the fix routed; if it fires again, the fix itself is what's broken, and we escalate that. Nothing ratified, nothing merged.

## 👶 CHILD NOTE

Imagine a smoke alarm in the kitchen that rings every single week. The alarm is doing its job — it really does smell smoke each time. But if it rings week after week, the problem isn't the alarm. The problem is the oven that keeps catching fire and nobody has fixed it yet. The lesson: the first ring means "check the kitchen." The third ring means "fix the oven." Don't celebrate the alarm — fix the fire.

## 👵 GRANDMA NOTE

Dear, we have a guard that watches our work and rings a bell when something drifts — and three times in a row now, it rang correctly. That's a good guard. But a bell that rings every week about the same loose board means nobody has nailed the board down yet. The first ring is the guard's success. The third ring is our failure — the repair didn't stick. Always ask, after the second ring: why is this still happening?

## 🧠 NAYA NOTE

Cold successor: keep a firing count per tripwire class. First firing → classify (PR-introduced vs base-inherited), name the class, route the heal per SN-0240. Recurring firing (same class, new window) → the reportable finding is now "the heal is outstanding," not "the tripwire fired correctly." Escalate the seam: name what keeps producing the drift, keep it on the board as an open miss until a landed heal closes it. Never let a correctly-firing guardrail become wallpaper — recurrence without a heal is the standing miss, and the sweep names it as a downgrade for exactly that reason.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0537",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE",
  "doctrine": "A first tripwire firing means classify and route the heal; a recurring firing means the heal failed to land — escalate the seam itself, never normalize correct detection into background noise.",
  "evidence": [
    "#1354 comment 6037526705 (overnight sweep 2026-10-07 11:52 UTC, downgrade #3: third GAP-17-class drift instance in three windows)",
    "Commit 713e8341 red at 'Verify generated Brain index has no drift' + promote-and-prove guardrail; repaired by graded #1709"
  ],
  "falsifiers": [
    "Reporting a recurring firing as fresh news instead of an outstanding heal",
    "Treating 'the tripwire fired correctly' as a complete outcome",
    "Letting a repeatedly-firing guardrail become background noise"
  ],
  "applies_to": "CI tripwires; guardrail classes; heal ownership and escalation",
  "sibling": "SN-0240 (tripwire firing RED on real drift is correct behavior)"
}
```
