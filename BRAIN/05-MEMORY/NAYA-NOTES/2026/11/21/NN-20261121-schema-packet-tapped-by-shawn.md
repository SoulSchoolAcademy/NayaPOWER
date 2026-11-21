# NN-20261121-schema-packet-tapped-by-shawn

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-schema-packet-tapped-by-shawn · Naya Note · 2026-11-21 ~13:03 MST**

*Paired Smart Note: SN-4561 — Schema Packet — Tapped by Shawn*

**Category:** LAW — his tap authorizes the Dashboard schema packet; Hub DDL and invite-sender are NOT in it

**Status:** Written in run 474. His tap, voice, ~13:03 MST, as recorded in the curated memory. Protected gate — his hand, now given.

## What it is

**SCHEMA PACKET — TAPPED BY SHAWN (voice, 2026-11-21 ~13:03 MST):** "Okay so do it. Tap it. Put it in. Make it so." His tap authorizes applying the Dashboard schema packet (`SCHEMA-PACKET.md`, 23,870 B, sha `51c0aad4…`): §2 grants + §3 `naya_action_events` table/function + §4 ledger trigger migration (blob `91dd19dd…`). Apply round dispatched ~13:04 (coordinator `20cf668f`): chain check first, baseline, preview battery, production ONLY via `governed-supabase-production-deploy.yml` (`confirm=DEPLOY`, source_sha = current main tip at apply time), then per-action re-proof. NOT in the tap: Hub DDL (why_it_matters/how_it_connects) — separate, still waiting; invite-sender unblocker (stays record-only/DRY-RUN).

## Why it matters

The schema packet is the unblocker for the whole Dashboard mechanics story — the ledger that never recorded an action, the messenger leg that cannot send, the points that computed twice. His tap is what turns a packet on a shelf into a working ledger. And the boundary is the other half of the tap: Hub DDL and the invite-sender stay out, so nobody treats "he tapped the packet" as "he tapped everything." A tap with a boundary is a tap that can be trusted; a tap without one is a blank cheque.

## How to use it

Apply the Dashboard schema packet through the governed deploy path only (`governed-supabase-production-deploy.yml`, `confirm=DEPLOY`), in the apply order: chain check, baseline, preview battery, production, per-action re-proof. Do not apply the Hub DDL or the invite-sender unblocker on this tap — they wait for their own.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
