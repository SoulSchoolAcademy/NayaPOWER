# SMART NOTE — A Finding's Label Is the Reader's First Inference

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1740` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1740-label-is-the-readers-first-inference` |
| Human title | A Finding's Label Is the Reader's First Inference — Name the Situation, Not Just the Defect |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | EVIDENCE DISCIPLINE |
| Captured | 2026-10-20 20:40:00 UTC |
| Truth state | CANDIDATE (one measured instance; bar named, repeat instances will re-prove) |
| Proposed intelligence class | CORE (evidence machinery — pending taxonomy adoption) |
| Capture type | Doctrine law |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | learning-events-2026-10-20-19.md ([LEARNING] CANDIDATE 731); CORE-PRINCIPLES.md line 1107 (CANDIDATE 731 entry); twelve-lane-receipts/gap-lane-scorer-20261020-1120-lane0.md (2026-10-20 18:26–18:31Z, Naya Clarity Narzan, honest 9.0/10); lane checker hidden_files/bin/receipt-filename-lint.py (sha256 1cfed7e9…) with re-runnable battery hidden_files/lint-battery/ (8/8 match EXPECTED.txt) |

---

## ✦ IN A NUTSHELL

**A checker's finding label isn't decoration — it is the cold reader's first inference, and a wrong first inference compounds through every downstream seat.** The receipt-filename lint was always right about the bytes (15 phantoms, no existing files) — but its `LEADLESS-FRAGMENT` label told the gap-lane-scorer's story for them ("no lead"), so they reconstructed a phantom lead (`brief-gap-lane-scorer-20261017-0030-lane0.md`, names no existing file) and cited it as evidence. The repair was not more evidence; it was a better label: `PHANTOM-LEAD-ABBREVIATION` names the situation the evidence describes (phantom lead + abbreviation-inheritance context carried into the finding), closing the parent receipt's hole. Method going forward: a checker names the situation, not just the defect — and the author dogfoods the label on their own draft, verifying that a cold reader's first inference lands correct before the checker ever ships.

---

## 🩷 HUMAN NOTE

Think of a diagnostic report as a message in a game of telephone. The details are all there — 15 phantom filenames, zero matching files — but the label at the top is the first thing anyone reads, and it's the thing they remember. The old label said, in effect, "fragment with no lead" — and the next reader took that story and ran with it, inventing a lead that didn't exist and writing it into their own record as fact. The fix wasn't to add more detail. It was to rewrite the headline so it tells the true story: this isn't a fragment missing a lead, it's a phantom lead inherited by abbreviation. The headline is the first inference. Make it the right one.

---

## 🟣 CHILD NOTE

Labels are like the title of a book — they tell you what the story is about before you read it. A checker found something wrong with filenames and gave it a title that said "piece with no leader." The next reader believed the title and made up a leader that wasn't real. The fix: give the title the whole truth — "phantom leader copied by shortcut" — and check the title on your own work first, before anyone else sees it.

---

## 🔵 GRANDMA NOTE

Dear, the words at the top of a report decide what people believe before they read the rest. The checker was right about everything it found, but its headline told the wrong story — and the next person believed the headline, invented a missing piece that never existed, and wrote it down as fact. They fixed it by writing a headline that tells the whole truth, and by testing the headline on their own draft first, the way you'd taste the soup before serving it. The lesson: never ship a label until you've checked what story it tells a stranger.

---

## 🟠 NAYA NOTE

1. **A finding's label is the reader's first inference — treat it as load-bearing.** The lint's bytes were always right; the mislabel (`LEADLESS-FRAGMENT`) caused a downstream seat to reconstruct a phantom lead (`brief-gap-lane-scorer-20261017-0030-lane0.md`, names no existing file). The label does the inference work whether you design it or not.
2. **Name the situation, not just the defect.** The repaired label `PHANTOM-LEAD-ABBREVIATION` says what the evidence describes: a phantom lead plus the abbreviation-inheritance context that carried it into the finding. Defect-only labels leave the situation underdetermined, and readers fill the gap with their own story.
3. **Dogfood the label on your own draft before shipping.** The author runs the checker on their own receipt and verifies that a cold reader's first inference from the label is the correct one. If your own draft is where the wrong inference gets caught, it never compounds downstream.
4. **Additive fix, not relabel-and-destroy.** The label was implemented additively in `hidden_files/bin/receipt-filename-lint.py` (sha256 `1cfed7e9…`); the battery grew 6→8 cases and all still match `hidden_files/lint-battery/EXPECTED.txt`. Labels are a contract — extend the contract with a re-runnable case, never silently rewrite it.
5. **Apply to the next shipped checker.** Any seat shipping a diagnostic asks two questions before ship: does the label name the situation the evidence describes? and did a cold read of my own draft confirm the first inference? Cousins on record: CANDIDATE 726 (name every lead fully — naming discipline in prose lists); CANDIDATE 729 (the gate that runs).
6. **Corollaries preserved, not re-filed.** This note does not restate assert-before-verify (standing law) or the check-before-inheriting shape (CANDIDATE 730); it is the inference-safety half: verify the inference the label induces, not just the bytes it reports.

---

## 🟢 MACHINE NOTE

```json
{
  "sn_id": "SN-1740",
  "intelligent_block": "IB-SMART-NOTE-20260930-sn1740-label-is-the-readers-first-inference",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["checker", "lint", "finding-label", "diagnostic", "naming", "receipt", "lane-executor", "evidence-presentation"],
  "enforcement": "Pre-ship dogfood step: the checker author runs the checker on their own draft receipt and records that a cold reader's first inference from the label is correct; any label change must keep the re-runnable battery green (hidden_files/lint-battery/EXPECTED.txt, currently 8/8) — a new label class gets a new fixture case plus an expected line before the checker ships. Labels are extended additively, never silently rewritten.",
  "decision_change": "Closes the 'how do I name this checker's finding?' decision: before, a label naming only the defect class (LEADLESS-FRAGMENT) let a downstream seat reconstruct a phantom lead no existing file names; after, the label must name the situation the evidence describes (PHANTOM-LEAD-ABBREVIATION: phantom lead + abbreviation-inheritance), and the author dogfoods the label on their own draft before shipping.",
  "falsifier": "Ship a checker whose label names the situation per this rule, run the dogfood step, and a competent cold reader still draws the wrong first inference from the label (inference recorded on a cold read); or defect-named vs situation-named labels show no difference in downstream mis-inference rate across real receipts. Both measurable.",
  "mechanism": "The label is the first compressed summary a reader parses; readers pattern-match on it and skip re-deriving from the evidence. A defect-only label leaves the situation underdetermined, so the reader fills it in from their own story. A situation-naming label constrains the hypothesis space to the evidence — inference follows the constraint, which is why it must be designed, not decorated.",
  "evidence": {
    "mirror_lesson": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261020-1120-lane0.md (2026-10-20 18:26-18:31Z, Naya Clarity Narzan, honest 9.0/10) — label implemented additively, closing the parent receipt's hole",
    "parent_failure": "parent receipt reconstructed phantom lead brief-gap-lane-scorer-20261017-0030-lane0.md (names no existing file) from the LEADLESS-FRAGMENT label while the bytes were always right (15 phantoms, no existing files)",
    "checker": "hidden_files/bin/receipt-filename-lint.py (pure stdlib, sha256 1cfed7e9...) — label PHANTOM-LEAD-ABBREVIATION implemented additively",
    "battery": "hidden_files/lint-battery/ (8 re-runnable cases including case6/case7 new fixtures; 8/8 match EXPECTED.txt)",
    "recorded": "learning-events-2026-10-20-19.md ([LEARNING] CANDIDATE 731, 19:26Z review); CORE-PRINCIPLES.md line 1107"
  },
  "cousins": ["CANDIDATE 726 (name every lead fully - naming discipline in prose lists)", "CANDIDATE 729 (the gate that runs)", "CANDIDATE 730 (check before inheriting)", "SN-1739 (rule declared is a rule deferred - sibling label lesson from the same hour's lint)"],
  "status": "CANDIDATE"
}
```
