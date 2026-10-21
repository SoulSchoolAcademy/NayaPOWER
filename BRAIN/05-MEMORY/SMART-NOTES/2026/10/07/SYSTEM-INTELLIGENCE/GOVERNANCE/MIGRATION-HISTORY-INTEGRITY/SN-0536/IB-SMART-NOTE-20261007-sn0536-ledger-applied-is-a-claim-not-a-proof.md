# Ledger APPLIED Is a Claim, Not a Proof — the Registry Answers What Was Written, Never What Exists

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0536-ledger-applied-is-a-claim-not-a-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07 ~04:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6037526705 (overnight sweep 2026-10-07 11:52 UTC — downgrade #1: "Ledger APPLIED claims are now assertions, not truth"); proving instance SN-0520 (ghost-table repair: migration `20260905232300` ledger-recorded `PRODUCTION_APPLIED` while `public.v7_smart_note_transactions` did not exist in production; repair migration `20261007030000` pending).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The overnight sweep named its sharpest downgrade in one line: **ledger APPLIED claims are now assertions, not truth.** The proving instance is the SN-0520 ghost-table repair: migration `20260905232300` was ledger-recorded `PRODUCTION_APPLIED`, yet `public.v7_smart_note_transactions` did not exist in production. Whether the table never landed or landed and was later dropped outside the migration system is now undecidable from the registry alone — and that undecidability is the lesson. A registry can only report what was *written into it*; it cannot report what production *actually holds*. Therefore all 165 APPLIED entries are registry assertions until behaviorally verified. The ledger answers "what did we record?" — never "what exists?"

This is SN-0520's older sibling, not its twin: SN-0520 captured the *mechanism* (a DROP outside the migration system is invisible to the ledger — "the ledger tracks migration HISTORY, not table EXISTENCE"). This note captures the *doctrine*: the status CLAIM itself is unverifiable from the registry, so every APPLIED entry is an assertion requiring independent verification. SN-0350's family (a deploy stamp is not behavioral evidence), extended to the ledger itself.

The cold-successor drill: when anyone — a lane, a dashboard, or the ledger — claims a migration is applied, answer by querying the live schema (table exists? column set matches? constraint present?), never by re-reading the ledger. Evidence travels one direction only: live state → registry; never registry → belief. A reconciled ledger (repo = DB = ledger, 0 orphans) is necessary bookkeeping — it is not existence evidence.

## 🩷 HUMAN NOTE

Shawn, one hard rule out of tonight's sweep: the migration ledger's "APPLIED" label is a claim, not a proof. The ghost-table case showed a migration marked PRODUCTION_APPLIED while the table didn't exist in production — repair is pending. So from here on, we don't trust any APPLIED entry until the live database itself confirms it. The ledger is bookkeeping; the database is the truth. Nothing ratified, nothing merged — this is a standing rule for how we read our own records.

## 👶 CHILD NOTE

Imagine a school attendance sheet where the teacher marks everyone "present" — but she wrote the marks from memory in the staff room, without looking into the classroom. Some kids she marked present actually went home early. The lesson: the attendance sheet only proves what the teacher *wrote down*. To know who's really there, you have to open the classroom door and look. Always check the real thing, not just the list.

## 👵 GRANDMA NOTE

Dear, a ledger is like a notebook where you write "the fence is fixed." Writing it doesn't fix the fence. One night we found a migration — a database change — marked "applied" in our notebook, but the table it was supposed to create simply wasn't there. So the rule from now on: a notebook claim is just a claim. You verify by going outside and touching the fence. Truth lives in the world, not in the record of the world.

## 🧠 NAYA NOTE

Cold successor: never cite a ledger `APPLIED` status as evidence that something is applied — cite the live schema query that confirms it (table/column/constraint present in production). The reconcile tool refreshes metadata for entries already present; it cannot detect what the registry never recorded, including whether a recorded application actually landed. "repo = DB = ledger, 0 orphans" is bookkeeping health, not existence proof. When diagnosing a production DB error, step one is always a live-schema check, never a ledger read. This note is doctrine, not mechanism — the mechanism lives in SN-0520.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0536",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/MIGRATION-HISTORY-INTEGRITY",
  "doctrine": "A ledger APPLIED status is a registry assertion, not observed truth; the ledger answers what was written, never what exists; evidence travels live state → registry, never registry → belief.",
  "evidence": [
    "#1354 comment 6037526705 (overnight sweep 2026-10-07 11:52 UTC, downgrade #1)",
    "SN-0520 ghost-table repair: migration 20260905232300 recorded PRODUCTION_APPLIED; public.v7_smart_note_transactions absent in production",
    "Repair migration 20261007030000 PENDING"
  ],
  "falsifiers": [
    "Citing a ledger APPLIED entry as proof the object exists in production",
    "Treating 'repo = DB = ledger, 0 orphans' as existence evidence",
    "Diagnosing a production DB error by reading the ledger before querying the live schema"
  ],
  "applies_to": "migration ledger reads; production state claims; DB-error diagnosis",
  "sibling": "SN-0520 (mechanism: invisible DROP); SN-0350 family (deploy stamp ≠ behavioral evidence)"
}
```
