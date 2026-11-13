# HUB LIVE LEG — Terra (INFRA/roads deploy seat) — 2026-11-13

## Authorization (Shawn's hand, recorded)

- **16:24Z — live tap:** Shawn: "make it so that the habit is live." Authorizes this
  live leg: the proven fixed Hub shell (bars shell, sha `a687f16a…`) goes live on
  nayanet.app — a restoration, not a top-up.
- **16:28Z — SN-2696 publication tap (UPDATE to the brief):** Shawn: "Yes, publish
  SN-2696 as the first public note." The boundary in the brief changes: SN-2696's
  public publication is APPROVED and rides this live leg. `/s/sn2696` rendering the
  note live is now an expected live outcome, not a gated check. No publication flag
  is flipped by this seat — the phase-1 worker's `PHASE1_CANDIDATE` allowlist already
  carries `sn-2696`, and the shell's `SLUG_MAP` resolves it; publication IS the live
  render.

## What this leg deploys (exactly)

1. The fixed shell — bars round, branch `hub/shell-bars-20261113`, tip `30324c36`,
   5,559,180 B, sha `a687f16a666f27875dcc2cdb6dbe5fca113cf7eed610d76ff5b39ee8fc8d02ac`
   — carrying BOTH fixes (slug: `SLUG_MAP` first in `findNoteBySlug` + install-modal
   suppression on note landings; bars: 9 round black circles + 3 ultimate gems).
2. That shell re-baked with the CURRENT baked notes (the 200 most recent from the
   live template, SN-2766 in the set, SN-2696 in the set) — see the bake-template
   proof below. The bars shell as filed carries older baked notes (SN-2766: 0x);
   shipping it as-is would roll the Hub's baked notes backwards.
3. `HUB/wrangler.toml` +4 `run_worker_first` patterns (`/robots.txt`, `/sitemap.xml`,
   `/images`, `/images/*`) on top of the base 8. No phase-2 patterns.
4. The UNCHANGED phase-1 worker `hub-worker-phase1.js` (49,174 B,
   sha `8ee4f8594a694b851e614348e7edf44baf882d6ccefab9d3cdc474707ab192d6`).
5. The `/hub/feed` one-line fix: `src="js/naya-search.js"` → `src="/js/naya-search.js"`.
6. The bake template fixed so the next SN sync cannot revert any of it (see below).

No other live touch, no merge of anything else, no mail, no redesign.

## Live BEFORE (first-hand, 16:26–16:30Z)

- `GET https://nayanet.app/hub` → 200, **4,992,296 B**,
  sha256 `fa81a5f4a70052fefff76137b3866df2271cfeeb2e52e2a969af55e2bf9b83ac`
  (saved: `work/live-hub-before.html`).
- Markers: `findNoteBySlug` **0** · `SLUG_MAP` **0** · `smart-notes/:slug` **0** ·
  `notes/:slug` **0** · `noteView` **0**. The bars round's "live 8a209533" baseline
  is stale, as the brief warned — live moved to the 16:17Z SN-sync rebake.
- Baked notes in live: `SN-2766` 5x, `SN-2696` 6x (note text), `sn2696` 2x.
- Live is byte-identical to the bake template (see proof).

## The bake template — PROVEN in writing (the revert trap, closed BEFORE deploy)

**The template the sync hook uses:** `~/workspace/user/files/index-2.html`.

Proof of use — `~/workspace/factory-pipeline/sync-smart-notes.py`,
`update_hub_and_deploy()` (lines ~1183–1250): it reads
`hub_path = '/home/hatch/workspace/user/files/index-2.html'`, injects the live
notes via `inject_live_notes()`, writes it back atomically, rebuilds
`feed-live.json`, then runs `deploy.py <hub_path> hub`, which deploys worker
`hub` (nayanet.app) from that file. Every new-note sync re-bakes from this file
and redeploys live from it.

**Does it carry the route? NO — proven first-hand, 16:30Z:**

| File | Bytes | sha256 (first 12) | findNoteBySlug | SLUG_MAP | smart-notes/:slug |
|---|---|---|---|---|---|
| `~/workspace/user/files/index-2.html` (mtime 16:09Z) | 4,992,296 | `fa81a5f4a700` | 0 | 0 | 0 |
| Live `GET /hub` | 4,992,296 | `fa81a5f4a700` | 0 | 0 | 0 |

Live == template byte-for-byte (same sha). The template is the pre-route shell
(the rebake briefs call it the STALE bake source, 5,068,216 B base, predating the
route) with the 16:09Z notes injection. **Had this leg deployed the fixed shell
without fixing the template, the next SN sync would have rebaked this route-less
file and redeployed it live, killing the restoration within the hour. The trap
was real and is closed below — no deploy happened before this proof.**

**The fix (applied before any deploy):** the template is replaced by the fixed
bars shell re-baked with the template's own current 200 live notes, plus the
`/hub/feed` absolute-src fix — built by `build-live-shell.py` in this work dir,
using the sync's own remove-then-inject steps (`inject_live_notes`, same
anchors, same script-safe JSON escaping). The new template was verified
(marker counts, 200 notes, SN-2766 + SN-2696 present, node `--check` on the
notes script block, CSS brace gate) BEFORE it was written, and written
atomically (temp + rename in the same directory, size-checked) over
`index-2.html`, with the pre-fix bytes preserved as
`work/index-2-BEFORE-20261113.html` (sha `fa81a5f4…`, verified identical).

**Second revert path, also closed:** the sync deploy path carries its
`run_worker_first` from local code, not from `wrangler.toml` —
`deploy_hub_assets.py` module default (base 8) and `deploy.py`
`HUB_ASSETS_CONFIG` (base 8). A sync redeploy after this leg would otherwise
have reverted the +4 config (robots/sitemap/images back to shell-served).
Both defaults are updated to base 8 + 4 in this round (local tooling only,
recorded in §5) so every future sync deploy carries the same config as the
repo. After the merge, main's `HUB/hub-worker.js` IS the phase-1 worker, so
the sync's `stage_hub_assets` (which fetches the worker from main) carries
phase-1 on every future sync deploy too.

## The live deploy path (why this shape sticks)

Live is served by worker `hub` (nayanet.app). Two writers can move it:

1. **GitHub auto-deploy** (`.github/workflows/deploy-hub-cloudflare.yml`): push
   to main touching `HUB/app/**`, `HUB/hub-worker.js`, or `HUB/wrangler.toml`
   → `wrangler deploy` in `HUB/`.
2. **The SN-sync hook** (`sync-smart-notes.py` → `deploy.py … hub`): on every
   new-note sync, stages `HUB/app` from main, overlays the baked template +
   fresh feed, deploys worker `hub` with main's `HUB/hub-worker.js`.

This leg lands the SAME bytes through BOTH paths so neither can revert the
other: the branch `hub/live-leg-20261113` carries the fixed shell (re-baked,
feed-fixed) as `HUB/app/index.html`, the unchanged phase-1 worker as
`HUB/hub-worker.js`, and `wrangler.toml` +4; merging it to main fires the
auto-deploy; the fixed template + the +4 deploy defaults + main's worker now
being phase-1 make every future sync deploy reproduce the same live state.

## Template fix — RESULT (16:32Z, verified by re-read)

`index-2.html` is now **4,960,598 B**,
sha256 `64380ef312fabf22682288968ef8acf95d1270b1fe5f3eeb44f98e356d69cded` —
identical to `work/index-intel-today-LIVE.html`. Markers: `findNoteBySlug` 4 ·
`SLUG_MAP` 2 · `smart-notes/:slug` 7 · `SN-2766` 5x · `SN-2696` 7x · baked
notes parsed back: exactly the 200 live notes, list-identical to the extract.
`/hub/feed` fix present (`src="/js/naya-search.js"` 1x, relative 0x).

**Next-sync proof (16:33Z, the sync's OWN function, not a re-implementation):**
`sync-smart-notes.py::inject_live_notes` run against the new template with the
same 200 notes reproduces the route (4/2/7), the 200 identical notes, the
absolute search src, and passes node `--check`. The output differs from the
template by exactly **2 bytes of script indentation whitespace** before the
`const NOTES` line (the anchor-indent artifact of the remove-then-inject) —
JS-identical, no functional difference, and stable across runs (the indent
carries, it does not accumulate). The next sync therefore rebakes the FIXED
shell with fresh notes; it cannot resurrect the route-less shell. The trap is
closed in substance, stated honestly in bytes.

## The deploy (16:34–16:37Z)

**Branch + merge (the GitHub path).** Branch `hub/live-leg-20261113` filed from
main head `536d4cc2` (re-read first-hand at filing; unchanged since 16:30Z),
one commit `03203ccd80fca23e46248fc8433c8e6c7891ecd7` carrying exactly the three
HUB files — `HUB/app/index.html` (4,960,598 B, sha `64380ef3`), `HUB/hub-worker.js`
(phase-1, 49,174 B, sha `8ee4f859`), `HUB/wrangler.toml` (+4). Read-back
verified via raw (index byte-identical, worker identical, wrangler +4 present);
the contents-API read-back returned 0 B for the 5 MB shell with the blob sha
matching — the API's 1 MB content limit, not a mismatch, and the raw read-back
is the proof. Compare: ahead 1, behind 0, merge-base = main head, exactly the
three files. **Merged 16:34:26Z** via the merge API: merge commit
`aca7b075fcc226eb44e3065af34f8a65d80d7721` (parents `536d4cc2` + `03203ccd`,
tree `48bb0556` — the branch tree, clean merge). Main's `HUB/app/index.html`
re-read after the merge: sha `64380ef3`. The auto-deploy workflow fired; live
`/hub` served sha `64380ef3` by 16:35:07Z (first poll, ~40 s after the merge).

**The stale-feed catch (found by my own curl battery, fixed in-round).**
The workflow deploy served the repo's stale `HUB/app/feed-live.json` —
**877 notes, SN-2696 and SN-2766 ABSENT** — because the workflow deploys
`HUB/app` as-is and the fresh feed (1,058 notes) lives only in the sync's
file. Consequence, measured live 16:36Z: bot `GET /s/sn2696` → **404 "Note
not found"** (the phase-1 worker renders its bot page FROM the served feed —
`phase1LoadFeed` → `phase1FindNote` — and the note was not in it). The live
worker script itself was verified phase-1 (bundled 29,614 B; `PHASE1_CANDIDATE`
4x, `phase1LoadFeed` 4x, `sn-2696` 1x). **Fix, same hour:** the sync's own
deploy path — `deploy.py ~/workspace/user/files/index-2.html hub`
(`deploy_hub_converged`: stages `HUB/app` from main `aca7b075`, overlays the
live shell + the fresh 1,058-note feed, script = main's `HUB/hub-worker.js` =
phase-1, `run_worker_first` +4 by the new default). Result: manifest 39 files
/ 21,975,763 B, 1 bucket / 1 file uploaded (only the feed was new), PUT `hub`
success, etag `81fbb511c95657ca`. Live re-verified immediately after (see below).
The workflow path alone is NOT sufficient for a live Hub deploy — it ships the
repo's stale feed. Open trap, named not fixed (see §NOT-DONE): main's
`HUB/app/feed-live.json` is still the stale 877-note copy; any future
workflow deploy will serve it until the next SN sync redeploys. The durable
fix (refresh that file on main, or make the workflow overlay the fresh feed)
is a captain's call — it is a fourth main file outside this leg's named list.

## Live AFTER (first-hand, 16:37Z — curl battery)

| Check | Result |
|---|---|
| `GET /hub` | 200, **4,960,598 B**, sha `64380ef3` — the deployed bytes exactly |
| Markers on live | `findNoteBySlug` 4 · `SLUG_MAP` 2 · `smart-notes/:slug` 7 · `SN-2766` 5x · `SN-2696` 7x · `src="/js/naya-search.js"` 1x, relative 0x |
| Browser `/s/sn2696` | **302** → `https://nayanet.app/#/smart-notes/sn2696` |
| Bot `/s/sn2696` | **200**, 14,285 B, title "The Infinite Smart Feeds — one feed per topic · NayaNET", canonical `/s/sn2696` |
| Browser `/s/sn0131` | **302** → `https://nayanet.app/#/smart-notes/sn0131` |
| Served `feed-live.json` | 200, 8,172,042 B, **1,058 notes**, SN-2696 ✓, SN-2766 ✓, newest SN-2766 |
| `/robots.txt` / `/sitemap.xml` | 200, 321 B real text / 346 B real XML (sitemap lists `/s/sn2696`) — the +4 working |
| `/hub/feed` | 200, the shell (4,960,598 B) |
| `/js/naya-search.js` | 200, 20,424 B, `application/javascript` — the absolute-src fix resolves to real JS |

Live BEFORE → AFTER: `fa81a5f4` (4,992,296 B, 0 route markers) → `64380ef3`
(4,960,598 B, route + bars + current notes). The shell, the worker, and the
feed all match the deployed set.

## Browser verification — walked from the LOGIN page (VM Playwright Firefox, alive)

The cold shared-link flow, per width (fresh context each): load the live deep
link `https://nayanet.app/#/smart-notes/sn2696` → entrance → enter name
"Probe Visitor" → note. Plus Hub-direct `https://nayanet.app/hub#/smart-notes/sn2696`.

| Width | Note renders | Title | Hook | IN A NUTSHELL | Boards | Upper bar | Trio | Install overlay (first paint / +3.5 s) | Console / page errors | Overflow |
|---|---|---|---|---|---|---|---|---|---|---|
| 390 | yes | SN-2696 · SYSTEM / INTELLIGENCE / FEEDS | yes | yes | 1 | 9 circles, 44px, 50% | 3 gems, 27px, 50% | no / no | 0 / 0 | 0 |
| 1440 | yes | same | yes | yes | 1 | 9 circles, 46px, 50% | 3 gems, 38px, 50% | no / no | 0 / 0 | 0 |
| 360 | yes | same | yes | yes | 1 | 9 circles, 44px, 50% | 3 gems, 27px, 50% | no / no | 0 / 0 | 0 |

- Labels (all widths): MAIL, DASHBOARD, BUSINESS, SPACE, GROWTH, CONNECTIONS,
  SMART LISTS, REPORTS, 10 APPS above; Personal / Business / Thing below.
  Gem SVGs three distinct (lengths 564 / 540 / 676). No Activity pill.
- Screenshots read by eye: `probe-live2-note-1440.png` (nine round black
  circles, three gems, full note with date, CREATE SPACE / FAVORITE / SAVE,
  LOVE/LIKE, SHARE INTEL — obsidian, nothing clipped) and
  `probe-cold-B-390.png` (same at phone width).
- Hub-direct `/hub#/smart-notes/sn2696` at 390 renders the note at 6 s and
  12 s with zero page errors — the Hub itself is proven independent of the
  entrance.
- `/hub/feed` loads clean at all three widths: 0 console errors, 0 page
  errors, 0 overflow (the pre-existing page error is gone — the absolute
  script src resolves to real JS).
- **360 timing note, characterized:** at +0.8 s after the title changed, the
  upper bar had not mounted yet (0 pills) in one run; at +1 s it is there
  (9 pills, 44px, 50%), stable at +3/+6/+10 s. First-paint mount lag at one
  width, not an absence — the bar is present in every settled read.
- **Re-entry behavior, observed (entrance session, not this shell):** a visitor
  who has already entered and then follows a FULL-navigation `/s/sn2696` link
  lands back on the entrance form and must enter their name again to reach
  the note (proven at 390, +5 s / +8 s, entrance title). The cold-link flow
  (the real shared-link flow) works — entrance → name → note — and in-Hub
  note links use client-side routing, so this bites only full-navigation
  link clicks from inside the Hub. Named here; the fix (entrance session
  persistence) belongs to the entrance/walk area, not this leg.

**SN-2696 is published live.** `/s/sn2696` renders the note live as the first
public note — browser (via the entrance) and bot (200, in initial HTML).
No publication flag was flipped by this seat: the worker allowlist already
carried the candidate and the shell already carried the map; the live render
IS the publication, on Shawn's 16:28Z tap.

## Self-checks (three rounds) + seven pre-merge answers

**Round 1 (the build):** template proven route-less in writing before any
deploy; live shell built from the asserted bars shell + the extracted 200
live notes (parsed back list-identical) + the feed fix; node `--check` and
CSS gate pass; template written atomically and re-read identical; the sync's
own inject function re-run on the new template preserves everything
(+2 B whitespace only). Found the deploy-defaults +4 revert path and aligned
both defaults.
**Round 2 (the deploy):** branch filed + read back byte-exact (raw), merge
clean, workflow landed live in ~40 s; the curl battery caught the stale-feed
bot 404 the workflow deploy shipped — and the Direct Upload fixed it the
same hour with the fresh feed, re-verified immediately.
**Round 3 (the browser proof):** the walked cold-link flow renders the note
at 390/1440/360 with the bars measured (not eyeballed once); the 360
first-paint lag characterized by re-measurement instead of smoothed over;
the re-entry friction probed separately and named; `/hub/feed` re-proven
clean.

**Score: 9/10, honestly.** What earns the 9: the revert trap proven and
closed before any deploy (template + sync proof + deploy defaults); the
branch + merge + both deploy paths verified byte-exact; the full live
battery green (shell sha, markers, bot 200, feed 1,058, robots/sitemap
real); the note renders walked from the login page at all three widths with
the bars measured and screenshotted. What keeps it from 10: the workflow
deploy shipped a stale feed and a bot 404 that my own battery had to catch
— fixed in-round, but the standing trap (stale `HUB/app/feed-live.json` on
main) is still open for the next workflow deploy, and the re-entry
name-again friction sits with the entrance, not fixed here.

**Seven pre-merge questions (answered in writing; the merge already landed
on Shawn's tap):**
1. Three self-checks done? Yes — rounds 1–3 above, each finding new things
   (the +4 defaults revert; the stale-feed bot 404; the 360 mount lag +
   the re-entry friction).
2. Honest 9+? Yes — 9/10, deduction named (the stale-feed catch + the open
   workflow trap).
3. Blast radius named? Live worker `hub` only: shell + worker + wrangler
   config + feed overlay, all read-back verified. Main gained exactly the
   three HUB files in one merge commit. No other worker, page, registry,
   or feed file touched on main. Local tooling: two deploy-default lines
   (+4) and the bake template — both recorded here. No mail. Nothing to
   roll back except a re-deploy of the same set.
4. Checks green? Yes — curl battery green after the Direct Upload; browser
   proof green at 390/1440/360; one known exception, named: the re-entry
   name-again behavior (entrance session, out of scope).
5. Five gates? Yes: right (the live Hub had lost the note route entirely;
   the restoration returns it through the approved fixes, nothing faked);
   truly needed (SN-2696's publication + the bars Shawn screenshotted both
   waited on this leg); mine to do (Shawn's 16:24Z tap + 16:28Z publish tap,
   named scope, no other live touch); now (the trap was proven closable
   first, then deployed); provable (every sha, count, and screenshot in
   this record, read first-hand).
6. Real proof? Yes — live bytes, shas, marker counts, bot HTML, browser
   measurements and screenshots, all first-hand in this round.
7. No silent known defects? None silent — the stale repo feed trap, the
   re-entry friction, the 360 mount lag, and the +2 B sync whitespace are
   all named here.

## DONE / NOT-DONE

**DONE:** authorization recorded (16:24Z live tap, 16:28Z SN-2696 publish tap)
· live BEFORE measured first-hand · bake template proven route-less in writing
and FIXED (fixed shell + current 200 notes + feed fix, atomic write, re-read
identical) · next-sync proof with the sync's own inject function · deploy
defaults aligned to +4 (both files) · branch filed (one commit, read-back
verified) · merged to main (aca7b075, clean) · workflow deploy verified live
· stale-feed bot 404 caught by the battery and fixed by Direct Upload the
same hour · full live verification: curl battery green, walked cold-link
flow at 390/1440/360, Hub-direct control, `/hub/feed` clean, bars measured
· SN-2696 published live as the first public note · record + scorecard +
receipt in the work dir.
**NOT-DONE (not mine, or owed elsewhere):** the stale `HUB/app/feed-live.json`
on main (877 notes) — any future workflow deploy serves it until the next SN
sync redeploys; durable fix is a captain's call (refresh the file on main or
make the workflow overlay the fresh feed) · the re-entry name-again friction
(entrance session persistence — walk/entrance area) · the 360 first-paint
mount lag (characterized, sub-second, no action) · checker + captain
double-check of this leg (owed after the fact — the deploy itself was on
Shawn's tap, the verification above is this seat's first-hand record).
