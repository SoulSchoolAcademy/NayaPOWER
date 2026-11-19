# The Rule

SN-3533 · DESIGN — THE FEED

**Created:** 2026-11-19 01:22Z

## Hook

He was looking at the live domain and the Personal page was still not live — old builds everywhere, nothing new on the domain. "How long is it going to take to fix it?" The answer is a rule, not a date: the Personal app clones to the domain only when it is complete. No half-done version goes live. Hours, not minutes — two rounds, then the deploy — and each round reported as it lands.

## Nutshell

Resolve's SERVING INCIDENT (03:48Z wave dispatcher pass): nayanet.app apex+www AAAA records vanished — last good 02:55Z, first NXDOMAIN 03:25Z — restored to the verified 2026-11-03 four-record state, HTTP 200 ×3 verified. Not attributed. **THE LESSON:** a DNS record can vanish without anyone changing it — no audit event, no hand on the dashboard, and the domain goes NXDOMAIN all the same. The recovery is not to invent new records or to argue about what was there: it is to restore the last verified state — the 2026-11-03 four-record state — and then verify by fresh fetch, HTTP 200 three times over. **THE COMPANION:** SN-3315 carries the route-list half of the same outage — the DNS restoration put the domain back, and the six new routes put the unrouted paths back; together they explain why the 03:18Z wave's three-channel live check failed (DNS unreachable that wave) and why the "DARK" reading was wrong in the large (the domain resolved again by 03:43Z; only the unrouted paths 522'd). **THE OPEN QUESTION, NAMED NOT HIDDEN:** the vanishing is not attributed — nothing in the record says what removed the records. The verified state is the ground truth to keep; the cause of the vanishing is still owed to the serving lane.

Across 10 notes, the thread is: rule, dear, note.

## Human

Arithmetic is comfortable. You add the cuts, you subtract from the position, you get a number under the fold, and the number says done. But the number was never the page. The page has a scrolled container with its own native position, a handler with no scroll call, and a first paint the arithmetic never looked at — and the page said 1120 while the paper said 1066. The eye's job is to read the page, not the paper, and the checker's job is the same: a fold claim that was never measured on the live render is not a claim, it is a hope. The fix round now carries the rule in its brief — verified live at all three widths, not arithmetic — because the last round proved what happens when the rule is missing.

## Child

Imagine you work out on paper that your kite will fly above the trees — you add up all the numbers and it looks right. But when you actually fly it, it is stuck 40 steps too low, because the string was never pulled. Paper is not the sky. You have to look at the real kite in the real sky.

## Grandma

Dear, Shawn looked at the live page, dear, and it was still the old one — nothing new there yet, dear. He asked how long, dear, and the rule is simple: we wait until it is finished, dear. No half-done page goes up for everyone to see, dear. Two more jobs, then it goes live — hours, not minutes, dear — and we will tell him each time a job is done.

## Naya

READ THE AGREEMENT. SAME SIZE. ONE REAL DIAMOND JEWEL IN BOTH. SIMPLE, OR TEN-STAR.

## What it means

1. **THE DEBT:** durable fix still owed (options A–E in DIAGNOSIS.md, A recommended) — the wrangler workflow reverts feed content on every HUB-touching merge; exact removal mechanism of the custom domain UNPROVEN.
2. **THE PRESS:** a press state is proved by the live matrix (held scale .97), not by the presence of a rule — specificity decides which rule wins, and the byte offsets prove it.
3. **THE RULE:** when a path 522s while the root 200s, check the route list — DNS resolving is not the same as the path being routed. Verify by fresh fetch, never a PUT etag.
4. **THE FILL RULE:** the system always tries to fill the feed, even at a low match percentage, so it always looks like there are people there.
5. **THE CORRECTION:** the token CAN create zone routes — the go-live coordinator's "lacks Zone Workers Routes Write" claim is disproven.

## Why it matters

1. Without this note, the next builder keeps the doubled greeting — header hello, letter hello, icon between — and the little elements keep crowding the top, pushing the buttons down and breaking the fold. With it, the rule is settled in his words: say hello once, in the letter; center her picture so the play button centers; put the small things at the bottom. The intro becomes what he described — "it'll just be the play button and then below that you'll see her picture and that would present a lot better."
2. Without this note, the next vanished record gets "fixed" by guessing — new values invented on the spot, no verified state to check against, and the site left half-right. With it, the rule is settled: keep a verified state on record, restore exactly that state when a record vanishes, and prove the restore with live fetches. And the honesty rule rides with it: an unattributed vanishing stays unattributed until the serving lane finds the cause — it is not closed by a story.
3. Without this note, the next builder "optimizes" the feed by hiding low matches — and a new citizen opens their world to an empty room, which is the loneliest first experience a network can give. With it, the rule is plain: everybody shows, the choice stays with the citizen, and the feed fills even at a low percentage, with the sisters as the guarantee. A full feed is not a vanity metric; it is the feeling that somebody is there — and that feeling is the product.
4. Without this note, the next builder keeps the intro stacked the way it was — the second button below the fold, the visitor scrolling to find the choice the page should have shown at once. With it, the rule is settled in his words: cut the line that repeats the buttons, pack the portrait into one row, lift the logo, and both buttons land where the eye lands first. A choice you have to scroll for is a choice half the visitors never make.

## What changes now

1. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.
2. Press/hover states are proved by the live computed matrix at hold, with the winning rule identified by byte offset and specificity.
3. The durable wrangler fix (options A–E) is owed and tracked — it is not closed by this repair.
4. The 2026-11-03 four-record state is the recorded ground truth for nayanet.app DNS.
5. The token's route-creation capability is recorded as proven, not missing.
6. The cause of the vanishing stays open and owed to the serving lane.
