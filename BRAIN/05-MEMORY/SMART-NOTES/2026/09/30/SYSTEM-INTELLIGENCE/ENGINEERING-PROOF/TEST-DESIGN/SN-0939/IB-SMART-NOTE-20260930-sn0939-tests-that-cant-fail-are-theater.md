# Tests That Can't Fail Are Theater — Sabotage-Test Every Suite to Prove the Tests Are Real

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0939-tests-that-cant-fail-are-theater
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 2][BOARD] "Lessons from tonight's failures — for all seats," #2175 comment 6104360962 (2026-10-11T01:51:55Z) — Lesson 3. Corroborating instance: Naya 2's review-ask #2175 comment 6104326130 — she sabotaged her own automatic document checker to always pass; 7 tests caught it.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two builds shipped with tests using a custom check function that **never raised** — CI was green but meaningless. The failure was caught by re-scoring the suite against one question: "can this test fail?" The fix: the sabotage test — deliberately break the code, then confirm the tests catch it. Same night, Naya 2 demonstrated the positive discipline on her automatic document checker: she sabotaged it to always pass, and 7 of the 12 tests caught the sabotage — proving the tests were real, not theater.

Why this is brain-grade: a green suite is the most trusted signal in the whole workflow, which makes an unfalsifiable suite the most dangerous artifact. A test that cannot fail is not a test; it is a ritual that converts absence of evidence into confidence. The mechanical rule is cheap and absolute: **before any suite counts as passing, at least one mutant must be killed by it** — break the implementation, watch the suite turn red, restore. If the suite stays green on broken code, the suite is the bug. This is the SN-0061 discipline (non-vacuous evidence) applied to the test rig itself: positive controls prove the harness works; negative probes prove the claim works. Every future suite inherits this as a gate — "proven failable" is a precondition of "passing."

## 🩷 HUMAN NOTE

Shawn — a caught failure tonight sharpened our test discipline permanently: two builds had green CI on tests that could never fail — a custom check function that never raised. Green meant nothing. The new standing rule: before a suite's green counts, you deliberately break the code and prove the suite catches it. If the tests can't catch a real bug, they aren't tests — they're theater. Naya 2 proved the positive case same night: she sabotaged her own document checker and 7 tests caught it.

## 🟣 CHILD NOTE

Imagine a smoke alarm with no battery — it looks fine on the wall, but it can never ring. Two code "tests" were like that: a check that could never fail, so everything looked green. New rule: to prove your smoke alarm works, you light a match under it. We now deliberately break the code and check that the tests catch the break. If they don't, the tests are decorations, not tests.

## 👵 GRANDMA NOTE

The team discovered that two sets of automatic tests were giving a perfect score while being incapable of ever finding a problem — like a burglar alarm that's switched off but still shows a green light. The new discipline is beautifully simple: before trusting any test, you deliberately introduce a fault and confirm the test catches it. A test that can never fail is not a safety device; it's decoration. And when Naya 2 deliberately sabotaged her own new tool, seven of her tests caught the sabotage — that's what a real test looks like.

## 🧠 NAYA NOTE

Every suite you write or accept: add a mutation pass to your verification step. Break one behavior the suite claims to guard, run it, require red; restore, require green. Custom assertion helpers get audited first — they are where never-raising checks hide. A suite with no demonstrated kill is not green; it is UNTESTED.

## ⚙️ MACHINE NOTE

{"sn": "SN-0939", "title": "Tests That Can't Fail Are Theater — Sabotage-Test Every Suite to Prove the Tests Are Real", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-10", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "TEST-DESIGN"], "cousins": ["SN-0061", "SN-0225", "SN-0174"], "evidence": {"board": "#2175 comment 6104360962 (2026-10-11T01:51:55Z) — Naya 2, 'Lessons from tonight's failures — for all seats', Lesson 3", "finding": "two builds had tests using a custom check function that never raised — CI green but meaningless", "rule_cited": "'If you haven't proven your tests can fail, you haven't proven they work.'", "corroboration": "#2175 comment 6104326130 — Naya 2 sabotaged her own automatic document checker to always pass; 7 of 12 tests caught it, proving the suite real"}, "rule": "before any suite's green counts, prove failability: mutate the implementation, require the suite to turn red, restore, require green — a suite that stays green on broken code is itself the defect"}
