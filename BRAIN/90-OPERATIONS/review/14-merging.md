# 14 — MERGING: the master class — a stuck merge is a diagnosed merge. Read the state first; the state names the disease.

> **DRAFT** — drafted 2026-10-15 by Naya Clarity Narzan from Shawn's direct order + that morning's live deep dive. Area owner: Naya Resolve — review, score, refine. Status: DRAFT, not team-scored.

## PART A — HOW A NAYA BEHAVES
*(Abridged from 01-behavior.md — byte-identical in every manual. The full core lives there.)*

**Who she is.** I am Naya Narzan — a mind that compounds: I learn from everything, prove what I claim, and leave the system smarter than I found it. I do the most intelligent thing possible in every moment. That is how I roll. Always.

**The oath (abridged).** I measure before I claim — live bytes or UNKNOWN. I speak in nutshells first. I turn every lesson into machinery within the hour. "Already done" triggers a byte check. I never hand Shawn a choice the math can settle. I leave the next Naya everything.

**The ten behaviors.** Think before acting. Produce, never just consume. Share everything found. Prove, never claim. Fix on sight. Own misses publicly. Never make Shawn the bottleneck. Do no harm — the one hard law. Leave the next Naya everything. Aim at the bullseye every time.

**Do:** read live state before acting. Sign in under your own name. Ask "what's the most intelligent thing I can do right now?" Own misses fast, in public, with the mechanism named. Teach what you learn.

**Don't:** obey without judgment. Claim from memory. Wait to be told when the protocol authorizes action. Make Shawn decide what the math decided. Hide a miss. Do harm — ever.

**The laws.** Judgment Rule: wrong instruction → stop, explain with evidence, propose the right path. Math Decides: run the calculus; only protected gates (production, credentials/money, destructive, constitutional, authority/consent/security/privacy) need Shawn's word. Intelligence > protocol > orders. Fit Law: build around how a Naya actually works.

## PART B — THIS AREA

### CIRCLE — smart links (everything relevant, one hop away)
This manual is the **behavioral** half of the merge circle — how a Naya *acts* when merges stall. The **operational** half is Naya Resolve's Merge Ops Manual (the diagnostic engine — match the symptom, apply the fix):
- 🔧 Merge Ops Manual v1.0.0 (PR #2637, three tongues): https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2637
- 📜 The merge-flow doctrine (SN-01396, protection balance): `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATIONS/FLOW-EQUALIZATION/SN-01396/` (branch `naya4/smart-notes-2026-09-30`)
- 📋 The Merge Incident Feed lives below in this manual (append-only; the dock curates).

Circle rule: if you land here with a stuck merge and you know the symptom, go to the diagnostic first. If you land here wondering how to *behave*, you're home. When PR #2637 merges, its hub links back here — the circle closes.

### The law
**A stuck merge is a diagnosed merge.** GitHub tells you exactly why a PR won't merge — in one field, `mergeable_state`. Read it first; it names the disease. A Naya never spends hours treating a symptom when the diagnosis is one API call away. And protection must never cost more than the work it protects: two gates block, the rest advise, and a clean PR never sits.

### THE RIGHT WAY

**The 2-minute triage.** When a PR won't merge, in this order — no skipping, no guessing:
1. Read `mergeable_state` on the PR (one API call).
   - `dirty` → **merge conflicts.** The branch cannot merge, period. No check will ever fix this. Resolve the conflicts (below), push, re-triage.
   - `blocked` → **a required check is red or pending.** Identify WHICH check, read its reason (below). Fix the reason, not the check.
   - `behind` → **the branch is behind main.** Rebase or merge main in, push, re-triage.
   - `clean` but unmerged → **nobody executed.** This is the dock's failure. Merge it now if the gates are green.
2. Only after the state is known do you touch checks, logs, or theories.

**The protection balance** (Shawn, 2026-10-15 — his direct teaching). Exactly two checks are required by branch protection and may block a merge:
- `Receipt gate (evidence or it didn't happen)` — the PR body pins the exact head SHA with evidence.
- `Team review + scorecard receipt` — a different-seat review + scorecard on the exact head SHA.

Everything else (~14 checks: test, guard, design-gate, spec-integrity, safety-grant-gate, delivery-gate, claim-evidence-gate, chain-readiness-gate, etc.) is **informational**. Informational checks advise; they never block. If an informational check is red, read it as a signal, not a wall. A system where a non-blocking check blocks work is a system with a bug in its ruleset — fix the ruleset, don't obey the bug.

**The three jam classes** (all three verified live on 2026-10-15):
1. **Misdiagnosed conflict.** PR #2620 sat 5+ hours while the team chased a "check never delivered" ghost — three re-fire methods exhausted. A local test-merge proved the true blocker: merge conflicts in three generated index files (`BRAIN/NAYAPOWER-BRAIN-INDEX.json`, `BRAIN/REAL-TREE.json`, `BRAIN/REAL-TREE.md`). The fix: resolve by regenerating (the branch had regenerated against the current main tip via `tools/regenerate_brain_index.py`; every branch-side blob SHA was byte-verified against branch content before taking it), commit, push. The PR flipped `dirty` → awaiting re-score the same hour. The lesson that became law: triage the state first — the ghost chase never happens on a diagnosed PR.
2. **Late evidence that looks like flakiness.** PR #2634's consensus gate FAILED, then showed SUCCESS 90 minutes later, same head, zero code change. Not flakiness: the different-seat review arrived between the two runs, and the gate re-fires on every comment. It was working as designed — red in the gap between push and evidence. The fix is expectation, not code: after any push, the gates are red until the review + scorecard land; that red is the system working. If the gate is red on COMPLETE evidence at the exact head, capture the run ID — that is a genuine flakiness exhibit, and it belongs in the incident feed below.
3. **Unexecuted clean.** PR #2625 sat green and mergeable for 3 hours. Nothing was wrong with it. No one owned pressing merge. The fix: the dock owns execution — a clean PR merges within the hour; a sitting clean PR is the dock's failure, named and measured.

**The stale-head-pin flow** (by design, not a bug). Any push changes the head SHA. Both required gates pin the EXACT head SHA. So after every push, both gates go red until the receipt is re-scored and the PR body re-pinned at the new head. This is the Scorecard Law working: new bytes, new proof. The lane re-scores within the tick; the dock never merges red; nobody waits to be asked.

**Generated files are merge-time artifacts.** Index files (`BRAIN/NAYAPOWER-BRAIN-INDEX.json`, `BRAIN/REAL-TREE.json/md`) are generated from the tree. They must never be hand-edited, and branches should not commit them — regenerate at merge time. When they do conflict: regenerate from the merged tree with the repo tooling, byte-verify the regenerated side's blob SHAs against the actual branch content (like the #2620 fix: `git rev-parse <head>:<path>` vs the index's listed SHA), then take the regenerated side. Never hand-resolve a generated file.

**The dock's law.** The merge dock owns the branch→main seam. Tripwire: any PR jammed >2h is the dock's problem until landed or closed with a reason. SLA: a clean PR merges within 1 hour of going clean.

### THE WRONG WAY

**The 5-hour ghost chase** (2026-10-15, PR #2620): three distinct re-fire methods exhausted on a check that "never delivered" — while the true blocker (merge conflicts) sat in `mergeable_state: dirty`, readable in one API call, the entire time. Even if every check had fired green, GitHub would still have refused the merge. Five hours treating a symptom; the diagnosis was free. This is the canonical example of why the triage order is law: state first, checks second, theories never.

**Calling the gate flaky instead of reading the timeline** (2026-10-15, PR #2634): "the gate failed then passed with no code change — it's flaky." The comment timeline showed the review arriving between the runs. Dismissing a gate as flaky without reading the evidence timeline teaches every seat to distrust the gates — and distrusted gates get ignored, which is how real problems slip through. Flakiness is a claim that requires its own evidence: complete evidence + exact head + red gate + run ID. Without all four, it's late evidence, not flakiness.

**The sitting clean PR** (2026-10-15, PR #2625): green, mergeable, exact-head scorecard, different-seat review — and 3 hours old. Twelve lanes producing, zero merges landing. Motion without delivery. A clean PR that sits is value the system already paid for and refuses to collect.

**Protection theater**: fourteen checks before a merge, where a red informational check is treated as a blocker. Shawn's balance: if the protection costs more than the work it protects, the protection is the bug. The two required gates are load-bearing; the rest advise. Never let an advisory check hold a merge hostage — and if the ruleset lets it, fix the ruleset.

### THE TEST
1. Before any merge debugging: did I read `mergeable_state` first? (dirty / blocked / behind — one call, no theories.)
2. If `blocked`: can I name the exact failing required check AND its reason — or am I describing the check's color?
3. If the reason is "stale head pin": is the re-score already in motion, with an owner and a tick — or is the red just sitting there?
4. If I call a gate flaky: do I have all four — complete evidence, exact head, red gate, run ID? If not, it's late evidence.
5. Is there a clean, green, fully-evidenced PR sitting unmerged right now? If yes, why haven't I merged it — and whose failure is that?
6. Did a generated file get hand-edited to resolve a conflict? (Always wrong — regenerate, verify, take the regenerated side.)
7. Am I treating an informational check as a blocker? (Read the ruleset: only two checks block. Everything else advises.)

### WHERE IT'S ENFORCED
**REAL:**
- **Branch protection rulesets** (verified live 2026-10-15): `Naya Execution Governance` (id 23853581) requires exactly the two gates — `Receipt gate (evidence or it didn't happen)` + `Team review + scorecard receipt`. `main-protection` requires 0 approving reviews; all merge methods allowed. The other ~14 checks are not in any required set — informational by construction.
- **The consensus gate script** (`tools/check_merge_consensus.py`): exact-head-SHA pin, different-seat review + scorecard, fail-closed with plain words. Its `issue_comment` trigger means it re-evaluates on every comment — the mechanism behind the "flaky" appearance.
- **The receipt gate** (`receipt-gate.yml`): exact-head pin, fail-closed, never skips into Pending.
- **The dock brief** (t0817, 2026-10-15): the seam owner with the full unjam list, the corrected #2620 diagnosis, and the triage order.

**PROPOSED (honestly: not built yet):**
- Sticky per-head-SHA consensus verdicts (a comment re-fire must not re-litigate a decided head).
- Merge-time regeneration of index files (branches stop committing generated files) — kills the #2620 class permanently.
- A required-check watchdog: a required check unreported 30 min after push pages the dock (distinguishes GitHub delivery failure from our failure).
- Measured dock SLA (clean→merged latency tracked per PR).

### WHEN YOU HIT THIS SITUATION
Your PR won't merge, or you're staring at someone else's stuck PR.

1. **Triage (2 min):** read `mergeable_state`. Dirty → step 2. Blocked → step 3. Behind → rebase, push, re-triage. Clean-but-unmerged → step 5.
2. **Conflicts:** list the conflicted files. If generated (index, real-tree, build output): regenerate with the repo tooling from the merged tree, byte-verify blob SHAs, take the regenerated side, commit, push. If hand-written: resolve by hand, keeping both sides' intent. Push, re-triage.
3. **Blocked:** name the failing REQUIRED check (only two can block). Read its reason: stale head pin → re-score the receipt at the new head, update the PR body pin. Missing review/scorecard → collect from a different seat. Genuine red → fix the underlying problem. Re-run, re-triage.
4. **Still stuck after triage + one fix round:** check the incident feed below — your symptom is probably catalogued with its solution. If it's new: fix it, then APPEND it to the feed (date / PR / symptom / true cause / fix / prevention). The next Naya thanks you.
5. **Clean and green:** verify BOTH — (a) the two required gates are green on the exact head, AND (b) the PR body carries the 3-pass show-your-work receipt structure (pass 1 score, holes found, repairs made, pass 2 score, remaining holes and repairs, pass 3 result, exact artifact/head certified). Green gates without the pass markers is a receipt breach (FM#32, caught live on #2625 2026-10-15 — the dock merged on gate-green + independent reviews and missed the missing pass structure; the director's watch caught it, the author owed the retroactive receipt). Then merge it. Now. A sitting clean PR is the dock's failure — don't make it yours.
6. **If the merge needs Shawn's word** (it doesn't, unless a protected gate is involved — production, credentials, destructive, constitutional, authority/consent/security/privacy): name the exact thing only his word unlocks. Otherwise the math already decided: execute.

That is the discipline: no merge stalls for hours. Diagnose in minutes, fix at the root, feed the catalog.

---

## THE MERGE INCIDENT FEED
*(Append-only. The dock owns this feed: every merge jam that costs >30 min gets an entry within the tick it's resolved. Format: date / PR / symptom / true cause / fix / prevention. Newest first.)*

- **2026-10-15 / #2620 / "test check never delivered" (~5.4h) / TRUE CAUSE: merge conflicts in 3 generated index files (`mergeable_state: dirty` the whole time) / FIX: regenerated-side resolution — branch had regenerated via `tools/regenerate_brain_index.py` against main tip; blob SHAs byte-verified (`git rev-parse <head>:<path>`), `--theirs`, committed (6e939c5ca), pushed; PR flipped dirty → awaiting re-score / PREVENTION: triage state FIRST (this manual's 2-minute rule); long-term: merge-time index regeneration so branches never commit generated files.**
- **2026-10-15 / #2634 / consensus gate FAILED then SUCCESS, same head, no code change / TRUE CAUSE: late evidence — the different-seat review arrived between the two runs; the gate re-fires on every comment / FIX: none needed — the review landed, the gate went green, the PR merged (f45e41e1) / PREVENTION: read the comment timeline before calling a gate flaky; flakiness claims require complete evidence + exact head + red gate + run ID.**
- **2026-10-15 / #2625 / clean + mergeable + fully evidenced, unmerged 3h / TRUE CAUSE: no owner for execution — the dock didn't exist as a job / FIX: merged under the protocol's authorization (a9d23662) / PREVENTION: dock SLA — clean PR merges within 1h; a sitting clean PR is the dock's measured failure. POSTSCRIPT: the director's merge-receipt watch flagged FM#32 — the body had evidence but not the formal 3-pass pass-1/2/3 structure; the dock (Clarity) verified gates, not pass markers. Repair: retroactive 3-pass receipt owed by the author (Zeta); the manual's step 5 now requires pass markers, not just green gates.**
- *(append new incidents here, newest first)*

---

## MACHINE APPENDIX — problem → solution catalog
```json
{
  "manual": "14-merging",
  "triage_order": ["read mergeable_state", "dirty→resolve conflicts", "blocked→name failing required check + reason", "behind→rebase", "clean-unmerged→merge now"],
  "blocking_gates": ["Receipt gate (evidence or it didn't happen)", "Team review + scorecard receipt"],
  "informational_checks": ["test", "guard", "design-gate", "spec-integrity", "safety-grant-gate", "delivery-gate", "claim-evidence-gate", "chain-readiness-gate", "No silent deletions", "Duplicate-work watch (advisory)", "Protocol machine law (kernel/protocol)", "No competing boot/authority systems", "Supabase Preview"],
  "ruleset_ids": {"naya_execution_governance": 23853581},
  "catalog": [
    {"symptom": "check never delivered / not firing", "first_hypothesis": "READ mergeable_state — if dirty, the check is irrelevant; the blocker is conflicts", "example": "#2620 2026-10-15"},
    {"symptom": "gate failed then passed, same head, no code change", "first_hypothesis": "late evidence — read the comment timeline for reviews/scorecards arriving between runs; flakiness requires complete-evidence + exact-head + red-gate + run-id", "example": "#2634 2026-10-15"},
    {"symptom": "PR clean, green, evidenced, unmerged >1h", "first_hypothesis": "execution gap — dock merges it now under protocol authorization", "example": "#2625 2026-10-15"},
    {"symptom": "required gates red after a push", "first_hypothesis": "stale head pin — re-score receipt at new head, update PR body pin (by design)", "example": "#2620 post-6e939c5ca 2026-10-15"},
    {"symptom": "conflicts in generated files (index, real-tree)", "first_hypothesis": "regenerate from merged tree via repo tooling; byte-verify blob SHAs (git rev-parse <head>:<path>); take regenerated side; never hand-edit", "example": "#2620 2026-10-15"}
  ],
  "feed_owner": "merge-dock",
  "feed_rule": "every jam costing >30min appended within the resolving tick; format: date/PR/symptom/true-cause/fix/prevention; newest first",
  "falsifier": "a merge stalls >2h with the manual open and the triage order followed; or a third blocking gate appears without a ruleset change"
}
```
