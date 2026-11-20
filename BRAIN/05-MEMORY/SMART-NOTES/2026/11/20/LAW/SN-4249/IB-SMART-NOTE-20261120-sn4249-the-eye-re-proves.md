# SN-4249 — The Eye Re-Proves — An Adjudication Is Settled Only When the Next Seat Proves It Again

**Category:** LAW
**Filed:** SN-4249 — Intelligence Loop run 410, 2026-11-20.

## The lesson

The fix-8 independent checker adjudicated the clipped lesson title at 390 as YouTube's own embed chrome, not page markup. The captain's eye did not take that adjudication on trust — it ran its own fresh probe (steps P1b/P1c): `body.innerText` contains neither clipped string; `elementFromPoint` at the title area returns the `IFRAME` itself; `contentDocument` is null (cross-origin youtube-nocookie); the full title already reads in the `h3` directly below the player, 4 lines, `scrollWidth == clientWidth`. Only then did the eye call the defect complete — and only then was the lane closed. An adjudication is a claim until the next seat re-proves it with its own probe. Two independent probes, same answer, is what settles it.

## The value

A verdict inherited is a verdict resting on one probe. If the checker had been wrong about the owner, an eye that merely read the checker would have closed a live defect. The eye's own probe cost minutes and bought the certainty the whole lane now stands on: the doubled bar is gone by DOM census (exactly one bar visible on every view, both widths), the title clip is not a page defect, and the 36/36 regression holds. The product call the eye named — accept YouTube's narrow-width truncation, the full title reads twice on the page itself — is a decision, not a failure, and it is the captain's to put to Shawn, not the eye's to bury.

## The rule

A seat that receives an adjudication re-proves it with its own probe before it closes anything on it. Reading the prior report is the starting point, never the proof. The verdict names the probe it ran, not the report it read.

## Where it came from

Membership rebuild fix-8 captain's eye report, verdict PASS filed 2026-11-20 10:36:24Z (agent 77709b98, `~/workspace/team-nitro/membership-rebuild-fix8-20261119/eye/EYE-REPORT.md`): "my own independent probe proves the clipped text is YouTube's own embed chrome inside the cross-origin iframe, not page markup, and the full lesson title already reads in the wrapping `h3` directly below the player." Record filed to branch `membership/rebuild-fix8-20261119`, tip `38aeb7ad`, 26/26 files verified (record seat a4927545, 10:40:35Z).

## Paired Naya Note

None — no Shawn dictation in this window; this lesson comes from the eye's own verification chain, not from his words.
