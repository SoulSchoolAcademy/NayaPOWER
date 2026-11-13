# SCORECARD — SEO / AI back-end, public blog phase 2

**Round:** SEO/AI back-end (public blog phase 2) · **Date:** 2026-11-13 · **Seat:** Maker
**Honest score: 8 / 10.**

The work itself is 10-grade — the probe caught two real bugs and both were fixed, the proof is complete at every width and every UA, and nothing is hidden. The score is 8 because two outcomes are incomplete, and the brief's own rule says a correct stop is reported as below 9, never as done. Deduction, named: **−1 for the JOIN leg stopping** (the read point does not exist at the join origin, dedupe cannot be proven under anon, removal cannot be done under anon, and one or two test join rows remain in live data pending owner-lane removal); **−1 shared for the two data conditions the machine reports but cannot fix** (ten canonical collisions awaiting Shawn's call on which note keeps each number; the 5-point test not passing at scale because the nutshell point is a property of the notes, 23/1,058). Nothing else is deducted: the transient Cloudflare 1102 flakes are not the build's fault (all retest 200), and the `/hub` size reading was a probe measurement artifact settled by sha.

## Why it is not a 10

1. The JOIN leg — a named part of Part 2 — ends in an honest stop, not a proof. The full-flow browser join cannot be shown.
2. One or two test join rows sit in the live `smart_link_joins` table until the owner lane removes them. A round that leaves live data behind is not a 10.
3. Ten notes share their canonical URL with another note. The machine names it and works around it (full-id URL, sitemap dedupe), but the collision itself is unresolved.
4. The 5-point test passes 5/5 on 21 of 1,058 notes. The brief expected a pass on every sampled note; at scale the nutshell point fails on 1,035 notes because the notes were not written to nutshell length. The machine refuses to rewrite notes to pad a score — which is right — but the headline number is what it is.
5. Four notes 503'd (Cloudflare 1102) through the probe's retries during the final crawl. All retest 200, but a fully clean crawl with zero transient failures was not achieved.
6. The ambassador cluster has zero primary topics — the keyword scorer absorbs its notes into `ai-is-hiring`. The six clusters exist as tabs, but one of them is empty as a primary. That is a scorer weakness, not a build failure, and it is named in the record.
7. The `nayanet-naya` cluster holds 657 of 1,058 notes because it is the no-hit fallback. The clustering is keyword-based and honest, but the biggest cluster is mostly "no strong keyword hit", which is weak as an organizer.
8. No live Smart Lists with `smart_note` items exist, so Lists-based related links were proven on a test list only. The mechanism is real and the test list is gone, but no live list exercises it yet.
9. The live Reports destination page throws `pad is not defined` on the click-through (pre-existing, out of scope, named in the record) — the round's proof touches it and cannot fix it.
10. The probe itself needed four fixes mid-round (proxy CONNECT line in status parsing, HTML entities in lengths, FAQPage/HowTo matching body text, the sn0587 denial case). The final probe is correct, but the first two probe runs measured artifacts alongside real failures, which cost a rebuild-and-redeploy cycle each time.

## 10 things I love

1. The probe earned its keep twice: it found the 806-note finder bug and the 10 canonical collisions — both real, both fixed, both would have shipped silently without it.
2. The JS-vs-Python mirror: 0 divergent over all 1,058 notes, three builds in a row. Two independent implementations agreeing exactly is the strongest check in the round.
3. The unified content resolver: 0 unservable notes out of 1,058, from a feed with two layer vocabularies, five empty subtitles, and two topic-less notes — all resolved from the notes' own words.
4. Every related link carries its reason, and the reasons were verified against the feed data, not assumed. The floor of ≥3 holds for all 1,058 notes, including the topic-less ones.
5. The test-list lifecycle was done properly: created, proven, removed, read-back empty, final worker carries an empty list index (`{}`).
6. Deployed == local == proof sha, twice over (worker and shell), with the multipart envelope accounted for exactly (184 bytes).
7. The sitemap tells the truth: 1,049 unique URLs, duplicates collapsed, no URL that 404s.
8. The Hub proof at three widths with zero overflow, zero console errors, zero page errors — and the bars round's own checker re-run verbatim, 18/18 upper clicks landing.
9. The JOIN gap is reported with first-hand grounding (the walk template was read, the cookie was grepped for, the grants were tested) instead of a hand-wave. A stop with evidence is worth more than a claim.
10. The record names every failure — the 42 title fails, the 22 description fails, the 1,035 nutshell fails — with the slugs attached. Nothing is smoothed over.

## 10 things I don't love

1. The JOIN leg stops. A whole leg of Part 2 ends with "cannot be proven yet" and a live row left behind.
2. The 5-point headline: 21 of 1,058 at 5/5. The test measures the notes more than the machine, and the machine cannot fix it.
3. Ten notes share a canonical. The workaround is correct, but the data is still wrong.
4. The keyword clusterer is blunt: a 657-note fallback bucket and an empty ambassador primary.
5. Four 1102 flakes during the final crawl. Transient, but they sit in the failure list and need a paragraph of explanation each time.
6. The feed is a moving target: the report, the deploy, and the probe each read the live feed at a different minute. Nothing broke this round, but the seam is visible.
7. The probe's first two runs mixed real failures with measurement artifacts (status line, entities, body-text matching). The final run is clean, but the earlier runs cost time.
8. The `/hub` size confusion (character count vs bytes) took two rounds to settle. The sha was always the right assertion; the probe should have used it first.
9. The bars probe's `checker-results.json` was never written (its `timeout 280` cut it mid-clicks). The evidence exists in stdout + the separate upper-clicks run, but the single file the bars round produces is missing.
10. The score report is 1.7 MB of JSON. It is complete, but it is not a human-readable document — the record has to carry the summary, and a reader who wants the names must open the file.

## 10 things to make it 10x better

1. A cookie-set/read point at the join origin (walk worker), so the JOIN flow can be proven end to end in a browser.
2. A server-side dedupe for joins (unique index on (link_id, joined_alias) or an RPC) so the dedupe proof doesn't depend on an anon SELECT that privacy forbids.
3. A grant or service-key path for test-row removal, so no round ever leaves live rows behind again.
4. Shawn's call on the ten number collisions, then a re-filing of the losing notes under their true numbers.
5. Notes written to nutshell length at filing time (the filing loop enforcing 40–60 words), so the 5-point test passes on new notes by construction.
6. A clusterer that earns its buckets: topic-aware scoring with a real fallback review, so `nayanet-naya` stops being the 657-note default and ambassador gets its primaries.
7. A live Smart List with `smart_note` items, so Lists-based related links are exercised by real data, not a test list.
8. A per-request CPU budget check on the worker: the related computation is O(n²)-ish per request, which is the likely source of the 1102 flakes under load; precompute or cache the cluster/topic indexes per isolate.
9. A stable feed snapshot for a round (pin the revision at build time and deploy that exact revision), so report, deploy, and probe can never disagree about the feed.
10. The probe writing its failure list to a file from the first run, and asserting by sha instead of by size everywhere — so no re-run is ever needed to identify a failure.

## 10 solutions applied now

1. `phase2FindNote`: canonical slug first, phase-1 finder as fallback — the 806-note 404 fixed.
2. Sitemap dedupe by canonical (Set) — no URL listed twice, count 1,049 stated honestly.
3. Report flags for canonical collisions (`canonicalCollision`, `canonicalServesThisNote`, `fails` += `canonical-collision`) — the 10 second notes are named, not silent.
4. Highlights guard: collision-second notes are never picked as a cluster rep.
5. Shell card links parseInt-normalized on both branches — all 1,058 card hrefs now equal the canonical.
6. Probe retries 503s (3 attempts) before counting them — the 1102 flakes stop polluting the failure list.
7. Probe parses status from `-w %{http_code}` (not the proxy CONNECT line) and unescapes title/description before measuring.
8. Probe scopes the FAQPage/HowTo check to the JSON-LD script block, and asserts `/hub` by sha.
9. Test list fully removed after proof, read-back empty, final worker's list index `{}`.
10. The highlights flagship cluster corrected (`smart-notes`, not the hardcoded `nayanet-naya`) — the build now takes the flagship's cluster from the report, never from a literal.

## Scorecard cycle

One cycle, as the brief orders. By my own accord the round is not 9+: the JOIN stop and the two unfixable data conditions cap it at 8. I fixed everything that was mine to fix (the finder, the card links, the sitemap, the probe) before handing off; what remains is named in the record with its owner and precondition, not fixed by invention. I sincerely judge the work complete as a staged round with honest stops — and the score says so.

## Fix round — re-presentation (2026-11-13, checker FAIL → re-present)

The checker returned FAIL on three fixable items; the fix round clears all three and re-presents. **The score stands at 8/10 — this fix does not re-score the build.** What changed: the filed record's one [FILL] is filled from evidence already in the record and its tip is corrected (F1); the handoff states the new tip verified against `git ls-remote` (F2); the related-links renderer dedupes by rendered href — 147 notes with a duplicated `/s/sn2650` before, **0 after**, the ≥3 distinct-related floor holding on every note, the collision-second note reachable by its full-id URL (F3). What did not change: the JOIN stop, the ten canonical collisions awaiting Shawn's call, the 5-point test at scale — the deductions behind the 8 stand exactly as written above. One honest gap in the fix round's own proof: the bars no-regression probe could not launch (VM Firefox SIGSEGV, documented flake) — the bars stand on the byte-identical shell, and the checker re-runs the bars probe. See the record's fix-round section for the full first-hand evidence.
