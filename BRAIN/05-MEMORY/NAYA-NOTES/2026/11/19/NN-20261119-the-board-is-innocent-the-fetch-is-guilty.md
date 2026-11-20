# NN-20261119-the-board-is-innocent-the-fetch-is-guilty

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261119-the-board-is-innocent-the-fetch-is-guilty · Naya Note · 2026-11-19 ~17:19–17:28 MST (00:19–00:28Z 2026-11-20)**

*Paired Smart Note: SN-3964 — The Board Is Innocent, the Fetch Is Guilty*

**Category:** Verification — Proof

## What it is

The captain's eye on the Hub follow-up 12 staged link came back GOES BACK on the solo-note route. SN-3615 search + Open: the search finds it first, Open navigates correctly to `#/smart-notes/sn3615` — but the board NEVER renders: "Opening your note…" plus an empty board after ~25 seconds, and on direct load too, with no error. The fallback SN-2654 hangs the same way after 15+ seconds. But the counter-evidence clears the board: sn3380 clicked from its feed board opens instantly and renders cleanly — winged frame, N medallion, purple ball, dark tile, IN A NUTSHELL / Child / Grandma / What It Means, no void gap. Same board, two entries — one renders, one hangs — so the failure is the FETCH path for notes outside the loaded feed, not the board design. The live feed passes (new notes sn3883/sn3884/sn3380/sn3381 arrived live during the check), footer/Keep-reading passes, the greeting passes except it read "Good afternoon, Jordan" — the wrong name, source under investigation in fix-13. Follow-up 13 is dispatched with the solo-note fetch as the bullseye.

## Why it matters

Blaming the board would rebuild a working thing while the real fault — the fetch for notes outside the loaded feed — stays broken. The contrast is the diagnosis: find the entry that works and the entry that fails, and the fault is whatever differs between them. And a symptom without a proven source (the wrong name) stays an open question, not a claimed cause.

## How to use it

When a render fails, test the same board through a different entry before touching the design. If it renders one way and hangs another, fix the path. Hub follow-up 13 is the next proof of this law.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
