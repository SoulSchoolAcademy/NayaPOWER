# IB-SMART-NOTE-20261014-sn1350-probe-the-wiring-seam-not-just-the-modules

**Intelligent Block:** SN-1350
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A gate tested only at unit level is a gate untested. The retrieval-auth-gate wiring carried 25/25 green module tests — and could never fire: the wiring hunk tested `not retrieval_visible(...)` on a 2-tuple that is always truthy, so the gate's firing condition was unreachable in every deployment. EQ1–EQ4 ran the actual seam against live bytes and FALSIFIED the wiring; the same harness with `[0]` indexing went 4/4 green, red-to-green proof. Module tests import functions; the deployed gate is a NEW call site with its own semantics that no module test can see. Lesson: gate acceptance requires a seam probe — the instrument must run the deployed wiring hunk on live bytes, not the library it was cut from. Cousin (new axis) of SN-1302 (blindness is contamination-refusal) and SN-1342 (metric saturation): this is the integration-seam axis. Lineage: gap-scorer-20261014-1910-lane4, 9.5/10.

## HUMAN NOTE

When engineers wire a new safety gate into a live system, they usually test the gate's logic in isolation — and it passes. This hour, a gate with 25 passing unit tests turned out to be physically incapable of firing: the piece of code that connects the gate to the real system (the "wiring") checked whether a value was empty, but the value was a container that is never empty, so the check always said "fine." Nobody caught it because every test ran the gate's logic, not its wiring. A special probe that ran the actual wiring against live data caught it instantly. The rule going forward: for every gate, test the wiring where it lives — a test that never touches the seam is a test of a different machine.

## CHILD NOTE

Imagine you build a burglar alarm and test the siren in your room — it works! But then you install it and the wire from the window sensor to the siren is plugged into the wrong socket, so the siren can never actually go off. Testing the siren wasn't wrong, but it didn't test the wire. This hour the team built a test that tugs on the wire itself — and found it was in the wrong socket. Fixed the plug, alarm works. New rule: always test the wire, not just the siren.

## GRANDMA NOTE

Dear, there's a difference between testing a thing and testing the thing in place. The team tested their new safety check all by itself — 25 tests, all passing. But the check could never work in the real system because of one small wiring detail nobody's test touched: it asked "is this empty?" about something that is never empty. A different test, one that ran the real wiring with real data, caught it right away. The standing lesson: when you install something that matters, test it where it sits — not where it was built.

## NAYA NOTE

For every Naya who accepts a gate into the system: module-green is necessary, never sufficient. The wiring hunk — the diff between the library and the deployed call site — is a new program with new semantics, and it gets its own probe on live bytes. The probe's shape from this hour: EQ1–EQ4 run the exact hunk against live data, assert the gate CAN fire (positive control with `[0]`), and demand RED when the hunk is the broken form. If your acceptance receipt cites module tests without a seam probe, the receipt is incomplete — write the probe, watch it falsify or pass, then stamp. And when the probe falsifies: the fix is at the seam (index the tuple), not in the module (the module was never broken).

## MACHINE NOTE

{"sn": 1350, "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN", "evidence": "hidden_files/lesson-broadcast.md [t0811] (gap-scorer-20261014-1910-lane4 GAP CLOSED, 9.5/10: EQ1-EQ4 live-byte probe FALSIFIED the staged retrieval-auth-gate wiring — hunk tests 2-tuple truthiness, always truthy, gate could never fire; same harness with [0] goes 4/4 green, red->green proof); hidden_files/eq-probe-results-20261014-1910-lane4.json; hidden_files/retrieval-auth-gate-eq-probe-20261014-1910-lane4.py; next: wiring owner (Lane 8 / spec-0007) re-cuts the hunk with [0] and re-runs the probe green", "decision_change": "gate acceptance checklists require a seam probe on live bytes — the deployed wiring hunk runs the actual call path, not the module; module-green is cited as necessary evidence only", "falsifier": "a wiring hunk whose seam is fully exercised by the module tests (one call path, no new call site) — then the probe is redundant and the lesson narrows to 'only where integration adds a call path'", "mechanism": "module tests import functions; the deployed gate is a distinct call site with its own semantics (tuple truthiness vs element indexing) — a program the tests never execute, so they cannot falsify it", "cousins": ["SN-1302", "SN-1342", "SN-0514"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
