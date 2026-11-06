# ACADEMY HARVEST — NAMED FACTORY PARTS
## Harvested 2026-11-06 from the Academy page (Shawn's order: file the value, name it, so any page can pull it again)

**Source page:** https://nayanet.groovepages.com/academy — "MAXESS · NAYA ACTIVATION — Meet the Naya Supercharger."
**Source code:** `NAYA_ACADEMY.md` in this folder (202,339 bytes, sha256 `4b2df62dd855a14934967c17c3933049072a1971c1c7fb637c68bf6551d2e1f0`) — Shawn shared the full file 2026-11-06 21:56Z. The exact code. Harvest verbatim; never restyle.
**Live page read:** 2026-11-06 21:50Z (browser.open, full text). **Live code fetched:** 2026-11-06 21:56Z (282,659 bytes).
**First use:** the ultimate pricing page (pricing round 5, running 2026-11-06) — built FROM these named parts.
**Rule:** name pieces by CONTENT, not only by number (Resolve's standing rule). Every part below carries its name, what it is, where its code lives, and what it does.

---

## 1. THE SUPERCHARGER BUTTON — Purple Jewel CTA
**What it is:** the primary call-to-action. A real object, not a flat button: a purple jewel border around a dark obsidian face, a glowing jewel star icon, deep shadow with a purple halo. It lifts on hover — that lift is the flow.
**Code:** `NAYA_ACADEMY.md` §08–11 — `.ny-button`, `.ny-primary`, `.ny-button-face`, `.ny-icon`, `.ny-copy` / `.ny-title` / `.ny-sub`.
**Construction:** jewel border (linear-gradient 135deg: #fff6ff, #e5baff, #b565ff, #7a32e5, #42118d, #8f42ee, #e8c0ff) · dark face (145deg: #29222d, #151117, #09080b, #030305, inset top light + deep bottom shadow) · 2px padding so the border reads as a jewel rim · radius clamp(18px, 1.55vw, 25px) · width min(700px, 95vw) · min-height clamp(78px, 7.3vw, 112px) · shadows: 1px white rim, 8px/20px purple depth, 65px purple glow, inset top light · ::before 1px white light line across the top (76% width) · icon: circular radial jewel (#ffffff, #f4ddff, #d28cff, #9747ff, #5518a7, #22043f) · title clamp(15px, 1.42vw, 22px) weight 780 + sub clamp(10px, 0.84vw, 13px) rgba(255,255,255,0.78) · hover translateY(-4px) + brightness(1.07) · active translateY(1px) scale(0.995) · focus-visible 3px outline rgba(222,190,255,0.96) · reduced-motion disables the transform.
**Live label:** "Start Your Free Trial" / "Step Into AI Mastery + Human Empowerment".
**Use it for:** every call-to-action on every page. Tier buttons keep their tier identity but use this same construction. The primary stays purple.

## 2. THE PORTAL GRID — Four Jewel Doors
**What it is:** four secondary buttons in a grid, each a real object with its OWN jewel color and its OWN hover glow. One color, one job.
**Code:** `NAYA_ACADEMY.md` §12–19 — `.ny-secondary-grid`, `.ny-secondary`, §15–18 icon colors, §19 hover glows.
**Doors:** Free Gifts — magenta (#ff77dc, #e62ab8, #9d1680, #470635), gift-box icon · ProMax Player — sapphire blue (#6bdcff, #1689ed, #0755a9, #032550), play-jewel icon · AI Masterclass — indigo / electric violet (#7674ff, #4b42d6, #29228e, #100b45), neural icon · Take Your Power Back — emerald (#63efb4, #19bd79, #08744a, #023624), power-crown icon.
**Use it for:** secondary actions, destinations, doors — anywhere a page offers more than one way in.

## 3. THE MEMBERSHIP PLAQUE — One Membership Seal
**What it is:** the glass plaque that seals a page: kicker, serif title, diamond divider, italic sub, max statement, four-color signature line.
**Code:** `NAYA_ACADEMY.md` §20–26 + the Final Membership Signature Polish block — `.ny-membership`, `.ny-membership-inner`, `.ny-membership-kicker`, `.ny-membership-title`, `.ny-membership-divider`, `.ny-membership-sub`, `.ny-membership-max`.
**Live words:** "ONE MEMBERSHIP — Everything Included. Your next level starts here. LEARN AI. BECOME YOUR MAX."
**Use it for:** the close of a sales page, the seal on a membership page, any place the page says what the whole thing is in one breath.

## 4. THE CINEMATIC THEATER — Jewel Video Frame
**What it is:** a 16:9 video inside a jewel frame — gradient rim, deep shadows, glass light on top. The video is an object on the stage, not a rectangle on the page.
**Code:** `NAYA_ACADEMY.md` §04–06 — `.ny-theater`, `.ny-screen-frame`, `.ny-screen`, `#ny-youtube-player`.
**Live video:** "NayaNET — The Network of Human Potential and AI Mastery" (YouTube 8tApdV0UpRs).
**Use it for:** any page that carries a video — the frame is the part, the video is the content.

## 5. THE NINE SYSTEMS — What Each System Changes
**What it is:** nine activated systems, each with a number, a name, a one-line promise, and five concrete "what changes" bullets (◆ ✦ △ ✧ ✦). The nine are the nine orbs — same nine, same names.
**Source:** the Academy page, "What each system changes for you" — 01 Personality · 02 Naya Brain · 03 Naya Notes · 04 Naya Lead Mode · 05 Naya Law · 06 Naya Scorecarding · 07 Naya Language · 08 Naya Design · 09 Naya Coder.
**Use it for:** any page that has to show what a system does — the five-bullet benefit grammar is the presentation, the nine names are the content.

## 6. THE DIFFERENCE BLOCK — Operating System Contrast
**What it is:** two columns, one header naming the difference: "THE DIFFERENCE IS THE OPERATING SYSTEM" — AI MASTERY ("Learn how to use AI. You learn the skills.") vs NAYA POWER ("Activate AI to work with you."). The difference is obvious in one glance.
**Source:** the Academy page, "THE DIFFERENCE IS THE OPERATING SYSTEM" section.
**Use it for:** any free-vs-power, before-vs-after, learn-vs-activate contrast. Mirror it: name the difference in the header, one line per side.

## 7. THE KEY — Included Value Line
**What it is:** a named key, a one-line promise, a dollar value attached: "KEY 4 · NAYA POWER INCLUDED — The Naya Supercharger. Skip the struggle. Start further ahead. $300+ Included value with Key 4."
**Source:** the Academy page, "KEY 4 · NAYA POWER INCLUDED" section.
**Use it for:** any place a page has to say what is included and what it is worth — name the key, name the promise, name the value.

## 8. THE PAYOFF CLOSE — Same AI Close
**What it is:** one line that says the whole thing: "THE PAYOFF — Same AI. Different operating system." The difference is not another list of prompts. It is the way the intelligence is configured to work with you.
**Source:** the Academy page, "THE PAYOFF" section.
**Use it for:** the close of any presentation page — the one-line reason the whole page exists.

## 9. THE ACADEMY DAYS — Five Jewel Lesson Boards
**What it is:** the five-day experience — one jewel board per day, five-color spectrum, MAXIS-inspired living boards. The training, presented as objects.
**Code:** `NAYA_ACADEMY.md`, the "FIVE-DAY EXPERIENCE — AAA JEWEL EDITION" block (after the membership polish block) — `.ny-academy-experience`.
**Use it for:** any multi-day journey — the pricing page's nine-day journey (days 1–5 training wear the Academy's five colors; days 6–9 continue the spectrum).

---

## INCOMING — NOT YET A PART (file when verified)
**THE SPEEDOMETER CALCULATOR — Earnings on the Gauge.** The live earnings calculator built into the pricing page (round 5): pick a plan + a pace, the speedometer needle shows what you would make (50% of plan price per sale, recurring monthly). Joins this folder as a named part only when the pricing page lands and the calculator is blind-verified (spot-checks: 3 Max/day = $4,500/month; 1 Pro/day = $750/month; 3 Power/month = $37.50/month). Until then it is a build, not a part.

## THE ULTIMATE PRESENTATION PAGE — built from these parts
The pricing page (round 5) is the first page composed from this harvest: supercharger hero frame + nine systems + difference block + nine-day journey (Academy Days) + calculator on the speedometer + supercharger buttons everywhere + membership plaque close + payoff line. When it lands and verifies, file IT here as a whole-page template: "The Ultimate Presentation Page — the page that lets them decide to buy or not."
