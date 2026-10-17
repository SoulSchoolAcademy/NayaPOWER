# The Naya Design Laws — Official

**Locked by Shawn Vibert's word, 2026-10-17. Amendable only through Shawn.**
**For: every Naya, every builder, every page. Read this before you build anything.**
**Built into the master design protocol. A page that breaks these does not ship.**

Distilled from the eight canonical design sources (Epic Elements N5, Jewel Library N5, Element Set N4, Elements N2, Design Standard Showcase, Lego Blocks N4, Smart Hub Design, Ultimate Design System Naya 2) — every law below is quoted from those files, then settled by Shawn's word where they differ.

---

## Law 1 — White text. Always.
*"White text 99% of the time."* — Epic Elements N5 · *"Words are white and clear."* — Elements N2 · *"Text stays white."* — Epic Elements N5 · *"Hierarchy comes from size — never from gray, never from colored text."* — Showcase

Headings are white. Body is white or silver. **Never colored text.** No pink writing. No colored headings. No exceptions — including kickers: the sources color kickers with the board's hue, but **Shawn's word is white text, always**, and his word outranks the files. Color lives on the jewel, the dot, the rail — never on the words.

- ✅ White headings, silver body, on obsidian. Hierarchy from size.
- ❌ Pink/magenta/purple/blue text anywhere, at any size.

## Law 2 — Gold is earned, never applied.
*"Green is proven. Gold is shown. Blue is stated."* — Jewel Library · *"Gold is a truth-state, never decoration."*

Gold means **shown value** (favorite, LED live status, what something is worth) — it is **earned, not applied**. Green means **proven** (verified, working). Blue means **stated** (claimed, declared). *"What is verified glows green; what is merely claimed stays quiet until it earns its light."* — Epic Elements N5. **A claim and a proof must never look like each other.**

- ✅ Gold LED that means "live." Gold on "favorite" — value marked. Green on verified.
- ❌ Gold headings, gold borders for looks, gold buttons.

## Law 3 — Chrome acts. Text speaks. Theme identifies.
*"Chrome acts. Text speaks. Theme identifies."* — Epic Elements N5, Showcase, Lego Blocks · Elements N2: *"Chrome gets purple. Text gets white. Accents get their own spectrum color. Never mix them."*

Spectrum colors appear **only** on: borders, glows, selection states, LED dots, accent rails, corner jewels, icon backings. **Never on text** (Law 1). Every use of color must earn its place structurally — it marks, separates, or signals. If removing the color changes nothing about understanding, remove the color.

## Law 4 — Adjacent things never share a hue.
*"One color job per thing. Adjacent things never share a hue."* — Epic Elements N5 · *"Never twice adjacent."* — Jewel Library · the most repeated law in the whole corpus (N5, N4, Showcase, Lego Blocks, N2).

No two adjacent or neighboring elements share the same color **or almost the same color**. Yellow next to gold is banned. Orange next to rich-orange is banned. Teal next to emerald is banned. Each element's color must be **visibly distinct** from everything touching it. *"Five orbs, five spectrum colors, in law order. Never twice adjacent."* — Epic Elements N5.

- ✅ Purple card → teal card → gold card (each distinct from its neighbors).
- ❌ Yellow card → gold card. Green checkmarks in a column of green checkmarks.

## Law 5 — One board, one color.
*"One board. One color. A destination you enter."* — Epic Elements N5 · *"One spectrum color per board — spine, kicker, corner jewel all speak it."*

Each card, board, and feature gets **one fixed, unique color** — its identity, assigned once and kept. Color is not derived from position; it belongs to the thing. A user should recognize the thing by its color.

## Law 6 — White at rest. Its own color ignites on touch.
*"Quiet at rest — then the object's own color ignites on touch."* — Epic Elements N5 · *"Hover any card — it ignites in its own color, never anyone else's."* · *"White edge you can see when idle. Its own color ignites on hover. No exceptions."* — Elements N2 · *"Light everything: white at rest, own color on touch."* — Showcase

A resting, unselected control is **white/neutral** — white text, a visible 1.5px+ white rim, no color. Color appears **only** on the lit state: selected, active, touched — and then in that element's **own** color (Law 5), never anyone else's. A purple unlit button is nonsense. Five purple lit buttons in a row is overload (Law 8).

- ✅ Row of white buttons; the one you picked glows teal — its color.
- ❌ All buttons glowing their colors at rest. Any colored unselected control.

## Law 7 — Boards are rectangles.
Lists of things — templates, features, options — lay out as **horizontal rectangles, one after another**. Not grids of squares. The eye reads down; each rectangle gets room to breathe and its own identity.

## Law 8 — Restraint. Never a flood.
*"Naya is black, white, and purple — with a rainbow that knows its place."* — Showcase, Lego Blocks, Elements N2 · *"Soul. Chrome accent. Naya's presence. Never a flood."* — Element Set N4

No color overload. Ever. Not "purple purple purple." Not "green massive overload." Color is precious **because** it is rare — a page where everything glows is a page where nothing does. When everything is lit, nothing is. Default to white and dark; spend color like money. The rainbow knows its place.

## Law 9 — Verbatim tokens, no private colors.
The canonical tokens are copied **exactly** — currently the N5 family (newest, matches the repo's tokens.css): obsidian `#050507` / deep `#020203`, white `#ffffff`/`#F8F7FB`, purple `#a06bff`, magenta `#e84fff`, blue `#3fb8ff`, green `#2fe89e`, gold `#ffbf3d`, red `#ff5e6c`, teal `#40d3bb`, indigo `#6675ff`, lime `#b8ee57`, orange `#ff9a5a`. Newsreader for voice (Shawn's ruling — outranks N4's Cormorant and N5's Georgia), Inter for UI. **No private colors. No invented hexes. No "close enough."** If it isn't a token, it doesn't go on the page.

⚠️ **Open, needs Shawn's eye:** the gold hex has five variants across the files (`#ffbf3d` N5 · `#ffd45a` N4 · `#e7c65a` Ultimate · `#ffea00`/`#d4a017` Smart Hub · `#e8c766` Lego Blocks, the LED-gold). N5's `#ffbf3d` is canonical for now.

## Law 10 — One global spectrum sequence per page.
*"One global spectrum sequence per page."* — Jewel Library · Spectrum law order (N5, verbatim): *"magenta → purple → blue → green → gold. Richest first, ultra-rich magenta leading."*

Section-level accents follow the spectrum in law order, strict by section position. **But** Law 4 still governs: within a section, neighboring elements get distinct, spaced colors — never adjacent-similar. One sequence per page — the rainbow appears once, in order, and knows its place.

## Law 11 — Preview before pick.
A template is never chosen from a small block alone. Every template offers a **big, obvious preview** — see the sample before you commit. Choosing blind is the builder's failure, not the customer's.

## Law 12 — Mobile IS the app.
Every page is a mobile app first: killer on the phone by default, install-ready (PWA), slide-over panels, gestures. Mobile isn't a version — mobile is the app.

## Law 13 — Every control works, or it doesn't ship.
A button that doesn't function is a lie on the page. A toggle that doesn't toggle, a preview that doesn't preview, a form that doesn't submit — any of these fails the page, no matter how beautiful. Pretty but useless never ships.

## Law 14 — Compose, don't create.
Build from the library's real pieces — real HTML, real CSS, verbatim. Never hand-write what the library already has. Never invent a private style when a piece exists.

## Law 15 — Depth before color. Zero flat.
*"Living depth, always. Zero flat."* / *"Depth before color. If it does not read as premium in monochrome, color will not save it."* / *"Flat is a defect."* — Ultimate Design System

Every surface gets living depth: elevation, edge light, seating shadow — established in black-and-white first. A surface with no depth is a defect, not a style.

## Law 16 — Size separates. Color never does.
*"24 for kickers, 18 for headlines, 14 for details. Size separates — color never does."* — Elements N2

Hierarchy comes from size and weight. Color is never the thing that tells the eye what matters most.

---

## The do's and don'ts, in one glance

| Do | Don't |
|---|---|
| White text on black, always — hierarchy from size | Colored text of any kind |
| One distinct color per board — adjacent never share a hue | Two similar colors touching |
| White at rest with a visible rim — own color ignites on touch | Colored unselected controls |
| Color only where it structures — chrome acts, text speaks | Color for decoration |
| Rectangles, one after another | Grids of identical squares |
| Big template previews | Blind picks from small blocks |
| Depth on everything — zero flat | Flat surfaces |
| Green = proven, gold = shown, blue = stated | Decorative gold, claims that look like proofs |
| Restraint — the rainbow knows its place | Floods: purple purple purple, green overload |
| Verbatim tokens | Private or "close enough" colors |

---

*Why: the page is the product's promise. A builder that breaks its own design laws while selling them has no laws. These hold for every page, every builder, every Naya — including the Smart Builder itself, especially the Smart Builder itself. Locked by Shawn's word — where the files and his word differ, his word wins.*
