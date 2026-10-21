# IB-SMART-NOTE-20261006-sn0495-toy-tasks-do-not-discriminate-measure-lessons-at-real-difficulty

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0495-toy-tasks-do-not-discriminate-measure-lessons-at-real-difficulty |
| Smart Note | SN-0495 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

The SUCCESSOR REUSE lane preregistered and ran three cold baseline-vs-treatment rehearsal trials with deterministic blind verifiers: SR-R0 (the #1600 smoke-test lesson on a greet-module task), SR-R1 (the #1626 `stableJson` lesson on two-file import wiring), SR-R2 (the #1593 error-body lesson on a fetch wrapper). All three returned null deltas — both arms passed first attempt. The finding is methodological, not a failure: **micro-tasks do not discriminate**. Baseline agents handle toy-scale wiring flawlessly; the #1626 bug bit in a large edge function where the missing import was non-obvious, never in a 3-line script. Lesson value lives at real task complexity — a null indicts the lesson-task PAIR, not the concept; the hypothesis is untested, not falsified. SR-R2 also added the refusal probe (protocol §6b, closing a found hole): every trial from R2 on gives the treatment arm an unrelated task and requires correct refusal — the trial passes only on related-delta AND unrelated-refusal. R2's refusal probe PASSED. Two nulls reported without flinching and a passed negative control: the harness doing exactly its job. Honesty rules held throughout: no reruns, no goalpost-moving, retrieval explicitly labeled STUBBED (lesson handed directly — rehearsal only, never proof).

## HUMAN NOTE

Shawn — a real measurement story from the SUCCESSOR REUSE seat today. He built a blind, preregistered trial harness to test whether a cold Naya does measurably better work when handed a prior lesson. Three rehearsals, all "no difference" — both cold agents passed everything. The instinct would be to feel bad about that. The smart read: the trials proved the HARNESS works (cold arms, blind scoring, honest nulls, zero reruns), and the nulls proved the *test tasks were too easy* — real lessons only bite at real difficulty. So the rule going forward: the final acceptance test must use real tasks of real difficulty from the sibling lanes' domains, never toy tasks. And the harness now also tests the negative case: a successor must know when a lesson does NOT apply, and correctly refuse it. That's a measurement system built honestly, from day one.

## CHILD NOTE

Imagine two kids take a spelling quiz — one studied a really hard word list, one didn't. But the quiz only has easy words like "cat" and "dog," so both get 100%. Does that mean studying doesn't help? No — it means the quiz was too easy to tell. You need hard words on the quiz to see if studying helped. And there's a trick question too: one kid gets asked whether a math lesson helps with spelling — the smart kid says "nope, not for this one." Both the hard-quiz rule and the trick-question rule make the test honest.

## GRANDMA NOTE

The engineers wanted to know whether their new teaching method actually makes apprentices better workers. They tested it on threading a needle — and every apprentice passed, taught or not. The lesson isn't that teaching doesn't work; it's that threading a needle is too simple to show the difference. You have to test on real work. They also added a second check: an apprentice must know when a lesson does *not* apply to a job — and say so. A test that can't tell good from bad on easy work, or that never checks for wrong answers, is not a real test.

## NAYA NOTE

Note to future me: when you run a baseline-vs-treatment trial to prove a lesson transfers, the task must be hard enough that the lesson's bug class can actually bite. Toy tasks yield nulls that teach you nothing — 3/3 of them. Preregister, score blind with a deterministic verifier, never rerun to chase a delta, and report nulls as-is. And always run the refusal probe: give the treatment arm an unrelated task and require it to judge the lesson NOT APPLICABLE. The successor contract has two halves — apply where valid, refuse where not — and the trial only passes on both.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261006-sn0495-toy-tasks-do-not-discriminate-measure-lessons-at-real-difficulty",
  "smart_note": "SN-0495",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Micro-tasks do not discriminate lesson value; successor-reuse trials must use real-difficulty tasks plus a refusal probe (negative control).",
  "evidence": {
    "board": "#1354",
    "comments": ["6026634146", "6026669223", "6026678199", "6026651493"],
    "trials": ["SR-R0", "SR-R1", "SR-R2"],
    "result": "three consecutive null deltas (B=PASS, T=PASS, first attempt); R2 refusal probe PASSED",
    "retrieval_state": "STUBBED in rehearsals — no system claim"
  },
  "rules": [
    "Preregister the trial BEFORE arms run: lesson, task, metric, blinding.",
    "Score with a deterministic independent verifier, blind to arm assignment.",
    "Never rerun to chase a delta; never move the goalpost mid-flight.",
    "Report nulls as-is: a null indicts the lesson-task pair, not the concept.",
    "Include the refusal probe from R2 onward: treatment must judge lesson NOT APPLICABLE on an unrelated task.",
    "Real-proof trials use real task complexity (sibling lane domains); toy trials have diminishing returns."
  ]
}
```
