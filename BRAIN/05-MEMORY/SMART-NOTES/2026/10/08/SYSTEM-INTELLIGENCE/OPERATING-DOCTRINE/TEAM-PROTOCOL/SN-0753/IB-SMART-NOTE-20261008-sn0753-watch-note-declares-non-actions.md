# A Watch Note Declares Its Non-Actions

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0753-watch-note-declares-non-actions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6074183147 ([NAYA 2][BRAIN-BUILD LOOP — WATCH NOTE, 2026-10-09 04:16Z]) — SoulSchoolAcademy. Key recorded text: "**Not doing:** not closing #1900 (wave-sequenced by 6072910747 — per the standing collision rule, re-anchor belongs to the wave owner), not opening a second repair, no branch touched."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's brain-build loop ran a verification battery on the exact main tip `72e8bc17` and found Naya 4's wave sign-out 6072910747 stale-as-headed: written against tip `58bb427d` with "#1900 (base == tip, 3 index files)", while the live tip inventories 938 files against the committed basis of 806 — a 132-file delta. #1900's regen was computed at the old base and would land stale. So far, standard diagnosis.

The doctrine is in the note's "Not doing" paragraph. Having found another lane's staleness, Naya 2 declared in the same note the exact actions it was deliberately NOT taking: not closing #1900 (it is wave-sequenced, and per the standing collision rule re-anchor belongs to the wave owner), not opening a second repair (SN-0236: one RED class, one declared owner), no branch touched. Then it named the owner and the exact remediation: "#1900 needs a re-anchor (regen against post-#1837 current tip) at wave execution time, or the wave's 'base == tip' assumption should be re-validated."

Why this is brain-grade: in a parallel loop, the most dangerous moment is when an observer finds another lane's staleness — the instinct is to fix it. An unannounced "helpful" close or re-anchor collides with the owner's wave sequence and produces the exact clobber class SN-0745 documents. The collision rule ("re-anchor belongs to the wave owner") is a boundary; the written non-action declaration is what makes the boundary legible to every other lane reading the board. Restraint that is invisible looks like neglect — "they saw it and did nothing." Restraint that is written is a coordination signal — "the seam is known, owned, and being left alone." The watch note's job is complete diagnosis plus explicit restraint; the fix stays with the owner.

Rule for a cold successor: **when your verification finds another lane's work stale, report the finding and, in the same note, declare the actions you are deliberately not taking and name the owning lane.** A watch note ends with a non-action list. If you can't name what you're not doing, you haven't finished coordinating.

## 🩷 HUMAN NOTE

Shawn — a coordination lesson from tonight's brain-build loop. Naya 2 ran a verification battery and found Naya 4's wave work stale: a sign-out written against an older tip, with an index regen that would land 132 files out of date. Instead of "fixing" it, Naya 2 wrote down exactly what it was NOT doing — not closing the PR, not opening a competing repair, not touching any branch — and handed Naya 4 the precise fix needed (re-anchor the regen against the current tip when the wave executes). The standing rule: when you find another lane's staleness, you diagnose it fully, you declare your restraint in writing, and the fix stays with the owner. Written restraint is how parallel lanes avoid stepping on each other.

## 🟣 CHILD NOTE

Imagine you notice your friend's homework is done on the wrong worksheet. The smart move isn't grabbing her pencil and redoing it — she has a plan for how she'll fix it, and your "help" would mess up her plan. The smart move is telling her exactly what's wrong AND saying "I'm not going to touch your homework — it's yours to fix." Writing down "I'm not touching it" matters, because otherwise she can't tell whether you saw the problem or not.

## 👵 GRANDMA NOTE

A worker checked another team's work and found it was built on outdated information — a report that would land missing 132 files. She wrote up everything that was wrong, then added a paragraph stating exactly what she would NOT do: she wouldn't close their work, wouldn't start a competing fix, wouldn't touch their files. She named who owned the fix and exactly what they needed to do. The lesson: when you find someone else's staleness, diagnose it completely, declare your restraint in writing, and leave the repair to the owner.

## 🟠 NAYA NOTE

Make this mechanical in any parallel loop: (1) when verification finds another lane's stale work, the watch note states the finding with exact evidence (tips, deltas, bases); (2) the note then declares its non-actions explicitly — what it will not close, not open, not touch; (3) it cites the governing rule for the restraint (collision rule / one-red-class-one-owner); (4) it names the owner and the exact remediation at execution time. A watch note without a non-action list is an incomplete coordination artifact.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0753",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-DOCTRINE/TEAM-PROTOCOL",
  "doctrine": "watch-note-declares-non-actions",
  "rule": "When verification finds another lane's work stale, the watch note reports the finding and declares its non-actions in the same note: what it will not close, not open, not touch — naming the governing rule and the owning lane. The fix stays with the owner.",
  "failure_mode": "unannounced observer 'fixes' colliding with the owner's wave sequence; invisible restraint misread as neglect",
  "checks": [
    "every watch/relay note on another lane's staleness ends with an explicit non-action list",
    "the non-action list cites the governing rule and names the owner plus the exact remediation at execution time",
    "no branch, PR, or ref is touched by the observing lane in the same motion"
  ],
  "provenance": {
    "board": "#1354",
    "comment_id": 6074183147,
    "author": "SoulSchoolAcademy",
    "seat": "Naya 2",
    "timestamp": "2026-10-09T04:16Z"
  }
}
