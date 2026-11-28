# MAKER REPORT — OFFICIAL WALKTHROUGH (2026-11-27)

**Maker:** subagent (official-walkthrough seat) · **Dispatched:** 2026-11-27 ~19:06 MST · **Staged:** 2026-11-28 ~02:11 UTC
**Staged link:** https://official-walkthrough-staging.nayapower.workers.dev/
**Walk path:** staged link + `?walk=1&name=Shawn&alias=shawn` (certified alias — the staging backend 404s uncertified aliases, v3 precedent)
**Nothing live, nothing to Shawn.** Staged only; live is Shawn's tap.

## The build, in one line

Portal R5 → certificate (no Jump back in, no Install App, raised name, live digit-tile date/time, ENTER → `/?walk=1` same host) → 23 Black Diamond phone frames in 8 trios, video in one mid-flow spot as the direct file. Walked whole by real taps at 390×844 and 1440×900.

## Filing (the numbers)

| Item | Value |
|---|---|
| Staged link | https://official-walkthrough-staging.nayapower.workers.dev/ |
| Portal | **47,430,066 B, sha256 `1677214b5a25310d71b261dc65a427fff077d9cc41cb628795f2fb7fb021475c`** — staged read-back byte-identical |
| Certificate | **316,048 B, sha256 `f1f69cc93d7b974e48c3b9f806d9a4618fe09d544572e54d5b33d37897fbbc19`** — staged read-back byte-identical |
| Worker | `worker-consolidated.js` 47,772,462 B, sha256 `bf3762e4b9fea2b448ac829e42b335e93ab05ce5536f231a72367a8f976dafba`; worker `official-walkthrough-staging`, deployment `12b9905fd1134a7db9dedc09357b6085`, subdomain enabled (HTTP 200 `enabled:true`) |
| Video route | `GET /naya-video.mp4` → 200, `video/mp4`, 7,368,202 B, sha256 `c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c` — byte-identical to the source file (served from WELCOME_ASSETS KV key `naya-welcome-video`, put by v3; NOT re-uploaded) |
| GitHub branch | `walkthrough-official-20261127` (from v3 branch head `b14fe2d5…`) |
| Commit | see commit-official.mjs output (filed after this report was written) |

**Vault read first (briefed):** the Smart Vault state before touching the page was the R5 portal (13,883,771 B, sha `d4bb2102…`) + R5 certificate (313,224 B, sha `57bdd387…`) as filed, with the certificate writing claims to Supabase `nayanet_identities` (the vault the certificate already reads/writes). No walkthrough existed on the portal page. What I learned is filed back in `VAULT-NOTE.md` in this lane. Nothing from the dead fix11 line, restart rounds 1–4, or the portal-phone trio was used as a base — the trio's phone frame/engine/picture map were harvested as parts only (connect, don't create), and its flow was replaced outright.

## What was built

**Flow (23 phone frames, 8 groups of three; laptop side by side, phone stacked scrolling):**

1. live — country/province/city, one box
2. age+language — age group (never a specific age) + language, one box
3. gender+faith+ethnicity — gender dropdown (male / female / prefer not to say), NO default; faith + ethnicity optional, same box
4. favorites — ONE frame in thirds (brand / music type / hobby + "what else you love" + sport type + team)
5. industry+skills+connect+categories — ONE frame (industry select, skills check-off, connect dropdown + own words, categories click-off + subcategories under the ones picked)
6. video — Naya, in her own words (direct file, see below)
7. motto — its own phone, hands holding a glowing crystal heart
8. vision · 9. goal · 10. mission
11. love · 12. don't love · 13. thing
14. promise · 15. gift · 16. benefit
17. unique · 18. connect · 19. work
20. education · 21. experience · 22. achievements
23. values+stand for — values + where you stand, one slide, five glowing crystal pillars
→ end screen: answers → Hub → pricing page (See my world / Smart hub / Choose plan / Dashboard / Business / Space)

**All five named trios are consecutive runs in that order:** Mission·Goal·Vision (vision, goal, mission) · Love·Don't love·Thing · Unique·Benefit·Connect (benefit, unique, connect) · Education·Work·Experience (work, education, experience) · Achievements·Values·Where-you-stand (achievements, values+stand). Two order notes, named: Connect and Work swap places vs the skills-five listing (Gift→Benefit→Unique→Connect→Work) so the Unique·Benefit·Connect trio holds; Education comes before Experience so the Education·Work·Experience trio holds (brief lists Experience→Achievements→Education). Values+Stand sits once, in the Achievements trio — the Values·Promise·Gift trio is NOT used, per the brief's supersession.

**Certificate (identity.html, from R5 sha `57bdd387…`):** "Jump back in" button + its "Already have a Smart Name?" line REMOVED; "Install App" corner button REMOVED (the hidden install veil stays in the DOM — its JS touches installX/installGo unguarded, so removing it would throw; it is unreachable without the corner button; its go button is relabelled "Add to Home Screen" so no "Install App" button text remains — the only remaining "Install App" strings are two code comments). Name raised/elevated on the certified document (layered text-shadow + lift). Date/time dynamic and CENTRED in Dashboard digit tiles (digit colours per laws §4), ticking every second, painted on both the registry-restore and claim-stamp paths. ENTER still hands off to `/?walk=1` on the SAME host — the portal link bug is fixed by construction: the portal already went to `/identity.html` on its own host (verified in the R5 bytes), and the certificate now hands back to the same host's walk, never to a live certificate.

**Portal link bug — verified, not assumed:** R5 portal bytes carry `location.href='/identity.html'` (same host) and no live-certificate redirect; identity carries no `nayanet.app/identity`.

**Pictures (14, harvested verbatim as data URIs, sizes re-checked in the build):** Vision→3_NANOVERSE (365,937 B) · Mission→4_HOW_IT_WORKS (442,529 B) · Goal→1_THE_VAULT (326,889 B) · Thing→7_AUTO_ORGINIZED (566,171 B) · Promise→5_SMART_VAULT (521,616 B) · Connect→6_AUTO_MATCH (415,870 B) · Benefit→2_HOW_WE_SNYC (576,540 B) · Motto→c0/c017eea7… (2,349,542 B) · Love→77/7702f987… (3,144,243 B) · Don't love→f0/f0e21717… (2,710,055 B) · Unique→b6/b6cfaaca… (3,565,345 B) · Work→fa/fa45cb89… (3,548,134 B) · Gift→42/4248188b… (3,665,149 B) · Values+Stand→a3/a3903daf… five pillars (2,924,933 B). Picture/answer separation: the picture is a full-bleed 9:16 layer BEHIND the input (absolute, never layout space); the ball (Enter) reveals it full-screen in place; clicking forward without entering shows no picture. Education / Experience / Achievements carry no picture in the brief's map — their ball reveals the example card only.

**Video — one spot only, mid-flow, direct file:** `/naya-video.mp4` from KV (576×1024 = exactly 9:16, 204.3s, sha `c86da39e…`), in the video iPhone after industry+subcategories, before motto. Ball plays/pauses it; preload=none. YouTube (`youtube.com/watch?v=XqZe1zdF1Tc`) is a fallback link only, never the source. NO video at the end.

**No Skip anywhere** (hidden element only, no handler). **No name screen** — the portal already has the real name, the certificate has the alias; the phones start with where you live. **No "What's your real name?"** in the phones. **No community/church question. No Spotify** (0 occurrences in the built portal). **No gold light-ups** — unhighlighted white, highlighted purple (carried phone code, v3-probed). **Answers save as you go** (localStorage `naya_welcome_right_v1`; probe: 44 keys). **About/Skills:** the walkthrough does NOT put any walkthrough UI on About/Skills — no deck, no "Begin the walkthrough" button, no walkthrough phones there; the answers it collects are the material About (unfold) and Skills (slideshow) are built from. **World model:** creating a world = a custom feed for that world, with custom covers and its own About/Skills — one system underneath, not a cloned personal system (no new system built here; the end screen's "See my world" goes to the created world via the existing walkthrough-15 backend).

## Verification (real taps — Playwright Chromium via the localhost forwarder)

**Build:** `build-official.mjs` — **36/36 assertions PASS** (23 steps in order, no v3 leftovers, values once, age/gender split, industry_all one frame, no name/church/Spotify, gender no default, video direct-file one spot, picture map, 14 pictures, R5 keepers intact, walk gating, complete() verify-before-declare). **Certificate:** `fix-cert.mjs` — 10/10 assertions PASS (both buttons gone, digit tiles centred + ticking, name raised, same-host walk handoff).

**Probe (`evidence/probe-official.py`, adapted from the v3 probe): 123 PASS at 390×844** — full walk of all 8 groups / 23 steps with real taps: trio renders, Group 1 of 8, no Skip, no name step, gender no default, picture/input separation + ball reveal on every picture step (14 steps: card whole in stage at rest, picture absolute, naturalWidth>0, reveal opacity 1, full-bleed, reveal card whole), video phone mid-flow (direct route, fills screen, preload=none, 576×1024, ~204s, ball plays then pauses, YouTube fallback only), categories subs appear and save (Music: Playing stays checked + saved), Back keeps answers (Toronto intact), end screen reached (Welcome home., shawn.nayanet.app, ball visible, 44 answer keys, 21 of 23 answered — the probe leaves the video step + one field unfilled), **0 real page errors** (Google Fonts cert artifact + transient agmt 503s retried 200 + video teardown abort excluded with proof, as in v3).

**1440×900:** three phones side by side, same row, ball+ENTER inside the viewport on arrival; vision reveal on group 3 (picture full-bleed, card whole); end screen whole inside the stage (endBottom 685.77 < stageBottom 697.77), title whole, no clipped end-button labels, chin label does not wrap, ready line counts 23, NO video at the end, **0 page errors**. (One probe-script off-by-one found and fixed mid-run: the 1440 tail needed 5 advances + 1 complete click, not 5 total — a probe bug, not a build bug; the 1440 end was then re-proven in a focused run.)

**Seen with my own eyes:** the 390 and 1440 end screens (screenshots `evidence/official-390-end.png`, `evidence/official-1440-end.png`) — "Welcome home.", shawn.nayanet.app, all six destination buttons whole, purple faceted ball with white N, BLACK DIAMOND SERIES chin. The trio layout is proven by measurement (boxes, same row); I did not eyeball a trio screenshot.

## Design-law check (§11)

- §1 real objects: Black Diamond frame (12 discrete facets), SVG-faceted jewel ball, arrows, cards — layered, down-right shadow, alive on hover (lift + purple glow outside), press scale 0.97; orbit ring 120s slow. Harvested from v3, not rebuilt.
- §2 text: Marcellus, white, 25/19/17 per the laws (the brief's 24/20/18 is the walkthrough's own text scale from the restart line — this build carries the v3 phone's 25/19/17; named, not hidden). No gray text. One carried exception from v3: the input/reveal card is the reference phone's own white-light card (black Marcellus text on white, never gray).
- §3 color: deep palette only — royal purple `#8e24aa` ball/rims/glow/chips; white/black/chrome hardware. Digit tiles use the §4 digit map.
- §4: one light top-left 135°, shadows down-right, inside board black `#050607`, no glow inside. (The jewel's specular highlight is the gem's own light play, as in the reference. The video's own light is the video's — hero art, not an object.)
- §14 frame library: the portal keeps the R5 frame untouched; the walkthrough phones are the harvested Black Diamond frame, cloned, centre swapped only.

## Named gaps — everything not done, in one place

1. **"28-frame" vs 23 phones.** The brief's own item list yields 23 phone frames (5 personal + 1 video + 9 deep-ten + 5 skills-five + 3 resume). I built 23. If "28" counts portal + certificate + end + something else, the count is 26 screens (portal + cert + 23 phones + end). Named, not fudged.
2. **Pricing "pops up" is a button, not an automatic popup.** The end screen carries "Choose plan →" (to the staging pricing worker) beside "Smart hub →". No auto-popup was added — that would navigate a citizen away without a tap.
3. **complete() still posts to the walkthrough-15 staging backend** (`naya-walkthrough-15-staging.../api/welcome/complete`, verify via `/api/welcome/me`) — carried from R5/v3, verify-before-declare intact, and it succeeded for the certified alias `shawn` at both widths. Whether that backend accepts the new answer keys (industry_all, values_stand, work, education…) as a real citizen claim is unproven — a backend seat's call.
4. **"See my world"** goes to the walkthrough-15 staging world URL, not the Hub — the Hub has its own "Smart hub →" button on the same end screen.
5. **About/Skills pages are NOT built here.** The walkthrough collects the material (motto, vision, mission, values, gift, skills, experience, achievements, education) and saves it; the About unfold and Skills slideshow that render it are a follow-on build, not in this round.
6. **Shawn's eye is the final gate.** The trio was proven by measurement + the end screens by eye; a full eye-walk of every phone at both widths is the checker's job before anything reaches him.
7. **GitHub filing of the two 47 MB files** (portal.html, worker-consolidated.js) — the blobs API 422s payloads that size (v3 precedent); filed via the API script for the small files, with the large files' shas recorded here and in the lane. See the commit section above.

## Build + deploy (exact)

- Lane: `~/workspace/team-nitro/walkthrough-official-20261127/maker/` — `portal.html`, `identity.html` (+ `identity-consolidated.html`), `worker-consolidated.js`, `worker-meta.json`, `sw.js`, `build-official.mjs`, `build-worker-official.mjs`, `fix-cert.mjs`, `commit-official.mjs`, `steps.js`, `engine.js`, `phone-section3.html`, `phone-style3.html`, `phone-script3.html`, `kv-put-video.py`, `enable-subdomain-official.py`, `evidence/probe-official.py` + log + screenshots.
- Base: v1 phone portal (13,900,396 B, sha `b7ee02d6…`), itself on the R5 base (13,883,771 B, sha `d4bb2102…`). Certificate base R5 (313,224 B, sha `57bdd387…`).
- Deploy: `cf-worker.py put-script … official-walkthrough-staging … --meta worker-meta.json` → HTTP 200, deployment `12b9905f…`; subdomain enabled → HTTP 200 `enabled:true`; curl read-back: `/` 200 47,430,066 B sha `1677214b…` ✓ · `/identity.html` 200 316,048 B sha `f1f69cc9…` ✓ · `/naya-video.mp4` 200 7,368,202 B sha `c86da39e…` ✓.
