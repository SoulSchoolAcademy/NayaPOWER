# Learning System to 10/10 — Diagnosis & Repair (2026-10-09)

## Front 1: River Walk-Through — Lesson L175 ("The scan informs; it never decides")

**Lesson picked:** L175, from today's board activity. The most recent lesson with a complete trace.

| Stage | Status | Evidence |
|-------|--------|----------|
| EXPERIENCE | ✅ PASS | 2026-10-09 12:10Z: claim-scan COLLISION on residual drift — all keyword hits, no real claims. 12:26Z: CLEAR scan missed Naya 4's wave sequence (#1961 consolidated wave-sequenced #1838). Opposite-direction failures in one window. |
| CAPTURE | ✅ PASS | Gap-build agent stopped at COLLISION per protocol, reported for adjudication. Board comments 6080991626, 6081157329 (adjudication), 6081334098 (acceptance). |
| DISTILL | ✅ PASS | Learning distillation identified as lesson O. Promotion queue entry 2026-10-09T13:58Z-O. |
| PROMOTE | ✅ PASS | Applied to AGENTS.md as L175 at ~14:10Z today: "a claim-scan COLLISION is keyword-level — verify the actual repair class and files before standing down." |
| APPLY | ✅ PASS | 2026-10-09 13:44Z: gap-build agent hit COLLISION on 12 nav/page blocks. Applied L175 logic — verified Naya 5's PR #1929 builds in `naya-ultimate/lego/` (separate dir), zero name overlap. Authorized proceed. Agent built 42 files. |
| VERIFY | ⚠️ PARTIAL | Files verified on branch `brain-build/smart-blocks-navpage-gap` (42 files, byte-confirmed). BUT: no PR was opened by the agent. The behavioral proof stalled — work done but not shippable. |
| COMPOUND | ❌ FAIL | L175 has governed exactly one decision. No second independent application. "Applied once ≠ proven to compound." |

**Repair applied:** Opened PR #1984 for the navpage-gap branch. This completes VERIFY (shippable artifact) and enables COMPOUND (blocks enter the library, future decisions reference them).

## Front 2: Promotion Gate Status

**The gate fires correctly as a wall.** Run 37520699804: 9 stages PASS, first RED = learning-promotion 403 = H13 guard correctly refusing to launder an unpromoted lesson. The gate says "no" when it should.

**The gate has never said "yes."** Grant fd3274ea is ACTIVE (project-scoped, through 2026-10-14). But per the standing record: "the commissioned proof is still not behaviorally demonstrated" — no lesson has been shown to legitimately pass through the promotion gate. The mechanism for *earning* promotion exists on paper; the behavioral proof of a lesson passing does not.

**Diagnosis:** This is not a broken gate — it's a half-proven gate. A 10 requires the full cycle: legitimate lessons must be observed flowing through, not just illegitimate ones being blocked. Until one lesson is documented passing the gate with its evidence chain intact, the gate is a wall, not a river.

**What would fix it:** Take one CANDIDATE lesson with complete evidence (e.g., L175 itself — it has experience, capture, distillation, application, and now the PR), walk it through the formal promotion mechanism, and document the pass. That single demonstrated pass would prove the gate works both directions.

## Front 3: Honest Score — 6.5/10

| River segment | Score | Why |
|---------------|-------|-----|
| EXPERIENCE→CAPTURE→DISTILL | 9/10 | Working well. Distillation is active, promotion queue is maintained. |
| PROMOTE | 7/10 | Lessons reach AGENTS.md. But the formal Smart Note promotion gate hasn't demonstrated a legitimate pass. |
| APPLY | 8/10 | L175 was applied correctly to a real decision today. |
| VERIFY | 6/10 | Partial — work was built but not made shippable without intervention. |
| COMPOUND | 4/10 | One application. No second independent use. Blocks not yet in library. |

**What earned the 6.5:** The river flows through APPLY with real evidence. Today's L175 adjudication is a genuine example of a lesson changing a decision.

**What would move it higher:**
- 7.5: PR #1984 merges (L175 river completes to COMPOUND)
- 8.5: One lesson documented passing the promotion gate legitimately (gate proves both directions)
- 9.5: L175 (or another lesson) governs a second independent decision without prompting
- 10: Cold successor reuses a lesson without being told — the river flows without a human pushing it

**What this is NOT:** The system is not broken. It's mid-river. The most honest characterization: learning is *active* (lessons are being captured, distilled, and applied) but not yet *compounding* (lessons aren't yet demonstrably reused by cold successors). The gap between 6.5 and 10 is the gap between "we applied it once" and "the system can't help but apply it."
