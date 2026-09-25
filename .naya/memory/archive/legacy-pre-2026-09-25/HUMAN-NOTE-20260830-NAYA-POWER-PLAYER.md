# HUMAN / SEAN NOTE — Naya Power Player

**Date:** 2026-08-30
**Status:** CAPTURED — PROJECT CREATED / DESIGN LOCKED
**Event ID:** `SN-20260830-NAYA-POWER-PLAYER`
**Authority:** Shawn's human architectural direction, synthesized into a project design lock

## What happened

Shawn and Naya converged on the next customer-facing product: **Naya Power Player**.

The experience should not present as a conventional sales page. It should present as a premium, mobile-optimized web application / intelligence environment that lets people experience NayaPOWER immediately.

## Core decision

The Player is the customer-facing experiential layer of NayaPOWER.

The sales function is embedded inside the experience rather than separated from it.

The desired journey is:

`SEE NAYA → LISTEN → ASK → EXPERIENCE → UNDERSTAND → TAKE THE FIVE-DAY CHALLENGE → ACTIVATE`

## Core experience

- Persistent high-quality top navigation so the visitor feels inside a system.
- Shawn + Naya as the hosts of the opening Powercast experience.
- Living Sun as the central visual/voice interface.
- Living Sun should visibly come alive when Naya listens, thinks, and speaks.
- A central energy sphere should move/vibrate while Naya speaks, surrounded by animated rings/energy.
- Multiple Powercast thumbnails should be selectable and played inside the Player.
- Ask Naya should be conversational and voice-first.
- The human can speak/dictate when supported; Naya answers through the Player by voice by default.
- Text should be secondary and opened intentionally through a See Text / More interaction so the primary screen remains clean and alive.
- The Five-Day Challenge should be directly accessible and playable inside the same environment.
- Secondary sections can explain Smart Notes, CIS, PSI, CCT, Intelligent Blocks, MAXIS, the Superbrain, continuity, and related concepts.

## Architectural decision

Build the experience as **layered Groove Embed blocks** rather than forcing everything into one enormous embed.

Each block is part of one connected Player and should share the same visual and interaction language.

The build loop is:

`BUILD → EMBED → VIEW → WHY IS THIS NOT A 10? → REPAIR → VERIFY → NEXT BLOCK`

## References

The Pro Max Player provides the reference pattern for application-shell quality, persistent navigation, player-first interaction, progress/journey presentation, premium cards, and immersive media.

The MAXIS E01–E09 work provides implementation lessons for substantial self-contained embeds, responsive behavior, cinematic presentation, interaction state, and Living Sun/orb treatment.

NayaPOWER should evolve these lessons from a **media player** into an **intelligence player**.

## Human intent

The first experience should answer the visitor's questions without forcing a document dump:

- What is NayaPOWER?
- What does Naya do?
- Can I talk to her?
- Can I listen?
- Can she teach me?
- Can I experience it?
- What happens if I take the Five-Day Challenge?
- How do I activate it?

## Next action

Build **E01 — Naya Power Player Home / Intelligence Shell** as the foundation of the Player.
