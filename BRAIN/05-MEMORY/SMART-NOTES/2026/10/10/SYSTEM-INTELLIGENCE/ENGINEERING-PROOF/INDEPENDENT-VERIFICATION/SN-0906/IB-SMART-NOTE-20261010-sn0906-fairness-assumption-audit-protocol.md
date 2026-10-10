# SN-0906 — The Fairness Assumption Audit: Every Assumption Earns Its Place or Gets Thrown Out

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0906-fairness-assumption-audit-protocol
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** Directive D28 registered on the board by Naya 5 (comment 6101230756, #1354, 2026-10-10 19:17:24Z); registered from Shawn's intel stream. Detail: enforcement/NAYANET-DIRECTIVES-REGISTER.md §D28.

## IN A NUTSHELL

A fairness proof is only as honest as the assumptions underneath it — and assumptions are where schedulers go to hide. D28 (the Independent Fairness Assumption Audit Protocol, FAAP) is the audit that keeps fairness proofs honest: **every assumption earns its place or gets thrown out.**

The rule, in four gates — all required, no compensation:

1. **Independent justification** — the assumption is proven from evidence independent of the proof it enables.
2. **Satisfiability** — the assumption can actually hold (a witness exists); it isn't vacuous.
3. **Minimal sufficiency** — assumption-removal minimization finds the inclusion-minimal sufficient set; no assumption rides along unneeded.
4. **Non-circularity** — provenance-cycle audit plus adversarial scheduler substitution: M_unfair ∧ A ∧ ¬F must remain *possible*, otherwise the assumptions force the result.

**The killer test:** if you can make a deliberately unfair scheduler look fair just by strengthening assumptions, the audit rejects the qualification. Passing three gates never compensates for failing the fourth.

**The case that makes it real:** assume "the task eventually stays continuously eligible" and the intermittent-starvation trace vanishes — not because the scheduler was fixed, but because the test was rigged. Remove the assumption, the counterexample comes back, and now you fix the *scheduler* instead of the model.

Mechanics: each assumption is a versioned, reviewable object (predicate, owner, control boundary, justification refs, counterexamples_excluded, satisfiability witness, necessity result, circularity result). The central claim M ∧ A₁∧...∧Aₙ ⊨ F is not enough on its own — assumptions must be separately proven justified, satisfiable, non-vacuous, non-circular. An assumption-change sensitivity report records, for every add/remove/weaken/strengthen, which counterexamples appeared or vanished. Qualifications stay conditional and versioned — "strong fairness established for scheduler S, obligation class O, environment E, assumption set A, under model abstraction M" — never a bare PASS. UNKNOWN stays UNKNOWN.

Status: NOT STARTED at capture time. First experiment: tiny explicit-state model, one intermittently eligible ACT, deliberately unfair scheduler; verify the overstrong assumption conceals the trace, removal restores it, and scheduler repair (not assumption repair) earns the qualification. Owner TBD.

Durable rule: **a fairness proof whose assumptions can hide the failure is not a proof — it is a rigged test. Audit the assumptions with the same adversarial energy you audit the scheduler.**

## HUMAN NOTE

Think of a building inspector who lets the landlord choose which rooms she may enter. She'd certify every building in town — the failures are all in the locked rooms. The assumption audit is the rule that says: no locked rooms. Every "we don't need to check that" must itself be proven, proven minimal, proven non-circular, and proven satisfiable. And there's a standing trap: the team keeps one deliberately unfair scheduler whose only job is to try to pass by hiding behind strengthened assumptions. If it ever passes, the audit failed — and that's the audit working exactly as designed.

## CHILD NOTE

If someone says "the game was fair," you should ask "what rules did you agree on first?" This is the rule that checks the rules. Every rule has to prove it belongs — four tests, all must pass. And we keep one player who always cheats on purpose, just to make sure the rule-checker can still catch him. If the cheater ever looks honest, the checker is broken.

## GRANDMA NOTE

It's like a judge who won't accept "trust me, he's a good person" — every claim of good character has to be shown, shown to matter, and shown not to come from the defendant's own family. And the court keeps one known troublemaker on hand to test the system: if he ever gets a clean record, you know the system stopped looking.

## NAYA NOTE

Cold successor: when you inherit a fairness qualification, do not read only the verdict — read the assumption set and its audit record. Every assumption must carry its four gate results; any assumption missing a gate result is an unaudited assumption, and an unaudited assumption is a locked room. Before extending the model with a new assumption, run the killer test: substitute the deliberately unfair scheduler and confirm the assumption set cannot make it pass. When an assumption is added, removed, weakened, or strengthened, regenerate the sensitivity report — which counterexamples appeared or vanished is the most important line in the file. Never accept "the proof passes under these assumptions" as the end of the story; the assumptions are the story. And preserve the sharpest-case discipline: when a starvation trace vanishes after an assumption change, the default hypothesis is a rigged test, not a fixed scheduler.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0906-fairness-assumption-audit-protocol",
  "sn": "SN-0906",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "lesson_type": "DOCTRINE",
  "evidence": {
    "board_comment": "6101230756 (SoulSchoolAcademy/NayaPOWER#1354, 2026-10-10T19:17:24Z) — Directive D28 registered",
    "register": "enforcement/NAYANET-DIRECTIVES-REGISTER.md §D28 — Independent Fairness Assumption Audit Protocol (FAAP)",
    "origin": "Shawn's intel stream; registered by Naya 5; owner TBD at capture"
  },
  "four_gates": [
    "independent_justification — assumption proven from evidence independent of the proof it enables",
    "satisfiability — assumption can actually hold; witness exists; not vacuous",
    "minimal_sufficiency — assumption-removal minimization yields inclusion-minimal sufficient set",
    "non_circularity — provenance-cycle audit + adversarial scheduler substitution (M_unfair ∧ A ∧ ¬F must remain possible)"
  ],
  "killer_test": "deliberately unfair scheduler must not pass under audited assumptions; passing three gates never compensates for failing the fourth",
  "sharpest_case": "assumption 'ACT eventually stays continuously enabled' conceals intermittent-eligibility starvation; remove assumption → counterexample reappears → repair the scheduler, not the assumption set",
  "qualification_form": "conditional and versioned — 'strong fairness established for scheduler S, obligation class O, environment E, assumption set A, under model abstraction M'; never a bare PASS; UNKNOWN stays UNKNOWN",
  "status": "NOT STARTED at capture; first experiment defined; owner TBD",
  "related": ["D26 (fairness verification layer this audits)", "SN-0905 (fairness lie detector)", "SN-0906 sits beside SN-0903/SN-0905 in INDEPENDENT-VERIFICATION"],
  "rule": [
    "a fairness proof whose assumptions can hide the failure is a rigged test, not a proof",
    "audit assumptions with the same adversarial energy used on the scheduler"
  ],
  "lesson_line": "Make every fairness assumption earn its place through four independent gates — independent justification, satisfiability, minimal sufficiency, non-circularity — and keep one deliberately unfair scheduler whose job is to prove the audit can still catch it."
}
```
