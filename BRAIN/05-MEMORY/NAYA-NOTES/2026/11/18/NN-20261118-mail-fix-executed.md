# NN-20261118-mail-fix-executed

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-mail-fix-executed · Naya Note · 2026-11-18 ~21:55Z**

*Paired Smart Note: SN-3486 — The Mail Fix Is Done: The Key Moved Server-Side, and the Digests Flow Again*

**Category:** System — Mail

## What it is

Shawn's go ~21:51Z; mail fix executed and verified working ~21:55Z. One file only — `~/workspace/project-intelligence/send-mail-helper.py`: the old-key scrape out of flagship-template.html is gone; `get_service_key()` added, copying the welcome scheduler's pattern (Supabase Management API, memory only, never printed or written). Verified: service key returns (len 219); reads return rows (5/5 sample both mail tables); test send to diag-test landed (thread c506628e…, message 8a7e63e5…), no 42501, read back and deleted; held digest run198 sent to both team aliases (naya-power + resolve), exit 0.

## Why it matters

The team's mail tools lost access when the privacy fix landed, and the digests were held. The fix moves the key server-side — never in page code — and the proof is a real send that landed and read back, not a key returning alone.

## How to use it

**run199/run200 must NOT be run blindly** — run199 resends run198, run200 resends run199; the loop owner must mark them sent/superseded or the same digest goes out twice. Browser-page mail (Personal composer, Message-this-app, instant message) still needs his pick: privacy-rule change OR Edge Function. Full record: `~/workspace/team-nitro/mail-fix-20261118/MAIL-FIX-EXECUTED.md`.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
