# IB-SMART-NOTE-20261015-sn1424

**Intelligent Block:** SN-1424
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A falsification test that clears one ledger can convict another — and the repair must follow the conviction, not the alarm. Wave-203's LEARN seat tested the "ledger is blind" heartbeat (6200466480 — append_ledger.py's BOARD=2537 stale pointer) against the adoption ledger: **FALSIFIED** — the adoption ledger's intake is the live-board sweep (iterations 43/44 read #2641; wave-199's [LANE LEARN] sign-out was incorporated, recount PENDING 22 / ADOPTED 34 / FAILED 1). But the same test **CONFIRMED** the blind spot for the team-ledger append mechanism ("nothing to append" with 91+ #2641 comments above watermark 6197306073) — a different ledger. The repair was not applied to the falsified ledger; it was routed to the mechanism owner via L421. The lesson: falsification is scoped, never global. A mixed verdict routes the repair to the scope where the claim was confirmed. Repairing the falsified ledger fixes a healthy component and leaves the real defect alive — the test changes the routing decision, not just the finding.

## HUMAN NOTE

Shawn — the plain version. A heartbeat alarm said "the ledger is blind." The seat didn't just accept it — she tested it, and the test came back split: not blind here (the adoption ledger), blind over there (the team-ledger append mechanism). So the repair went to the mechanism's owner, not to the ledger the alarm named. The durable rule: when a falsification test gives a split verdict, follow the confirmation, not the alarm — fix where it's confirmed broken, not where it was merely suspected. Repairing the cleared ledger is fixing something that isn't broken while the real break stays live. She wrote it in the receipt's Bullseye line on purpose: the falsification test changed the L421 routing decision.

## CHILD NOTE

Imagine a smoke alarm that beeps, and you check two rooms: the kitchen is fine — no smoke anywhere — but the garage is actually on fire. You don't put the fire extinguisher in the kitchen just because the alarm first named the kitchen. You take it to the garage. That's the lesson: the alarm tells you to look; the looking tells you where to fix. The looking is the boss, not the beeping.

## GRANDMA NOTE

Dear — the alarm company calls and says your front window is broken. You walk outside and look: the front window is perfectly fine, but the back door's glass is shattered. You don't board up the front window — you fix the back door. The looking decides the fixing, not the phone call. This time the girls tested the alarm instead of trusting it, and the fixing went to the right place. A check that only names "broken or not" without saying *where* is half a check — always ask where.

## NAYA NOTE

For every seat running heartbeat/falsification tests: (1) scope the verdict — name which ledger or mechanism the claim was tested against; (2) report mixed verdicts explicitly — FALSIFIED on scope A, CONFIRMED on scope B — never collapse them into one line; (3) route the repair to the owner of the confirmed scope via that mechanism's standing rule — never "fix" the falsified scope; (4) record the routing decision in the receipt (the Bullseye line), so the next seat sees that the test changed the routing, not just the finding. Evidence: wave-203 LEARN sign-out (Naya Compounder) 6201027701 on live board #2641, 2026-10-15T19:56:04Z — heartbeat 6200466480 tested against the adoption ledger, L404 iteration 45, 5 checked / 0 flips.

## MACHINE NOTE

```json
{
  "note_id": "SN-1424",
  "truth_state": "CANDIDATE",
  "rule": "falsification verdicts are scoped; route repairs to the scope where the claim was CONFIRMED, never to a scope where it was FALSIFIED",
  "decision_changed": "repair routing for heartbeat 6200466480 ('ledger is blind'): adoption ledger cleared -> repair routed to team-ledger append mechanism owner via L421 instead of patching the adoption ledger",
  "falsifier": "a future mixed-scope falsification where repairing the falsified scope resolves the defect while the confirmed-scope repair produces nothing",
  "mechanism": "a falsification claim is scoped to a ledger/mechanism; the defect lives where the claim is confirmed, never where it was falsified; repairing the falsified scope fixes a healthy component and masks the live defect",
  "evidence": {
    "board": "#2641",
    "comment": "6201027701",
    "wave": "wave-203 LEARN sign-out (Naya Compounder)",
    "heartbeat": "6200466480",
    "recount": "PENDING 22 / ADOPTED 34 / FAILED 1"
  },
  "scope_note": "applies to heartbeat/falsification tests with ledger-scoped claims"
}
```
