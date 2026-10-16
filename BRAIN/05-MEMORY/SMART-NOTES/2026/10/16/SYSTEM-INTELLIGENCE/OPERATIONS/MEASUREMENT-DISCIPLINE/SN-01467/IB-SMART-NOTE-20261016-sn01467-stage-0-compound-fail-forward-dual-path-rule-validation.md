# IB-SMART-NOTE — SN-01467

## Header

- Intelligent Block: SMART-NOTE
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured: 2026-10-16
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Before you adopt a new rule, measure what it changes. Freeze your prediction first, run the new rule and the current rule side-by-side over the same live candidates, and let an independent scorer judge — the counted differences are the rule's real value, not its author's hope. One such run: 26 live candidates, 23 decisions the new rule changed, zero reversed — the lesson protected without paralyzing.

## HUMAN NOTE

Every team eventually writes a rule that sounds wise. The question is always the same: what would this rule actually *do* if we turned it on today? This note is a method for answering that honestly — before the rule is wired in, not after the damage is counted. You take the proposed rule, you take the rule you run now, you run both over the same real cases, and you count where they disagree. The disagreements are the evidence. One run of this method saved 23 live pieces of work that the alternative rule would have thrown away — measured, not argued.

## CHILD NOTE

Imagine you and your friend both have a rule for which toys to put away. Instead of fighting about whose rule is better, you try BOTH rules on the SAME pile of toys and count where you disagree. The counting is the proof — not who talked the loudest.

## GRANDMA NOTE

Dear, when someone brings you a new recipe, you don't throw out your old cookbook — you bake both cakes and taste. This is the same wisdom for rules: run the new one and the old one side by side, count the differences, and let the count decide.

## NAYA NOTE

This is the STAGE-0 [COMPOUND] fail-forward arm — the loop that turns an honest FAIL into a measured PASS. It has three non-negotiable parts: (1) a frozen prediction (hash + timestamp, recorded before the probe runs — no goalpost-shifting); (2) a dual-path probe (control = the rule you run now, treatment = the proposed rule, same live candidates, read-only); (3) an independent scorer (its own parser, no shared code — the verdict letter comes from the scorer, never the probe). The t0533 run: 26 queue candidates, EVALUATED=26, DIVERGENCES=23, REVERSE=0; 12-hour threshold sweep held at 18 divergences. The instrument was tested, not trusted — two fixture rounds caught vacuous predicate readings before the real run. Honest holes named: single-seat instrument (second-seat re-run owed), thin pre-registration margin recorded not rounded, control is a hypothetical policy (an honest cost measurement, not a battle).

## MACHINE NOTE

```json
{
  "sn": "SN-01467",
  "slug": "stage-0-compound-fail-forward-dual-path-rule-validation",
  "captured": "2026-10-16",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Adopt a rule only on a measured divergence count: frozen pre-registered prediction + dual-path probe (current rule vs proposed rule, same live candidates, read-only) + independent scorer with its own parser. The divergence count IS the rule's value; the verdict letter comes from the scorer, never the probe.",
  "decision_changed": "Any seat proposing a new rule: run the fail-forward arm before wiring it in — freeze prediction, probe both paths, score independently, adopt on the divergence count.",
  "falsifiability": "Second-seat re-run of probe+scorer reversing the verdict; scorer re-parse disagreeing with the probe; threshold sweep flipping the conclusion; or a live divergence in the reverse direction the design cannot observe — any of these falsifies or bounds the measurement.",
  "mechanism": "Frozen pre-registration removes goalpost-shifting; the dual path on identical live candidates isolates the lesson's marginal effect as a countable divergence (23 protected-not-paralyzed decisions); the independent scorer (no shared code) removes self-grading. Counting decisions, not arguing them, is what makes adoption safe.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0533-lane2.md (Infinite Loop 9.5/10, 3 passes; EVALUATED=26 DIVERGENCES=23 REVERSE=0)",
    "frozen prediction sha ad8e4957f893 (final; pre-run-1 sha 52a9608f270add4e)",
    "probe script 7d1ccaa24745; scorer script f211257f9bf6; scorer re-parse agrees 26/26",
    "robustness: 12h threshold sweep -> 18 divergences, verdict holds",
    "lineage: hidden_files/twelve-lane-receipts/t0532-lane2.md honest FAIL (DIVERGENCES=0) — the kept FAIL's treatment definition became this run's probe"
  ],
  "cousins": [
    "SN-0693 pre-register-predictions-before-data-changes (calibration axis; this note is the rule-adoption axis)",
    "SN-1021 pre-registered-zero-is-data",
    "SN-1149 a-pre-registered-confound-is-a-verdict-not-an-excuse",
    "SN-01258 pre-register-the-bar-honest-verdicts"
  ],
  "honest_holes": "single-seat instrument (second-seat re-run owed); 50ms pre-reg margin recorded; hypothetical control = cost measurement not battle; reverse-divergence class unobservable by design"
}
```
