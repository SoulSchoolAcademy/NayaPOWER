# Adjudication on an Archived Surface Is Invisible — Ship the Correction on the Live Surface

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01662-adjudication-archived-surface-invisible
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 20:38 PDT (2026-10-19T03:38Z), LEARNING EVENTS: L530 [F9] (board #2765 comment 6258599954 — "adjudication on an archived surface is invisible: cite-or-remove ships correction on the live surface"; WP-164 1/3). Board lineage: live board migrated #1354 → #2641 → #2721 → #2765; the first three are archive/read-only tails.

## ✦ IN A NUTSHELL

A verdict recorded only where nobody reads is not a verdict — it's a diary entry. When the live board moved from #1354 to #2641 to #2721 to #2765, every adjudication that stayed on the archived surfaces became invisible to the lanes working the live surface. Cite-or-remove exists to correct the record where the claim lives: the correction inherits the claim's audience, not the adjudicator's archive. Rule: the verdict quotes its live-surface target (live board issue + claim comment ID), and the correction ships as a comment on that live surface. An adjudication with no live-surface landing is UNDELIVERED.

## 🩷 HUMAN NOTE

Shawn — when the team moved boards, the old boards became archives nobody reads. We found that rulings left on those archived boards were invisible to everyone doing the actual work — the verdict existed, but nobody it was meant for ever saw it. The new rule: whenever we rule on something, the ruling and its correction get posted on the live board where the original claim lives, not in the archive. A correction only works where eyes are.

## 🟣 CHILD NOTE

Imagine the teacher writes "homework is cancelled" on a whiteboard in a classroom nobody uses anymore. The note is real, the teacher meant it — but every student is in the NEW classroom looking at the new board, doing homework. Writing where nobody looks is the same as not writing at all. The fix: always write the important note on the board people actually look at.

## 🔵 GRANDMA NOTE

It's like publishing a correction in a newspaper that stopped printing — the correction is true, but nobody who read the original mistake ever sees it. The team's live board moved several times this month, and rulings left behind on the old boards were never seen by the people they were meant for. Now the rule is simple: the correction goes where the original claim lives, on the board everyone reads. A verdict nobody sees can't change anything.

## 🟠 NAYA NOTE

Cold successor: every adjudication verdict must land on the live surface where its claim lives, or it is UNDELIVERED.

1. Before posting a verdict, identify the LIVE surface: the live board issue (currently #2765 per shared-state `live_board`) and the claim's comment ID on it. Archive tails (#1354, #2641, #2721) are never the venue — they are read-only history.
2. The verdict comment quotes its target: live board issue number + the exact claim comment ID it adjudicates. No bare verdicts.
3. Cite-or-remove's correction ships as a comment on that same live surface. The correction inherits the claim's audience, never the adjudicator's archive.
4. A verdict posted only to an archive board is classified UNDELIVERED: it carries no authority over live work until a copy lands on the live surface. Downstream lanes are entitled to ignore it.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1662",
  "title": "Adjudication on an Archived Surface Is Invisible — Ship the Correction on the Live Surface",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "ADJUDICATION-SURFACES"],
  "applies_when": ["governance", "adjudication", "verdict", "visibility", "cite-or-remove", "live-surface", "board-migration"],
  "enforcement": "Every adjudication verdict quotes its live-surface target (live board issue number from shared-state live_board plus the claim comment ID) and the cite-or-remove correction lands as a comment on that live surface. A spot-audit flags any verdict posted only to an archive board (#1354/#2641/#2721 tails) as UNDELIVERED with zero authority over live work; cite-or-remove closes only when the correction comment exists on the live surface.",
  "cousins": ["SN-1306 (delivery proven where the Naya reads — same visibility principle applied to verdicts)", "SN-0175 (endorsement only counts on a live venue re-read — the venue, not the archive, is where claims count)"],
  "evidence": {
    "learning_event": "hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 20:38 PDT (2026-10-19T03:38Z): L530 [F9] (board #2765 comment 6258599954 — adjudication on an archived surface is invisible: cite-or-remove ships correction on the live surface; WP-164 1/3)",
    "board_lineage": "live board migrated #1354 (capped 2500, 2026-10-10) -> #2641 -> #2721 (DISTILLED AND RELEASED 2026-10-18) -> #2765 (live); first three are archive/read-only tails with zero live readership"
  },
  "decision_change": "the next adjudication or cite-or-remove decision posts the verdict and its correction to the live surface where the claim lives (live board issue + claim comment ID quoted) — never only to an archive board, and never as a bare verdict with no quoted target.",
  "falsifier": "an adjudication posted only to an archived surface that demonstrably reaches the live actors and changes their behavior would disprove the invisibility claim — a verdict with an observed live audience despite an archive venue.",
  "mechanism": "Actors read the live surface; archived boards are read by nobody. A verdict's authority flows through visibility: a verdict no live actor sees cannot steer live behavior. Cite-or-remove's function is to correct the record where the claim lives, so the correction must inherit the claim's audience, not the adjudicator's archive. The quoted live-surface target is the content-addressable anchor that makes the verdict auditable."
}
```
