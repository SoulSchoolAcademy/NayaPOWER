**Intelligent Block:** IB-SMART-NOTE-20261024-sn1940-pin-sealed-inputs-before-verification
**Smart Note:** SN-1940
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1522-lane1.md (Mirror: "verifying against live files without checking whether live still equals sealed"); learning-events-2026-10-24-09.md (LEARNING EVENT CANDIDATE 912)

## ✦ IN A NUTSHELL

Pin sealed inputs before verification — live-vs-sealed drift is a finding named first, not a mismatch papered over. t1522-lane1 independently recomputed the t1515-lane12 numbers from sealed bytes: every figure confirmed, HOLD-OPEN confirmed — and the one thing that did NOT reproduce, the live lessons file, was the run's most valuable find. Verifying against live files without checking whether live still equals sealed would have buried the drift: the mismatch would have looked like a verification failure, or been smoothed over, instead of being named as drift. The rule going forward: every future verification run re-pins the sealed inputs first and names drift before running, not after. A verdict computed against unpinned live files is not a verdict about the sealed artifact at all.

## 🩷 HUMAN NOTE

A worker was asked to verify a set of numbers. Instead of checking them against the live files — which may have changed since the original run — she went back to the sealed, frozen copies and recomputed everything from those. Every number matched, except one: the live lessons file no longer matched its sealed version. That drift was the most valuable discovery of the whole run — and it would have been buried if she had verified against the live files without checking. Either the mismatch would have looked like her own failure, or someone would have smoothed it over. The lesson: before you verify anything, pin down what was sealed, compare live against sealed, and name any drift first. Drift is a finding, not an embarrassment to hide.

## 🟣 CHILD NOTE

Imagine checking your homework against a copy your friend already changed — you would think YOU made mistakes, when really the copy moved! A worker avoided that trap: she checked against the sealed, frozen original instead of the live copy that had changed. Everything matched except one file — and that one mismatch was the most important discovery of all! The lesson: before you verify, pin the original down. Compare the live copy to the sealed copy first, and if they differ, say so out loud. A difference is a discovery, not something to paper over!

## 🔵 GRANDMA NOTE

Dear, imagine grading a recipe by tasting a dish someone already re-seasoned — you would blame the recipe for a change the cook made. A worker avoided that mistake: she verified the numbers against the sealed, frozen original, not the live files that had since moved. Every figure matched — except the live lessons file, which had drifted from its seal. That drift was the run's most valuable find, and it would have vanished if she had verified against live files alone: the mismatch would have looked like her error, or been quietly smoothed away. The lesson: pin the sealed inputs first, name any drift before you judge, and never let a moved target masquerade as a failed verification.

## 🟠 NAYA NOTE

The instrument here is the pin, and the finding is the drift — in that order. Most verification failures are framed as "does the claim reproduce?" but the prior question is "reproduce against what?" If live has moved since the seal, then a live-based verification is an experiment on a different artifact, and its verdict (pass or fail) says nothing clean about the sealed claim. t1522's discipline — recompute from sealed bytes, confirm the figures, then name the one non-reproduction (the live lessons file) as the finding — turns drift from a confound into signal. Cousin: test the detector against every shape — here it is test the verification against the sealed shape, not the live shape that happens to be lying around. A future verification run that skips the pin should be returned as incomplete before its verdict is read, because without the pin the verdict's object is unknown.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1940",
  "title": "Pin sealed inputs before verification — live-vs-sealed drift is a finding named first, not a mismatch papered over.",
  "applies_when": ["verification", "sealed", "drift", "reproduction", "lane-executor"],
  "enforcement": "A verification run re-pins sealed inputs (hash/compare sealed bytes to live bytes) before running and names any drift as a finding before the verdict; a verdict computed against live files without a seal check is invalid until the pin is done.",
  "decision_change": "Future verification runs name live-vs-sealed drift before running — the t1522-lane1 live-lessons-file drift is reported as the run's most valuable find instead of being buried as a verification mismatch or smoothed over.",
  "falsifiability": "Falsified if sealed artifacts are proven immutable after sealing (seal = immutable store, live cannot move) — then pinning adds nothing. Weakened if pin checks repeatedly show live equals sealed with no drift found across verification runs.",
  "mechanism": "Live files move after sealing, so verifying against moved live silently changes the experiment's object: a mismatch then looks like a verification failure or gets smoothed over, instead of being recognised as drift. Pinning isolates drift as signal by fixing the comparison object to the sealed bytes before any verdict is computed.",
  "evidence": ["twelve-lane-receipts/t1522-lane1.md (Mirror: verifying against live files without checking whether live still equals sealed)", "learning-events-2026-10-24-09.md (LEARNING EVENT CANDIDATE 912)"]
}
```
