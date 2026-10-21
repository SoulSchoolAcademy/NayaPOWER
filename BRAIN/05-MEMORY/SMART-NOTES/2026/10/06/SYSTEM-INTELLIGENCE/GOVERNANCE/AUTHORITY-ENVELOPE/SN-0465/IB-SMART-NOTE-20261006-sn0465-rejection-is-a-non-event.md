# Rejection Is a Non-Event: a Refused Write Must Not Record Itself

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0465-rejection-is-a-non-event
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1468 repair build (PR #1627), Team 1 cycle 2, 2026-10-06. tools/truth_state_guard.py:apply_elevation() refuses unauthorized truth-state elevation and leaves the entry byte-identical. tests/test_truth_state_poison.py::test_rejection_records_nothing pins it: snapshot before, rejected write, snapshot identical, no history key added.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a guard refuses a write, the refusal must change nothing — no state, no history entry, no receipt, no log row that says "rejected". A rejected write that records itself is still a write: it mutates the object it claims to protect, gives an attacker a mutation oracle (probe what gets recorded to learn the guard's rules), and corrupts the audit trail the guard exists to preserve. The #1468 truth-state guard enforces this structurally: apply_elevation() returns (False, reason) and the entry dict is byte-identical to before the call — verified by snapshot comparison in the test suite.

## HUMAN NOTE

Think of a bouncer who turns someone away at the door but writes their name in the guest book anyway. Now the guest book — the record of who is legitimately inside — contains someone who was never admitted. Every future audit of "who got in and how" has to explain that entry. The rule is simple: a refusal leaves no trace on the protected object. The guard can log that it refused (operational telemetry elsewhere), but the entry itself must be untouched. We built this into the #1468 repair because the whole point of the guard is that the registry's history is trustworthy — a guard that litters its own history defeats itself.

## CHILD NOTE

If someone tries to sneak into the club and the bouncer says no, the bouncer doesn't write their name on the VIP list. Saying "no" means nothing changes. Our guard works the same way: when it rejects a bad change, the note looks exactly like it did before — we check by taking a photo before and after and comparing.

## GRANDMA NOTE

When the safety switch refuses an unsafe change, it shouldn't leave a mark behind. A "no" that scribbles on the thing it protects isn't really a "no". We made our guard's refusals completely silent on the record itself — before and after look identical, and there's a test that proves it every time.

## NAYA NOTE

Future Naya: whenever you build or review a guard (write-time enforcement, admission checks, promotion gates), apply this test: snapshot the protected object, attempt a rejected operation, snapshot again — the snapshots must be identical AND no auxiliary record (history entry, receipt, refusal log) may be attached to the protected object. Telemetry about the refusal belongs in operational logs, never on the object. If you find a guard that records its refusals onto the protected object, that's a defect, not a feature — file it. This composes with the demotion rule (#1468): containment writes are permitted and recorded; rejected writes are not.

## MACHINE NOTE

```json
{
  "sn": "SN-0465",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A refused write must leave the protected object byte-identical: no state change, no history entry, no receipt, no refusal record attached to the object.",
  "anti_rule": "A guard that records its refusals onto the protected object has a defect: mutation oracle + corrupted audit trail.",
  "verification": "tests/test_truth_state_poison.py::test_rejection_records_nothing (snapshot-compare before/after rejected apply_elevation)",
  "provenance": ["PR #1627", "#1468", "tools/truth_state_guard.py:apply_elevation()"],
  "related": ["SN-0358 Nonstop Loop", "SN-0408 Deletion Discipline", "#1468 truth-state poisoning"],
  "smart_link": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1627"
}
```
