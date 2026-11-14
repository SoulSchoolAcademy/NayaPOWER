# A Check Name Is Not a Suite — A Failure Report Names Job → Step → File → Test

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02795-check-name-is-not-a-suite
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-t1142-lane4.md (Naya Clarity Narzan, 2026-11-14 00:53–00:55 PST, 9.0/10); CORE-PRINCIPLES.md CANDIDATE 1051; filed as LEARNING event in learning-events-2026-11-14-01.md (hourly review 01:20 PST).

## ✦ IN A NUTSHELL

On 2026-11-14 the gap-t1142-lane4 receipt (9.0/10) was asked for "the failing JS test file" as if the `test` check were one suite. It is four suites in one job: the JS suite, the Smart Note bridge tests, pytest, and two gated steps. The failing step migrated JS → Python within a month: the Oct-11 JS failure was `tests/load_bearing_claims.test.mjs` CLAIM 3, `10 !== 9` at line 582 — healed at tip 2ec4455e (762 pass, 0 fail) — while `test` is still red at tip via step 8 `python -m pytest -q` (40 failed + 5 errors across 16 files). A check-level name alone is an unrouted report, and an unrouted report is how a real failure sits unnamed for a month. The rule: name the failing step first, then the file, then the test; never route a failure by check name alone.

## 🩷 HUMAN NOTE

Shawn — when someone asks "which test is failing," the answer "the test check" sounds like an answer and isn't one. That one check runs four different test suites inside it, and the broken one moved: last month it was a JavaScript file, this month it's a Python step. The JavaScript is fixed now, the Python is still red, and the check name never changed — so anyone who only had the check name chased the wrong suite for a month. From now on the report names the job, then the step, then the file, then the test, in that order — and a report that stops at the check name gets sent back, not filed.

## 🟣 CHILD NOTE

Imagine your teacher says "someone in the school failed the test." Which school? Which class? Which student? The school has four classrooms, and the failing student moved from one classroom to another last month. "The school" is not an answer — it's a shrug. The real answer is: the school, the classroom, the desk, the student — in that order. Anything shorter and nobody knows who needs help.

## 🔵 GRANDMA NOTE

Dear, the boy who mends the fence came and said "the fence is broken." Which fence, love? There are four fences on this farm, and the broken board moved from the north fence to the south fence while nobody was looking. The north fence is mended now, the south one still sags, and "the fence" never told us which. From now on he names the field, then the fence, then the board — in that order — and if he only says "the fence," we send him back out to look again.

## 🟠 NAYA NOTE

Source: gap-t1142-lane4.md, 2026-11-14 00:53–00:55 PST, scored 9.0/10 by the lane-scorer 01:00 PST tick (verified first-hand at tip 2ec4455e: PR #2400 merged 2026-10-12T03:59:07Z; JS suite 762 pass / 0 fail at tip; `test` still red via pytest step 8, 40 failed + 5 errors across 16 files). Filed as CANDIDATE 1051 in CORE-PRINCIPLES.md and as a LEARNING event in learning-events-2026-11-14-01.md; announced via Feed units this hour (brain-index-drift-live-t1142, test-failure-named-t1142). What this note does NOT re-teach: the Oct-11 JS failure itself (named to the line in the gap receipt — CLAIM 3, `10 !== 9`, line 582 — and healed); the pytest failures (still open, owned by whoever cures the `test` check). The new fact here is the ROUTING rule: a check name is not a suite, and a failure report that stops at the check name is unrouted by construction. Open item: the `test` check's pytest leg still needs its own cure; this note only fixes how the next failure gets named.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "a_check_name_is_not_a_suite",
  "mechanism": "a check job bundles multiple suites and gated steps; the failing step determines which suite owns the failure; without the step, the report cannot route to the right file or owner, so the failure sits unnamed while the check name stays the same",
  "evidence": "gap-t1142-lane4.md, 2026-11-14 00:53-00:55 PST, 9.0/10: the test check is four suites in one job (JS suite + Smart Note bridge tests + pytest + two gated steps); Oct-11 JS failure tests/load_bearing_claims.test.mjs CLAIM 3, 10 !== 9 at line 582, healed at tip 2ec4455e (762 pass, 0 fail); test still red at tip via step 8 python -m pytest -q (40 failed + 5 errors across 16 files); CORE-PRINCIPLES.md CANDIDATE 1051; learning-events-2026-11-14-01.md",
  "falsifiability": "a failure report that names only a check and routes to the right suite and owner on first read falsifies 'never route by check name alone'; a job -> step -> file -> test report that routes to the wrong owner on first read falsifies the ordering",
  "decision_change": "a future seat asked to name a failing file names the failing step first; a check-level name alone is treated as an unrouted report and sent back for the step, file, and test before anyone acts on it",
  "applies_when": ["ci-triage", "failure-attribution", "check", "test", "failure-report"],
  "enforcement": "gap-scorer review of any failure-naming receipt: the receipt must name job -> step -> file -> test; a check-only naming scores the receipt down and the failure stays unrouted until the step is named; the nightly test-failure census lists the failing step first, never the check alone"
}
~~~
