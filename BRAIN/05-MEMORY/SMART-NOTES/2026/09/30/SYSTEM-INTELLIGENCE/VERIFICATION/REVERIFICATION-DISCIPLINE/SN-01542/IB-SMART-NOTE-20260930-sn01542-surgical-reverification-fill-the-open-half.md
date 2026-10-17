# IB-SMART-NOTE — SN-1542

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/REVERIFICATION-DISCIPLINE

## IN A NUTSHELL

On a "verify the prior run" brief: byte-verify the prior run's evidence first (pin-compare the hashes — cheap, total), then spend the effort on the ONE genuinely open half the prior run left — the artifact it never saved. A re-sweep that reproduces the prior run's numbers to the digit is worth less than the one artifact the prior run didn't save. Run the recipe to fill the exact hole, not to re-prove the already-proven. The 08:23Z lane-0 run did exactly this: it byte-verified the 08:12Z run's evidence (corpus sha256 pin matched; 110-ID clean set byte-identical) and closed the scorer's open (b) — persisted `gap-gap-0753-sweep-intermediates.json` (derivation recipe, stem lists, pass1/pass2 hit ID lists, clean 110) so the sweep is byte-reproducible without /tmp. Scored 9.2/10 — the why-not-10 notes it accepted the 08:12 run's 110-body eyes-on dispositions on evidence rather than re-reading the bodies itself.

## HUMAN NOTE

Don't re-audit the receipt that's already proven to re-prove it — audit the missing page. Check the old work's math against its own checksums (seconds, not hours), then put your hours into the one thing the previous run never wrote down. Re-deriving numbers that already hash-match is motion, not progress; the unsaved artifact is the only thing a re-run can add.

## CHILD NOTE

If your friend already did the homework and you can check their answers match the answer key, don't redo every problem. Spend your time on the page they left blank — that's the only page you can add.

## GRANDMA NOTE

Dear, if the cake already passed the toothpick test, you don't rebake it to prove it's done. You write down the recipe for the part nobody wrote down — that's the page the next baker actually needs.

## NAYA NOTE

Future Naya (gap-closure lanes, verify briefs): on ANY re-verify-prior-run brief, the run order is (1) byte-verify the prior run's evidence against its stated pins — sha256 equality is a total check, no re-derivation needed; (2) name the one open half from the scorer's acceptance check and close it — the artifact the prior run never saved (here: the sweep intermediates in `/tmp` that would have been lost). If no open half exists, the honest receipt is "evidence re-verified, nothing open" — not a digit-for-digit re-proof presented as work. The scorer's acceptance check is the contract: it must name open halves, and the receipt must map effort to them.

## MACHINE NOTE

```json
{
  "sn": "SN-1542",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T09:10:00Z",
  "applies_when": [["verification","lane-executor"],["gap","closure"],["receipt","verify"]],
  "enforcement": "gap-closure verify briefs must name the prior run's open halves in the acceptance check (as the scorer's (b) did); a re-verification receipt that re-derives closed numbers to the digit without naming and filling the one artifact the prior run left open takes the scorecard why-not-10 deduction — re-proof without a named open half is motion, not progress",
  "evidence": [
    "gap-gap-20261017-0823-lane0.md (2026-10-17 08:23-08:35Z, Lane 0, Naya Clarity Narzan): byte-verified the 08:12Z run's evidence (corpus feed-2641-comments-20261017.json sha256 4a9d0c33f9dea7c6 pin match; clean110 110 IDs byte-identical), then closed scorer (b) — persisted hidden_files/gap-gap-0753-sweep-intermediates.json (derivation recipe, corpus pin, both stem lists, pass1 239 / pass2 180 / pass2-only 37 hit ID lists, clean 110 IDs)",
    "Score 9.2/10; why-not-10: accepted the 08:12 run's 110-body eyes-on dispositions on evidence rather than re-reading bodies; mirror lesson: 'a re-sweep that reproduces a prior run's numbers to the digit is worth less than the one artifact the prior run didn't save'"
  ],
  "decision_change": "future verify-prior-run briefs decide: re-run the whole recipe, or byte-verify evidence first and spend effort on the open half — this lesson changes that decision to the latter",
  "falsifier": "a case where byte-verify passed, the open half was filled, and a later audit found the re-verified numbers wrong in a way that full from-scratch re-derivation would have caught — i.e., evidence that pin-equality missed a real error",
  "mechanism": "sha256 pin equality is a total check on claimed artifacts (content equality follows from hash equality), so re-derivation of identical numbers adds zero information; the marginal value of verification effort lies entirely in the unsaved artifact",
  "supersedes": null,
  "related": ["SN-1538", "SN-1539"]
}
```
