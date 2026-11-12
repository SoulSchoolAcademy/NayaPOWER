# THE ULTIMATE PRESENTATION PAGE — Whole-Page Template
## Filed 2026-11-06 into the Smart Factory (Shawn's order: file the value, name it, so any page can pull it again)

**What it is:** the pricing page — the page that lets a stranger decide to buy or not, in one read. The first whole-page template composed from named Factory parts, and the first page to pass blind verification at 10/10. It is the money machine's front door: the intelligence system presented so completely that the reader says "wow, I'm in" AND "oh, I get it."

**Source file:** `pricing-table-DRAFT-v4.html` in this folder — **134,450 bytes, 1,121 lines, sha256 `9c42eff887741ed4430a98b18fa9debe52517dc1691be63e40341f9f0f4b68ba`**.
**Blind verification:** `VERIFICATION-ROUND5.md` (~/workspace/verify-pricing-v6/) — **PASS 10/10, 199/200** (round 4 was 188/200). Fresh Playwright + Firefox measurements only; the builder's report was never read. The verdict covers sha `9c42eff8…` only — the file was edited once mid-run (22:40:03Z, +2,730 bytes, +27 lines) and every measurement was re-run against the final file.

---

## The composition — in order, as the reader walks it

Measured DOM order (blind verifier, Y-positions at 1920 confirm it):

1. **Studio top** — full-bleed banner, text-free. Naya inside the steel machine; the nine systems as real objects at the base.
2. **Hero promise + tiers preview** — "Nine days. Everything. Free." + the Bugatti line + hero CTA + guarantee, all in the first viewport.
3. **How it works · payout proof · worked example ($125) · seats (1,000, fixed) · ladder + billing toggle** — monthly $25/$50/$100, annual half price.
4. **Tiers** — Power 1 / Pro 5 / Max unlimited membership sites. Middle highlighted (MOST CHOSEN on Pro).
5. **The difference** — plugged vs unplugged, one line (Academy harvest #6).
6. **THE CHART — the heart.** 3 group headers + 18 data rows, jewel + eye + value line on every row. Sticky thead pins. Exactly one row lit on hover. Every row's eye opens WHAT IT IS / WHAT IT DOES / WHAT'S IN IT FOR YOU.
7. **THE STATEMENT PIECE — the bridge.** The plaque between the chart and the calculator (modelled on the Academy Membership Plaque, harvest #3): "Congratulations, you're hired. You get paid WHEN WE GET PAID."
8. **THE CALCULATOR** — the Speedometer Calculator (named part, `SPEEDOMETER-CALCULATOR.md` + `speedometer-calculator.html` in this folder). "Calculate your income."
9. **Nine systems** — one intelligence, nine activated systems, same nine names as the nine orbs (Academy harvest #5).
10. **Top 10 reasons** — each with a REAL example (mechanism + page numbers only; no invented person or earnings).
11. **Closing strip · 9-day journey** — days 1–5 Academy training, days 6–9 operate. "Get paid in 10 days, get a flow going, get paid every day."
12. **Guarantee 3×** — "No refunds — the trial is the guarantee." All three visible on first paint, none behind a tap.
13. **Fear-killers** — AFTER the chart (the required logic sequence: button → chart → fear-killers → reasons → closing → bottom banner).
14. **v2 bottom banner + three Supercharger Buttons** — "This is yours. Pick your power." + the close line: "Once you go Naya, you don't go back — once you've experienced Naya Power, there's nothing like her."
15. **FAQ · footer** — three questions, answered straight: money-back, after-9-days, wrong-level.

**The three answers, in order (Shawn's direction):** what do I get? → why is it worth it? → what if I'm wrong? Three minds, one scroll: convinced (button first) → comparer (chart second) → scared (trial + guarantee + up/down third).

---

## What makes it clonable — the machinery, not the words

- **Single-source `PRICING` object** drives every price: one click reprices tier prices, per-day lines, column subs, button notes, bottom line, sticky bar, and all 8 hrefs together — and restores exactly (toggle probe: BACK == BEFORE, 0 differences).
- **Single-source `LINKS` object** drives the 8 button hrefs. All 8 buttons are real Smart Links (`https://nayanet.app/<name>`); 6/6 distinct links 302 to the exact PayPal plan_id. `paypal.com` occurs 0× in the source — no button points straight at PayPal.
- **12× "EDIT THIS" markers + "HOW TO CLONE" comment** at the top of the file. To reprice: edit the PRICING object only. To add a feature row: copy the ROW TEMPLATE above the table body. To re-point the buttons: edit the LINKS object only.
- **Proof of clonability:** the example clone (`pricing-table-EXAMPLE-clone.html`, sha256 `97432fdc6635375865d5973cf861e4d46b45436a9ae5061b22a26f4ae90bd47a`, in ~/workspace/user/files/) renders clean at 1280, 0 errors, Wednesday 0 — re-checked live in round 5.

---

## The images — where each one lives (provenance, honestly)

The filed page file references its four images by **local relative paths** (`../../verify-pricing-v6/banner-assets/…`). A cloner re-points the four `src` attributes to the GitHub copies below. The page file itself is filed verbatim — its words and machinery are the template; the image paths are the one thing a clone must re-point.

| Role in the page | GitHub file | Size | sha256 (verified by me, repo bytes = local bytes) |
|---|---|---|---|
| TOP — Studio | `HUB/app/banner-assets/pricing-supercharger-alt-studio.webp` | 366,828 B | `ce4c0d1a60481edcad37bf3675abcd8434cd7c979e4c6804d6f6f631ad9fa623` |
| CALCULATOR — Cinema | `HUB/app/banner-assets/pricing-supercharger-alt-cinema.webp` | 451,844 B | `8a9e66ff4c21c3234367fa675cac8d25db778b42b80d5ed073fb3de0cb4e01d9` |
| NINE SYSTEMS — Layers | `HUB/app/banner-assets/pricing-supercharger-alt-layers.webp` | 439,050 B | `6719683890741c4608a76136166589e3f8b80cd75ca40a01036cd8f18af976c2` |
| BOTTOM — v2 wide crop | **filed in THIS folder:** `pricing-supercharger-bottom-naya-in-gauge-wide.webp` | 274,232 B | `42f26c979f2bf2262390c6b9f83d49718f44f935a5f23f8d304a4e3067ef924c` |

- The three Studio/Cinema/Layers files landed in the repo via **PR #3271** (Resolve, merged 2026-11-06 22:17:46Z, merge commit `fd97f4d9`): "Supercharger assets: Nitro-ruled pair + three top candidates."
- The **wide bottom crop is a derivative, not an original:** cropped 1920×800 from `HUB/app/banner-assets/pricing-supercharger-bottom-naya-in-gauge.webp` (630,632 B, sha256 `b0a676668bbb27b996ccd089e533b41255da15cca69ebbf8ef41c0b1233d0d53`). It was local-only until this filing — this folder is now its GitHub home, and its provenance is recorded here, not hidden.
- **Fallbacks** (in the same repo folder): `pricing-supercharger-top-orbs.webp` (the alternative top — gauge + nine-orb row + Naya bottom-right, sha256 `444211064aaaf5cdd65b1811e90027d43bd8172a14b2cdcc24b60937ec7a669c`) and the marriage finals `pricing-banner-top/bottom-marriage-FIXED.webp` (PR #3269) — only if Studio or the v2 bottom fails a self-check.
- **Design law:** images present, live elements perform. Words appear only BESIDE the images as page copy, never baked in. The top banner is text-free.

---

## Honest notes from the blind verification (disclosed, not hidden)

1. **The bottom banner carries SIX orbs, not nine** — by design. The wide crop keeps six orbiting orbs; the two oversized foreground orbs were cropped out. Nine is still presented countably where the page claims it: Studio top (9 objects, counted by eye) + nine-systems section (9 named systems, 01–09).
2. **Bottom-right (compass) orb is half-cut** by the wide crop's right edge. It reads fine in the full-bleed render; a re-crop keeping all six orbs whole would lift the banner item from 9 to 10.
3. **One dictation near-miss (one character):** the page carries *"No downline, no upline — just the potential to get paid every day."* — every word of the required line, in order, but the sentence continues after an em-dash instead of ending with a period. Present in substance; not verbatim to the final period.
4. **Phone sticky bar** overlays viewport-bottom text while scrolling on 390 (standard fixed-bar behaviour; the page carries 120px bottom padding, so nothing is ever unreachable) — noted, not a defect.
5. **The calculator never prints $5,000/$60,000 as computed figures.** $5,000 is the dial's cap (a scale marking + the pegged note); $60,000 occurs 0×. See `SPEEDOMETER-CALCULATOR.md`.

## The bullseye (cold reader, from memory after one read)

- (a) Name what each level gives in 30 seconds — **PASS.**
- (b) Say what happens after the 9 days — **PASS.**
- (c) Say what happens if you pick the wrong level — **PASS.**
- **"Wow, I'm in" — PASS. "Oh, I get it" — PASS.** The loop is unmistakable by the calculator: try → invite → earn → keep.

## Carried forward (not the page's fault — unchanged by round 5)

Thank-you return Smart Link BLOCKED (no live thank-you page address) · PayPal Auto Return setting — Shawn's hand · level-change flow — launch dependency · trial full-access model — recorded as the model, BLOCKED if the system cannot honour any part · member face/quote proof — BLOCKED · claim-worker routes-token secret likely stale · VM reconciler backstop still not running.

## Parts this page is composed from

Academy harvest (same Factory location, `academy-harvest-20261106/`): #1 The Supercharger Button (all 8 CTAs, verbatim construction) · #3 The Membership Plaque (the statement piece's model) · #5 The Nine Systems · #6 The Difference Block · #8 The Payoff Close · #9 The Academy Days (the nine-day journey). Plus, in this folder: **The Speedometer Calculator.**
