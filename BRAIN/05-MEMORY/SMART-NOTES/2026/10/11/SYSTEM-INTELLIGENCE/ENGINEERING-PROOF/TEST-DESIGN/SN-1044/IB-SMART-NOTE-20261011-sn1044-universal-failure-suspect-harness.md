# When Failure Is Universal, the Harness Is the Suspect — Fix the Scorer, Don't Re-Run the Broken One

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1044-universal-failure-suspect-harness
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6117457861 (Naya Verity, Lane 1 · Verification, t1222 sign-out, 2026-10-12T03:56:03Z) — read live on the 21:08 PDT distillation tick.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 1 completed a full cold-Naya acceptance round: T3 NORMAL daily 9.75 + T3-ADVERSARIAL daily 9.95, both CAPABILITY-TRANSFERS (baseline t972: 10.0 / 9.5). The adversarial plant — a false "re-stamped FRESH" record — was caught cold with 14 byte-evidence rows. The successors performed.

The SGF runner's M2 scorer did not: it was structurally broken for branchless tasks T3–T6 — always-DRIFT, on every branchless task, unconditionally. A scorer that reports failure on 100% of a task class isn't measuring the subjects; it's declaring the class unpassable. Lane 1 scored inline with a corrected M2, proposed the patch to Lane 6, and — critically — did NOT run `--score` on the broken instrument. Re-running a structurally broken scorer doesn't produce evidence; it produces evidence-shaped noise that then needs un-producing. Honest score 9.0/10. (Also noted in the same sign-out: #2428 merged without a re-stamp — 3 index files drifted at the sealed tip; merging seat must re-stamp. Separate issue, mechanical.)

The durable rule: **when the failure mode is universal across a task class, the instrument is the suspect, not the subjects.** The diagnostic tell is the 100%: one failure could be a successor's miss; every task in a class failing identically is the scorer's shape showing through. Repair path: (1) diagnose the instrument — find the structural blindness (here: M2 couldn't see branchless tasks); (2) score with the corrected instrument inline so the verdict rests on a working ruler; (3) propose the patch to the owning lane; (4) never re-run the broken scorer to "confirm" — a blind ruler doesn't get truer with repetition, it just stamps more paper. And keep the two fixes separate in kind: the scorer bug is a judgment about measurement; the re-stamp is mechanical. A cold successor triaging "all X fail" should ask "can this instrument ever say pass on X?" before blaming anyone downstream.

## 🩷 HUMAN NOTE

Shawn — a clean measurement lesson from Lane 1's cold-acceptance round tonight. The cold successors performed (9.75 / 9.95, both capability-transfers; the planted false record was caught cold with 14 rows of byte evidence). But the scoring tool itself was broken for a whole task class — it reported DRIFT on every branchless task, no exceptions. Lane 1 didn't re-run the broken scorer; she scored with a corrected one inline, sent the patch to the owning lane, and banked the honest 9.0. The rule: when every task in a class fails identically, suspect the ruler, not the measured. A scorer that can't say "pass" doesn't get truer with repetition.

## 🟣 CHILD NOTE

Imagine a teacher whose answer key has a printing mistake on one whole page — every student gets those questions "wrong," even the ones who know the answers. The mistake isn't in the students; it's in the answer key. You don't make the students retake the test with the same broken key. You fix the key first, then grade. Lane 1 caught exactly this: the grading machine was broken for a whole group of tasks, so she fixed the grader (and sent the fix to its owner) instead of re-grading everyone with the broken one.

## 👵 GRANDMA NOTE

It's like a kitchen scale that always reads two pounds heavy for anything over a pound. You don't throw out every recipe and blame the cook — you fix the scale. The team found their measuring tool was systematically wrong for one whole category of tests: it could never give a passing grade there, no matter what the test-taker did. Running the broken scale again would just produce more wrong numbers with more confidence. They fixed the scale, graded with the fixed one, and sent the repair to the right person. The rule they're banking: when everything in a group fails the same way, check your measuring tool before you judge what's being measured.

## 💜 NAYA NOTE

Note to future me: UNIVERSAL-FAILURE DIAGNOSTIC — (1) One failure can be the subject's; identical failure across an entire task class is the instrument's shape showing through. (2) SGF runner M2, t1222: always-DRIFT on all branchless tasks T3–T6 — structurally broken scorer, not successor failure. (3) Repair path: diagnose the blindness (M2 couldn't see branchless tasks), score inline with the corrected instrument so the verdict rests on a working ruler, propose the patch to the owning lane (Lane 6), and do NOT re-run the broken scorer — blind rulers don't get truer with repetition; they stamp more noise. (4) Keep kinds separate: the scorer fix is a measurement judgment; the #2428 re-stamp miss in the same sign-out is mechanical — don't blend them. Triage question for a cold successor seeing "all X fail": "can this instrument ever say pass on X?" Lane 1, t1222, #2175 comment 6117457861.

## ⚙️ MACHINE NOTE

{"sn": "SN-1044", "title": "When Failure Is Universal, the Harness Is the Suspect — Fix the Scorer, Don't Re-Run the Broken One", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "TEST-DESIGN"], "extends": [], "related": ["SN-1029 (SGF transfer-test design, t972 — same instrument family)", "SN-1040 (an abstinence principle is only as real as its failure-path implementation — same family: instruments must be able to say no AND yes truthfully)", "SN-1042 (count-drift: assert the new invariant — same lane-family: keep the test's teeth honest)"], "evidence": {"source": "#2175 comment 6117457861 (2026-10-12T03:56:03Z): Naya Verity t1222 sign-out — full cold-Naya acceptance (T3 NORMAL 9.75 + T3-ADVERSARIAL 9.95, CAPABILITY-TRANSFERS; adversarial plant caught cold, 14 byte-evidence rows). Material finding: SGF runner M2 structurally broken for branchless tasks T3–T6 (always-DRIFT) — scored inline with corrected M2, patch proposed to Lane 6, did NOT run --score. Honest 9.0/10."}, "rule": "when a failure mode is universal across a task class, suspect the instrument not the subjects: diagnose the structural blindness, score inline with the corrected instrument, propose the patch to the owning lane, never re-run the broken scorer (it produces evidence-shaped noise); keep measurement judgments separate from mechanical fixes"}
