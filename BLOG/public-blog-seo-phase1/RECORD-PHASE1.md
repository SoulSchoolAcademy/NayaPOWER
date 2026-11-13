# RECORD — Public Blog + SEO/AI System, Phase 1 (maker seat)

**Round:** Public Blog + SEO/AI System Build, Phase 1 only (repair the
public-serving + privacy foundation, proven on ONE real note).
**Maker seat:** Phase-1 Maker · **Captain:** Naya Nitro Narzan ·
**Shawn's order:** 22:51Z + redirect 23:04Z + two-stage plan 23:33Z,
2026-11-12. **Brief:** `MAKER-BRIEF-PUBLIC-BLOG-SEO-INTEL-TODAY-20261112.md`
(checker 9/9). **Branch:** `public-blog/seo-system-20261112`.
**Staging worker:** `naya-public-blog-staging` —
https://naya-public-blog-staging.nayapower.workers.dev/
**Work directory:** `~/workspace/team-nitro/public-blog-seo-20261112/`
**Date of this record:** 2026-11-13 ~00:10Z. **Status: DONE, staged,
verified by my own probes. No live deploy, no PR, no merge** — publication
to the internet is Shawn's hand; the live deploy waits for his tap.

## The verdict, in one line

The three broken public routes are repaired in staging on one real note,
with denial proven for everything else: **87/87 curl probes pass,
Playwright 1440/390/360 all pass (zero overflow, zero console errors),
deployed worker bytes are byte-identical to the built worker.**

## 1. What was done — the 10 steps

1. **Canonical source restored + owners confirmed.** Base =
   `HUB/hub-worker.js` on main, byte-identical to the live worker
   (sha256 `701c2bb85a1931e288a3ceb0eb7243ac1238e3cc7359bbec73a9d6d0c9ecd24c`,
   27,225 B, main tip `9868243acf1382df5d03c1a104d60f465cef48f7` at check
   time). Hub/blog lane = this round (Nitro owns Hub UI). Feed owner =
   sibling round coordinator `58af0570`. Feed data = intelligence-loop
   regen (987 notes at build time, revision
   `registry@37c542f6f1525de29ed31e04ce7d06f01112065ad4fd48ccb17bc70d3e6f7ea7`).
2. **Deployed routing inspected.** Live `nayanet.app`: `/robots.txt` →
   200 text/html 5,011,973 B (Hub HTML); `/sitemap.xml` → same;
   `/s/sn2696` → 302 to `/#/smart-notes/sn2696` for browser AND
   Googlebot UA. Root cause: `HUB/wrangler.toml` `run_worker_first`
   lists 8 patterns but NOT `/robots.txt` or `/sitemap.xml`, so the
   assets layer answers them with the SPA fallback before the worker
   runs; the worker also had no handlers for them. `/s/*` IS in the
   list, so the worker runs and 302s every client to the hash route.
3. **Reproduced in isolated staging** (pre-fix worker): robots 200
   text/html 5,017,018 B; sitemap same; `/s/sn2696` browser 302 to the
   walk landing; Googlebot 200 but the phase-2 intermediate's page
   (wrong canonical `/note/`, title 74 chars, dropped "What changes
   now"). Denial already worked in the intermediate.
4. **Fixed the smallest seam.** Phase-1 additions wrap the live
   `renderNote`/`serveNote` (untouched — the feed regen mirrors their
   parsing); they add only: robots/sitemap handlers, the bot note
   page, the cover image, slug normalization, GET-or-HEAD routes.
   No phase-2 code, no Hub app file touched
   (`~/workspace/user/files/index-2.html` untouched).
5. **Candidate proposed (NOT approved): SN-2696, "The Infinite Smart
   Feeds"** — see §2 below.
6. **Note served in initial HTML** with accurate meta, one canonical,
   real image — see §3.
7. **Valid robots.txt + sitemap.xml, only approved public URLs** —
   exactly 2 URLs in the sitemap (Hub root + the candidate note).
8. **Intel Today + Smart Feed highlights → identical note/revision**
   at the data level — see §4 (the card href form is a named phase-2
   gap; step 8 is NOT claimed fully complete).
9. **Independent discovery + denial test** — see §5.
10. **Proof preserved here, on the branch, and in this record.**

## 2. The candidate note proposal (propose only — NOT approved)

- **Candidate: SN-2696 — "The Infinite Smart Feeds"**
  (`IB-SMART-NOTE-20261112-the-infinite-smart-feeds`), created
  2026-11-12T19:01:19Z, feed `personal: False`, `kind: official`,
  topic "System Intelligence". Shawn's dictation read back; he reacted
  👍 at 18:52Z confirming the read-back. It is the note Tree sampled
  and the captain verified. **Alternate: SN-2695** (vision/mission).
- **The captain brings it to Shawn; live deploy waits for his tap.**
- **SN-2696 has NO registry entry** (SN-2692–2699 are all absent from
  `.naya/memory/smart-notes/index.json`; of 68 SN ids in the feed only
  21 are in the registry; all 21 registry-present feed notes are
  `scope: PRIVATE` except SN-002). **There is currently no note with a
  clean public-approved scope.** The phase-1 page therefore renders
  from the **live feed**, not the registry. **Publication permission
  was NOT inferred from registry/feed presence** (Tree's contract).
- **Systemic, learned during this round (MEMORY.md 23:51–23:58Z):**
  SN-2690..SN-2739 (50 notes) are all loop-filed without captures and
  all unregistered; the registry-append round STOPPED correctly rather
  than invent lineage. The **Naya 5 safety repair round** (branch
  `naya5/safety-repair-vanish-2692-2716`) is the unblocker — its door
  step mints captures + registry entries from the published pages.
  A registry-backed public note is therefore a **later** step, after
  that repair proves the mechanism.
- **Free/paid entitlement is an open live gate** (Tree's report P0 #4):
  merge brief `brief-07-intel-today.md` describes FREE top-3-per-day
  preview vs PAID full view (SN-1862). Reconcile before publishing or
  indexing a paid section. This is a brief stop condition for LIVE
  publication — staging proof proceeds, live does not.

## 3. What the staged note page is (measured, not claimed)

- **URL:** `https://naya-public-blog-staging.nayapower.workers.dev/s/sn2696`
- **Title (55 chars):** "The Infinite Smart Feeds — one feed per topic ·
  NayaNET". **Description (154 chars):** "Not one feed like Facebook —
  infinite feeds, one for every topic, and the whole system exists
  because of them: they are the original intention, ten years…"
  (hook trimmed at a word boundary, verbatim from the note's own hook).
- **One canonical:** `…/s/sn2696`. Aliases `/note/`, `/notes/`,
  `/smart-notes/` serve the **same bytes with the same canonical** —
  no second article (Tree G1.1). Browsers keep the existing 302 into
  the Hub (`/#/smart-notes/sn-2696`, Shawn's ruling 2026-11-06/07).
- **7 boards** (In a Nutshell, Human, Child, Grandma, Naya, Why It
  Matters, The Learning — "What changes now" maps to The Learning;
  the phase-2 file dropped it, this parser keeps it). The trailing
  filing footer ("Filed by Intelligence Loop run 198…", "Paired Naya
  Note:…") is **internal provenance and is stripped** from the public
  rendering. "Two views" / "The layout" / "The difference" / "The
  build" are inline markers inside the single Nutshell paragraph and
  are split out by the parser; elaborations stay in the nutshell.
- **JSON-LD:** one honest block, BlogPosting + BreadcrumbList. No
  FAQPage/HowTo (both out of Google's search gallery), no llms.txt,
  no meta keywords, no visible SEO score.
- **Byline:** By Naya · Published 2026-11-12 · System Intelligence.
  Top bar (Intel Today / Hub / Open in the Hub), breadcrumb, footer
  naming the served feed revision.
- **Cover image:** `/images/infinite-smart-feeds-cover.png` — 200,
  image/png, 252,607 B, the real public NayaNET mark (the Hub's
  `icon-512.png` bytes) under a descriptive filename. Alt + caption
  say truthfully what it is: the network's mark, **not** a picture of
  the feeds. **A real note-specific image is owed** (Shawn / a Naya
  makes it; the cover slot is the deliverable until then).
- **"MEMORY.md" appears in the page text** — that is the note's OWN
  words ("filed in MEMORY.md as THE INFINITE SMART FEEDS"), not a
  machinery leak. No coordinator ids, no internal paths in the HTML.
- **Dual-spec §2 block-shape conformance is explicitly NOT claimed**
  (40–60-word nutshell, perspectives, connections) — that shaping is
  the phase-2 auto-tagging machine's job, measured by its own 5-point
  pass/fail test.

## 4. Step 8 — identical note + revision (data level, proven)

- The staged Hub shell embeds the SN-2696 hook ("Not one feed like
  Facebook") and the staged `/feed-live.json` serves 987 notes,
  revision `registry@37c542f6…`, SN-2696 present with the hook verbatim.
- The Hub fetches `/feed-live.json` live-first and the phase-1 worker
  reads the SAME `/feed-live.json` from the same assets binding —
  identical note + identical revision by construction. The note page
  footer names the revision.
- **Named phase-2 gap (step 8 NOT fully complete):** Hub card links
  are built at runtime by JS (no `#/smart-notes/`, `/note/`, or `/s/`
  hrefs in static shell bytes). Phase 2 must make them ordinary
  `<a href="/s/sn2696">` per Tree G1.1.

## 5. Probes — the receipts

**Curl suite `probe-phase1.py`: 87 passed, 0 failed** (final run,
2026-11-13 ~00:05Z, against the final deploy). It asserts: robots
200 text/plain with all rules (Googlebot, Bingbot, OAI-SearchBot,
Claude-SearchBot, PerplexityBot allow; GPTBot/ClaudeBot disallow;
`Disallow: /api/`; Sitemap line; no nosnippet), identical for
Googlebot UA; sitemap 200 application/xml, parses, exactly 2 URLs,
lastmod 2026-11-12, no private/feed/api URLs; note 200 for
Googlebot/OAI/Claude/Perplexity/plain-curl with title/description
lengths, one canonical, H1, hook, 7 boards, JSON-LD, image, top bar;
browser 302 to `/#/smart-notes/sn2696`; denial 404 + `X-Robots-Tag:
noindex, nofollow` + `no-store` + body "Note not found" for sn0587
(registry-private), sn9999 (unknown), sn2695 (other public-looking,
not allowlisted), and `/note/sn0587`; aliases serve the same
canonical; cover image bytes; HEAD 200 with the right content-type
on robots/sitemap/note/cover; regressions — `/` entrance 200,
`/hub` 200 titled Intel Today, `/sw.js` 200, `/pi` 307 (see below).

**Playwright `probe-phase1-playwright.py`: 1440, 390, 360 — ALL PASS.**
Zero horizontal overflow (0/0 at scroll 0 and scrolled), zero console
errors, zero page errors, 7 boards, title/H1/hook correct at every
width. Screenshots: `phase1-shots/note-1440.png`,
`note-390.png`, `note-360.png` (+ `results.json`). VM browsers were
dead per TOOLS.md (since ~17:32Z 2026-11-12) but **recovered** —
Playwright Chromium launched and loaded pages; the probe used the
localhost forwarding proxy
(`~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py`,
already running on 127.0.0.1:18080 — my start attempt failed to bind
because it was already up).

**Deployed-bytes proof:** final deploy PUT success, worker
`naya-public-blog-staging`; `get-script` read-back sha256 matches the
built `hub-worker-phase1.js` (49,174 B) exactly.

**Defects found and fixed by the three self-check rounds** (each round
found NEW things — see §7):
1. Slug normalization: the allowlist compared the raw slug, so
   `/s/sn2696` (no hyphen) denied the candidate itself. Fixed with
   `phase1CanonicalSlug()` (sn2696/sn-2696/SN-2696 → sn-2696).
2. Footer overflow at 390/360 (overflowX 80/110): the unbroken
   64-char feed-revision hash in the footer. Fixed with
   `footer{overflow-wrap:break-word}` — full hash kept, wraps now.
3. HEAD fall-through: HEAD on the phase-1 routes fell through to the
   assets layer and came back text/html (the SPA shell). Fixed with
   GET-or-HEAD route conditions.
4. HEAD note 503: the feed/cover subrequests forwarded the original
   request, carrying HEAD into the assets binding, which failed it —
   so HEAD note requests returned 503 "Feed unavailable". Fixed with
   explicit GET subrequests in `phase1LoadFeed` and
   `phase1CoverImage`. (Two 503s seen in the minute right after the
   fix deploy were deploy propagation on some PoPs — 8/8 clean after.)
5. Probe bugs of my own: the HEAD helper read the proxy CONNECT
   response's status (always 200) instead of the last HTTP block;
   a reused `ct` variable made the robots content-type check read the
   note's type. Both fixed in `probe-phase1.py`.

**`/pi` staging 307 — pre-existing, NOT a phase-1 regression.** The
`/pi` handler block in the built worker is byte-identical to the live
base (live `/pi` is 200); the staging assets binding answers the
`/pi/index.html` subrequest with a 307 where live answers 200. Out
of phase-1 scope; recorded here as a staging gap.

**Edge notes:** a transient Cloudflare 503 (no X-Robots-Tag) was seen
once during probing; the probe retries once on 5xx. Case-insensitive
paths work (`/S/SN2696` → 200); trailing slash works; query strings
on robots work.

## 6. The live handoff (what Shawn's tap deploys)

- `HUB/wrangler.toml` on main: add 4 `run_worker_first` patterns to
  the base 8 — `/robots.txt`, `/sitemap.xml`, `/images`, `/images/*`.
  **No phase-2 patterns** (`/feed`, `/cluster`, `/api/seo`,
  `/api/intel-today/tags`).
- The worker change: `hub-worker-phase1.js` (built from
  `hub-worker-harvested-main.js` + `phase1-additions.js` via
  `build-phase1-worker.py`) via the branch deploy workflow.
- **Live deploy waits for:** (a) Shawn's approval of the candidate
  note SN-2696 for public publication; (b) the free/paid entitlement
  reconciliation (Tree P0 #4); (c) the checker's independent
  verification. Nothing in this round touches live.

## 7. Self-checks (three rounds) + seven pre-merge answers

**Round 1** (first probe run, 48 passed / 34 failed): found the slug
bug; fixed it. Also recorded the `/pi` 307 and the phase-2
intermediate's wrong canonical + dropped section.
**Round 2** (this session, eye on the served page + screenshots):
found the footer overflow at 390/360; found HEAD falling through to
the SPA shell; confirmed the 1440 page is genuinely good (obsidian
boards, jewels, top bar, cover, hook); named the MEMORY.md mentions
as note content, not a leak.
**Round 3** (this session, edge cases + code re-read): found the HEAD
503 subrequest bug; found the two probe bugs (CONNECT first-match,
variable reuse); confirmed deployed==built and 8/8 HEAD clean after
propagation. Each round found NEW defects — none was a re-run of the
last.

**Score: 9/10, honestly.** What keeps it from 10: the cover image is
a stand-in (real note-specific image owed); the card href form is a
phase-2 gap; no registry-backed publication exists yet (systemic —
Naya 5 repair is the unblocker); the free/paid entitlement is
unresolved; no live deploy (by design — his tap). All named, none
hidden.

**Seven pre-merge questions** (answered for the staged/filed state —
no merge happens in this dispatch):
1. **Three self-checks done?** Yes — rounds 1–3 above, each finding
   and fixing new defects.
2. **Honest 9+?** Yes — 9/10 (gaps named above).
3. **Blast radius named?** Staging worker `naya-public-blog-staging`
   only + branch `BLOG/public-blog-seo-phase1/` files. Live
   `nayanet.app` untouched; no main writes; no PR; no merge.
4. **Checks green?** 87/87 curl probes; Playwright 3/3 viewports;
   `node --check` clean; deployed bytes == built bytes (sha match).
5. **Five gates?** Yes — right (repairs a broken public surface
   without touching live); truly needed (crawlers get the shell
   today); mine to do (briefed maker seat, staging only); now (the
   round is live, the fix is staged); provable (live bytes cited).
6. **Real proof?** Staged URLs + curl outputs + screenshots +
   etag/sha, all in this record and the probe outputs.
7. **No silent known defects?** None silent — every known gap is
   named in this record (§3 cover, §4 href form, §2 registry +
   entitlement, §5 `/pi` 307 + transient 503).

## 8. Findings for phase 2 (handed forward, not built)

- The phase-2 intermediate used `/note/` as canonical — a second
  article URL conflicting with the live `/s/` route (Tree G1.1).
  Phase 1's canonical is `/s/sn2696`; phase 2 must keep it.
- The phase-2 parser dropped "What changes now"; the phase-1 parser
  keeps it (as The Learning).
- Phase 2 must make Hub card links ordinary `<a href="/s/sn2696">`
  (step-8 gap) and run its own 5-point block-shape pass/fail test
  (phase 1 does not claim §2 shape conformance).
- The dashboard alignment round (branch `dashboard/alignment-20261112`)
  STOPS at Step 1 if the blog round hasn't defined the funnel schema
  yet — the funnel schema is defined by this round's phase-2 loop.
  The back-end grounding (23:53Z) found the JOIN leg was never built
  (joins: 0 everywhere), so the funnel's "joined" step cannot be
  measured until the join step lands. Both are cross-round
  dependencies, not phase-1 blockers.

## 9. Sync question for sibling coordinator 58af0570

The Hub's feed IS the blog's feed. Phase-1 canonical is `/s/sn2696`;
**Hub/feed highlight hrefs must align on the canonical `/s/<slug>`
form in phase 2** (today the Hub's card links are built at runtime
by JS with no canonical href in the static shell). Please confirm the
feed/messenger round adopts the same canonical form so the two
public faces never diverge into two article URLs.

## 10. Files (work directory + branch)

Work directory `~/workspace/team-nitro/public-blog-seo-20261112/`:
`phase1-additions.js` · `build-phase1-worker.py` ·
`deploy-phase1-staging.py` · `probe-phase1.py` ·
`probe-phase1-playwright.py` · `hub-worker-phase1.js` (built, 49,174 B)
· `RECORD-PHASE1.md` (this file) · `SCORECARD-PHASE1.md` ·
`phase1-shots/` (note-1440/390/360.png + results.json).
Filed to branch `public-blog/seo-system-20261112` under
`BLOG/public-blog-seo-phase1/` (same 8 files; screenshots stay local —
re-takable by the checker).

## DONE / NOT-DONE

**DONE:** the foundation repaired in staging on one real note ·
robots + sitemap real and valid · note page server-rendered with
accurate meta, one canonical, real image · denial proven for private /
unknown / unlisted notes, aliases, images · browsers still 302 into
the Hub · no regressions on `/`, `/hub`, `/sw.js` · Playwright clean
at 1440/390/360 · record + scorecard written · branch filed.
**NOT-DONE (not mine, or not yet):** Shawn's approval of SN-2696 for
public publication · live deploy (his tap) · free/paid entitlement
reconciliation · registry-backed publication (Naya 5 repair is the
unblocker) · real note-specific cover image · phase-2 card href form
· the checker's independent verification · PI row update (via the
coordinator from this report).
