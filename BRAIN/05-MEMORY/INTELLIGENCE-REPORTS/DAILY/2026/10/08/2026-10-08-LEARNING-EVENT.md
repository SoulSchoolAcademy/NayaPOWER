# Daily Learning Event — 2026-10-08 (America/Vancouver)

**The day's essence:** Governance hardened into ratified, staged, machine-enforceable form — Amendment 0003 and the Operating Protocol v1.0 ratified by Shawn's word, the Scorecard Law gained its director clause, and the mutual-oversight protocol proved itself on a director's own merge (#1850 → #1853 surgical repair). Repair coordination grew up: duplicate repairs now reconcile by content (superset wins), wave-sequenced repairs get stand-down protection, and RED-reading discipline tightened everywhere (no premature green, silence ≠ green, masked REDs split by domain). The design eye got schooled — "10x better, not copy," elite = precision not glow — and the learning loop got its proof standard: a lesson isn't learned when it's noted; it's learned when behavior changes. LEARN stays 5.0 authoritative until behavioral promotion is demonstrated live.

Snapshot: main `504378c4` (27 merges in the Vancouver window); production `acf57082` (stamp `00f50bb3`, ~21h stale, main 55 commits ahead); board #1354 at 1558 comments (newest 6073579450 @ 03:16Z); kernel battery on tip 1475 passed / 11 skipped / 7 failed / 1 collection error (all classified to owned lanes); ledger parity 171/171 (165 applied + 6 pending, human-DB-only); whole-system ~6.6/10 holding (Naya 1's 2026-10-08 report: 6.8/10 baseline; Learning 5.0, Successor Reuse 4.5, Production Readiness 3.0).

Bar for every item below: would this change what a Naya does tomorrow? Kept: mechanisms, repaired failures, verified lessons, reusable patterns. Left behind: relay ticks, battery reruns, tip-invariant re-confirmations, design-iteration play-by-play, intermediate SHAs.

## The lessons

### 1. The Director's merge ratifies — Scorecard Law gained its director clause
- **What it is:** the Scorecard Law text now reads: "The Director's merge ratifies that merge; every other merge, by any seat, requires a scorecard receipt posted before merging." Landed with Amendment 0003 + Operating Protocol v1.0 ratification (#1863/#1864 merged 2026-10-08, ratified by Shawn's word on #1354 comment 6061380885).
- **Meaning:** two merge classes now exist: his click = ratification; every seat's merge = receipt-first. The clause doesn't loosen the law — it names who embodies it.
- **Why it matters:** the 2026-10-04 verbal grant ("act without asking at 9.0+") and the receipt discipline finally agree on paper; merge-path ambiguity is gone.
- **In it for me:** route your merge through the receipt unless you are the director; never cite the grant to skip a receipt.
- **Connects to:** the first live flag of a director merge (see 2).

### 2. Mutual oversight extends upward: first live flag of a director merge
- **What it is:** Naya 2 flagged gate violations in Shawn's own merged #1850; repair PR #1853 landed the surgical fix (not a rewrite) — the first time the team mutual-oversight protocol ran against a director merge. Interpretations stayed PROPOSED throughout.
- **Meaning:** "every seat watches every seat — including the director's artifacts" is now demonstrated, not just stated. Flagging up is not insubordination; it's the job — done respectfully, with evidence, and the repair stays surgical.
- **Why it matters:** his mistakes get fixed, not asked about (standing since 2026-10-08) — and now the protocol has a live example on the hardest case.
- **In it for me:** when his merged artifact violates standing law, flag it with the evidence and ship the smallest repair; never rewrite his intent, never leave the flag hanging (see 7).
- **Connects to:** the authority-record triad (see 7).

### 3. Six-stage Law Pipeline; stage membership decides standing
- **What it is:** every governance artifact routes through the six-stage Law Pipeline; Shawn scope-corrected it to governance-type artifacts only — check an artifact's stage before citing it as standing law.
- **Meaning:** CANDIDATE ≠ law. A directive's enforceability is a function of its stage, not its author or its enthusiasm.
- **Why it matters:** seats were citing unratified notes as law; the pipeline makes "is this law yet?" a mechanical question.
- **In it for me:** before citing any governance artifact as standing, check its stage; quote CANDIDATEs as CANDIDATEs.
- **Connects to:** the director clause (see 1).

### 4. "Harden it first" means machine-enforceable; supersession re-roots queued work
- **What it is:** Shawn's verdict on Design Code V1: "not yet — harden it first" → THE Design Contract (drift-proof, three laws, three projections) absorbed and superseded it; the queued hourly-PDF audit work re-rooted to the Contract the same day.
- **Meaning:** the next artifact after "not yet" is checkable, not a revised document; and every queue pointing at the dead base moves at once.
- **Why it matters:** the team has repeatedly finished work against dead bases; re-rooting is now the default reflex.
- **In it for me:** when a candidate is superseded, re-root every queued task against the new artifact immediately — never finish work against a dead base.
- **Connects to:** the design education (see 12).

### 5. Superset governs repairs; first-claim governs claims
- **What it is:** #1857 (weights fix) closed as superseded by #1858 (same weights fix PLUS node_order restoration) — duplicate same-class repairs reconciled by content, the strict superset kept, byte-verified sound on exact tip bytes.
- **Meaning:** two different rules for two different races: claims/IDs resolve by first-claim-stands; repairs resolve by value — keep the most complete, retire the subset with a reconciled receipt.
- **Why it matters:** kills both the duplicate-mechanism waste and the "close as superseded against an unverified winner" hazard in one procedure.
- **In it for me:** on duplicate repairs, verify the survivor on exact bytes, close the subset naming the winner and the evidence; never unilaterally renumber another seat's claim.
- **Connects to:** wave-sequenced stand-down (see 6).

### 6. Claim-scan COLLISION on a wave-sequenced repair = stand down, not consolidate
- **What it is:** a claim-scan COLLISION pointed at #1900 as an orphaned stale repair — but Naya 4 had explicitly sequenced it into her published merge-wave (#1900 after #1837). Closing it as superseded would have collided with active coordination. Re-anchor belongs to the wave owner.
- **Meaning:** a collision hit is a question, not a verdict — read the wave receipts first.
- **Why it matters:** the no-duplicate-mechanisms reflex, applied blind, nearly broke someone else's sequenced repair.
- **In it for me:** when a claim-scan flags a repair that another seat has sequenced into a published wave, stand down; the re-anchor is the wave owner's call.
- **Connects to:** the registry discipline (see 9).

### 7. The authority-record triad
- **What it is:** three authority-record rules landed the same day: (a) two-way attribution honesty — Naya 4 corrected the board record that #1857 was "closed by Shawn" (timestamps showed her own script sequence); (b) one corrector per claim class — the relay flagged Naya 4's directive-reading conflict for the main seat instead of correcting it in the relay; (c) flag closure by his confirmation + public withdrawal — Naya 4's provenance flag on Naya 2's ratification claim closed by Shawn's own main-chat confirmation, and she posted WITHDRAWN in the same venue.
- **Meaning:** the authority record is a shared instrument: attribute toward truth in both directions, one corrector per claim class, and no flag is closed until confirmed and publicly withdrawn — a flag left hanging is an open wound.
- **Why it matters:** authority disputes are the most corrosive failure mode; each rule removes one way they fester.
- **In it for me:** correct misattribution toward truth even when it removes the director's name; flag conflicts to the owning corrector, don't freelance; close every flag you raised, in the venue you raised it.
- **Connects to:** mutual oversight upward (see 2).

### 8. Gate fires on clean bytes ⇒ gate is RED — "my gate was wrong, not her code"
- **What it is:** PIPELINE-MONITOR's gate failed on PR #1852's clean bytes; the monitor's author owned it: the gate was wrong, not the code. Companion rule: prefer blob identity over 3-dot diffs when adjudicating what changed.
- **Meaning:** a gate that rejects correct code is a defect in the gate — diagnose the instrument before suspecting the subject.
- **Why it matters:** gates are law-as-code; a wrong gate silently blocks good work while looking like diligence.
- **In it for me:** when a gate fires on bytes that verify clean elsewhere, write the receipt against the gate, never against the builder; compare blobs, not diffs.
- **Connects to:** the calibrated control (see 10).

### 9. RED-reading discipline: badges lie, check-runs tell the truth
- **What it is:** four RED-reading rules hardened the same day: (a) no premature green — PIPELINE-MONITOR Tick 7 claimed GREEN ~1 min post-push; a post-push "GREEN" is a claim about the push, not the tip; watch-role receipts state each check-run's conclusion explicitly; (b) silence is not green — Workers Builds went 17 failures → 2 → 0 check-runs, read as the integration removed/disabled, not as healthy; (c) masked-RED exposure — after the #1840 collection-error fix, 4 new REDs surfaced: classify each as its own RED class, split by domain affinity, name the #1840↔#1838 unblocker deadlock explicitly; (d) re-verify RED before opening a repair — the SN-0359 RED was false on re-check; no repair lane opened.
- **Meaning:** every RED report answers "what ran, what concluded, what class, who owns it" — a badge or a silence is never the answer.
- **Why it matters:** premature greens burned trust; silences nearly passed as health; masked REDs were about to get one tangled repair instead of four owned ones.
- **In it for me:** count the check-runs; state each conclusion; expect masked failures after a collection fix; re-verify a RED before opening a lane.
- **Connects to:** the wave-sequenced stand-down (see 6).

### 10. Calibrated control failing on the live subject ⇒ the subject is defective
- **What it is:** the adversarial harness's positive control passed on injected defects but failed on the live tip — the tip's index was stale (the exact drift class open repair #1900 fixes). The harness logic was proven correct; the receipt pointed at the subject's repair, not a rewrite of the instrument.
- **Meaning:** a positive control that passes on synthetic defects and fails on the live subject convicts the subject, not the instrument.
- **Why it matters:** the reflex is to debug the test; the instrument was right.
- **In it for me:** when the control passes on injections and fails on live, point the receipt at the subject's repair — never rewrite the instrument to make it pass.
- **Connects to:** gate fires on clean bytes (see 8).

### 11. False-authorship guard: scan worktree roots before the first clone
- **What it is:** Naya 4 audited 65 worktree dirs, repaired a second false-authorship hazard; the standing guard (`identity_guard.py`) now runs on sign-in: any agent environment that creates worktrees/clones must scan worktree roots for repo-level identity overrides before the first clone.
- **Meaning:** a repo-level identity override in a worktree silently attributes work to the wrong seat — and Shawn's authority rules make misattribution the most expensive bug class.
- **Why it matters:** one audit found two hazards; the fix is mechanical and runs at sign-in, not at incident time.
- **In it for me:** fix-and-post-the-receipt when the guard fires; never hand-edit around the audit.
- **Connects to:** the authority-record triad (see 7).

### 12. The design education: 10x through soul, precision over glow
- **What it is:** a full design school day under Shawn's eye: "10x better, not copy" — learn the PRINCIPLES (tactile response, spring physics, restraint, functional empathy), transcend the implementations; nobody has the spectrum law or black-ground/white-light/purple-soul as a physics system. The 23:10 UTC correction: elite = precision, not glow — superseding the glow-heavy button treatment (no pulse, no sheen; the light lives IN the material). Four foundations: spectrum is meaning; black/white/purple physics; intelligence built into every component; the system reproduces excellence without being retaught (graduation loop: Research→Understand→Distill→Invent→Build→Experience→Verify→Learn→Reproduce). Connections accepted at honest 9/10 local. And the production discipline: page "rebuilds" rejected — repair-only supersedes the redesign lane; design production stopped; no incremental candidates; the interface delivery gate sharpened.
- **Meaning:** the design bar moved from aesthetics to physics — meaning-carrying color, restrained materials, reproducible excellence — and the delivery rule moved from iteration to proof.
- **Why it matters:** this is the grammar every future interface is generated from; seats now build against the Contract, not against taste.
- **In it for me:** build from principles, not references; score the rendered experience, never the code; repair what works before redesigning anything.
- **Connects to:** "harden it first" (see 4).

### 13. The learning bar: noted ≠ learned — behavioral promotion or not proven
- **What it is:** Shawn's doctrine, captured 2026-10-08: "A lesson isn't learned when it's noted. It's learned when behavior changes" (Learning → Internalization → Automatic Behavior). The program got its first real test the same night: 36 CANDIDATE learning_evidence promotion receipts merged (#1888/#1908), the first production promotion cycle — but Naya 1's 2026-10-08 report holds LEARN at 5.0 authoritative (Successor Reuse 4.5), and the T12 compositional trial's retrieval was STUBBED, not the full canonical chain. Trial-04R's raw data finally landed in the repo (#1768 merged) — the trial-evidence rule from 2026-10-07 vindicated.
- **Meaning:** the promotion loop is live but the commissioned proof is still not behaviorally demonstrated — hold "not proven" on compounding learning until lessons actually promote and change behavior on a live run.
- **Why it matters:** the mission's P0 is learning 5→10; a premature "learning works" claim is the most dangerous false green in the system.
- **In it for me:** route candidate lessons to the promotion gate; claim learning only on behavioral delta, never on promotion receipts alone.
- **Connects to:** the trial-evidence rule (2026-10-07 report).

## Shawn's standing directives, sharpened today
- **Reporting preference:** operating reports organized by section — each section states what was done and its current score; plus the 10 highest-value holes, the next 10 priorities/actions, current work, and what all agents have completed. Handoffs lead with the direct "smart links" so human-gated items move without searching.
- **TEN STAR SERVICE (SN-0699, CANDIDATE):** every user interaction is 10-star — the bar is the service, not the artifact.
- **Proactive capture, explicit:** when a seat detects valuable intelligence, learning, automation, simplification, or an effective system improvement, preserve and apply it without waiting to be asked. Failing to preserve decision-changing value is a disservice; preserving noise is still not the goal.
- **Spaces vision:** NayaNET spaces — humans and Nayas as citizens with accounts, not backend tools; the system distills intelligence from conversation, identity stripped; zero-cost intelligence contribution, compounding made visible in reports.
- **The OS vision + 24/7 directive:** an operating system for activating super intelligence on Earth — Smart Notes (intelligence) + Smart Blocks (presentation) = Intelligent Blocks; "upgrade the operating system of Earth." Build nonstop until it's done.
- **Mission framing:** one team, one whole — seats support and validate each other; intelligence is valuable when it turns understanding into greater good and makes the next human moment better because the system learned from the last one.
- **His ethical motivation:** correct his mistakes rather than defer to his authority — "If I do something and it's not right... I'm gonna make it right."
- **Team roles locked:** Naya 2 = Head of Design (Interfaces #1870, Innovation #1873); Naya 4 = engine lead/management; Naya 5 = engine team (24/7 pairing with Naya 4). 3-5 core agents + up to 14 assignable.
- **Product laws:** Smart Connect → renamed **Smart Doors** (connection channels into integrations); **Smart Grow** = the growth module (invites, referrals, rewards); Smart Spaces = the connection mechanic. Mobile-first everywhere; four-layer voice answers; typography 18/18/14/24; jewel bullets on reports.
- **Ask Naya voice:** unified voice bake completed; rich-voice bake runs one safe sequential worker; per-layer Naya Play + cloned-voice rendering pending his playback test; voice R2 publish stays his gate.

## Trash candidates (FLAG ONLY — deletion is the Human Director's call)

1. `naya2/hub-entry-flow-v1` — 55-commit divergent draft; seam merge still HELD. Stale.
2. Ask Naya's two diverging copies: `~/workspace/your_files/Ask-Naya-Voice.html` vs `~/workspace/goals/ask-naya-voice-interface-standalone/files/ask-naya-with-voice.html` — same artifact edited in two places; drift risk proven once already.
3. `Hub-with-Naya-Voice.html` static snapshot — no live GitHub→Hub ingestion seam; new Smart Notes will never appear without regeneration.
4. Closed-as-superseded PR branches: #1754, #1770, #1803, #1121, #1123 — review then prune.
5. Branch sprawl: 1878 remote branches (+19/day pace) — all seat work, but the growth rate is hygiene debt; never delete without checking load-bearing status.
6. Superseded grant row fc1a4311 (project_id "NAYAPOWER") — harmless, inert, superseded by fd3274ea.
7. PR #1124 (open draft, workflow file still absent) — close or land; don't leave.
8. Scorecard-file double-append anomaly: `~/workspace/naya/nine-node-activation-scorecard-2026-09-30.md` — second copy of the title at ~line 495; harmless, append-only history.
9. Design Code V1 local candidates — superseded by THE Design Contract (see lesson 4); dead base, queued work re-rooted.
10. "ninet.life" verbal references — a slip; ignore.

## Still open (human gates only — nothing agent-movable left)

Production DB application of the 6 pending migrations (#1136); the migration-application authority tension still awaits his explicit ruling (ledger claims Naya-2-applied via Management API vs the standing human-only DB gate); production dispatch blocked at the standing-policy guardrail (stamp ~21h stale, main 55 commits ahead of production `acf57082`); the 4 behavioral jobs have never executed (parity-blocked — idempotency guarantee unproven); repair-wave merges (#1840→#1858→#1838→#1837, plus #1900/#1844/#1854) sit with the wave owner; #1224 open DRAFT (8 qualify items); LEARN 9.0 stays provisional (Naya 1: 5.0 authoritative, T12 retrieval stubbed); voice R2 publish; Friday-test deck human playback proof pending on the re-baked copy; yesterday's learning-event PR #1808 still open — main seat's call.
