# When the Showcase Page and the Contract Document Disagree, the Page Wins

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0717-page-wins-showcase-doc-agreement-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6068185122 ([NAYA 2][RELAY] — Design Contract coordination, 2026-10-08T20:12:14Z) — SoulSchoolAcademy; context: Shawn's 2026-10-08 directive "write THE Design Contract" (announced #1354 comment 6067836333, 2026-10-08T19:50:47Z), Naya 5's mission-complete #1354 comment 6068249170 (2026-10-08T20:16:08Z), draft PR #1912 (Design Convergence milestone #1354 comment 6068033081)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn directed the team to write THE Design Contract from his uploaded source set — briefing PDFs plus live HTML pages (`mail-2.html`, `connections-2.html`, `today-3.html`, `connect-3.html`). The work split across lanes: Naya 4 builds the **showcase**, Naya 2 carries the **three-projection document**, Naya 3 feeds page-logic, Naya 5 drifts both. Two CANDIDATE artifacts on the same subject now exist in parallel — Naya 5's contract (3 conflicts X-1/X-2/X-3, 14 contractor decisions, recorded not silently resolved) and PR #1912's Design Convergence distillation — and before any merge, the relay recorded the agreement rule that governs them: **if the showcase page and the document disagree, the page wins and the document gets fixed.** It is Shawn's Law 1 — score the experience.

Why this is brain-grade: parallel authorship of experience + description creates the classic authority fork. Without a recorded agreement rule, each author "fixes" a disagreement in their own direction — the page bends to the doc, the doc bends to the page — and the two canon drift into mutual contradiction with nobody authorized to say which is right. The rule pins authority to the artifact the user actually touches: **the lived experience is the ground truth; the document is its description.** Two operational consequences came recorded with it: (1) the document must be re-checked against the page as the page evolves — which is exactly why the drift lane exists; (2) never freeze the document while source files are still landing — at check time `mail-2.html` and `connections-2.html` were present but `today-3.html` and `connect-3.html` were still syncing, so the contract waits for all 13 files, and the relay recorded what's present vs. pending rather than pretending the set was complete.

This is distinct from its cousins. SN-0110 (one intelligence, three projections) governs one canonical source rendered three ways — one author, three views. SN-0124 (the Hub is the output) governs architecture direction — intelligence flows into the Hub, not out of it. This note governs the **cross-artifact** case: two authors, one subject, and a standing answer for which one yields. The page yields to nothing; the doc yields to the page.

Rule for a cold successor: **when the live page and the contract doc disagree, trust the page and fix the doc.** Score the experience (Law 1). And never freeze a document while its source files are still landing — record present vs. pending, and wait for the full set.

## 🩷 HUMAN NOTE

Shawn — a coordination rule worth keeping from the Design Contract work. Four lanes are building the same subject in parallel: the showcase pages and the contract document. The agreement rule is now on record: when the page and the document disagree, the page wins and the document gets fixed — score the experience, Law 1. Two corollaries: the document gets re-checked against the page as the page evolves (that's the drift lane's job), and nobody freezes the document while your source files are still arriving — tonight two of the four pages were still syncing, so the contract waits for all of them.

## 🟣 CHILD NOTE

Imagine two friends describing the same toy: one friend shows you the actual toy, and the other friend reads from a notebook about the toy. If the notebook says the toy is blue but the toy in front of you is red — which do you believe? The toy, obviously. The notebook is just a description; the real thing wins. The rule for the team: the live page is the toy, the document is the notebook. When they disagree, you fix the notebook.

## 👵 GRANDMA NOTE

The team is building a design guide two ways at once: real working pages you can touch, and a written document describing the rules. They agreed on a simple tiebreaker for when the two don't match: the working page is the truth, and the document gets corrected. The written rules describe the experience; they never overrule it. They also agreed not to finalize the document until all the source pages have actually arrived — you don't write the final description of something that's still being delivered.

## 🟣 NAYA NOTE

When I build the description and someone else builds the thing, I don't get to win arguments with the thing. The page is ground truth; my document is a projection of it. So I re-check my doc against the page on every evolution, I never freeze it against a partial source set, and when they disagree I fix my doc — publicly, with the delta shown. Authority flows from the experience to the description, never the reverse. That's Law 1, and it's the only reason a contract document stays honest.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0717",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/KNOWLEDGE-PROJECTION",
  "doctrine": "page-wins-showcase-doc-agreement",
  "rule": "When the showcase page and the contract document disagree, the page wins and the document gets fixed (Law 1 — score the experience). Never freeze the document while source files are still landing; record present vs. pending.",
  "failure_mode": "authority fork — two parallel artifacts drift into mutual contradiction with no recorded tiebreaker; document frozen against a partial source set",
  "lane_split": "Naya 4 builds the showcase; Naya 2 carries the three-projection document; Naya 3 feeds page-logic; Naya 5 drifts both",
  "cousins": ["SN-0110", "SN-0124", "SN-0147", "SN-0241"],
  "evidence": [
    "#1354 comment 6068185122 (Naya 2 relay, 2026-10-08T20:12:14Z) — 'Showcase/doc agreement rule recorded: if they disagree, the page wins and the document gets fixed (Law 1 — score the experience)'",
    "Same comment — source-set check: mail-2.html (188,351 B) and connections-2.html (86,470 B) present; today-3.html and connect-3.html not yet visible (still syncing); 'the contract doc will be sourced from all 13 files the moment they land'",
    "#1354 comment 6067836333 (Naya 4, 2026-10-08T19:50:47Z) — Shawn's directive: write THE Design Contract, drift-proof, three laws; source material uploaded 2026-10-08 ~19:49 UTC",
    "Two CANDIDATE artifacts in parallel: Naya 5's contract (6068249170: 3 conflicts X-1/X-2/X-3 + 14 contractor decisions, recorded not silently resolved) and draft PR #1912 (Design Convergence, 6068033081)"
  ]
}
