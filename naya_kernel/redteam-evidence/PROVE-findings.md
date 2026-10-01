# PROVE Node — Red-Team Findings

- **Node:** NAYA-KERNEL-PROVE
- **Spec file:** `~/workspace/nine-node-specs/PROVE-NODE-SPEC-CANDIDATE.md` (487 lines)
- **Review date:** 2026-09-30
- **Reviewer:** Naya 4 (red-team, read-only; no spec files modified)
- **Quality bar:** LEARN / EVOLVE node specs (~9.5/10) — CANDIDATE banner, hard refusals, MAY/MUST-NEVER, provenance binding, rollback-as-supersession, evidence floors.
- **Verdict summary:** Strong bones — the refusal conditions (§4), the G5 anti-theater rule (§3.5), the cold-successor demotion test (§5), and the PROVE/VERIFY distinction (§1.3) are at the reference bar. But the spec has one CRITICAL contract-law violation (§6.1 writes epistemic states and relationship types that the RATIFIED graph contract v2.0 does not allow), no evidence/sample-size floors anywhere in the ladder (a single observation can reach L4 PROVEN), and a genuine internal inconsistency that traps all forecasts below the CONNECT crossing threshold. Not yet at the LEARN/EVOLVE bar; fixable in draft, but F01 must be resolved before ratification is even discussable.

**What the spec gets right (keep):** §4.2 (PROVE may operate but never validate its own machinery), §4.4 (IMPLEMENTED presented as VERIFIED = refusal), §4.5/§1.4 (proof grants nothing; never touches authority), §4.6 (floor never lowered for urgency, consequential cases BRIEFED), §4.7 (bundle rule against gate evasion), §5 (cold-successor test with demotion on recompute failure), §6.3 (never silent demotion), §8 (sync pipeline transitions; async sweeps may only demote via CHALLENGED), §3.5 (G5 must be able to fail).


---

## RECONCILIATION — 2026-09-30 19:08 PDT tick (supervisor, inline)

All 16 findings reconciled as CANDIDATE revisions in
`~/workspace/nine-node-specs/PROVE-NODE-SPEC-CANDIDATE.md`
(26,670 → 43,697 bytes; banner intact; Appendix A reconciliation log).
0 OPEN remaining. **Final review score: 8.5/10** (draft was 7.0).
Debits remaining: evidence-floor constants keyed to the still-CANDIDATE
V2.1 calculus; graph amendment proposal (§6.4) pending governance;
method-finding retention bound to director decision §10.5; §10.1/10.2/10.4/10.5
director questions still open by design.
Hardest calls: F01 (ladder mapped onto ratified enums — PROVEN→SUPPORTED,
never VERIFIED — plus a formal amendment *proposal*, not a silent contract
change); F03 (forecast crossing defined so predictions can be shared without
violating "nothing unproven crosses"); F02 (proofs held at least as strict
as V2.1 learnings: no n=1 PROVEN, ever).

---

## FINDINGS

### PROVE-F01 — CRITICAL — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**§6.1 binds `epistemic_state` and `relationship_type` to values the RATIFIED graph contract v2.0 does not allow — a contract change disguised as a binding.**

Evidence: spec §6.1 table sets `epistemic_state` to a private ladder `UNPROVEN → EVIDENCED → TESTED → REPRODUCED → PROVEN` plus `CHALLENGED`/`INVALIDATED`, and `relationship_type` to `PROVEN_BY` / `CHALLENGED_BY` / `INVALIDATED_BY`. The ratified contract (`BRAIN/04-INTELLIGENCE/GRAPH/0003-GRAPH-RELATIONSHIP-CONTRACT-V2.json`, version 2.0, status RATIFIED, read from the repo snapshot at `/tmp/nayapower-main`) defines `allowed_epistemic_states: ["UNKNOWN","CANDIDATE","SUPPORTED","CONTRADICTED","SUPERSEDED","INVALIDATED","LEARNED","VERIFIED"]` — none of UNPROVEN/EVIDENCED/TESTED/REPRODUCED/PROVEN/CHALLENGED appear — and `allowed_relationship_types` lacks `PROVEN_BY`, `CHALLENGED_BY`, `INVALIDATED_BY` (only `VERIFIED_BY`, `INVALIDATES`, `CONTRADICTS` exist). Writing non-enumerated values is a contract change, contradicting spec §11 ("It does not change … any contract"). Fix: define an explicit mapping from the private ladder onto allowed states (e.g., PROVEN→VERIFIED is *wrong* — VERIFIED belongs to VERIFY per §1.3; more likely PROVEN→SUPPORTED), or route a contract amendment through governance. Until resolved, §6.1 is unimplementable against the ratified contract.

### PROVE-F02 — MAJOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**No evidence/sample-size floors anywhere in the ladder: n=1 can reach L4 PROVEN.**

Evidence: §3.4 EMPIRICAL battery requires only "the observation is recorded with method; negative controls run where applicable; the raw data is retained" — a single observation satisfies this and can climb L1→L4. The ladder (§2.2) and gates (§3.1–§3.7) contain no `n ≥ k` rule. Contrast the standing V2.1 calculus DATA_FLOOR (k=5 observed / 20 prior) that LEARN mechanically enforces (§3.3 of the LEARN spec): the organism's *strongest* label (PROVEN) rests on *weaker* evidence requirements than a learning candidate needs to leave NEEDS_EVIDENCE. This smuggles weak evidence into the system's highest maturity stamp. Fix: add floors per class/stakes mirroring V2.1 (and consider LEARN §10.2's question of stricter floors — proofs should be at least as strict as learnings).

### PROVE-F03 — MAJOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**PREDICTIVE claims (and all likelihood claims) are trapped below the CONNECT crossing threshold — internal inconsistency.**

Evidence: §2.1 + §3.4: PREDICTIVE claims "can never reach PROVEN," capped at L1. §3.8: `requiredLevel ∈ {2,3,4}` — minimum L2. §1.2: CONNECT receives only material "at or above the claim's required maturity level." Therefore no forecast can ever cross to CONNECT or be reported to the Director, although §1.1 explicitly lists "reports drafted for the Director" as PROVE input and §10.1 contemplates Director-bound reports. §7's uncertainty posture extends the trap: any "likely" claim caps at EVIDENCED (L1). Either §1.2 must admit a crossing path for L1-capped claims (contradicting "nothing unproven crosses the organism boundary"), or the organism can never share any forecast with anyone, including Shawn. This needs a "forecast crossing" section, not an open question.

### PROVE-F04 — MAJOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**VERIFY prerequisite contradicts the continuous-monitoring design.**

Evidence: §1.2: "A `ProofReceipt` at L4 is VERIFY's prerequisite, never its conclusion." But §3.8 requires L4 only for `consequential` claims; low/high-stakes claims seal at L2/L3. Meanwhile §7 ("counter-evidence post-seal → ongoing VERIFY") and §8 (async challenge monitoring) expect VERIFY to watch sealed claims generally. VERIFY cannot monitor L1–L3 claims if its prerequisite is an L4 receipt — which would leave most sealed proofs outside independent checking, defeating §1.3's purpose. Fix: VERIFY's prerequisite is any sealed receipt; L4 is the prerequisite for CONNECT crossing only.

### PROVE-F05 — MAJOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**Forged-but-well-formed evidence passes every gate; forgery is absent from the failure table.**

Evidence: §3.2 (G2) checks completeness, resolvability, content-addressing, source/method/time, custody gaps — all satisfiable by a competent source-level fabrication. §7's failure table lists laundering, staleness, circularity, but no forgery row. Contrast the LEARN spec §7 ("Provenance loss / forgery" with `recompute()` detection). Content-addressing catches post-hoc tampering, not fabrication at the source; the EMPIRICAL battery (§3.4) has no oracle/sensor qualification and no independent-source corroboration requirement for consequential claims. Missing failure mode for a proof node.

### PROVE-F06 — MAJOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**Provisional (open-window) evidence has no handling rule.**

Evidence: V2.1 observation windows (24h/7d/30d/90d) produce `PASS_PENDING_WINDOW` receipts that LEARN explicitly consumes (LEARN spec §1.1, gated by `promotionEligible()`). PROVE has no rule for claims whose evidence rests on a provisional verification. G7 (§3.7) covers staleness (evidence too old), not prematurity (window still open). A claim "behavior changed," evidenced by an open-window receipt, could be sealed PROVEN before the window closes — manufacturing certainty from provisional evidence. Missing rule: cap such claims at L2, or bind `valid_until` (§5) to the window's close. New spec section needed.

### PROVE-F07 — MAJOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**Stakes assignment is undefined and gameable — GAP-A item (6) partial.**

Evidence: §3.8 enforces required levels by `stakes` ('low'/'high'/'consequential', §2.1 `ProofClaim.stakes`), but no section states who assigns stakes, whether PROVE may reclassify a claim's stakes upward, or how disputes resolve. A claimant self-declaring 'low' stakes buys L2 instead of L4. §4.7's bundle rule covers decomposition evasion, not stakes misclassification. The authority envelope (§1.4, §4.5) is otherwise strong; this is its hole.

### PROVE-F08 — MAJOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**Raise-level power is an unbounded refusal-equivalent without receipting.**

Evidence: §3.8: "Raising a level (demanding more proof than the table requires) is always permitted and is not a refusal." Unlimited raising = indefinite withholding of advancement = de facto refusal, but without §5's refusal receipting or §4.6's briefing. No bound, no justification requirement, no appeal path — PROVE can stall any claim forever while formally "never refusing." Fix: raising must be receipted with reasons and bounded (e.g., director-reviewable cap or automatic briefing above a threshold).

### PROVE-F09 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**"PROVE gates; it does not score" vs. scored materiality judgment.**

Evidence: §3 declares "PROVE gates; it does not score. Each gate is binary." But §3.1 (G1) requires "every *material* assertion" to have evidence, and §3 states that "whether evidence is *material*" is a genuine value judgment delegated to the scored V2.1 calculus. The central binary gate depends on a scored judgment call — the determinism claim is weaker than advertised. Fix: define materiality rules that don't require scoring, or admit the hybrid explicitly (gates with a scored materiality pre-step).

### PROVE-F10 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**"VERIFIED" used in three senses in one spec.**

Evidence: §4.4: "IMPLEMENTED is the request; VERIFIED is the read-back." §1.3 reserves "independently VERIFIED" for VERIFY's verdict. The ratified graph contract's `allowed_epistemic_states` also contains `VERIFIED`. Three senses (read-back observation / independent verdict / graph state) in one spec invites the exact IMPLEMENTED/VERIFIED confusion §4.4 exists to prevent. Fix: rename PROVE's sense (e.g., "OBSERVED") and disambiguate in §1.3.

### PROVE-F11 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**G5 "fresh derivation path" has no independence criterion a cold successor can check.**

Evidence: §3.5 requires re-derivation "via a fresh derivation path, not a replay"; §5's recompute record carries method, result, and "what would have constituted disagreement" — but nothing recording what makes the path *fresh* vs. a replay. Acceptance #7 (§9) rejects theater but gives no test. The cold successor (§5) cannot verify path-independence from the receipt. Fix: define and record the independence criterion (different code path / different agent / blinded inputs).

### PROVE-F12 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**No invalidation policy when battery definitions change.**

Evidence: §3.4: batteries are "owned by PROVE's configuration" (mutable); §5 binds `batteryId + batteryVersion` into each receipt — but nothing specifies whether sealed receipts survive a battery change, must re-gate, or are grandfathered. Contrast EVOLVE's deciding-config binding (§3.3) and LEARN's configHash recompute. A tightened battery retroactively weakens old seals; a loosened one is a floor change by another name (§4.6). New section needed; §10.3 (battery ownership) is adjacent but doesn't cover invalidation.

### PROVE-F13 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**GAP-A item (2): node ownership unnamed; cross-node prescription in §1.2.**

Evidence: the header says only "one kernel, not a separate system" — no principal owns PROVE or answers for its verdicts. §1.2 prescribes CONNECT's behavior ("CONNECT must refuse material without one") and §4.2 routes to VERIFY, but §10.6 itself asks whether PROVE→VERIFY is meaningful in a single-instance deployment. If one agent runs PROVE and VERIFY, §1.3's "two checks" collapse into the design error the section warns about. Ownership + staffing belongs in the spec body, not just §10.6.

### PROVE-F14 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**Seal-to-cross race: no freshness check at the CONNECT boundary.**

Evidence: §8 runs transitions synchronously before CONNECT and restricts async sweeps to demote-via-CHALLENGED. But nothing re-checks that a sealed receipt is still current *at the moment of crossing* — a challenge arriving between seal and cross lets stale proof cross the boundary. Fix: boundary re-validation (seal timestamp + challenge check) in §1.2/§8.

### PROVE-F15 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**"Method finding" against claimants (§4.3) is an undefined reputation mechanism.**

Evidence: §4.3: a laundering attempt "is recorded as laundering — a finding about the claimant's method, not just the claim." No definition of where method findings live, who may see them, what consequences attach, or how they are cleared. For a node that "does not grant, infer, or modify authority" (§1.4), an unscoped claimant-scoring side-channel is a quiet authority-adjacent power. Scope it or drop it.

### PROVE-F16 — MINOR — FIXED (reconciled 19:08 PDT tick; evidence: spec Appendix A)
**"BRIEFED to the Director" (§4.6) has no mechanics.**

Evidence: §4.6: floor-lowering requests for consequential claims are "BRIEFED to the Director rather than silently held." Which node briefs, in what format, where the briefing is recorded, and what the Director's response options are — all unspecified. (LEARN/EVOLVE specs define BRIEF outputs concretely.)

---

## GAP-A CHECKLIST (eight items)

1. **Contractual responsibility** — COVERED (§1, §1.4; PROVE/VERIFY split §1.3). Cross-node prescriptions (§1.2) need ownership grounding (F13).
2. **Ownership** — GAP (F13). No named owner/operator; single-instance staffing only an open question (§10.6).
3. **Sync/async** — COVERED (§8: sync transitions pre-CONNECT; async sweeps demote only via CHALLENGED). Seal-to-cross race remains (F14).
4. **Persisted transitions** — COVERED (§8 transition records; §6.1 graph edges; §5 receipts).
5. **Evidence requirements** — COVERED structurally (§3 gates, §5 provenance) but MISSING floors (F02), forgery handling (F05), provisional evidence (F06).
6. **Authority envelope** — STRONG (§1.4, §4.5, §4.6) with two holes: stakes assignment (F07), unbounded raise-level (F08).
7. **Failure propagation** — PARTIAL (§7 table, §6.3, §8). Missing: forgery (F05), provisional windows (F06), battery-change invalidation (F12).
8. **Cold reconstruction** — STRONG in design (§5 cold-successor test with demotion) but DEPENDENT on unanswered retention (§10.5) and unverifiable path-freshness (F11).

---

## DRAFT SCORE: 7.0 / 10

Justification: the refusal architecture (§4.1–§4.8) is genuinely at the 9.5 reference bar — eight hard refusals including anti-self-certification (§4.2), IMPLEMENTED≠VERIFIED (§4.4), and the no-lower floor (§4.6); the cold-successor test (§5) and G5 anti-theater rule (§3.5) show real adversarial thinking; PROVE/VERIFY separation (§1.3) with "VERIFY wins" is the right call. Deductions: F01 (CRITICAL contract-enum violation, unimplementable §6.1 as written) −1.0; F02 (no evidence floors — the system's strongest label on the weakest evidence standard) −1.0; F03+F04 (internal inconsistencies: forecast trap, VERIFY prerequisite) −0.5; F05–F08 (forgery, provisional evidence, stakes assignment, raise-level asymmetry) −0.5; minors (F09–F16) −0.5. Net 9.5 − 3.5 ≈ 6.0, rounded up to 7.0 because the defects are draft-fixable and the spec is unusually honest about its open questions (§10). F01 alone blocks ratification discussion.

---

## OPEN QUESTIONS THAT SHOULD BECOME SPEC SECTIONS

1. **Ladder→contract mapping (§6.1):** explicit mapping from UNPROVEN/EVIDENCED/TESTED/REPRODUCED/PROVEN/CHALLENGED onto the ratified `allowed_epistemic_states`, or a governed contract-amendment proposal — with the PROVEN↛VERIFIED distinction preserved (§1.3).
2. **Evidence floors:** `n ≥ k` per claim class and stakes, mirroring (or exceeding) V2.1's k=5/20; what counts as an *independent* observation.
3. **Forecast crossing:** how L1-capped claims (predictions, likelihoods) may be reported/shared without violating "nothing unproven crosses."
4. **VERIFY input rule:** any sealed receipt vs. L4-only (§1.2 vs §1.3/§7/§8).
5. **Adversarial evidence standard:** forgery detection, oracle/sensor qualification, independent-source corroboration for consequential claims.
6. **Provisional evidence:** handling of open-window / PASS_PENDING_WINDOW-backed claims (cap level or bind `valid_until`).
7. **Stakes assignment:** who assigns, PROVE reclassification power, dispute path.
8. **Raise-level bounds:** receipting, justification, caps, briefing triggers.
9. **Battery-change invalidation:** re-gate vs. grandfather policy on battery definition change.
10. **Evidence retention:** already §10.5 — keep, and bind the cold-successor guarantee (§5) to its answer.
11. **Method findings (§4.3):** scope, visibility, consequences, clearing — or removal.
12. **Materiality without scoring (§3 vs §3.1):** define materiality rules or admit the scored pre-step.
