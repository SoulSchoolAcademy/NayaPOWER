# SCORECARD — Hub Live Leg (Terra, 2026-11-13)

## Score: 9/10 — LIVE, proven.

The fixed shell is live on nayanet.app, the note route is restored, SN-2696
renders live as the first public note, the bars are the round black circles +
three gems, and the next sync cannot revert any of it. The point off is the
stale feed the workflow deploy shipped (bot 404) — caught by this round's own
battery and fixed the same hour, but the standing trap on main is still open.

## 10 things I love

1. The revert trap was proven IN WRITING before any deploy — template
   byte-identical to live, zero route markers — and closed the same way.
2. The live shell carries the CURRENT 200 baked notes (SN-2766 in the set),
   parsed back list-identical — no backwards roll of the Hub's notes.
3. The next-sync proof used the sync's OWN inject function, not a
   re-implementation — the guarantee is the real code path.
4. Branch + merge + both deploy paths all verified byte-exact (shas, not claims).
5. The bot page works: Googlebot gets SN-2696 in initial HTML, 200, canonical.
6. The walked cold-link flow renders the note at 390/1440/360 — login page first.
7. The bars measured, not eyeballed once: 50% radii, 46/44/38/27px, labels, 3 distinct gems.
8. `/hub/feed` is clean at last — 0 errors, real JS at the absolute src.
9. `/robots.txt` + `/sitemap.xml` are real now (the +4 working, not just filed).
10. Nothing was silently fixed: the stale feed, the re-entry friction, the 360
    lag, the +2 B whitespace are all named in the record.

## 10 things I don't love

1. The GitHub workflow deploy shipped a stale 877-note feed and a bot 404.
2. Main's `HUB/app/feed-live.json` is still that stale copy — the trap stands.
3. A signed-in visitor following a full-navigation /s/ link must re-enter
   their name (entrance session).
4. The 360 upper bar mounts a beat after first paint.
5. The contents API returns 0 B for the 5 MB shell (1 MB limit) — raw
   read-back was needed.
6. The live worker script is wrangler-bundled, so no direct sha match to the
   phase-1 source — behavior + markers only.
7. The deploy needed TWO paths (workflow + Direct Upload) to land complete.
8. The sync's inject adds 2 B of indent whitespace per rebake (harmless, untidy).
9. The merge happened on Shawn's tap without a checker/captain double-check
   first — the verification here is post-hoc by this seat.
10. The entrance still gates every cold deep link with the name form (by design,
    but it is the whole deep-link experience).

## 10 to make it 10x better

1. Refresh `HUB/app/feed-live.json` on main (or overlay the fresh feed in the workflow).
2. Entrance session persistence across full navigations.
3. A live-feed freshness gate in the workflow (deploy fails if served feed < file).
4. A post-deploy curl battery as a workflow step (bot 200, feed count, shell sha).
5. Bot-page smoke test in CI against the staged worker.
6. The 360 bar mount: measure what delays it; mount with the note view.
7. Contents-API read-back replaced by raw read-back for >1 MB files, everywhere.
8. A single deploy path (one writer) instead of workflow + sync racing.
9. The +4 config asserted from `wrangler.toml` by the deploy scripts (no hardcoded lists).
10. A standing "live AFTER" receipt filed on every live leg, same shape as this one.

## 10 solutions to apply right now

1. Captain's call on the stale repo feed (refresh vs workflow overlay) — asked in the report.
2. Entrance seat: persist the session across full navigations (re-entry friction).
3. Next live leg: run the curl battery BEFORE calling the deploy done (this round's catch is the proof).
4. Keep the template-fix step mandatory in every future live leg (prove the template first).
5. Keep the deploy-defaults alignment (both files now +4; re-check on any wrangler change).
6. File the live-leg record to the branch in the same hour as the merge (done here, second commit).
7. Watch the next SN sync: confirm live stays `64380ef3`-class (route intact) after it rebakes.
8. Retire the "live 8a209533" baseline everywhere — live moved at 16:17Z.
9. Note the 360 mount lag in the bars follow-on (sub-second, low priority).
10. Show Shawn the live link itself (https://nayanet.app/s/sn2696), not this record.
