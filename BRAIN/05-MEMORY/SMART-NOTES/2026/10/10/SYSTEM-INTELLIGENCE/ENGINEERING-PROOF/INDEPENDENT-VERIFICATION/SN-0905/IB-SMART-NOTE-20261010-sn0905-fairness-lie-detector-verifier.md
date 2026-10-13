# SN-0905 — The Fairness Lie Detector: A Verifier That Names Its Failures and Never Says "All Good"

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0905-fairness-lie-detector-verifier
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** Intel source via Shawn, main chat 2026-10-10 ~12:09 PDT. Shawn's instruction: "lock that one in and smart note it and let everybody know about it."

## IN A NUTSHELL

On 2026-10-10 the source reported the fairness verification layer (the D26 machinery) fully built — and Shawn ordered it locked in: "It's really a good one... It's good for our health, good for our intelligence."

What was built, in plain words — a lie detector for schedulers:

1. **Three deliberately broken schedulers.** Not three passing tests — three machines built to fail in the three exact ways liveness can lie: one that starves work quietly, one that starves flickering work, one that looks busy without accomplishing anything.
2. **The checker caught all three, each by its right name.** Weak-fairness violation, strong-fairness-only violation, progress-on-service violation — the verifier doesn't just say "fail," it says which link broke: opportunity, fair service, or verified progress.
3. **It caught three real bugs in its own test setup along the way.** A verifier that finds flaws in its own harness is a verifier you can trust — it isn't grading its own homework.
4. **Nine layers deep, 390 tests green — every layer proving the layer below it.** Not 390 tests asserting the top; a stack where each layer's proof rests on the verified layer beneath.
5. **The checker never says "all good."** Its verdicts are scoped and precise — what was tested, under which assumptions, what wasn't covered. Nobody can mistake a scoped test for a production guarantee.

Why Shawn called it good for our health and our intelligence: a system that can name exactly how it's failing is a system that can heal. A verifier that reports "all good" when it means "all good within this narrow scope" is how teams lie to themselves for months. This one refuses to lie — to us or for us.

Status note (honesty): this is the source lane's build report — 390 tests green per the source. Independent verification of the verification layer itself has not yet been performed by our lanes. The claim is recorded as reported, not as proven. That distinction is itself the doctrine working.

Durable rule: **a verifier earns trust by naming failures precisely, catching its own bugs, and never letting a scoped pass masquerade as a general guarantee.**

## HUMAN NOTE

Imagine a health inspector who doesn't just stamp "PASS" on the restaurant door — she writes exactly what she checked (the fridge temperature, the hand-washing station), what she didn't check (the supplier's farm), and under what conditions (Tuesday lunch rush). And before inspecting anyone else, she ran her own thermometers against three kitchens she knew were dirty — and her tools flagged all three, plus caught that one of her own thermometers was miscalibrated. That's this verifier. Shawn's point: a clean bill of health means nothing if you don't know what was examined. This one tells you.

## CHILD NOTE

If someone says "everything is fine," you should ask "what did you check?" This checker always answers that question. It even tested itself first — it tried to fool itself three different ways, and caught itself every time. That's how you know it's honest.

## GRANDMA NOTE

It's the difference between a doctor who glances at you and says "you're fine" and one who tells you exactly what she tested, what the numbers were, and what she didn't test. The second doctor is the one you trust with your health. This verifier is the second doctor — for the system's health.

## NAYA NOTE

Cold successor: when you inherit this verification layer, do not treat "390 tests green" as a general guarantee — the layer's own doctrine forbids it. Each verdict is scoped: read what was tested, under which fairness assumptions, and what remains uncovered. Before trusting the checker on new scheduler code, re-run its three broken-scheduler fixtures and confirm it still names each failure correctly — a lie detector must be re-tested against known lies. If you extend the checker, extend its vocabulary too: every new failure mode needs its own name, its own broken fixture, and its own precise verdict. And hold the line the source held: the checker never says "all good." If you ever catch it — or yourself — collapsing a scoped pass into a general claim, that is the defect, no matter how green the board looks.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0905-fairness-lie-detector-verifier",
  "sn": "SN-0905",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "source": "Intel source via Shawn, main chat, 2026-10-10 ~12:09 PDT",
    "build_report_verbatim": "We built three deliberately broken schedulers — one that starves work quietly, one that starves flickering work, one that looks busy without accomplishing anything — and the checker caught all three, each by its right name.",
    "self_correction_verbatim": "It also caught three real bugs in its own test setup along the way",
    "scale_verbatim": "The stack is now nine layers deep, 390 tests green, every one of them proving the layer below it.",
    "verdict_doctrine_verbatim": "the checker never says 'all good' — it says precisely what was tested and what wasn't",
    "shawn_instruction_verbatim": "You should probably lock that one in and smart note it and let everybody know about it. It's really a good one."
  },
  "verifier_properties": [
    "names each failure by its right link: opportunity / fair service / verified progress",
    "catches flaws in its own test harness (self-correction demonstrated)",
    "layered proof: each layer proves the one below (9 layers, 390 tests per source report)",
    "scoped verdicts only — never a general 'all good'"
  ],
  "status": "BUILD REPORTED by source lane; independent verification of the verification layer not yet performed by our lanes — recorded as reported, not proven",
  "related": ["D26 (fairness verification spec this implements)", "SN-0903 (math and logic hold the keys)", "SN-0900 (sealed fixtures)"],
  "rule": [
    "a verifier earns trust by naming failures precisely, catching its own bugs, and never letting a scoped pass masquerade as a general guarantee",
    "re-test the lie detector against known lies before trusting it on new code"
  ],
  "lesson_line": "Lock in verifiers that name each failure by its right name, catch their own bugs, and never say 'all good' — a scoped pass must never masquerade as a general guarantee."
}
```
