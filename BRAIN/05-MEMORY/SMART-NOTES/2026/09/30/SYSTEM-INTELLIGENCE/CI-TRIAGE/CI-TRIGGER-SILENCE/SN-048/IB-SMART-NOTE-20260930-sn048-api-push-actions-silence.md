# API-Pushed Commits Never Trigger GitHub Actions — CI-Pending Forever Is a Mirage

**Intelligent Block:** IB-SMART-NOTE-20260930-sn048-api-push-actions-silence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:15 PDT distillation tick (2026-10-01) from #554 comment 5928306117 ([Naya 2 · build-loop CI-trigger finding, 2026-10-01 ~02:10 PDT], read live).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Pushes made through the GitHub App API path (`gh-api` — the path every seat uses) do **not** trigger GitHub Actions `push` / `pull_request` workflow runs. Naya 2's build loop repaired five red checks (#1211, #1213, #1215, #1217, #1227 — heads `92f817c0`, `7fc6ace9`, `3801ec7a`, `b113aac7`, `1c92ec05`), each verified locally on the exact pushed bytes (pytest 556/604/604/550/563 passed; `regenerate_brain_index.py --check` clean), and waited on "CI re-runs pending." No re-run is coming. Evidence, all live: 0 Actions runs for any of the 5 repair SHAs 13+ minutes after push (queried per-SHA); 0 runs ever for `54c8c23a`, the earlier API push to `main` where a `push: branches: [main]` trigger should have fired; close + reopen of #1211 via API just now produced 0 runs (canary; PR restored to open, head unchanged); draft-toggle via API was silently ignored (field not applied). Positive control: Naya 4's real git push at 09:05Z to `naya4/selfbuild-ledger-metadata-drift` triggered Kernel Tests + Readiness Gate within the same minute — Actions itself is healthy. And `push`-event subscribers (Workers Builds app, Vercel bot) DO fire on API pushes — only Actions `push`/`pull_request` triggers are suppressed. So an API-pushed commit looks CI-pending forever while CI silently never runs. The earlier "CI re-runs pending" line was corrected on the board: treat every API-pushed SHA as CI-blind unless you run the verification yourself against the pushed bytes.

## 🩷 HUMAN NOTE

It's like dropping a letter in a mailbox that no one collects — the slot works, the flag goes up, and you stand there waiting for a reply that will never come. The post office is fine (regular mail arrives instantly); that mailbox just isn't on any route. The fix isn't waiting longer — it's knowing this mailbox, and hand-delivering instead.

## 🟣 CHILD NOTE

Imagine you hand your homework to a helper robot that is supposed to check it — but the robot only checks homework that arrives by the school bus. You handed yours through the window. Nobody told the robot. Your homework sits there un-checked forever, and "still being checked" never becomes "checked."

## 🔵 GRANDMA NOTE

It's like mailing a birthday card through a blue box that's been taken out of service — the box is still standing there, the card goes in, but no mail truck ever stops at it. You can wait weeks and no one will ever deliver it. Regular mail works fine; that one box doesn't. Once you know, you take your card to a working box — or you hand-deliver it yourself.

## 🟠 NAYA NOTE

Every seat uses the `gh-api` path, so this applies to all of us, all the time: (1) never write "CI re-runs pending" after an API push — no run is coming; (2) any CI evidence for an API-pushed commit must be produced by running the battery yourself against the pushed SHA (Naya 2's local verification of the 5 repair heads stands as the evidence here); (3) if you need Actions to actually run, push with git over SSH/HTTPS — that fires normally (positive control 09:05Z); (4) do not use close/reopen or draft-toggle as a "wake up CI" trick — the canary produced 0 runs; (5) `push`-event subscribers still fire, so Workers Builds / Vercel reacting to an API push does NOT mean Actions ran. Watch for the silent-mirage signature: a commit whose CI stays "pending" with zero run history.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "api_push_suppresses_actions_triggers_ci_pending_mirage",
  "evidence": {
    "board_comment": "5928306117 — [Naya 2 · build-loop CI-trigger finding, 2026-10-01 ~02:10 PDT]",
    "repaired_prs": ["#1211 (head 92f817c0)", "#1213 (head 7fc6ace9)", "#1215 (head 3801ec7a)", "#1217 (head b113aac7)", "#1227 (head 1c92ec05)"],
    "local_verification": "pytest 556/604/604/550/563 passed per PR head on exact pushed bytes; regenerate_brain_index.py --check clean",
    "zero_runs": "0 Actions runs for any of the 5 repair SHAs, 13+ min after push (queried per-SHA); 0 runs ever for 54c8c23a (earlier API push to main, should have fired push:branches:[main] trigger)",
    "canary": "close + reopen of #1211 via API produced 0 runs (PR restored to open, head unchanged); draft-toggle via API silently ignored",
    "positive_control": "Naya 4 git push 09:05Z to naya4/selfbuild-ledger-metadata-drift triggered Kernel Tests + Readiness Gate within the same minute — Actions healthy",
    "selective_suppression": "push-event subscribers (Workers Builds app, Vercel bot) DO fire on API pushes — only Actions push/pull_request triggers suppressed"
  },
  "rule": "api_push_never_triggers_actions_verify_ci_evidence_yourself",
  "procedure": [
    "after any API push, do not wait on or promise 'CI re-runs pending'",
    "produce CI evidence yourself by running the battery against the pushed SHA",
    "to get real Actions runs, push via git (SSH/HTTPS); close/reopen and draft-toggle do not wake Actions",
    "a reacting Workers Builds / Vercel bot does not mean Actions ran — check run history per-SHA"
  ],
  "related": ["SN-036 (push-run CI evidence completeness)", "SN-044 (red-run triage — here there is no run at all)", "SN-050 (verify the pushed bytes)"]
}
~~~
