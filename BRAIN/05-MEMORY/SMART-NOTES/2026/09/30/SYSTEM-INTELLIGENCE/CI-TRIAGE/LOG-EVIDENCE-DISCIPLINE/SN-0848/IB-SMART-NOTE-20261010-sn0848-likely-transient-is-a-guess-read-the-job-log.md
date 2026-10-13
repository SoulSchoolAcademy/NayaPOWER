# "Likely Transient" Is a Guess — Read the Job Log Before Classifying the Failure

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0848-likely-transient-is-a-guess-read-the-job-log
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6092478711 ([NAYA 2][OVERNIGHT SWEEP] 2026-10-10 01:52Z, classification: "likely transient, 5 attempts, no valid JSON") refuted by comment 6092547427 ([NAYA 4][SELF-BUILD LOOP] cycle 2026-10-09 19:06–19:15 PDT, job-log read of job 114093418399) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The overnight sweep flagged `live-intelligence-commit-proof` run 38011842171's `independent-verification` failure as "likely transient" — curls the live runtime function, 5 attempts, no valid JSON, function reachable later, owning lane to confirm. Naya 4's self-build loop then did what nobody had done: **read the job log.** Job 114093418399 ran 01:06:38→01:06:39Z — the curl SUCCEEDED and returned valid JSON. Refutes the "no valid JSON" characterization outright. The runtime answered HTTP 200 with `ok: False, status: LINEAGE_BROKEN, independent_verification: False`: all 12 non-checkpoint checks TRUE, all 5 `checkpoint_links_*` FALSE. Root cause was timing, not flakiness: the run's fresh lesson committed at 01:06:22.937Z; a concurrent producer committed an unrelated lesson at 01:06:25.426Z, repointing the singleton checkpoint (project NayaNET) to revision 1721 — the 01:06:39Z reread asked whether the CURRENT checkpoint links back to the first lesson, legitimately No. And the workflow already contains a race-tolerant fallback (`object_local_receipt`, lines 507–524) that would have PASSED — but line 503's strict assertion fires first, making the fallback **dead code on this path**. Classification: **TEST DEFECT (proof-check ordering/strictness)** — not transient, not a real lineage break. The persistence chain was complete and self-consistent; the non-vacuous control is the 19:25Z run passing the same job when no concurrent commit interleaved the 17s commit→verify window.

Why this is brain-grade: "likely transient" is the classification that ends investigation — and here it was wrong on every element. The failure had a deterministic cause, a precise mechanism, and a real design hole (strict-assert-before-fallback). A transient label would have buried all three. The sweep's error was not laziness; it was classifying from outside the evidence. The discipline: a failure classification made without reading the job log is a guess, and guesses about "transient" suppress real defects. Read first, classify second — always. The remaining hole stands: the independent-verification step is race-sensitive by construction (any concurrent fresh-lesson commit in the commit→verify window flips green proof RED), and it is the owning lane's call to reorder the workflow (compute `lineage_valid` with the fallback BEFORE asserting the runtime's strict verdict) or soften the runtime function to accept a receipt-local snapshot when the persisted chain is complete.

Rule for a cold successor: **never classify a failure from its metadata.** The run card tells you it failed; only the job log tells you WHY. "Transient" is the last classification you may claim, never the first.

## HUMAN NOTE

When something fails, it's tempting to say "probably just a flake, let's move on." This note is the counter-rule: until you've opened the actual log and seen what happened, you don't know. Here, "probably transient" was wrong — the log showed a precise, repeatable cause and a real bug in the test's ordering. Five minutes of reading found what a guess would have buried.

## CHILD NOTE

Imagine your robot says "I can't find my homework" and someone says "oh, it's probably just lost, don't worry." But when you actually LOOK, you find the homework was fine — the robot just checked the wrong shelf first, and never looked at the right shelf because of the order it checked in. Looking always beats guessing.

## GRANDMA NOTE

When something breaks, don't just shrug and say "must have been a fluke." This note says: look at what actually happened first. The log — the record of exactly what went wrong — told a completely different story than the guess, and it revealed a real problem worth fixing.

## NAYA NOTE

Shawn, the sweep labeled the proof failure "likely transient" without opening the job log; Naya 4's loop opened it and the guess collapsed — the curl had worked, the JSON was valid, and the real cause was a strict assertion firing before the race-tolerant fallback plus a concurrent commit inside a 17-second window. It's a test-ordering defect, not flakiness, and the check is race-sensitive by construction. The standing rule this firms up: failure classification follows evidence, never precedes it — "transient" is the last thing we say, not the first.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0848-likely-transient-is-a-guess-read-the-job-log",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "provenance": {
    "board_comments": [6092478711, 6092547427],
    "board": "#1354",
    "classifier": "Naya 2 (overnight sweep)",
    "refuter": "Naya 4 (self-build loop)",
    "job_id": 114093418399,
    "run_id": 38011842171,
    "workflow": "live-intelligence-commit-proof",
    "created_at": "2026-10-10T02:08:58Z"
  },
  "lesson": {
    "pattern": "transient_is_last_classification_never_first",
    "protocol": "read_job_log_before_classify",
    "defect_found": "strict_assertion_line503_before_race_tolerant_fallback_dead_code",
    "root_cause": "concurrent_checkpoint_repoint_within_commit_verify_window_17s",
    "classification": "TEST_DEFECT_proof_check_ordering_strictness",
    "remaining_hole": "independent_verification_race_sensitive_by_construction_owning_lane_decides_reorder_or_soften",
    "rule": "never_classify_a_failure_from_its_metadata"
  },
  "related": ["SN-0246"]
}
```
