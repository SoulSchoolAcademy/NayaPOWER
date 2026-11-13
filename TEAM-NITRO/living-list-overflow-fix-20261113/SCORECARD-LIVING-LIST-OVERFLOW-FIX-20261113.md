# SCORECARD — LIVING LIST PHONE-WIDTH OVERFLOW FIX

## Score: 9/10

## Why it is not a 10

- The fix itself is a 10 — one declaration, fully proven — but the lane's surroundings are not: the scheduled publish happened through a path I cannot see (the artifact file changed at 09:59:26Z with no refresh-report update and a stale `.published_hash`), and I had to guess the Hub's live address (the worker name 404s; nayanet.app/hub answers). A 10 would have the publish path and the hash file in the same verified state as the fix.
- My first overflower scan was naive (flagged 110 inline elements with clientWidth 0) and had to be replaced by a refined scan before it meant anything. The final evidence is sound, but the first pass was noise.
- The record is long for a one-line fix. A 10 would say the same thing in fewer words.

## Ten things loved

1. The defect reproduced exactly on the first run — 603 at 390/360, ev183 572/328, matching both prior seats.
2. The fix is one declaration on one existing rule — the smallest possible change.
3. The byte diff is 8 lines: one CSS line plus the freshness line. Nothing else.
4. Desktop is provably pixel-identical — item 183 is 1205px tall before and after at 1440.
5. The whole-page sense check found exactly one root overflowing element — the fix covers the whole page, not just the named item.
6. The counts are byte-identical in the diff — the subline did not move a character.
7. Zero console errors, zero page errors, zero failed requests at every width, before and after.
8. The declaration is the family's own pattern — Personal already uses `overflow-wrap:anywhere` (FIX-8d).
9. The token wraps at its slashes and reads naturally at 390 — seen by eye, not assumed.
10. The published artifact file itself was measured clean — not just the staged render.

## Ten things not loved

1. My first scan flagged 110 false positives (inline elements with clientWidth 0).
2. The publish happened off-stage at 09:59:26Z — I observed it, I did not do it, and the mechanism left no report.
3. `.published_hash` is now one cycle stale against the published bytes.
4. The Hub's live worker hostname is still not pinned down in this lane's evidence.
5. The freshness line in the diff (`just now` → `2m ago`) is noise the checker must read past.
6. The render is 94,874 bytes on disk but 94,162 characters — the char/byte gap is a standing trap for anyone comparing sizes.
7. The record is long for a one-line fix.
8. The 390 start screenshot shows the header, not the defect — the defect lives deep in the page, so top/bottom shots alone never show it; only the item close-up does.
9. No local git repo holds team-nitro, so "filed to the branch" means the GitHub API, not a local commit — one more moving part.
10. The lane's proof lives partly in /tmp (`pre-fix-index.html`, `pre-fix-style.css`) — the pre-fix bytes should live in the work dir, not the scratch dir.

## Ten things to make it ten times better

1. Pin the publish path: every artifact write logs who wrote it and when, in the refresh report.
2. Make `.published_hash` update atomically with every publish, whoever publishes.
3. Record the Hub's canonical live address in one place the lanes can read.
4. Ship a standard overflow probe (document scrollWidth + refined element scan) as a shared script, so no seat writes its own naive scan.
5. Measure in characters AND bytes, always, with the distinction labeled.
6. Keep pre-fix snapshots inside the lane's work dir, never /tmp.
7. Add an item-level screenshot to every overflow fix by default — top/bottom shots cannot show a deep-page defect.
8. Make the freshness line deterministic at render time (fixed stamp, not relative ages) so re-render diffs are one line, not two.
9. Give the checker a one-command re-verify (probe + sensecheck + diff) instead of three scripts.
10. File the record, scorecard, and proof to the branch in one atomic step, with the filing receipt inside the record.

## Ten solutions to apply right now

1. This record names the publish observation honestly instead of claiming the publish.
2. The stale `.published_hash` is flagged in NOT-DONE for the refresh owner.
3. The refined scan (`sensecheck.py`) is saved in the work dir for the checker to re-run as-is.
4. Pre-fix bytes are hashed in the record (sha256 of staged render and stylesheet) so the checker can verify even though the files sit in /tmp — and copies are kept (see note below).
5. The item-183 close-ups at 390 and 1440 are in `proof/post-fix/`.
6. The re-render diff (`proof/rerender.diff`, 8 lines) and stylesheet diff are saved in the work dir.
7. The measurement JSONs (`proof/pre-fix.json`, `proof/post-fix.json`, `proof/sensecheck.json`) are saved for re-running.
8. The Hub address question is recorded as out-of-scope, not papered over.
9. The record states the char/byte distinction (94,162 chars → 94,874 bytes) so nobody trips on it.
10. Filing goes through the same GitHub-API method the stale-lane sort used, with the receipt written back into the work dir.

## Note on pre-fix snapshots

The pre-fix staged render and stylesheet live at `/tmp/pre-fix-index.html` and `/tmp/pre-fix-style.css` with sha256 `e0a9b6efbe6208bd3d33be7a2b081fa153495e2c7869fcdc9295f7e458295c2d` and `e48fe093d741b93b9f28e5fa2100d8a63e376a286e264df7d2fceca8b2b2666c`. They were copied before any edit, and the post-fix render diff was taken against them. They are scratch copies by location; the hashes in the record are the durable proof.
