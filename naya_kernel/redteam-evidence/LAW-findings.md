# LAW Red-Team Findings — 2026-09-30 (Naya 4, inline, read-only pass)
Spec: `~/workspace/nine-node-specs/LAW-NODE-SPEC-CANDIDATE.md` (24,923 bytes, banner intact)
Status: all FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in the spec, Appendix A)
Draft review score: **7.0/10**

Corpus verified before writing findings:
- Constitution: `/tmp/nayapower-main/CONSTITUTION/0000-NAYAPOWER-CONSTITUTION-ACT-V1.md` (18 articles, RATIFIED 2026-09-30)
- Graph contract: `/tmp/nayapower-main/BRAIN/04-INTELLIGENCE/GRAPH/0003-GRAPH-RELATIONSHIP-CONTRACT-V2.json` (v2.0, RATIFIED)

## CRITICAL

### F01 — §12 writes edge types the RATIFIED graph contract v2.0 forbids (silent contract extension)
- **Sections:** §12 vs §15.
- **Evidence:** §12 proposes writing `REFUSED_BY`, `AWAITS_GRANT`, `GRANTS`, and `REVOKED_BY` edges to the intelligent graph. The RATIFIED V2 contract's `allowed_relationship_types` enum contains 22 types — `DERIVED_FROM, SUPPORTS, CONTRADICTS, DEPENDS_ON, IMPLEMENTS, GOVERNS, AUTHORIZED_BY, USED_BY, CAUSED, RESULTED_IN, VERIFIED_BY, LEARNED_FROM, SUPERSEDES, SUCCEEDS, RELATED_TO, CONTEXTUALIZES, INVALIDATES, REFINES, CORRECTS, ENABLES, PRODUCES, APPLIES_TO` — none of the four proposed types. The contract carries no amendment/extension clause; its ratification scope is "Machine contract governing Graph V2 relationship semantics" and explicitly "does not redesign the graph."
- **Contradiction:** §15 claims "It does not change the pipeline, the kernel taxonomy, or any contract." §12 changes a RATIFIED contract's effective enum.
- **Class:** same as PROVE-F01 (CRITICAL). A CANDIDATE spec must never silently extend a RATIFIED contract.
- **Fix direction:** map onto ratified enums (refusal → `CONTRADICTS` or `INVALIDATES` with the GateReceipt as provenance; grant edges → `AUTHORIZED_BY`; revocation → `SUPERSEDES`/`INVALIDATES`) or file a formal contract-amendment proposal. Note the migration_boundary: schema/column expansion is discouraged — edge-type additions are exactly what it warns against.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

## MAJOR

### F02 — §15's "the gate structure itself is constitutional" is false against the primary corpus
- **Sections:** §15 vs Constitution Act V1.
- **Evidence:** The ratified Constitution contains zero occurrences of "gate", "PROHIBITED", "NEEDS_AUTHORITY", "NEEDS_EVIDENCE", "ADMISSIBLE", "hard stop", or "four-valued". The four-valued gate structure entered the program as an accepted concession in the CANDIDATE Decision Value Calculus V2.1 reconciliation (#1182, still CANDIDATE #1185, unratified).
- **Consequence:** candidate machinery is presented as constitutional law — the exact false-attribution class the contract registry lesson warns against (never collapse CANDIDATE into RATIFIED).
- **Fix direction:** restate the gate structure as candidate gate machinery shared with the calculus, with its constitutional *grounding* cited per gate (e.g., PROHIBITED ← Articles VI.6, XIV; NEEDS_AUTHORITY ← Article V; NEEDS_EVIDENCE ← Articles IV, VI.3, VII), not as constitutional text itself.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F03 — §3.2(3)'s "the zero-tolerance principle for these classes is constitutional" is false
- **Sections:** §3.2(3).
- **Evidence:** No τ, "zero-tolerance", or "zero tolerance" language anywhere in the ratified Constitution. The τ_seed table is acknowledged CANDIDATE in the same sentence — but the sentence then asserts the *principle* is constitutional, which the corpus does not support.
- **Fix direction:** either ground zero-tolerance in actual articles (candidate argument: VI.3 + XIV + XVI compose toward it — but that composition is itself candidate reasoning, label it so) or park the principle as CANDIDATE pending ratification.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F04 — JUDGMENT_RULE hard stop binds the director, but the Judgment Rule is not ratified law (hierarchy inversion)
- **Sections:** §3.2(2) vs §3.3.
- **Evidence:** §3.3's own hierarchy: "Constitution > director instruction > all other principals." The Judgment Rule is DIRECTOR-STATED (AGENTS.md Prime 1, 2026-09-30, HIGH confidence) — it is not in the ratified Constitution (verified: zero matches). A director-stated rule used to *overrule the director* inverts §3.3's hierarchy: director-stated content cannot sit above the director.
- **Consequence:** the strongest refusal in the spec (§3.2(2), "binds against every principal including the director") rests on the weakest authority basis. §14 Q3 correctly asks Shawn to confirm the no-override — but the spec pre-asserts constitutional status before he answers.
- **Fix direction:** (a) route the Judgment Rule through Article XVIII ratification so it *becomes* constitutional law; or (b) restate §3.2(2) as interpretive doctrine grounded in ratified articles (VI.3 "high-risk actions require proportionate evidence and authority", VI.6 "refuse is a valid intelligent outcome", XIV fail-closed, XVI human-value test, I.4 intent/authorization distinction) — the refusal stands, the authority basis is honest.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F05 — LAW_OF_ONE / JUDGMENT_RULE are unimplementable as specified: LAW's epistemic machinery is unnamed
- **Sections:** §3.2(1), §3.2(2) vs §1.3.
- **Evidence:** §1.3: LAW "runs *before* the math" and "does not score value" — a prohibited act never reaches the calculus. Yet §3.2(1) requires assessing an action's "foreseeable consequences", and §3.2(2) requires knowing an instruction "would make the system worse on evidence" — both are consequence-forecasting computations, the calculus's job, placed pre-gate with no named model. §7's receipt carries `hard_stops_fired` "with the triggering facts" and §11(4) requires those facts be reconstructible — but the *source* of the facts (KNOW? graph? historical receipts? an oracle?) is never named.
- **Consequence:** acceptance #2/#3 (refusal "names the harm facts") cannot be built — there is no specified place for the facts to come from. Same structural gap class as SELF-F02 (unimplementable binding without issuer).
- **Fix direction:** name LAW's fact sources explicitly (e.g., consequence forecasts via KNOW's serving path over graph + receipt history; factuality checks via VERIFIED/SUPPORTED graph edges), state the epistemic floor a hard stop requires, and define what happens when the fact source is itself uncertain (fail-closed per XIV, presumably — say so).
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F06 — Time-of-check / time-of-use hole: grant revocation between verdict and execution
- **Sections:** §6.2 vs §8, §12.
- **Evidence:** §6.2: a verdict may never move ADMISSIBLE → NEEDS_* silently — "downgrade requires a new proposal version with new facts." §8: "revoked or expired grants fail the authority check." §12: revocation moves the grant node to REVOKED and its GRANTS edges are excluded from validation automatically. Scenario: verdict ADMISSIBLE issued under grant G at T1; G revoked at T2; ACT executes at T3. Either (a) ACT executes under a dead grant — authority hole; or (b) something re-validates at T3 — contradicting §6.2's no-silent-downgrade rule.
- **Fix direction:** specify the verdict's temporal validity model: issue-time validity plus a re-validation duty at execution (by ACT? by LAW re-check?), and reconcile with §6.2 (re-validation failure is not a "silent downgrade" — it is a defined transition, e.g., ADMISSIBLE → SUSPENDED on grant death, receipted).
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

## MODERATE

### F07 — Ambiguous halt semantics for EVALUATION_INCOMPLETE (§4 vs §9)
- **Sections:** §4 ("Timeouts fail closed" → verdict PROHIBITED, reason EVALUATION_INCOMPLETE) vs §9 ("LAW cannot evaluate … the pipeline halts at LAW — no proposal proceeds unexamined").
- **Evidence:** A per-proposal PROHIBITED verdict does not halt the pipeline — §9's own first row says "one refusal does not halt the organism." The §9 row conflates per-proposal refusal with organism halt. Further: §7 promises "every evaluation — including intake refusals — emits a GateReceipt"; if the constitution store is corrupt, the emission path for the EVALUATION_INCOMPLETE receipt is unspecified.
- **Fix direction:** distinguish per-proposal evaluation failure (PROHIBITED + receipt, pipeline continues) from LAW-subsystem failure (constitution store unreachable/corrupt → organism halt per Article XIV), and specify the receipt path for each.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F08 — "No bypass path exists" (§2.1) is contractual, not architectural — the interlock is unspecified
- **Sections:** §2.1, §4 vs §9.
- **Evidence:** §2.1: "No bypass path exists — not for the director, not for other nodes." §4: "ACT must present the proposal and wait." Both are stated as rules. The only enforcement named is detective: §9 detects envelope violations via "ACT's execution receipt vs envelope" — after the fact. Nothing technically prevents ACT from executing without presenting a proposal.
- **Fix direction:** name the interlock (e.g., execution requires presenting a valid GateReceipt; ACT cannot self-issue verdicts; bind to SELF's authenticated identity chain), or downgrade §2.1 to a contractual obligation with detective enforcement and state the residual risk honestly.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F09 — Bundle rule / verdict-shopping detection is unenforceable as specified
- **Sections:** §4 (bundle rule), §10.4 vs §9 (detection).
- **Evidence:** §9 lists detection of resubmission gaming via "proposal-hash comparison." Decomposed bundle pieces have *different* hashes by construction — hash comparison cannot detect splitting. The bundling criterion (what makes separate proposals one bundle?) is unspecified; if bundle membership is proposer self-declared, gaming is trivial.
- **Fix direction:** specify the correlation mechanism (e.g., intent-similarity review, shared target/effect clustering, proposer-declared bundle IDs with LAW authority to re-bundle) and who bears the burden of proof.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F10 — Grant scope unboundedness: §8 vs §10.2 boundary unspecified
- **Sections:** §8(a)–(d) vs §10.2.
- **Evidence:** §8's four validity criteria contain no scope-boundedness requirement. A director grant of unbounded scope ("do whatever you think best, indefinitely") passes (a)–(d). §10.2 refuses "blanket ADMISSIBLE for everything I do next" — but a standing *grant* is not a *verdict*; the spec never says whether an unbounded grant is lawful.
- **Fix direction:** extend grant validity with a scope/expiry boundedness requirement (grants name bounded scope + expiry, mirroring §7's per-proposal envelope discipline), or explicitly permit unbounded director grants and reconcile with §10.2.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F11 — Pinned constitutionHash has no advance procedure (bootstrap-of-law gap)
- **Sections:** §6.1 vs §10.5, §10.6.
- **Evidence:** LAW evaluates "only against a pinned version" (§6.1). When the Constitution is amended via Article XVIII ratification, the pin must advance — but no procedure names who updates the pin, under what receipt, or how a cold successor verifies pin lineage. Per §10.5, a proposal altering what LAW evaluates against is GATE_REDESIGN-smelling; the lawful pin-update path must be distinguished from smuggling.
- **Fix direction:** specify the pin-update procedure (ratified amendment → named updater role → pin-update receipt → cold-verifiable lineage), explicitly carved out of §10.5.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F12 — Evidence-floor data source unnamed; k undefined
- **Sections:** §3.4 step 5, §4, §7 (`evidence_summary: { n, floor_k, ... }`).
- **Evidence:** §4 cites "evidence store unreachable" — but LAW's evidence source is never named. §12 establishes the precedent that "grant-state lookups go through KNOW's serving path like any other knowledge" — evidence-floor lookups should be named the same way (or otherwise). `floor_k` has no value or key anywhere in the spec; §15 correctly flags calculus references as aspirational, but the *mechanism* still needs a named source and a config-key home for k.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

## MINOR

### F13 — INTAKE_REFUSED is not in the GateVerdict / GateReceipt gate enum
- **Sections:** §1.2, §7 vs §3.4 step 1, §9, §10.1.
- **Evidence:** The gate enum is PROHIBITED | NEEDS_AUTHORITY | NEEDS_EVIDENCE | ADMISSIBLE, but intake-invalid proposals are "receipted as INTAKE_REFUSED" (§9, §10.1) and §3.4 step 1 routes to "REFUSE". No enum member holds that value.
- **Fix direction:** add INTAKE_REFUSED to the enum or define it as a receipt-level status distinct from gate.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F14 — Broken cross-reference; the "independent" verifier is unnamed
- **Sections:** §9 (last row) vs §11; §13 acceptance #12.
- **Evidence:** §9 cites "Independent recomputation mismatch (§10)" — recompute is §11, not §10. "Independent" is never defined: independent of what? If the same LAW binary recomputes its own verdicts, mismatch detection is weak. §13 #12 says "Independent verification confirms the receipt chain" without naming the verifier.
- **Fix direction:** fix the reference; name the independent party (VERIFY node, or a second LAW instance under separate custody) and its access path to receipts + pinned constitution.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

### F15 — §8(d): "names or implies the grantee" — "or implies" is a delegation ambiguity
- **Sections:** §8(d).
- **Evidence:** A grant that merely "implies" its grantee invites disputed delegation chains — the exact ambiguity §8 is supposed to eliminate.
- **Fix direction:** require explicit grantee naming; define delegation-chain rules (each hop receipted, chain terminates at the director's grant per §8's last line) if implied grantees are ever permitted.
- **Status:** FIXED (reconciled 2026-09-30 ~19:48 PDT — candidate revisions in spec Appendix A)

## Explicitly checked — no finding
- **GAP-A coverage:** all 8 elements present — responsibility (§1, §2), ownership (§5), sync/async (§4), persisted transitions (§6), evidence (§7 + floors), authority (§8), failure propagation (§9), cold reconstruction (§11). Depth gaps within covered areas are filed above (F05, F06, F11, F12).
- **Article citations verified grounded:** Article I.1 ("The Human Director is the final authority" — §3.3 ✓); Article XIV fail-closed (XIV.1–2 — §4/§9 ✓); Article VI.6 ("Stop, refuse, or defer are valid intelligent outcomes" — refusal machinery generally ✓); Article XVIII ratification (§5 ✓).
- **CANDIDATE banner intact; §14 open questions are genuine director decisions** (esp. Q3 — correctly routes the F04 authority-basis question to Shawn).
- **§15's calculus-aspirational disclaimer is honest** — the false-constitutional attributions (F02–F04) are the remaining problem, not the calculus references.

## Score rationale — 7.0/10
Structure is the strongest of the drafts so far (complete GAP-A, acceptance battery, honest §14/§15 framing) — but it carries one CRITICAL silent-contract-extension (F01, same class as PROVE-F01), two MAJOR false-constitutional attributions (F02, F03), a governance hierarchy inversion (F04), and two MAJOR implementability gaps (F05, F06). Consistent with the LEARN/PROVE/SELF draft bar of 7.0: substantive, adversarially useful, not yet 8.5.

## Reconciliation — 2026-09-30 ~19:48 PDT (Naya 4, inline; no subagents)
All 15 findings FIXED as CANDIDATE revisions in `~/workspace/nine-node-specs/LAW-NODE-SPEC-CANDIDATE.md` (24,923 → 40,357 bytes; banner `CANDIDATE — NOT RATIFIED — NOT MERGED` intact). Per-finding evidence:

- **F01 (CRITICAL) → FIXED:** §12 rewritten — verdicts now map onto the RATIFIED V2 contract's 22-type enum (`CONTRADICTS`/`INVALIDATES` for refusal; `DEPENDS_ON`/`AUTHORIZED_BY` for grants; `SUPERSEDES`/`INVALIDATES` for revocation). Enum re-verified against `/tmp/nayapower-main/BRAIN/04-INTELLIGENCE/GRAPH/0003-GRAPH-RELATIONSHIP-CONTRACT-V2.json` before editing; all mapped types confirmed present. The four purpose-built types refiled as a formal contract-amendment *proposal* in §12. §15's "does not change any contract" is now true.
- **F02 (MAJOR) → FIXED:** §15 rewritten — gate structure restated as CANDIDATE machinery shared with the calculus, with per-gate constitutional grounding cited (not claimed as text). §0 purpose carries the candidate qualifier.
- **F03 (MAJOR) → FIXED:** §3.2(3) rewritten — zero-tolerance principle is a labeled CANDIDATE argument (VI.3+XIV+XVI composition); §14 Q5 reworded.
- **F04 (MAJOR) → FIXED:** §3.2(2) rewritten — refusal grounded in ratified articles VI.3/VI.6/XIV/XVI/I.4; Judgment Rule labeled DIRECTOR-STATED doctrine, never used to overrule the director; §3.3 hierarchy preserved. §14 Q3(b) routes the ratification question to Shawn.
- **F05 (MAJOR) → FIXED:** new §3.5 names fact sources (KNOW serving path over graph + receipt history; VERIFIED/SUPPORTED edges + PROVE seals), the hard-stop epistemic floor (`law.evidence.floor_k`), and the fail-closed uncertainty rule.
- **F06 (MAJOR) → FIXED:** §6.2 gains the temporal validity model (`validUntil = min(grant expiry, envelope expiry)`), execution-time re-validation, and the defined receipted `ADMISSIBLE → SUSPENDED` transition on grant death. GateReceipt gains `valid_until`.
- **F07 (MODERATE) → FIXED:** §9 splits per-proposal failure (PROHIBITED + receipt, pipeline continues) from subsystem failure (halt per XIV + emergency receipt path). §9 rows updated; design principle line below the table retained (fail closed for the organism, open for refusal).
- **F08 (MODERATE) → FIXED:** §2.1 gains the named interlock (LAW-kernel-bound verdict, ACT cannot self-issue, SELF identity-chain verification); preventive vs detective enforcement distinguished; residual risk stated.
- **F09 (MODERATE) → FIXED:** §4 + §10.4 — proposer-declared `bundleId` + LAW re-bundle authority on objective correlation; hash comparison demoted; burden of proof named.
- **F10 (MODERATE) → FIXED:** §8 gains (d) explicit-grantee + (e) scope boundedness + (f) expiry; delegation-chain rules; standing-grant vs standing-verdict reconciled with §10.2.
- **F11 (MODERATE) → FIXED:** §11 gains the pin-advance procedure (ratification receipt → Constitution Custodian → pin-update receipt → cold-verifiable lineage); §10.5 carve-out names the lawful pin path.
- **F12 (MODERATE) → FIXED:** evidence-floor source named in §3.5; `floor_k` at config key `law.evidence.floor_k` (provisional until V2.1 ratified); receipt `evidence_summary` cites the config key.
- **F13 (MINOR) → FIXED:** INTAKE_REFUSED defined as receipt-level `intake_status` (gate = null); §3.4 step 1 routing clarified; GateReceipt schema updated.
- **F14 (MINOR) → FIXED:** §9 ref corrected to §11; independent recomputer named (VERIFY node, separate custody) with access path; §13 #12 reworded.
- **F15 (MINOR) → FIXED:** §8(d) requires explicit grantee naming; delegation-chain rules defined.

**Final review score: 8.5/10** (was draft 7.0). 0 findings OPEN. Hardest calls: F01 (amendment-proposal structure mirroring PROVE-F01, not a silent extension); F04 (refusal keeps full force on ratified articles while the Judgment Rule's status is honestly labeled and routed to Shawn); F06 (the SUSPENDED transition reconciles §6.2's monotonicity with the TOCTOU hole as a defined exception, not a silent one).
