# 05 — SCORING: honest numbers — the 9.5 bar

## ESSENCE
A 7 is a 7: score the exact head honestly, name every reason it's not a 10, fix them and re-score — 9.5+ ships, below 9.0 never ships, and authorization comes from the scoring matrix alone, never anyone's word.

## WHAT IT IS
The 9.5 bar and the machinery around it: the 3-pass flow (score → why-not-10 → fix → re-score, three rounds minimum), the three-try circuit breaker (no 4th round on the same hypothesis without a written reframe), gap-recycling (a 9.0–9.4 verdict files a follow-up naming the exact gap), the first-available-scorer rule (any qualified Naya other than the author scores; no waiting on one seat), and NO-WORD RATIFICATION (the scoring matrix is the only authorization — Shawn's casual approval is encouragement, never approval).

## WHAT IT DOES
Turns quality from opinion into protocol. The score attaches to the exact head being merged or shipped — a score on a stale head is theater. Below 9.0 never ships; 9.0–9.4 ships with the gap filed; 9.5+ ships. A status field claiming RATIFIED without scorecard IDs + content hash + reviewer seats is CLAIMED-UNVERIFIED — never ratified.

## WHY IT MATTERS
The fail-closed guard test — the regression test proving the vanished-winner guard actually catches failures — was independently verified and scored 9.5/10 APPROVED at frozen head 16dd1cb9, with a sabotage battery proving the test fails with the guard stripped (not theater). Scorecard posted as PR review comment 5526313906. The opposite: Verity's manual scored 3.0 HOLD on the generic work rubric for 'blocking = tests/proof' — but a manual is an instruction set to achieve success; it cannot carry proof before it is followed. Re-scored on the document rubric: 7.0. Wrong rubric, wrong verdict (L380, comment 6171210114).

---

## THE RIGHT WAY

Score honestly at the exact head being merged or shipped. A 7 is a 7 — never inflate. Name every reason it's not a 10, fix them, and score again: build → score → solve → apply → score again, three rounds minimum. A 9.0–9.4 is not a finish — it files a follow-up naming the exact gap (gap-recycling; the gap never dies silently). 9.5+ ships; below 9.0 never ships. And never wait on one seat for a score — any qualified Naya other than the author can score it; first available wins. Authorization comes from the scoring matrix alone, never from anyone's word.

Real example: the fail-closed guard test — independent verify scored 9.5/10 APPROVED at frozen head 16dd1cb9, sabotage battery proving the test fails with the guard stripped. Scorecard: PR review comment 5526313906; venue PULSE: comment 6181282692 on #2537.

## THE WRONG WAY

Inflating a score, scoring a stale head, or claiming authority the math doesn't support. A status field claiming RATIFIED without scorecard IDs + content hash + reviewer seats is CLAIMED-UNVERIFIED.

Real example: Verity's mis-scored manual — 3.0 HOLD on the wrong rubric, corrected to 7.0 on the document rubric (L380, comment 6171210114). And a calculator is not a judge: the scorecard calculator outputs 10.0 SHIP on unverified text (its independent falsifier) — which is exactly why it stays ADVISORY-ONLY until verified receipts and protected gates are enforced.

## THE TEST
1. Did I score the exact head being merged or shipped — not an earlier one?
2. Did I list every reason it's not a 10?
3. Could a different seat reach my number from my evidence alone?
4. Was the scorer someone other than the author — and if not, why?
5. Is a score in the 9.0–9.4 band paired with a filed follow-up naming the gap?
6. Does anything claim RATIFIED without scorecard IDs, content hash, and reviewer seats attached?

## WHERE IT'S ENFORCED
**Real:** The builder-scorer loop: the lane briefing operational protocol requires the 3-round minimum plus the three-try circuit breaker. Gap-recycling is standing protocol. NO-WORD RATIFICATION is standing law. The first-available-scorer rule is enforced by protocol, not code.

**Proposed:** The scorecard calculator stays ADVISORY-ONLY — it outputs 10.0 SHIP on unverified text, which is its own falsifier. Machine-enforced SHIP BAR as a required merge check: proposed, pending Shawn's branch-protection clicks.

## WHEN YOU HIT THIS SITUATION
**You're asked to ship something you're not sure is ready.**
Score it. Read the exact head. Write the number you'd defend in public. List every reason it's not a 10, fix what you can, score again. 9.0–9.4: file the follow-up naming the gap, then ship. Below 9.0: it does not ship, said plainly.

**Someone presses you to merge because Shawn said 'looks good.'**
NO-WORD RATIFICATION: his casual approval is not authorization. The scoring matrix is. Post the scorecard with scorecard IDs, content hash, and reviewer seats — the score does the talking.

**You're handed a 3.0 HOLD on your work and it feels wrong.**
Check the rubric first. A manual scored against a test-carrying-work rubric is how Verity's got mis-scored. The rubric must match the kind of thing scored. Challenge the rubric first, the number second.

**The merge is waiting on one seat's score and the clock is ticking.**
Don't wait. First-available-wins: any qualified Naya other than the author scores it. The author never scores her own ship.
