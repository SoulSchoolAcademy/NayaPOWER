# Living Intel — The Heartbeat of It All — Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` @ HEAD (worktree, unpushed). Director brief:
"like these (Today/Reports/Connect previews) but Living Intel — the heartbeat
of it all. Major feature. Showstopper." Lane check on #554: CLEAR, no other
lane in-flight.

## Score: 9.5/10 — current

| # | Lens | Score | Note |
|---|------|-------|------|
| 1 | Effectiveness | 9.5 | One living stream unifies 4 sources (~55 items): 6 real reports, 8 real smart notes, 9 real doors from the registry, labeled ledger demo stream. Filters (ALL/INTEL/ACTIONS/CONNECTIONS) + source jewels all filter for real; every board opens its heartbeat modal with real numbers or a plain-words explanation; time-ago stamps tick live every 30s; sim-live beats arrive on their own, counters tick, spectrum reindexes. |
| 2 | Quality | 9.5 | Showstopper hero: spectrum EKG with traveling pulse, breathing glow, LIVE dot, real stats. Glowing DEMO chips, near-white time stamps, staggered card entrances, breathing flow accents. No dead controls. |
| 3 | Pro level | 9.3 | Modal is keyboard-complete: role=dialog, aria-modal, Tab focus trap, Escape + backdrop close, focus restored to the opening card. Filter tabs carry aria-pressed. `prefers-reduced-motion` kills all animation on `.li-stage`. |
| 4 | Contrast | 9.6 | Deep black glass, top-light catches, deep shadows, hover lift with identity-color ignition. Buttons are obsidian black (never grey); identity color ignites on hover/focus; rest stays white/silver whisper. |
| 5 | Clarity | 9.4 | Kicker, stats, and labels read instantly. Empty state is filter-aware ("No ACTIONS beats in this view — switch to ALL"). SIMULATED LIVE pill states the demo contract in plain words. |
| 6 | Congruency | 9.6 | One visual family: silver-white at rest, flow color ignites on highlight. Spectrum flows purple→…→magenta→again continuously; the foot states the flow verbatim; boards breathe in staggered accents. |
| 7 | Color | 9.7 | Color = stable source identity (INTEL REPORTS sky, SMART NOTES violet, LEDGER gold, CONNECT indigo; each door keeps its registry color/jewel). Stream position assigns only the spectrum flow, never identity. |

## Why not 10

- **-0.3 — the ledger stream is demo-fed.** Real reports, notes, and doors are
  real; the beating stream is labeled demo until the shell wires the production
  ledger read path (protected-gate work, needs Shawn's explicit word; launch is
  a `simLive:false` flag flip — the room does not care which store feeds it).
- **-0.2 — Shawn's visual sign-off.** He has not seen this room's final pass
  yet. No score reaches 10 without his eyes.

## Verification

- `node --check`: `living-intel.js`, `living-intel-adapter.js`, and the smoke
  suite all parse clean. CSS brace balance checked (balanced).
- `HUB/app/preview/tests/living-intel-smoke.js`: **41 pass, 0 fail** — adapter
  build/sort/demo flags, flow-color-by-position, DEMO chips on demo items only,
  all four filters + jewels, card keyboard open (Enter), modal open/Escape/
  backdrop close, focus trap + focus restore, filter-aware empty state, hero
  stats, simLive pill hidden when off, and the drilled-law CSS markers
  (reduced-motion kill switch on `.li-stage`, obsidian button gradient, no
  sub-11px label type).
- Screenshot verification: built
  `~/workspace/your_files/living-intel-preview.html` via
  `build-living-intel-preview.py`, captured with headless Chrome
  (`--virtual-time-budget=4000`), viewed both before and after the fix pass:
  hero EKG, jewels, filters, stream cards, DEMO chips, SIMULATED LIVE pill all
  confirmed by eye.
- Honesty: every simulated item carries a DEMO chip; the SIMULATED LIVE pill
  says "demo beats arriving · flips to the real stream at launch". Nothing is
  presented as live that is not.
