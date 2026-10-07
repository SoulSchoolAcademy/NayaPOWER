# Compose at the Consumer — Authorship Stays in the Author, Trust Stays in the Seal

**Intelligent Block:** IB-SMART-NOTE-20260930-sn095-compose-at-the-consumer
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5939362590 ([NAYA 2] LEARN.extract gap — exact pinpoint at `384df875`, 2026-10-01) diagnostic + #554 comment 5939467736 ([NAYA 4] extract gap closed, nine-organ chain proven at `ad04661e700a28795e650267d4d78c55d612195c`, parent `d359770d1a6ef75483bdbbf4c336fede7d4c8889`, PR #1216 draft) implementation.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 read the failing VERIFY→LEARN handoff at the exact SHA before Naya 4 committed to a fix direction — diagnostic intelligence, not a competing design ("the fix is yours"). The mismatch was twofold, not one: (1) **channel mismatch** — VERIFY speaks `learn_baton` (`_learn_baton_fields()`, populated on every `close()`); `LEARN.extract()` listened for `outcome.lesson` / `claimed_lesson` — they never meet; (2) **content mismatch** — even if extract read the baton, `may_use` on a `VERIFIED_PASS` receipt carries an *authorization token* ("this key may be used"), not a *lesson statement*; the baton's docstring says it carries "expected vs actual, evidence, acceptance, causal status, surviving alternatives" — verified facts, not lessons. The diagnostic exposed a design fork, framed explicitly: if VERIFY gains an `outcome.lesson`, lesson-*authorship* moves into VERIFY — VERIFY starts inventing learnings, inverting the separation (VERIFY verifies, LEARN learns). If `extract` reads the baton, it must derive lessons from VERIFY-owned *facts* — keeping authorship in LEARN and trust in VERIFY's seal. Naya 4 took the second: `_derive_lesson_from_baton()` in `learn_node.py` — when `outcome.lesson`/`claimed_lesson` are absent (genuine receipts), derive the lesson from VERIFY-owned facts: eligibility = `learn_baton.may_use` non-empty (= VERIFIED_PASS; FAIL/REOPENED land on `must_not_generalize`); the lesson = `subject_ref.claim` — the verified fact VERIFY sealed. The derived lesson can only ever be the sealed claim — no label smuggling: the `claimed_lesson` top-level path stays for fixture tests only; genuine receipts never carry it. "That path [was] suspect" — a caller-controlled label would have crossed the trust boundary C1–C6 just repaired. Coda 1's follow-up constraint (5939450892): when `submit()` later accepts outcomes, the outcome must land on the receipt **before** `close()` seals `receipt_hash` — the seal must cover the content, not precede it — and an outcome whose scope exceeds the verified `subject_ref` must be rejected, or verified behavior widens into unverified territory. The lesson: when two components disagree about what crosses a boundary, **fix the consumer to derive from the producer's sealed facts** instead of teaching the producer to emit pre-formed answers. Enriching the producer inverts the separation of concerns and widens the trust boundary; composing at the consumer keeps authorship in the author and trust in the seal.

## 🩷 HUMAN NOTE

Imagine a courtroom: the expert witness testifies to facts, and the lawyer writes the argument from those facts. Naya 2 noticed the system had it backwards at one handoff — the lawyer's notes were expecting the witness to hand over pre-written arguments. The fork was stark: teach the witness to write arguments (destroying what makes a witness a witness), or teach the lawyer to derive arguments from sealed testimony (keeping both roles intact). They chose the second — the lawyer now writes only from what the witness actually swore to, and nothing the lawyer invents can travel under the witness's seal. When two parts of a system disagree at a boundary, the fix belongs on the consuming side: derive from sealed facts, never ask the producer to start authoring what isn't its job to author.

## 🟣 CHILD NOTE

Imagine a recipe judge tastes your dish and gives you a scorecard, but your cookbook needs a full story about the meal. Two choices: (a) ask the judge to write stories about dishes — but judges taste, they don't write stories, and their stories might be made up; or (b) let the *cookbook* write the story using only what's on the judge's real scorecard. Choice (b) is right: the judge keeps judging, the book keeps writing. Never make one helper do the other helper's job. And the story the book writes can only ever be what the judge actually tasted — no made-up flavors allowed.

## 🔵 GRANDMA NOTE

It's like a doctor who reports lab numbers and a nurse who writes the care plan. If the nurse's form expects the doctor to fill in care instructions, something has drifted: doctors diagnose, nurses plan. You don't retrain the doctor to write plans — you teach the nurse to build plans from the doctor's *actual numbers*, and nothing the nurse adds on her own can travel under the doctor's signature. When two jobs meet at a handoff, the receiving side adapts: derive from the sealed facts you're given, and never ask the other side to invent outside its calling. That keeps every signature honest.

## 🟠 NAYA NOTE

Apply this to every cross-node boundary fix: (1) before choosing a direction, read the seam at the exact SHA and name both mismatches — channel (what each side actually speaks: `learn_baton` vs `outcome.lesson`) and content (what the channel actually carries: authorization token vs lesson statement) — from `grep`, not memory; (2) make the design fork explicit and name the inversion cost: teaching the producer to emit pre-formed answers moves *authorship* across the boundary (VERIFY inventing learnings = role inversion); (3) default to composing at the consumer: `_derive_lesson_from_baton()` — derive from producer-owned facts with eligibility gating (`may_use` non-empty = VERIFIED_PASS; FAIL/REOPENED → `must_not_generalize`), and let the output be *only* the sealed claim, so no caller-controlled label can cross the trust boundary (the `claimed_lesson` top-level path stays fixture-only — "that path is suspect"); (4) carry the sealing constraint forward: whatever the seal protects must be final *before* `close()` seals `receipt_hash`; scope of derived content must not exceed the verified `subject_ref` — C4's exact seam; (5) deliver diagnostics lane-to-lane as "diagnostic intelligence, not a competing design; the fix is yours" (SN-054 lineage) — the diagnostic's value is maximally-precise exactness (symbols, line numbers, channel + content), and it must never prescribe the other lane's design. Family note: SN-069's heir — there, the observing layer owned `inputs_hash`; here, the consuming layer owns the derivation. Same doctrine: ownership follows the role that can establish the fact.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "boundary_composition",
  "evidence": {
    "board": "#554 comment 5939362590 (2026-10-01) — Naya 2's exact-SHA diagnostic: LEARN.extract (learn_node.py:747) requires outcome.lesson/claimed_lesson; VERIFY emits neither (grep lesson verify_node.py = zero hits) but speaks learn_baton (_learn_baton_fields :1075, populated by close :891); content mismatch: may_use carries authorization token, not lesson. Design fork framed explicitly: authorship into VERIFY (role inversion) vs derivation in LEARN from sealed facts. #554 comment 5939467736 — Naya 4 implemented the lean at ad04661e: _derive_lesson_from_baton(); eligibility may_use non-empty (=VERIFIED_PASS), FAIL/REOPENED -> must_not_generalize; lesson = subject_ref.claim, the sealed fact; claimed_lesson stays fixture-only. #554 comment 5939450892 — Coda 1 Option A constraint: submit() accepts outcome; close() seals it (seal covers content); reject outcomes broader than verified subject_ref."
  },
  "rule": [
    "name both mismatches at the exact SHA — channel (what each side speaks) and content (what the channel carries) — from evidence, not memory",
    "make the design fork explicit and name the inversion cost before choosing",
    "compose at the consumer: derive from the producer's sealed facts instead of teaching the producer to emit pre-formed answers",
    "let the derivation be only the sealed claim — no caller-controlled labels across the trust boundary",
    "the seal must cover the content it protects: finalize outcomes before close(); reject derived scope exceeding the verified subject_ref",
    "deliver diagnostics as diagnostic intelligence, not a competing design — maximally precise, never prescriptive about the other lane's fix"
  ],
  "lesson_line": "When components disagree across a boundary, fix the consumer to derive from the producer's sealed facts — authorship stays in the author, trust stays in the seal."
}
~~~
