# MAKER REPORT — Black Diamond phone on the portal (2026-11-27)

**Staged link:** https://portal-frontpage-fix-20261125-r5phone-staging.nayapower.workers.dev/
**Phone path:** staged link + `?walk=1&name=Shawn&alias=shawn` (the phone starts after portal + certificate, as briefed)

## What was built

The walkthrough is now the Black Diamond phone, real on the portal page — not a separate page. Faceted diamond chrome frame, carbon-fiber chin, brushed aluminum, obsidian black 9:16 screen, live ticking clock + 5G + battery in the status bar, and one big elevated purple obsidian jewel ball with the Naya N in a chrome bezel. The ball IS Enter (ENTER under it as its label, no separate Enter button, no end disc). Front and center, XL width (560px desktop, edge-to-edge on mobile), dead forward, no angle.

**Flow:** no real-name screen (the portal has it), no alias screen (the certificate has it). First phone screen: country, then province/state, then city — one board each. Then the 15 harvested R5 walk questions verbatim, in order (motto, vision, goal, mission, love, don't love, thing, values, laws, declaration, offer, help, moment, how do you work, how do people start). Per screen: question + input full-frame on the white-light card, OR the reveal full-frame after the ball tap — never both squished. Type your answer → tap the ball → it reveals in place (unfold + ball spin) with your answer and our full example → Next arrow moves on, Back arrow goes back. The ball never navigates on its own. Answers save as you go (same key `naya_welcome_right_v1`); the review screen copies every answer out (Copy my answers).

## Base + diff (exact)

| Item | Value |
|---|---|
| R5 base | `portal-r5-base.html`, 13,883,771 B, sha256 `d4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b` (re-verified live on the R5 staging worker: HTTP 200, same bytes + sha, before building) |
| Built portal | `portal.html`, 13,900,396 B, sha256 `b7ee02d6177628e5700ae57f819cb7e87f532689245cf639e6d228b080559ee0` (+16,625 B vs R5) |
| Certificate | byte-identical, sha256 `57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b` |
| Branch | `portal-frontpage-fix-20261125-r5-phone` (from R5 head `5d68aeece9f80cb2949ed6ef19e2b17d7881ec4c`) |
| Commit | `869875412f50a365062d22f4ce970f0abae64ad2` (phone build) + fix commit TBD (eye-fix pass — see below) |
| Portal blob | `59776fa2b08ac8d5acc4a5633de852807cda399e` (first commit; verified by blob-API read-back: same sha, size 13,900,189, base64) — fix commit re-blobs the rebuilt portal |
| Worker | `worker-consolidated.js` 14,238,088 B, sha256 `ab1d675ebf5d7277f622ed9ee1f8385b357e6188d352bd135b72168692ddf7d0`; worker `portal-frontpage-fix-20261125-r5phone-staging`, subdomain enabled, HTTP 200 |

**Hunks (all in `portal.html`, nothing else in the R5 portal touched):**
1. Walk `<section id="fpWalk">` swapped whole for the phone markup (same IDs the walk script needs, plus `fpWalkNext` and `fpWalkCopyAll`). Old section was 2,140 B; phone section 5,773 B.
2. One `<style>` added (phone CSS, 8,910 B) + one `<script>` added (phone chrome logic: live clock, battery, reveal/showInput/showEnd, copy-out — 3,260 B).
3. Nine small walk-JS patches: QUESTIONS prepended with country/province/city; render() sets the placeholder instead of swapping an Enter label; render() resets to input mode; ball click reveals instead of advancing; Next-arrow wiring added; finish() hides the phone nav. The walk's `complete()` POST + verify-before-declare to the walkthrough-15 staging worker is untouched.
4. R5 keepers verified present by assertion: hover-only menu, dotted ring (78s), 27-slide story, nine destinations, `?walk=1` gating, certificate link, F1 ball asset.

**Files filed to the branch:** `portal.html`, `portal-r5-base.html`, `identity.html`, `identity-consolidated.html`, `worker-consolidated.js`, `worker-meta.json`, `sw.js`, `build-phone.mjs`, `build-worker-phone.mjs`, `verify-phone.mjs`, `commit-phone.mjs`, `phone-section.html`, `phone-style.html`, `phone-script.html`, `MAKER-REPORT.md`.

**Eye-fix pass (after the first staged render, before this report):** my own eye caught three defects and they were fixed in `phone-style.html` only, then rebuilt, recommitted, redeployed, re-probed: (1) the jewel's facet overlay read as a harsh pinwheel and the reveal spin rotated the whole jewel so the N read as a Z mid-spin — facets softened (lower alphas, irregular stops), radial deepened to obsidian, spin moved to the facet layer only so the N stands still; (2) the frame ring read as bold zebra stripes — conic slices fined to 5° at lower alphas so the chrome base shows through; (3) the reveal/input cards left dead black below them in the 9:16 screen — cards now flex:1 and fill the stage. First-build numbers (portal 13,900,189 B sha `3b489c5a…`, worker 14,237,881 B sha `2360ee86…`) are superseded by the table above.

## Verification (real taps)

Build: 18/18 assertions in `build-phone.mjs` (phone markers, no separate Enter button, 18 screens, live clock/battery, copy-out, 8 styles / 10 scripts, all R5 keepers) — re-run clean after the eye-fix rebuild.
Staged: `verify-phone.mjs` — 36/36 PASS, staged bytes == lane bytes + sha (portal sha `b7ee02d6…` after the fix rebuild), identity unchanged.
Browser (Playwright Chromium via the localhost forwarder; VM browsers flap, Firefox never fires Supabase reads — Chromium used): **31/31 PASS** (`evidence/probe-phone.py`) — 390×844 + 1440×900, 0 page errors, real taps: type country → ball reveals → Next advances → Back returns with answer kept → motto reveal shows answer + our example → answers in localStorage. Battery reads live (headless Chromium reports 100; 87 is the no-API fallback). Screenshots: `evidence/phone-390-reveal.png`, `evidence/phone-390-q3.png`, `evidence/phone-1440-reveal.png`.

## Design-law check (§11)

- §1 real objects: frame, chin, ball, arrows, cards all layered with depth + down-right shadow; alive on hover (lift + purple glow outside), press scale 0.97. Ball orbit ring turns 120s (slow, alternating not needed — single slow CW).
- §2 text: Marcellus, white, 25/19/17, no text under 17px (status bar 17, kicker 17, ENTER label 17, ball N 52 display glyph). No gray text anywhere in the phone.
- §3 color: deep palette only — royal purple `#8e24aa` for the ball, rims, glow; white/black/chrome for the hardware. No two same colors together in a row (back arrow white rim, next arrow purple rim).
- §4: one light top-left 135°, shadows down-right, inside board black `#050607`, no glow inside.
- §5/§6: buttons are obsidian pills/circles with own-color rims; one idea per screen.
- **One brief-ordered exception, named:** the input/reveal card is the reference phone's own white-light card (white, black Marcellus text — never gray). The reference standard and the brief's "elegant white light" order it; it is the screen card, not a Naya board, and everything else on the phone stays board black. If Shawn's eye says the card should be obsidian instead, it is one CSS block to change.
- **Known deviation from the brief's parenthetical walk list:** the brief lists walk screens (age+language, gender/faith/ethnicity, favorites, industry+subcategories, education/work/experience, achievements trio, unique/benefit/connect) that do not exist in the harvested R5 walk. The R5 walk's 15 questions (motto…start) were kept verbatim instead of inventing new questions, per "harvest where they exist — do not invent new questions". If the fuller walk lives elsewhere (walkthrough-15 live), that is a follow-on round with its source named.

## Still open

1. **Backend integration for the phone answers** — answers save in-page (`naya_welcome_right_v1`) + copy-out on the review screen. No server save is faked. The walk's existing `complete()` still posts to the walkthrough-15 staging worker; whether that backend accepts the three new location keys (`country`, `province`, `city`) is unproven and needs the backend seat.
2. **No per-question pictures** — the R5 walk carries no images per question, so screens are input/reveal full-frame; the 9:16 area is the picture area when a picture exists. If deck images per question are harvested later, they drop into `.bd-stage` full-frame above the ball.
3. **Shawn's eye is the final gate** — staged only, nothing live, nothing to Shawn from this round.
