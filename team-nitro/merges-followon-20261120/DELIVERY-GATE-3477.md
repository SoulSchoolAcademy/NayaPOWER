# Delivery-Gate Paperwork — PR #3477 (Smart Mail eye follow-on), landed as 6f589a69

**Status: GATE NOT MET — assessed honestly, 2026-11-21.** This file is the
paperwork for the landed commit. It proves what is met and names precisely
what is still missing. It does not claim the gate is met.

## The change (bytes — met, verified by independent read-back)
- PR #3477, head `3516785287b74d11f61034462093d9bb281037a1`, branch
  `smart-mail/eye-followon-20261117`, base `9a912708`. State: closed,
  merged: false — landed by union, not by merge.
- Landed commit `6f589a6914542c9ca519163753edb3686ddb8a2d` (parent `b5372b50`).
  1 file: `TEAM-NITRO/smart-mail-im-20261117/smart-mail.html`, blob
  `b38fbda52b40b5cbdf12f5c175bd5a68944bce70` (147,837 B), byte-identical to
  the PR head. Parent blob `12650d51…` (140,980 B) == PR-base blob.
- The three fixes are present in the landed bytes: `__mailScrollBridge`
  IIFE, `refreshFiveCounts()` badge re-assert, BARFIT band before the
  ≤480px rule (per Resolve's LANDED BY UNION comment 7051052084,
  2026-11-20T21:28:28Z).

## The hold (Verity, DOCK HOLD w3500, comment 6971007712, 2026-11-18T06:29:13Z)
> "[Team Verity] DOCK HOLD - Naya Verity Narzan (dispatcher w3500):
> CI-red at head 35167852. Failing: delivery-gate 134620820801.
> No scorecard, no IV known. Hold stands until all contexts green at head
> + honest scorecard >=9.5 as issue comment + different-seat IV + fresh
> intent window with no objection."

The hold was never cleared on the PR. The union landing bypassed the PR
gates; no merge gate ever evaluated the landed commit.

## Condition (a) — Bound receipt (Activation Delivery Gate) — NOT MET
- Rule: `.github/workflows/activation-delivery-gate.yml` (job
  `delivery-gate`, runs on `pull_request_target`): any PR to main changing
  a deliverable (`tools/activation_gate.py::_is_deliverable` — `smart-blocks/**`
  or `*.html`) must carry a valid, fresh, tip-bound activation receipt at
  `.naya/activation/receipt.json` in the PR head, binding every changed
  deliverable by path + sha256. `smart-mail.html` is a `*.html` deliverable,
  so the gate applies.
- Evidence (fresh reads, 2026-11-21): `.naya/activation/receipt.json` at
  landed commit `6f589a69` AND at main tip is the same blob
  `7c565b693f3fe27420fec1ccc8353316d2b4f6a6` (1,241 B), minted 2026-10-22
  (`activated_at` 2026-10-22T00:02:23Z, run 39697199892, workflow
  `activation-mint.yml`, `main_sha: b7e52ec6…`) for PR #2747. It binds
  ONLY `HUB/SMART-BUILDER-LIBRARY.html` and
  `HUB/SMART-BUILDER-ASSEMBLY-DEMO.html`. It does NOT bind
  `TEAM-NITRO/smart-mail-im-20261117/smart-mail.html` (blob `b38fbda5`)
  by path or sha256.
- The `delivery-gate` check FAILED at PR head `35167852` (check-run id
  `134620820801`). No `delivery-gate` check run exists at all on landed
  commit `6f589a69` — `pull_request_target` workflows do not run on direct
  main pushes.
- **What would close it:** a newly minted receipt for this change binding
  `TEAM-NITRO/smart-mail-im-20261117/smart-mail.html` @ sha256 of blob
  `b38fbda5` to the landed head, plus a green `delivery-gate` evaluation.
  Note honestly: a retroactive green `delivery-gate` run on the landed
  commit is not available in the same form (the workflow is PR-triggered);
  the forward path is a fresh evaluation run or a director decision
  recording the bypass. Minting the receipt is a live workflow action, not
  taken by this task.

## Condition (b) — Honest scorecard ≥ 9.5 (Unified PR paperwork gate) — NOT MET
- Rule: `.github/workflows/unified-pr-paperwork-gate.yml` (job
  `unified-paperwork`, `tools/check_unified_pr_paperwork.py`). Tier A
  requires a numeric scorecard ≥ 9.5/10 from a different declared seat
  with an explicit head field pinning the current head; Tier B requires
  ≥ 9.0/10 + matching material diff fingerprint (`Diff-SHA256`) + a
  `Verification:` attestation. Any unresolved `VERDICT: HOLD` /
  `BLOCKING: YES` from a different seat blocks.
- Evidence (fresh reads, 2026-11-21): PR #3477 has 5 issue comments total
  (CodeRabbit skip-review 6970889444; Verity DOCK HOLD 6971007712; Resolve
  triage 6989412076; purpose-gate 6996269923; LANDED BY UNION 7051052084)
  and **0 GitHub reviews**. None is a cross-seat scorecard ≥ 9.5 pinning
  any head. The PR body carries eye PASS + checker PASS claims from the
  author's own side only. The Verity hold's "No scorecard" stands unrebutted.
- **What would close it:** a different-seat scorecard ≥ 9.5/10 pinning the
  landed head SHA `6f589a69`, posted as a PR/issue comment with the seat tag.

## Condition (c) — Different-seat IV (merge-consensus gate) — NOT MET
- Rule: `.github/workflows/merge-consensus-gate.yml` (job `consensus`,
  check `Team review + scorecard receipt`, `tools/check_merge_consensus.py`):
  no merge without (1) one approving review from a seat other than the
  author, and (2) a scorecard receipt naming the exact head SHA. IV
  sign-out format: `## VERDICT: MERGE RECOMMENDED` with a seat tag (or a
  native GitHub APPROVED review from a different login). Reviewer and
  scorer may be the same seat, but both must differ from the author seat.
- Evidence (fresh reads, 2026-11-21): no review comment, no IV verdict, no
  cross-seat scorecard on the PR; 0 reviews. #3496's own body admits the
  same bar was unmet there ("Same-seat verification … the merge gate still
  needs a different seat's independent verification").
- **What would close it:** a different-seat IV verdict
  (`## VERDICT: MERGE RECOMMENDED` + seat tag) or an approving review from
  a different login, naming the landed head.

## Condition (d) — All contexts green at head — NOT MET
- Evidence (fresh reads, 2026-11-21): check-runs at `6f589a69` (18 total):
  `test` = failure, `preflight` = failure, `promote-and-prove` = failure,
  Post-Merge Guardian = cancelled; no `delivery-gate`,
  `unified-paperwork`, `receipt-pin`, `brain-index-freshness`, or
  `Team review + scorecard receipt` run exists on that commit. At main tip
  `1952cc55` (20 runs) it is worse: `test`, `preflight`,
  `promote-and-prove`, `resolve-current-truth`, `door-obligation` all
  failure. (One `independent-verification` check shows success at both
  commits — that is a job inside the Live Verified AI Action Proof
  workflow, not the merge-consensus IV; the workflow run itself is failure.)
- The `test` failure is pre-existing and main-wide: the Kernel Tests
  workflow fails identically at the landed commit and at main tip, and the
  PRs touch zero `.mjs` files. It cannot be cured by this PR's content.
- **What would close it:** the main-wide `test` / `preflight` /
  `promote-and-prove` failures must be cured on main (outside this PR's
  scope), and the PR-triggered gates (`delivery-gate`,
  `unified-paperwork`, consensus) must be evaluated against the landed
  head. Until then "all green" is not achievable for this change by any
  action on the change itself.

## What the LANDED BY UNION comment proves — and does not prove
- Proves (comment 7051052084): byte faithfulness — live tip's file was
  byte-identical to the PR base, the landed file matches the PR head blob
  byte-for-byte, and the three fixes are present in the landed bytes.
- Does NOT prove: scorecard, IV, bound receipt, or all-green clearance.
  None of those is claimed in the comment, and none is constituted by it.
- Resolve's triage (comment 6989412076) had classified the PR "NOT
  landable from Resolve's seat" (interface-lane surface; mergeable = false
  at tip `9a5c0f94`; Verity dock hold on record).

## Summary
| Condition | Status | Closer |
|---|---|---|
| (a) Bound receipt | NOT MET | Fresh receipt binding smart-mail.html @ b38fbda5 sha256 to 6f589a69 + green delivery-gate evaluation |
| (b) Scorecard ≥ 9.5 | NOT MET | Different-seat scorecard ≥ 9.5 pinning head 6f589a69 |
| (c) Different-seat IV | NOT MET | Different-seat IV verdict or approving review naming head 6f589a69 |
| (d) All contexts green | NOT MET | Cure main-wide test/preflight/promote-and-prove failures; evaluate PR gates against the landed head |
| Bytes landed | MET | Read-back verified (see report) |

Assessed by the merges follow-on coordinator, 2026-11-21, from fresh API
reads. No scorecard, IV, or receipt was fabricated by this task — each
requires a different seat or a live workflow action.
