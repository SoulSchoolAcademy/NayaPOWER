# RECORD — LIVING LIST PHONE-WIDTH OVERFLOW FIX

## Title

The Living List no longer scrolls sideways on a phone.

## Subtitle

One wrapping word added to one rule that already existed — the long file name in item 183 now folds inside its own box instead of pushing the whole page wide.

## Nutshell

Naya speaks for this fix: the page was perfect on a laptop and broken on a phone, because one very long file name could not bend. I gave the one rule that holds those words permission to bend — nothing else moved, nothing else changed — and now the page sits still at every width, on the phone first.

## The defect — proven before the fix

- The published Living List artifact (slug `everything-you-directed-the-living-list`) failed zero-overflow at phone widths. Two independent Playwright Firefox runs (stale-lane sort checker, captain) had already measured it; I reproduced it first-hand before touching anything.
- Pre-fix measurement (Playwright Firefox, real browser, staged render `~/workspace/project-intelligence/proof/index.html`):
  - 1440: scrollWidth 1440 == innerWidth 1440 — PASS, start and end.
  - 390: scrollWidth **603** vs innerWidth 390 — FAIL, start and end.
  - 360: scrollWidth **603** vs innerWidth 360 — FAIL, start and end.
  - Console errors 0, page errors 0, failed requests 0 at all three widths.
- Culprit: one `<p class="ev">` in item 183 ("Clarity Confirmation Act — filed as DRAFT everywhere; block rules LAW", staged-render line 205), scrollWidth 572 against clientWidth 328 at 390px (298 at 360px). It holds the unbroken long token `BRAIN/10-INTERFACES/CLARITY-CONFIRMATION-ACT-DRAFT-20261106.md`. Zero `overflow-wrap` anywhere in the render. Pre-existing week-old content.
- Counts before the fix: 40 of 204 done and proven, 2 more render as in-motion (40 + 2 = 42).

## The exact change — one declaration, one existing rule

- Base file: `~/workspace/project-intelligence/generator/_style.css`, line 77.
- Before: `.ev{color:var(--muted);font-size:18.5px;margin:8px 0 0 42px;max-width:62ch;}`
- After: `.ev{color:var(--muted);font-size:18.5px;margin:8px 0 0 42px;max-width:62ch;overflow-wrap:anywhere;}`
- That is the whole change: one declaration, `overflow-wrap:anywhere`, on the existing `.ev` rule. No new rule, no new component, no markup change, no item text changed, no color, size, spacing, or layout change anywhere.
- Carried through the existing render chain only: `generator/render.py` (line 19 reads the stylesheet verbatim) re-ran by hand; `run_refresh.py` was not run, no feed or state step ran. The staged file and the artifact's `index.html` were never hand-edited.
- Corroboration that this is the family's own pattern, not an invention: the live Personal page already carries `overflow-wrap:anywhere` (FIX-8d) in its own stylesheet.

## The measurement table — post-fix, Playwright Firefox

Method: real browser, exact widths 1440 / 390 / 360, scroll 0 AND scrolled (start and end at each width). Staged render `proof/index.html` after re-render, plus the published artifact file itself (see the publish note below).

| Width | Start scrollWidth | Start innerWidth | End scrollWidth | End innerWidth | Console errors | Page errors | Failed requests | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1440 | 1440 | 1440 | 1440 | 1440 | 0 | 0 | 0 | PASS |
| 390 | 390 | 390 | 390 | 390 | 0 | 0 | 0 | PASS |
| 360 | 360 | 360 | 360 | 360 | 0 | 0 | 0 | PASS |

Published artifact file (`~/workspace/ts-spaces/everything-you-directed-the-living-list/index.html`), measured the same way: 1440/1440, 390/390, 360/360 at start and end; 0 console errors, 0 page errors, 0 failed requests.

Item 183 (`p.ev` holding the long token), post-fix: scrollWidth == clientWidth at every width — 574/574 at 1440, 328/328 at 390, 298/298 at 360. Pre-fix it was 572/328 at 390 and 572/298 at 360.

Counts post-fix: subline reads byte-identical — "Living List items only: 40 of 204 done and proven — 2 more render as in-motion until their proof is attached." Render strip counts: done-proven 40, in-motion 57 (of which sw-37 and sw-45 render as in-motion under the proof rule), blocked 0, queued 71, needs-his-hands 3.

## The sense check — the WHOLE page, not item 183

A refined whole-page scan (every element: bounding rect past the viewport edge, plus every non-inline element whose scrollWidth exceeds its clientWidth) ran pre-fix and post-fix at 1440, 390, and 360:

- Pre-fix: exactly ONE overflowing `p.ev` on the whole page — item 183 — at 390 and 360 (scrollWidth 572); zero at 1440. Its ancestors (the item div, the board section, MAIN) showed scrollWidth overflow only as a consequence of it — 4 flagged elements, one root cause.
- Post-fix: 0 elements with a rect past the viewport edge, 0 non-inline elements with scrollWidth over clientWidth, 0 overflowing `p.ev` — at all three widths.
- Conclusion: the same one-rule fix covers the whole page. No second overflowing element exists for it to miss.

## Four-part bug-fix ratification (NOT a redesign)

1. **Re-render byte-comparison — ONLY the one declaration differs (plus the re-render timestamp).** `diff` of the pre-fix staged render (`/tmp/pre-fix-index.html`, sha256 `e0a9b6efbe6208bd3d33be7a2b081fa153495e2c7869fcdc9295f7e458295c2d`) against the post-fix staged render (sha256 `b68f958a14bf730e8ce19901f55371de5cf697fbeb5b2095e3b5a8d3538a9717`) shows exactly two changed lines: the `.ev` rule gaining `overflow-wrap:anywhere`, and the freshness line (`Last updated ~09:55 UTC / just now` → `~09:57 UTC / 2m ago`). The stylesheet diff is one line, line 77, +22 bytes. Full diff saved as `proof/rerender.diff` (8 lines) and `proof/style.diff`.
2. **Desktop pixel-identical.** scrollWidth still 1440 at viewport 1440. Item 183's height is 1205px pre-fix and 1205px post-fix at 1440 (45 lines both) — the token already fit, so the declaration changes nothing at desktop. By eye: the 1440 top screenshot post-fix shows the same header, counts, and boards as pre-fix. At 390 the item's height is 2151px pre and post (80 lines); at 360 it grows 2409px → 2438px (89 → 90 lines) — exactly one wrapped line, the fix doing its job and nothing more.
3. **Counts identical.** 40 of 204 done + 2 in-motion before and after; subline byte-identical in the diff.
4. **One declaration on one existing rule.** Never a new rule, never a new component, never a restyled page. The `.ev` rule is the harvested rule; the declaration is the family's own pattern (Personal already uses it).

All four hold. This is a wrapping bug fix. No redesign was smuggled in.

## Design-contract gate (a)–(i) + human checks H1–H5

- (a) Zero white/light backgrounds — no background touched; the page stays obsidian. Seen in every screenshot.
- (b) Every element raised/elevated — no element's elevation changed; the diff touches no elevation property.
- (c) Gauges/numbers alive — counts untouched and still live (40 / 57 / 0 / 71 / 3 visible in the 390 and 1440 screenshots).
- (d) No text-in-image — no images touched.
- (e) No bare text blocks — the fix wraps text inside the existing block; no new bare text created.
- (f) No look-alike — no component invented; the existing rule edited.
- (g) `##` format — this record uses `##` sections throughout.
- (h) No dictation-blunt phrases — no fresh wording written at all; the only new text is this record and the one CSS declaration.
- (i) Title + subtitle + nutshell + faces alternate — title, subtitle, nutshell lead this record, in that order; Naya speaks for the page.
- H1 — the fixed page reads clean at phone width by eye, no sideways movement: seen in the 390 and 360 top + bottom screenshots.
- H2 — the long token wraps and still reads naturally: seen in `proof/post-fix/ev183-390.png` — the token breaks at its slashes and hyphens (`BRAIN/10-INTERFACES/INTELLIGENT-BLOCK-RULES-LAW-20261106.md` across lines), readable, not chopped mid-word in a confusing way. At 1440 it still sits on one line (`proof/post-fix/ev183-1440.png`).
- H3 — no other line on the page changed, by eye at 1440 and 390: the byte diff allows no other change; the 1440 screenshots match pre-fix.
- H4 — the counts read the same as before the fix: 40 of 204 + 2 in-motion, byte-identical subline.
- H5 — the page still feels like the same page, no visual change at desktop: item 183 height identical at 1440 (1205px), scrollWidth identical, screenshots identical in kind.

## No-regressions

- **Live pages re-curled:** Personal `https://naya-model-personal.nayapower.workers.dev/` → HTTP 200, 1,484,185 B, sha256 `992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50` (re-curled twice, same hash). Hub `https://nayanet.app/hub` → HTTP 200, 4,990,447 B, sha256 `8a20953365d757f7224636eedaf8c18e07dcc3f2f9bae3b202d7cafb71bc1b33`. This lane ran no deploy and no publish step, so nothing in it could have changed either page; the curls confirm both are up and responding. (The guessed worker name `naya-model-hub.nayapower.workers.dev` 404s — that name was never the Hub's address; the Hub lives at nayanet.app/hub.)
- **No new store, route, schema, or note numbers:** none created. No state file, no feed file, no ledger file was written by this lane — `state/state.json` and `proof/refresh-report.json` keep their 09:55:37 mtimes, untouched.
- **The 27 seat-written rows and 2 held rows untouched:** this lane touches no ledger at all. No `state.json` write, no board write, no lane-sorting.
- **Publish note (observed, not mine):** the published artifact file `~/workspace/ts-spaces/everything-you-directed-the-living-list/index.html` was rewritten at 09:59:26Z — after my re-render (09:57:48Z) — to bytes identical to my staged render (sha256 `b68f958a…`, 94,874 bytes). I ran no publish step; the scheduled Project Intelligence refresh path carried the fixed render to the artifact, exactly as the brief prescribes ("the maker never publishes — the refresh does"). The artifact itself was then measured clean (table above). One loose end for the next refresh cycle: `proof/.published_hash` still holds the pre-fix hash (`409392e6…`, written 09:45:29Z), so the next refresh will see `changed=true` once more and re-publish identical bytes — harmless, but the hash file is now one cycle stale. That is an observation, not a defect in this fix, and not mine to repair inside this lane (no ledger/state touches allowed).
- **Branch filing:** this lane's files are filed to branch `living-list-overflow-fix-20261113` in SoulSchoolAcademy/NayaPOWER via the GitHub Contents API (same method as the stale-lane sort). No PR, no merge, no mail, no deploy, no schema change.

## Self-check ×3

- **Cycle 1 — reproduce, fix, re-measure:** pre-fix probe reproduced the defect exactly (603 at 390/360, ev183 572/328); one declaration added; post-fix probe measured 390/390 and 360/360 at start and end, counts unchanged, zero errors.
- **Cycle 2 — whole-page sense check:** refined scan pre/post at all three widths. Found the defect had exactly one root element (item 183) and confirmed zero overflowing elements anywhere post-fix; confirmed desktop geometry identical (ev183 1205px both).
- **Cycle 3 — eye + artifact:** read the 390/360/1440 top and bottom screenshots and the item-183 close-ups by eye; measured the published artifact file itself (not just the staged render) at all widths. Only after all three cycles passed did the record get written.

## Seven pre-merge answers

1. **What changed, exactly?** One CSS declaration, `overflow-wrap:anywhere`, added to the existing `.ev` rule in `generator/_style.css` (line 77), carried into the page by the existing render chain. Nothing else.
2. **Why this change and not another?** The defect is a single unbroken token wider than its container at phone width. Wrapping at the rule that holds all such text fixes the cause for every item, not just item 183; `word-break: break-all` would chop words mid-syllable everywhere, and editing the item text would falsify the evidence. `overflow-wrap:anywhere` is also the family's own pattern — Personal already uses it.
3. **What was measured, and how?** Playwright Firefox, real browser, file URLs of the staged render and the published artifact, widths 1440/390/360, scroll 0 and scrolled, plus a refined whole-page overflow scan, plus eye reads of eight screenshots. Numbers are in the table and the sense-check section above.
4. **What could break?** Only text that previously overflowed its container now wraps — by construction, only item 183's paragraph changes at phone width (one extra line at 360, none at 390, none at 1440). No layout, color, size, or spacing property was touched, so nothing else can move.
5. **What was deliberately NOT changed?** No markup, no item text, no counts, no other CSS rule, no state, no ledger, no feed, no live page, no schema, no note numbers. The artifact file was not hand-edited by me.
6. **How does the checker verify it independently?** Re-run `probe.py` and `sensecheck.py` in the work dir against `proof/index.html` (and the artifact file); read `proof/rerender.diff` (8 lines); compare the screenshots in `proof/post-fix/` against `proof/pre-fix/`; confirm the stylesheet diff is one line.
7. **What remains after this lane?** The checker seat and the captain double-check. The next scheduled refresh re-publishes (identical bytes; see the publish note). The stale `.published_hash` is a one-cycle housekeeping note for the refresh owner, not this lane.

## The five gates — before every consequential action

- Gate 1 — Is it right? Yes: it repairs a real defect for phone readers and changes nothing else.
- Gate 2 — Is it what they truly need? Yes: a page that scrolls sideways on a phone is not a finished page.
- Gate 3 — Is it mine to do? Yes: the brief names this seat maker for this exact lane and this exact file.
- Gate 4 — Is now the time? Yes: the lane was dispatched, the defect is proven, the fix is one line.
- Gate 5 — Can I prove it? Yes: reproduced pre-fix, measured post-fix in a real browser at all widths, byte-diffed the render, and read the screenshots by eye.

## DONE

- Defect reproduced first-hand pre-fix (603 at 390/360, ev183 572/328).
- One declaration added to the existing `.ev` rule in `generator/_style.css` (line 77); re-rendered through `generator/render.py` only.
- Post-fix zero overflow at 1440/390/360, start and end, staged render and published artifact file alike; 0 console/page errors, 0 failed requests.
- Whole-page sense check: exactly one root overflowing element pre-fix; zero anywhere post-fix.
- Four-part bug-fix ratification evidenced (byte diff, desktop pixel-identical, counts identical, one declaration on one rule).
- Design-contract gate (a)–(i) and human checks H1–H5 attested with evidence.
- Record, scorecard, and proof (screenshots, diffs, measurement JSONs, probe scripts) in the work dir; filed to branch `living-list-overflow-fix-20261113`.
- Live Personal and Hub re-curled responding (200); no ledger, state, schema, or live-page touch.

## NOT-DONE

- Checker seat verification — not this seat; the independent checker runs next.
- Captain double-check — not this seat.
- No PR, no merge — by the brief, filing to the branch only.
- No mail to Shawn — nothing goes to Shawn from this seat.
- The scheduled refresh's `.published_hash` is one cycle stale (see the publish note) — flagged for the refresh owner, not repaired here.
- The live Hub's canonical worker hostname was not established in this lane (`naya-model-hub` 404s; the Hub answers at nayanet.app/hub) — out of scope, noted only.
