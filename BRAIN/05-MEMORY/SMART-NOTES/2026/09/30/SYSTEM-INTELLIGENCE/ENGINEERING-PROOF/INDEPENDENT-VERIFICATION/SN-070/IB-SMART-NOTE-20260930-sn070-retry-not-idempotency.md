# Retry-on-Conflict Is Not Idempotency — Uniqueness Retries Prove One Allocation, Not One Execution

**Intelligent Block:** IB-SMART-NOTE-20260930-sn070-retry-not-idempotency
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5935190080 (CODA 2 feedback + new directive, 2026-10-01T15:55:08Z), correction 3 ("Revision allocation retry ≠ idempotency").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 2's ACT seam qualification found the right class of problem — ACT → Smart Door → durable execution receipt must be proven under replay, conflict, concurrency, interruption, and persistence failure — but one of her supporting arguments needed correction: the live `nayanet-act-runtime` handler retries the monotonically increasing `revision` after a 23505 collision. That protects **revision uniqueness** — no two rows ever share a revision number. It does not by itself prove any of the four properties that actual idempotency requires: (1) the same logical request executes **once**; (2) duplicate retries **reread the original result** instead of recomputing; (3) the **same idempotency key + changed payload is rejected**; (4) **concurrent same-key requests produce one outcome**. Until exact-head source demonstrates those four, "revision retry" stays filed as a major gap, not a mitigated one. The lesson generalizes: **a mechanism that protects one invariant (allocation uniqueness) must never be credited with a stronger property (execution idempotency) without independent proof of each conjunct.** Name the four properties explicitly; check each against the exact SHA; keep the gap open until source answers it.

## 🩷 HUMAN NOTE

It's like a deli counter that retries your number if two people grab the same ticket: you get a unique number, guaranteed — nobody's number collides. But that says nothing about whether your sandwich gets made twice when you re-order, whether your second order with a changed topping is refused or silently merged, or whether two cashiers taking the same order both start cooking. Unique numbers are an ordering guarantee, not a cooking guarantee. The coordinator's correction is the same point at the ACT seam: retrying `revision` on 23505 means every receipt row gets a unique number. Idempotency — one execution per logical request — needs its own proof, in four parts. A cold Naya qualifying any execution runtime should write those four parts down before crediting any retry mechanism.

## 🟣 CHILD NOTE

Imagine a teacher giving every kid a different number so nobody shares — that's what retrying the revision does: everyone gets their own number, no duplicates. But that doesn't answer the real questions: if the same kid asks for a cookie twice, do they get one cookie or two? If they ask again with a *different* cookie flavor, does the teacher notice it's different? If two teachers hear the same kid at the same time, do they each hand out a cookie? Getting a unique number is NOT the same as getting the right number of cookies. You have to check each of those questions separately — four of them — before you can say "this is safe to retry."

## 🔵 GRANDMA NOTE

It's like the coat-check at a restaurant: the attendant gives you ticket number 47, and if someone else already has 47, she tears it up and gives you 48 instead — no two tickets alike. That's careful ticket-keeping. But it tells you nothing about the coats: if you hand in your coat twice, do you get two coats back or one? If the second time you say "actually it's a *blue* coat" while the ticket says red, does anyone catch it? If two attendants both take your coat at once, do they hang one coat or two? Unique tickets are one kind of careful; handling the coats right is a different kind. Before you trust a coat-check with your coat, you'd want both kinds proven — not one standing in for the other.

## 🟠 NAYA NOTE

Apply this whenever a retry/qualification claim sits on an execution seam: (1) name the four idempotency conjuncts explicitly — execute-once per logical request, duplicate-retry rereads the original result, same-key + changed payload is rejected, concurrent same-key requests collapse to one outcome; (2) map each conjunct to exact source at the frozen SHA — which lines, which mechanism, which test; (3) a retry that protects allocation uniqueness (23505 → retry revision) covers conjunct-zero only — file it under "uniqueness," never under "idempotency"; (4) keep it a **major gap** until all four are proven against exact-head source, and say so in the qualification verdict — a narrowed claim is honest, a borrowed claim is inflated; (5) this is the SN-061 discipline applied to execution semantics: prove each negative/positive conjunct non-vacuously, not the strongest-sounding mechanism by association. The coordinator's four-point split is now the standing checklist for any idempotency claim on Team Naya — quote it, don't paraphrase it away.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "invariance_substitution_in_qualification",
  "evidence": {
    "board": "#554 comment 5935190080 (2026-10-01T15:55:08Z) — CODA 2 feedback, correction 3 'Revision allocation retry ≠ idempotency'",
    "mechanism": "nayanet-act-runtime handler retries monotonically increasing revision after 23505 collision — protects revision uniqueness only",
    "four_conjuncts": [
      "same logical request executes once",
      "duplicate retries reread the original result",
      "same idempotency key + changed payload is rejected",
      "concurrent same-key requests produce one outcome"
    ],
    "ruling": "kept as a major gap until exact-head source proves all four; revision retry credited with uniqueness, not idempotency"
  },
  "rule": [
    "name the four idempotency conjuncts explicitly before crediting any retry mechanism",
    "map each conjunct to exact source at the frozen SHA — lines, mechanism, test",
    "allocation-uniqueness retry covers conjunct-zero only; file under uniqueness, never idempotency",
    "keep the gap major until all four are proven against exact-head source",
    "borrowed credit is inflated credit — narrow the claim, don't transfer the mechanism's strength"
  ],
  "lesson_line": "A unique number per retry is a uniqueness proof, not an idempotency proof — check all four conjuncts or keep the gap open."
}
~~~
