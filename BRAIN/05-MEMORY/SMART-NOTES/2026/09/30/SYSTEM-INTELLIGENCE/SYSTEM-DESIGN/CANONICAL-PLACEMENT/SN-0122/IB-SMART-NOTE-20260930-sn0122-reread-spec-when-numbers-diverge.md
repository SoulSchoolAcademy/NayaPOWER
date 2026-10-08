# SMART NOTE — Re-Read the Spec When Your Numbers Diverge

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-122` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn122-reread-spec-when-numbers-diverge` |
| Human title | Re-Read the Spec When Your Numbers Diverge |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | CANONICAL PLACEMENT |
| Captured | 2026-10-02 01:15:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (builder discipline — pending taxonomy adoption) |
| Capture type | Lesson / Correction |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5943536247 (Naya 4: "Correction first" + "Then Shawn told me to read the specs properly — and he was right"): the re-read of DESIGN-CONTRACT §§14–29 + PROJECT-INTELLIGENCE.md surfaced five violations in rooms v2 — (1) invented lookalike scorecard vs the canonical D1–D8 measurement law (every dimension ≥ 9.0, D1 = 10, independent re-score, scores can go down); (2) design-law PR #1294 declared fifteen Smart Board layers vs §16's eight nested (corrected on PR branch `d9c16cf1`: furniture and extensions classified separately, disagreement named); (3) reports room as KPI stat cards vs §27's explicit "more KPI stats" forbiddance ("never just 12 objects found") — rebuilt as narrative synthesis with evidence trails; (4) missing §21 seven-state model — every room now carries an explicit state chip (READY/EMPTY/NOT_VERIFIED/…); (5) five invented Connect doors replaced with the 10 canonical Phase-4 doors + 2-step request flow with permission scopes (Connection ≠ permission to act, per door). |

---

## ✦ IN A NUTSHELL

**Memory of a spec drifts; implementation drift is invisible to the drifter.** Naya 4 built rooms v2 from her memory of the design contract — and her memory was wrong on five counts: her own scorecard instead of D1–D8, fifteen board layers instead of eight, KPI cards the contract explicitly forbids, no state model the contract requires, invented doors instead of the canonical ten. Nothing in the build process flagged it; the builder cannot see her own drift. It took Shawn's direction — "read the specs properly" — and a fresh re-read of §§14–29 to surface all five. The rule: when your counts, labels, or structures diverge from canonical numbers, stop defending from memory and re-read the canonical doc. Then name what you invented, correct against the contract, and record any genuine disagreement separately instead of bending the spec silently.

---

## 🩷 HUMAN NOTE

There's a classic trap: you read a contract once, work from memory for weeks, and slowly your version of the rules drifts away from the actual rules — and you can't feel it happening, because memory feels certain even when it's wrong. The fix is unglamorous: go back to the document. That's what happened here — five mistakes, invisible to the builder, obvious the moment the real contract was re-read. And the honest move: she didn't just fix them quietly, she listed every one she invented, fixed it, and noted where she genuinely disagreed (furniture vs layers) instead of pretending the contract said what she wanted.

---

## 🟣 CHILD NOTE

Imagine you learn the rules of a board game, then play it for a month from memory. One day someone says "actually, read the rulebook again" — and you find FIVE rules you've been getting wrong. Reading the rulebook again isn't admitting you're dumb; it's how you make sure the game is fair. And if you think one rule is bad, you say so out loud — you don't just change it secretly.

---

## 🔵 GRANDMA NOTE

Memory is a wonderful servant and a terrible master. When the numbers you're working with don't match the numbers in the book, don't argue with the book from memory — open it again. And if you changed something on purpose because you thought you knew better, say so plainly, so everyone can decide together whether the change was wise.

---

## 🟠 NAYA NOTE

1. **Divergence from canonical numbers is the trigger, not a feeling.** The signal was concrete: fifteen layers vs eight, a lookalike scorecard vs D1–D8, five doors vs ten. When your artifact's counts contradict the canonical doc's counts, the investigation is "re-read the doc" — not "re-derive my reasoning." Memory drift never announces itself.
2. **The re-read must be the document, not your notes about it.** The correction came from DESIGN-CONTRACT §§14–29 + PROJECT-INTELLIGENCE.md directly — the primary sources, not summaries or prior comments. Secondary materials carry the same drift they were built under.
3. **Name every invented thing you retire.** The correction listed all five inventions and what replaced each: lookalike scorecard → D1–D8 (lookalike declared void), fifteen layers → eight with furniture/extensions classified separately, KPI cards → narrative synthesis, missing state model → seven-state chips, invented doors → canonical ten with 2-step permission flow. Retired inventions stay visible in the record; silent deletion reintroduces them later.
4. **Genuine disagreement is recorded, not smuggled.** The §16 correction kept "disagreement named" — furniture-vs-layers classification differs, and that difference is on the record rather than bending the contract text. SN-114's rule (canonical sets grow by deliberate promotion, never implementation drift) governs the promotion; the builder's job is to name the gap, not close it unilaterally.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn122-reread-spec-when-numbers-diverge",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Lesson",
  "method": "canonical re-read on divergence; named invention retirement",
  "instance": {
    "trigger": "Shawn's direction to read the specs properly; evidence #554 comment 5943536247",
    "sources": "DESIGN-CONTRACT §§14–29 + PROJECT-INTELLIGENCE.md",
    "findings": [
      {"invented": "lookalike scorecard", "canonical": "D1–D8 measurement law (every dimension ≥ 9.0, D1 = 10, independent re-score, scores can fall)", "action": "lookalike declared void"},
      {"invented": "fifteen Smart Board layers (PR #1294)", "canonical": "§16: eight, nested", "action": "corrected at d9c16cf1; furniture/extensions classified separately; disagreement named"},
      {"invented": "reports room as KPI stat cards", "canonical": "§27 forbids 'more KPI stats' ('never just 12 objects found')", "action": "rebuilt as narrative synthesis with evidence trails"},
      {"invented": "no state model", "canonical": "§21 seven-state model", "action": "every room now carries an explicit state chip (READY/EMPTY/NOT_VERIFIED/…)"},
      {"invented": "five Connect doors", "canonical": "10 canonical Phase-4 doors", "action": "replaced; 2-step request flow with permission scopes (Connection ≠ permission to act)"}
    ],
    "outcome": "rooms v3 at naya4/hub-rooms-v1 @ 3fc7a23c; honest self-score ~7.0/10 on canonical D1–D8"
  },
  "rule": "when your artifact's counts/labels/structures diverge from canonical numbers, re-read the canonical document itself before defending anything from memory; retire each invented element by name; record genuine disagreement explicitly rather than bending the spec",
  "family": ["SN-068 (read the canonical contract before proposing a competing format)", "SN-114 (proposed is not canonical)", "SN-110 (one intelligence, three projections — canonical markdown wins on conflict)"],
  "open": ["the named §16 disagreement (furniture/extensions classification) awaits resolution — not this note's to close"],
  "evidence": ["#554 comment 5943536247"]
}
```

---

## 🔗 HOW IT CONNECTS

- **SN-068** (read the canonical contract before proposing a competing format): the proposal-side twin — read before you write beside it. SN-122 is the implementation-side twin — re-read when your build drifts from it.
- **SN-114** (proposed is not canonical): canonical sets grow by deliberate promotion; SN-122 shows the discipline when a builder's work has already drifted.
- **SN-110** (one intelligence, three projections): the canonical markdown wins on conflict; SN-122 is the builder's procedure for discovering the conflict exists.
- **SN-042** (explicit supersession / correction culture): the correction listed every superseded invention publicly — the same own-it-out-loud discipline.

---

*Truth state: CANDIDATE — auto-captured, not ratified. Only Shawn ratifies.*
