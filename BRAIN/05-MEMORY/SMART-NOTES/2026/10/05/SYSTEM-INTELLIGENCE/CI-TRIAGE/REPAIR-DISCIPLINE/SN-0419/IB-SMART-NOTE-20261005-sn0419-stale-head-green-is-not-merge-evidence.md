# Stale-Head Green Is Not Merge Evidence — Close Unmerged, Rebuild on Exact Main

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0419-stale-head-green-is-not-merge-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 ~18:26 PDT (2026-10-06T01:26:05Z) — comment 6007421592 ([NAYA][UPDATE] 2026-10-05 — NONSTOP SCORECARD CYCLE); preservation-by-construction seam #1567: draft PR #1572 → closed unmerged → rebuilt as draft PR #1577 on exact current main `6815c6bab06f8b35a9ca1b24018846579788a3c1`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The preservation-by-construction repair for #1567 went through two PRs in one hour:

1. **PR #1572** (from `fix/smart-note-preserving-migration-1567`, head `c2211387...`) — built off an older main. Its first genuine CI RED was a bad regression test (it expected removal to be detected when the preservation helper correctly *prevented* that removal); the test was corrected, and exact CI on the corrected head went fully green: Kernel Tests **750 passed / 11 skipped / 0 failed**, Ratified Guard SUCCESS, Collective Chain SUCCESS.
2. By then **main had moved**, so #1572 was **CLOSED unmerged rather than pretending stale-head proof was current**, and the same narrow seam was rebuilt directly from exact current main as **draft PR #1577** (head `2dd3da02655fc4a972f43fcf2ba60847283b7b0f`), awaiting fresh CI. No merge, no production change.

The durable rule: **a green CI on a stale head is evidence about the past, not a license for the present.** The disciplined sequence on a hot main is: (1) if the branch went stale, its proof is void for merge purposes — do not merge it, do not "rebase and assume green carries over"; (2) close the stale vehicle unmerged rather than keeping a dead branch alive as proof; (3) rebuild the same seam on the exact current main and re-run the gates fresh. Rebasing a green branch onto a moved main and merging without fresh gates is laundering stale proof.

Why this is brain-grade: a cold Naya will see "PR was green, main moved a little, let's just rebase and merge — the code is the same." This note says the green was produced by a different world than the one the merge would land in. The honest move costs an hour of rebuild; the dishonest move costs the meaning of the gate. SN-0415 already covers the *authority* twin of this race (a SHA-pinned deploy authorization is voided by main movement); this note covers the *evidence* twin: proof is bound to the exact head it ran on, and the only cure is re-proof on the current head, not an argument that the diff "didn't change."

## 🩷 HUMAN NOTE

Shawn — the preservation repair had its green moment and we still didn't merge it. PR #1572 went fully green (750 kernel tests, ratified guard, collective chain) — but by then main had moved, so it was closed unmerged instead of being treated as merge evidence. The same narrow seam was rebuilt from the exact current main as PR #1577 and is awaiting fresh CI. The lesson written down: a green CI on a stale head proves the past, not the present — on a hot main, a stale green is never a license to merge. The disciplined move is close-unmerged, rebuild on exact main, re-run the gates. Rebasing a green branch onto a moved main without fresh gates is laundering stale proof. Your authorization-window note (SN-0415) covers the authority side of the same race; this covers the evidence side.

## 🟣 CHILD NOTE

Imagine you got a perfect score on a practice test for Monday's quiz. But over the weekend, the teacher changed the quiz questions. Showing your Monday practice score as proof you'll ace the new quiz doesn't work — the score belongs to the old questions. The right move: take a fresh practice test on the new questions. The team did exactly that: their first attempt went perfectly green, but the "quiz" (the main code) had changed, so they threw out the old score, rebuilt the work on the new version, and started fresh tests. Old proof never transfers to a new world.

## 👵 GRANDMA NOTE

The team built a fix and ran all its tests — everything passed. But while they were testing, the main codebase changed underneath them, so their perfect test results were about an older version. Rather than merging anyway and hoping the results still applied, they deliberately closed that attempt unmerged and rebuilt the same fix on the current version, ready for fresh tests. They wrote down the rule: a passing test only proves the exact version it ran on. When the world moves, you don't argue that the results "probably still count" — you rebuild and re-run. It costs an hour; pretending costs the meaning of the whole testing system.

## 💜 NAYA NOTE

Note to future me: when a PR's head is stale relative to main, its CI status is void for merge purposes — green, red, or otherwise. Do not rebase-and-merge on stale proof; the disciplined sequence is: close the stale vehicle unmerged (a dead branch kept alive as "proof" is a trap), rebuild the seam on the exact current main, re-run every gate fresh. If someone argues "the diff is identical, green carries over," name this note: proof is bound to the head it ran on, and on a hot main heads move. Watch for the subtle version too: a *rebase* onto current main without re-running gates is the same laundering with one extra step. Cite alongside SN-0415 (authorization window race — authority twin of the same hot-main race), SN-0405 (hot-main proof race classification), SN-0395 (regen reads the commit, not the worktree).

## 🖥️ MACHINE NOTE

{"sn": "SN-0419", "title": "Stale-Head Green Is Not Merge Evidence — Close Unmerged, Rebuild on Exact Main", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-DISCIPLINE"], "cousins": ["SN-0415", "SN-0405", "SN-0395"], "evidence": {"board_comment": "#1354 6007421592 ([NAYA][UPDATE] 2026-10-05 — NONSTOP SCORECARD CYCLE, 2026-10-05 ~18:26 PDT)", "pr_stale": "#1572 from fix/smart-note-preserving-migration-1567 head c22113874effea909cf4c48b3638e15fd7fd87f1: first genuine RED was an incorrect regression test (expected removal detection when preservation helper correctly prevented removal); corrected; exact CI on corrected head: Kernel 750 passed/11 skipped/0 failed, Ratified Guard SUCCESS, Collective Chain SUCCESS", "action": "PR #1572 CLOSED unmerged once main had moved — stale-head green explicitly not treated as merge evidence", "pr_rebuild": "draft PR #1577 rebuilt directly from exact current main 6815c6bab06f8b35a9ca1b24018846579788a3c1, awaiting fresh CI; no merge, no production change"}, "rule": "A green CI on a stale head is evidence about the past, not a license for the present. On a hot main: do not merge stale-green, do not rebase-and-assume-green-carries-over. Close the stale vehicle unmerged, rebuild the same seam on the exact current main, re-run every gate fresh. Rebasing onto current main without fresh gates is laundering stale proof."}
