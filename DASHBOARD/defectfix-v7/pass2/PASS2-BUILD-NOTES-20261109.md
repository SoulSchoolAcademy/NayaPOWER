# Dashboard done-done pass-2 — BUILD NOTES (builder seat, 2026-11-09)

Branch: `dashboard/done-done-pass2-20261109`. Base: the live hero-fix page
(`hero-fix-deploy-source.html`, 1,695,318B, sha256 `124aa4176c…`), never fix-9, never fresh.
Built page: `DASHBOARD/defectfix-v7/pass2/dashboard-pass2.html` (1,702,517B local;
sha256 `38c2c492…` at filing — re-verify after any later edit).
Activation: all five §1 files read 2026-11-09 ~17:49Z before any design work.

## Applied-laws table

| Law read | Quoted (short, verbatim) | Part it produced in this build |
|----------|--------------------------|--------------------------------|
| Playbook Truth 2 | "Every element is a physical object with material, weight, and a light source." | Both new boards: harvested `.ph-card` obsidian glass, 135° gradient, shadow down-right; jewel lit in the board's own color |
| Playbook Truth 1 | "Every position is calculated by formula. Never eyeballed." | Board colors placed by the spectrum walk, not by eye: headliner purple (0) → Smart Links indigo (1) → Reports blue #3fb8ff (2) → What Naya Does green #2fe89e (3) |
| Playbook rule 10 | "Harvest, don't invent." | Zero new CSS. Boards use `.ph-card` + `.os-jewel` verbatim from fix9-work.html; the only adaptation is the outer element being an `<a>` (display:block) so the whole board is the door |
| Playbook, Color | "Color ignites on touch, in the element's OWN color only." | No `.ph-nutshell` box on the new boards (its gold is hardcoded) — nutshells are plain white text; hover ignites blue/green via the harvested `.ph-card:hover` rules that use `var(--ac)` |
| Intelligence Report | "Physical is not a style. It's a requirement." / "Don't touch unasked." | Diff is purely additive (124 lines) except one replaced guard line; hero, numbers, gauge math untouched |
| Intelligent Block Rules L4 | "every object owns ONE spectrum color. Its identity." | Reports owns blue #3fb8ff; What Naya Does owns green #2fe89e; jewels carry the same color |
| Intelligent Block Rules L6 / D4 | "Every number is a door. Tap it, it opens its records." | Both boards are doors: the whole board is the link to its destination |
| Clarity Act §2a gate 5 | "Can I prove it? … Receipt before report." | Acts-gap list marks 1/10 PROVEN, 9 NOT YET; the ledger-hop proof is left to the verifier as PROVEN / NOT PROVEN, never assumed |
| Clarity Act §3m forbidden 7 | "Light backgrounds. Zero white or light surfaces, ever." | Gate (a) PASS: 0 light surfaces; base canvas #050607 |
| Naya Brand, Buttons | "Every button is a real object: elevated, deep, lit, with real lift and real light." | Boards lift on hover (translateY(-4px)) and ignite in own color; no flat button added |

## Design-contract gate measurements (checker `check-gate.py`, this file)

- (a) Zero white/light backgrounds — PASS (solid_light_surfaces=0, light_gradient_surfaces=0; base canvas #050607).
- (b) Every element raised/elevated — PASS (299/324 with depth, ratio 0.923; the 25 without depth are pre-existing orb/stage containers, none added by this build).
- (c) Gauges/numbers alive — PASS (#tn-tacho-mount in DOM, needle-law gauge present, 4 gear-tooth occurrences, 35 tiled digits).
- (d) No text-in-image, no pasted document — PASS (0 hits; 1 img is a data-URI payload, no text signal).
- (e) No bare text blocks — PASS (56 substantial blocks, 0 bare, ratio 1.0).
- (f) No look-alike — PASS (0 lookalike buttons; every element traces to `.ph-card` / `.os-jewel` harvest sources or an id/data-* address).
- (g) `##` sections — PASS (this file and the acts-gap list use real `##` sections).
- (h) No dictation-blunt phrases — PASS (0 banned phrases; the word "blockchain" appears nowhere).
- (i) Title+subtitle+nutshell — PASS for the two new boards (each carries title + subtitle + nutshell, all non-empty); story-board check N/A (no `.calc-story-card` on this page). No faces on the new boards, so no alternation question arises.
- OVERALL from the checker: PASS — MACHINE ONLY, HUMAN CHECKS PENDING.

## L1–L7

- L1 Stranger test — PASS (board by board): Reports — she asks "what is a daily intelligence report?"; answered in the nutshell ("what you learned, what moved, and what it means… every day openable"). What Naya Does — she asks "what does Naya actually do for me?"; answered ("See everything she can do — your reports, your notes, your pages, your lists, your stats") and the board opens the full definition.
- L2 Perfect-words law — PASS: public copy is crafted in her voice; the old/new internet contrast is rewritten, not pasted from dictation; no process talk or stage directions on the page.
- L3 Title + subtitle + nutshell — PASS: both boards carry all three, each non-empty.
- L4 Naya speaks, faces alternate — N/A: no faces on the new boards (no face invented, no face repeated).
- L5 Test in his head — PASS (attested in H4 below).
- L6 `##` sections — PASS: acts-gap list and this file use `##` sections throughout.
- L7 One ultimate ten — PASS for the acts-gap list: one set of ten acts, each named once with verdict + evidence + missing; no second set.

## H1–H5 (builder attestation; Shawn's eye is the final gate)

- H1 Stranger test — PASS (see L1).
- H2 Perfect-words law — PASS (see L2).
- H3 Face quality — N/A (no faces added).
- H4 Test in his head — PASS: 10-star service? The Reports board puts a daily report one tap away; the What-Naya-Does board answers the first question a stranger asks. Obvious? Both boards say what they open and open it. Useful? Yes — reports and the definition were both hard to find before. Awesome? The boards are the one board design, in sequence, lit in their own colors.
- H5 One ultimate ten — PASS (see L7).

## What changed (diff vs base — additive only, one replaced line)

1. Two boards after the Smart Links board closes: Reports (blue #3fb8ff, opens
   `https://nayanet.app/rooms/reports`) and What Naya Does (green #2fe89e, opens
   `https://nayanet.live/s/sn2532`). Whole board is the door.
2. Ledger spine: `window._osTrackBoardOpen` + delegated click handler. Clicks write
   `smart_notes` rows with `k:'board-open'` (board + destination + time) through the
   page's own Supabase client — the same pattern as the existing `k:'connect'` /
   `k:'save'` event rows. Navigation waits for the write or a 600ms timeout,
   whichever first; with no connection the link navigates immediately. The row is
   invisible to the score and to notes/wall renders (spine counts only k-filtered
   arrays: `k==='wall'`, `k==='note'`, `k==='save'`). `window.loadPointsBoard` and
   `supabase-ready` preserved (grep-verified). NO sync claim added anywhere.
3. Orb-mini race (item 5): root cause found — the hero orb nodes render DURING PARSE
   (head poll calls `loadPointsBoard()` as soon as it exists) but TnTacho and
   `_upgradeOrbNodes` are defined in a LATER script; the call sites guard on
   `typeof window._upgradeOrbNodes === 'function'` and silently skip, the head poll
   then sees children in `#os-ld-nodes` and stops, and nothing re-sweeps unless a
   Supabase re-render happens — hence intermittent 0/9 vs 9/9. Fix: `_upgradeOrbNodes`
   now queues renders that arrive before TnTacho (retry every 100ms, max 50 tries)
   instead of dropping them; immediately after its definition the build sweeps every
   `.os-ld-node` already in the document and installs a MutationObserver (childList +
   subtree on `document.body`) so every node rendered later upgrades ON RENDER.
   Idempotent via `data-mini`. No hero change, no new gauge, no number/gauge-math change.
4. The single replaced line in the whole diff: the old silent-return guard in
   `_upgradeOrbNodes` (`if (!box || !window.TnTacho || !TnTacho.mountMini) return;`).

## Verification the builder ran

- All 18 inline `<script>` blocks pass `node --check` (0 failures).
- Design-contract gate: OVERALL PASS — MACHINE ONLY (see above).
- `diff` vs base: 124 lines, all in the three insertions above, except the one guard line.
- HTTP (curl, this VM, 2026-11-09): all 18 Dashboard-linked pages 200 (see
  `PAGES-18-HTTP-20261109.md`); `nayanet.live/s/sn2532` returns 000 from curl here
  (VM-egress limitation, not a verdict — real-browser check required).
- SN-2532 read from main (blob `4f6f4e5a`, 14,199B); acts-gap list written with
  1 PROVEN / 9 NOT YET (see `ACTS-GAP-LIST-SN2532-20261109.md`).

## DONE

- (1) Reports board built, in the one design, in sequence, click opens the Reports room.
- (2) Ledger spine: tracking wiring preserved, both new boards wired through the same
  ledger; no unproven sync claim; DEMO labeling untouched.
- (3) 18 pages: no link changed; HTTP table written for the verifier.
- (4) What-Naya-Does board built + acts-gap list file written (ten acts, verdicts).
- (5) Orb-mini upgrade deterministic on node render (sweep + observer + queued retry).
- Built page + gap list + 18-page table + these notes filed to GitHub branch
  `dashboard/done-done-pass2-20261109` via `gh-direct.py`, one write at a time,
  read-back verified. No deploys, no merges, no PRs.

## NOT DONE (for the verifier / coordinator — not hidden, not deferred as passes)

- Live-browser verification: screenshots 1440/390/360, scroll 0 + scrolled, both boards
  clicked to their destinations, zero console errors, zero overflow, hero items (a)–(u)
  still passing, 5 fresh loads at 390 + 5 at 1440 each showing 9/9 orb-mini mounts
  within 1s. (Builder has no live browser; the verifier does this.)
- Ledger-hop proof, hop by hop, PROVEN / NOT PROVEN: (hop 1) a real click moves a
  Dashboard stat; (hop 2) the Smart Ledger room shows the event; (hop 3) the Dashboard
  reads the ledger's answer. The board-open write is the mechanism; whether it lands
  in the ledger and surfaces in Dashboard stats is UNPROVEN until the verifier tests it
  live. The worker → Supabase write hop was already UNVERIFIED (pricing audit 17:48Z).
- The 18-page table's Renders / Works / Tracked columns (verifier's live clicks).
- `nayanet.live/s/sn2532` from a real browser (curl 000 here is a VM limit).
- Deploy to worker `naya-model-dashboard` (coordinator, after the verifier passes).
- Merge (Shawn's hand only).

## Self-scorecard

- Why it is not a 10: no live-browser proof exists yet (no screenshots, no clicked
  boards, no 9/9 load runs, no ledger hop seen landing) — the build is proven static
  only; the orb-mini fix's determinism is reasoned from the parse order, not yet
  measured across 10 fresh loads; the board-click tracking is best-effort by design
  and its landing is unproven until the verifier tests it.
- 10 things I love: (1) the diff is purely additive — one replaced line; (2) zero new
  CSS, harvest-only boards; (3) the color sequence walks cleanly indigo → blue →
  green; (4) the orb-mini root cause is named exactly (parse-order race, not a
  mystery); (5) the fix upgrades on node render, not on a sweep; (6) the tracking
  row cannot touch the score (k-filter proof); (7) navigation can never be trapped
  by a slow insert (600ms cap); (8) the acts-gap list is brutally honest (1/10);
  (9) all 18 pages return 200; (10) every script block parses clean.
- 10 things I don't love: (1) no live render seen; (2) the 150–600ms navigation wait
  is a compromise, not a guarantee the write lands; (3) board-open rows land in
  `smart_notes`, a notes table, which is a ledger of convenience, not a dedicated
  click table; (4) the nutshells are plain paragraphs — no visual nutshell treatment,
  because the harvested one is hardcoded gold; (5) no face on either board (L4 N/A,
  but a face would warm them); (6) the Reports board duplicates the existing Reports
  section's job in miniature; (7) the What-Naya-Does board points at a share link
  curl cannot even reach from here; (8) the observer watches the whole body subtree
  (cheap, but broad); (9) the retry interval (100ms × 50) is a bounded poll, not an
  event; (10) the gate's (b) 25 depth-less elements are pre-existing and untouched.
- 10 things to make it 10x better: (1) live-browser proof of everything; (2) a
  dedicated click-events table instead of `smart_notes` rows; (3) mint the two board
  destinations as real Smart Links so clicks flow through the redirect worker and
  land in `smart_link_daily_stats`; (4) an own-color nutshell treatment for boards;
  (5) faces beside the board words, alternating; (6) a live ledger-hop dashboard
  showing hop 1→2→3 as it happens; (7) the Reports room backfill ingested (service
  key) so the Reports board opens onto a live room; (8) operated-act receipts for
  all ten SN-2532 acts; (9) the orb-mini observer narrowed to the known orb
  containers; (10) a `keepalive` write path so the click record cannot be lost on unload.
- 10 solutions to apply right now: (1) file to the branch and hand to the verifier
  immediately — the live proof is the next step, not more building; (2) keep the
  600ms cap (never trap navigation); (3) keep the additive-only diff (no hero risk);
  (4) keep the acts-gap list honest (1/10) — do not soften it; (5) name the
  `smart_notes` tracking as provisional in the handoff so the coordinator can choose
  the Smart Link route; (6) leave the gold `.ph-nutshell` unused on these boards
  (own-color law); (7) leave the 18 pages untouched (verify-only); (8) leave the
  hero, numbers, and gauge math untouched; (9) record the orb-mini root cause in
  these notes so the verifier knows what to measure (10 fresh loads); (10) no deploy,
  no merge, no PR — the coordinator deploys after the verifier passes.
