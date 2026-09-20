# 🔱 Naya Power Player

**Status:** PROJECT CREATED — DESIGN LOCKED / BUILD NEXT
**Date:** 2026-08-30
**Project:** Naya Power Player
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## North Star

Build the NayaPOWER customer experience as an **app-like intelligence environment**, not a conventional sales webpage.

The Player should let a visitor immediately:

- meet Shawn + Naya;
- experience the Living Sun;
- listen to Powercasts;
- ask Naya questions about NayaPOWER;
- hear Naya answer by voice by default;
- optionally reveal the answer as text;
- dictate a question when supported;
- enter and progress through the Five-Day Challenge;
- explore the NayaPOWER intelligence ecosystem;
- understand the value by experiencing it;
- move naturally toward activation.

## Core product principle

> **Do not merely tell visitors what NayaPOWER does. Let them experience NayaPOWER.**

The sales function is embedded inside the product experience:

`SEE NAYA → LISTEN → ASK → EXPERIENCE → UNDERSTAND → CHALLENGE → ACTIVATE`

## Experience architecture

### 1. App shell

The page presents as a high-end mobile-optimized web application:

- persistent top navigation;
- premium dark/purple visual language;
- app-like controls and cards;
- responsive/mobile-first behavior;
- `+ Explore` or equivalent ecosystem control;
- connected sections that feel like one application.

### 2. Living Sun

The Living Sun is the visual centerpiece and the voice/interaction surface for Naya.

Intended states include:

`IDLE → LISTENING → THINKING → SPEAKING → TEACHING → POWERCAST`

Visual behavior should include:

- luminous outer rings;
- changing energy/color states;
- an animated central energy sphere;
- a visibly moving/vibrating core while Naya speaks;
- synchronized speaking state when technically supported.

The Living Sun must be treated as a functional interaction surface, not decorative artwork.

### 3. Shawn + Naya Powercast

The opening experience should present Shawn + Naya as the hosts of the NayaPOWER story.

Powercasts should be represented by premium thumbnails/cards. Selecting a Powercast loads it into the Player rather than navigating away from the environment.

The system should be designed so additional Powercasts can be added later without redesigning the Player shell.

### 4. Ask Naya

Ask Naya is the interactive intelligence layer.

Default interaction:

`HUMAN SPEAKS/TYPES → NAYA PROCESSES → LIVING SUN ACTIVATES → NAYA SPEAKS BACK`

Voice is the default response presentation because the Player should feel like a living conversation rather than a text-heavy chatbot page.

Text remains available through an explicit **See Text / More** affordance. Text should not dominate the primary experience.

When implemented, dictated questions should use the microphone/listening state and then return the response through the Living Sun/player.

Naya's answers must be grounded in actual available NayaPOWER knowledge. The UI must not imply live Superbrain grounding until that connection is implemented and verified.

### 5. Five-Day Challenge

The Player should make the Five-Day Challenge immediately discoverable and playable inside the same environment.

Primary journey:

`DAY 1 → DAY 2 → DAY 3 → DAY 4 → DAY 5`

The challenge is a primary conversion mechanism because the product is intended to be **experienced**, not merely explained.

### 6. Intelligence ecosystem

Secondary exploration should explain the major NayaPOWER concepts after the visitor has experienced the core interaction.

Candidate ecosystem modules include:

- Smart Notes;
- Daily Intelligence;
- CIS / Compounding Intelligence System;
- PSI / Primary Intelligence System;
- Collective Chain Technology;
- Intelligent Blocks;
- MAXIS;
- Naya Superbrain;
- continuity / Naya-to-Naya learning.

Exact taxonomy remains subject to canonical repository architecture.

## Groove Embed architecture

This project is intentionally designed as **layered Groove Embed blocks**.

We do not need to force the entire experience into one giant embed.

Each block should:

1. perform one coherent application function;
2. preserve the shared NayaPOWER visual language;
3. communicate with the surrounding Player where required;
4. remain independently editable/testable in Groove;
5. stack vertically into one seamless application experience;
6. avoid visible seams between embeds.

The prior E01–E09 MAXIS work is a reference for modular section construction. The Pro Max Player is a reference for application-shell quality and player interaction.

## Reference learning

### Pro Max Player

Use its design intelligence as inspiration for:

- persistent application navigation;
- player-first experience;
- premium cards;
- progress/journey presentation;
- ecosystem navigation;
- immersive media controls;
- visual hierarchy;
- app-like rather than webpage-like presentation.

Do **not** copy it mechanically. NayaPOWER should evolve the pattern from **media player → intelligence player**.

### MAXIS / E01–E09

Use the strongest implementation lessons from the E01–E09 work for:

- substantial self-contained embeds;
- responsive interaction;
- Living Sun/orb behavior;
- accessibility and interaction state;
- cinematic presentation;
- layered section construction;
- premium visual treatment.

## Build sequence

Start with **E01 — Naya Power Player Home / Intelligence Shell**.

E01 should establish:

- application shell;
- top navigation;
- responsive layout;
- Shawn + Naya identity;
- Living Sun centerpiece;
- initial Powercast presentation;
- Ask Naya entry point;
- Five-Day Challenge entry point;
- premium NayaPOWER visual language.

Then add subsequent blocks one at a time and evaluate each in the actual Groove environment.

The working loop is:

`BUILD → EMBED → VIEW → WHY IS THIS NOT A 10? → REPAIR → VERIFY → NEXT BLOCK`

## Quality bar

Every block must be judged as a production-quality customer experience, not merely as code that renders.

The final Player must feel:

**alive · premium · intelligent · simple · immersive · fast · trustworthy · app-like**

## Protected truths

- The Player is a customer-facing experience project; it does not replace the canonical NayaPOWER Superbrain.
- Groove is the presentation/execution surface for these embeds, not a new intelligence authority.
- GitHub remains the canonical source for project intelligence and architecture decisions.
- No unsupported capability may be represented as implemented or verified.
- Voice-first interaction is a UX design decision; actual voice generation/grounding remains subject to implementation and verification.
- The Living Sun is an interaction metaphor until its runtime behavior is actually implemented and verified.

## Next action

Build the first Groove block:

**E01 — Naya Power Player Home / Intelligence Shell.**

The first block should be treated as the foundation of the entire Player, not as a disposable hero section.
