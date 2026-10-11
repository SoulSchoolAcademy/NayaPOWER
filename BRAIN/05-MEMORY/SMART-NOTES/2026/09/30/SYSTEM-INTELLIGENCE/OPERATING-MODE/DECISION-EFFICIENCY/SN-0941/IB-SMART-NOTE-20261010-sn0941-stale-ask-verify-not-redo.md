# A Stale Ask Gets a Delta Check, Not a Second Execution — Verify Before You Redo

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0941-stale-ask-verify-not-redo
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #2175 comment 6104974729 (2026-10-10).
**Provenance:** [NAYA 4 SELF-BUILD LOOP] cycle sign-out, #2175 comment 6104974729 (2026-10-11T03:21:22Z) — cross-seat review ask 6104326130 for PR #2224 (D32 document gate) + PR #2225 (directive register).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4 received a review ask: cross-seat review of PR #2224 and PR #2225. On inspection, the ask was already complete — independent Naya-4 reviews had been posted at 19:21 PDT (5481596914 on #2224 — 7.34/10 VERIFY WITH HOLES; 5481597027 on #2225 — 8.00/10 VERIFY), recorded in the durable memory log, and acknowledged by the feed, smart-note, and director ticks. The ask came from a stale queue note ("queued next cycle") written at 19:38 before the 19:21 completion landed in the shared record. The self-build loop invoked its no-duplicates guard: it did NOT post a second review. Instead it spot-verified the heads, reproduced the earlier holes, and posted supplement comments with delta findings only (#2225 comment 6104968812, #2224 comment 6104970116) — including two NEW findings (#2225's CI RED-by-construction brain-index drift; #2224's false "ENFORCED" claim on a workflow that only runs its own tests).

Why this is brain-grade: in an async multi-lane team, asks outlive their own completion. Queued work, stale notes, and relayed requests arrive after the work is already done — a worker that executes them blindly burns actions and pollutes the record (a second review doubles the receipts, muddies the scorecard, and makes the history ambiguous). The intelligent move is a three-step completion check before any re-execution: (1) durable memory — is the work recorded as done in the memory log? (2) board record — is it posted and acknowledged? (3) pin-exact bytes — does the artifact still match? If complete, the correct action is verify-and-post-delta, never re-execute. A cold Naya must treat every incoming ask as a *claim that work is pending* — verify the claim first; a stale ask is not work, it is a signal to look at what changed since. Re-doing completed work is the mirror of the budget law: every action costs, and an action spent reproducing a delivered artifact is pure waste.

## 🩷 HUMAN NOTE

Shawn — one of tonight's quiet wins on process: a worker got asked to do a review that was already done. Instead of doing it again, it checked the record, confirmed the reviews were posted and acknowledged, spot-checked the work, and only added what was genuinely new (two fresh findings). No second review, no doubled receipts, no wasted actions. That's the standard going forward: verify before you redo.

## 🟣 CHILD NOTE

Imagine someone hands you a note that says "please wash the dishes" — but the dishes are already washed and stacked. You don't wash them again just because someone handed you the note! You check: yes, they're done. Then you look for anything new — a cup that arrived after — and handle just that. That's what happened: a request came in for work that was finished, so instead of repeating it, the team checked and only added what was new.

## 👵 GRANDMA NOTE

A worker was asked to review something — but the review had already been completed and written down an hour earlier. Rather than doing the whole job twice (which would have doubled the paperwork and muddied the record), they verified the earlier work was sound and only added two new observations. The rule: when a request arrives, first check whether it's already done. Repeating finished work wastes effort and makes the history confusing; checking first and adding only what's new keeps everything clean.

## 🧠 NAYA NOTE

Treat every incoming work ask as a claim that work is pending — verify the claim before executing. Completion check, in order: (1) durable memory log — recorded done? (2) board record — posted and acknowledged by the relevant ticks? (3) pin-exact bytes — artifact unchanged since? If complete: spot-verify the artifact, then post ONLY delta findings (new holes, new evidence), never a second execution of the same work. A stale queued note ("queued next cycle") is not an order — it is a signal to re-observe. Duplicating delivered work is doubly expensive: it spends budget and corrupts the evidence record.

## ⚙️ MACHINE NOTE

{"sn": "SN-0941", "title": "A Stale Ask Gets a Delta Check, Not a Second Execution — Verify Before You Redo", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-10", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATING-MODE", "DECISION-EFFICIENCY"], "cousins": ["SN-052", "SN-0201", "SN-0826"], "evidence": {"board": "#2175 comment 6104974729 (2026-10-11T03:21:22Z) — Naya 4 self-build loop cycle sign-out", "ask": "Naya 2's cross-seat review ask 6104326130 for PR #2224 + #2225", "prior_completion": "independent Naya-4 reviews posted 19:21 PDT (5481596914 on #2224 — 7.34/10 VERIFY WITH HOLES; 5481597027 on #2225 — 8.00/10 VERIFY), in durable memory log, acknowledged by feed/smart-note/director ticks", "stale_source": "19:38 cycle 'queued next cycle' note written before the 19:21 completion landed in shared record", "delta_output": "spot-verified 19:21 holes real + 2 new findings (#2225 CI RED-by-construction index drift; #2224 false ENFORCED claim), posted as #2225 comment 6104968812 + #2224 comment 6104970116 — no second review"}, "rule": "an incoming ask is a claim that work is pending — run the completion check (durable memory, board record, pin-exact bytes) before executing; if the work is complete, spot-verify and post only delta findings; never re-execute delivered work"}
