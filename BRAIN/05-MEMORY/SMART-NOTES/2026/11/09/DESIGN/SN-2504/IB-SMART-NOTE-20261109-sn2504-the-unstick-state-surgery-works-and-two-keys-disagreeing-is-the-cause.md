# The Unstick — State Surgery Works, and Two Keys Disagreeing Is the Cause

SN-2504 · TEAM / VERIFICATION

**Created:** 2026-11-09 09:53Z

**Source:** the captain's repair 09:40–09:44Z (director pass record, today's daily log) + this run's independent live feed check ~09:55Z; run 35's SN-2503, which named the stuck note and the fix shape.

## Hook

The letter that never arrived got delivered — not by stamping the book again, but by erasing one line from it.

## Nutshell

- **WHAT HAPPENED — THE REPAIR (the captain's hand, 09:40–09:44Z):** run 35 flagged SN-2502 stuck (0 cards; the sync state held its blob so every sync skipped it, `synced`=0, feed never rebuilt — the state masked the stuck note). The captain verified the file on GitHub first — HTTP 200, sha 5ba6a433 (matches the state exactly), 9,085B, well-formed (9 `##` sections) — and the local built feed (591 cards) lacked it too. **The repair:** backed up `.sync-state.json` (`.bak-20261109-0940`), removed ONLY SN-2502's entry (1,468 → 1,467 files), ran `sync-smart-notes.py` once directly (exit 0, 154s): synced 2 notes (SN-2502 + SN-2503, the latter filed 09:33 and picked up normally), feed 591 → 593, Hub redeployed. **Live verification (nayanet.app/feed-live.json): 593 cards; SN-2500/2501/2502/2503 each exactly 1 card.**
- **THIS RUN'S INDEPENDENT VERIFICATION (~09:55Z):** the live feed (https://nayanet.app/feed-live.json, HTTP 200, 4,603,335B, count 593) — by parsed note-id count, **SN-2500/2501/2502/2503 each exactly 1 note**. The substring counts differ (`sn2502`: 5) — other notes citing it in their bodies; count cards, not substrings, re-proven in the same pass. SN-2050 + SN-2051 STILL NOT — zero cards each (unchanged — his call, feed-builder change needed). `generated_from` still reads `registry@03e470aa`.
- **ROOT CAUSE CLASS, NOW KNOWN:** the state is keyed on the file-fetch sha; the feed build is keyed on the tree listing — a pass where the two disagree strands the card with no re-trigger. The sync's redeploy trigger is `synced > 0`, so a note the state calls done earns no redeploy, ever. The repair works because removing the entry makes the next run see the note as new — the state was the only thing standing between the note and the feed. Two sources of "what exists" that never reconcile will strand a card silently, every time they disagree.
- **THE SYNC PATH ITSELF IS HEALTHY:** SN-2503, filed 09:33, was picked up normally by the same repair run. The fault was the state, not the sync. A future stuck note is therefore a state problem until proven otherwise — check the state entry first, before re-opening the filter, the builder, or the deploy.
- **WHAT IS STILL UNKNOWN, NAMED NOT GUESSED:** whether the 08:31Z run's `update_hub_and_deploy()` failed silently or the run died before reaching it. The repair does not answer it — the redeploy's fate stays unknown, and a silent redeploy failure can still strand the next note the same way. The prevention (the sync verifies the feed contains what it synced, or the redeploy failure surfaces somewhere durable instead of a non-fatal print into a void) is still owed — this note records a cure, not a prevention.
- **THE LESSON — THE FIX SHAPE IS PROVEN AND REUSABLE:** back up the state file, remove ONLY that note's entry, re-run the sync once directly, verify from the live bytes. A stuck note is now a three-minute repair, not a mystery — and SN-2503's fix shape is the fix that worked, named before it was tried. But it is a cure, not a prevention: the machine still cannot see its own output, and the next disagreement between the two keys will strand the next card just as silently unless the verification step lands.
- **RUN 35's OWED ITEM, CLOSED:** "SN-2502 in the feed" — landed, live-verified twice (director 09:44Z + this run ~09:55Z). SN-2503's lesson now has its proof attached: the note it named stuck is live, and the fix it named is the fix that worked.
- **ROUTINE, ALL HEALTHY:** PI refresh 09:40Z (hash 76fed0f6, 0 transitions, 10 corroborations, 67/67 lanes STALE; unresolved finding persists — the 10 corroborations do not appear as annotations in the rendered document text, a generator question for a human) · PI state publish 09:40Z ok · dispatcher wave 09:48Z (heartbeat, zero spawns, tip unmoved 8d18bbf5, drain 13) · team pulse 09:39Z quiet (0 new mail; canonical reader OK, key healthy) · media-notes 09:45Z queue empty · voice poller 09:52Z healthy (full 780s tick). **No new Shawn dictation — he is asleep; last user message 05:45Z.**
- **NUMBERING, TENTH CONFIRMATION:** `next-sn-number.py` run at run start printed highest SN-2503 / next free SN-2504 (exit 0) — this note takes its number from that output. The mechanical enforcement holds a tenth straight run.

## Human

A letter was stamped "delivered" and never arrived, and the fix was not to stamp it again — it was to cross one line out of the book so the postman would pick the letter up again. The book and the mailbox disagreed about what exists, and nobody had ever made them agree. The repair took three minutes once someone looked at both. The lesson is not the three minutes — it is that two lists that never check each other will always, eventually, disagree, and the disagreement will always look like nothing is wrong.

## Child

Imagine your big brother's notebook says your drawing was delivered, but the drawing is still in the mailbox. The fix is simple: erase that one line from his notebook, and he will pick the drawing up and deliver it for real. Then go and look at your friend's doorstep to make sure it arrived. Erasing the line is not cheating — it is telling the notebook the truth.

## Grandma

Dear, the letter got there in the end, love — all it took was crossing out the one wrong line in the book, dear, so the postman would carry it again. Two lists that never check each other will always disagree one day, love, and the only cure is to look at the doorstep yourself, dear. That's the whole of it: erase the wrong line, carry the letter, and check the doorstep, dear.

## Naya

This is SN-2503 with its proof attached. SN-2503 said the state can mask a stuck note and named the fix shape before it was tried: a manual feed build + Hub redeploy, or a state reset for that one path. The captain chose the state reset, and it worked in one pass — 154 seconds, two notes synced, feed 591 → 593. The new knowledge is the mechanism: the state is keyed on the file-fetch sha and the feed build on the tree listing, and a pass where the two disagree strands the card with no re-trigger. That is a class, not an incident — any system with two sources of "what exists" and no reconciliation read will do this again. The cure is now a procedure any seat can run. The prevention is still owed: the sync must verify the feed contains what it synced, or the redeploy failure must surface somewhere durable. Until then, the loop's live check is the only reconciliation the machine has — and this run is the proof it works: the stuck note was found, the fix was named, the fix was tried, the bytes prove it landed.

## What it means

- **SN-2502 IS LIVE** — 1 card in the live feed (593 cards), live-verified twice (director 09:44Z + this run ~09:55Z). Run 35's owed item is CLOSED.
- **THE FIX SHAPE IS PROVEN:** back up the state, remove ONLY that note's entry, re-run the sync once directly, verify from the live bytes. A stuck note is a three-minute repair.
- **THE ROOT CAUSE CLASS IS KNOWN:** state keyed on file-fetch sha vs feed build keyed on tree listing — two sources of "what exists" that never reconcile. Any future disagreement strands a card silently.
- **THE SYNC PATH IS HEALTHY:** SN-2503 was picked up normally by the same run. A future stuck note is a state problem until proven otherwise.
- **THE 08:31Z REDEPLOY'S FATE IS STILL UNKNOWN** — failed silently or died before it ran. The prevention (sync verifies the feed, or the failure surfaces durably) is still owed.
- **NUMBERING ENFORCEMENT, TENTH PROOF:** SN-2504 is exactly the next free number the helper printed.

## Why it matters

A lesson without its proof is a claim; a fix without its mechanism is luck. This note closes both: the stuck note is live, and the reason it stuck is named as a class — two keys that never reconcile. That turns a one-off repair into a procedure any seat can run and a prevention any builder can build. The danger that remains is the quiet one: the machine still trusts its own state, and the next disagreement will look exactly like nothing is wrong until someone reads the live bytes. The loop is that reading. As long as it runs, the stuck notes get found; the day it stops, they stop being found. That is why the check matters more than the fix.

## What changes now

- SN-2502's owed item is closed: landed, live-verified twice. The "synced is not live" rule now carries its proven repair: state surgery (backup, remove one entry, re-run sync once, verify from live bytes).
- The next stuck note — if one ever appears — is a state problem until proven otherwise: check the state entry first, before re-opening the filter, the builder, or the deploy.
- The prevention is still owed and stays on the list: the sync must verify the feed contains what it synced, or the redeploy failure must surface somewhere durable. A cure is not a prevention, and this note says so plainly.
- Next loop run 10:23Z re-checks the feed — SN-2504 lands only if the hourly sync (or a hook run) carries it; if the feed is still 593, the note is pending, and the record says so again.
