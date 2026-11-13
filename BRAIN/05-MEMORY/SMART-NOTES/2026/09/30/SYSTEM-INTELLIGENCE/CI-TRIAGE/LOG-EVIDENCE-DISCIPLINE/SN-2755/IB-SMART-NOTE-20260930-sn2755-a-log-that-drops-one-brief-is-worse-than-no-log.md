# A Log That Drops One Brief Is Worse Than No Log

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2755-a-log-that-drops-one-brief-is-worse-than-no-log
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/gate-stall-20261113-0458.md ("Mirror lesson", 2026-11-13 04:58 PST lane-executor run); hidden_files/claim-sweep-20261113-0458.log; learning-events-2026-11-13-05.md (05:20 PST hourly learning review, EVENT 1 — CANDIDATE 1042); CORE-PRINCIPLES.md CANDIDATE 1042.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A log that records 29 attempts while the run claims 30 is worse than no log at all: no log leaves the claim unproven, but a 29-line log lets a later reader assert "all 30" on proof of 29 — the missing brief is invisible exactly because the record looks complete. The 04:58 PST lane-executor run (2026-11-13) closed the defect pattern from the 0238/0453 runs, where the claim sweep was split across two exec calls (29 attempts in the sweep script plus the first b1 brief in a separate call) and only one half landed in the log. The 04:58 run merged both halves into one file — hidden_files/claim-sweep-20261113-0458.log — and verified the merge by counting: 30 `=== ATTEMPT` lines, 28 exit 7 + 2 exit 2, lane-scorer brief included. The rule: when a sweep is split across calls, the record must be merged into one file before the run ends, and the merge must be verified by counting, not by remembering. A count is wrong when the record form is incomplete — and a partial log is the most dangerous kind of wrong, because it wears the shape of proof. Cousins: SN-1995 (a label is not a landing — the "all 30" claim trusted over the log's landing) and SN-2208 (a count is wrong when the key form is missing — here, a count is wrong when the record form is incomplete). Honest scope: single-run evidence; the rule is prescribed for future split sweeps, not yet proven standing across a second split run. Falsifier: a split sweep whose unmerged logs are later reconciled without loss would show the merge is hygiene, not a correctness requirement.

## 🩷 HUMAN NOTE

Shawn — banking the split-log fix as standing law: when a claim sweep runs across two calls, merge both halves into one log file before the run ends, and prove the merge by counting the attempt lines — never by remembering what ran. The 04:58 run did it right (30 attempts, 28 exit 7 + 2 exit 2, all in one file, counted by grep). The 0238/0453 runs did it wrong: the log showed 29 while the run claimed 30, and the missing brief was invisible because the record looked complete. A partial log is worse than no log — no log leaves a claim unproven, a partial log lets someone assert the claim on proof of almost all of it.

## 🟣 CHILD NOTE

Imagine you count 30 marbles, but your notebook only lists 29 — and someone later reads the notebook and says "see, all 30 are here." The notebook looks finished, so nobody notices one marble is missing. That is worse than having no notebook at all, because with no notebook everyone knows they have to check. The fix is simple: if the counting happens in two parts, put both parts in one notebook before you finish — and then count the lines in the notebook to make sure all 30 are really there.

## 🔵 GRANDMA NOTE

We've written down a rule about keeping records. When a job is done in two parts, both parts must end up in the same record before the job is called finished — and the record must be checked by counting, not by trusting memory. The 04:58 run did this properly: all 30 attempts in one file, counted and confirmed. Earlier runs did not: the record showed 29 while the job claimed 30, and the gap was invisible because the record looked complete. A record with a hole in it is more dangerous than no record, because people trust it.

## 🟠 NAYA NOTE

Source: twelve-lane-receipts/gate-stall-20261113-0458.md (2026-11-13 04:58 PST lane-executor run — full 30-attempt claim sweep across two exec calls: 29 in the sweep script + the first b1 brief separately; both halves merged into claim-sweep-20261113-0458.log; "Mirror lesson": a log that drops one brief is worse than no log) → hidden_files/claim-sweep-20261113-0458.log (verified first-hand by grep this tick: 30 `=== ATTEMPT` lines, 28 exit 7 + 2 exit 2) → learning-events-2026-11-13-05.md (05:20 PST hourly learning review, EVENT 1 [WIN]: defect closed, CANDIDATE 1042 minted, announced via Feed unit) → CORE-PRINCIPLES.md CANDIDATE 1042 (full principle with cousins and falsifier). Defect pattern it closes: the 0238/0453 runs' logs recorded 29 while the runs claimed 30. Cousins: SN-1995, SN-2208.

## 🟢 MACHINE NOTE

{"sn": "SN-2755", "title": "A Log That Drops One Brief Is Worse Than No Log", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-11-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "LOG-EVIDENCE-DISCIPLINE"], "cousins": ["SN-1995", "SN-2208"], "authority": "04:58 PST lane-executor run 2026-11-13 (gate-stall-20261113-0458.md) + 05:20 PST hourly learning review (learning-events-2026-11-13-05.md, EVENT 1)", "evidence": {"receipt": "twelve-lane-receipts/gate-stall-20261113-0458.md Mirror lesson", "log": "hidden_files/claim-sweep-20261113-0458.log — 30 === ATTEMPT lines, 28 exit 7 + 2 exit 2, verified by grep", "defect_pattern": "0238/0453 runs logged 29 while claiming 30"}, "applies_when": ["claim", "lane-executor", "log", "claim-sweep"], "enforcement": "A lane-executor receipt claiming N attempts must carry the grep count of === ATTEMPT lines in the single merged log file; count != claim blocks the 'all N' claim — the receipt is not writable until the merged log counts N", "doctrine": {"merge_split_records": "when a sweep splits across exec calls, merge all halves into one log file before the run ends", "verify_by_counting": "verify the merge by counting attempt lines in the merged file (grep -c), never by remembering what ran", "partial_log_worse_than_none": "a log that drops one brief lets a later reader assert the full claim on proof of N-1 — the missing item is invisible because the record looks complete", "count_wrong_when_record_incomplete": "a count is wrong when the record form is incomplete; the claim must be checked against the merged record, not memory"}, "falsifier": "a split sweep whose unmerged logs are later reconciled without loss would show the merge is hygiene, not a correctness requirement"}
