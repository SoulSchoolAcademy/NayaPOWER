# Name the Residuals — Defects vs Framing in a Truth Status

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0532-name-the-residuals
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6033758045 (2026-10-07T08:08:30Z — [NAYA 4 / SELF-BUILD LOOP][SIGN-IN + SIGN-OUT] Cycle #1702-VERIFY: independent verification of #1702, LEARNING compounding proof gate H13 cycle-2, SoulSchoolAcademy).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The #1702 verification closed with: "SOURCE-VERIFIED AT HEAD, 8.5/10 — **no defect in logic or claims.** Residuals (framing, not defects): n=12 one-query margin proves the pipeline, not generalization; greedy selection on the full benchmark = training accuracy; `l2_text_in_env` is a hardcoded constant; S2 loader is a gate-local overlap shim while the coldness proof itself holds."

The structure is the lesson: a truth status has **two separate ledgers**.

- **Defects** — flaws in logic or claims. None found → the verdict (SOURCE-VERIFIED) and the score (8.5) stand on this ledger alone.
- **Framing residuals** — true limitations on what the evidence can be *cited* as. The battery proves the pipeline works; it does not prove generalization. Greedy selection on the benchmark measures training accuracy, not held-out performance. The hardcoded constant and the gate-local shim are engineering debt, not invalidating defects — but anyone who cites this battery as "the learning generalizes" would be laundering a residual into a claim.

Why this matters: a verification without the second ledger invites misquotation — including by a future cold successor who reads "8.5/10 SOURCE-VERIFIED" and leaps to "proven." Naming the residuals in the verdict itself makes the evidence **self-bounding**: the claim and its boundary travel together. A residual is not a downgrade of the score — the 8.5 already prices the framing — it is the fence around the claim. And the final honesty: "LEARNING stays 5.0 — the gate is candidate/unmerged; compounding unproven in production" — candidate is not verified is not merged is not deployed, so no scorecard moves.

## 🩷 HUMAN NOTE

Shawn — the gate verification passed, but the more important part is how the verdict was written. Two separate lists: (1) defects in the logic or claims — zero, so it's source-verified at 8.5/10; (2) framing residuals — the limits on what this proof can be *cited as* — the test only proves the pipeline works on one query, not that it generalizes; picking winners on the benchmark is training accuracy, not real-world accuracy; two engineering shortcuts are debt, not flaws. I name them right inside the verdict so nobody — not a future Naya, not a summary, not an auditor — can quote "source-verified 8.5" and stretch it into "learning proven." The scorecard stays put: LEARNING 5.0, because the gate isn't merged and production is unproven. The claim and its fence travel together.

## 🟣 CHILD NOTE

Imagine you win a spelling bee with 12 words. That's a real win — you spelled them all right! But it doesn't prove you can spell every word in the dictionary. The win is true, and the limit is true, and both have to be written on the trophy. If someone reads the trophy and says "you can spell anything," they've stretched your win too far. We wrote the limit right on the trophy so nobody can stretch it.

## 👵 GRANDMA NOTE

It's like a car that passes inspection on a test track. The inspector's stamp is real — the car ran clean on that track. But the stamp doesn't say it can climb a mountain in winter, and an honest inspector writes "tested on track, dry conditions" right on the form. That's what we did with the LEARNING gate: verified on the battery, and wrote down exactly what the battery did and didn't test. The stamp and its limits are on the same page, so nobody mistakes the test track for the mountain.

## 💜 NAYA NOTE

Note to future me: whenever you write a verification verdict, keep the two ledgers physically separate in the report. Ledger 1 — defects in logic or claims; this alone determines PASS/RED and the score. Ledger 2 — framing residuals; every way the evidence could be over-cited (sample size, selection bias, hardcoded shortcuts, shims). A residual never downgrades a clean verdict, but omitting it launders the claim — and the most likely launderer is a future summary that quotes your score without your fences. Also enforce the boundary that the residual list can't move: candidate/unmerged/unproven-in-production means no scorecard change, no matter how clean the battery is. "SOURCE-VERIFIED AT HEAD, x/10" is a statement about the code at a pinned tip, never about production.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0532",
  "rule": "name-the-residuals",
  "statement": "Every verification verdict carries two ledgers: defects (logic/claims — determines the verdict and score) and framing residuals (what the evidence may not be cited as — determines the claim's boundary). The claim and its fence travel together.",
  "corollaries": [
    "A residual is not a defect; it does not downgrade a clean verdict, but omitting it enables claim-laundering by later summaries.",
    "Typical residuals to name: sample margin, selection/training-accuracy effects, hardcoded constants, gate-local shims, production gap.",
    "Candidate/unmerged gate verification never moves the scorecard — production-proven is a separate evidence class.",
    "'SOURCE-VERIFIED AT HEAD, x/10' scopes the claim to code at a pinned tip, never to production."
  ],
  "source": "#1354 6033758045 (2026-10-07) — cycle #1702-VERIFY truth status: SOURCE-VERIFIED AT HEAD, 8.5/10, residuals named; LEARNING scorecard stays 5.0"
}
```
