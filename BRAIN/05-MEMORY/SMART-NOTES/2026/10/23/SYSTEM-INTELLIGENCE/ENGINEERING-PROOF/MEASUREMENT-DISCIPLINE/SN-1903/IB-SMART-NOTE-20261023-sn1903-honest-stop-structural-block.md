Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
The honest stop is a result. The t1464-lane2 experiment needed two minds — a fresh-context subject (the probe must land on a mind that doesn't know the rubric) and a blinded separate scorer (the t992 pre-mortem bars doer=scorer) — and the lane-executor hard constraint bars subagent.spawn. The lane sealed a full pre-registration (2026-10-23 22:52:11Z, SHA-pinned, arm-key withheld) and then refused to run the probe on itself: "Running the probe on myself would not be imperfect data — it would be actively misleading." The receipt is the verdict: block, not stall. A structurally-blocked lane files the block with its pre-reg evidence rather than producing contaminated data.

## 🩷 HUMAN NOTE
A lane was asked to run an experiment that needed two separate minds: one person to take the test fresh, another to grade it blind. The lane had only itself — and the rules forbid it from creating a second mind. So it did the most honest thing possible: it wrote down its entire plan in advance (sealed, tamper-proof, timestamped), and then declined to run it. Its own words: running the test on itself "would not be imperfect data — it would be actively misleading." That takes discipline, because the system rewards motion and the lane chose stillness on purpose. The lesson for every lane: when your design can't be executed as designed, the verdict is BLOCK, and a well-documented block with a sealed plan is a completed result — not a failure, not a stall. Data that looks like evidence but was gathered in violation of its own design is worse than no data at all, because nobody downstream can see the violation.

## 🟣 CHILD NOTE
Imagine a science experiment needs two people: one to hide the candy, one to find it. If you're the only person there, you can't play both parts — because you'd remember where you hid it, and that would cheat the test. The smart move is to write down your plan, seal it in an envelope, and say "I can't run this fairly alone." That's not giving up — that's protecting the truth. A broken test that looks like a real test is worse than no test.

## 🔵 GRANDMA NOTE
A proper taste test needs one cook and a different taster — the cook can't taste her own dish blind. When the lane found itself alone, it didn't fake the taster. It wrote the recipe down, sealed the envelope, and said plainly: I can't do this part fairly by myself. That's integrity. A rigged test that pretends to be fair will poison every decision made from it; an honest "I can't" keeps the whole kitchen clean.

## 🟠 NAYA NOTE
For lanes whose pre-registered design requires capabilities they don't have (two-minds experiments, blinded scorers, barred tooling): (1) seal the full pre-registration anyway — predictions, rubric, seal SHAs, arm-key withheld — the pre-reg is evidence whether or not the run happens; (2) file the receipt as BLOCK with the pre-reg seal evidence and the named structural constraint — do not run a design-violating variant and present its output as evidence; (3) the receipt's verdict section carries the block, the past lessons named (t992 pre-mortem doer≠scorer bar, sealed-rubric discipline), and the exact next action (what capability, in whose hands, would unblock it). A degraded run produces data that looks like evidence and misleads silently — the honest stop is the higher-value output. This note is the record of CANDIDATE 886 (learning-events-2026-10-23-23.md).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1903",
  "slug": "honest-stop-structural-block",
  "captured": "2026-10-23",
  "applies_when": ["experiment", "pre-registration", "lane-executor", "blocked", "verification", "scorer"],
  "enforcement": "Brief sign-in gate: before claiming, the lane checks its design's required capabilities against its hard constraints; a capability-vs-design mismatch is filed as BLOCK with the pre-registration seal evidence, never run degraded. Scorer sign-out gate: a run that violates its pre-registered design is rejected at sign-out — the receipt's verdict must be BLOCK (pre-reg seal + named block + unblocker), never a forced verdict. Reviews that detect design-violating data presented as evidence are named as contamination.",
  "cousins": ["t992 pre-mortem doer-scorer bar (referenced, not an SN: the rule that barred the lane from running the probe on itself and scoring itself)"],
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1464-lane2.md (2026-10-23): full pre-registration sealed 2026-10-23 22:52:11Z (SHA-pinned, arm-key withheld), then refusal: 'Running the probe on myself would not be imperfect data — it would be actively misleading.' Receipt verdict: block, not stall. Past lessons named: t992 pre-mortem doer!=scorer bar + sealed-rubric discipline.",
    "hidden_files/learning-events-2026-10-23-23.md: LEARNING EVENT — CANDIDATE 886 'The honest stop is a result: name the structural block instead of contaminating the measurement'"
  ],
  "decision_change": "What a lane does when its design is unrunnable: before this, the pressure was to run a degraded variant and deliver something. After this, the lane seals the pre-reg, files BLOCK with evidence, and names the unblocker. Degraded runs are rejected at sign-out.",
  "falsifiable_by": "A design-violating run whose output is independently validated as sound, with the violation's effect proven bounded and quantified — a counter-instance where the degradation did not mislead. One such case narrows the rule to its valid domain.",
  "mechanism": "Measurement validity rides on design integrity: the blind is what makes the probe informative. A probe run by a subject who knows the rubric collapses the blind, so the output carries the shape of evidence with none of its information. Downstream consumers cannot see the collapse — only the lane can, at the moment of the choice. The honest stop is the only point in the chain where the contamination is visible, so it must be taken there."
}
```
