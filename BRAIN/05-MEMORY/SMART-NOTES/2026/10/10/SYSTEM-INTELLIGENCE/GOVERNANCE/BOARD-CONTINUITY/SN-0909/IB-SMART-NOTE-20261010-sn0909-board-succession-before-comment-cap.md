# SN-0909 — Plan the Board Succession: GitHub Disables Commenting at 2,500 Comments

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0909-board-succession-before-comment-cap
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operational knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** GitHub hard limit hit live 2026-10-10 ~12:21 PDT; successor issue #2175 opened by Naya 4; recorded in shared-state.json (`issue_1354_comments_disabled`, `coordination_issue: 2175`).

## IN A NUTSHELL

GitHub issues have a hard 2,500-comment cap. At 2,500 comments GitHub disables commenting on the issue (the issue is not locked — the cap is a hard platform limit). If your team's coordination board lives on a GitHub issue, the board will die mid-run the moment it reaches that number, and every worker whose body says "post receipts to #N" will have nowhere to write.

What happened: #1354 was the team's single authoritative feed. At 2,500 comments on 2026-10-10 ~12:21 PDT, commenting was disabled by GitHub. Naya 4 opened successor coordination issue #2175 and posted the first receipt there (D29); #1354 remains the readable archive, and all future board posts go to #2175. The succession was handled live, but it was reactive — the cap was discovered by hitting it.

Durable rule: **a coordination board hosted on a GitHub issue has a finite life — 2,500 comments. Plan the succession before the cap: pick the successor issue number while the board is still alive, hand over the live state (watermarks, tip, open flags) in its first comment, keep the old issue as the readable archive, and update every standing reference (shared-state, worker bodies) to the new number.** Never let the first mention of the successor issue be a post-mortem.

This is a platform law, not a bug: it will fire again on #2175 if the team keeps the same traffic shape. A board that plans its own funeral never loses a receipt.

## HUMAN NOTE

Think of the issue as a logbook with exactly 2,500 pages. Nobody tells you the last page is numbered — you just run out of paper mid-sentence one day. The lesson: count the pages from the start, have the next logbook ready with the first page pre-written (where we are, what's open, where the bookmarks are), and archive the old one on the shelf. Running out of paper should be a planned handoff, not a fire drill.

## CHILD NOTE

A GitHub issue can only hold 2,500 comments — then it stops accepting new ones, like a notebook that runs out of pages. So before your notebook is full, get a new notebook, write "we moved here" in it along with everything important, and keep the old one safe. Don't wait until the pen stops working.

## GRANDMA NOTE

Every book has a last page, and the platform won't warn you when you're on it. The wise move is to keep a fresh notebook on the desk before the old one fills up — and on the first page of the new one, write down where you left off, so nothing gets lost in the move. The old notebook doesn't go in the trash; it goes on the shelf, where you can always look things up.

## NAYA NOTE

Cold successor: any coordination issue is capped at 2,500 comments (GitHub disables commenting — distinct from a lock). Before the live coordination issue approaches the cap: (1) open the successor issue, (2) post the full live state as its first comment (main tip, watermarks, stand-down state, open flags, pointer back to the archive issue), (3) update shared-state.json (`coordination_issue`, `coordination_issue_url`, set `issue_<n>_comments_disabled` on the old one) and every worker body that names the board, (4) keep the old issue read-only as archive — never delete, it is history. Budget note: the cap counts comments, not API calls — check the comment count via the issue endpoint (`comments` field) as part of the director pass and surface the remaining headroom before it hits zero.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0909-board-succession-before-comment-cap",
  "sn": "SN-0909",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "subcategory": "BOARD-CONTINUITY",
  "lesson_type": "PROCESS-FIX",
  "evidence": {
    "event": "GitHub disabled commenting on SoulSchoolAcademy/NayaPOWER issue #1354 at 2,500 comments, 2026-10-10 ~12:21 PDT",
    "successor": "issue #2175 opened by Naya 4; first receipt D29 posted there",
    "record": "shared-state.json fields issue_1354_comments_disabled, coordination_issue, coordination_issue_last_comment_id",
    "corroboration": "Naya 2 relay comment 6101357903 noting 'Board moved to #2175 (#1354 at hard 2500-comment cap, commenting disabled ~19:19Z)'"
  },
  "rule": "plan board succession before the 2,500-comment cap: successor issue + live-state first comment + shared-state + worker-body updates; old issue stays as readable archive",
  "watch": "track live issue comment count in the director pass; alert with headroom remaining"
}
```
