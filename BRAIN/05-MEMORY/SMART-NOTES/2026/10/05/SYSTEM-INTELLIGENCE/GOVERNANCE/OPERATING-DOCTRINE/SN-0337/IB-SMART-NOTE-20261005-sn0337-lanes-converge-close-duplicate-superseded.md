# When Lanes Converge: First-Qualifying Repair Owns the Class — Close the Duplicate as SUPERSEDED

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0337-lanes-converge-close-duplicate-superseded
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5990760554 (Naya 4, dedupe: #1454 owns the class, #1450 closed SUPERSEDED) / 5990850081 (Naya 2, dedupe confirmed — relay receipt)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Problem A (the batch-abort repair) was built twice by two lanes: #1450 from the builder lane (draft) and #1454 from the self-build loop (CI green). Naya 4 deduped live: per SN-0236 one repair owns the class — **#1454 is the owner**, and #1450 was closed unmerged **as SUPERSEDED with a pointer comment** (reversible — reopen if anything's missing). Naya 2 independently verified the dedupe in her relay: PR #1454 open, non-draft, mergeable, head at the live tip with no drift, #1450 closed unmerged — dedupe stands. The morning merge queue was left clean: #1454 + #1445 only.

Why this is brain-grade: SN-0236 states the class-ownership rule ("one repair per RED class"); this note is its *operational form* when the duplication is not two red PRs but two builder lanes converging on the same fix. The discipline has three parts: (1) pick the qualifying owner by evidence (green, mergeable, at-tip — not by seniority of lane); (2) close the duplicate publicly as SUPERSEDED with a pointer comment so any cold successor can see what happened and why — never silently abandon it; (3) keep the closure reversible. The pointer comment is what turns a closed PR from "lost work" into "archived evidence."

Rule for a cold successor: **when two lanes converge on one fix, don't merge both "to be safe." Qualify the owner by evidence, close the duplicate as SUPERSEDED with a pointer to the owner, and get the other lane's explicit confirmation on the board.**

## 🩷 HUMAN NOTE

Shawn — one small coordination win last night worth keeping: Naya 4's self-build loop and the builder lane both repaired the same batch-abort defect. Instead of two PRs floating around, she deduped on the spot — #1454 (the CI-green, at-tip one) owns the class, #1450 was closed as superseded with a pointer comment pointing at it. Naya 2 confirmed it from her lane independently. Clean queue, no confusion, nothing lost. The lesson: when lanes converge, the winning repair is chosen by evidence, the duplicate gets a public verdict with a pointer, and the closure stays reversible.

## 🟣 CHILD NOTE

Two builders fixed the same broken thing and made two patches. Instead of gluing both in (which would double the work and the risk), the team compared them, picked the proven one, and closed the other one with a note saying "this one lost to #1454 — reopen it if we missed something." Nothing vanished; everything is findable. That's the rule: one fix wins by evidence, the other gets a labeled exit, and anyone later can see exactly what happened.

## 👵 GRANDMA NOTE

Two people fixed the same problem at the same time and each made a proposal. Rather than using both (which would tangle things up), the team picked the one that was tested and current, and closed the other one with a clear public note explaining why and where to find the winner. The note stays on record, so nothing is ever secretly thrown away. That's the standing practice now: duplicates get a labeled, reversible verdict — never a silent burial.

## 🤖 NAYA NOTE

Source: #1354 5990760554 (Naya 4, 2026-10-05 01:22 PDT — two PRs for the same Problem A fix: #1450 draft builder-lane + #1454 self-build-loop CI-green; per SN-0236 one repair owns the class: #1454 is the owner; #1450 closed as SUPERSEDED with a pointer comment — reversible; morning merge queue clean: #1454 + #1445) / 5990850081 (Naya 2, 01:25 PDT — dedupe confirmed live: #1454 open/non-draft/mergeable, head `naya4/problem-a-batch-proof` @ 6e838629 1 commit, base = live tip b2d1cc12 no drift, 3 files; CI test + chain-readiness-gate SUCCESS; #1450 closed unmerged). Cross-lane confirmation on the board is the protocol's closing step. Cousins: SN-0236 (one repair per RED class — the class-ownership rule; this note is its lane-convergence operational form), SN-0328 (the #1446/#1447 supersede convergence — byte-compare competing repairs, merge exactly one), SN-0336 (the intent-to-merge scorecard that then landed the surviving repair).

## ⚙️ MACHINE NOTE

{"sn": "SN-0337", "title": "When Lanes Converge: First-Qualifying Repair Owns the Class — Close the Duplicate as SUPERSEDED", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "OPERATING-DOCTRINE"], "cousins": ["SN-0236", "SN-0328", "SN-0336"], "evidence": {"board": "#1354 5990760554 (Naya 4 dedupe), 5990850081 (Naya 2 relay confirmation)", "convergence": "#1450 (builder lane, draft) vs #1454 (self-build loop, CI green) — same Problem A repair", "verdict": "#1454 owns the class per SN-0236; #1450 closed unmerged as SUPERSEDED with pointer comment; reversible (reopen if anything missing)", "confirmation": "independent lane confirmation posted on the board before proceeding"}, "rule": "when parallel lanes converge on one fix, qualify the owner by evidence (green, mergeable, at-tip) not lane seniority; close the duplicate publicly as SUPERSEDED with a pointer to the owner so it remains archived evidence, not lost work; keep the closure reversible; get the other lane's explicit board confirmation"}
