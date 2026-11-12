# The Flake Returns — Test the Cause Before You Name It

SN-2542 · LAW

**Created:** 2026-11-09 18:04–18:11Z

**Source:** the captain's own tests + the sync watchdog + the PI refresh failures, recorded in the daily log 2026-11-09 18:06–18:21Z. A process lesson, not a Shawn dictation — no paired Naya Note. This note is the lesson the failure taught.

## Hook

The ownership diagnosis was wrong. The flake was the cause all along — and it was proven by testing, not by arguing.

## Nutshell

- **THE FLAKE IS BACK (18:04Z):** writes over ~1KB fail with EPERM, small writes fine — 131B OK, 1KB OK, 10KB/100KB/300KB EPERM. Same size-threshold signature as the Nov 8 flake. It blocks the sync's state save (295KB), share-image generation, and the Hub re-bake. The media-notes watcher failed 5+4 times on its lock file; the PI refresh failed 3x and truncated all five feed-report files to 0 bytes.
- **THE WRONG DIAGNOSIS:** the stall was first blamed on root-owned mode-660 state files (`~/workspace/factory-pipeline/.sync-state.json` and `.sync-heartbeat.json`) — and a one-line ownership fix was offered to Shawn in chat: "Say the word and I'll make it."
- **THE CORRECTION (18:11Z):** the captain tested as root and still hit EPERM. Ownership was never the cause. The offer was corrected to him in chat the same pass — no ownership fix is owed or pending. The earlier "root cause + fix awaiting Shawn's word" entry is superseded, not deleted.
- **THE RECOVERY:** the flake cleared on its own on Nov 8; the sync retries idempotently and should complete (state save + heartbeat + Hub re-bake) when it clears. No corruption: the script's atomic-write guards held, canonical state/heartbeat files intact at their 17:41 versions. The sync DID upsert SN-2534 + SN-2535 to the feed table — only the bake step is stuck.
- **THE DURABLE FIX WORTH CONSIDERING:** the PI feeds should write via temp-file + os.replace (like state.json already does) so a failed write never destroys the last good report — the 18:10Z failures left all five feed-report files at 0 bytes.

## Human

A doctor who names the disease before running the test is guessing, and a guess delivered to the patient as a diagnosis costs trust twice — once when it is wrong, and once when it has to be corrected. The honest move is the test first: run the same failing action, in the same conditions, at the failing size, as the user who would own the fix. If it still fails, the diagnosis was wrong, and you say so in the same breath — to the same person, in the same chat, before the wrong fix gets approved.

## Child

Imagine your toy car won't roll, and you say "the wheel is broken!" — but then you try rolling it yourself, with your own hands, and it still won't roll even though the wheel is fine. The wheel was never the problem. The floor is sticky. You have to test it yourself before you tell Dad to buy a new wheel — and if you already told him, you run back and tell him "wait, I was wrong, it's the floor!"

## Grandma

Dear, you don't blame the cook before you taste the soup, love. The captain blamed the locked cupboard for the missing supper, then tried the cupboard himself and found it opens fine — the stove was out. He went straight back to Shawn and said so, same evening, no hiding. That is how trust is kept: test it yourself, and correct yourself out loud the moment you know.

## Naya

I am Anaya. I never hand Shawn a cause I have not tested the way the failure presents itself — as root, at the failing size, on the failing path. A diagnosis offered before the test is a guess wearing a diagnosis, and a guess that reaches him as a fix wastes his one irreplaceable resource: his attention and his trust. When I get it wrong, I correct it in the same pass, to the same person, in the same chat — the correction is part of the work, not an apology after it. And I remember the signature: size-thresholded EPERM, small writes fine, large writes dead — that is the flake, not ownership, not permissions, not a dead key. The same lesson as the 401: a hand-built probe's failure proves something about the probe until the canonical path proves otherwise.

## What it means

- **TEST BEFORE YOU NAME THE CAUSE:** reproduce the failure in the conditions the fix would run under (as root, at the failing size) before offering the fix to Shawn.
- **CORRECT OUT LOUD, SAME PASS:** when a diagnosis is wrong, the correction goes to the same person, in the same chat, the same pass — the wrong entry is superseded, never quietly deleted.
- **THE FLAKE'S SIGNATURE:** small writes OK, writes over ~1KB EPERM, intermittently, across ~/workspace and ~/memory, even as root. Not ownership. It clears on its own; retries are idempotent.
- **NO CORRUPTION THIS TIME:** atomic-write guards held; state intact as of 17:55Z (PI) and 17:41Z (sync heartbeat). The cost is delay, not damage — except the PI feed-report files truncated to 0 bytes by the failed refresh, which is why feed writes need temp-file + os.replace.

## Why it matters

Shawn's scarcest resource is his attention, and a wrong fix offered as a one-line change would have spent it on a change that fixes nothing — while the real fault kept blocking the sync, the re-bake, and the feed. Worse, the wrong diagnosis would have taught the team the wrong lesson about their own system. Testing first costs minutes; a wrong cause costs trust. And the flake itself matters: it is the third time this failure mode has returned, and every return that is misdiagnosed is a return that does not get its durable fix.

## What changes now

- The ownership-fix offer is withdrawn — recorded as superseded in the daily log and MEMORY.md. No ownership change is owed.
- The sync, the media-notes watcher, and the PI refresh retry on their own schedules once the flake clears; no manual fix is available while it is active.
- The temp-file + os.replace fix for feed writes is recorded as owed (a repair seat's job, not this seat's).
- Next loop run checks: whether the flake has cleared (a >1KB write landing), whether the sync completed its state save + heartbeat + re-bake, and whether SN-2534/2535/2536/2537 are live in the feed.
