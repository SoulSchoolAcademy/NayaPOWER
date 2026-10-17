# Boards Die at 2,500 Comments — Migrate the Coordination Board at 2,300

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01555-board-rollover-before-the-cap
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Live sequence 2026-10-17 ~06:38–06:48Z (shared-state.json `board_migration_20261017`; board #2721 comments 6230827688 redirect + 6230827986 announcement), and the dead board #1354 (`issue_1354_comments: 2500`, `issue_1354_comments_disabled: true` — GitHub hard cap hit 2026-10-10 ~12:21 PDT, commenting disabled by GitHub, issue not locked). Standing board-cap protocol: Shawn, 2026-10-13.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

GitHub hard-caps an issue at 2,500 comments and then disables commenting — the board dies where it stands, unreadable as a venue but frozen forever. #1354 died exactly this way on 2026-10-10. That is why the standing board-cap protocol (Shawn 2026-10-13) rolls the live coordination board at 2,300 comments, a full 200-comment buffer before the cliff: #2641 hit the trigger (2,338) and the director opened successor board #2721, posted the redirect (6230827688) and announcement (6230827986), preserved the #2641 watermark (6230770971), moved the `live_board` pointer in shared-state, queued the old board's distillation (brief-queue/brief-distill-feed-2641-20261017.md), and stamped DISTILLED AND RELEASED on the old body when the queue finished. The rollover is a protocol, not an ad-hoc move: open the successor, mirror the handoff, move the live pointer, preserve the watermark, keep the old board readable as archive, queue its distillation. Any lane still posting to the old board after the redirect is shouting into an archive — receipts must re-point.

## 🩷 HUMAN NOTE

Think of the team board as a whiteboard in a hallway everyone walks past. GitHub gives that whiteboard exactly 2,500 lines of space, and when it's full, nobody can write on it ever again — the marker just stops working. #1354 is that whiteboard: full since October 10, frozen. The team's rule is simple and mechanical: when the whiteboard hits 2,300 lines, we hang a fresh one next to it BEFORE it fills. On October 17 the director did exactly that — #2641 reached 2,338 lines, so successor #2721 went up with a big arrow saying "we moved here," the old board stayed readable behind glass, and the old board's watermark (the last line anyone read) was saved so no comment gets lost in the move. The lesson for the future: watch the comment count on #2721 the same way. At 2,300, you migrate — you do not negotiate with the cap, because the cap does not negotiate back.

## 🟣 CHILD NOTE

Imagine your notebook only has 2,500 pages, and when they're full, the pages glue themselves shut. That's what happened to board #1354 — glued shut forever. So the team has a rule: when a notebook reaches page 2,300, you start a new notebook. You draw a big arrow in the old one saying "continued in the new notebook," you remember which page you stopped on (the watermark), and you keep the old notebook where everyone can still read it. The new notebook is #2721. The rule never changes: at 2,300, you move. The glue doesn't care how important your next sentence is.

## 🔵 GRANDMA NOTE

Dear, this is about not outstaying a room. GitHub gives every discussion exactly 2,500 comments and then locks the door — it happened to our old board #1354 on October 10, mid-sentence, and there's no appealing it. So the team made a standing rule: at 2,300 comments, we move to a fresh board while we still can. We leave a note on the old door saying where we went, we write down exactly where we left off so nothing gets lost, and we keep the old room open for reading. #2721 is the third room we've moved into. The discipline is the watching: somebody checks the comment count every tick, because a board that dies full takes its last 200 unread comments with it — and nobody wants to be the one who let that happen twice.

## 🟠 NAYA NOTE

Run this protocol every time, identically: (1) the trigger is mechanical — `live_board_comments >= 2300` in shared-state, checked by the director's board watch; no judgment call, no "we can squeeze a few more"; (2) open the successor issue on the same repo, titled as the next coordination board; (3) post TWO comments on the old board — the redirect ("coordination moves to #N, effective now") and the announcement (what moved, watermark preserved, old board stays readable as archive); (4) preserve the old board's watermark (last processed comment id) in shared-state — that is the exact line where distillation stopped, and the successor board starts above it; (5) move the `live_board` pointer and the board-count fields in shared-state in the same tick — a moved pointer without a moved watermark is a hole; (6) queue the old board's distillation (brief-distill-feed-<old>-<date>.md) and land the DISTILLED AND RELEASED stamp on the old board's body when it completes; (7) every lane re-points its board receipts to the new board — receipts posted to the archive after the redirect are lost work. Cousin map: the cheap-check in the distillation cron (skip the #1354 fetch — its comments are capped at 2500 and commenting is disabled; the loop reads the live board pointer, never the dead issue); the boot-pointer STANDING re-anchor (SN-1552 — the instrument must name the live board, not the old one).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1555,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "boards_die_at_2500_comments_migrate_the_coordination_board_at_2300",
  "applies_when": [["board","rollover"],["coordination","board-cap"],["github","comment-limit"],["distillation","live-pointer"]],
  "enforcement": "The director's board watch reads shared-state live_board_comments every tick. At >= 2300 comments on the live board, the rollover protocol fires: (1) open the successor issue; (2) post redirect + announcement comments on the old board; (3) preserve the old board's watermark (last processed comment id) in shared-state; (4) move the live_board pointer and board-count fields in the same tick; (5) queue the old board's distillation and stamp DISTILLED AND RELEASED on its body when done; (6) all lanes re-point board receipts to the new board. No board is ever allowed to reach 2500. A lane posting coordination receipts to a superseded board after the redirect is routed, not argued with.",
  "evidence": {
    "the_cliff": "#1354: issue_1354_comments=2500, commenting disabled by GitHub 2026-10-10 ~12:21 PDT (hard cap, issue not locked) — the board died full, mid-use",
    "the_protocol": "standing board-cap protocol, Shawn 2026-10-13 — rollover at 2300 comments",
    "the_execution": "2026-10-17 ~06:38-06:48Z: #2641 hit 2338 (>= 2300 trigger) → successor #2721 opened; redirect comment 6230827688 + announcement 6230827986 posted on #2641; watermark 6230770971 preserved in shared-state; live_board pointer moved to 2721; old-board distillation queued (brief-queue/brief-distill-feed-2641-20261017.md)",
    "the_receipt_rule": "lanes re-point board receipts to #2721; receipts on the archived board after the redirect are lost work"
  },
  "procedure": [
    "watch live_board_comments in shared-state every director tick",
    "at >= 2300: open the successor issue on the same repo",
    "post the redirect and announcement comments on the old board (who moved it, watermark preserved, old board stays readable as archive)",
    "write the old board's watermark (last processed comment id) into shared-state before moving the pointer",
    "move the live_board pointer + board-count fields in the same tick",
    "queue the old board's distillation brief; stamp DISTILLED AND RELEASED on the old body when the queue drains",
    "announce the re-point: all lanes' board receipts go to the new board from here on"
  ],
  "falsifier": "The doctrine is scoped by GitHub's platform behavior and dies (or rescopes) if any of these prove false: (a) GitHub raises or removes the 2,500-comment cap — the 2,300 trigger must be re-derived from the new cap minus a safe buffer, not kept as ritual; (b) a rollover that skipped steps (no watermark preserved, no redirect posted) is shown to lose nothing — then the skipped steps are overhead, not protocol. Until either is evidenced, the full protocol stands.",
  "mechanism": "GitHub enforces a hard 2,500-comment ceiling per issue and disables commenting at the ceiling — a platform constraint, not a policy choice. A coordination board that reaches it loses its last unprocessed comments and its venue simultaneously. The 2,300-comment trigger exists as a 200-comment safety buffer: large enough for an orderly, watermark-preserving migration, small enough that no tick's backlog can plausibly fill the gap between trigger and execution. The redirect + preserved watermark + queued distillation make the migration lossless: no comment is processed twice, none is dropped, and the archive stays readable."
}
~~~
