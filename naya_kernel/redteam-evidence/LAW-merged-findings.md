# LAW — Merged Spec Red-Team Findings (read-only review)
**File reviewed:** `~/workspace/nine-node-specs/LAW-NODE-SPEC-CANDIDATE.md`
**Reviewed:** 2026-09-30 20:28 PDT (Naya 4, inline — no subagents)
**Review mode:** read-only per 20:10 PDT routing note; merged-spec finalization belongs to the main agent's merge-finalizing pass.
**Spec status:** CANDIDATE — NOT RATIFIED — NOT MERGED (banner intact, 18,813 bytes)
**Corpus:** `~/workspace/repo-ground/NayaPOWER` (stale copy; contract claims verified here before writing — same corpus the 19:58 tick used)

## Method
Full read of the merged spec; every external claim checked against the corpus BEFORE writing.
Checked: internal contradictions, Appendix A/B carry-forward claims vs body (merge-integrity),
GAP-A coverage, contract-law (silent extension of RATIFIED contracts), evidence floors,
consistency with the LEARN/EVOLVE quality bar.

## MODERATE

### M-LAW-01 — Acceptance battery phantom: "14 criteria stand" but are not in the body
- **Sections:** §13 vs Appendix A ("From Naya 4's draft (incl. all 15 red-team fixes): ... acceptance battery 1–14").
- **Evidence:** §13 states "Draft §13's 14 criteria stand, plus the PDF's golden proofs" — then enumerates ONLY the PDF golden proofs (§65 first behavioral proof, §66 golden negative trio, §67 golden positive). The 14 draft criteria are nowhere in the body. This includes the F14-reworded criterion #12 ("Independent verification confirms the receipt chain"), whose fix is therefore unverifiable in the merged spec. Same defect class as ACT-merged M01/M03.
- **Fix direction:** enumerate the 14 criteria in §13 (or an appendix), or restate which survive and which the PDF proofs supersede.

### M-LAW-02 — Open questions phantom: Q1–Q6 "stand" but are not stated
- **Sections:** §14 vs Appendix A ("open questions Q1–Q6").
- **Evidence:** §14 gives the six questions' TOPICS in one parenthetical (evaluation-window bound; NEEDS_AUTHORITY wait bound; director PROHIBITED-override + Judgment Rule ratification via Article XVIII; envelope-violation consequences; τ_seed briefing; refusal surfacing) but never states the questions themselves. Only Q7 is fully stated. The OPEN director decisions were dropped, not parked — including Q3(b), the Judgment-Rule ratification question the F04 fix explicitly routed to Shawn. Same defect class as ACT-merged M03 (there: Q10 dropped entirely; here: topics named, questions unstated — weaker, still a phantom).
- **Fix direction:** state Q1–Q6 verbatim in §14.

### M-LAW-03 — Interlock carry-forward is partial: no name, no preventive/detective split, no residual risk
- **Sections:** §2.1 vs Appendix A ("named interlock") vs LAW-findings.md F08 FIXED evidence.
- **Evidence:** §2.1 says "enforced by the named interlock" — but no proper name is given ("the named interlock" is a descriptive phrase, not a name). The F08 FIXED evidence claimed: "§2.1 gains the named interlock (LAW-kernel-bound verdict, ACT cannot self-issue, SELF identity-chain verification); preventive vs detective enforcement distinguished; residual risk stated." The body carries the mechanism (LAW-kernel-bound GateVerdict, ACT cannot self-issue, SELF identity-chain verification) but NOT the preventive-vs-detective distinction and NOT the residual-risk statement. §9's "ACT envelope violation → constitutional violation event, surfaced" is detective *response*, not a residual-risk statement about the interlock itself (i.e., that nothing technically prevents ACT from executing without presenting — the exact honesty F08 demanded).
- **Fix direction:** give the interlock a proper name; add the preventive/detective distinction and the residual-risk sentence the F08 fix claimed.

### M-LAW-04 — Confirmation step and PDF terminal states unmapped to the four gates
- **Sections:** §3 (evaluation order) vs §9 (failure taxonomy) vs §16 (state machine) vs Appendix B #4.
- **Evidence:** §3's evaluation order ends "...evidence floor → confirmation → ADMISSIBLE + envelope" — but "confirmation" is never defined: who confirms, within what bound, what happens on timeout, what a confirmation attaches to. §16 lists REQUIRES_CONFIRMATION as a terminal state, yet no section defines its emission rule. Appendix B #4 declares the PDF's terminal states (AUTHORIZED, DENIED, REQUIRES_CONFIRMATION, AMBIGUOUS, EXPIRED, REVOKED, OUT_OF_SCOPE) "COMPATIBLE" with the draft's four-gate verdict enum — but the body never gives the mapping. §9's taxonomy adds DEFERRED and INCONCLUSIVE, which likewise have no gate assignment (is INCONCLUSIVE NEEDS_EVIDENCE? is DENIED PROHIBITED? is AUTHORIZED ADMISSIBLE?). The compatibility is asserted in the appendix, not specified in the body.
- **Fix direction:** define the confirmation step (confirmer, bound, timeout → which gate) and publish the taxonomy→gate mapping table.

### M-LAW-05 — VERIFY backstop named but not operationalized
- **Sections:** §9 ("LAW's own compromise → VERIFY-node (separate custody) recomputation mismatch → halt") vs LAW-findings.md F14 FIXED evidence.
- **Evidence:** The F14 FIXED evidence claimed the independent recomputer was named "with access path." The merged body names VERIFY with separate custody but gives no trigger (continuous? sampled? on-demand?), no cadence or sampling rule, and no access path (how VERIFY reads GateReceipts + the pinned constitution). A backstop with no trigger is a sentence, not a mechanism. §11's `recompute(receipt)` defines the function signature but not who calls it or when.
- **Fix direction:** specify trigger/cadence (or sampling policy with rationale) and VERIFY's read path to receipts + pinned constitution.

### M-LAW-06 — floor_k provisional status is stale against the spec's own V2.1 account
- **Sections:** §3 ("hard-stop epistemic floor at config `law.evidence.floor_k` (provisional until V2.1 ratified)") vs §15 + Appendix B #2.
- **Evidence:** §15 and Appendix B #2 record the V2.1 binding as merged into main via #1186/#1190/#1192 (director-authorized; verified against live main 20:08 PDT). §3 still conditions the floor on "until V2.1 ratified" — a status the spec itself says is past. The config key's basis is now orphaned: either bind `law.evidence.floor_k` to the ratified V2.1 evidence-floor machinery (with the actual key/value or derivation rule), or restate precisely what remains provisional and why ratification didn't settle it.
- **Fix direction:** update §3 to the post-ratification state; resolve the floor_k basis.

## MINOR

### M-LAW-07 — "CONTRACT-class" is not a ratified intelligence class
- **Sections:** §5 ("The contract itself is governed (CONTRACT-class+, ratification required)").
- **Evidence:** The five ratified intelligence classes are CORE / REUSABLE / CONTEXT / REFERENCE / EPHEMERAL (ratified 2026-09-30; corpus SN-011 proposes the same five). "CONTRACT-class" is not among them. This is candidate-internal terminology, not a silent contract extension — but it risks confusion with ratified law.
- **Fix direction:** classify under one of the five ratified classes, or explicitly propose CONTRACT as a sixth class.

### M-LAW-08 — §12 endpoint node types are candidate modeling; selector-exclusion claim unreferenced
- **Sections:** §12.
- **Evidence:** The five mapped edge types (CONTRADICTS, INVALIDATES, DEPENDS_ON, AUTHORIZED_BY, SUPERSEDES) are all verified present in the RATIFIED V2 22-type enum (corpus: `BRAIN/04-INTELLIGENCE/GRAPH/0003-GRAPH-RELATIONSHIP-CONTRACT-V2.json`, status RATIFIED) — the F01 fix stands. But the endpoints (proposal/article/grant *nodes*) are the spec's own candidate graph modeling: no node-type schema exists in the corpus to reconcile against, so this is flagged for implementation reconciliation, not filed as a violation. Separately, "Revoked grants' AUTHORIZED_BY edges are excluded from validation by the V2 selector automatically" asserts selector filtering semantics (plausible via `allowed_status: REVOKED`, but unreferenced to the selector's actual filter rules).
- **Fix direction:** reconcile endpoint node types with the knowledge-node schema at implementation; cite the selector's revocation-filter rule or soften "automatically."

### M-LAW-09 — "Constitution Custodian" role named but undefined
- **Sections:** §11 ("ratification receipt → Constitution Custodian → pin-update receipt").
- **Evidence:** F11's fix introduced the Custodian as the pin-update actor; the merged spec never defines what holds the role (human office? node? key-holder?) or how it is appointed/rotated. The pin-advance procedure names an actor without an identity.
- **Fix direction:** define the Custodian (type, appointment, rotation, compromise handling).

## Explicitly checked — no finding
- **Contract-law (§12):** all five mapped edge types verified in the RATIFIED V2 22-type enum before writing; the four purpose-built types are filed as an explicit amendment *proposal*, not a change. No silent extension. F01 fix preserved.
- **Tier 0 hard stops:** "harm, illegality, evidence destruction, broken trust" grounded in `CONSTITUTION/0002-JUDGMENT-RULE-PRIME-DIRECTIVE-V1.md` §2.3 ("harm to people, illegal acts, destruction of evidence, breaking trust"). Precedence chain "HARD STOP > informed principal decision > literal instruction" matches 0002 §3.3 verbatim.
- **F02/F03/F04 fixes preserved:** no false constitutional attributions in the merged spec — gate structure not claimed constitutional; zero-tolerance labeled CANDIDATE argument (VI.3+XIV+XVI composition); Judgment Rule labeled director-stated, refusal grounded in ratified articles, hierarchy "Constitution > director instruction > all other principals" intact (§3).
- **F06 (SUSPENDED), F07 (per-proposal vs subsystem failure split), F09 (bundleId + re-bundle authority), F10/F15 (grant criteria a–f, explicit grantee, delegation chains), F12 (floor_k config key), F13 (INTAKE_REFUSED as receipt-level status):** all present on disk in the merged body.
- **GAP-A:** all 8 elements present — responsibility (§1–2), ownership (§5), sync/async (§4), persisted transitions (§6), evidence (§3.5 + §7), authority (§8), failure propagation (§9), cold reconstruction (§11).
- **SmartLedger `law` stream (§7):** treated as a candidate proposal, not a silent extension — no ratified stream set exists in the corpus to violate; consistent with the 20:18 ACT treatment of the `execution` stream.
- **Appendix B resolutions #1–#5:** consistent with the body except where filed above (B #4's compatibility claim is the subject of M-LAW-04).
- **Evidence floors:** no statistical claims in the spec; floor_k honestly labeled provisional (modulo M-LAW-06 staleness).

## Score
**Merged LAW: 7.5/10** (was reconciled draft 8.5/10). Same profile as merged ACT (7.5/10): the PDF machinery is real value and the F01–F15 fixes largely survived the merge, but the carry-forward appendices overclaim what the body contains (M-LAW-01/02/03/05) and two depth gaps need spec work (M-LAW-04/06). Rises to ~8.5 once M-LAW-01–M-LAW-06 are fixed. All 9 findings are OPEN — reconciliation belongs to the merge-finalizing pass (main agent's lane), not this worker.
