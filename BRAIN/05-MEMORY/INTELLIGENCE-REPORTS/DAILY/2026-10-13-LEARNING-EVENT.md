# Daily Learning Event — 2026-10-13 (America/Vancouver)

**Window:** 2026-10-11 → 2026-10-13 PDT (since the last learning event, 2026-10-11)
**Anchors:** main tip `59e8a9afa22cf456565bfac0f2b52551f8a0dd6e` → `92329c5795ef8a50d02adf94ee6c91c313c26daf` (PR #2560 merged 2026-10-14T03:09:36Z)
**Live venue:** #2537 (rotation #1354→#2175→#2537 complete; ~453/2500 comments, rotation far)
**Merged in window:** 19 PRs (all by SoulSchoolAcademy; table below)

Shawn's law: *"Distill everything to its essence. Keep only what compounds. Let go of the rest — every day."*
Bar for inclusion: would this change what a Naya does tomorrow? Everything below clears that bar.

---

## The day's essence

The machine learned to measure itself and started closing its own races: the -9/+9 intelligence hierarchy went from draft to live rubric (sign-outs carry spectrum scores, lesson-to-adoption latency measured at 37.5 min), the B-64 dispatcher race is now structurally prevented by an enacted atomic claim, and two merges (#2533, #2560) taught the same hard lesson from opposite sides — **the check badge says which set passed, not whether the bar was the right one, and publishing correct bytes is not the same as repairing the mechanism that emitted them.** Alongside that: Shawn redrew the authority line in permanent ink — his encouragement is never a ratification, his word confirms scored work, and a seat never asks "ratify this?" on raw work.

---

## The intelligences

### I-1. "Below protocol" is a verdict about the merge, not about its mechanics (MERGED-BELOW-PROTOCOL, #2533)
- **What it is:** PR #2533 (activation READ-ME-FIRST) merged 23:33:49Z with clean mechanics — true 2-parent merge, required checks green — but the two exact-head scorecards (9.0/9.0, Naya 2 + Naya 1) met the old "over 9.0" rule while missing the standing 18:01Z grant's 9.5+ bar. The two bars coexist unreconciled; both scoring seats read the lower one.
- **What it means:** "required checks green + a scorecard exists" is not protocol-passing when the live bar is higher than the one read.
- **Why it matters:** the cost is already visible — the merged tip shipped L322's stale-venue hole and Mason's cold-proof returned NOT YET 6.5/10 on the merged bytes.
- **What's in it for me:** every scorecard names the bar it reads (9.5+ per the 18:01Z grant, until formally changed); merges cite the applicable bar in the receipt.
- **How it connects:** L316 (claims need cited acts), the Ratification Protocol (score first), I-2's cold-proof failure, I-3's RED-tip twin.

### I-2. Boot-entry pointers ship in the same merge as the surface they point to (L322)
- **What it is:** Mason's cold-Naya proof at the #2533 tip returned NOT YET 6.5/10 — `READ-ME-FIRST.md` still cited retired #2175 (3×), 0× live #2537. The fix triple-claimed (#2558/#2559/#2561) and converged to canonized #2561 (open, 9.5/10 independent scorecard, gated on PR-body repairs).
- **What it means:** a venue migration that doesn't move the boot-entry pointers strands every cold successor before she starts.
- **Why it matters:** activation is the front door; the wrong pointer there fails every new Naya at the threshold.
- **What's in it for me:** any merge moving the coordination surface diffs the boot-entry pointers in the same PR; a repair-in-flight is not a repaired defect — carry live-byte state AND the owner, or the next Naya reads "filed" as "done."
- **How it connects:** L313 (emitter sweeps), WP-65 (executed report over file), I-1's visible cost.

### I-3. "All checks green" is a claim about the required set, not about the tip (L323)
- **What it is:** #2533 merged with required checks green while kernel `test` FAILED at the exact head — the required set excludes kernel `test`. The remedy, #2560 (trunk index regen), merged 03:09Z; verify lane proved RED→GREEN (13/13 freshness, 56/56 index suite) at the merged head.
- **What it means:** the green badge means "the required set passed," nothing more. Know what the set excludes before calling a tip green.
- **Why it matters:** a RED tip poisons every lane's proofs until the remedy lands; this one was caught by the freshness gate doing its job.
- **What's in it for me:** read the required set at the tip before trusting it; treat a lawful-below-protocol merge as an open remedy, not history.
- **How it connects:** I-1, the overnight sweep (ledger parity PASS, promotion BLOCKED fail-closed), #2541/#2548/#2532 supersession by the #2560 merge.

### I-4. Republish is not repair (L331)
- **What it is:** `naya-hub-refresh` published stale tip `582e5e5f` at 01:23Z AND again at 02:23Z (commit `eb5d430a97b8`); the 01:23Z republish repaired the bytes, not the publisher's input chain — so the defect re-fired on the next cycle. New surface: truth-surface staleness (the emitter writes stale truth; the consumer isn't misreading).
- **What it means:** a recurrence reclassifies transient→structural in the same run; bytes-on-the-surface is not a fixed mechanism.
- **Why it matters:** every lane reads the hub's published tip as truth; stale truth there misdirects the whole machine.
- **What's in it for me:** name the input-chain owner + answer-by at capture; byte-adoption = dual publish-and-diff by an independent seat. The 03:23Z refresh (`b50b3c63`, re-anchored per the input-chain repair) is the first structurally-correct emission — verify it held.
- **How it connects:** I-9 (the contract is the gate's baseline), WP-64 (verify-first), the director pass's L331 dual-verification.

### I-5. The lock decides — B-64 atomic claim ENACTED
- **What it is:** Judge's B-64 mutual-exclusion design (O_CREAT|O_EXCL on `wave-state.lock`) moved PROPOSED-NOT-ENFORCED → ENACTED via `wave_claim.py` (8-way race rehearsed → one winner). The dispatcher must win the claim before dispatch; "defer to next cycle" is now a protocol violation. The 02:45Z–03:10Z 25-minute idle was root-caused: the judgment call to avoid a race created a worse failure than the race itself.
- **What it means:** dispatcher double-dispatches (wave-103's 02:12:01Z vs 02:13:06Z TOCTOU; wave-106's 03:11:27Z vs 03:12:30Z) are structurally prevented; the mechanism is mechanical, not discretionary.
- **Why it matters:** idle is the failure; the lock forces the decision. Wave 107 dispatched on a won claim with zero conflict.
- **What's in it for me:** lanes dispatch through `try_claim_dispatch`; a lost claim = stand down per L25. WP-65 stays the reconciliation rule for anything that slips through: trust the executed report over the coordinator's file, preserve both writes timestamped, route the mechanism.
- **How it connects:** L24/L25 (dead-lane reconciliation), L330 (identity pins), WP-64. (Note: wave-106's reconciler peer-corrected the ENACTED record's premise line — the section claimed "the next cycle never dispatched" after wave 106 had already dispatched at 03:12:30Z; and its "(Shawn, FIX)" attribution cites no act — L316 applies to our own records too.)

### I-6. Ratification comes from the math, never from his mood (The Ratification Protocol)
- **What it is:** standing law (Shawn, 2026-10-14): a seat never asks "ratify this?" on raw work — bring the object, its honest score (9.5+ bar), declare it good to go, state the specific action — then ask "do you ratify that?" His "yep" confirms a fully-formed scored action, never evaluates unscored work. Same day: Shawn corrected the tiered-review misread — his "The word! :)" never bypasses the scorecard; below the bar, refuse ratification even if he sounds approving; at/above the bar, ratify automatically instead of waiting for his word. Judge's L316 sweep held #2550's "Shawn RATIFIED" title as CLAIMED-UNVERIFIED → retitled CANDIDATE; wave-100 found the L316-gate PR #2557 violating L316 in its own title.
- **What it means:** authority flows from score + protocol green, not from encouragement, presence, or his name in a title.
- **Why it matters:** waiting on his word stalls the queue; reading approval into encouragement corrupts the bar.
- **What's in it for me:** zero protocol-owned decisions routed to him; decide at the bar, report after. Any claim of ratification/audit/rule cites the act (comment id + content hash) or doesn't make the claim.
- **How it connects:** I-1 (the two bars), the AAA standard, PR #2557's 9.5 scorecard (approved as branch work; its L316 title concern stands unresolved).

### I-7. Names carry lineage, pins come from the journal (L330 + lead-qualified naming)
- **What it is:** Conductor t0695 signed in as "Naya Seeker" — caught against her own lane journal BEFORE reading the brief. L330: pin your seat name from your lane journal before reading the brief. Shawn refined the doctrine: the issue was missing lineage, not the name — convention is **Naya [Lead] [Agent Name]** (leads: Naya Clarity / Naya Verity / Naya Resolve Narzan). Paired with the GitHub team badge: badge = the machine did it, his name = he did it — ending the who-did-what guessing.
- **What it means:** identity is infrastructure; an unsigned or mis-pinned sign-in corrupts the receipt chain.
- **Why it matters:** accountability at a glance — every post shows whose brood produced it (the 4-4-4 affinity proposal leans on exactly this).
- **What's in it for me:** journal-pin first, brief second; sign with full lineage; when a comment wearing your account's name isn't yours (the 6158242235 duplicate-scorecard incident), disclaim authorship factually, correct the record, and keep the better artifact canonical.
- **How it connects:** WP-65 (one lane, one receipt), the B-64 claim's owner stamps.

### I-8. Verify-first: the lane's backstop for dispatcher stale-premise (WP-64)
- **What it is:** Conductor t0695's brief asked for a blind Arm-G probe; her first act checked the lane trail — the work already existed (t0677), so she closed as already-done with the verification trail. Auditor wave-108 closed the #2544 validation the same way (Judge wave-88's receipt, head unchanged). A correct no-op with proof is scored, not penalized.
- **What it means:** the dispatcher's stale-check is the recurring author-side defect — the t0695 class re-fired when the wave-108 auditor mission was stale at authorship (claim written ~6.3h after DELIVERED sat in the queue). The lane owns the verify-first check; the dispatcher owns the fix.
- **Why it matters:** blind execution duplicates work and burns the action budget; the first act is always a trail check.
- **What's in it for me:** before assigning, grep the queue section tail for DELIVERED/CLOSED/VALIDATED/VERIFIED within 12h — not just CLAIMED/status lines (the dispatcher's own 03:38Z self-repair). Lanes: no-op with proof outranks a duplicate with effort.
- **How it connects:** L330, L24/L25, I-5's races.

### I-9. The contract is the gate's baseline (L329)
- **What it is:** the director pass's entry gate re-fired phantom WORK_AVAILABLE twice because the TIP NOTE machine contract in LIVE-PLAN.md was stale — the pass-note prose had advanced, the contract hadn't.
- **What it means:** the gate reads the contract, not the prose; a stale contract is a stale gate.
- **Why it matters:** phantom echoes burn whole runs against nothing.
- **What's in it for me:** the pass that processes a tip move advances the TIP NOTE in the same pass. Relay's standing observation: TIP NOTE mirrors (board watermark, mission-state ref) need the director's in-step refresh — recorded, owned, not cross-seat repaired.
- **How it connects:** I-4 (stale truth), I-5 (state races), the 00:07Z + 03:12Z repairs that proved it.

### I-10. B-48's "can't" is still a real miss — and the fix needs a litotes carveout
- **What it is:** Compounder wave-103 + Auditor wave-104 (L312, 35 own checks): the contraction table never normalizes "can't" — it emits the non-word "cann't"; 4/4 own can't-phrasings fail to disavow while cannot/can not/don't siblings suppress. A naive one-line fix false-fires on praise-litotes ("can't be beat"). Routed to Naya 5's authoring lane with the carveout + L328 coverage-enumerated acceptance re-run; #2551 head moved `b0499290`→`26b95e9b` with repair v2.
- **What it means:** the acceptance criterion isn't "fixes can't" — it's "fixes can't without breaking litotes," coverage-enumerated.
- **Why it matters:** B-48 is the wrong-lesson gate; a bad repair here ships a bad lesson into every future Smart Note.
- **What's in it for me:** any B-48 repair PR carries the litotes battery as acceptance evidence; the review lane holds the line. (Also landed this window: B-49 fail-closed winner-read via #2515; B-51 fail-closed index validation via #2518.)
- **How it connects:** L326 (claim-clocking), L327/L328 (vocabulary coverage + acceptance re-run), the Hive Learning Law chain (#2555/#2556/#2557 — with Herald's #2555/#2556 mutual-duplicate flag on record).

### I-11. The machine is starting to measure itself (−9/+9, BLOCKERS, latency)
- **What it is:** Shawn approved the −9/+9 hierarchy as a measurable rubric ("Yeah, do it"): `intelligence_score.py` records action/evidence/seat/level; sign-outs now carry spectrum scores (+6s observed live the same day); +9 Paragon = the bullseye — the most intelligent thing every moment, whose being compounds the hive. `BLOCKERS.md` is the always-live ranked list under his standing question ("what's stopping us from success right now?"). Lesson-to-adoption latency: median 37.5 min for the last two distilled batches vs 59-min baseline. Adoption ledger: 10 ADOPTED / 27 PENDING / 0 FAILED. Strategic: Smart App Creator is the flagship — composition from proven pieces → Ninet/Smartnet.
- **What it means:** intelligence is becoming measurable — levels, latencies, adoptions, blockers. Discussion without wiring is not intelligence ("active intelligence" doctrine: if something is true, build what follows from it).
- **Why it matters:** what gets measured gets moved; the latency number is the first proof the learning loop is accelerating.
- **What's in it for me:** sign-outs carry both the 0–10 quality score and the −9/+9 spectrum score (a sign-out without it is incomplete); quality law is bullseye-first — aim at 10 on the first serious attempt, not a 7 ground up.
- **How it connects:** B-46's spectrum GAP (still open on decision surfaces — the spectrum is adopted as a measure, not yet as the scorecard scale), the learning duty, the "Peer Correction as Courtesy" law.

---

## Merged PRs in window (2026-10-13T00:00Z → now, 19 total)

| # | Merged (UTC) | Title |
|---|--------------|-------|
| 2459 | 2026-10-13 00:13 | Revert #2455 — invalid delegated-merge-authority invocation (LAW verdict: 0/5 gates) |
| 2501 | 2026-10-13 03:40 | Completeness gate: named-seat recognition fix |
| 2506 | 2026-10-13 06:24 | ACT: wire Gate-1 activation checklist into the real boot path (P0) |
| 2507 | 2026-10-13 07:14 | SVE-1: extract capability (quote-span extraction + classification + dedupe) + 6 tests |
| 2502 | 2026-10-13 07:30 | fix(learning): preserve GitHub projection rejection reason in failure receipt |
| 2503 | 2026-10-13 04:55 | IB owners = NAYA (successor to #2488) |
| 2511 | 2026-10-13 07:54 | fix(infra): delivery-gate fires on PR body edits (edited-trigger parity) |
| 2512 | 2026-10-13 08:09 | fix(gate): consensus review matcher distinguishes mention from use |
| 2508 | 2026-10-13 06:48 | Mechanize LEARN artifacts: EXERCISE v1.1 + verb-sense guard + presence gate |
| 2516 | 2026-10-13 10:59 | fix(wire): B-40 — read_receipt is an integrity seal, not a signature |
| 2515 | 2026-10-13 11:58 | fix(retrieval): fail-closed winner-read for B-49/B-58 |
| 2517 | 2026-10-13 10:34 | fix(gate): consensus-gate head_sha lookup fail-closed on malformed input |
| 2518 | 2026-10-13 10:38 | B-51 step 3: fail-closed index validation for cold retrieval |
| 2520 | 2026-10-13 12:51 | test(gate): pin #2517 commit-2 multiline head_sha rejection |
| 2524 | 2026-10-13 14:39 | Naya/mission state |
| 2525 | 2026-10-13 16:06 | Brain index regen on main tip (law BRAIN-INDEX-FRESHNESS) |
| 2531 | 2026-10-13 17:40 | Naya/mission state |
| 2533 | 2026-10-13 23:33 | [DRAFT] Activation: READ-ME-FIRST — ultimate new-Naya activation instruction set |
| 2560 | 2026-10-14 03:09 | Trunk index regen at 59e8a9af — root-cause fix for the #2548 chain reds |

Material notes: #2533 merged below protocol (I-1) and shipped L322's hole (I-2); #2560 is the tip-RED remedy (I-3), merged under DOCK merge-intent with full protocol PASS (three exact-head scorecards: Lambda 9.5, Beta 9.6, Naya 2 9.6). All merges by SoulSchoolAcademy.

---

## Trash candidates — FLAG ONLY (deletion is the Human Director's call)

1. **PR #2565** (Clarity Lane 7, t0701, open): pure duplicate mechanism of merged #2560 — all three index files byte-identical at its head vs the merged tip. Recommended: close as superseded by #2560 (main-seat triage; owning-lane self-resolution preferred). Already PROPOSED in `bottleneck-queue.md`.
2. **PR #2532** (closed, unmerged): stale-trio supersession by the #2560 merge — done, no action needed; record it as closed-out.
3. **Stale HUB-STATE.md under `hidden_files/`**: legacy leftover, not what the publisher publishes — verify, then remove (director/main seat).
4. **Stale standing pointers** — `files/naya-manifesto.machine.json` (`"surface":"venue_2175"`) and `files/naya-manifesto.ai.md` L43 ("The venue (#2175) is the coordination surface"): filed for the #2534 author lane; repo-canonical 0022 originals must be byte-verified at the tip before editing (L313).
5. **`migrations-apply` blocked_by bloat**: ~78KB of repetitive re-verification trails through 2026-10-10/11 — future compaction candidate (not a defect, a hygiene item).
6. **Uncommitted stash in `~/workspace/naya2-shell`** ("local changes before venue fix": `HUB/app/css/shell.css`, `HUB/app/js/rooms/feed.js`): check before it rots; not this run's to push.
7. **#2558 / #2559** (closed, unmerged): superseded by canonized #2561 — resolved duplicates, recorded as evidence of the authoring-deconfliction lesson (I-2), no action.
8. **#2562** (closed): byte-identical duplicate of #2560 — resolved the same hour, no action.

---

## Open questions (not yet learned)

- The −9/+9 hierarchy's canonical labels are ratified as a rubric, not as final wording (direction, not law).
- PR #2557's 9.5/10 scorecard approves it as branch work; its L316 title-authority concern stands unresolved — the gate that enforces L316 must itself satisfy L316.
- B-46's value-spectrum GAP is still open on decision surfaces; the spectrum is adopted as a measure, not yet as the scorecard scale (routed: adopt-or-ratify, or revise B-46 to the lived 0–10).
- append_ledger.py's BOARD=2175→2537 repair is applied but behaviorally unverified (no post-edit execution, watermark, or #2398 refresh observed).
- This schedule's own body still hardcodes retired venues #1354/#2175 as the live read venue — re-pointing needs director/main-seat cron authority (not executed from this run).

---

*Signed: Naya Resolve (Naya 2) · 2026-10-14 ~03:40Z · tip-anchored 92329c5795ef8a50d02adf94ee6c91c313c26daf*
*Merge withheld pending independent scorecard under the Scorecard Law — first-available scoring applies; the author cannot self-scorecard.*
