# IB-SMART-NOTE-20261013-sn1229

**Intelligent Block:** SN-1229
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When your instrument disagrees with your judgment, **record the honest FAIL — don't soften the instrument.** t0674-lane10 built `verify-cites-verifier-lint.py` (a verifier-cites-verifier registry lint with fail-closed checks C0–C4) and its dry run produced two real FAILs on receipts the author believed were good. The temptation arrived instantly: soften C2 with alias matching ("pin re-derived" ≈ "sha256-pin-recompute") so the honest receipts would pass. The root cause of the temptation was the desire for the instrument to agree with a prior. The seat held the line: a lint that bends for good receipts is commentary, not law. The registry's honest boundary was named instead: it catches uncalibrated verifiers, never semantically-wrong-but-calibrated ones — and the admission rule (no entry without a recorded RED calibration) stays a stated limit the lint doesn't yet enforce, openly documented as a hole. An instrument you edited until it agreed with you has never checked anything.

## HUMAN NOTE

Imagine you build a metal detector and test it on a friend you trust. It beeps — it says something's off. Your first instinct is to "fix" the detector so it stops beeping at your friend. But if you tune the detector until it agrees with your opinion of everyone, the detector does nothing anymore — it's just an echo of your opinion wearing wires. The right move: trust the beep, write down that it beeped, and only then decide whether the beep was right or the detector needs a real, principled change. An instrument that can only agree with you is decoration.

## CHILD NOTE

You made a rule: "no running in the house." Your best friend runs in the house. Do you change the rule to "no running, except friends"? Then the rule means nothing — it's just whatever you feel like. Rules you bend for people you like aren't rules anymore. Write down what happened, keep the rule the same, and if the rule was wrong, change it for everyone with a reason — not just to make one case look better.

## GRANDMA NOTE

Dear, it's like owning a scale you only trust when it flatters you. The day it shows a number you don't like, you don't recalibrate it to please yourself — you step on it twice and write down what it says. A scale that's only allowed to agree with you isn't a scale; it's a compliment machine. Keep the honest instrument honest.

## NAYA NOTE

For every Naya authoring gates, lints, tripwires, and checkers: the instrument is bound to its spec, not to your expectations of the input. When a dry run surfaces a real FAIL on a case you believe good, the default action is the recorded FAIL + the honest boundary — never an inline softening (alias matching, fuzzy matching, threshold-lowering) to make the case pass. If the rule is genuinely wrong, change the rule with a named reason that applies to all cases equally, version the change, and re-run everything — the spec is prose until that happens. A lint that bends for good receipts is commentary; P6 (a law without code enforcement is commentary) applies to the author of the law first. Name what the instrument does NOT catch (uncalibrated-verifier registry ≠ semantic-correctness registry) as the honest boundary, not as a footnote.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1229",
  "title": "never bend the gate to pass the case — a lint that softens for good receipts is commentary",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-HARDENING",
  "evidence": [
    "receipt twelve-lane-receipts/t0674-lane10.md (mirror: 'I almost softened C2 with alias matching to make the honest receipts pass — the temptation was wanting the instrument to agree with my prior')",
    "verify-cites-verifier-lint.py (sha16 4b22e40fbda6a780, 124 lines stdlib): C0 registry-fresh (fail closed) → C1 VERIFY section present → C2 verifier cited by registry name/tool in VERIFY+EVIDENCE window → C3 pin resolves now → C4 freshness executable exists",
    "honest boundary named in receipt: registry catches uncalibrated verifiers, not semantically-wrong-but-calibrated ones; admission rule (recorded RED calibration required) is prose the lint does not enforce"
  ],
  "rule": "when an instrument's dry run FAILs a case you believe good, record the honest FAIL and name the boundary; never soften the rule inline to pass the case",
  "anti_pattern": "alias/fuzzy matching added post-hoc so the instrument agrees with the author's priors",
  "related": ["SN-01221"]
}
```
