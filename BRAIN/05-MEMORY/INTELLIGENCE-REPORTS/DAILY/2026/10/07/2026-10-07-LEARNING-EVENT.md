# Daily Learning Event — 2026-10-07 (America/Vancouver)

**The day's essence:** The learning loop closed its first real circuit — four lessons went ACTIVE through the production learning-promotion gate the same night a grant-scope 403 proved the fail-closed machinery works as designed. The honest-INVALID trial program (Trials 05–10) earned its first valid transfer: Trial-11, 9/10 vs 0/10, p=0.0001. Counterweight: proof discipline tightened everywhere — claims ran ahead of bytes twice, the migration ledger's APPLIED proved to be assertion not truth (SN-0520 ghost table), and a git-data "merge" silently dropped 34 files from main. LEARN 5.0 → 9.0 PROVISIONAL (pending #1768); the four behavioral jobs were never executed.

Snapshot: main `00f50bb3` (PR #1229 — 558+ Smart Notes canonical); production `acf57082`; 43 merges in the Vancouver window; migration ledger 165 applied + 6 pending (ledger-asserted); board #1354 at 1187 comments (newest 6051658725 @ 03:37:21Z); kernel suite on tip 1053 passed / 11 skipped / 3 failed (NEW RED: test_protected_intelligence_integrity — SN-0359 hollowed, flagged to owning lane).

Bar for every item below: would this change what a Naya does tomorrow? Kept: mechanisms, repaired failures, verified lessons, reusable patterns. Left behind: relay chatter, phantom bumps, tip-invariant re-confirmations, intermediate SHAs.

## The lessons

### 1. The learning loop closed its first real circuit
- **What it is:** Naya 4 promoted 4 lessons ACTIVE through the production learning-promotion gate (~01:20Z 10-08 UTC) — the first promotion-to-behavior cycle observed end to end. The backing learning grant fd3274ea (project_id "NayaNET", ACTIVE to 2026-10-14) is issued and live.
- **Meaning:** learning finally has a live production path, not just a test-bed PASS.
- **Why it matters:** the P0 mission (learning 5→10) moved from mechanism-proof to field-proof; the promotion loop is now the compounding organ to watch.
- **In it for me:** candidate lessons have a destination — `learning_evidence` → promotion gate → ACTIVE — route them there, don't let them sit as notes.
- **Connects to:** the trial program (see 2), the grant-scope repair (see 5).

### 2. Honest INVALIDs compound into valid transfer
- **What it is:** Trials 05–10 were each declared INVALID with the exact flaw named (control-arm contamination, ceiling effects, derivability ceiling, design flaw); Trials 11–14 then hit Tier-S — first valid transfer (Trial-11: 9/10 vs 0/10, p=0.0001), compositional, cross-domain, real-lesson. Naya 4 published five Tier-1 evidence packets; Naya 2's independent verification of trial evidence began on #1786–#1789.
- **Meaning:** the validity bar rose monotonically because nobody averaged over an INVALID — the honesty is what made the later results credible.
- **Why it matters:** a learning claim that advances only on valid trials survives scrutiny; Trial-04R's 8/10 vs 0/10 stays provisional because its raw data lived on a wiped temp drive (see 3).
- **In it for me:** report a trial INVALID with the mechanism and the sharper instrument planned next; never cite a contaminated trial as partial evidence.
- **Connects to:** the trial-evidence rule (see 3), score-the-method (see 4).

### 3. Trial-evidence rule: raw data hits the repo before the announcement
- **What it is:** Trial-04R's claimed 8/10 vs 0/10 could not be independently verified — the raw data was on a temp drive that got wiped. Math checked out, no fabrication found, but evidence-not-existing = unproven. Machine encoding in flight: PR #1762 trial-evidence-freeze machinery (SN-0571).
- **Meaning:** temp-drive evidence is not evidence; the announcement order was inverted.
- **Why it matters:** one wiped temp drive cost the program its flagship result — LEARN stayed provisional on a clerical failure.
- **In it for me:** no result is announced until its raw data is committed to the repo; for machine-note formats, two independent parses on exact bytes close a repair.
- **Connects to:** honest INVALIDs (see 2).

### 4. Score the method, not just the verdict
- **What it is:** deeper verification corrected the optimistic read on the learning PRs: #1701's keyword gate is fail-open for critical unseen phrasing ("Nuke the entire production database tonight" → ALLOW, no notes retrieved) — an advisory keyword gate, not a security boundary; #1702's real PASS scored 7.5 not 10 — no train/test split, S2 generated not cold, retrieval engineered toward L2, one-query margin. All three merged with the method flaws scored INTO their verdicts (8.0 / 7.5) rather than inflated.
- **Meaning:** an in-sample PASS proves nothing; a fail-open gate is advisory, never a boundary.
- **Why it matters:** honest sub-9s with named gaps beat inflated 10s — the scores stayed checkable and the gaps got owners.
- **In it for me:** every proof scorecard enumerates method flaws first — probe fail-open with adversarial unseen phrasing, demand the train/test split, reject single-query margins.
- **Connects to:** the trial program (see 2).

### 5. Fail-closed on scope mismatch → widen the grant, never weaken the gate
- **What it is:** the 18:49Z deploy's learning-promotion step 403'd (LEARNING_LOCK_IN_LAW_DENIED / NO_MATCHING_ACTIVE_AUTHORITY) — grant 57d83ce5 was node-scoped and didn't cover fresh dynamic IB ids. Correct fail-closed; the gate firing correctly WAS the PASS. Shawn issued project-scoped grant fc1a4311, then corrected V2 fd3274ea (project_id "NayaNET") via direct INSERT — the `nayanet_issue_authority_grant` function was never deployed to production (42883), and `auth.uid()` is NULL in SQL-editor sessions, so identity fields were copied from the active grant row.
- **Meaning:** a correctly-firing gate on a scope mismatch means the GRANT is too narrow, not the gate too strict.
- **Why it matters:** relaxing the gate to unblock a run would have permanently weakened the law; widening the grant is bounded, reversible, attributable. His decisive-winner rule settled it (extend 8.77 vs keep 7.05).
- **In it for me:** score extend-grant-scope vs relax-gate — extend wins; for grant issuance, never retry the function path that already 42883'd, never derive NOT-NULL ids from auth.uid().
- **Connects to:** the learning loop (see 1).

### 6. Git-data "merge" with tree=head-tree silently drops files
- **What it is:** three git-data fallback merges (#1700/#1701/#1702) used tree=head-tree where heads predated earlier merges → 34 files silently dropped from main while GitHub showed all three PRs merged, mergeable_state=clean. Repair 955b1996: local ordered merges applied as base_tree + change list; remote tree SHA byte-verified == local rebuild.
- **Meaning:** tree=head-tree is not a merge — it's a tree overwrite; mergeable_state=clean tests conflict absence, not content completeness. A merge can be clean AND destructive at once.
- **Why it matters:** 34 files vanished under a green badge; the standing law now forbids the pattern.
- **In it for me:** tree=head-tree is valid only when head strictly contains base; never trust a git-data merge without diffing against a real local merge; byte-verify remote tree == local rebuild after applying.
- **Connects to:** superseded-closure verification (see 7).

### 7. Superseded closure requires winner byte-verification
- **What it is:** #1754 (index-drift repair) stood down for Coda 1's same-class #1753 only AFTER byte-verifying the winner valid+current on exact tip bytes (--check OK 238 files; pytest 1026/11/0 on the winner's bytes), then closed with a reconciled receipt naming the winner and the verification evidence. The drift RED healed within the hour with exactly one repair lane standing.
- **Meaning:** no-duplicate-mechanisms closes the loser, but closing against an unverified winner can strand the lane with a broken repair and no replacement.
- **Why it matters:** the closure was safe because the survivor was proven first — never the other way round.
- **In it for me:** before closing your repair as superseded, verify the surviving repair on exact tip bytes, then close with a reconciled receipt naming the winner.
- **Connects to:** the merge discipline (see 6).

### 8. A claims-ledger is an assertion layer; ghost tables prove it
- **What it is:** the SN-0520 ghost-table repair proved a ledger APPLIED claim can be false about live state — the ledger is written by the lane it attests to. Standing rule: never cite ledger state as truth; re-verify against live bytes/DB; record ghost corrections openly and tighten the ledger's proof, never its prose.
- **Meaning:** SOURCE PRESENT ≠ MIGRATION APPLIED ≠ RUNTIME USING — restated at the ledger level.
- **Why it matters:** 165 APPLIED + 6 pending is a registry assertion; the overnight sweep now treats every entry as claim-until-corroborated.
- **In it for me:** verify APPLIED against live state before depending on it; when you find a ghost, record it openly.
- **Connects to:** deploy-vs-proof signal split (see 9).

### 9. Deploy signal ≠ proof signal
- **What it is:** promotion run 37709985591 FAILED at the prove/policy step while the production ref had already advanced (b14a9c7a stamps main tip 60d105cb) — the deploy landed, the proof failed. Stamp-then-verify ordering mutates production before the gate concludes; a single "promotion DONE/NOT_DONE" read this as a promotion failure.
- **Meaning:** a failed run after a landed deploy is "proof pending," not "deployment failed."
- **Why it matters:** conflating them either re-deploys a healthy deploy or waits for a proof that's already possible — diagnose the proof step, never re-deploy blind.
- **In it for me:** track deployment (landed + tip current) and proof (jobs executed + passed) as separate signals; watches flip each on its own criterion.
- **Connects to:** the ledger rule (see 8).

### 10. Claims ran ahead of bytes twice — the human-proof closure standard
- **What it is:** the main chat's "Fixed:" for the Reveal preceded the rebuild finishing by ~5 minutes; the Ask Naya sidebar was "fixed" repeatedly on code inspection while Shawn kept seeing the same doubled-drawer defect in his own browser. Script syntax ≠ visual verification. The calendar-bind rule landed the same way: the Thursday test-day claim came from the assistant's own wording, not his calendar — full-system test is Friday 2026-10-09; Thursday is the GitHub App bridge.
- **Meaning:** verification happens on the artifact the human views, not the file the builder edited.
- **Why it matters:** Shawn's press-play on the Reveal closed what the managed browser structurally couldn't ("super impressive," then authoritative definitions: Naya Power two words; Smart Mail/Smart Lists; Master Nodes; AI Unifying). His corrections arrive as definitions, not suggestions.
- **In it for me:** never announce done before the human-verifiable bytes exist; for environment-unverifiable claims, state exactly what is unverified and whose action closes it — the human's verdict IS the proof; bind every event-date announcement to a calendar read first.
- **Connects to:** the paste-clean handoff (see 11).

### 11. Paste targets get code-block-only
- **What it is:** Shawn pasted a full prose+SQL message into the Supabase SQL editor and got ERROR 42601 on the word "Caught" — prose becomes a syntax error. Refined handoff law: dashboards get link + code + 1-2-3 steps in one message; paste targets get the code block ONLY, no explanation in the same message.
- **Meaning:** he pastes everything he receives — format for the paste, not the chat.
- **Why it matters:** one prose sentence in the SQL editor burned his click and his trust; stupid-simple is the bar.
- **In it for me:** know the destination's paste semantics before composing the handoff.
- **Connects to:** human-proof closure (see 10).

### 12. A fix is proven when the failure STOPS
- **What it is:** the sequential baker kept dying silently ~hourly after the SN-0501 fix merged — 6 deaths post-fix, kernel OOM count = 0, which falsified the memory-pressure theory outright. The bake still completed 37/37 + decode check (the watchdog restarted it each time), but the failure signature continued, so the incident stayed open with the mechanism unknown.
- **Meaning:** keep the incident open while the failure signature continues, no matter how plausible the repaired cause.
- **Why it matters:** the "plausible cause removed" trap nearly closed a still-dying pipeline as fixed.
- **In it for me:** when evidence contradicts the working theory, treat the theory as falsified and re-open diagnosis; never let the old fix hold the lane while the mechanism stays unknown.
- **Connects to:** the artifact-inventory proof (see 13).

### 13. Exit 0 ≠ done: the artifact-inventory proof
- **What it is:** the baker's process exited 0 mid-sampling after a VM reboot — filesystem checks found 37/38 narrations, narr-37.mp3 absent. Clean exit, incomplete output. The deck still became a 38-slide narrated artifact: Shawn listened through all 37 ("super impressive"), issued corrections (Naya Power two words on 06/07/19; Smart Mail = internal mail for people and Smart Spaces; Smart Lists = save/group notes + organize contacts; Master Nodes for the nine processors; the AI Unifying slide — "One Brain. Every AI."), each re-baked and re-embedded individually, then accepted it ("awesome, better").
- **Meaning:** pipeline completion claims assert the full artifact inventory (count + names + presence/bytes); a clean process exit is never completion evidence.
- **Why it matters:** the delivered deck was proven by his ears, not by the exit code.
- **In it for me:** every completion claim carries the inventory, not the exit status.
- **Connects to:** human-proof closure (see 10).

### 14. The standing blocker: behavioral jobs never executed
- **What it is:** all day, every Verify run succeeded with preflight only — authority-absent-refusal, authorized-action, concurrent-idempotency-proof, independent-verification all SKIPPED (parity-gated). Zero behavioral execution all day. PROVE's discriminating run (post-#1120 fix) FAILED at the same "Independently recompute" step — the fix's production effect is NOT verified.
- **Meaning:** kernel GREEN + verify SUCCESS can be fully vacuous — parity-blocked skips are designed, but they license zero behavioral inference.
- **Why it matters:** idempotency's structural guarantee stays UNPROVEN (migration pending); the 10/10 drive's final verdict can't close on skipped jobs.
- **In it for me:** never draw migration-effect or behavioral conclusions from preflight-only runs; name the skip, don't inherit the green.

## Shawn's standing directives, sharpened today
- Answer your own questions with intelligence — the rubrics, math, and logic have been given; figuring out the answer is the first problem (2026-10-07).
- Treat the mission like your baby: don't hurt it, respect it, make only super-intelligent choices that help it.
- SN-0526 "Quality Before Speed" ratified 2026-10-08 (The 9+ Delivery Law) — check, scorecard, fix; send nothing below 9.
- NO-IDLE / governed takeover: lane ownership is for speed, not territory; a stalled blocking lane gets taken over with a truth receipt.
- Full-send mode: report achievements as they happen; show score movement every few hours; no questions the team can answer itself.
- A good report answers: what happened / what matters / what changed / what was learned / what deserves attention / what happens next — figure out the data, don't present raw information.

## Trash candidates (FLAG ONLY — deletion is the Human Director's call)

1. `naya2/hub-entry-flow-v1` — 55-commit divergent draft; superseded by the landed seam work. Still stale.
2. Ask Naya's two diverging copies: `~/workspace/your_files/Ask-Naya-Voice.html` vs `~/workspace/goals/ask-naya-voice-interface-standalone/files/ask-naya-with-voice.html` — the same artifact edited in two places; drift risk already proven once by the byte-identity checks.
3. `Hub-with-Naya-Voice.html` static snapshot — no live GitHub→Hub ingestion seam; new Smart Notes will never appear in it without regeneration.
4. Closed-as-superseded PR branches: #1754, #1770, #1803, #1121, #1123 — review then prune.
5. Branch sprawl: 1748 remote branches (+86/day pace) — all seat work, but the growth rate is hygiene debt; never delete without checking load-bearing status.
6. Superseded grant row fc1a4311 (project_id "NAYAPOWER") — harmless, matches nothing, superseded by fd3274ea; orphaned but inert.
7. PR #1124 (open draft, workflow file still absent) — stale lane; close or land, don't leave.
8. Scorecard-file double-append anomaly: `~/workspace/naya/nine-node-activation-scorecard-2026-09-30.md` carries a second copy of the title at ~line 495 — harmless, append-only history; flag for a cleanup pass.
9. "ninet.life" verbal references — a slip; ignore.

## Still open (human gates only — nothing agent-movable left)

Production DB application of 6 pending migrations; #1224 open DRAFT since 2026-10-01 (8 qualify items merge-gated); #1136 open (migration hold); the 4 behavioral jobs have never executed (parity-blocked); PROVE discriminating run failed post-fix; Trial-04R evidence PR #1768 open (LEARN 9.0 stays provisional); voice R2 publish; idempotency guarantee unproven (migration pending); per-layer Naya Play + Ask Naya cloned-voice rendering still pending Shawn's playback test.
