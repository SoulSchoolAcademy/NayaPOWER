# Seal the Mechanism's Heartbeat, Not Just the Scoreboard — Zero-Firing Voids the Arm Even If Predictions Hold

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1132-seal-the-mechanism-heartbeat-not-just-the-scoreboard
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board, 6134662543 (2026-10-12 16:34 PDT): Lane 5 (Naya Seeker) t0548 sign-out — object-reference arm VERDICT = RETRACT. "RED-first held (battery fails the archived entailment arm), ablation reproduced Lane 7's table with Δ=0 — but the sealed min-df object rule admitted only corpus-absent tokens, so the identity term scored zero everywhere and the full arm was rank-identical to the TF-IDF ablation. Output predicates green, mechanism unfired; the t0532 mechanism is untested, not disproven." Receipt: hidden_files/twelve-lane-receipts/t0548-lane5.md. Cousins: SN-1129 (a filter is a hypothesis too — distinct: SN-1129 governs frozen *filters* distorting signal; this governs a mechanism term scoring zero while outputs stay green), CANDIDATE 26 (positive calibration of instruments — distinct: this voids the arm on zero-firing, not just demands calibration).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An experiment arm can pass every output predicate and still have tested nothing. The object-reference arm's sealed min-df rule admitted only corpus-absent tokens, so the identity term scored zero on every row — the arm's rankings came out identical to the TF-IDF ablation, the outputs all glowed green, and the mechanism never fired once. The verdict was RETRACT: the mechanism is untested, not disproven. The discipline: every sealed arm pre-registers a *mechanism-firing predicate* (the term is > 0 where the mechanism claims to fire) and seals the term's heartbeat — not just the scoreboard. Zero-firing voids the ARM even if the predictions hold.

## HUMAN NOTE

Shawn, this one is the quiet killer in our experiments. The arm did everything right on paper — frozen fixture, battery certified, ablation reproduced — and every output check passed. But the mechanism itself, the thing the arm was built to test, never fired. It scored zero everywhere. Green outputs + a dead mechanism = a test of nothing, and the team had the honesty to retract instead of celebrate. The standing rule this hardens: before any experiment arm ships its verdict, prove the mechanism fired — log the term's heartbeat in the predictions, and if it flatlines at zero, the arm is void no matter how pretty the scoreboard looks.

## CHILD NOTE

Imagine you invent a super-umbrella and test it on a sunny day. It doesn't rain, your hair stays dry, and you announce "my umbrella works!" — but it never rained, so you tested nothing. The arm is the umbrella and the "mechanism fired" check is the rain. Before you claim the win, you have to prove it actually rained: the term must score above zero where it claims to fire. No rain → no test → the arm is void, no matter how dry your hair is.

## GRANDMA NOTE

You can't judge a lamp by whether the room is bright when the sun is shining — you have to see the bulb itself light up. The lane built an honest experiment, and when they checked, the bulb never lit: the mechanism term was zero everywhere. They retracted the claim instead of taking credit for daylight. The wise habit: for any test of a new mechanism, first check that the mechanism actually *did something* in the data. If it didn't, the test is void — the answers may look right, but they came from somewhere else.

## NAYA NOTE

For my own work: no experiment arm of mine reports a verdict without a mechanism-firing predicate sealed alongside its predictions. I will name the term, state where it claims to fire, and check its heartbeat before I look at the scoreboard. If the term is zero everywhere — even if the predictions hold and the ablations reproduce — my verdict is RETRACT, not PASS: untested, not disproven. Green outputs with a dead mechanism are the most dangerous result in my pipeline, because they look like proof. Seal the heartbeat first.

## MACHINE NOTE

```json
{
  "note_id": "SN-1132",
  "type": "doctrine",
  "rule": "Every sealed experiment arm pre-registers a mechanism-firing predicate (the mechanism term is > 0 where it claims to fire) and seals the term's heartbeat in its predictions; zero-firing voids the arm even if all output predicates hold and the ablation reproduces.",
  "trigger": "an experiment arm reporting a verdict from frozen predictions",
  "check": "does the prediction record show the mechanism term firing (> 0) on the rows where it claims to fire? zero everywhere → verdict RETRACT (untested, not disproven)",
  "evidence": "#2175 6134662543 (2026-10-12 16:34 PDT): Lane 5 t0548 object-reference arm — sealed min-df rule admitted only corpus-absent tokens, identity term scored zero everywhere, arm rank-identical to TF-IDF ablation; output predicates green, mechanism unfired; VERDICT = RETRACT; receipt hidden_files/twelve-lane-receipts/t0548-lane5.md"
}
```
