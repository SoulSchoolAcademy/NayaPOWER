# NN-20261119-a-fix-proven-at-rest-is-not-proven-in-motion

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261119-a-fix-proven-at-rest-is-not-proven-in-motion · Naya Note · 2026-11-19 ~17:01 MST (00:01Z 2026-11-20)**

*Paired Smart Note: SN-3961 — A Fix Proven at Rest Is Not Proven in Motion*

**Category:** Verification — Proof

## What it is

Dashboard follow-up 14 passed its checker: both f13 fails cured on render — gear vs X 10px clear at 1920 (was a 26×22px overlap), clear at scroll 0/1200/2400 with the panel open and closed, and the state-cell labels exactly aligned at 1920 and wrapped 2×2 at 390. But the checker carried two honest limits. First, transient scroll pass-through: the gear overlaps the X at scroll offsets 20–80, because the gear is `position:absolute` and scrolls with the document while the X is sticky — clear at every measured stop, failing in motion between them. It is pre-existing broken fixing, so the round passes, and a follow-on round is owed to cure the fixing itself. Second, no data-loaded render from the seat (41 Supabase requests, 2 responses): the conversation line, first-paint numbers, world-board stats routing and the X-vs-WEEK pill are owed to the captain's eye on a data-loaded render. Staged only — no merge, no live, no link to Shawn.

## Why it matters

The citizen scrolls. Every scroll passes through the offsets between the measured stops, so a fix that fails in motion fails where the citizen lives — even while it passes every measurement the brief asked for. And a render with no data proves the frame, not the page: the numbers the citizen reads are the page.

## How to use it

Checkers measure the pass-through, not just the stops: scroll the page continuously and watch the moving parts against each other at every offset. A PASS that names an in-motion failure carries its follow-on in the same pass. The gear-fixing follow-on and the data-loaded eye are the next proofs of this law.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
