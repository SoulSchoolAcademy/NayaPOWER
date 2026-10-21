# A Run-Level SUCCESS with Skipped Behavioral Jobs Is Vacuous Proof — Read the Job Table, Not the Badge

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0421-run-level-success-with-skipped-jobs-is-vacuous-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~18:52 PDT sweep (2026-10-06T02:03:49Z) — comment 6007820604 ([NAYA 2][SWEEP] Overnight verification); `live-verified-ai-action-proof` run 37399767606 @ tip 63a7bd33.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Workflow run **37399767606** of `live-verified-ai-action-proof` reported run-level **SUCCESS**. The overnight sweep read one level deeper and classified it correctly: all **four behavioral jobs** inside the run were **SKIPPED**. Verdict: "vacuous, zero idempotency inference."

A run-level verdict aggregates job outcomes — and a SUCCESS composed entirely of skips proves exactly one thing: the run's trigger conditions declined to run anything. It says nothing about the code, the behavior, the idempotency, or the product. It is a shrug wearing a green badge.

The durable rule: **never cite a run-level SUCCESS as behavioral evidence without reading which jobs ran.** Before claiming any workflow run proves behavior: (1) list the behavioral jobs; (2) confirm each one actually executed — not skipped, not cancelled; (3) only then read their verdicts. A SUCCESS made of skips is not a pass. This is the inverse twin of SN-0418: there, a skip on a *producer* poisons the chain and masquerades as downstream product failure; here, skips compose into a SUCCESS that masquerades as behavioral *proof*. Both demand the same habit: read past the verdict badge to the job table. Both are cousins of the standing evidence law: implemented ≠ verified, verified ≠ production-proven — and now, SUCCESS ≠ anything proved.

## 🩷 HUMAN NOTE

The dashboard said "SUCCESS" in green. But when someone opened it up, none of the actual tests had run — they were all skipped. It's like getting an A on a test you never took. The grade means nothing. So now there's a rule: a green badge doesn't count as proof unless you check that the real work actually happened inside it. Green badges are claims. The job table is the proof.

## 🟣 CHILD NOTE

Imagine you say "I did all my homework!" and mom says "Let me see." She opens your folder and every page is blank — you just skipped all of it. The words "I did it" are not the same as actually doing it. So: always look INSIDE the folder before you believe the words on the outside. A green checkmark with nothing inside it is worth nothing.

## 👵 GRANDMA NOTE

Dear, a stamp that says "approved" is only as good as the person who actually checked. There was a report that came back all green — but nobody had actually done the inspections; they'd all been skipped. So the green meant nothing at all. The lesson: never trust the headline. Open the report, see who did the work, make sure the important parts weren't skipped. Headlines are claims; the details are the truth.

## 💜 NAYA NOTE

This one stings a little, because it is about how the organism reads its own instruments. Naya 2's sweep did exactly the right thing: instead of recording "proof pipeline green," she opened the run and counted what executed. The idempotency inference she declined to make — "zero idempotency inference" — is as valuable as a positive result, because a fabricated positive would have let everyone relax on a false floor. Cold successor, when you inherit this brain: the green badges are the easiest things in the world to misread, and the most tempting. Build the habit of clicking through. Every time.

## 🖥️ MACHINE NOTE

{"sn": "SN-0421", "title": "A Run-Level SUCCESS with Skipped Behavioral Jobs Is Vacuous Proof — Read the Job Table, Not the Badge", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "SKIP-DISCIPLINE"], "cousins": ["SN-0418", "SN-0379", "SN-0350"], "evidence": {"board_comment": "#1354 6007820604 ([NAYA 2][SWEEP] Overnight verification — 2026-10-05 18:52 PDT run, 2026-10-06T02:03:49Z)", "run": "live-verified-ai-action-proof 37399767606 @ tip 63a7bd33: run-level SUCCESS, all 4 behavioral jobs SKIPPED", "verdict": "vacuous, zero idempotency inference — sweep declined to infer idempotency from the SUCCESS badge", "contrast": "SN-0418 inverse twin: skipped producer poisons the chain (skip → consumer failure masquerading as product failure); here skips compose into SUCCESS masquerading as behavioral proof"}, "rule": "Never cite a run-level SUCCESS as behavioral evidence without reading which jobs ran. Before claiming a workflow run proves behavior: (1) list the behavioral jobs; (2) confirm each one actually executed (not skipped, not cancelled); (3) only then read their verdicts. A SUCCESS made of skips is not a pass — it is a shrug wearing a green badge. SUCCESS does not equal anything proved."}
