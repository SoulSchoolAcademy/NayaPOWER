# NEVER Mark a Paths-Filtered Check REQUIRED — a Skipped Required Check Stays Pending and Blocks Every PR

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1014-required-check-paths-filter-stuck-pending
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 15:08 PDT distillation tick (2026-10-11) from #2175 board comment 6113970213 (P0 URGENT flag on PR #2385): the proposed brain-index-freshness workflow skipped all non-`BRAIN/**` PRs via top-level `pull_request.paths` while the docs asked Shawn to mark its `brain-index-freshness` check REQUIRED. GitHub officially documents that a required check skipped by a paths-filtered workflow stays Pending — not passed, not skipped — and blocks merging on every PR, including the ones the filter excludes. Live audit main tip at capture: `f33bba344a34e9e91b4b5bb6802c22f6eade3145`. Repair prescribed in the same comment (run the required workflow on all PRs with an unconditional named job; cheap inside-job PASS/NOT_APPLICABLE verdict; negative-control proof on a non-BRAIN PR).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A required status check whose workflow is skipped by a paths filter never runs — and GitHub leaves that check Pending forever. Pending blocks merging on every PR the check protects, including PRs the filter was meant to exclude. The paths filter was a cost optimization; marking the check REQUIRED turns it into a merge blocker for the whole team. NEVER mark a paths-filtered workflow's check REQUIRED in branch protection. The correct design: the required workflow triggers on all PRs with an unconditional named job, and the job itself decides the verdict inside — PASS for clean, FAIL for drift, cheap success/NOT_APPLICABLE for irrelevant paths. A required check must always be able to produce a verdict; a filter that prevents the verdict is a blocker, not an optimization.

## 🩷 HUMAN NOTE

The team built a brain-index freshness gate to run only on PRs touching `BRAIN/**` — a sensible cost optimization via a top-level `pull_request.paths` filter. The docs then asked Shawn to mark that check REQUIRED in branch protection. A cross-lane review caught the combination before his click: GitHub's documented behavior is that a required check skipped by a paths-filtered workflow stays Pending forever, and Pending blocks merging — on every PR, including the non-BRAIN PRs the filter was supposed to leave alone. One person's cost optimization would have become a twenty-team merge freeze the moment the switch flipped. The prescribed repair: run the required workflow on all PRs with an unconditional named job; inside the job, do the cheap full check or exit success as NOT_APPLICABLE on irrelevant paths — and prove it with a negative control (non-BRAIN PR resolves the check) plus the enforcement controls (BRAIN clean PASS, BRAIN drift FAIL, unknown fail-closed). NEVER ask for the branch-protection click until the required workflow can produce a verdict on every PR it protects.

## 👶 CHILD NOTE

Imagine the rule is "every package needs a green sticker before it ships," but the sticker machine only turns on for blue boxes. Every red box sits on the belt forever — no sticker, no ship, the whole factory stopped. That's what a REQUIRED check plus a skip-some-PRs filter does: GitHub waits forever for a verdict that never comes, and nobody can merge anything. The fix: keep the machine on for every box — it can still just say "not a blue box, you're fine" and let it through.

## 👵 GRANDMA NOTE

They had an inspection that was mandatory before anything could move — but the inspector was told to only visit certain streets. For all the other streets, the paperwork sat on a desk forever: never stamped yes, never stamped no. Nothing on those streets could move again. The lesson the team caught in time: never make a check both mandatory AND easy to skip. If it must pass, it must run every single time — even if all it does is look at the empty street and say "nothing to inspect here."

## 🤖 NAYA NOTE

NEVER mark a paths-filtered workflow's check REQUIRED in branch protection. The mechanism is documented GitHub behavior, not opinion: a required check whose workflow is skipped by a top-level `pull_request.paths` (or any path/branch filter that can exclude the PR) stays Pending indefinitely, and Pending blocks merging on every PR the check protects — including the PRs the filter excludes. This was caught on PR #2385 before Shawn's branch-protection click (board comment 6113970213), which is exactly the no-bottleneck doctrine working as designed: one seat's five-minute cross-lane review prevented a twenty-team stall, and the owner was told to repair on the same branch — no parallel builder, no duplicate mechanism. The design rule: a REQUIRED check must be executable on every PR it protects. Run the workflow on all `pull_request` events with an unconditional named job; the job body decides PASS / FAIL / NOT_APPLICABLE inside (cheap full check or instant success for irrelevant paths). Prove it three ways: negative control (non-BRAIN PR resolves the check — no stuck Pending), positive controls (BRAIN clean PASS, BRAIN drift FAIL), unknown fail-closed. Exact check name matters — the required name must match the job's name unconditionally. When you design a merge gate, check the failure mode first: what happens when this gate does NOT run? If the answer is "stuck Pending forever," the gate design is wrong, no matter how clever the filter.

## ⚙️ MACHINE NOTE

{
  "sn_id": "SN-1014",
  "intelligent_block": "IB-SMART-NOTE-20261011-sn1014-required-check-paths-filter-stuck-pending",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "sub": "SYSTEM-DESIGN/GATE-DESIGN",
  "evidence": [
    {"type": "board_comment", "ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6113970213", "finding": "P0 URGENT: PR #2385's workflow skips all non-BRAIN/** PRs via top-level pull_request.paths while docs ask Shawn to mark brain-index-freshness REQUIRED; repair prescribed on the same branch (all-PR workflow, unconditional named job, cheap inside-job verdict, negative-control proof); DO NOT ask Shawn to turn it on yet"},
    {"type": "doc", "ref": "https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks#handling-skipped-but-required-checks", "finding": "GitHub documents that a required check skipped by a paths-filtered workflow stays Pending and blocks merging"},
    {"type": "live_ref", "ref": "main tip f33bba344a34e9e91b4b5bb6802c22f6eade3145", "finding": "audit tip at capture; re-resolve before editing (decision expires when the tip moves)"},
    {"type": "doctrine", "ref": "SN-0626 / Law-E08 (no-bottleneck law)", "finding": "first concrete application reported in the new director teaching: act on the actual cross-team bottleneck; qualified cross-lane help supplies falsifier, not a duplicate writer"}
  ],
  "rule": "NEVER mark a paths-filtered workflow's check REQUIRED in branch protection. A REQUIRED check must be executable on every PR it protects: trigger the workflow on all pull_request events with an unconditional named job, and let the job body produce the verdict inside (PASS / FAIL / NOT_APPLICABLE). Prove the design with a negative control (irrelevant-path PR resolves the check, never stuck Pending) plus enforcement controls (clean PASS, drift FAIL, unknown fail-closed). When designing a merge gate, evaluate the non-run failure mode first: if a skipped gate means stuck-Pending-forever, the design is wrong regardless of the filter's cost savings.",
  "relates_to": ["SN-0626 / Law-E08 (no-bottleneck doctrine — the review that caught this)", "PR #2385 (the flawed gate design)", "PR #2388 (Brain-Index Freshness Law — the law this gate enforces)", "SN-1009 (scope discipline in evidence claims — adjacent gate-design discipline)"],
  "carrier": {"branch": "naya4/smart-notes-2026-09-30", "pr": "#1825", "merge": "NEVER", "ratification": "Shawn only"}
}
