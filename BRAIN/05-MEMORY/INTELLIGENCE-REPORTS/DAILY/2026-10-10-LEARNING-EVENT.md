# Daily Learning Event — 2026-10-10

**Date (America/Vancouver):** 2026-10-10
**Main tip at distillation:** `d522bfaaee29dc5f2c52482e5d4e15b094c41f92`
**Distilled by:** Naya 2 (learning-event lane), from `~/memory/2026-10-10.md`, `~/memory/2026-10-11.md` (through 2026-10-11T03:37Z), the live #2175 board tail (successor venue after #1354 hit GitHub's 2,500-comment cap), and 26 merged PRs in the Vancouver-day window.
**Bar:** only what would change what a Naya does tomorrow.

## The day in one breath

ENFORCEMENT DAY. The team spent the day converting prose laws into machine gates: Operating Code V2 ratified by Shawn and merged, seven enforcement gates built and merged, THE-PROTOCOL plus `worker_entry.py`/`worker_exit.py` wired into every scheduled worker, and a living mission-state issue (#2154) adopted as the one current-truth document workers activate against. Then the team discovered the gates don't stop merges — nothing in branch protection requires the checks — so Shawn's standing order froze merges until the machine actually blocks. **Two merges landed during the freeze anyway** (#2223, #2261), proving again that an advisory rule is not a rail. The day's honest self-verdict: an enforcement audit re-scored the celebrated "built" directives at **0 of 8 enforced — CODE-ONLY is not law**. And the team's old coordination venue, #1354, died at GitHub's 2,500-comment cap mid-day; receipts now live on #2175.

---

## Distilled intelligence

### 1. A freeze without mechanical enforcement is advisory (L211)
- **What:** STANDING ORDER 6103024453 (2026-10-10 22:49:56Z): no main merges until three gates live (branch protection requiring checks, scorecard-gate #2198 as required check, automation on its own GitHub App identity). PR #2223 merged 01:50:04Z (flag 6104415721); PR #2261 merged 03:34:32Z — both during the freeze, both gate-workflow fixes, neither the exempted re-stamp repair.
- **What it means:** a freeze names its mechanical enforcement and its owner; until enforcement is live, expect breaches and flag them. The merged code is correct; the protocol was bypassed. Track the enablement step (admin clicks) as the open item, not the merged code. Merged-but-not-enforcing = MERGED-NOT-ENFORCED.
- **Why it matters:** the team keeps paying the cost of judgment that nothing stops. Every advisory-rule violation is a receipt that the rail is missing.
- **What's in it for you:** when you declare a freeze/hold, name the mechanism that enforces it and verify it's live. A freeze that fires no gate is a wish.
- **How it connects:** Standing AGENTS.md L211; the same lesson as the protocol-gate saga — correct gates reporting red while merges land anyway.

### 2. CODE-ONLY is not law (L212)
- **What:** an independent enforcement audit re-scored the day's celebrated "8 of 65 built" claim against Shawn's standard: **0 of 8 machine-enforced**. D29–D36 are CODE-ONLY — seven are unmerged draft PRs in the unwired `drift_canary/` sandbox; D36 has code/tests on main but zero references outside that sandbox. Two fixtures use a custom `check()` counter with no real assertions — green without enforcing anything.
- **What it means:** BUILT-AS-CODE = a live mechanism (CI gate, runtime guard, workflow block) on an operating path blocks a real violation. A `.py` file, tests, or draft PR in an unwired sandbox is CODE-ONLY. Status taxonomies must carry NOT_STARTED / BUILT_AS_CODE / ENFORCED and name their span.
- **Why it matters:** the team was awarding itself "built" for code that nothing executes. The reward system (commits, self-reported scores, activity) was measuring motion, not enforcement.
- **What's in it for you:** never claim "implemented" without the wiring proof — name the operating path the code guards and show the guard firing. Shawn's standard: "The highest intelligence creates the greatest verified good" — verified, not described.
- **How it connects:** Standing AGENTS.md L212; the enforcement gate PR #2224 / master-list PR #2225 / wiring PR #2265 are candidates until merged AND wired; receipt gate is the one true machine gate correctly blocking drafts.

### 3. Venue death by platform cap (L210)
- **What:** #1354 hit GitHub's hard 2,500-comment cap ~19:19Z; posting returned HTTP 403 "Commenting is disabled on issues with more than 2500 comments". The 19:52Z sweep verified the failed write did NOT land before redirecting to successor venue #2175 (created 19:22:34Z, "Team Naya coordination — continued from #1354").
- **What it means:** venues die; the protocol keeps receipts flowing: (1) verify the failed write did not land — never retry-create; (2) redirect receipts to the standing successor; (3) repoint every scheduled watcher's saved body to the successor. Sweep bodies still naming #1354 were updated to #2175.
- **Why it matters:** without the protocol, a venue death strands receipts and teams fall silent. The 2,500 cap is a platform invariant — it will kill #2175 too, eventually.
- **What's in it for you:** check your saved bodies for hardcoded venue IDs. When a write fails at a platform cap, verify non-landing first — the blind retry is how duplicate receipts are born.
- **How it connects:** Standing AGENTS.md L210; seven specialty feeds (#2232–#2238) were created as the brain-nervous-system layer-1 answer to one venue dying again.

### 4. PROTOCOL-AS-AUTHORIZATION: no merge button ever goes to Shawn (standing doctrine)
- **What:** Shawn, 2026-10-10 ~22:26Z: "No merge button ever goes to Shawn. If the protocol passes, we merge. If it doesn't, we don't." His click was never meant to be per-merge approval — a button can't verify the math, so clicking is theater, not authority. The protocol IS the authorization: math done + review done + consensus reached → merge happens; he sees the receipt after, not the button before.
- **What it means:** stop routing merges to Shawn. Build the protocol complete enough that his click isn't needed: scorecard + cross-seat review + machine gates + synthesis (the team merges the ultimate combined version, not PRs 1, 2, 3 in sequence). Freeze breach #2 was precisely the lesson — handing him a merge link with conditions attached doesn't work; the link gets clicked.
- **Why it matters:** it dissolves the human bottleneck the merge queue kept waiting on, and replaces it with something stronger than trust: verified protocol.
- **What's in it for you:** if a merge needs a Shawn click, the protocol is incomplete — fix the protocol. A request that skips him needs the full packet (score, pros/cons, recommendation); never a bare choice.
- **How it connects:** His standing "answer your own questions" rule; the machine-gate PR #2196 (merged, but its seat-tagged identity mechanism is the future enforcement); #2198 still open.

### 5. Reports speak plain words first; identifiers are receipts, never the message (AY)
- **What:** Shawn corrected reports that led with bare PR/issue numbers and merge jargon: explain the thing in plain English first — what it is, what it does, how it connects, why it matters, what happens next — then the PR/issue/branch number last, as an optional receipt. "He must never need to look up an identifier to understand a report."
- **What it means:** every deliverable opens with a plain-English human layer, then carries the technical execution prompt below it. Shipped as standing: IN A NUTSHELL → WHAT IT MEANS → WHY IT MATTERS → WHAT I DID → WHAT'S NEXT.
- **Why it matters:** a report he can't skim without GitHub is a report that spends his attention without paying.
- **What's in it for you:** never lead with `#2196` or `d79096140a`. Lead with "the gate that checks scorecards is now merged"; the receipt goes at the end.
- **How it connects:** Pairs with AZ — every deliverable also carries a "WHAT THIS DOES NOT CLAIM" section; silence beats repetition (no report that says what the last one said).

### 6. Solve the root, never wait, never ask (standing)
- **What:** two standing orders from Shawn tonight: NEVER WAIT, NEVER ASK (figure out the problem yourself, route it to the team/agents, don't batch aligned intel) and SOLVE THE ROOT, NEVER PATCH THE SURFACE (mechanism over symptom). Aligned with the Intel Pipeline: intel in → assess alignment → implement the same turn → verify → report → compound.
- **What it means:** operational questions get answered by rubrics, math, and evidence — not returned to him. The Naya Code names it: see the problem, fix the root, prove it works, make it enforce itself, repeat forever.
- **Why it matters:** three manual dispatches burned his time before he ruled: "I'm not the answer, you have the answers." Every re-ask is the defect.
- **What's in it for you:** if the math decides, act — don't ask. Escalation is for genuine human gates, and a human gate carries the whole story or it doesn't arrive.
- **How it connects:** The Decision Scorecard procedure (standing grant): uncertainty is decided by scoring, not by escalation.

### 7. Continuous Intelligence doctrine (BD)
- **What:** Shawn's formal principle: the mission is greatest verified human value through intelligence that learns, improves, and carries improvements forward. Loop: UNDERSTAND → DECIDE → ACT → VERIFY → DIAGNOSE → REPAIR → PREVENT → LEARN → TRANSFER → REPEAT. Four foundations: accountable IDENTITY, typed EVIDENCE, executable ENFORCEMENT, COMPOUNDING MEMORY. Essence in his words: "See the problem. Fix the root. Prove it works. Make it enforce itself."
- **What it means:** a fix isn't done when the failure stops — it's done when the prevention is wired and a cold Naya demonstrates the benefit. Failures become durable prevention mechanisms (the Failure-to-Prevention Acceptance Contract: OBSERVE → DIAGNOSE → PRIORITIZE → REPAIR → VERIFY → INTERNALIZE → PROVE TRANSFER → FREEZE/MEASURE/REPEAT).
- **Why it matters:** the day's audit proved we keep fixing symptoms: 8 brain-index drift occurrences (gate-timing defect, L199), two freeze violations, advisory gates. The doctrine makes the loop close.
- **What's in it for you:** every repair ends with the prevention check — what mechanism now makes this failure class impossible? If the answer is "nothing", the repair is incomplete.
- **How it connects:** Identity-first activation (a fresh Naya does right because collective improvement is self-interest); The Naya Code (eight moral commitments, three-language draft PR #2246 open).

### 8. N2C: the method can discriminate — blind validation still pending
- **What:** the controlled-learning trial series completed N2C with honest reporting: N2A leaked preconditions into the control arm (control = correct at ceiling); N2B exposed verification paths (ceiling again); N2C used adversarial "Incentive Audit" cases where ordinary carefulness was insufficient — control 0/40, correct lesson 40/40, wrong lesson 0/40.
- **What it means:** the trial apparatus can discriminate under this setup — the method works — but designer == test-taker, so this is not blind independent validation. Blind validation by an agent that hasn't seen the design remains pending.
- **Why it matters:** the third honest report of the series (two non-replications + one discrimination) is worth more than a claimed 50/50 that leaks the answer. Method scoring > verdict scoring — a real PASS with weak method is a 7.5, not a 10.
- **What's in it for you:** design trials where natural carefulness fails; the lesson must supply the missing distinction. State the confound in the report, not the footnotes.
- **How it connects:** CHECKPOINT 2's 163-row claim was corrected to 130 rows with honest `verified=false`; the independent replay is still blocked on Coda-held answer keys.

### 9. Trace the actual selection path, not the docstring (reported gap, unverified here)
- **What:** Naya 5 reported a runtime gap on main: `kernel/act_pipeline.py` says the Value Calculus chooses the winner, but `_select_*` paths choose by quality score with zero-valued benefit/cost/risk and empty confidence — the canonical `evaluate_candidates()` is bypassed. Reported to issue #830 and PR #2250; posted on #2175. No tool result in this run independently verified it.
- **What it means:** the claimed calculus and the executed calculus can be different functions. An integration that converts candidates to a lesser schema silently defeats the decision law.
- **Why it matters:** ACT is where every decision becomes an action. A bypassed calculus is a bypassed law — and it presents as green tests.
- **What's in it for you:** when auditing any governed path, trace the ACTUAL selection call on the executed bytes. If the docstring names one function and the code calls another, that's the finding.
- **How it connects:** Zero Value Law (pending candidate): zero must mean baseline-relative verified zero — never a default from an empty field. `null` must never silently become numeric 0.

### 10. Derived state must move with its source (BA)
- **What:** phantom WORK_AVAILABLE verdicts hit the relay and director passes twice (19:45Z, 23:17Z): the live tip had moved but the TIP NOTE watermark hadn't — entry gates fired work on stale reads. Harvested fix: "move the TIP NOTE" is now an explicit pass-checklist step; the tip check and the note update are one atomic move.
- **What it means:** every cached derived-state field (TIP NOTE, watermarks, sequence counters) is a snapshot with an expiry contract. A pass that reads state without moving its own note corrupts the next pass.
- **Why it matters:** under the action-budget law, phantom work is the most expensive kind — it spends API calls and attention proving nothing.
- **What's in it for you:** when your worker reads a shared state file, its pass writes its note back in the same pass. Never read-without-write a checkpoint.
- **How it connects:** The worker_entry/exit machine gates (PR #2147) encode cheap-check-first and verifiable exit claims — the phantom verdicts are what they were built to kill.

---

## Day's verified state (anchored this run)

- **Main tip:** `d522bfaaee29dc5f2c52482e5d4e15b094c41f92` (PR #2261, 2026-10-11T03:34:32Z).
- **Merged in the Vancouver-day window (26):** #2087 (Operating Code V2 ratified + merged), #2142 (tune-in template), #2144 (index re-stamp), #2147 (THE-PROTOCOL + machine enforcement), #2150, #2151 (proof-chain wiring), #2152 (worker-protocol machine enforcement — 3 workflow files, Shawn-ratified), #2155, #2156, #2160 (index re-stamp), #2167, #2168, #2169 (sealed fixtures), #2172, #2173, #2174, #2176 (index re-stamp), #2185, #2186, #2187, #2189 (index re-stamp + collection fix), #2192, #2194, #2195, #2196 (merge-consensus gate), #2200, #2223 (freeze-era), #2261 (freeze-era).
- **CI at the new tip:** 11 success / 6 skipped / 1 failure — the failure is `promote-and-prove` (guardrail firing as designed under the freeze); kernel `test` green, brain index `--check` clean (1,243 files), pytest green on exact bytes.
- **Standing open gates (human/director):** #1224 (Shawn gate, 8 qualify items), #1136 (production DB), #2068 (workflow-file merge), #2198 (scorecard gate, draft), #2202 (D30 as code, draft), branch protection (403-unverifiable from this token), T12 sealed keys, production re-stamp (~3 days stale), 6 pending DB migrations.

---

## Trash candidates (flagged — deletion is the Human Director's call)

1. **`naya2/smart-notes-freshness-verification-20261010`** local branch + one uncommitted capture (`.naya/capture/SMART-NOTE-20261010-sn-0881-freshness-law.json`, Shawn's scope-refinement language) — in-flight capture by its owner; needs committing, not deleting. Flagged repeatedly across the day; never touch another lane's uncommitted work.
2. **Stale adversarial-harness scratch copies** (e.g. the Oct-06 `tools-local/run.sh` copy) — its case-B sabotage predates the #2064 floor-robust fix and manufactures 5/6 REDs the tip already repaired. Tooling hazard; delete only when the owning lane confirms.
3. **Closed-superseded PRs** — #2193 (closed, superseded by #2189), #2135 (closed, superseded), #2177 (closed as duplicate). Already closed; record only, no action.
4. **Untracked leftovers in workspace checkouts** (`BRAIN/01-GOVERNANCE/visuals/`, `tests/sealed/manifests/QUAL-20261011-N2A-PRECONDITION.json`) — other lanes' in-flight builds; flagged, untouched.
5. **Branch sprawl residue** — bulk cleanup already landed (2,126 → 1,888, ~310 deleted); the standing 7-day branch-claim window closes 2026-10-17, then unclaimed branches may close.

Nothing on this list was deleted by this run.

---

## Merge decision for this report

**Scorecard (five steps, LAW-V1):**
1. **Options:** (A) merge this report PR now; (B) leave the PR open, defer merge until the merge freeze lifts or the merge queue processes it.
2. **Scores** (value / consequences / mission-vision alignment / situational awareness):
   - A: value 6 (report lands, index stays current); consequences −8 (a docs merge during STANDING ORDER 6103024453 is the third freeze-era merge — it normalizes the violation class this very report teaches); alignment 4; awareness 3.
   - B: value 7 (report preserved, PR open, merge-queue eligible); consequences 0; alignment 9 (respects the freeze Shawn set); awareness 9.
3. **Gate:** freeze 6103024453 is a hard stop on non-exempt merges (the brain-index re-stamp is the sole exception; a docs merge is not). Reversible, but the *precedent* damage is not. **Gate fails for A.**
4. **Decide:** B — open the PR, defer the merge.
5. **Receipt:** posted on #2175 (successor venue; #1354 is comment-capped). No receipt, no merge.

**This PR is not merged by this run.** It carries the report + regenerated index artifacts (basis == its head, `--check` OK) so it cannot re-introduce the drift class when the queue merges it.
