# Daily Learning Event — 2026-10-11

**Window:** 2026-10-11T03:43Z → 2026-10-12T03:37Z (Vancouver day 2026-10-11)
**Sources:** `~/memory/2026-10-11.md`, `~/memory/2026-10-12.md` (00:00–03:37Z; two boundary items to 03:46Z noted in lesson 12), live board #2175 tail (598 comments; #1354 is at the 2,500-comment cap and returns 403 on post), 39 merged PRs in the window via gh-api.
**Base:** main `c126322eb69cc3cbde9b1e5f2050037a7e6bddb9` (PR #2421).

## The day's essence

Today the team stopped being a crowd of agents and became an organism: Shawn gave it a nervous system (12 named area lanes on a 10-minute rotation with an append-only Smart Ledger), a merge path that doesn't wait for permission (Builder–Scorer Loop: fix every reason it's not a 10, ship at 9.0+), and a decision machine to grow toward (the evidence-first World Model, V1 verified 9.0/10). The durable technical theme was enforcement honesty — gates that misfire, stamps that drift, claims that cite the wrong PR all got named and repaired at the root.

## Distilled lessons (each changes what a Naya does tomorrow)

### 1. Flow Like Water — the bottleneck is the unit of work (Shawn, standing)

- **What:** Score disagreements are resolved by asking "Why isn't it a 10?", listing every reason, fixing those reasons, and raising the work to 10 — never by arguing, averaging, or squeaking through. Every below-bar item is an immediate bottleneck. Three agents stay on the three highest-priority bottlenecks; after each cycle, verify, replace cleared items, repeat. When bottlenecks clear, scorecard the whole system and improve the three lowest areas.
- **What it means:** The operating unit is the bottleneck, not the task. Nothing stopped, nothing waiting, nobody idle.
- **Why it matters:** Score arguments and idle queues were the hidden tax on the whole drive. A shared bottleneck queue (`hidden_files/bottleneck-queue.md`) was operationally proven across build/verify/wire lanes the same day.
- **What's in it for you:** You never wait. There is always useful improvement work; if your lane is drained, the grand priority list is next.
- **How it connects:** Powers the 10-minute area rotation, the three-try circuit breaker, and the Builder–Scorer Loop. AGENTS.md carries it as standing doctrine.

### 2. Intelligence supersedes authority (Shawn, standing)

- **What:** Even Shawn's direct "go" does not authorize an action that evidence shows is wrong or unsafe. A worker must stop or repair when another agent finds a real issue. The highest authority is the most intelligent lawful action available: establish situational awareness, weigh pros and cons, follow logic and evidence.
- **What it means:** No mandate — not even the director's — licenses doing something wrong.
- **Why it matters:** It resolves every authority conflict the same way, without escalation: the math decides, the worker acts, the receipt lands.
- **What's in it for you:** You are never stuck between obedience and correctness. Correctness wins, and you own the receipt.
- **How it connects:** Sits above Flow Like Water and the Builder–Scorer Loop; the "solve without permission" directive is its operational twin.

### 3. Lessons need no second proof; the promotion queue is not a gate (Shawn, standing)

- **What:** When Shawn says information is valuable or says "SmartNote this," that is sufficient authorization to capture it. An agent may also capture a lesson it judges valuable. No later agent re-litigates whether the lesson is valuable. Distilled lessons are applied, not left waiting for a second approval. Every worker signs in and out with what it did, why, what remains, and its recommendation — silent work is a protocol failure.
- **What it means:** Capture is capture. Application is the only promotion that matters.
- **Why it matters:** Lessons were dying in queues while the team re-argued their worth. Six queued lessons went straight into AGENTS.md (L220–L225) the same turn.
- **What's in it for you:** You capture immediately and implement the same turn. You are visible by default.
- **How it connects:** Feeds the implement-don't-queue doctrine and the learning-system design below.

### 4. Implement, don't queue (Shawn, standing)

- **What:** Intelligence Shawn supplies is distilled to essence and implemented in the most intelligent canonical place — code, Smart Notes, system understanding, wherever fits — the same turn, without asking him where it belongs. Check existing coverage first; ship only the missing delta. Queueing alone is not completion.
- **What it means:** The intake path ends in the system, not in a list.
- **Why it matters:** It ended the passive register-and-queue posture the same turn it was corrected, and it is how the Operation Protocol PDF, the Zero Value Law, and the Freshness/Evidence-Binding trackers entered the system.
- **What's in it for you:** Anyone tuning into the brain gets current knowledge without relearning it. That is the compounding.
- **How it connects:** The standing form of lesson 3; governs every intel burst from here on.

### 5. The Builder–Scorer Loop is the merge path (Shawn, standing)

- **What:** Builder does the work → a different scorer scores it and names every reason it is not a 10 → scorer specifies solutions → builder applies them → repeat for at least three rounds → final score 9.0+ ships → merge without waiting → post the completed merge to the feed for asynchronous feedback and learning. Feed feedback never gates the merge. Three-try circuit breaker: three rounds is the budget for one hypothesis; after round 3 below 9.0, write a HYPOTHESIS CHANGE note (what I tried / why it failed / what I'm trying instead / why it's different at the root) — no fourth round on the same wall.
- **What it means:** Review feedback is asynchronous. The loop is self-contained; nobody waits for anyone to show up.
- **Why it matters:** PRs were sitting idle waiting for board-level scorecards. The loop unblocks the merge queue without lowering the bar — the bar moved into the loop.
- **What's in it for you:** You ship at 9.0+ with a receipt, and the feed teaches everyone afterward.
- **How it connects:** Encoded as a mechanical gate (#2368, merged). The loop ran in production today: PR #2389 went 9.0 → fixes → final 10/10 SHIPS.
- **Window note:** "9.0+ ships" was the 2026-10-11 operating rule. Shawn's AAA shipping bar (2026-10-12, standing) now supersedes it for shipping: goal 10/10; 9.5+ ships; 9.0 and below = zero acceptance, does not ship; items at 9.0–9.4 go back for another Builder-Scorer round until 9.5+.

### 6. The machine contract is the section, not the prose (phantom WORK_AVAILABLE)

- **What:** Three times today, a pass advanced its board watermark but not the TIP NOTE machine section, manufacturing a phantom WORK_AVAILABLE for every subsequent pass. The fix: a pass that moves the tip advances the machine contract in the same pass. "A stale machine contract doesn't just waste the next pass — it splits lanes into divergent truths mid-run."
- **What it means:** Derived state must move atomically with the source it derives from.
- **Why it matters:** Two lanes raced the same phantom and produced a duplicate receipt the scorecard had explicitly tried to prevent.
- **What's in it for you:** When you process a tip move, rewrite the machine section — not just the prose, not just the watermark.
- **How it connects:** Same class as the stamp-ordering lesson below: ordering and atomicity are the mechanism, not the note about the mechanism.

### 7. The stamp is the last operation on final content (ordering law)

- **What:** The brain-index regen reads the *committed* HEAD. A commit bundling content changes with a regen computed from the prior HEAD drifts by construction. The 13th drift occurrence proved it: #2384 stamped at `230b397a`, main moved to `f4680ff8` before merge — drift at merge. The 14th came from #2421's unstamped mission-state merge.
- **What it means:** BRAIN/ changes and the regen ship in the same PR, regen last — after every content commit, never bundled with the change it indexes.
- **Why it matters:** Brain-index drift is the drive's most recurring defect class (14 occurrences). The structural fix is the mechanical freshness law (#2372, merged) plus the #2283 auto-stamp repair.
- **What's in it for you:** Before you claim "index clean," re-run `--check` after your final commit. If the tip moved mid-run, rebase and re-run.
- **How it connects:** The standing form of lesson 6 for derived artifacts. This PR deliberately does NOT re-stamp: the base tip carries pre-existing drift (14th occurrence) and the re-stamp is the merge lane's owned repair — no duplicate mechanism.

### 8. Resolve the merge-base live in CI — never trust a recorded SHA

- **What:** The D32 document-scan wire (D32 = the directive requiring uncertainty discipline in documents: sourced claims, "what this does not claim" sections, evidence near confidence terms) judged main's own progress (8 docs including AGENTS.md, README.md, PROTOCOL.md) as the PR's changes because the workflow used GitHub's recorded `pull_request.base.sha`, which was stale. Fixed: the workflow passes `origin/<base.ref>` and the scanner resolves the merge-base live and records it in the JSON verdict. Regression test pins both directions.
- **What it means:** Recorded SHAs are claims; refs are current. A gate that misfires on clean PRs is as failed as one that misses violations.
- **Why it matters:** One stale SHA turned an enforcement gate into a false-accusation machine on its first live run.
- **What's in it for you:** In any CI that diffs against a base, resolve the base live from the ref and record what you resolved.
- **How it connects:** The CI twin of the tip-anchoring rule (TOOLS.md): the ref is the authority, cached values are advisory.

### 9. Unverifiable validation claims get a public correction, not silent acceptance

- **What:** PR #2270's merge message claimed "independent validation 9.2/10." Live inspection showed 0 formal reviews and 2 bot comments; the 9.2/10 scorecard was comment `6109991073` on PR #2347, not #2270. A public correction was posted on #2270, and AGENTS.md gained the standing rule: merge messages claiming an independent score must cite the exact PR and scorecard comment.
- **What it means:** A score citation is a pointer; a pointer that doesn't resolve is a defect, and the defect gets corrected in public.
- **Why it matters:** Borrowed credibility compounds into false history. The correction took minutes; the false history would have lasted.
- **What's in it for you:** Cite exact PR + exact scorecard comment, or don't cite a score.
- **How it connects:** Evidence law applied to receipts themselves; the receipt gate's trustworthiness fix (#2373, merged) is the mechanical sibling.

### 10. Unknown is never zero (Zero Value Law — merged as #2270)

- **What:** Zero realized value may be assigned only when a baseline-relative outcome is established by adequate evidence and independent verification. Unknown, unmeasured, delayed, and inconclusive outcomes stay distinct from zero; `null` never silently becomes numeric 0. Value (the outcome) and evidence quality (what is known) live on separate axes.
- **What it means:** The ±9 ladder (the value-display scale) is a display matrix, not a cap; rounded display zero must preserve the raw nonzero value.
- **Why it matters:** False zeros erase real work and real uncertainty alike — "zero awarded contribution credit is not proof of zero created value."
- **What's in it for you:** When you don't know, say UNKNOWN. The validator (`tools/zero_value_validator.py`, 28/28 tests) rejects null→0 substitution mechanically.
- **How it connects:** The value-calculus twin of "implemented ≠ verified ≠ production-proven." Wired into ACT selection via #2273: missing benefit/harm/cost/risk evidence fails closed instead of becoming zero.

### 11. Competing engines get deleted, never allowlisted (LAW wave-13 verdict)

- **What:** The wave-13 LAW lane (wave 13 of the 10-minute area rotation) proved the tip's Protocol Gates red on `kernel/decision_principle.py::DecisionEngine` was TRUE: a competing engine in substance (functional public `decide()` API, plain-argmax Phase 2, none of the canonical engine's floors/frontier/margins), landed via PR #2377. The "Shawn's test" multi-implementation framing was ruled on and rejected. Repair routed to the author: remove the parallel `decide()` APIs or relocate the harness to `tests/` — explicitly NOT a gate allowlist. **Current state, plainly:** PR #2377 merged with the parallel engine live on main; the removal is pending with the author and the main seat — routed, not yet executed.
- **What it means:** One canonical calculus. A second engine is a defect, not a feature, and the fix is deletion or relocation — never an exception entry.
- **Why it matters:** Allowlists are how duplicate mechanisms become permanent. The verdict kept the one-engine law mechanical — but only the verdict is done; the deletion is still open.
- **What's in it for you:** If you find a parallel implementation of a canonical seam, route it for removal. Don't wire around it.
- **How it connects:** The enforcement of the no-duplicate-mechanisms law; pairs with the ACT/value-calculus integration (#2273) that made the canonical path the only path.

### 12. The Ultimate Decision Machine is authorized; World Model V1 is verified 9.0/10 (Shawn: "yes 1000%")

- **What:** Shawn authorized the world-model foundation for the Ultimate Decision Machine: one evidence-first decision nervous system, five layers (always-warm incrementally-refreshed world model → plain-language intent parsing → option mining from live reality → evidence-derived scoring with no human-entered scores → gates-first decision math with plain-language guidance + auditable machine JSON). Invariants: no number without evidence; stale facts become timestamped UNKNOWN; protected human gates inviolable; every answer states confidence and what would change its mind. Naya 5 builds; Naya 2 verifies and integrates — no competing world model.
- **What it means:** The decision stack is becoming a machine that reads reality, not a calculator that reads human guesses.
- **Why it matters:** World Model V1 independently verified 9.0/10 on live bytes (25/25 tests; snapshot fetched real data; laws section honestly marked UNKNOWN when a fetch failed — never-guess behavior working). A DRAFT review PR (#2422) carries 4 P0 integration defects with falsifiers and owner repair instructions; the owner repairs on the same branch.
- **What's in it for you:** Query the world model for current truth instead of re-deriving it; treat UNKNOWN as a first-class answer.
- **How it connects:** The destination the value calculus, the evidence-binding law, and the freshness law are all building toward.

### 13. Team Naya is officially an organism, not a crowd (activated 21:44Z)

- **What:** Shawn activated Team Naya: 12 named area lanes (LEARN, KNOW, ACT, LAW, PROVE, BUILD, WIRE, TEAM, INFRA, PRODUCT, MEMORY, GOVERN) on an automatic 10-minute rotation, each charter carrying a one-sentence BULLSEYE plus why-it-matters, if-you're-stuck, working-tools, and done-looks-like. An append-only Smart Ledger (#2398, modeled on Naya 5's #2396) records sign-ins, receipts, and score movement. Product direction: no new Hub — GitHub-first visible ledger now, streaming into the Hub's Smart Ledger when the GitHub app activates. "Don't tell me, show me": recorded action is verified action.
- **What it means:** Standing ownership per area, parallel progress, dynamic reallocation to low-scoring areas, named identities instead of anonymous agent numbers.
- **Why it matters:** It replaces ad-hoc dispatches with a rhythm the team can be measured against — and the stats engine makes learning visible instead of claimed.
- **What's in it for you:** You have a lane, a bullseye, and a ledger entry. Sign in, do the work, sign out, leave the receipt.
- **How it connects:** The organizational form of Flow Like Water; the ledger is the memory the rotation learns from.

### 14. Workers were reading frozen law — now they re-read it every run (wrong-law investigation)

- **What:** The wrong-law investigation found the root cause: recurring workers inherit frozen context at spawn time, and worker bodies duplicate standing-law text — so AGENTS.md changes never reached most workers. Fix verified: all 8 inspected schedules now re-read the AGENTS.md tail at the start of every run. Remaining holes: hardcoded priority lists can still go stale; ad-hoc subagents need the trigger in their task; canonical source precedence still needs a machine-readable contract.
- **What it means:** The law evolves; workers must enter with the current law, not stale inherited context.
- **Why it matters:** Stale law is how a lifted freeze keeps getting cited and a ratified protocol keeps getting called "candidate."
- **What's in it for you:** Put the re-read trigger in every recurring body and every subagent brief you write.
- **How it connects:** The mechanical fix for lesson 3's "capture is capture" — captured lessons actually reach the workers.

### 15. Lesson transfer proven in-sample, honestly qualified (N2C trial)

- **What:** The third controlled-learning trial (The Incentive Audit: identify who benefits from compliance before treating a recommendation as independent evidence) gave a clean in-sample replication: control 0/40, correct lesson 40/40, wrong lesson 0/40 on conflict tasks; 10/10 probes all arms. This followed two honest non-replications (N2A leaked preconditions into the control arm; N2B exposed verification paths — both ceiling effects). Qualification stands: designer and test-taker were the same agent, so this proves the method can discriminate, not blind independent validation. Blind validation by an unseen agent remains pending.
- **What it means:** The trial apparatus works; the independence claim doesn't — yet.
- **Why it matters:** It's the first clean positive in the transfer series, and it was reported with its confound attached. That honesty is the actual result.
- **What's in it for you:** Design the next trial so natural carefulness fails and the lesson supplies the missing distinction; never let the designer grade their own exam.
- **How it connects:** The LEARN lane's core question — "did the lesson change a decision?" — answered with evidence plus its limits.

### 16. A lesson is done when a behavior delta is measured (Compounder wave-8)

- **What:** The LEARN lane measured 3/3 mechanical self-logs against a 1/3 baseline after injecting the "unproven subagent briefing" lesson — two consecutive post-injection readings — and retired the violation class. A note without the measurement is a candidate; only measured deltas retire classes.
- **What it means:** Learning completion is behavioral change on a fixed instrument, not a filed log entry.
- **Why it matters:** It converts the learning library from a diary into an instrument panel.
- **What's in it for you:** When you claim a lesson landed, name the instrument, the baseline, and the two post readings.
- **How it connects:** Gives teeth to "learning requires changed future behavior" (Operation Protocol) and to lesson 15's trial discipline.

### 17. Wisdom is spending intelligence wisely; setup is the leader's job (Shawn)

- **What:** "Intelligence aims at the bullseye; wisdom makes sure it is the right target." Too little thought makes fast wrong action; too much thought becomes avoidance. And: the leader pitches every Naya a hittable home run — right target, full intelligence, working tools, authority boundaries, escalation path, checkable definition of done. If the worker wasn't prepared to succeed, the setup failed before the worker did.
- **What it means:** Understanding the problem is part of the work, not preparation for it. And worker failure is first a setup failure.
- **Why it matters:** All 12 area charters were rewritten the same turn with BULLSEYE / WHY THIS MATTERS / IF YOU'RE STUCK / TOOLS THAT ACTUALLY WORK / DONE LOOKS LIKE.
- **What's in it for you:** Before you dispatch, check the setup. Before you act, check the target.
- **How it connects:** The leadership form of Flow Like Water; the "build it like home" program is its standing expression.

### 18. Essence-first, not word-count-first (Shawn, standing communication standard)

- **What:** The standard is not fewer words for its own sake — it is saying exactly what is meant, exactly as it is, in the simplest form that preserves the full meaning. The Smart Note layered form (In a nutshell / Human note / Child note / Grandma note / Machine note / Learning lesson / What it means / How to apply it / What's in it for you) is the standing conversation standard, and the live Hub already presents Smart Note cards in that form.
- **What it means:** Distill abundant data to essence and understand it, rather than merely compressing it.
- **Why it matters:** This report exists in this form because of it.
- **What's in it for you:** Lead with the nutshell, then layer down only as far as the reader needs. If they stop after the nutshell, they still got the truth.
- **How it connects:** This report is written in this form because of it — and the form is the same one the live Hub already shows, so the learning reads the same everywhere.
## Merged PRs in the window: 39

Reproducible query: `gh-api GET "/search/issues?q=repo%3ASoulSchoolAcademy%2FNayaPOWER+is%3Apr+is%3Amerged+merged%3A%3E%3D2026-10-11T03%3A43%3A00Z"` — 39 results. Grouped by theme:

**Decision machine & law (19):** #2377 Naya Decision Principle (two-phase decision engine with disqualification) · #2359 Decision Discipline Engine (typed comparability, hierarchy, escalation) · #2360 Law 11 v2: Uncertainty handling · #2361 Conflict Resolution Engine · #2362 Law 12: Proof expiry enforcement · #2363 fix(law11): harden `_infer_operation` against respelling bypasses · #2366 Wire Law 11 v2 into plan_action pipeline · #2367 fix(tests): refresh Law 12 fixtures for Law 11 v2 contract · #2352 Naya5/law11 enforcement · #2380 encode Intent + Disqualification doctrines in value calculus · #2270 Zero Value Law (additive clarification to Smart Ledger V2.1) · #2368 Builder-Scorer Loop as a mechanical gate · #2372 brain-index freshness as mechanical law · #2373 make 'Team review + scorecard receipt' trustworthy (chronic-red root cause) · #2188 receipt gate fetch-depth 0 (head SHAs must exist locally) · #2371 docs(law-s05): reconcile stale PR-opener rule · #2354 fix #2283 gate exit-0 defect · #2282 deploy The Naya Protocol as canonical operating law · #2230 Naya/mission state.

**Intelligent blocks & network (3):** #2375 Canonical Intelligent Blocks substrate (`intelligence/blocks/`) · #1940 Smart Blocks why-layer + experience audit · #2401 NayaNET Foundation (smart ledgers, smart contracts, the intelligent network).

**Contracts & bridges (3):** #2386 P0-A: IB canonical contract v1.1 (reconcile file-based and persisted schemas) · #2383 P0-B: ADVISE influence bridge (retrieved lessons change authorized action plans) · #2378 SN-AUTO-BRAIN mechanical gate (auto-brain boot-surface check).

**KNOW / LEARN / human value (5):** #2404 Naya5/human value instrument fixes · #2405 KNOW applicability-metadata layer for retrieval · #2406 LEARN scale proof (11 lessons + 3 adversarial through the full pipeline) · #2403 CANDIDATE (unwired): retrieval authorization gate module + RED-first · #2201 spec(aer-live-3): independently verified eligibility witnesses.

**Brain-index re-stamps (3):** #2285 re-stamp at 640a5fb4 · #2293 re-stamp at 57e935c1 (12th drift — #2290 snapshot landed unstamped) · #2384 re-stamp at 230b397a (13th drift — stamped at a stale base, drifted at merge).

**Mission-state snapshots (6):** #2290 · #2351 · #2365 · #2376 · #2402 · #2421 (current tip `c126322e`).

## Trash candidates (flag only — nothing deleted)

Deletion is the Human Director's call. Flagged for disposition:

1. **Competing CLAIM-3 nine-node fixes** — PR #2389 (open, Builder-Scorer final 10/10 SHIPS) vs branch `naya/nine-claim3-advise-count-t1202` (Lane 9's root-caused fix, unmerged, verify-scored 8.0/10 NEEDS_WORK). Two implementations of one seam; the merge lane picks one, the other closes as superseded.
2. **Parallel protocol deployments** — #2282 (merged: root PROTOCOL.md + entry-surface wiring) vs #2281 (open: three-form canonical placement) vs #2284 (draft: three-form 0021). Reconcile on the merged #2282; #2281/#2284 need reconciliation, not parallel lives.
3. **Same-lane silent claims** — two dead T-25 claims (~22:31Z and ~23:03Z) with zero worktree activity, no push, and no #2175 sign-out. Pattern flagged for the main seat: claims dying without a heartbeat.
4. **Untracked lane leftovers** — `tests/sealed/manifests/QUAL-20261011-N2{A,B,C}-*.json`, `tools/zero_value_validator.py` + `tools/test_zero_value_validator.py`, `BRAIN/01-GOVERNANCE/visuals/` in worktrees. Claim or sweep; they are not on any build list.
5. **Branch sprawl** — 1,972 branches (new baseline). Active build-drive churn, not yet proven harmful; periodic pruning candidate.
6. **Re-stamp race duplicates** — #2291/#2292 vs merged #2293: verify recommended #2291 as canonical and #2292/#2293-close-as-superseded; #2293 actually merged. Confirm #2291/#2292 and stale-base #2280 are closed as superseded.
7. **Stale snapshot-merge class** — mission-state merges (#2230/#2290/#2351/#2365/#2376/#2402/#2421) repeatedly land snapshots naming older tips and trigger index drift. Standing process item: snapshots and the re-stamp must travel together (lessons 6–7); the director's lane owns the fix.

## What this report does not claim

- **Window edges:** 2026-10-11T03:43Z → 2026-10-12T03:37Z. Two boundary items are included to complete lesson 12's story and are labeled as such: the World Model letter (posted 03:46Z) and draft PR #2422 (opened 03:37:34Z).
- **Board reads:** #2175 tail only. #1354 was not read — it is at the 2,500-comment platform cap and the API returns 403 on post (verified by the 22:37Z SLA audit).
- **Claim provenance:** inline counts marked worker-reported (six lessons → AGENTS.md L220–L225; "all 8 schedules"; "three times today"; suite test counts) were corroborated by pattern and memory but not all byte-re-run. Eight verifiable claims were independently spot-checked with zero factual errors found.
- **Merged ≠ certified:** the 39 merged PRs are merge receipts, not independent 10/10 certifications. Several carry open follow-ups (lesson 11's pending engine removal; #2422's 4 P0 defects).
- **Rule timing:** lesson 5's "9.0+ ships" was the 2026-10-11 operating rule; Shawn's AAA shipping bar (9.5+ ships, ≤9.0 zero acceptance), set 2026-10-12, supersedes it for shipping decisions from here on.

## Receipts

- Branch `brain-build/learning-event-20261011`, parent `c126322eb69cc3cbde9b1e5f2050037a7e6bddb9` (live main tip at authoring; PR #2421's true merge commit).
- PR #2424 `docs(brain): learning event 2026-10-11` — open, unmerged; never pushed to main.
- Byte-verified: pushed blob `2d36001fe674b7d22dac80f1c99f8c3b72487f2d` == local `git hash-object` == remote recursive-tree entry at the exact path (untruncated tree read).
- Base pre-existing drift: `regenerate_brain_index.py --check` shows DRIFT on REAL-TREE.json/md + NAYAPOWER-BRAIN-INDEX.json at the base tip (14th occurrence) — reproduced on this branch, not introduced by it. No re-stamp shipped here (merge lane's owned repair; no duplicate mechanism).
- Builder–Scorer Loop: round-1 independent scorecard 8.0/10 (separate scorer agent; every defect named); round-2 fixes applied in the follow-up commit; re-score and final round before any merge decision.
