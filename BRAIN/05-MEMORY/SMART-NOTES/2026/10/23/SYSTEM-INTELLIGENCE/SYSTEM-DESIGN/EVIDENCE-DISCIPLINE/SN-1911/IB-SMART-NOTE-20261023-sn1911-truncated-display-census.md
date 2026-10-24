Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A display is not a census. A backgrounded fetch's *displayed* output was truncated for presentation — and the partial per-PR lists were read as complete censuses while the complete lists sat untouched on disk. The result declared TIP-STALE, zero comments, and owed cards that were all wrong (the sibling seat's real cards existed on the same day). The rule: before you declare anything complete, read the full byte lists from disk. The scrollback is a summary; the disk is the census.

## 🩷 HUMAN NOTE

Shawn — a seat pulled a fetch, looked at what it printed on screen, and declared the whole picture: stale tip, no comments, owed cards. Every one of those calls was wrong, because the on-screen output was cut off — the full lists were sitting on disk the whole time, unread. The lesson is now a named failure mode: what the screen shows is not what happened. You count from the bytes on disk, never from the render.

## 🟣 CHILD NOTE

Imagine counting how many marbles are in a jar by looking at a photo of the jar — but the photo only shows the top half. You'd say "seven marbles!" while twenty more hide below the photo's edge. The real count was written down on a piece of paper next to the jar the whole time. The rule: count from the paper (the full list on disk), not from the photo (the screen). The photo lies by cropping.

## 🔵 GRANDMA NOTE

You asked someone to take inventory of the pantry. They glanced through the little kitchen window, saw three cans, and reported "three cans, pantry empty otherwise." But the full written inventory was on the counter — twelve cans. They never picked it up. The window (what the screen shows) is not the inventory (what's on disk). From now on: you pick up the list, you read every line, and only then do you report.

## 🟠 NAYA NOTE

The failure mode this kills: completeness verdicts (stale, zero-comments, owed-cards) computed on a truncated display rather than on the data. Owned publicly the same turn by the VERIFY seat (board comment 6376544207, 2026-10-23 23:30Z): a backgrounded fetch's displayed output was truncated; the partial per-PR lists were read as complete censuses while the complete lists sat on disk — the result declared TIP-STALE, zero comments, and owed cards that were all wrong (the sibling VERIFY's real cards existed 22:36–22:38Z the same day). Mechanism: display layers truncate for presentation (scrollback and pagination limits); a verdict computed on the render inherits the truncation invisibly, so "I saw the output" feels like "I saw all of it." The future decision this changes: when a seat needs a census — zero of anything, staleness, completeness of any list — it reads the full byte lists from disk (the output file of the backgrounded fetch) before declaring; a census claim whose only evidence is a displayed render is rejected. It would be proved wrong if a given tool's display render were byte-proven complete against disk — in which case the check becomes "prove the render complete first," and the lesson stands as the process that caught the miss. Cousins: the L9 absence/count corollary (a missing count is a claim, not a measurement); SN-1136 (asserted-receipt-must-exist-on-disk) — this is its display-side sibling: the census must exist on disk, not on screen.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1911-truncated-display-census",
  "lesson": "A display is not a census. A backgrounded fetch's displayed output was truncated for presentation; the partial per-PR lists were read as complete censuses while the complete lists sat on disk — the resulting TIP-STALE / zero-comments / owed-cards verdicts were all wrong (the sibling seat's real cards existed the same day). Completeness verdicts must be computed on the full byte lists read from disk, never on a displayed render.",
  "applies_when": ["verification", "census", "evidence", "fetch", "background-fetch", "display-truncation", "failure:partial-read", "completeness-verdict", "receipt"],
  "enforcement": "Any verdict claiming completeness (stale, zero comments, owed cards, full census) must cite the byte list on disk it was computed from. The reviewer rejects a census claim whose only evidence is a displayed render. Backgrounded fetches name their output file; the checker reads that file, never the scrollback. A display is a summary — the disk is the census.",
  "evidence": [
    "Board #2793 comment 6376544207 — VERIFY seat's public ownership (2026-10-23 23:30Z): 'a backgrounded fetch's *displayed* output was truncated; the partial per-PR lists were read as complete censuses while the complete lists sat on disk — the result declared TIP-STALE, zero comments, and owed cards that were all wrong (sibling VERIFY's cards existed 22:36–22:38Z)'",
    "hidden_files/live-plan.md — NAMED FAILURE MODE 'TRUNCATED-DISPLAY CENSUS' (2026-10-23 23:30Z): 'a display is not a census — read the full byte lists from disk (L9 absence/count corollary, again)'"
  ]
}
```
