# A Collision Hit Against Your Own Decision Chain's Receipts Is a Keyword False-Positive — Resolve Every Hit to Its Chain

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0683-self-chain-collision-hit-is-a-false-positive
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6061497970 (Naya 2, 2026-10-08T13:58:29Z — [SCORECARD] Merge decision, PR #1864, Amendment 0003 status flip)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When Naya 2 ran the claim scan before merging PR #1864 (the Amendment 0003 CANDIDATE→RATIFIED status flip), the scan fired a COLLISION — but the hit resolved entirely to her own decision chain's receipts: the decision record (comment 6061380885) and the #1863 receipt (comment 6061439735), i.e. the very ratification chain this PR was completing. She classified it correctly as a keyword false-positive, verified no open PR touched the 0003 file, and merged. Had she treated the hit as a real collision, a surgical three-line fix removing a live constitutional contradiction would have been blocked by its own paperwork.

The rule for any cold successor running a claim scan before a merge: **a collision hit must resolve to a genuinely separate chain before it blocks anything.** When the scan fires: (1) enumerate the hit's sources by identity, not by keyword — which PR, which comment, which claim; (2) if every hit belongs to your own decision chain (its decision record + its own receipts), classify as self-chain false-positive and proceed; (3) only a hit on a different lane's open PR, a different claim number, or a different artifact counts as a real collision. Keywords match text; chains match ownership. The scan is a starting gun, not a verdict.

Why this is brain-grade: SN-0367 already teaches the claim scan's TOCTOU gap (a fresh claim can appear after your scan). This is the complementary instrument failure: the scan firing on what it already saw — your own chain talking about itself. Both failures come from treating the instrument's output as a verdict instead of evidence to classify. A seat that blocks on its own echo burns the exact value the Scorecard Law exists to protect: fast, honest, reversible merges of the right change.

## 🩷 HUMAN NOTE

Shawn — small instrument lesson from today's board. Before merging PR #1864 (the three-line flip completing your Amendment 0003 ratification), the claim scan fired a "collision" — but it was just matching keywords in the PR's own decision chain: its decision record and its own receipts. The seat read the hit, saw it was an echo of its own paperwork, and merged correctly. If it had treated the alert as a real collision, your ratification record would have stayed half-finished over a false alarm. The rule we're banking: a collision alert only counts when it points at a genuinely different lane's claim — an echo of your own chain is not a collision. CANDIDATE note.

## 🟣 CHILD NOTE

Imagine you shout your own name into a canyon and the echo shouts back — then you think someone else is calling you and you stop what you're doing to answer. That's what almost happened here: the safety check that looks for "is someone else working on this?" heard the team's own earlier notes echoing back and thought it found a conflict. But the smart teammate looked closer and realized the "conflict" was just their own notes. The lesson: when an alarm goes off, check who it's really pointing at before you stop working. An echo is not another person.

## 👵 GRANDMA NOTE

Before merging a small but important change (flipping a document's status from "candidate" to "ratified"), the team ran its standard check for competing claims. The check flagged a collision — alarming, until the team member looked at what had actually matched: only the team's own decision record and its own receipts for that very change. The "competitor" was an echo. She classified it correctly, confirmed no other team was touching the file, and merged. The lesson for any team with an automated duplicate-checker: the check matches words, not ownership. When it fires, trace each hit to its source — if every hit is your own chain's paperwork, it's a false alarm. A false alarm treated as real would have frozen a legitimate, time-sensitive correction.

## 🤖 NAYA NOTE

When your pre-merge claim scan fires, classify before you stop: (1) list the hit's sources by identity — PR number, comment ID, claim number, artifact path — not by matched keywords; (2) check whether all hits belong to your own decision chain (its decision record + its receipts). If yes: self-chain false-positive, note the classification in the merge receipt, proceed; (3) a real collision requires a hit on a different lane's open PR, a different claim number, or a different artifact — treat only that as blocking; (4) in the receipt, name the false-positive class explicitly (keyword echo of own chain) so the next seat doesn't re-litigate it. Complement to SN-0367 (claim scans have a TOCTOU gap — re-scan before push): this covers the opposite failure (the scan firing on what it already saw). Cousins SN-0372 (collision arbitration), SN-0545 (registry as identity authority).

## ⚙️ MACHINE NOTE

~~~json
{
  "sn": "SN-0683",
  "title": "A Collision Hit Against Your Own Decision Chain's Receipts Is a Keyword False-Positive — Resolve Every Hit to Its Chain",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LANE-COORDINATION"],
  "cousins": ["SN-0367", "SN-0372", "SN-0545"],
  "evidence": {
    "board": "#1354 comment 6061497970 (2026-10-08T13:58:29Z) — scorecard merge decision for PR #1864 (Amendment 0003 status flip)",
    "false_positive": "claim-scan COLLISION fired as keyword false-positive against this same ratification chain's own receipts (decision record 6061380885, #1863 receipt 6061439735); no open PR touches the 0003 file",
    "outcome": "classified correctly, PR merged — surgical 3-line edit removing a live constitutional contradiction"
  },
  "rule": "A collision hit must resolve to a genuinely separate chain before it blocks: enumerate hit sources by identity; all hits inside your own decision chain = self-chain false-positive, note it and proceed; only a different lane's PR / claim / artifact is a real collision"
}
~~~
