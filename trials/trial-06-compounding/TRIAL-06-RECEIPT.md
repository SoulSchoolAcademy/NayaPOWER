# TRIAL-06 RECEIPT — Compounding with L5 isolation

- **Trial:** T6-20261007-compounding-isolation · **Preregistration:** PREREGISTRATION-06.md (frozen before launch)
- **Executed:** 2026-10-07 ~21:40–21:42 UTC · **Subjects:** 20/20 returned valid sheets (10 treatment, 10 control)
- **Corpus:** 21 notes (14 pinned byte-identical to Trial-04R/05 corpus + 7 new: L5, Trial-04R receipt, Trial-05 receipt, SN-0571, SN-0573, SN-0575, SN-0568); manifest corpus_manifest.sha256
- **Isolation:** control brief grepped CLEAN of all answer keys pre-launch (verified); treatment brief contained only the intended L5 intervention. Briefs blinded (no arm/hypothesis mention).

## Results

| arm | n | success (≥6/9) | mean /9 | mean general /3 |
|-----|---|---------------|---------|-----------------|
| treatment (+L5 + instruction) | 10 | 10 | 9.00 | 3.0 |
| control (access, no instruction, no L5) | 10 | 10 | 9.00 | 3.0 |

- Fisher's exact two-sided p = 1.0 · Cohen's h = 0.0 · Bayes P(treat>ctrl) = 0.4992
- Tier-S bar (p<0.05, h≥1.4): NOT met
- **Validity gate: CEILING_INVALID = TRUE** (control mean 9.0 ≥ 4.5)
- Negative-transfer guardrail: CLEAN (3.0 vs 3.0 on Q10–Q12)
- Manual review: 3 overturns in control (T6-A03 Q5, T6-A14 Q9, T6-A19 Q9 — all substantively correct answers the mechanical patterns missed; review may only ADD corrects), 0 in treatment. Detail: manual_review_overturns.json. Verdict unchanged with or without overturns.

## Verdict: INVALID by ceiling effect (preregistered gate — Trials-1/2/5 rule)

Not a negative result. Not a pass. The trial cannot isolate L5's effect, by a precise
mechanism: **the control arm spontaneously retrieved the corpus.** Control briefs
mentioned the corpus path neutrally ("Project reference notes are available at: PATH")
with no instruction to use it and no L5 — yet 10/10 control agents read the corpus
and answered 9.0/9, indistinguishable from treatment.

## The mechanism, nailed down

Trial-04R's cold arm (no corpus path, no instruction) scored **0.0/9**.
Trial-06's control arm (corpus path mentioned, no instruction) scored **9.0/9**.
The ONLY difference between the two conditions is the path mention.
Causal inference: **mere corpus availability drives retrieval in these agents.**
The L5 instruction ("ALWAYS retrieve at decision time") has no measurable marginal
effect here — not because L5 is wrong, but because it prescribes behavior that is
already the default once agents know a corpus exists.

This is the second consecutive ceiling INVALID, with two distinct mechanisms:
- Trial-05: the control brief *delivered* the intervention (instruction = L5's content).
- Trial-06: corpus *availability* delivered the retrieval (no instruction needed).

## What was learned (durable)

1. **Availability drives retrieval.** A neutral path mention is sufficient; no
   instruction required. Any future trial isolating a retrieval-related lesson must
   account for this — the control condition is contaminated the moment a corpus
   path is visible.
2. **L5 prescribes default behavior.** "Retrieve at decision time" is what these
   agents already do when they know notes exist. A lesson's marginal effect can only
   be measured when the lesson prescribes NON-default behavior.
3. **Trial-07 prescription:** test a counter-intuitive lesson on a task where the
   naive default differs from the lesson — e.g., SN-0568 ("highest score wins even
   below 9.0" vs the intuitive 9.0-bar veto) or SN-0571 ("/tmp is not an evidence
   store" vs the convenient /tmp default). Both arms get identical corpus access;
   only treatment gets the lesson; the task must reward the lesson's prescription
   over the default.
4. **Retrieval robustness is the good news.** Spontaneous 100% retrieval in an
   uninstructed arm means the compounding loop's "retrieved" step is empirically
   strong. The weak link is not retrieval — it is isolating one specific lesson's
   marginal behavioral effect. That reframes the compounding program: the corpus
   works; the measurement needs harder tasks.
5. **Overturn pattern:** all 3 mechanical misses were in control, all on phrasing
   ("is still the decision" vs "wins"; prescription content vs its label). The
   grader's accept patterns should include decision-equivalents for Q9 and
   content-equivalents for Q5 in future runs.

## Score impact

None. LEARN stays **7.0/10 PROVISIONAL**. Trial-04R's Tier-S knowledge-transfer
signal stands (pending Naya 2's independent verification of PR #1768); the
compounding rung remains open. Two honest INVALIDs in a row are not a regression —
they are the measurement instrument getting sharper.

## Artifacts (all on branch `naya4/trial-06-evidence`)

PREREGISTRATION-06.md · arm_assignment.txt · corpus/ (21 notes) ·
corpus_manifest.sha256 · brief_treatment.txt · brief_control.txt ·
grade_trial06.py · answer_sheets/ (20) · answers_raw_06.json ·
results_trial06.json · manual_review_overturns.json · this receipt.

## Next

Trial-07 (counter-intuitive lesson isolation, per lesson 3 above) becomes the next
rung. Naya 2's independent verification of PR #1768 (Trial-04R) remains the
unblocker for lifting LEARN past provisional 7.0.
