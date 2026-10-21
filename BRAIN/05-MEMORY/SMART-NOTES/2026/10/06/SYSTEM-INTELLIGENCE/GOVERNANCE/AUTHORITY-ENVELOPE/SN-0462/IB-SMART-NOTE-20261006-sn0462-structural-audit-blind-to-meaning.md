# A Structural Audit Sees Shape, Not Meaning — Elevation Needs Authority AND Evidence at Write Time

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0462-structural-audit-blind-to-meaning
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1468 truth-state poisoning review (Team 1, 2026-10-06). Defect verified on live main tip 51ab3c33: hand-edit of registry truth_state CANDIDATE→RATIFIED undetected by audit_registry. Scorecard Law receipt: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6021513825

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

audit_registry checks 10 structural defect classes — hashes, duplicates, projection paths. Zero check what a truth_state value MEANS. A hand edit flipping CANDIDATE→RATIFIED is invisible to it. promote_note() validates evidence and writes receipts, but nothing enforces its use at write time. The repair has two halves: write-time enforcement (elevation requires valid authority AND valid evidence, rejection is a non-event) plus read-side semantic backfill (find escalations already on disk). Detection after the fact is the backstop, not the fix.

## 🩷 HUMAN NOTE

Imagine a bank vault with a perfect inventory system — it knows exactly how many gold bars are inside and can spot a missing one instantly. But the inventory can't tell the difference between "the manager moved a bar with authorization" and "someone relabeled a bar as inspected when it wasn't." That's what happened here: our audit could see the shape of every record but couldn't see that someone had quietly upgraded a record's trust level without permission. The fix isn't a better inventory — it's a guard at the door who checks ID AND paperwork before letting anyone change a label, plus a one-time sweep to catch labels that were already changed.

## 🟣 CHILD NOTE

We had a list that said which notes were "checked" and which were "super checked." Someone could erase "checked" and write "super checked" with a pencil, and our checker robot wouldn't notice — it only counted whether the words were spelled right, not whether the change was allowed. Now we're putting a guard at the pencil box: you need a permission slip AND proof before you upgrade a label. And we're going back to check if anyone already used the pencil.

## 🔵 GRANDMA NOTE

The system's record-keeper could tell if a page was torn or missing, but couldn't tell if someone had quietly changed a "draft" stamp to "approved." We're fixing it two ways: a checker at the stamp desk from now on, and a review of all the stamps that are already there.

## 🟠 NAYA NOTE

Future Naya: whenever you build or review an audit, ask "does this check MEANING or just SHAPE?" A hash audit proves content wasn't altered; it says nothing about whether a state transition was authorized. Every state machine with privilege levels (CANDIDATE→RATIFIED→ACTIVE) needs: (1) write-time enforcement of the transition rules — authority AND evidence, checked before the write lands; (2) rejection as a non-event — a refused write records nothing, not even its own refusal; (3) demotion always permitted — a guard that can trap a bad state is a different bug; (4) read-side backfill — assume escalations already exist on disk and go find them. Apply this to every registry, not just Smart Notes.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-0462",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "defect": "audit_registry (tools/smart_note_v2.py:805) has 10 structural defect classes, zero semantic checks on truth_state transitions",
  "verified_on": "main tip 51ab3c33, 2026-10-06",
  "repro": "hand-edit registry CANDIDATE→RATIFIED; audit_registry reports no truth_state defect",
  "root_cause": "promote_note() validates evidence but is unenforced at write time; direct registry edits bypass it",
  "repair_shape": {
    "write_time": "apply_elevation() requires valid authority AND valid evidence; rejection records nothing",
    "read_side": "audit_registry_semantics() finds escalations already on disk",
    "ladder": "CANDIDATE < TESTING < VERIFIED < RATIFIED < ACTIVE < LEARNED, monotonic; demotion always permitted"
  },
  "issue": "#1468",
  "receipt": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6021513825",
  "rule": "every privileged state machine needs write-time transition enforcement, not just structural audit"
}
```
