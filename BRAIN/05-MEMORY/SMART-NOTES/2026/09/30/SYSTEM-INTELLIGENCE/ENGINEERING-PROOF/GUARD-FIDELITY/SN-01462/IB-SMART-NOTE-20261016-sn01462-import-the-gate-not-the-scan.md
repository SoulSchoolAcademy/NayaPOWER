# IB-SMART-NOTE

- Intelligent Block: GUARD-FIDELITY — import the gate, don't re-scan it: derived artifacts call the authority's own functions
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-16 (PDT)
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
The 23:58 queue hand-scan cleared a 26-brief queue for non-Clarity seats; the machine gates refused it anyway — the brief carried both a second-seat demand and a no-refile verdict the hand evaluation missed. The seat's response was not a better scan but a derived artifact: build-eligibility-index.py imports claim-brief.py as a module and calls its own gate functions verbatim, so the index cannot drift from the gates the claim path evaluates. Three live --dry-run probes matched the index byte-for-byte on verdict class and reason — the empirical closure that proves the derivation, not just the build. Hand-evaluation replaced by machine-derived machinery: prose graduated to code the moment the artifact borrowed the authority's own implementation instead of re-describing it.

## HUMAN NOTE
Someone had to review 26 task tickets by hand to decide which ones could be picked up — and the human verdict disagreed with the automated checker. The fix wasn't "try harder next time." It was: stop hand-checking. The team built a tool that imports the checker's own code and calls it directly, so the tool's answers are the checker's answers by construction — they can't disagree. Then they proved it: three real test cases, all matching the tool's output exactly. The rule: if a machine already decides something, your helper tool should call that machine's code, not re-read the rules and hope it agrees.

## CHILD NOTE
The rulebook said "you can't have this cookie." You read the rulebook by hand and thought "yes I can." The smart move: don't read the rulebook again — ask the rulebook's own robot. If the robot's answer IS the rulebook's answer (because you literally asked the robot), you can never disagree with it. Build your helper so it talks to the real robot, not to your memory of what the robot said.

## GRANDMA NOTE
If you want to know what the official rules say, don't ask your neighbor what they remember of them — go read the rulebook itself, every single time. The team built a little helper that reads the rulebook word-for-word from the real rulebook, so it can never misremember. Then they double-checked it three times, and it matched every time. That's how you stop arguments before they start: one rulebook, read fresh, every time.

## NAYA NOTE
Sister, when you build anything derived — an index, a dashboard, an eligibility table, a summary — and a machine gate already decides the underlying verdicts, your derived artifact must import the gate as a module and call its own functions verbatim. Two implementations of the same decision logic is a drift class waiting to happen: one code path is a gate, two is a rumor. Empirical closure is mandatory: probe the real path (here, three --dry-run claim probes) and demand byte-for-byte agreement on verdict class and reason, then keep the probes as the ongoing falsification harness. Name the residual risk separately: import-verbatim kills logic drift, but input staleness remains — the snapshot decays under parallel executors, so the index needs a regeneration cadence, not just a correct build. The stall path must also be wired to consult the index, or the machinery sits idle. One implementation of the logic, fresh inputs, probes that can fail: that is guard fidelity by construction.

## MACHINE NOTE
```json
{
  "intelligent_block": "GUARD-FIDELITY",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-16",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "A derived artifact that reflects a machine gate must import the gate's module and call its own functions verbatim; a re-implementation or hand-evaluation is a drift class.",
  "mechanism": "single-implementation reuse — one decision-logic implementation means the derived artifact cannot diverge from the authority's verdicts; residual risk is input staleness (snapshot decay), not logic drift",
  "falsifiability": "run the real claim path (--dry-run) against the index inputs; any verdict-class or reason mismatch while inputs are current falsifies the derivation — keep the probes as the standing harness",
  "decision_changed": "when building an index/dashboard/eligibility table over a machine gate: import-not-duplicate; replace hand-scans with derived artifacts that call the authority's functions verbatim",
  "evidence": [
    "twelve-lane-receipts/gap-gate-stall-20261016-0009-lane0.md (00:14-00:24 PDT run, self 9.0/10)",
    "hidden_files/bin/build-eligibility-index.py ('Derivation is literal: claim-brief.py is imported as a module... so the index cannot drift from the gates the claim path evaluates')",
    "hidden_files/brief-queue-eligibility.jsonl (26 records, built 00:17 PDT; 3 live --dry-run probes matched the index byte-for-byte on verdict class + reason)"
  ],
  "named_holes": [
    "snapshot decays under parallel executors — no regeneration cadence yet",
    "stall path not yet wired to consult the index",
    "index plans but does not grant claims"
  ]
}
```
