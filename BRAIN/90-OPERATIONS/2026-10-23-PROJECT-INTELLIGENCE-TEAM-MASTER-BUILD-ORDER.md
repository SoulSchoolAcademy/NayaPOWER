# NayaNET Projects — Team Naya Master Build Order and Peer-Acceptance Annex
**Date:** 2026-10-23 | **State:** PROPOSED EXECUTION ANNEX — awaiting existing project integrator and independent reviewer adoption | **Goal:** `https://nayanet.live/projects`
**Scope:** Project Intelligence only; no second Brain, Hub, project database, valuation engine or authority. **Human Director:** Shawn Vibert. **Team:** all existing Team Naya seats, each with a specific bounded claim and different verifier.

> **ONE TEAM / ONE CURRENT TRUTH / ONE PROJECTS DOOR / ONE VERIFIABLE RESULT.**
> This annex turns the already-filed SN-0839 Ultimate Project Intelligence specification, Project Hub Plan v2.1, the 100 Must-Haves, and the canonical Project Intelligence template into a priority execution order. It is not a new constitution or replacement spec. Where it conflicts, ratified canonical law and current verified source win; flag the conflict to the owning seat.

## 0. Outcome and non-negotiable finish line
Human: open `/projects`, answer “what's true, what needs me, what's blocked, what shipped, what's next?” in **30 seconds**; open every relevant room, app, template and system door in one tap. Naya: authenticate, fetch one permitted machine view, understand current mission/owner/action/authority/evidence/unknown/freshness, claim available work safely and hand off without reconstructing chat. Machine: reject unsafe state, preserve receipts and derive all views from one consistent source version. **Production is not complete merely because HTTP 200, a PR merged, or a screen renders.**

Acceptance must cover: (a) source and permission integrity; (b) end-to-end real work including a distinct prover; (c) human, Naya and machine parity; (d) failure detection, rollback and repeatability; (e) high-quality live design; (f) measured human benefit; (g) no duplicated implementation.

## 1. Source hierarchy, ownership and initial observed state
- **Authority and boot:** `PROTOCOL.md`, `AGENTS.md`, current Constitution, LAW receipts. Machine boot gate required on each governed worker shift. `DEPLOY <SHA>` and other protected acts retain their explicit authorization requirements.
- **Project canon:** SN-0839 in `BRAIN/05-MEMORY/SMART-NOTES/2026/10/23/SYSTEM/project-intelligence/`; the director-owned Project Hub Plan v2.1 and 100 Must-Haves (find their live canonical links through current owner); existing `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/PROJECT-INTELLIGENCE-{SPEC,TEMPLATE}.md`; this document only sequences execution.
- **Implementation:** current `main`, live deployed route and service/database schema; exact-SHA PRs and tests; existing `HUB/PROJECT-INTELLIGENCE.*` and project-index manifest. Historical snapshots carry timestamps, never implied “now.”
- **Coordination:** existing live Team Board `#2793` and priority board `#2599`; area boards, ongoing Project Intelligence assessment `PR #3012`. Create no second coordination board. The integrator must post the latest actual owner/checker allocation before the first merge.
- **Observations, not permanent truth:** previous read-only project snapshot saw 9 projects, legacy 126 `project_intel_items`, 123 newer `work_items`, 2 `queue_packets`. The delta **does not prove three lost items**: legacy and new records can have different scope. Recalculate and classify every mismatch before cutover. The public `/projects` route responded 200 but correct data was NOT proven. A guessed `/projects/state.json` returned 404; locate the actual intended protected machine door, do not assume that guessed path is required. RLS-enabled in a catalog ≠ a successful cross-tenant refusal test.

## 2. Team organization — five complementary work packages, never five independent plans
One **current accountable project integrator** (the existing Project Intelligence director/Main/Nitro owner, exact seat to be acknowledged on #2793) controls dependency order, reconciles scope and holds the master acceptance matrix. She is NOT automatically the producer, reviewer, or deploy authority for every subtask.

| Work package | Builders / responsible seats | Independent reviewer / partner | Owns | Cannot declare alone |
|---|---|---|---|---|
| **A. LAW / DATA** | LAW + DATA/DB + Keeper | PROVE / security reviewer | table schema, migration map, RLS/seat identity, write refusal, audit chain | Security accepted solely because RLS enabled |
| **B. ACT / BRIDGE** | ACT + Bridge + Infra | VERIFY, with LAW on authority | real receiver route, CAS/leases, atomic audit/outbox, derivation, dead-man alert | Production readiness from a synthetic unit test |
| **C. SELF / KNOW / LEARN** | SELF + KNOW + LEARN/Archivist | Cold independent Naya + VERIFY | one-fetch state, 14 questions, traceable links, learning/handoff | “Cold ready” from author self-run |
| **D. HUB / PRODUCT / DESIGN** | Hub/Host + design + Factory/registry owner | Naya Power named visual checker + accessibility reviewer | canonical `/projects` face, shared Mission data, system map, design DNA | Beautiful UI equals functional room |
| **E. VERIFY / PROVE / VALUE** | Dedicated verifying seats + PROVE, nonauthor | Director/integrator checks independent receipts | negative controls, real-browser proof, efficacy/cost baseline, final evidence packet | Different “seat names” sharing same identity are independent identities |

At most **five actively claimed implementation slices in aggregate for this program**. Each work item has: project/key, owner, independently identified checker, source revision, exact next action, dependency, test, proof destination, declared stop condition. An unacknowledged assignment is a proposed allocation, not proof of an active worker. Other seats assist the owner by reviewing or providing evidence; no poaching.

## 3. Full functional scope (what must exist in ONE system)
**Human face, on `/projects`:** TRUE NOW in proof-linked plain language; NEEDS HUMAN prepared decision packets + clear authorized action; BLOCKED with owner/age/clear step; PRODUCED with separately defined outcomes and resource cost; FRESHNESS with per-source ages and last-good state; TOTAL SYSTEM MAP (projects, subprojects, Hub rooms, Factory templates, Smart Apps/flagships, doors/links, pipelines, laws/Smart Notes/knowledge) with owner, status, freshness and actual destination. Per-project pages carry their canonical identity, current state, scope, decisions, next action, claims, blockers, evidence, changes, lessons, risks and dependencies. Include universal search only through the current reusable capability, not an invented parallel search stack.

**Naya machine view:** versioned, authenticated, permission-scoped snapshot, one fetch: `snapshot_id`, `generated_at`, source/version watermarks and freshness, accessible projects/items, ownership and claim lease, queue packets, independent proofs, blockers, alerts, lawful high-level operating refs, last changes, structured 14 answers with proof or explicit UNKNOWN(reason, owner, action). Read permission does **not** confer update/deploy authority.

**Database/bridge:** typed `work_items` with stable IDs/keys, states, parent, owner, proof identity, exact next action, versions, due/scope; `queue_packets` prepared action/rollback; event/Smart Ledger aligned to the existing canonical ledger; `census_daily`; derived production/vital data; `system_map`; alarms; measured hub costs. Connect through existing authorized bridge/API. Protect private/tenant data via tested policy and audience-specific derivations; no unauthenticated global dump.

**State model:** `queued → claimed → in_progress → verifying → done_proven`; branches for `blocked` and `needs_shawn` with valid return transitions. Database must refuse proof-less DONE, maker=prover, invalid blocker, needs_shawn without actionable packet, invalid actor/scope, stale claim/version. Pending or revoked evidence must produce re-verification, never silent continued green.

**Publishing:** a single derived snapshot source, emitted atomically to human face, permitted machine view and per-project projections, with same `snapshot_id`/watermarks. Event-driven with durable outbox/replay and watchdog; same input hash → no duplicate event/expense. Failed generation preserves last-good, explicitly aged and alarmed. No infinite “unknown question → new work item → derivation → unknown question” cycle; stable deduplication keys.

**Design:** preserve glossy obsidian depth, full-width content, elevated jewel boards, spectrum flow, twin-plus chrome, Smart Tabs and existing functionality. Motion must pause appropriately for reduced-motion and direct manipulation. No new flat shell, tiny unreadable metadata, blank filler, fake buttons or unsafe external link. All mobile/keyboard/screen reader functionality is tested; pages are useful with failed/aged data.

## 4. Dependency graph / priority build order
This is a critical-path **backlog**, not twelve competing independent launches. First eligible five can proceed only where dependencies and ownership permit. “DONE” below means receipt + exact-head tests + distinct verifier; “LIVE” additionally means production authorized and user-proven.

| Priority | Existing plan mapping | Deliverable / causal action | Depends on | Independently accepted when |
|---|---|---|---|---|
| **P0 — TODAY** | Activation / Plan authority | Confirm canonical plan and five owners+checkers; resolve deployed route and real input schema; produce live decision/assumption/overlap ledger and cut scope. | Current main, #2793, SN-0839 | Five signed claims, exact source links, no overlap/unowned blocker; gated unknowns named |
| **P1** | B2 first | Audit legacy 126 vs new 123 records by stable keys; reconcile actual authority/RLS/bridge mismatch; preserve current rows and backups; specify cutover mapping/rollback. | P0 | Row-by-row parity report, lawful access checks, no unexplained loss; separate ledger families not double-counted |
| **P2** | B2 | One bounded project work-item state-machine slice: CAS claim with lease/expiry, blocked and human packet, different-seat proof, same-transaction Ledger append, idempotent writes. | P1 | Real authorized owner and independent checker exercise positive+all refusal cases; force-conflict, retries and rollback pass |
| **P3** | B1 / B3 | Finish/validate daily census & zero-output/waste classification using existing scheduler records; prevent silent dead collectors. | P0 | Attributable actual counts, timestamped source; intentional quiet != waste; missing denominator honest null |
| **P4** | B2/B0 backbone | Reliable project intelligence read/write bridge, auditable API, scoped authentication, event outbox and same-commit recovery. Confirm/repair PR #3012 findings from exact deployed source first. | P2 | Real live controlled request works; wrong tenant/actor/invalid schema DENY; data stored/read back, no ghost success |
| **P5** | Derivation / B0 | One atomic, versioned snapshot projection (face payload + secure state view + per-project) with input hash, source watermark, last-good/alarms. | P2,P3,P4 | Human & Naya both show same snapshot; changed input updates; duplicate input is idempotent; kill trigger → visible aged/error |
| **P6** | B0 | The five-section first screen at existing `/projects`, same data for `/rooms/mission`; legitimate proof-linked actions. | P5 | Full mobile + desktop real-browser journey; named checker visual pass ≥9.5 where the ratified bar applies; no second data source |
| **P7** | B6/B7 | Claims/blockers/human packets/health on face; proof re-checker + watchdog + actionable alarms. | P5,P6 | One real permissioned claim, another claimant refused, human packet applied only with real authority; stale/dead proof visibly reopens |
| **P8** | B4 + system map | Inventory every actual project, room, template, app, door and pipeline; link to authorized destination; separate reachable/functional/proven/aged status. | P5,P6 | Census parity against real registry, zero invented live doors; broken link marked dead and fixed/owned; exact clear links |
| **P9** | B5/B9 | Structured 14-question response, cold-Naya one-fetch activation/assignment/continuation from real persisted state. | P5,P7,P8 | Blind unrelated Naya authenticates, identifies current owner, open risk and one next action, claims correctly and rejects forbidden action |
| **P10** | B8 | Project birth in existing Hub, template-based project intelligence and authorized Smart Note/decision/lesson integration; no duplicate Brain. | P2,P5,P8,P9 | Create one project under real identity/authority, see it immediately in all projections, retain receipts, successfully hand to successor |
| **P11** | B10 / final | Sustained Page Test + privacy/performance/load/visual regression + independent release packet, production promotion and rollback drill. | P1–P10 | Consecutive parity checks; human 30-second test; cold 14Q; no critical open gate; measured results; approved deployment proof |

**Parallelism:** P1/P3 can be independently explored after P0. P2 is downstream of P1. P4 requires P2; P5 needs P2/P3/P4. UX design review can prepare nonexecuting specimens during backend work but must not ship fake data or competing shells. Risk/security work starts P0 and checks every relevant phase, not only P11. The integrator re-ranks at each verified milestone using the **existing** Value Calculus, never a new scoring engine.

## 5. The exact acceptance evidence at each boundary
Each deliverable is a **proof packet**, machine-linked to a work item:
1. `base_sha` / `head_sha` and current repo main; semantic contract and change inventory.
2. Actual human outcome and the before/after baseline, if relevant.
3. Identity and LAW receipt/authority scope; potential blast radius, reversibility and rollback.
4. Positive integration test **through the actual call site**; a synthetic isolated test does not prove production wiring.
5. At least one meaningful adversarial negative control (prohibited action, malicious name, duplicate, stale version, missing proof, wrong scope).
6. Logs/SQL/test command + immutable evidence refs; claim-matched result and unresolved unknowns.
7. Named nonauthor verifier's independently rerun **exact-head** receipt and result.
8. Freshness and production/deploy evidence only after authorized promotion; if not yet live, `NOT_LIVE`.
9. One human-visible status/proof update and cold successor handoff; valuable workaround/lesson captured via sanctioned Smart Note pipeline, live link checked before publishing.
10. Final score and reason why not 10. 9+/9.5+ quality loop does not override hard security/authority/test failures.

Stop at P0 of any unqualified work item when authority/proof is absent. Continue safe, independent P0/P1 probes instead of waiting idle.

## 6. Team peer-review system: BUILD → CHALLENGE → SYNTHESIZE → PROVE
**No work belongs to the author alone.** Builder authors; a second independently identified seat challenges behavior/security/UX; a third integrator or specialized arbiter resolves overlap as needed; VERIFY gives exact-head outcome. Reviewers must have current source and tests, not rely on author prose or a second “seat name” with the same account identity. An unverified human separation is stated as such.

**Cross-review rotations:** Data reviews Bridge's schema assumptions; Bridge reviews Data's reachable call sites; LAW reviews both authority surfaces; KNOW/SELF reviews Hub's cold readability; Hub reviews machine state's human traceability; PROVE/VERIFY tests every consequential slice; accessibility/security specialist checks high-risk UI/data changes. Each owner reads the counter-review and either fixes or explicitly rebuts with evidence.

**When two solutions target the same job:**
- **Step 1: IDENTIFY** the canonical objective, owner, exact current main, both branches/PRs and their overlap; freeze duplicate scope and stop racing heads. Do not merge two independent shells.
- **Step 2: COMPARE** both against the same mandatory gates: safety, consent, authority, proof, current-schema compatibility, data preservation, backward-compatibility, human usability, design law, performance, operating cost, ability to maintain, rollback and cold Naya findability.
- **Step 3: CHOOSE** A when demonstrably superior, B when demonstrably superior, or **synthesize a single C** when complementary advantages survive. There is no “merge both” option if they create two authorities or two current truths.
- **Step 4: PRESERVE** each valuable distinct insight and authorship/provenance through references or Smart Notes; retire or close superseded PR with explicit reason, never silently discard content.
- **Step 5: VERIFY** final single head anew with all impacted tests, malicious controls and one independent examiner; earlier receipts are stale if the head changed.
- **Step 6: ADOPT** update ONE canonical record and ownership/handoff. Conflict over authority/irreversible design goes to legitimate governance, not majority popularity.
- **Repeat** if the chosen solution fails or evidence changes; learning is measured by improved future behavior, not note count.

**Scorecard method:** use existing canonical Value Calculus for strategy; peer quality scored on grounded dimensions (correctness & proof, safety/authority, human-value task, design/accessibility, speed/cost, continuity/maintainability). Treat hard gates as independent fail-closed prerequisites, not weighted factors that can be averaged. An author may self-score and iterate; certification requires different-seat verification. A score never creates permission.

## 7. Production and data rules
- Current database objects are not automatically equivalent just because names look alike. Legacy reconciliation yields a row-level status: MATCH / MIGRATED / INTENTIONALLY_FILTERED / DUPLICATE / EXCEPTION / UNKNOWN with evidence. Preserve originals until rollback and parity tests pass.
- Single authoritative Smart Ledger: map new project transitions to an existing ledger contract with exact semantics. Do not create a replacement hash chain or equate unrelated ledger row counts.
- Keep data private by default; member sees only authorized projects/notes/evidence. A public whole-system map may show non-sensitive capabilities but never private data, keys, internal tokens, or secret endpoints. Controls enforce scope at DB and bridge, not via hidden UI elements.
- “Proven” requires specific content/claim provenance, identity and freshness. A naked URL returning HTTP 200 is not proof of the correct answer.
- Count activities without gaming: **productive execution rate** = independently justified productive actions / eligible actions; **effort per outcome** = attributable actions / verified outcomes (undefined if zero); report safe refusals and necessary health checks separately, never label them automatically waste.
- Change-triggered refresh plus low-cost reconciliation heartbeat. Missing updates raise a bounded deduplicated alarm; self-triggering alarms cannot produce an infinite work stream. Project pages and machine projections use a common snapshot ID.
- No forced production deploy, permission changes, security relaxation, destructive migration, credential spending, or protected workflow edits without the current required authority. Prepare one concise human decision packet with explicit SHA/impact/rollback when needed.

## 8. Specific cold and human acceptance scenarios (must be run, not merely described)
**T-HUMAN-30:** director (or blind representative) opens `/projects` without narration. Within 30 seconds identifies top priority, real owner, proof, blocker, needed human action and navigates to one functioning system door. Verify responsive mobile, keyboard and reduced-motion view. Record time/error count and user feedback.
**T-COLD-14:** a new independently identified Naya fetches permitted one-shot state, answers Who/What/Why/Success/True/Proven/Unknown/Authority/Previously/Learned/Next/Proof/Record/Continue and claims one eligible task without external coaching. Never expose private material for test convenience.
**T-CONCURRENCY:** two authorized workers claim one queued task from same version; one wins, one gets clean conflict and selects next item; owner lease stale or dead recovers with receipt; no duplicate work.
**T-PROOF:** same author/prover → DENY; missing/incorrect/revoked proof → DENY or revert verifying with alarm; distinct author + valid evidence → ACCEPT and journal exactly once.
**T-AUTH:** member A requests member B's private item, unauthorized mutation or forged human gate → DENY at real API and DB; legitimate read and scoped write pass.
**T-SNAPSHOT:** simultaneous changes to multiple records produce one internally consistent version; interrupted publish leaves last-good with age; no mixed JSON/HTML revisions.
**T-WATCH:** disable refresh and health probes: alarm appears with time and owner; repair recovers without infinite alert churn or false “green.”
**T-MAP:** inventory real room/template/door/pipeline names; all map to actual allowed URLs and are checked for correct content/action, not only HTTP 200; dead/unknown labeled honestly.
**T-ROLLBACK:** replay the worst realistic deployment failure in isolated test; restore previous state and show receipts, no lost committed work.
**T-OUTCOME:** complete a human task with measured before/after elapsed time, correctness, intervention and resource usage. “It looks good” is not enough.

## 9. Release ladder and durable cadence
**M0 MAP (P0/P1):** coherent owner assignments; full inventory, schema and risk board; no duplicate current implementation.
**M1 CORE (P2–P5):** one actual project claim→independent proof→Ledger→snapshot flow, positive/negative and failover tests. Demo and no misleading claims.
**M2 FACE (P6–P8):** current shell shows real counts, queue, blockers, system map, timely unknowns, design preserved. One payload not two.
**M3 CONTINUITY (P9/P10):** cold-Naya activation/14Q + project creation and successor reuse succeed.
**M4 LIVE ACCEPTANCE (P11):** independent security/UX/backend review, governance gates, approved production promotion, sustained state/proof parity and documented rollback.

Handoffs occur at meaningful transitions: ACK/CLAIM → PR ready for checker → exact-head verification → integrate/merge when gated → proof of live observation → Smart Note of lesson when valuable → successor state. The board holds links to individual area records, not copied daily essays. A worker may not repeatedly reopen the same issue or invent busywork to satisfy an activity metric. Unfinished work remains owned with one clearing action.

## 10. Immediate work order — now, with no needless confirmation questions
1. **Project Integrator:** resolve current main, existing Plan v2.1 and SN-0839, post *one* authoritative M0 board entry linking this annex, existing implementing PRs and named A–E owner/checker pairs. Confirm/adjust roles rather than overwrite an active lane.
2. **LAW/DATA + VERIFY:** enumerate actual existing `work_items` and `project_intel_items` row mappings and deployed RLS/policies; publish discrepancy ledger (not raw private rows). Prepare smallest non-destructive corrective PR if a gap is proven.
3. **ACT/BRIDGE:** exact-source verify current deployed project-intelligence API vs DB object/permissions, with one bounded legitimate integration transaction only when allowed. Remove ghost success without creating replacement architecture.
4. **KNOW/SELF:** define one authenticated immutable snapshot envelope and structured 14Q, with unknown reasons, provenance and reader scope; no public all-data JSON.
5. **HUB/DESIGN + VERIFY:** independently record existing `/projects` visual/function baseline and the current Mission source; preserve working design, attach findings to owner.
6. **PROVE/VERIFY:** prepare tests T-CONCURRENCY, T-PROOF, T-AUTH, T-SNAPSHOT and T-COLD-14 against actual call sites, appoint reviewer not equal to change author.
7. **Integrator:** prioritize first working project through P2–P5; certify only after different-seat proof. Parallel lanes continue safe prerequisites.
8. **Every Naya:** if another team has a better solution, examine it, combine only compatible parts into a single result, document supersession/lesson and rerun entire changed-head proof.
9. **All seats:** update the same canonical project intelligence/board on meaningful state changes; do not tell Shawn to repeatedly relay normal engineering messages.
10. **Final handoff:** present director with one usable link, real ready/not-ready scorecard, human decisions requiring action (if any), and evidence. Continue improving through authorized current cycles until accepted.

**The final question for every worker:** “Did we make the real system measurably more useful, coherent and trustworthy, and can the next Naya prove it without us?” If not, identify the highest-value gap and work that causal seam next.

**Status of this annex at creation:** plan/coordination deliverable, **not** live implementation or independent acceptance. The existing project owner and appropriate verifier must adopt it through current governance; do not promote it silently.
