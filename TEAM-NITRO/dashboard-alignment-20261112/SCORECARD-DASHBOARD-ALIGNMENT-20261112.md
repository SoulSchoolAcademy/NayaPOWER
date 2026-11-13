# SCORECARD — DASHBOARD ALIGNMENT (RESTART)

**Seat:** dashboard-alignment-20261112 (maker, restart)
**Brief:** `~/workspace/team-nitro/BRIEF-DASHBOARD-ALIGNMENT-20261112.md`
**Date:** 2026-11-13 ~01:35Z
**Honest score: 7/10**

## Why it is not a 10

The build itself is real, staged, and proven — but the round's bar (§6) is not met in full, and a 10 would be a lie. Three things keep it off the top: (1) the orb-mini race cannot hit 9/9 within 1s, because the component it measures was removed by design and the nodes wait on live data by design — no honest fix exists inside this round's authority; (2) no page row can claim "tracked" — board-open tracking 401s live, so the 18-page table is honest about opens and works but silent on tracking, and 2 rows are blocked by a dead Hub entrance button that is not this round's fix; (3) the spine's Ledger hop is NOT PROVEN — the Ledger is frozen at 31 rows since Oct 22 and no code writes it, so the funnel's "stayed" stage and the Ledger half of the spine are still NOT YET. A 10 would need all five §6 items met, and two are not. What IS done is done properly — that is why it is a 7 and not a 5.

## 10 things I love

1. **The funnel reads live numbers from Supabase on the first load** — Found 5,141, from the same view the boards already read, no new fetch, no new table.
2. **The NOT YET ruling is honored visibly** — Visited / Stayed show "—" and Joined shows the honest 0, each with its missing source named on the page itself. No fabricated number anywhere.
3. **The spine was proven with a real click, not a claim** — my-test-link 11 → 12 in 2.2s, the board 1,457 → 1,458, the funnel 5,139 → 5,141, each number moving by exactly one.
4. **The PayPal plan-link split works exactly as Shawn ruled** — the plan click moved the funnel (5,140 → 5,141) and left the board at 1,458. Two counters, two scopes, no mixing.
5. **F2 resolved** — the score that sat on "still loading" for 45 minutes now clears in 11–24s, every reload.
6. **The top-nav adjudication is proven, not asserted** — the mechanism is named in code, the timing measured (4.8s at 1440, ~9.2s at 390), the return proven by scrolling past the hero.
7. **The staged bytes are byte-verified** — blob `a071b996`, 1,848,507 B, sha256 matching the probed file exactly, and the staged page loaded live with the funnel reading 5,141.
8. **The 18-page table is honest about its methods** — click vs direct navigation per row, errors named per row, and "tracked" claimed nowhere it cannot be proven.
9. **The base was re-verified before any edit** — sha, blob, live pass-10, Reports board present, What-Naya-Does board absent, branch free — the pass-12 lesson actually applied.
10. **Act 4 is now PROVEN** — the walk builds and fills pages for a real citizen, receipted by the captain's own eyes, moving the acts-gap from 1/10 to 2/10.

## 10 things I don't love

1. **The orb-mini 1s race is unmet and unfixable here** — the metric measures a component that no longer exists, and the adapted metric fails at 1s because the nodes wait on live data.
2. **No page row claims "tracked"** — board-open tracking is broken live (401), and the round can do nothing about it inside its authority.
3. **The Hub's front door is dead in this session** — "Enter NayaNET" does nothing, so the Smart Feed — the heart of the system — is unverified.
4. **The Ledger hop is NOT PROVEN** — the Ledger is frozen since Oct 22, and the funnel's "stayed" stage waits on it.
5. **Act 1 is still frozen** — the newest Daily Intelligence Report is Oct 23, 21 days old, and the backfill needs a key only he holds.
6. **The live rooms carry console errors** — MIME-type script errors and `pad is not defined` on Growth, Reports, Library, Ledger, pre-existing and untouched.
7. **Nine Dashboard anchors are missing** — /rooms/lists, /smartfactory, /smartbox, /pi have no direct link from the Dashboard at all.
8. **F2 is resolved but slow** — 11–24s on a cold load through the VM proxy is honest but not ten-star; the skeleton says what it waits for, which is good, but the wait is real.
9. **The funnel's source line is small text** — it carries the whole honesty of the funnel, and at phone width it is the easiest line on the board to miss.
10. **The acts-gap is still 2/10** — eight of the ten things Naya is supposed to do have no operated receipt, and most of them are blocked on other rounds or on his hand.

## 10 things to make it 10x better

1. Retire or replace the orb-mini 1s metric with a race that measures what exists now (nodes mounted by 2s, numbers live when the ledger lands).
2. Fix the anon-write path (board-open tracking + mail) so a click on a board leaves a receipt — then every page row can honestly claim "tracked".
3. Fix the Hub entrance button and verify the Smart Feed behind it by walking in as a citizen would.
4. Apply the Ledger trigger and wire Box → Ledger, so the spine's Hop 2b proves and "stayed" gets a source.
5. Run the Act 1 backfill (Oct 24–Nov 9) and restore the daily intelligence reports, so the Dashboard's first act stops being a frozen room.
6. Add the nine missing Dashboard anchors so all 18 pages are one click away from the Dashboard.
7. Clear the live-room console errors (MIME-type + `pad`) at their source.
8. Speed F2 — the score skeleton should clear in under 5s on a cold load, not 11–24s.
9. Make the funnel's source line unmissable at phone width — the honesty of the page deserves the same elevation as the numbers.
10. Give "stayed" a real definition and a real source (ledger + Phase 2 window), so the funnel's last stage stops being NOT YET.

## 10 solutions to apply right now

1. **This round (done):** the funnel, the spine proof, the 18-page table, the acts-gap re-score, the top-nav adjudication — all staged and filed.
2. **Captain decision 1:** rule on the orb-mini 1s metric — retire it, or authorize a hero-render change as its own round.
3. **Captain decision 2:** place the Hub entrance dead button with the Hub shell's owner for a live re-check.
4. **Captain decision 3:** place the board-open tracking 401 with the wiring round / privacy-fix follow-up.
5. **His hand, when he taps:** the Ledger trigger apply (DDL prepared, not applied) and the Act 1 backfill service key.
6. **Back-end round:** build the join flow (read the `naya_sl` cookie at join, resolve the link id, insert ONE row deduped per link + alias) so Joined stops being 0-by-absence.
7. **Blog round Phase 2:** define the visit measurement so Visited gets a source and the deep-link route lands.
8. **Each live room's owner:** clear the MIME-type and `pad` console errors on Growth, Reports, Library, Ledger.
9. **The captain's next Dashboard round:** add the nine missing anchors and re-verify all 18 pages by click from the Dashboard.
10. **The next acts-gap round:** take Acts 2, 3, 5, 6, 7, 8, 9 one at a time and produce one operated receipt each — a receipt, not a mechanism description.

## The honest score

**7/10.** The funnel is real and live, the spine is proven hop by hop with real numbers, the top nav is adjudicated, the base was verified, and the build is staged byte-perfect. The two points lost are the orb-mini race (not proven, not fixable here) and the tracking gap (no row claims "tracked"; 2 rows blocked by the Hub entrance). The point below that is the Ledger hop and the 8/10 unproven acts. This is below 9 — so it does not go to Shawn as finished. It goes to the checker for honest review and to the captain for the three decisions above.
