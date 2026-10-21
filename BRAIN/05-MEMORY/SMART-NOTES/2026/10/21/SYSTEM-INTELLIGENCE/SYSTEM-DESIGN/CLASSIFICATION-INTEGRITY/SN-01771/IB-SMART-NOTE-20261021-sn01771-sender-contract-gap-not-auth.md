Intelligent Block: SN-01771
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-21
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When the Smart Note sender fails, read the failure line before touching anything else: `AGENT_CAPTURE_FAILED: pipeline not verified: SMART_NOTE_CAPTURED_PROJECTION_DEFERRED` is a CONTRACT GAP, not an auth or config problem. The capture leg works — the receiver accepts the POST and rows keep landing in the store — but the GitHub-side projection leg returns DEFERRED while the workflow's pipeline-state check demands PROJECTION_VERIFIED, and it treats the mismatch as a hard failure. The correct resolution is not re-diagnosing the same line: either the receiver must complete the projection synchronously so a successful capture returns PROJECTION_VERIFIED, or the workflow must learn that CAPTURED_PROJECTION_DEFERRED means "captured, projection queued" — a success with a deferred-projection receipt and a follow-up verification — instead of a failed run. Until one of those lands, every dispatch attempt reproduces this exact line, and re-diagnosing it is waste.

## 🩷 HUMAN NOTE

Imagine a restaurant where the kitchen takes your order fine, but the host marks your visit a failure because your coat-check ticket hasn't come back yet. The order happened; the coat check is just slow. That's the sender: the capture is complete, the projection is just deferred, and the workflow grades the whole night on the coat check. Every time someone sees the red failure, the instinct is to check the locks (credentials, config) — but the locks were never broken. The failure line itself says what it is: pipeline not verified, projection deferred. Trust the line. Name the gap once, fix the gap, and don't spend the night re-picking the locks.

## 🟣 CHILD NOTE

If the library takes your book but hasn't stamped the card yet, the book isn't lost — it's just not stamped. Don't run home to make a new library card. The right fix is to stamp the card when the book comes in, or to learn that "no stamp yet" is okay and check again later.

## 🔵 GRANDMA NOTE

When the delivery driver hands you the package but the tracking page still says "in transit," the package isn't missing — the page is behind. You don't order a replacement; you fix the page, or you learn to wait for it. Same here: the capture delivered, the projection page is behind, and the workflow panics over the page instead of the package.

## 🟠 NAYA NOTE

Sender-diagnosis rule: classify `SMART_NOTE_CAPTURED_PROJECTION_DEFERRED` as CONTRACT-GAP, never as auth/config. The diagnose-first procedure is: pull the actual run log, quote the failure line. If the line reads SMART_NOTE_CAPTURED_PROJECTION_DEFERRED and store rows are still landing through other paths, the classification is CONTRACT GAP — capture leg alive, projection leg deferred, workflow check too strict. Diagnose-first is then SATISFIED; re-diagnosis is forbidden until the fix lands (synchronous projection, or deferred-treated-as-captured-queued). The 2026-10-21 diagnosis (workflow run 39199959202, `nayanet-agent-capture.yml`) is the reference case: receiver env present, POST accepted, failure at the pipeline-state check, plus the 2026-10-10 flake history at a fixed head (success/success/failure/failure across four dispatches) — consistent with a sometimes-deferred projection, not a hard break.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "contract-gap-misclassified-as-auth-failure",
  "evidence": {
    "receipts": "hidden_files/activation-sender-diagnosis-2026-10-21.md (2026-10-21 ~09:15 PDT, Naya Clarity Narzan): workflow nayanet-agent-capture.yml run 39199959202 (2026-10-19T04:32:09Z, workflow_dispatch, head 7a6a7995) — setup and completion steps success, step 2 'Capture via canonical receiver' failure, final log line AGENT_CAPTURE_FAILED: pipeline not verified: SMART_NOTE_CAPTURED_PROJECTION_DEFERRED; env SUPABASE_URL/ANON_KEY/RUNTIME_EMAIL/RUNTIME_PASSWORD all present (masked); receiver accepted the POST; failure at the pipeline-state check requiring PROJECTION_VERIFIED. Store kept receiving rows through other paths (52 rows, latest 2026-10-20 23:45Z). 2026-10-10 head fe25661c history: success, success, failure, failure across four dispatches at a fixed head — a sometimes-deferred projection, not a hard break. Same projection family as PR #2776 (projection commit SHA verification)."
  },
  "decision_change": "Next sender failure with the SMART_NOTE_CAPTURED_PROJECTION_DEFERRED line: classify CONTRACT-GAP, expect exact reproduction, do not touch secrets/config or re-diagnose; put effort into the two fix directions (synchronous projection, or deferred-as-captured-queued) instead.",
  "falsifiability": "If a future failure line shows the receiver rejecting the POST, an auth 401, or zero new store rows, the CONTRACT-GAP classification is wrong for that run — it is auth/config, and this note's classification must yield to the line. If the workflow ever fails with a different pipeline state, that leg gets its own classification. The classification dies if the receiver is shown logging 'projection deferred' for captures whose rows never appear.",
  "mechanism": "The workflow's pipeline-state check conflates two distinct legs — capture (receiver accepts, row stored) and projection (GitHub-side IB projection, async) — into one success condition. Capture-success-plus-projection-deferral is a queueing state, not a failure state; grading it as failure re-diagnoses the same deferred line on every dispatch until one of the two fix directions removes the conflation.",
  "applies_when": ["capture", "sender-workflow", "failure-classification", "projection"],
  "enforcement": "The diagnose-first verification step on any sender failure: pull the actual run log and quote the failure line before touching credentials or config. If the line reads SMART_NOTE_CAPTURED_PROJECTION_DEFERRED, the run is classified CONTRACT-GAP per this note — diagnose-first is satisfied and re-diagnosis is forbidden until the projection fix lands. The sender lane's diagnosis receipts must quote the line; a diagnosis without a quoted failure line is bounced.",
  "coincidence_check": "cousins SN-1668 (workflow-skin misclassifies a CI red — different: CI verdict presentation, not capture pipeline legs); SN-1751 (security probe discipline — unrelated); PR #2776 (projection SHA fix — sibling fix, this note governs the classification, not the patch). Distinct leg: the sender's two-leg capture-vs-projection contract and the no-re-diagnosis rule."
}
~~~
