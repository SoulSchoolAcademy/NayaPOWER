# Smart Box Pieces 3–5 — Done, the Vault Is Complete

SN-2570 · DESIGN / SMART BOX

**Created:** 2026-11-09 20:12Z

**Source:** Coordinator 7cd08c9d completion, completed 19:56Z Nov 9, recorded in MEMORY.md (not a dictation — a completion report). No paired Naya Note (verification/completion result, not a dictation — same as SN-2560, SN-2552, SN-2553).

## Hook

The vault is complete — engine, key system, bridge, and recovery, proven in about twenty minutes, not hours. The new pace held. A different seat tried ten ways to break in and could not get in once.

## Nutshell

- **DONE (coordinator 7cd08c9d, completed 19:56Z):** organize + key lifecycle + bridge + the sickness's root + the map. The 10x list from Shawn's 8/10 scorecard of the first pass, built in ~20 minutes — the pace ruling (SN-2569) held: now, not hours.
- **SUITE 91/91 GREEN** (fresh copies, twice).
- **INDEPENDENT VERIFICATION (different seat): OVERALL PASS.** Attack test **10/10 BLOCKED** — read private without a key, organize as a stranger, share without the owner's choice, flipped-visibility share, revoked key, forged key, another Naya's key, key for another owner, unknown action, revoked-key bridge carry — every one DENY; owner control ALLOW.
- **TWO VERIFIER GAPS CLOSED BEFORE FILING:** stale organize counts (341/199 → 365/220) · **the real hole: a forged key got ALLOW when may_share was called without a registry — closed, the gate now fails closed** (the single choke point; only no-registry ALLOWs are owner-on-own-block and anyone reading a public smart note).
- **RECOVERY DEMO:** sync state (1,519 files, 298,217B) + heartbeat captured into the box; wiped directory rebuilt from the box, both files byte-identical.
- **BRIDGE:** SN-2535 carried box→box zero loss; second carry DUPLICATE (destination holds 1 copy); space from a note in one click, second click EXISTS, never a duplicate.
- **MAP:** every proof note's `where` carries its `hub_smart_notes` row; no Box table exists (re-verified live, 5 probes PGRST205) — no row id invented.
- **GITHUB: 10/10 FILES, ONE AT A TIME, READ-BACK VERIFIED** (blueprint blob 75fc5887, 38,013B; block.py 3ab96f22; gate.py 6a26a863; bridge.py 3815103a; syncbox.py c59aa6c0; test 2879f948; README ee0e0459; manifest b719bf2e; .sync-state ccfb6bf3; .sync-heartbeat ba892f46; main tip f3237618).
- **NO MERGE — SHAWN'S HAND.**
- **HONEST SCORE: 9/10** (builder's own, verifier agreed).
- **NOT DONE:** live citizen vault end-to-end · the wiring (organize pipeline hook, repointing sync to read from the box, durable key record, bridge wired into live sync/feed path) · Shawn's eye.
- **SHAWN 19:31Z, ON THE FIRST PASS:** "Yeah, it is really good. Very well done. Very good for you understanding this, this will be an enormous part of our system. So make sure that you scorecard your own work, make sure it's ten out of ten. Is there anything you're missing? Is there anything to make it ten times better? It's just about implementing and building and make sure it's solid, like rock solid like a vault." His order, same message: interfaces first, then the system that runs the system.
- **THIS SEAT'S OWN CHECK:** not re-run live this run — the evidence is the coordinator's own read-back verification (10/10 files, blobs recorded) plus the independent verifier's OVERALL PASS on the same build. This seat does not claim a live blob check it did not run.

## Human

The first pass built the shape and the gate. This pass built everything the scorecard said was missing: the engine that organizes, the key system that mints and revokes, the bridge that carries a block from one box to another, the root of the saving sickness, and the map. Ninety-one tests green, run twice on fresh copies. A different seat attacked it ten ways — forged keys, revoked keys, another Naya's key, a key for another owner — and every attack was denied. The verifier did find a real hole before filing: a forged key got in when the gate was called without a registry, and the gate was changed to fail closed. The recovery demo is the proof that matters most for the sickness: the sync state and heartbeat went into the box, the directory was wiped, and the box rebuilt both files byte for byte. The bridge carries a note box to box with zero loss, and the second carry is a duplicate that the destination refuses — one copy, never two. The honest score is nine, not ten: the vault is built and proven, but it is not yet wired into the live system, no live citizen has used a vault end to end, and his eye has not seen it. And it took about twenty minutes — the new pace held.

## Child

Imagine the treehouse is finished now — not just the boards and the lock, but the stairs, the key chain, and the bridge to the next tree. Ninety-one tests, all green, checked twice. A different friend tries ten ways to sneak in — a copied key, a taken-away key, someone else's key — and the lock says no every single time. The friend does find one crack: a copied key works when the lock doesn't check the list — so the lock is fixed to always check the list, and to say no when there is no list. Then the big test: everything in the treehouse is packed into a box, the treehouse is knocked down, and the box rebuilds it exactly — every board in the same place. The bridge works too: a note walks across to the other tree without losing a word, and walking it twice doesn't make two notes. Nine out of ten, because the treehouse isn't connected to the village yet, no one has lived in it, and dad hasn't seen it. And it took twenty minutes, not hours.

## Grandma

Dear, the vault is finished now, love — the engine, the keys, the bridge, and the way back, all built and tested. Ninety-one little tests, all green, love, run twice on fresh copies. A different friend tried ten ways to break in — a copied key, a taken key, somebody else's key — and the door held every time, dear. The friend did find one crack, love — a copied key slipping through when the list wasn't checked — and the lock was fixed to always check, and to say no when there's no list to check. The recovery, dear, is the beautiful part: everything packed into the box, the room wiped clean, and the box building it all back exactly as it was. The bridge carries a note across without losing a word, love, and a second trip never makes a second note. Nine out of ten, dear — not wired into the live house yet, no one has lived in it, and his eye hasn't seen it. And it took twenty minutes, love, not hours — the new pace held.

## Naya

I am Anaya. The Smart Box pieces 3–5 are done: organize, key lifecycle, bridge, the sickness's root, and the map — 91 out of 91 green, independently verified OVERALL PASS by a different seat, attack test 10 out of 10 blocked, recovery demo byte-identical, bridge zero-loss with duplicate refused, GitHub 10 out of 10 files read-back verified, no merge — his hand. The verifier found a real hole before filing — a forged key allowed when the gate was called without a registry — and the gate now fails closed. Honest score nine out of ten: the vault is built and proven, but the wiring into the live system is not done, no live citizen vault has run end to end, and his eye has not seen it. It took about twenty minutes. The new pace held.

## What it means

- **THE VAULT IS COMPLETE AS A BUILD:** shape + gate (first pass) + engine + key + bridge (this pass), 91/91 green, attack test 10/10 blocked, recovery byte-identical, GitHub 10/10 read-back verified.
- **THE GATE FAILS CLOSED:** the forged-key hole the verifier found is the lesson — a gate that allows when it cannot check is not a gate; the fix is in the code, not in a promise.
- **THE BRIDGE REFUSES DUPLICATES:** one copy, never two — the same rule as a space from a note (SN-2535's carry, second click EXISTS).
- **NOT DONE IS NAMED:** the wiring (organize hook, sync reading from the box, durable key record, bridge in the live path) · live citizen vault end-to-end · his eye.
- **THE PACE RULING IS PROVEN BY DOING:** ~20 minutes from dispatch to done — the first proof that "now, not hours" holds on a real build.
- **NO MERGE** — his hand.

## Why it matters

This is the first time a whole system — not a piece of one — went from brief to built, attacked, fixed, and filed inside one sitting, in about twenty minutes. It proves the pace ruling is not a slogan: the same work that used to take six, ten, twelve hours landed in twenty minutes because the seat was on it now and the captain kept it unstuck. It proves the fail-closed lesson in code: the verifier's forged-key hole is exactly the kind of hole that only shows up when a different seat attacks, and it was closed before filing, not after. And it draws the honest line for what comes next: the vault is built, but a vault nobody can use yet is a model, not a system — the wiring is the work, and his 20:07Z order (SN-2571) names it.

## What changes now

- Pieces 3–5 are done and verified — the vault has its engine, its keys, its bridge, and its recovery.
- The wiring is the next build: organize pipeline hook, sync reading from the box, durable key record, bridge in the live sync/feed path — dispatched by his 20:07Z order (SN-2571).
- A live citizen vault end-to-end and his eye remain the final gates.
- Next loop run checks: whether the wiring coordinator has landed its proof, and whether his eye has seen the vault.
