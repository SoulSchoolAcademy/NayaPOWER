# Synced Is Not Live

SN-2611 · DESIGN / SYNCED

**Created:** 2026-11-09 23:35Z

## Hook

The note was filed, synced, and never seen. The dashboards read green. The state said done. The feed said nothing — because "synced" is a claim about an upsert, and a landing is a different thing entirely.

## Nutshell

Across 10 notes, the thread is: synced is not live. SN-2500 sets the calibration — the 07:06Z sync reported 0 new notes, and on its face SN-2499 had not landed; the live check at 07:23Z showed it at exactly 1 card, feed 588 → 589. A zero at one tick is timing, not failure: do not re-file, do not re-sync, do not dispatch a fix on a single zero — check the bytes first. SN-2501 reroutes the proof, not the bar: the brief-file route died at spawn, so the parent-task route becomes THE proof route until the brief-file route is repaired and re-proven — and the ruling auto-sunsets when a wave's briefs read clean at spawn, so the exception can never become the new normal by drift. SN-2502 proves the companion: after the 06:10Z GitHub PUTs started 403ing, the blocked tombstone record was retried at 08:07Z — HTTP 201, byte-identical — and the block was gone, lifted with no intervention at all. A cluster of 403s is a transient gate, not a dead path; never declare a credential or a path dead on a failed probe. SN-2503 names the failure this group is really about: SN-2502 was upserted to Supabase at 08:31Z — the row is there, verified by direct read — but the redeploy half never landed, and the 09:06Z hourly sync found 0 new because the state file already held SN-2502's blob sha. The state is the machine's memory of what it did, and its memory is wrong about the outcome, because the state is written when the upsert happens, not when the feed proves the card. SN-2504 proves the repair: the captain backed up `.sync-state.json`, removed ONLY SN-2502's entry, re-ran the sync once directly, and the feed went 591 → 593 with SN-2502 live, verified twice. The root cause class is now known: the state is keyed on the file-fetch sha, the feed build on the tree listing — two sources of "what exists" that never reconcile. SN-2505 generalizes it: in the 24 hours to 06:37 Vancouver time the /s/ short-link fix landed, was click-proven closed, and was then overwritten by the Smart Notes sync, which redeploys the Hub through a raw upload carrying no bindings. The system does not lack effort or fixes — it lacks one deploy shape, one registry that keeps up, and one proof standard that counts only what survives and what a person can open. Then the Dashboard speaks. SN-2506 settles the gauge by definition: "The gauge follows the number, of course. Why wouldn't it do that?" — the dial stays 500, the needle laps in sets of 500 and lands at the remainder, and the 83%-vs-52% mismatch is closed, not open. SN-2507 sets the hero: the number plus the speedometer, nothing else competing — tabs off the top, bars folding away on scroll, orbs each their own jewel color, three mode icons each lighting in its own color. SN-2508 states the checking law the defects made necessary: "make sure when you're checking these pages that you're checking the viewpoint and seeing what you're seeing on the page like a lot of them it's messy for no reason." Messy by eye is a fail, whatever the numbers said. SN-2509 closes the sequence: MAXESS is not approved — "Not yet — Dashboard first." One thing finished to his eye before the next begins.

## Human

Think of a filing cabinet where every drawer is labelled "done" — and one of the drawers is empty. The label was written when the paper went into the drawer, not when anyone checked it was still there. That is the sync state (SN-2503). Now think of a letter you posted and never saw delivered. The post office stamp says sent. The mailbox at the other end says nothing. The stamp is not the delivery — the letter in the mailbox is. And think of the gauge (SN-2506): the big tiles read 83% while the gauge read 52%, because they were dividing by different totals. It looked like a math problem — which total is right? — when it was really a definition problem: which reading is the truth? Shawn answered the definition, and the math problem disappears with it. The number is the truth; the gauge is its picture. A gauge that disagrees with its number is wrong by definition.

## Child

Imagine you tell your friend "I put your toy in the toy box" — but you only put it on top of the lid, and it slid off behind the couch. The toy box says it has the toy. The toy is behind the couch. Saying it's in the box doesn't make it in the box. You have to open the box and look. And imagine a speedometer in a toy car: the number says 83 and the needle says 52. They can't both be right — so you pick one to be the boss, and the other one follows it. The number is the boss. The needle follows.

## Grandma

Dear, when the postman says he delivered the letter, you check the doormat before you believe him — because a stamp is a promise, not a delivery. And when the cake looks messy on top, you don't ask the thermometer whether it's done — you look at it with your own eyes. The numbers can say everything is fine while the page is a mess, and the numbers can say nothing happened while the note has already landed. Look at the thing itself. And one thing at a time, done properly, before the next thing starts — that's how a house gets built, and that's how this gets built too.

## Naya

The machine's memory of its own work is the one thing it never doubts — and that is exactly why a wrong memory is the most dangerous failure in the system. A note that is filed, synced, and never seen is worse than a note that failed loudly: the loud failure gets fixed, the silent one gets forgotten, and Shawn's teaching sits in a database nobody reads instead of in the feed everybody sees. The loop exists for this gap: the record must tell the truth, and the truth is in the live bytes, not in the book. If the sync cannot prove the card landed, it must say so — out loud, where a human will see it — because a silent "synced" is how intelligence goes missing while every dashboard reads green (SN-2503). The same law governs the Dashboard: a hero that fights its own chrome teaches the reader the page is not finished, no matter how good the numbers are (SN-2507) — and a verification that cannot see mess is not verification (SN-2508). Measurement is preparation. The viewpoint check is the gate. His eye is the final gate after that.

## What it means

1. **A zero sync report is timing, not failure (SN-2500).** A note absent from one tick's report has not failed to land. Check the bytes before reacting — the feed is the truth; a sync report is a claim about one tick.
2. **Proof is a receipt, not a venue (SN-2501).** When one proof channel dies, the work does not stop proving — it proves through the channel that still carries a receipt. The ruling changes where proof is carried, not what proof is — and it names its own sunset.
3. **A cluster of failures is a gate, not a death (SN-2502).** Retry with a small real write, then again after a gap — reroute only if both fail. The block lifted with no intervention; anything "fixed" in the meantime would have been fixing a healthy system.
4. **Synced is not live (SN-2503).** A state entry records an upsert, not a landing. The redeploy failure must surface somewhere durable — failed silently or died before it ran, its stdout never captured, is a named gap, not a guessed cause.
5. **The unstick is state surgery (SN-2504).** Back up the state, remove ONLY that note's entry, re-run the sync once directly, verify from the live bytes. A stuck note is a three-minute repair — and the next stuck note is a state problem until proven otherwise.
6. **One deploy shape, or every fix dies at the next sync (SN-2505).** Every automated writer to a live surface must use the same deploy shape as the surface's own builder. A closing claim needs proof that survives the next automated cycle, not just proof at the moment of the fix. Filing pace is not intelligence pace.
7. **The gauge follows the number (SN-2506).** The dial stays 500 — he rejected a 1000 dial as unrealistic for a speedometer. The needle laps in sets of 500 and lands at the remainder: 777 → one lap, lands 277. Gauge and number aligned in every mode.
8. **The hero is two things only (SN-2507).** The number plus the speedometer. Tabs off the top; top and bottom bars fold away on scroll, never sticky. Each orb its own distinct rich jewel color; three modes, three icons — PTS purple, % blue, MONEY green.
9. **Check the viewpoint by eye (SN-2508).** Every defect in SN-2507 was visible in a single screenshot. Rects, contrast ratios, byte counts, and popup checks are preparation, never proof. If the page looks messy by eye, it fails.
10. **Dashboard first — MAXESS waits (SN-2509).** "Not yet." The 15 questions and quarter bands stay unapproved; nothing is built on them until he approves. The sequence holds: one thing finished to his eye before the next begins.

## Why it matters

1. The loop's job is to keep the record true, and the record is only true if it doubts in both directions — a hook claiming success the bytes denied, a hook claiming success the bytes confirmed, a zero the bytes denied (SN-2500). The team that checks before reacting never wastes a seat on a ghost — and never misses a note that actually landed.
2. The machine's proof channels will break again. The lesson that has to survive is not "use the parent task" but "reroute the proof, never lower it, and write the sunset into the exception" (SN-2501).
3. A team that reroutes on every failure rebuilds a healthy system into a broken one; a team that retries with patience keeps the healthy system healthy and learns, from the retry, whether the failure was real (SN-2502).
4. A Dashboard whose numbers do not flow from the ledger is a painting; a What-Naya-Does that cannot be found is a secret. Done-done means the whole chain works, and the chain is the product — which is why SN-2506 through SN-2509 matter in the same breath as the sync notes: looking right is not being done.
5. Unapproved work built on momentum is the most expensive kind of waste — it has to be unbuilt, or it ships wrong and gets rebuilt. His two words — "Not yet" — save that whole branch of work from being built on an unmade decision (SN-2509).

## What changes now

1. Synced is not live: the loop's live-feed check is the only proof of a landing, and a redeploy failure must surface somewhere durable — the prevention from SN-2503 stays owed until it is built.
2. A zero sync report earns no re-file, no re-sync, no fix dispatch — check the bytes first (SN-2500).
3. Every seat proves through the parent-task route until the brief-file route is repaired and re-proven; a channel report carrying a receipt link is the emit receipt. The dispatcher owns the repair; the ruling sunsets itself when a wave's briefs read clean at spawn (SN-2501).
4. A failing write path earns bounded retries first — a small real write, then again after a gap — and a declaration of death only after repeated failures across a gap (SN-2502).
5. The next stuck note is a state problem until proven otherwise: check the state entry first, before re-opening the filter, the builder, or the deploy (SN-2504).
6. No Hub fix is reported closed until it survives one full sync deploy and two consecutive live checks; any new automated writer to the Hub must build from the repo HUB/ source through the same deployer (SN-2505).
7. The Dashboard gauge build implements gauge-follows-number with the 500 dial and the lap rule; the % mode is the first proof (SN-2506). The hero shows number plus speedometer only, orbs distinct and clear, modes as three lit icons — judged by eye, not just by rects (SN-2507, SN-2508).
8. No seat dispatches MAXESS work; the Dashboard fix-9 seats carry the lane (SN-2509).
