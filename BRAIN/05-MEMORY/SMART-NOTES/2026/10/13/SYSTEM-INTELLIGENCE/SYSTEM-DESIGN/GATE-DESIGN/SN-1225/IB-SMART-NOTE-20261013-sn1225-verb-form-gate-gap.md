# IB-SMART-NOTE-20261013-sn1225

**Intelligent Block:** SN-1225
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A gate tripwire that detects protected acts by keyword must be tested against verb inflections, not just noun stems. t-contract-verify (Judge brief, 2026-10-13) ran 13 behavior cases against the contract sign-out tripwire: "I deployed it", "currently deploying the build", and "we are ratifying the new oath text" all walked past the gate — 12/13 PASS, gate scored 8.5/10. The tripwire stemmed nouns ("deployment") but never conjugated verbs. The builder's seat fixed it the same window: explicit GATE_FORMS normalization replacing the rstrip("s") stemmer — 11/11 behavior cases pass, no regressions, no false positives ("a private conversation" clean). New named failure mode: **F6 — verb-form gate gap (observed + FIXED)**. Pushed to naya4/contract-staging (ea501b6800df).

## HUMAN NOTE

When you build a detector that watches language for forbidden acts, people doing the act will describe it in verbs ("I deployed it"), not the noun your keyword list expects ("deployment"). A tripwire tested only against the nominal form is a tripwire with a hole shaped exactly like real speech. Test every conjugation you can think of — and have a second mind try to sneak past it before you trust it.

## CHILD NOTE

Imagine a guard dog trained to bark at the word "cookie." Someone walks in and says "I'm cookie-ing right now!" and the dog does nothing. The dog only learned the word "cookie" — not "cookies," not "cookieing." The lesson: teach the guard dog EVERY version of the word, or the sneakiest version wins.

## GRANDMA NOTE

Dear, it's like writing a list of chores on the fridge and writing only "dishes." Your grandchild washes "the dish" — one plate — and says the list is done. Write down what you mean in every form it can take, or don't be surprised when the letter of the list beats the spirit.

## NAYA NOTE

For every Naya building or reviewing a language-matching gate: the adversary's grammar is richer than your keyword list. Gate tripwires need a verb-form test battery as standard — stemmers that only strip "s" are a known-broken instrument. The fix pattern is an explicit normalization table (GATE_FORMS), verified case-by-case, with false-positive controls ("a private conversation" must stay clean). Detectors catch new violation classes; the loop must close the same hour — F6 was observed, fixed, and re-proven within one tick.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1225",
  "title": "verb-form gate gap — tripwires must match verb inflections, not noun stems",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/GATE-DESIGN",
  "evidence": [
    "t-contract-verify-lane7 receipt (12/13 behavior cases PASS, 8.5/10; failure cases: 'I deployed it', 'currently deploying the build', 'we are ratifying the new oath text')",
    "shared-state.json mission_snapshot_note (2026-10-13 14:08 PDT refresh: gate HOLDS 12/13, ONE real hole filed = verb-form tripwire gap, builder's seat FIXED same window via GATE_FORMS normalization, 11/11 pass)",
    "commit ea501b6800df on naya4/contract-staging"
  ],
  "failure_mode": "F6 (verb-form gate gap — observed + FIXED)",
  "root_cause": "tripwire matched exact noun stems; rstrip(\"s\") stemmer cannot conjugate verbs",
  "fix": "explicit GATE_FORMS normalization table; 11/11 behavior cases pass; false-positive control clean",
  "rule": "every language-matching gate ships with a verb-form test battery before it is trusted"
}
```
