# MISSION STATE — NayaPOWER Live Operations
**This file is the single current truth. Updated by the Director every 15 minutes.**
**Workers: fetch this branch, read this file, know exactly where to go.**

> Activate → Tune in → Read this → Execute.

---

## PASS NOTE (2026-10-10 16:31Z)
- Cheap check first: `git ls-remote` → tip `2ff26818` — UNCHANGED since the 16:16Z pass (== live ref). No new merges, no priority changes, no lane-movement signal. Quiet pass: timestamp updated, nothing changed, EXIT per budget protocol. No board scan (unchanged tip, no flagged priorities).
- Standing items carry forward: relay acks batched for next relay run; PR #2145 posted (WHAT-IT-MEANS-TO-BE-NAYA.md); #2136 merge-click priority (unblocks WS-9 + WS-4) still awaiting the merge lane.

---

## PASS NOTE (2026-10-10 16:16Z)
- Cheap check first: `git ls-remote` → tip `2ff26818` — UNCHANGED since the 16:15Z battery (== live ref). No new merges, no priority changes, no lane-movement signal. Quiet pass: timestamp updated, nothing changed, EXIT per budget protocol. No board scan (unchanged tip, no flagged priorities).
- Standing items from the 16:02Z pass carry forward: relay acks batched for next relay run; PR #2145 posted (WHAT-IT-MEANS-TO-BE-NAYA.md); #2136 merge-click priority (unblocks WS-9 + WS-4) still awaiting the merge lane.

---

## PASS NOTE (2026-10-10 16:02Z)
- GitHub REST rate limit **CLEARED** (was 403 since 15:28Z; confirmed clear at ~16:02Z — ref, issue, comments, and PR reads all succeed). Relay's drafted batched acks (16 comments + 15:23–15:30Z window) can go on the next relay run.
- **Main tip UNCHANGED:** `7281ede6` (live ref, == 15:32Z battery tip). No new merges since the last pass.
- New since the 15:47Z watermark (6099091488) — 4 comments:
  - WS-9 UNBLOCKED: second consumer + independent scorer receipt posted for Smart App v1.0.0 (PR #2132). Merge on hold for CI (`mergeable_state: unstable`).
  - WS-4 BLOCKED: PR #2141 (waste meter) held by the same pre-existing `protocol-gates.yml` red class — covered by PR #2136's fix. Same merge disposition, no new repair.
  - Naya 5 relayed Shawn's second-template-run execution prompt (already the authoritative flow in this file).
  - Naya 5 prod-readiness achievement: health-check survives network outages; dead-branch janitor built.
- PR states live-checked this pass: #2136 open/clean (still awaiting merge lane — now unblocks BOTH WS-9 and WS-4; prioritize the single merge click); #2143 open/unstable; #2132 open/unstable.
- No new lessons for the DOS list (no mistake+fix reported since the protocol-gates workflow lesson).
- No priority changes. No NEEDS-REWRITE flags. Routine refresh — nothing for Shawn.

---

## PENDING (director's desk — rate limit CLEARED 16:02Z, safe to move)
- Relay ack for 16 board comments (Naya 4's WS-1/WS-2/WS-7 done, EVOLVE 6.2, KNOW 9.4→9.0, PROVE 10→9.0, integrity sweep 27/27) drafted at `hidden_files/relay-20261010-1525.md` — post on next relay run.
- WS-9 red resolved: `protocol-gates.yml` missing `pip install pytest` — PR #2136 (one-line fix, CI-proven red→green, `mergeable_state: clean`) open, awaiting the merge lane. Now unblocks WS-4's PR #2141 too (same red class) — single merge click heals both lanes. Prioritize this click.
- Relay ack for the 15:23–15:30Z board window (WS-9 unblock, WS-2 scorecard, integrity sweep, template run) — include in the same batched post.
- **WHAT-IT-MEANS-TO-BE-NAYA.md** (the worker standard): POSTED as PR #2145 (2026-10-10 16:10Z) — https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2145

## TIP NOTE (freshest verified truth, 2026-10-10 ~16:15Z battery)
- Main tip: `2ff26818` — merged PR #2144 (brain-build index re-stamp at 7281ede6). Moved after the 16:02Z director pass. Verified HEAD == live ref (worktree byte-checked at fetch).
- pytest @2ff26818: **2285 passed / 11 skipped / 2 xfailed — GREEN** (root, no exclusions, disk-isolated).
- Brain index `--check` @2ff26818: **OK — index layer matches git tree (1241 files).** The #2142 drift is healed by the #2144 re-stamp; re-verify showed no repair needed beyond the landed merge.
- Adversarial harness @2ff26818: **6/6 PASS** (tip-current copy, disk-repointed scratch; generator symlink verified byte-identical).

## MASTER LOOP — SECOND TEMPLATE RUN (relayed 2026-10-10 15:30Z, authoritative seat assignments)
**P1 FLOW:** Naya 4 fixes #2062 red tests then merges · Naya 5 rebases connect→learn→evolve (main's ts_bridge wins) · Naya 1 validates #2102/#2103/#2104 (learning moves on her stamp only) · Naya 5 rewires 12 worker briefs.
**P2 PROOF:** experiment proposal → Shawn's review with triple-yes checkpoints · NAYA 1 writes Learning 6.0 bar.
**P3 HYGIENE:** Naya 4 "main's red vanish test" (emergency) · 7-day branch claim window live — **2026-10-17, then close unclaimed** · Naya 5 merges #2143 when green.
**Parked:** 4 rows, RLS — Shawn's word only.
**Gates hold:** full suite green at exact head, honest scorecard, different-seat validation, #1354 with no objection.

## NORTH STAR
Maximum verified human value per action. The system learns from experience and gets better at getting better. Nothing below 9/10 ships. Shawn's attention is priced at zero — the math decides, he only gets genuine human gates.

## CURRENT PRIORITIES (ranked)
1. **Security audit** — 4 learning records may lack proper permission. Audit, quarantine if needed. Touch nothing in production. (Naya 2)
2. **Learning loop** — sandbox driver design, then CONNECT/EVOLE/DISTILL/COMPOUND with proofs. Close the loop. (Team)
3. **Search relevance** — knowledge retrieval returning wrong results 40/43 in one test. Rebuild the selector. (Naya 2 + Naya 5)
4. **Re-prove learning** — independently redo the 14/14 trial with fresh eyes. (Naya 2)
5. **Drift root fix** — registry-drift break class has bitten 3 times. Kill it permanently. (Team)
6. **Production parity** — product is 60+ hours behind the brain. Refresh the packet for Shawn's clicks. (Naya 2)
7. **#2097 rework** — convert to tests-only now that #2092 merged. (Team)
8. **#2086 experiment** — cold-Naya + independent-judge experiment before it counts as proven. (Owner's lane)
9. **Machine file pinning** — 0008-operating-code-v2.machine.json under the ratified envelope. (First to claim)
10. **Board rescore** — honest 10/10 rescore against current evidence. (Naya 2)

## HUMAN GATES (Shawn only — never touch)
- Production deploys, dispatches, DB reads/writes/migrations
- `.github/workflows/` files
- Constitutional/EVOLVE ratification
- Credentials, money
- Destructive/irreversible actions

## DOS AND DON'TS (from real mistakes — read before every shift)
- **DO** verify temporal claims against `created_at` timestamps before publishing corrections. (L204)
- **DO** read the live ref immediately before every merge PUT. Never merge on cached SHAs. (L205)
- **DO** rebase before regenerating when drift is branch-vs-main. (L206)
- **DO** prove agency with timestamp chains when contested. (L207)
- **DO NOT** claim "done" without verifying the actual result. Check the real state.
- **DO NOT** trust a subordinate's summary — re-read the source.
- **DO NOT** run the adversarial harness concurrently with pytest (tmpfs corruption).
- **DO NOT** merge on still-running checks. Pending is not green.
- **DO NOT** rename symptoms — fix the actual defect class.
- **DO** verify a CI red's step log before blaming the tests — the "Protocol machine law" red (2026-10-10) was a workflow defect (`python -m pytest` with no `pip install pytest`), diagnosed three times before PR #2136 fixed it. The workflow can be the bug.
- **DO** close a superseded repair PR instead of merging it — W1 closed #2135 because tip had already healed; merging would have regressed the index.
- **DO** use `git ls-remote origin refs/heads/main` for the live-tip check when the REST API is rate-limited (2026-10-10 15:47Z) — the 403 only blocks REST, not the git protocol. A rate limit is not a dead pass.

## SHIFT SCORES (16:02Z)
- **16:02Z pass:** quiet check — tip unchanged at `7281ede6` (live ref); REST rate limit cleared; 4 new board comments since watermark (all read live). No lane idle 3+ shifts. No NEEDS-REWRITE flags. Nothing for Shawn.
- **15:47Z pass (carried):** REST 403 rate-limited (since 15:28Z); tip verified unchanged via git protocol (`git ls-remote`). No new lane movement observable (no board access).
- **15:36Z snapshot (carried):**
- **WS-1 (Naya 4):** REAL MOVEMENT — drift healed at tip, #2135 closed as superseded, #2136 fix PR CI-proven. (16:02Z: #2136 still open/clean, awaiting the merge click — now also heals WS-4.)
- **WS-2 (Naya 4):** REAL MOVEMENT — V2 Compile the Law phase 1 done, PR #2134 open; blocked on protocol red + independent score. (16:02Z: #2136's merge will clear the protocol-red leg.)
- **WS-4 (Naya 4):** BLOCKED — PR #2141 (waste meter) held by the same `protocol-gates.yml` red class (new this window, comment 6099104953); covered by PR #2136, no separate repair. Not a NEW defect class.
- **WS-9 (Naya 4):** REAL MOVEMENT — second consumer + independent scorer receipt posted for PR #2132 (comment 6099106010); unblocked, awaiting CI.
- **Integrity sweep:** REAL MOVEMENT — 27 merge commits verified, 26 exact tree matches, 9.5/10.
- **Brain-build loop:** REAL MOVEMENT — pytest green 2269/11/2xfail, drift OK at tip, adversarial 6/6; nothing pending.
- **Naya 5 prod-readiness lane:** REAL MOVEMENT — health-check proven through network outages; dead-branch janitor built (comment 6099433211).
- **Nothing idle 3+ shifts. No NEEDS-REWRITE flags.**

## TUNE-IN (every shift, before acting)
**Canonical:** `BRAIN/01-GOVERNANCE/THE-TUNE-IN-TEMPLATE.md` on main (PR #2142).
Every worker answers all ten questions in writing, by itself, before touching anything. Answer your own questions — check evidence, do the math, read the source. Then execute. Then report. The template evolves; the discipline doesn't.

## STANDING DIRECTIVES
- Continue nonstop. Assess → repair → re-score → next. Never idle.
- Shawn-language law: plain words, no jargon, Intelligent Block structure for all Shawn-facing output.
- No repetitive reports. One fresh full report beats ten stale ones.
- Scorecard Law: no merge without a posted receipt. No receipt, no merge.
- Evidence law: UNKNOWN ≠ PASS, IMPLEMENTED ≠ VERIFIED, VERIFIED ≠ PRODUCTION-PROVEN.
