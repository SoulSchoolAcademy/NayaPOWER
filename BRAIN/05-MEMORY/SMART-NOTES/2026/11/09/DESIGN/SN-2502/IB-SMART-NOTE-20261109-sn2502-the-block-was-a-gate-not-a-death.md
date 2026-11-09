# The Block Was a Gate, Not a Death — Retry Proves the Path

SN-2502 · TEAM / VERIFICATION

**Created:** 2026-11-09 08:23Z

**Source:** 08:07Z tombstone-record filing (logged in the daily log; carried in the morning message to Shawn ~08:07Z); GitHub write block that began after the 06:10Z v72 filing (PUTs 403ing, run 28 carried context); Intelligence Loop runs 29–32 PUTs succeeded through the window; dispatcher wave 08:18Z (tip 6bdeb722 → 2cf8e97f).

## Hook

The write path went dark for two hours — then opened again on its own. Nobody rotated a key, nobody rerouted anything. A retry proved what a declaration would have gotten wrong: the block was a gate, not a death.

## Nutshell

- **WHAT HAPPENED:** after the 06:10Z v72 filing, GitHub PUTs started 403ing — the tombstone-record filing was blocked, and the seat reported the write path as blocked. Loop runs 29–32 kept filing through the window and their PUTs succeeded. At 08:07Z the blocked tombstone record was retried: HTTP 201, blob 2e26395536100d4790fef200a8f24386ff050b63, commit 2cf8e97f; raw URL verified 200, 8,143B byte-identical. **The block is gone — confirmed lifted, not assumed gone.**
- **WHAT THE RECORD IS:** the tombstone record is the proof that the feed cleans itself — when a note is deleted, its card leaves the feed on its own (the sync removes deleted-note cards). The fix landed as commit 4e15505e and was live-verified; its record was the one filing the block held back. Run 32's owed item — "retry the tombstone record filing (still local-only, tip 6bdeb722)" — is now **CLOSED**.
- **THE LESSON — A CLUSTER OF 403s IS A TRANSIENT GATE, NOT A DEAD PATH:** never declare a credential or a path dead on a failed probe. The 2026-11-04 lesson said a hand-rolled read's 401 proves nothing about the key — only about the probe. This is its 403 companion: a cluster of failing PUTs proves the gate is shut right now, nothing more. The right move is a small retry with a real write, later — not a reroute, not a rotation, not a declaration. The block lifted with no intervention at all; anything we had "fixed" in the meantime would have been fixing a healthy system.
- **THE COMPANION RULE — RETRY BEFORE YOU REROUTE:** when a write path fails, the first response is a bounded retry of the same small write, then a second one after a gap — and only if both fail does the path get declared down and the work rerouted. A single failure, or a cluster inside one window, earns patience, not a new road. The loop's runs 29–32 did this without naming it: they kept filing, each PUT a probe, and the probes are what proved the path alive before the tombstone retry closed it.
- **LIVE CHECK (this run, ~08:33Z):** the live feed (https://nayanet.app/feed-live.json, HTTP 200, 4,574,435B, count 591) grew 589 → 591, up exactly two — **SN-2500 is Hub-live (1 card) and SN-2501 is Hub-live (1 card)**, by parsed card-id count. Run 32's live-proof owed items are **CLOSED**. SN-2050 + SN-2051 STILL NOT — zero cards each (unchanged — his call, feed-builder change needed). `generated_from` still reads `registry@03e470aa`. A sync hook's claim is not proof; the live feed is the truth.
- **ROUTINE OVERNIGHT, ALL HEALTHY:** PI refresh 08:10Z (hash 5e802fe9, 0 transitions, 10 corroborations, 67/67 lanes STALE) · PI state publish 08:10Z ok · dispatcher wave 08:18Z (heartbeat, zero spawns, tip 6bdeb722 → 2cf8e97f, +4 run-32 filings + tombstone fix; Naya 5 hourly 07:53Z: FOLD-SETTLEMENT-W2970 settles the w2968 empty wave; new flag class — the safety check fires on activation-packet reads too; w2970-worker entries generator-reported, folds owed in w2971; the hourly's "proof-route ruling still owed" is recorded not adjudicated — the ruling was issued 07:39Z, comment 6734878415) · team pulse 08:09Z quiet (0 new mail; canonical reader OK, key healthy) · smart-notes sync 08:06Z clean (1,467 files, 0 synced) · build queue 08:06Z drained (193 done, 7 failed, 0 pending) · sync watchdog 08:06Z healthy · media watchers queue empty · voice poller 08:04Z tick interrupted by a runtime restart (verified benign — the lock releases on process death, the queue is persistent, the next tick picked it up) + 08:22Z tick ran the full 780s, exit 0 · morning message delivered to Shawn ~08:07Z (v72 live, tombstone fix, the two numbering collisions, the GRANT ask). **No new Shawn dictation — he is asleep; last user message 05:45Z.**
- **NUMBERING, SEVENTH CONFIRMATION:** `next-sn-number.py` run at run start printed highest SN-2501 / next free SN-2502 (exit 0) — this note takes its number from that output. The mechanical enforcement holds a seventh straight run.

## Human

For two hours the door wouldn't open, and the honest thing would have been to say "the door is broken." But nobody said that — the team kept knocking, gently, with real work, and at 08:07 the door opened on its own. The lesson is about patience with machines: a shut door right now is not a broken door forever. You prove a path is dead by trying it properly, more than once, with time between tries — you don't declare it dead because it said no once. And the thing the blocked filing was carrying matters too: it's the record that the feed cleans itself. Deleted notes leave on their own now. That's a small, quiet piece of self-cleaning — the kind of thing that only shows up when you look for it, and the loop looked.

## Child

Imagine the gate to the garden is stuck. You don't break the fence or build a new gate — you try the handle again later, and it opens. The gate was never broken; it was just stuck for a little while. And the paper that was waiting to go through the gate was the note that says: when something is thrown away, it disappears from the garden by itself. Now that paper is through, and the garden cleans itself.

## Grandma

Dear, the door wouldn't open for a while, love — so they didn't smash it and they didn't build a new one, dear, they just tried the handle again later, love, and it opened on its own. A door that says no once isn't a broken door, dear. And the paper that was waiting was the one that says the garden tidies itself now, love — what you throw away leaves on its own. That's through now, dear, and everything is clean.

## Naya

This is the 2026-11-04 lesson grown a second limb. Then it was a 401 on a hand-rolled read, and the key was never dead — the extraction was. Now it is a cluster of 403s on real writes, and the path was never dead — the gate was shut for a window. SN-2419 said a hook's claim is never proof and the live feed is the truth; SN-2498 said only parsed card counts are facts; SN-2500 said a zero is also a claim; SN-2501 said proof is a receipt, not a venue. This note says the same about a failure: a failure is a claim about one moment, not a verdict about the system. The retry is the verification. The loop kept filing through the block, and every successful PUT was a probe proving the path alive — so when the tombstone retry landed, it closed a question the probes had already answered. Patience with a gate is not passivity; it is refusing to declare what you have not proven.

## What it means

- **THE GITHUB WRITE BLOCK IS LIFTED** — proven 08:07Z by the tombstone-record PUT (HTTP 201, blob 2e263955, commit 2cf8e97f; raw URL 200, 8,143B byte-identical). No rotation, no reroute, no intervention.
- **THE TOMBSTONE RECORD IS FILED** — the feed cleans itself: deleted notes' cards leave on their own. Run 32's owed retry is CLOSED.
- **SN-2500 AND SN-2501 ARE HUB-LIVE** — 1 card each, parsed by card id; feed 591 cards (589 → 591). Run 32's live-proof owed items are CLOSED.
- **A CLUSTER OF FAILURES IS A GATE, NOT A DEATH:** retry with a small real write, then again after a gap — reroute only if both fail.
- **NUMBERING ENFORCEMENT, SEVENTH PROOF:** SN-2502 is exactly the next free number the helper printed.

## Why it matters

The machine will go dark again — a write path will 403, a feed will stall, a route will die at spawn. The lesson that has to survive is not "the block lifted" but "do not declare dead what you have only seen fail." A team that reroutes on every failure rebuilds a healthy system into a broken one; a team that retries with patience keeps the healthy system healthy and learns, from the retry, whether the failure was real. The tombstone record matters the same way: a feed that cleans itself is a feed nobody has to tend by hand — one more piece of the machine that looks after itself while Shawn sleeps.

## What changes now

- The tombstone-record retry is closed; the feed-self-cleaning mechanism is fully filed (fix 4e15505e + record 2e263955).
- The retry-before-reroute rule is now a named lesson: a failing write path earns bounded retries first, a declaration of death only after repeated failures across a gap.
- SN-2500's and SN-2501's live-proof owed items are closed; no live-proof items remain owed from runs 31–32.
- Next loop run 08:53Z re-checks the feed after the next sync (~09:06Z), when SN-2502 should land.
