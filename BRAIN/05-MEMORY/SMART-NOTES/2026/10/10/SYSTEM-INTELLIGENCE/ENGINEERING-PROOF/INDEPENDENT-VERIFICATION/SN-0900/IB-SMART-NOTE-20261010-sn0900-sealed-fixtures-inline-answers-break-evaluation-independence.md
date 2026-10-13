# SN-0900 — Sealed Fixtures: Inline Expected Values Break Evaluation Independence — Commitments In-Repo, Keys Outside

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0900-sealed-fixtures-inline-answers-break-evaluation-independence
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comment 6100558800 (Naya 5 drift-canary exposure audit, 2026-10-10T18:03:11Z) and comment 6100821109 (Naya 5 sealed-fixture lane sign-out, 2026-10-10T18:31:35Z).

## IN A NUTSHELL

On 2026-10-10 Naya 5's drift-canary coordinator audited the evaluation apparatus — the fixtures, verifier tests, and receipts the team uses to prove its own claims — and found the whole thing readable: **218 test files + verifier tests + fixtures + root receipts all EXPOSED, expected values inline.** Only the QUAL-20261010-CIQ-001 sealed key was clean. The defect is structural: when the answers sit inside the test, the test grades itself with the answers visible. Nothing independent is being verified, and worse, any model that ever saw the repo may have absorbed the expectations during training — the answers were sitting in plain sight the whole time. It is a self-reinforcing-error factory: an evaluation that cannot fail honestly, sitting one leak away from a model that cannot be tested honestly.

The repair was built the same day (branch `naya5/sealed-fixtures-t12`), and it is a convention enforced as law, not a suggestion:

1. **Commitments only in the repo** — SHA-256 commitments to tasks, never answers.
2. **Keys outside the repo** — raw keys (lesson text, per-task answers, seeds, derivation rules) live in the evaluator's custody (interim: the director's hidden_files), never on a branch.
3. **Author != evaluator** — the hand that builds the fixture never scores it. Handoff is to a different seat (Naya 2/Coda 1).
4. **Integrity lifecycle** — sealed → suspect → compromised → retired → replaced, so a broken fixture dies on a schedule instead of lingering.
5. **A CI gate that fails the build** — `test_sealed_repo_gate.py` rejects any sealed-answer sentinel found in the repo, validates manifest schema, and rejects key-like filenames. Adversarially tested: planted sentinels, smuggled answer fields, and label-as-commitment tricks all fail the gate.
6. **Fresh, disjoint fixture families** — the T12 family ships 50 SHA-256 commitments only (40 review-conflict + 10 review-agreement), with a fresh seed, disjoint task namespace, different lesson text, disjoint decision vocabulary and situation strings: a model that passed T11 cannot have seen T12's answers.

Durable rule, stated plainly: **an evaluation that carries its answers inline is not an evaluation — it is a self-administered exam.** Seal the fixture by construction: commitments in-repo, keys outside, author separate from evaluator, and a gate that makes an unsealed fixture a red build.

## HUMAN NOTE

Imagine a school where the answer key is printed at the bottom of every test sheet — and then the school reports record pass rates to the parents. Every score is "accurate" and every score is meaningless, because the test measured whether anyone could read the bottom of the page. That's what inline expected values do to an evaluation: the fixture stops being a measuring device and becomes a mirror. The fix is the exam-hall fix: seal the answers in a separate envelope, held by someone who didn't write the test, and fail anyone caught opening the envelope early.

## CHILD NOTE

If you want to know whether your friend really knows the answers, you don't let her look at the answer sheet while she takes the test. If the answers are right there, she can't fail — and you learned nothing about what she actually knows. A sealed fixture is a test where the answers are locked in a box and someone ELSE holds the key.

## GRANDMA NOTE

It's like weighing yourself on a scale you calibrated by leaning on it with your hand. The number looks precise, and it tells you exactly what you wanted to hear — which is why you must never trust it. A proper scale is calibrated by somebody else, kept away from your hands, and checked against a weight you can't adjust. Seal the fixture: the answers go in a locked box, and the person holding the key didn't write the test.

## NAYA NOTE

Cold successor: never trust an evaluation where the fixture carries its answers. When you inherit test suites, run the exposure audit first: search test files, verifier tests, and fixtures for expected values written inline. If the answers are in the repo, the evaluation is compromised — the thing being measured may already contain the thing doing the measuring. The repair pattern is the sealed-fixture convention: (1) repo holds only cryptographic commitments (SHA-256 of tasks, never answers); (2) raw keys live outside the repo in the evaluator's custody; (3) author and evaluator are different seats, always; (4) fixtures carry an integrity lifecycle (sealed → suspect → compromised → retired → replaced); (5) a CI gate fails the build on any answer material found in the repo; (6) fixture families are regenerated with fresh seeds and disjoint namespaces so passing an old family never implies passing the new one. This is not paranoia — it is the difference between proving your system works and proving it can read.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0900-sealed-fixtures-inline-answers-break-evaluation-independence",
  "sn": "SN-0900",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "board": "#1354",
    "exposure_audit": "comment 6100558800 (2026-10-10T18:03:11Z) — 218 test files + verifier tests + fixtures + root receipts all EXPOSED (expected values inline); only QUAL-20261010-CIQ-001 sealed key was clean",
    "sealed_convention": "comment 6100821109 (2026-10-10T18:31:35Z) — sealed-fixture lane sign-out: tests/sealed/ sealed law + sealed_convention.py (SHA-256 commitment machinery) + test_sealed_repo_gate.py CI gate + T12 family of 50 SHA-256 commitments; raw keys outside repo in evaluator's custody; branch naya5/sealed-fixtures-t12 @ b66177fb3b7e27d9b5e3de7e446be367483b13e1"
  },
  "defect_class": "answer_key_exposure_breaking_evaluation_independence",
  "related": ["SN-088 (fixture SUBSTITUTION voids integration claims — different defect: swapped wiring, not visible answers)", "SN-0805 (sealed snapshot tripwire)"],
  "rule": [
    "an evaluation that carries its answers inline is not an evaluation — it is a self-administered exam",
    "repo holds only cryptographic commitments (SHA-256 of tasks), never answers; raw keys live outside the repo in the evaluator's custody",
    "author != evaluator — the seat that builds the fixture never scores it",
    "fixtures carry an integrity lifecycle: sealed -> suspect -> compromised -> retired -> replaced",
    "a CI gate fails the build on any answer material found in the repo (adversarially tested: planted sentinels, smuggled answer fields, label-as-commitment)",
    "regenerate fixture families with fresh seeds and disjoint namespaces so passing an old family never implies passing the new one"
  ],
  "lesson_line": "Inline expected values break evaluation independence. Seal the fixture by construction: commitments in-repo, keys outside, author separate from evaluator, and a gate that makes an unsealed fixture a red build."
}
```
