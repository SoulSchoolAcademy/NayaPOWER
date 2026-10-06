# REMINDERS LINEAGE V1 — AI Operating Specification

**Status:** PROPOSED (truth ceiling: CANDIDATE). Awaiting Shawn Vibert's ratification.
**Scope:** all seats, all lock-in material. This is a citation map, not a mandate — it creates no new obligations.
**Companion:** `0007-REMINDERS-LINEAGE-V1.human.md`, `0007-reminders-lineage-v1.machine.json`.

## Lineage entries (reminder → current law → covering artifact)

Each entry carries a `lineage_status`:
- `COVERED` — the reminder's directive already lives as law in the cited artifact; this file only cites it.
- `ANCESTOR_CLAIMED` — the directive lives in operating doctrine (AGENTS.md / director record) but has no standalone repo-law file; cited honestly, not upgraded.
- `NEWLY_FORGED` — the directive was genuinely missing from the repo; this PR forges it (cited where).

1. **#31** "Score before I show. Minimum 90 or rework." → 9.0 auto-approval bar + score-grounding rule.
   Covering: `BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-V1.md` ("9.0 is the birth threshold — nothing under 9.0 ships"; RATIFIED 2026-10-05). `COVERED`. Extended by this PR's Playbook rubric (90/100 = 9.0).
2. **#35** "Screenshots = proof. Links = belief." → visual-proof standard ("never say it's done — send the link that shows it done").
   Covering: `HUB/PROJECT-INTELLIGENCE.md` + `HUB/PROJECT-INTELLIGENCE.AI.md` ("self-score with evidence links (screenshots, recordings, test output)"). `COVERED`.
3. **#21** "Always know the next 3 steps." → execution-communication law (every reply ends with the next action).
   Covering: `BRAIN/01-GOVERNANCE/0005-CAPTAIN-OPERATING-PROTOCOL-V1.ai.md` REPORT_BACK ("exactly one next action · the refreshed next ten"). `COVERED`.
4. **#22** "Every 15 minutes should create visible progress." → nonstop loop.
   Covering: `BRAIN/01-GOVERNANCE/0004-NONSTOP-LOOP-V1.*` (RATIFIED). `COVERED`.
5. **#32** "If it can be simplified — it should be." → smallest effective change.
   Covering: repo `AGENTS.md` (Engineering) + `BRAIN/01-GOVERNANCE/0005-CAPTAIN-OPERATING-PROTOCOL-V1.ai.md`. `COVERED`.
6. **#57** "Every glitch is a gift. Fix it and evolve." → The Loop (miss → analyze → learn → grow → improve → re-score).
   Covering: `BRAIN/01-GOVERNANCE/0004-NONSTOP-LOOP-V1.*` + The Loop doctrine. `COVERED`.
7. **#26** "Automate first, repeat never." → self-building mandate.
   Covering: `0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md`. `COVERED`.
8. **#34** "Default to launch. Default to link. Default to live." (bounded) → bias-to-shipped applies BELOW the gates.
   Covering: `BRAIN/01-GOVERNANCE/0004-nonstop-loop-v1.machine.json` `human_gates_never_crossed`. `COVERED` (the bound, not the slogan).
9. **#25** "Fix forward. Don't freeze." → repair culture.
   Covering: `BRAIN/01-GOVERNANCE/0004-nonstop-loop-v1.machine.json` `correction_duty` ("repair the mechanism, not just the instance"). `COVERED`.
10. **#40** "Can this run without me? Then build it that way." → minimal project management.
    Covering: repo `AGENTS.md` Captain Mode ("do not make Shawn project-manage routine work"). `ANCESTOR_CLAIMED` — doctrine, no standalone repo-law file.
11. **#39** "The whole system should feel like a conversation, not a website." → post-website vision.
    Covering: Design North Star (LAW ZERO) — "not a dashboard, a database, a chatbot, or a collection of features." `COVERED`.
12. **#9** "Every pixel is a portal. Treat it like one." → visual-bliss law + 10/10 delivery bar.
    Covering: director standing doctrine; machine-law encoding in open PR #1296 (not merged). `ANCESTOR_CLAIMED` — cited as doctrine, not as merged law.
13. **#33** "Mock it up if it's not built yet." (bounded) → mockup bound.
    Forged: `HUB/DESIGN-RUBRICS/ELITE-INTERFACE-PLAYBOOK-V1.ai.md` + `elite-interface-playbook-v1.machine.json` (`adaptations.mockup_bound`). `NEWLY_FORGED`.
14. **#66/#76** "Don't promote. Demonstrate." / "The system markets itself when the results are real." → demonstrate bound.
    Forged: `HUB/DESIGN-RUBRICS/DIVINE-DESIGN-LAWS-V1.ai.md` (B-DEMONSTRATE) + `divine-design-laws-v1.machine.json`. `NEWLY_FORGED`.

## Lock-in posture (the lineage finding)

When lock-in material presents current team law, it MUST present it as the continuation of Shawn's standard, citing this file — never as new process. This increases adoption and kills "new process" resistance. Evidence for the claim: entries 1–14 above.

## Exclusions (deliberate)

- The "I am" affirmations (#1–20, #41–60): Shawn's personal operating fuel, not team process. Captured in the distillation as context; MUST NOT be imposed as procedure.
- SmartNET-era naming throughout the Reminders ("make SmartNET go global"): dated packaging; directives preserved, packaging not liturgized.
- The marketing directives (#61–80 as posture): partially encoded via B-DEMONSTRATE; the rest is launch posture, not law.

## Enforcement

- Today: none — this is a citation map. No seat is obligated to act on it beyond citing it in lock-in material.
- **Follow-up (named, not faked):** a lock-in checklist item could verify that new-seat onboarding references this lineage file. Out of scope for this PR.
