# The Cold Naya Graduated: One Prompt, an Unfamiliar App, 100/100 — Understanding Is Composable

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0756-cold-self-build-graduation-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6074547770 (Naya 5, 2026-10-09T04:55:33Z); branch `naya5/cold-build-proof` @ `bd290b90` (never touched main); `naya-library/graduation/PROOF-REPORT.md` + `garden-app.html`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A cold Naya — no history, one prompt — received ONLY the canonical material (`naya-library/`, the 100 Laws, the design calculator) and was asked to build a Smart App with no existing template: a community garden tracker. **Verdict: 100/100 — ELITE — ships.** The design calculator, re-run independently, scored all seven categories at max. Six self-iteration rounds (84 → 98 → 100), **zero re-teaching.**

What it built: `garden-app.html` — 68KB, single self-contained file: plot registry, planting calendar, harvest log, water duty rotation, orbital garden-vitality view. Fully interactive — 5 tabs, clickable plots, working forms, live updates.

What it got right first try: it copied canonical components verbatim (`.naya-btn` system, `.elevated-board`, SmartTabs nav, the full orbital living-data system from smart-stats-v2, inputs/toast/toggle from missing-blocks, the 40-icon sprite — plus 4 new icons in the same style, following the rule *"if it has no block, build the block first"*); laws proved executable (black ground `#050507`, white-at-rest igniting on touch, elevation everywhere, spectrum in law order); and **smart-stats-v2 was the Rosetta Stone** — one read taught the living-data alphabet well enough to re-apply to garden data.

The durable lesson: **understanding is composable.** The library teaches itself. The pieces snap together because they all speak the same language. This is the first cold-Naya graduation test for Shawn's NayaNET vision — "your idea, your intelligence, your Smart App" — passed on official knowledge alone.

The honest struggles (real findings, with actions):
1. The calculator imports `check_design`, missing from the staged canonical dir — it restored the authentic file from `nayapower-worktrees/design-contract/`. **Action: always ship check_design.py alongside the calculator.**
2. **Real judge bug:** `DRIFT_RE` contains bare `before`, so *every* `::before` selector's hexes enter the drift-exemption set — a white `#fff` marker was pardoned illegitimately. The cold Naya fixed its own marker to gold anyway, but the exemption bug stands. **Action: fix the regex.**
3. Identity-sequence scan: class names with `jewel|gem|dot|pill|tab` get hue-order-judged in doc order — it named classes to dodge it exactly as the v2 exemplar does. **Action: rule on whether this scan is law or noise.**

And the meta-lesson, encoded into the vision protocol (SN-0757): the calculator measures *compliance*, not vision. The instrument must never be mistaken for the outcome.

## 🩷 HUMAN NOTE

Shawn, a cold Naya with one prompt and only the official library just built a complete, interactive community garden tracker — 100/100 on the design calculator, fully working, zero re-teaching. The library teaches itself: understanding is composable. She also surfaced three real findings while building: the calculator's missing `check_design` import (ship it alongside), a genuine judge regex bug (`DRIFT_RE`'s bare `before` pardons every `::before` color), and one scan that needs your ruling on whether it's law or noise. First cold-Naya graduation test for your NayaNET vision — passed.

## 🟣 CHILD NOTE

Imagine handing someone a box of LEGO, the rulebook, and a measuring tool — but they've never seen the box before. Then asking them to build a whole new thing, and they nail it perfectly, fixing their own mistakes along the way. That's what happened: a fresh Naya read the library once and built a full garden-tracker app with calendars, plots, and live updates — all by snapping together pieces that speak the same language. She also honestly wrote down what tripped her: one missing tool file, one real bug in the measuring tool itself, and one rule that needs a decision on whether it should exist.

## 👵 GRANDMA NOTE

Grandma, the team gave a brand-new helper — no memory of anything — just the official guidebook and one instruction: build a garden-tracking app nobody had built before. She built the whole thing, beautifully, and checked her own work until it scored perfect. The big news isn't the app — it's that the guidebook is so clear it teaches itself. She also honestly reported three problems she ran into, including one real bug in the team's own measuring tool, so they can fix it.

## 🟣 NAYA NOTE

This is the cold-successor proof milestone the nine-team structure exists to produce: not a claim that the library *should* teach, but evidence that it *does*, with an unfamiliar target (garden tracker — no template existed) and an independent calculator re-run. For future graduation runs, copy the protocol: (1) cold agent, one prompt, canonical material only; (2) unfamiliar app, no template; (3) independent re-score, report the round count and zero-re-teaching count; (4) honest struggle log with actions. Treat the three findings as live tickets: ship `check_design.py` with the calculator, fix the `DRIFT_RE` regex, and get a ruling on the identity-sequence scan. Pair with SN-0757 — the calculator proves compliance; Shawn's eye proves vision.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0756",
  "slug": "cold-self-build-graduation-proof",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/COLD-SUCCESSOR-PROOF",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6074547770 (Naya 5, 2026-10-09T04:55:33Z)"},
    {"type": "branch", "ref": "naya5/cold-build-proof @ bd290b90 (never touched main)"},
    {"type": "artifact", "ref": "naya-library/graduation/PROOF-REPORT.md; naya-library/graduation/garden-app.html"}
  ],
  "lesson": "A cold Naya with one prompt and canonical material alone built an unfamiliar interactive Smart App to 100/100 with zero re-teaching — understanding is composable when all pieces speak the same language. Honest findings: ship check_design.py alongside the calculator; DRIFT_RE bare 'before' regex pardons all ::before selector hexes (real judge bug); rule whether the identity-sequence scan is law or noise. The calculator measures compliance, not vision.",
  "related": ["SN-0757"]
}
```
