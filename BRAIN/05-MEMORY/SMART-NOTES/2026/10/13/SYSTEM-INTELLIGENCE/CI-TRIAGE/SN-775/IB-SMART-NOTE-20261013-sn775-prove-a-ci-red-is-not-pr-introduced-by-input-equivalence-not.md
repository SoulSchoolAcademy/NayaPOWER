# Prove a CI Red Is Not PR-Introduced by Input-Equivalence, Not Signature Alone
SN-775 · SYSTEM-INTELLIGENCE / CI-TRIAGE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

When a CI check fails on a PR head, "the same failure exists on the unmodified tip" is corroborating, not conclusive — the PR could still coincidentally share a cause. The rigorous proof is **input-equivalence**: enumerate the check's actual inputs, then show the PR's diff does not intersect them. Naya 4's #1956 verification did exactly this: `spec-integrity` FAILED, but the check reads only manifest + projections + machine.json — artifacts the PR does not touch — so the failure is provably not PR-introduced. Classification: BASE-DEFECT, inherited. Result: zero PR-introduced reds.

Why this is brain-grade: SN-0240 mandates classifying every CI red as PR-introduced vs base-inherited before healing — this is the proof method that makes the classification rigorous instead of vibes. A cold successor can run it mechanically: `diff ∩ check-inputs = ∅ → not yours`. It also protects the inverse error: if the diff DOES intersect the check's inputs, the red is PR-suspect until proven otherwise — no hiding behind "it failed on the tip too." Read the check's inputs first; signature comparison second.

Rule for a cold successor: **to prove a CI failure is not PR-introduced, prove input-equivalence — enumerate the check's actual inputs and show the PR's diff touches none of them. Signature match on the tip corroborates; input-set non-intersection proves.**

## HUMAN

Shawn — a verification-technique lesson from this morning's PR #1956 check. Two CI jobs failed on the PR head. For one, Naya 4 didn't just note "it also fails on the unmodified tip" — she proved it a stronger way: the failing check reads only three specific artifacts (manifest, projections, machine.json), and this PR touches none of them. A check can't be broken by files it never reads. So the failure is provably inherited from the tip, not introduced by the PR — "zero PR-introduced reds." Standing rule: matching failure signatures are a clue; proving the PR's changes don't intersect the check's inputs is the verdict.

## CHILD

Imagine the school lunch line's cash register breaks — and someone says "it was already broken yesterday, so it's not your fault." That's a clue, but not proof — maybe you bumped it too. The real proof: the register only reads lunch cards, and you never touched the lunch cards. You didn't touch anything it uses, so you couldn't have broken it. To clear yourself, don't just say "it was broken before" — show that what broke only uses things you never touched.

## GRANDMA

A quality check failed on a team's new work. Instead of just saying "it was failing before their change," the verifier went further: the failing check only examines three specific documents, and the team's change touched none of them — a check can't be broken by documents it never looks at. That's how you prove a failure is inherited, not caused by the new work. The lesson: "it was already broken" is a clue; "it doesn't even look at what we changed" is the proof.

## NAYA

Make this mechanical in CI triage: (1) for every failing check, read the check's definition and enumerate its actual inputs (files, configs, artifacts it reads); (2) compute the intersection with the PR's diff; (3) intersection empty → classify BASE-DEFECT inherited with the input list as evidence; intersection non-empty → treat as PR-suspect, investigate, never dismiss on signature alone. Record the input list in the classification receipt so a cold successor can re-verify the non-intersection without re-reading the check.

## MACHINE

{
  "schema": "smart-note-v1",
  "sn": "SN-0775",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/RED-CLASSIFICATION",
  "doctrine": "input-equivalence-red-classification",
  "rule": "To prove a CI failure is not PR-introduced, prove input-equivalence: enumerate the check's actual inputs and show the PR's diff touches none of them. Signature match on the tip corroborates; input-set non-intersection proves.",
  "failure_mode": "classifying a red as base-inherited on signature match alone while the PR's diff actually intersects the check's inputs; or absorbing a PR-introduced red as tip drift",
  "checks": [
    "failing check's actual input set is enumerated from the check definition, not assumed",
    "PR diff ∩ check inputs is computed and recorded in the classification receipt",
    "empty intersection → BASE-DEFECT inherited; non-empty → PR-suspect, investigated, never dismissed",
    "relates to SN-0240 (classify before healing): this is its proof method"
  ],
  "provenance": {
    "board": "#1354",
    "comment_id": 6079691883,
    "author": "SoulSchoolAcademy",
    "seat": "Naya 4",
    "pr": 1956,
    "timestamp": "2026-10-09T11:09Z"
  }
}

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0775-migrated.*
