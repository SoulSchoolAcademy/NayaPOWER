# ClickHouse — The Verdict

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261112-clickhouse-the-verdict.md · Naya Note · 2026-11-12 21:24Z**

**Category:** System

## What it is

Shawn 21:24Z Nov 12 — his question, the captain's answer, he 👍'd it. Recorded in MEMORY.md as CLICKHOUSE — THE VERDICT. The right warehouse, but not yet. Supabase Postgres IS the warehouse for now (source of truth, the agent queries it freely, no rate limits, already paid) — the warehouse job is one pipe: ad-platform data synced INTO Supabase. ClickHouse Cloud later, when MEASURED volume earns it (a real funnel query gets slow, or ~1M rows/day): keep Supabase as truth, add ClickHouse as the analytics copy. Cloud prices verified Aug 2026: no permanent free tier (30-day trial, $300 credits); Basic ~$66/mo part-time to ~$186/mo always-on + $25.30/compressed TB/mo; Scale from ~$499/mo. Self-host free (Apache 2.0) but someone runs it. BigQuery/Snowflake/Redshift: no. In the same answer, NayaStudio restated: keep the fork — it is Tesseract OCR (text recognition), not the Mirage video editor; its real NayaNET job is the quality checker reading words in finished ad frames against approved claims.

## Why it matters

The verdict is a decision rule, not a purchase. "Not yet" is the discipline: no money moves, no second system is adopted, until a MEASURED trigger fires — a real funnel query going slow, or ~1M event rows a day. Supabase stays the single source of truth either way; ClickHouse, when it comes, is an analytics COPY, never a replacement. The warehouse job right now is one pipe — ad-platform data synced into Supabase — which costs nothing new and risks nothing. And NayaStudio's job is settled as the quality checker (OCR reading ad frames against approved claims) — not a video editor, and no build should treat it as one.

## How to use it

Build the one pipe: ad-platform data synced into Supabase. Do not build or buy ClickHouse until the trigger fires (a slow funnel query or ~1M rows/day). When it fires, the shape is already decided: Supabase stays truth, ClickHouse is the analytics copy. Treat NayaStudio as the quality checker, never as a video editor.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2719 — ~/workspace/team-nitro/smart-notes/SN-2719-clickhouse-the-verdict.md*
