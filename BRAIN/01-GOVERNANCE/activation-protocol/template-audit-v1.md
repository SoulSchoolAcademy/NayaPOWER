# Template Audit V1 — Path of Least Resistance

**Built:** 2026-10-09 by Naya 4, Layer 5 of the Activation Protocol (Shawn's authorization, AI Waste Thesis ~18:17 PDT).
**Principle:** following the law should be EASIER than breaking it. If a seat must invent the law's shape from scratch — calculator fields, ritual fields, evidence fields — the environment is taxing compliance and subsidizing waste. Fix the environment, not the seat.
**Verdict scale:** LAW-DEFAULT (following the template = following the law, nothing to fix) · LAW-HOSTILE (the template, or its absence, makes the law harder than breaking it — fixed below).

**Templates audited:** 6. Verdicts: 1 LAW-DEFAULT, 4 LAW-HOSTILE, 1 mixed.

---

## T1 — Dispatch brief template → MIXED (LAW-DEFAULT on activation + verification; LAW-HOSTILE on calculator + quality gate)

**Template:** `workspace/goals/bring-naya-to-life/hidden_files/learn/brief-template.md` (Subagent Brief Template v1, LEARN-managed — hand-edits between markers are overwritten by learn-ingestion).

**What's already good (saying so, not rebuilding):**
- §0 ACTIVATION is LAW-DEFAULT: ritual receipt fields (session id, live main SHA, component SHAs, freshness, cite-the-receipt) are baked in as numbered steps. A seat that follows the template activates.
- §5 Verification contract and §3 hard prohibitions are LAW-DEFAULT: the law's teeth are pre-loaded as fields/sections the seat reads at boot.
- §8 handoff's 9-part shape is LAW-DEFAULT.

**The gaps (where breaking the law is easier than following it):**
1. **Calculator fields don't exist.** §9 carries the "compressed decision standard" as prose in a checklist paragraph ("objective, current reality, available actions, value of each…"). A seat must invent the format. OL-1.4 (Decision Calculator — Shawn: objective, top 3 choices, pros/cons of each, percentages, winner) is law but has no fill-in fields.
2. **Quality gate is empty.** §7 is two LEARN markers with nothing between them. There is no place to record the quality scorecard ref, the compliance scorecard ref, or the Delivery Gate's five checks (useful, valuable, on-brand, accurate, aligned).
3. **Plain words is not a field.** OL-2.1 (Plain Meaning First) has no dedicated summary field in the brief's handoff contract.
4. **Evidence-per-claim is not structured.** §5's verification contract is law-as-prose; there is no per-claim evidence table the seat fills.

**Fix:** because the file is LEARN-managed (hand edits overwritten), the fix ships as an adoptable addendum with LEARN markers — `fixed-dispatch-brief-addendum.md` (standalone, same directory as this audit). It adds: **§2b DECISION CALCULATOR** (fill-in fields), **§7 QUALITY GATE** (fill-in fields incl. delivery-gate five checks), a **PLAIN-WORDS SUMMARY** field in §8, and an **EVIDENCE TABLE** field in §5. Insertion points are marked; the learn-ingestion system adopts them as managed content.

---

## T2 — PR template → LAW-HOSTILE (missing entirely)

**Template:** `.github/pull_request_template.md` — does not exist in the repo (`.github/` holds only workflows). Every seat invents its PR body from scratch. The law's requirements — plain-words summary, evidence, scorecard refs, activation receipt ref — are optional prose a seat may or may not remember.

**Fix:** full fixed template below and as standalone file `fixed-pr-template.md` (assembly: write to `.github/pull_request_template.md`).

---

## T3 — Issue templates → LAW-HOSTILE (missing entirely)

**Template:** `.github/ISSUE_TEMPLATE/` — does not exist. Claims, work items, and bug reports land with no structure: no objective field, no evidence field, no authority field. A claim without structure is a claim that can't be scored.

**Fix:** minimal fixed issue template below (assembly: `.github/ISSUE_TEMPLATE/work-item.md`). Kept small on purpose — an issue is a work REQUEST, not a review.

---

## T4 — Activation receipt template → LAW-HOSTILE (hollow)

**Template:** `NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json` — exists, but it is a skeleton of nulls: no ritual-domain binding fields, no freshness rule in the schema, no validity criteria (what makes a receipt VALID vs present). A seat can fill every field and still be unactivated in every way that matters.

**Fix:** NOT rebuilt here — receipt hardening belongs to Layer 2 (activation ritual with teeth), which owns this file. Flagged so the layers connect: Layer 2's hardened receipt must add (a) named law-domain fields, (b) a freshness TTL in the schema, (c) a validity predicate, or D1 of the compliance scorecard will keep scoring receipts that Layer 2 can't produce.

---

## T5 — Design blocks directory → LAW-HOSTILE (dangling reference)

**Template:** `BRAIN/10-INTERFACES/DESIGN-BLOCKS/` — does not exist on main. The brief template (§7b) instructs seats to "Build from Smart Blocks (`BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/`) — never ad-hoc CSS" — a path that resolves to nothing. A seat that tries to follow the law finds no blocks; a seat that breaks it finds CSS everywhere. The law is literally harder than breaking it.

**Fix:** NOT built here — the block library is a lane-owner deliverable (PR #1967, open as draft: 148 blocks; master catalog pending). Flagged as a Layer 5 finding: until the directory lands on main, §7b of the brief points at air. Recommended interim: the brief's §7b should name the interim source of truth (the design-doctrine.md + the draft PR) instead of the missing path.

---

## T6 — Report / data schemas → LAW-DEFAULT (good — said so, not rebuilt)

**Templates:** `.naya/specifications/NAYA-DECISION-VALUE-CALCULUS-V2.1.schema.json` (machine twin of the calculator), `0003-full-auto-merge-v1.machine.json` (five-step receipt schema), the System Scorecard's fixed areas + method rules, and (new) `compliance-scorecard-template.json` from Layer 4.

**Verdict:** the machine side is already structured. The gap was never here — it was that no independent-REVIEW template existed (fixed by Layer 4's compliance scorecard) and the human-side templates above lacked the matching fields (fixed by this audit). No rebuild.

---

# FIXED TEMPLATES

## FIXED (1) — Dispatch brief addendum

Standalone file: `fixed-dispatch-brief-addendum.md`. Insert the three sections at their marked points in the brief; the learn-ingestion system adopts them as LEARN-managed content.

## FIXED (2) — PR template (assembly target: `.github/pull_request_template.md`)

<!-- PR template — fill in every section. Delete a section only if it truly doesn't apply, and say why. -->

## 1. Plain-words summary
<!-- What changed, in words a non-technical human understands: what happened, what's going on, should anyone be concerned. (Operating Law 2.1) -->
[fill in]

## 2. Objective
[What this PR is for — one or two sentences.]

## 3. Decision calculator
<!-- The math behind the approach. Required for any non-trivial change. (Operating Law 1.2, 1.4) -->
- **Objective:** [ ]
- **Options considered:** [as many as are real — never ritualistically three]
- **Option A:** [summary] — pros: [ ] / cons: [ ] — score: [ ]/10
- **Option B:** [summary] — pros: [ ] / cons: [ ] — score: [ ]/10
- **Winner:** [ ] — chosen by the numbers because: [ ]
- **Gate check:** [ ] PROHIBITED / [ ] NEEDS_AUTHORITY / [ ] NEEDS_EVIDENCE / [x] ADMISSIBLE
- **Falsifier:** [the concrete evidence that would prove this decision wrong]

## 4. Evidence the change landed
<!-- Claims carry sources. A PR that can't prove its change landed is a claim, not a delivery. (Operating Law 4.6, 8.3) -->
- [ ] Diff reviewed against the actual base (not memory): base SHA [ ]
- [ ] Tests: [green on head SHA ___ / not applicable because ___]
- [ ] Proof the change is IN the branch: [blob SHAs / test output / render — what did you check?]

## 5. Scorecards
<!-- Both halves of the review. (Operating Law 5.4) -->
- Quality scorecard ref: [ ]
- Compliance scorecard ref: [ ]
- Activation receipt ref (work done activated): [ ]

## 6. Delivery gate (all five, or don't send)
<!-- Operating Law 2.2 — check each honestly. -->
- [ ] Useful — this does something someone needs
- [ ] Valuable — the value exceeds the review cost
- [ ] On-brand design — matches the design doctrine (or N/A: no user surface)
- [ ] Accurate — every claim above is true to the evidence
- [ ] Aligned with intent — this is what was actually asked for

## 7. Risks and reversibility
- Risks: [ ]
- Reversible in one commit? [yes / no — if no, human gate required]

---

## FIXED (3) — Issue template (assembly target: `.github/ISSUE_TEMPLATE/work-item.md`)

```markdown
---
name: Work item
about: A claim, task, or bug that a seat will pick up
---

## What
[One plain-words paragraph: what is wanted or what's wrong.]

## Why it matters
[The value if fixed / the cost if ignored.]

## Evidence so far
[Links, SHAs, screenshots, comment ids — whatever exists. "None yet" is an honest answer.]

## Authority
[ ] Within existing standing authority — any seat may claim
[ ] Needs Shawn's word — protected gate: [which one]

## Acceptance
[How a reviewer will know it's done. One to three checkable lines.]
```
