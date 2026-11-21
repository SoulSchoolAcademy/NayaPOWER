# NN-20261121-we-gotta-fix-it-the-supabase-red-spike

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-we-gotta-fix-it-the-supabase-red-spike · Naya Note · 2026-11-21 ~10:27–10:29 MST**

*Paired Smart Note: SN-pending — Fix It, Don't Just Explain It (takes the next free number at filing)*

**Category:** LAW — a red signal is a fix order, not an explanation prompt; fixed is proven by the numbers moving, never by a code change alone

**Status:** Written in run 469. His words from his own screenshots of the Supabase dashboard, as recorded in MEMORY.md from the same call — sent to the Dashboard mechanics coordinator (926c2517). The cause of the errors is not in the screenshots; the Postgres error log is that round's job.

## What it is

**THE SUPABASE RED SPIKE — FIRST-HAND FROM HIS SCREENSHOTS (2026-11-21 ~10:27 MST):** project `supabase-red-cable` (dahisasgpfvziswqvmvm), STATUS Healthy, Nano, Canada Central, CPU 8% / Disk 24% / RAM 65% / 15 of 60 conns, last backup 7h ago, last migration `person_timeline_view_columns_repai…`. Last 24h: 164,872 total requests, 97.0% success. POSTGRES 5,526 calls, ERRORS 2,497 (~45% failing) — red bars concentrated Nov 20 ~11am, tapering to green by Nov 21 morning. EDGE FUNCTIONS 83,895, 0 errors; AUTH 8, 0 errors; STORAGE 0; REALTIME 0. The 97% hides the Postgres failures because edge dominates the total. State-change machinery exists in the functions list: triggers `items_state_changed` + `items_transition_log` (fire + log on every item state change), `bookings_fill_owner` + `bookings_guard_slot`.

**HIS READING OF IT:** "And then you can see there's some kind of message in the screenshots that I don't understand. So there's been a change of state."

**THE FIX ORDER (2026-11-21 ~10:29 MST):** "Yeah, because something happened and it doesn't look good. We gotta fix it." Sent to the Dashboard mechanics coordinator (926c2517): pull the Postgres error log, name which calls are failing and why, fix the cause, prove it by the error count falling + a real action landing in the Ledger and moving the Dashboard number. No "fixed" from a code change alone.

## Why it matters

"Healthy" just means the server is up — not that every call worked. The headline said 97% success while nearly half the Postgres calls were failing; the headline hid the failure because edge calls dominate the total. A red panel is not a chart to admire or explain — it is a thing that happened, a change of state, and the response is to fix the cause. And "fixed" is not a code change — it is the error count falling and a real action landing in the Ledger and moving the Dashboard number. That is the same law as the Dashboard itself: it has to WORK, not just be there.

## How to use it

When a panel goes red: pull the error log, name which calls are failing and why, fix the cause, then prove it by the numbers moving — the error count falling, a real action landing in the Ledger, the Dashboard number moving. Read the panels, not the headline: a healthy overall percentage can hide a failing subsystem. Never call it fixed from a code change alone.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
