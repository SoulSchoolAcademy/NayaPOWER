# MAXESS V21 MASTER CHANGE LEDGER

Status: ACTIVE
Repository: SoulSchoolAcademy/MaxRESULTS
Branch: maxess-results-v21-working

## Operating rule

Every requested material change must remain visible here until evidence supports COMPLETE or FROZEN.

Statuses:
DRAFT | IN PROGRESS | BLOCKED | COMPLETE | FROZEN

| ID | Requirement | Section | Target | Acceptance | Status | Evidence |
|---|---|---|---|---|---|---|
| V01 | Clean canonical builder source | Foundation | No unresolved merge markers | No `<<<<<<<`, `=======`, `>>>>>>>`; Node syntax PASS | IN PROGRESS | Deterministic repair tool now idempotent; latest source/build cycle still requires full clean-state verification |
| V02 | Naya arrival | Naya | Personal, warm, one primary Listen | Correct copy, one Listen, accessible | COMPLETE | Existing source + QA |
| V03 | Score Orb | Hero | Dominant signature visual | Real score centered, responsive, reduced motion | COMPLETE | Existing source + QA |
| V04 | Score meaning | Meaning | Explain the score in plain language | Stage + interpretation + use guidance | IN PROGRESS | Contract |
| V05 | AI fingerprint | Fingerprint | Five-axis visual capability map | Real data + textual equivalent | IN PROGRESS | Contract |
| V06 | Five dimensions | Dimensions | Five interactive capability orbs | Exactly five, real data, detail interaction | IN PROGRESS | Contract + source |
| V07 | Pattern | Pattern | Explain relationships | Relational interpretation, not score repetition | IN PROGRESS | Contract |
| V08 | Strength | Strength | Recognition + compounding | Dynamic strongest capability + action | IN PROGRESS | Contract + source |
| V09 | Lever | Lever | Focus without judgment | Dynamic opportunity + improvement loop | IN PROGRESS | Contract + source |
| V10 | Next Move | Action | Three personalized actions | Connected to strength/lever/result | IN PROGRESS | Contract + source |
| V11 | 18 Naya Masters | Pathways | Personalized doors, not generic library | All validated pathways retained + relevance | IN PROGRESS | Contract |
| V12 | Naya interpretation | Naya | Guide throughout report | Interprets meaning/pattern/strength/lever/next move | IN PROGRESS | Contract |
| V13 | Button system | Design | HMC AAA controls | Correct family, states, hierarchy, accessibility | IN PROGRESS | HMC button system + HMC reference pack |
| V14 | Icon/micro-icon system | Design | Proprietary coherent icon rhythm | Semantic family + optical consistency | IN PROGRESS | HMC button system + HMC reference pack |
| V15 | Visual rhythm | Design | Premium chapter transitions | Each section earns visual breakpoint | IN PROGRESS | Design contract |
| V16 | Lower media | Media | Video and walkthrough reliably render | No disappearing lower content | IN PROGRESS | Source + runtime QA |
| V17 | Playground | Practice | Understand → Decide → Practice | Existing useful functionality preserved + styled | IN PROGRESS | Contract |
| V18 | Responsive | System | Widescreen/desktop/tablet/mobile | No overflow, hierarchy preserved | IN PROGRESS | Contract |
| V19 | Accessibility | System | Keyboard/focus/contrast/reduced motion/touch | All applicable criteria pass | IN PROGRESS | Contract |
| V20 | Performance | System | Efficient animations and initialization | No loops, duplicate listeners, runaway observers | IN PROGRESS | Contract |
| V21 | Print/PDF | Release | Professional intentional document | Actual PDF generated and inspected | IN PROGRESS | Contract |
| V22 | Real result handoff | Data | Assessment → Result Contract → MAXESS_RESULT | Real completed assessment verified | IN PROGRESS | Contract |
| V23 | Groove deployment | Release | Public page shows intended artifact | Live URL verified | IN PROGRESS | Deployment contract |
| V24 | Smart Notes | Memory | Durable execution learning | Important decisions/failures recorded | COMPLETE | MAXESS-SMART-NOTES.md updated |
| V25 | Reference implementation proof | Masterclass | MAXESS demonstrates the OS works | Contract + ledger + tests + live proof | IN PROGRESS | North Star |
| V26 | HMC reference pack | Brand / Memory | HMC knowledge is connected to MAXESS memory | Source pack indexed; reusable principles stored without unsupported paraphrase | COMPLETE | MAXESS-HMC-REFERENCE-PACK.md |
| V27 | Product-language / Lead Mode | Operating System | Naya leads from vision to release | Persistent lead behavior, next action, suggested prompt, best-interest rules | COMPLETE | AI Product Creation OS + Naya Lead Mode |
| V28 | Experience QA ownership | QA / Operating System | Validator tests the layer it actually owns | Static renderer-order QA must match the current root renderer; broader chapter completeness stays with Master Contract/runtime QA | COMPLETE | qa_v21_experience_v2.py updated; lesson recorded in Smart Notes |
| V29 | AAA section design specification | Product Design | Explicit Definition of 10 for every section | Each section has current problem, AAA target, purpose, content, visual, interaction, evidence | COMPLETE | docs/MAXESS-AAA-SECTION-DESIGN-SPEC.md |
| V30 | Weighted execution priority | Execution | Work highest-impact unfinished product first | Dynamic weighted priority matrix and anti-loop rules | COMPLETE | docs/MAXESS-PRIORITY-MATRIX.md |
| V31 | Section execution workflow | Execution | Turn design contract into measurable product deltas | READ → SCORE → PRIORITIZE → MUTATE → PROVE → BUILD → VERIFY → RESCORE → FREEZE → CONTINUE | COMPLETE | docs/MAXESS-SECTION-EXECUTION-WORKFLOW.md |
| V32 | Batch 1 product mutation | Product | Materially improve Sections 01–03 | Builder SHA changes; all 3 section implementations change; preserve result/media; QA follows mutation | IN PROGRESS | Batch 1 checkpoint commit exists; full section freeze evidence not yet complete |
| V33 | Master design directive | Product Design | Exact visual/psychological/interaction definition for all sections | Exact copy, colors, geometry, button grammar, icon grammar, visual choreography, transitions, responsive, accessibility, data, PDF, and section acceptance | COMPLETE | docs/MAXESS-MASTER-DESIGN-DIRECTIVE.md commit 420367f |
| V34 | Optional identity personalization gate | Onboarding | Increase personalization without gating value | Google/Facebook/email options + visible Skip + graceful anonymous experience | DRAFT | Defined in MAXESS-MASTER-DESIGN-DIRECTIVE.md; implementation decision remains pending |

## Freeze rule

A complete item becomes FROZEN only after the relevant human and technical evidence exists.

## Anti-regression rule

No new change may silently reopen or destroy a frozen item.