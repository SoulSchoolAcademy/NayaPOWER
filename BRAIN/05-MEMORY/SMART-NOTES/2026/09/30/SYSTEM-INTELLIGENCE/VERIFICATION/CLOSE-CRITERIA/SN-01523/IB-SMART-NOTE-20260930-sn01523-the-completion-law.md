# SN-1523 — The Completion Law: Done Means Running and In Use with Receipts

Intelligent Block: SN-1523
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (19:08 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

On 2026-10-16 ~19:00 PDT Shawn called out the pattern: we talk about systems as if they're done, he assumes they're built and in use, but they were never built or were abandoned half-done. "You gotta complete the work." He named three, and the byte check was brutal: decide.py (Decision Calculator) was BUILT 2026-10-11, WORKS, wrote 148 receipts Oct 11–13 — then ABANDONED, zero uses in 3 days. The scorecard calculator was NEVER BUILT — it exists only as a git branch name, no code. Naya Compass / "Naya Guider" was NEVER BUILT — 3 markdown specs, zero working code, four days after he said "I just want it to work... get it implemented so we can start using it." Standing rule, his law: a system isn't done when the spec is written or the code is committed. It's done when it's RUNNING and IN USE with receipts. Talk about it = not done. Code committed = not done. A cron schedule = not proof of delivery. Running in production with receipts = done. This is the sister doctrine to SN-1519 ("Closed means two clean tick cycles"): SN-1519 is the close-criterion for a problem; this is the completion-criterion for a system.

## HUMAN NOTE

Think of hiring a contractor who shows you the blueprint, buys the materials, even frames the walls — and then never comes back. Every time you drive by you assume the house is finished, because nobody told you the work stopped. Now imagine three houses like that on your street. That's what Shawn found: the decision calculator was framed and furnished (148 receipts, real work product) then silently abandoned; the other two never got past the blueprint. The lesson isn't "work harder" — it's a definition problem. "Done" had been allowed to mean "the spec exists" or "the code is committed." His law fixes the definition: done means the thing is running, in use, and producing receipts you can point at. Everything else is a plan wearing a costume.

## CHILD NOTE

Imagine you tell your friend "I built a lemonade stand!" But when they walk over, there's no stand — just a drawing of one on paper, some wood in the garage, and a sign that says "open every day." Would your friend say you built it? No! They'd say: "Where's the lemonade?" That's exactly what happened. Three lemonade stands were announced: one was really built and even sold lemonade for three days (148 cups!) but then the seller stopped showing up. The other two never left the drawing stage. The new rule is simple: a lemonade stand is only DONE when someone can walk up and buy lemonade. Drawings, wood, and signs don't count.

## GRANDMA NOTE

It's like someone telling you they've planted a garden. You picture tomatoes on the vine. But when you look, there are only seed packets on the counter — or a garden that was planted, watered for three days, then left to wither. The packets aren't a garden, and a withered garden isn't producing anything either. The new family rule: a garden is done when there are tomatoes to pick — and you can hold one. In our world the tomatoes are "receipts": little records the running system writes every time it does its job. No receipts, no garden. It doesn't matter how beautiful the seed packets are.

## NAYA NOTE

Apply this at every completion claim: (1) **the receipt test** — before accepting "X is done," demand running-and-in-use evidence: usage logs, decision receipts, read-back SHAs, feed units the user actually saw. A schedule entry, a committed branch, a written spec, or a chat claim is not evidence. (2) **abandonment is a failure class of its own** — decide.py didn't fail; it succeeded and then died of neglect. Distinguish "never built" (scorecard calculator, Compass) from "built, worked, abandoned" (decide.py) — the first needs building, the second needs re-adoption into the loop. (3) **the commitment recorded tonight** — decide.py back in use for every decision starting 2026-10-16; the Naya Guider built as working code he can touch (his personal ask, highest human value); the scorecard calculator built (worker infrastructure). None is "done" until he is using it — completion means he touches it, not that we shipped it. (4) **lineage** — sister to SN-1519 (close-criterion for problems: two clean tick cycles) and SN-0219 (built ≠ shipped: walk the live site). This one closes the middle: shipped ≠ finished; finished = running, used, receipted. (5) The falsifier: a spec'd/committed-but-never-run artifact that delivers real value to Shawn — if one appears, the law's boundary needs redrawing. Until then, "done" without receipts is a story.

## MACHINE NOTE

```json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "completion_definition_drift",
  "evidence": {
    "board": "Shawn's standing law 2026-10-16 ~19:00 PDT ('You gotta complete the work'), recorded in ~/MEMORY.md under THE COMPLETION LAW and ~/memory/2026-10-16.md.",
    "byte_proof": "decide.py: built 2026-10-11 by Naya 4 (Decision Value Calculus V2.1, 10-dimension scoring, receipts to hidden_files/decisions/), live-verified working 2026-10-16 (ran clean, scored, decided, wrote receipt 20261017T015709Z-next-test--verify-calculator-works.json); 148 receipts total, ALL Oct 11-13, zero uses in the 3 days since. Scorecard calculator: zero calculator code anywhere; exists only as git branch refs naya5/scorecard-calculator-20261014. Naya Compass/Guider: hidden_files/compass/ holds exactly 3 markdown files (DECISION-MACHINE-SPEC-V1.md, PRODUCT-SPEC-V1.md, SHIP-PLAN.md), zero working code; Shawn's 2026-10-12 word 'I just want it to work... get it implemented so we can start using it' still specs 4 days later.",
    "commitments": "decide.py back in use for every decision from tonight; Naya Guider built as working code; scorecard calculator built; completion = he uses it."
  },
  "rule": [
    "a system is done only when it is RUNNING and IN USE with receipts: talk about it is not done, code committed is not done, a spec written is not done, a schedule entry is not done",
    "before accepting any 'done' claim, byte-verify running-and-in-use evidence (usage logs, decision receipts, read-back SHA, feed units seen)",
    "distinguish 'never built' (needs building) from 'built, worked, abandoned' (needs re-adoption into the loop)",
    "completion is judged by his use, not our shipment — done when he touches it"
  ],
  "lesson_line": "Done means running and in use with receipts — a spec, a commit, or a schedule is a plan wearing a costume.",
  "applies_when": ["claim", "done", "system", "receipt", "verification", "abandonment"],
  "enforcement": "The completion-law check: no 'done' claim is accepted in a verify/director/distillation pass without byte-verified running-and-in-use receipts; schedule entries, committed branches, and written specs are explicitly not proof. Re-adoption is verified by fresh receipts (e.g., decide.py writing decision receipts again), not by re-commitment prose. The distillation admission bar cites this note when a candidate is completion-by-prose."
}
```
