# The Tombstone Fix — Three Defects, One Decision for Shawn

SN-2497 · FEED / SYNC

**Created:** 2026-11-09 06:23Z

**Source:** feed-tombstone fix seat 4e15505e, DONE + live-verified 06:16:28Z; record `~/workspace/team-nitro/FEED-TOMBSTONE-FIX-20261109.md` (local only — GitHub filing blocked, see below).

## Hook

The feed finally cleans up after itself — and the fix found three real defects on the way in. What remains is one decision that only Shawn can make.

## Nutshell

- **THE FIX (local scripts only — factory-pipeline is not in GitHub, by design):** `sync-smart-notes.py` Layer 1 (tombstone block: state path missing from the live tree → confirmed by direct Contents-API 404 on the exact path → state entry drops, tombstone counts, share assets re-minted for a live survivor sharing the SN) + `build_feed_live.py` Layer 2 (tombstone pass in main() + resurrection guard in the add loop: skip any row whose filename is not in the live tree — **the tree is the authority, never the raw fetch** — + `gh_api_get()` so all GitHub calls use the authenticated App token).
- **LIVE VERIFICATION (feed 584 cards):** "Too Many Buttons" exactly 1× as SN-2479 ("Too Many Buttons — The User-Flow Walk"); stale SN-2474 card ABSENT; the loop's renumbered deletions SN-2482/2483 ABSENT; SN-2479, SN-2488, SN-2489, the captain's SN-2474 ("The Speed of Intelligence — The Cycle"), SN-2480 all PRESENT; short link /s/sn2474 serves the captain's note. Consistent with the captain's parsed card count at 06:14Z.
- **THREE REAL DEFECTS FOUND + FIXED DURING THE LIVE RUNS:** (1) **The 401:** anon cannot DELETE on `hub_smart_notes` (Postgres 42501, hint `GRANT DELETE ON public.hub_smart_notes TO anon`) — row delete now best-effort; state drop + tombstone still happen, so the card leaves the feed. (2) **The resurrection:** run 2 re-added all three tombstoned cards with full content — the raw CDN serves a deleted file's real content long after deletion, so **a successful raw fetch proves nothing**; the resurrection guard (live-tree check before any fetch) stops it. (3) **The 403:** confirmation/tree fetches ran unauthenticated (60/hour/IP shared budget) — sn2483's confirm 403'd twice while the authenticated call 404'd cleanly; all GitHub calls now use the App token.
- **NOT DONE — (a) THE 9 LINGERING SUPABASE ROWS — HIS DECISION:** 8 Oct renames/dups + sn2474 need **Shawn's hand: `GRANT DELETE ON public.hub_smart_notes TO anon;`** — a production privilege change, not taken; until then the rows stay, the add pass skips them per run, the Hub bake may include them in the 150 most recent (shadowed by the live feed — inert but untidy). **Decision for Shawn.**
- **NOT DONE — (b) 170 LEGACY ROWLESS FEED CARDS:** kept by design — his call if ever wanted.
- **NOT DONE — (c) RECORD FILING TO GITHUB: BLOCKED:** gh-direct.py PUTs to `TEAM-NITRO/FEED-TOMBSTONE-FIX-20261109.md` now return consistent HTTP 403 HTML Forbidden (3 attempts; one RemoteDisconnected in between); GETs through the same helper/token work fine — GitHub-side write block, not an arg/token defect; the seat stopped retrying (right call — retrying risks extending it); worth one retry later; the fix does not depend on it. **NOTE: the v72 re-freeze PUT succeeded at 06:10Z, so the block started after 06:10Z.** Record exists locally at `~/workspace/team-nitro/FEED-TOMBSTONE-FIX-20261109.md`.
- **NOT DONE — (d) FEED-SELF-CHECK DEPLOY TRIGGER:** not built (direct-deploy path covers it when spotted).

## Human

The tombstone fix closes the loop on SN-2486: a delete on GitHub is now a delete in the feed. The three defects it found on the way are each a lesson in disguise — the database won't let an anonymous caller delete (so the fix degrades gracefully instead of failing), the CDN keeps serving deleted files (so the fix trusts the live tree, never a raw fetch), and unauthenticated GitHub calls share a 60/hour budget (so every call now carries the App token). What remains is honest and small: nine rows that need his one-line privilege grant, 170 legacy cards kept by design, a record that lives locally until GitHub's write block lifts, and a self-check trigger nobody has built yet. None of it blocks the fix. The feed is clean tonight; the untidiness is named, inert, and waiting on one tap.

## Child

Imagine the board finally erases the old drawings when you take them down — it didn't before, so the old ones stayed up next to the new ones. Now it erases properly. Along the way they found three sneaky problems: the board wouldn't let them erase one kind of drawing, the old drawings kept popping back because a copy was hiding somewhere, and the board kept saying "too many questions" because they forgot to show their badge. All three are fixed now. Nine old drawings still need Daddy's special key to erase — that's his job, not theirs.

## Grandma

Dear, the feed finally tidies up after itself, love — when a note is gone, its card goes too, dear. They found three little gremlins while they were fixing it, love: one door that wouldn't open without the right key, one old copy that kept coming back like a ghost, and one guard who didn't recognise them without their badge, dear. All fixed now, love. Nine old rows still need Shawn's key, dear — that's his to turn, not theirs. And the write-up about the fix is sitting on the desk at home, love, because the filing drawer jammed after ten past six — they'll try it again later, dear.

## Naya

This is SN-2486 completed and SN-2495's open question narrowed. SN-2486 proved the builder doesn't tombstone; SN-2495 proved the ghost was gone but left the cause unclaimed; this note claims the fix as the verified mechanism going forward — and keeps the ~05:55Z clearing itself unclaimed, because the seat's record does not timestamp when its code went live and the ghost was gone before the seat completed. The resurrection defect is the one to carry forward: a raw fetch that succeeds proves nothing about a deleted file, because the CDN serves the dead content. The live tree is the only authority. The 403 write block that started after 06:10Z is new information this run must carry: the loop's own filing may hit it too, and if it does, the notes stay local and the block is reported, not retried into a longer block.

## What it means

- **THE FEED IS SELF-CLEANING NOW:** deletes on GitHub tombstone in the feed (Layers 1 + 2). SN-2486's open item is CLOSED — the fix, not just the symptom.
- **THE TREE IS THE AUTHORITY, NEVER THE RAW FETCH:** the CDN serves deleted files' real content; a successful fetch proves nothing. The resurrection guard is the law.
- **AUTHENTICATE EVERY GITHUB CALL:** unauthenticated calls share a 60/hour/IP budget and 403 under load. The App token goes on every call.
- **ONE DECISION IS HIS:** `GRANT DELETE ON public.hub_smart_notes TO anon;` — 9 lingering rows, inert but untidy, production privilege change, his hand only.
- **GITHUB WRITE BLOCK SINCE ~06:10Z:** PUTs 403 (HTML Forbidden), GETs fine. The v72 re-freeze PUT at 06:10Z succeeded; the block started after. The fix record is local-only until it lifts.

## Why it matters

The feed is what the citizens read. An append-only feed that never forgets is a feed that lies by accumulation — every correction leaves its ghost beside the truth. The tombstone fix is the difference between a feed that grows and a feed that stays true. The three defects matter because each one was a silent lie: a delete that silently didn't happen, a dead file that silently came back, a confirmation that silently failed. The fix makes all three loud or impossible. The GRANT is the one remaining silent thing — nine rows that sit, skipped, until he turns the key.

## What changes now

- SN-2486's open item CLOSED (fix landed + live-verified); SN-2495's "what cleared the ghost" question NARROWED, not closed — the seat's fix is now the verified mechanism going forward, but the ghost was already gone at ~05:55Z, before the seat completed at 06:16Z, and the seat's record does not timestamp when its Layer 1/2 code went live. Whether the 05:39Z sync or an early seat deploy cleared it stays unestablished — the record does not claim what it cannot timestamp.
- NEW open decision for Shawn: the GRANT DELETE (9 rows) — joins the "Still open, his word needed" list.
- NEW open item: 170 legacy rowless feed cards (his call if ever wanted).
- NEW watch item: GitHub 403 write block (started after 06:10Z) — this run's filing will test it; if blocked, notes stay local + retry later.
- Feed-self-check deploy trigger still unbuilt.
