# SCORECARD — Hub Shell Bars: round black circles + the three ultimate gems
## 2026-11-13 · Maker seat · One cycle, done properly (looked at the page)

**Basis:** the staged note page `/s/sn2696` as it stands (baseline probe, Playwright
Firefox, 390/1440/360, screenshots read by eye — `baseline-bars-*.png`,
`baseline-note-*.png`). The note renders; the bars are the square chips Shawn
called wrong. Every "don't" below is answered by a solution in §4, and every
solution is applied in this round unless marked otherwise.

## 10 things I love
1. The note itself renders beautifully — title, hook, boards, obsidian black, no modal.
2. The upper row's labels are clear single words — a stranger knows where each door goes.
3. The trio's three tiles are big, thumb-friendly targets at the very bottom.
4. The bar stack is flush — the obb-bar sits exactly on the trio (obb bottom == trio top), no gap, no overlap.
5. Zero overflow, zero console errors, zero page errors on the note landing at all widths.
6. The lane-stacking script measures instead of hardcoding — the obb-bar follows the trio.
7. The slug fix + modal guard survive — the note lands under the short slug, no install modal.
8. The count bubbles exist on the trio (hidden at 0, shown when live).
9. The upper row scroll-snaps — no half-sliced pill at rest; the trailing circle peeks as the affordance.
10. The shell's own eco CSS already holds the round-circle object — the fix is a harvest, not an invention.

## 10 things I don't love
1. The upper chips are square rounded-rects with colored borders — the exact thing Shawn called wrong.
2. The trio tiles are big colored squares with no labels — a stranger can't tell what they open.
3. Two bars read as two different systems (pill chips vs big tiles) — no family resemblance.
4. The Activity door appears TWICE (upper pill + trio segment) — doubling up.
5. A stray green dot floats on the upper bar's top edge (the Activity badge) — reads as a defect.
6. The trio's colors shout channels (blue mail / green activity / gold spaces) instead of worlds.
7. The trio tiles are 54px — oversized next to the 29px upper jewels; the bottom bar dominates the screen.
8. The upper jewels are tiny (26–29px) inside 52–58px pills — most of the pill is chrome, not icon.
9. No gems — nothing at the bottom says Personal / Business / Thing.
10. The Search button and the rail's nav labels sit under the bars at max scroll (pre-existing, out of scope — search and side rail ride the Personal-complete round — but visible on the page, so named, not hidden).

## What would bring 10x more value
1. Round black circles + gems — the bars become the elite doors Shawn ordered.
2. Labels under every circle — a stranger navigates with zero learning.
3. One visual family for both bars (same object, same glow language).
4. Worlds, not channels, at the bottom — Personal / Business / Thing with live counts.
5. Kill the duplicate Activity door — one door per destination.
6. Kill the stray green badge dot with the pill it belongs to.
7. The trio at 38/27px — the bottom bar stops dominating and the content breathes.
8. Gems as the faces of the doors — three distinct silhouettes a child can tell apart.
9. Counts live from the shared stores — the bottom bar is alive, not decoration.
10. Keep the stack flush and the content clear — the fix must not cost a pixel of reading room.

## 10 solutions applied right now
1. Restyle `.obb-jewel` into the shell's own `.eco-bb-ico` circle (46/44px, 50%, obsidian gradient, own-color rest glow via `--obb`); `.obb-pill` becomes the transparent column button.
2. Remove the Activity pill + its badge from the markup (and the dead `.obb-badge` rule).
3. Transplant the bottom-icons Hub leg trio CSS verbatim (gate tile + the three named adaptations).
4. Transplant the messenger gems verbatim (amethyst / emerald / diamond SVGs).
5. Re-key SEGS to personal / business / thing, counts from the shared stores, taps by full URL.
6. Keep the lane-stacking script + `syncStack` measurement — no hardcoded offsets.
7. Keep `.main` computed padding (220px desktop / 380px phone) — it clears the new stack; do NOT apply 161/193 (it would under-clear the obb-bar stack: 161 < 166 desktop). The brief's 161/193 was calibrated for the live Hub stack (eco + trio, no obb-bar); this shell's stack adds the obb-bar. Condition in the brief ("if the computed padding does not clear") does not fire.
8. Update the eco-offset fallback 79px → 85px at both sites (the new trio height per the round) with a named comment; the measured `--notif-h` still rules.
9. Verify radii / sizes / clicks / cover on staging at 1440 / 390 / 360 with fresh profiles.
10. Diff the whole file against the base; every hunk inside the bar regions; the slug fix byte-identical.

## Decisions riding with the build
- **Clearance:** no `.main` change. Measured stack after the edit ≈ 166px desktop / ≈ 145px phone; computed padding 220 / 380 clears it by ≈ 54 / ≈ 235px. Re-proven by the final cover probe, not by the text.
- **Eco offset:** the measured mechanism stays (`syncStack` + `--notif-h`); only the pre-init fallback text moves (79 → 85). The eco dock does not mount on the note landing (baseline: 0 buttons at all widths), so the rule is not exercised here — it still guards every other view.
- **Ask-room override:** the 71px lift is the ask-room's own height, not the trio's — unchanged by this round. The eco leg of the override follows `--notif-h` automatically, and the obb-bar follows via its lane script. Prove by opening the ask-room in the final probe, or name it open in NOT-DONE.
- **Mail / Activity doors:** gone from the bar (trio law: worlds, not channels). Mail lives in the page's inbox view / Smart Mail. The `nayanet.notif.spaces` key keeps its name (the Hub writes it); only the segment is re-labelled Thing.
- **Counts:** Personal = ActivityLog unread, Business = `nayanet.notif.mail`, Thing = `nayanet.notif.spaces`. External writers (`set('mail')`, `bump('spaces')`) are untouched and still feed the new keys.
