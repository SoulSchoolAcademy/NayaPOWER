# THE NAYA CODE — the spec for making objects (Shawn, 2026-11-16 23:41Z)

## Why this document exists — the correction, owned

Shawn's words, 23:41Z: the Smart Note Studio is *"not exactly what I meant."* He did not mean a standalone place where someone types something random in and it outputs a note in one format or another, right on the spot — and he did not mean selling the feature, or selling the presentation, or a page that teaches people about blocks. What he meant: **when people go to create with NayaNET, they build pages — and when they put input in to create a page, we output it in the format they want.** The input → formatted output IS page creation. It lives inside creation, not as a feature to sell.

And the deeper assignment in the same message: he was trying to get alignment on high-level design. *"See, even on this page none of those boards are elevated, none of them are active, they're all dead. If you really understood, then all the boards and every button should all be active and alive — when I hover over any of them the whole thing would fill alive."* He is not asking for that page to be edited. He is asking for an elite designer by default — one who just knows the language and designs in it. So he uploaded the photos: 18 screenshots, so the language could be found in them, the pattern named, and the spec written — so objects (buttons, boards, icons) can be made and repeated from the spec, because the language can be seen.

This is that spec. It is written from the 18 photos he uploaded (`~/workspace/user/media_library/image/aaa_1.png` … `aaa_19.png`, `AAA_4.png` … `AAA_17.png` — the deck end, the founder's letter, the nine-systems hero, the vault, the pain boards, the pricing tiers, the Smart Feed card, the pricing chart, the letter view, the Smart Stats gauges, the Dashboard vortex, the Hub feed, the membership doors, the connections cards, the action pills, the bottom bar, the feed tabs). The palette was measured from the files: the black reads `#000000` at the dark end in every photo, and the bright colors cluster on the Playbook spectrum (purple, blue, green, gold, orange, red, magenta) — the photos agree with the Playbook's canonical hexes, which this spec keeps.

## §1 — THE ONE FAMILY (the family rule)

**One code. The same elements, in different ways. Never a new board, button, or icon — the same ones, recombined.**

Everything in NayaNET looks like the same family because it IS the same code. A button, an icon, and a board are one anatomy, one language (`THE-NAYA-DESIGN-LANGUAGE.md`): obsidian black inside, white in the middle as a real object, color on the edge, elevation, one light from the top-left, alive on hover. The family is not a style guide — it is the code the objects are written in. When a new page needs a button, it does not design a button. It takes the family's button and gives it its own color and its own word.

## §2 — THE OBJECTS (the catalog — every object, one construction each)

**1. THE BOARD.** The big one: the letter boards, the pain boards ("Why this happens" / "The solution" / "What's in it for you"), the Smart Note boards, the app cards. An obsidian slab, rounded corners (18–22px), a thin bright rim in its OWN color (red for pain 1, gold for the pains, purple for the deck), white text inside, elevated with a real shadow down-right. Three sentences per board, one idea each. Three boards, then a button. The face sits in a circle beside it (see 7), speaking what's in it.

**2. THE PILL BUTTON.** The row of eight (Message green · About gold · My World orange · Skills red · Connections magenta · Invite purple · Share blue · Join NayaNET green), the tier buttons (Choose Naya Power / Pro / Max), "Start free now ◆", "Keep reading ◆", "Enter NayaNET ◆". An obsidian pill (radius 999px), rim in its own color, icon on the LEFT, white word(s) in the middle. Two-line variant: the label on top, the subtext under it in smaller white. The pill is the button — the same pill everywhere, only the color and the word change.

**3. THE TILE.** The bottom bar's six (+, mail, activity, home, grid, +). A square obsidian tile (~14px radius), rim in its own color, white glyph in the middle as a real object with depth. One tile, one glyph, one color.

**4. THE ICON.** The circle inside the rectangle (sidebar buttons), the orb (the Smart Note's purple orb, the gauge jewels). An obsidian circle, rim in its own color, white glyph as an object — a jewel piece, never a dot. The icon represents what it is: mail is a mail glyph, home is a home glyph, a mic for Ask, a heart for Life. Two identical shapes in different colors are not two icons.

**5. THE DIGIT TILE.** The prices ($25 / $50 / $100, struck-through $50 / $100 / $200), the match percentages (94% / 91% / 88% / 92% / 89%), the points (408), the clicks (1566), the money ($4,500 / month). An obsidian tile, rim in its own color, white digit(s) in the middle. Number on top, label underneath ("CLICKS", "JOINS", "/ month"). A digit's color is its digit's color — the number is the hero, the tile is the machine around it.

**6. THE CHIP / TAB.** The topic chips (All, The Intelligent Internet, AI Is Hiring…), the feed tabs (Personal blue · Collective gold · World green · Worlds purple), the range pills (HOUR / DAY / WEEK / MONTH / ALL), the mode pills (PTS / % / MONEY). An obsidian pill, rim in its own color when lit, white word. The lit one lights up in its own color; the rest wait quietly in obsidian and white.

**7. THE FACE CIRCLE.** Naya's face in a circle beside the speaking board — top-right in the deck with a green glow, top-left in the pain boards with a gold rim, beside the Smart Feed card. The circle's rim takes the board's color. She is quoting the board, speaking it to them. The placeholder before a citizen uploads their own picture is a neutral glowing orb/monogram — never a stock photo of a person.

**8. THE GAUGE / DIAL.** The Smart Stats gauges, the Dashboard vortex (0–500, needle lapping in sets of 500, "1ST LAP — 398"), the money gauge ($4,500 of $10,000). An obsidian dial, an aluminum ring, a needle, digit tiles orbiting it. The number is the hero; the gauge is the machine that carries it.

## §3 — THE STATES: ALIVE (the law the photos break)

This is the first law of the spec, because it is the failure the photos show: **in the photos, none of the boards are elevated, none are active, they are all dead.** A Naya object is never dead.

- **REST:** obsidian + white + rim. Quiet, but present — elevated, shadowed, real. A real object sitting on the page, not a flat picture of one.
- **HOVER:** the whole thing comes alive. It lifts. The outside light ignites in its own color — the rim brightens, the halo and underglow appear, the white in the middle pops. Not a color change. A physical response: the object fills alive under the hand.
- **ACTIVE / PRESSED:** it depresses (scale 0.97), the light shifts across its surface.
- **DEAD IS A DEFECT.** A board or button that does nothing on hover is unfinished, whatever else it does. The check: hover every object on the page. If nothing comes alive, it is not done. The checker names the dead ones; the maker brings them alive.

## §4 — THE COLOR LANGUAGE (which color means what)

The spectrum is the Playbook's, and the photos confirm it: purple `#a06bff` joins / primary · blue `#3fb8ff` smart notes / information · green `#2fe89e` shares / positive · gold `#ffbf3d` comments / attention · orange `#ff9a5a` creating / energy · red `#ff5e6c` likes / urgency · magenta `#e84fff` sales / premium. The photos add the per-object mapping, which the spec records so it is never re-decided: Message green, About gold, My World orange, Skills red, Connections magenta, Invite purple, Share blue, Join NayaNET green; Personal blue, Collective gold, World green, Worlds purple; Naya Academy purple, AI Masterclass blue, Fast Action Club green; Ask purple, Life green.

The rule, always: the rim takes the object's OWN color. At rest the page is obsidian and white. Color ignites on touch, in the element's own color only. No colored backgrounds. No color washes. No gray text — white, or bright high-contrast.

## §5 — THE CONSTRUCTION (how to build one — the repeatable part)

- **HARVEST, NEVER INVENT.** The canonical bytes live in the three reference objects (`THE-NAYA-DESIGN-LANGUAGE.md` §3): the top-left + (the button), the Smart Note board (the board and the black), the X button (the inside). A new object is measured against them, by eye.
- **THE BLACK:** board black, harvested verbatim from the Smart Note board. The photos measure `#000000` at the dark end — black black, obsidian glass, never off-black inside an icon or button.
- **MEASUREMENTS:** spacing in multiples of 8px (8, 16, 24, 32, 48, 64, 96). Text 12 (caption), 14 (body), 16 (subhead), 20 (headline), 28 (hero), 48 (display). Rims thin and bright (1.5–2px; edge bars 2–3px). Pills radius 999px; boards 18–22px; tiles ~14px. Light at 135°, shadow down-right. Every position calculated, never eyeballed.
- **THE WHITE:** the white in the middle is an object with depth and its own edge light, sitting ON the black — never a flat mark written onto it.
- **THE LIGHT:** one source, top-left, always. The light lives OUTSIDE only — rim, halo, underglow. No glow inside, ever.

## §6 — THE FAMILY TEST (how a maker proves it)

- Does it look like its siblings? Same black, same rim rule, same white, same elevation, same light. Hold it next to the three reference objects — does it speak the same language?
- Hover it. Does the whole thing come alive?
- Which reference object was it measured against? Named, not assumed.
- Read it as a reader. Shawn's eye is the final gate.

## §7 — WHAT THIS CHANGES (recorded, so it is never re-argued)

- **THE STUDIO IS THE CREATION ENGINE, NOT A FEATURE.** The Smart Note Studio's engine — speak or type anything in, out comes the format they want (unfold down or sideways, six perspectives) — is HOW PAGES GET CREATED inside NayaNET. It lives in creation. The standalone page stands as the engine's proof, not as a product to sell, and never as a page that teaches people about blocks. The Black Diamond fix round on the Studio file stands — the file holds the engine's code, and its buttons must speak the language too.
- **THE PHOTOS ARE THE CANON.** The 18 uploaded screenshots are the visual reference set for this spec. When the spec and a photo disagree, the photo is read first and the disagreement is named — never silently resolved.

## §8 — THE ORBIT (circles have flow around them — Shawn, 2026-11-16 23:52Z)

**Boards light up. Circles have circles flowing around them.**

A circle in NayaNET is never a still circle. It carries flow: one or more rings — or an orb — circling around it, moving slowly, alive. In most cases, ALL circles have flow around them: the face circle, the + button, the orbs, the gauge jewels, the icon circles. The circling is what makes them feel alive — they are circling, they are moving, they are not dead pictures. The motion is slow (ambient 60–180s, per the Playbook — never frantic, never faster than 12s), and concentric sets alternate direction (CW, CCW, CW, CCW — the alternation is the vortex). And boards light up: on hover the WHOLE board fills alive — the board itself lights, not just its rim — the light, the lift, and the orbit together. A circle without flow, a board that does not light up, is unfinished.

## §9 — THE OFFICIAL FORMATS (the unfold and the slideshow — Shawn, 2026-11-16 23:52Z)

There are two official formats, and they are ONE idea: **press the button, go to the next experience.** Press the button, go to the next block. Go to the next image. Go to the next board. It feels interactive because it IS interactive — and in their brain they are taking bits in at a time, instead of taking the whole web page or the whole book. We understand human psychology: they can only take in so much. Break up the colors, have the contrast, have the elevation, make it feel alive — and the experience is a whole lot better for them. They like that. It feels better, it looks better, it IS better.

- **THE UNFOLD (going down).** Press the button, the next piece unfolds down the page. One board at a time, one idea each, three sentences per board. The letter unfolds down. The deck's unfolding, harvested verbatim, is the model.
- **THE SLIDESHOW (going sideways).** Press Next, the next screen slides in. One screen at a time, one image or board, with Back and Next. The deck slides sideways.

Both formats are OFFICIAL — one canonical implementation each, harvested verbatim from the proven source, reused everywhere, never reinvented per page. The Smart Note Studio's engine (speak/type anything in, out comes the format they want) is the creation engine that outputs in these formats — it lives in creation, and every page created comes out in one of these two formats, the citizen's choice.

## §10 — THE PAGES THAT SPEAK THE LANGUAGE (Shawn, 2026-11-16 23:52Z)

The whole system speaks this language, and everything built in the future is built in it. The pages:

- **THE UNIVERSAL SMART APP — the Smart Feed.** It automatically syncs up the content and the users, and presents in the universal format. That is what it is called: the Universal Smart App.
- **THE CENTER HUB.** A little bit different, but similar — the center, the home, the main page.
- **THE PERSONAL PAGES.** About and Skills — the presentation of them, their skills. The World is the calendar. Connections — all their contacts, the list. Invite — inviting people. Share and Join. **About and Skills each get BOTH presentations — the unfold down AND the slideshow — with a bridge page: in a nutshell about, then "which presentation do you want?"** Click a button, see one presentation; click the other, see the other. The same for Business and Space, so they get to know all about it, with a presentation right on the page.
- **SMART LISTS and CONNECTIONS — the same style.** Organizing and grouping of lists, and matching people up. One style for both.
- **THE CORE UNDERNEATH — Auto Match and Auto Organizer.** The core system underneath everything.
- **SMART FEEDS and SMART TABS.** The tabs organize the feeds into topics, into sub-topics — and you can save those feeds.
- **SIDEBARS and PLUS BUTTONS.** They let you access your world, on each page — and if you want to see what's going on, the plus buttons open it.
