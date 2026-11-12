# The Mail Is Safe — 1,789 Records, Our Key Lost Access

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261112-the-mail-is-safe.md · Naya Note · 2026-11-12 19:27Z**

**Category:** Mail / Access / Privacy

## What it is

Shawn's dashboard check at 19:27Z Nov 12, from his own screenshot: `smart_mail_messages` holds **1,789 records** (page 1 of 18, 100 rows) — the mail is THERE, visible in the Supabase dashboard under Role: postgres. Our reader lost access, not the mail: the anon key reads 0 rows on both mail tables and writes 401 since the 18:54–19:05Z window. The most likely cause is the mail privacy fix landing (the RLS repair that removes anon access — the end-state we wanted for privacy); the team's mail tools just need the right key now.

**The fix:** move the team's mail tools to the server-side key (the pattern the worker's `/api/claim` already uses) — his hand, a credential/access change. Until it lands, the team-pulse receipt check and the intelligence loop's mail step cannot complete.

Test rows for the joint cleanup (add): certs **147** (`capwalkfix1`) + **148** (`capwalkfix2`), both "Naya Nitro Narzan", claimed 19:26Z · KV `complete_capwalkfix1` + `complete_capwalkfix2`.

## Why it matters

The mail was never lost — only our key to it. That distinction decides everything: no data recovery, no rebuild, no panic — just the right key on the team's mail tools. And the cause is the privacy fix we wanted: the RLS repair doing its job, removing anon access. The end-state we wanted for privacy arrived before the tools were moved to the server-side key — the order flipped, and the fix is his hand because it touches credentials.

## How to use it

Move the team's mail tools to the server-side key (the `/api/claim` pattern) — his hand, a credential/access change. Until it lands, treat mail-new as UNKNOWN, never 0, and send no receipts on a blind read. Hold the loop's digests; do not claim mail sent that was not sent.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2702 — ~/workspace/team-nitro/smart-notes/SN-2702-the-mail-is-safe.md*
