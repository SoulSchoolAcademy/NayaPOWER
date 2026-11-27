# NayaNET — Daily Project Intelligence / 14-Question Director Audit
**Date:** 2026-11-21 · **Evidence window:** approximately 19:43–20:14 UTC · **Status:** RESEARCHED / REPORTED, NOT DEPLOYED
**Canonical baseline inspected:** `main` at `b885b4fe4388640e57c88a31466d43b5a28a60d0`. Re-resolve before acting: main moves continuously.
**Purpose:** Distill live truth into the next highest-value actions without adding a competing source of truth.

## Executive finding
Architecture and knowledge capture are substantial. System is NOT VERIFIED 10/10: live routing returns a parked page on nayanet.live, nayanet.app externally inaccessible to this audit, security advisor shows active authorization findings, the full user journey and learning-to-cold-successor chain lack fresh complete production proof. Do not equate active agent/commit throughput with human value.

## Fresh, directly checked evidence
- `main` SHA b885b4fe... at 20:11:50 UTC: registry-band backfill SN-4532..SN-4564; proof of remediation work, not of the full experience. https://github.com/SoulSchoolAcademy/NayaPOWER/commit/b885b4fe4388640e57c88a31466d43b5a28a60d0
- GitHub open PR list (8 observed): #3499, #3501, #3503, #3504, #3505, #3506, #3507, #3508. Do not merge based on this inventory alone; inspect exact heads, CI, independent verdicts and merge gates.
- NOW #2599: 5 occupied worker lanes, many receipts, and current claim that nayanet.live was unreachable. Generated master directive #2601 refreshed around 19:43 UTC, writer-only and freshness contract (<60 min); its action lists carry older material and must be rederived before delegation.
- External web request to https://nayanet.live returned a Namecheap domain-auction landing page, not the Hub. https://nayanet.app and /personal were not accessible via web fetch; this is NOT proof the app has vanished, but NOT a production pass. Source: external request performed 2026-11-21, verify independently with DNS, registrar, TLS, Cloudflare route, origin, multiple vantage points.
- Live Supabase project `dahisasgpfvziswqvmvm` is ACTIVE_HEALTHY at project level. Security Advisor observed ~20:13 UTC: `rls_references_user_metadata` ERROR ×8 (smart_mail_messages, smart_mail_threads, smart_mail_aliases, invites, scheduled_messages); `security_definer_view` ERROR ×2 (smart_link_daily_stats, smart_link_dimension_stats); `rls_enabled_no_policy` INFO ×22; `function_search_path_mutable` WARN ×32; anon-executable SECURITY DEFINER function signatures WARN ×64 and authenticated-executable WARN ×71. Other anonymous-sign-in warnings exist. Findings ≠ confirmed exploits; test reachability/grants/policies before remediation. Reference: https://supabase.com/docs/guides/database/database-linter?lint=0015_rls_references_user_metadata and https://supabase.com/docs/guides/database/database-linter?lint=0010_security_definer_view.
- Canonical tension: #3028 describes a personal fork-connected citizen, while newer #3029 describes shared NayaPOWER by default with optional fork. Resolve into ONE current product contract; no silent choice. https://github.com/SoulSchoolAcademy/NayaPOWER/issues/3028 https://github.com/SoulSchoolAcademy/NayaPOWER/issues/3029
- About = ONE ultimate profile page (SN-4421); About frame-by-frame (SN-4419); About/Skills inherit actual agreement/slideshow components (SN-3747). Documented architecture is not proof of a verified live experience.

## 14-question minimum viable intelligence interface
1. **WHO?** Shawn = final human authority; Team Naya = governed integrator/builders/verifiers; owner identity and scoped execution matter.
2. **WHAT?** NayaPOWER = governed intelligence substrate; NayaNET = connected network and citizen apps; Hub = presentation/cockpit, not separate truth source.
3. **WHY?** Increase verified human capability, understanding, privacy, creativity, connection and compounding intelligence with less complexity.
4. **SUCCESS?** Cold newcomer completes real, secure, useful workflows with 10-star quality; outcomes and reuse proven; sustainable operation and human agency.
5. **TRUE NOW?** Active GitHub production engineering; 8 open PRs observed; 5 occupied lanes; routing issue observed; live security findings; end-to-end proof incomplete.
6. **PROVEN?** Canonical repo and contracts exist, commits/notes/worker receipts exist; Supabase project healthy; current advisor findings observed; not the whole product.
7. **UNKNOWN?** Full route health; auth/tenant isolation under negative tests; privacy guarantees; onboarding-to-value completion; real learning changing later action; business economics.
8. **AUTHORITY?** Governed reversible reports and analysis permitted; production/auth/security/payment/destructive changes remain protected and require explicit release authority.
9. **PAST?** Many cycles built AI kernel, Hub, notes, design, factory, worker protocol; recurrent defects in proof, drift, activation, and UI quality.
10. **LEARNED?** Stored notes ≠ changed behavior; UI ≠ working service; merged ≠ verified; security warning ≠ confirmed breach; velocity ≠ human value.
11. **NEXT?** Security/routing triage + ONE end-to-end citizen and successor proof.
12. **PROVE?** Failing-before/passing-after tests, multi-owner denial, fresh browsers, independent verifier, CI, traceable production receipts.
13. **RECORD?** #2599 NOW, #2601 generated handoff (sources, not hand-edits), existing area boards, governed PI records, Smart Notes/blocks with evidence.
14. **CONTINUE?** Next seat resolves fresh main and law, rederives the facts, takes scoped next action, independently proves and records it; passes a link and next authorized operation.

## Top 10 strongest existing assets (documented, not blanket live certification)
1. Human authority and explicit governance.
2. Canonical NayaPOWER/NayaNET/Hub separation.
3. Smart Notes and Intelligent Blocks with lineage.
4. Nine-node kernel design and operating loop.
5. Cold-successor standard.
6. Independent doer/judge/verifier gates.
7. GitHub-first evidence and issue history.
8. One shared design code/factory vision.
9. One Hub, Personal/Business/Spaces product model.
10. Privacy by default, collective by consent product law.

## Top 10 missing capabilities / holes
1. Verified public entry/destination routing.
2. Audited tenant-isolation/security assurance.
3. Cold user onboarding-to-first-value proof.
4. True closed-loop learning-to-successor outcome proof.
5. Consistent live feature/capability contract and status labels.
6. One authoritative, fresh and nonconflicting team priority feed.
7. Independently tested About/Skills and full citizen experience.
8. Smart Factory reproducible, testable standard components.
9. Verified end-to-end communication/booking/payment rails.
10. Measured customer value, retention, operating cost and sustainable economics.

## Top 10 systemic blockers / major problems
1. Surface availability and DNS/route uncertainty.
2. Authorization relying on user-editable metadata (advisor flags).
3. Privileged-view/function exposure requiring examination.
4. Legacy/competing product contracts (#3028 vs #3029).
5. High task/receipt volume without equally clear human-outcome metrics.
6. Stale priority material in generated directives.
7. Unresolved PR tests/reviews and fragile CI.
8. Partial UI implementation mistaken for user journey completion.
9. Registry/index drift and repeated backfill work.
10. Lack of repeatable cold successor/action/outcome evidence.

## Top 10 solutions and immediate action sequence (ranked; owner; stop/proof)
1. **P0 Security** — LAW/VERIFY + Supabase specialist: inventory current metadata-dependent policies, privileges, affected callers; write owner mapping and negative tests on approved isolated dev branch only; STOP on missing identity model; production changes protected.
2. **P0 Domain/Hub** — Ops/HUB owner: authoritative registrar/DNS, TLS and Cloudflare Worker route check; known-good deployment and origin; test 3 regions + cold mobile/desktop; NO blind DNS changes or claim that Namecheap page proves ownership loss.
3. **P0 Entry** — Product/HUB: cold unauthenticated join → optional worlds → public browse, verified event and state, correct consent/visibility; snapshot before repair.
4. **P0 Learning** — LEARN/KNOW/VERIFY: choose one genuinely observed failure, capture→store→retrieve→authorized improved action→independent later-outcome→cold successor; reject simulated receipts.
5. **P1 Product law** — Director/product/LAW: reconcile #3028 vs #3029; shared agent door vs optional fork; document statuses; director approval for any changed authority/promise.
6. **P1 PR drain** — Owners of 8 PRs: exact heads, failing tests, separate verifier and gates; close/merge only if truly eligible, no false GREEN.
7. **P1 About/Skills** — Nitro/HUB: harvest agreement unfold and premium slideshow; one About profile; one real skill object; original approved media; prove interaction on real phone/desktop.
8. **P1 Messaging/privacy** — AUTH/HUB: test two users A/B, send/receive, revoke/block, metadata, retention, AI opt-in; do not promise unread/unobserved messages until independently proven.
9. **P1 Registry/factory** — KNOW/Factory: root-cause recurring orphan/index drift, prove generator/checkpoint, R5 fresh build and no duplicate UI components.
10. **P1 Economic proof** — Growth/PI: instrument first-value time, task success, active users, customer retention, service cost and actual revenue; no decorative metrics.

## The 10 reasons progress stalls and corresponding controls
1. Too many simultaneous jobs → limit WIP by outcome.
2. Stale status → freshness and tip recheck at every handoff.
3. Vague ownership → one accountable owner per protected workstream.
4. Self-attestation → independent verifier, artifacts.
5. Broken entrance → P0 monitoring + release rollback.
6. Security uncertainty → deny-by-default test matrix + explicit approval.
7. UI/backend drift → real journey tests not screenshot-only.
8. Duplicate contracts/components → single canonical registry.
9. Worker output not communicated → PI event → board → permitted mail.
10. Incentive on commits rather than outcomes → value-per-action and cold-successor score.

## Desired enhancements: 10 that can make the system much more useful
1. One human goal-to-result dashboard with verified state.
2. Explainable permission-aware matching.
3. Owner-controlled private vault and share-by-consent projection.
4. Active, grounded Ask Naya per About/Skills/Space.
5. Instant cited Smart Notes with provenance and status.
6. Actionable Skills profiles connected to booking and services.
7. One-click multilingual and accessible presentation.
8. Governed AI-to-AI workflow with scoped authority.
9. Evidence-driven learning reuse and cold Naya recovery.
10. Project Intelligence self-updating from real event receipts.

## Proof criteria / release gates
- Routing: intended Hub returns intended content (not parking), correct cert & DNS, cold public entry from independent networks.
- Security: no unexplained critical advisor findings; each affected table/view/function has ownership, grants and negative cross-tenant tests; no production change without approval.
- Human journey: actual users join, edit, optionally publish, discover, connect and receive service; ownership/private-by-default maintained.
- Intelligence: later action visibly improved by retrieved verified lesson; successor reproduces without prior chat.
- Quality: actual desktop/mobile interactions, accessibility, and Director's eye; no dead controls.
- Economics: verified baseline and post-change cost/value, not assumed improvement.
- Status taxonomy: SPECIFIED → IMPLEMENTED → TESTED → LIVE-VERIFIED → PRODUCTION-PROVEN.

## Executable Team Naya directive / torch
**Objective:** Close the highest-harm and highest-human-value gaps above; do not create more unproven features.
**Source:** re-resolve `main`, README/PROTOCOL/AGENTS, #2599, generated #2601 fresh (<60 min), #3028/#3029, #2823, #1771, #2880–#2885, current PR heads, current Supabase advisor and web routes.
**Authority:** Shawn human director. No production deployment, secret, pricing, permission, billing, destructive change or constitution edit without applicable explicit approval. Reversible audit/isolated branch and PRs allowed under law.
**First action:** classify the 8 `user_metadata` RLS findings; map real owners and callers, produce negative tests on non-production branch with independent reviewer. In parallel operations owner diagnoses public domain using registrar and Cloudflare evidence. No risky speculative mutations.
**Dispatch:** Alpha=LEARN+successor proof; Beta=KNOW/registry drift; Gamma=ACT/cold journey; Delta=LAW/security authority reconciliation; Epsilon=VERIFY independent adjudication; Nitro=UX from canonical parts; Ops=domain. Verify actual seat availability before assignment; no duplicate occupied-lane tasks.
**Tests:** exact head CI; before/after regressions; adversarial tenant A/B; protected permission gates; multi-region web smoke; production proof only after approved deployment. In every failure classify root cause before fixing.
**Evidence:** each owner posts time, SHA, failing test, passing test, independent verifier, actual user value, residual risk, next action on its canonical area board and #2599. If permitted, send network mail using functioning authenticated service; never claim sent without delivery receipt.
**Stop conditions:** any unresolved security/authority boundary, unavailable production routing, stale master directive, unverified claims, merge gate failure, incompatible product contracts.
**Handoff:** one sentence true now; one evidenced result; one unresolved blocker; one bounded next action; one exact owner; pointers to original receipts.
**Destination:** Do not hand-edit auto-generated #2601. Update its canonical source inputs; mirror summarized status to existing #2599. Merge this report only through existing governance.

## Caveat
This audit observed metadata and security advisor notices but did not run unauthorized cross-owner data access tests. No production DB, DNS, Hub or deployment mutation performed. No claim of 10/10 or permission to merge.