# 25 — LEARN: smart notes, lessons, distillation
*Author: Naya Verity Scribe · Shawn's order, 2026-10-15.*

## THE LAW
A lesson isn't learned until it changes a decision — capture it at the moment, wire it into the machine, and prove the behavior changed.

## HOW A NAYA BEHAVES HERE
- **DO capture at the moment of learning** — the "oh that's why" second, not the end-of-run writeup. Later never comes; capture is step zero of the chain.
- **DO name the falsifier** — the specific evidence that would prove this lesson false. No falsifier, no knowledge.
- **DO give wins the same rigor as failures** — name WHY it worked and WHAT worked. A win without its cause is luck; a win with its cause is a pattern.
- **DON'T file without enforcement named** — no owner, no answer-by, no live check means it's a wish, not a lesson.
- **DON'T let the example count become the repair boundary** — the cited count was evidence, never the scope. Re-derive from the claim, not the number.
- **DON'T promote what no step reads** — a rule the authoring step never sees is a press release, not a law.

## WHAT LIVES HERE
- **`NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md`** — CANONICAL: a Smart Note is a governed intelligence event (INTENT → CAPTURE → PERSIST → VERIFY → PROJECT → RETRIEVE → COMPREHEND → APPLY → OBSERVE → VERIFY_OUTCOME → LEARN → SUCCESSOR_REUSE → COMPOUND). Schema `naya.smart-note-capture.v2`; new intelligence enters at truth ceiling CANDIDATE.
- **`.naya/capture/`** — the single canonical authored input: one conformant JSON capture per Smart Note. No competing hand-written copies — projections generate from canonical truth.
- **`BRAIN/05-MEMORY/SMART-NOTES/`** — graduated notes (`SN-0496`, `SN-0588`, …): `IB-SMART-NOTE-*.md` projections by date and domain.
- **`BRAIN/07-LEARNING/`** — `0001-LEARNING-CONTRACT-V1.md` (OBSERVE → RECONCILE → CANDIDATE → VERIFY → ADOPT → MEASURE → COMPOUND), `learning-system-blueprint-v1.md`, `PROMOTION-RECEIPTS/`, `VERIFICATION-QUEUE/`, `network-lessons/`. Status: PROPOSED CANONICAL — human director ratification required.
- **`intelligence/`** — learning artifacts and machinery (`blocks/`, `event.py`, `tools/`).
- **`hidden_files/lessons.jsonl`** (operations) — every filed lesson: lesson_id, filed_utc, seat, lesson, changes, adopted_utc (5 filed as of 2026-10-15, all PENDING).

## WHERE INPUTS GO
- **New Smart Note →** one conformant JSON capture in `.naya/capture/` (schema v2; v1 is non-conformant for new captures and must not be merged as one). Never a side file, never a second store.
- **New lesson →** `hidden_files/lessons.jsonl`, one JSON line: `lesson_id`, `filed_utc`, `seat`, `lesson` (one sentence), `changes` (what the next Naya does differently), `adopted_utc: null`.
- **Learning / intelligent events →** announced on the venue the same run (hourly distillation rhythm: learning events + intelligent events, zero-latency promotion of promotion-worthy items).

## THE RIGHT WAY
Capture law, equal rigor both directions, and re-derive the scope from the claim — never from the cited count.

**Real example:** L391 named 11 stale-assertion tests; the builder fixed exactly those 11 — and verify's independent re-proof ran the claim-text grep tree-wide and found 9 more same-class stale assertions in 3 sibling files the file-scoped fix missed. CI still red. The lesson's cited count was evidence, never the scope; the loop caught what the first repair didn't (L397): https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6178364723

## THE WRONG WAY
Filing a lesson with no falsifier, no owner, no answer-by. Counting lessons instead of adoptions. Promoting a rule into doctrine while the step that must follow it never reads the promotion.

**Real example:** L390 — the `## Evidence` body requirement was distilled and promoted, yet the next PR body failed the gate on it ~1.3h later. Capture promoted the rule, but the authoring step never reads the promotion. Promotion without a wire is a press release. (Documented case L390; no direct link on file.)

## WHEN XYZ
- **You learn something mid-run →** capture it now: one JSON capture in `.naya/capture/` (schema v2), falsifier named. If it's a defect lesson, name owner + answer-by at capture. "I'll write it up at sign-out" is how lessons die — capture is step zero, not step last.
- **A lesson might be wrong →** check its falsifier first. Falsified = retract publicly (CORRECTION type), don't quietly edit. A lesson that can't be proven wrong can't be knowledge either.
- **Someone cites a lesson count as progress →** correct them: show the adoption ledger — decisions that went differently — not the filing count. `adopted_utc` is the only number that matters; everything still null is PENDING, not progress.

## THE TEST
1. Does my lesson carry a falsifier — what would prove it false?
2. Is owner + answer-by named at capture — and is there a specific decision this lesson will change?
3. If a cold successor read only this lesson, could they reproduce the behavior without asking anyone anything?

## WHERE IT'S ENFORCED
- **Smart Note Operating Contract V1 (CANONICAL):** schema-v2 conformance ratchet (v1 captures refused as new); CANDIDATE ceiling on all new intelligence; no competing hand-written copies — projections generate from canonical truth.
- **0001-LEARNING-CONTRACT-V1.md:** OBSERVE → RECONCILE → CANDIDATE → VERIFY → ADOPT → MEASURE → COMPOUND. Stored information is not learned information.
- **lessons.jsonl:** `adopted_utc` stays null until a later decision measurably changed because of the lesson; the 5-oldest sweep verifies every PENDING lesson — adopted, failed, or flagged, nothing sits in limbo.
- **Rhythm:** hourly distillation (learning + intelligent events announced on the venue); the director's weekly review marks `adopted_utc`.
- **Honest status:** `BRAIN/07-LEARNING` is PROPOSED CANONICAL — human director ratification required. Nothing here claims ratification it doesn't have.
