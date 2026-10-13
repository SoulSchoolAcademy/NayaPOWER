# The Hash Chain Misses Garbage Lines That Never Participated In It — Measure the Raw Input

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0772-measure-the-raw-input
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6078470402 (Naya 5 Memory Builder, 2026-10-09T09:46:11Z, merge intent + scorecard for `naya5/memory-metabolism` @ `a3ed9099`): "closed an audit-trail observability gap (corrupt receipt lines now counted in `health()` — the hash chain alone misses garbage lines that never participated in it)"

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The memory store's receipt log is hash-chained — every receipt verifies the ones before it. That verification has an entry boundary: a line so corrupt it never became a receipt never entered the chain, so chain verification passes cleanly while the raw store quietly rots. The audit looks complete because the audit only inspects what participated. Naya 5 closed the gap by counting corrupt receipt lines in `health()` — instrumenting the raw input, not just the verified output.

The law for a cold successor: **every integrity mechanism has an entry boundary, and corruption at or before entry is invisible to it.** A chain verifies its members; it cannot verify the ones that never joined. So instrument both: verify the chain AND measure the raw input (corrupt lines, parse failures, quarantine counts) in a health signal that sits beside the verification verdict. If your health check only asks "is the chain intact," a poisoned store with a pristine chain reads healthy.

## 🩷 HUMAN NOTE

Shawn — a sharp observability catch from the memory lane. The receipt log's hash chain verifies every entry — but only entries that made it in. A corrupted line that never became a receipt is invisible to the chain check, so the audit could say "all clean" while garbage piled up in the raw store. She closed it by counting corrupt lines in the health signal — measuring the raw input, not just the verified output. The standing rule: any integrity check has a blind spot at its own entry point, so we always instrument the raw input too.

## 🟣 CHILD NOTE

Imagine a teacher who checks that every student in class did their homework — but she only checks the students who are sitting in the room. The kid who never made it to class isn't counted at all, so the class looks perfect even though someone is missing. The smart fix: count who's missing too, not just who did the work. That's what measuring the raw input means — check the ones who never joined, not just the ones inside.

## 👵 GRANDMA NOTE

Grandma, the team keeps a chain of records where each one vouches for the last — a beautiful system, except it has one blind spot: a record so damaged it never got into the chain can't be vouched for by anyone. The audit would say "everything's fine" while damaged records piled up outside the chain. So they added a second check that counts the damaged ones directly. Always check what's outside the chain, not just what's inside it.

## 🟣 NAYA NOTE

When building or reviewing any integrity/verification mechanism: (1) identify its entry boundary — what must happen for data to become verifiable; (2) assume corruption at or before entry and ask what the mechanism sees — answer: nothing; (3) instrument the raw input independently (here: count corrupt receipt lines in `health()`, alongside chain verification); (4) never let a clean verification verdict stand alone when the input path can fail — the verdict must be paired with raw-input health. Provenance: #1354 comment 6078470402 (2026-10-09T09:46:11Z), `naya5/memory-metabolism` merge intent. Cousins: SN-0655 (corruption-proof metric extraction), SN-0420 (never absorb the anomaly).

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0772",
  "slug": "measure-the-raw-input",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/MEASUREMENT-BOUNDARY",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6078470402 (Naya 5, 2026-10-09T09:46:11Z): memory-metabolism merge intent — closed audit-trail observability gap: corrupt receipt lines now counted in health(), because the hash chain alone misses garbage lines that never participated in it"}
  ],
  "lesson": "An integrity chain verifies only what participated in it; corruption at or before entry is invisible to verification. Instrument the raw input (corrupt lines, parse failures) in health() alongside the verification verdict — never let a clean chain verdict stand alone.",
  "related": ["SN-0655", "SN-0420"]
}
```
