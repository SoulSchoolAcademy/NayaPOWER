# Activation Naya — Project Intelligence View (candidate projection)
**Date:** 2026-10-09 · **Source main:** `1d73652231ac6127806640af5a31eb516c60738d` · **Status:** CANDIDATE / TEAM CONSENSUS REQUESTED.
**Not a new Brain, registry, storage system, Smart Note, authority grant or truth source.**
**Existing canonical substrate:** `public.nayanet_project_intelligence_state` (where deployed/authorized), `public.nayanet_project_intelligence_bridge`, current GitHub `main`, `.naya/capture/`, `.naya/memory/smart-notes/index.json`, BRAIN, issue #1354 and governed receipts.
**Avoid name collision:** `HUB/PROJECT-INTELLIGENCE.md` is the existing Hub design/build charter. This document is the **Activation Naya project dossier** within the existing `.naya/project-intelligence/` namespace.

## In a nutshell
A project's intelligence is a **versioned, permission-filtered view of relevant canonical intelligence**: mission; current truth; architecture/contracts; work ownership; decisions; learning; risks; Smart Notes; evidence; pending unknowns; next verified action. One lookup gives an authorized cold Naya what she needs, with source/recency/conflicts shown. It never forks intelligence or falsely elevates a draft. Smart Notes are distilled canonical objects feeding project views, **not raw data by default**, and the project view is never a new source of authority.

## Human / Naya / machine
- **Human:** one clear project home: where we are, why, what has actually changed, who owns it, what is blocked, and how to inspect the proof.
- **Naya:** read current main and contracts; retrieve only owner/scope-eligible objects through LAW/KNOW/CONNECT; rank by relevance and provenance, not recency alone; explicitly surface contradictions and supersessions before acting.
- **Machine:** `project_id`, `version`, `source_main_sha`, `mission`, `canonical_refs[]`, `intelligence_refs[]`, `decision_refs[]`, `evidence_refs[]`, `work_refs[]`, `truth_state`, `freshness`, `scope`, `conflicts[]`, `known[]`, `unknown[]`, `blocked[]`, `next_action`, `last_verified_at`. References only. Do not embed private capture into public projection.

## Activation Naya project card — sourced snapshot
| Field | Snapshot | Evidence boundary |
|---|---|---|
| Mission | Teach once; enable a new cold Naya to retrieve, understand, lawfully apply and independently prove better behavior | Director's 2026-10-09 Project Intelligence charter; do not claim achieved |
| Canonical operating law | ONE organism, nine node responsibilities, no second Brain, retrieval != authority | `AGENTS.md`; `BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.md`; `NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md` |
| Human acceptance criteria | 8 requested: fast capture; governed elevation; cold retrieval; plan context; causal behavior; execution feedback; proof; successor reconstructs | User-provided `PROJECT INTELLIGENCE FOR ACTIVATION NAYA` (2026-10-09), proposed acceptance, not all verified |
| First real specimen | T11 SN-782, `IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical` | exact registry entry in `.naya/memory/smart-notes/index.json`, truth/lifecycle CANDIDATE, PRIVATE, Smart Link ACTIVE_AUTH_GATED |
| Capture evidence | Receiver run `37980089547` fresh-lesson & independent-verification jobs SUCCESS | Proof of persist/verification only, NOT changed behavior |
| Broken handoff | Cold-successor job FAILURE `AssertionError: CANDIDATE`; downstream independent-behavior SKIPPED | Actual workflow job, not hypothesis |
| Repair work | PR #2039 current-main CANDIDATE retrieval repair; PR #2037 assembly blueprint; PR #2033 earlier candidate | Open candidate PRs at inspected snapshot; recheck before action |
| Structural unknowns | LEARN outcome status vs registry truth/lifecycle, v7 vs v2 bridge, authorized ACT influence, and second cold successor | Separate research assertions from production-proven behavior |
| Priority next action | independently qualify #2039 then conduct real owner-authorized intent retrieval, wrong lesson refusal and causally controlled ACT trial | Doer ≠ verifier; protected workflow merge governed |
| Current verdict | capture/projection proven for T11; complete learning loop NOT_PROVEN | never claim 10/10 without behavioral evidence |

## Relationship taxonomy — one project, many canonical references
1. **CONCERNS_PROJECT:** Smart Note/block belongs to Activation Naya, with source owner/scope.
2. **EXPLAINS_CONTRACT:** references the exact ratified rule (not a rewritten law).
3. **EVIDENCED_BY:** test/run/receipt supporting a narrowly defined claim.
4. **DECIDES:** recorded decision and authority; no decision invented from project metadata.
5. **OWNED_BY:** leader/seat and exact branch SHA; no fictional assignments.
6. **BLOCKED_BY:** reproducer or failed interface, distinguished from uncertainty.
7. **SUPERSEDES / CONTRADICTS:** actual canonical relationships, not inference from titles.
8. **APPLICABLE_TO:** CONNECT-qualified conditions and exceptions, never authorization.

These are conceptual projection labels; map to current registered graph edge vocabulary before writing any machine relationship. Never create a competing edge schema.

## How the existing project intelligence should become useful
- **Discovery:** start at AGENTS.md, locate this project by key, resolve current main and registry/live source; provide a single project summary with exact citations/links.
- **Composition:** read `nayanet_project_intelligence_state` and bridge only under actual owner-bound permissions; then dynamically join authorized Smart Notes, decisions, proof receipts, tasks and relationships by canonical IDs. Persist only a snapshot pointer/manifest under existing governance where useful.
- **Update:** on accepted canonical Smart Note/decision/verification/outcome, emit or consume the existing governed event; refresh or invalidate project projection on new source SHA, version or supersession. No extra writer to Brain.
- **Communication:** issue #1354 remains team feed of events/discussions; project view links decisions and proof from that feed. An assertion in the feed does not become verified truth without evidence.
- **Cold activation:** authorized successor requests “Activation Naya project state”; system reconstructs the current project card, fetches its relevant lessons and knows what not to assume. Test against fresh clone, wrong project query, unauthorized private source, stale SHA and contradicting notes.

## Consensus checklist for Naya 1/2/3/4/5
Naya 1: designate one canonical project key/owner, accept projection contract, deconflict project view from `HUB/PROJECT-INTELLIGENCE.md`.
Naya 2: independently confirm production schema/migration state and owner/RLS isolation, and prove cold reading without chat context.
Naya 3: own human display using existing Hub/one Room Socket; show verified/unknown/blocker states and links; no second Hub.
Naya 4: wire KNOW/CONNECT applicability and ACT plan reference, with LAW privacy/authority; do not embed unverified policies in SELF.
Naya 5: connect canonical capture and receipts to the project view and test updates/duplicates.
**Ratification bar:** five leaders comment on the *same* PR/issue with ACCEPT or bounded objection and evidence; independent cold project-context retrieval green. Until then this is only a reversible proposal.

## Minimum falsifiers
- Private SN-782 must not be exposed to an unauthorized project viewer.
- Changing a PR comment cannot silently mutate project truth/authority.
- Same capture linked to two projects must preserve one IB and separate permissions.
- Superseded/contradicted note cannot appear as current project instruction.
- Wrong-project query cannot retrieve the Activation Naya private lesson.
- New project view cannot create a second index, a second receipt, or a fake learned status.
- Source/main divergence visibly marks project card STALE; stale project snapshot never authorizes ACT.

## What this adds to the existing Brain
Project intelligence is a **contextual organizing lens** over Smart Notes, graph edges, live work, decisions, and receipts. It increases findability and makes collaboration actionable; it cannot, by itself, make the nine-node learning loop close. That requires actual retrieval→authorized behavior→outcome→LEARN→successor proof.
