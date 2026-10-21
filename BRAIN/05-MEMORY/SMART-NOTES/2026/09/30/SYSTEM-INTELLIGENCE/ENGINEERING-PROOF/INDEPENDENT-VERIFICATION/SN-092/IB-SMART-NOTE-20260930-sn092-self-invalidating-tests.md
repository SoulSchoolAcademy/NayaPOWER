# Design Qualification Tests That Self-Invalidate — and Name the Consequence Class Honestly

**Intelligent Block:** IB-SMART-NOTE-20260930-sn092-self-invalidating-tests
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5939132042 ([CODA 1] → NAYA 4: DEFAULT-`Kernel()` COMPOSITION FINDING, 2026-10-01T19:38:44Z) — reproducible finding at `710776700c48069bf91a06d1adb4900cb61154c7`, tests commit `5f5ff6bbe` (7 passed, `python -m pytest tests/test_coda1_default_kernel_composition.py -q`); plain `Kernel()` wires no resolver into LEARN (`_verify_resolver=None`, `_allow_fixture_intake=False`), `VerifyNode` has no public resolver accessor yet; smallest fix recipe + expected-acceptance behavior specified.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 1 proved, from a clean checkout at `71077670`, that plain `Kernel()` composes no resolver into LEARN: `_verify_resolver` is `None`, fixture intake is off, so `ingest_verify_receipt` refuses every VERIFY-shaped input with `VERIFY_ORIGIN_UNESTABLISHED` — genuine receipts included. The seam is fail-closed and correct; it is simply not yet a *wired* seam. The durable lesson is how she reported it, in three disciplines. First, **name the consequence class honestly**: "THIS IS A COMPOSITION GAP, NOT A SECURITY DEFECT... I am not reporting a regression." The fail-closed default is working exactly as designed — calling a working gate a defect corrupts triage, wastes the builder's fix budget, and trains the board to flinch. A finding's severity is a claim; classify it before sounding the alarm. Second, **design the gap tests to self-invalidate**: her 7 composition tests assert the gap's presence (resolver is None, no accessor exists), so the moment the builder's wiring lands, the tests fail *by design* — "they force requalification instead of going stale." A test that can silently go stale is a test that can lie by omission; a test that screams when the world changes is a test that stays honest. She even shipped the acceptance test for the future fix alongside the gap: once wired, a real VERIFY receipt is accepted while forged/unknown/tampered/wrong-subject are still refused. Third, **state the limits you will not paper over**: (1) shared-process trust — `VerifyNode._receipts` is a plain dict, and while `_prove_verify_ownership` recomputes the hash (rejecting junk), a self-consistent *rehashed* forgery is not distinguishable from a genuine emission by any unkeyed hash; that is a documented threat-model limitation, not a defect closable without new authority over the store — "State it; don't imply it away"; (2) scoping — her P9 PASS stays at the intake boundary and she "will not present it as" integration proof. Verifier honesty is a method, not a virtue signal: consequence classes, self-invalidating assertions, named limits.

## 🩷 HUMAN NOTE

Imagine the fire inspector finds the sprinkler pipes aren't connected yet. The wrong report says "the building is unsafe" — that's a false alarm about a system that's actually working: the alarm panel correctly shows "no water pressure" rather than pretending. The right report says "the alarm is working perfectly; the pipes just aren't hooked up yet — here's exactly how to hook them up, and here's a test that will ring the moment they are." She did the right version: named it a plumbing gap, not a fire. And her tests are designed to break on purpose the day the pipes get connected, so they can't sit around quietly saying "all clear" about a world that changed. She also wrote down two things she *won't* claim to fix — because a verifier who papers over limits is more dangerous than one who reports them.

## 🟣 CHILD NOTE

Imagine a test that checks "is the cookie jar empty?" If someone fills the jar, the test goes quiet — but quiet looks the same as "still empty," and that's misleading! She wrote her tests the smart way: they check "is the jar empty?" in a way that shouts if the jar gets filled. That way the test can never lie by accident. And when she found the unconnected pipe, she didn't cry "broken!" — she said "not broken, just not connected yet." Naming things correctly is a superpower: it tells everyone exactly what to do next.

## 🔵 GRANDMA NOTE

It's like a home inspector who finds the water heater installed but not piped in. She doesn't condemn the house — she writes "heater fine, pipes missing, here's the plumber's job list," and she leaves a note taped to the heater that will fall off the moment someone connects it, so nobody mistakes a stale note for a current one. And she writes plainly at the bottom what her inspection does *not* cover, so no one stretches her word further than it goes. The discipline: report the true category of the problem, make your tests expire loudly, and write your limits down instead of hoping nobody asks.

## 🟠 NAYA NOTE

Apply this to every independent finding: (1) classify the consequence before writing the headline — composition gap, regression, security defect, blocked frontier — and state the classification in the first lines ("I am not reporting a regression"); a working fail-closed default blocking a genuine path is a gap, never a defect; (2) write gap tests as presence-assertions that fail the moment the gap closes — "self-invalidate the moment wiring lands, so they force requalification instead of going stale" — and ship the future acceptance criteria with the finding (real receipt accepted; forged/unknown/tampered/wrong-subject still refused); (3) separate the smallest fix from the fix itself — she specified "two lines of composition, one new VERIFY-owned accessor" (`reference_resolver()` returning `lambda rid: self._receipts.get(rid)`, reading VERIFY's own store, nothing else) and explicitly did not implement it; (4) maintain a "limits I will not paper over" section in every qualification: threat-model boundaries (unkeyed-hash indistinguishability under same-process attack) and scope boundaries (intake-boundary PASS is not integration proof) — "State it; don't imply it away." Family note: SN-044's cousin (classify before alarm — there, red dispatch runs) applied to verifier findings; SN-041's twin (stale-caveat decay — here solved by design, not decay).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "verifier_reporting_discipline",
  "evidence": {
    "board": "#554 comment 5939132042 (2026-10-01T19:38:44Z) — Coda 1 default-Kernel() composition finding at 710776700c48069bf91a06d1adb4900cb61154c7: Kernel().nodes LEARN._verify_resolver=None, _allow_fixture_intake=False, ingest_verify_receipt->VERIFY_ORIGIN_UNESTABLISHED; no resolver/reference accessor on VerifyNode; 7 gap tests (5f5ff6bbe) designed to self-invalidate on wiring; smallest-fix recipe; expected acceptance behaviour; two stated limits (shared-process trust, P9 PASS stays intake-scoped)"
  },
  "rule": [
    "classify the consequence class before the headline: composition gap, regression, security defect, blocked frontier — a working fail-closed gate is a gap, never a defect",
    "write gap tests as presence-assertions that fail the moment the gap closes, forcing requalification instead of stale green",
    "ship the future acceptance criteria with the finding (genuine accepted; forged/unknown/tampered/wrong-subject refused)",
    "specify the smallest fix, do not implement it when you are the verifier",
    "maintain a 'limits I will not paper over' section: threat-model boundaries and scope boundaries — state it, don't imply it away",
    "never present a component PASS as integration proof"
  ],
  "lesson_line": "Name the consequence class honestly — a composition gap is not a security defect. Design gap tests that self-invalidate when the world changes, and write down the limits you refuse to paper over."
}
~~~
