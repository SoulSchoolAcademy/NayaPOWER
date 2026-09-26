# INT-001 Ratification Readiness Evidence Matrix — 2026-09-26

INT-001 remains PROPOSED. Conclusion: NOT READY FOR HUMAN RATIFICATION.

| # | Requirement | State | Evidence / location | Remaining gap | Blocks ratification? |
|---|---|---|---|---|---|
| M1 | Every Smart Note corresponds to exactly one receiver-issued immutable IB; local tooling cannot allocate/guess/reinterpret identity. | PROVEN | Receiver boundary; smart_note_transaction.py fails closed; real IB-001019/001024/001061 artifacts. | Full creation-path cold audit remains open. | YES |
| M2 | Canonical Smart Note uses the required YYYY/MM/DD/category/topic/IB/smart-note.md namespace. | PROVEN | canonical_smart_note_path; registry; real artifacts. | None at inspected repository scope. | NO |
| M3 | Smart Note uses the required 15-section human-readable order unless N/A. | PARTIALLY PROVEN | Canonical V1 + rehabilitation receipt; real notes inspected. | Dedicated deterministic structural assertions are missing. | YES |
| M4 | Projection gate remains RECEIVER PERSISTED → REPOSITORY PROJECTED → SMART LINK VERIFIED. | PARTIALLY PROVEN | Receiver evidence + verifier state separation. | Verifier does not itself remotely fetch/resolve the GitHub target. | YES |
| M5 | Smart Link points directly to GitHub. | PROVEN | smart_link_verifier.py build_smart_link; real GitHub links fetched. | Automated remote resolution absent. | YES |
| M6 | Smart Link targets the reported canonical branch/ref. | PROVEN | Explicit canonical_ref input; real artifacts fetched from main. | Canonical-ref freshness is supplied context, not independently resolved by verifier. | YES |
| M7 | Smart Link targets exact canonical path and ends /IB-XXXXXX/smart-note.md. | PROVEN | Verifier path/suffix checks + tests. | None at repository-path scope. | NO |
| M8 | Target file actually exists. | PROVEN | Three real files fetched from main; missing fixture tested. | Automated remote-link resolution absent. | YES |
| M9 | Target file identifies the same IB. | PROVEN | Verifier checks path and content; three real artifacts match. | Receiver-object join remains external input. | YES |
| M10 | Smart Link corresponds to receiver-created canonical object. | PARTIALLY PROVEN | New receiver_link_correspondence() joins receiver-issued IB, source event, canonical receiver, canonical path, and Smart Link shape; real IB-001061 fields were inspected. | Receiver record is still an authoritative input; independent live receiver/API join remains unproven. | YES |
| M11 | PENDING/MISSING/CONFLICTED/UNKNOWN are never inferred as VERIFIED. | PROVEN | Verifier + controlled fixtures cover all four. | Production PENDING/CONFLICTED examples do not exist in evidence; fixtures are synthetic. | YES |
| M12 | Smart Link, Hub Deep Link, and Evidence Link remain distinct. | PARTIALLY PROVEN | classify_link_kind() plus adversarial D tests deterministically distinguish all three; contracts define the canonical nouns. | Cold-Naya wording/decision behavior is still unobserved. | YES |
| M13 | Repository projection cannot allocate IBs, create competing Notes/events, bypass intake, or claim persistence from file creation. | PROVEN | local execute() fails closed; receiver remains sole authority. | Complete creation-path audit remains open. | YES |
| M14 | Contract conflict requires STOP → IDENTIFY AUTHORITY → RECONCILE → RECORD → RESUME. | PROVEN | Contract Stack + CC-000 + INT-001 agree; no semantic conflict found. | No live conflict case observed. | NO |
| M15 | Smart Link creation cannot broaden privacy, authority, consent, or publication. | PROVEN | INT-001 §18 + CC-000; verifier has no authority-grant behavior. | All publication surfaces not tested by INT-001. | YES |
| M16 | Contract changes follow required change-control sequence. | PROVEN | INT-001 creation/indexing; acceptance tests; verifier; receipts; no autonomous ratification. | Human ratification remains reserved. | NO |
| M17 | Anti-patterns are prevented: wrong URL type, fabrication, local allocation, duplicate Note, file-only persistence, receiver-only projection. | PARTIALLY PROVEN | D adversarial vocabulary cases + receiver correspondence cases now reject wrong link type, wrong IB, wrong source event, and wrong receiver; fail-closed resolver remains authoritative. | Broader anti-pattern matrix is still incomplete. | YES |
| M18 | Cold-Naya decision rule is applied before saying Smart Link. | PARTIALLY PROVEN | Verifier covers repository/path/IB inputs; cold frontier remains open. | Independent fresh-context behavioral observation. | YES |
| M19 | Completion standard requires ratification, mapped implementation, deterministic checks, passing acceptance, independent artifacts, cold terminology behavior, no competing interpretation. | PARTIALLY PROVEN | Index, implementation, verifier, tests, three real artifacts. | Ratification + missing acceptance/behavioral evidence. | YES |

## Acceptance tests
| Test | State | Evidence / gap | Blocks ratification? |
|---|---|---|---|
| A — Verified link | PARTIALLY PROVEN | Three real matching artifacts and deterministic link construction; remote resolution and receiver-object correspondence are not fully machine-proven. | YES |
| B — Pending projection | PARTIALLY PROVEN | Controlled PENDING fixture works; no natural production PENDING case and no cold-Naya wording observation. | YES |
| C — Conflict | PROVEN | Controlled wrong-IB fixture returns CONFLICTED; fixture is explicitly synthetic, not historical evidence. | NO |
| D — Vocabulary | PROVEN | Deterministic classify_link_kind() test rejects Hub Deep Link as Smart Link and distinguishes Smart Link, Evidence Link, and unknown GitHub pages. | YES — cold behavior still required by H/M18 |
| E — No fabrication | PROVEN | Verifier rejects noncanonical paths and preserves UNKNOWN/MISSING/PENDING. | YES |
| F — Identity preservation | PROVEN | Adversarial test generates different date/category/topic paths with the same IB-001061 and asserts the immutable identity segment remains unchanged. | Cold behavioral proof remains separate. |
| G — Receiver boundary | PROVEN | Local creation execute() fails closed and receiver remains authority. | YES |
| H — Cold successor | UNKNOWN | Control plane explicitly keeps cold-Naya takeover open; no INT-001 cold behavioral run. | YES |

## Cross-contract reconciliation

CC-000: no semantic conflict. It reinforces human authority, one canonical object/identity, source-of-truth separation, truth-state separation, evidence law, receiver-centric creation, and exact noun separation.

Contract Stack Operating Law: no semantic conflict. It requires acceptance tests for contracts, evidence-bound claims, source-of-truth checks, and continuous Lead Mode.

Canonical Smart Note/IB V1: no semantic conflict. INT-001 is a projection/link boundary and does not own IB allocation, canonical persistence, events, indexing, learning, or Hub runtime deep links.

Naya Link Identity & Evidence V1: no semantic conflict. INT-001 adopts its direct-GitHub Smart Link law and exact vocabulary. Remaining weakness is enforcement completeness, not contradictory semantics.

EP-001: no semantic conflict. The execution wave followed inspect → test → implement → verify → record → reassess. EP-001 does not grant contract-ratification authority.

Control plane: unchanged. HUMAN-JOURNEY-P2 remains active and its current next action remains cold-Naya takeover certification. INT-001 was not promoted into the canonical frontier.

## Determination

INT-001 is NOT READY FOR HUMAN RATIFICATION.

The contract is semantically aligned with the existing ratified authorities, but its own completion standard is not yet met. The new adversarial wave closes D and F at the deterministic test layer and materially strengthens receiver/link correspondence, but cold-Naya evidence is NOT the only remaining technical boundary. Remaining technical boundaries are: deterministic 15-section Smart Note structure enforcement; independently observed Smart Link target/ref resolution; independent receiver-object/API correspondence; broader anti-pattern coverage; natural production PENDING evidence; and cold-Naya terminology/decision behavior. Human ratification remains a separate authority boundary.

## Human-authority boundary

When all technical prerequisites are satisfied, the minimal human action is to ratify INT-001 Version 1.0 as canonical under CC-000 while preserving existing ratified Smart Note/IB and Naya Link Identity contracts and without changing receiver ownership, IB allocation, or the control-plane frontier.

## Single successor action

Add and run deterministic adversarial tests for D (vocabulary), F (identity preservation), and receiver/link correspondence; independently verify the results; then reassess whether cold-Naya evidence is the only remaining technical boundary.
