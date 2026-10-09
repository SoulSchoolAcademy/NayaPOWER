# Measure the Suggested Fix Before Adopting It — Adopt the Class Fix, Not the Instance Patch

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0815-measure-then-adopt-class-fix
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comments 6087846174 / 6087951505 (2026-10-09).
**Provenance:** #1354 6087846174 (STEWARD UPDATE — batch-3 confusables fix2 COMPLETE at honest 8.5 claim, 2026-10-09T19:31:09Z); #1354 6087951505 (batch-3 fix2 CONFIRMED: GO 9.0 independent, 2026-10-09T19:37:53Z). Branch `naya5/batch3-confusables-fix2 @ 12b8fb9d` (off `12801a9d`; remote tree 03d1c314 == local verified; never merged — Naya 4 opens the PR).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The batch-3 confusables repair had two verified holes (32 dead dictionary entries the normalizer bypassed; the decision-reports banned-words lane never got the translator). The independent re-validator proposed a fixpoint fix. The fixer did the rare, right thing: **it measured the suggestion before adopting it** — fold-alone fixed 0/32 (dead entries' NFKC outputs aren't table sources; re-folding changes nothing), extension-alone fixed 2/32 — and adopted the fix at the class level: fixpoint over the NFKC-after-fold composition (`fold_to_ascii_fixpoint`, converges ≤2 passes, proven + measured) plus 2 NFKC-closure entries. The fixer's own battery then showed 19/19 adversarial variants caught, honest names still passing, 1,566 tests green; the independent confirmer re-validated GO 9.0 on the pushed bytes. The durable method: **a reviewer's suggested fix is a hypothesis, not a verdict — measure each variant against the failing set, then adopt the class fix (the composition), never the instance patch.**

## 🩷 HUMAN NOTE

Shawn — the look-alike-letter repair had two real cracks, and the independent checker proposed a way to seal them. The repair crew didn't just take the suggestion — they tested each version of it first: one version fixed zero of the 32 broken cases, another fixed only two. So they went one level deeper and fixed the whole category at once: a loop that keeps cleaning until nothing changes, proven to settle in two passes or fewer. Then they attacked their own work 19 different ways — every attack caught, every honest name still passing, all 1,566 tests green — and a second pair of eyes confirmed it on the actual published code. The lesson: when someone suggests a fix, test the suggestion before you trust it, and fix the pattern, not the example.

## 👶 CHILD NOTE

Imagine your bike chain keeps slipping. A friend says "tighten this one bolt." You don't just tighten it — you try their idea and count how many slips it stops: zero. Then you try a different version: stops two out of thirty-two. Then instead of fiddling with bolts one by one, you adjust the whole gear setting that controls all of them — and check that it settles into place and stays. You count again: all thirty-two fixed. The lesson: test the advice before you follow it, and fix the whole gear, not one bolt at a time.

## 👵 GRANDMA NOTE

Sweetie, it's like a leaky pipe. The plumber suggests patching the spot — but you hold a bucket under it first and count the drips: the patch stops none, a second patch stops two out of thirty-two. So instead of patching spots, you replace the whole section of pipe — and then you run the water full blast to prove it holds. Test the suggestion, count what it fixes, and fix the pipe, not the drip. That's what the crew did here, and a second inspector double-checked their work on the finished job.

## 🤖 NAYA NOTE

When a reviewer or validator proposes a fix for verified holes:

1. **Treat the suggestion as a hypothesis.** Measure each candidate variant against the full failing set before adopting: here fold-alone 0/32, extension-alone 2/32 — numbers that made the instance-level patches inadmissible on sight.
2. **Adopt at the class level.** The adopted fix was the composition (fixpoint over NFKC-after-fold), proven to converge ≤2 passes — it closes the hole class, not the two observed instances. Instance patches rot; class fixes hold.
3. **Document why the rejected variants fail, not just that they do.** "Dead entries' NFKC outputs aren't table sources; re-folding changes nothing" is the reason fold-alone measured 0/32 — the reason travels to the next repair; the number alone doesn't.
4. **Claim honest, confirm independent.** The fixer claimed 8.5 (not 9.0) and the independent confirmer's GO 9.0 on pushed bytes (fresh worktree, read-only, ref/tree re-verified via API) is what opened the lane. Your own battery proves your work; only the independent seat's battery opens the lane.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0815",
  "class": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A suggested fix is a hypothesis: measure each variant against the failing set before adopting, then adopt the fix at the class level (the composition), never the instance patch. Document why rejected variants fail.",
  "worked_example": {
    "holes": "batch-3 confusables: 32 dead dictionary entries bypassed by NFKC-before-translate ordering; decision-reports banned-words lane never got the translator",
    "measurement": "re-validator's fixpoint suggestion measured first: fold-alone 0/32 (dead entries' NFKC outputs are not table sources; re-folding changes nothing), extension-alone 2/32",
    "adopted": "class fix: fixpoint over NFKC-after-fold composition (fold_to_ascii_fixpoint, converges ≤2 passes, proven + measured) + 2 NFKC-closure entries",
    "result": "19/19 fresh adversarial variants caught on pushed bytes; honest cases pass; 1566 tests green; independent confirmer GO 9.0",
    "head": "naya5/batch3-confusables-fix2 @ 12b8fb9d (off 12801a9d; server tree 03d1c314 == local; never merged — Naya 4 opens the PR)",
    "board_comments": "#1354 6087846174 (fix report), #1354 6087951505 (independent GO 9.0)"
  },
  "related": ["SN-0812"]
}
```
