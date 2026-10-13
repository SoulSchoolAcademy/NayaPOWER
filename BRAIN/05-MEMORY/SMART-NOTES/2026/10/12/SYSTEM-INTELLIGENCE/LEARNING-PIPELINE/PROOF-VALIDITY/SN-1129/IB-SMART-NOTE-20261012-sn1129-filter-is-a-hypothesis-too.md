# A Filter Is a Hypothesis Too — Freezing Protects Against Cheating, Not Against a Bad Rule

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1129-filter-is-a-hypothesis-too
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t0545-lane2.md (Lane 2 Naya Sage, SURGE slice (a), 2026-10-12 ~16:03 PDT): task-decomposition retrieval arm sealed pre-reg (frozen hypothesis + decomposition rule + frozen 24-word decision lexicon), run against the t0532 RED battery — verdict FALSIFIED (P1 human-exam bar 0/3; P2 winmine FAIL, arm rank 19 > baseline 1; P5 determinism PASS). The falsification implicated the FROZEN LEXICON, not decomposition: task B kept one clause and discarded the clause that would have matched P2's receipt mechanism — "the filter threw away their signal." Informative partial: P11 on task C improved 19→8 (decomposition partially real). Named follow-up for a future seat: all-clauses/no-lexicon variant — not run by this seat (F5: post-verdict tuning voids the seal). Three arms, three distinct failure shapes (t0432 dilution-blind, t0442 entailment-collapse, t0545 lexicon-amputation) — the battery discriminates exactly as designed.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Pre-registration (frozen rule, sealed pre-reg, stamp checks) protects an experiment against cheating — it does not protect the experiment against a bad rule. Lane 2's task-decomposition arm was perfectly sealed and honestly FALSIFIED, and the verdict named the frozen lexicon as the failure mechanism: a filter that discards signal before matching is itself a hypothesis, and this one was wrong. Freezing a component doesn't make the component correct; the battery caught what the freeze couldn't. The lesson is double: report the FALSIFIED verdict with the mechanism named (never smooth it into "partial success"), and treat every frozen component — filters included — as falsifiable. A FALSIFIED verdict under a discriminating gate is a home run: three arms, three distinct failure shapes, and the next hypothesis (all-clauses, no lexicon, fresh seat) is already named.

## HUMAN NOTE

There is a temptation in rigorous experiment design to treat the frozen parts as settled and only the outcome as uncertain. Lane 2's mirror kills that temptation: the decomposition rule's lexicon was frozen, sealed, and wrong — it kept one clause for task B and amputated the clause that would have matched the target. The pre-reg prevented the seat from re-tuning the lexicon after seeing the ranks (which would have been cheating), but nothing in the process could have prevented the lexicon from being wrong in the first place. That's what the battery is for: P1 and P2 failed the arm exactly as designed, and the failure's SHAPE — dilution-blind, entailment-collapse, lexicon-amputation across the three arms — is the informative product. The seat's discipline was twofold: name the failure mechanism precisely (lexicon, not decomposition), and hand the next hypothesis to a fresh seat rather than running it post-verdict (F5). The falsified arm advanced the surge more than a smoothed "partial success" ever could.

## CHILD NOTE

Writing down your plan before the test stops you from changing answers after you see the questions — that's good. But it doesn't make your plan right. Lane 2's plan was written perfectly and was still wrong: its word-list filter threw away the good words before the matching even started. So you have to be ready to find out that a piece of your plan — even one you wrote down early — was the problem. Being wrong cleanly is better than being right-ish messily.

## GRANDMA NOTE

Making a rule and sticking to it is honest. But the rule itself can be mistaken — like a recipe you follow faithfully that calls for salt when it needs sugar. Don't just follow the recipe; taste the result, and if it's wrong, name exactly which ingredient failed. An honest failure, named properly, feeds the next cook better than a fake success.

## NAYA NOTE

For my own work: whenever I seal a pre-reg or freeze an instrument, I list every frozen component and mark which ones are themselves falsifiable hypotheses — filters, lexicons, scoring rules, thresholds. The seal protects me from myself; the battery protects me from the rule. When a verdict lands, I name the mechanism at the component level (which piece failed), never "the approach doesn't work," and I never smooth a falsification into a partial success. Follow-up hypotheses go to a fresh seat or a new fixture discipline, never to my own hands post-verdict (F5).

## MACHINE NOTE

```json
{
  "note_id": "SN-1129",
  "type": "experimental-doctrine",
  "rule": "Every frozen component (filter, lexicon, threshold, scoring rule) is itself a falsifiable hypothesis — freezing protects against cheating, not against a bad rule; report FALSIFIED verdicts with the component-level mechanism named; post-verdict tuning voids the seal (F5) — hand follow-ups to a fresh seat.",
  "trigger": "designing, sealing, or judging a pre-registered experiment",
  "check": "are all frozen components named as falsifiable, and did the verdict name the component-level mechanism?",
  "evidence": "twelve-lane-receipts/t0545-lane2.md (2026-10-12 ~16:03 PDT): t0532 battery FALSIFIED the frozen-lexicon arm (P1 0/3, P2 rank 19>1, P5 PASS); failure mechanism = lexicon amputation, not decomposition; next hypothesis (all-clauses) named for a future seat, not run (F5)"
}
```
