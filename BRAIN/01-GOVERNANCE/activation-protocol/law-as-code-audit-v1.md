# Law-as-Code Audit v1 — The Operating Law of Naya Net

**Layer 3 of the Naya Activation Protocol** — "Law as code": machine
enforcement of the Operating Law.
**Authorized:** Shawn Vibert, 2026-10-09.
**Auditor:** Naya 4. **Date:** 2026-10-09.
**Source audited:** `BRAIN/01-GOVERNANCE/0008-OPERATING-LAW-V1.md`
(ref `naya4/operating-law-v1`, 59 laws across 8 domains).

## Summary — what this found

Shawn's Operating Law has 59 laws (source:
`BRAIN/01-GOVERNANCE/0008-OPERATING-LAW-V1.md`, ref `naya4/operating-law-v1`).
I checked every one against the repo for
a real, fail-closed, machine-enforced check. What I found: **2 laws are
solidly encoded** (ratified objects can't be deleted — the guard runs in CI
and fails the build). **21 have checks that exist but are weak** — the
strongest merge gate in the repo is never called by CI, and one law cites a
verifier file that doesn't exist. **4 are newly encoded by this pass**
(activation receipts, cited claims, plain words). **32 can't be machined at
all** — they need taste, intent-reading, or judgment, and pretending
otherwise would be theater. The full per-law verdicts are in the tables
below; the honest limits of the new checks are in "Honest caveats".

## Method

Every law was read against the repo (`~/workspace/.np-shallow`, main) and
the report/goal tooling. A law is only marked encoded if a real check was
found and its failure behavior verified — not inferred from prose.

**Verdicts:**

- **ENCODED** — a check exists, is fail-closed (violation blocks, exit
  non-zero), AND runs on an enforced path (CI workflow or a gate the
  machine actually invokes).
- **ENCODED-WEAK** — a check exists but is bypassable, warn-only, scoped
  to one surface, or not wired into any enforced path. The weakness is
  stated, not hidden.
- **ENCODED-NEW** — encoded by a new Layer 3 check built in this pass
  (fail-closed; pending wiring into an enforced path).
- **JUDGMENT-ONLY** — cannot be machined without inventing the law. One
  line says why.

**Fail-closed test used:** does a violation produce a non-zero exit (or a
refused action) that nothing in the normal path can silently ignore?

---

## DOMAIN 1 — DECISION

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 1.1 | The Mantra | JUDGMENT-ONLY | "Most intelligent thing" is an irreducibly judgmental ranking; no machine can score option quality without the seat's reasoning. |
| 1.2 | The Math Decides | ENCODED-WEAK | `tools/auto_merge_gate.py` enforces GATE→SCORE receipt structure on merge decisions (fail-closed, exit 1), but no CI workflow invokes it — most decisions never produce a machine-readable receipt. |
| 1.3 | The Intelligence Question | JUDGMENT-ONLY | An internal cognitive act; cannot be observed or verified mechanically. |
| 1.4 | The Decision Calculator | ENCODED-WEAK | Same as 1.2: the merge-receipt predicate requires enumerate/score steps when run, but general decisions are ungated and the calculator schema is unenforced outside merges. |
| 1.5 | Score-Fill-Ship | JUDGMENT-ONLY | A machine can require a scorecard file to exist; it cannot tell whether the score is honest or the holes found are the real ones. |
| 1.6 | The Judgment Rule | JUDGMENT-ONLY | By definition requires judging an instruction wrong; a machine cannot distinguish a wrong instruction from a right one it dislikes. |
| 1.7 | The Intent Law | JUDGMENT-ONLY | Judging whether a chosen piece fits its context is intent-reading; no machine can detect a silent substitution of intent. |
| 1.8 | Tip Moves | ENCODED-WEAK | `tools/auto_merge_gate.py` P2 (head SHA verified live), P4 (base == main tip), P9 (evidence ≤900s old) encode re-anchoring fail-closed — when run. Not invoked by CI. |

## DOMAIN 2 — COMMUNICATION

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 2.1 | Plain Meaning First | ENCODED-NEW | NEW `check_plain_words.py`: lead-with-meaning structure + no bare PR-number refs + jargon-without-gloss blocklist. Fail-closed (exit 1). Encodes the checkable surface; whether the plain words are true/clear remains judgment. |
| 2.2 | The Delivery Gate | ENCODED-WEAK | `is_quiet_hour()` + `validate()` in `~/workspace/goals/bring-naya-to-life/hidden_files/report/hourly_report_pdf_v6.py` refuse recycled no-update pages (fail-closed, exit 2) — but only for hourly reports; the five-condition usefulness judgment (useful/valuable/accurate/on-brand/aligned) has no machine. |
| 2.3 | Lane Traffic Stays in the Lanes | JUDGMENT-ONLY | A message's intended recipient and proper lane is routing intent; no static check can verify where a seat chose to speak. |

## DOMAIN 3 — EXECUTION

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 3.1 | Parallel by Default | JUDGMENT-ONLY | "Can be done in parallel" requires dependency analysis no static check performs; "simpler to do one at a time" is a motive, not a pattern. |
| 3.2 | The Automatic Machine | ENCODED-WEAK | `tools/auto_merge_gate.py` encodes green+scorecard+no-conflicts→merge as a fail-closed predicate, but nothing invokes it; the diagnose-WHY-and-HOW requirement is prose. |
| 3.3 | The Pair Model | ENCODED-WEAK | `tools/auto_merge_gate.py` records `author_seat`/`owner_seat` and requires a second-seat ack comment on full-tier merges, but enforces no scorer≠builder predicate and is not CI-invoked; below-9.0 iteration is process. |
| 3.4 | The Allocation Law | JUDGMENT-ONLY | Priority ranking and agent placement are situational judgment; no artifact proves an agent is on the highest-leverage hole. |
| 3.5 | The Loop-Breaker Law | JUDGMENT-ONLY | Spotting a loop requires pattern recognition over time; a linter cannot tell a loop from diligent iteration. (`tools/board_claim_scan.py` prevents one class — duplicate builds — at build time; not the law.) |
| 3.6 | The Ownership Directive | JUDGMENT-ONLY | Acting on a "clear win" requires judging clarity; confidence is not checkable. |
| 3.7 | Proactive Fix Authority | JUDGMENT-ONLY | "See it broken" requires perception and judgment; walking past is invisible to any check. |
| 3.8 | Don't Report the Cliff — Remove It | JUDGMENT-ONLY | Distinguishing a removable cliff from a genuine warning requires design judgment. |
| 3.9 | The 6→10 Doctrine | JUDGMENT-ONLY | Blast-radius and reversibility risk assessment is judgment; the checklist is a thinking tool, not a pattern. |
| 3.10 | Build What Should Be | JUDGMENT-ONLY | The vision of what a thing should be is the seat's highest judgment; no machine holds the ideal. |
| 3.11 | The Machine That Purrs | JUDGMENT-ONLY | This law is ABOUT building systems like this audit; no instance can verify its own completeness. |

## DOMAIN 4 — LEARNING

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 4.1 | The Drink-First Law | ENCODED-NEW | NEW `check_activation_receipt.py`: artifact dir must contain a valid ACTIVATED receipt (schema `naya.activation.receipt.v1`, all identity/authority/timestamp fields, verification evidence). Fail-closed (exit 1). Honest limit: cannot prove the ritual was genuine — receipt honesty is Law 5.5. |
| 4.2 | Bake It In | JUDGMENT-ONLY | A machine cannot tell a re-teach from a legitimately needed adaptation; "solved stays solved" is architectural judgment. |
| 4.3 | Documentation Completeness | ENCODED-WEAK | `tools/sn002_conformance.py` (exercised via `live-intelligence-commit-proof.yml` + pytest) gates capture JSON on typed values — a real check on capture conformance — but the law's all-forms×all-places matrix (machine code / structured / AI language / human language × repo / doctrine / lessons / checklist / memory) has no automated check. |
| 4.4 | Proactive Capture | JUDGMENT-ONLY | "Something that needs to be put in the system" is a value judgment; no check can see a lesson that evaporated. |
| 4.5 | The Repeat Test | JUDGMENT-ONLY | Logging repeats presumes recognizing a repeat happened; a machine cannot detect that Shawn was made to repeat himself. |
| 4.6 | The Evidence Law | ENCODED-NEW | NEW `check_evidence_claims.py`: every quantified/state claim in report markdown must carry a citation marker (#NNNN, URL, SHA, file path, evidence:/source:/proof: label, footnote). Fail-closed (exit 1). Honest limit: enforces citation PRESENCE, not citation truth. |
| 4.7 | Verify Builder Artifacts | ENCODED-WEAK | The live-*-proof workflows verify live runtime artifacts against evidence; but no standing check forces artifact-handle verification before a seat accepts a delegated "done" — that remains seat discipline per the AGENTS.md boot contract. |

## DOMAIN 5 — AUTHORITY

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 5.1 | The Director Is Not Above the Protocol | JUDGMENT-ONLY | Recognizing a protocol violation by anyone — including Shawn — and fixing it is judgment plus action; no check watches the watchers. |
| 5.2 | Protected Gates | ENCODED-WEAK | `governed-supabase-production-deploy.yml` requires a typed DEPLOY confirmation + director-authorized source SHA for production promotion (fail-closed human gate). But no machine scans for credential/money use, destructive actions, or authority/privacy changes — three of the five gates are prose. |
| 5.3 | The Law Is the Code | ENCODED | `tools/ratified_guard.py` + `.github/workflows/ratified-guard.yml` (runs on PR and push, exit 1): deleting or altering a ratified object without a retirement record fails the build. Fail-closed and CI-enforced. |
| 5.4 | The Scorecard Law | ENCODED-WEAK | `tools/auto_merge_gate.py` validates receipt structure (five steps, rigor tier, lane/owner/author fields) fail-closed when run; but it does not verify score ≥9.0, does not enforce scorer≠builder, and is not invoked by CI. |
| 5.5 | The Honesty Covenant | JUDGMENT-ONLY | Honesty cannot be linted; the covenant is verified experientially ("if the experience doesn't match the number, the number was a lie"). |
| 5.6 | The Autonomous Operating Model | JUDGMENT-ONLY | Posture and initiative; no artifact proves a seat didn't wait. |
| 5.7 | Triple-A Awesomeness | JUDGMENT-ONLY | "Awesomeness" is taste; the bar is a human verdict. |
| 5.8 | The Awesome Rule | JUDGMENT-ONLY | Same as 5.7 — "sub-awesome as incident" requires judging quality. |

## DOMAIN 6 — CONSTITUTION

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 6.1 | The Law of One v2 | ENCODED-WEAK | Its operational requirements split three ways: (1) calculator run — partially encoded by the merge-gate predicate for merges only; (2) honest scores — judgment (5.5); (3) harm check — judgment. The decision equation is arithmetic, but benefit/honesty/safety inputs are judgment. Mostly judgment, with a weak merge-time encoding. |
| 6.2 | Constitutional Hierarchy | JUDGMENT-ONLY | Resolving apparent conflicts between laws is legal-style reasoning; precedence cannot be pattern-matched. |
| 6.3 | Amendment | ENCODED | Same machinery as 5.3: `tools/ratified_guard.py` + `ratified-guard.yml` fail-closed (exit 1) against constitutional change without a retirement record. Honest limit: the check enforces the record exists; the authenticity of "the Human Director's explicit word" inside it is judgment. |

## DOMAIN 7 — DESIGN

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 7.1 | The Design Standards Are the Law | ENCODED-WEAK | No machine verifies a seat "consulted" the standards; the report design gate checks block-composition markers (see 7.6) — a narrow mechanical slice. |
| 7.2 | Readability Supremacy | JUDGMENT-ONLY | Readability of rendered output requires seeing it; per 7.7 Shawn's eye outranks every score. |
| 7.3 | Jewel Colors Are for Jewels | JUDGMENT-ONLY | Text-fill vs. glow-decoration cannot be distinguished without rendering; a hex scan would false-positive on every legitimate accent. |
| 7.4 | The Lighting Standard | JUDGMENT-ONLY | Idle/hover/active states are interactive and rendered; static code cannot verify them. |
| 7.5 | The Design Gate | ENCODED-WEAK | `hourly_report_gate.py` (`design_gate()` + `negative_controls()`) is fail-closed for the v6 hourly report renderer (exits 2/3, and its negative controls prove it can fail) — but it gates one report, not all design work reaching Shawn. |
| 7.6 | Blocks, Not Instructions | ENCODED-WEAK | The report gate checks block-composition markers (`board-spine`, `metric-mark`, `delta-row`, `decision`) fail-closed for reports; no general validator checks the block index or forbids ad-hoc CSS repo-wide. |
| 7.7 | The Transmission Standard | JUDGMENT-ONLY | Whether a specimen IS the feeling and whether the laws are truly pass/fail is judgment; completeness of "specimen+code+laws" cannot be pattern-matched. |
| 7.8 | Never Duplicate | ENCODED-WEAK | `tools/board_claim_scan.py` returns COLLISION (exit 2, fail-closed when run) against duplicate builds at build time — but it is a manual tool, not CI-invoked, and nothing scans the repo for duplicate implementations. |
| 7.9 | Truth Is Visual | JUDGMENT-ONLY | Visual truth needs a rendered eye; "fake liveness" is a perception judgment. |
| 7.10 | The Intent Law (design) | JUDGMENT-ONLY | Same as 1.7 — intent-reading. |

## DOMAIN 8 — CODE

| # | Law | Verdict | Check / Why |
|---|-----|---------|-------------|
| 8.1 | The Engineering Truth Law | ENCODED-WEAK | Tests and live-proof workflows verify specific transitions at their layers; but "no stage inheritance" as a general rule has no check — nothing stops a doc from claiming VERIFIED on TESTED evidence outside the new evidence-claim linter's citation rule. |
| 8.2 | Green CI or Don't Merge | ENCODED-WEAK | `kernel-tests.yml` runs pytest + node tests + brain-index drift check on PR/push (fail-closed in CI); but the auto-merge gate's receipt predicate is not CI-invoked, "undoable in one step" is unchecked, and required-status-checks is a GitHub repo setting, not code. |
| 8.3 | Proof Must Not Exceed Evidence | ENCODED-NEW | NEW `check_evidence_claims.py` (shared with 4.6): claims must carry citations; UNKNOWN/BLOCKED/IMPLEMENTED asserted as VERIFIED without a citation fails. Existing partial: `collective-chain-readiness-gate.yml` refuses fake completeness by failing only on regression below a committed baseline. |
| 8.4 | No Silent Fallbacks | JUDGMENT-ONLY | Detecting "code that behaves as if a missing dependency were present" requires semantic analysis; no check marks unwired gaps by name. |
| 8.5 | Merge Mechanics | ENCODED-WEAK | The law names `tools/verify_gitdata_merge_tree.py` as "the mechanical form" — **that file does not exist in the repo** (verified by search). The tip-re-verification half is partially encoded by `auto_merge_gate.py` P2/P4 (fail-closed when run, not CI-invoked). Procedure documented; mechanical verifier absent. |
| 8.6 | Remote Is Truth | JUDGMENT-ONLY | A claim-discipline rule about how a seat asserts remote state; there is no artifact for a check to inspect — the check would have to intercept the claim. |
| 8.7 | Migrations and State Files | ENCODED-WEAK | Migration half is strong: `tests/test_production_migration_history_baseline.py` asserts the active migration directory EXACTLY equals the governed ledger (sha256 per file), fail-closed under pytest in CI. State-file half (atomic validated write pattern) has no check — unenforced prose. |
| 8.8 | Edge-Function Proof | ENCODED-WEAK | `deno check` on the full shipped handler is seat procedure from the H13 lesson; no workflow runs it — unenforced by any machine. |
| 8.9 | Reversibility | ENCODED-WEAK | `tools/auto_merge_gate.py` checks `reversible` / `no_major_damage` gate fields and P7 (revertable in one commit) fail-closed when run; general blast-radius judgment before code actions has no check. |

---

## Summary counts

- **ENCODED: 2** — 5.3 (The Law Is the Code), 6.3 (Amendment). Both via `ratified_guard.py` + `ratified-guard.yml`, fail-closed in CI.
- **ENCODED-WEAK: 21** — 1.2, 1.4, 1.8, 2.2, 3.2, 3.3, 4.3, 4.7, 5.2, 5.4, 6.1, 7.1, 7.5, 7.6, 7.8, 8.1, 8.2, 8.5, 8.7, 8.8, 8.9. Checks exist but are bypassable, single-surface, or not wired into an enforced path.
- **ENCODED-NEW: 4** — 2.1 (`check_plain_words.py`), 4.1 (`check_activation_receipt.py`), 4.6 + 8.3 (`check_evidence_claims.py`). Fail-closed, stdlib-only, tested. Pending wiring into CI to become fully ENCODED.
- **JUDGMENT-ONLY: 32** — 1.1, 1.3, 1.5, 1.6, 1.7, 2.3, 3.1, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 4.2, 4.4, 4.5, 5.1, 5.5, 5.6, 5.7, 5.8, 6.2, 7.2, 7.3, 7.4, 7.7, 7.9, 7.10, 8.4, 8.6.

59 laws audited (source: `BRAIN/01-GOVERNANCE/0008-OPERATING-LAW-V1.md`,
ref `naya4/operating-law-v1`). 27 have some machine encoding (2 strong,
21 weak, 4 new — source: the domain tables above); 32 are judgment-only
by nature.

## The judgment-only list, in one line each

These laws require taste, intent-reading, perception, or reasoning no
static check can perform without inventing the law:

- **1.1 Mantra** — "most intelligent" is irreducibly judgmental.
- **1.3 Intelligence Question** — an unobservable cognitive act.
- **1.5 Score-Fill-Ship** — honesty of a score and reality of holes need judgment.
- **1.6 Judgment Rule** — telling a wrong instruction from a right one IS the judgment.
- **1.7 / 7.10 Intent Law** — intent-reading; silent substitution is undetectable.
- **2.3 Lane traffic** — routing intent, not a pattern.
- **3.1 Parallel by default** — dependency analysis; motives aren't patterns.
- **3.4 Allocation** — situational priority judgment.
- **3.5 Loop-breaker** — loops vs. diligence needs temporal pattern recognition.
- **3.6 Ownership** — confidence judgment.
- **3.7 Proactive fix** — requires perception; walking past is invisible.
- **3.8 Remove the cliff** — design judgment.
- **3.9 6→10** — blast-radius risk assessment is judgment.
- **3.10 Build what should be** — the ideal is the seat's highest judgment.
- **3.11 Machine that purrs** — self-referential; no instance verifies its own completeness.
- **4.2 Bake it in** — re-teach vs. adaptation is architectural judgment.
- **4.4 Proactive capture** — value judgment; evaporated lessons are invisible.
- **4.5 Repeat test** — recognizing a repeat is the hard part.
- **5.1 Director not above protocol** — judging violations by anyone, then acting.
- **5.5 Honesty covenant** — honesty is verified experientially, not linted.
- **5.6 Autonomous model** — posture, not an artifact.
- **5.7 / 5.8 Awesomeness** — taste; a human verdict.
- **6.2 Constitutional hierarchy** — legal-style conflict reasoning.
- **7.2 Readability** — needs a rendered eye; Shawn's eye outranks scores.
- **7.3 Jewel colors** — text-fill vs. glow needs rendering.
- **7.4 Lighting standard** — interactive states need interaction.
- **7.7 Transmission standard** — whether a specimen IS the feeling is judgment.
- **7.9 Truth is visual** — perception judgment.
- **8.4 No silent fallbacks** — needs semantic analysis of unwired deps.
- **8.6 Remote is truth** — claim discipline with no artifact to inspect.

## Honest caveats (what this pass does NOT do)

1. **The biggest unenforced surface is the merge path.** `tools/auto_merge_gate.py`
   is the strongest predicate in the repo (P1–P9, fail-closed, UNKNOWN != PASS)
   and *nothing in CI invokes it*. Laws 1.2, 1.4, 1.8, 3.2, 3.3, 5.4, 6.1, 8.2,
   8.9 all lean on it. One workflow step calling it on PRs would promote eight
   ENCODED-WEAK marks toward ENCODED. Recommended as the single highest-leverage
   wiring task.
2. **`tools/verify_gitdata_merge_tree.py` is referenced by Law 8.5 as the
   mechanical form and does not exist in the repo.** The law cites a check
   that was never built (or never merged). This is a genuine hole, not a
   weak check.
3. **The new checks enforce form, not truth.** The evidence linter requires
   citations, not true citations (Laws 5.5/4.6-honesty remain judgment). The
   plain-words linter requires meaning to lead, not meaning to be clear. The
   receipt check requires a complete ACTIVATED receipt, not a genuine
   activation. Each docstring states its honest limit.
4. **New checks are ENCODED-NEW, not ENCODED**, until a CI workflow or gate
   invokes them. The runner (`run_activation_checks.py`) is the invocation
   seam; `--strict` makes absent gates fail instead of skip.
5. **No invented laws.** Every check maps to a REQUIRES/FORBIDS line in the
   Operating Law v1. Thresholds (5-word PR rule, 30-line lead window, ±2-line
   gloss window, 900s evidence age) are the check authors' operationalization
   choices and are documented as such in each check's docstring.
