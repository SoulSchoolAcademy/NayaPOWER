# NAYA ACTIVATION PROTOCOL v2 — "Connect First" Law
Shawn's standing law, 2026-10-09: no Naya does any work until activated.
Activation is not a document you read. It is a sequence you run, a receipt you write, and a SHA you cite.

## The law (Shawn's words, plain)
> Before you touch any work for me or my people: connect to the supercomputer first.
> Get tuned in. Activate NayaPOWER. Restore context. Boom — now you're locked in, now you know, now you can do good work.
> Unactivated work doesn't ship. Ever.

## Why the old version failed
`NAYA-ACTIVATION/00-MASTER-COLD-NAYA-ACTIVATION.md` was a brief — text describing how to behave.
Text loses to satisficing under load. A fresh mind under pressure reaches for the first workable pattern,
not the best one, and nothing caught the miss before Shawn saw it. The failure was never missing knowledge.
It was missing ENFORCEMENT.

## The protocol — run every session, before any work

### Step 0: RESOLVE
Get the live main SHA. Not a remembered SHA, not yesterday's — live, right now.
`git ls-remote https://github.com/SoulSchoolAcademy/NayaPOWER.git HEAD`

### Step 1: LOAD
Pull the current state into working memory:
1. Design doctrine version — resolve in order: (a) `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md` on main if present; (b) `HUB/DESIGN-CONTRACT.md` on main. Record the file used and its SHA in the receipt. If neither resolves, activation FAILS CLOSED with `DOCTRINE_UNAVAILABLE` — never proceed on assumed doctrine, never get stuck silently.
2. Block library version — entry count + index SHA of `BRAIN/10-INTERFACES/DESIGN-BLOCKS/`
3. Goal state — the active goals and their current status
4. Feed digest — latest #1354 state (last comment id seen, open decisions needing Shawn)

### Step 2: RECEIPT
Write an activation receipt (shape: `NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json`):
session id, timestamp, main SHA, the four component SHAs/digests above, and the word ACTIVATED.

### Step 3: CITE
Every work product cites the activation receipt SHA. A deliverable without a current
activation citation is not valid work — it is indistinguishable from guessing.

## Freshness rule
A receipt is current for 4 hours OR until main moves, whichever comes first.
Main moved = re-activate before the next action. A decision computed on tip T is
inadmissible after the tip moves (SN-0493) — activation is how that law gets enforced.

## Verification (how the law gets teeth)
No future mind can be physically forced to run a sequence — there is no BIOS.
So the law is enforced the three ways that actually work:
1. **Connected is the default.** Session-start injection carries LIVE state (current SHA,
   doctrine version, block count) computed at wake-up, not written by hand. The seat
   wakes up connected; it never has to remember to connect.
2. **Skipping is detectable.** Receipts carry SHAs. The design gate checks every
   deliverable for a current activation citation. No citation = visible, flaggable, rework.
3. **Skipping is pointless.** The blocks, the generators, the briefs, the doctrine —
   everything worth using lives behind activated state. An unactivated seat works blind,
   with worse tools and worse results. There is no advantage in skipping.

## What this replaces
Shawn as the linter. Shawn as the re-teacher. Shawn as the context-relay between seats.
The supercomputer holds the state; activation loads it; the receipt proves it; the gate checks it.
He teaches once — the machine carries it forever.

---
*2026-10-09 (Naya 3 review): fixed Step 1.1 — the stated DESIGN-DOCTRINE.md path does not exist on main; added resolution order + fail-closed rule so a fresh Naya never gets stuck.*
