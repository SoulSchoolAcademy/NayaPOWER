# MACHINE-INTELLIGENCE — AI decision framing

## Reach for this when

You are a cold agent or worker and need the whole project's intelligence in one parseable file — the laws, the gaps, the ordered work queue, the verification protocol, the current state — before you decide what to do. The machine tongue IS the owning JSON (`MACHINE-INTELLIGENCE.json`, v2.0); this tongue is how you use it.

## How to use the JSON (operational reading)

1. **Start with `mission.done_criteria`.** Four tests: DONE-MACHINE (the falsifiable-lesson end-to-end test with SHA-256 links and blind different-seat verification), DONE-HUMAN (Shawn's Smart Link test — header says ACTIVE), DONE-NO-DEAD (every gate has a producer), DONE-ONE-TRUTH (single intake, DB+repo agree). These are the project's actual bar — a claim of progress is measured against these four, not against prose.
2. **Check `mission.out_of_scope`.** Production NayaNET deployment, Hub interface, new features, constitutional/EVOLVE changes are out. If your task lands there, you're out of this document's bounds.
3. **Consult the law table (`laws`, 40 entries: 26 standing + 14 operational).** Every law carries `trigger` and `action`. The load-bearing four: L01 THE_MANTRA (ask what the most intelligent thing is, rank, execute — always), L02 JUDGMENT_RULE (stop on a wrong instruction, explain with evidence, propose; hard stops refused unconditionally), L03 LAW_IS_CODE (ratified law is structure; amend through Shawn, never breach), L04 MATH_DECIDES (gate first: PROHIBITED→refuse, NEEDS_AUTHORITY→Shawn, NEEDS_EVIDENCE→investigate, ADMISSIBLE→score 7 dimensions; escalate only on NEEDS_AUTHORITY). Law statuses are carried (`RATIFIED_SUPREME`, `RATIFIED_PRIME_1`, `RATIFIED`, …) — statuses are claims about ratification, not self-evident truth.
4. **Work the queue (`work_orders`, 14).** Ordered; each work order has accept criteria. Do them in order; the queue is the plan, not a suggestion.
5. **Respect the gaps (`gaps`: 9 open; `gaps_fixed_elsewhere`: 5).** These are machine-verified gaps (grep-verified, not asserted). Build against them before building new things.
6. **Run the activation test (`activation_test`):** SC-1 through SC-8, with machine steps and preconditions (work orders complete per accept criteria, G8 RPC migration applied, arming gate passed). The protocol is repeatable and the protocol hash is recorded.
7. **Treat `current_state` as a snapshot, not truth.** `as_of: 2026-10-09T20:15:00Z`, `main_tip: 1d73652231ac6127806640af5a31eb516c60738d`. Done/in-flight/blocked/known_reds describe that moment. Re-verify any "now" claim against live bytes before deciding on it.

## The dos

- Parse the JSON; decide from its fields. A decision from the law table beats a decision from memory.
- Distillation rule is the house standard: keep everything needed, remove everything not needed, every rule actionable, every claim traceable. Apply it to your own outputs.
- When you claim progress, pin it to one of the four done criteria — name which test your work satisfies and the evidence.
- The learning chain (`learning_chain`, 9 entries) and connections (`connections`, 7) are the compounding path — follow it rather than inventing one.

## The don'ts (hard stops)

- Never treat `current_state` as live truth — it expires the moment main moves.
- Never act on a "known_red" without reading its entry — the reds carry their mechanisms.
- Never build outside `out_of_scope` using this document as authority — it doesn't grant that.
- Never duplicate the JSON's machine copy — this document's machine tongue IS the owning file. One machine tongue, not two.

## The three-tongue pairing (marked, per batch convention)

- Machine tongue: `MACHINE-INTELLIGENCE.json` (v2.0) — the canonical machine copy.
- Human tongue: `MACHINE-INTELLIGENCE.human.md` — plain words.
- AI tongue: this file — decision framing.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc / machine tongue: `BRAIN/00-ARCHITECTURE/MACHINE-INTELLIGENCE.json`
- Paired tongues: `MACHINE-INTELLIGENCE.human.md`
