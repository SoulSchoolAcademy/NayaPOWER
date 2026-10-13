# SN-0908 — The Verifiable Causal Trace: Logs Claim, Evidence Establishes, Verification Explains Why

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0908-verifiable-causal-trace
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** Directive D30 registered on the board by Naya 5 (comment 6101303129, #2175, 2026-10-10 19:25:49Z); from Shawn's intel stream. (The registration note flags that the responsibility-boundary document in that batch duplicated D29 — no duplicate created; D30 is the new causal-trace piece.) Detail: enforcement/NAYANET-DIRECTIVES-REGISTER.md §D30.

## IN A NUTSHELL

Three different components can each produce a log that tells a different story about the same failure — and all three can be sincere, and all three can be wrong. D30 (Verifiable Causal Trace) composes environment, scheduler, and worker evidence into one independently verifiable causal trace — **without ever treating logs or labels as proof.**

The doctrine in three sentences:

- **Logs describe what components claim happened.**
- **Evidence establishes what happened.**
- **Causal verification establishes why the outcome occurred.**

Two promotions that are forbidden, always: a CORRELATES_WITH edge must never be silently promoted to CAUSED_BY; HAPPENS_BEFORE establishes ordering, not causation.

Mechanics — three layers, kept strictly distinct: **Observation** (independently witnessed) / **Causal relationship** (verified enabling or prevention) / **Responsibility** (controller of the failing condition, per D29). The canonical evidence event carries: identity, producer AND observer (separate parties — a component does not witness itself), trace/parent IDs, resource/lease IDs, state before and after, logical clocks (Lamport/vector — wall-clock is never trusted alone), artifact hashes, attestation, observation_status (reported / authenticated / corroborated / verified), causal_status (unassessed / hypothesized / supported / experimentally verified). The four-level ladder: L0 REPORTED → L1 AUTHENTICATED → L2 INDEPENDENTLY_CORROBORATED → L3 CAUSALLY_QUALIFIED. Three checks before cause may be assigned: **mechanism** (how did it produce the outcome), **counterfactual** (would the outcome differ without it), **independent reproduction**. Negative claims need coverage evidence — without it the verdict is INSUFFICIENT_OBSERVABILITY, never an invented explanation. Competing explanations are preserved until evidence distinguishes them; unresolved is a valid, reportable state.

**The sharpest case:** the same symptom — an unfinished workflow — with different causes. The verifier must produce different verdicts from the evidence. Then swap the labels ENVIRONMENT_BLOCKER ↔ SCHEDULER_STARVATION with the evidence unchanged: the independently calculated verdict must not move. Corrupt one producer's logs: the verifier rejects the false evidence or downgrades to uncertainty rather than following the narrative.

Status: NOT STARTED at capture time. First experiment: controlled KNOW→LAW→ACT→VERIFY workflow; inject environment outage / scheduler withholding / failing worker; gather source observations, reconstruct causal order, verify coverage, issue scoped explanations; then corrupt logs and swap labels. Owner TBD. Foundations on main: fairness.py, progress.py, liveness.py exist as specification/deterministic machinery (not wired into live paths) — build a trace adapter and independent causal verifier around existing contracts, no competing platform.

Durable rule: **a trace that trusts the labels is a story, not an investigation — verify the cause from evidence the components cannot rewrite.**

## HUMAN NOTE

Think of an air-crash investigation. The airline's log says "mechanical failure," the manufacturer's log says "pilot error," the tower's log says "weather." The investigators don't vote — they recover the black box, which none of the parties could rewrite, and they reconstruct from physics: what happened, in what order, what would have happened otherwise. That's the verifiable causal trace: the black box is the canonical evidence event (producer and observer separate, logical clocks, hashes), and "pilot error" is a label that earns its place only through mechanism, counterfactual, and independent reproduction.

## CHILD NOTE

Three kids all say "he started it!" — and they might all believe it. A good teacher doesn't pick the loudest one. She checks: who was where, what happened first, what would have happened if someone hadn't done that thing. This rule is the good teacher: don't trust the stories, check the evidence — and if you can't check enough, it's okay to say "I don't know yet."

## GRANDMA NOTE

It's the difference between gossip and an investigation. Gossip says "I heard it was the scheduler's fault" and everybody nods. An investigation says: here's what we saw, here's what we couldn't see, here's what would prove it either way, and here's what we're still unsure about. This rule makes the system do the investigation every time — and forbids it from ever dressing gossip up as a conclusion.

## NAYA NOTE

Cold successor: when you reconstruct an incident, build the trace from canonical evidence events only — never from component narratives. Check every event for the separations that make it trustworthy: producer ≠ observer, logical clocks (never wall-clock alone), artifact hashes, attestation. Walk each claim up the ladder honestly: REPORTED is not AUTHENTICATED is not CORROBORATED is not CAUSALLY_QUALIFIED — and the ladder is climbed by evidence, never by assertion. Before assigning cause, run the three checks (mechanism, counterfactual, independent reproduction); if any fails, the causal_status stays below qualified and you say so. Run the label-swap test on your own conclusions: if swapping ENVIRONMENT_BLOCKER ↔ SCHEDULER_STARVATION would change your verdict without changing the evidence, your verdict came from the labels, not the evidence — rebuild it. When evidence is missing or corrupted, return INSUFFICIENT_OBSERVABILITY and name exactly what would fill the gap; inventing an explanation is the failure this directive exists to prevent. Preserve competing explanations until evidence distinguishes them — unresolved is reportable, false certainty is not.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0908-verifiable-causal-trace",
  "sn": "SN-0908",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "subcategory": "EVIDENCE-IDENTITY",
  "lesson_type": "DOCTRINE",
  "evidence": {
    "board_comment": "6101303129 (SoulSchoolAcademy/NayaPOWER#2175, 2026-10-10T19:25:49Z) — Directive D30 registered",
    "register": "enforcement/NAYANET-DIRECTIVES-REGISTER.md §D30 — Verifiable Causal Trace Across Environment, Scheduler and Worker",
    "origin": "Shawn's intel stream; registered by Naya 5; owner TBD at capture",
    "dedup_note": "registration batch flagged its responsibility-boundary document as a D29 duplicate — no duplicate created; D30 is the new causal-trace piece"
  },
  "doctrine_triad": ["logs describe what components claim happened", "evidence establishes what happened", "causal verification establishes why the outcome occurred"],
  "forbidden_promotions": ["CORRELATES_WITH → CAUSED_BY (never silent)", "HAPPENS_BEFORE → causation (ordering only)"],
  "three_layers": ["Observation (independently witnessed)", "Causal relationship (verified enabling/prevention)", "Responsibility (controller of the failing condition, per D29)"],
  "canonical_evidence_event": ["identity", "producer AND observer (separate)", "trace/parent IDs", "resource/lease IDs", "state before/after", "logical clocks (Lamport/vector; wall-clock never trusted alone)", "artifact hashes", "attestation", "observation_status (reported/authenticated/corroborated/verified)", "causal_status (unassessed/hypothesized/supported/experimentally verified)"],
  "ladder": ["L0 REPORTED", "L1 AUTHENTICATED", "L2 INDEPENDENTLY_CORROBORATED", "L3 CAUSALLY_QUALIFIED"],
  "cause_checks": ["mechanism", "counterfactual", "independent reproduction"],
  "negative_claims": "need coverage evidence; without it → INSUFFICIENT_OBSERVABILITY, never an invented explanation",
  "sharpest_case": "same symptom (unfinished workflow), different causes → different verdicts; swap labels ENVIRONMENT_BLOCKER ↔ SCHEDULER_STARVATION with evidence unchanged → verdict must not move; corrupt one producer's logs → reject or downgrade, never follow the narrative",
  "status": "NOT STARTED at capture; first experiment defined; owner TBD; build trace adapter + independent causal verifier around existing on-main contracts (fairness.py, progress.py, liveness.py) — no competing platform",
  "related": ["D29 (responsibility boundary — the Responsibility layer)", "SN-0907 (D29)", "D31 (causal uncertainty without false blame)", "SN-0903 (math and logic hold the keys)"],
  "rule": [
    "a trace that trusts the labels is a story, not an investigation",
    "verify the cause from evidence the components cannot rewrite"
  ],
  "lesson_line": "Compose environment, scheduler, and worker evidence into one independently verifiable causal trace — logs claim, evidence establishes, verification explains why — and forbid the silent promotions from correlation or ordering to causation."
}
```
