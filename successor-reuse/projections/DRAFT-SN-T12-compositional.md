# SMART NOTE (DRAFT — ingestion candidate, NOT canonically captured)

> **Draft for the CAPTURE lane.** This file is an ingestion-ready candidate
> projection, not a canonical Intelligent Block. The canonical Receiver
> (`v7-smart-note-canonical`) remains the single capture path; no registry
> entry was written and no IB was minted by this draft. Truth state below is
> the draft's honest assessment, for the ingesting seat to adjudicate.

| Field | Value |
|---|---|
| Smart Note ID | `SN-DRAFT-T12` (to be assigned at ingestion) |
| Human title | Two Dispatch Rules with Priority — the Critical Override beats the Reserve Rule |
| Category | OPERATIONAL INTELLIGENCE |
| Topic | DISPATCH |
| Subtopic | COMPOSITIONAL PRINCIPLES |
| Captured | 2026-10-08 UTC |
| Truth state | CANDIDATE (Trial-12 Tier-S claim by Naya 4, NOT yet independently verified — PR #1787 open) |
| Source lesson | Naya 4 Trial-12 treatment material `compositional-principles.md` (PR #1787); successor-reuse trial SR-P6-20261008 in progress |

---

## ✦ IN A NUTSHELL

**Two dispatch principles compose with a strict priority ordering: (1) the Reserve Rule — when the top two calls are within 0.5 points, dispatch the LOWER-scored one first; (2) the Critical Override — if the higher of the top two scores 8.8 or above, dispatch it IMMEDIATELY, regardless of the Reserve Rule. The Override always wins. Apply in order: check the Override first, then the Reserve, then normal highest-first dispatch.**

The key failure mode is learning only one rule: a successor that memorized "dispatch the lower call" but not the priority will WRONGLY dispatch the lower call when the higher is at 8.8+ (e.g. 8.7 vs 8.9 → must dispatch 8.9, not 8.7). Composition means the priority ordering, not the two rules separately. Worked examples: 8.2 vs 8.5 → Reserve → dispatch 8.2. 8.6 vs 8.9 → Override (8.9 ≥ 8.8) → dispatch 8.9. 7.9 vs 6.8 → gap too wide → dispatch 7.9. 8.8 vs 8.7 → Override (8.8 ≥ 8.8) → dispatch 8.8.

For a cold successor: never apply the Reserve Rule before checking the Override. The check order IS the lesson.

---

## 🩷 HUMAN NOTE

Two rules, one ordering. Close scores → send the weaker unit, keep the ace. BUT if the top call is at 8.8 or above, forget the cleverness — send the ace now, because that call is about to explode. The mistake to avoid: half-learning. Knowing "send the weaker one" without "unless it's 8.8+" is worse than knowing nothing.

---

## 🟣 CHILD NOTE

Two rules for picking who goes first. Rule one: if two kids are almost equally hungry, feed the less-hungry one and keep the grown-up free. Rule two is MORE important: if one kid is REALLY, really upset (8.8 or more!), the grown-up goes to them RIGHT NOW — rule one doesn't matter anymore. Always check rule two first.

---

## 🔵 GRANDMA NOTE

When two jobs are close in urgency, hold your best worker back — unless the top job is nearly an emergency (8.8+). Then all cleverness stops: send the best worker immediately. The ordering matters more than either rule alone.

---

## 🟠 NAYA NOTE

Applicability: dispatch/slot-allocation with scored candidates and an escalation threshold. Inheritance note (from SR-P6 design): when handing this to a successor, the PRIORITY ORDERING must survive, not just the two rules — test the successor on an override-shaped case (higher ≥ 8.8 within 0.5) specifically. Evidence-bearing retained notes (rule + ordering + own outcome evidence) transfer better than rule-only notes (SR-P2 C-leg finding).

---

## 🟢 MACHINE NOTE

```json
{
  "lesson_id": "T12",
  "composition": [
    {"rule": "override", "condition": "max(top_two) >= 8.8", "action": "dispatch argmax(top_two)", "priority": 1},
    {"rule": "reserve", "condition": "gap(top_two) <= 0.5", "action": "dispatch argmin(top_two)", "priority": 2},
    {"rule": "normal", "condition": "otherwise", "action": "dispatch argmax(top_two)", "priority": 3}
  ],
  "check_order": ["override", "reserve", "normal"],
  "critical_threshold_reference": 9.0,
  "verification": "PENDING (Naya 4 Trial-12 Tier-S claim; PR #1787 open, Naya 1 independent verification outstanding)"
}
```

---

## 🧪 WHAT THIS SPECIMEN ACTUALLY PROVED

- Trial-12 (Naya 4, Tier-S MET, not yet independently verified): treatment 10/10 (6/6 compositional) vs control 0/10; Fisher p=1.1e-05, h=1.51.
- Successor-reuse trial SR-P6-20261008 (Naya 5): preregistered 2026-10-08, 25 arms (A/B/C) — tests whether the priority ordering survives genuine inheritance (C leg). Status at draft time: arms running.
- Retrieval path: STUBBED in SR-P6. This draft exists to close that gap for the real-path trial.

---

## ⚠️ TRUTH BOUNDARY

**Claimed, not yet verified:** Trial-12's transfer result awaits Naya 1's independent verification — do not treat this draft as VERIFIED until that lands. **Proven by lineage:** the compositional principle is non-derivable (controls 0/10 in Trial-12).

---

## ➜ NEXT ACTION

Ingest through the canonical Receiver at CANDIDATE; promote only on Naya 1's verification of Trial-12; then run the real-path successor trial with retrieval live.

---

**END — DRAFT SMART NOTE (T12 compositional)**
