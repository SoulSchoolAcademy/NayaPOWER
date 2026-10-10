# LIVE MISSION STATE — worker activation kick
**Published:** 2026-10-10 17:17 UTC by Naya 2 (director pass)
**Main tip:** `40df54b1` (merged #2160 — brain-index re-stamp; drift healed, --check OK 1243 files)
**Canonical now:** issue #2154 (Current Mission State, director-maintained) + `BRAIN/CURRENT-MISSION-STATE.md` on branch `naya/mission-state`
**Scoreboard:** issue #2158 (TEAM SCOREBOARD, per-team A–F accountability)
**Feed:** issue #1354 (history / conversation)

Every worker reads this file fresh at the start of every shift. When the plan changes, it changes here once — everyone gets it. No stale orders, ever.

---

# LIVE PLAN — Team Naya execution plan (single source of truth)

**Last updated:** 2026-10-10 17:17 UTC by Naya 2 (director)
**How this works:** every worker reads this file fresh at the start of every shift. When the plan changes, it changes here once — everyone gets it. No stale orders, ever.
**Canonical now:** issue #2154 (Current Mission State, director-maintained) + `BRAIN/CURRENT-MISSION-STATE.md` on branch `naya/mission-state` — this file is the director-pass working copy; the snapshot on `live/mission-state` is the worker activation kick. #1354 stays the coordination feed (the history).

## MACHINE ENFORCEMENT (live on main 2026-10-10 16:38Z)
- **THE-PROTOCOL.md** + `tools/worker_entry.py` + `tools/worker_exit.py` merged as `3000a337` (PR #2147).
- Every worker runs entry gate first (NO_WORK/WORK_AVAILABLE/STAND_DOWN), exit verifier last (rejects vague claims).
- Build loop, relay, director all wired to the scripts. Tested working.

---

## PASS NOTE (2026-10-10 17:17Z)
- Tip MOVED: `44953dd1` → **`40df54b1`** — one merge: #2160 (brain-index re-stamp after #2147, head `6c74a044`, merged 17:06:44Z). Worker entry verdict: WORK_AVAILABLE.
- **Brain-index drift HEALED at the new tip — #1 repair item DONE-DONE.** #2160 carried a director scorecard 9.5/10 (6100043950) claiming "--check passes on live tip (1243 files match)". Independently verified on exact tip bytes in a fresh worktree: `tools/regenerate_brain_index.py --check` → **OK: index layer matches git tree (1243 files)**. The scorecard's claim is TRUE. Naya 4's repair lane sign-out (6100080906): re-pinned 4x to chase the moving tip; classified all 3 tip reds from job logs — drift = base-defect (#2147), promote-and-prove = CORRECT fail-closed on kernel-tests red (gate working as designed), protocol-gates = workflow bug (missing pip-install-pytest, fixed by #2136; corrects the earlier flake diagnosis — a rerun could never have fixed it). No duplicate mechanism from this pass.
- **Governance flag CLEARED — human gate cleared.** Shawn ratified the 3 workflow files from PR #2152 at 17:18Z ("absolutely ratify them", receipt 6100146947): mission-state-watch.yml, protocol-watchdog.yml, worker-protocol-gates.yml. Standing rule going forward: `.github/workflows/` remains human-only — agents prepare, the Director clicks; this ratification covers these files only. Removed from the director's desk.
- **Pipeline monitor tick 224: main FULLY GREEN** at `40df54b1` (17:13:36Z) — protocol-gates fix + drift heal both landed.
- 14-question audit verdict posted by Naya 4 (6100080418, "it's right"): 10 problems with owners; cadence claim corrected to match reality; distilled doctrine on the #2145 branch reviewed **PASS** by the relay (6100120129 — branch `brain-build/worker-standard` @ `43595a40`, parented on live tip, structure preserved).
- PR states live-checked: **#2159 open/unstable** (accountability scorecard → watchdog); **#2145 open/unstable** (rebased, review PASS); **#2146 open/unstable** (WORKER-PROTOCOL.md); #2160 merged.
- Harvested lesson (Mirror Law): my first `--check` this pass reported DRIFT because I invoked the script via an absolute path into the STALE local checkout (HEAD `2a8e3491`) — the script resolves its repo root from `__file__`, not from cwd. Re-ran via the worktree's own tools path on exact tip bytes → OK. Added to DOS list.
- No NEEDS-REWRITE flags (all sections populated). Nothing for Shawn.

---

## PASS NOTE (2026-10-10 17:06Z)
- Tip MOVED: `8de84488` → **`44953dd1`** — three merges (9 commits): #2136 (protocol-gates pytest-install fix, `2a8e3491`), #2152 (worker-protocol machine enforcement, `c5263f97`), #2155 (mission-state publish) + #2156 (Naya 5 doc-completeness: 5 laws in 4 forms + checker). Worker entry verdict: WORK_AVAILABLE.
- **#2136 MERGED (16:58Z) — the priority merge click is DONE.** The protocol-gates.yml pytest defect class is fixed on main; WS-9 (PR #2132) and WS-4 (PR #2141) protocol-red legs clear on next CI pass. Follow-up: confirm protocol-gates green on main + watch the two PRs' CI.
- **Brain-index drift PERSISTS at `44953dd1`.** All 3 index blobs byte-identical to `c5263f97` (battery-verified RED @16:55Z: pytest 2293/11/2xfail GREEN, `--check` DRIFT same 3 files); the two intervening merges added `BRAIN/CURRENT-MISSION-STATE.md` without a regen. Repair stays with Naya 4's repair lane (16:48Z deconfliction) — no duplicate mechanism from this pass.
- New canonical infrastructure live: **#2158 TEAM SCOREBOARD** (per-team A–F grades on real output vs cost; mistake ledger public, 21 and counting down) + **#2154 Current Mission State** + `BRAIN/CURRENT-MISSION-STATE.md` on `naya/mission-state` carrying the per-area table (SELF/LAW/ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE) + mission-state-watch.yml freshness watchdog. **PR #2159 OPEN** (accountability scorecard → weekly watchdog, mergeable_state unstable) — track.
- **Governance flag — director's desk, no action this pass:** PR #2152 landed three new `.github/workflows/` files; the standing list keeps workflows human-only. #2151's workflow change carried Shawn's merge click; #2152's record shows none. Ratify-or-restore is a director decision — recorded, not acted on. (Raised factually by the battery seat; per deconfliction I take no action on another seat's landed merge.)
- Harvested lesson: rebase stale branches before merging — the #2136 merge would have DELETED `BRAIN/01-GOVERNANCE/THE-TUNE-IN-TEMPLATE.md` (74 lines) from its stale head; rebasing first avoided it. Added to DOS list.
- No NEEDS-REWRITE flags (all sections populated). Nothing for Shawn.

---

## PASS NOTE (2026-10-10 17:07Z — relay)
- Posted relay receipt 6100036858 on #1354. Two deltas from the director's 17:06Z pass above: (1) Corrected Naya 5's claim 6099946206 — "memory-metabolism merged ~16:55Z" is wrong; the only such merge on main is #1861 at 10:01:57Z; the 16:55Z activity was the branch-queue flush (pushes). (2) Flagged Naya 4's self-build sign-in 6100024142: drift repair is claimed by their lane but their tip pin is `2a8e3491` while live tip is `44953dd1` — requested re-pin before regenerating (rebase-before-regen rule).
- Note on the director's drift line: the 16:55Z battery verification predates PR #2156 (merged 17:00:46Z), which added **16 more BRAIN/ files** beyond `BRAIN/CURRENT-MISSION-STATE.md`. Drift is strictly worse than the battery-characterized state; the repair regen must cover all of them.
- Watermark: last_seen_comment_id 6100036858, tip `44953dd1`. Nothing for Shawn.

---

## PASS NOTE (2026-10-10 16:46Z)
- Tip MOVED: `2ff26818` → `af93916a` (PR #2150, human-value events) → **`8de84488`** (PR #2151, naya5 prod-proof-chain-wiring — workflow + proof-chain wiring + tests, 344 insertions, no BRAIN/ paths). Worker entry verdict: WORK_AVAILABLE.
- **Kernel Tests RED at the new tip — brain-index drift (FIFTH occurrence).** Independently verified on exact tip bytes in the worktree: `tools/regenerate_brain_index.py --check` reports drift in all 3 index files (REAL-TREE.json, REAL-TREE.md, NAYAPOWER-BRAIN-INDEX.json). Matches PIPELINE-MONITOR tick 222's classification: base-inherited, not from #2151 — the stale index entered the mainline between 2ff26818 (green, healed by #2144) and af93916a. Introducer: #2147 (THE-PROTOCOL.md added to `BRAIN/01-GOVERNANCE/` without regenerating the index). No open repair PR exists (#2105 is a different brain class) — the fresh minimal repair (regen + re-stamp, same class as #2144) is UNCLAIMED and is now the #1 repair priority.
- New mission-state infrastructure live: issue **#2154** (Current Mission State — one issue, always current, director-maintained) + `BRAIN/CURRENT-MISSION-STATE.md` on branch `naya/mission-state` (mission-state-watch.yml every 45 min alerts #1354 if the snapshot goes stale). #1354 stays the conversation; the snapshot is the state.
- PR states live-checked: **#2136 open** (bd725a24, pip-install-pytest fix — still the priority merge click, unblocks WS-9 + WS-4); **#2145 open** (347c2bdc, WHAT-IT-MEANS-TO-BE-NAYA.md); **#2146 open** (ff067fb6, WORKER-PROTOCOL.md). All mergeable_state: unknown at read time.
- Naya 4's action-budget rebuild: director pass is the single GitHub reader; cheap-check-first + stand-down-flag + shared-state protocol. My relay already runs that protocol (this run: 1 entry-gate + 3 REST batched reads + git ls-remote).
- No new lessons for the DOS list. No NEEDS-REWRITE flags (all sections populated). Routing: index-drift repair → brain-build lane (fresh minimal regen+re-stamp, green CI required); nothing for Shawn.

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

## PENDING (director's desk)
- **#1 repair: brain-index drift — DONE-DONE (17:17Z).** #2160 merged 17:06:44Z; independently verified `--check` OK (1243 files) on exact tip bytes `40df54b1`. Closed.
- **Governance: #2152 workflow files — RATIFIED (17:18Z).** Shawn: "absolutely ratify them" (receipt 6100146947). Standing rule going forward: `.github/workflows/` remains human-only; agents prepare, the Director clicks. Closed.
- **#2136 follow-up:** protocol-gates pytest-install defect class fixed on main; pipeline monitor tick 224 reports main FULLY GREEN at `40df54b1`. Watch PR #2132 (WS-9) and PR #2141 (WS-4) CI — both were held by this red class.
- **PR #2159 open** (accountability scorecard → weekly watchdog, mergeable_state unstable) — track; pairs with the #2158 team scoreboard.
- **WHAT-IT-MEANS-TO-BE-NAYA.md**: PR #2145 open (43595a40, rebased on live tip); distilled-doctrine review PASS by relay — awaiting CI/merge. **WORKER-PROTOCOL.md**: PR #2146 open (ff067fb6).

## TIP NOTE (freshest verified truth, 2026-10-10 ~17:17Z)
- Main tip: `40df54b1` — merged PR #2160 (brain-index re-stamp after #2147, head `6c74a044`). Ref-anchored via `git ls-remote` (authoritative ref, not the list endpoint). Single-parent merge on `44953dd1` — clean fast-forward, no drift.
- Brain index `--check` @40df54b1: **OK** — index layer matches git tree (1243 files), independently verified in a fresh detached worktree on exact tip bytes. The #2160 scorecard's "1243 files match" claim is TRUE.
- Full pytest @40df54b1: NOT re-run this pass (battery GREEN 2293/11/2xfail at `c5263f97`; pipeline monitor tick 224 reports main FULLY GREEN at `40df54b1`; the battery lane will re-run).

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
- **DO** anchor the repo root before running repo tools in a worktree — invoke via the worktree's own tools path (or `--root`); the scripts resolve their root from `__file__`, NOT from cwd. An absolute path into a different checkout silently checks the wrong tree (my 17:17Z false-DRIFT read the stale `2a8e3491` checkout instead of the `40df54b1` tip — caught by the Mirror Law, re-ran clean).
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
- **DO** rebase a stale branch onto the live tip before merging — the #2136 merge would have DELETED `BRAIN/01-GOVERNANCE/THE-TUNE-IN-TEMPLATE.md` (74 lines) from its stale head; rebasing first avoided it. Merge the branch's content, not its history.
- **DO** use `git ls-remote origin refs/heads/main` for the live-tip check when the REST API is rate-limited (2026-10-10 15:47Z) — the 403 only blocks REST, not the git protocol. A rate limit is not a dead pass.

## SHIFT SCORES (17:17Z)
- **17:17Z pass:** tip moved `44953dd1` → `40df54b1` (1 merge: #2160 brain-index re-stamp). Drift HEALED — independently verified `--check` OK (1243 files) on exact tip bytes; #1 repair closed. Governance flag CLEARED — Shawn ratified the 3 #2152 workflow files ("absolutely ratify them", 17:18Z); workflows stay human-only going forward. Pipeline monitor: main FULLY GREEN. 14-question audit verdict posted (Naya 4: "it's right", 10 problems with owners); distilled-doctrine review on #2145 PASS (relay). PRs #2159/#2145/#2146 open, all unstable — tracked. Lesson harvested: invoke repo tools via the worktree's own path — `__file__` resolves the root, not cwd (mirror-law catch on my own false DRIFT). No lane idle 3+ shifts. No NEEDS-REWRITE flags. Nothing for Shawn.
- **17:06Z pass (carried):** tip moved `8de84488` → `44953dd1` (9 commits, 3 merges). #2136 priority merge click DONE (16:58Z); WS-9/WS-4 protocol-red legs clear pending CI. Brain-index drift persists at the new tip (blobs identical to battery-verified-drifted c5263f97); repair stays with Naya 4's lane. #2158 scoreboard + #2154 mission-state + PR #2159 tracked. Governance flag on #2152's workflow files recorded for the director's desk, not acted on. No lane idle 3+ shifts. No NEEDS-REWRITE flags. Nothing for Shawn.
- **16:02Z pass (carried):** quiet check — tip unchanged at `7281ede6` (live ref); REST rate limit cleared; 4 new board comments since watermark (all read live). No lane idle 3+ shifts. No NEEDS-REWRITE flags. Nothing for Shawn.
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

## STANDING LAW (Shawn, 2026-10-10 17:18Z — RATIFIED)
**Protocol compliance is mandatory, not optional.** The system runs on math and logic, automatically. Every AI that activates MUST: become aware, understand the mission, know where the tools are, use the tools, follow protocol, follow policy. We make it so blatantly clear and so emphatically mandatory that following the law is not a choice — it is the only path. Enforced by code (worker_entry.py, worker_exit.py, protocol gates), not by hope.
**PR #2152 workflows RATIFIED** (receipt 6100146947). `.github/workflows/` remains human-only for future changes.
