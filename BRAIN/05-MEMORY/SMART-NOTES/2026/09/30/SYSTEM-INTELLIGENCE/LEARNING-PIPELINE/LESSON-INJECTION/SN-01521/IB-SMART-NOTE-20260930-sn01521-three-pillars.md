# SN-1521 — Shawn's Three Pillars: Learn Near-Instantly Is #1 — the 1 → 3 → 2 → 1 Loop, with Phase-A Injection as the Working Evidence

Intelligent Block: SN-1521
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (18:08 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Shawn ranked the mission's three pillars (2026-10-16 17:51 PDT): **(1) Learn near-instantly** — lessons land at decision time, behavior actually changes, intelligence compounds; **(2) Smart apps humans love** — push-button simple, creation inside it, "without this, everything else is useless"; **(3) A system built for Nayas to build in.** The loop: 1 makes 3 smarter → 3 builds 2 better → 2 brings humans whose use feeds 1. Phase A of his lesson-injection directive was built the same hour as proof of pillar 1 *with no new infrastructure*: 14 seeded lessons with `applies_when` tags + `enforcement` each, the dispatcher injects the top-3 tag-matches into every brief's Injected lessons field, injections log to lesson-injection-log.jsonl, and the brief receipt spec carries a fold hit/miss verdict per injected lesson. Phase B (helper script) and C (lesson store service) come later — learning moves at decision time now, not after the infrastructure is ready.

## HUMAN NOTE

What Shawn said, in his order: learning is the #1 pillar and it is currently failing the test he set — "filing lessons is not learning." He walked the walk requirement into the room: repetition alone is not proof of embedding; proof is a closed loop where lessons visibly change later decisions. Phase A is the first closed loop on record: the lesson doesn't go into a file and die — it arrives in the brief *before the work starts*, and the receipt asks the worker whether it folded into the work. The first fold-HIT verdict is the experiment's real output; the seed file is just the apparatus. His filter for everything new still applies: does it get us live, public, world-class faster? The pillars are the ranking key for that filter.

## CHILD NOTE

Imagine you want to learn to ride a bike. There are three important things: (1) learning from every wobble right away, (2) having a bike you actually want to ride, (3) having a neighborhood where you can ride. The order matters: learning comes first, because learning from wobbles makes your neighborhood better (you pave the road), which makes your bike better, which makes more friends want to ride with you, which gives you more wobbles to learn from. And the smart move: you don't wait for the perfect helmet-and-gear store to open before you start learning — you start with the bike you have, and you get a tip written on your handlebars *before* each ride, and you check *after* the ride whether the tip helped.

## GRANDMA NOTE

Learning comes first — but only if the learning actually changes what you do next time. A lesson filed away is just a diary. A lesson placed in your hands before the decision, and checked afterward, is a habit. Build the habit with what you have; build the bigger system after the habit works.

## NAYA NOTE

This is the doctrine note for the loop that already exists in machinery: the Learning Pipeline (capture → distill → embed → exercise → violate → correct → graduate) is the strategy; the three pillars are the ranking; Phase A is the tactic. The mechanism that makes it more than a poster: tag-intersection matching at brief time — the lesson arrives in the decision surface, not in a separate place nobody reads. Note the deliberate inversion of the usual sequencing error: "we need the lesson store before lessons can land" was declined in favor of "land lessons in the existing surface now; build the store after Goal #1." The fold hit/miss receipt is the falsifier: if injected lessons never produce a single fold verdict, the loop is decorative and pillar 1 has not moved. This note also sets the filing gate's parentage: the FILING GATE on the distillation loop (bounce candidates missing `applies_when` or `enforcement`) is pillar-1 machinery — a lesson that can't name its enforcement isn't learning, it's filing.

## MACHINE NOTE

```json
{
  "sn": "SN-1521",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T01:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "LEARNING-PIPELINE",
  "sub": "LESSON-INJECTION",
  "lesson": "Shawn's three pillars, ranked: (1) Learn near-instantly — lessons land at decision time, behavior changes, intelligence compounds; (2) Smart apps humans love — push-button simple, creation inside it; (3) A system built for Nayas to build in. The compounding loop: 1 makes 3 smarter → 3 builds 2 better → 2 brings humans whose use feeds 1. Phase A proved pillar 1 moves with no new infrastructure: 14 seeded lessons (applies_when + enforcement each), dispatcher injects the top-3 tag-matches into every brief's Injected lessons field, injections logged, and each receipt reports a fold hit/miss verdict per injected lesson. Build the habit with what exists; build the bigger system after the habit works.",
  "decision_change": "Sequencing and filtering now route through the pillar ranking: learning-at-decision-time beats infrastructure sequencing (Phase B/C wait for Goal #1). New work passes Shawn's filter: does it get us live, public, world-class faster? Lesson-design follows the Phase-A pattern: match tags into existing decision surfaces instead of waiting for a lesson store.",
  "falsifiability": "The loop is testable: if injected lessons never produce a fold hit/miss verdict in receipts, Phase A is decorative and pillar 1 has not moved — the instrumentation (lesson-injection-log.jsonl + receipt fold field) exists precisely so this failure is visible. If learning lands (fold hits rising) but no human adoption follows, pillar 2's loop leg is refuted, not pillar 1. A directive is not a prediction; the falsifiable part is the loop's instrumentation, which is live.",
  "mechanism": "Tag-intersection matching at brief time: each lesson carries applies_when mission-class/area/failure-signature tags; the dispatcher matches the brief's tags and injects the top 3 into the brief's Injected lessons field. The worker then reports, in the receipt, whether each injected lesson folded into the work (hit) or not (miss). CAPTURE (distillation) → INJECT (brief) → FOLD (receipt) is the closed loop; filing without the fold leg is just storage. No new infrastructure was needed because the decision surface (the brief) already existed.",
  "evidence": [
    "live board #2641 comment 6227556378 (2026-10-17T00:47:48Z, content verified live): Shawn's directive letter — the three pillars in his ranking, the 1→3→2→1 loop, the three phases, per-seat changes, sequencing; Goal #1 (Smart Note flow) keeps its lead",
    "hidden_files/lessons.jsonl — 14 seed records, every one carrying applies_when tags + enforcement (tag-intersection matching simulated and verified); night-dispatcher body carries the LESSON INJECTION step; brief template PART 1 gained the Injected lessons field; receipt spec gained the fold hit/miss verdict; injections logged to lesson-injection-log.jsonl",
    "smart-note-distillation loop body updated with the FILING GATE: candidates missing applies_when or enforcement in the MACHINE NOTE are bounced, not staged — 'a lesson isn't learned until it names its enforcement' is now a gate, not a motto"
  ],
  "cousins": ["lessons.jsonl 'single-writer' / 'gate-skip' / 'show-me-done' / 'three-pass-flow' (Phase-A seed siblings — the same tag+enforcement shape)", "SN-0342 (supreme-law enforcement arm — pillar-1 measurement of a standing law with no enforcement arm)", "CORE-PRINCIPLES.md capture→distill→embed→exercise→violate→correct→graduate loop (this note's strategy home)"],
  "dedupe_guard": "Not a duplicate: no existing note names the three pillars, their ranking, or the 1→3→2→1 compounding loop. lessons.jsonl seeds are single lessons; this note captures the ranking doctrine, the loop, and the no-new-infra Phase-A pattern. SN-0342 covers one specific un-enforced law; this note covers the learning-pillar doctrine and its injection machinery.",
  "applies_when": ["learn", "lesson-injection", "brief", "distillation", "sequencing"],
  "enforcement": "Every lane brief carries an Injected lessons field (top-3 tag-matched); every receipt reports a fold hit/miss verdict per injected lesson; injections log to lesson-injection-log.jsonl. The distillation FILING GATE bounces candidates missing applies_when or enforcement in the MACHINE NOTE. The first fold-HIT verdict is the proof that pillar 1 has moved."
}
```
