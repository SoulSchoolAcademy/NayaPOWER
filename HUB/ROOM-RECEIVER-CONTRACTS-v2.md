# HUB ROOM RECEIVER CONTRACTS v2 — rooms 6–12

**Status:** DRAFT — for team review alongside the Master Build Contract (PR #2700). Not merged. Not ratified.
**Author seat:** Naya Clarity Narzan (Naya 4), 2026-10-16 ~00:45 PDT, at Shawn's word: *"complete the contract for each room."*
**Basis:** each room's latest page file was audited from its own bytes on 2026-10-16 (inputs, localStorage keys, network calls, bridge seams, baked-data markers). Universal audit finding: **every room is a static island** — 0 network calls, no bridge seams, localStorage-only persistence. The contracts below are what each room must receive to stop being an island.

**The universal pattern (from the Master Contract §4.6):** receiver contract frozen → page made bridge-ready → sender lands on a ready socket → no localStorage-only islands, no sender without a receiver. One writer per path. Honest empty/offline states. Amendment = version bump + migration note.

**Envelope (all rooms):** `{room, kind, contract_version:"v2", payload, event_id, received_at}`. The bridge translates storage rows into this envelope; the page renders the envelope and nothing else.

Rooms 1–5 (Smart Feed, Today, Reports, Smart Ledger, Activity Feed) are covered by the Symphony contracts v1. What follows is rooms 6–12.

---

## Room 6 — Intelligent Library
**Audited:** `library-v3.html` (126 KB). Keys: `naya.library.blocks.v3`, `naya.library.pins.v1`, `naya.library.tabs.v1`. 0 network. No bridge seam.
**Receives:** `library-block` — `{id, title, kind, body, source_ref, topics[], created_at}`. Blocks are published intelligence entries (notes, report nutshells, lessons).
**Sender (one writer):** the intelligence publish pipeline (pump for notes, report emitter for report nutshells). Table: `nayanet_intelligent_blocks` (exists, 191 rows — already on the realtime publication as of T1).
**Returns:** pins and tab order — local-first (`naya.library.pins.v1` stays the cache); cross-device pin sync is opt-in, consent-gated.
**Honest states:** empty shelf ("no blocks published yet"), offline ("showing cached blocks").

## Room 7 — Smart Connect
**Audited:** `connect-3.html` (139 KB). 0 network. No bridge seam. Doors render from baked markup.
**Receives:** `door-state` — `{door_id, name, status: "open"|"closed"|"setup-needed", target_url, last_verified_at, verified_by}`.
**Sender (one writer):** the door-setup workers (goal: "make every Smart Connect door actually work"). Table: new `connect_door_states` (to create) — doors are setup state, not intelligence; they deserve their own table.
**Returns:** "test this door" → verification request event → worker re-verifies → new `door-state` arrives. The loop is the feature.
**Honest states:** a door whose `last_verified_at` is stale shows "unverified," never a green open-door lie.

## Room 8 — Your Connections
**Audited:** `connections-3.html` (86 KB; `connections-10.html` is byte-identical). Key: `naya.mail.compose.request`. 0 network. No bridge seam.
**Receives:** `connection` — `{id, name, relationship, last_contact_at, notes_ref, source: "user"|"naya"}`.
**Sender (one writer):** the relationship map (`~/memory/people/` is the human record; the bridge projects consented entries). Table: new `user_connections` (to create).
**Privacy:** personal data — local by default; any cross-device or shared sync needs Shawn's explicit consent path (same gate as the Activity Feed). The contract ships with sync OFF.
**Honest states:** empty ("no connections added"), private ("kept on this device").

## Room 9 — Smart Lists
**Audited:** `lists-3.html` (338 KB). Key: `naya.smartlist`. 0 network. No bridge seam.
**Receives:** `smart-list` — `{id, title, items: [{text, done}], source: "note"|"manual"|"naya", updated_at}`.
**Sender (one writer):** the pump (lists distilled from notes) + the user (manual lists) — two writers, one table, split by `source`. Table: new `smart_lists` (to create).
**Returns:** item check/uncheck → row update → realtime broadcast → every device converges.
**Honest states:** offline edits queue locally and sync on reconnect; the page says "2 changes waiting to sync."

## Room 10 — Smart Mail (NayaNET-native messaging — NOT email)
**Shawn's word, 2026-10-16 ~00:25 PDT:** Smart Mail is the communication system *inside* NayaNET — mail anyone by their alias, mail the spaces. It is not email and never touches external mail. (Correction: the earlier "mail line" hold was premised on external email — wrong premise. The internal system has his word: build it.)
**Audited:** `mail-3.html` (188 KB). Keys: `naya.smartmail.sent`, `naya.mail.compose.request`, `naya.people.registry`. 0 network. No bridge seam.
**Receives:** `mail-thread` — `{id, subject, preview, from_alias, to_alias|space_ref, received_at, thread_ref}`; `mail-message` — `{id, thread_id, from_alias, body, sent_at}`.
**Sender (one writer):** the messaging service (to build) — alias registry + space channels. Tables: `smart_mail_aliases` (10 seeded from the page's own registry), `smart_mail_threads`, `smart_mail_messages` — **CREATED 2026-10-16, all three on the realtime publication, send/receive round-trip proven** (thread `e24d37a6-…`, naya4 → team-naya). RLS currently off — per-alias policies are a follow-up for the bridge team, not blocking.
**Returns:** compose → send → row insert → realtime → the recipient's Smart Mail lights up. The compose box stops being a draft pad and becomes a sender.
**Addressing:** aliases resolve via the people registry and the space registry (`naya.people.registry` is the local seed).
**Honest states:** "no messages yet," offline outbox ("1 message waiting to send"), unknown alias ("no one on NayaNET goes by that alias").
**Contract status:** UNBLOCKED — build it.

## Room 11 — Smart Spaces
**Audited:** `spaces-4.html` (175 KB). Keys: `naya.spaces.pins.v1`, `naya.connection.v1`. 0 network. No bridge seam.
**Receives:** `space` — `{id, name, pins: [], member_refs: [], updated_at}`.
**Sender (one writer):** the user + the team (spaces are shared canvases). Table: new `smart_spaces` (to create).
**Returns:** pin/unpin → row update → realtime → shared members see it live.
**Honest states:** "you haven't pinned anything here yet," offline queue like Smart Lists.

## Room 12 — PowerCast (the 12th room)
**Audited:** `powercast-v516-ecobar.html` (1.6 MB). Keys: `pc-pos`, `pc-queue`, `pc-saved`, `pc-topics`. 0 network. No bridge seam. Has its own goal: "PowerCast ultimate player."
**Receives:** `episode` — `{id, title, audio_url, duration_s, topics[], published_at, source_brief}`.
**Sender (one writer):** the podcast pipeline (briefings and generated episodes). Table: new `powercast_episodes` (to create).
**Returns:** play position, queue, saves — local-first (`pc-pos` etc. stay the cache); cross-device resume is opt-in.
**Honest states:** no episodes ("nothing published yet"), audio unreachable ("couldn't load this episode — retry").

## Room 0 — Settings (the control surface)
**Audited:** `settings-preview.html` (19 KB). Key: `naya.settings`. Contains `simLive` markers — its "live" toggles are simulated. 0 network.
**Receives/writes:** `setting` — `{key, value, scope: "device"|"account", updated_at}`. This room is primarily a WRITE path: the human's hand on the system's dials.
**Sender (one writer per key):** the settings service (to build) — one writer, versioned keys, every change logged.
**Protected:** some dials touch Shawn's protected gates (deploy, credentials, privacy, ratification) — those settings are read-only in the UI without his explicit word, and the contract marks each key's gate class.
**Honest states:** a setting the bridge can't reach shows "not connected," never a fake toggle.

---

## Build order (T15 broken down)

1. Library (table exists, data exists — fastest win after the first five)
2. Smart Connect (door-setup goal is live — pair the contract with that goal's workers)
3. Smart Lists (pump-adjacent — lists fall out of notes)
4. PowerCast (own goal, own pipeline — parallelizable)
5. Spaces, Connections (new tables, consent paths — steady work)
6. Settings (write-path service + gate classes — careful work)
7. Smart Mail (UNBLOCKED per Shawn's word — alias messaging + space channels, NayaNET-native)

**Amendment guardrail:** frozen means frozen — version bump + migration note + both sides updated. Silent shape drift is a breach.
