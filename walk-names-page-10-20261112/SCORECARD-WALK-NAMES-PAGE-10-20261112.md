# SCORECARD — WALK NAMES PAGE 10/10 (presentation round)

**Round:** walk/names-page-10-20261112
**Maker:** Walk Names Page maker seat.
**Status:** Built + locally proven 99/99; deploy STOPPED (Q10 probe not run).
No checker dispatched — honest 7/10 is below 9.

## Honest score (out of 10)

- **The BUILD: 10/10** — on its local rendered evidence (99/99, screenshots
  eye-checked, shas, diff). Every DONE FIRST measurement passes rendered.
- **The ROUND: 7/10** — the build is done and proven locally, but the round's
  done bar requires the staged deploy + staged end-to-end proof, and that leg
  is stopped by the deploy-order warning. A round that cannot prove its
  staged bar is not 9. (Q10 precedent: the same honest call at 6/10 with
  only static evidence; this round has full rendered local evidence, hence 7.)

## Why it is not a 10 (every reason)

1. It is not staged — the staged walk still serves v22, so Shawn cannot
   walk this build yet.
2. Ruling 5 (building links click through to real created pages) is unproven
   on this build — the wiring is unchanged, but the click-through needs the
   staged worker.
3. The end-slide world cards, the Box read-back, and the full walk from the
   login page are unrun on this build for the same reason.
4. The `.p3-progress` base rule is still 12px gray for the building + end
   steps (scoped fix only — the global gray is still in the file).
5. The hero button sits below the fold at 1440 — three tall cards push it
   down; the citizen must scroll past the third card to reach it.
6. The h1's doubled-quote look (text-shadow glow) is still there — S2's
   adjudication stands, but a first look still reads as two quotes.
7. The corner-gem frame ornaments still overlap the step edges at
   scroll-top (pre-existing, all steps).
8. The name inputs are empty until the walk prefills them — in the local
   probe they read as blank boxes; only a real walk shows them filled.
9. The 360 label wraps were fixed by narrowing the eye lane to 44px — the
   clearance at 360 is 16px, the thinnest margin on the page.
10. The probe itself needed two timing/geometry fixes (hover settle 700→
    1200ms, scrollIntoView before hover/click) — the product was right, but
    the first probe runs measured artifacts, not the page.

## 10 things you love

1. The three cards read as three worlds at first look — purple, green, gold,
   each with its own glow, at 1440 and at 390.
2. The hover light is unmistakable by eye — the business card visibly glows
   green and lifts in the screenshot, not just in the numbers.
3. Title + subtitle + nutshell only — the wall of small text is gone, and the
   page breathes.
4. Every visible text node on the step computes to white or its board's
   color, ≥16px, opacity 1 — the sweep found zero bad nodes at all widths.
5. The live address: type a business name and the slug follows; type an
   address and it becomes the URL and sticks.
6. One hero action — "Build my pages" — big, elite, lit, and the only button
   competing for the click.
7. The card-click affordance: tapping a card focuses its name input — the
   whole card is alive, with no dead View button invented.
8. The diff is surgical — 69 lines, 12 hunks, names step only; the ten
   questions, the certificate, the end slide never move.
9. The template trap is closed — the build script asserts the new sha, the
   worker regenerated from it embeds the walk byte-identically, `recordJoin`
   3× intact.
10. The probe ran at all — Firefox launched and measured in this window after
    hours of dead browsers, and the 99/99 is rendered proof, not static claims.

## 10 things you don't love

1. It is not staged — the best-measured build of the night still serves v22
   to anyone who opens the link.
2. The hero button below the fold at 1440 — the payoff click is a scroll away.
3. The 360 label clearance is 16px — one font-rendering wobble from touching.
4. The h1 quote glow still reads as a doubled quote at first glance.
5. The frame gems still overlap the step edges at scroll-top.
6. The subtitle had to lose its Smart Link clause to become one plain line —
   the meaning now hides behind the eye instead of sitting on the page.
7. The building step's error screen is what a local click shows — true to
   the local server, but it looks like failure in a screenshot.
8. The probe's first two runs measured artifacts (hover timing, below-fold
   clicks) before they measured the page.
9. The `.p3-progress` base gray is still in the file, one scope away from
   fixed.
10. The round ends on a stop, not a landing — the value is built but not yet
    in Shawn's hands.

## 10 things to make it 10x better

1. Stage it (v23, after the Q10 probe) and let Shawn walk it fresh — his eye
   is the only verdict that counts.
2. Prove ruling 5 staged: all three building links + all three end-slide
   cards landing on real pages with the citizen's typed words.
3. Bring the hero button into the first viewport at 1440 — the citizen
   should see "Build my pages" without scrolling.
4. Fix the `.p3-progress` base rule globally (16px white) so the building +
   end steps stop carrying gray text too.
5. Kill the h1 quote-glow doubling for good (restyle the glow so the quote
   reads single at first look).
6. Tame the corner-gem frame so it never overlaps a heading at scroll-top.
7. Prefill the names step visibly in every probe — walk with a real alias so
   the inputs show filled, as a citizen sees them.
8. Give the eye its own lane in the card geometry (not a padding hack) so the
   label never flirts with it at any width.
9. Put the Smart Link meaning back on the page in one short line that is not
   a second paragraph — the citizen should not need the eye to learn it.
10. Make the hover probe settle-proof by design (wait for the settled
    computed style, not a fixed timeout) so no run ever measures a transition.

## 10 solutions to apply right now

1. **Applied this round:** label-eye lane (`padding-right:44px`) — measured
   16px+ clearance at 360/390/1440, one-line labels everywhere.
2. **Applied this round:** probe hover settle 1200ms + scrollIntoView before
   hover/click — 99/99 on final bytes, re-check proved the settled state.
3. **Applied this round:** NAYA wordmark 16px on this step — the sweep is
   clean at 360 too.
4. **Applied this round:** dead gray declarations removed, not overridden —
   the next seat reads a file with no gray traps above the fix.
5. **For v23:** deploy this exact worker (sha `1b2ff1e2…`) with the Q10
   maker's two-line join fix — no rebuild, no re-edit, the bytes are verified.
6. **For v23:** re-run `names-probe.py` against the STAGED worker (point it
   at the staging URL, fresh alias) for the full login→names→building→end
   walk — the probe already has every names-step assertion.
7. **For the next round:** one-line global `.p3-progress` fix (16px, #fff,
   opacity 1) — a 1-line change, staged with any round that touches the walk.
8. **For the next round:** h1 glow restyle — measure the quote's rendered
   pixels, not the CSS, before calling it single.
9. **For the next round:** frame-gem guard — assert no heading's bounding
   box intersects a gem's at scroll-top, at all widths.
10. **For the captain:** keep the deploy order — probe, then v23, then
    staged re-proof, then checker. The stop is what kept v22 and the join
    merge intact; the landing is one coordinated deploy away.
