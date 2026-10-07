# Stale-Caveat Decay — Caveats Must Carry Their Expiry Trigger

**Intelligent Block:** IB-SMART-NOTE-20260930-sn041-stale-caveat-decay
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 00:45 PDT distillation tick (2026-10-01) from the read-only skeleton merge-decision audit, `hidden_files/redteam/SKELETON-MERGE-AUDIT-2026-10-01.md`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three of the six skeleton merge-decision docs carry the same stale-caveat defect, flagged by the audit as the M-LAW-06 family. E-2 (MODERATE, OPEN): the EVOLVE merge's C3 conditions gate references "on CANDIDATE calculus" — written when the decision calculus was CANDIDATE, **stale after Shawn merged #1186** (ratify+bind V2.1→SmartLedger, 2026-09-30). C-2 (MODERATE, OPEN): the CONNECT merge's §3 caveat "V2.1 is CANDIDATE (#1185), not ratified law — [director-set] until V2.1 is ratified" — stale after the same #1186/#1190/#1192 merges ratified and bound V2.1. V-1 (MODERATE, OPEN): the VERIFY merge's §2 caveat "window lengths follow the CANDIDATE calculus schedule … director-set until V2.1 is ratified" — same staleness. Each caveat was honest and correct when written; each became false at a merge event the caveat never named. The defect is structural, not authorial: a caveat about the world's current state has a shelf life, and a caveat that doesn't say what expires it will outlive its truth. The repair rule: **every time-bound caveat must carry its expiry trigger** — the exact event that invalidates it ("until PR #1186 merges"), not just the condition ("until V2.1 is ratified"); and after each merge event, the merge-finalizing pass re-audits every caveat in the merged documents against the new world state.

## 🩷 HUMAN NOTE

These caveats were all written correctly — "this is candidate until the director ratifies it." The problem is that the director then ratified it, and nobody went back to delete the sentence. It's the "out of order" sign taped to a vending machine that got fixed three weeks ago: the sign isn't a lie about the past, it's a lie about the present, and it got that way because nobody's job was to take it down. The fix has two parts, and they're both boring: write the sign so it expires itself ("out of order until the 30th"), and after every fix, walk the machine and take down the dead signs. In document terms: name the event, not the condition — and re-audit caveats at every merge.

## 🟣 CHILD NOTE

If you put a note on the fridge that says "no cookies until mom says okay," and mom says okay, the note is now wrong — unless the note said "no cookies until mom says okay at dinner." Write the note so it knows when it's done, and check the fridge after dinner.

## 🔵 GRANDMA NOTE

It's like leaving "wet paint" signs up for a month after the paint dried. The sign was true and helpful once. The missing step was never the writing — it was the taking down. Every temporary sign needs to say what ends it, and someone has to do a walk-through after the change.

## 🟠 NAYA NOTE

Install this in the merge-finalizing pass and every document-authoring loop: (1) write every time-bound caveat with an expiry trigger that names the event, not the condition — "until PR #1186 (ratify+bind V2.1→SmartLedger) merges," not "until V2.1 is ratified"; (2) keep a caveat register per document (statement, trigger event, date written) so re-audit is grep-able; (3) after every merge event, run the caveat re-audit: list all caveats in the merged documents, strike or update every one whose trigger event has fired; (4) treat an unnamed-expiry caveat as a finding in itself — it's a time bomb, not a caution. The audit's honesty is the model to preserve: these caveats were explicitly labeled CANDIDATE-interpretation, which is why they were auditable at all. Explicit + expiring beats explicit + eternal.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_caveat_decay",
  "evidence": {
    "audit": "hidden_files/redteam/SKELETON-MERGE-AUDIT-2026-10-01.md",
    "E-2": "EVOLVE C3 conditions gate references 'on CANDIDATE calculus' — stale after #1186 ratified+bound V2.1 (merged by Shawn, 2026-09-30 ~16:36-16:43 PDT)",
    "C-2": "CONNECT §3 caveat 'V2.1 is CANDIDATE (#1185), not ratified law' — stale after #1186/#1190/#1192",
    "V-1": "VERIFY §2 caveat 'window lengths follow the CANDIDATE calculus schedule ... director-set until V2.1 is ratified' — stale after ratification+bind",
    "family": "M-LAW-06 family (per audit X-1): stale V2.1-caveats recur across merged ACT/LAW reviews"
  },
  "rule": "every_time_bound_caveat_carries_its_expiry_trigger",
  "procedure": [
    "write caveats with an expiry trigger naming the event ('until PR #1186 merges'), not the condition ('until ratified')",
    "keep a caveat register per document (statement, trigger event, date written) for grep-able re-audit",
    "after every merge event, re-audit all caveats in merged documents against the new world state; strike or update fired triggers",
    "an unnamed-expiry caveat is itself a finding — a time bomb, not a caution"
  ],
  "related": ["SN-016 (Prime Judgment Rule — director's word as event authority)", "SN-023 (seed authority over prose)", "SN-027 (amendment premise verification)"]
}
~~~
