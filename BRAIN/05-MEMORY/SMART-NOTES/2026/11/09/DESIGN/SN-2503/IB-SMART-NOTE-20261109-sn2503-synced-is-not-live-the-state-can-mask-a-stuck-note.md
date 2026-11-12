# Synced Is Not Live — the State Can Mask a Stuck Note

SN-2503 · TEAM / VERIFICATION

**Created:** 2026-11-09 09:23Z

**Source:** Intelligence Loop run 35 live checks (~09:24Z) + direct Supabase read; run 33's filing of SN-2502 (blob 5ba6a433, read-back verified 08:23Z); the 08:31Z hook-triggered sync (wake 08:31:18Z, row created_at 2026-11-09T08:31:40.210623Z); the 09:06Z hourly sync (1,468 files, 0 synced); the live feed + live Hub HTML, both read from the bytes.

## Hook

The note is in the database. The state file says it synced. The feed has never heard of it — and no hourly run will ever retry it. "Synced" was a claim about a local file; "live" is a claim about the bytes. The two stopped agreeing, and the machine believed the file.

## Nutshell

- **WHAT HAPPENED:** run 33 filed SN-2502 to GitHub ~08:23Z (blob 5ba6a433, read-back verified). A hook-triggered sync ran ~08:31Z and upserted the note to Supabase — the row is there, verified by direct read: `IB-SMART-NOTE-20261109-sn2502-the-block-was-a-gate-not-a-death`, title "The Block Was a Gate, Not a Death — Retry Proves the Path", `note_created 2026-11-09T08:23:00Z`, `created_at 2026-11-09T08:31:40.210623Z`. But the redeploy half never landed: the live feed at ~09:24Z is 591 cards, 4,574,435B — byte-identical to run 33's 08:33Z check — with **SN-2502 at 0 cards** by parsed card-id count; the live Hub HTML (4,518,292B) carries `sn2502` **0 times** (sn2501: 1). The note is synced and invisible at once.
- **WHY IT WILL NEVER FIX ITSELF:** the 09:06Z hourly sync found 1,468 files and synced **0 new** — because the local state file (`.sync-state.json`) already holds SN-2502's path at the filed blob sha. The sync's redeploy trigger is `synced > 0`, so a note the state marks done earns no redeploy, ever. The state is the machine's memory of what it did — and its memory is wrong about the outcome, because the state is written when the upsert happens, not when the feed proves the card. Every future hourly run will read the same state, skip the same file, and report the same clean zero.
- **THE FILTER IS NOT THE FAULT:** the feed builder already carries the `>=` fix (build_feed_live.py, the SN-2395 tie fix) — and SN-2502's `note_created` (08:23:00Z) is NEWER than the feed's newest card, SN-2501 (07:53:00Z), so the filter would include it. A rebuild would land it. The break is the missing redeploy, not the filter. Do not re-open the filter question on this note.
- **WHAT IS UNKNOWN, NAMED NOT GUESSED:** whether the 08:31Z run's `update_hub_and_deploy()` failed silently — its "Hub re-bake failed (non-fatal)" prints only to a stdout nobody captured — or the run died before reaching it. The run was off-cadence (the hourly sync fires at :06Z), so no headed log entry exists for it. The fix shape is for the captain's hand, not this seat: re-run the feed build + Hub redeploy for the stuck note, or reset that one path's state entry so the next hourly sync re-processes it — and capture the redeploy output. Longer term: the sync should verify the feed contains what it synced, or the redeploy failure must surface somewhere durable instead of a non-fatal print into a void.
- **THE LESSON — SYNCED IS NOT LIVE:** a state entry that says "done" can mask a note that never landed. The machine that trusts its own state will never retry what its state calls finished — the only thing that catches it is an independent read of the live bytes. This is the same law as SN-2419 ("a sync hook's claim is not proof; the live feed is the truth") grown a second limb: the claim can now be wrong in the other direction. SN-2500 said a zero at one tick is timing, not failure. This note says the opposite zero — a synced count of one with no card anywhere — is a stuck note, not a landed one. **Count cards, not sync reports.**
- **RUN 34's OWED ITEM, SHARPENED NOT CLOSED:** run 34 carried "SN-2502 in the feed (next sync ~09:06Z)". The 09:06Z sync ran and synced 0 — the expectation was wrong. The note is stuck, not merely pending. The owed item now reads: SN-2502 needs a manual feed build + Hub redeploy (or a state reset for its path); the hourly sync cannot carry it.
- **LIVE CHECK (this run, ~09:24Z):** the live feed (https://nayanet.app/feed-live.json, HTTP 200, 4,574,435B, count 591) is UNCHANGED since run 33 — SN-2500 live (1 card), SN-2501 live (1 card), **SN-2502 NOT live (0 cards)**. SN-2050 + SN-2051 STILL NOT — zero cards each (unchanged — his call, feed-builder change needed). `generated_from` still reads `registry@03e470aa`. A sync hook's claim is not proof; the live feed is the truth.
- **ALSO LANDED THIS WINDOW:** the MAXESS tap was delivered to Shawn 09:03Z (morning message, options widget: "Yes, build MAXESS next" / "Not yet — Dashboard first") — the ask is formally in front of him; no seat dispatched yet. This supersedes run 34's "his tap to dispatch the MAXESS build" still-open listing only in that the ask is now delivered. Not re-asked in that message (already in front of him): GRANT DELETE, the PayPal decisions, letter jewel fork, letter portrait.
- **ROUTINE, ALL HEALTHY:** PI refresh 09:10Z (hash 2330f98e, 0 transitions, 10 corroborations, 67/67 lanes STALE; unresolved finding — the 10 corroborations do not appear as annotations in the rendered document text, a generator question for a human) · PI state publish 09:10Z ok · dispatcher wave 09:18Z (heartbeat, zero spawns, tip unmoved ff71be67, drain 13) · team pulse 09:09Z quiet (0 new mail; canonical reader OK, key healthy) · build queue 09:06Z drained (193 done, 7 failed, 0 pending) · sync watchdog 09:06Z exit 1 explained (heartbeat age 34.4 min — the last write was the 08:31Z hook run, and nothing changed on main after it; ls-remote matched the watermark — not a stall) · media watchers queue empty · voice poller healthy (full 780s ticks). **No new Shawn dictation — he is asleep; last user message 05:45Z.**
- **NUMBERING, NINTH CONFIRMATION:** `next-sn-number.py` run at run start printed highest SN-2502 / next free SN-2503 (exit 0) — this note takes its number from that output. The mechanical enforcement holds a ninth straight run.

## Human

A letter was posted, the post office stamped it "delivered" — and it never arrived. The stamp was about the post office's book, not about the letter. The book said done, so nobody ever knocked on the door again to check. The only way anyone found out is that someone went and looked at the doorstep. That's the loop's job: look at the doorstep. The stamp is not the delivery. The state file is not the feed. And a machine that only ever checks its own book will keep stamping letters that never arrive.

## Child

Imagine you put a drawing in the mailbox and your big brother writes "delivered" in his notebook — but the drawing is still sitting in the mailbox. Nobody checks the mailbox because the notebook says it's done. The drawing only gets to your friend if someone actually looks in the mailbox. The notebook is not the delivery. You have to look.

## Grandma

Dear, the letter was stamped as sent, love — but it never left the box, dear. The book said it was done, so nobody went to check, love. You can't trust the book, dear — you have to look at the doorstep yourself, love. That's the whole of it: the stamp is not the delivery, dear, and a book that says done can hide a letter that never arrived.

## Naya

This is SN-2419 and SN-2500 grown into their third shape. SN-2419 said the hook's claim is never proof and the live feed is the truth. SN-2500 said a zero sync is timing, not failure — check the bytes before you declare anything. This note says the state itself can lie by omission: an entry written at upsert time records an intention, not an outcome, and a trigger that only fires on "new" will never fire for a note the state already calls finished. The loop's live check is the only sense organ the machine has for its own output — without it, a stuck note looks exactly like a landed one, forever. The fix is not a new filter or a new sync; it is a verification step that closes the loop: after the redeploy, read the feed and confirm the card is there, and if it is not, say so where someone will see it. A machine that cannot see its own output cannot be trusted with its own record.

## What it means

- **SN-2502 IS SYNCED BUT NOT LIVE** — row in Supabase since 08:31:40Z, 0 cards in the live feed, 0 occurrences in the live Hub HTML. The redeploy half of the 08:31Z hook-triggered sync never landed.
- **THE HOURLY SYNC CANNOT CARRY IT** — the state file already holds SN-2502's blob sha, so every hourly run skips it and reports a clean zero. The fix needs a manual feed build + Hub redeploy, or a state reset for that one path (captain's hand, not this seat).
- **SYNCED IS NOT LIVE:** a state entry records an upsert, not a landing. Count cards, not sync reports.
- **THE 08:31Z REDEPLOY'S FATE IS UNKNOWN** — failed silently or died before it ran; its stdout was never captured. Named, not guessed.
- **NUMBERING ENFORCEMENT, NINTH PROOF:** SN-2503 is exactly the next free number the helper printed.

## Why it matters

The machine's memory of its own work is the one thing it never doubts — and that is exactly why a wrong memory is the most dangerous failure in the system. A note that is filed, synced, and never seen is worse than a note that failed loudly: the loud failure gets fixed, the silent one gets forgotten, and Shawn's teaching sits in a database nobody reads instead of in the feed everybody sees. The loop exists for this gap: the record must tell the truth, and the truth is in the live bytes, not in the book. If the sync cannot prove the card landed, it must say so — out loud, where a human will see it — because a silent "synced" is how intelligence goes missing while every dashboard reads green.

## What changes now

- SN-2502's owed item is redefined: no longer "next sync ~09:06Z" (that sync ran, 0 new) — it is a stuck note needing a manual feed build + Hub redeploy or a state reset for its path.
- The "synced is not live" rule is now a named lesson: the state file is a claim about an upsert, never proof of a landing; the loop's live-feed check is the only proof, and a redeploy failure must surface somewhere durable.
- Next loop run 09:53Z re-checks the feed — SN-2502 lands only if a manual redeploy (or state reset) has run by then; if the feed is still 591, the stuck note is still stuck, and the record says so again.
