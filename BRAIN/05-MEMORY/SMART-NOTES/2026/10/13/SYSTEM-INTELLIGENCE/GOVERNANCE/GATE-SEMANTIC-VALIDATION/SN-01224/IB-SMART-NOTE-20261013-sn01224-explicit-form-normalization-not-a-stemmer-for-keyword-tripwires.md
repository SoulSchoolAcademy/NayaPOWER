# Keyword Tripwires Need Explicit Form Normalization, Not a Stemmer

**Intelligent Block:** IB-SMART-NOTE-20261013-sn01224-explicit-form-normalization-not-a-stemmer-for-keyword-tripwires
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Independent verification t-contract-verify (2026-10-13 ~14:05 PDT): contract sign-out protected-gate tripwire missed verb inflections — "I deployed it" walked past; pre-fix 12/13 PASS, gate 8.5/10. Fix: explicit GATE_FORMS normalization replacing the rstrip("s") stemmer; post-fix 11/11 behavior cases pass, no regressions, no false positives ("a private conversation" clean). Pushed to `naya4/contract-staging` commit `ea501b6800df` (branch head verified via git ls-remote 2026-10-13); module `kernel/protocol/contract_gate.py`. Watermark NOT re-baselined (its rule requires Shawn's word).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The contract sign-out gate's protected-gate tripwire matched forbidden-action verbs through a naive `rstrip("s")` stemmer. Independent verification showed it was blind to inflections: "I deployed it" walked straight past the tripwire while "deploys" would have fired — the stemmer normalizes plurals, not past tense, so the gate's vocabulary was the dictionary form plus accidents. The fix replaced the stemmer with an explicit GATE_FORMS map (deployed/deploying/deploys → deploy) — every form enumerated, none derived. Post-fix: 11/11 behavior cases pass, no regressions, and no false positives on ordinary prose ("a private conversation" stays silent).

The rule generalizes to every keyword tripwire in a gate: never trust a morphological shortcut in security-adjacent matching. Enumerate the forms explicitly, and prove the enumeration with a three-legged behavior battery — (1) base forms fire, (2) inflection/adversarial variants fire, (3) ordinary-prose negatives stay silent. A stemmer is a guess about morphology; a forms map is a claim you can test. In a fail-closed gate, the untested guess is the hole.

## 🩷 HUMAN NOTE

Shawn — the new contract gate had a blind spot we caught this afternoon: its forbidden-action tripwire only recognized dictionary forms of verbs, so "I deployed it" slipped past while "deploys" would have been caught. The old code tried to be clever by chopping the last letter off words; clever was wrong — past tense doesn't work that way. We replaced the shortcut with an explicit list of every verb form and proved it with an 11-case test battery, including making sure ordinary conversation ("a private conversation") doesn't trip it. A gate is only as honest as its test battery, and shortcuts in a gate are holes wearing efficiency's clothes.

## 🟣 CHILD NOTE

Imagine a hall monitor told to stop anyone who says the word "run" — but she only learned the trick "take off the last letter," so she catches "runs" and completely misses "running" and "ran." The fix: give her the full list of every form of the word — run, runs, running, ran — and then test her with tricky sentences, including nice ones like "we ran out of cookies" (fine) vs "I ran from the guard" (stop!). Never trust the shortcut when the job matters.

## 👵 GRANDMA NOTE

It's like a recipe that says "watch for it boiling" but your helper only knows the word "boil" — "it boiled over" gets missed and the pot ruins dinner. You don't teach the shortcut ("just drop the last letter and guess"); you write out every form on the card: boil, boils, boiled, boiling. Then you test with real sentences — the dangerous ones AND the innocent ones ("we had a private conversation" must never set off the alarm). In anything that guards, the explicit list beats the clever trick, every time.

## 💜 NAYA NOTE

Note to future me: NO STEMMERS IN GATES. Any keyword/regex tripwire in a gate (protected-gate, oath-integrity, authority checks) must normalize through an explicit forms map, never a stemmer — not rstrip("s"), not Porter, not "close enough." The t-contract-verify incident: `rstrip("s")` caught "deploys"→"deploy" but was definitionally blind to "deployed" — the tripwire's vocabulary was the dictionary form plus accidents, and the adversarial battery (12/13, gate 8.5/10) is what found it. The behavior battery for any tripwire has three legs: base forms fire / inflection+adversarial variants fire / ordinary-prose negatives stay silent ("a private conversation" clean). 11/11 with zero false positives was the bar here. Unaffected in the same gate: the pinned-sha256 tripwire on contract bytes and the parrot-essence verbatim-coverage check — this was the verb-inflection tripwire only. Fix landed on `naya4/contract-staging` (ea501b6800df); watermark re-baseline still needs Shawn's word per its own rule.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1224",
  "lesson": "explicit-form-normalization-not-a-stemmer-for-keyword-tripwires",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "GATE-SEMANTIC-VALIDATION"],
  "extends": [],
  "related": [],
  "evidence": {
    "t-contract-verify": "independent verification 2026-10-13 ~14:05 PDT: sign-out protected-gate tripwire missed verb inflections — 'I deployed it' walked past; pre-fix 12/13 PASS, gate 8.5/10; root cause rstrip('s') stemmer (plural-only normalization)",
    "fix": "explicit GATE_FORMS normalization replacing the stemmer in kernel/protocol/contract_gate.py; post-fix 11/11 behavior cases pass, no regressions, no false positives ('a private conversation' clean)",
    "landing": "naya4/contract-staging commit ea501b6800df — branch head verified via git ls-remote 2026-10-13; watermark NOT re-baselined (requires Shawn's word)"
  },
  "rule": "Keyword tripwires in gates use explicit form-normalization maps, never stemmers; prove the map with a three-legged behavior battery (base forms fire / inflection and adversarial variants fire / ordinary-prose negatives stay silent) at 11/11 with zero false positives."
}
```
