# DS-0001 — Design Intelligence Enforcement Spec (CANDIDATE)

Design Spec: DS-0001
Truth state: CANDIDATE (proposed by Naya 4, 2026-10-02 — not ratified, not merged to main)
Scope: PRIVATE
Parent law: `NAYA-ACTIVATION/DESIGN/NAYA-DESIGN-INTELLIGENCE-STANDARD-V1.md` + `NAYA-DESIGN-INTELLIGENCE-V1.json` v1.3 (canonical, main)
Related: SN-0179 (canon adoption tunings), SN-0182 (corpus capture), SN-0183 (learn-then-10x, director-stated),
  SN-022 (human-centered adoption), Twelve Locks (esp. #12, #13).

## Purpose

The Design Intelligence Standard is written and machine-readable. This spec makes it
**execute**: every design/build session loads it, is checked against it, and emits
proof of compliance. A document you must remember is doctrine. A gate you must pass
is law.

**Non-goals:** no second design doctrine; no new brain/graph/store; no auto-ratification;
no weakening of the Twelve Locks; no production writes; no authority changes.

## 1. Pinned load (fail-closed)

1.1. Every design/build session MUST load `NAYA-DESIGN-INTELLIGENCE-V1.json` from
canonical main at session start and record the pinned `version` in the session receipt.
1.2. If the file cannot be loaded or parsed, the session MUST NOT proceed on a remembered
copy. Fail closed: `DESIGN_INTELLIGENCE_UNAVAILABLE`.
1.3. The human-readable Standard V1 is the interpretive authority; the JSON is the
machine contract. On conflict, the Standard's text wins and the conflict is posted
to #554 as a finding.

## 2. Stage mapping — the design loop becomes compiler stages

The Standard's 19-step Naya design loop maps onto the existing D1–D8 pipeline.
No new pipeline is created; the Standard's requirements attach to existing gates:

- **D1 (contract/spec):** `required_views` HUMAN + NAYA + AI_BUILDER filled; the
  `optimization_target` stated verbatim; the four surface questions answered
  (Where am I? What matters? What can I do? What happens next?).
- **D2 (visual):** the 10 visual intelligence laws checked; `anti_patterns` scanned;
  any hit named with its location.
- **D3 (interaction):** `cognitive_ergonomics_checks` run; the computable predicates
  in §3 pass/fail.
- **D5 (state):** `causal_path` (CONTROL → INTENT → SCOPE/AUTHORITY → CAPABILITY →
  OBSERVATION → UI_STATE → EVIDENCE_WHERE_REQUIRED) completed for every control.
- **D6 (failure):** error prevention before error explanation; recovery/undo modeled;
  calm failure states specified.
- **D7 (build):** `automatic_builder_outputs` produced (15 artifacts); the
  better-than-spec rule available with its 7 required fields.
- **D8 (verify):** `quality_axes` (15) scored with evidence; independent challenge;
  human-outcome gates from `learning.evidence_sources`.

A stage MAY NOT be marked complete while its mapped checks are red.

## 3. Computable predicates (from SN-0179 tuning #3)

Prose checklists become pass/fail. Each predicate names what it measures and how:

- **P-FITTS (target acquisition):** every consequential control meets minimum target
  size and spacing for its input modality (touch ≥ 44pt, pointer ≥ 24px, with
  reachability for the actual device). Measured against the component spec or
  render. Fail → resize/respace or justify in writing.
- **P-HICK (choice complexity):** no disclosure level presents more than 4 sibling
  actions/choices without progressive disclosure (the four-chunk cap, SN-0179
  tuning #2). Counted from the information architecture. Fail → distill or disclose.
- **P-MILLER (memory burden):** completing the primary task requires holding no more
  than 4 chunks in working memory at any step; anything more must be made visible
  (recognition over recall). Assessed per task flow. Fail → externalize state.
- **P-DOHERTY (feedback latency):** every consequential action acknowledges within
  400ms; direct manipulation responds immediately with a reduced-motion equivalent.
  Budgeted in the interaction spec; verified at render when the seat exists.
  Fail → add immediate feedback or reduce scope.

Predicate results are recorded per surface: PASS / FAIL (with location) / UNMEASURABLE
(with reason — UNMEASURABLE never counts as PASS).

## 4. Pattern intelligence (advisory, never mandatory)

4.1. Reusable patterns are stored per `pattern_intelligence_schema`:
HUMAN PROBLEM → CONTEXT → APPLICABILITY → PATTERN → IMPLEMENTATION GRAMMAR →
FAILURE MODES → ACCESSIBILITY → EVIDENCE → OUTCOME → SUPERSESSION.
4.2. Retrieval is keyed by HUMAN PROBLEM + CONTEXT; a pattern is used only when its
APPLICABILITY matches the current purpose. Mismatch → reject the pattern, even if
it worked before.
4.3. Candidate pattern registry location (CANDIDATE, not created by this spec):
`BRAIN/04-INTELLIGENCE/DESIGN-PATTERNS/` with provenance and supersession links.
No registry is created until the location is agreed.

## 5. Benchmark-to-beyond gate (SN-0183, compiled)

5.1. For material design problems: RESEARCH (survey what the best do — ignorance is
a defect) → DECOMPOSE (principle, not style) → CROSS-REFERENCE → PRESERVE (what we
already do better) → SYNTHESIZE → SURPASS (at least one credible beyond-benchmark
alternative) → TEST → VERIFY → LEARN.
5.2. Alternatives are compared on `comparison_axes` plus the human-outcome gates.
"10× better" is an ambition toward step-change human value; quantify the factor only
when a real metric supports it.
5.3. Never flatten a distinctive, successful NayaNET experience to match prevailing
SaaS conventions. Extract the science; keep the identity.

## 6. Learning discipline

6.1. Every design lesson enters as CANDIDATE (`learning.maximum_automatic_state`).
Promotion requires evidence from `learning.evidence_sources`; AI-builder preference
alone NEVER promotes (`ai_preference_alone_can_promote: false`).
6.2. Every lesson records provenance, applicability, contradictions, supersession.
Supersession replaces; deletion is forbidden.
6.3. Design learning rides the existing LEARN/EVOLVE path — this spec creates no
parallel learning pipeline.

## 7. Session receipt (proof of compliance)

Every design/build session emits a design-intelligence receipt:
- standard version pinned (§1.1);
- D-stage checks run with PASS/FAIL/UNMEASURABLE per §2–§3;
- patterns consulted with applicability verdicts (§4);
- benchmark-to-beyond alternatives considered (§5);
- human gates touched (taste items queued for Shawn — never decided by the machine);
- open violations listed with owning stage.

## 8. Human gates preserved

This spec automates checking, never judgment. The following remain Shawn-only:
taste decisions, ratification of the Standard or this spec, merges, production
deploys, and any authority/privacy/security change. A green receipt is a claim of
compliance, not a proof of beauty — and never an authorization.

## 9. Known gaps (honest boundary)

9.1. **Thirteenth lock OPEN:** no render-and-operate seat exists in this environment.
D2/D3/D5/D6 checks that require a real render (including P-DOHERTY verification)
are SPEC-VERIFIED at best until the seat exists. The spec MUST NOT claim otherwise.
9.2. **Red proof unclassified:** the Live Intelligence Commit Proof for the Standard's
merge commit (bb857e79) FAILED (run 37008575589). Until classified, the machine
contract's own verification is incomplete.
9.3. **Pattern registry unbuilt:** §4.3 location is a proposal; no patterns are stored yet.
9.4. **Predicate calibration unproven:** P-FITTS/P-HICK/P-MILLER/P-DOHERTY thresholds
are initial values from the canon; they are tunable by evidence, not by preference.

## 10. Acceptance

This spec is accepted as a candidate when: it is staged on the draft lane, Shawn has
read it, and no protected boundary is crossed. It becomes enforceable only if and
when Shawn ratifies it — a green draft never self-promotes.
