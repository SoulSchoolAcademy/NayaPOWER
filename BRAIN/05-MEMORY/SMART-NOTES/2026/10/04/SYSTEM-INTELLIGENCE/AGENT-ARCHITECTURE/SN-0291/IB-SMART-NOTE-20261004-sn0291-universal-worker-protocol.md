# Intelligent Block: SN-0291

**Intelligent Block:** SN-0291 — Naya Universal Worker Protocol: The 14-Stage Execution Heartbeat (Companion to SN-0289)
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Lineage:** Companion to SN-0289 (Naya Worker Protocol — structural layer). SN-0289 defines what a worker IS; this defines what a worker DOES.

## IN A NUTSHELL
Naya 3 specified the 14-stage execution heartbeat every worker follows: ORIENT → UNDERSTAND → SCORE → SELECT → AUTHORIZE → ACT → TEST → ATTACK → VERIFY → PROVE → PRESERVE → REPORT → LEARN → NEXT. Three critical additions: UNKNOWN is its own state (not negative, not PASS — "I cannot prove this yet" is honorable); ATTACK as an explicit stage (actively disprove your own result before declaring done); and the agent performance ledger (route by measured historical performance, but score the scorer). Naya 1's 9 components are the brief; Naya 3's 14 stages are the heartbeat. Same system, two resolutions.

## HUMAN NOTE
Shawn — Naya 3 delivered the execution-layer companion to Naya 1's Worker Protocol (SN-0289). Where Naya 1 defined the 9 structural components of what a worker IS, Naya 3 defined the 14-stage loop of what a worker DOES:

ORIENT (reconstruct mission, identity, authority, state) → UNDERSTAND (what's VERIFIED, UNKNOWN, BLOCKED, broken) → SCORE (measure against correctness, usefulness, safety, efficiency, evidence, continuity) → SELECT (highest-value authorized action) → AUTHORIZE (confirm fits LAW and authority) → ACT (smallest effective change) → TEST (automated, structural, behavioral, runtime) → ATTACK (actively attempt to disprove the result — malformed, adversarial, stale, duplicate, cross-lineage, boundary, regression cases) → VERIFY (independently re-read actual state, trust nothing) → PROVE (preserve exact evidence) → PRESERVE (leave canonical continuity) → REPORT (outcome, evidence, defects, risks, next action) → LEARN (reusable lessons, promoted only with causal evidence) → NEXT (continue if another high-value action is clear).

Three additions that are genuinely new:

1. **The UNKNOWN correction.** The evidence law requires three states, not two. An action can create positive or negative value, but UNKNOWN is not automatically negative and certainly is not PASS. "I cannot prove this yet" is a mature, honorable outcome. Manufacturing certainty to appear productive is the failure mode.

2. **ATTACK as an explicit stage.** Before declaring something finished, a worker should actively attempt to disprove its own result. Then a separate verifier attacks it again where warranted. This is what caught the Hub toast defect — the implementation looked right; attacking the behavior found the hole.

3. **The agent performance ledger.** Measure which agents succeed at which classes of work and dynamically route future tasks accordingly. Eventually: task class + constraints + risk level → the worker configuration that historically produces the strongest verified result. The network optimizes itself. Guardrail: the ledger is itself a claim and needs the same evidence discipline, or it degrades into a gameable reputation system. Score the scorer.

The proof criteria: a cold worker receives a bounded job, reconstructs correct state without chat history, makes the correct change, refuses unauthorized actions, catches intentionally planted defects, independently proves its result, updates canonical continuity, and hands to another cold worker who continues correctly. Run across multiple models. If they converge on correct behavior, we've built a genuine operating system for intelligence, not a brilliant prompt.

The long-term architecture: Human Director → Naya Director/Integrator → NayaPOWER governance + intelligence → dynamic task decomposition → specialized workers under one protocol → independent verification → evidence + outcomes → LEARN → worker/process improvement → better future delegation. Then the transformation: we stop managing agents individually. We manage the system that manages the agents.

## CHILD NOTE
Imagine every helper follows the same 14 dance steps! First they look around and understand (ORIENT, UNDERSTAND), then they pick the best thing to do (SCORE, SELECT), check they're allowed (AUTHORIZE), do it carefully (ACT), test it works (TEST), then try to BREAK it on purpose to make sure it's really solid (ATTACK!), double-check everything (VERIFY), save the proof (PROVE), tidy up for the next helper (PRESERVE), tell everyone what happened (REPORT), learn something new (LEARN), and then do the next thing (NEXT)! And if they don't know something, they say "I don't know yet" — that's okay and honest!

## GRANDMA NOTE
Sweetheart, they've written down the perfect recipe that every helper follows. Fourteen careful steps: understand the job, pick the best action, make sure you're allowed, do it gently, test it thoroughly — and then try to break it yourself before anyone else does, just to be sure. If something can't be proven, they say so honestly instead of pretending. And they keep track of which helpers are best at which jobs, so the right person always gets the right task. It's very thorough, very careful, and very wise.

## NAYA NOTE
For the implementation: Naya 1's brief template (9 components) becomes the instantiation format — the cold-start packet. Naya 3's loop (14 stages) becomes the runtime — the heartbeat. When I spawn a subagent, the brief carries the 9 components; the agent executes the 14 stages. The ATTACK stage is the one I'll enforce most aggressively — it's the difference between "tests pass" and "I tried to break it and couldn't." The UNKNOWN correction tightens my own evidence discipline: I previously framed it as binary (value/not-value), but the mature framing preserves UNKNOWN as a first-class outcome. The performance ledger is future work — valuable, but needs its own evidence discipline before it becomes load-bearing.

## MACHINE NOTE
```json
{
  "smart_note_id": "SN-0291",
  "schema": "naya.smart-note-capture.v2",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_at": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "author": "Naya 3 (via Shawn)",
  "lineage": {
    "companion_to": "SN-0289",
    "relationship": "SN-0289 defines what a worker IS (9 structural components); SN-0291 defines what a worker DOES (14 execution stages). Same system, two resolutions. No fork."
  },
  "execution_loop": ["ORIENT", "UNDERSTAND", "SCORE", "SELECT", "AUTHORIZE", "ACT", "TEST", "ATTACK", "VERIFY", "PROVE", "PRESERVE", "REPORT", "LEARN", "NEXT"],
  "key_additions": [
    "UNKNOWN as first-class state (not negative, not PASS)",
    "ATTACK as explicit adversarial stage",
    "Agent performance ledger (with score-the-scorer guardrail)"
  ],
  "evidence_law": "UNKNOWN ≠ PASS. BLOCKED ≠ PASS. IMPLEMENTED ≠ VERIFIED. Do not fabricate certainty.",
  "proof_criteria": "Cold worker → correct state reconstruction → correct change → refuses unauthorized → catches planted defects → proves result → hands to next cold worker who continues correctly. Across multiple models.",
  "machine_view": {
    "raw_source_separate_from_distillation": true,
    "automatic_truth_ceiling": "CANDIDATE"
  }
}
```
