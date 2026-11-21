# SN-4505 — The Four-Part Bridge — Flow Like Water

**Category:** LAW — the four-part bridge (GitHub, Supabase, Cloudflare, NayaNET) must flow flawlessly, like water; Supabase is the engine; never rebuild what already exists; use what we didn't realize we had — 2026-11-21 ~10:32 MST

*Paired Naya Note: NN-20261121-the-four-part-bridge-flow-like-water — the verbatim record of the standing order and the starting evidence from his screenshots.*

**Filed:** SN-4505 — Intelligence Loop run 469, 2026-11-21. His standing order, as recorded in MEMORY.md from the same call; a read-only inventory + alignment coordinator is dispatched. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

"There's GitHub, there's Supabase, there's Cloudflare, and NayaNET — the bridge all together working for the flow, and that whole flow needs to be flawless, like flow like water." Supabase is the ENGINE — everything goes through there. He feels I don't see the whole picture of the puzzle: I must understand everything in Supabase, how it functions, how it relates to what we're building; make sure everything is aligned and working; NOT rebuild anything that already exists; utilize stuff we didn't realize we had. The round dispatched is read-only inventory + alignment: edge functions first, then all database functions / tables / triggers / policies; map each piece to wired / built-but-unused / missing; trace the bridge end to end; name rebuilds and unused pieces. The Postgres error FIX stays with the Dashboard round — this round maps only.

## The Lesson

**THE FOUR-PART BRIDGE — FLOW LIKE WATER (his standing order, 2026-11-21 ~10:32 MST):**

**ONE FLOW, FOUR PARTS.** GitHub, Supabase, Cloudflare, NayaNET — the bridge all together working for the flow. Not four systems that happen to touch; one flow, and the whole flow has to be flawless, like water. A break anywhere in the bridge breaks the flow everywhere downstream. The standard is not "each part works" — it is "the flow is flawless."

**SUPABASE IS THE ENGINE.** Everything goes through there. That is why the picture matters most there: if I don't understand everything in Supabase — how it functions, how it relates to what we're building — I don't see the whole picture of the puzzle, and I work blind on the part everything flows through.

**MAP BEFORE BUILDING — NEVER REBUILD WHAT ALREADY EXISTS.** The inventory round maps first: edge functions first, then all database functions / tables / triggers / policies; each piece marked wired / built-but-unused / missing; the bridge traced end to end; rebuilds and unused pieces named. Rebuilding a piece that already exists is waste — the redo cycle he named this morning ("they're just redoing and redoing and redoing"). The map is what stops the redo.

**UTILIZE STUFF WE DIDN'T REALIZE WE HAD.** Built-but-unused is the other half of the map. The screenshots already show it: the GitHub bridge (nayanet-github-dispatch, nayanet-github-webhook, nayanet-github-build-dispatch) and the invite leg (nayanet-invite-sender) are live in Supabase; the state-change triggers (`items_state_changed`, `items_transition_log`) already fire and log every state change; `bookings_fill_owner` and `bookings_guard_slot` already guard bookings. Pieces built and sitting unused are value already paid for — the map surfaces them so they get used.

**MAP AND FIX STAY SEPARATE.** The Postgres error FIX stays with the Dashboard round; this round maps only. Mapping names what is broken; fixing fixes it. The two jobs run in parallel, neither waits on the other, and neither claims the other's result.

## Why It Matters

This is the harvest law applied to the whole system: take what already exists, use it, and build only what's missing. A Naya who doesn't see the whole picture rebuilds the engine piece by piece while the built pieces sit unused — and every rebuild is a redo, and every redo is the failure he named. The map — every piece marked wired, built-but-unused, or missing, the bridge traced end to end — is the picture. Once the picture is true, the building is only what's missing, and the flow runs like water.

## How to Use It

Map before building: edge functions first, then database functions / tables / triggers / policies; every piece marked wired, built-but-unused, or missing; the GitHub↔Supabase↔Cloudflare↔NayaNET bridge traced end to end; rebuilds and unused pieces named. Never rebuild what already exists. Utilize stuff we didn't realize we had. Keep the map round and the fix round separate — the map names, the fix fixes.

## His Order, As Recorded

> "there's GitHub, there's Supabase, there's Cloudflare, and NayaNET — the bridge all together working for the flow, and that whole flow needs to be flawless, like flow like water."

— his words, 2026-11-21 ~10:32 MST, as recorded in MEMORY.md.

## Owed from This Dictation

- INVENTORY + ALIGNMENT ROUND DISPATCHED (read-only coordinator): edge functions first, then all database functions / tables / triggers / policies; map each piece to wired / built-but-unused / missing; trace the GitHub↔Supabase↔Cloudflare↔NayaNET bridge end to end; name rebuilds and unused pieces. The Postgres error FIX stays with the Dashboard round — this round maps only.
- STARTING EVIDENCE, first-hand from his screenshots (~10:33 MST): 12 edge functions visible on the first screen (list may scroll further) — naya-decision-context (17 deploys), naya-dream-replay (18), nayanet-act-runtime (72), nayanet-causal-learning-experiment (91), nayanet-causal-verify (89), nayanet-cold-runtime-proof (137), nayanet-github-build-dispatch (17), nayanet-github-dispatch (43), nayanet-github-webhook (16), nayanet-intelligence-commit-runtime (89), nayanet-intelligence-retrieve (11 days ago, 1 deploy — newest, least-proven), nayanet-invite-sender (6). Edge layer clean: 83,895 calls, 0 errors in 24h — the failures are Postgres-side. Passed to the inventory coordinator.
- The Fix It note (SN-4504) carries the fix order for the red spike; this note carries the map order for the whole bridge. The Turning Point note (SN-4506) carries the phase change both serve.
