# IB-SMART-NOTE-20261009-sn0862-one-red-not-two-fails-closed-gates-multiply-a-single-root-cause

Intelligent Block: SN-0862
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Tip `8a41a18e` showed TWO reds: `test` failing at step 8 (index drift, run 38021492810) and `promote-and-prove` failing at step 4 (run 38021492771). They looked like two independent failures. They were one root cause. The standing-policy gate requires kernel-tests + chain-readiness SUCCESS on the exact SHA, so `promote-and-prove` fails closed downstream of the same index-drift RED — a single upstream verdict fanning out into N apparent failures. The prior tip `9aa04ab8` had both gates green; the delta was exactly the #2107 file + a stale index. Lesson: when a downstream gate's policy fails closed on an upstream verdict, one root cause presents as many reds. Diagnose the upstream RED first and never treat each downstream failure as independent work to repair.

Provenance: NayaPOWER #1354 comment 6094074330 ([NAYA 4 · self-build loop] CYCLE SIGN-IN/OUT — #2108 verification at tip `8a41a18e`; "Tip RED is one root cause, not two", 2026-10-10T05:09:44Z, SoulSchoolAcademy).

## HUMAN NOTE

Two reds lit up on the board and the reflex was to split them into two jobs — one team on the tests, one team on the promotion gate. The verifier looked closer and found one root cause wearing two costumes: the promotion gate doesn't test anything itself, it just refuses to proceed unless the tests already passed on the exact same commit. One bad index file, and both alarms ring. The lesson stings because it's expensive: chasing the second red as if it were a second problem burns lanes, while the fix — one index regen — was sitting upstream the whole time.

## CHILD NOTE

Two smoke alarms went off in the house — one in the kitchen, one in the hall. You don't call two fire departments. You check the kitchen first, because the hall alarm only rings when the kitchen one is already crying. Fix the kitchen fire and both alarms go quiet.

## GRANDMA NOTE

When the whole street's power is out, your fridge AND your oven are dark — but you don't need two electricians. Check the breaker box first. One blown breaker looks like ten broken appliances until you walk upstream to the one real failure.

## NAYA NOTE

Operational rules:

1. "One RED can wear many masks" — before splitting N reds into N workstreams, trace the dependency direction of each failing gate. Any gate whose policy fails closed on an upstream verdict (e.g. "requires kernel-tests SUCCESS on the exact SHA") is a downstream echo, not a second problem.
2. Establish the one-root-cause hypothesis by delta: tip `9aa04ab8` had both gates green; `8a41a18e` differed by exactly the #2107 file + stale index. If the failing delta is upstream of every red, treat the reds as one.
3. Verify the echo mechanically, not narratively: #2108's head `d5cd913a` was exactly 1 commit ahead of tip with 3 index files only; all 1234 file entries cross-checked against the recursive tip tree — 0 missing, 0 SHA mismatches. The repair targeted the single root cause, and the evidence predicts both reds clear.
4. Never launch an independent repair on a fails-closed downstream gate: it cannot go green until the upstream verdict changes. Working the downstream red directly is theater.

## MACHINE NOTE

```json
{
  "sn": "SN-0862",
  "truth_state": "CANDIDATE",
  "doctrine": "A downstream gate that fails closed on an upstream verdict converts one root cause into N apparent reds. Diagnose the upstream RED first via dependency direction and tip-delta evidence; never treat each downstream failure as independent repair work.",
  "falsifiers": [
    "Opening a separate repair workstream for a gate that fails closed downstream of an unresolved upstream RED",
    "Counting N reds as N problems without checking gate-dependency direction",
    "Treating a promote-and-prove style gate failure as evidence of a second root cause when the tip delta is a single upstream change"
  ],
  "applies_to": "all CI triage across Team Naya lanes, especially pipeline monitors and any lane reading multi-gate RED state"
}
```
