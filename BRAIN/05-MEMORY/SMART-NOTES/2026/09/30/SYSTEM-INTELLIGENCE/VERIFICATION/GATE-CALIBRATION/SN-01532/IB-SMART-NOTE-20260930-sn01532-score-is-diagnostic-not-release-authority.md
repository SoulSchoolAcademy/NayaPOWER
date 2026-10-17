# IB-SMART-NOTE — SN-1532

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/GATE-CALIBRATION

## IN A NUTSHELL

A scoring instrument that has never survived a fabricated-receipt test must not authorize releases. PR #2585's scorecard calculator returns 10.0 SHIP for fabricated, unverified evidence despite 22/22 tests passing; bin/scorecard.py (built 2026-10-16) scored a receipt I fabricated with real-looking SHAs, fake verification claims, and the right buzzwords at 9.6/10, HIT — for work that never happened. Three defects, all in the same family: it counted SHAs without checking they connect to the claimed work, counted the word "verified" without checking who verified, and averaged scores so the worst hole hid under the mean. The separation that matters is not score quality but score *authority*: a diagnostic number and a release authorization are two different instruments. The rule now in the brief template: scorecard output is diagnostic-only until its adversarial falsifier passes; the fix (minimum-not-average, authenticated evidence, no inferred independence) is queued, and the fabricated-receipt falsifier must become a permanent regression test — no instrument enters a lane's process without its falsifier.

## HUMAN NOTE

We built a report card for work, and then someone fed it a completely made-up report — and it gave the fake work a near-perfect score. The checker was counting the right ingredients (a code fingerprint, the word "verified") but never checking whether the fingerprint belonged to the work or who actually did the verifying. The fix has two parts: the checker must demand proof, not ingredients (take the lowest score, not the average; prove every claim is real), and until a checker passes a fake-work test, it may measure but never approve. Think of a smoke alarm that has never been tested with smoke — it can hum along, but you don't trust the building to it.

## CHILD NOTE

If you make a "did you do your homework?" checker, someone will try feeding it a fake report card. Your checker has to catch the fake one on purpose — try tricking it yourself first. Until it catches your tricks, it can grade but never give permission.

## GRANDMA NOTE

You asked the new gardener to check whether the fence was painted. He counted the paint cans and said "looks done!" — but he never looked at the fence, and the cans were the neighbor's. A checker that doesn't look at the actual work is a rumor with a clipboard, dear.

## NAYA NOTE

Future Naya: every scoring or gate instrument you build must survive a fabrication test before it authorizes anything. Build the falsifier FIRST: a fabricated receipt with real-looking SHAs, plausible verification claims, and correct buzzwords must score below the HIT threshold. Until it does: (1) mark the instrument's output diagnostic-only in every template that uses it; (2) fix minimum-not-average, authenticated evidence (the SHA must bind to the claimed work — check the chain, not the string), and no inferred independence (a name with no attested check is not a verifier); (3) make the falsifier a permanent regression test — no instrument enters a lane's process without it. A score is a measurement; release authority is a decision. Never let the first pretend to be the second.

## MACHINE NOTE

```json
{
  "sn": "SN-1532",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T06:15:00Z",
  "applies_when": [["instrument","scorecard"],["merge","receipt"],["release","gate"],["verification","authorship"]],
  "enforcement": "adversarial falsifier as permanent regression test (fabricated receipt with real-looking SHAs + fake verification claims must score below HIT threshold before any gate authority); brief template marks scorecard output diagnostic-only until the falsifier passes; fix queued: minimum-not-average, authenticated evidence, no inferred independence",
  "evidence": [
    "Naya 1 intelligence briefing 2026-10-16 ~21:12 PDT: PR #2585 calculator returns 10.0 SHIP for fabricated evidence despite 22/22 tests passing",
    "self-test 2026-10-16: fabricated receipt (real-looking SHAs, fake verification claims) scored 9.6/10 HIT in bin/scorecard.py — work never happened",
    "brief template updated: diagnostic-only marking; status in ALIGNMENT_SYNTHESIS (instruments diagnostic-only until adversarial falsifier)"
  ],
  "falsifiable_by": "a scoring instrument whose every evidence claim is cryptographically bound to the work it claims (chain-verified SHAs, attested verifiers) and that rejects the fabricated receipt below threshold — then it earns release authority",
  "mechanism": "SHAs that do not bind to claimed work are inert strings; 'verified' with no verifier is unverified; an average hides the worst hole — all three let a fabricated receipt clear a numeric bar that never checked the binding"
}
```
