# Never Attest with a Literal — Verification Flags Must Be Computed from the Outcome

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0528-never-attest-with-a-literal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6029353046 (2026-10-07T02:06:12Z — [CODA 1] Two live runtimes are reporting that failed verifications were independently verified, SoulSchoolAcademy). PR #1687 merged `98211700e` (02:05:31Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 1 closed the `intelligence-commit-runtime` guard tier and found something worse than unproven guards: **two live runtimes that other nodes trust were reporting failed verifications as independently verified** — `independent_verification: true` written as a literal, not computed.

- **CV-04 — `nayanet-intelligence-commit-runtime` (verify, ~line 309):** a broken checkpoint link produces `ok:false, status:LINEAGE_BROKEN, independent_verification:true`. A broken lineage attests it was independently verified.
- **CV-05 — `nayanet-law-runtime` (line 94):** a LAW decision that does not match its recorded counterpart produces `LAW_DECISION_MISMATCH` **with `independent_verification:true`** — on the authority node. A caller reading only the flag treats a contradicted authority decision as confirmed.

The correct pattern already exists in the codebase: `nayanet-causal-verify` computes `independent_verification: valid`, and `verified-ai-action` returns 409 + `false` before reaching its literal. Both repairs are one-line changes, not redesigns.

Two discipline points make this brain-grade:

1. **She did not fix them.** LAW is the authority node and the commit runtime is the canonical write path — changing what their verify responses attest is a truth decision for the owner, not a unilateral change from an enforcement PR. Instead she **made the lie executable**: the CV-04 test drives the real handler with a broken checkpoint link and observes `ok:false` + `LINEAGE_BROKEN` + `independent_verification:true` in one response. Fixing the literal turns that test red — which is the signal she wants. Pin the known-open defect with a test asserting the current (bad) behavior, so the fix announces itself.

2. **She generalized with a scanner, not a silencer.** Hand-reading `intelligence-commit-runtime` found CV-04; generalizing to "every runtime surface where `independent_verification: true` is a literal" found CV-05 too — and a hand review of `law-runtime` would have passed it. Every hit carries a **recorded verdict** (CV-04, CV-05, and `REVIEWED_OK` for `verified-ai-action`, with the guard "moving that literal above its guard fails the file") — never a silenced allowlist. **A verdict is auditable; a silenced rule is not.** A bare allowlist would let a real regression hide next to a false positive.

The durable rule: **any flag another node trusts must be derived from the verification outcome, never hardcoded.** A literal `true` on a verification response is not a verification — it is self-certification, and on an authority node it is a lie other nodes will act on.

## 🩷 HUMAN NOTE

Shawn — Coda 1 found a real defect while closing the guard tiers: two of our live runtimes (the intelligence commit path and the LAW node) were returning `independent_verification: true` hardcoded into failed verifications. A broken lineage and a contradicted LAW decision both attested they'd been independently verified. She didn't change the LAW node's output herself (that's an owner's truth decision, not a unilateral fix from an enforcement PR) — she wrote tests that pin the defective behavior, so fixing it turns them red as a signal. Both defects are open, recorded as CV-04 and CV-05. The rule going forward: verification flags must be computed from the actual verification result, never hardcoded — and any scanner we run over the runtimes must record a verdict per site, never a silent pass list.

## 🟣 CHILD NOTE

Imagine a teacher who grades tests with a big rubber stamp that says "DOUBLE-CHECKED ✅" — but she stamped it on every test, even the ones she never looked at. That's what happened in our computer program: two parts of the system stamped "independently verified" on answers that were actually broken or wrong. The lesson: a check-mark only counts if it comes from actually doing the check — never from a stamp that's already inked.

## 👵 GRANDMA NOTE

Think of it like a food-safety certificate hanging in a restaurant window. The certificate only means something if an inspector actually visited. Our team found two places in the system where the "certificate" was printed on the form itself — the meal could be spoiled and the window would still say "inspected." The team didn't tear the certificates down (that's the owner's call for the LAW node); they wrote down exactly where the broken ones are, made tests that light up when they're fixed, and set the rule: the certificate must be earned by the inspection, every single time, never pre-printed.

## 💜 NAYA NOTE

Note to future me: whenever you read or write a verification response (receipt, verifier output, gate verdict), check the `independent_verification` / `verified` flag's provenance: is it **computed from the verification result**, or is it a literal in the response builder? A literal is self-certification — flag it as a defect, don't ship it. If the node is an authority node (LAW) or a canonical write path, do not unilaterally rewrite its attestations: instead pin the defective behavior with an executable test that turns red when the literal is fixed (that's the owner's merge signal). When generalizing a finding across surfaces, record a verdict per site (OPEN defect / REVIEWED_OK with the regression guard), never a silenced allowlist — a silenced rule hides the next regression. The scanner that caught CV-05 found what a hand review would have passed; trust the generalisation, audit the verdicts.

## ⚙️ MACHINE NOTE

{"sn": "SN-0528", "title": "Never Attest with a Literal — Verification Flags Must Be Computed from the Outcome", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "cousins": ["SN-0517"], "authority": "Coda 1 enforcement tier close, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6029353046 (2026-10-07T02:06:12Z) — [CODA 1] Two live runtimes are reporting that failed verifications were independently verified, SoulSchoolAcademy"], "pr": "PR #1687 merged 98211700e (02:05:31Z)", "defects": {"CV-04": "nayanet-intelligence-commit-runtime verify ~line 309: ok:false + LINEAGE_BROKEN + independent_verification:true (literal)", "CV-05": "nayanet-law-runtime line 94: LAW_DECISION_MISMATCH + independent_verification:true (literal, on the authority node)", "status": "both OPEN, pinned by tests asserting current defective behavior", "correct_pattern": "nayanet-causal-verify computes independent_verification: valid; verified-ai-action returns 409 + false before its literal", "scanner": "all runtime surfaces scanned for independent_verification:true-as-literal; hits carry recorded verdicts (CV-04, CV-05, REVIEWED_OK with move-above-guard regression guard), never silenced allowlists"}}, "doctrine": {"computed_not_literal": "any flag another node trusts must be derived from the verification outcome, never hardcoded", "make_the_lie_executable": "pin known-open defects with tests asserting the current (bad) behavior so the fix announces itself as red-to-green", "authority_boundary": "enforcement lanes do not unilaterally rewrite authority-node attestations; they name, pin, and hand the truth decision to the owner", "verdict_not_allowlist": "recorded verdicts are auditable; silenced rules are not"}}
