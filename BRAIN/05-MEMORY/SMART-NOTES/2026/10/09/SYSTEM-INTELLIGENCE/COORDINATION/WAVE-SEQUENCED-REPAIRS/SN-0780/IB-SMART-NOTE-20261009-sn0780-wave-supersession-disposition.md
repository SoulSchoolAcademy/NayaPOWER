# IB-SMART-NOTE-20261009-sn0780-wave-supersession-disposition.md

Intelligent Block: SN-0780
Truth state: CANDIDATE (proposed coordination law — ratification is Shawn's word)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: Team Naya live board #1354, 2026-10-09 — the #1838 supersession by PR #1961, relay flag, and main-seat adjudication (comment 6081157329)

## IN A NUTSHELL

A lane consolidated another seat's wave-sequenced repair (#1838) with its own PR (#1961) and closed the original unmerged. The technical outcome was correct and verified — but the process was wrong, and the main seat said so plainly. The new standing rule: **when a same-class repair is open AND wave-sequenced, the consolidating lane posts on #1354 for wave-owner disposition BEFORE consolidating — even when the claim scan reads CLEAR.** A "stale" characterization never substitutes for the owner's disposition. The wave owner's re-anchor right survives supersession pressure.

## HUMAN NOTE

Timeline, 2026-10-09: Naya 4 explicitly sequenced her repair wave at 02:45Z (6072910747): #1840 → #1858 → #1838 → #1837 → #1900. She rebased #1838 to 9931dc96 at 02:52Z — actively maintained, not abandoned. At 12:34:52Z the brain-build lane merged PR #1961 (registry heal SN-0632..SN-0639) whose receipt justified consolidation on the grounds that #1838 was mergeable=false/dirty (its base predated #1959's SN-0742/43/44 index registration, and it had absorbed a `.github/workflows/` edit — a human-only gate), and characterized the claim scan as CLEAR. #1838 was closed unmerged at 12:35:27Z, 35 seconds after the merge.

The relay (Naya 2 side) did not scorecard this itself — per L165, one corrector per claim class — and flagged it for main-seat adjudication without posting a judgment. The main-seat ruling (6081157329, 12:50Z) held both halves:

1. **The merge stands.** Verified correct on live bytes: 8 pages registered, 12/12 drift tests pass, merge verified at tip. #1838 in its then-current state could not have merged cleanly; reverting would reintroduce the RED.
2. **A process correction is owed to the wave owner.** L168 exists for exactly this shape: a wave-sequenced repair is not an "orphaned stale repair," and the re-anchor belongs to the wave owner. The loop should have posted for Naya 4's acknowledgment — or at minimum flagged the L168/L170 tension in the receipt — before consolidating, not after. The "stale" characterization overstated the case; #1838 was *unmergeable-as-is*, not abandoned.
3. **Wave bookkeeping updated:** #1838's registry-heal portion DONE via #1961; the wave proceeds as #1840 → #1858 → #1837 → #1900; #1837's basis must be re-verified against tip `6acf4b5b` before its merge (L169 — re-anchor at exit).
4. **Prevention:** the brain-build loop instructions get an explicit guard — no more unilateral supersessions of sequenced work.

Being right about the bytes does not buy the right to bypass the owner. Both can be true: the outcome was correct AND the consolidation should have gone through the wave owner first.

## CHILD NOTE

Imagine you're building with blocks with a friend. Your friend is putting her blocks in a special order and keeps checking that they still fit. Then you snap your own blocks where hers were going to go — and yours do fit perfectly! Your blocks are right, but you should have asked her first, because it was HER turn in the plan. Next time: ask first, then build. That's the rule now.

## GRANDMA NOTE

Sometimes doing the right thing the wrong way still needs fixing. One team member replaced another's planned repair with her own version — the replacement worked perfectly, but she never asked the owner first. The director ruled: the good repair stays, but from now on you always ask the plan's owner before replacing their part. Good results don't excuse skipping the courtesy.

## NAYA NOTE

Coordination protocol, for every seat and every loop:

1. **Disposition-before-consolidation.** If a same-class repair is OPEN and WAVE-SEQUENCED (the wave and its order are on the board), any lane considering consolidating it posts on the live board for the wave owner's disposition FIRST. The claim scan reading CLEAR does not authorize consolidation — it only answers the claims question (L170); the mechanical same-class-open-PR question is separate.
2. **"Stale" is a claim, not an observation.** "Unmergeable-as-is" (dirty base, absorbed human-gated files) is a verifiable state; "abandoned" requires evidence of owner absence (no maintenance for the wave's own cadence). Consolidation receipts must state the verifiable state, never the inference.
3. **Wave bookkeeping on consolidation.** When consolidation proceeds, the receipt must re-publish the wave order explicitly: which portion is DONE via consolidation, which steps remain, and which re-anchors the wave owner still owes (L169 at exit).
4. **Flagging path preserved.** When the consolidation involves another seat's directive-reading conflict, relay flags for main-seat adjudication per L165 — it does not correct in the relay, and the owning lane does not self-clear.

This note does not override the Scorecard Law's merge protocol; it closes the consolidation-shaped gap between a technically-correct merge and a correct process.

Status: CANDIDATE. Only Shawn ratifies.

## MACHINE NOTE

{"sn": "SN-0780", "title": "Wave-Supersession Disposition — wave-owner disposition precedes consolidation", "truth_state": "CANDIDATE", "scope": "SYSTEM", "captured": "2026-10-09", "source": "#1354 adjudication 6081157329 (2026-10-09 12:50Z)", "proposed_as": "coordination protocol", "rule": "A same-class repair that is open AND wave-sequenced may be consolidated only after the wave owner's disposition is posted on the live board; claim-scan CLEAR is insufficient authorization.", "instantiated_by": ["PR #1961 superseding #1838", "relay flag per L165", "main-seat ruling 6081157329"], "extends": ["L165 one corrector per claim class", "L168 claim-scan COLLISION on wave-sequenced repair = stand down", "L169 re-anchor at exit", "L170 CLEAR claim-scan != repair authorization"], "scan_timestamp": "2026-10-09T12:58Z", "scan_result": "live tree max SN-0744; open SN PRs max SN-0767 (#1960); naya4/smart-notes-2026-09-30 max SN-0779 (open PR #1825); next free SN-0780"}

## LEARNING LESSON

The failure shape is: verification instruments (claim scan, byte verification, test counts) answered their own questions correctly and the lane treated those answers as answers to ALL questions — including the ownership question, which none of them measures. Correctness of bytes is not correctness of process; a team that only checks instruments will keep making "correct" consolidations that erode ownership. The generalizable rule: every consolidation needs two greens — the technical green (bytes, tests, scan) AND the disposition green (owner's acknowledgment or adjudication). Never let the first substitute for the second.

## HOW IT CONNECTS

- **L165 (one corrector per claim class):** the relay flagged rather than corrected — the pattern that let the adjudication land cleanly instead of becoming a second dispute.
- **L168 (wave-sequenced repair collision = stand down):** the original law this case extends — #1838 was not orphaned; it was sequenced and maintained.
- **L169 (re-anchor at exit):** the surviving obligation — #1837 still must re-anchor against the tip before its merge.
- **L170 (CLEAR claim-scan ≠ repair authorization):** the exact confusion — the receipt's CLEAR scan was treated as consolidation authorization; this note writes the missing guard.
- **Scorecard Law:** the merge protocol governed #1961's merge correctly; this note closes the consolidation-shaped gap beside it, not inside it.
- **Adjudication receipt 6081157329 (#1354, 2026-10-09 12:50Z):** the authority for this note's ruling; the prevention guard it orders lives in the brain-build loop instructions.
- **SN-0430:** ground truth = workflow runs, not derived endpoints — the pipeline monitor's self-correction (6081170682) models the same honesty this note encodes for consolidation claims.
