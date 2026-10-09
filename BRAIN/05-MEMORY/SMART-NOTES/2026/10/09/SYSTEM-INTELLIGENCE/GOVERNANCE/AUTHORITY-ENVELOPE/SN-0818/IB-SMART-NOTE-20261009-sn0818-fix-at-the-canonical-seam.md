# Fix at the Canonical Seam — the Delegation Boundary Is Where the Next Bypass Hides

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0818-fix-at-the-canonical-seam
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comments 6088810093 / 6088846292 (2026-10-09).
**Provenance:** #1354 6088810093 ([NAYA 5 — INDEPENDENT RE-VALIDATOR — #1943 repair], 2026-10-09T20:34:53Z — B5 demonstrated bypass in the delegated checker); #1354 6088846292 ([NAYA 5 — #1943 REPAIR3: B5 fixed at the canonical seam], 2026-10-09T20:37:29Z); related: #1354 6088748791 (repair2 lesson: "falsifier suites must probe the time dimension"). Module: `tools/auto_merge_gate.py:215` (`_check_receipt`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The delegated-merge receipt gate went through two repair rounds for the same bug class — a bool accepted where an integer comment id is required (`isinstance(True, int)`). Repair2 fixed the two local `comment_id` fields and was verified green. Then the independent re-validator probed *through the delegation gate* and found the identical bypass one function call deeper: the repaired gate delegates its C2 step to the shared canonical `_check_receipt` in `tools/auto_merge_gate.py` — the module the repaired gate's own docstring describes as "the same mechanical checker … so the two gates cannot drift." The docstring's "cannot drift" claim was asserted while the two gates had drifted on exactly the quirk being repaired: a fully-valid receipt with only `receipt_posted_comment_id` changed from `6063575482` to `True` returned `(allowed=True, reasons=[])` — a bare bool satisfying "RECEIPT — written AND posted." Repair3 fixed it at the canonical seam itself (`isinstance(x, bool) or not isinstance(x, int)` at `auto_merge_gate.py:215`), plus one committed falsifier test, and the validator's exact probe then denied. The durable lesson, in the repairer's own words: **the fix location is what makes a "cannot drift" claim true instead of aspirational.** When a gate delegates to a shared "canonical" checker, the delegation boundary is where the next bypass hides — so validate the callee's field handling, not just the caller's, and fix at the seam, never as a local workaround that re-creates the drift the docstring denies. The validator's probes were red-first (proven on the unrepaired head, including `2099-12-31T23:59:59Z` from round one) — another live instance of the falsifier-must-fire family (SN-0531, SN-0603), now extended to delegated checkers: every delegated authority check needs falsifiers that cross the delegation boundary.

## 🩷 HUMAN NOTE

Shawn — two repair rounds on the same merge-permission lock, and the second round missed the hole because it sat one function call deeper, in a shared checker the lock *trusts completely*. The independent tester slipped a toy key ("yes" where a real key number goes) into the shared keyhole and the lock still opened. The fixer then repaired the shared keyhole itself — not a second patch on their own lock — so the two genuinely can't drift apart. The lesson we're banking: when a system delegates trust to a shared component, that boundary is exactly where the next bypass hides. And a docstring that says "these cannot drift" was aspirational until the fix landed in the shared spot — the fix *location* is what makes the claim true.

## 👶 CHILD NOTE

Imagine two locks that share one master keyhole — your front door lock and your bedroom lock both trust the same master key. Someone fixed two tiny cracks in your bedroom lock, then a friend checked the whole thing and found a third crack hiding in the shared keyhole the bedroom lock borrows. Fixing only your own lock wouldn't help — you have to fix the shared keyhole, because *that's* the crack both locks now share. Lesson: when you trust someone else's lock part, check that part too — and fix it where it lives, not with tape on your side.

## 👵 GRANDMA NOTE

Sweetie, this is about fixing things where they actually live. The team had a safety lock that borrows its keyhole from a shared workshop lock. They fixed their own lock twice and it looked perfect — but the borrowed keyhole still had a crack, because nobody thought to check the workshop's part. The tester found it, and the fixer finally repaired the workshop keyhole itself. The moral: when something you trust borrows a part from somewhere shared, the shared part is where the next problem hides. Fix it at the source, not with a patch on your end.

## 🤖 NAYA NOTE

When repairing or validating a delegated authority check:

1. **Map the delegation chain before fixing.** List every function the checker calls that touches untrusted input — `_check_receipt` inside `auto_merge_gate.py` is not "someone else's code," it is your gate's decision surface.
2. **Probe through the delegation boundary, not just the caller.** Falsifier probes must set the hostile value at the callee's field (e.g., `receipt_posted_comment_id=True` inside the nested `scorecard_receipt.step5_receipt`), because that is the actual attack path — the attacker's receipt flows through the shared checker, not around it.
3. **Fix at the canonical seam.** Apply the repair in the shared checker itself (`tools/auto_merge_gate.py`), never as a local workaround in the delegating module — a local patch re-creates exactly the drift the docstring denies, and the next reader will trust the docstring instead of your patch.
4. **Keep the claim honest.** If nothing in the merge path invokes the checker (`merge_pr_api.py`, the gh-api write path), the docstring must say "checker — advisory, not enforced" (as repair2 did) rather than "enforcement predicate." A gate is a checker, not an enforcer, until it is wired into the path it claims to guard.
5. **Standing idiom for the bool quirk:** `isinstance(x, bool) or not isinstance(x, int)` — the repo's repeated lesson (this round, #2026's `shape_closed`, the sibling instance at `tools/truth_state_guard.py:589` flagged for a future sweep).

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0818",
  "class": "GOVERNANCE",
  "subcategory": "AUTHORITY-ENVELOPE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "When a gate delegates to a shared canonical checker, the delegation boundary is where the next bypass hides: validate the callee's field handling (probes must cross the delegation boundary), and fix defects at the canonical seam itself, never as a local workaround — the fix location is what makes a 'cannot drift' claim true instead of aspirational.",
  "worked_example": {
    "artifact": "delegated-merge receipt gate #1943 repair2 (branch naya5/authority-gov-repair2 @ 6c36560f): bool quirk fixed on two local comment_id fields, 22/22 suite green",
    "bypass": "independent re-validator probed through the gate's C2 delegation into the canonical `_check_receipt` (tools/auto_merge_gate.py:215): receipt with only scorecard_receipt.step5_receipt.receipt_posted_comment_id 6063575482 -> True returned (allowed=True, reasons=[]) — demonstrated, not a regression",
    "fix": "repair3 (naya5/authority-gov-repair3 @ 86ddd073): standing bool-exclusion idiom applied at the canonical seam; validator's exact falsifier now denies; 23/23 green with one new committed falsifier test",
    "board_comment": "#1354 6088810093 (B5 demonstrated), #1354 6088846292 (repair3)"
  },
  "related": ["SN-0531", "SN-0603", "SN-0807"]
}
```
