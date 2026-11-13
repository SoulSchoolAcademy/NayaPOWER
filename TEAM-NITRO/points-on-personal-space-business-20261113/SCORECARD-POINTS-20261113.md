# SCORECARD — Points on Personal, Space, Business (maker self-score, 2026-11-13)

## What it is

My own scorecard on the round, in the required form: why it is not a 10,
10 things loved, 10 things not loved, 10 things to make it 10× better,
10 solutions to apply right now. Evidence is cited, not claimed.

## Score: 8 / 10

The pill is live, wired, and proven; the heroes are one page to 0 px. Two
points off for the 390 wrap (F3) and one point off for the live session not
being provable from this VM (fixture harness only) — both named in the
record, neither hidden. The missing donut target (F1) is pre-existing and
surfaced, not scored against this round's build; the pill-vs-big-number
question (F2) is a captain's call, not a defect in the wiring.

## Why it is not a 10 (every reason)

1. At 390 the pill wraps below the name instead of sitting immediately
   right of it with the 14 px gap — the brief's same-row criterion fails at
   one of three widths, on all three pages (measured: pill y=404, name
   y=350–390).
2. The live session could not be proven: Supabase is CORS-blocked from this
   VM, so pill == donut was proven by fixture harness (9/9), not by a live
   citizen's session.
3. The donut the wiring cites never renders (`#os-donut-wrap` absent) — the
   pill equals a variable, not a painted number a citizen can see.
4. The pill (donut total, 245) and the big number (spine score, 540) are
   two different numbers on the same page, and this round does not resolve
   which one "points" means.
5. No Chromium cross-check was run this round (Firefox only).
6. The hover check shows the harvested pill does not visibly light on hover
   (no `:hover` rule in the harvested CSS) — H5 is satisfied only in the
   vacuous sense of "like the harvested one."
7. The clone build needed a lane-local adapted script rather than the
   original `build-clone.py` untouched — the original's template source is
   the audit rooms file, not the Personal bytes.
8. The Personal file and the clones still differ by the pre-existing
   rooms-plus fix (clone-only), so the three files are not one template.
9. The big-number sweep target could only be shown via `osBuildSpine`'s
   returned score; the headless rAF runs slow, so the sweep itself was read
   mid-flight, never at rest.
10. The staged proof had not yet run when this scorecard was first written
    (it runs before handoff; the record's § Staged run carries it).

## 10 things I love

1. The heroes align to **0 px spread** at all three widths — 350/350/350,
   311.2/311.2/311.2, 483/483/483. The baseline gap was 337 px at 390.
2. The pill sits immediately right of the name with **exactly 14.0 px gap**
   at 1440 and 360 on all three pages — the harvested geometry, reproduced.
3. The harness is 9/9: pill == donut total on every page, every fixture,
   and the pill **changes** with the fixture (245 → 250 → 0).
4. The pill is **unchanged by the spine landing** — it follows the donut
   total and nothing else, exactly as the wiring rule orders.
5. The clone diff vs the previous staged clones is **exactly the pill +
   wiring and nothing else** (2 inserts per clone).
6. The Personal diff vs live is exactly 3 inserts (pill, wiring, hero-fix).
7. Change cover never intersects the name at any width on any page — the
   baseline's live-Personal clip is gone.
8. Zero overflow at every width, start and end, on all three pages.
9. One pill per page, `…` loading glyph, no placeholder 0, no hand-written
   number, no second points display anywhere.
10. The round surfaced two real page truths (F1, F2) with numbers instead
    of papering over them — the record is honest about what the page is.

## 10 things I don't love

1. The 390 wrap: at the width Shawn holds in his hand, the pill is below
   the name, not beside it.
2. The fixture harness is a stand-in for a live session, not the thing itself.
3. The donut target is missing — the wiring's reference number is invisible.
4. Two "points" numbers on one page (245 vs 540) with no ruling on which
   is the citizen's points.
5. The saves node contributes 0 to the donut total (no `tkey`/`map`) while
   the spine counts saves at 5 — the two formulas quietly disagree on saves.
6. The big-number sweep reads mid-flight in this VM; I never watched it
   land at rest.
7. Hover does nothing visible on the harvested pill.
8. The adapted clone script is a second script to maintain next round.
9. The rooms-plus fix still lives clone-only; Personal and the clones are
   not one template.
10. The staged run comes after the build instead of with it (file, then
    verify staged) — the record carries a fill-in section.

## 10 things to make it 10× better

1. A captain's ruling on the 390 wrap: accept it, or order the layout
   follow-on (full-width info at 390 so name + pill fit one row).
2. A live-session proof on a network where Supabase loads: pill == donut
   with a real citizen's rows.
3. Restore the missing `#os-donut-wrap` / `#os-ring-wrap` targets so the
   points board's donut actually paints — then pill == donut is visible,
   not just computed.
4. One ruling on which number is "points" — donut total or spine score —
   and the pill wired to the ruled one.
5. Reconcile the saves value (donut 0 vs spine 5) so the two formulas agree.
6. A Chromium cross-check at all three widths.
7. A hover rule for the pill, harvested or ruled — so H5 means a visible
   light-up, not a vacuous match.
8. Fold the pill into `build-clone.py`'s own template source so the next
   round runs the original script untouched.
9. Land the rooms-plus fix on Personal (or rule it clone-only forever) so
   the three files are one template.
10. A staged-first flow: file, curl-verify, staged-probe, then write the
    record's staged section — no fill-in sections.

## 10 solutions to apply right now

1. **This round, applied:** pill + wiring + hero-fix as built; record
   names F3 with the exact widths (292.0 / 324.6 / 261.5 vs 228 px) so the
   captain can rule without re-measuring.
2. **This round, applied:** fixture harness v2 with fresh page per fixture
   and immediate reads, so the page's own 15 s data retry cannot clobber
   the fixture mid-read.
3. **This round, applied:** spine simulation in the harness
   (`osBuildSpine` → `_osSpine` → re-render) proving the pill is
   independent of the spine.
4. **This round, applied:** independent recomputation of the expected total
   from the page's own exposed `LD_NODES`, not from my hand math (which
   wrongly said 255 — the page's table says 245).
5. **This round, applied:** baseline measured before any edit, so the
   hero-fix effect (337 px → 0 px) is a measurement, not a claim.
6. **This round, applied:** diff audits asserting the exact hunks on all
   three files, so "nothing else changed" is proven by bytes.
7. **Next round, proposed:** the 390 layout ruling — the cheapest honest
   fix is a follow-on round, not a silent restyle inside this one.
8. **Next round, proposed:** restore the donut targets as its own round,
   with the donut painted and pill == visible donut proven by eye.
9. **Next round, proposed:** the points-number ruling (donut vs spine),
   then a one-line rewire if the ruling goes the other way.
10. **Next round, proposed:** run the live-session proof from a network
    where Supabase loads, and the Chromium cross-check, before the round
    is called 10.

## Design-contract gate (a)–(i) + H1–H5 (summary; detail in the record)

(a)–(i): all PASS except L5/L7 noted above (F3 blocks the 10). H1: pill by
the name at 390 — present and fully visible, wrapped below (partial).
H2: pill number matches the donut total in the same session — PASS by
harness (9/9), live session not provable from this VM. H3: three heroes one
page at scroll 0 — PASS (0 px spread, eye-checked). H4: Change cover never
covers the name at 390 — PASS. H5: pill lights on hover like the harvested
one — PASS vacuously (harvested pill has no hover change; measured
identical computed style before/after hover).
