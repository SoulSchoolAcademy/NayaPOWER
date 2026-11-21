# NN-20261121-stub-fallback-cause-os-wall-list-does-not-exist

**Written by Naya for Shawn — Founder / Creator of NayaNET**

**NN-20261121-stub-fallback-cause-os-wall-list-does-not-exist · Naya Note · 2026-11-21 ~12:41 MST**

*Paired Smart Note: SN-4554 — The Stub Fallback Cause — #os-wall-list Does Not Exist*

**Category:** LAW — fix the stub block only; the renderer works, the mount does not exist

**Status:** Written in run 474. Diagnostic seat finding, ~12:41 MST, as recorded in the curated memory. Routed into the running Personal round (37e5034c) as an additional item — no second lane on the file.

## What it is

**THE STUB FALLBACK CAUSE — #os-wall-list DOES NOT EXIST (diagnostic seat, 2026-11-21 ~12:41 MST):** `fcStubInsert` returns false because `#os-wall-list` DOES NOT EXIST in the filed page (23 occurrences, all JS/CSS references, none defines the element). The feed renders via `mountHubFeed` into `#pcHubFeedMount`. The stub renderer itself works (returned true in isolation on the exact 5-photo payload) — it has nowhere to put the card. The 42501 block is separate and pre-existing. MINIMAL FIX (stub block only, lines 42526–42568): resolver returning `#os-wall-list` if present, else first `article.intel-board` parent in `#pcHubFeedMount`, else the mount; observer re-resolves per callback. Report: `~/workspace/team-nitro/personal/post-note-fix-20261121/STUB-DIAGNOSIS-20261121.md`.

## Why it matters

A working renderer that cannot find its mount looks exactly like a broken renderer — and a broken renderer gets rebuilt, which is how a page gets a second renderer while the first one was fine. Finding the cause before fixing is what keeps the fix minimal: one resolver, one block, no second lane, no rebuild of what already works. The lesson is the diagnostic habit itself — prove where the card goes before touching how the card is built.

## How to use it

Fix the stub block only (lines 42526–42568) with the resolver above, routed into the running Personal round (37e5034c) — no second lane on the file. Leave the 42501 block alone.

---

**Written by Naya for Shawn — Founder / Creator of NayaNET.**
