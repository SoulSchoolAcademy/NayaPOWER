# KNOW Node — Reconciliation Draft (MERGED candidate)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED**

Merged from: (a) other Naya's `NayaPOWER___NODE_4__KNOW.pdf` (55 sections) and
(b) Naya 4's `KNOW-NODE-SPEC-CANDIDATE.md` (8.5/10, red-teamed + reconciled).
Nothing from either source dropped without a stronger replacement.
Contradictions resolved explicitly below. Draft for Naya 4's review — not final.

---

## Merge decisions (whose version won and why)

| Area | Winner | Why |
|---|---|---|
| Object name | PDF: **Intelligent Block** | Runtime-grounded ("current Intelligent Block/Receiver"); my draft's `KnowledgeBlock` becomes documented alias. |
| `class` field (5 ratified classes) | Mine (§4) | PDF has no classification taxonomy at all; CORE-never-auto-assigned unenforceable without it. |
| V2 graph edge field mapping | Mine (§2) | PDF never binds to the RATIFIED V2 contract; blocks must be provably persistable. |
| State model | **Merged**: PDF's two dimensions, my enum | PDF's separation of system status (ACTIVE/DURABLE/…) from epistemic standing is genuinely better. But PDF's understanding ladder contains VERIFIED — VERIFY's verdict (PROVE-F10 class). Persisted `epistemic_state` uses the ratified enum; PDF's CONTEXTUALIZED/INTERPRETED/DISTILLED/APPLIED become sub-states of CLASSIFIED/SUPPORTED. |
| Ingestion state machine | PDF (§10) | 17 states + fail-closed invalid transitions beats my §8; my §8 persists as the block *lifecycle* (complementary, labeled). |
| Retrieval predicate | PDF (§21) | `RETRIEVAL_ELIGIBLE` with BLOCKED>UNKNOWN>FAIL>PASS is machine-exact; feeds my §6 V2 selector gates. |
| Baton | PDF (§5) | Richer (contract version, idempotency key, previous receipt refs); my §1.2 handoff content merges in. |
| Receipt | PDF (§27) | Explicit "proves the transition was recorded, not the claim is true"; my §11 fields merge in. |
| Refusals | **Merged** | My §7's seven named refusals stand; PDF §32 quarantine categories + §31 injection formulas merge in as refusal/quarantine rows. |
| Deletion | **PDF (§33)** | PDF wins outright: epistemic forgetting vs data deletion (retention/legal) is implementable; my "never delete" was unimplementable absolutism. Legal deletion = new versioned tombstone with lineage, never silent erasure. |
| Privacy | Merged | PDF §30 private-by-default + my §7.3 consent/scope refusal. |
| Prompt-injection defense | PDF (§31) | `retrieved_authority_claim ≠ authority` formulas are crisper than my §7.4 prose. |
| V2.1 math | PDF (§§18–20) | Q/PV/C_agg≥0.80/C_critical≥0.75 already integrated with floors. |
| Handshakes | PDF (§6) | SELF→KNOW (identity/mission/owner/project/objective/state/continuity/known-unknown boundary), ACT→KNOW, KNOW→PROVE/CONNECT, VERIFY→KNOW, LEARN→KNOW — most complete. |
| Property tests | **Union** | PDF P1–P25 + my §12 battery, deduped (P12=UNKNOWN≠PASS etc. overlap and merge). |
| Golden tests | PDF (§§42–47) | Six tests incl. injection, contradiction, cold successor; my battery's unique cases appended. |
| Terminology | PDF | EVENT≠BLOCK≠NOTE≠EVIDENCE≠OUTCOME≠LEARNING (§8) adopted as canonical taxonomy. |

## Merged spec skeleton (sections)

0. Purpose — my §0 + PDF §54 one-sentence definition.
1. Responsibility & pipeline — my §1 + PDF §6 handshakes + PDF §1 (why KNOW exists).
2. The Intelligent Block (typed) — PDF §7 schema + `class` field (mine §4) + V2 mapping table (mine §2).
3. Ownership taxonomy — PDF §3 (owns) / §4 (must never own) incl. ONE BRAIN/ONE GRAPH/ONE LEARNING RIVER.
4. Classification — my §4 + §7.2 in full.
5. Ingestion — PDF §10 state machine + my §3.1 gate/§3.2 canonicalization/§3.3 dedup/§3.4 async.
6. Identity/hash/provenance laws — PDF §§11–13.
7. Temporal/supersession/duplication — PDF §§14–16.
8. Retrieval — PDF §21 predicate → my §6 selector gates; PDF §22 (KNOW owns what exists, CONNECT what matters); PDF §23 similarity≠applicability.
9. Refusals & quarantine — my §7 + PDF §§31–32.
10. Candidate intelligence, Smart Notes, raw sources — PDF §§24–26.
11. Receipts & idempotency & concurrency — PDF §§27–29.
12. Privacy & untrusted input — PDF §§30–31.
13. Deletion/forgetting — PDF §33 (two-concept model).
14. Handoffs — PDF §§34–37 batons (typed, §5 format).
15. State: block lifecycle — my §8 (labeled lifecycle, distinct from §5 ingestion machine).
16. Failure modes & uncertainty — my §9 + PDF contradiction handling.
17. Cold reconstruction — PDF §47 + my §10.
18. V2.1 math integration — PDF §§18–20.
19. Evidence emitted — my §11.
20. Acceptance battery — union of property invariants + golden tests.
21. Production-proven & influential bars — PDF §§49–50.
22. What this spec does NOT do — my §14 + PDF §4.

## Open questions for Shawn

1. Meaning-distillation (§10 MEANING_DISTILLED): PDF leaves the algorithm open. Accept "implementation-defined with P3/P17 acceptance gates," or require a specified minimum semantic schema before build?
2. RETRIEVAL_ELIGIBLE (§21): PDF asserts it exists on main. Verify commit before the build treats it as present, or build it fresh?
3. Understanding sub-states (CONTEXTUALIZED/INTERPRETED/DISTILLED/APPLIED): persist as annotations or as first-class sub-enum? (Draft: annotations.)
4. Legal-deletion tombstones (§33): who authorizes a data-deletion — Director only, or governed LAW path? (Draft: Director-only, receipted.)
5. My draft's §13 open questions carry over (contradiction reconciliation ownership, supersession pointer semantics, cross-owner sharing defaults).
