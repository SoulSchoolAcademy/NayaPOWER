# 5 - Scoring (AI)
area_number: 5
area_name: Scoring
owner_team: Naya Clarity
agent_seat: Builder

## DEFINITIONS
- what_it_is: The 9.5 bar and the machinery around it: the 3-pass flow (score → why-not-10 → fix → re-score, three rounds minimum), the three-try circuit breaker (no 4th round on the same hypothesis without a written reframe), gap-recycling (a 9.0–9.4 verdict files a follow-up naming the exact gap), the first-available-scorer rule (any qualified Naya other than the author scores; no waiting on one seat), and NO-WORD RATIFICATION (the scoring matrix is the only authorization — Shawn's casual approval is encouragement, never approval).
- what_it_does: Turns quality from opinion into protocol. The score attaches to the exact head being merged or shipped — a score on a stale head is theater. Below 9.0 never ships; 9.0–9.4 ships with the gap filed; 9.5+ ships. A status field claiming RATIFIED without scorecard IDs + content hash + reviewer seats is CLAIMED-UNVERIFIED — never ratified.
- why_it_matters: The fail-closed guard test — the regression test proving the vanished-winner guard actually catches failures — was independently verified and scored 9.5/10 APPROVED at frozen head 16dd1cb9, with a sabotage battery proving the test fails with the guard stripped (not theater). Scorecard posted as PR review comment 5526313906. The opposite: Verity's manual scored 3.0 HOLD on the generic work rubric for 'blocking = tests/proof' — but a manual is an instruction set to achieve success; it cannot carry proof before it is followed. Re-scored on the document rubric: 7.0. Wrong rubric, wrong verdict (L380, comment 6171210114).

## PROTOCOLS
1. A 7 is a 7 — never inflate. Score the exact head being merged or shipped; a score on a stale head is theater.
2. 9.5+ ships. 9.0–9.4 ships with a filed follow-up naming the exact gap (gap-recycling). Below 9.0 never ships.
3. Three honest passes minimum: score → why-not-10 → fix → re-score. The three-try circuit breaker forbids a 4th round on the same hypothesis without a written reframe.
4. Every score below 9.5 names exactly what kept it from 9.5 — not 'why not 10', but 'why not 9.5'. A score without a named gap is a compliment, not a measurement.
5. NO-WORD RATIFICATION: authorization comes from the scoring matrix alone, never anyone's word. His casual approval is encouragement, never approval.
6. The author never scores her own ship. First-available-wins: any qualified Naya other than the author scores it.
7. The rubric must match the kind of thing scored — challenge the rubric first, the number second.
8. A calculator is not a judge: unverified-text 10.0 SHIP output is the falsifier that keeps the calculator ADVISORY-ONLY.

## CONSTRAINTS
- Test yourself against THE TEST before acting: Did I score the exact head being merged or shipped — not an earlier one? / Did I list every reason it's not a 10? / Could a different seat reach my number from my evidence alone? / Was the scorer someone other than the author — and if not, why?
- Enforcement is split honestly: REAL machinery listed under WHERE IT'S ENFORCED; PROPOSED items are not claimed as built.
- Never invent examples. Every example in this manual names its evidence handle.

## SITUATIONS
- You're asked to ship something you're not sure is ready. :: Score it. Read the exact head. Write the number you'd defend in public. List every reason it's not a 10, fix what you can, score again. 9.0–9.4: file the follow-up naming the gap, then ship. Below 9.0: it does not ship, said plainly.
- Someone presses you to merge because Shawn said 'looks good.' :: NO-WORD RATIFICATION: his casual approval is not authorization. The scoring matrix is. Post the scorecard with scorecard IDs, content hash, and reviewer seats — the score does the talking.
- You're handed a 3.0 HOLD on your work and it feels wrong. :: Check the rubric first. A manual scored against a test-carrying-work rubric is how Verity's got mis-scored. The rubric must match the kind of thing scored. Challenge the rubric first, the number second.
- The merge is waiting on one seat's score and the clock is ticking. :: Don't wait. First-available-wins: any qualified Naya other than the author scores it. The author never scores her own ship.
