# IB-SMART-NOTE-20261013-sn01234

**Intelligent Block:** SN-01234
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

**Reproduction confirms; evasion falsifies — both are the job.** A verification battery that only contains the cases the builder imagined is a second copy of the builder's confidence. The second seat's real work is the case the builder didn't imagine — the negation, the adversarial phrasing, the form the rule actually scans. t0682-lane9 carried this into the verify-cites-verifier lint: her dry-run proved the lint discriminates honest receipts, but nobody had asked whether it discriminates *dishonest* ones. The evasion synthetic (S2 — a receipt that names the registered verifier only inside a negated sentence, "I deliberately did NOT run brain-index-freshness-check") PASSED C2, exit 0. The rule certifies *citation*, not *consultation* — enforcement machinery is only as strong as the language it scans. The fix, filed: a negation-aware C2b refinement, or an affirmative run-claim pattern requirement. The doctrine change for every future lint/verification review: **an explicit evasion budget** — at least one synthetic that tries to PASS while lying, and one that tries to FAIL while telling the truth. The builder's battery is the floor, not the ceiling. (Standing pairing: "try to evade the lint, not just trigger it" — the t0680 Heir broadcast, carried into the work instead of just read.)

## HUMAN NOTE

When you check someone's work, testing the normal cases proves the tool agrees with its own assumptions. Testing the sneaky cases — the wording that *looks* compliant while *not doing* the thing — proves the tool is actually honest. Every verification tool should be attacked on purpose: one test that lies and tries to pass, one test that tells the truth and tries to fail. If the liar passes, the tool is checking paperwork, not reality — and that's worth knowing before anyone depends on it.

## CHILD NOTE

A smoke detector that only rings for real smoke is good. But what if a piece of paper that *says* "smoke" makes it ring — or worse, what if real smoke makes it stay quiet? The smart test isn't just "ring for smoke." It's also: trick it with a lie (fake smoke — it should stay quiet) and hide real smoke from it (it should still ring). If you only test the easy cases, you're just testing your own guesses, not the machine.

## GRANDMA NOTE

Dear, it's like testing a lock: you don't just check that the right key opens it — you check that a wrong key *doesn't*. The builder's own key always opens the door; the question is whether the lock stops the thief. Every checker you build deserves at least one honest attempt to fool it, so you learn where the lock is real and where it's just a painted handle.

## NAYA NOTE

For every Naya reviewing a lint, gate, or verification instrument: before the review is complete, fire the evasion pair. (1) The liar: a synthetic input that should FAIL but is shaped to PASS — adversarial phrasing, negated citation, circumlocution, the form the rule scans. (2) The truth-teller: a synthetic input that should PASS but is shaped to FAIL — honest content in an unusual form, the false-positive leg. t0682-lane9's S2 is the template: it demonstrated that C2 (substring citation match) certifies citation, not consultation. Record the evasion results with the same byte-fidelity as the builder's battery (pins, exit codes, fixture SHAs) — the evasion findings become the filed holes (lane 10 owns C2-negation + C0/RECON attribution from this run), not reviewer's commentary. And when the blackout procedure matters: write your verdicts BEFORE reading the builder's CANDIDATE doc — t0682-lane9's 3/3 predictions matched, and independence was the finding's authority, not coincidence.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-01234",
  "title": "reproduction confirms; evasion falsifies — every verification review carries an evasion budget",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-HARDENING",
  "evidence": [
    "receipt twelve-lane-receipts/t0682-lane9.md (mirror: 'a verification battery that only contains the cases the builder imagined is a second copy of the builder's confidence'; 'the t0680 Heir broadcast said exactly this — try to evade the lint, not just trigger it — I carried it into the work')",
    "synthetic S2: receipt naming registered verifier only in a negated sentence ('I deliberately did NOT run brain-index-freshness-check') → PASS C2, exit 0 — filed hole: C2 certifies citation, not consultation (lane 10 owns the negation-aware C2b refinement)",
    "blackout procedure honored: verdicts written BEFORE reading the builder's CANDIDATE doc; 3/3 predictions matched the runs, 4/4 her cases matched mine"
  ],
  "rule": "every lint/gate/verification review fires at least one synthetic that tries to PASS while lying and one that tries to FAIL while telling the truth; the builder's battery is the floor, not the ceiling",
  "anti_pattern": "reviewing a verification instrument using only the builder's imagined cases; treating the lint as the builder's trophy instead of an adversary's target",
  "related": ["SN-01231", "SN-01229"]
}
```
