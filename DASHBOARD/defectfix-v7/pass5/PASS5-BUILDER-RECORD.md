# PASS-5 BUILDER RECORD — Dashboard no-gray-text round (20+10 loop, round 5)

- **Builder seat:** pass-5 builder (subagent 74dca49d)
- **Started:** 2026-11-10 ~04:12Z
- **Brief:** `~/workspace/team-nitro/DASHBOARD-PASS5-BRIEF-20261110.md` (checker 7/7)
- **Base:** GitHub blob `a334b437` (1,773,677 B), branch `dashboard/pass4-one-family-20261109`, path `DASHBOARD/defectfix-v7/pass4/dashboard-pass4.html`
- **Target branch:** `dashboard/pass5-no-gray-text-20261110`
- **Target path:** `DASHBOARD/defectfix-v7/pass5/dashboard-pass5.html`
- **Status:** STARTED — four required docs read in full (Orientation, Brand, Bullseye, Brief). Fetching base via git-blobs API next.

## The six exact changes
1. Minis UP — gauge + tiles centered in widened bars; numbers never touch bottom edge.
2. Every mini shows its live number in digit tiles underneath, ALWAYS — 0 for zero/not-tracked, never a bare dash.
3. Remove ALL gray/small/unreadable text on boards (not tracked yet / not counted / needs views / Quiet… / stuck Reading your Smart Links…).
4. ≥12px clear space between gauge lowest point and top of digit tiles.
5. Board headers one clean object — small flat subtitles become real object or removed.
6. EVERY mini gauge click drills into that stat's deeper stats — harvest hero orb click behavior, no invented drill.

## Do NOT touch
Hero gauge · payout line · D4-R1 scroll-margin rule. No redesign, no invented component, no merge, no deploy.

## Progress log
- 04:12Z — checkpoint 1: four docs read; record created; fetching base.
- Base fetched: blob a334b43747ec5d7884ebeef485b3995ca7e211e8, 1,773,677 B, sha256 a4a5d3ccfa8895063b8549105a22a268b461911652d9b05f9aff8f1b74823162 (matches pass-4 deploy record).
- Recon done. Cell builders (all emit `.os-sl-gauge` = dial + num + lab + sub): `slGaugesHTML>cell` L13795 (link cards), `_boardCell` L19091 (world/page/link boards), Reports `cell` L19252. `miniConvert` L25276 returns early on '—' — so '—' numTxt never tiles; fix at the sources ('—' → '0').
- Hero-orb harvest CONFIRMED: orbs are `<button class="os-ld-node" data-node="key">` (L19859); delegated click L18415 → `ldOpenNode(key)` (L18189): 1st click features metric on hero gauge via `_setFeaturedMetric`, 2nd click opens that metric's drill view (sales/joins/notes/invs/posts/shares/comments/likes/saves). Sales drill even carries a Revenue orb (s-rev) and joins drill a Click-Thru orb (j-ctr).
- Drill mapping (per metric, same everywhere): clicks→sales · joins→joins · CTR→joins (j-ctr lives there) · views→sales (funnel top of link clicks) · revenue→sales (s-rev lives there) · posts→posts · invites→invs · actions counted→data-os-go="today" (Today's Intel breaks down the mix) · messages→data-os-go="inbox" (inbox is the messages' deeper view). Both attributes are existing harvested page patterns; no new drill invented.
- Board headers: `_boardHTML` L19174-19182 emits `what` span (`.os-wb-id span`, 12.5px) + `note` p (`.os-wb-note`) — the four quoted subtitle lines. Fix #5: remove BOTH lines from `_boardHTML` (header = jewel + title; the 4-cell stat row is the board's live reading). Also remove Reports quiet `<p id="os-reports-quiet">` (L8632) + its un-hide in `_renderReportsBoard`.
- `Reading your Smart Links…` (L8579, static in #os-sl-mine): remove static line (host starts empty) + 10s settle-timeout guard in `loadSmartLink` writing the honest connection-unavailable note if the promise never settles.
- Subs: REMOVE `.os-sl-gauge-sub` from all three cell builders ('not counted'/'needs views'/'not tracked yet'/'no clicks yet'/'all time'/'X joins'/'X% became joins'/MOCK tags — all redundant with sibling cells, the mock outline, or the 0 tiles). Labels stay, forced #fff + bigger.
- Do NOT touch: hero gauge, payout line L8578, D4-R1 rule L27532.
- Baseline measured on pass-4 (Playwright Firefox, sandbox, gauges force-mounted with the page's own `_osMountSlMinis`): 20 minis, only 2/20 tiled (18 bare '—'); gap dial→tiles 0px everywhere; visible-dial→tiles 53px phone / 7px desktop; subs 'all time'/'no clicks yet'/'not counted'/'not counted yet'/'not tracked yet'; Reading line stuck (spine never answers in sandbox); 0 console errors; 0 overflow.
- Edits applied (apply-pass5.py, 20 asserted replacements + 3 follow-ups): E1 PASS-5 CSS (bar padding 20/6/16, cell flex-centered with 10/12 padding, num margin-top 14px, labels #fff 11px/10px, dial cursor pointer) · E2 slGaugesHTML cell (sub gone, data-node on dial) · E3 _boardCell (sub gone, '—'→'0', drill attr) · E4 Reports cell + quiet line removed · E5 _boardHTML headers removed · E6 Reports subtitle removed · E7 Reading line removed + 10s timeout + rejection handler · E8 mini-drill delegation (document click + keydown, ldOpenNode) · E9 link-row guard · E10 board-open guard · E11 mock outline on link/world board rows · E12 featured labels 'clicks · not counted yet'→'clicks', 'joins · not counted yet'→'joins' · E13 MOCK comment truthed. All 18 inline script blocks pass node --check. Diff vs base: 283 lines; D4-R1 + payout byte-identical; no 'blockchain'.
- Verified on pass-5 (probe.py --clicks, 360/390/1440, scroll 0 + scrolled, screenshots): 20/20 minis tiled, all '0'; gap mount→tiles 14px, visible-dial→tiles 67px phone / 21px desktop; tiles→bar-bottom clearance 45–351px phone / 47px desktop; labels pure white 10px/11px; zero subs, zero board subtitles/notes, zero gray text in mini/label areas; Reading line gone; Reports quiet gone; 0 console errors; 0 overflow. Clicks 20/20: Actions→#today · Posts→os-creations-view · Messages→#inbox · Invites→os-invites-view · clicks→os-sales-view · joins→os-joins-view · CTR→os-joins-view · views→os-sales-view (all with #drill-<key>). Two-click sequence proven (data landed): 1st click features sales on the hero gauge, 2nd opens the sales drill. Mock mode: world views sample 708 inside the dashed outline, 16/16 tiled, 0 subs. showView('dashboard') in sandbox writes the honest 'Connection unavailable' note (no stuck line). Reports door paragraphs measured 14px rgb(232,232,236) — white, kept.
- Known limits (for the verifier, live): (a) per-link Smart Links cards never render in the sandbox (no ledger) — same code path + CSS as the verified boards, but the verifier must SEE a link card live; (b) D4-R1 scroll rest not re-measured on the taller rows (rule untouched; geometry driver is trailing space, unchanged; the "label clear" check is moot — the label is gone); (c) the 10s hang-timeout path unexercised (sb undefined in sandbox; only the sb-null path observed); (d) hero gauge caption still says 'Quiet — nothing measured yet.' in its rest state — DO-NOT-TOUCH this round, flagged not fixed; (e) historical comments still quote removed strings (L13753, D4-R1 comment) — annotated where it matters.
- NOT in this round: no merge, no deploy (coordinator deploys after independent verification).

## FILING (GitHub, read-back verified)
- **Branch:** `dashboard/pass5-no-gray-text-20261110` (created from pass-4 head `43a937e743c97645082f903f654b100c4c6615cf`)
- **File:** `DASHBOARD/defectfix-v7/pass5/dashboard-pass5.html` — blob `4b4084e1aad4e3fbd64d1052abc2f48cdc56ac23`, 1,778,959 B, commit `1bb12951049ef7a6866400c8031faa35161c6258`; read-back via git-blobs API: BYTE-IDENTICAL, sha256 `0e4ef2fef4ccf54c178155f86d14176a56418d1d7590732ce39321b583b4a388`
- **Record:** `DASHBOARD/defectfix-v7/pass5/PASS5-BUILDER-RECORD.md` — blob `8503cb89c0b74dcf2ce02e786b0d277ae6f34400`; branch head `edcceadac96ce3aebc5e9ff59fa8b16e2423b157`
- **Link:** https://github.com/SoulSchoolAcademy/NayaPOWER/blob/dashboard/pass5-no-gray-text-20261110/DASHBOARD/defectfix-v7/pass5/dashboard-pass5.html
- **Diff vs pass-4 base:** 283 lines changed; base blob `a334b43747ec5d7884ebeef485b3995ca7e211e8` (1,773,677 B) untouched (sha256 `a4a5d3cc…` re-verified after editing).
- **Local work files:** `~/workspace/team-nitro/dashboard/defectfix-v7/pass5/` — `dashboard-pass5.html` (deliverable), `dashboard-pass4-base.html` (base copy), `apply-pass5.py` (edit script), `probe.py` (Playwright verification probe), `PASS5-BUILDER-RECORD.md` (this record).

## SELF-SCORECARD (maker's own, before handoff)
**Self-score: 9/10.** All six brief changes are complete and measured-pass in the sandbox. The point off is for the live-only verifications I cannot do here (link cards with real data, D4-R1 rest on taller rows, hang-timeout path) and the 67px phone dial→tile air (tacho internal slack shared with the hero — out of scope to touch).

**Why it is not a 10 (every reason):** (1) phone dial→tile air is 67px — loose-looking, driven by the tacho mount's internal 53px slack I must not touch; (2) per-link cards unverified live (no ledger in sandbox); (3) D4-R1 rest not re-measured on taller rows; (4) 10s timeout path unexercised; (5) first click with live data only FEATURES the metric (second drills) — faithful to the hero orbs, but a beat slower; (6) CTR/views/revenue map to a neighboring drill, not their own (no such orb exists); (7) hero caption still carries the Quiet phrase (do-not-touch); (8) stale comments still quote removed strings; (9) Reports door paragraph kept (white 14px, deliberate — but a strict eye could flag it); (10) phone 2x2 rows have uneven heights (351px clearance on short cells).

**10 things I love:** (1) 20/20 minis show a live 0 in digit tiles — zero bare dashes; (2) zero subs, zero subtitles, zero quiet lines — boards are only gauge + number + white label; (3) header is one clean object: jewel + title; (4) air everywhere — 14px mount gap, 21/67px visible gap, no crashes; (5) labels pure white and bigger; (6) every mini click drills to its own stat — 20/20 click-tested; (7) two-click hero semantics preserved exactly (feature then drill); (8) mock numbers stay marked (dashed outline on world board too); (9) stuck Reading line gone + honest degradation; (10) nothing else moved — hero, payout, D4-R1, Show on gauge / Open it all byte-identical.

**10 things I don't love:** (1) 67px phone air; (2) link cards unverified live; (3) D4-R1 rest unmeasured; (4) timeout path unexercised; (5) neighboring-drill mappings; (6) first-click-features pacing; (7) hero Quiet caption remains; (8) stale comment quotes; (9) Reports door paragraph kept; (10) uneven phone row heights.

**10 things to make it 10x better:** (1) live-data verification (link cards, D4-R1 rest, timeout); (2) a dedicated CTR/views/revenue drill view (future round, Shawn's call); (3) shrink the tacho mount's internal slack (hero-safe TnTacho change); (4) first-click drill option for minis; (5) remove stale comment quotes; (6) hero caption aligned with the no-gray-text law (his call); (7) equal-height phone mini rows; (8) a zero that pulses gently so 0 reads alive; (9) Reports door paragraph as a real object or removed; (10) mock legend on the summary card.

**10 solutions to apply right now:** (1) ship this round as-is — all six changes measured-pass; (2) list the live-only checks for the verifier (above); (3) mapping documented in code comments; (4) hero caption flagged, untouched; (5) Reports paragraph kept deliberately; (6) TnTacho internals untouched; (7) file to GitHub on the new branch, read-back verified; (8) hand the verifier exact measurements + live checks owed; (9) no merge, no deploy; (10) record kept here, checkpointed.
