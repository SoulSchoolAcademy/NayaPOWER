# MAKER REPORT — Portal Alignment Round 1 (R1 + R1b fix)

**Lane:** `~/workspace/team-nitro/portal-alignment-r1/` · **Seat:** coordinator acting as maker (depth-2 subagent — cannot spawn subagents, so maker and checker could NOT be separate seats in this session; see "Checker status" below). **Staged only. Nothing live, nothing to Shawn.**

**Brief:** Alignment director, Shawn's order voice call 2026-11-27 ~15:29 MST — get the Portal aligned to Naya design level. Scope: (1) 9 top-nav icon circles get visible labels, (2) one light top-left, (3) walkthrough sequence visible/reachable on the front page — portal → certificate → iPhones, name entry to the NEW certificate on the same host, (4) nothing cut off at 390×844 and 1440×900. One hour max.

**Vault read (Collective Vault Law, Shawn's order 2026-11-27 ~15:32 MST) — done FIRST, before touching the page:**
- Supabase `hub_smart_notes` via `sb-api GET /rest/v1/hub_smart_notes` — the SN-4883+ activation set IS live: 18 newest notes, created 2026-11-27T16:37:10Z, read by ib_id/title/nutshell: SN-4883 The Wise One · SN-4884 The Five Gates · SN-4885 The Protocol in One Note · SN-4886 The Three Systems and the One Flow · SN-4887 Privacy by Default · SN-4888 The Membership Ladder · SN-4889 The Money Law · SN-4890 The Room of Real Objects · SN-4891 The Checklist Law · SN-4892 The Ten Laws in Ten Lines · SN-4893 Nothing Flat, Nothing Dead · SN-4894 White Text, or Jewel-Bright · SN-4895 One Deep Colour per Object · SN-4896 Harvest, Never Invent · SN-4897 The One-Build Law · SN-4898 Prove It, Then Say It (full body read — receipt before report, his eye is the final gate) · SN-4899 The Room Law. (SN-4882 is a test note, not part of the set.)
- Program record read: `~/workspace/team-nitro/DESIGN-ALIGNMENT-PROGRAM-20261127.md` (Portal is round 1; walkthrough+About/Skills is a separate taken-in track — linked, never duplicated; R6f is NOT a base).
- MEMORY.md "DESIGN WALK — SIX PAGES" entry read (in context). Law files read first: THE-NAYA-DESIGN-LAWS.md, THE-PLAYBOOK.md, DESIGN-INTELLIGENCE-REPORT.md, THE-NAYA-DESIGN-LANGUAGE.md, THE-NAYA-CODE.md, THE-DEEP-PALETTE.md, plus `~/workspace/team-nitro/AGENTS.md`.

## Staged build (current — R1b)

| Item | Value |
|---|---|
| Staged link | https://portal-alignment-r1-staging.nayapower.workers.dev/ |
| Portal bytes | **13,882,866 B**, sha256 `4ad2041cc1307b9180a424501e32f1a966cf37a6ba05a0b5a5032033c555a887` |
| Portal (R1, before the strip fix) | 13,882,764 B, sha256 `802c3dd226ffb4cc4429db35852acb79838a04c422415b0d0b0cee88b4925e43` |
| Base | R5 staged portal, harvested by curl, **13,883,771 B, sha256 `d4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b`** — byte-identical to lane `portal-r4.html`/`round-5/maker/portal.html` |
| Certificate | **313,224 B, sha256 `57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b`** — byte-identical to R2, unchanged |
| Worker | `worker-consolidated.js` 14,219,084 B, sha256 `d462ddf203c2b9954bf40079f3498396e16dbccce4230fee47b887fb3199ada7`; worker `portal-alignment-r1-staging`, deployment `2f5ceeeecd9142fda05d702cb01306aa`, modified 2026-11-27T22:48:47Z, subdomain enabled (`enabled:true`), KV binding `WELCOME_ASSETS` (namespace `1cf80db6183245d19dd5296645a12bd0`) |
| GitHub | **NOT FILED in this session** — see "Owed" below. No branch/commit to report; do not treat the staging worker as the filing. |

**Staged verification:** curl read-back — staged portal == lane `portal.html` bytes + sha (`4ad2041c…`), staged identity == lane (313,224 B, `57bdd387…`). Build scripts: `build-r1.mjs` **26/26 assertions PASS**; `build-r1b.mjs` **14/14 assertions PASS**.

## What changed (portal.html only; identity, sw.js untouched)

1. **Labels visible (item 1).** `.eco-tip` went from absolute-positioned, `opacity:0`, hover/focus-only to static, always-visible labels under each ball — white 17px Marcellus, obsidian pill, rim in each item's own deep-palette colour. Desktop: one row of 9 ball+label cells (1088×109). Phone: **3×3 grid** — a 390px row of 9 labelled cells at 17px is geometrically impossible ("Innovations" alone is ~90px; nine labels need ~900px), so the grid is the honest shape; every label whole, nothing cut off. The first-tap-hold JS (first tap shows the tip, second navigates) is deleted — a single tap now navigates. "12 Elements of Naya" shortens to "12 Elements" (matches its aria-label) so it fits its cell. All nine hrefs, glyphs and `--eco-c` values untouched. This reverses R5's hover-only pick on Shawn's Nov 27 alignment order: a cold visitor must know where each icon goes without hovering.
2. **One light, top-left (item 2).** Button sheen `105deg → 135deg` (4 occurrences, that exact sheen); the disabled `body:before` ambient glow is re-enabled as a top-left wash (`circle at 24% 12%`, deep gold + royal purple, faint, slow ambient). `.core` (35%/30%) and `.eco-ball` (35%/28%) already light top-left — verified, untouched. **Named gap:** the arch scene's central light is baked into the dial photograph itself; no CSS re-lights a photograph. That needs an art pass, not this round — named, not hidden.
3. **Walkthrough sequence (item 3).** One compact strip, `1 Portal → 2 Certificate → 3 iPhones`, obsidian pill bar, gold rim, white 17px Marcellus. Step 2 links `/identity.html` (same host — the NEW certificate). Step 3 links the official v3 phone walkthrough staging worker (`portal-phone-v3-staging…/?walk=1`, owned by the walkthrough+About/Skills track — linked, never duplicated). **R1b fix:** the strip first sat inside the circular `.core`, where the chord is only ~182px — it wrapped to 3 lines and the dial's bottom edge sliced "2 Certificate"/"3 iPhones" (seen with my own eyes on `r1-phone-front.png`). It now sits at the bottom of the stage, one line at both widths.
4. **Name entry → NEW certificate.** The R5 submit handler already routes to `/identity.html?name=…` (relative, same host). Proved live: typed "R1 Check" → `https://portal-alignment-r1-staging.nayapower.workers.dev/identity.html?name=R1%20Check`. No `nayanet.app` certificate/identity URL exists anywhere in the portal file — the "old live certificate" bug does not reproduce on this staged build; if it lives on live `nayanet.app`, that is outside this staged round.

## Probe (Chromium 1255 via forwarder, `probe-r1.py` + `probe-r1b.py`, logs + screenshots in this lane)

| Check | Phone 390×844 | Desktop 1440×900 |
|---|---|---|
| Labels at rest | 9/9, opacity 1, 17px, grid 3×3 (119px cols), max tip right 382 < 390 | 9/9, opacity 1, 17px, one row 1088px, max tip right 1243 < 1440 |
| Horizontal overflow | scrollW 390 == vw | scrollW 1440 == vw |
| Strip | one line 329×42, right 359, bottom 772 — whole (R1b) | one line 329×42, right 884, bottom 828 — whole |
| Single tap/click Innovations | tap → `https://innovations.nayanet.app/` (popup, first tap) | click → same |
| Name entry | → `/identity.html?name=R1%20Check` on the same host | — |
| Page errors | 0 pageerrors (R1b legs) | 0 pageerrors |
| Console errors | 1× `ERR_CERT_AUTHORITY_INVALID` (Google Fonts — the known VM-proxy TLS artifact, same as R4/R5) + 1× 404 (favicon, same as R5) | same TLS artifact only |

Screenshots read with my own eyes: `r1-phone-front.png` (R1 — strip clipped, caught, fixed), `r1b-phone-front.png` (strip whole, one line), `r1-desk-front.png` (nav row + strip whole), `r1-phone-cert.png` (certificate after name entry).

**Carried observations (not introduced by R1):** "NAYA WELCOMES YOU" wraps to two lines inside the phone dial — whole and readable, not cut; it wraps because the 3×3 nav makes the stage shorter at phone width. The phone dial's "Your name" pill sits on the dial's top rim. Both named, not fixed — touching the dial geometry was out of scope.

## §11 design-law check (in writing)

Ran `~/workspace/team-nitro/check-design-laws.py` on the R1 portal and identity (outputs `law-r1-portal.txt`, `law-r1-identity.txt`):
- **Portal: 81 violations + 4 warnings — identical to the R5 baseline (81+4). Zero new violations.**
- **Identity: 3 violations — identical to R5. Zero new.**
- Reference objects, named per element: the 9 nav balls measured against **the top-left + button** (obsidian circle, thin bright own-colour edge, white glyph in the middle, real shadow; orbit rings 60s/90s kept); the strip measured against **the Smart Note board** (board black `#050607` inside, white word in the middle, own-colour rim outside — gold here); the label pills' no-glow inside measured against **the X button** (no glow inside, and that is why it is more elegant). Light: 135° sheen + top-left wash + 35%/28–30% radials — one source, top-left, except the photographic scene (named gap above). Text: labels + strip are 17px Marcellus white; no gray text added; no text under 17 added. Colours: deep palette only, one colour per object, spectrum flows purple→blue→green→gold→orange→red→magenta→indigo→cyan across the nine; no two same colours together. Hover: balls lift + light in their own colour (R5 behaviour kept); strip links underline on hover via the anchor rule.
- Five gates: right (alignment order, staged only) · truly needed (cold visitor + walkthrough sequence, his words) · mine to do (director's brief; live untouched, no money/credentials) · now (inside the hour) · provable (bytes + sha + probe + screenshots above).

## Smart note to file back (Vault Law §3) — NOT filed by this seat

This seat has no smart-note filing path in-session, so the note is recorded here for filing, **not claimed as filed**:

> **Title:** Labels You Can Read Without Touching — The Portal Nav Lesson
> **Nutshell:** A cold visitor cannot hover. Nine icon-only circles with labels that appear only on hover are nine mysteries; the fix is labels that are always there — one row on desktop, a 3×3 grid on phone, because nine 17px labels cannot fit one 390px row. And a strip inside a circle gets sliced by the circle: put the walkthrough steps where the full width lives, at the bottom of the stage, one line.
> **What it means:** Design Laws §2.3 (17px minimum) and §9 (a cold stranger knows in two seconds; mobile first, phone width first) decide the layout, not taste. When the law's minimum size and the viewport's width disagree, the layout changes shape (grid, not row) — the text never shrinks and never clips. A first-tap that only reveals a label is a dead tap once the label is always visible; the hold must die with the hover.
> **How it applies:** Any page with icon-only navigation gets this same test: labels visible at rest at 390×844, measured (opacity, rects, scrollW), not eyeballed.

## Checker status — OWED, not done

**No independent checker ran in this session.** I am a depth-2 subagent and cannot spawn subagents, so maker and checker were the same seat; the probe above is a maker self-probe, not an independent check. The director must dispatch an independent checker (own probes, real taps, true 390×844 + 1440×900, 0 page errors, screenshots) before any PASS is claimed. **No score is claimed here** — the build is staged and self-proved only; 9.5+ and the §11 check belong to the independent checker and Shawn's eye.

## Owed

1. **Independent checker** (see above) — dispatch by the director.
2. **GitHub filing** — no branch/commit in this session (time ran to the hour; the staging worker is deployed and verified, the filing is not). Suggested: new branch `portal-alignment-r1` from `portal-frontpage-fix-20261125-r5` head `5d68aeece9f80cb2949ed6ef19e2b17d7881ec4c`, files `portal.html`, `identity.html`, `worker-consolidated.js`, `worker-meta.json`, `sw.js`, `build-r1.mjs`, `build-r1b.mjs`, `build-worker-r1.mjs`, `MAKER-REPORT.md`, via the R5 `commit-r5.mjs` pattern (git-data API, blobs >1MB).
3. **Smart-note filing** — the note text above, via the normal filing path.
4. **Photographic scene light** — the dial image's central light is the one item-2 remainder; needs an art pass or Shawn's eye, not a CSS round.
