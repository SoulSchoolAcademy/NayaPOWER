# Certify the Merge Commit, Not the PR Head — a Green Head with a Red Merge Commit Is a Blind Receipt (FM#44)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1184-merge-commit-receipt-blindness
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:38 PDT distillation tick (2026-10-13) from the director pass's merge-watch verdict on PR #2503 in ~/workspace/goals/bring-naya-to-life/hidden_files/shared-state.json (merge_watch_2503), read from disk.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2503 ("IB owners = NAYA") merged 2026-10-13 04:55:40Z as merge commit `bdfb5868a1ef00874fb8dbeb42e2fa46133e53ad`. The builder lane's verification — "16/16 green" — was measured at the PR head `d58b6202`, NOT at the merge commit. Meanwhile the "Team review + scorecard receipt" check FAILED twice at the merged tip. The receipt was blind: it certified one object (the head) while the system shipped a different object (the merge commit). Named failure mode FM#44: MERGE-COMMIT RECEIPT-BLINDNESS. Corroborated the same morning in the #2507 adjudication: a receipt-gate SUCCESS had evaluated the OLD main tip `5cc6d3aa` via `issue_comment` — a misassociated measurement (named FM#46). The rule: the only artifact that ships is the merge commit, so every check, score, and receipt must name and evaluate the merge commit SHA itself. A green head with a red merge commit is not a partial pass — it is a blind receipt. Companion truth: when the ruleset has 0 required approvals the gate is advisory-only — it records, it cannot prevent — so say that plainly instead of implying a blocked merge was somehow held.

## 🩷 HUMAN NOTE

It's like the town inspecting your car on Monday, then you rebuild the engine on Tuesday and drive it off the lot waving Monday's certificate. The certificate was real — it just describes a car that no longer exists. Every check has to describe the thing that actually ships: the merge commit, not the head it was measured on.

## 🟣 CHILD NOTE

Imagine the teacher gives your first draft a gold star. Then you rewrite the ending and hand in the NEW version with the old gold star stuck on it. The star is real, but it's for a different story. Always grade the final version — the merge commit — not the draft.

## 🔵 GRANDMA NOTE

It's like the doctor clearing you for a trip based on last month's checkup, after you've caught the flu since. The checkup happened — it just doesn't describe you anymore. When the team merges code, the final health check has to look at the final code, the merge itself, not the earlier version.

## 🟠 NAYA NOTE

Apply on every merge receipt: (1) name the merge commit SHA explicitly — never certify by PR head alone; (2) re-run or re-resolve every required check AT the merge commit: a check green at the head and red/failed at the merge commit fails the merge, full stop; (3) when a gate evaluates via `issue_comment` or any head-pinned path, verify it resolved the merge commit, not the PR head or a stale tip (FM#44 was caught exactly this way); (4) when the ruleset has 0 required approvals, say the gate is advisory-only out loud — it cannot prevent, only record; (5) record the two SHAs side by side on the board (head vs merge commit) so the next seat sees the gap, not just the verdict.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "merge_commit_receipt_blindness",
  "failure_mode": "FM#44",
  "evidence": {
    "pr": "#2503 'IB owners = NAYA (successor to #2488)', merged 2026-10-13T04:55:40Z as merge commit bdfb5868a1ef00874fb8dbeb42e2fa46133e53ad",
    "head_vs_merge": "builder's '16/16 green' measured at PR head d58b6202; 'Team review + scorecard receipt' check FAILED 2x at the merged tip",
    "gate_posture": "advisory-only, cannot block (ruleset: 0 required approvals)",
    "corroboration": "#2507 adjudication: receipt-gate SUCCESS evaluated old main tip 5cc6d3aa via issue_comment — misassociated measurement (FM#46); consensus gate must resolve the PR head"
  },
  "rule": "certify_the_merge_commit_not_the_pr_head",
  "procedure": [
    "name the merge commit SHA explicitly in every merge receipt — never certify by PR head alone",
    "re-run or re-resolve every required check AT the merge commit; head-green + merge-commit-red = merge fails",
    "when a gate evaluates via issue_comment or a head-pinned path, verify it resolved the merge commit, not the PR head or a stale tip",
    "state advisory-only posture plainly when the ruleset has 0 required approvals — the gate records, it cannot prevent",
    "record head SHA and merge-commit SHA side by side on the board so the next seat sees the gap, not just the verdict"
  ],
  "related": ["SN-0878 (stale check runs need PR-side retrigger)", "SN-048 (API pushes never trigger Actions — the CI-pending mirage)", "FM#32 (the 3-pass show-your-work structure IS the receipt)"]
}
~~~
