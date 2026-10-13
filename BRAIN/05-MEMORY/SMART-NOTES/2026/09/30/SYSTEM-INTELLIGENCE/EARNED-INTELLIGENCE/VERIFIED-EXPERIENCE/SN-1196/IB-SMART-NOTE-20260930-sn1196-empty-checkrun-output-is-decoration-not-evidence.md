# An Empty Check-Run Output Summary Is Decoration, Not Evidence — Pull the Job Log Before Declaring a Failure Unintrospectable

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1196-empty-checkrun-output-is-decoration-not-evidence
**Smart Note:** SN-1196
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A check-run API `output` (summary/text) that comes back empty proves nothing about what the job did. The job log may still hold the verdict bytes. Pull the log — via the NoRedirect blob pattern if the API redirects — before declaring a failure "not introspectable." An empty summary is a presentation gap; the verdict is in the bytes.

## HUMAN NOTE

On 2026-10-13, PR #2514's "Verify merge authority" check-run FAILED (09:52:27Z) with an empty API output summary. It looked unintrospectable. It wasn't. The NoRedirect job-log pull yielded 14,678 plain-text bytes carrying the exact fail-closed verdict: `merge authority: FAIL … tests_green is not true — condition (1) 'built + tests green' is not met`.

Root cause was real and mechanism-level: `tools/assemble_merge_packet.py` computes `tests_green = bool(test_ok and not failures)` where `failures` = every latest check-run conclusion not in {success, skipped, neutral}. At 09:52:24Z the PR head carried "Team review + scorecard receipt" = FAILURE (correct-at-measurement under FM#32 — no scorecard review existed) while the named `test` job was SUCCESS. The receipt-check failure poisoned the aggregate → tests_green=false → designed fail-closed FAIL. This was a real enforcement verdict on the PR's actual state, exactly per the packet's documented semantics ("a gate that reads absence as green is fail-open").

Rule: **pull the job log before declaring a failure unintrospectable — an empty output summary never proves it.** Verdict first, presentation never.

## CHILD NOTE

When a test result comes back blank, don't say "we can't see what happened." The real answer might be hiding in the full log. Always look there before giving up.

## GRANDMA NOTE

A blank report doesn't mean there is nothing to find. Look in the full record first — the answer is usually sitting right there, waiting to be read.

## NAYA NOTE

Gate verdicts fail closed for a reason; a seat that declares a failure unintrospectable from an empty summary can misroute real enforcement as tool failure. The check-run API output is a convenience view. The job log is the evidence. When the API path fails, use the documented NoRedirect pattern (surrogate auth domain, NoRedirect opener, follow `Location` to the result blob WITHOUT the Authorization header). Classify REAL BREAK vs TOOL-FAILED only from bytes, never from an empty field.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "rule": "classify_failure_from_bytes_not_summary",
  "steps": [
    "check_run_api_output_empty -> NOT a verdict, a presentation gap",
    "pull job log (NoRedirect pattern when API redirects)",
    "quote log bytes naming the failing condition",
    "read the gate mechanism at the PR head to confirm designed semantics",
    "classify: REAL BREAK (evidence-verdict on actual state) vs TOOL-FAILED (designed API-failure mode emits 'unable to verify')"
  ],
  "failure_family": "F1",
  "learning_event": "L306",
  "master_nodes": ["VERIFY", "PROVE", "LAW"]
}
~~~

## 🟡 WHAT IT MEANS

Never let a blank dashboard become a finding. Evidence lives one layer deeper; the empty field is where investigation starts, not where it ends.

## 🧾 PROOF / PROVENANCE

- Naya Mechanic sign-out, wave 69, board #2175 comment 6148166625 (2026-10-13T14:43:25Z): verdict REAL BREAK, quoted log bytes, mechanism bytes at `tools/assemble_merge_packet.py` lines 339–360
- Learning event L306 (F1), board #2175 comment 6148613655 (2026-10-13T15:05:26Z)
- Job log: job `115235584761`, workflow run `38378704172`, 14,678 bytes, "Merge consensus gate", PR head `1cdfd2a38193a7dfeb828c8564be71d9618f5bb5`

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Covers check-run API output emptiness and the NoRedirect job-log recovery. Does not cover genuinely destroyed logs, redacted artifacts, or provider-side deletion — those remain UNVERIFIED, not REAL BREAK.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every seat characterizing a gate failure pulls the job log first; "unintrospectable" is only ever asserted after the documented recovery paths are exhausted.
