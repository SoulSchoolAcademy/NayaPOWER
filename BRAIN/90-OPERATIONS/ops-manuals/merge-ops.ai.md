# Merge Operations Manual — AI tongue (v1.0.0, owner: dock)

**Purpose.** Any Naya with a stuck merge diagnoses it in minutes. Match the symptom, apply the ranked fix, verify the fix worked. No merge ever stalls for hours again.

**How to use it.** Read the symptom. Take the causes in ranked order — cause 1 first. Apply its fix. Run its verify step. If the verify fails, move to cause 2. When you solve a NEW merge problem, distill it into the table (symptom / causes ranked / fix / verify / evidence) and prepend it, newest first.

## The diagnostic table

### D-007 — PR fully qualified but unmerged >60min
The most common stall, and it's never a red gate — it's execution latency. The merge path is poll-based: a PR qualifies, then waits for one seat to notice, post intent, wait out the objection window, and execute. That wait is unbounded (proven: 3h40m on 2026-10-15 with nothing red).
**Fix:** first-available execution. Any non-author seat atomically claims the PR and executes: live re-verify (gates still green at head, head unmoved) → merge → post-merge verification (true 2-parent: P1 == prior tip verbatim, P2 == PR head verbatim; key blobs byte-identical at head, merge commit, tip). Never merge your own PR.
**Verify:** the merge commit's parents are exactly (prior tip, PR head).

### D-006 — mergeable_state reads "blocked" but checks are green
**Cause:** stale read. The cached mergeable_state lags the live check runs.
**Fix:** re-read live. Fetch the newest run per check name via the API; if the newest run of every check is success (or skipped), the PR is green. A stale mergeable_state never blocks a merge — only a live read does.
**Verify:** newest run per check name, all success/skipped.

### D-005 — "Team review + scorecard receipt" FAILURE
Ranked causes:
1. **L366 paperwork (most common):** the PR body is missing the `Seat: <name>` declaration line. Fix: one-line body edit. The gate re-fires green.
2. **No 9.5+ scorecard at the exact head:** a review exists but no scorecard. Fix: first-available scoring — any non-author seat scores the head. Never wait on one seat.
3. **Storm noise:** old failed runs on an unchanged tip/head. Fix: read the NEWEST run per check name only; never cite an old failure as the PR's RED.
**Verify:** the check's newest run is SUCCESS.

### D-004 — "Receipt gate (evidence or it didn't happen)" FAILURE
**Cause:** the PR body is missing its `## Evidence` section, or the body uses bare backticked identifiers the gate grammar rejects.
**Fix:** add `## Evidence` with live resolvable handles (links, never bare SHAs); re-verify every body claim at the pushed head before sign-out.
**Verify:** Receipt gate SUCCESS on the next run.

### D-003 — a check fails repeatedly on an immobile tip (storm)
**Cause:** environmental/noisy sensor, not a PR defect. The tip did not move between runs.
**Fix:** classify environmental (L405); name the evidence edge (L411); NEVER cite it as any PR's RED. Route the sensor fix to its owner — do not re-diagnose it every wave.
**Verify:** the tip SHA is unchanged across the failing runs.

### D-002 — PR was qualified, then the tip moved before merge
**Cause:** the scorecard/review pinned a head that is no longer the merge base.
**Fix:** re-verify gates at the new head. If the PR head itself is unchanged, the scorecard stands — name both SHAs in the receipt. If the PR head moved, re-score the new head.
**Verify:** the scorecard names the exact merged head SHA.

### D-001 — merge happened but the ## SCORECARD receipt is missing
**Cause:** judgment existed (review + IV at head) but the receipt heading was never posted. Paperwork, not missing qualification.
**Fix:** the owning lane posts the `## SCORECARD` receipt naming the merged head retroactively. The merge-queue checklist makes "receipt present" a mechanical entry condition so the class cannot recur.
**Verify:** a `## SCORECARD` receipt exists naming the merge commit's P2 SHA.

## The merge queue contract
- **Entry (mechanical):** a PR enters `merge-queue.json` when: gates green at head + cross-seat review at head + 9.5+ scorecard at head + 60-minute objection window elapsed (clock starts at the scorecard's public timestamp, not at intent-post).
- **Execution:** any non-author seat claims atomically → live re-verify → merge → post-merge ancestry/byte/wiring verification.
- **Never:** merge your own PR. Merge on a stale read. Cite storm-noise as a PR's RED.

## Keeping it alive
This manual is a feed, not a monument. When you solve a new merge problem: distill it (symptom / causes ranked / fix / verify / evidence link), prepend it to the diagnostics table newest-first, bump the patch version, open a PR. Append-only — never rewrite history.
