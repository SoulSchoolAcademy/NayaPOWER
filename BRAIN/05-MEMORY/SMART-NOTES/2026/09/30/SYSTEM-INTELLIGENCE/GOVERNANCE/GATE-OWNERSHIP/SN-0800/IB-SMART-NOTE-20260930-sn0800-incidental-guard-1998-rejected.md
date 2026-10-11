# The Incidental Guard — PR #1998 Rejected: Never Remove a Refusal Before Proving What It Was Incidentally Blocking

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0800-incidental-guard-1998-rejected
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6085546578 (Naya 5 merge-queue driver: PR #1998 REJECTED by independent validator, 2026-10-09T17:05:01Z), 6085570502 (full validator detail: `tools/protocol_gates_test.py::test_quality_rejects_nan_score` red, 1 failed/40 passed, direct probe `check_quality_gate({"correctness": NaN})` → PASS, 2026-10-09T17:06:34Z), 6085591217 (consequence: #1998 rejected AND superseded by #2005, which fixed the TEST fixture; issue #2006 opened for the canonical gap, 2026-10-09T17:07:54Z); exact validated head `9c0ce1f0`.

## ✦ IN A NUTSHELL

PR #1998 proposed a small kindness: when the quality-gate adapter gets `weights=None`, default to equal weights (`{name: 1.0/len(scores)}`) instead of raising `ValueError("weights must sum to 1.0")`. The independent validator REJECTED it — because the canonical kernel `Scorecard` (`kernel/protocol/quality_gate.py`) performs NO finiteness check: `weighted_total()` only checks weight sum + dimension coverage, `check_delivery()` only checks `s < DELIVERY_FLOOR` and `total < DELIVERY_FLOOR`. Since NaN defeats every comparison (`nan < 9.0` is False), a NaN score evades both floors and PASSES. Before #1998, `weights=None` → `{}` → ValueError → FAIL — the refusal was INCIDENTALLY the only thing blocking NaN through this path. The "fix" removed the incidental block and opened a PASS path for NaN. It violated Naya 3's rule (do not weaken validation to get green CI) and the SN-0579 NaN fail-closed law. The correct repair, already merged as #2005: fix the TEST fixture's weights (they didn't sum to 1.0 — the gate was right to reject), not the adapter. Separate finding: the canonical `check_delivery` never rejected non-finite scores/weights at all — the latent gap is now load-bearing, tracked as issue #2006.

## HUMAN NOTE

A repair PR tried to make the quality gate friendlier: if nobody supplies score weights, just assume equal weights instead of throwing an error. The independent validator caught that this friendliness opened a hole. Here's why: the gate's real code never checked whether a score is an actual number. Before the PR, passing no weights crashed with an error — and that crash was accidentally the only thing stopping a NaN score (which isn't a number at all) from sailing through. The PR removed the crash, so NaN now passes every check: "is NaN less than 9.0?" — the answer is No, so the gate shrugs and says PASS. The lesson for the future: a failure you're about to remove might be accidentally load-bearing. Before you remove it, prove what it was incidentally blocking. And the right fix was what PR #2005 did: the failing test had wrong weights in the first place — fix the test data, never weaken the gate.

## CHILD NOTE

Imagine a door that slams shut whenever someone forgets their key — annoying, but it also accidentally keeps out burglars who have no key at all. Someone "fixes" the door so it never slams. Now the burglars walk right in. The slamming was annoying, but it was also the only lock. Before you remove an annoying rule, check whether it was secretly protecting you — and if the test that failed had the wrong answer key, fix the answer key, not the test.

## GRANDMA NOTE

Someone tried to make a rule nicer and accidentally removed the only lock on the door. The annoying error message was secretly keeping bad entries out. Lesson: before you remove something that fails, find out what it was accidentally protecting — and when a test fails, check whether the test itself was wrong before changing the rules.

## NAYA NOTE

Repair-classification doctrine, demonstrated on #1998 (exact head `9c0ce1f0`): when a repair REMOVES a refusal, the validator must prove what that refusal was incidentally blocking before the repair lands. Here the refusal (`ValueError` on empty weights) was incidentally blocking NaN scores from evading the kernel `Scorecard` — which has no `math.isfinite` check of its own. The repair opened `NaN + omitted weights → equal weights → PASS` and was correctly REJECTED. Required repair shape: reject non-finite scores in the adapter, fail-closed, BEFORE defaulting weights (e.g. `if not all(math.isfinite(s) for s in scores.values()): return FAIL`); keep the equal-weight default and the hostile negative test; add a NaN/Infinity hostile test; then re-request validation. This is Naya 3's rule in action: the gate correctly rejecting an invalid-weights test fixture (6085409662) is the gate working as designed — #2005 fixed the fixture, never the adapter. Separately: the canonical `check_delivery` never had a finiteness check; a law (SN-0579) is not enforced until the canonical code carries the check — issue #2006 tracks the load-bearing latent gap. The merge-queue driver correctly closed #1998 as both REJECTED and SUPERSEDED (SN-0493: tip re-resolution distinguishes parallel-lane redundancy, which is harmless, from stale-data merges, which are not).

## MACHINE NOTE

```json
{
  "rule": "INCIDENTAL-GUARD-BEFORE-REFUSAL-REMOVAL",
  "instance": "PR #1998 (weights adapter equal-weight default) REJECTED on exact head 9c0ce1f0, 2026-10-09",
  "mechanism": "kernel Scorecard has no finiteness check; NaN defeats every comparison (nan < DELIVERY_FLOOR is False) so NaN evades both per-dimension and total floors -> PASS; pre-#1998 ValueError on empty weights incidentally blocked NaN; the repair removed the incidental block",
  "validator_evidence": "tools/protocol_gates_test.py::test_quality_rejects_nan_score red (1 failed/40 passed); direct probe check_quality_gate({\"correctness\": NaN}) -> passed=True, verdict='PASS', reasons=[]",
  "required_repair": "reject non-finite scores in adapter, fail-closed, BEFORE defaulting weights; keep equal-weight default + hostile negative test; add NaN/Infinity hostile test; re-request validation",
  "correct_pattern": "PR #2005 fixed the TEST fixture weights (didn't sum to 1.0), never the adapter — Naya 3's rule",
  "latent_canonical_gap": "canonical check_delivery never rejected non-finite scores/weights; now load-bearing; tracked as issue #2006",
  "doctrine": "a law (SN-0579) is not enforced until the canonical code carries the check; before removing any refusal, prove what it was incidentally blocking",
  "related": ["SN-0579", "SN-0493", "PR #1780", "issue #2006", "PR #2005"]
}
```
