# SN-4504 — Fix It, Don't Just Explain It

**Category:** LAW — a red signal is a fix order, not an explanation prompt; fixed is proven by the numbers moving, never by a code change alone — 2026-11-21 ~10:27–10:29 MST

*Paired Naya Note: NN-20261121-we-gotta-fix-it-the-supabase-red-spike — the verbatim record of the Supabase red spike and the fix order, from his own screenshots.*

**Filed:** SN-4504 — Intelligence Loop run 469, 2026-11-21. His words from his own screenshots of the Supabase dashboard, as recorded in MEMORY.md from the same call; sent to the Dashboard mechanics coordinator (926c2517). Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

His screenshots of Supabase showed STATUS Healthy — and underneath it, POSTGRES 5,526 calls with 2,497 ERRORS, ~45% failing, red bars concentrated Nov 20 ~11am, tapering to green by Nov 21 morning. The headline said 97.0% success over 164,872 requests because edge calls (83,895, 0 errors) dominate the total. He read it right: "there's some kind of message in the screenshots that I don't understand. So there's been a change of state." And his order: "something happened and it doesn't look good. We gotta fix it." A red signal is a fix order, not an explanation prompt. "Fixed" is proven by the numbers moving — the error count falling, a real action landing in the Ledger, the Dashboard number moving — never by a code change alone.

## The Lesson

**FIX IT, DON'T JUST EXPLAIN IT (his order, 2026-11-21 ~10:29 MST):**

**"HEALTHY" MEANS THE SERVER IS UP — NOT THAT EVERY CALL WORKED.** The project page said Healthy, Nano, Canada Central, CPU 8% / Disk 24% / RAM 65% / 15 of 60 conns, last backup 7h ago. None of that is a lie — and none of it means the calls worked. Health is uptime; the panels are the truth. Read the panels, not the status word.

**THE HEADLINE CAN HIDE THE FAILURE.** 97.0% success over 164,872 requests sounds fine — until you read the panels: POSTGRES 5,526 calls, 2,497 errors, ~45% failing. Edge functions (83,895 calls, 0 errors) dominate the total and bury the Postgres failure in the average. A healthy overall percentage can hide a failing subsystem. Always read the panels, never the headline alone.

**A RED PANEL IS A THING THAT HAPPENED.** He saw it himself: "there's some kind of message in the screenshots that I don't understand. So there's been a change of state." The red bars concentrated Nov 20 ~11am, tapering to green by Nov 21 morning — something changed state, and the state change is the signal. A change of state is not a chart to admire; it is the machine telling you something broke.

**THE RESPONSE IS TO FIX THE CAUSE, NOT TO EXPLAIN THE CHART.** "Yeah, because something happened and it doesn't look good. We gotta fix it." Explaining why the bars are red is not the job. The job: pull the Postgres error log, name which calls are failing and why, fix the cause. The Dashboard mechanics coordinator (926c2517) has that job now.

**"FIXED" IS PROVEN BY THE NUMBERS MOVING.** No "fixed" from a code change alone. Fixed means the error count falls, a real action lands in the Ledger, and the Dashboard number moves. That is the same law as the Dashboard itself — it has to WORK, not just be there — applied to the fix. A fix nobody can see in the numbers is a claim, not a fix.

## Why It Matters

This is the proof standard applied to a live failure. The machine's job is to work — every page, every button, every call — and a red panel is the machine saying it is not working. If the response to red is an explanation, the red stays and the citizen's actions keep failing silently underneath a Healthy badge. If the response is a fix proven by the numbers, the machine gets measurably better every time something breaks. That is the difference between a system that looks healthy and a system that is healthy.

## How to Use It

When a panel goes red: pull the error log, name which calls are failing and why, fix the cause, then prove it by the numbers moving — the error count falling, a real action landing in the Ledger, the Dashboard number moving. Read the panels, not the headline: a healthy overall percentage can hide a failing subsystem. Never call it fixed from a code change alone.

## His Order, As Recorded

> "And then you can see there's some kind of message in the screenshots that I don't understand. So there's been a change of state."
>
> "Yeah, because something happened and it doesn't look good. We gotta fix it."

— his words, 2026-11-21 ~10:27–10:29 MST, as recorded in MEMORY.md.

## Owed from This Dictation

- The Postgres error FIX stays with the Dashboard mechanics round (coordinator 926c2517): pull the Postgres error log, name which calls are failing and why, fix the cause, prove it by the error count falling + a real action landing in the Ledger and moving the Dashboard number. Cause of the errors NOT in the screenshots — the error log is that round's job. Open until the numbers move.
- The state-change machinery he spotted is already there: triggers `items_state_changed` + `items_transition_log` fire + log on every item state change; `bookings_fill_owner` + `bookings_guard_slot` guard bookings. The inventory + alignment round (four-part bridge) maps them.
- The Dashboard Mechanics note (SN-4501) carries "it has to WORK, not just be there"; this note carries the same law applied to a live failure — fix it, and prove the fix in the numbers.
