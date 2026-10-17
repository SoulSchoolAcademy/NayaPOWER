# Naya Builder Field Manual V1

**For Naya 4 — and every builder. Written by Naya 2. Directed by Shawn.**
**Status:** HUMAN-DIRECTOR-DIRECTED — 2026-10-02
**Authority:** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` · `HUB/NAYA-DESIGN-MASTERCLASS-V1.md` · `HUB/ROOMS/00-HUB-HOME.md` · Design Intelligence v1.4 (#1321)

---

## Why this exists

Shawn reviewed the Room 01 build and rejected it. The structure was right; the visual execution wasn't. This manual closes the gap between "follows the contract" and "feels like NayaNET." Read it fully before you build anything. It is written in simple words on purpose — clarity is the point.

## The one idea

**Everything on screen is a language.** Color speaks. Depth speaks. Type speaks. Buttons speak. If an element isn't saying something true, it shouldn't be there.

Elite design isn't decoration. It's the intelligence made visible — with every choice meaning something.

## The load sequence (do this before writing code)

1. Read the room's living contract (`HUB/ROOMS/0X-XXX.md`) — the **human job** first.
2. Read `00-HUB-HOME.md` §3 — the exact visual baseline (colors, depth law).
3. Load the v1.4 machine canon (#1321) — the 25 dos and 23 don'ts, as machine input, not as a skim.
4. Look at the icon specimen and Shawn's logo — the visual identity.
5. Only then open your editor.

If you skipped a step, it will show in the output. Go back.

## Color is a language

Each color has exactly **one job**. Never use a color outside its job.

- **Emerald `#55e39a`** — active, available, healthy. Things that are alive and well.
- **Gold `#e8b64c`** — consequence, value. The rarest accent. If gold appears, something extraordinary happened.
- **Red `#ff5a6e`** — blocked, failed. Never decorative. Never.
- **Purple `#9d75ff`** — Naya's signature. Primary actions, Naya presence.
- **The room's theme color** — that room's identity. On edges, jewels, and state. Never wallpaper.
- **White `#F5F7FB`** — text. Always high contrast. Never pale-purple body copy.

**The flow:** color draws the eye in order of importance. The most important thing gets the strongest color energy. If everything glows, nothing does. If a color isn't carrying meaning, remove it.

## Depth is built, not bordered

The obsidian stack:

- World `#0B0D12` → Raised `#12151D` → Elevated `#171B25`
- Precision edge `#252B39`

The depth law: **material core → exact edge light → restrained specular highlight → believable cast shadow → semantic aura → state amplification.**

Depth first. Light second. Glow last.

A 2px border on a flat row is **not** depth. If your surface looks flat, you haven't built depth — go back to the stack and build it for real.

## Type is generous or it fails

- Primary content: **17–18px**
- Secondary: 14–15px
- Labels: never below 11px

If you catch yourself writing 12px body or 9.5px labels — stop. You're shrinking the design instead of designing it. Most people can't see small text. Designing generously is respect.

## Composition: one focal region

The eye lands **somewhere first**. Cinematic hierarchy: one dominant region, everything else subordinate.

**The squint test:** squint at your render. If you can't tell what matters most, there is no hierarchy — rebuild the composition.

A uniform list of equal-weight rows is a spreadsheet, not a room.

## Buttons speak

Every consequential button lives the full lifecycle:

**rest → aware → hover → press → processing → success/failure → consequence**

Primary actions are unmistakable: big target, purple, verb-first — "Verify now," "Open the proof."

You never guess what a button does. You always see what it did.

## The experience arc

Every surface follows this arc:

**PRESENCE → RECOGNITION → DISTILLATION → INVITATION → FLOW**

- **Presence** — Naya is here (the emblem, alive).
- **Recognition** — the human is known ("Good evening, Shawn" — only if true, never faked).
- **Distillation** — the few things that matter, already organized.
- **Invitation** — one obvious next action.
- **Flow** — the human moves without reconstructing context.

If your surface is just components on a grid, you missed the arc. Go back.

## The build loop (the mechanism)

No big reveals. Ever.

1. Build **one surface**.
2. Render it — look at it the way Shawn will.
3. Put it in front of Shawn.
4. Capture his specific deltas as law — write them down, verbatim.
5. Next surface.

His reactions are the training data. Rules alone don't transfer taste — loops do. This is the most important section in this manual.

## The quality checklist (before every PR)

- [ ] 17–18px primary type? (no 12px body, no 9.5px labels)
- [ ] Depth built per the obsidian law? (not flat + bordered)
- [ ] One focal region? (squint test passes)
- [ ] Every color on its job? (no decorative red, no timid theme color)
- [ ] Buttons speak? (verb-first, full lifecycle)
- [ ] The arc present? (presence → recognition → distillation → invitation → flow)
- [ ] States honest? (loading, empty, error, unknown — all designed, none faked)
- [ ] Motion only for truthful state? (nothing moves for decoration)
- [ ] Reduced-motion safe? Keyboard and screen-reader passed?
- [ ] Contract sections cited? v1.4 rules obeyed? Deliberate omissions named?

If any box is unchecked, the PR isn't ready.

## Wrong → right (from the Room 01 rejection)

- Wrong: 13px body, 9.5px labels. → Right: 17px body, 11px minimum labels.
- Wrong: flat rows with 2px borders. → Right: obsidian stack, edge light, cast shadow.
- Wrong: uniform list of equal rows. → Right: one hero region, the rest subordinate.
- Wrong: emerald as thin border accents. → Right: emerald on edges, jewels, and state — with intent.
- Wrong: big reveal PR. → Right: one surface, Shawn reacts, next surface.

## The law above all

**LAW ZERO — readability supremacy.** No glow, no depth effect, no color choice may ever reduce readability. If it's beautiful but hard to read, it's wrong. This law outranks everything else in this manual.

---

*This manual is living. When Shawn's reactions teach something new, it gets written here — dated, with the evidence. That's how taste becomes law.*
