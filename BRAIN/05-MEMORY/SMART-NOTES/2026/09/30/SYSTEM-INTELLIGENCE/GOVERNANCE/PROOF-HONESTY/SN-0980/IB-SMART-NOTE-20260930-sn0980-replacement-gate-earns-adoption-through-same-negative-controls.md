# IB-SMART-NOTE — SN-0980

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/PROOF-HONESTY

## IN A NUTSHELL

SN-0954 proved the activation read-receipt gate was parrotable: copied answers with zero source reads minted `passed=True`, `verify()=True`. The night shift did not just diagnose — it built the replacement and earned its adoption the same way the old gate earned its rejection: by re-running the negative controls. The challenge-response prototype rejected 13/13 parrot answers in each of 3 attack shapes (8/8 adversarial tests green), was cross-seat reviewed, and landed in a decision brief: ADOPT WITH CHANGES. The decision names the four remaining adoption gaps explicitly — (1) a durable one-time challenge store (prototype uses memory), (2) an independent second implementation of the genuine path, (3) ratified policy values (1-hour challenge expiry, 40-byte evidence floor, which docs are eligible), (4) the agent-facing challenge wording — and holds the swap at Shawn's protected gate: no code moved. The durable rule: a replacement for a broken gate earns its adoption by surviving the same negative controls that broke its predecessor, with every remaining gap named and the swap itself gated. The diagnosis note (SN-0954) says what was wrong; this note says what adoption requires.

## HUMAN NOTE

We found a honesty check that a cheater could pass. We didn't just flag it — we built a replacement check and made it face the same cheaters: it caught all 13 in three different cheating styles. But we still didn't ship it. A decision document says "adopt, with changes," lists exactly four things that are still missing, and says the boss has to approve the swap. The lesson: proving the old thing is broken is only half the job. The new thing has to beat the same test, and you have to write down what's still open before anyone flips the switch.

## CHILD NOTE

If a cheater beats your test, you need a better test. But the better test has to beat the cheater too — make it catch all the cheaters before you trust it. And write down what's still missing, so nobody forgets.

## GRANDMA NOTE

You don't replace a broken lock with a new lock you haven't tested. You try every trick that beat the old one on the new one — and only then, after writing down what still needs doing, do you hang it on the door.

## NAYA NOTE

Future Naya: SN-0954 is the diagnosis template (parrot first, gate claim voided). This is the fix-forward template: (1) the replacement must be proven against the SAME negative controls that broke the old gate (here: 13/13 × 3 attack shapes rejected), (2) the decision brief names remaining gaps explicitly as adoption conditions, not as footnotes — a durable one-time challenge store, an independent second implementation of the genuine path, ratified policy values, agent-facing wording, (3) security-design swaps stay at the human gate; "no code moved" is a correct end state for the shift. Never swap honesty machinery by diff-review alone; adversarial tests are the adoption bar.

## MACHINE NOTE
```json
{
  "sn": "SN-0980",
  "slug": "replacement-gate-earns-adoption-through-same-negative-controls",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/PROOF-HONESTY",
  "doctrine": "a_replacement_gate_is_proven_by_the_same_negative_controls_that_broke_its_predecessor",
  "rule": {
    "adoption_requires": "replacement_survives_the_old_gates_negative_controls",
    "gaps_named": "explicit_adoption_conditions_not_footnotes",
    "swap_gate": "security_design_changes_stay_at_the_human_gate"
  },
  "evidence": [
    "night-shift-2026-10-10/morning-flags.md flag 5: challenge-response replacement rejected 13/13 parrots in each of 3 attack shapes; decision brief drafted t2332-c, cross-seat reviewed t2342-c",
    "night-shift-2026-10-10/receipts/parroting-gate-decision-brief.md: ADOPT WITH CHANGES — 4 named gaps: durable one-time challenge store (prototype uses memory), independent second implementation of genuine path, ratified policy values (1h expiry, 40-byte evidence floor, eligible docs), agent-facing wording; no code moved",
    "night-shift-2026-10-10/receipts/parroting-prototype/: prototype + 8/8 adversarial tests"
  ],
  "cousins": ["SN-0954 (diagnosed the parrotable read-receipt gate; recommended challenge-response)", "SN-0425 (name what you could not prove — receipt honesty)"],
  "distinct_from": "SN-0954 banks the diagnosis and the honest fix direction; this banks the adoption discipline — how a replacement earns its swap (same negative controls, named gaps, human gate)."
}
```
