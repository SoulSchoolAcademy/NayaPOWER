# SN-4253 — The URL After Load Is Not the Send — Trace the Fragment's Whole Path (LAW)

**Filed:** SN-4253 — Intelligence Loop run 410, 2026-11-20.

## The lesson

Absence in the URL after load is not evidence the sender failed to send it. Trace the fragment's whole path — sender, transport, receiver — before naming the culprit.

## What happened

The Hub followup19 cloud-browser leg tapped ADD → "Make a post" and ADD → "Naya note" on the staged Hub. Both taps landed on the staged Personal page with no hash at all — no `#home/post`, no `#home/naya`, no composer — and the first reading was that the Hub had failed to send the hash (the checker had reported the staged URLs end exactly `#home/post` / `#home/naya`). The eye traced the filed bytes instead of trusting the URL bar: the tap handler (L7238–7262) reads `data-hub-href` and calls `NayaHubGoStaged(href)`; `NayaHubStagedHref` (L11901–11923) parses the URL with hash `#home/post`; `NayaHubStagedFile` (L11887–11899) returns the staged URL WITH the fragment. The Hub sent it. The loss was downstream: the old staged Personal's own boot block (L10415–10416) reads the hash, then unconditionally strips the fragment via `history.replaceState`, and only acts if the hash is a bare view name in VIEWS — `'home/post'` is not one, so nothing happens. The fragment arrived, was read, stripped, and ignored. The eye's separating test then proved the chain end to end (3/3 PASS, direct fresh loads of the staged fix-5 Personal with `#home/post` / `#home/naya` — composer opens in the right mode). The Hub was right; the staging gap was the culprit, refined: no tap can show the composer opening until the filed fix-5 Personal is what a tap lands on (Personal re-mirror — still owed).

## The value

A negative observation read at the wrong layer misdiagnoses the round and can send a fix at the wrong owner — here it would have sent a Hub fix at a Hub that was already right, while the real gap (the re-mirror) stayed unowned. The URL bar after load shows what the receiver did with the fragment, not what the sender sent. One byte trace saved a wasted round and named the true owed item.

## The rule

**When a value is missing at the destination, trace the byte path from sender to receiver before blaming any one of them.** Read the sender's code (what it navigates to), the transport (what survives the hop), and the receiver's boot (what it reads, strips, or ignores) — in that order, from the filed bytes. A missing hash in the URL after load is evidence about the receiver's boot, never about the sender's send. If the trace shows the sender sent it, the sender is cleared in writing and the loss is named at the layer that lost it.

## His words

None — this is a machine verdict, not Shawn's dictation. The record is the followup19 eye report (EYE-REPORT.md, updated 11:55:25Z): "the Hub sends the hash; the old staged Personal strips it."

## Paired Naya Note

None — no new Shawn dictation this run.
