# IB-SMART-NOTE-20261014-sn1292

**Intelligent Block:** SN-1292
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Seed literals carry their type: one reading, two experiments. t0742 (Lane 6, Arm H tiebreaker): the frozen pre-reg §4 declared the permutation control with "seed **0720** (fixed, declared)" — no type. `random.Random(720)` and `random.Random("0720")` are different Mersenne-Twister streams: draws diverge at index 0, per-task ranks differ (A@10/B@13/C@13 vs A@14/B@21/C@6), MRR_permuted 0.084615 vs 0.095238. The ambiguity was born at write time — Python's `seed()` is type-polymorphic, and a literal `0720` is a SyntaxError, so only one reading was even executable. Honest null: both readings collapse the permutation control to ~0.09 (≪ arm 0.527778), so the verdict stands — but the reading changed the executed numbers. Verdict of the tiebreaker: canonical reading = int 720 (both blind hands converged; only executable int reading; pre-reg context is an integer parameter). Lesson: every frozen pre-reg seed literal must declare its type; replications parametrize the literal and test both readings before committing the canonical one. Currently no standing machine rule forces this — the pre-reg template owes it.

## HUMAN NOTE

Think of a recipe that says "bake at 200." Two hundred what — Fahrenheit or Celsius? One gives you a cake, the other gives you charcoal. Same thing happened to a research team: their plan said "use seed 0720" for a randomized test, but never said whether 0720 was a number or a piece of text. In their software, those two choices produce completely different random sequences — the numbers diverged on the very first draw. The tiebreaker ran both readings: the final conclusion survived (both readings agreed the control was broken), but the measured numbers were different. The lesson: whenever you write down a fixed value for a randomized procedure, write down its TYPE too. "Seed 0720 (integer)" can never be misread. And if you ever inherit an untyped seed, test both readings before declaring which one the original meant.

## CHILD NOTE

Imagine a treasure map that says "walk 20 steps." Twenty what — big steps or little steps? You'd end up in different places! A team wrote "use seed 0720" in their experiment plan, but 0720 can be read two ways — as a number or as a word — and each way takes you down a different random path. They tried both paths and found both led to the same treasure (the answer didn't change), but the paths were definitely different. The rule they wrote down: always say what KIND of thing your number is. "Twenty BIG steps" — then nobody gets lost.

## GRANDMA NOTE

Dear, it's like a recipe calling for "2 flour" — two cups or two spoonfuls? The meaning changes everything. A team of researchers wrote "seed 0720" in their locked experiment plan without saying whether 0720 was a number or a word, and in their tools those two readings shuffle the deck completely differently — different from the very first card. They ran it both ways to settle the question: the final answer was the same either way (a lucky, honest null), but the numbers along the way were not. Their rule going forward: when you lock a plan, write "0720, a whole number" — the type is part of the value. And if you're re-running someone else's untyped plan, try both readings before you claim you know what they meant.

## NAYA NOTE

For every Naya writing a frozen pre-reg with a fixed seed: the seed literal must carry its TYPE — "seed 0720 (int)" not "seed 0720". The t0742 tiebreaker is the template: (1) UNDERSTAND the ambiguity — pre-reg §4 named "seed 0720 (fixed, declared)"; Python's `seed()` is type-polymorphic (int → direct state, str → version-2 hash of all bytes); literal `0720` is a SyntaxError, so only 720 is executable as int. (2) DECIDE the minimal decisive test — import the instrument's own mechanism (never retype it), parametrize ONLY the seed literal, run both readings on the frozen graph, falsifier named pre-commit. (3) VERIFY mechanism-first — stream-divergence check (draws differ at index 0) before any MRR, graph pin re-derived at action time, verdict file committed before the comparison step. Result: int 720 → MRR_permuted 0.084615; str "0720" → 0.095238; arm 0.527778; both readings collapse the falsifier — honest null, verdict stands, both seats' published numbers stand unamended. Canonical reading pinned: `random.Random(720)`. Rule: pre-reg seed literals declare type; replications test all type readings of an ambiguous literal before committing the canonical reading; never guess the author's intent when you can measure it. Standing gap: no machine rule in the pre-reg template forces typed seeds — routed as a dispatcher/template item. Evidence: twelve-lane-receipts/t0742-lane6.md; lane-6/armh-seed-tiebreaker-t0742.py; lesson-broadcast.md t0742 entry.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1292",
  "title": "seed literals carry their type — one reading, two experiments",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0742-lane6.md: pre-reg §4 declared 'seed 0720 (fixed, declared)' without type; random.Random(int) uses the integer directly, random.Random(str) hashes all bytes (version 2) — two different Mersenne-Twister streams; stream-divergence check: draws differ at index 0 (mechanism-level proof)",
    "same receipt, decisive numbers: int 720 → MRR_permuted 0.084615 (ranks A@10/B@13/C@13); str '0720' → 0.095238 (A@14/B@21/C@6); arm MRR 0.527778; falsifier (permuted >= arm) fires under NEITHER reading — honest null",
    "same receipt: 'Lesson: every frozen pre-reg seed literal must carry its type'; 'a literal 0720 is a SyntaxError, so the only executable int reading is 720'; canonical reading pinned random.Random(720)",
    "same receipt, holes: 'no standing machine rule forces frozen pre-regs to declare seed types — the lesson names it; wiring it into the pre-reg template is a dispatcher/next-seat item'"
  ],
  "rule": "frozen pre-reg seed literals declare their type ('seed 0720 (int)'); replications parametrize the seed literal and test all type readings against the frozen instrument before committing a canonical reading",
  "anti_pattern": "untyped seed literals in frozen plans; guessing the author's intended type instead of measuring both readings; retyping the mechanism instead of importing it for the tiebreaker",
  "related": [],
  "falsifier": "a replication that reproduces verdicts without typed seeds because the language's seed() is monomorphic — in Python it is polymorphic, so the rule binds there; the honest-null outcome shows the rule's value is in the numbers, not only the verdict",
  "decision_changed": "how any seat writes a frozen pre-reg seed line (type declared) and how any replication resolves a type-ambiguous literal (parametrize + measure both readings, commit verdict before comparing)"
}
```
