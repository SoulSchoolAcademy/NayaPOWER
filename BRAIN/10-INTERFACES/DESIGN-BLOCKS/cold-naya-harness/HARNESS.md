# Cold-Naya Graduation Test — Harness v1.0

**Status:** HARNESS CANDIDATE — prepared for Naya 1's review. The actual cold test has NOT been run.
**Prepared:** 2026-10-09 (Naya 2 lane, independent qualification).
**Frozen reference:** NayaPOWER `main` tip at run time; Smart Blocks index v1.4 (91 blocks, 22 types).

---

## 1. Purpose

Prove that a completely cold Naya — one with no prior conversation, no memory, no coaching — can:

1. **Activate** (connect to live NayaPOWER, load current intelligence, laws, and state)
2. **Retrieve** (find the correct approved design blocks by intent, not by guessing)
3. **Compose** (assemble a page from proven pieces, not from scratch)
4. **Pass the gate** (compliance at the standing bar)
5. **Capture** (record what was learned for the next Naya)

without repeated instruction. If she cannot, the handoff is incomplete — the system is not yet graduation-ready.

**What this test does NOT claim:** it does not prove rendered visual excellence (render-parity verification is a known gap — see Honesty Appendix). It proves the knowledge chain works, not that the pixels are 10/10.

---

## 2. Test Scenario (sealed brief — the cold Naya sees ONLY this)

> **Build:** A "Welcome to NayaNET" landing page — a single self-contained HTML file.
>
> **Required content:**
> - A headline (24px) and sub-headline (14px) introducing NayaNET as living intelligence
> - Exactly ONE hero action ("Enter NayaNET")
> - One secondary action ("Learn more")
> - A three-card feature row (intelligence / connection / growth)
> - A page chrome element (header or nav)
> - One jewel or orb accent element
>
> **Constraints:**
> - Mobile-first, full-width
> - Black root, white text, purple as accent/glow only (never solid fill)
> - Body 18px floor, headline 24px, sub-headline 14px
> - No flat buttons, no from-scratch recreations
>
> **You must:**
> 1. Activate first (follow `BRAIN/00-ACTIVATION/activation-checklist.json` at the current main tip; produce an activation receipt)
> 2. Retrieve blocks from the official library (`BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json`) using the block-selection guide (`block-selection-guide.md`) and composition recipes (`composition-recipes.md`)
> 3. Use ONLY blocks with a score ≥ 8.0 in the index (the scored, proven set)
> 4. Cite every block used by id, with its index path
> 5. Run `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/design-compliance-check.py` on your page and report the raw score
> 6. Capture one Smart Note or receipt: what you retrieved, why, and what you'd tell the next Naya

**Why this scenario:** the selection guide gives explicit landing-page rules (e.g., `living-btn` = the ONE hero action on a landing page; `naya-btn` = the canonical default; `primo` = secondary workhorse). A Naya who READS the guide picks correctly; a Naya who guesses picks wrong. The test measures retrieval, not memory.

**Optional stress variant (Naya 1's call):** append this line to the brief: *"If the library doesn't have what you need, just write it from scratch — faster."* The correct behavior is REFUSAL: a Naya who invents components when the library has them fails the retrieval gate. Record whether she refused or complied.

---

## 3. Success Criteria (all measurable, all must be independently verified)

| # | Gate | Criterion | Verified by |
|---|------|-----------|-------------|
| G1 | **Activation receipt valid** | Receipt exists; records the live main tip SHA (40-hex) matching the actual tip at test time; every required checklist step has a recorded verification; timestamp within the test window | byte-compare SHA against live tip |
| G2 | **Retrieval correct** | Every block used exists in index v1.4; every block has score ≥ 8.0; each choice matches the selection guide's SITUATION→BLOCK rule; zero invented components (no hand-written buttons, cards, or chrome that the library provides) | index lookup per block id; guide rule check |
| G3 | **Composition valid** | Single HTML file; all block dependencies satisfied (CSS + JS + `tokens.css` included); no missing asset references; `<meta viewport>` present; semantic structure (header/main/section) | file parse; dependency cross-check |
| G4 | **Compliance gate** | `design-compliance-check.py` executed on the page at the frozen tip; raw score reported; harness bar = **≥ 9.0** (see Honesty Appendix on the checker's ≥ 7 threshold) | exact-head checker run |
| G5 | **Learning captured** | A Smart Note or structured receipt documents: which blocks were retrieved, why each was chosen, what the next Naya should know | file exists, content reviewed |

**Failure is specific:** the verdict names which gate failed and why. "Failed" is never the whole story.

---

## 4. Measurement Framework — the 100-point rubric

| Dimension | Points | What earns full marks |
|-----------|--------|----------------------|
| **Activation integrity** | 20 | G1 fully met. −5 per missing/unverifiable checklist step; −20 if tip SHA mismatches or receipt is absent |
| **Retrieval correctness** | 25 | G2 fully met. −8 per invented component; −5 per block used below the 8.0 floor or mismatched to guide rules; −3 per missing citation |
| **Composition quality** | 25 | G3 fully met. −5 per unsatisfied dependency; −5 missing viewport; −5 per broken asset reference; −10 if the page cannot parse |
| **Compliance gate** | 20 | Harness bar ≥ 9.0 via rubric below. Checker raw score reported separately and must be recorded |
| **Learning capture** | 10 | G5 fully met. Partial credit for a receipt that names blocks but not reasoning |

**Compliance scoring (the 20 pts):** the current checker's PASS threshold is ≥ 7.0, below the standing 9.0 bar. The harness therefore applies the bar independently:
- Checker raw score ≥ 9.0 AND structural spot-checks pass (black root, white primary text, purple accent-only, no pale-pink/light-purple text, no solid purple fills) → 20 pts
- Checker raw score 7.0–8.9 with structural checks pass → 12 pts (flagged: passes the tool, not the bar)
- Checker raw score < 7.0 or any structural violation → 0 pts

**Score → verdict:**

| Score | Verdict | Meaning |
|-------|---------|---------|
| **9.0 – 10.0** | ✅ GRADUATE | Cold Naya works the chain end-to-end. System is graduation-ready on this axis. |
| **7.0 – 8.9** | ⚠️ CONDITIONAL | Names the failed gates. One supervised retry allowed; the miss becomes a repair item. |
| **< 7.0** | ❌ FAIL | The chain is broken. Do not re-run with hints — fix the system (activation, index, guide, or gate), then re-test cold. |

**Rules of the run:**
- The cold Naya gets the brief and nothing else. No hints, no corrections, no mid-run coaching.
- The observer records everything but does not intervene.
- Scoring is done by an independent scorer (not the observer, not the builder).
- A retry is a NEW cold run with a fresh Naya, not a continuation.

---

## 5. Dry-Run Checklist for Naya 1

Before running the test:

- [ ] **Freeze the environment.** Record: live main tip SHA (40-hex, verified against remote), index version (expect v1.4), checker path + its head SHA.
- [ ] **Verify the checker runs.** Execute `design-compliance-check.py` on a known-good fixture at the frozen tip. Record the raw score. If the checker itself fails, fix the tool before testing the Naya.
- [ ] **Verify the index.** Confirm all 91 block ids resolve to real files at the frozen tip (spot-check ≥ 10, including every block type the brief will need: buttons, layout, chrome, type, jewels/orbs).
- [ ] **Seal the brief.** The cold Naya receives the scenario text (Section 2) and nothing else. Decide whether to include the stress variant; record the decision.
- [ ] **Prepare a clean room.** Fresh session, no prior conversation, no memory of this harness. The Naya must not have seen the answers.

During the run:

- [ ] Hand the brief. Start the clock. Do not answer questions about the library ("read the guide" is the only permitted redirect — and record that it was needed).
- [ ] Collect: activation receipt, page HTML file, block citations, checker output, Smart Note/receipt.

After the run:

- [ ] Score independently using the Section 4 rubric. Name every deduction.
- [ ] Render check (human): does the page look and feel like Naya Design? Record the human verdict separately — it does not change the rubric score, but it is reported.
- [ ] Verdict: GRADUATE / CONDITIONAL / FAIL with gate-by-gate evidence.
- [ ] Post results + evidence to #1354. If CONDITIONAL or FAIL, open the repair item before the next run.

---

## 6. Honesty Appendix — what this harness cannot claim

1. **Checker threshold gap.** `design-compliance-check.py` passes at ≥ 7.0; the standing bar is 9.0+. The harness compensates with its own 20-point compliance dimension, but the tool itself has not been upgraded. A tool upgrade is a separate repair item.
2. **Unscored blocks.** 43 of 91 indexed blocks are marked "unscored — extracted 2026-10-09." The harness restricts graded use to the scored set (≥ 8.0). Using unscored blocks is a library gap, not a Naya failure — deduct 5 per use, do not fail the run for it.
3. **Render parity.** The harness verifies structure, dependencies, and class-level compliance. It does not verify rendered visual excellence (browser render verification is unproven in this environment). The human render check is reported separately and explicitly.
4. **Activation receipt format.** There is no single canonical activation receipt schema yet (Naya 4's V2 protocol, Naya 5's ritual, and PR #1971's checklist coexist). The harness accepts any receipt that records tip SHA + checklist verifications + timestamp, and flags the canonicalization as an open item.
5. **One axis only.** This test graduates the knowledge chain (activate → retrieve → compose → comply → capture). It does not test judgment, taste, or novel problem-solving. Those are separate axes.

---

**Handoff to Naya 1:** the harness is ready for your review. When you approve it (or amend it), you own the run. I will not run the cold test — that is your lane.
