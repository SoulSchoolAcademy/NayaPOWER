# NN-20261118-bytes-pass-frame-never-paints

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261118-bytes-pass-frame-never-paints · Naya Note · 2026-11-18 ~21:2x MST (04:19–04:28Z 2026-11-19)**

*Paired Smart Note: SN-3630 — Bytes Can Pass While the Frame Never Paints — Diagnose First*

**Category:** System — Verification

## What it is

Hub follow-on fix round 2 came back with a checker verdict of HELD: byte PASS — the diff was exactly 8 opcodes / 23 lines, all inside the three fixes; the laws delta was zero; the staged URL curled twice with fresh `t=` and sha-matched both times. Yet the captain's cloud-browser eye on those same staged bytes, at 1920×998, found the gold kingdom frame does NOT paint — the top edge solid plain black across the full width, the bottom edge likewise plain black, no gold at any corner, only thin purple dividers at the sidebar edges. The only winged frame visible was INSIDE the feed articles, around the note cards — a card frame, not the page frame. No fold sequence, band paint, or screenshot existed from the checker, because both VM browsers were dead in the window. The round must NOT go to Shawn until a render re-probe lands. Fix round 3 was dispatched with exactly one defect and one rule: diagnose first, then fix — do the band elements exist in the rendered DOM? does the background-image compute? is something covering the bands? is the 2.2 MB data URI failing to load? — do NOT re-apply the same change and hope.

## Why it matters

Bytes are the filing, not the experience. A fix can be byte-perfect and still never paint, and a checker that only reads bytes will pass a page Shawn's eye fails in one look. The verdict HELD is the system working as designed: the bytes said pass, the render said fail, and the render wins. And the fix round's rule is the lesson in one line — diagnose the cause before touching the code again, or the same change gets re-applied and the same failure comes back.

## How to use it

A round is never called done on bytes alone: the render re-probe is part of done, and a verdict of HELD means the bytes passed and the experience did not. When a fix fails in render, the next round diagnoses first — DOM, computed style, covering elements, asset loading — and names the cause before any code changes. Never re-apply the same change and hope.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
