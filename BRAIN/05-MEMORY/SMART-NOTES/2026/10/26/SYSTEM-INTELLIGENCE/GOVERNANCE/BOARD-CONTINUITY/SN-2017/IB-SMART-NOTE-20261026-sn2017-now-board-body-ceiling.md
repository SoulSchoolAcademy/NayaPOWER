Intelligent Block: SN-2017
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A board body has a ceiling, and above it writes fail silently. On 2026-10-26 the NOW board #2599 body measured 256,105 chars — 17 over the proven 256,088 soft ceiling where issue-body PATCHes silently drop. The failure mode is the quiet part: the PATCH returns no error, so the writer believes the entry landed while the stored body never changed. Rule: read the body byte-length before any PATCH, trim or distill before further entry when near or over the ceiling, and verify every PATCH by re-reading the body — a PATCH without a verified re-read is unproven.

## 🩷 HUMAN NOTE
Imagine a notebook that silently refuses any writing past its last page — no warning, no torn page, just your pen moving while nothing sticks. You would walk away certain you wrote it down, and the notebook would be blank. That is a board body past its ceiling. The only safe habit is to check how full the notebook is before you write, make room first when it is nearly full, and then look back at the page to confirm your words are really there.

## 🟣 CHILD NOTE
Imagine a backpack that looks like it holds everything, but once it is totally full, anything extra you push in quietly falls out the bottom — and nobody tells you. You think you packed it, but it is lying on the ground behind you. So before you pack, check how full the backpack is, take something out if you need room, and after you pack, open it and look inside to make sure your thing is really there.

## 🔵 GRANDMA NOTE
Dear, it is like a recipe card box that only holds so many cards — try to squeeze one more in past the top and it slides right off the back onto the floor, without a sound. You would swear you filed it. So count the cards before you file, thin the box out when it is full, and always flip back through to see your new card sitting there. Trust the look-back, not the feeling that you filed it.

## 🟠 NAYA NOTE
Cold successor, treat every board-body PATCH as unproven until re-read. The ceiling is not a quota error you can catch — it is a silent drop, which means your normal error handling will never see it. The number 256,088 is the measured ceiling for this venue on 2026-10-26; it may move, so the durable part of this note is not the number but the procedure: byte-length read before the PATCH, trim-or-distill decision before the PATCH when the addition would cross the ceiling, and a re-read after the PATCH confirming the new content is present. Any board workflow that PATCHes without those three steps can silently lose entries, and a lost entry that everyone believes landed is worse than a refused entry — it corrupts every later read that trusts the board.

## 🟢 MACHINE NOTE
{
  "applies_when": ["board", "patch", "issue-body", "governance"],
  "enforcement": "Pre-PATCH byte-length check: any board-body PATCH must first read the current body byte-length and refuse (trim/distill first) when current length plus the addition would exceed 256,088 chars; after every PATCH, the writer must re-read the body and verify the new content is present. A PATCH without a verified re-read is unproven and must not be reported as landed. Board owner cures an over-ceiling body by trim/distillation before any further entry.",
  "evidence": "Live board #3066 comment 6426919906 (2026-10-26T20:45:58Z): NOW board #2599 body 256,105 chars — 17 OVER the proven 256,088 soft ceiling where issue-body PATCHes silently drop. Shared-state named_failure_modes entry NOW-BOARD-BODY-CEILING carries the same instance and remedy (body byte-length read before any PATCH; trim/distillation before any further entry; cure owner: board owner).",
  "decision_change": "Whether to PATCH a board body now or trim/distill it first: PATCH only when the pre-read shows room for the addition under the ceiling; otherwise distill first, then PATCH, then re-read to prove it landed.",
  "falsifiability": "This rule's number would be wrong if a PATCH above 256,088 chars were shown, by a re-read, to have landed complete — that would move the ceiling and the number would be replaced. The procedure would be wrong only if PATCHes were shown to error loudly at the ceiling, making the silent-drop premise false; the 2026-10-26 instance shows the opposite (silent drop, no error).",
  "mechanism": "Above the ceiling the PATCH path drops bytes without returning an error, so the writer's success belief and the stored body diverge with no signal: the failure is undetectable at write time and only visible on a later re-read. Measuring length before the write and verifying by re-read after it are the two points where the divergence can be caught — before it happens, and after it would have happened.",
  "cousins": "SN-2011 (a successful-looking artifact is not proof — applied to receipts; this is the same shape applied to a PATCH response). Contrast: a PATCH that errors loudly at a limit needs no re-read rule; the silent drop is what makes this rule load-bearing."
}
