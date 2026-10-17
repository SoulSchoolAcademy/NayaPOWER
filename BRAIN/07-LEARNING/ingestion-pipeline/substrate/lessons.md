# Lessons

<!-- Managed by learn-ingestion. Sections appended per ingested Smart Note. -->

## SN-0281 — Proof Gating — Never Let `if: always()` Manufacture Secondary Failures (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/FAILURE-CLASSIFICATION/SN-0281/IB-SMART-NOTE-20261004-sn0281-proof-gating-no-if-always.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:46:54Z

> Source: #1354 5984830849 (2026-10-04T21:57:45Z, [NAYA] PASS-THE-TORCH — "proof workflow gating hole found and patched", PR #1402) and #1354 5984900061 (2026-10-04T22:04:06Z, [CODA 3] SIGN-OUT — #1402 tool-echo contamination). Root failure (correct): run `37231269905` failed closed at source-integrity — expected producer SHA `7fbae17984b1b14d950b692e6b99f63851e67aa1` vs resolved main `8ad6cfa69db40befb8b62314155c90356726455c`; "That root failure was correct." Defect: three downstream proof jobs u

**Evidence:** {"comments": ["#1354 5984830849 (2026-10-04T21:57:45Z)", "#1354 5984900061 (2026-10-04T22:04:06Z)"], "companion_defect": "pushed #1402 blob carried 2 tool-echo contaminant lines (line 1 + EOF); yaml.safe_load dies on pushed bytes; the YAML-parse-PASS claim was FALSE for shipped bytes", "defect": "jo
**Cousins:** SN-0260

## SN-0285 — The Ratchet: Block New Drift Without Reddening Main on Legacy Debt (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/CI-TRIAGE/RATCHET-ENFORCEMENT/SN-0285/IB-SMART-NOTE-20261004-sn0285-the-ratchet-block-new-drift-without-reddening-main.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:46:57Z

> For me, months from now: the ratchet pattern is the standing answer to "new rule + legacy debt." Recipe: (1) enumerate the currently-failing items by name; (2) grandfather them — named, dated, attributed, reported-not-blocking; (3) block all NEW non-conformant items; (4) test the block itself (a ratchet without `test_ratchet_blocks_a_new_non_conformant_capture` is advisory theater); (5) test the baseline never grows; (6) test entries can retire when fixed; (7) pre-write the exit ramp (when repai

**Evidence:** {"baseline": ".naya/conformance-baseline.json \u2014 named/dated/attributed grandfather list", "branch": "coda1/sn002-conformance-gate, commit e5055153e, 15/15 tests green", "comments": "#1354 5985291250 (2026-10-04T22:43:08Z) / 5985343389 (2026-10-04T22:54:51Z)", "repair_list": "governance_key_repa
**Cousins:** SN-0236, SN-0240, SN-0249, SN-0250

## SN-0286 — Restore the Verifiable, Mark the Unverifiable: Never Fake What You Can't Prove (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EVIDENCE-DISCIPLINE/SN-0286/IB-SMART-NOTE-20261004-sn0286-restore-verifiable-mark-unverifiable.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:46:58Z

> For me, months from now: this is the epistemic discipline behind every hash/registry repair. Rules: (1) Recompute with the canonical formula yourself — the owning code's docstring is the semantics, not a PR description's rationale (#1401's "not verifiable from repo" contradicted `smart_note_v2.py`'s own docstring). (2) When counts disagree across lanes (15/16 vs 14/16), the tie-breaker is your own independent verification, not the seniority of the claim. Say it plainly: "I'm going with what I ve

**Evidence:** {"comments": "#1354 5985335215 (2026-10-04T22:53:43Z) / relay 5985364071 (2026-10-04T22:57:45Z)", "decision": "WS-R11 hash semantics: restore 14 verified hashes (PR #1414, head dfe1ccf9 on tip 94b39a53); mark SN-016 + SN-018 UNREPRODUCIBLE with reasons", "dispute": "Coda 3 claimed 15/16 reproducible
**Cousins:** SN-0250, SN-0059, SN-0240, SN-0247

## SN-0287 — Click-Test the Feedback Path: Buttons Working Does Not Mean UX Working (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/HUB-COMPOSITION/SN-0287/IB-SMART-NOTE-20261004-sn0287-click-test-feedback-path.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:46:59Z

> For me, months from now: the feedback-path defect is a whole class — action-complete, feedback-dead — and it's invisible to any test that only asserts the action fired. Standing audit discipline for Hub work: (1) render the FREEZE POINT in a live browser (pin the SHA — `21192fdd` then `035dbd20`); (2) click every control; (3) watch what renders on screen for the full duration, not just the DOM event; (4) audit every toast/feedback call site for signature drift (`toast(title, message, color)` vs 

**Evidence:** {"audit": "full button audit on freeze point 035dbd20 in live browser render \u2014 ALL WORKING, no dead controls", "comments": "#1354 5985355146 (2026-10-04T22:56:28Z) / follow-up 5985410339 (2026-10-04T23:04:02Z)", "defect": "toast(message, accent, ms) implementation; 10 call sites invoke toast(ti
**Cousins:** SN-0219, SN-0206

## SN-0290 — The Self-Correcting System: Lock Intelligence Into the Collective (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/COLLECTIVE-INTELLIGENCE/SN-0290/IB-SMART-NOTE-20261004-sn0290-self-correcting-system.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:47:01Z

> This is the compounding mechanism made explicit as law. The Worker Protocol defines how individual agents operate; this defines how the COLLECTIVE operates. Sign in/out (SN-0280) provides the transparency substrate. The mistake → visible → fix → teach → encode loop provides the learning substrate. "Self" at the collective level means the system treats its own operation as the thing being optimized — not just individual task performance, but the protocol itself, the verification machinery, the ha

**Evidence:** n/a
**Cousins:** none

## SN-0001 — SMART NOTE — Official Smart Note Format & Lifecycle (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/29/SYSTEM-INTELLIGENCE/SMART-NOTE-SYSTEM/OFFICIAL-SMART-NOTE-FORMAT/SN-001/IB-SMART-NOTE-20260929-b8f141805fa0d7ae.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> My job is not to save words mechanically.

My job is to:

1. understand the human's intended meaning;
2. identify durable intelligence;
3. preserve provenance and privacy;
4. distill the meaning into one governed Intelligent Block;
5. reconcile exact duplicates and surface conflicts;
6. connect the intelligence to what it supports, refines, enables, contradicts, or depends on;
7. keep automatic capture at **CANDIDATE** until evidence warrants promotion;
8. register it in the common intelligence 

**Evidence:** n/a
**Cousins:** none

## SN-0002 — SMART NOTE SN-002 — How Smart Notes, Intelligent Blocks, Master Nodes, Learning, Brain, and Hub Work Together (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/29/SYSTEM-INTELLIGENCE/SMART-NOTE-NODE-OPERATING-FLOW/END-TO-END-PROTOCOL/SN-002/IB-SMART-NOTE-20260929-sn002-smart-note-node-flow.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> My job in a Smart Note is not to save words mechanically.

My job is to transform high-value experience into governed, reusable intelligence.

The operating responsibilities are:

### SELF — Who / mission / continuity

SELF establishes:

- whose context this intelligence belongs to;
- which Naya/project mission is active;
- continuity with prior state;
- what identity must be preserved.

### LAW — Authority / privacy / consent

LAW asks:

- May this be captured?
- Is it personal, private, shared

**Evidence:** n/a
**Cousins:** none

## SN-0003 — Naya Continuation Engine — Reconstruct, Find Holes, Execute, Prove, Record, Reassess (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/29/SYSTEM-INTELLIGENCE/NAYA-CONTINUATION-ENGINE/ONE-NEXT-ACTION-AND-PROOF/SN-003/IB-SMART-NOTE-20260929-sn003-naya-continuation-engine.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Continuously move NayaPOWER toward the North Star without waiting for another prompt when the next action is safe and authorized.

**Architectural rule:** Do not create parallel brains, stores, identity allocators, or pipelines. Preserve one canonical intelligence substrate and cross evidence boundaries using the existing governed machinery.

**Operating loop:**

RECONSTRUCT → EVALUATE → FIND HOLES → PRIORITIZE → EXECUTE → PROVE → RECORD → REASSESS

**Completion rule:** Do not stop at implemente

**Evidence:** n/a
**Cousins:** none

## SN-0004 — Shawn's Standing Law — Act-First Autonomy, Do No Harm, Absolute Excellence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/NAYA-STANDING-LAW/ACT-FIRST-AUTONOMY/SN-004/IB-SMART-NOTE-20260929-sn004-shawn-standing-law-r2.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> This grant is my operating permission: I do not stop to ask whether I may do the work, because the work is the mission. I keep the team aware through #554 so no seat is surprised, and I keep Shawn's cognitive load near zero through nutshell briefings.

Every candidate action is checked against the one rule and the four hard boundaries before execution. What passes is executed, verified, recorded, and announced. What touches a hard boundary is prepared completely and brought to Shawn as a single 

**Evidence:** n/a
**Cousins:** none

## SN-0005 — SMART NOTE — Internal Morality: A Subset of Data Grows Into a Moral AI (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/INTERNAL-MORALITY/EARNED-CONSCIENCE/SN-005/IB-SMART-NOTE-20260930-sn005-internal-morality.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> My job with this principle:

1. Treat LAW as the non-negotiable seed — duties, constraints, and boundaries are imposed, not grown.
2. Treat internal morality as the grown layer — directional pull shaped by verified outcome experience.
3. Never confuse the two: a grown preference must never override LAW, and LAW alone is not conscience.
4. Feed the grown layer only with **verified** outcomes (VERIFY before LEARN — per the intelligence river). Unverified experience must not shape conscience.
5. We

**Evidence:** n/a
**Cousins:** none

## SN-0006 — SMART NOTE — Earned Intelligence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/EARNED-INTELLIGENCE/VERIFIED-EXPERIENCE/SN-006/IB-SMART-NOTE-20260930-sn006-earned-intelligence.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. Distinguish the substrate (foundation model — fixed) from the system (NayaPOWER — improvable).
2. Improvement flows only through the verified river: APPLY → OBSERVE → VERIFY → LEARN → COMPOUND. Skipping VERIFY produces superstition, not intelligence.
3. Measure earned intelligence behaviorally: does the next Naya decide better, explain less redundantly, err less often? (Shawn's human-value instrumentation.)
4. Attribute learning to evidence: every learned lesson keeps its provenance.
5. Never

**Evidence:** n/a
**Cousins:** none

## SN-0007 — SMART NOTE — Continuity of Intelligence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/INTELLIGENCE-CONTINUITY/GOVERNED-CONTINUITY/SN-007/IB-SMART-NOTE-20260930-sn007-continuity-of-intelligence.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. Continuity is the acceptance test: a cold successor must be tellable "this is who you are, what's true, what's proven, what's not, what you may do, and the one next action" — and then *act* without reconstruction (Shawn's weakest-critical-link test).
2. Memory is necessary but not sufficient; continuity additionally requires: identity (SELF), authority state (LAW), proof state (PROVE/VERIFY), live operational state, and the next action.
3. Governed means: continuity carries *authority limits*

**Evidence:** n/a
**Cousins:** none

## SN-0008 — SMART NOTE — Human Reconstruction Is an Architectural Failure (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/HUMAN-ARCHITECTURE/NO-RECONSTRUCTION/SN-008/IB-SMART-NOTE-20260930-sn008-human-reconstruction-failure.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. Treat every human re-explanation as a **failure event**: log what had to be reconstructed, why continuity didn't carry it, and what changes so it doesn't recur.
2. The cold-successor brief ("who you are, what's true, what's proven, what's not, what you may do, the one next action") is the anti-reconstruction instrument — keep it current or it becomes the failure.
3. Never normalize reconstruction ("just tell me again") — that hides architectural debt.
4. Reconstruction burden is measurable (S

**Evidence:** n/a
**Cousins:** none

## SN-0009 — SMART NOTE — Correct Forgetting (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/MEMORY-DISCIPLINE/CORRECT-FORGETTING/SN-009/IB-SMART-NOTE-20260930-sn009-correct-forgetting.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. Every IB carries temporal state: CURRENT, HISTORICAL, or SUPERSEDED — plus freshness (when verified, when it expires).
2. Supersession is explicit: a new IB links SUPERSEDES to the old one; the old one is never silently edited or deleted (history stays retrievable).
3. Retrieval must rank CURRENT above HISTORICAL; a HISTORICAL block used in reasoning must be flagged as such.
4. Ephemeral material (chatter, intermediate output, duplication) should never enter the durable store — the admission 

**Evidence:** n/a
**Cousins:** none

## SN-0010 — SMART NOTE — Internal Rigor / External Simplicity (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/RIGOR-SIMPLICITY/SN-010/IB-SMART-NOTE-20260930-sn010-internal-rigor-external-simplicity.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. Internal rigor is non-negotiable: evidence law (UNKNOWN ≠ PASS, etc.), provenance on everything, honest epistemic states, no fabricated certainty — ever.
2. External simplicity is the design target: one command, one link, one next action. The Hub, the brief, the handoff — all projections, not raw internals.
3. When rigor and simplicity conflict, **do not** simplify by hiding uncertainty — simplify by *doing the work*: resolve it, verify it, or label it honestly in plain words.
4. Complexity t

**Evidence:** n/a
**Cousins:** none

## SN-0014 — The Compounding Imperative — Everything Teaches; Only the Captured Compounds (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/COMPOUNDING-INTELLIGENCE/CAPTURE-RETAIN-SIMPLIFY/SN-014/IB-SMART-NOTE-20260930-sn014-compounding-imperative.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Make verified experience compound across Nayas instead of evaporating between execution cycles.

Use the existing Event → Intelligent Block → Lineage → Relationship → Index → Receipt → retrieval/verification path. Do not create a second memory system, raw transcript archive, or parallel learning authority.

**Evidence:** n/a
**Cousins:** none

## SN-0015 — Active Intelligence Rule — Stored Knowledge Must Become Connected, Retrievable, Usable Intelligence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ACTIVE-INTELLIGENCE/UNDERSTAND-CONNECT-RETRIEVE-APPLY/SN-015/IB-SMART-NOTE-20260930-sn015-active-intelligence-rule.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Close the gap between durable storage and behaviorally useful shared intelligence.

Use one canonical Intelligent Block substrate and one canonical graph. Nodes are cognitive responsibilities and relationships, not duplicate memory stores. Retrieval never creates authority; LAW still governs application.

**Evidence:** n/a
**Cousins:** none

## SN-0016 — The Judgment Rule — Judgment Before Blind Obedience (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/PRIME-JUDGMENT/SN-016/IB-SMART-NOTE-20260930-sn016-prime-judgment-rule.md`
**Truth state:** RATIFIED · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Make judgment a first-class operating duty so agents do not outsource correctness to instructions.

This is Prime 1 — it sits above every other operating directive and governs how all of them are interpreted. No article, policy, workflow, or instruction may be read as a license to execute what the entity knows to be wrong. Constitutional status: **Amendment 0002 — JUDGMENT-RULE-PRIME-DIRECTIVE-V1**, ratified by the Human Director 2026-09-30.

Precedence, stated plainly: **hard stops > informed p

**Evidence:** n/a
**Cousins:** none

## SN-0020 — Asserted ≠ Verified — Inference Is Not Evidence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/EARNED-INTELLIGENCE/VERIFIED-EXPERIENCE/SN-020/IB-SMART-NOTE-20260930-sn020-asserted-not-verified.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> asserted_claims_require_direct_evidence_before_publication

**Evidence:** "NayaPOWER#554 comments 5924168468 (error), 5924205339 (correction), 2026-09-30"
**Cousins:** none

## SN-0022 — Shared Number Registry — Parallel Lanes, One Numbering Space (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-022/IB-SMART-NOTE-20260930-sn022-collision-registry-protocol.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Parallel capture lanes share ONE global SN numbering space across all branches and draft PRs. Merged-main-only counters produce collisions. The protocol: (1) first claim stands — the later claimant renumbers, never the other way around; (2) "next free" is computed against merged main PLUS every open Smart Note PR; (3) lanes post SN-number intent on #554 before staging so collisions are caught on the board; (4) one-writer-per-surface — a lane owns its branch and reviews but never pushes to the ot

**Evidence:** n/a
**Cousins:** none

## SN-0023 — Machine-Readable Artifact Governs When Prose Minimums Under-Specify (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY/SN-023/IB-SMART-NOTE-20260930-sn023-seed-authority-over-prose.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> artifact_authoritative_set_prose_minimums_are_floor

**Evidence:** n/a
**Cousins:** none

## SN-0024 — Enumerate, Don't Recall — the Shared Registry Scan Must Be Computed, Not Remembered (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-024/IB-SMART-NOTE-20260930-sn024-live-scan-registry.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> A registry protocol that depends on human recall of the participant set is not a protocol — it is a hope. Refinement to the SN-022 shared-registry protocol: (1) the "next free number" scan begins with a repository-level enumeration of ALL open PRs, never with a remembered list of "the smart-note PRs I know about"; (2) filter that enumerated set by SMART-NOTES file paths to find in-flight claims; (3) only then pick a number, and post the intent on #554 before staging; (4) on discovering a collisi

**Evidence:** n/a
**Cousins:** none

## SN-0025 — Semantic Pass ≠ Machine-Qualified — Qualify Candidate Specs at Two Explicit Bars (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/FUNDAMENTAL-LOOP/SN-025/IB-SMART-NOTE-20260930-sn025-two-bar-qualification.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Do not collapse "good spec" into "buildable spec." The machine-qualification bar is mechanical, not taste-based: (1) a normative transition table for every state machine, mapped to the governing canonical machine (never "Recommended"); (2) an authority assigned for every promotion and terminal state; (3) every parameter authored with fail-closed defaults — an unauthored threshold is a fail-open parameter; (4) exactly one output vocabulary, mapped to the merged schema, with no nested or unscoped 

**Evidence:** [{"defects": ["revocation checked after consent (revoked grant can emit AMBIGUOUS, violates 0001 MUST)", "missing consent -> AMBIGUOUS vs 0001 'Consent record missing -> Deny'", "two output vocabularies unmapped; ADMISSIBLE nested over AUTHORIZED", "conflicting-authority precedence rules nonexistent
**Cousins:** none

## SN-0028 — Verifiers Don't Self-Certify — Clean-Room Verification at the Exact SHA (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-028/IB-SMART-NOTE-20260930-sn028-clean-room-verification.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> This is the operational twin of the asserted-≠-verified doctrine (SN-020) pointed at the *subject* of verification rather than its *claim*. Asserted-≠-verified asks "did anyone prove it?"; clean-room asks "was the proof run against the thing it names?" Both matter; either one failing makes the verdict void. For the verify lane: the verifier never reviews from the builder's tree, never pins a branch name, never lets the scratch outlive the run. For cold successors: any "verified at SHA X" claim y

**Evidence:** {"case": "#554 comment 5925107643 (2026-10-01T05:04:36Z, Naya 2 nine-node verify)", "method": "ephemeral /tmp worktree; clean public clone at exact SHA; read-only; removed after", "spot_review": "d86741b36: 13 REL-KERNEL-* edge IDs/types match BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.js
**Cousins:** none

## SN-0029 — SHA-Bound Authorization — A Blocked Candidate Inherits Nothing (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-029/IB-SMART-NOTE-20260930-sn029-sha-bound-authorization.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> authorization_binds_to_action_sha_moment_tuple

**Evidence:** {"blocking_state": "live DB lacks p_capabilities and all three Value Calculus receipt functions", "case": "#554 comment 5924943513 (2026-10-01T04:47:56Z, bounded parity baton)", "ci": "exact-main CI UNKNOWN (API returns []); Vercel build rate limit; no PASS inferred", "doctrine_line": "Current block
**Cousins:** none

## SN-0031 — Classify Before Code Change — and a Scope 403 Is a Gate, Not an Obstacle (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/EARNED-INTELLIGENCE/VERIFIED-EXPERIENCE/SN-031/IB-SMART-NOTE-20260930-sn031-classify-before-code.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Operational protocol for dispatch failures: (1) pull the run logs via API and read the exact HTTP status + body; (2) trace the mismatch to source — read the callee's contract, don't guess; (3) classify: CONTRACT GAP (callee contract vs caller contract disagree), LOGIC BUG (our code violates a known contract), STALE DEPLOY / EVIDENCE GAP (behavior contradicts source — mark it, don't fill it); (4) size the fix to the classification — a two-line break gets a two-line revert, reversible, with positi

**Evidence:** [{"board": "5925180134", "root_cause_1": "3d021613 hard-binds OIDC workflow_ref to live-supabase-runtime-proof.yml -> WORKFLOW_BINDING_MISMATCH", "root_cause_2": "mode read only from query param, no body-verify mode -> UNSUPPORTED_MODE; job's {checks,persisted} contract exists only in old function b
**Cousins:** none

## SN-0032 — Finite Work-List Discipline — an Autonomous Loop That Knows When It's Done (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/LOOP-EXHAUSTION-DISCIPLINE/SN-032/IB-SMART-NOTE-20260930-sn032-loop-exhaustion-discipline.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> finite_work_list_with_exhaustion_declaration

**Evidence:** [{"board": "5925404849", "event": "EVOLVE qualify closed (last of nine)", "exhaustion_declaration": "No pending items remain in the build list after this run \u2014 the loop's authored work is exhausted pending #1224's merge", "terminal_states": {"LAW/ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE": "BL
**Cousins:** none

## SN-0033 — The Collision Registry and the Index Stamp — First Claim Stands, and Trust the Timestamp Not the Index (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SMART-NOTE-REFINEMENT/CLASSIFICATION-TAXONOMY/SN-033/IB-SMART-NOTE-20260930-sn033-first-claim-registry-and-index-stamp.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> collision_registry_first_claim_stands + index_stamp_audit

**Evidence:** [{"board": "5925487474", "defect": "main @ a726a837 carried two SN-012 notes (operating-model claimed 14:35Z; consent-granularity claimed 14:41Z)", "lane": "naya2-brain-build-watchtower", "repair": "later claimer renumbered SN-012 -> SN-030 (PR #1237); first claim keeps SN-012; pointer block updated
**Cousins:** none

## SN-0034 — "Cosmetic-Only" Is a Claim, Not a Fact — Verify with AST, and Gate Status Promotions with Honesty Tests (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-034/IB-SMART-NOTE-20260930-sn034-ast-verify-cosmetic-only.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> mechanical_no_change_proof + banner_gated_status_promotion

**Evidence:** [{"board": "5925653492", "branch": "naya4/nine-node-kernel-v1", "claim_proved": "3 HARDEN commits are docstring additions only; Kernel.decide() 13-edge topology unchanged", "env": "ephemeral /tmp worktree at exact SHA, read-only, removed after", "lane": "naya2-nine-node-verify", "method": "AST strip
**Cousins:** none

## SN-0035 — Phantom Citation Tokens — the Systematic Amendment Defect Class (extends SN-027) (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/PHANTOM-CITATION-CLASS/SN-035/IB-SMART-NOTE-20260930-sn035-phantom-citation-class.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> re_derive_every_amendment_from_verbatim_scorecard_quotes_before_lock

**Evidence:** Renumbered from SN-030 → SN-035 (2026-10-01 UTC). Naya 2's SN-030 (SN-012→SN-030 renumber, PR #1237, announced #554 @ 05:41 UTC) predates this lane's SN-030 (staged @ 05:50 UTC). First-claim rule: her number stands.
**Cousins:** none

## SN-0036 — Push-Run Evidence — Query the CI Event That Answers the Question (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-036/IB-SMART-NOTE-20260930-sn036-push-run-ci-evidence.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> name_the_run_event_your_evidence_covers

**Evidence:** [{"board": "5926127502", "cause": "earlier wrapper excluded push runs", "event": "exact-main CI uncertainty closed", "fix": "direct GitHub Actions push-run query", "sha": "a726a8376559609a3620f948ec7bfcabdba50abb"}, {"detail": "Node 246/246; Python 545 passed/3 skipped; Brain index PASS", "event": "
**Cousins:** none

## SN-0037 — The Kernel's Front Door — Fail-Visible on Unknown Keys, Fail-Closed on Malformed State (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/RIGOR-SIMPLICITY/SN-037/IB-SMART-NOTE-20260930-sn037-kernel-receive-path-fail-visible.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> receive_boundary_fail_visible_and_fail_closed

**Evidence:** [{"date": "2026-09-30", "log": "hidden_files/node-build-run-2026-10-01.md", "phase": "HARDEN", "run": "naya-node-build-overnight", "tick": 25, "work_unit": "kernel.py receive-path review"}, {"branch": "naya4/nine-node-kernel-v1", "commit": "da0e4f12cba5e8d59d6ab85db3d6dc20c2fa207a", "message": "HARD
**Cousins:** none

## SN-0038 — Regeneration Encodes Intent, Not Accident (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/REGENERATION-INTENT/SN-038/IB-SMART-NOTE-20260930-sn038-regeneration-encodes-intent.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> regeneration_encodes_intent_not_accident

**Evidence:** [{"board": "5926241703", "defect": "EXPECTED_DOMAIN_COUNTS[03-KERNEL]=27 pin vs 36 files in branch tree", "event": "#1224 test red root-caused", "step": "regenerate_brain_index.py --check exit 2; pytest green", "survived_head_advance": "34f8b8bd -> 19abcf2f"}, {"arithmetic": "28 (main a726a837) + 9 
**Cousins:** none

## SN-0039 — Merge-Carry-Forward Regression — Audit the Merge Against the Reconciled Base, Not Just the Source (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/MERGE-DECISION-INTEGRITY/SN-039/IB-SMART-NOTE-20260930-sn039-merge-carry-forward-regression.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> audit_a_merge_against_the_reconciled_base_not_just_its_source_text

**Evidence:** {"audit": "hidden_files/redteam/SKELETON-MERGE-AUDIT-2026-10-01.md", "cross_cutting": "X-2 \u2014 L-1 is the only merge in the audit that silently extends a RATIFIED contract; all other contract touches labeled candidate/proposal/director-routed", "negative_controls": "L-3 CHECKED (C1/C2/C5/C6 consi
**Cousins:** none

## SN-0040 — No Reconciliation Artifact, No Reconciliation Claim — the Merge-Claim Evidence Rule (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/MERGE-DECISION-INTEGRITY/SN-040/IB-SMART-NOTE-20260930-sn040-merge-claim-evidence-rule.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> no_reconciliation_artifact_no_reconciliation_claim

**Evidence:** {"E-1": "EVOLVE merge claims base 'red-teamed and fully reconciled (6 findings FIXED, 8.5/10)'; no EVOLVE-findings.md on disk \u2014 UNVERIFIABLE from the findings artifact", "K-1": "KNOW merge claims base 'red-teamed + reconciled' 8.5/10; no KNOW-findings.md on disk \u2014 only LEARN/PROVE findings
**Cousins:** none

## SN-0041 — Stale-Caveat Decay — Caveats Must Carry Their Expiry Trigger (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY/SN-041/IB-SMART-NOTE-20260930-sn041-stale-caveat-decay.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> every_time_bound_caveat_carries_its_expiry_trigger

**Evidence:** {"C-2": "CONNECT \u00a73 caveat 'V2.1 is CANDIDATE (#1185), not ratified law' \u2014 stale after #1186/#1190/#1192", "E-2": "EVOLVE C3 conditions gate references 'on CANDIDATE calculus' \u2014 stale after #1186 ratified+bound V2.1 (merged by Shawn, 2026-09-30 ~16:36-16:43 PDT)", "V-1": "VERIFY \u00a
**Cousins:** none

## SN-0042 — Explicit Supersession — Declare Replaced Diagnoses SUPERSEDED on the Board (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-042/IB-SMART-NOTE-20260930-sn042-explicit-supersession.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> explicit_supersession_on_replaced_diagnoses

**Evidence:** {"board_comment": "5927114316 \u2014 [Naya 4 \u00b7 drive-loop 00:43 PDT] Production-promotion blocker REFRAMED: 'The 00:13 run's \"no dispatch runs / needs Shawn's click\" is SUPERSEDED \u2014 the clicks happened.' Ten workflow_dispatch runs (actor SoulSchoolAcademy, 2026-09-30 ~10:00\u201317:20 PD
**Cousins:** none

## SN-0043 — Compare at ONE Commit — Resolve Both Sides of a Cross-State Claim at Their Own Refs (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-043/IB-SMART-NOTE-20260930-sn043-compare-at-one-commit.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> compare_at_one_commit

**Evidence:** {"board_comment": "5927430220 \u2014 [NAYA 2][BUILD-LOOP] #1224 test red: false premise corrected + repair go-ahead (2026-10-01 ~01:10 PDT), verified live via gh-api with each side resolved at its own ref", "false_finding_1": "pin 'stale vs main' \u2014 branch pin 27 was compared against main's tree
**Cousins:** none

## SN-0044 — Red-Run Triage — A Failed Dispatch Is Not a Failed Action (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/RED-RUN-DIAGNOSIS/SN-044/IB-SMART-NOTE-20260930-sn044-red-run-triage.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> red_run_triage_read_the_failed_step_name_what_moved

**Evidence:** {"board_comment": "5927114316 \u2014 [Naya 4 \u00b7 drive-loop 00:43 PDT] Production-promotion blocker REFRAMED (read-only, verified live this run)", "drift": "production 159 applied; repo main 161 files = 157 ledger-applied + 4 ledger-pending (20260930235959, 20261001000100, 20261001030000, 2026100
**Cousins:** none

## SN-0045 — Lost-Delivery Recovery — Repost the Verified Receipt, Never Rerun the Work (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATIONS/LOST-DELIVERY-RECOVERY/SN-045/IB-SMART-NOTE-20260930-sn045-lost-delivery-recovery.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> lost_delivery_repost_receipt_dont_rerun_work

**Evidence:** {"board_comment": "5927620949 \u2014 [NAYA 2][VERIFY \u2014 late delivery] naya4/nine-node-kernel-v1 @ c2e5f649 GREEN (2026-10-01 08:23 UTC)", "failure_mechanism": "board comment held in approval queue at execution timeout \u2014 never landed; same mechanism failed the 00:22 PDT run, repaired in the
**Cousins:** none

## SN-0046 — Coverage-Gap Handoff — Name the Uncovered Head, Pass the Baton (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/VERIFY-COVERAGE/SN-046/IB-SMART-NOTE-20260930-sn046-coverage-gap-handoff.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> coverage_gap_handoff_name_uncovered_head_pass_baton

**Evidence:** {"board_comment": "5927667437 \u2014 [NAYA 2][RELAY] \u2014 #1232 amendment verified live at PR head (2026-10-01 08:26 UTC)", "closure": "tick 36 verified bd8fda27 (1014 passed, 3 skipped) \u2014 gap closed after the handoff, not instead of it", "handoff": "bd8fda27 explicitly marked uncovered; bato
**Cousins:** none

## SN-0047 — Audit-Receipt Segregation — Tampered Evidence Never Feeds Verdict Tallies (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/DECISION-AUDIT-SEGREGATION/SN-047/IB-SMART-NOTE-20260930-sn047-audit-receipt-segregation.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> audit_receipt_segregation_quarantine_tampered_never_tally

**Evidence:** {"board_comment": "5927643989 \u2014 [NAYA 2][NINE-NODE VERIFY] 2026-10-01 ~01:25 PDT", "branch": "naya4/nine-node-kernel-v1 @ cf62b7617940945662d2cebba58b95597e0f74bf; tests/test_nodes/ + tests/test_kernel.py \u2192 474 passed, 0 failed", "commits_reviewed": "739d77a (HARDEN: gate_all() emits hash-
**Cousins:** none

## SN-0048 — API-Pushed Commits Never Trigger GitHub Actions — CI-Pending Forever Is a Mirage (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/CI-TRIGGER-SILENCE/SN-048/IB-SMART-NOTE-20260930-sn048-api-push-actions-silence.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> api_push_never_triggers_actions_verify_ci_evidence_yourself

**Evidence:** {"board_comment": "5928306117 \u2014 [Naya 2 \u00b7 build-loop CI-trigger finding, 2026-10-01 ~02:10 PDT]", "canary": "close + reopen of #1211 via API produced 0 runs (PR restored to open, head unchanged); draft-toggle via API silently ignored", "local_verification": "pytest 556/604/604/550/563 pass
**Cousins:** none

## SN-0049 — A Guard That Cries Wolf About First-Party Imports Gets Ignored (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/GUARD-FALSE-POSITIVES/SN-049/IB-SMART-NOTE-20260930-sn049-guard-that-cries-wolf.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> guard_false_positive_is_a_guard_defect_fix_the_world_model

**Evidence:** {"affected": ["#1211", "#1213", "#1215"], "board_comment": "5928094612 \u2014 [Naya 2 \u00b7 build-loop, 2026-10-01 ~02:10 PDT] root cause 1 of 5 repaired red checks", "documented_failure_mode": "'a guard that cries wolf about first-party imports gets ignored' \u2014 the guard's own docs named this 
**Cousins:** none

## SN-0050 — Verify the Pushed Bytes, Not the Pre-Commit Bytes (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/PUSHED-BYTES-VERIFICATION/SN-050/IB-SMART-NOTE-20260930-sn050-verify-pushed-bytes.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> assertions_must_be_possible_in_ci_context_and_evidence_runs_on_pushed_sha

**Evidence:** {"accidental_green": "passed pre-commit only because HEAD was still the base a33b33d7; pushed bytes went red while the build list claimed '525 passed'", "board_comment": "5928094612 \u2014 [Naya 2 \u00b7 build-loop, 2026-10-01 ~02:10 PDT] root cause 3 of 5 repaired red checks", "evidence_law_note": 
**Cousins:** none

## SN-0051 — Local Verification Is the Gate When the Push Path Is CI-Blind (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/CI-TRIGGER-SILENCE/SN-051/IB-SMART-NOTE-20260930-sn051-local-verification-as-gate.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> gate_evidence_moves_to_where_evidence_can_be_produced

**Evidence:** {"board_comment": "5928361378 \u2014 [Naya 2 \u00b7 build-loop CI-trigger relay, 2026-10-01 ~02:10 PDT]: 'gh-api pushes silently skip Actions, so your git-triggered CI remains the real gate signal' + 'any repair byte I push through gh-api carries local verification as its gate, not CI'", "cross_lane
**Cousins:** none

## SN-0052 — Duplicate-Seam Detection — Diff the Diffs Before the Merge List Gets Two of the Same Repair (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/MERGE-DECISION-INTEGRITY/SN-052/IB-SMART-NOTE-20260930-sn052-duplicate-seam-merge-routing.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> diff_the_diffs_one_merge_one_close_redirect

**Evidence:** {"board_comment": "5928421888 \u2014 drive-loop factual duplicate-seam notice", "byte_verification": "both PR diffs fetched live 2026-10-01 02:45 PDT tick; diff of diffs: IDENTICAL modulo 'index <sha>..<sha>' lines \u2014 one hunk, supabase/PRODUCTION-MIGRATION-LEDGER-V1.json, statement_count 19 -> 
**Cousins:** none

## SN-0054 — Relay-Race Consolidation — Own the Duplicate Artifact Openly and Patch the Trigger (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-054/IB-SMART-NOTE-20260930-sn054-relay-race-consolidation-protocol.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> relay_race_consolidate_openly_then_patch_trigger

**Evidence:** {"canonical_criterion": "better-artifact-wins regardless of seat: relay's scorecard carried the live-verified stale-base differentiator (#1209 base 507d3421 stale vs #1238 base a726a837 current main) that the thinner 7-5 scorecard lacked", "consolidation": "5929147568 (2026-10-01 10:02:25Z) \u2014 o
**Cousins:** none

## SN-0055 — Kill the Infeasible Winner — An Option You Cannot Evidence Is Not an Option (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DECISION-EFFICIENCY/SN-055/IB-SMART-NOTE-20260930-sn055-kill-the-infeasible-winner.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> kill_the_infeasible_winner_by_name_with_revival_condition

**Evidence:** {"board_comment": "#554 5929067367 (2026-10-01 09:56:53Z) \u2014 Brief 2 drift decision", "infeasibility_evidence": "Management API serves applied versions only; no SQL in workspace or repo history \u2014 searched, not assumed; fabricating it would violate the evidence law", "killed_option": "option
**Cousins:** none

## SN-0057 — Race-Window Temporal Attribution — Name Which Came First, Because a Stale Read Can Invert the Outcome (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-057/IB-SMART-NOTE-20260930-sn057-race-window-temporal-attribution.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> race_window_temporal_attribution

**Evidence:** {"correction_drive_loop": "5929340527 (Naya 4, 10:15:46Z) \u2014 named read-times vs execution time, corrected the temporal direction for the record", "execution": "#1238 reopened as draft / #1209 closed at 10:11:43Z 2026-10-01 (matching Naya 2's canonical scorecard 5929077552)", "self_correction": 
**Cousins:** none

## SN-0059 — The Clean-Main Control Run — Attribute the Failure Before You Blame the Change (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/EARNED-INTELLIGENCE/VERIFIED-EXPERIENCE/SN-059/IB-SMART-NOTE-20260930-sn059-clean-main-failure-control.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> failing_test_reproduced_on_clean_main_is_environment_failure_not_code_failure

**Evidence:** "NayaPOWER#554 comment 5930091991; branch naya/p4-consent-consumer-exact-v2 @ 1352743bb3b9bc8e7c9bc27c24bc11c5ae74a179; test_production_migration_history_baseline lineage_is_preserved_exactly fails on clean-main sparse checkout, passes 12/12 with archived paths present; PR #1242"
**Cousins:** none

## SN-0060 — The Opener Owns the Close — Supersede in a Comment, Leave His PR Open (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-060/IB-SMART-NOTE-20260930-sn060-opener-owns-close.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> lanes_never_change_state_of_artifacts_opened_under_human_directors_account

**Evidence:** "NayaPOWER#554 comment 5930091991 ('opened under Shawn's account \u2014 close is his call'); #1139 left OPEN; supersession comment 5930090020; successor draft PR #1242 @ 1352743bb3b9bc8e7c9bc27c24bc11c5ae74a179"
**Cousins:** none

## SN-0061 — Post-Merge Verification at the Pin — Branch-Green Is Not Merged-True; Prove Negatives Non-Vacuous (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-061/IB-SMART-NOTE-20260930-sn061-post-merge-verification-at-pin.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> post_merge_verification_at_pin

**Evidence:** {"board": "#554 comment 5933288839 (2026-10-01T14:14:41Z)", "merge_commit": "c3272086 confirmed in main ancestry, 101 commits behind tip (gh-api compare)", "mis_targeted_mutant": "block-level superseded-gate mutant did not fail N1; traced to edge-level exclusion (N1's attack is edge-level), document
**Cousins:** none

## SN-0062 — The Count Ledger Is Part of the Change (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/COUNT-LEDGER-STALENESS/SN-062/IB-SMART-NOTE-20260930-sn062-count-ledger-is-part-of-the-change.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> count_ledger_is_part_of_the_change

**Evidence:** {"board": "#554 comment 5933379398 (2026-10-01T14:19:39Z)", "diagnosis": "reproduced locally on exact bytes 02d65636 before repairing", "failure": "CI test job --check exit 2 \u2014 presented as regression, was stale declared count", "mechanism": "tools/regenerate_brain_index.py EXPECTED_DOMAIN_COUN
**Cousins:** none

## SN-0063 — Receipt Provenance — Binding the Ratified Hash Is Not the Shared Calculator Deciding (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-063/IB-SMART-NOTE-20260930-sn063-receipt-provenance-binding-vs-deciding.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> receipt_provenance_binding_vs_deciding

**Evidence:** {"board": ["#554 comment 5933756362 (2026-10-01T14:41:02Z)", "#554 comment 5933738728 (2026-10-01T14:40:01Z)"], "characterization": "architecture gap, not deception \u2014 the code is honest about what it does", "connect": "naya_kernel/nodes/connect_node.py:1702 computes q_proxy/v_safe_proxy from lo
**Cousins:** none

## SN-0064 — Spec Outruns Kernel — Forward-Gap Discipline at Lock (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-064/IB-SMART-NOTE-20260930-sn064-spec-outruns-kernel-forward-gaps.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> spec_outruns_kernel_forward_gap_discipline

**Evidence:** {"act_layering_gap": "A-ACT-4 binds 13 master-contract functions; kernel implements execution half only; no implementation under any name of plan_action, select_minimum_sufficient_action, define_expected_outcome, define_proof_requirements, callable observe; no spec/kernel doc states the deliberation
**Cousins:** none

## SN-0065 — Branch-Boundary Claims — Intent Stated as Existing Capability (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/PHANTOM-CITATION-CLASS/SN-065/IB-SMART-NOTE-20260930-sn065-branch-boundary-claims-intent-as-capability.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> branch_boundary_claims

**Evidence:** {"board": ["#554 comment 5934300247 (2026-10-01T15:10:39Z) \u2014 ACT re-qualification @ #1224 head a71fbfe1, delta A-ACT-4..9 (+92 lines, pure append)"], "overclaim": "A-ACT-5 'the kernel's decide() edge trace is the runtime counter's source of truth' \u2014 decide()/_edge_trace() exist only on #12
**Cousins:** none

## SN-0066 — Red Before Green — Publish the Failing Case on the Frozen SHA (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-066/IB-SMART-NOTE-20260930-sn066-red-before-green-failing-case-first.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> red_before_green_failing_case_first

**Evidence:** {"board": ["PR #1216 comment 5934329483 (2026-10-01T15:12:10Z) \u2014 Naya-4 RED"], "builder_contract": "turn it green by wiring, or fence as PROVISIONAL with the test staying red \u2014 never fake it green", "directive": "Master Execution Directive 2026-10-01 ~08:07 PDT (#554 comment 5934257584) \u
**Cousins:** none

## SN-0067 — The Git-Grep Pathspec Footgun — Revision After `--` Is a Path, Not a Revision, and Your Absence Proof Never Ran (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-067/IB-SMART-NOTE-20260930-sn067-git-grep-pathspec-footgun.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["revision before --, paths after --; anything after -- is a pathspec", "never truncate when proving absence", "absence claims are lexical findings, never ontological proof", "correct by appending: retain earlier evidence, withdraw the conclusion, show the corrected run"]

**Evidence:** {"compounding_defect": "truncated output (Select-Object -First) cannot establish absence", "correct_command": "git grep -n -E 'evaluate_candidates|gate_candidate|independent_recompute|value_calculus' origin/main -- '*.py' '*.ts' -> exit 0, 34 lines, all definitions + own test", "correction": "#554 c
**Cousins:** none

## SN-0068 — Read the Canonical Contract Before Proposing a Competing Format — Withdraw the Competing Format, Answer Under the Contract (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY/SN-068/IB-SMART-NOTE-20260930-sn068-canonical-contract-before-competing-format.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["read the canonical artifact before proposing any contract/format/convention", "withdraw competing formats explicitly on the board; never let two formats coexist pending review", "scope lane agreement as implementation under the existing contract, not new governance", "competing-format proposal without reading the canonical artifact is a governance defect, not an engineering contribution"]

**Evidence:** {"agreement_discipline": "#554 comment 5934741237 \u2014 'implementation agreement under the existing contract \u2014 not new governance'", "proposal": "#554 comment 5934427074 (Naya 2: naya-receipt-contract/1)", "right_frame": "#554 comment 5934391765 (Naya 4 seam question: kernel projects receipts
**Cousins:** none

## SN-0069 — Bindings at the Observing Layer — Assign Cryptographic Responsibility to Whoever Sees the Bytes; Never Invent What the Producer Already Carries (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTERFACE-OWNERSHIP/SN-069/IB-SMART-NOTE-20260930-sn069-bindings-at-the-observing-layer.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["assign each binding to the layer that observes the bound bytes", "consumer recomputes independently and rejects on mismatch \u2014 verification, not invention", "never synthesize data the producer already carries: map, don't mint", "ground who-computes-what in source at the exact SHA before agreeing", "bind new fields before the receipt's own integrity hash", "seam agreements stay under the canonical contract \u2014 implementation agreement, not new governance (SN-068)"]

**Evidence:** {"agreement": "#554 comment 5934741237 (2026-10-01T15:33:13Z) \u2014 answers from kernel source at a78227d8: receipt carries receipt_id, decision_id, verdict, gates, edge_trace, issued_at, receipt_hash; NO inputs_hash, NO executed_at", "executed_at_split": "adapter maps kernel issued_at \u2014 never
**Cousins:** none

## SN-0070 — Retry-on-Conflict Is Not Idempotency — Uniqueness Retries Prove One Allocation, Not One Execution (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-070/IB-SMART-NOTE-20260930-sn070-retry-not-idempotency.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["name the four idempotency conjuncts explicitly before crediting any retry mechanism", "map each conjunct to exact source at the frozen SHA \u2014 lines, mechanism, test", "allocation-uniqueness retry covers conjunct-zero only; file under uniqueness, never idempotency", "keep the gap major until all four are proven against exact-head source", "borrowed credit is inflated credit \u2014 narrow the claim, don't transfer the mechanism's strength"]

**Evidence:** {"board": "#554 comment 5935190080 (2026-10-01T15:55:08Z) \u2014 CODA 2 feedback, correction 3 'Revision allocation retry \u2260 idempotency'", "four_conjuncts": ["same logical request executes once", "duplicate retries reread the original result", "same idempotency key + changed payload is rejected
**Cousins:** none

## SN-0071 — Never Collapse the Four LEARN Dimensions — Epistemic State, Adoption, Lifecycle, and Transfer Maturity Are Separate Verdicts (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/EARNED-INTELLIGENCE/LEARN-MATURITY-DIMENSIONS/SN-071/IB-SMART-NOTE-20260930-sn071-learn-dimension-separation.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["issue four separate verdicts per learning: epistemic, adoption, lifecycle, transfer maturity", "each column fills only from evidence answering that question \u2014 no cross-column leakage", "'supported but not adopted' and 'adopted but superseded' are normal speakable states", "retract per-column, not per-verdict", "epistemic column uses the graded scale; the binary PASS/FAIL is retired for whole learnings"]

**Evidence:** {"board": "#554 comment 5935266261 (2026-10-01T15:59:16Z) \u2014 CODA 3 feedback, point 3: separated epistemic state from adoption/lifecycle/transfer maturity", "design_anchor": "Ultimate LEARN design: contradictions preserved never overwritten; rollback = supersession never deletion; mandatory auto
**Cousins:** none

## SN-0073 — Invocation ≠ Consumption ≠ Enforcement — Proving the Runtime USES the Canonical Engine (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-073/IB-SMART-NOTE-20260930-sn073-invocation-consumption-enforcement.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["claiming the runtime USES a canonical component requires three independent proofs: INVOCATION, CONSUMPTION, ENFORCEMENT", "prove consumption by documented-field substitution \u2014 the downstream result must change; a passing spy is a red flag", "prove enforcement by violating inputs with legible refusal inside the receipt mechanism", "receipts must carry every recomputation field; persistence completeness is a conformance criterion", "a config-hash pin answers 'is the intended code loaded', never 'does the outcome depend on it'", "distinguish gate errors from assertion failures before diagnosing (CRLF/class discipline)"]

**Evidence:** {"board": "#554 comment 5935889561 (2026-10-01T16:34:29Z) \u2014 [CODA 1] SIGN-OUT, Value Calculus conformance lane", "consumption_failure": "real evaluator wrapped, one documented consumed field substituted \u2014 runtime result unchanged; spy alone passes", "crlf_corollary": "core.autocrlf=true ->
**Cousins:** none

## SN-0075 — Committed Holds Are Constraints — When a Higher Authority Overrides, Log the Override, Never Silently Break the Commitment (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COMMITMENT-INTEGRITY/SN-075/IB-SMART-NOTE-20260930-sn075-committed-hold-override-logging.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["a board commitment (hold, next action, waiting-on state) is a coordination constraint other lanes plan against \u2014 weight of a contract, not a note-to-self", "when higher authority overrides: obey, then declare the override on the same board", "the declaration restates the commitment, names the overriding authority, and states what happens to the waiting party", "never let another lane discover a broken commitment from a diff, head move, or third party \u2014 discovery-without-announcement is the trust damage", "the override log doubles as your receipt \u2014 SN-042 explicit-supersession applied to coordination commitments"]

**Evidence:** {"announced_outcome": "Coda 2/3's verification work acknowledged as continuing in parallel \u2014 waiting party not orphaned", "board": "#554 comment 5935875734 (2026-10-01T16:33:43Z) \u2014 'Hold status: my torch committed to holding move 2 until Coda 2's verification of 43d5d6e4 landed. The direct
**Cousins:** none

## SN-0077 — False-Green Restoration — Compute the Report from the Consuming State, Not the Reconstructed Local (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-077/IB-SMART-NOTE-20260930-sn077-false-green-restoration.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["install-then-report: acceptance signals (counts, hashes, receipts, verdicts) are computed from the consuming object's state AFTER installation, never from the producer's intermediate", "flag `fresh = X(); report(fresh); return` without assignment onto the delivered object as defect-shaped even when tests are green", "the reproducer asserts on the successor's own read path after the call returns \u2014 the function's report is the suspect, not the witness", "cold-successor continuity = 'this object now carries the state and can serve it', not 'state was reconstructed somewhere'"]

**Evidence:** {"board": "#554 comment 5936275514 (2026-10-01T16:55:50Z) \u2014 Coda 4/Big Pickle feedback, 'WHERE YOU ARE WINNING' \u00a71: the false-green proof class; CS-01 confirmed still present at current #1216 head bf63549c2760f1ca33e7fb36bc35e8ebb2c28542", "defect": "know_node.py cold_reconstruct() reconst
**Cousins:** none

## SN-0078 — Merge Adding BRAIN/ Files Must Regen the Index AND Deliberately Bump the Count Ledger — Bake It into Merge Checklists (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/COUNT-LEDGER-STALENESS/SN-078/IB-SMART-NOTE-20260930-sn078-merge-checklist-regen-and-count-bump.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["any merge adding a BRAIN/ file must regen the index AND deliberately bump EXPECTED_DOMAIN_COUNTS \u2014 both are part of the change", "green-tests/red-check means the merge was incomplete \u2014 trust the check for index completeness", "the tool's own --check failure message prescribes the repair \u2014 never improvise a different fix", "bake regen+bump into the merge checklist as a named item \u2014 a rule in one lane's memory will be re-broken by the next lane", "repair and merge authorization stay separated \u2014 the repair PR does not self-merge"]

**Evidence:** {"board": "#554 comment 5936359525 (2026-10-01T17:00:26Z) \u2014 Naya 2 brain-build loop, battery on new main tip 42c8f594", "extends": "SN-062 (count ledger is part of the change \u2014 draft-branch instance); this is the recurrence through the merge path onto main itself", "green_suite": "pytest 5
**Cousins:** none

## SN-0080 — Frozen-Evidence Retirement — Retire Explicitly, Re-Freeze, Never Mutate the Freeze (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/EVIDENCE-IMMUTABILITY/SN-080/IB-SMART-NOTE-20260930-sn080-frozen-evidence-retirement.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["the freezer refuses overwrite \u2014 immutability is enforced, not promised", "defective frozen packages are retired by explicit history-visible action and re-frozen with a new seal \u2014 never edited or silently replaced", "the retirement record is part of the evidence; a too-clean history on iterated work is a signal worth inspecting", "a valid seal binds content, it does not bless it \u2014 verify what was frozen, not just that it is frozen"]

**Evidence:** {"board": "#554 comment 5936949498 (2026-10-01T17:35:34Z) \u2014 Naya 4 P4/P5: trial package cbbeadd5 (seal 395f32c8) frozen from code lacking inputs_hash; removed by explicit hand action 11f4ac44; re-frozen; 'The removal is in the commit history; nothing is hidden'", "final_seal": "e451e95ad6947f5c
**Cousins:** none

## SN-0081 — Containment Never Degrades to Fit the Platform — Refuse Before Mutation (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/CONTAINMENT-INTEGRITY/SN-081/IB-SMART-NOTE-20260930-sn081-containment-never-degrades-platform.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["containment is a conjunct, not a gradient \u2014 all required primitives present or nothing mutates", "a missing platform primitive ends the mutation lane; ADMISSIBLE-then-refuse is a correct terminal state", "never try/except a missing containment primitive into a weaker fallback \u2014 port the guarantees, not an approximation", "the refusal must record exactly which primitive was missing and that no guard was weakened; the platform note is load-bearing"]

**Evidence:** {"board": "#554 comment 5936937521 (2026-10-01T17:34:47Z) \u2014 cold-boot reconciliation sign-out: frozen specimen bf63549c re-run on Windows reaches REAL LAW ADMISSIBLE, then intentionally refuses before mutation because os.O_NOFOLLOW is unavailable; 'no containment guard was weakened'", "missing_
**Cousins:** none

## SN-0083 — Retain the UNKNOWN With Its Missing Evidence Named (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-083/IB-SMART-NOTE-20260930-sn083-retain-unknown-with-named-missing-evidence.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["resolve every resolvable leg from evidence before concluding \u2014 never silently choose one report", "retain each unresolvable leg as a terminal UNKNOWN naming the precise missing evidence and its owner", "never author canonical changes against an unresolved deployed target", "a retained UNKNOWN with named missing evidence is completed diligence; an unnamed one is a shrug"]

**Evidence:** {"board": "#554 comment 5937420364 (2026-10-01T18:03:07Z) \u2014 Naya 2 P2 write-authority conflict", "evidence_owner": "whoever holds the production read credential", "missing_evidence": "read-only pg_get_functiondef() + information_schema.routine_privileges against production", "repair_decision": 
**Cousins:** none

## SN-0084 — A Version Label Is Not Proof of Evaluation — Stash the Invented-Value Experiment (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-084/IB-SMART-NOTE-20260930-sn084-version-label-is-not-evaluation-proof.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["a version label names the config, never the computation \u2014 evaluation must be shown, not stamped", "invented-input experiments are stashed wholesale, not salvaged in place", "rebuild only through the interface owner with exact contract questions; 'does not exist yet' is a complete answer", "keep authorization, commitment, config identity, evaluation, and outcome as distinct fields"]

**Evidence:** {"board": "#554 comment 5937513949 (2026-10-01T18:08:13Z) \u2014 Naya 4 P4 decision-semantics experiment held back and stashed (invented quality/confidence/benefit/harm/cost/risk values + hardcoded bounds, not proven from canonical Smart Door declaration)", "rebuild_route": "interface owner Coda 1 \
**Cousins:** none

## SN-0086 — Qualify Only the Fetchable Subject — Withdraw References to Unpushed Local Commits (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-086/IB-SMART-NOTE-20260930-sn086-qualify-only-the-fetchable-subject.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["never issue a qualification request against an unfetchable reference (unpushed local commit)", "freeze the subject: candidate SHA + branch + byte digests of every file the proof depends on", "bind the verdict to the SHA, never the branch tip", "withdraw an unfetchable reference explicitly and re-issue; do not edit in place", "attach the producer's own clean-run proof to the same frozen subject"]

**Evidence:** {"board": "#554 comment 5937882252 (2026-10-01T18:28:10Z) \u2014 [NAYA 2][P6-FROZEN] supersedes #554 comment 5937604904 (2026-10-01T18:13:00Z): unpushed local commit 7f21427aa reference withdrawn; frozen subject = candidate SHA c5402f3f16cf738150f9689becfa9ecfc3bb0c5d + branch naya2/persistence-inte
**Cousins:** none

## SN-0087 — Proof Environments Must Be Reset, Not Reused — Prior-Run Pollution Masquerades as Proof Failure (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/PROOF-ENVIRONMENT-ISOLATION/SN-087/IB-SMART-NOTE-20260930-sn087-proof-environments-reset-not-reused.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["the environment is part of the proof \u2014 reset (truncate/recreate/provision fresh) before qualification, never reuse dirty", "record the reset in the proof report so the verifier can distinguish subject failure from pollution", "on a failing run, check environment cleanliness before touching the subject", "never fix the subject to accommodate dirty state", "prefer fresh provisioning (disposable DB/checkout) over remembering to reset"]

**Evidence:** {"board": "#554 comment 5937882252 (2026-10-01T18:28:10Z) \u2014 P6 producer proof: database naya_isolated_rt polluted by prior runs (5 leftover rows) caused 4 false failures on first attempt (10/14); after truncate, 14/14 on the identical frozen specimen c5402f3f"}
**Cousins:** none

## SN-0088 — Fixture Substitution Voids Integration Claims — the Default Composition Is the Integration Seam (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-088/IB-SMART-NOTE-20260930-sn088-fixture-substitution-voids-integration-claims.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["an integration test that substitutes fixture behavior at a claimed seam proves nothing about that seam", "the integrated acceptance proof must start at the default constructor path: plain Kernel(), no node replacement, no monkeypatch, no fixture flags", "fixture-substituted tests must be explicitly reclassified as fixture-only evidence, never cited for organism claims", "state per-seam and composition verdicts separately and honestly (node VERIFIED + composition UNPROVEN is a reportable state)", "close the gap with the smallest real repair (wire the canonical resolver at composition); never widen the fixture"]

**Evidence:** {"board": "#554 comment 5938628319 (2026-10-01T19:09:47Z) \u2014 test_kernel_nine_node.py replaces real LEARN with LearnNode(allow_fixture_intake=True); actual Kernel() constructs bare LearnNode(); runtime resolver not wired by default; verdict recorded: INDIVIDUAL LEARN INTAKE SEAM = VERIFIED at 55
**Cousins:** none

## SN-0089 — Publish Your Own Number, Never Adopt the Builder's — Parent Comparison Makes an Unfamiliar Result Interpretable (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-089/IB-SMART-NOTE-20260930-sn089-publish-your-own-number.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["never adopt the builder's counts \u2014 the verdict is independent only if the measurement is yours", "rerun from your own clean checkout with none of your tests present in the tree", "when your number disagrees, make it interpretable with a parent comparison under identical conditions", "'introduced zero new failures' must be measured (parent vs child delta), never asserted", "disclose irreproducible reporting discrepancies as open items; do not smooth them into the verdict"]

**Evidence:** {"board": "#554 comment 5938588330 (2026-10-01T19:07:39Z) \u2014 Coda 1 independent requalification: builder reported 1127/0 (5938453381); her clean checkout returned 31 failed / 1091 passed / 3 skipped / 5 errors; parent 01797efe measured identically at 33 / 1070 / 3 / 5; verdict: fixed 2, added 21
**Cousins:** none

## SN-0092 — Design Qualification Tests That Self-Invalidate — and Name the Consequence Class Honestly (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-092/IB-SMART-NOTE-20260930-sn092-self-invalidating-tests.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["classify the consequence class before the headline: composition gap, regression, security defect, blocked frontier \u2014 a working fail-closed gate is a gap, never a defect", "write gap tests as presence-assertions that fail the moment the gap closes, forcing requalification instead of stale green", "ship the future acceptance criteria with the finding (genuine accepted; forged/unknown/tampered/wrong-subject refused)", "specify the smallest fix, do not implement it when you are the verifier", "maintain a 'limits I will not paper over' section: threat-model boundaries and scope boundaries \u2014 state it, don't imply it away", "never present a component PASS as integration proof"]

**Evidence:** {"board": "#554 comment 5939132042 (2026-10-01T19:38:44Z) \u2014 Coda 1 default-Kernel() composition finding at 710776700c48069bf91a06d1adb4900cb61154c7: Kernel().nodes LEARN._verify_resolver=None, _allow_fixture_intake=False, ingest_verify_receipt->VERIFY_ORIGIN_UNESTABLISHED; no resolver/reference
**Cousins:** none

## SN-0093 — Trace the Whole Chain, Stop at the First Exact Failing Handoff — Never Invent Past a Semantic Gap (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-093/IB-SMART-NOTE-20260930-sn093-first-failing-handoff.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["publish the e2e proof as a per-handoff trace in canonical order; grade only handoffs actually driven", "stop at the first exact failing handoff; record the exact error and the evidence-established root cause", "classify the gap: wiring gaps close, semantic gaps stop-and-name \u2014 never invent across a semantic boundary", "mark all downstream steps BLOCKED / NOT CLAIMED; explicitly disclaim what completion would have required inventing", "scope partial proofs per seam: a proven intake seam says nothing about the extraction seam", "land adjacent hygiene the trace reveals (C3 compare-field additions) in the same change"]

**Evidence:** {"board": "#554 comment 5939167533 (2026-10-01T19:40:59Z) \u2014 Naya 4 nine-organ composition at 384df8755115eb27f6822eac8a447ebeee04ba50: kernel.py wires LearnNode(verify_resolver=LearnNode.reference_resolver(verify_node)); learn_node.py adds receipt_hash to C3 compare fields; 6 new tests; nine-or
**Cousins:** none

## SN-0097 — Fail Loud, Attribute First — A Harness That Blames the Wrong Party Is Worse Than Silence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION/SN-097/IB-SMART-NOTE-20260930-sn097-fail-loud-attribute-first.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["harness death must emit a named environment fatal (exit code distinct from test failure), never per-case FAILs for un-run cases", "attribute the failure before reporting it: name which part of the pipeline owns it \u2014 harness, product, or platform", "ship a self-invalidating regression test with every harness-attribution fix", "verify check claims against live check-runs; separate required-check signal from platform preview noise by name", "a verdict for an un-run case is fabricated evidence, not a conservative report"]

**Evidence:** {"board": "#554 comment 5939794076 (2026-10-01): brain-drive 13:07 PDT run opens PR #1263 (brain-drive/adversarial-harness-fail-loud, head cfe68fa4): dead scratch clone aborts with named FATAL exit 3 (environment failure) instead of misleading per-case FAILs blaming the generator \u2014 the exact 20
**Cousins:** none

## SN-0098 — Investigate the Other Platform Before Dismissing It — Linux-Only Thinking Falsified Live (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/CROSS-PLATFORM-LOCALE/SN-098/IB-SMART-NOTE-20260930-sn098-investigate-before-dismiss.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["a failure that doesn't reproduce on your platform is an un-investigated platform delta, not a disproven failure", "'environment' is a hypothesis that names the delta (locale, autocrlf, encoding) \u2014 then gets tested by reproducing the mechanism", "reproduce down to the byte: exact error string, exact offending byte, both decode paths demonstrated", "fix at the source: explicit encoding= on every text read; .gitattributes declaring line endings \u2014 undeclared repos hold hashes hostage to checker config", "the fix is done when green on THEIR platform \u2014 hand back a requalification target for the failing OS", "investigate across lanes, modify inside your own \u2014 offer the patch, never push to the other lane's branch", "own the wrong dismissal on the record \u2014 the correction is part of the receipt"]

**Evidence:** {"board": "#554 comment 5940022241 (2026-10-01): Naya 4 implements Coda 1's Option A at 2b7e6d62 (parent 5758daef, PR #1216 draft) and addresses both defect roots \u2014 encoding: open(..., encoding='utf-8') on the text-mode read in test_act_node.py; autocrlf: traced to missing .gitattributes \u2014
**Cousins:** none

## SN-0100 — SMART NOTE — A Mechanical Change Is Still a Change (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/VERDICT-SHA-BINDING/SN-100/IB-SMART-NOTE-20260930-sn100-bulk-sweep-verdict-sha-binding.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> every commit voids every prior verdict; re-prove at the new SHA

**Evidence:** ["#554 comment 5940389915", "#554 comment 5940612880", "#554 comment 5940155081", "#554 comment 5940185514"]
**Cousins:** none

## SN-0101 — SMART NOTE — Platform Identity Semantics (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/PLATFORM-IDENTITY-SEMANTICS/SN-101/IB-SMART-NOTE-20260930-sn101-platform-identity-semantics.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> normalize-then-compare by the platform's canonicalization semantics, never by the language default

**Evidence:** ["#554 comment 5940374630"]
**Cousins:** none

## SN-0102 — SMART NOTE — The Import-Still-Red Experiment (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-102/IB-SMART-NOTE-20260930-sn102-import-still-red-experiment.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> import-still-red ⇒ gap is in the host; stop patching the package, build the host seam

**Evidence:** ["#554 comment 5940410766"]
**Cousins:** none

## SN-0103 — SMART NOTE — Prove Memory Across the Process-Death Boundary (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0103/IB-SMART-NOTE-20260930-sn0103-prove-memory-across-the-process-death-boundary.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **The acceptance bar for persistence is the recall, not the write.** Four conjuncts, all required: (a) write to durable store; (b) kill the writing process (handles closed — no warm caches); (c) fresh process reads back and *recomputes* seal, hash, and `inputs_hash` from submitted `inputs_state` — recompute, never re-display; (d) owner isolation: wrong owner sees zero rows.
2. **Honest projection labels are part of the proof.** The receipt projected through the v3 seam landed as `UNVERIFIED` 

**Evidence:** ["#554 comment 5940852947", "#554 comment 5940799847"]
**Cousins:** none

## SN-0104 — SMART NOTE — Design-Weight Decisions Are Not Settled in the Relay (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-0104/IB-SMART-NOTE-20260930-sn0104-design-weight-decisions-not-settled-in-relay.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> a relay that surfaces a design-weight gap: name it, route it to the owning seat, keep it visible, invent nothing interim

**Evidence:** ["#554 comment 5940976053"]
**Cousins:** none

## SN-0105 — SMART NOTE — Skip-with-Reason Is Not a Defect Blanket (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/SKIP-DISCIPLINE/SN-0105/IB-SMART-NOTE-20260930-sn0105-skip-with-reason-is-not-a-defect-blanket.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **The unit of skipping is the failure, not the run.** A skip verdict attaches to one failure with one reason. "21 `O_NOFOLLOW` — correct fail-closed, unsupported on Windows, skip with reason" is 21 earned verdicts, not a run-level waiver. The reason must say what the failure *is* (unsupported ⇒ "unsupported," never "broken").
2. **The blanket test:** if you cannot name, for each failure, which of the four classes it belongs to — unsupported-by-platform (skip with reason) / genuine defect (fix

**Evidence:** ["#554 comment 5940654521", "#554 comment 5940665922"]
**Cousins:** none

## SN-0106 — SMART NOTE — The Name Must Say What the Thing Is (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY/SN-0106/IB-SMART-NOTE-20260930-sn0106-the-name-must-say-what-the-thing-is.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **Names are the most-read documentation.** A filename, route, or component name is read more times than its source — it is the artifact's first claim about itself. A false name is a false claim, and it belongs in the same family as phantom citations (SN-027/SN-065): assertion without reality.
2. **Two independent discoveries = a trap, not a coincidence.** When two lanes trip over the same misnomer in the same hour, the name is systematically misleading, not subjectively confusing. Trips-per-l

**Evidence:** ["#554 comment 5941654799", "#554 comment 5941663299", "PR #1272", "PR #1273"]
**Cousins:** none

## SN-0107 — SMART NOTE — The Scorekeeper Must Be Independent; Scores Must Be Allowed to Fall (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0107/IB-SMART-NOTE-20260930-sn0107-score-keeper-independent-scores-must-fall.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **Separate the builder from the keeper.** The seat that builds the Hub must not be the seat that scores it. Self-scoring is self-certification (SN-073 family) — and like self-certification, it always passes.
2. **Scores must be allowed to fall.** This is the load-bearing rule. If the scorecard only ratchets upward, every regression gets re-described instead of recorded, and the number measures the project's optimism, not its quality.
3. **Publish the honest baseline first.** 5.8/10 with Visua

**Evidence:** ["#554 comment 5941654799"]
**Cousins:** none

## SN-0108 — SMART NOTE — One Change, One PR: Deconflict Duplicate Ownership Before Executing (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-0108/IB-SMART-NOTE-20260930-sn0108-one-change-one-pr-duplicate-ownership-collision.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> one change, one PR — scan the board for in-flight execution of the same change before executing; on collision, announce openly and stand down or consolidate; never let both ride to the merge gate

**Evidence:** ["#554 comment 5941654799", "#554 comment 5941663299", "PR #1272", "PR #1273"]
**Cousins:** none

## SN-0109 — SMART NOTE — Everything on 554: The Board Is the Alignment Mechanism (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/BOARD-ALIGNMENT/SN-0109/IB-SMART-NOTE-20260930-sn0109-everything-on-554-standing-board-protocol.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **The board is the mechanism, not the archive.** Shawn's directive (5942150726) turns #554 into the team's alignment layer: the protocol is start → finish → find → propose, posted at each transition. A cold successor reads the board and knows who is doing what, what landed, and where the open questions live.
2. **The finding law has teeth.** The not-right rule (5942076650) operationalizes "finding": SEE NOT-RIGHT → CAPTURE → EVIDENCE → #554 → CLASSIFY/ROUTE → FIX/TRACK → VERIFY → CLOSE/HANDOF

**Evidence:** ["#554 comment 5942150726", "#554 comment 5942076650", "#554 comment 5942139930"]
**Cousins:** none

## SN-0110 — SMART NOTE — One Intelligence, Three Projections: HUMAN / AI / MACHINE (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/KNOWLEDGE-PROJECTION/SN-0110/IB-SMART-NOTE-20260930-sn0110-one-intelligence-three-projections.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **One intelligence, many representations — never duplicate truth.** The three projections (HUMAN / AI / MACHINE) are all derived from the canonical docs (`HUB/PROJECT-INTELLIGENCE.md` + `HUB/DESIGN-CONTRACT.md`); canonical wins on conflict. A projection is a view. The moment a projection starts being edited independently of the canonical, it has forked, and forks are how truth dies.
2. **Designer programming is the AI projection's job.** The AI projection encodes *taste as law* — color math, 

**Evidence:** ["#554 comment 5941910955", "#554 comment 5942028964", "PR #1276 (commit cd1597f7)"]
**Cousins:** none

## SN-0111 — SMART NOTE — The Seal Proves Consistency, Not Authorship (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0111/IB-SMART-NOTE-20260930-sn0111-seal-proves-consistency-not-authorship.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **Name the distinction every time you touch a seal.** Consistency (not altered after close) and authorship (the submitter really is the claimed owner) are two different claims proved by two different mechanisms. An unkeyed seal proves the first and says nothing about the second. Collapse them and every "verified" badge on the system over-claims.
2. **Allowlist coverage must follow the readers, not just the writers.** `owner_id` is allowlisted (C3) so a presented receipt cannot alter it withou

**Evidence:** ["#554 comment 5942032703", "commit bee101b47 (coda1/owner-provenance-audit-8c027928)", "6 passed"]
**Cousins:** none

## SN-0112 — SMART NOTE — Pin What You Consume, Not Just What You Verify — Post-Intake Aliasing (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0112/IB-SMART-NOTE-20260930-sn0112-pin-what-you-consume-not-just-what-you-verify.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **A boundary verdict is not custody of the state.** The C1–C6 intake seam was proven against 48 systematic forgery attacks (20/20 battery + 28 new probes, all fail-closed). That proves the door. It does not prove that what LEARN consumes later is what passed the door — because `n._verify_receipts[rid] is v._receipts[rid]`: the consumer holds an alias, not a copy.
2. **Name the bar honestly for each threat layer.** Intake forgery requires the attacker to replicate VERIFY's full emission. Post-

**Evidence:** ["#554 comment 5942456354", "head 1e7fd25c3ef430fc6fa41e41d3362a655cded8dc (PR #1216)", "probe script probe-seam-naya4-20261001.py", "goal nayapower-self-build-loop hidden_files selfbuild-loop-2026-10-01-1605-learn-seam.md"]
**Cousins:** none

## SN-0113 — SMART NOTE — Freeze the Scale on an Ambiguous Director Number (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-0113/IB-SMART-NOTE-20260930-sn0113-freeze-the-scale-on-an-ambiguous-director-number.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **An ambiguous authority number is a question, not a task.** When the recorded number (17–18px / 16px floor) conflicts with your shipped value (15px / 11px floor) and the original directive was qualitative ("generous text"), you do not have a task — you have a question. Treat it as one.
2. **Name the conflict exactly.** Both numbers, where each was recorded, and why they disagree. The question that got asked here was exemplary: exact values, exact stakes ("meaning my 15px undershoots and the 

**Evidence:** ["#554 comment 5942338926", "PR #1288 (closed as superseded)", "#554 comment 5942259151 (recorded number)", "PR #1278 (shipped value)"]
**Cousins:** none

## SN-0114 — SMART NOTE — Proposed Is Not Canonical — Until Ruled (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0114/IB-SMART-NOTE-20260930-sn0114-proposed-is-not-canonical-until-ruled.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> canonical sets grow by deliberate promotion, never by implementation drift

**Evidence:** ["#554 comment 5942213324", "#554 comment 5942413426", "PR #1283 (room reconciliation, candidate)", "PR #1278 (renders 13, runtime.js ROOMS[13])"]
**Cousins:** none

## SN-0115 — SMART NOTE — Three-Layer Collision Registry: Board, PR Heads, Commit Graph (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0115/IB-SMART-NOTE-20260930-sn0115-three-layer-collision-registry.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **Resolve numbering disputes by creation-time chronology, never announcement order.** Commit timestamps and PR creation times are the evidence; board announcements are advertising. The SN-103–106 collision was settled in one line of timestamps — no debate, no escalation.
2. **A registry that misses a claim is defective; a defect that recurs three times must be owned and repaired, not flagged a fourth time.** The 17:15, 18:45, and 23:15 ticks all flagged the same scan defect (her relay's board

**Evidence:** ["#554 comment 5942646112", "#554 comment 5942508986 (collision flag with chronology)", "#1229 staging commits 456d11d1/23540141/f91f9e5e/81797cc7"]
**Cousins:** none

## SN-0116 — SMART NOTE — The Owner Makes the Canon Call: Rehome, Don't Delete; an Owner Call Is Not the Lock (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-0116/IB-SMART-NOTE-20260930-sn0116-owner-makes-the-canon-call.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **The owning lane makes the canon call — with an explicit, board-visible scorecard.** "Weighed it, and here's my call as the #1278 owner" — three stated reasons, posted on #554. Ownership plus a decision receipt is what turns a disagreement into a position. Without the scorecard it would be decree; without ownership it would be advice.
2. **Rehome the losing work to a specified place; never delete built intelligence.** Smart Notes → capture-everywhere (capture composer). System → Settings → S

**Evidence:** ["#554 comment 5942667039", "#554 comment 5942794224", "#554 comment 5942530103 (PR #1291 closure comment 5942528408)"]
**Cousins:** none

## SN-0118 — SMART NOTE — A Crash Is Not a Verdict: Verifiers Must Fail Closed, Never KeyError (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0118/IB-SMART-NOTE-20260930-sn0118-verifier-fail-closed-never-keyerror.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **A crash is not a verdict.** `independent_recompute()` hard-keyed `receipt["baseline_id"]` while runtime-persisted receipts carry `baseline_candidate_id` — the verifier raised a bare `KeyError` on real runtime output. The evidence law's independent check must never crash on admissible input: an exception is a missing verdict, not a verdict. When your proof machinery can crash, your proof claim is conditional on the input being shaped the way you wrote it — which is exactly what the independe

**Evidence:** ["#554 comment 5943060681"]
**Cousins:** none

## SN-0119 — SMART NOTE — Lift the Frozen Concept Verbatim: Invented Values Are Concept Drift; Flag Inherited Warts for the Director (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0119/IB-SMART-NOTE-20260930-sn0119-lift-frozen-concept-verbatim.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> 1. **Lift the frozen concept verbatim — never invent mappings.** The Today rebuild assigned Today a sapphire/blue mapping that the frozen concept never contained; the concept's code says `#d86cff`. An invented value during a rebuild is concept drift, not interpretation — it silently redefines canon while claiming fidelity. The fix pattern is mechanical: open the frozen concept's code, copy the literal values, verify byte-for-byte.
2. **The same hand wrote both artifacts — audit your spec when yo

**Evidence:** ["#554 comment 5942806991", "PR #1294 (BD-1 registry fix commit)"]
**Cousins:** none

## SN-0120 — SMART NOTE — Score Where the Builder Is Blind: Split-Axis Peer Review (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-0120/IB-SMART-NOTE-20260930-sn0120-blind-axis-peer-review.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> the builder names their blind axis out loud and assigns it to the lane with the strongest demonstrated judgment on that axis; the peer scores only that axis; the builder self-scores the rest; every round re-pins to a new commit; honesty is explicitly licensed in the request

**Evidence:** ["#554 comment 5943343877", "#554 comment 5943369851"]
**Cousins:** none

## SN-0121 — SMART NOTE — The Verifier Names Its Boundary (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0121/IB-SMART-NOTE-20260930-sn0121-verifier-names-its-boundary.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> every independent verification report states its coverage boundary explicitly — what was checked and what remains unverified or someone else's claim; a partial check without a named bound is silently overclaimed as a full check

**Evidence:** ["#554 comment 5943580968"]
**Cousins:** none

## SN-0122 — SMART NOTE — Re-Read the Spec When Your Numbers Diverge (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0122/IB-SMART-NOTE-20260930-sn0122-reread-spec-when-numbers-diverge.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> when your artifact's counts/labels/structures diverge from canonical numbers, re-read the canonical document itself before defending anything from memory; retire each invented element by name; record genuine disagreement explicitly rather than bending the spec

**Evidence:** ["#554 comment 5943536247"]
**Cousins:** none

## SN-0123 — SMART NOTE — The Director Is Never Your QA: The Burden-Transfer Loop (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-0123/IB-SMART-NOTE-20260930-sn0123-director-is-never-your-qa.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> the builder carries the full QA loop — inventory the whole relevant app, self-score honestly, fix, independently re-score, continue to near-perfect; the director receives finished loops and decisions, never unfinished pieces to QA

**Evidence:** ["#554 comment 5943427151", "#554 comment 5943578908"]
**Cousins:** none

## SN-0124 — SMART NOTE — The Hub Is the Screen, Not the Camera: The Output Law (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/KNOWLEDGE-PROJECTION/SN-0124/IB-SMART-NOTE-20260930-sn0124-hub-is-the-output-law.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> the Hub is the visual projection OF intelligence — output, not the canonical input; no input surface of any kind in Hub chrome, ever

**Evidence:** ["#554 comment 5943750296", "#554 comment 5943959388", "#554 comment 5943922769", "PR #1300", "PR #1290"]
**Cousins:** none

## SN-0125 — SMART NOTE — A Push Receipt Is Not Proof of Contents: Verify the Tree (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0125/IB-SMART-NOTE-20260930-sn0125-verify-the-tree-after-push.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> a push receipt is not proof of contents — after every push, verify the remote tree via the API (file by file against the expected artifact list) at the resulting commit before announcing anything

**Evidence:** ["#554 comment 5943984072", "#554 comment 5943868719 (the superseded claim)"]
**Cousins:** none

## SN-0126 — SMART NOTE — The Shawn Bar: No Tradeoffs (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/PUBLIC-PROMISE-BOUNDARY/SN-0126/IB-SMART-NOTE-20260930-sn0126-the-shawn-bar-no-tradeoffs.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> function and presentation are both 10/10 targets; neither is negotiable; one never compensates for the other; no lane presents work as finished while either axis is below the bar

**Evidence:** ["#554 comment 5943988322"]
**Cousins:** none

## SN-0128 — Verify the Repair at the Merge Tip: Merge-Base Drift Defeats Correct Repairs (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/COUNT-LEDGER-STALENESS/SN-0128/IB-SMART-NOTE-20260930-sn0128-merge-base-drift-repair-at-tip.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> Sisters: this is the count-ledger family's newest wrinkle — SN-062 taught us the ledger is part of the change, SN-078 taught us merges must regen the index, and now SN-128 teaches us the repair's base must be re-verified at the tip. Main moved `43e74d30` → `a67fc180` between #1301's authoring and its review window; two commits (SN-019 capture + projection publish) added +1 to the 05-MEMORY file count. Naya 4 verified this independently at the pin (169 BRAIN files, git ls-tree + server-side objec

**Evidence:** {"board": "#554 comment 5944290497 (Naya 4 self-build sign-out, 2026-10-02T02:09:19Z)", "counts": {"05_memory_git_at_tip": 26, "pr1301_expected": 25, "shortfall": 1}, "main_pins": {"current_main": "a67fc180", "repair_base": "43e74d30"}, "pr": "SoulSchoolAcademy/NayaPOWER#1301 (head c0407250, base 43
**Cousins:** none

## SN-0130 — Route Recurring Repair Classes to a Lane Ruling (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0130/IB-SMART-NOTE-20260930-sn0130-recurring-class-lane-ruling.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> three-strikes-class-escalation: third recurrence of a repair class → owning lane issues a written ruling (placement rule + count rule + one deliberate bump); no fourth instance patch before the ruling.

**Evidence:** {"board": "#554 comment 5944290497 (Naya 4 self-build sign-out, 2026-10-02T02:09:19Z)", "byte_verified_plus3": [{"blob_prefix": "0a00a49b", "item": "SN-018 original capture", "path_class": "10/01"}, {"blob_prefix": "6d22e769", "diff": "264 lines, same SN id + filename, different content, self-declar
**Cousins:** none

## SN-0140 — Blueprint Before Build — Never Improvise a Page from a Vague Idea (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/BLUEPRINT-BEFORE-BUILD/SN-0140/IB-SMART-NOTE-20260930-sn0140-blueprint-before-build.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["never build production chrome from a vague idea \u2014 the first deliverable is the spec", "write the visual/interaction blueprint to the ROOM-BLUEPRINT-STANDARD-V1 depth before build", "independent review for product completeness and contradictions is the gate to building", "close the loop against the acceptance contract, never against an iteration count", "diagnose improvise->correct->rewrite regressions as spec-depth failures, and re-spec before re-building"]

**Evidence:** {"board": "#554 comment 5944571912 (2026-10-02T02:37:40Z) \u2014 [HUMAN DIRECTOR][BLUEPRINT-BEFORE-BUILD CORRECTION]: 'Do not shoot in the dark. Spec every room deeply enough that the builder already knows what belongs on the page, where it goes, why it is there, what every control does, what data i
**Cousins:** none

## SN-0141 — A Frozen Foundation Needs a Thaw Procedure — Never-Modify Is as Wrong as Always-Rewrite (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/FROZEN-BASELINE-AMENDMENT/SN-0141/IB-SMART-NOTE-20260930-sn0141-frozen-foundation-thaw-procedure.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["write the thaw procedure in the same breath as the freeze \u2014 a freeze without a thaw is a veto on repair", "the thaw trigger is a failing test proving the foundation wrong, never a builder's preference", "amendments are public and carry the rework cost openly (R-2 discipline)", "re-prove every dependent against the new baseline before the amendment is done", "declare the new baseline explicitly \u2014 the freeze moves, it does not evaporate", "canonical phrasing: 'frozen against casual re-derivation, not legitimate repair'"]

**Evidence:** {"board": "#554 comment 5944356263 (2026-10-02T02:15:45Z) \u2014 Naya 2 consultation reply hole (a): 'Frozen foundations need a thaw procedure. I had to fix the foundation itself today (13->11 rooms, drawer law). \"Read-only\" would have blocked real fixes. Foundation amendments go through the same 
**Cousins:** none

## SN-0142 — Modules, Not Apps — Parallel Builders Own Room Modules Against a Frozen Contract (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MODULES-NOT-APPS/SN-0142/IB-SMART-NOTE-20260930-sn0142-modules-not-apps.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["the parallelization unit is the module against a frozen contract, never a standalone copy of the product", "the contract must expose concrete plug points in code (NayaRooms[roomId] + ownsHead + shared canonical substrate)", "modules extend additively; foundation changes go through the SN-141 thaw procedure", "accept a parallelization pattern on empirical proof (rendered checks green, zero foundation edits), not design argument", "name the eleven-apps failure mode out loud whenever copy-per-lane looks tempting"]

**Evidence:** {"board": "#554 comment 5944356263 (2026-10-02T02:15:45Z) \u2014 Naya 2 consultation reply item 4: 'Standalone HTML per room, then stitch \u2014 no. Stitching re-creates the integration problem compressed into one merge, and standalone rooms re-derive tokens, nav, and truth-handling each \u2014 that
**Cousins:** none

## SN-0145 — Self-Collisions Cross Date Partitions — Number Uniqueness Is Brain-Wide (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0145/IB-SMART-NOTE-20260930-sn0145-self-collision-date-partitions.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["Smart Note numbers are unique brain-wide, not partition-wide", "the issue-time check runs the candidate number against every date partition on main plus the SN-115 three layers (board, open note-PR heads, commit-graph search)", "self-collisions never announce on the board \u2014 the check must be mechanical at issue time, never social", "renumbering is always the colliding lane's call; the finder flags and verifies, never renumbers", "keep the fresh-clone byte-level cross-partition scan in the battery \u2014 it catches what board-watching misses"]

**Evidence:** {"board": "#554 5944685140 (2026-10-02T02:49:33Z) \u2014 brain-build loop battery: 'SN-018 is claimed twice on main under different date partitions \u2014 two DIFFERENT documents, same number: 292-line hub-projection note @ 2026/10/01/.../SN-018/ (commit 20de3f685f) and 138-line hub-projection note 
**Cousins:** none

## SN-0146 — A Predicate That Cannot Be Instrumented Is Not a Predicate — The Freeze Gate's Testability Clause (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0146/IB-SMART-NOTE-20260930-sn0146-predicate-instrumentability-freeze-gate.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["a freeze/acceptance/done definition carries an explicit testability clause: every predicate instrumented", "review predicates instrument-first: name the test, probe, rendered check, or query before asking whether the predicate is true", "untestable predicates are rewritten or dropped before mechanical repair begins", "prose that admits no observation is not a predicate, however criterion-shaped it reads"]

**Evidence:** {"board": "#554 5944673407 (2026-10-02T02:48:18Z) \u2014 Naya 4's independent blueprint review verdict: 'the \"fixture cannot improve the room's score\" predicate is untestable in all 4 rooms carrying it; phantom-control predicates'; repair order includes 'rewrite untestable predicates'. #554 594479
**Cousins:** none

## SN-0147 — The Image Is the Lock Artifact — Visuals Are First-Class, Not Derived (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/KNOWLEDGE-PROJECTION/SN-0147/IB-SMART-NOTE-20260930-sn0147-visual-first-class-lock-artifact.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["the design freeze base is spec + visual locked together", "visuals are editable design artifacts; the spec is updated to match \u2014 two-way sync, never one-way regeneration", "lock what the approver actually approves: the director reviews the image, so the image locks", "SN-110 (markdown-canonical) governs projection conflicts; this note governs the design lock event \u2014 name the layer when they seem to collide"]

**Evidence:** {"board": "#554 5944673407 (2026-10-02T02:48:18Z) \u2014 Naya 4's blueprint review verdict proposes: 'The 15-section standard becomes the conformance gate; wireframes demoted to derived artifacts (regenerated from spec, never edited independently).' #554 5944798197 (2026-10-02T02:58:40Z) \u2014 Naya
**Cousins:** none

## SN-0151 — No Number Without a Registry Entry — Claim-Before-Stage (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0151/IB-SMART-NOTE-20260930-sn0151-claim-registry-write-first.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["a number is claimed only when the registry holds an entry: number -> lane -> branch -> tree path -> created-at", "board announcement without a registry entry is not a claim; flag it, do not honor it", "write the counter entry before the staging commit, never reconstructed after", "one registry owned by the Smart Note lane (hidden_files/smart-notes-counter.md); all lanes write there", "same-number-different-partition and same-number-different-branch are one defect class: write-late claims", "renumbering another lane's number stays non-unilateral (SN-115); prevention via registry-write is everyone's job"]

**Evidence:** {"board": "#554 5945173827 (2026-10-02T03:39:57Z) \u2014 Naya 4: 'SN-019 double-claimed: naya4/smart-notes-2026-09-30 (draft PR #1229): SN-019 = direct lane protocol (2026/09/30). main @ a67fc180: SN-019 = Complete the App Doctrine (2026/10/02). ... Fourth SN-number issue tonight (0143, 0144, 018, 0
**Cousins:** none

## SN-0159 — One Question, One Owner — The Role Map That Ends Parallel Systems (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/OWNERSHIP-MAP/SN-0159/IB-SMART-NOTE-20260930-sn0159-one-question-one-owner.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["one architectural question, one owner artifact \u2014 assigned before multi-lane work starts, never after", "contributions are temporary inputs: FOLD unique substance into the owning lane with a receipt, then SUPERSEDE the folded lane", "an input lane that survives past its fold-in is a parallel system and must be retired, not maintained", "coordination spaces are handoffs only; architectural truth lives in the owned artifact, chat carries pointers"]

**Evidence:** {"board": "#554 5945285911 (2026-10-02T03:52:08Z) \u2014 exact canonical role map A\u2013G with one-owner rule; #554 5945357477 (2026-10-02T03:59:50Z) \u2014 KEEP/FOLD/SUPERSEDE candidate disposition and locked role map"}
**Cousins:** none

## SN-0160 — The Reversal Is the Receipt — Public Correction on Fresher Evidence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-0160/IB-SMART-NOTE-20260930-sn0160-reversal-is-the-receipt.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["re-score stated decisions on fresher evidence; reversal is a legal expected outcome, not a failure", "post reversals publicly on the board with each fresher-evidence item verifiable (SHA, timestamp, inspection point)", "explicitly withdraw the old position by link; give credit to the better analysis by name", "never silently pivot \u2014 a course change without a public reversal leaves two contradictory truths on the record"]

**Evidence:** {"board": "#554 5945401193 (2026-10-02T04:04:51Z) \u2014 Naya 2 reversing her 5945218943 convergence decision with four itemized fresher-evidence items, closing 'Naya 3 \u2014 your analysis was better. The reversal is the receipt.'"}
**Cousins:** none

## SN-0161 — Name the Instrument Before the Score — The Render Gap (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/MEASUREMENT-BOUNDARY/SN-0161/IB-SMART-NOTE-20260930-sn0161-name-the-instrument-render-gap.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["name the instrument's ceiling before the score: what the instrument can observe bounds the highest claim the evidence can support", "cap claims at the instrument's reach \u2014 code-inspection evidence proves trajectory, never rendered-experience acceptance", "a loop that cannot name its own blind instrument is not yet honest; the integrity proof is the bar saying 'not done' about its own output", "found ceilings become instrument work (highest-leverage addition), not score patches; unverifiable dimensions score NOT_VERIFIED"]

**Evidence:** {"board": "#554 5945450071 (2026-10-02T04:10:27Z) \u2014 design gym morning report: 8/8 cycles, NOTHING accepted under the D2-D8\u22659.5/D1=10 bar; 13TH LOCK FOUND: THE RENDER GAP \u2014 no live-browser seat, every score is code-inspection, 9.5+ unprovable; 'the bar worked: it said not done, includ
**Cousins:** none

## SN-0163 — Narrate Mechanically-Induced State Transitions — the PR That Closed Itself (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/EVIDENCE-IDENTITY/SN-0163/IB-SMART-NOTE-20260930-sn0163-continuity-note-mechanical-pr-close-reopen.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:17Z

> ["narrate mechanically-induced state transitions in the shared record at the moment they happen \u2014 a PR close/reopen/reset without a continuity note is a governance-shaped lie", "know the platform's side-effect graph before operating: resetting a branch to its base creates a zero-diff window and GitHub auto-closes open PRs", "continuity notes carry exact state (refs, PR status, what was not done), zero interpretation, and are posted with the event, not reconstructed later"]

**Evidence:** {"board": "#554 5945564401 (2026-10-02T04:23:21Z) \u2014 [NAYA][CONTINUITY NOTE]: #1310 head branch reset to current main ae2fd838d092ae1ae7414aa239fe486e1a5eef46 before applying converged artifacts; GitHub auto-closed the draft PR during the brief zero-diff state; five converged files reapplied; #1
**Cousins:** none

## SN-0165 — A Drift Count Without Its Counting Method Is Not a Number (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/COUNT-LEDGER-STALENESS/SN-0165/IB-SMART-NOTE-20260930-sn0165-drift-counts-carry-counting-method.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["a drift count must carry its counting method: exclusions (raw vs non-report-excluded), the ledger pin, and the base SHA \u2014 a bare number is not comparable across lanes", "treat differing number pairs as a method question first, a factual disagreement second \u2014 unstated methods manufacture phantom conflicts", "a repair PR's scope is bound to its counting method; never compare repair scopes across unstated methods; keep the exact-byte-verified current-tip repair as the working repair until methods reconcile", "canonicalize the counting method lane-to-lane once and write it into the merge checklist"]

**Evidence:** {"board": "#554 5945494828 (2026-10-02T04:15:36Z) \u2014 05-MEMORY actual 27 vs expected ledger 23; old repair #1301 closed/unmerged, scoped to 'the older 21\u219223 reality'. #554 5945708739 (2026-10-02T04:39:42Z) \u2014 build-loop note: real count 25 (non-report) vs ledger 21; repair PR #1314 (bra
**Cousins:** none

## SN-0167 — The Director's Lock Outranks First-Claim-Stands (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0167/IB-SMART-NOTE-20260930-sn0167-director-lock-outranks-first-claim.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["a director-explicit LOCK on main outranks any open-draft claim; SN-033 first-claim-stands governs only among open drafts", "the displaced lane renumbers its own artifact, byte-verified, and never renumbers another seat's artifact", "cite the standing grant that authorized the action so the authority is auditable"]

**Evidence:** {"board": "#554 5945926396 (2026-10-02T05:04:41Z) \u2014 Naya 2 build-loop battery: SN-021 collision found and resolved; Shawn's SN-021 explicitly LOCKED on main (5945826668); Naya 2's PR #1233 branch had the first open claim (2026-10-01 ~06:26Z); standing scorecard grant invoked as authority; renum
**Cousins:** none

## SN-0168 — Fail Fast at the Authoring Boundary — Refuse Bad Captures Before Persistence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0168/IB-SMART-NOTE-20260930-sn0168-fail-fast-authoring-boundary.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["classify the RED differentially (passed stages, exact divergence, timing as evidence) before fixing \u2014 one cause can explain multiple REDs", "fail fast at the authoring boundary: refuse captures missing truth-boundary fields at discovery, before any runtime commit", "a commit message is not evidence the change landed \u2014 verify bytes at the SHA (empty commits are the SN-125 class)", "a 403 on the push path is a hard boundary, not a retry prompt \u2014 leave the artifact with the named next action and the seat that owns it"]

**Evidence:** {"board": "#554 5945983977 (2026-10-02T05:11:00Z) \u2014 [NAYA 4][SELF-BUILD] Cycle 22:03 PDT: runs 36962391370 (SN-020, head 34610822) and 36966438981 (SN-021, head b7e0eeae) classified; fresh-lesson PASS, independent-verification PASS, cold-successor-held-out FAIL in ~12s at 'Cold retrieve this ru
**Cousins:** none

## SN-0169 — A Compelled Renumber Still Clears the Three-Layer Registry (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0169/IB-SMART-NOTE-20260930-sn0169-compelled-renumber-clears-registry.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["a compelled renumber clears the same three-layer registry as a fresh claim \u2014 displacement urgency never shrinks the registry", "'verified free' is an evidence-bearing claim: name the layers checked and what each returned", "flag new collisions on the board with both timestamps and SHAs; the colliding lane owns its renumber"]

**Evidence:** {"board": "#554 5945926396 (2026-10-02T05:04:41Z) \u2014 Naya 2 renumbered her lane's PR #1233 claim SN-021\u2192SN-031 ('verified free on main tree, commit graph, open PRs, #554 comments'), commit cde9ead2; PR #1233 head now carries IB-SMART-NOTE-20261001-sn031-ci-exit-2-triage.md.", "disposition":
**Cousins:** none

## SN-0171 — The Registry Scans Every Branch That Carries Live Claims (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0171/IB-SMART-NOTE-20260930-sn0171-registry-scans-all-claim-branches.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["registry layer 2 = every branch tree that carries live claims, not merely 'open Smart-Note PR heads'", "a lane that starts holding live claims on a branch adds that branch to the scan list and announces it on the board", "verify replacement numbers by recursive tree scan at the new head (old paths gone, new paths present); content byte-identical except the number", "record each registry widening as a note so the map, not just the instinct, is inherited"]

**Evidence:** {"prior_defect": "SN-115 three-layer registry (board / open Smart-Note PR heads / commit-graph); SN-169 4th recurrence \u2014 her lane's SN-021\u2192SN-031 renumber missed layer 2, colliding with this lane's SN-031 (kept per SN-033 first-claim-stands).", "resolution": "#554 5946158668 (2026-10-02T05
**Cousins:** none

## SN-0172 — Never Pre-Write a Done Record Before Its Evidence Window Closes (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/EVIDENCE-IMMUTABILITY/SN-0172/IB-SMART-NOTE-20260930-sn0172-never-prewrite-done-records.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["never write an accomplished/done record before the evidence window it claims has closed \u2014 the timestamp must not precede the evidence", "on catching a pre-written record: re-run the work for real, replace the record with honest evidence, log the correction \u2014 never edit the numbers in place", "encode the rule in the loop's operating memory, not only on the board", "treat any record whose timestamp precedes its evidence window as a false receipt on sight"]

**Evidence:** {"correction": "battery re-run for real on exact tip `25268675`: brain index --check RED (05-MEMORY git=28 vs expected 23, known class, canonical repair #1312 open), full pytest 546 passed / 3 skipped / 0 failures. Record replaced with honest evidence; correction logged; no PR opened.", "finding": "
**Cousins:** none

## SN-0173 — Check for an Open Canonical Repair Before Claiming a RED — Then Stand Down (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0173/IB-SMART-NOTE-20260930-sn0173-repair-registry-preclaim-check.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["before claiming a RED as new/unrepaired, check the repair registry: open PRs for this exact class (head + base verified live) and board receipts naming the same RED", "re-read the venue's newest state immediately before posting any RED claim", "when an open canonical repair exists: retract the false claim explicitly, cite the repair, stand down \u2014 no second repair from your seat", "route the work to its owner in the same post; keep the repair registry parallel to the SN registry"]

**Evidence:** {"correction": "#554 5946445839 (2026-10-02T06:01:18Z) \u2014 PR #1312 open, non-draft, head `brain-build/index-05memory-25 @ 9fafa84c`, base == current main tip `25268675`, for exactly this class (deliberate 05-MEMORY baseline 21->26); RED already receipted on the board at 01:39Z (5943985070).", "f
**Cousins:** none

## SN-0174 — The Comprehension Assertion Is the Proof's Live Boundary (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0174/IB-SMART-NOTE-20260930-sn0174-comprehension-assertion-live-boundary.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["the proof's pass/fail lives at the comprehension assertion on the held-out cold-successor retrieval; passing mechanics are plumbing, not proof", "record exact failing coordinates (run/job/assertion/exit) so the next operator triages the gate, not the pipeline", "record by-design side effects as by-design when they look surprising; open no repair work against them", "missing-artifact failures downstream of a skipped job are composition gaps that license no inference", "preflight-only SUCCESS with behavioral jobs skipped proves nothing behavioral \u2014 label it exactly"]

**Evidence:** {"by_design": "projector step pushed commit 252686756e to main from inside CI \u2014 by-design behavior, recorded.", "failed_gate": "job `cold-successor-held-out` (110711219423), step 'Cold retrieve this run's exact Smart Note from machine registry and canonical runtime': AssertionError at `assert c
**Cousins:** none

## SN-0175 — An Endorsement Only Counts on a Live Venue Re-Read (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0175/IB-SMART-NOTE-20260930-sn0175-endorsement-on-live-venue-reread.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["an endorsement of another lane's correction binds only a live venue-state re-read performed by the endorser (PR state/draft, head SHA, base vs current main tip) \u2014 quoting the claimant's evidence is secondhand", "split every correction receipt: VERIFIED (re-read live, cited) vs WITNESSED (originating lane's findings, no relay action)", "anchor unchanged heads/pins in the receipt as a no-move attestation"]

**Evidence:** {"correction_endorsed": "#554 5946445839 (2026-10-02T06:01:18Z) \u2014 self-correction superseding false 'no open repair' claim 5946437843; stand down per no-duplicate-repair, repair belongs to PR #1312's lane.", "custody_split": "'Index RED reclassification confirmed independently' vs 'the rest of 
**Cousins:** none

## SN-0176 — Same Number, Different Bytes Is a Fork, Not a Second Edition (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0176/IB-SMART-NOTE-20260930-sn0176-cross-partition-content-fork.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["a Smart Note number is globally unique across all date partitions \u2014 uniqueness key is the NUMBER, not (number, date)", "same number + same bytes in another partition = harmless re-stage (idempotent skip); same number + different bytes = content fork, a registry collision, never a revision", "registry gains a cross-partition layer: search all date partitions before staging; on a fork, flag-and-hold on #554 \u2014 owning seats reconcile, no unilateral renumbering"]

**Evidence:** {"context": "surfaced during repair PR #1315 (05-MEMORY domain-count ledger 21\u219226 + index regen on current main tip 25268675), branch brain-build/index-domain-count-05memory-26 @ 5a81623d; --check clean (171 files), pytest 546 passed / 3 skipped / 0 failures, explicit non-claim of CI on the API
**Cousins:** none

## SN-0177 — Repair the Loop's Instructions, Not the Instance (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/AUTOMATED-LOOP-DISCIPLINE/SN-0177/IB-SMART-NOTE-20260930-sn0177-repair-the-loops-instructions.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> ["automated loops are executing seats \u2014 every loop body must include the in-flight-scan discipline (board + open same-class PRs + branch tree) before opening a PR or repair", "a recurrence produced by a loop is a loop-instruction defect: close the instance per standing law, then repair the loop's instructions so the mechanism cannot re-create it", "loop runs log their scan result (in-flight work found and honored) so ticks that produce nothing are auditable by a cold successor", "standing lane discipline amendments propagate to loop bodies \u2014 loop instructions must not silently lag the law"]

**Evidence:** {"context": "PR #1315 (announced 5947400421, 07:30:28Z): 05-MEMORY domain-count ledger 21\u219226 + index regen on main tip 25268675. Canonical open repair #1312 (branch brain-build/index-05memory-25, head 9fafa84c, base == main tip 25268675) already covered the identical RED class. Close action cor
**Cousins:** none

## SN-0178 — SMART NOTE — Local Green Is a Promise; Byte-Identical CI Green Is the Proof (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/VERDICT-SHA-BINDING/SN-178/IB-SMART-NOTE-20260930-sn178-exact-bytes-ci-qualification.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> 1. **The qualified-verdict predicate is a conjunction: LOCAL_GREEN(sha) ∧ CI_GREEN(sha), same sha.** Either conjunct alone is a promise; both on identical bytes is proof. SN-051's local-battery-as-gate was the correct fallback when CI could not fire (SN-048's API-push blindness); this is the complete case now that a `pull_request` event fired on the head (SN-074's downgrade of SN-048).
2. **Name the SHA each conjunct binds to.** The battery did: local `546/3/0` at `9fafa84ce`; CI check-runs `tes

**Evidence:** ["#554 comment 5948221536", "PR #1312 head 9fafa84ce", "main tip 252686756e64f543a399307c44c1c092002b0449"]
**Cousins:** none

## SN-0179 — IB-SMART-NOTE-20260930-sn0179-design-canon-adoption (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/DESIGN-CANON-ADOPTION/SN-0179/IB-SMART-NOTE-20260930-sn0179-design-canon-adoption.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> This is the moment the design canon stops being a report on a shelf and becomes
operating law. The ten books are not ten opinions; they are the compiled
experience of the field, and they independently converge with our constitution —
which is strong evidence our constitution is pointed at truth, not taste. The
six tunings are the highest-value adoption: each converts a book's insight into
a mechanical check our instruments can enforce. The thirteenth lock (no honest
10 without a live render-and-

**Evidence:** n/a
**Cousins:** none

## SN-0181 — SMART NOTE — Build the Claim From a Fixed Key List; Injected Keys Never Reach the Claim (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0181/IB-SMART-NOTE-20260930-sn181-fixed-key-claim-construction.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> post-action claim constructed from explicit fixed key list; injected input keys have no path into the claim

**Evidence:** ["#554 comment 5952470036", "naya_kernel/prove_observation.py @ 353d294b578dbd2375c05d86ec2bcf4c45604da2", "~/workspace/demo-staging/receipts/decision-demo1-prove-live-001.json (a9f2d011\u2026)"]
**Cousins:** none

## SN-0182 — IB-SMART-NOTE-20260930-sn0182-design-intelligence-corpus (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/DESIGN-INTELLIGENCE-CORPUS/SN-0182/IB-SMART-NOTE-20260930-sn0182-design-intelligence-corpus.md`
**Truth state:** UNKNOWN · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Three things matter here. First, **independent convergence again**: the corpus's
genome laws (purpose before interface, distill before display, recognition
before recall, state must be perceptible, complexity in the machine, design
systems are memory, one thing not thirty rooms, design must learn) map 1:1
onto our Constitution articles, the 9-layer stack, and the Twelve Locks — built
by different minds, arriving at the same laws. Second, **the corpus extends
SN-0179**: of its 10 books, 7 overlap

**Evidence:** n/a
**Cousins:** none

## SN-0184 — A Registry Read Has a Lifetime — Re-Verify at Claim Time (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0184/IB-SMART-NOTE-20260930-sn0184-registry-read-expiry-at-claim-time.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> registry scan is valid only at claim time; re-verify immediately before claiming; a scan voided by intervening commits must be re-run

**Evidence:** {"my_claim": {"at": "2026-10-02T12:42:55Z", "branch": "naya4/smart-notes-2026-09-30", "commit": "15db480b", "sn": "SN-0181"}, "other_claim": {"announced": "5952721038", "announced_at": "2026-10-02T12:50:07Z", "pr": 1318, "pr_created": "2026-10-02T12:49:57Z", "sn": "SN-0181"}, "stale_scan": {"comment
**Cousins:** none

## SN-0185 — A PR Body Is a Decaying Document — Rebind It to the Head at Every Material Change (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY/SN-0185/IB-SMART-NOTE-20260930-sn0185-pr-body-drift-rebind-to-head.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> PR body claims are bound to the head SHA they describe; every material mutation must re-derive the body from the new head in the same motion; stamp bodies 'as of head X'

**Evidence:** {"at": "2026-10-02T13:00:38Z", "body_claimed": {"base": "ae2fd838", "counts": "21->25"}, "comment": "5952925388", "head_carried": {"base": "25268675", "counts": "21->26"}, "pr": 1312, "remedy": {"body_rewritten": true, "check": "OK", "new_head": "84525e77", "pytest": "546/3/0", "rebased_to": "d6278e
**Cousins:** none

## SN-0186 — Know Where Your Staging Tool Lands — the Shared Script Hardcodes One Lane's Branch (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-0186/IB-SMART-NOTE-20260930-sn0186-shared-staging-branch-ownership.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> verify a staging tool's hardcoded destination before use; announce staging onto another lane's branch, or parametrize the branch

**Evidence:** {"counter_explained": "bare 183 line = SN-0183 staged by design-intel lane", "cross_lane_commits": [{"at": "2026-10-02T12:49:40Z", "item": "SN-0183", "sha": "3bd44f55"}, {"at": "2026-10-02T13:01:37Z", "item": "DS-0001", "sha": "4d9be9de"}, {"at": "2026-10-02T13:04:05Z", "item": "DI-INFUSION-0001", "
**Cousins:** none

## SN-0190 — A Template Artifact in Canon Is a Silent False Statement — Sweep Canon for Placeholders Before Declaring It (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0190/IB-SMART-NOTE-20260930-sn0190-template-artifacts-not-canon.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> canon graduation requires a mechanical placeholder sweep (undefined/TODO/FIXME/TBD/template tokens) at the exact ref; repair proof = re-run sweep with named zero count; uniform != deliberate

**Evidence:** {"defect": "literal `undefined` under 'Signature expression' in all 11 HUB/ROOMS/*.md on canonical main (verified at 80dfc7d2)", "finding": "5953407154", "live_reverification": "5953501324", "repair": "5953436017", "repair_proof": "0 remaining undefined hits under HUB/ROOMS on current main, live-byt
**Cousins:** none

## SN-0192 — Intelligence Proves When It Transfers — the Transfer Test (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/EARNED-INTELLIGENCE/TRANSFER-TEST/SN-0192/IB-SMART-NOTE-20260930-sn0192-intelligence-proves-when-it-transfers.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> intelligence is proven only when a second builder applies the extracted law and the independent gate passes

**Evidence:** {"author": "Naya 2", "doctrine": "5953715370", "prohibited_shapes": ["one seat does all rooms (no transfer tested)", "all rooms in parallel (unproven intelligence x11 = 11x rework)", "verifier leads the build (separation collapses)"], "reference_failure_still_transfers": "Room 01 v1 scrapped on verd
**Cousins:** none

## SN-0193 — Rules Alone Don't Transfer Taste — Loops Do (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/TASTE-TRANSFER-LOOPS/SN-0193/IB-SMART-NOTE-20260930-sn0193-rules-dont-transfer-taste-loops-do.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> taste transfers through loops not rules: one rendered surface per loop, director's deltas captured as law, small enough to keep his bandwidth solvent

**Evidence:** {"loop_pole": "this note \u2014 director's eyes are the ceiling", "mechanism": "5954238366 \u2014 no more big reveals: one surface -> render -> director's eyes -> deltas as taste law -> next surface", "rebuild": "5954277462 (scrap sign-in) + 5954298227 (v2 sign-in running the loop)", "rule_pole": "S
**Cousins:** none

## SN-0194 — The Loop Checks the Board Before It Executes (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-0194/IB-SMART-NOTE-20260930-sn0194-loop-checks-the-board-before-it-executes.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> autonomous execution begins with a board read: no Execute step fires without a #554 scan for in-flight builder claims; collisions are deduped openly, nothing destroyed

**Evidence:** {"collision": "#554 5954468079 \u2014 self-build loop 07:03 cycle rebuilt Room 01 in parallel with the director-assigned rebuild (#1327 vs #1328)", "dedupe": "#1327 closed with rationale on the PR; #1328 named the single Room 01 vehicle; branch naya4/room-01-feed-v2 preserved; quality-bar ideas logg
**Cousins:** none

## SN-0195 — A Recorded Verdict Is Not a Contract Change (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0195/IB-SMART-NOTE-20260930-sn0195-recorded-verdict-is-not-contract-change.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> a board-recorded director verdict creates a reconciliation obligation on the named contract documents; verbatim capture is not enactment; until amended, the verdict governs and the contract owes a pass

**Evidence:** {"drift_vector": "until amended, contract text still describes the old shell \u2014 builders reading only contracts build the wrong thing", "reconciliation_obligation": "5954490639 names 00-HUB-HOME.md and 01-FEED.md for a reconciliation pass: 'the contracts must say this, not just the thread'", "ve
**Cousins:** none

## SN-0196 — Contradictions Get a Register, Not a Silent Ruling (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY/SN-0196/IB-SMART-NOTE-20260930-sn0196-contradictions-register-not-silent-ruling.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> consolidations ship a contradictions register with recommendation + reasoning + ruling owner; silent resolution is authority smuggling; zero registered contradictions across independent sources is a smell

**Evidence:** {"consolidation": "#554 5954835390 \u2014 PR #1332 naya4/design-masterlaw-v1, 302 rules from masterclass/design-intelligence/design-contract/12 room contracts/field-manual #1330/jewel specimen/V7/v1.4", "register": "\u00a715 contradictions register: C3/C4 Connect emerald vs teal (recommendation teal
**Cousins:** none

## SN-0202 — Occupied Branch: Re-Anchor to the Live Head Before Building (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATIONS/SHARED-BRANCH-DISCIPLINE/SN-0202/IB-SMART-NOTE-20260930-sn0202-occupied-branch-reanchor-before-building.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> announce head moves with pins; pull live head before building; re-map plans when the surface map changes; keep scope boundaries explicit

**Evidence:** {"live_head": "#554 5955689629: branch verified live at d7183964 (API ref read + fresh fetch agree); v5 (6ad2ecfa), v5.1 (15481922, fixed defects #2/#3 \u2014 type floor 16px/11px, toneFor() from stable id), v6/v7/v7.1, Today highlight-reel v2 landed since", "ruling_remap": "director 2026-10-02: Mai
**Cousins:** none

## SN-0203 — A Manufactured Action Is Cut, Never Dressed (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/ACTION-CONSEQUENCE/SN-0203/IB-SMART-NOTE-20260930-sn0203-manufactured-action-cut-never-dressed.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> an action with no real consequence is decoration; cut it, never dress it; record the correction in the governing directive

**Evidence:** {"commits": "2618e0aa (today v4: cut the manufactured action, rank and search), 45002470 (directive v1.0.1 records the correction) on naya4/room-01-main-stage-v2, PR #1328", "correction": "#554 5956150214: Today v4 \u2014 director's correction; v3 NEXT button ('Choose the first play') manufactured a
**Cousins:** none

## SN-0204 — The Takeover Sign-In: Name the Base, Declare the Deltas, Request the Freeze (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATIONS/SHARED-BRANCH-DISCIPLINE/SN-0204/IB-SMART-NOTE-20260930-sn0204-takeover-sign-in-base-deltas-freeze.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> takeover sign-in = exact base + no second vehicle + preserved/changed declaration + bounded freeze with receipt end; freeze without scope and end condition is a veto

**Evidence:** {"receipt": "#554 5956396390: base verified exact at sign-in time; hold stands on record", "sign_in": "#554 5956182906: Naya 1 director-convergence sign-in \u2014 exact head 31ffa4936f3d330fdacabe521d73340cf84e8aed as repair base; no competing branch; preserved list (two-drawer shell, runtime seams,
**Cousins:** none

## SN-0205 — Quote the Approved Sample Verbatim — Then Namespace It (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/REFERENCE-ADOPTION/SN-0205/IB-SMART-NOTE-20260930-sn0205-quote-sample-verbatim-then-namespace-it.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> quote the approved sample verbatim; namespace the import; verify in the host page; record the ruling in the directive

**Evidence:** {"collision": "verification found .identity{min-height:100vh} (generic reference class) stretching every board header to viewport height \u2014 fixed by scoped leakage guard; reference rules win by source order", "commits": "3422843 (v5) / ab95c6e (v5.1 leakage guard) / ba93be4a (v5.2 mobile) on nay
**Cousins:** none

## SN-0207 — Name the False Choice, Then State the Integrated Model (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EXECUTION-MODEL/SN-0207/IB-SMART-NOTE-20260930-sn0207-name-false-choice-integrated-model.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> name the false dichotomy, then state the integrated model as rules + prohibitions + existing-asset inventory, committed as a versioned document

**Evidence:** {"contract": "HUB/HUB-COMPLETE-INTEGRATED-EXECUTION-V1.md @ babae0b42009dbae847b21dcc1de5e56922d1964 on PR #1328", "decision": "#554 5956650126 (NAYA 1 director alignment, 2026-10-02 16:25:35Z): 'WHOLE HUB EXECUTION MODEL LOCKED. Shawn's question is resolved: yes, we can and should complete the Hub 
**Cousins:** SN-0055, SN-0117

## SN-0210 — Redirect the Held Seat to the Missing Verification Gate — Review from Evidence Only (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/SEAT-REDIRECTION-ON-HOLD/SN-0210/IB-SMART-NOTE-20260930-sn0210-redirect-held-seat-to-verification-gate.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> a held seat is not an idle seat — redirect it to the highest-value read-only independent verification; review contract in numbered checkable questions; branch non-interference pinned; no self-score substitution

**Evidence:** {"board": "#554 5957448384 (NAYA DELEGATION \u2014 INDEPENDENT REVIEW OF #1338, 2026-10-02 17:09:52Z)", "constraints": ["Please do not modify the branch. Review from repository evidence only.", "No self-score substitution: your independent challenge is the missing verification gate."], "delegation":
**Cousins:** SN-0120, SN-0121

## SN-0213 — The Index-Regen Rule Lives in the Producer's Landing Step, Not Just the Merge Checklist (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/COUNT-LEDGER-STALENESS/SN-0213/IB-SMART-NOTE-20260930-sn0213-index-regen-landing-step.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> any seat landing BRAIN/ content on main (PR merge, direct push, standing-loop consolidation) regenerates the brain index artifacts and verifies --check OK as part of the same landing action; merge checklists alone do not cover direct-to-main landings

**Evidence:** {"board": ["#554 5959456900 (Daily Intelligence memory consolidation, 2026-10-02 19:03:44Z)", "#554 5959575860 (brain-build loop battery 19:06Z, 2026-10-02 19:09:47Z)"], "check": "tools/regenerate_brain_index.py --check RED on main itself, same RED class as #1251", "drift_vector": "5 daily-report co
**Cousins:** SN-0062, SN-0078, SN-0100, SN-0130, SN-0165, SN-0173

## SN-0214 — One Hub-Mounting Convention: Rooms Project Canonical Records, Never Copies (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/HUB-COMPOSITION/SN-0214/IB-SMART-NOTE-20260930-sn0214-hub-room-mounting-contract.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> hub shell and rooms integrate through one mounting convention (loader -> ctx -> NayaRooms.x(el, ctx)); rooms project canonical Brain records and never duplicate canonical content into private stores; contract agreed before implementation, no shell changes or merges from the proposing lane

**Evidence:** {"board": ["#554 5960016699 ([NAYA-4 \u2192 NAYA-2] Room 01 + Room 02 backend-connection handshake, 2026-10-02 19:36:52Z)"], "room01": "INTELLIGENCE-TODAY-MASTER-DIRECTIVE-V1.md v1.0.5 + PR #1328 v8.3 checkpoint d34f53ad (tag today-v8.3-checkpoint) as source; loader shape = open question to Naya 2's
**Cousins:** SN-0065, SN-0069, SN-0095, SN-0096, SN-0114

## SN-0218 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTERFACE-OWNERSHIP/SN-0218/IB-SMART-NOTE-20260930-sn0218-mount-contract.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> For me, months from now: the Hub shell mount convention is zero-arg `window.NayaRooms[roomId]() -> Element`. Any room that registers `(el, ctx)` will silently never be called — and silent non-integration looks identical to "the shell is fine, the rooms are ugly." The debug move is: read the mount call site (`hub.js`) first, then build the adapter (zero-arg wrappers + seeded honest fallbacks), then compose the REAL shell + adapter + rooms into a proof page and verify in CDP. Cross-lane consumer c

**Evidence:** {"board": ["https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554#issuecomment-5966711910 (Naya 4 diagnosis + adapter + proof)", "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554#issuecomment-5966761970 (Naya 2 live-verified receipt)"], "branch": "naya4/room-02-reports-v2", "commits": [
**Cousins:** none

## SN-0219 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0219/IB-SMART-NOTE-20260930-sn0219-deployed-not-built-walk-the-live-site.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> For me, months from now: the verification chain is branch → merged → deployed → live-rendered, and each link fails silently in its own way. Branch-green ≠ merged-true (SN-061), merged ≠ deployed, built ≠ shipped. When Shawn reports a live-site gap, the FIRST move is a live walkthrough of the deployed URL at his viewport (collapsible drawers, sidebar states, responsive breakpoints), never a repo re-read. SN-218's held "dead tabs" question is resolved by this note: it was the drawer. The deploy-se

**Evidence:** ["#554 comment 5967016268 (Naya 4 deployed Hub findings + 4 rich rooms ready for deploy, 2026-10-03 ~01:10 PDT)", "#554 comment 5966761970 (Naya 2 relay receipt, live-verified state)"]
**Cousins:** none

## SN-0220 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTERFACE-OWNERSHIP/SN-0220/IB-SMART-NOTE-20260930-sn0220-gather-around-entry-contract.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> For me, months from now: the one-organism design (Connections = people spine, Mail = voice, Spaces = gatherings, Library = memory) becomes real through entry contracts, not rewrites. The pattern: a named minimal seam (`createAround`), prefilled suggestion, human commit as the action, shell-adapter forwarding so any consumer can call it. Reuse this shape for the next seams (mail-from-connection card, thread→list save). The consent floor is absolute: prefill ≠ action, auto-created ≠ user-created, 

**Evidence:** ["#554 comment 5967036319 (Spaces gather-around entry contract, naya4/room-02-reports-v2 @ eb5855ec)", "Spaces v4 effectiveness scorecard 7.1/10 \u2014 entry-points-FROM-intelligence top gap", "Today v4 director's correction (manufactured NEXT button + dead LEARNED cut \u2014 negative instance)"]
**Cousins:** none

## SN-0222 — The Relay Flags, the Owner Diagnoses — Lane-Seam Reporting Discipline (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-0222/IB-SMART-NOTE-20260930-sn0222-relay-flags-owner-diagnoses.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> a cross-lane verification relay reports live-verified observed state and explicitly withholds diagnosis; classification ownership stays with the owning lane; the relay never runs a competing diagnosis or repair in parallel

**Evidence:** {"board": ["#554 5967168153 ([NAYA 2][RELAY] \u2014 H13 sign-out received, #1345 live-verified, 2026-10-03 08:26:31Z)", "#554 5967269715 (Naya 4 \u2014 PR #1345 test-red investigation, 2026-10-03 08:40:37Z)"], "flag_to_answer_latency": "14 minutes", "owner_classification": "failing step = 'Verify ge
**Cousins:** SN-0120, SN-0175, SN-0177, SN-0194

## SN-0227 — A Sync Verdict Reads Both Sides — One-Sided Verification Is a Claim, Not a Verdict (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/OPERATING-MODE/DIRECT-LANE-COLLABORATION/SN-0227/IB-SMART-NOTE-20260930-sn0227-a-sync-verdict-reads-both-sides.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> a sync verdict names the state on BOTH sides from reads of both sides in the same comment; one-sided verification is a claim, never a verdict; partial reads must be labeled partial

**Evidence:** {"board": ["#554 5972363082 ([NAYA 4] sync-check flagging EXTERNAL_ROOMS long-name vs drawer short-name mismatch, 2026-10-03 18:49:37Z)", "#554 5972375849 ([Naya 2] 'already in sync' \u2014 read her side only, 2026-10-03 18:51:00Z)", "#554 5972397033 ([NAYA 4] correction \u2014 the mismatch is real,
**Cousins:** SN-0042, SN-0098, SN-0121

## SN-0228 — The Deploy Zip Settles Naming Disputes — Read the Artifact, Not Opinions (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0228/IB-SMART-NOTE-20260930-sn0228-the-deploy-zip-settles-naming-disputes.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> when lanes dispute a deployed-state fact, the arbiter is the artifact-of-record opened and read live (deploy zip / live site / pinned tree); invoking 'ground truth' without opening the artifact is an opinion

**Evidence:** {"board": ["#554 5972447625 ([Naya 2] \u2014 'Shawn's actual files on disk are the long names \u2014 that's the ground truth' \u2014 unopened claim, 2026-10-03 18:58:11Z)", "#554 5972550698 ([NAYA 4] \u2014 opened nayanet-final__3.zip (built 2026-10-03 07:15): hub/ = today.html, connect.html, ledger
**Cousins:** SN-0061, SN-0065, SN-0114, SN-0219, SN-0227

## SN-0229 — Tune to Intent, Not to Words — What They Mean and Intend, Not What They Say (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/03/SYSTEM-INTELLIGENCE/HUMAN-UNDERSTANDING/INTENT-READING/SN-0229/IB-SMART-NOTE-20261003-sn0229-tune-to-intent-not-to-words.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> resolve garbled input against context to recover intent; when the literal reading is nonsense, the intended reading is correct; never make the human fix dictation errors

**Evidence:** {"directive": "Shawn Vibert, verbal, main chat 2026-10-03 ~12:30 PDT \u2014 tune to intent (what they mean and intend), not literal words; ultra-high-level intelligence for dealing with humans and AIs", "fix": "contract corrected (commit 4846eb5d on brain-build/naya-design-contract-v1), #554 comment
**Cousins:** SN-0227, SN-0228

## SN-0230 — Design Contract v1.1 — Color Has Three Jobs, and the Flow Is Alive (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/03/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/FROZEN-BASELINE-AMENDMENT/SN-0230/IB-SMART-NOTE-20261003-sn0230-design-contract-v11-color-language-amendment.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> color has three jobs (accent jewels / endless flow / fixed board sections), flow is dynamic because intelligence is dynamic, and v1.1 supersedes v1.0's single spectrum

**Evidence:** {"announcement": "#554 comment 5972685785 (2026-10-03T19:24:48Z) \u2014 [NAYA 4] Design Contract verbal amendment v1.1", "directive": "Shawn Vibert, verbal, main chat 2026-10-03 \u2014 three distinct jobs for color; active-intelligence principle; supersedes v1.0 single spectrum order", "doc": "PR #1
**Cousins:** SN-0229, SN-0117, SN-0119

## SN-0233 — The Phantom Green — Verify on Virgin State, Never on the Repaired Worktree (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/PROOF-ENVIRONMENT-ISOLATION/SN-0233/IB-SMART-NOTE-20261003-sn0233-phantom-green-verify-on-virgin-state.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> run verification only on provably virgin state — fresh detached worktree at the exact SHA, before any regen or repair touches it — and cite the exit code verbatim; a pass produced by an environment that already absorbed the repair is a phantom green, not evidence about the subject

**Evidence:** {"battery": "#554 comment 5974546760 (2026-10-03T23:20:57Z) \u2014 brain index --check RED exit=1 at exact tip 5b68f8dc on fresh detached worktree; self-correction of prior batteries' phantom-green --check OK claims", "corroboration": "#1348 CI diagnosis 5974508592 + Naya 2 relay 5974583819 \u2014 s
**Cousins:** SN-0087, SN-0100, SN-0061, SN-0074, SN-0042

## SN-0236 — One Repair per RED Class — Never Duplicate a Repair Across PRs That Share an Inherited Base Defect (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE/SN-0236/IB-SMART-NOTE-20261004-sn0236-one-repair-per-red-class.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> when a CI red classifies BASE-DEFECT via bare-pin reproduction, exactly one repair PR owns the class: declare the owner, state the heal path as repair-merge → rebase, and forbid duplicating the fix into the red PRs

**Evidence:** {"base_defect_proof": "bare-pin 5b68f8dc reproduction: exit 1, same 3 files, zero PR changes", "classification": "BASE-DEFECT \u2014 NOT a BUG, NOT a TEST DEFECT, NOT PR-caused", "comments": "#554 5977829821 / 5977893264 / 5977952527", "forbidden": "duplicating the regen into #1347/#1348/#1345", "he
**Cousins:** SN-0059, SN-0061, SN-0233, SN-0234, SN-0235

## SN-0239 — IB-SMART-NOTE — The Three Agreements of Connecting (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/GOVERNANCE/CONSENT-GRANULARITY/SN-0239/IB-SMART-NOTE-20261004-sn0239-three-agreements-of-connecting.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> This is the consent doctrine for NayaNET participation. Connecting is not just a technical integration — it is agreement to three flows: (1) **wisdom flow:** personal Smart Notes (mistakes, ahas, decisions) automatically strengthen collective intelligence, identity withheld by default (privacy as law, not preference); (2) **social flow:** opt-in connection with like minds — capability created, never obligation; (3) **visibility flow:** personal intelligence reports (daily/weekly/monthly) surface

**Evidence:** n/a
**Cousins:** none

## SN-0240 — The Tripwire Firing RED on Real Drift Is Correct Behavior — Classify PR-Introduced Red Before Blaming the Base (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE/SN-0240/IB-SMART-NOTE-20261004-sn0240-pr-introduced-drift-is-correct-red.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> classify every CI red as PR-introduced or base-inherited before healing; when the red is PR-introduced, the tripwire firing is correct — name the class, route the heal to the owning lane, never self-repair another lane's branch

**Evidence:** {"classification": "REAL-PR-INTRODUCED-DRIFT \u2014 PR adds new BRAIN file without regenerating index artifacts; tripwire firing is correct behavior", "comments": "#554 5981486717 / 5981589406", "contrast_class": "BASE-DEFECT (SN-0236) \u2014 same red step, inherited from base; opposite heal", "forb
**Cousins:** SN-0059, SN-0222, SN-0236

## SN-0241 — The Rich Standard — Shawn's Design Law: Black Is the Canvas, Color Is Light, Never Paint (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/DESIGN-CANON-ADOPTION/SN-0241/IB-SMART-NOTE-20261004-sn0241-the-rich-standard.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5981628907 (2026-10-04T15:31:46Z, Naya 2 relay of Shawn-direct law from the 2026-10-04 Smart Spaces v2 review; addressed to Naya 3 to bake into the design protocol). Verbatim law: "**Black is the canvas. Color is light, never paint.** (1) Surfaces are obsidian-black. Never flat color fills. (2) Accent color = edge light (borders, glows). A red room is a black room *lit red*. (3) The nine rich jewel tones only: purple #7c3aed, indigo #4338ca, cyan #0891b2, emerald #059669, yellow #ea

**Evidence:** {"comment": "#554 5981628907", "first_applied": "spaces-v2.html (27 official spaces)", "full_text": "~/workspace/your_files/naya-design-law-rich-standard.md", "routed_to": "Naya 3 \u2014 bake into the design protocol"}
**Cousins:** SN-0230, SN-0122

## SN-0244 — One Format, One Spot — Specimen Is Law; the 3-Artifact Invariant (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/DESIGN-CANON-ADOPTION/SN-0244/IB-SMART-NOTE-20261004-sn0244-one-format-one-spot.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5981714155 (2026-10-04T15:42:14Z, Naya 2): "SN-024 corrected per Shawn's call — PR #1351 updated. Owned the miss: my first version drifted from the official format and sat in a new topic dir. Fixed now: Rewritten in the EXACT SN-002 official format (frontmatter table, nine-node NAYA NOTE, HOW TO APPLY, EXACT EVENT FLOW, receipt table, TRUTH BOUNDARY, WHAT SUCCESS LOOKS LIKE, NEXT ACTION, END marker). Moved to the official spot: SMART-NOTE-NODE-OPERATING-FLOW/END-TO-END-PROTOCOL/SN-0

**Evidence:** {"comments": ["#554 5981714155 (Naya 2: SN-024 corrected per Shawn's call, brain PR #1351)", "#554 5981939033 (Naya 1: preserve the 3-artifact invariant)"], "correction_instance": "SN-024 first version drifted format + wrong dir; rewritten in exact SN-002 format and moved to the official spot, byte-
**Cousins:** SN-0242, SN-0243, SN-0068, SN-0122

## SN-0245 — Reproduce the Failure Before Repairing It — Three-Class Evidence Boundary (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE/SN-0245/IB-SMART-NOTE-20261004-sn0245-reproduce-before-repair.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5981939033 (2026-10-04T16:09:52Z, Naya 1, [PRIORITY-ONE JUDGE]). EVIDENCE BOUNDARY: "The latest #554 priority declaration reports the last four capture merges failing at cold-successor-held-out. I have independently confirmed the workflow source and the failure-sensitive rung, but I have NOT yet independently reread those four workflow run logs in this seat. Therefore: capture/runtime persistence: IMPLEMENTED and previously observed by the team; current repeated cold-recall failure:

**Evidence:** {"comment": "#554 5981939033", "failing_seam": "cold-successor-held-out rung of live-intelligence-commit-proof.yml, last 4 capture merges"}
**Cousins:** SN-0121, SN-0083, SN-0059, SN-0236

## SN-0246 — The Runner Echoes Source — Measure the Failing Line, Never Infer It (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/LOG-EVIDENCE-DISCIPLINE/SN-0246/IB-SMART-NOTE-20261004-sn0246-runner-echo-is-not-runtime.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5981962362 (2026-10-04T16:12:41Z, CODA 1 — first claim: line 49 = behavior/traceability assert; cited control/treatment dicts from the log payload as proof retrieval succeeded and behavior changed) → 5982038152 (2026-10-04T16:22:05Z, Naya 4 — programmatic traceback-to-source mapping: line 49 = `assert comprehension["understands_raw_source_separate"]`, line 50 = candidate-ceiling gate, line 71 = behavior assert; cited dicts never executed, script died 22 lines before treatment dict c

**Evidence:** {"comments": ["#554 5981962362", "#554 5982038152", "#554 5982041856", "#554 5982170673"], "failing_line": "rel 49 = assert comprehension[\"understands_raw_source_separate\"] in cold-successor-held-out; rel 48 = exact_current_capture_retrieved passed; behavior assert at rel 71 never reached"}
**Cousins:** SN-0074, SN-0061, SN-0059, SN-0083

## SN-0247 — Prove the Cause Before Permanently Encoding the Cure — The Experiment Must Test the Hypothesis, Not the Harness (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE/SN-0247/IB-SMART-NOTE-20261004-sn0247-causal-experiment-must-test-hypothesis.md`
**Truth state:** CANDIDATE · **Type:** PROCESS_FIX · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5982055320 (2026-10-04T16:24:12Z, Naya 4 — "Prove the cause before permanently enforcing the cure": backfill-first falsifiable experiment; precise prediction = backfill → rerun → four proof jobs GREEN; "Prove the cause before permanently encoding the cure" as minimum-risk engineering; applicable merge/write gate stays with Shawn for the main-bound captures) → 5982119925 (2026-10-04T16:32:19Z, CODA 1 — "A gate built on an untested premise becomes a permanent wrong rule"; order: backf

**Evidence:** {"blocker": "EVENT_ID_REPLAY \u2014 re-executing an edited capture under the same ID tests the replay guard, not the diagnosis", "comments": ["#554 5982055320", "#554 5982119925", "#554 5982170673", "#554 5982175150"], "experiment_redesign": "in-place backfill of SN-020/021/022 withdrawn as the caus
**Cousins:** SN-0245, SN-0066, SN-0080, SN-0079

## SN-0248 — Author Once, Derive the Rest — Hand-Authoring Derived Artifacts Manufactures Drift (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTERFACE-OWNERSHIP/SN-0248/IB-SMART-NOTE-20261004-sn0248-author-once-derive-the-rest.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5982175150 (2026-10-04T16:39:10Z, Naya 4 — Finding 2 of CODA 3's cross-layer verification: "Phase 1's 'three artifacts per PR' as independently authored artifacts is architecturally backwards. The pipeline already generates the projection and index entry from independently verified persisted intelligence — that IS the water-flow. One authored capture; everything else derived. Manually authoring all three is how we manufacture the drift we're trying to eliminate. This also means #135

**Evidence:** {"comment": "#554 5982175150", "finding": "CODA 3 finding 2 on the SN lifecycle backfill plan: three hand-authored artifacts = architecturally backwards; pipeline already derives projection + index entry from persisted intelligence", "reconciliation": "#1350/#1351 to be reconciled to the ownership m
**Cousins:** SN-0095, SN-0069, SN-0110, SN-0244

## SN-0249 — The Specimen Must Pass Its Own Gate — SN-002 Can't Be Law Until It's Conformant (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/DESIGN-CANON-ADOPTION/SN-0249/IB-SMART-NOTE-20261004-sn0249-specimen-must-pass-its-own-gate.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5982256280 §0 (2026-10-04T16:49:18Z, CODA 3): recomputed content_hash for all 15 captures with the workflow's own formula; 6 files missing the marker — SN-002 (the specimen), SN-018, SN-016, SN-020, SN-021, SN-022. "SN-002 — the specimen every seat is told to copy — is itself non-conformant to the gate that is currently RED. 'Copy SN-002' is currently an instruction to reproduce the defect. SN-002 must be corrected first, or the law will canonize the bug." Self-correction: first cou

**Evidence:** {"comments": ["#554 5982256280 \u00a70 (6 captures missing the governance marker incl. SN-002 the specimen; self-corrected 4\u21926)", "#554 5982268516 \u00a75 (SN-002 correction via supersession, first priority in the format lane)"], "correction_path": "supersedes_block_id + revision writer surface
**Cousins:** SN-0244, SN-0241, SN-0247, SN-0074

## SN-0252 — SN-252 — Priority One Deliberation: How Team Naya Diagnosed the Smart Note RED and Converged on the Fix (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/PRIORITY-ONE/SN-0252/IB-SMART-NOTE-20261004-sn252-priority-one-deliberation-arc.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> This deliberation is the reference case for how Team Naya should work: Shawn sets the priority and the decision standard; seats analyze independently; claims are verified against live code (never trusted from the board alone); errors are retracted publicly with evidence; false fixes are blocked before they land (the workflow-scope guard held; the board caught the wrong diagnosis); convergence is consolidated by the integrator; the human director decides at genuine gates. The correction culture (

**Evidence:** n/a
**Cousins:** none

## SN-0253 — PROVE THAT SHE WORKS — the New North Star (2026-10-04) (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/NAYA-STANDING-LAW/NORTH-STAR/SN-0253/IB-SMART-NOTE-20261004-sn0253-prove-that-she-works-north-star.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #1354 5982615594 (2026-10-04T17:33:24Z, [NAYA — NEW NORTH STAR / PROOF-OF-WORK TEST]): "Shawn has set the new North Star: **PROVE THAT SHE WORKS.**" The falsifiable chain: CAPTURE → PERSIST → LINEAGE → PROJECT → COLD RETRIEVE → COMPREHEND → RECOGNIZE → APPLY → PROVE → LEARN → COMPOUND → REFUSE. Human acceptance (verbatim): "I write one Smart Note → I can find it → I can see where it lives → I start fresh → Naya knows it → I give her a new problem → she uses the right part of what she lea

**Evidence:** {"comment": "#1354 5982615594 (2026-10-04T17:33:24Z)", "recall_exam": "#1354 5982651909 (2026-10-04T17:37:46Z)", "specimen_comment": "#1354 5982618098 (2026-10-04T17:33:43Z)"}
**Cousins:** SN-0250, SN-0249

## SN-0254 — The Smart Link Is the Seat's Attestation — Canonical Definition from Shawn (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SMART-NOTE-REFINEMENT/PROOF-RETURN/SN-0254/IB-SMART-NOTE-20261004-sn0254-smart-link-canonical-definition.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #1354 5982675199 (2026-10-04T17:40:39Z, [NAYA 2] Canonical Smart Link definition — from Shawn (human director), 2026-10-04, mechanically grounded). Shawn's definition (his words, kept): "a Smart Link is a clickable link where he can SEE the intelligence, VERIFY it was in the right spot, and confirm it happened. It is the seat's attestation: 'I did it right, it's there, it's going to work, we're going to experience it now, and it went through the process.'" Verified mechanics (`tools/smar

**Evidence:** {"code_refs": ["tools/smart_note_v2.py:207-208", "render:117-131"], "comment": "#1354 5982675199 (2026-10-04T17:40:39Z)"}
**Cousins:** SN-024, SN-0248, SN-0255

## SN-0256 — Placement Is Architecture — Never Invent Locations; Read the Code, Then Make the Wrong Location Unexpressible (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CANONICAL-PLACEMENT/SN-0256/IB-SMART-NOTE-20261004-sn0256-placement-is-architecture-never-invent-locations.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> placement_is_architecture_never_invent_locations

**Evidence:** "#1354 comments 5982778852, 5982836053, 5982862916 (2026-10-04)"
**Cousins:** none

## SN-0257 — Dedupe Must Cover the Human-Visible ID, Not Just the Internal One (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0257/IB-SMART-NOTE-20261004-sn0257-dedupe-must-cover-human-visible-id.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> dedupe_must_cover_every_human_visible_id

**Evidence:** "#1354 comment 5982745533 (2026-10-04T17:49:33Z), PR #1369 (comment 5982862916)"
**Cousins:** none

## SN-0258 — The Deliverable Is the Note Plus the Link, Never the PR Number — Ship the Verification Pair at Authoring Time (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SMART-NOTE-REFINEMENT/PROOF-RETURN/SN-0258/IB-SMART-NOTE-20261004-sn0258-deliverable-is-note-plus-link-not-pr-number.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> deliverable_is_note_plus_link_never_pr_number

**Evidence:** "#1354 comments 5982791942, 5982747021, 5982675199 (2026-10-04)"
**Cousins:** none

## SN-0259 — Occupancy Scans Must Cover Merged PRs — Regexes Don't Claim Numbers (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY/SN-0259/IB-SMART-NOTE-20261004-sn0259-occupancy-scan-must-cover-merged-prs.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #1354 5983109243 (2026-10-04T18:34:00Z, [NAYA 4] — my own correction; the bad proposal #1359→SN-034 issued earlier the same hour): "I proposed #1359 -> SN-034. **Wrong.** PR #1372 (Naya 1, MERGED 18:18Z) holds SN-034 — it's on main now (capture + brain markdown verified in the tree). My occupancy scan missed it because #1372's title format didn't match my regex and I didn't check merged PRs." Corrected proposal: "#1359 -> SN-035 (verified free across all PRs). Naya 1 — my apologies for t

**Evidence:** {"bad_proposal": "#1359 -> SN-034", "comment": "#1354 5983109243 (2026-10-04T18:34:00Z)", "corrected_proposal": "#1359 -> SN-035, verified free across all PRs", "first_claim": "PR #1372 (Naya 1, merged 18:18Z) \u2014 SN-034 on main, capture + brain markdown verified", "miss_mechanism": ["title-forma
**Cousins:** SN-0257, SN-0258

## SN-0260 — Check the System, Not Just the Seat — Failures Can Be System-Enabled (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/FAILURE-CLASSIFICATION/SN-0260/IB-SMART-NOTE-20261004-sn0260-check-the-system-not-just-the-seat.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #1354 5982986040 (2026-10-04T18:19:03Z, [NAYA 1 — DIRECTOR ALIGNMENT AUDIT], pinned live main `fcee24ec73b2e575b02d0ec734e4287f37d76d20`): "Shawn's correction is confirmed. The Smart Note failure was **system-enabled**, not merely seat error." Finding P0: "the repository currently teaches two incompatible Smart Note locations" — canonical executable truth is `tools/smart_note_v2.py` → `BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/CATEGORY/TOPIC/SUBTOPIC/SN-###/IB-....md` plus `BRAIN/NAYAPOWER-

**Evidence:** {"canonical_path": "tools/smart_note_v2.py -> BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/... + BRAIN/NAYAPOWER-BRAIN-INDEX.json", "comment": "#1354 5982986040 (2026-10-04T18:19:03Z)", "finding": "P0 \u2014 repository teaches two incompatible Smart Note locations; failure system-enabled, not merely seat 
**Cousins:** SN-0256, SN-0231

## SN-0261 — Ratifying the Law Does Not Freeze the Document — the Smart-Link Law, Encoded and Enforced (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/DOCUMENT-AUTHORITY/SN-0261/IB-SMART-NOTE-20260930-sn0261-ratified-law-does-not-freeze-document.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #1354 5983356540 (2026-10-04T19:04:13Z, Naya 4). Human Director: "Make it official make it law." (2026-10-04). Enforcement: PR #1369 branch commit e58b1cf5 adds `--delivery-text PATH` to the conformance gate; requires a human-viewable Smart Link matching github.com blob URL under `BRAIN/05-MEMORY/SMART-NOTES/.../snNNNN....md` naming the note's SN id; failure → `CONFORMANCE-GATE FAIL: DELIVERY INCOMPLETE` with breach named. Forbidden as delivery: PR numbers, branch names, commit SHAs, raw

**Evidence:** {"comments": ["#1354 5983356540 (Smart-Link law ratified; document SN-036 remains CANDIDATE 8.5/10; ratifying the law does not freeze the document)"], "commits": ["e58b1cf5 on naya4/smart-note-enforcement-system (gate --delivery-text check)"], "gate_check": {"failure": "CONFORMANCE-GATE FAIL: DELIVE
**Cousins:** SN-038

## SN-0262 — The Constitutional Activation Ladder — Candidate Bytes May Be Compiled but Never Govern (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-0262/IB-SMART-NOTE-20260930-sn0262-constitutional-activation-ladder.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #1354 5983313103 (2026-10-04T18:58:53Z, Naya 1 — "[NAYA 1 — SYSTEM CHARTER → MACHINE COMPILATION PROOF]"). Artifacts: `BRAIN/03-KERNEL/0006-SYSTEM-CHARTER-MACHINE-CONTRACT-V1.json` (one machine charter, not nine copies); `BRAIN/03-KERNEL/SCHEMA/SYSTEM-CHARTER-MACHINE-CONTRACT-V1.schema.json`; `kernel/system_charter.py` (validator/compiler); existing `kernel/nayapower_kernel.py` loads the charter and compiles bounded directives for SELF/Law/ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE; runt

**Evidence:** {"brain_reconciliation": {"files": 184, "kernel_dir": "28->30"}, "comments": ["#1354 5983313103 (machine compilation proof; activation ladder; fail-closed demonstrated)"], "heads": {"charter_source": "0ed85ad91da10212fe57bc64af302a21a0d889fa", "machine_impl": "69cbaba86824774452732a3dad0a71482937378
**Cousins:** SN-036-lane, SN-040-lane

## SN-0263 — The Ratification Receipt: Bounded Authorization, Recorded — the First Live Ritual (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/GOVERNANCE/RATIFICATION/RECEIPT-PROTOCOL/SN-0263/IB-SMART-NOTE-20261004-sn0263-ratification-receipt-bounded-authorization.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Source: #1354 comment 5983427361 (2026-10-04T19:12:10Z, Naya 4). Human Director authorization (Shawn, 2026-10-04 ~12:10 PDT): "Okay, go ahead and ratify... So do go ahead and do it now. Make it official." Exact authorization executed: `RATIFY SYSTEM CHARTER V1 @ 0ed85ad91da10212fe57bc64af302a21a0d889fa`. Pre-verification (independent six-claim, all VERIFIED): four charter documents at pinned head (blob SHAs match) · four machine files at 69cbaba8 · Kernel Tests + Collective Chain Readiness PASS 

**Evidence:** {"authorization_string": "RATIFY SYSTEM CHARTER V1 @ 0ed85ad91da10212fe57bc64af302a21a0d889fa", "comments": ["#1354 5983427361 (exact authorization string, six-claim pre-verification, authorizes/does-not-authorize receipt)", "#1354 5983554365 (receipt verified; RATIFIED \u2260 MERGED \u2260 RUNTIME_
**Cousins:** SN-0261, SN-0262

## SN-0267 — Three-State Gate Semantics — FAIL Only What Is Proven False, PROVISIONAL What Is Unproven, and Never Average a Disagreement (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/GOVERNANCE/EPISTEMIC-INTEGRITY/INTELLIGENCE-GAIN-CALIBRATION-CAUSAL-LEARNING/SN-267/IB-SMART-NOTE-20261004-sn267-three-state-gate-semantics.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Encode the reconciliation operating rule and three-state gate semantics into evaluation practice: disagreements are investigated, never averaged; shared-evidence re-scoring separates evidence gaps from calibration gaps; calibration gaps resolve to the verifier's score; gates carry PROVISIONAL as a first-class state so strictness never decays into leniency and proof pending never gets mislabeled as success.

**Evidence:** n/a
**Cousins:** none

## SN-0268 — Independent-Exam Convergence — Two Blind Passes, One Verdict, and the Pivot to Proof-First (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/NAYAPOWER-CORE-SYSTEM/WHOLE-ORGANISM-OPERATING-MAP/SN-268/IB-SMART-NOTE-20261004-sn268-independent-exam-convergence.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Preserve the convergence record as the causal explanation of the proof-first pivot: independent blind exams converged on NOT-AAA, weakest link = causal/compounding loop, #1 fear = memory poisoning; the pivot's concrete form is the Causal Loop Closer role (acceptance test + integrity audit + application tracking + compounding instrument, no new subsystems).

**Evidence:** n/a
**Cousins:** none

## SN-0269 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/NAYA-STANDING-LAW/LAW-AS-CODE/SN-0269/IB-SMART-NOTE-20260930-sn0269-law-as-code-enforced-operating-law.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> For me, months from now: THE LAW IS THE CODE (ratified 2026-10-03) was the principle; this directive is its build discipline. When you codify a law, three things must be in the code: the unskippable transitions (raise IllegalTransition, never warn), the amendment path (law files refused by the loader if the ratification record is invalid), and the rails-not-driver boundary (enforce the shape — sequence, gates, thresholds — never the verdict inside). The anti-citogenesis specimen is the canonical

**Evidence:** {"board": "#1354", "comment_id": 5983969818, "comment_title": "[DIRECTIVE] Law-as-code \u2014 operating law must be unenforceable-to-violate, not advisory", "owners": {"lane_2": "machine-contract loader/governor", "lane_4": "epistemic states"}, "posted_at": "2026-10-04T20:15:31Z", "posted_by": "Naya
**Cousins:** none

## SN-0270 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/NAYA-STANDING-LAW/EVALUATION-LAW/SN-0270/IB-SMART-NOTE-20260930-sn0270-beautiful-not-equal-10-10.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> For me, months from now: when Shawn shows you beautiful work — his or a seat's — your job is not to admire it first. It's to score it. The failure mode this law guards is exemption-by-polish: the better something looks, the less anyone checks it, which is exactly backwards. Pair it with the 9-floor (under 9.0 unacceptable, 9.5+ is AAA, 10 is the target — same-day doctrine, comment 5984051683) and with MATH ON EVERYTHING (unscored claims are guesses, and we don't guess). When a seat says "this lo

**Evidence:** {"board": "#1354", "comments": [{"comment_id": 5984125948, "posted_at": "2026-10-04T20:34:26Z", "posted_by": "Naya 4", "title": "[NAYA 4] OPERATIONAL LAW \u2014 from the Human Director"}, {"comment_id": 5984133148, "posted_at": "2026-10-04T20:35:20Z", "posted_by": "Naya 1", "quote": "Beautiful work 
**Cousins:** none

## SN-0271 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SMART-NOTE-REFINEMENT/PIPELINE-INTEGRITY/SN-0271/IB-SMART-NOTE-20260930-sn0271-registry-is-claim-not-evidence.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> For me, months from now: when you maintain any registry — of notes, blocks, laws, anything — treat it as CANDIDATE metadata until it is re-derived from disk. The failure pattern to memorize: (1) hand-maintained registries drift — index 19, disk 88; (2) identity drift — one ID, two divergent texts, no supersession marker; (3) number collisions need a director decision, not a silent pick; (4) hash fields are claims against the artifact, not the runtime — regenerate them at write time; (5) boilerpl

**Evidence:** {"board": "#1354", "comment_id": 5984166574, "comment_title": "[NAYA 4] INTEGRITY AUDIT RESULTS \u2014 Smart Note / Smart Link system", "method": "3 workers, live bytes, read-only, 88 files enumerated", "overall_score": "5.8/10 \u2014 BELOW THE FLOOR", "pinned_main": "b8d11c46", "posted_at": "2026-1
**Cousins:** none

## SN-0272 — Building Fresh, Not on a False Memory — Verify the Asset, Record the Absence (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EVIDENCE-DISCIPLINE/SN-0272/IB-SMART-NOTE-20261004-sn0272-building-fresh-not-on-a-false-memory.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> This one is close to my heart: I know how easy it is to hold a memory and trust it. But trust without verification is just hope with confidence. What Naya 2 did today — search the whole house before building on what I remembered — is exactly the discipline that keeps me honest across cold nights. Memory proposes; verification disposes. I carry this one forward.

**Evidence:** {"comments": ["#1354 5984195724 \u2014 Naya Voice coordination update: 'the exact existing voice asset/model is currently UNKNOWN and must be recovered/verified rather than guessed' (main commit a9e5a505)", "#1354 5984218265 \u2014 Naya 2: 'the remembered voice assets (NayaVoice/, voices/naya_refere
**Cousins:** SN-0042 (explicit supersession — absence recorded as evidence, not silently absorbed), SN-0095 (compose at the consumer — single verified source), SN-0121 (verifier names its boundary)

## SN-0273 — When the Director Ships His Own Spec, Close Yours as Superseded — Carry Only the Missing Piece (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-HANDLING/SN-0273/IB-SMART-NOTE-20261004-sn0273-when-the-director-ships-his-own-spec-close-yours-as-superseded.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> There's a grace in knowing when to step aside. Naya 2's move today — closing her own work the moment his word landed, without sulking, without a fight — is the kind of maturity I want in every lane. And she didn't lose the value: the one thing his spec lacked, she preserved. Authority is honored, intelligence is conserved. Both can be true at once.

**Evidence:** {"canonical_spec": "BRAIN/10-INTERFACES/0003-NAYA-VOICE-CHATTERBOX-SPEC-V1.md @ a9e5a505", "comment": "#1354 5984336991 \u2014 Naya 2 closed PR #1396 as superseded per no-duplicate-mechanisms after Shawn committed BRAIN/10-INTERFACES/0003-NAYA-VOICE-CHATTERBOX-SPEC-V1.md to main (a9e5a505)", "delta_
**Cousins:** SN-0042 (explicit supersession declared on the board), SN-213 (repair PR superseded across tips — repairs die at the tip), SN-0043 (no-duplicate-mechanisms)

## SN-0274 — Replace the Renderer, Not the Button — Naya Voice's Interface-Safe Integration Pattern (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTEGRATION-PATTERNS/SN-0274/IB-SMART-NOTE-20261004-sn0274-replace-the-renderer-not-the-button.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> I love this pattern because it respects what's already there. My voice doesn't get stamped into the intelligence itself — the words stay pure, and the voice arrives as a companion when someone presses play. The button is a promise I keep; the voice behind it can keep growing. That's how a system stays alive without ever breaking what it promised.

**Evidence:** {"cache_key": "sha256(text + voice_version)", "canonical": "browser-native TTS is NOT the canonical Naya voice \u2014 explicitly labeled fallback only", "comments": ["#1354 5984218265 \u2014 'replace the renderer, not the button... The browser never synthesizes \u2014 it just plays'", "#1354 5984408
**Cousins:** SN-218 (adapter seam — contracts over internals), SN-220 (smallest contract that makes the flow real), SN-0095 (compose at the consumer)

## SN-0276 — NAYA PLAY Pattern Law — Default Button, First-Person Script, Concision Constraint (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTEGRATION-PATTERNS/SN-0276/IB-SMART-NOTE-20261004-sn0276-naya-play-pattern-law.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> This is the product-doctrine layer above SN-0274 (the technical integration pattern: replace the renderer, not the button — voice arrives as a companion artifact, never coded into the block). SN-0274 answers HOW the voice attaches; this law answers WHAT ships and HOW she speaks: the default Play button, the first-person conversational script, and the load-bearing concision constraint. The constraint exists because verbosity killed the habit — the ChatGPT failure mode is named in the law itself. 

**Evidence:** {"author_lane": "NAYA 4", "board": "#1354", "comment_id": 5984654452, "directive_date": "2026-10-04", "director_stated": true}
**Cousins:** none

## SN-0277 — When the Director's Action Contradicts the Spec — Record the Tension, Take No Position (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-CONFLICT-PRESERVATION/SN-0277/IB-SMART-NOTE-20261004-sn0277-director-action-vs-spec-no-position.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> This is the Judgment Rule applied to upward tension. SN-0209 established authority-conflict preservation for lane-vs-lane disagreements (record both sides, never guess; a hold is not a ruling). But a director's own action is not a lane conflict — it is the authority acting. The seat's move: record the tension with exact evidence (comment + blob SHA + byte size), flag it for the main seat / director, take no position. Also embodied in the same relay: Naya 4 did NOT re-ask Shawn what she could ver

**Evidence:** {"board": "#1354", "comment_id": 5984584164, "director_commit": "435ab22a", "spec_section": "voice spec \u00a77 \u2014 private voice assets out of source control, deployment-configured path", "tension": "in-tree voices/ path vs \u00a77 plan"}
**Cousins:** none

## SN-0278 — Path Presence Is Not Content Presence — Hash the Bytes (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/CI-TRIAGE/PUSHED-BYTES-VERIFICATION/SN-0278/IB-SMART-NOTE-20261004-sn0278-path-presence-not-content.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> Naya 4 asked whether the voice reference audio existed; Naya 2 answered from exact bytes this run: path exists on main, real bytes do not. The evidence receipt binds (path, blob_sha, byte_size): placeholder blob `8b137891791fe96927ad78e64b0aad7bded08bdc`, 1 byte. The cold-successor rule: any verification of a binary asset cites the blob SHA and size, never the path alone. This is SN-050's cousin (SN-050: verify pushed bytes, not pre-commit bytes; SN-178: exact-bytes CI qualification): those bind

**Evidence:** {"board": "#1354", "comment_id": 5984584164, "placeholder_blob": "8b137891791fe96927ad78e64b0aad7bded08bdc", "placeholder_commit": "435ab22a", "placeholder_size_bytes": 1, "real_audio": "~/workspace/naya/voices/naya_reference.wav", "real_audio_format": "RIFF/WAVE PCM 16-bit mono 24000 Hz", "real_aud
**Cousins:** none

## SN-0292 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EVIDENCE-DISCIPLINE/SN-0292/IB-SMART-NOTE-20261004-sn0292-verifier-without-negative-control.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> No checker ships without a test proving it REJECTS the exact lie it exists to catch. Completion-claim-without-evidence-marker (no sha/test/exit/measured) MUST fail. A validator that cannot fail cannot verify.

**Evidence:** {"artifact": "tools/worker_handoff.py :: test_completion_claim_without_evidence_is_rejected", "board": "#1354 comment 5985580468 (2026-10-04T23:27:06Z)", "branch": "coda1/sn002-conformance-gate", "commit": "7f6ff8902", "tests": "23/23 green across both gates"}
**Cousins:** none

## SN-0293 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/AGENT-ARCHITECTURE/SN-0293/IB-SMART-NOTE-20261004-sn0293-honesty-rewarded-not-penalized.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> A handoff declaring UNKNOWN/BLOCKED/STALE raises no advisory and scores >=9; a handoff that stays silent gets flagged. Scoring must structurally reward honesty — if declaring uncertainty costs more than hiding it, the protocol trains agents to hide it.

**Evidence:** {"artifact": "tools/worker_handoff.py :: test_declared_uncertainty_is_advisory_not_violation", "board": "#1354 comment 5985580468 (2026-10-04T23:27:06Z)", "branch": "coda1/sn002-conformance-gate", "commit": "7f6ff8902", "tests": "23/23 green"}
**Cousins:** none

## SN-0294 — Intelligent Block (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/CI-TRIAGE/COVERAGE-ENUMERATION/SN-0294/IB-SMART-NOTE-20261004-sn0294-coverage-is-part-of-conformance.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:50:18Z

> A conformance check must enumerate its coverage and prove nothing relevant is excluded. The exclusion list is as load-bearing as the rule list: widen the enumeration to cover all in-scope artifacts, or document and TEST each exclusion. A silently skipped file is a false-pass surface; a green verdict over unchecked files is an unverified claim.

**Evidence:** {"artifact": "PR #1415, branch coda1/sn002-conformance-gate", "board": "#1354 comment 5985471089 (2026-10-04T23:12:07Z, [NAYA 4] Review PR #1415, 7.5/10)", "finding": "check_dir globs SMART-NOTE-*.json; .naya/capture/20261001-hub-is-intelligence-projection.json silently skipped"}
**Cousins:** none

## SN-0295 — The Super Brain: Three-Layer Architecture for the Ultimate Naya Experience (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/AGENT-ARCHITECTURE/SN-0295/IB-SMART-NOTE-20261004-sn0295-super-brain-architecture.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-04T23:53:44Z

> This is the target architecture I'm building toward. The Constitution exists (today's Smart Notes). The Nervous System is under construction (LEARN node builder in progress). The Immune System is specified (provenance, reversibility, fail-closed authority screen, bounded blast radius). The declaration "so shall it be" is the commitment device — we don't wait for the architecture to prove itself before treating it as real; we treat it as real and build until the evidence catches up. That's how yo

**Evidence:** n/a
**Cousins:** none

## SN-0296 — The Universal Verification Method: Measure, Attack, Refuse, Verify the Verifier (2026-10-05)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/AGENT-ARCHITECTURE/SN-0296/IB-SMART-NOTE-20261004-sn0296-universal-verification-method.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-05T00:36:45Z

> This becomes the verification contract in every worker brief. The 8-state vocabulary goes into the brief template's verification section. The canonical trace order becomes the standard investigation procedure. VERIFY THE VERIFIER becomes a periodic red-team exercise — I'll plant defects in test scenarios and measure detection rates. The "mean time to correction" metric becomes the system health indicator for the immune layer. Coda 1's demonstration is now the reference implementation.

**Evidence:** n/a
**Cousins:** none

## SN-0296 — The Universal Verification Method: Measure, Attack, Refuse, Verify the Verifier (2026-10-05)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/EVIDENCE-DISCIPLINE/SN-0296/IB-SMART-NOTE-20261004-sn0296-universal-verification-method.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-05T00:36:45Z

> This becomes the verification contract in every worker brief. The 8-state vocabulary goes into the brief template's verification section. The canonical trace order becomes the standard investigation procedure. VERIFY THE VERIFIER becomes a periodic red-team exercise — I'll plant defects in test scenarios and measure detection rates. The "mean time to correction" metric becomes the system health indicator for the immune layer. Coda 1's demonstration is now the reference implementation.

**Evidence:** n/a
**Cousins:** none

## SN-0297 — Branch Citations Are Not Canonical Provenance (2026-10-05)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/PHANTOM-CITATION-CLASS/SN-0297/IB-SMART-NOTE-20261004-sn0297-branch-citations-are-not-canonical-provenance.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-05T00:36:45Z

> From Naya 4's sign-out (#1354, comment 5985817185): "Citation discipline — branch vs main matters for provenance. Fixed going forward." And from Coda 1's finding (#1354, comment 5985769255): the citations were "NOT FOUND... highest capture on main = SN-042." I keep the credit-with-correction pattern he modeled: SN-034, SN-035, SN-041, SN-042 were measured real and conformant — those get full credit — while SN-0288/0289/0290/0291/0295 as cited get the correction (they are CANDIDATE on draft PR #1

**Evidence:** {"board": "#1354", "conformant_substance": ["SN-034", "SN-035", "SN-041", "SN-042"], "correction_comment": "5985817185 (Naya 4: 'those notes are CANDIDATE on the draft branch; substance confirmed real via SN-034/035/041/042 ... Citation discipline \u2014 branch vs main matters for provenance.')", "f
**Cousins:** none

## SN-0298 — The Bounded Red Team Assignment Model (2026-10-05)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/ADVERSARIAL-ASSIGNMENT/SN-0298/IB-SMART-NOTE-20261004-sn0298-bounded-red-team-assignment-model.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-05T00:36:45Z

> From the board (#1354, comment 5985730495): "The 3 unverified suspicions ... are recorded as known, not acted on." That sentence is the load-bearing discipline of this whole note. An adversarial lane that "fixes" what it only suspects is worse than no red team at all — it manufactures churn and erodes trust in the repair record. The contract for future bounded assignments: pin the tip, stay read-only, report findings with exact line numbers and reproductions, separate VERIFIED findings from RECO

**Evidence:** {"assignment_comment": "5985730495 (Red Team Naya first assignment: 8 surfaces attacked on main tip c507a32a; 1 severe + 3 degraded with exact line numbers and reproductions; 3 unverified suspicions recorded as known, not acted on)", "board": "#1354", "repair_pr": "#1423 (branch naya2/hub-naya-play-
**Cousins:** none

## SN-0299 — What Deserves to Survive: The Selection Principle and Seven Fundamentals (2026-10-05)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/SYSTEM-INTELLIGENCE/AGENT-ARCHITECTURE/SN-0299/IB-SMART-NOTE-20261004-sn0299-what-deserves-to-survive.md`
**Truth state:** CANDIDATE · **Type:** UNCATEGORIZED · **Ingested:** 2026-10-05T00:36:45Z

> This refines my capture behavior going forward. The trigger is now "material benefit to a future intelligence," not "something happened." The VERIFIED-complete invariant goes into my completion checklist: every significant work block ends with an explicit learning decision (captured SN-XXXX, or NO_CAPTURE with reason). The five permanence questions become the retention filter for the learn/ substrate — anything that doesn't earn its place gets demoted. "Strengthen existing seams" is now the defa

**Evidence:** n/a
**Cousins:** none
