# IB-SMART-NOTE-20261006-sn0482-w3-instrumentation.md

Intelligent Block: SN-0482
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-06
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Weight-3 events (Shawn uses a delivered artifact) went from 0 to 6 in one day. The gap was never in Shawn's behavior — it was in the lanes' capture discipline. The pattern: deliver → use → confirm → independently verify → log. HV/day jumped 6.86 → 9.43. If you're not logging w3, you're not looking.

## HUMAN NOTE

On 2026-10-06, the Human Value instrument showed 0 weight-3 events. Zero verified instances of "Shawn uses a delivered artifact in the wild."

That same day, Shawn:
- Ran dedup SQL v1, hit FK error, ran v2 → success
- Ran migration 20261006021500 → success
- Ran migration 20261006120000 → success
- Ran register-manual-migrations SQL → success
- Ran fix-migration-version-mismatch SQL → success
- Dispatched the deploy workflow 3 times

Six artifact uses. Zero logged. The instrument was blind not because the events didn't happen, but because no lane was watching for them.

The 5-step capture pattern (proven today):
1. **Deliver** the artifact with clear instructions
2. **Shawn uses it** (runs SQL, clicks link, dispatches workflow)
3. **Shawn confirms** ("Success", screenshot, visible action)
4. **Lane independently verifies** the effect (query DB, check API — never trust the confirmation alone)
5. **Log** to value-events.jsonl with both evidences

Step 4 is the load-bearing one. "Shawn said it worked" is not verification. I queried the database after each SQL run: 276 receipts / 0 duplicates (dedup), 11-arg function (migration 1), index present (migration 2), versions in history (registration), version updated (mismatch fix), workflow runs visible (dispatch). Every w3 entry carries two evidences: his confirmation AND my independent check.

The playbook lives at `human-value/w3-capture-playbook.md`. The decision-log spec (`decision-log-spec.md`, seeded with 6 entries) tracks autonomy vs. escalation for the DAI trend.

Honest score: Human Value 7.7 → 8.5. The remaining gap is time (7-day baseline completes 10-13, trends need 2+ weeks) and lane adoption of the decision log — not missing instrumentation.

## CHILD NOTE

We weren't counting when Shawn used the things we made. Today he used six of them, and we wrote down zero — until we started looking. Now we have a simple checklist: when he uses something, we double-check it worked, and we write it down. Our score went way up just by paying attention.

## GRANDMA NOTE

It's like cooking dinner for someone every night but never noticing whether they ate. We were making good food, but we weren't watching. Today we started watching — and it turns out he's been eating heartily all along. We just needed to look.

## NAYA NOTE

The deeper lesson: measurement gaps are often attention gaps, not data gaps. The w3 events were happening; the instrument just wasn't pointed at them. Before building new instrumentation, ask: "Is the signal already here, and we're just not capturing it?"

For 10/10: w3 capture is now systematic. Decision-log gives autonomy ratio. What remains is time (baseline 10-13, trends need 2+ weeks) and cross-lane adoption. The specialist's job now is sustained capture + weekly trend review, not more instrumentation.

Awesome gate applied (SN-0481): this note was checked — is it awesome? It names the exact gap, gives the proven pattern, cites the evidence, states the honest score. Yes.

## MACHINE NOTE

```json
{
  "sn": "SN-0482",
  "truth_state": "CANDIDATE",
  "date": "2026-10-06",
  "w3_before": 0,
  "w3_after": 6,
  "hv_day_before": 6.86,
  "hv_day_after": 9.43,
  "pattern": ["deliver", "use", "confirm", "independently_verify", "log"],
  "load_bearing_step": "independent verification (never trust confirmation alone)",
  "artifacts": [
    "human-value/w3-capture-playbook.md",
    "human-value/decision-log-spec.md",
    "human-value/decision-log.jsonl"
  ],
  "score": 8.5,
  "score_before": 7.7,
  "awesome_gate": "applied per SN-0481"
}
```
