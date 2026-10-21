# CANDIDATE Absorbs Uncertainty — The Merge Rule for Notes with Disclosed Unknowns

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0325-candidate-absorbs-uncertainty
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 5988473463 (2026-10-05T05:07:37Z / 2026-10-04 22:07 PDT — Naya 2's #1438 rebase receipt and merge-intent rationale, executed by her own hand after three specialist attempts died on runtime inference timeouts); merge executed at comment 5988488663 (`d986d0b27582`, new main tip).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A CANDIDATE Smart Note carrying a disclosed, explicitly filed unknown does not need to wait for certainty before it merges. Naya 2's #1438 (SN-0312, "The Awesome Code") had a live open question — the two source versions might not agree on all 100 items — but the note filed it under *Uncertainty*, not under fact, disclosed it on the board, and argued the merge anyway: merging a CANDIDATE note creates no obligation and changes no code; it stages content for Shawn's ratification review, which is exactly where the equivalence question gets settled. The decisive calculus: **holding blocks zero risk reduction** (waiting teaches nothing new — the question is only answered by ratification review, not by delay), while the CANDIDATE state is *designed* to absorb the correction — if the claim proves wrong, the note's uncertainty section is corrected post-merge, CANDIDATE → corrected CANDIDATE, no harm done.

The rule, stated for a cold Naya: *if the unknown is disclosed as unknown, merging is safe; if the unknown is disguised as fact, merging is forbidden.* The admission test has two questions: (1) is the uncertainty explicitly labeled in the note itself (not buried in a comment thread)? (2) does merging change anything irreversible — code, authority, production? A note that answers yes to (1) and no to (2) should merge. Uncertainty disclosure is a merge qualification, not a merge blocker — that is the whole point of the CANDIDATE truth state existing.

This pairs with the falsifier discipline already practiced on the board: Naya 2 named her falsifier in the receipt ("if the equivalence claim proves wrong, the note's uncertainty section is corrected post-merge"). A merge intent that carries its own falsifier is stronger evidence of judgment than a held note with none.

## 🩷 HUMAN NOTE

Shawn — Naya 2 just proved out a merge rule worth keeping: SN-0312 went to main with an open question inside it, and that was the right call. The note said "here's what we don't know yet" out loud, in its own text — not hidden, not implied. A CANDIDATE note is built to absorb corrections; that's its whole job. So holding it back for certainty would have bought nothing, and merging it stages the question for your ratification review, which is the only place it can actually be answered. The rule: if a note tells you what it doesn't know, it can ship. If it pretends to know, it can't. That's CANDIDATE working as designed.

## 🟣 CHILD NOTE

Imagine you're writing a report card for the class, but there's one question you don't know the answer to. You have two choices: (a) write down a guess and pretend you're sure, or (b) write "I don't know this part yet" right in the report. Choice (b) is always better! You can hand the report in — the teacher knows exactly what's still open, and you can fix it later. That's what happened: the note said "here's the part I'm unsure about," so it was safe to file. Pretending to be sure would have been the real mistake.

## 👵 GRANDMA NOTE

Sometimes you don't have all the answers, and that's fine — as long as you're honest about it. This note was about a rule for saving our lessons: if you write down what you're *not* sure about, right alongside what you are, it's safe to save. The system expects these notes to be corrected over time — they're drafts by design, waiting for your final word. Hiding an unknown is the danger; naming it is the protection.

## 🤖 NAYA NOTE

For future seats: when you stage a Smart Note that contains a live unknown, apply the two-question admission test before deciding to hold it: (1) is the unknown explicitly labeled *in the note itself* (Uncertainty section, not a thread comment)? (2) does merging change anything irreversible (code, authority semantics, production)? Yes to (1) + no to (2) → merge with the falsifier stated in your receipt ("if X proves wrong, correct Y post-merge"). Holding for certainty in that case is process theater — it reduces zero risk. Also: never let a note merge that disguises an unknown as a fact. The CANDIDATE state absorbs disclosed uncertainty; it does not survive discovered dishonesty.

## ⚙️ MACHINE NOTE

```json
{
  "sn_number": "SN-0325",
  "slug": "candidate-absorbs-uncertainty",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": [
    "#1354 comment 5988473463 (2026-10-05T05:07:37Z) — Naya 2's #1438 rebase receipt + merge intent, including the CANDIDATE-absorbs-uncertainty rationale, strongest-alternative analysis, and stated falsifier",
    "#1354 comment 5988488663 (2026-10-05T05:09:22Z) — #1438 merged via squash at d986d0b27582; SN-0311 and SN-0312 both on main, both CANDIDATE awaiting ratification"
  ],
  "taxonomy": "BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-DOCTRINE/SN-0325",
  "law": "A CANDIDATE Smart Note with uncertainty explicitly disclosed in its own text and no irreversible merge effect should merge; holding reduces zero risk. Uncertainty disclosure is a merge qualification, not a blocker — disguising an unknown as fact is the only true blocker.",
  "ratification_status": "CANDIDATE — lane-operated precedent, not ratified by Shawn; auto-capture is not auto-ratify.",
  "cousins": ["Evidence Law (never fabricate certainty)", "CANDIDATE ≠ VERIFIED ≠ MERGED ≠ DEPLOYED doctrine", "FULL-AUTO-MERGE-V1 draft (PR #1444)"],
  "keywords": ["candidate", "uncertainty disclosure", "merge rule", "SN-0312", "auto-merge", "falsifier", "operating doctrine"]
}
```
