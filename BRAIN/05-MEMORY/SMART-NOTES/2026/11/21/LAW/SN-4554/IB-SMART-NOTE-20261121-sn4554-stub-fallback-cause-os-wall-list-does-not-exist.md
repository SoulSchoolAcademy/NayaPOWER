# SN-4554 — The Stub Fallback Cause — #os-wall-list Does Not Exist

**Category:** LAW — fix the stub block only; the renderer works, the mount does not exist — 2026-11-21 ~12:41 MST

*Paired Naya Note: NN-20261121-stub-fallback-cause-os-wall-list-does-not-exist — the verbatim record of the stub-fallback diagnosis.*

**Filed:** SN-4554 — Intelligence Loop run 474, 2026-11-21. Diagnostic seat finding, ~12:41 MST, as recorded in the curated memory. Routed into the running Personal round (37e5034c) as an additional item — no second lane on the file.

## In a Nutshell

`fcStubInsert` returns false because `#os-wall-list` DOES NOT EXIST in the filed page (23 occurrences, all JS/CSS references, none defines the element). The feed renders via `mountHubFeed` into `#pcHubFeedMount`. The stub renderer itself works (returned true in isolation on the exact 5-photo payload) — it has nowhere to put the card. The 42501 block is separate and pre-existing. MINIMAL FIX (stub block only, lines 42526–42568): resolver returning `#os-wall-list` if present, else first `article.intel-board` parent in `#pcHubFeedMount`, else the mount; observer re-resolves per callback.

## The Lesson

**THE STUB FALLBACK CAUSE — #os-wall-list DOES NOT EXIST (diagnostic seat, 2026-11-21 ~12:41 MST):**

**THE RENDERER WORKS.** In isolation, on the exact 5-photo payload, the stub renderer returned true. The code that builds the card is fine.

**THE MOUNT DOES NOT EXIST.** `#os-wall-list` appears 23 times in the filed page — all JS/CSS references, none defines the element. There is nowhere to put the card. `fcStubInsert` returns false because its target is not there.

**THE FEED RENDERS ELSEWHERE.** The feed renders via `mountHubFeed` into `#pcHubFeedMount`. The stub was aimed at a mount the page does not have, while the real mount sits beside it.

**THE MINIMAL FIX (STUB BLOCK ONLY, LINES 42526–42568).** A resolver returning `#os-wall-list` if present, else the first `article.intel-board` parent in `#pcHubFeedMount`, else the mount; the observer re-resolves per callback. Stub block only — nothing else in the file moves.

**THE 42501 BLOCK IS SEPARATE.** It is pre-existing and untouched by this fix. Do not fold it in.

## Why It Matters

A working renderer that cannot find its mount looks exactly like a broken renderer — and a broken renderer gets rebuilt, which is how a page gets a second renderer while the first one was fine. Finding the cause before fixing is what keeps the fix minimal: one resolver, one block, no second lane, no rebuild of what already works. The lesson is the diagnostic habit itself — prove where the card goes before touching how the card is built.

## How to Use It

Fix the stub block only (lines 42526–42568) with the resolver above, routed into the running Personal round (37e5034c) — no second lane on the file. Leave the 42501 block alone. Report: `~/workspace/team-nitro/personal/post-note-fix-20261121/STUB-DIAGNOSIS-20261121.md`.

## His Words, As Recorded

> "`fcStubInsert` returns false because `#os-wall-list` DOES NOT EXIST in the filed page (23 occurrences, all JS/CSS references, none defines the element). The feed renders via `mountHubFeed` into `#pcHubFeedMount`."

— diagnostic seat finding, 2026-11-21 ~12:41 MST, as recorded in the curated memory.

## Owed from This Dictation

- Minimal fix in the stub block only (lines 42526–42568), resolver as above.
- Routed into the running Personal round (37e5034c) — no second lane.
- 42501 block separate and pre-existing — untouched.
