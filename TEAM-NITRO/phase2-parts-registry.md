# Phase 2 Complete: Smart Factory Parts Registry

## The 16 Design Systems — Harvested

| System | File | Parts | Type |
|--------|------|-------|------|
| Beautiful Button Set N4 | Naya_Beautiful_Button_Set_N4.html | 53 buttons | Buttons |
| Epic Elements (Lego N5) | Naya_Epic_Elements_-_Lego_pieces_N5.html | 27 elements | Mixed |
| Jewel Library N5 | Naya_Jewel_Library_-_N5.html | 4 jewels | Orbs/Jewels |
| Elite Buttons N5 | Naya__Elite_Buttons_N5.html | 26 buttons | Buttons |
| Building Blocks | Naya_Building_Blocks_-_The_Ultimate_Design_System_-_Naya_2.html | TBD | Blocks |
| Design Element Set N4 | Naya_Design_Element_Set_N4.html | TBD | Elements |
| Design Elements N2 | Naya_Design_Elements_N2.html | TBD | Elements |
| Design Standard Showcase | Naya_Design_Standard_Showcase__1.html | TBD | Reference |
| Lego Blocks N4 | Naya_Lego_Blocks_N4.html | TBD | Blocks |
| Ultimate Design System | Naya_Ultimate_Design_System_-_Naya_2.html | TBD | System |
| Smart Hub Design | Naya_Smart_Hub_Design.html | TBD | Hub parts |
| Smart Blocks | naya-smart-blocks.html | TBD | Blocks |
| Ask-Naya Design | Ask-Naya-Page_Design-2.html | TBD | Page parts |
| Smart Spaces Design | Smart_Spaces_Page_Design.html | TBD | Space parts |
| Welcome Design | Welcome_Page_Design.html | TBD | Onboarding |
| Maxis App Design | Maxis_App_Design.html | TBD | App parts |

## The Ultimate Number — A Digital Asset (2026-11-07)

| Asset | File | Parts | Type |
|-------|------|-------|------|
| The Ultimate Number | TEAM-NITRO/number-concepts/top-10-number-concepts.html (blob c08aab17, 30,655B) | tile, reel, cap, platter, flash, fit | Number |

The number is an element on its own — an object of itself. Each digit is a tile built from the Dashboard button anatomy: 2px coloured rim, glossy cap, black gradient face, white digit, halo and drop shadow. Chakra colours (1 red, 2 orange, 3 gold, 4 emerald, 5 cyan, 6 indigo, 7 royal purple, 8 lavender, 9 hot pink, 0 white). Slow-mo staggered reveal, colour-sync flash, dynamic growth (725 → 7,250 → 10,725), no limit (tiles shrink to fit the page). Shawn's verdict: better than he envisioned, a work of art, locked. Used by the Dashboard (number + gauge) and the Pricing calculator (Power / Pro / Max → the number they can make). Smart Note SN-2221. The rule: any page that needs a number harvests this one — never invent a new one.

## The Academy Conversion Sections — Digital Assets (2026-11-08)

| Asset | File | Size | Type |
|-------|------|------|------|
| Academy conversion page (Block 1) | DESIGN-BLOCKS/academy-assets-20261108/academy-conversion-page.html (blob d5d786d8, 46,335B) | 46,335B | Conversion |
| Academy five-day experience (Block 2) | DESIGN-BLOCKS/academy-assets-20261108/academy-five-day-experience.html (blob bd0dabfe, 42,639B) | 42,639B | Conversion |
| Academy CTA override (Block 3) | DESIGN-BLOCKS/academy-assets-20261108/academy-cta-override.js (blob b1156e1f, 7,885B) | 7,885B | Conversion |
| Academy E05 — Does Any of This Sound Familiar? | DESIGN-BLOCKS/academy-assets-20261108/maxess-e05.html (blob 4cc851a7, 13,882B) | 13,882B | Conversion |
| Academy E06 — Meet the Naya Supercharger | DESIGN-BLOCKS/academy-assets-20261108/maxess-e06.html (blob 21c546e9, 55,467B) | 55,467B | Conversion |
| Academy E08 — Human Maximus Ecosystem | DESIGN-BLOCKS/academy-assets-20261108/maxess-e08.html (blob bd3559bc, 23,700B) | 23,700B | Conversion |
| Academy E09 — Member Preview | DESIGN-BLOCKS/academy-assets-20261108/maxess-e09.html (blob 1f13e373, 15,026B) | 15,026B | Conversion |
| Academy assets index | DESIGN-BLOCKS/academy-assets-20261108/README.md (blob c0122e44, 3,922B) | 3,922B | Index |

CORRECTION (Shawn, 2026-11-08 21:15Z): these are Academy / Human Maximus conversion sections. They are NOT the MAXESS engine — MAXESS is the future scoring engine (15 questions, answers worth 4/3/2/1/0, percentage + level report). The filenames keep their sent names (maxess-e05 etc.) verbatim; the name in this registry is the correction. Source: the Academy page's full source as sent by Shawn 2026-11-08 ~20:50Z; local files ~/workspace/team-nitro/factory-assets/academy/ (208,856B total). Layers stay separate, fragments stay fragments; the CTA override is truncated as sent. The local README still carries the pre-correction "MAXESS" labels — the file is verbatim, the correction lives here and in the commit messages.

## Parts Categories for the Generator

1. **Buttons** (110+): From Beautiful, Elite, Epic — all spectrum colors, all states
2. **Orbs/Jewels** (4+): From Jewel Library — the 3D objects
3. **Blocks** (TBD): From Building Blocks, Lego — layout components
4. **Elements** (TBD): From Design Elements — UI primitives
5. **Page Parts** (TBD): From Ask-Naya, Spaces, Welcome — page-specific components
6. **Numbers** (1): The Ultimate Number — the only number; every page harvests it

## The Rule

Every part in the registry traces to one of these 16 files. The generator pulls from here. Nothing is invented. Everything is harvested.

Phase 2 complete. Moving to Phase 3: Build the universal template.
