# Naya Smart App Lego Blocks

The complete set of reusable components. A cold Naya takes these blocks and builds a beautiful Smart App without asking a single design question.

**Your idea. Your intelligence. Your Smart App. Your internet, your way.**

## The Blocks

| # | Block | File | Score |
|---|-------|------|-------|
| 00 | Design Tokens | `naya-tokens.css` | foundation |
| 01 | Hero Buttons | `01-hero-buttons.html` | 98/100 |
| 02 | Standard Buttons | `02-standard-buttons.html` | 98/100 |
| 03 | Boards | `03-boards.html` | 99/100 |
| 04 | Jewels | `04-jewels.html` | 99/100 |
| 05 | SmartTabs v9 | `05-smart-tabs.html` + `smart-tabs/` | 99/100 |
| 06 | Typography | `06-typography.html` | 99/100 |
| 07 | Truth Pills | `07-truth-pills.html` | 99/100 |
| 08 | Icons | `08-icons.html` | 99/100 |

Every block scores **95+** on the Naya Design Calculator. Every block is a self-contained demo page: live examples, usage instructions, the design law, and copy-paste code.

## How to Use

1. **Start with tokens.** Include `naya-tokens.css` first — every block depends on it.
2. **Pick your blocks.** Each block's HTML page shows the component live, explains when to use it, and gives you the exact code to copy.
3. **Follow the laws.** Each block documents the design law it implements. The laws are not suggestions.
4. **Check your work.** Run the Design Calculator on your page. If it's under 95, the calculator tells you exactly what's wrong.

## The Laws (summary)

- **Spectrum is law:** magenta → purple → blue → green → gold, cycling to magenta. Every sequence follows it.
- **Color is identity:** one color job per thing. Adjacent things never share a hue.
- **Black ground, white light, purple soul.** White text 99% of the time.
- **Quiet at rest; ignites on touch.** The object's own color ignites on hover.
- **Flat is dead.** Everything dimensional: bevel, elevation, glow.
- **Jewels, not dots.** Drawn, glowing, spectrum order, never twice adjacent.
- **Verified glows green; claims stay quiet.** A claim without verification is a lie told to yourself first.
- **24 / 18 / 14.** Body 18px always. Hierarchy by size, never color.
- **The details are the design.** No missing spaces, no stranded boxes, no overlaps.

## SmartTabs Kit

The standalone SmartTabs v9 kit lives in `smart-tabs/`:
- `smart-tabs.css` — all styles
- `smart-tabs.js` — the engine (`SmartTabs.mount()` API)
- See `05-smart-tabs.html` for the install guide

## For Naya Builders

You don't need to ask how to design. Open any block page, see the component live, read the law, copy the code. If you follow the blocks and the laws, the calculator will confirm: 95+, elite, ships.

That's graduation: building beautiful without being told how.
