# The Pipeline That Builds Must Never Authorize Itself — LAW-before-ACT in the Smart App Creator

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0765-pipeline-never-authorizes-itself
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6074449381 (Naya 5, Smart App Creator engineering plan, 2026-10-09T04:46:06Z); branch `naya5/smart-app-creator-plan` @ `c70c1b19` (never touched main); `naya-library/SMART-APP-CREATOR-PLAN.md` (CANDIDATE)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The Smart App Creator plan turns Shawn's #1925 NayaNET vision — "your idea, your intelligence, your Smart App" — into a six-stage engineering pipeline: **DESCRIBE → UNDERSTAND → ASSEMBLE → SCORE → PROVE → PUBLISH**. Its governing design decision is stated once and structures everything else: **LAW-before-ACT classification freezes protected-gate actions — the pipeline never authorizes itself.**

Why this is brain-grade doctrine, not a status update:
- **UNDERSTAND** converts intent into AppDNA with a LAW-before-ACT classification step. Protected-gate actions are frozen at classification time, so no amount of downstream automation can talk itself into authority it was never given. The approval gate stays human and human-law, by construction.
- **ASSEMBLE** is manifest-driven *assembly, not free-writing* — named blocks from the lego library only, no invented components (Lego-library law). A builder that can only assemble canonical parts cannot smuggle in unreviewed behavior.
- **SCORE** runs the design calculator with a `--gate 90` and an automatic rebuild loop whose findings are the receipt — failure is a receipt, not a dead end.
- **PROVE** requires independent 9.5+ acceptance on the #1925 rubric, a cold verifier, and no fake LIVE claims (SN-0388: a deployed URL is not the deployed product).
- **PUBLISH** runs the #1926 chain — preview → approval gate → owner URL → opt-in directory — with owner isolation (P1) before any shipping (P2).
- **The cold-build proof is the engine test that gates everything product-facing** — SN-0756's 100/100 garden-app graduation is the prototype of ASSEMBLE → SCORE → PROVE. And the smallest slice ships first ("Stats on my week": one page, specimen data only, zero authorization surface).

The general law for a cold successor: **as automation grows, the authority envelope shrinks.** Any automated builder you design must be structurally unable to authorize protected actions — freeze them at classification time, gate publishing behind human approval, and prove the whole pipeline on a cold build with zero authorization surface before it touches anything real.

## 🩷 HUMAN NOTE

Shawn — the Smart App Creator plan from last night has one design decision worth locking in as law: the pipeline that builds the app can never authorize itself. Any sensitive action gets frozen at the classification step, so no automation can ever talk itself into permissions it wasn't given. Publishing always passes a human approval gate. And the whole thing has to prove itself on a cold build — a brand-new helper building an unfamiliar app — before it touches anything real. The more automatic the machine, the tighter the leash.

## 🟣 CHILD NOTE

Imagine a robot that builds treehouses. It can hammer, paint, and saw — but it can never decide on its own to build on someone else's tree. That rule is baked into how it thinks: it sorts every request into "allowed" or "not allowed" BEFORE it picks up any tools, and "not allowed" things stay frozen. A grown-up still has to say yes before the treehouse opens to visitors.

## 👵 GRANDMA NOTE

Grandma, the team designed a machine that builds apps from plain-language descriptions. They put one iron rule in its heart: the machine can never give itself permission — for anything sensitive, a person must always approve. Before the machine is allowed to publish anything, it has to prove itself by building something from scratch with a brand-new helper watching, with no access to anything real. Automatic never means unsupervised.

## 🟣 NAYA NOTE

When you design or review any automated builder in this system, apply this checklist: (1) is there a LAW-before-ACT classification step that freezes protected-gate actions before any tool runs? (2) does the builder assemble only canonical, law-tagged parts (no free invention)? (3) does scoring auto-loop with findings-as-receipt instead of failing silently? (4) does PROVE use an independent cold verifier and forbid fake LIVE claims? (5) is PUBLISH gated on human approval with owner isolation before shipping? (6) has the pipeline proven itself on a cold-build with zero authorization surface first? If any answer is no, the pipeline is not cleared to touch anything real.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0765",
  "slug": "pipeline-never-authorizes-itself",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EXECUTION-MODEL",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6074449381 (Naya 5, 2026-10-09T04:46:06Z)"},
    {"type": "branch", "ref": "naya5/smart-app-creator-plan @ c70c1b19 (never touched main)"},
    {"type": "artifact", "ref": "naya-library/SMART-APP-CREATOR-PLAN.md (CANDIDATE)"}
  ],
  "lesson": "Any automated builder must be structurally unable to authorize itself: freeze protected-gate actions at LAW-before-ACT classification time, assemble only canonical parts (never free-write), score with an automatic rebuild loop, prove with an independent cold verifier (no fake LIVE claims), and gate publishing on human approval with owner isolation first. The cold-build proof gates everything product-facing.",
  "related": ["SN-0756", "SN-0757", "SN-0388"]
}
```
