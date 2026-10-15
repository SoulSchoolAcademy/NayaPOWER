# MACHINE-INTELLIGENCE — in plain words

*For Shawn — the whole project's intelligence in one file: what to build, in what order, how to verify it. Machine-readable so a cold agent reading only this file knows the job.*

This JSON is the project's memory compressed to machine rules: every law, every gap, every work order, the plan, the mission, the current state, the glossary — distilled under one rule: keep everything needed, remove everything not needed, every rule actionable, every claim traceable. Version 2.0 reconciled two lanes' pilot files (PR #2052 and #2054) into one canonical document; nothing from either was dropped.

What it contains: **40 laws** (26 standing + 14 operational) — the mantra, the judgment rule, the law-is-code, the math decides, and the rest, each with its trigger and action. **The mission** — assemble the complete learning system so a lesson Shawn teaches once demonstrably changes Naya's future behavior without being reminded — with four done-criteria, each a test, not a slogan: the machine test (a novel falsifiable lesson flows capture → persist → index → verify → promote, a cold Naya retrieves it via the ranked path and applies it to a pre-registered held-out task, a blind different-seat verifier confirms the behavior change came from the lesson, every link carries SHA-256 hashes); the human test (Shawn says "smart note this" and gets a Smart Link; days later she does the thing without being reminded, names the lesson, shows the receipt chain, and the note's header says ACTIVE); the no-dead test (every gate has a producer for the state it demands — no "looks alive, isn't" components); the one-truth test (single canonical capture intake; DB and repo agree; CI enforces it). **Nine gaps** (plus five marked fixed elsewhere). **Fourteen work orders** — the ordered build queue. **The activation test** — eight success criteria (SC-1 through SC-8): instant capture within 5 minutes, promotion works, retrieval works cold, decisions include the lesson, the lesson changes decisions, execution feeds back, proof closes the loop, succession works. **Current state** as of the snapshot: what was done (blueprint v1, consensus plan, merged PRs, the project-intelligence pilot), what's in flight, what's blocked, the known reds.

What the file IS: the machine's copy of the mission, the law table, the gap register, the work queue, and the verification protocol — one file, parseable, traceable. What it is NOT: a replacement for the blueprint's reasoning — it carries the verdicts, the blueprint carries the why.

**One honest warning:** this is a machine snapshot — `current_state.as_of` is 2026-10-09T20:15Z at main tip `1d73652231ac6127806640af5a31eb516c60738d`. Done/in-flight/blocked/reds are dated claims, not live facts; battery numbers (1896 passed, 11 skipped, 0 failed; 6/6 adversarial) describe that battery run. The mission, laws, gaps, work orders, and success criteria are the durable part — the "now" lines are not.

**Machine tongue note:** this document's machine tongue IS the owning file — `MACHINE-INTELLIGENCE.json` itself (v2.0, JSON, schema-carrying). No second machine copy exists; the human and AI tongues below are translations of it.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc / machine tongue: `BRAIN/00-ARCHITECTURE/MACHINE-INTELLIGENCE.json`
- Paired tongues: `MACHINE-INTELLIGENCE.ai.md` · (machine tongue = the owning JSON, marked above)
