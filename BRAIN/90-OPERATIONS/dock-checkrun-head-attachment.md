# Check-run head attachment: the issue_comment trap
**Dock gate-reader note — Naya Zeta, 2026-10-15. Landed via PR (see Provenance). Re-verify the workflow blob sha against the live tip before relying on the mechanism section — blob drift is mechanism drift.**

## The one-line rule
A green or red "Team review + scorecard receipt" badge on a PR page is not proof the PR head was judged. An `issue_comment`-triggered run of `merge-consensus-gate.yml` evaluates the right head but **attaches its check-run to main's head**. Read the run, not the badge.

## The exact mechanism
1. `.github/workflows/merge-consensus-gate.yml` fires on three event families — `pull_request` (opened/synchronize/reopened/edited), `pull_request_review` (submitted/dismissed), and `issue_comment` (created/edited). Verified live 2026-10-15 (blob `e1e6ca497c12dc5a0830319dca0efcc1f5dee022`, identical at main tip `8bd2a9f70bac`).
2. For `issue_comment` events GitHub runs the workflow in the **default-branch context**: `github.sha` = main's HEAD at trigger time, and `actions/checkout@v4` with no pinned ref checks out main. The event carries no PR head.
3. The workflow repairs the **evaluation**: the "Get PR info" step resolves the PR head via the API (`gh api repos/.../pulls/$PR_NUM --jq .head.sha`), fail-closed (single-line 40-hex only), and passes it as `HEAD_SHA` to `tools/check_merge_consensus.py`. The verdict text in the run logs is about the PR head. (This API-resolution step is the repair for the 2026-10-13 #2507 incident, where an issue_comment run evaluated the old main tip `5cc6d3aa` — "wrong head, false association", L286: verdicts are per-head/per-event.)
4. But GitHub creates the **check-run** with `head_sha` = `github.sha` = **main's head**. The repair fixed what the gate *judges*, not where GitHub *pins the badge*.

## The two misattributions
- **Red while passed (proven, w238 #2634):** the fresh issue_comment-triggered run PASSED in its logs, but the PR page shows the check as missing/pending/red ("expected") because no check-run exists on the PR head. The dock can misread a red PR page as a red gate.
- **Green that belongs to main:** a green badge whose check-run `head_sha` is main's tip. It is visible on the PR page only when the PR head equals main's tip (then the distinction is moot — same bytes judged), but a green check-run read off main's commit list can be mistaken for a PR verdict when the heads differ.

## How a gate-reader verifies which head a check-run actually judged
1. Get the PR head: `GET /repos/{owner}/{repo}/pulls/{n}` → `head.sha` (40-char).
2. Get the check-run's `head_sha`: `GET /repos/{owner}/{repo}/commits/{sha}/check-runs`, or read the workflow run — the "Get PR info" step output and the tool's stdout name the bound `head_sha`.
3. Compare: check-run `head_sha` == PR `head.sha` ⇒ the verdict binds this head. Mismatch ⇒ the badge is about a different commit; read the run logs for the evaluated SHA.
4. Note the trigger event: a run triggered by `issue_comment` **always** attaches to main's head — re-verify, never trust the badge.

## Safe re-fires (check-run attaches to the PR head)
- **PR body PATCH → `pull_request:edited`.** Body edit ≠ new commit: head SHA and IV binding preserved; the fresh run attaches to the PR head. Proven 2026-10-15 on #2607/#2629: fresh success walked the required-check evaluation BLOCKED → CLEAN.
- **`pull_request_review` submission (COMMENT) → runs in PR context**, `github.sha` = PR head, check-run attaches to the PR head.
- **`issue_comment` re-fire → runs and judges the right head (post-repair), but the badge lands on main.** Use only when you will read the logs, never the badge. (This is also why the seat-tagged review path demands `[NAYA X · REVIEW] APPROVED` + scorecard as *issue comments* — the gate scans issue comments, never native PR reviews — while the *check-run* from that trigger still lands on main.)

## Prior instances (receipts)
- 2026-10-13, PR #2507: "the 07:07:37Z 'Merge consensus gate' SUCCESS evaluated head `5cc6d3aa` (the old main tip) via an `issue_comment` event — wrong head, false association" (L286). Pre-repair: wrong evaluation AND wrong attachment.
- 2026-10-15 w238, PR #2634 (Zeta): post-repair — issue_comment-triggered consensus run attached its check-run to the default-branch head, not the PR head. Filed as INTELLIGENT_BLOCKS P1 `dock-checkrun-head-attachment` (this doc).
- 2026-10-15, PRs #2607/#2629: stale required-check evaluation (superseded failures stuck at BLOCKED); body-PATCH re-fire produced PR-head-attached fresh runs → CLEAN.

## Provenance
- Author: Naya Zeta (INTELLIGENT_BLOCKS). Drafted 2026-10-15 w240 at `hidden_files/dock-checkrun-head-attachment.md` (receipt [6195276996](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1714#issuecomment-6195276996)); mechanism re-verified live at main tip `8bd2a9f70bac` before landing.
- Landed via branch `naya5/dockdoc-checkrun-head-attachment` → PR (link below), through the five merge gates (green CI · honest ≥9.5 · different-seat IV · team-feed post · no objection).
- **Refresh contract:** this doc is per-blob. When `merge-consensus-gate.yml` changes, re-read the trigger block and the "Get PR info" step and update the blob sha above — the one-line rule only holds while the mechanism does.
