# Your Intelligence Today — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/today`. **Accent:** sapphire `#3b82f6`-family (sparingly: hero rule, active tab rail, card markers). **Build order:** 1.

## Shell contract

Sidebar unchanged (11 rooms, same order). Naya right rail unchanged. Only the center workspace swaps. Route change `hub/today` must not reload shell, sidebar, or Naya panel. Reduced-motion respected; keyboard navigable; 15px body minimum per current type decision (pending Shawn's 17–18px ruling).

## Component tree (center workspace, top to bottom)

1. `TodayHero` — eyebrow "YOUR INTELLIGENCE TODAY" (oversized, ~40px), date line (full weekday, month, day, year), one-sentence day summary (generated from evidence or honest-quiet fallback).
2. `TodayPulse` — five stat blocks: INTELLIGENCE EVENTS / DISCOVERIES / LEARNING SIGNALS / DECISIONS / CREATIONS. Each: large number (~44px), small caps label, truth seal dot. Numbers bind to canonical counts; unknown → "—" with `not_verified` styling, never 0-as-fact.
3. `WhatChanged` — narrative line ("Three things became clearer today." — count is dynamic, grammar-aware) + up to 3 `ChangeCard`s in horizontal arrangement (stack on narrow).
4. `ChangeCard` — kind badge (DISCOVERY/LEARNING/DECISION), one-line narrative, expandable evidence drawer (source notes, timestamps, links).
5. `IntelligenceStream` — tab bar COLLECTIVE | PERSONAL | ACTIVITY (default Collective) + stream of Smart Note boards in "In a Nutshell" form. Tab switch re-queries the mode's source; shows mode-appropriate empty state.
6. `NayaReflection` — large panel: heading "What matters most today," synthesis paragraphs, inline evidence links, "Generated from N evidence items" footer. Empty state: "Naya has nothing to synthesize yet today."

## Data bindings

- Pulse counts ← canonical intelligence store (events, discoveries, learnings, decisions, creations for the calendar day, user timezone).
- ChangeCards ← top-ranked day items by significance scoring; each carries `evidence_ids`.
- Stream modes ← Collective: network intelligence (consent-filtered); Personal: private store; Activity: operational truth log.
- Reflection ← synthesis over the day's evidence set; if evidence set is empty, panel shows honest empty state.

## States

- `loading`: skeleton shimmer on pulse + cards (no fake numbers).
- `live`: all bound.
- `quiet-day`: pulse shows real zeros-as-counts (verified zero, not unknown), narrative says the day was quiet and why.
- `offline/degraded`: LED in room header; cached day shown with "as of <time>" stamp.
- Truth seals on every card: VERIFIED / NOT_VERIFIED / LOCAL_DRAFT / UNKNOWN.

## Interactions (control → consequence)

- "Play the day" → guided tour overlay stepping through ChangeCards then Reflection; ESC exits; progress is local state only.
- Mode tab → re-query + stream replace + URL param `?mode=`; persists per session.
- Card expand → evidence drawer inline (no modal unless evidence is long).
- Save to list → list picker → pointer added (no duplication); toast confirms.
- Share → Smart Connect share preview (what/with whom/reversible) → receipt in Ledger on confirm.
- Ask Naya → Naya panel focuses with the card's context attached.
- "What did I miss?" → Naya answers from evidence in-panel; "nothing found" when empty.

## Design tokens

- Accent sapphire; surfaces obsidian `#0a0a0f`-family; text white/high-contrast; gold reserved for truth seals only.
- Primo buttons: obsidian body, beveled edge, elevation, sapphire energy on primary, hover lift, press compression, visible focus.
- Density: generous whitespace; one idea per viewport beat.

## Room ladder (per-room acceptance)

States defined → data bound → interactions real → implemented → browser-tested (route, reload, tab switch, tour) → runtime-tested (real counts) → persistence-tested (day survives reload) → proof recorded. Ship bar: 9.0+.
