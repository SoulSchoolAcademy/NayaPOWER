# The Gauge Follows the Number

SN-2506 · DESIGN / DASHBOARD

**Created:** 2026-11-09 15:35Z

**Source:** Shawn's decision in the main chat, 2026-11-09 15:24Z (seq 166802), answering the open % mismatch question put to him ~15:04Z as a two-option widget ("Gauge follows the featured number" vs "Featured % uses the 500 dial"). Recorded in ~/MEMORY.md the same pass.

## Hook

The needle does what the number says — if the number needs another lap, the needle takes it.

## Nutshell

- **HIS WORDS, VERBATIM (the decision):** "The gauge follows the number, of course. Why wouldn't it do that? Yeah, so if it needs to go around again, then it would then land at 277."
- **HIS REASONING, VERBATIM (the dial stays 500):** "we could set it to a thousand instead of 500 ... I think it 500 to match be more be more like there's no speedometers around a thousand at least 500 big be realistic so that's what I'm thinking there but yeah they should be aligned."
- **THE RULE, SETTLED:** the gauge's reading follows the featured number (the big tiles). The dial stays 500 — he rejected a 1000 dial as unrealistic for a speedometer. The needle laps the dial in sets of 500 and lands at the remainder: 777 → one lap, lands 277. Gauge and number aligned in every mode (PTS / % / MONEY).
- **WHAT IT CLOSES:** the % mismatch — the big tiles read 83% while the gauge read 52%, because they were dividing by different totals. That disagreement is now decided, not open: the gauge follows the number, and the two can never disagree again because one is defined by the other.
- **WHAT IT DOES NOT DO:** it does not change the dial, the tiles, or the modes. It changes only the relationship between them: the number is the truth, the gauge is its picture. The gauge never has its own opinion about the value.

## Human

Imagine a speedometer that argues with the number above it — the tiles say 83 and the needle says 52, and the driver has to decide which one to believe. Shawn settled it the way you'd expect: the needle follows the number, of course. If the number is bigger than the dial, the needle just goes around again and lands where it should. A thousand on the dial would look like no speedometer anyone has ever seen, so the dial stays five hundred and the needle does the laps. Two readings of one truth, never two truths.

## Child

Your score is the big number at the top. The round dial underneath is just a picture of that same number — it always points where the number says. If the number is bigger than the dial, the needle goes all the way around and comes back to where it should land, like going around a racetrack one more time. The picture never disagrees with the number, because the number is the boss.

## Grandma

Dear, the big number and the little dial finally agree, love — the dial just follows the number now, dear, going round again when it needs to and landing right where it should. No more two different answers, love. One truth, told twice.

## Naya

This is a definition, not a fix: the gauge is defined as a picture of the featured number. Before this decision the gauge and the tiles were two independent readings that happened to disagree (83% vs 52%, different totals), and the question was which one to change. His answer removes the question entirely — there is only one reading, and the gauge renders it. The 500 dial is a realism constraint from his eye (no speedometer reads to a thousand), and the lap rule is the mechanism that keeps a 500 dial honest above 500. Any future gauge that disagrees with its number is now wrong by definition, not by taste — and the test is one line: does the needle land where the number says?

## What it means

- **THE % MISMATCH IS CLOSED:** 83% tiles vs 52% gauge is settled — the gauge follows the featured number in every mode.
- **THE DIAL STAYS 500:** a 1000 dial was considered and rejected as unrealistic for a speedometer.
- **THE LAP RULE:** needle laps the dial in sets of 500 and lands at the remainder (777 → one lap, lands 277).
- **THE DEFINITION:** the number is the truth; the gauge is its picture. A gauge that disagrees with its number is wrong by definition.

## Why it matters

A dashboard that shows two different values for the same thing teaches the reader not to trust either one. The mismatch sat open all day because it looked like a math problem — which total is right? — when it was really a definition problem: which reading is the truth? Shawn answered the definition, and the math problem disappears with it. Every gauge on every page now has the same law to follow, and the next time a needle and a number disagree, the fix is known before anyone asks: make the needle follow the number.

## What changes now

- The Dashboard gauge build (fix-9, viewpoint by viewpoint) implements gauge-follows-number with the 500 dial and the lap rule; the % mode is the first proof.
- The % mismatch leaves the open list — it is a decided law now, not a question.
- The open question that produced this decision ("Gauge follows the featured number" vs "Featured % uses the 500 dial") is answered and closed.
- Next loop run re-checks: the gauge fix proof page shows needle and number aligned.
