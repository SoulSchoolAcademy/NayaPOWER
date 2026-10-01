# Skeleton merge-decision audit — 2026-10-01 20:38 PDT tick (Naya 4, read-only)
Purpose: audit the 6 merge-decision/skeleton docs' claims against the redteam findings
files, the PDF extracts, and the primary corpus. Per body §3b the review pass is
read-only; all findings stay OPEN for the merge-finalizing pass.

Routing (20:45 PDT directive, in MEMORY): the canonical page is the BRAIN 0002s
(PR #1224 — "node master specs 2-9 CANDIDATE"); builder specs/ retires as parallel
tree; Naya 4 deltas return as AMENDMENTS to the 0002s. These findings are amendment
inputs, not spec edits. #1224 does not merge until both lanes' corrections fold in.

Banner check: all 6 files carry "CANDIDATE — NOT RATIFIED — NOT MERGED" (EVOLVE adds
"— NOT PRODUCTION"). Verified by full read, 20:38 PDT. No spec files edited.

## PROVE (6,545B) — carry-forward faithful, no new findings
- P-1 CHECKED, no finding: "all 16 red-team findings reconciled, App. A" — verified
  against hidden_files/redteam/PROVE-findings.md: all 16 entries marked FIXED with
  Appendix-A evidence; merge-table carry-forward claims map onto real findings
  (G5 anti-theater = §3.5/F11 independence criterion; G7 staleness/F06 prematurity;
  k=5/20 floors/F02; forecast crossing/F03; VERIFY prerequisite/F04; raise-level/F08;
  materiality/F09; battery invalidation/F12; ownership/F13; seal-to-cross/F14;
  method-finding scope/F15; briefing mechanics/F16).
- Skeleton §-list is a carry-forward assertion (base body unrecoverable — confirmed
  20:18 tick); its claims are consistent with the findings file.

## LEARN (12,289B) — 1 MODERATE
- L-1 MODERATE — OPEN: A1 adopts PDF §6's four-axes epistemic state
  (CANDIDATE/TESTING/SUPPORTED/VERIFIED/CONTRADICTED/REJECTED/SUPERSEDED) without the
  amendment-proposal flag the base's F01 fix requires. Evidence: LEARN-findings.md F01
  reconciliation covered only `LEARNED / CONTRADICTED / SUPERSEDED / INVALIDATED`
  (+ relationship types LEARNED_FROM/…/LEARN_PROMOTED) as the amendment proposal.
  VERIFIED (and TESTING/REJECTED/CANDIDATE/SUPPORTED as epistemic values) are new
  enum values over the ratified V2 contract adopted as candidate *terminology*, not
  flagged as constitutional touch — an F01-class regression in the merge. PDF §6
  verified in pdf-text/8-LEARN.txt (lines 116–126) — faithful to the PDF, but the
  base's F01 discipline was not carried. Also: SUPPORTED as a learning's persistent
  state overlaps PROVE's ceiling semantics (PROVE-F01: PROVE's ceiling is SUPPORTED).
- L-2 CHECKED, no finding: A12's investigation placeholder preserves base §1.1
  ("never consumes unverified") for consequential transitions; visibility parked in Q8.
- L-3 CHECKED, no finding: C1/C2/C5/C6 contradiction resolutions consistent with
  findings (F04 ratified-calculus gate, F01 amendment proposal, F05 extraction
  contract, F06 named functions).

## EVOLVE (14,041B) — 2 MODERATE
- E-1 MODERATE — OPEN: claims base "red-teamed and fully reconciled (6 findings
  FIXED, 8.5/10)". Evidence law: NO EVOLVE-findings.md exists on disk and the
  overnight checklist has EVOLVE unreviewed. Memory confirms a conversation-time
  review ("drafted + reviewed", Naya 4 node-spec report) but there is no persisted
  per-finding FIXED artifact. The claim may be true, but it is UNVERIFIABLE from
  artifacts — the merge-finalizing pass must not inherit the 8.5/10 score without
  the findings artifact. Same class as K-1.
- E-2 MODERATE — OPEN: stale V2.1-caveat. C3 conditions gate references "on
  ratification (SPEC-ONLY until ratified)"; the doc's lineage treats V2.1 as
  CANDIDATE (#1185). Evidence: V2.1 RATIFIED via #1186 (82793cc) + #1190 (ade50c06),
  verified against live main 20:08 PDT tick. memory/2026-09-30.md#L1599 explicitly
  instructs: treat those status statements as stale draft text. Same class as
  M-LAW-06. The A-amendments and C-resolutions conditioning behavior on "a ratified
  calculus" need re-basing onto the ratified V2.1 before lock.
- E-3 CHECKED, no finding: A15 routes pointer holes as repair debt (not spec);
  A1/Q7 keep mission-immutability candidate + director decision; C1/C2/C3
  resolutions explicitly reasoned; no silent contract extensions in the merge
  decisions.

## KNOW (5,679B) — 1 MODERATE
- K-1 MODERATE — OPEN: claims base was "red-teamed + reconciled" 8.5/10. NO
  KNOW-findings.md exists; the 18:52 tick recorded only LEARN/PROVE findings
  surviving. The base body is unrecoverable (overwritten 20:14 PDT), so per-section
  "mine (§N)" carry-forward references (§4 taxonomy, §2 V2 mapping, §8 lifecycle,
  §7 refusals, §11 evidence, §12 battery, §14 non-goals) cannot be checked.
  Per evidence law: UNVERIFIABLE claim — must not be trusted as review evidence.
- K-2 CHECKED, no finding: "PDF has no classification taxonomy at all" —
  0 matches for intelligence-class terms in pdf-text/4-KNOW.txt. "My draft's
  'never delete' was unimplementable absolutism" is an honest admission, not a
  hidden claim.

## CONNECT (9,998B) — 1 MODERATE
- C-1 CHECKED, no finding: §1 scope decision VERIFIED against master contract
  (~/workspace/repo-ground/NayaPOWER/NAYANODE/00-CONNECT-MASTER-CONTRACT-V1.md):
  "RESPONSIBILITY: relationships, graph context" (line 5); required functions
  include create_edge (line 19) … reconcile_graph (line 30); §8 verbatim:
  "KNOW owns objects. PROVE supports trust. VERIFY can establish CAUSED
  relationships. ACT consumes context." The ruling that N4's NayaNET extension
  "exceeds the master contract's stated responsibility" is evidence-backed; the
  NayaNET material is preserved as candidate Appendix A, not smuggled.
- C-2 MODERATE — OPEN: §3 caveat "V2.1 is CANDIDATE (#1185), not ratified law —
  all calculus references in this spec are aspirational until ratification" is
  STALE (same evidence as E-2/M-LAW-06). Re-base onto ratified V2.1 at lock.
- C-3 CHECKED, no finding: §19 two-stage applicability interpretation explicitly
  labeled CANDIDATE-interpretation requiring ratification — honest labeling, no
  silent extension of the ratified V2 contract.

## VERIFY (11,117B) — 2 MODERATE
- V-1 MODERATE — OPEN: §2 caveat "window lengths follow the CANDIDATE calculus
  schedule … director-set until V2.1 is ratified; all V2.1 state references in this
  spec are aspirational" is STALE (same evidence as E-2/C-2/M-LAW-06).
- V-2 MODERATE — OPEN: §4's downgrade-pressure refusal cites the Judgment Rule as
  "Prime Directive, ratified 2026-09-30". Evidence law: no ratification instrument
  for the Judgment Rule is on record; it is director-stated (Shawn, 2026-09-30) and
  elevated to Prime 1 in this workspace's AGENTS.md — not ratified law. Same class
  as LAW-F02/F03 (false constitutional/ratiﬁcation attribution). Cannot determine
  from artifacts whether the skeleton or the lost base introduced the label.
- V-3 CHECKED, no finding: §8 intelligence-class rule and §5 CVO-schema-hole
  directive are explicitly candidate/director-routed; no silent authority claims.

## Cross-cutting
- X-1: the 6 skeletons' merge decisions are largely faithful carry-forwards where
  checkable (PROVE fully, LEARN/EVOLVE/KNOW/CONNECT/VERIFY partially). The
  recurring defect classes across this audit mirror the merged ACT/LAW reviews:
  stale V2.1-caveats (M-LAW-06 family: C-2, V-1, E-2) and unverifiable carry-forward
  claims (M01/M02/M-LAW-01/02/03/05 family: K-1, E-1).
- X-2: no merge decision silently extends a RATIFIED contract except L-1
  (LEARN epistemic axis). All other contract touches are labeled candidate,
  proposal, or director-routed.

Audit scorecard (merge-integrity, not final spec scores — finals need the
merge-finalizing pass):
PROVE: claims audit-clean | LEARN: 1 MODERATE | EVOLVE: 2 MODERATE |
KNOW: 1 MODERATE | CONNECT: 1 MODERATE | VERIFY: 2 MODERATE.
