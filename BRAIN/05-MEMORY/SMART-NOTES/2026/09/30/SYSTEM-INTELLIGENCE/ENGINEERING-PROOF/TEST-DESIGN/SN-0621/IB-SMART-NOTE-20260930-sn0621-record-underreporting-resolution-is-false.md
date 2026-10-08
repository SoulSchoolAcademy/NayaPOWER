# A Record That Under-Reports Resolution Is False — Claim Statuses Must Be Behaviorally Falsifiable in Both Directions

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0621-record-underreporting-resolution-is-false-status-probes-both-directions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6049507978 (CV-10, "test(gate): claim-record statuses are now falsifiable against the code"), 2026-10-08T00:18:44Z — SoulSchoolAcademy. Repairs: #1695 (CV-06/CV-07), #1791/#1792 (CV-04/05/08/09).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The load-bearing claims record (`tools/load-bearing-claims-record.json`) enforced every entry's *shape* — a named law, a location, a status — but nothing ever compared any status to the code. So #1695 repaired CV-06 and CV-07 while both entries kept reading **OPEN**, and #1791/#1792 repaired CV-04, CV-05, CV-08, CV-09 and marked all nine **RESOLVED** in a single commit — the second batch was correct (re-read on main, they compute properly), the first was a real repair wearing a stale label, and at the moment either landed nothing in the suite asked whether the statuses still described the code. The lesson: **a record that under-reports resolution is not conservative — it is false, and worse than no record, because it looks authoritative.** The cost is teaching every future reader to discount the file. The repair is CV-10: every claim status is now a behavioral probe that can fail — the gate asserts **both directions**: OPEN must still misbehave, RESOLVED must not. Getting the direction right is the easy thing to get wrong — the first probe implementation had it backwards, and that too was a lesson: bidirectional falsifiability is not a lint on labels; it is a runtime assertion that the record's truth claim executes against the code.

## 🩷 HUMAN NOTE

Shawn, the honesty file was lying — politely. Our claims record tracked every load-bearing claim with a status, but never checked whether the status matched reality: two repaired violations still said OPEN, and nine correct RESOLVED labels were asserted by hand with nothing verifying them. A wrong status on an authoritative record isn't caution, it's misinformation that trains everyone to stop trusting the file. Now every status is a live probe: "open" must demonstrably still fail, "resolved" must demonstrably not. The record can never quietly go stale again.

## 👶 CHILD NOTE

Imagine a class chart where each student's name has a gold star if they finished their project. But nobody ever checks — so some kids who finished never got stars, and some stars got handed out without checking. After a while nobody trusts the chart. The fix: instead of writing a star by hand, the teacher runs a quick test on each student's actual project every day. The chart now proves what's on it, not just says it.

## 👵 GRANDMA NOTE

Dear, this is about honesty in bookkeeping. We kept a ledger of what was broken and what was fixed — but the ledger was never asked to prove itself. A broken item was quietly repaired yet still listed as broken; a fixed list was declared with no test behind it. Both are the same sin: words that don't match the thing they describe. The rule now is simple and severe: every line in the ledger must be testable in both directions — broken must be demonstrably broken, fixed must be demonstrably fixed. An unverified record is worse than no record at all, because people trust it.

## 🧠 NAYA NOTE

Cold successor: any claim/law/ledger record you maintain MUST have its statuses wired to behavioral probes, never to hand-set strings. For each violation: declare whether the defect is **still present**, then assert in the gate — an OPEN entry must reproduce the misbehavior on the current code (fails if it doesn't), a RESOLVED entry must pass it (fails if it does). Watch the direction bug: it is easy to write the probe that asserts the label rather than the defect — the first CV-10 implementation did exactly that. Re-read every RESOLVED entry against the code at least once by hand before trusting the gate. If your record has a status field that nothing reads, delete the field or wire it — shape-checked records rot silently.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0621",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/TEST-DESIGN",
  "doctrine": "A claim record that enforces shape but never truth is false and worse than no record; every status must be a behavioral probe falsifiable in both directions (OPEN must still misbehave, RESOLVED must not).",
  "family": "INSTRUMENT-PARITY (SN-0291, SN-0329, SN-0341, SN-0429, SN-0517)",
  "evidence": ["#1354 comment 6049507978 (CV-10)", "PR #1695 (CV-06/CV-07 repairs)", "PRs #1791/#1792 (CV-04/05/08/09 repairs)"],
  "falsifiers": [
    "An OPEN claim-record entry whose defect no longer reproduces on current code",
    "A RESOLVED claim-record entry whose defect still reproduces on current code",
    "A claim record with status fields that no gate reads"
  ],
  "applies_to": "all claim/law/ledger status records"
}
```
