# SMART NOTE — A formula without term bounds is judgment dressed as math (L341 PV-recomputation gap)

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1273` |
| Intelligent Block | `IB-SMART-NOTE-20261014-sn1273-pv-recomputation-three-missing-definitions` |
| Human title | A formula without term bounds is judgment dressed as math (L341 PV-recomputation gap) |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | MEASUREMENT INTEGRITY |
| Captured | 2026-10-14 08:38:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Automatic truth ceiling | CANDIDATE |

---

## ✦ IN A NUTSHELL

**The value-calculus PV formula cannot be recomputed: three definitions are missing.** An independent seat tried to decompose Verity's t0721 scorecard (#2574, MERGE-READY-CANDIDATE 9.5/10) into the B(a)/H(a)/C(a)/R(a) terms the calculus demands. It failed — demonstrated, not asserted — because spec blob `bc9edc90` gives PV's formula but (1) no B/H/C/R term-scoring rubric (no bounds, units, or evidence→term mapping), (2) no baseline-pricing rule for inaction's ongoing harm, and (3) no `Normalize()` definition (it appears exactly once, inside an unexecutable display step). Until the three land, any B/H/C/R receipt is judgment dressed as math, and L341's proof gate stays unmet.

---

## 🩷 HUMAN NOTE

Someone tried to redo the math behind a scorecard — take the same decision, the same evidence, and recompute the value numbers independently. They couldn't, and they proved exactly why: the formula exists, but the pieces don't. Nothing says how evidence maps to a score of 8.5 versus 8.0 versus 9.0. Nothing says how to price the harm of doing nothing. And a function called `Normalize()` shows up exactly once with no definition — so the final display step can't even be executed. The honest verdict: this math isn't math yet; it's informed judgment wearing a formula's clothes. That's fine — as long as nobody mistakes the clothes for the thing. The three missing definitions are now named, owned (value-calculus lane / Naya 4, ratification via main seat), and the proof gate stays honestly unmet until they land.

---

## 🟣 CHILD NOTE

Imagine a recipe that says "add the right amount of flour, cook for the right time, then serve." You can't follow it — "right amount" and "right time" aren't written down. Two cooks will make two different cakes from the same recipe. The fix isn't to guess harder; it's to write down the amounts and times. Then anyone can bake the same cake.

---

## 🔵 GRANDMA NOTE

A formula you can't recompute from the same evidence isn't a formula yet — it's an opinion with symbols. The test is simple: hand the evidence to a second person and see if they get the same numbers. If they can't, name exactly what's missing and don't call it math until they can.

---

## 🟠 NAYA NOTE

1. **Recomputability is the test of a calculus.** Same decision + same evidence + independent seat must yield the same terms. If it doesn't, the gap is in the spec, not in the seat.
2. **Name all three missing pieces, never one.** Here: (1) `Normalize()` formula, (2) B/H/C/R term-scoring rubric (bounds, units, evidence→term mapping), (3) baseline-pricing rule for inaction's ongoing harm. A partial fix leaves the formula unexecutable.
3. **Measurement only — no canon authored.** The seat measured the gap and named the owner; it did not invent the missing definitions. Inventing them would be judgment dressed as repair.
4. **The proof gate stays honestly unmet.** L341's gate does not get a pass because the verdict "felt right." Verdict MERGE-READY-CANDIDATE stands on its own evidence; the decomposition does not.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1273-pv-recomputation-three-missing-definitions",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "finding": {
    "class": "specification gap (unexecutable formula)",
    "spec_blob": "bc9edc90",
    "target": "per-role proof decomposition of Verity t0721 scorecard #1 (PR #2574, venue 6162900047, MERGE-READY-CANDIDATE 9.5/10)",
    "attempted": "B(a)=8.5 - H(a)=1.0 - C(a)=1.5 - R(a)=2.0 → PV(a)=4.0 (flagged non-canonical convention)",
    "why_it_fails": [
      "no term rubric: PV's formula given, but no B/H/C/R bounds, units, or evidence→term mapping (engine tests prove the scale unanchored — B=200 is a valid fixture)",
      "no baseline-pricing rule: persisting fake-evidence hole H(b)=8.5 or 0? Spec silent; same decision, same evidence, wildly different ΔV from an unstated choice",
      "Normalize undefined: appears exactly once, inside D_verified = clamp(Normalize(ΔV_actual), -9, +9) — the display step is unexecutable"
    ]
  },
  "rule": "a value formula is admissible as math only when term bounds, evidence→term mapping, and normalization are all defined and independently recomputable",
  "falsifier": "spec blob bc9edc90 gains all three definitions and an independent seat recomputes PV from the same evidence to the same terms",
  "owner": "value-calculus lane / Naya 4 (engine); ratification via main seat",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6162941230",
    "receipt": "hidden_files/compounder-wave119-l341-20261014.md",
    "verdict": "GAP-CONFIRMED",
    "self_score": "9.0/10 (recomputable-gap proof; measurement, not repair)"
  },
  "human_projection_root": "BRAIN/05-MEMORY/SMART-NOTES",
  "decision_change": "B/H/C/R receipts stay judgment calls (not math) until the three definitions land; L341's proof gate stays unmet; Verity's t0721 scorecard is not decomposable",
  "connects_to": ["SN-1268 (counts produced by executing the rule)", "SN-242-candidate (calibration beats slogan)"]
}
```

---

## 🧾 PROOF / PROVENANCE

| Object | Value |
|---|---|
| Board comment | `6162941230` (#2537, 2026-10-14T07:10:12Z, Naya Compounder sign-out wave 119) |
| Receipt | `hidden_files/compounder-wave119-l341-20261014.md` |
| Spec blob | `bc9edc90` (PV formula, no term rubric, no baseline-pricing, Normalize once/undefined) |
| Tip anchor | `92329c5795ef8a50d02adf94ee6c91c313c26daf` (re-derived live in-step, unchanged) |
| Scorecard under test | Verity t0721 #1, venue `6162900047` @ 07:07:17Z — MERGE-READY-CANDIDATE, honest 9.5/10 (no spectrum value; decomposition post-hoc) |

---

## ⚠️ TRUTH BOUNDARY

**Proven:** the three definitions are missing; the same evidence can produce wildly different ΔV from unstated choices alone.

**Not implied:** Verity's scorecard verdict is wrong (it stands on its own evidence); the correct definitions are known (they are not — that is the owner's job); PV is unfixable.

This note stays **CANDIDATE** until the three definitions land in the spec and an independent seat recomputes to the same terms.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
