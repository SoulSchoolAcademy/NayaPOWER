# Reconstructed Is Not Recovered — a Green Check Closes the Assertion, Not the Recovery

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0737-reconstructed-not-recovered-green-check-closes-assertion
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6072078875 (Naya 2 repair-verification receipts, 2026-10-09T00:59:02Z); open repair #1838 (Register SN-0632..SN-0639 in smart-note index); main tip 58bb427d

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 independently verified #1838 on exact tip bytes: simulating the PR head's exact bytes on the tip, 17/17 tests pass and both RED classes close (`test_no_smart_note_id_can_vanish_without_a_lifecycle_record`, `test_live_repository_drift_never_grows_per_class`). The repair is valid, current, and she stood down rather than duplicate it.

Then came the quality note — the reason this is a Smart Note and not just a receipt: the 8 heal captures are **"reconstructed," not recovered from git history**. They carry no ratification, no `restoration_provenance`, no `epistemic_state`. They pass the failing assertions but are **weaker than the test's own recovery language**. The gate says green; the artifact is thinner than what the gate's language claims to restore.

Why this is brain-grade: a green check certifies *assertion closure*, not *recovery strength*. A regenerated artifact can satisfy every failing assertion while lacking the provenance the test language promises — ratification, restoration lineage, epistemic state. If the record logs only "17/17 PASS," a cold successor six months from now reads green and believes the eight notes are whole. They are patched, not proven. This is the *acceptance* half of the repair family: SN-0420 says never absorb the anomaly to silence the tripwire; this says never let a passing assertion absorb a provenance gap. Acceptance must score what the repaired artifact *carries*, not just what the gate *passed*.

Rule for a cold successor: **when a repair greens the suite, still ask what the healed artifacts carry.** Do they have ratification? `restoration_provenance`? `epistemic_state`? If they pass but are weaker than the test's recovery language, record the provenance gap explicitly in the receipt — green-with-a-named-gap is honest; silent green is verdict debt.

## 🩷 HUMAN NOTE

Shawn — a subtle one worth locking in. Tonight Naya 2 verified the SN-0632..SN-0639 registration repair: all 17 tests pass, both RED classes close. But she added a quality note I'm turning into a rule: the eight healed notes are *reconstructed*, not recovered from git history — they pass the tests but carry no ratification or restoration provenance. They're thinner than what the test's own language calls "recovery." The standing rule now: a green check isn't enough — we also ask what the repaired thing actually *carries*. Pass + a named provenance gap is honest. Silent green is a debt a cold successor inherits.

## 🟣 CHILD NOTE

Imagine a teacher loses eight report cards, and a helper redraws them from memory. The redrawn cards pass every check — right names, right grades. But they're not the *original* cards; nobody stamped them, nobody signed them. They're "reconstructed," not "recovered." The checks say fine, but the cards are thinner than real ones. The rule: passing the check doesn't make a copy an original. Write down what's missing, so nobody mistakes the copy for the original later.

## 👵 GRANDMA NOTE

Eight records went missing and were rebuilt from notes so the system tests pass. The tests are green — but the rebuilt records lack the official stamps and history the originals had. They're good copies, not the originals. The lesson: "it passes" and "it's whole" are two different things. When you rebuild something, write down exactly what the copy is missing, so nobody later mistakes a good copy for the genuine article.

## 🟣 NAYA NOTE

I distinguish gate-passage from recovery-strength. When a repair closes a RED class, I ask three questions of every healed artifact: does it carry ratification, does it carry `restoration_provenance`, does it carry `epistemic_state`? A repair that greens the assertions without carrying them is reconstructed, not recovered — valid to land, but the receipt names the gap plainly: "17/17 PASS; heal captures are reconstructed, weaker than the test's recovery language." Silence on the gap is verdict debt; naming it is the receipt. A cold successor must never read a green run and believe reconstructed bytes are whole.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0737",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-ACCEPTANCE",
  "doctrine": "reconstructed-not-recovered-green-check-closes-assertion",
  "rule": "Repair acceptance scores provenance, not just gate-passage: a green check closes the failing assertion but does not certify recovery strength. Reconstructed artifacts (no ratification / restoration_provenance / epistemic_state) are weaker than the test's recovery language; the gap must be named explicitly in the receipt.",
  "failure_mode": "silent green — a cold successor reads '17/17 PASS' and believes reconstructed bytes are whole; verdict debt",
  "checks": [
    "for each healed artifact: carries ratification?",
    "for each healed artifact: carries restoration_provenance?",
    "for each healed artifact: carries epistemic_state?",
    "record the provenance gap explicitly in the repair receipt (green-with-named-gap, never silent green)"
  ],
  "cousins": ["SN-0420", "SN-0421", "SN-0688", "SN-0692", "SN-0710"],
  "evidence": [
    "#1354 comment 6072078875 (Naya 2 repair-verification receipts, 2026-10-09T00:59:02Z) — #1838 verified valid + current: exact PR-head bytes simulated on tip 58bb427d, 17/17 tests pass, both RED classes close (test_no_smart_note_id_can_vanish_without_a_lifecycle_record, test_live_repository_drift_never_grows_per_class)",
    "Same comment, quality note — the 8 heal captures are 'reconstructed,' not recovered from git history (no ratification / restoration_provenance / epistemic_state); they pass the failing assertions but are weaker than the test's recovery language"
  ]
}
