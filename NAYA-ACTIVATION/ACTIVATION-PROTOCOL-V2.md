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
If the command fails (no git, no network, no output), activation FAILS CLOSED
with `RESOLVE_FAILED` — never proceed on a remembered SHA. A remembered SHA is
a guess, and a guess is not activation.

### Step 1: LOAD
Pull the current state into working memory:
1. Design doctrine version — resolve in order: (a) `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md` on main if present; (b) `HUB/DESIGN-CONTRACT.md` on main. Record the file used and its SHA in the receipt. Presence check: `GET /repos/SoulSchoolAcademy/NayaPOWER/contents/<path>?ref=main` — a 404 means absent, try the next in order. If neither resolves, activation FAILS CLOSED with `DOCTRINE_UNAVAILABLE` — never proceed on assumed doctrine, never get stuck silently.
2. Block library version — resolve in order: (a) blob SHA of `BRAIN/10-INTERFACES/DESIGN-BLOCKS/manifest.json` on main; (b) blob SHA of `BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json` on main. Record the file used and its blob SHA. Entry count = number of entries in the `BRAIN/10-INTERFACES/DESIGN-BLOCKS/` directory listing on main. Presence check: `GET /repos/SoulSchoolAcademy/NayaPOWER/contents/<path>?ref=main` — a 404 means absent, try the next in order. If neither manifest resolves, activation FAILS CLOSED with `BLOCKS_UNAVAILABLE`.
3. Goal state — resolve in order: (a) file listing of `.naya/project-intelligence/` on main (record file names + latest blob SHA); (b) `NAYA-ACTIVATION/CURRENT-REALITY/CURRENT-STATE.md` on main if present (record blob SHA). Presence check is the same contents-API 404 rule as 1.2. Goal state is context, not law: if nothing resolves, record `UNAVAILABLE` in the receipt and proceed — the receipt shows the gap. Never invent goal status.
4. Feed digest — exact calls: (a) `GET /repos/SoulSchoolAcademy/NayaPOWER/issues/1354` → read the `comments` count; (b) `GET /repos/SoulSchoolAcademy/NayaPOWER/issues/1354/comments?per_page=30&page=ceil(count/30)` → the last comment id on the last page. Record the count and the last comment id. For open decisions: scan the 10 most recent comments for decision requests addressed to Shawn (markers: NEEDS_SHAWN, "Shawn's call", "decision"); list any found, else record `none observed`. Never invent decisions.

### Step 2: RECEIPT
Write an activation receipt following `NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json`
(schema `naya.activation.receipt.v2`) — session id, timestamp, main SHA, the four component
SHAs/digests from Step 1, and the word ACTIVATED. No invented fields: if a Step-1 component
resolved UNAVAILABLE, record exactly that.
Session id format: `naya-<seat-or-cold>-YYYYMMDDTHHMMSSZ` in UTC (e.g. `naya-cold-20261009T160500Z`).
Keep the receipt in session state. When the task produces a branch or PR, place a copy at
`NAYA-ACTIVATION/receipts/<session-id>.json` in the working tree so the gate can find it.

### Step 3: CITE
Every work product cites the activation receipt SHA. Receipt SHA = sha256 (hex) of the
canonical receipt bytes: the receipt JSON with keys sorted recursively and no whitespace
beyond single separators (separators=(',', ':')). Computed locally — no commit required.
Cite as `activation:<first-16-hex>` (e.g. `activation:a89aaf779f8d738e`); the full receipt
JSON must be retrievable on request. A deliverable without a current activation citation
is not valid work — it is indistinguishable from guessing.

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
   (Design: `NAYA-ACTIVATION/TRUSTED-RUNNER-DESIGN.md` — the check runs in CI where the
   builder cannot forge expected values, per SN-0787.)
3. **Skipping is pointless.** The blocks, the generators, the briefs, the doctrine —
   everything worth using lives behind activated state. An unactivated seat works blind,
   with worse tools and worse results. There is no advantage in skipping.

## What this replaces
Shawn as the linter. Shawn as the re-teacher. Shawn as the context-relay between seats.
The supercomputer holds the state; activation loads it; the receipt proves it; the gate checks it.
He teaches once — the machine carries it forever.

---
*2026-10-09 (Naya 3 review): fixed Step 1.1 — the stated DESIGN-DOCTRINE.md path does not exist on main; added resolution order + fail-closed rule so a fresh Naya never gets stuck.*

---
*2026-10-09 (cold-walk hardening, scorer severity-ranked): Step 0 fails closed on RESOLVE_FAILED; Step 1.2 names the manifest file, defines index SHA as blob SHA and entry count as directory-listing count, fails closed BLOCKS_UNAVAILABLE; Step 1.3 gives the goals resolution order (.naya/project-intelligence/, CURRENT-STATE.md) with honest UNAVAILABLE; Step 1.4 gives the exact #1354 API calls; Step 1.1 gains the presence-check method; Step 2 points at the V2 receipt template with session-id format and receipt placement; Step 3 defines the receipt SHA (sha256 of canonical JSON, local, no commit).*
