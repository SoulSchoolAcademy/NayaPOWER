# BLESSED 05 — Briefing Strip · Blessing Report
**v1.0.0 · Built 2026-10-31 · Builder: Nitro lane (subagent)**
**Factory gap #1** (parts map v1 §(a)): the single most-needed missing part — Dashboard · Intel Today · Reports. No registry entry or block existed before this build. This is canon inventory #5.

## The part (ONE importable file — import, never copy)
| Part | File | sha256 |
|---|---|---|
| 05 Briefing strip | `nj-briefing-strip.html` | d1f99ac216a0 |

One self-contained file: `<style>` once per page + documented markup pattern + `<script>` once per page (idempotent via `window.NayaBrief`). Specimen assembled verbatim by `build-specimen.py` — never hand-copied.

**The shape:** one horizontal strip, full width — WHAT (the fact) + WHY (why it matters) + ONE VERB (the action). The Tell-Me-My-Stats strip. The whole strip is ONE control (`<a>` or `<button>` — documented both patterns).

## Law compliance (measured, not claimed)
- **DNA**: obsidian face `linear-gradient(180deg,#17171e,#0a0a0f 70%,#050507)` · white rim **2px** at rest (measured) · hairline top edge light · own-color ignition on touch ONLY · cast shadows, never glow-as-depth · white text always.
- **Measured rest**: border `2px solid rgba(255,255,255,.3)` · min-height 60px (≥44px) · radius 18px · box-shadow present · what `rgb(255,255,255) 16px/800` · why `rgb(255,255,255) 15px/500` · verb `rgb(255,255,255) 15px/800` — hierarchy from size/weight, never color (Law 1).
- **Measured hover**: rim `rgb(160,107,255)` (own color) · arrow own-color + `translateX(4px)` · text stays white.
- **Law 6**: rest background contains zero spectrum tokens (gate-scanned). Ignition is edge-only: rim + own-color glow + arrow.
- **Law 5/4**: one strip owns one color; specimen walks purple → blue → green → gold → orange → red → magenta (Law 10 sequence), adjacent strips never share a hue.
- **Tokens**: verbatim only. No private hexes.
- **States, all defined**: rest · hover-touch (lift −2px, rim ignites, arrow nudges) · press (sink +1px; `nj-is-pressed` via touch handlers — `:active` is unreliable on mobile Safari, measured) · focus-visible (rim + own-color ring, always visible).
- **Phone (390px)**: wraps gracefully — separators retire, verb keeps its own tappable line; scrollWidth 390 = zero overflow (measured).
- **Accessibility**: min-height 60px · keyboard focus ring · `prefers-reduced-motion` respected · native `<a>`/`<button>` semantics (no ARIA inventions).

## Gate: 19/19 PASS at 1440px + 390px · Zero JS errors
`design-gate.py --file specimen.html --widths 1440,390` → **GATE PASSED** (evidence/gate-output.txt). Includes Law 6 no-colored-control + no-colored-text checks.

## Rendered review (builder)
- `evidence/specimen-1440.png` — spectrum walk renders premium: obsidian faces, clean white rims, white text, verbs right-aligned with colored arrows; hover/press/focus states visually distinct.
- `evidence/specimen-390.png` — wraps cleanly, no overflow, verb keeps its own line.
- `evidence/nj-ev-hover.png` — hover clip: purple rim ignition, arrow nudged, text white, face obsidian.
- One fix made during build: phone wrap left a dangling `·` after the why — both separators now retire on phone; lines read clean.

## Ten-star self-score: 9/10 (honest, test by test)
1. **Awe AND ease** — pass. Beautiful and instantly readable in one glance.
2. **Everything works** — pass. The whole strip is one control; no dead elements.
3. **Nothing invented** — pass. The part takes real content via markup; specimen copy is labeled specimen (same convention as 01).
4. **Alive, not decorated** — pass. Ignition, arrow nudge, press sink, touch press-state — all with purpose.
5. **Ends when its value ends** — pass. One line, no filler.
6. **Speaks human** — pass. "825 points to go — about 33 wall posts at your pace · See how."
7. **One shot** — pass. Arrives finished.
8. **His eye is the gate** — **unproven** (by definition at builder stage). The −1.
Never inflated: a 9 is the highest a builder can honestly claim before his eye and the Same-Language pass.

## How it connects (the import contract — verbatim, never rewritten)
Three steps, in this order, copied verbatim from `nj-briefing-strip.html`:
1. Paste the `<style>` block **once per page** (in `<head>`).
2. Use the markup pattern **per briefing instance** — an `<a class="nj-brief">` (whole strip is one link; give it the destination `href`) or a `<button type="button" class="nj-brief">` (action variant, no destination). Both patterns are documented in the file's header comment.
3. Paste the `<script>` block **once per page** (before `</body>`).
- **Idempotent**: the script exits immediately if `window.NayaBrief` exists — pasting it twice (or two strips on one page) never double-binds. Proven by the guard at the top of the IIFE.
- **Per-instance color**: set `--nj-c` (verbatim spectrum token) + `--nj-c-rgb` (same color as r,g,b) inline per strip. One strip owns one color; adjacent strips never share a hue (Law 4/5).
- **No build step, no dependency, no framework**: the part works from the pasted bytes alone. Content flows in through the markup spans (`nj-brief-what`, `nj-brief-why`, `nj-brief-verb`) — the part never fetches, never invents.
- **Touch behavior**: the script adds `nj-is-pressed` on `touchstart`/`touchend`/`touchcancel` because `:active` is unreliable on mobile Safari (measured during build).

## Its family (who it composes with, who consumes it)
- **Same DNA as blessed-01** (the jewel button family): identical obsidian face gradient (`linear-gradient(180deg,#17171e,#0a0a0f 70%,#050507)`), white rim at rest, own-color ignition on touch only, white text always. A briefing strip beside a jewel button reads as siblings — you can tell they're family.
- **Spectrum walk**: adjacent strips walk the Law 10 sequence (purple → blue → green → gold → orange → red → magenta), same as every other blessed surface. Proven in `specimen-1440.png`.
- **Consumers** (parts map v1 §(a), factory gap #1): Dashboard · Intel Today · Reports — the Tell-Me-My-Stats strip each of those pages needs. First consumer: the reworked dashboard (same-language pass owed after the chart lands).
- **Companions**: stat orbs, pills, and charts feed it numbers; the strip's job is the sentence — WHAT + WHY + ONE VERB — never the raw data display.
- **Distinct from** the matrix's existing `briefing-strip` row (HERO family): that is the dashboard's living-intelligence strip (`living-intel-block.html` — breathing orb + living line + insight card). This part (`nj-briefing-strip`) is the one-line Tell-Me-My-Stats strip. Different files, different shapes, different jobs — both blessed, never confused.

## What remains for full blessing
- [ ] **Nitro's independent rendered review** (desktop + phone, real address) — the builder cannot bless its own work.
- [ ] **Same-Language pass** against the first consuming page (the reworked dashboard — its first consumer).
- [ ] File into the Smart Factory + PARTS-MATRIX entry (the filing law).
