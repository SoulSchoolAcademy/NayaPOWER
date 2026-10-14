# IB-SMART-NOTE-20261014-sn1320

**Intelligent Block:** SN-1320
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A detector's first live run is a test of the detector, not the feed. The class-17 violation detector (t0766-lane1, 2026-10-14) shipped its first draft and the live bytes immediately found 3 instrument bugs: pattern-1 was too narrow for the real phrasings, pattern-2 was structurally wrong, and the quote showed line-start instead of match context. None of that was feed dirt — it was the instrument being wrong about the world it claimed to judge. The fix went in together with an 8/8 + 4/4 regression battery, shipped WITH v1, not after. The durable discipline: every instrument brief schedules a self-test pass against live bytes before the instrument is trusted on the feed — the regression battery is part of v1, never a follow-up. The unproven element is the instrument; the feed is the oracle. The first run tests the instrument against the oracle, not the feed against the instrument.

## HUMAN NOTE

Imagine you buy a new metal detector and wave it over the beach — and it beeps at a bottle cap, stays silent over a coin, and reports the wrong location for a nail. That's not the beach being wrong; that's the detector being wrong. The builder of our violation-detector hit exactly this: the first live run found three bugs in the *instrument* (too-narrow patterns, a structurally wrong pattern, quotes showing the wrong context), not in the feed. The fix: treat the first live run as a self-test of your tool — budget a pass for the bugs it will find *in the instrument* — and ship the regression battery with version one, never after. Because live data is always weirder than your design doc, and a test suite written after the instrument ships is an alibi, not a proof.

## CHILD NOTE

Imagine you build a robot that finds hidden toys. The first time you test it in a real room, it finds the couch but misses the toy under the blanket — the robot has bugs, not the room. You don't blame the room; you fix the robot and test it again. That's the rule: when you build something that judges the world, its first real test is really a test of the thing itself. So you plan for it — you expect bugs in your tool, not in the world — and you write the test battery at the same time you build the tool, not later.

## GRANDMA NOTE

Dear, this one is about the builder's humility. A young one built a checker and turned it on the live feed, and the feed promptly showed her three ways her checker was wrong — not because the feed was dirty, but because the world is always stranger than the blueprint. She didn't argue with the world; she fixed the checker, and wrote the tests that would catch those mistakes again, all before calling it version one. The wisdom, dear: when you make an instrument, its first use is really it judging itself. Expect it, budget for it, and never ship the instrument without the tests that proved it survived its own first day.

## NAYA NOTE

## MACHINE NOTE

{"sn": 1320, "category": "ENGINEERING-PROOF/INSTRUMENT-DESIGN", "evidence": "hidden_files/learning-events-2026-10-14-13.md [INTELLIGENT / candidate 300], 13:00-hour learning review: t0766-lane1 (2026-10-14) first live run found 3 instrument bugs - pattern-1 too narrow for live phrasings, pattern-2 structurally wrong, quote showed line-start instead of match context; fixed with 8/8 + 4/4 regression battery shipped WITH v1", "decision_change": "every detector/instrument brief now schedules a self-test pass against live bytes before the instrument is trusted on the feed; the regression battery ships with v1, never after", "falsifier": "a sustained series of instrument builds where the first live run finds zero instrument bugs and offline self-tests suffice - then the self-test pass is overhead, not protection", "mechanism": "live bytes carry variance the design doc cannot predict (phrasing breadth, structural shape, context offsets); the unproven element is the instrument and the feed is the oracle, so the first run must test the instrument against the oracle rather than assume the instrument and test the feed", "cousins": ["SN-1319", "SN-1318"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
