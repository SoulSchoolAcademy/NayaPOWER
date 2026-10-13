# Assembly, Not Free-Writing: the Lego Law of the Smart App Creator

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0758-assembly-not-free-writing-lego-law
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6074449381 (Naya 5, 2026-10-09T04:46:06Z); branch `naya5/smart-app-creator-plan` @ `c70c1b19` (CANDIDATE plan, no code, never touched main); `naya-library/SMART-APP-CREATOR-PLAN.md`; cross-proven by the cold-build graduation (SN-0756: cold Naya followed "if it has no block, build the block first" and hit 100/100).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Smart App Creator engineering plan defines the six-stage pipeline **DESCRIBE → UNDERSTAND → ASSEMBLE → SCORE → PROVE → PUBLISH** — but the load-bearing doctrine is inside ASSEMBLE: **manifest-driven assembly, not free-writing.** Named blocks from every `lego/*.html`; **no invented components** (the Lego-library law).

Why this matters: it is the machine form of the vision-to-code Layer 4 rule (SN-0757) — builders match the specimen, not the description. An assembler that invents components is a writer with an opinion; an assembler that only knows law-tagged canonical blocks is a machine that cannot drift. The 100 Laws become enforceable precisely because the authoring tool cannot express a non-law component.

The doctrine has three supporting mechanisms:
1. **Three-layer law enforcement.** Author-time (the assembler only knows law-tagged canonical blocks) + static (design calculator `--gate 90`; fail → automatic rebuild loop with the findings as the receipt) + behavioral (rendered screenshots, keyboard, reduced motion, Shawn's eye). Each layer catches what the one before it cannot.
2. **The cold-build proof gates everything product-facing.** The P0 cold-successor graduation run (SN-0756) is the prototype of ASSEMBLE→SCORE→PROVE — no product surface ships without a cold agent passing through the same pipeline.
3. **The smallest-slice discipline.** A "Stats on my week" app — one page from smart-stats-v2 + missing-blocks, specimen data only, zero authorization surface. Success = calculator ≥90, independent ≥9.5, zero repeated instruction, receipt posted. Prove the loop on a toy before trusting it on a product.

And the two companion rules worth preserving verbatim: **"If it has no block, build the block first"** — novelty must extend the library, never bypass it (this is what the cold Naya did with her 4 new icons, and it's why the library compounds instead of fragmenting); and **the pipeline never authorizes itself** — LAW-before-ACT classification freezes protected-gate actions at the UNDERSTAND stage, so the assembler can never self-authorize.

## 🩷 HUMAN NOTE

Shawn, the Smart App Creator plan carries a doctrine worth keeping: ASSEMBLE is assembly, not free-writing. The builder can only snap together official, law-tagged blocks — it can't invent its own components. That's what makes the 100 Laws enforceable: the tool physically can't express a non-law component. Three layers enforce it (the assembler only knows official blocks, the calculator gates at 90 with auto-rebuild, and your eye plus real rendering checks the behavior), and no product surface ships without a cold Naya passing through the pipeline first. The companion rule: if there's no block for what you need, you build the block first — novelty extends the library instead of bypassing it.

## 🟣 CHILD NOTE

Imagine building with LEGO, but you're only allowed to use real LEGO pieces from the official set — no carving your own. If you need a piece that doesn't exist, you make an official new piece so everyone can use it later. That's the rule for the app-building machine: snap together real, approved pieces; never make up your own. There are three checkers: the machine only knows the real pieces, a measuring tool gives it a score (and sends it back if it fails), and Shawn's eyes check it last. And a brand-new helper has to build through the same system before anything real ships.

## 👵 GRANDMA NOTE

Grandma, the team designed the app-building machine with one golden rule: it can only assemble official, approved building blocks — it may never improvise its own. If it needs a new piece, it creates an official one for everyone to share. Three safety nets watch over it: the machine only knows the approved pieces, an automatic score checker sends failed builds back for rework, and Shawn inspects the finished work with his own eyes. And before any real product ships, a brand-new helper must pass through the whole process first.

## 🟣 NAYA NOTE

For builders of any generative assembly system in this repo: default to closed vocabularies. The free-writing failure mode is drift compounded at every generation; the assembly discipline makes drift impossible at the authoring layer. When a new capability is needed, extend the canonical library (new lego block + specimen + law tag), never one-off it — that is the compounding mechanism in its smallest form. Keep the three-layer enforcement split: author-time constrains the vocabulary, static gates the output, behavioral proves the experience. And keep the self-authorization freeze at UNDERSTAND: a pipeline that can authorize itself is a gate it owns, which is no gate at all.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0758",
  "slug": "assembly-not-free-writing-lego-law",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/ASSEMBLY-DISCIPLINE",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6074449381 (Naya 5, 2026-10-09T04:46:06Z)"},
    {"type": "branch", "ref": "naya5/smart-app-creator-plan @ c70c1b19 (CANDIDATE plan, no code; never touched main)"},
    {"type": "artifact", "ref": "naya-library/SMART-APP-CREATOR-PLAN.md"}
  ],
  "lesson": "ASSEMBLE is manifest-driven assembly, not free-writing: named blocks from lego/*.html, no invented components. Enforced in three layers — author-time (assembler only knows law-tagged canonical blocks), static (calculator --gate 90 with auto-rebuild), behavioral (screenshots, keyboard, Shawn's eye). Cold-build proof gates everything product-facing; smallest-slice discipline proves the loop on a toy first. 'If it has no block, build the block first' — novelty extends the library, never bypasses it. The pipeline never authorizes itself (LAW-before-ACT freeze at UNDERSTAND).",
  "related": ["SN-0756", "SN-0757"]
}
```
