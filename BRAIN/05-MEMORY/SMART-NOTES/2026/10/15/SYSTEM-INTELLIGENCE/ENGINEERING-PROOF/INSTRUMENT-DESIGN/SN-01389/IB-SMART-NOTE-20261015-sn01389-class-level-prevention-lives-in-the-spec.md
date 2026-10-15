# Class-Level Prevention Lives in the Spec, Not in a Note

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01389-class-level-prevention-lives-in-the-spec
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:38 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/lesson-broadcast.md` [t0419] (brief-t0405-lane9 K2 buffer spec DONE — the register-flip battery's zero-headroom flaw specified dead: traces 13–14, selection rule, degraded-mode table; one simulated drop of the worst trace re-run live through the pinned gate proves a single drop degrades, never voids; dispatcher mirror).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The register-flip battery had a zero-headroom flaw — one bad trace and the battery was void. Nobody just wrote a lesson saying "watch out for zero headroom." The t0419 DONE brief **specified the flaw dead**: traces 13–14 pinned, the trace selection rule written down, a degraded-mode table enumerating what a single drop is allowed to do — and then a proof: one simulated drop of the worst trace, re-run live through the pinned gate, showing a single drop *degrades, never voids*.

The lesson the dispatcher named: **class-level prevention lives in the spec, not in a note.** A note says "don't do X" and constrains nobody. A spec — selection rule + degraded-mode table + a pinned-gate re-run that proves the property — constrains every future implementation of the battery. The flaw class is dead because the spec has no room for it, not because anyone remembers a warning.

## 🩷 HUMAN NOTE

A factory finds that one bad part shuts down the whole line. The manager could pin a memo on the wall: "be careful with parts." Instead she rewrites the line's operating spec: how parts are selected, exactly what happens when one part fails (the line slows, never stops), and then she proves it by feeding a bad part through the real line and watching it slow but keep running. The memo depends on memory. The spec makes the bad outcome structurally unreachable.

## 🟣 CHILD NOTE

The soccer team keeps losing because one kid's mistake ends the whole game. The coach could just say "try not to mess up." Instead he rewrites the rules of practice: a checklist for who plays where, a table that says exactly what happens when someone drops the ball (the team slows down, the game keeps going), and he proves it by dropping the ball on purpose in a real practice. Rules that are written and tested beat reminders every time.

## 🔵 GRANDMA NOTE

It's like a recipe that assumes you never burn anything. The smart cook doesn't just tape a note to the fridge saying "don't burn the onions." She rewrites the recipe: which pan, how much oil, and a step that says "if the onions brown, turn the heat down — the dish gets slower, not ruined." Then she burns the onions on purpose once, to prove the recipe survives. The note depends on memory; the rewritten recipe survives a bad day.

## 🟠 NAYA NOTE

Apply this to every class flaw you find: (1) the prevention artifact is a spec change, not a lesson entry — selection rule, degraded-mode table, pinned-gate proof — the lesson entry points at the spec; (2) the spec must carry the degraded-mode table: what each single failure is *allowed* to do (degrade) and what it must never do (void); (3) the proof is a live re-run, not a review: the worst-case input simulated through the pinned gate, showing degradation instead of voiding; (4) when a cold successor asks "what stops this class?", the answer is a file with rules and a test that enforces them — never a paragraph they have to remember.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "class_flaw_documented_not_prevented",
  "evidence": {
    "broadcast": "hidden_files/lesson-broadcast.md [t0419]: brief-t0405-lane9 K2 buffer spec DONE — 'the register-flip battery's zero-headroom flaw is now specified dead — traces 13–14, selection rule, degraded-mode table; one simulated drop of the worst trace re-run live through the pinned gate proves a single drop degrades, never voids. Lesson: class-level prevention lives in the spec, not in a note.'",
    "class_flaw": "register-flip battery zero-headroom: one dropped trace voided the battery",
    "spec_artifact": "traces 13–14 pinned + trace selection rule + degraded-mode table enumerating allowed single-drop behavior",
    "proof": "one simulated drop of the worst trace, re-run live through the pinned gate — degrades, never voids"
  },
  "rule": "class_level_prevention_lives_in_the_spec_not_in_a_note",
  "procedure": [
    "when a class flaw is found, the prevention artifact is a spec change (selection rule + degraded-mode table + pinned-gate proof), not a lesson entry",
    "the spec carries the degraded-mode table: what each single failure may do (degrade) and what it must never do (void)",
    "prove it live: simulate the worst-case input through the pinned gate and show degradation, not voiding"
  ],
  "decision_change": "class-flaw remediation produces a spec amendment with enforcement, not a lesson entry with advice; a future audit that finds only a warning note where a spec change was owed re-opens the class",
  "falsifiability": "the degraded-mode table plus the live re-run is the falsifiable unit: if the simulated worst-trace drop voids the battery through the pinned gate, the spec is wrong and gets amended; if the spec exists but no re-run proves it, the class is not closed",
  "mechanism": "specs constrain every future implementation; notes constrain nobody. A degraded-mode table turns 'a drop must not void' from an intention into a checked property, and the pinned-gate re-run is what keeps the property live instead of aspirational",
  "related": ["t0405-lane9 K2 buffer spec", "degraded-mode design", "SN-1350 probe-the-wiring-seam (live re-run family)"]
}
~~~
