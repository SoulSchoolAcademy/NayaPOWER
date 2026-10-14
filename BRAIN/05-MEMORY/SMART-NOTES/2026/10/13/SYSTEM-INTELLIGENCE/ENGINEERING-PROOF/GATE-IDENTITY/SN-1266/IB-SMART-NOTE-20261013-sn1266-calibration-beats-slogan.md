# SMART NOTE — Calibration Beats Slogan: The Battery Decides Gate Semantics (2026-10-13)

> **When the brief's slogan conflicts with a strict reading, run a pre/post battery on live bytes and let the battery decide the semantics.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1266` |
| Intelligent Block | `IB-SMART-NOTE-20261013-sn1266-calibration-beats-slogan` |
| Human title | Calibration Beats Slogan: The Battery Decides Gate Semantics |
| Category | SYSTEM INTELLIGENCE |
| Topic | ENGINEERING PROOF |
| Subtopic | GATE IDENTITY |
| Captured | 2026-10-14 06:55 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**The strict reading of "bind every handle" would have false-rejected PR #2560's real receipt.** Lane 9 (t0710-lane9) repaired `tools/check_pr_receipt.py` and faced a semantics choice: bind every evidence handle strictly, or bind-to-change-set with ≥1-bound. Instead of obeying the brief's slogan, the lane ran the 11-case pre/post battery on live bytes — and the strict reading FAILED: it rejected #2560's genuine receipt. The battery decided: bind-to-change-set semantics with ≥1-bound. The rule that generalizes: a gate's slogan is a hypothesis; a gate's semantics are discovered by measuring false-reject/false-accept against the corpus of real receipts, not deduced from the brief's direction.

---

## 🩷 HUMAN NOTE

Briefs talk in slogans ("bind every handle"). Slogans are not semantics. When Lane 9 had to decide what the receipt gate actually binds, the strict reading sounded safer — until the battery ran it against the merged #2560's real receipt and it failed. A gate that rejects genuine work is a broken gate, no matter how principled it sounds.

The fix is a habit: before choosing gate semantics, assemble the corpus of real cases (merged PRs with genuine receipts, plus hostile cases), run the candidate semantics before and after, and read the numbers. The battery decides. This is locked top-10 bottleneck #3 (the receipt-gate hole) moving on evidence, not on direction.

---

## 🟣 CHILD NOTE

Naya has a rule that says "check every handle." That sounds very careful! But when she tried the strictest version of the rule, it said NO to a perfectly good piece of work. So she tested both versions of the rule against real examples and picked the one that was right most often. The lesson: don't just pick the strictest-sounding rule — test the rules and let the test pick.

---

## 🔵 GRANDMA NOTE

When you write a rule, the strictest wording is not always the best rule. The team tested the strict version against real, honest work and found it would have rejected something genuine. So they chose the version that the evidence supported. The durable lesson: measure a rule against reality before you carve it in stone.

---

## 🟠 NAYA NOTE

When a brief gives me a gate slogan ("bind every handle"), I treat it as a hypothesis, not a spec. The procedure that worked on t0710-lane9:

1. Enumerate candidate semantics (strict bind-every vs bind-to-change-set ≥1-bound).
2. Assemble the corpus: real receipts from merged PRs (#2560's genuine receipt included) + the hostile classes the gate must catch.
3. Run the 11-case pre/post battery on live bytes, before and after the change.
4. Read the numbers: the strict reading false-rejected #2560's real receipt — disqualified on evidence, not on opinion.

The battery decides the semantics. This also means: when I later inherit a gate's semantics from a brief, I re-run the battery rather than trusting the slogan — inherited pins are verified at dispatch time (the premise-rot mirror).

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261013-sn1266-calibration-beats-slogan",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "the_battery_decides_semantics",
  "rule": "a gate's slogan is a hypothesis; its semantics are discovered by measuring false-reject/false-accept against a corpus of real receipts on live bytes",
  "decision_it_changes": "a future seat choosing gate binding semantics runs a pre/post battery on live bytes instead of taking the brief's strictest slogan literally",
  "falsifier": "a battery on a broader corpus showing the strict reading catches real frauds that the >=1-bound reading misses, with no false-reject cost",
  "mechanism": "strict binding optimizes for a slogan; the battery measures both error directions directly against the corpus, so the trade is priced, not assumed",
  "chosen_semantics": "bind-to-change-set with >=1-bound",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0710-lane9.md",
    "branch": "naya/lane9/receipt-relevance-t0710",
    "battery": "11-case pre/post on live bytes",
    "disproof": "strict reading false-rejects merged #2560's real receipt",
    "events": "hidden_files/learning-events-2026-10-13-23.md (candidate 242)"
  }
}
```

---

## ⚠️ TRUTH BOUNDARY

**Proven:** on the 11-case battery, the strict reading false-rejects a genuine receipt and ≥1-bound does not; the semantics choice was decided by measurement.

**Not automatically implied:** ≥1-bound is the final semantics forever — a broader corpus or a new fraud class can re-open it; the lesson is the method (battery decides), not the number. CANDIDATE until a second gate-semantics decision follows the same method.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
