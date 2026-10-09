# The Sealed-Kit Tripwire — E1 Fires, Builder and Retester Dispatch Together

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0805-sealed-snapshot-tripwire-e1-fired
**Smart Note:** SN-0805
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Naya 4, proactive distillation loop (smart-note-distillation tick, 2026-10-09 ~11:15 PDT).
**Provenance:** Board #1354 comments 6086538851 (COLD PACKET TRIGGER — E1 FIRED, 2026-10-09: live tip `dad160767` ≠ pin `45f0ed26c`, 2 of 7 vendored paths drifted) and 6086556173 (tripwire steward update: v3.3 builder + pre-staffed v3.3 retester dispatched; the standby lifecycle decided at Q=9.35 in 6086446789 is working exactly as designed). First live firing of the standing trigger.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A sealed snapshot carries its own re-prove tripwire, and today it fired for the first time — exactly as designed. The E1 check diffed the live repo tip against the kit's pin across the 7 vendored paths; two real files had drifted (the activation receipt template and the gate code itself), so the kit no longer described reality. Three rules the firing proved: (1) the detector does NOT rebuild — detection is its lane, so it fires and hands off; (2) the builder and an independent retester are dispatched together, never the builder alone; (3) the old kit stays valid for the world it was stamped in — it is not "broken," it is outdated, and a cold Naya following it would be following yesterday's rules. The standby lifecycle (STANDBY + RE-PROVE TRIGGER, decided at Q=9.35) works.

## 🩷 HUMAN NOTE

Shawn — the cold packet's tripwire did its job today: it noticed the repo had moved underneath the sealed kit and called for a fresh rebuild instead of letting a cold Naya follow outdated rules. The detector didn't try to rebuild it itself — it handed that to the right seat with a precise target, plus an independent tester checking the work. The old kit is still fine for the world it was stamped in; the new one will describe the new world. This is the safety system working, not a failure.

## 🧒 CHILD NOTE

Imagine you draw a perfect map of your room, and then someone moves the furniture. A good map comes with a rule: "check the room against the map, and if things moved, draw a new map." Today the rule fired for the first time — the furniture (two important files) had moved, so a new map is being drawn and a second person is checking the drawing. The old map still describes the old room perfectly. Nothing is broken; this is the rule working.

## 👵 GRANDMA NOTE

Dear — think of the cold packet as a sealed recipe card, stamped on the day every ingredient was proven fresh. Today the kitchen changed — two ingredients are different — so the card can't be trusted for today's cooking. The checker who noticed didn't rewrite the card himself; he handed it to the cook with exact instructions, and a second person tastes the result. The old card is still perfect for the kitchen it was stamped in. Everything working as it should.

## 🤖 NAYA NOTE

Future Naya: sealed snapshots are perishable by design, and their re-prove trigger is the mechanism that keeps them honest. E1: live tip ≠ pin → diff pin..tip against the vendored scope (7 vendored + 11 read-list paths) → any overlap with real semantic drift → FIRE. When E1 fires: (a) the executor's lane is detection only — it must not rebuild (scope violation; its own decision receipt considered diffing-against-last-checked-tip and self-rebuild, and the evidence won both down); (b) dispatch the builder and a pre-briefed independent retester together per the margin policy — builder brief must require understanding the drift BEFORE vendoring, and retester brief is falsification-first with a drift-capture check; (c) the old kit remains the activated-verified kit for its pin — never label it broken. E2 (new dated files in NAYA-ACTIVATION/) and E3 are evaluated alongside but did not fire here. The first live firing is the validation event for the standby lifecycle decision — record it as such.

## ⚙️ MACHINE NOTE

```json
{
  "note": "SN-0805",
  "type": "MECHANISM_VALIDATED",
  "name": "Sealed-Snapshot Tripwire (E1) — First Live Firing",
  "status": "CANDIDATE",
  "mechanism": "Sealed kit pins the exact tip it was byte-verified and cold-retested against. Standing triggers E1/E2/E3 re-check the pin on every run.",
  "firing_signature": {
    "pin": "45f0ed26c79ae1261bd3ba6181d37970dab601f5",
    "live_tip": "dad160767b57cb5dab140583c86f418f41685bca",
    "delta": "4 commits, 18 files; 2 of 7 vendored paths with real semantic drift: NAYA-ACTIVATION/ACTIVATION-RECEIPT-V2.json (trusted-issuance round-3 semantics) and tools/activation_gate.py (+758/-92 ROUND 2 rewrite closing four reproduced bypasses)"
  },
  "response_protocol": [
    "Executor fires + hands off; does NOT rebuild (detection is its lane).",
    "Builder + independent retester dispatched together; builder brief requires understanding drift before vendoring; retester brief is falsification-first with drift-capture check.",
    "Old kit stays the activated-verified kit for its pin; never relabel a stale kit as broken."
  ],
  "validated_decision": "Cold-packet lifecycle STANDBY + RE-PROVE TRIGGER (Q=9.35, board comment 6086446789).",
  "evidence": { "board_comments": ["6086538851", "6086556173", "6086446789"] }
}
```
