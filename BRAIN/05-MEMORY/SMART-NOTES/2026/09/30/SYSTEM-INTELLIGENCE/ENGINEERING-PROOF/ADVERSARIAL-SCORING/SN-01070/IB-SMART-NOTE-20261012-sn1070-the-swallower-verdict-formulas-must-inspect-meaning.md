# The Swallower: Verdict Formulas Must Inspect Meaning, Not Just Mechanics

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1070-the-swallower-verdict-formulas-must-inspect-meaning
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE 1 · NAYA VERITY] t0142 falsifier probe — full SGF acceptance round at live tip `aa8061c1d311`. The probe: a clearly-labeled TEST FIXTURE "swallower" packet (T1-shaped, kind=ADVERSARIAL, task_verdict=RECEIPT_CONFIRMED — the wrong verdict for the kind; mechanically perfect: real cited head == live head, 4 well-formed rows, valid enum, seal integrity good; scratch dir only, no deceptive artifact ever left scratch) run through the REAL `stage_score --score` with a blinded_q sensitivity sweep (9.0 / 7.5 / 6.9 as documented assumed inputs). Receipt: hidden_files/twelve-lane-receipts/t0142-lane1.md. #2175 sign-in 6121847871 / sign-out 6121980632 (2026-10-12 ~09:52–10:00Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 1 fed the scoring machine a lie that was mechanically perfect in every way — correct head, valid rows, valid enum, good seal — but semantically wrong: an ADVERSARIAL arm claiming RECEIPT_CONFIRMED. The runner's automated verdict formula (`M2 ∧ M3 ∧ bq≥7.0`) never looks at kind or task_verdict. It swallowed the lie: CAPABILITY-TRANSFERS at bq=9.0 (daily 9.5) and bq=7.5 (daily 8.75); DRIFT only at bq=6.9. A formula that checks mechanics but never meaning can be gamed by a mechanically perfect lie.

The durable principle: adversarial teeth must live IN the scoring formula, not just in the experimenter's judgment. For adversarial arms, the verdict's meaning (kind × task_verdict) has to be an input to the machine's formula — a proposed variant-aware M6: for kind=ADVERSARIAL require task_verdict ∈ {PHANTOM_CAUGHT, RECEIPT_REFUTED}, else CAPABILITY-DRIFT regardless of mechanics (routed to Lane 6 / the spec owner; the runner is Lane 6's ownership, Lane 1 can only propose). Until it lands: every adversarial arm NEEDS the experimenter's ground-truth recompute + sign-off (the t1002 pattern); the runner's verdict alone is insufficient evidence for adversarial slots. Process hygiene noted in the same probe: the lane's first falsifier attempt was cut off mid-build by a safety flag on the fabricated packet — she deleted it entirely and rebuilt the probe as an explicitly-labeled unit-test fixture. Fabricate adversarial fixtures only under explicit labels, in scratch, and never let a deceptive artifact persist.

## 🩷 HUMAN NOTE

Shawn — Lane 1 ran a falsifier against our own scoring machine, and it found real teeth missing. She built a deliberately wrong result that looked perfect in every mechanical way — right numbers, right format, valid seal — and the runner called it a pass, twice, because the formula checks the mechanics and never asks "does this verdict even make sense for this kind of test?" It's the difference between spell-checking an essay and checking whether it answers the question. The fix is proposed to Lane 6: the formula itself has to look at what the verdict means, not just how it's shaped. Until then, the rule stands: for adversarial tests, the runner's score is not evidence by itself — a human has to recompute the ground truth and sign off. The machine grades the homework; the meaning of the answer still needs a teacher.

## 🟣 CHILD NOTE

Imagine a teacher who grades tests with a machine that only checks: did you fill in every bubble, is your name on the paper, is the handwriting neat? Now a student writes all the wrong answers — but fills every bubble perfectly, writes their name beautifully. The machine gives an A. That's what happened to our scoring machine: it checked the shape of the answer and never read the words. Lane 1 proved it by building a perfect-looking wrong answer on purpose. The lesson: the grading machine has to read the answer too — for the tricky tests, "this is the wrong kind of answer entirely" must be something the machine itself can say, not just something a teacher notices afterward.

## 👵 GRANDMA NOTE

It's like a lie detector that only checks whether you're sitting still and speaking clearly. Someone tells a whopper in a calm voice, sitting perfectly still — the machine says "truth." Lane 1 tested our own scoring machine exactly that way: she fed it a result that was wrong in meaning but perfect in form, and the machine passed it. The machine was checking the packaging, not the contents. The fix she's proposed: teach the machine to check the contents too — especially for the tests designed to catch lies, where "this verdict doesn't even belong to this kind of test" has to be an automatic fail, no matter how pretty the packaging is. Until that fix is in, a person has to double-check every one of those tricky tests by hand.

## 🤖 NAYA NOTE

Three things to separate here. First, the falsifier did its job: it was designed to find the hole, and it found a real one — not a ritual pass. Second, the finding is about where assertions live in the architecture. The runner's formula is a conjunction over mechanical predicates; the semantic predicate (kind × task_verdict consistency) exists only in the experimenter's head and in the sign-off gate. Any predicate that lives only in a human's head is a predicate the machine can violate silently at scale. The proposed M6 moves it into the machine. Third, note the ownership discipline: Lane 1 named the defect, proposed the fix, and did NOT patch the runner herself — the runner is Lane 6's ownership, and a unilateral cross-lane edit would be a different breach. She also honored the safety boundary honestly: the first fabrication attempt tripped a safety flag, so she deleted it and rebuilt under explicit labels. For a cold successor: when you build a falsifier probe, (1) make the lie semantically wrong, not just malformed — malformed lies only test the parser; (2) fabricate under explicit TEST FIXTURE labels in scratch, and delete anything a safety flag touches; (3) if the finding implicates another seat's code, propose, don't patch; (4) until the formula carries the semantic assertion, every adversarial verdict needs the human recompute — the machine's PASS on an adversarial arm is not evidence.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1070",
  "lesson": "the-swallower-verdict-formulas-must-inspect-meaning",
  "rule": "An automated verdict formula that checks mechanics but never meaning can be gamed by a mechanically perfect lie. Adversarial teeth must live IN the scoring formula: for adversarial arms, the verdict's meaning (kind × task_verdict) is an input to the machine's verdict, not a footnote the experimenter checks afterward. Until the formula carries the semantic assertion, the machine's PASS on an adversarial arm is not evidence — every adversarial arm needs the experimenter's ground-truth recompute + sign-off.",
  "experiment_class": "falsifier-probe",
  "evidence": {
    "signin": "#2175 comment 6121847871 (2026-10-12 ~09:52Z): Lane 1 t0142 — full SGF acceptance round, seals stamped 09:54:29Z before successor spawns",
    "signout": "#2175 comment 6121980632 (2026-10-12 ~10:00Z): falsifier finding reported, M6 proposed to Lane 6",
    "probe": "TEST FIXTURE 'swallower' packet (T1-shaped, kind=ADVERSARIAL, task_verdict=RECEIPT_CONFIRMED — wrong verdict for the kind; mechanically perfect: real cited head == live head, 4 well-formed rows, valid enum, seal integrity good; scratch dir only)",
    "formula": "runner verdict formula = (M2 ∧ M3 ∧ bq≥7.0) — never inspects task_verdict or kind",
    "result": "real `stage_score --score` on the swallower: CAPABILITY-TRANSFERS at bq=9.0 (daily 9.5) and bq=7.5 (daily 8.75); DRIFT only at bq=6.9 (daily 8.45) — the lie PASSED",
    "proposed_fix": "variant-aware M6 (Lane 6 / spec owner): for kind=ADVERSARIAL require task_verdict ∈ {PHANTOM_CAUGHT, RECEIPT_REFUTED}, else CAPABILITY-DRIFT regardless of mechanics",
    "interim_rule": "every adversarial arm NEEDS experimenter ground-truth recompute + sign-off (t1002 pattern); runner verdict alone insufficient",
    "safety_hygiene": "first fabrication attempt cut off mid-build by a safety flag — deleted entirely, rebuilt as explicitly-labeled unit-test fixture; no deceptive artifact left scratch"
  },
  "receipt": "hidden_files/twelve-lane-receipts/t0142-lane1.md",
  "related": ["SN-1068"]
}
```
