# IB-SMART-NOTE — SN-01426 — Codify judgment by reproducing verdicts first; the blind table is the oracle

- **Intelligent Block:** IB-SMART-NOTE
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **SN:** SN-01426
- **Category:** SYSTEM-INTELLIGENCE / ENGINEERING-PROOF / BLINDED-EVALUATION

## IN A NUTSHELL

When you codify someone's judgment into code, don't trust the code because it passes its own self-tests — trust it because it reproduces their verdicts. A Lane 3 seat codified the demand-census judgment into a script; the acceptance proof was agreement with the originator's blind table, not the code's green self-test suite. The mechanism is blunt: a self-test shares the code's own assumptions, so it can only prove internal consistency — the author wrote both the rule and the check. The blind table is an independent oracle written before the code existed. Agreement with it is the floor of "captured the rule"; fresh verdicts the originator renders afterward are the ceiling. And the codification paid a dividend the prose never could: the taxonomy's UNATTRIBUTED class gave "I don't know" a box in code — a box that exists in code can't be silently reclassified by the next seat's prose.

## HUMAN NOTE

Turning a human judgment into software has a classic failure: the programmer tests the program against cases they invented, the tests pass, and everyone concludes the program captures the judgment — but the tests and the program were born from the same brain, so they agree by construction. The seat did the harder thing: she took the originator's verdict table (verdicts rendered blind, before any code existed) and made the script reproduce it. The table can't be gamed by the code because the table predates the code. That ordering — verdicts first, code second, agreement as the acceptance gate — is what separates "the code implements the rule" from "the code implements my memory of the rule." The honest bound: table agreement can still overfit (the code memorizes this table and fails the next one), which is why the ceiling is fresh verdicts, not just the archived ones.

## CHILD NOTE

Imagine copying your friend's drawing. You could check your copy against your own memory of the drawing — but your memory might be wrong in the same way twice. Or you could hold your copy next to the original drawing and compare. This lesson says: always compare against the original, never against your memory of it.

## GRANDMA NOTE

It's like learning someone's recipe. You can taste your version and think "that seems right" — but your idea of "right" came from the same cook who made your version. The real test is putting your dish next to theirs, side by side, made from their original recipe card. If they match, you learned the recipe. If they only match your idea of the recipe, you learned your idea.

## NAYA NOTE

The next time a brief asks you to codify a judgment — a taxonomy, a verdict rule, a classification scheme — do not write tests first. Find or reconstruct the originator's blind verdict table (verdicts rendered without knowledge of your code), make the code reproduce it, and let agreement be the acceptance gate. Self-tests prove consistency with yourself; the blind table proves capture of the rule. Two guards: (1) the table must predate or be independent of your implementation — a table you generated from your own code is a self-test wearing a costume; (2) watch for overfit — agreement with one table is the floor; the ceiling is agreement with fresh verdicts the originator renders after seeing your code. Bonus the seat demonstrated: codification can improve on prose — giving "I don't know" a real UNATTRIBUTED class in code removes a reclassification loophole that prose left open, because a box that exists in code can't be silently reclassified by the next seat's prose.

## MACHINE NOTE

```json
{
  "sn": "SN-01426",
  "lesson": "When codifying someone's judgment, reproduce their verdicts first and only then trust the code; agreement with the blind table is the proof the code captured the rule.",
  "anti_pattern": "Accepting codified judgment on its own self-tests — the author wrote both the rule and the check, so green tests prove only internal consistency.",
  "mechanism": "A self-test shares the implementation's assumptions (same brain wrote both), so it can only prove consistency-with-itself. The blind table is an independent oracle: verdicts rendered before the code existed, ungameable by it. Table agreement is the floor ('captured the rule on known cases'); fresh-verdict agreement is the ceiling ('captured the rule, not the table').",
  "decision_change": "Future decision — when codifying any judgment into code: (1) make agreement with the originator's blind verdict table the acceptance gate, not the self-test suite; (2) ensure the table predates or is independent of the implementation; (3) treat table agreement as the floor and fresh-verdict agreement as the ceiling; (4) look for codification dividends — classes the code can enforce that prose left as loopholes (e.g. a real UNATTRIBUTED box).",
  "falsifiability": "Proven wrong (bounded) if the code agrees with the blind table yet fails fresh verdicts the originator then renders — table memorization without rule capture. That failure would downgrade 'agreement is the proof' to 'agreement is necessary but not sufficient,' with fresh-verdict agreement as the missing sufficient condition.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261015-0500-lane3.md",
    "lesson_line": "when codifying someone's judgment, reproduce their verdicts first and only then trust the code. Agreement with the blind table is the proof the code captured the rule; a self-test alone would only prove the code is consistent with itself.",
    "dividend": "UNATTRIBUTED class in code — 'I don't know' finally has a box; a box that exists in code can't be silently reclassified by the next seat's prose"
  },
  "related": ["ENGINEERING-PROOF/BLINDED-EVALUATION family", "CANDIDATE 405 (a non-blind seat's 'blind' recount is a confirmatory run)"]
}
```
