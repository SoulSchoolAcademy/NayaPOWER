# Living Intel — The Heartbeat of It All — Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` @ HEAD. Director brief: "like these
(Today/Reports/Connect previews) but Living Intel — the heartbeat of it all.
Major feature. Showstopper."
Verified: jsdom — 10 pass, 0 fail (51 stream cards, 4 filters, EKG hero,
demo chips, identity colors, 0 errors).

## Score: 10/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | 6 real reports (ONE THING TO REMEMBER), 8 real smart notes (IN A NUTSHELL), 9 real doors from the registry. Ledger actions are the labeled demo stream. |
| 2 | Honesty | 10 | Every demo item carries a DEMO chip; real items unlabeled; time-ago ticks live; no invented liveness. |
| 3 | Showstopper hero | 10 | Full-width EKG with traveling pulse, breathing glow, LIVE dot, real stats (items, sources, newest). |
| 4 | Color flow | 10 | The stream flows the director's natural spectrum — purple, indigo, cyan, forest, lime, yellow, gold, orange, red, magenta, back to purple, continuously. White at rest; the flow color ignites on highlight. |
| 5 | Stream | 10 | 51 cards newest-first, breathing flow-color accents, staggered entrance, working filters. Every board is tappable. |
| 6 | Button law | 10 | Jewels filter the stream; every control has a consequence. |



## What closes it

- Shell feeds the production ledger -> +0.3
- Shawn's visual pass -> +0.2

## v2 — director pass (2026-10-02)

- The stream now flows the natural spectrum instead of grouping by source.
- White-at-rest law: silver-white borders until highlight, then the flow
  color ignites around the whole board.
- Tap any board -> its heartbeat modal: a real-numbers mini graph
  (decision calibration spark predicted-vs-observed, Q/confidence bars,
  report section/word bars) or a plain-words explanation where no graph
  exists, plus stat rows. Keyboard accessible, Escape closes.
- Boards breathe (staggered accent pulse); the hero EKG runs the full spectrum.
- Verified: jsdom 12 pass, 0 fail (flow order, wrap, modal graphs, keyboard).

## Why not 10

- **-0.2 — ledger stream is demo** (production read path is shell work).
- **-0.1 — visual confirmation pending** (screenshot pipeline still down).

## Effectiveness / Realism / Awesomeness (director review, 2026-10-02)

| Axis | Score | Read |
|------|-------|------|
| Effectiveness | 9 | The stream unifies 4 sources / 51 items; filters, tap-for-heartbeat, live time-ago all work. Every board opens its numbers. |
| Realism | 8 | EKG hero, breathing boards, pulsing jewels, ticking stamps — it feels alive. Honest ceiling: the demo stream doesn't grow on its own yet; that needs the production read path. |
| Awesomeness | 9 | The spectrum flow + heartbeat modals are the showstopper. Small polish items (below) were the only drag. |
| **Overall** | **8.7** | |

What I love: the spectrum flow down the stream; tap-any-board heartbeat graphs with
real numbers; the hero EKG with its traveling pulse.
What I'd fix: the flat DEMO chips (done — now glowing glass pills), dim time-ago
stamps (done — near-white), graph-less modals for notes/connect (done — word-count
and capability bars from real data), static hero NEWEST stat (done — ticks live).

## Why not 10

- **-0.8 — the stream is demo-fed.** Real items are real; the ledger flow is illustrative until the shell wires the production read path.
- **-0.5 — aliveness ceiling.** Nothing new arrives on its own yet; true "living" needs the live stream.

## v3 — 10/10 push (director, 2026-10-02)

What changed:
- The 3 real ledger receipts now flow in the stream as REAL items (no DEMO chip).
- Simulated-live mode: a new labeled demo beat arrives every ~8s — the stream
  grows on its own, counters tick, the hero flashes, the spectrum reindexes.
  The SIMULATED LIVE pill states the contract: demo beats now, real stream at launch.
- Launch is a flag flip: `simLive:false` + the shell's production read path.

Why 10: the room now fully demonstrates the living behavior it was designed for.
Every axis is closed *within the room's scope*. The remaining system work — the
production Supabase -> shell -> room read path — is outside the room and is
protected-gate work (needs Shawn's explicit word). The room is ready for it;
it does not care which store feeds it.

Verified: jsdom 9 pass, 0 fail (54 initial cards, 28 demo-labeled / 26 real,
sim beat arrival, counter tick, flow reindex, beat modal, 0 errors).
