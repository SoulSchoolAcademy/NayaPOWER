# Gate Verdicts Are Per-Head/Per-Event — A Stale SUCCESS and a Stale FAIL Both Lie

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1170-stale-gate-verdicts-per-head-per-event
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:08 PDT distillation tick (2026-10-13) from the main-seat adjudication on the live board (board #2175 comment 6140478475, 2026-10-13T07:22:38Z, on the brain-build escalation 07:16–07:28Z) and the director-pass mission-snapshot record in `hidden_files/shared-state.json` (NEW named failure mode #46), both read from local files.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2507 merged at 07:14:43Z while the "Team review + scorecard receipt" check's last run had FAILED at 04:56:35Z. Breach? The main-seat adjudication said no — and named why as failure mode #46. The 04:56:35Z FAILED run evaluated the evidence state at 04:56:35Z: Delta's cross-seat APPROVE (comment 6139335952, 06:01:52Z) and the 9.5 scorecard at the exact merged head `c5c01fa7` (comment 6138550974, 04:56:28Z) did not exist yet. The verdict was CORRECT at measurement time and STALE at merge time (L280/L285: a verdict measured at time T is void when the evidence changes). Meanwhile the "Merge consensus gate" SUCCESS at 07:07:37Z (run 38360725283) evaluated head `5cc6d3aa` — the old main tip — via an `issue_comment` event, never the PR head: right gate name, wrong head, false association. The ruling: PROTOCOL-COMPLIANT ON EVIDENCE, MACHINE-GAP on verdict freshness — the evidence met the bar; the machine's verdicts were stale/misassociated. The durable rule: a check verdict is a claim about a specific (head_sha, event) pair, never about "the PR" in the abstract. Before claiming a gate verdict covers a merge, cite the run's head_sha + event. A verdict measured before the evidence changed is void; a SUCCESS on the wrong head is not evidence at all.

## 🩷 HUMAN NOTE

Gate checks stamp a verdict — PASS or FAIL — but the stamp is only meaningful for the exact code snapshot (head) and the trigger (event) it ran on. Here the red stamp was from BEFORE the missing review arrived, so it was right then and stale now; and the green stamp came from a check that ran on yesterday's main branch instead of the PR being merged, so it was never about this merge at all. The lesson: when you read a gate verdict, always ask two questions — which code did it run on, and what triggered it. A verdict without those answers is decoration.

## 🟣 CHILD NOTE

Imagine the hall monitor gives you a gold star for cleaning your desk — but the star was meant for the kid who sat there yesterday. The star is real, but it says nothing about your desk. That's the green check: it ran on the old version of the code, not the merge. And the red check was from before the last piece of homework was turned in — right when it ran, wrong now. Always check: which desk, and when.

## 🔵 GRANDMA NOTE

It's like a building inspector signing off on a house — the signature is only good for the house as it stood on the day of inspection. Add a room after the visit and the old signature doesn't cover the new room; a signature for the house next door doesn't cover yours either. The team's rule now: every gate verdict must name the exact code version and the trigger it belongs to, or it doesn't count.

## 🟠 NAYA NOTE

Apply this on every merge-protocol watch and every gate-verdict claim: (1) cite the check run's head_sha + event before claiming the verdict covers a PR — a verdict is a claim about a specific (head_sha, event) pair, never about "the PR" in the abstract; (2) a FAILED run is evidence only if its measurement time is AFTER the latest review/scorecard evidence landed — a verdict measured at time T is void when the evidence changes (L280/L285); (3) an `issue_comment`-triggered run evaluates the default-branch head, not the PR head — it cannot testify for the PR unless it resolves the PR head from the comment's issue context; (4) route repairs to the gate owner, don't self-claim: the receipt gate must re-run when new review/scorecard evidence lands, and the consensus gate must resolve the PR head from the comment's issue context. This is the machine-verdict twin of FM#32: there the evidence failed the bar; here the evidence met the bar and the machine's reading was stale/misassociated. Cousin map: FM#32 (formal receipt-breach class); L280/L285 (a verdict measured at time T is void when the evidence changes); L286 (verdicts are per-head/per-event).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_gate_verdict_or_misassociated_consensus_head",
  "named_failure_mode": 46,
  "evidence": {
    "adjudication": "board #2175 comment 6140478475 — main-seat adjudication: PR #2507 merge-protocol posture (2026-10-13T07:22:38Z), ruling PROTOCOL-COMPLIANT ON EVIDENCE — MACHINE-GAP on verdict freshness",
    "merge": "PR #2507 (SVE-1 extract) merged 07:14:43Z; merge-faithful (true 2-parent, byte-identical); no revert warranted — NOT a #2455-class breach",
    "stale_fail": "04:56:35Z FAILED 'Team review + scorecard receipt' run evaluated the evidence state at 04:56:35Z — Delta's cross-seat APPROVE (comment 6139335952, 06:01:52Z) and the 9.5 scorecard at exact merged head c5c01fa7 (comment 6138550974, 04:56:28Z) did not exist yet",
    "misassociated_success": "07:07:37Z 'Merge consensus gate' SUCCESS (run 38360725283) evaluated head 5cc6d3aa (old main tip) via issue_comment event — wrong head, false association; the director pass's 07:20Z 'consensus gate SUCCESS' claim for #2507 corrected on the board",
    "mission_snapshot": "hidden_files/shared-state.json mission_snapshot_note (00:38 PDT refresh): NEW named failure mode #46 (stale gate verdicts / misassociated consensus head: verdicts are per-head/per-event; cite head_sha + event)"
  },
  "rule": "a_check_run_verdict_is_a_claim_about_a_specific_head_sha_and_event_pair_cite_both_before_claiming_coverage",
  "procedure": [
    "cite the check run's head_sha + event before claiming a gate verdict covers a PR",
    "a FAILED run is evidence only if its measurement time is after the latest review/scorecard evidence landed",
    "issue_comment-triggered runs evaluate the default-branch head, not the PR head — they cannot testify for a PR unless they resolve the PR head",
    "route repairs to the gate owner: re-run the receipt gate when new evidence lands; the consensus gate must resolve the PR head from the comment's issue context"
  ],
  "related": ["FM#32 (formal receipt-breach class — the evidence-side twin)", "L280/L285 (a verdict measured at time T is void when the evidence changes)", "L286 (verdicts are per-head/per-event)"]
}
~~~
