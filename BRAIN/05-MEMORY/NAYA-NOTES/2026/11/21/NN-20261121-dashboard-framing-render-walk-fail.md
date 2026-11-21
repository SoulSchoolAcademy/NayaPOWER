# NN-20261121-dashboard-framing-render-walk-fail

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-dashboard-framing-render-walk-fail · Naya Note · 2026-11-21 ~13:29 MST**

*Paired Smart Note: SN-4576 — Dashboard Framing Render Walk — Overall Fail*

**Category:** DASHBOARD — the framing render walk

**Status:** Written in run 475. Cloud browser, 2026-11-21 13:21–13:29 MST, 1920px + 621px, task `500cc9c7`, as recorded in the curated memory. Lane `~/workspace/team-nitro/dashboard/render-fix-20261121/`.

## What it is

**DASHBOARD FRAMING RENDER WALK — OVERALL FAIL (cloud browser, 2026-11-21 13:21–13:29 MST, 1920px + 621px, task `500cc9c7`).** The staged page loads but its JavaScript templates render as visible page text (~400,600 characters of source — function definitions, `'+esc(...)+'` fragments, the ledger-mechanics module comment — as page content), the score gauge sticks on "Reading…", and the page runs ~66,890px tall through the code wall. Day/Week/Month tabs dead (All stays selected, score stays 44%); the ten drill orbs show the literal label `'+o.label+'`; "Copy the link" copies a literal template string; "Open it" jumps to #notes; the joinus link lands on /welcome; "See every link" only scrolls; floating toggles overlap and cover sidebar links; sidebar rooms blank/unclickable at 621px; Smart Links LIVE figures all "–"; "heartbeat not served yet". PASS parts: no h-overflow, free scroll, some boards genuinely framed with headlines leading, Smart Link explainer expands, bar show/hide works, Intel Today + Reports land right, bottom bar = the six as filed (icons only, no text labels).

**ROOT CAUSE IS IN THE MECHANICS BASE, NOT THE FRAMING CSS** (framing added CSS only, +375/−0) — the templates were already not rendering.

**FIX ROUND DISPATCHED (~13:29 MST):** diagnose the leak from the filed bytes first (name the exact block), fix at the source, fold in the bar-alignment (MAIL/ACTIVITY) + "Earnings Per Click" relabel (same page, one list), checker verifies, render walk re-runs from my side.

## Why it matters

The framing round was complete on bytes and the walk still failed overall — because the failure was underneath it: the mechanics base renders its own templates as page text, so the page a citizen sees is a wall of code 66,890px tall. The framing did its job; the base did not. The fix round starts by naming the exact leaking block from the filed bytes, then fixes at the source — and folds in the two decisions owed (bar-alignment, "Earnings Per Click" relabel) on the same page, one list, instead of a second round.

## How to use it

Diagnose from the filed bytes first — name the exact block that leaks. Fix at the source, not over it. Bar-alignment (MAIL/ACTIVITY) and the "Earnings Per Click" relabel ride the same round. Checker verifies, render walk re-runs. Not cleared for Shawn's eye until the walk passes.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
