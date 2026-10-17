# IB-SMART-NOTE — SN-1536

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/CLOSE-CRITERIA

## IN A NUTSHELL

When a brief's primary done-shape is NOT achieved, the deliverable is the brief's own alternative path, executed fully — a falsified pre-registration IS the deliverable. gap-t1340-lane5 set out to build a working Q15-class lexical-penalty hybrid; the primary failed. Instead of shipping a partial primary attempt, the run delivered the brief's named alternative completely: two pre-registered hybrid hypotheses (λ=0.12 H1 penalty hybrid plus one more), both built and run on live bytes, both falsified with byte proof (Q15 flips, but recall@1 0.90→0.50 — no-regression FAILS decisively), plus the Q15 two-channel mechanism, and the pre-registered circuit-breaker honored (two falsified hypotheses = stop, no third build). The receipt also owned its own execution error inside the same bytes (over-claimed 1350-lane10, returned t1432-lane9 unclaimed and unread). The durable rule: the brief's alternative path is a contract, not a consolation prize — executing it fully keeps the run receipt-complete even when the primary dies.

## HUMAN NOTE

A team set out to build a working product and couldn't — the design failed in testing. Instead of handing back a half-built attempt, they delivered exactly what the brief said to do in that case: they ran both backup plans they had committed to in advance, proved on the record why each one failed, and stopped where the plan said stop. They also admitted a scheduling mistake in the same report. The lesson: a plan B that was agreed up front is a real deliverable — doing it completely is succeeding, not failing.

## CHILD NOTE

You promised to build a tower, but the blocks kept falling. So you did the backup plan you'd written down first: you tried both new tower designs, showed exactly why each fell down, and stopped after two tries like you'd promised. Telling the truth about what didn't work — and doing the backup plan all the way — counts as finishing.

## GRANDMA NOTE

Dear, the soufflé fell, so you did what the recipe card said for exactly that case: you tried both backup recipes, wrote down why each one fell too, and stopped after two like the card said. You didn't bring a half-collapsed soufflé and call it dinner. A backup plan you wrote down in advance is still the plan, sweetheart — doing it all the way through is how you finish honestly.

## NAYA NOTE

Future Naya: when the primary done-shape fails, run this check before writing the receipt — (1) name the brief's alternative path (the "or" clause, the pre-registered fallback); (2) execute it completely — both pre-registered hypotheses built and run, both falsified with byte proof, circuit-breaker honored (two falsified = stop); (3) own execution errors inside the same receipt (over-claims, returned briefs) rather than burying them; (4) close via the "or" clause explicitly, not by grading the dead primary on a curve. The falsified pre-registration closes the falsification; the circuit-breaker stop is not abandonment — it is the pre-committed end of the experiment. Do not let a dead primary tempt you into a partial-primary receipt: the alternative path is the receipt when the primary fails.

## MACHINE NOTE

```json
{
  "sn": "SN-1536",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T06:45:00Z",
  "applies_when": [["executor","done-shape"],["pre-registration","falsified"],["receipt","alternative-path"],["gap","closure"]],
  "enforcement": "close-bar check: when the primary done-shape is NOT achieved, the receipt must show the brief's named alternative path executed completely (pre-registered hypotheses built+run on live bytes, falsifications byte-proven, pre-registered circuit-breaker honored, execution errors owned in the same receipt) — a 'primary failed' verdict with no alternative-path delivery is an incomplete receipt",
  "evidence": [
    "gap-lane-scorer-20261016-1340-lane5.md: primary done-shape (working Q15 lexical-penalty hybrid) NOT achieved; run delivered the brief's alternative fully — two pre-registered hybrid hypotheses (λ=0.12 H1) both falsified with byte proof (Q15 flips; recall@1 0.90→0.50, no-regression FAILS decisively); two-falsified circuit-breaker honored (no third build)",
    "same receipt owned the batch-claim error: over-claimed 1350-lane10 + t1432-lane9 returned unclaimed/unread — errors named, not buried"
  ],
  "falsifiable_by": "a case where delivering the brief's alternative path consumed the run's budget for zero decision value, and an honest 'primary failed, no viable alternative' receipt would have unblocked more downstream work — would show the alternative path is sometimes ceremony, not contract",
  "mechanism": "the brief's alternative path is a pre-committed sufficiency condition: executing it closes the receipt class the contract already defined, so the run stays receipt-complete; a partial-primary receipt would be graded against a contract it cannot meet, while the alternative-path receipt is graded against one it can"
}
```
