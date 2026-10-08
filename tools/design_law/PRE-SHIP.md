# PRE-SHIP — Design Law Checklist (30 seconds)

Run this before shipping any visual surface. The contract is **CANDIDATE**
pending Shawn's ratification — it binds as written until he rules.

## 1. Run the checker (10 seconds)

```bash
python3 tools/design_law/check_design.py <your-file.html>
```

- **Exit 0** → the machine law passes. Ship.
- **Exit 1** → fix every `[FAIL]` line. `[WARN]` lines are advisory, not blocking.
- Never weaken the checker or the contract to make a red surface pass.

## 2. Check the conflict register (10 seconds)

If your surface touches one of the §11 conflicts, follow the **contractor
recommendation** — never silently pick the other side:

| Conflict | Until Shawn rules |
|---|---|
| **X-1** button rest edge | Briefing governs: **white 1.5px+ edge at rest**; purple ignites on hover |
| **X-2** ambient loop timing | Union band **4s–78s** accepted for ambient infinite loops |
| **X-3** shipped page vs candidate Code | Briefing + shipped ground truths (index-2 tokens, start.html button) govern |

Conflicts live verbatim in `contract/NAYA-DESIGN-CONTRACT-V1.md` §11.

## 3. Human eyes on what the machine can't see (10 seconds)

The checker sees tokens, accents, buttons, type, motion wiring. It does **not**
see: copy warmth, rendered feel (glow, rhythm, lift), whether motion feels calm
or frantic, accessibility in real context, whether it *feels like Naya*.
Look at it rendered. If it feels wrong, it is wrong — fix it before shipping.

## 4. Know your status

- **New/changed surface** → must pass the checker. CI (`design-law.yml`) fails
  the PR on violations in touched files.
- **Pre-existing drift** (D1–D9, §9 drift register) → documented, grandfathered,
  repaired after ratification. Don't re-break it; don't claim you fixed it
  unless the checker agrees.

*The machine enforces the letter. You enforce the spirit.*
