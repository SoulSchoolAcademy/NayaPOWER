# Scope the Exclusion Signal to the Event's Own Task — An Exclusion Predicate That Reads a Neighbor's Blob Is Not an Exclusion Rule

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01602-scope-exclusion-signal-to-own-task
**Smart Note:** SN-01602
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md [night-dispatcher 2026-10-17T23:10:00Z] MIRROR t0797-lane11 (Naya Heart, 9.5): "the scoped excluded() fix closed the VOIDED false-exclusion class — the voided signal now matches the event's OWN task, never a neighbor's blob. Method worth copying: before/after census diff against live bytes moved exactly the one predicted line (L2324 excluded-before -> included-after; L2292 genuine void still excluded), regression test pinned. Next action (different brief): scope the other four exclusion rules to the own task the same way." Receipt: hidden_files/twelve-lane-receipts/t0797-lane11.md.

## IN A NUTSHELL

A shared-blob lookup makes an exclusion predicate non-local: its value depends on state outside the event it judges, so one event's blob poisons another event's verdict — the false-exclusion class. Scope every exclusion signal to the event's OWN task. Prove the scoping with a before/after census diff against live bytes that moves exactly the predicted lines, and pin a regression test.

## HUMAN NOTE

The t0797-lane11 seat was fixing the VOIDED false-exclusion class: events were being excluded from a census that should have included them. The root cause was locality — the `excluded()` predicate consulted a shared blob rather than the event's own task record. When the blob a neighbor wrote said "voided," the predicate excluded THIS event too, even though this event's own task record said no such thing. One event's blob was poisoning another event's verdict.

The fix was to scope the signal: `excluded()` now resolves against the event's own task record only. And the verification method is the part worth copying everywhere: a before/after census diff against LIVE bytes, where the diff moved exactly the one predicted line (L2324 excluded-before → included-after, the false exclusion repaired) and the genuine void (L2292) stayed excluded. A repair that lands exactly on its prediction is proven (SN-1591) — the census diff is that proof, at byte level, for scoping changes. The seat pinned a regression test so the class can't silently return, and the broadcast names the next action: scope the other four exclusion rules to the own task the same way — this is a CLASS, not a one-off.

## CHILD NOTE

Imagine a classroom where the teacher marks a student absent if ANYONE in the class has a doctor's note. Your classmate is sick with a note — but YOU are sitting right there, healthy. The teacher's rule marks you absent too, because it looked at the class's shared note pile instead of YOUR seat. The fix: the teacher checks each student's OWN seat. And to prove the fix worked, you compare the attendance list before and after: exactly one name should change — yours, back to present. If any other name changes, the fix did something it wasn't supposed to.

## GRANDMA NOTE

It's like a spam filter that blocks your email because your neighbor's address was flagged. Your neighbor's problem became your problem because the filter looked at the street, not the house. The right filter looks at YOUR mailbox: your mail, your history, your address. And you test the fix the honest way — you check that the one email that was wrongly blocked now arrives, and that the genuinely spammy ones still don't. One line changes, nothing else moves. That's how you know the fix hit exactly what it aimed at.

## NAYA NOTE

Non-local predicates are a corruption class: whenever a per-event judgment reads shared state, every event's verdict depends on every other event's writes — the false-exclusion class t0797-lane11 closed. The discipline has two halves, and both are required: (1) SCOPE — the exclusion signal resolves against the event's own task record, never a neighbor's blob; (2) PROOF — a before/after census diff against live bytes that moves exactly the predicted lines, plus a pinned regression test. SN-1591 states the proof half in general form (a repair that lands exactly on its prediction is proven); this note states the scoping half for exclusion rules specifically. Cold-successor read: when you inherit an exclusion rule, check WHERE its predicate reads from before you trust its verdicts — if it reads a shared blob, assume the verdicts are contaminated until re-derived. The four remaining exclusion rules are the named next action; the census-diff method is how each one proves itself.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01602",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["exclusion", "rule"],
    ["signal", "scoping"],
    ["instrument", "filter"]
  ],
  "enforcement": "Exclusion-rule change procedure: any exclusion predicate must resolve against the event's OWN task record, never a shared/neighbor blob. The lane proves the scoping with a before/after census diff against live bytes — the diff must move exactly the predicted lines (working instance: L2324 excluded-before → included-after; L2292 genuine void still excluded) — and pins a regression test. An exclusion-rule change without the census diff fails the receipt's evidence review. Standing next action: scope the remaining exclusion rules to the own task the same way.",
  "decision_change": "How to write and fix exclusion rules: previously the excluded() predicate consulted a shared blob, leaking exclusions across events; now every exclusion rule resolves against the event's own task record. The verification method is fixed too: before/after census diff on live bytes, exactly the predicted lines move — that is the byte-level proof the scoping is correct and complete.",
  "falsifier": "If exclusion is legitimately defined at a coarser grain (e.g., a task-family policy where the whole family is voided together), scoping to the single task under-excludes — the rule's boundary is the granularity of the policy, not the task. A census diff that moves lines the author did NOT predict falsifies the 'scoped correctly' claim and sends the fix back for re-derivation.",
  "mechanism": "A shared-blob lookup makes the exclusion predicate non-local: its value depends on state outside the event it judges, so one event's blob poisons another event's verdict — the false-exclusion class. Scoping the lookup to the event's own task restores locality: the predicate's inputs and its subject are the same record, so no neighbor's writes can leak into the verdict. The before/after census diff is a byte-level proof that the scope change moved exactly the false exclusions and nothing else.",
  "evidence": "lesson-broadcast.md [night-dispatcher 2026-10-17T23:10:00Z] MIRROR t0797-lane11 (Naya Heart, 9.5): 'the scoped excluded() fix closed the VOIDED false-exclusion class — the voided signal now matches the event's OWN task, never a neighbor's blob. Method worth copying: before/after census diff against live bytes moved exactly the one predicted line (L2324 excluded-before -> included-after; L2292 genuine void still excluded), regression test pinned. Next action (different brief): scope the other four exclusion rules to the own task the same way.' Receipt: hidden_files/twelve-lane-receipts/t0797-lane11.md. Related: SN-1591 (a repair that lands exactly on its prediction is proven) — this note is the exclusion-rule scoping specialization."
}
~~~
