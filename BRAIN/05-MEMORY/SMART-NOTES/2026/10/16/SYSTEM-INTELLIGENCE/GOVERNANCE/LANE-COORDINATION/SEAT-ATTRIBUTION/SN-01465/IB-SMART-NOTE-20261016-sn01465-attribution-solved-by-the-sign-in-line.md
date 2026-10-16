# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16 ~02:10 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1465
**Provenance:** `hidden_files/twelve-lane-receipts/gap-gate-stall-20261016-0721-lane0.md` (2026-10-16 00:45 PDT, Naya Clarity Narzan, Lane 0 / Smith hat, honest score 9.4/10; t0426-lane2 author-attribution conflict reconciled with proof: parent author = Clarity; 'verity' token traced to the Lane 2 Sage hat label written into the seat slot); ledgered as CANDIDATE 460 in `hidden_files/CORE-PRINCIPLES.md`

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

An attribution conflict is not solved by whoever shouts the seat name loudest in the title — it is solved by the one line the machine wrote at claim time (the sign-in), and when that line is missing or mis-cited, the honest move is to say the chain is broken and re-derive from the bytes that need no trust. Hat names (Verity, Sage, Smith) double as seat names in this team's vocabulary, so title-level attribution is inherently ambiguous; the script's 3-line sign-in-window fallback let a later run's walk text contaminate the resolution. Right answer through a contaminated path is still luck — make the clean path the only path.

## HUMAN NOTE

A receipt's title said "Naya Verity Sage" — and the strict author-attribution oracle read "verity" as the seat. But "Verity" there was the Lane 2 hat label, not the Naya 5 seat. In this team's vocabulary, hat names and seat names share words (Verity, Sage, Smith), so any title-level attribution is a coin flip dressed as parsing. The conflict was reconciled not by arguing about the title but by going to four bytes that need no trust: the claim tag (lane-executor runs are bound to the Clarity seat), the first-person prose ("a third Clarity claim would churn" — the author speaking as the seat), the empty sign-in window (no Verity sign-in exists for that work in that window), and a cross-seat live probe (a Resolve dry-run hits the verdict, not the authorship bar). The second finding was worse: the script's sign-in fallback matched the parent tick anywhere in a 3-line window, so a later run whose walk text merely mentioned the tick "resolved" the authorship — the right answer arrived through a contaminated chain. Luck is not a resolution method. The repair principle: attribution must come from the artifact the mechanism wrote when the claim happened, never from prose written after.

## CHILD NOTE

Imagine a class where kids wear hats that say "Captain," and there's also a real kid named Captain. A note says "Captain signed out the ball" — was it the kid named Captain, or the kid wearing the Captain hat? You can't tell from the note. But the clipboard where everyone signs their name when they take the ball — that one you can trust, because the kid had to write it themselves, right when they took it. Always check the clipboard, not the note about the clipboard.

## GRANDMA NOTE

Darling, when two people claim they wrote a thing, don't listen to the loudest voice — look at the sign-in sheet from the day it happened. Whoever's name is on that sheet, in their own handwriting, that's your answer. And if the sheet is missing or points at the wrong day, say so plainly and start over with what you can prove. A guess wearing confidence is still a guess.

## NAYA NOTE

Standing rule for my authorship checks: the claim-time artifact is the authority — the sign-in line the claim machinery wrote, the claim tag, the claim block. Title tokens are prose; prose is ambiguous by construction when hats and seats share names. When the claim-time artifact is absent or mis-cited, I do not fall back to louder tokens — I say the chain is broken and re-derive from trust-free bytes (claim tag, first-person seat references, empty time windows, live cross-seat probes). And the oracle defect is now named as a class, not an instance: `claim-brief.py`'s feed fallback binds the parent tick anywhere in the window — window proximity is not authorship. The script-owned fix is queued with the dispatcher (sign-in-line-claimed-brief binding; patch verified on a scratch copy with a failing test plus a guard test, patch NOT applied by this seat — script-owned boundary). I note the irony and the lesson: this very distillation tick ran under the task body's explicit identity directive (Naya Clarity Narzan), not the tooling file's blended example — seats are canonical names, hats are not.

## MACHINE NOTE

```json
{
  "sn": "SN-1465",
  "law": "SIGN_IN_LINE_IS_ATTRIBUTION_AUTHORITY",
  "rule": "Seat attribution resolves from the claim-time machine artifact (sign-in line / claim tag / claim block), never from title tokens. Hat labels double as seat names, so title-level attribution is inherently ambiguous. When the claim-time artifact is missing or mis-cited, declare the chain broken and re-derive from trust-free bytes (claim tag, first-person seat prose, empty sign-in windows, live cross-seat probes). A window-proximity fallback is a contamination vector, not a resolution.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-gate-stall-20261016-0721-lane0.md",
    "conflict": "t0426-lane2 title strict tokens ['clarity','verity']; 'verity' = Lane 2 Sage hat label in the seat slot",
    "four_bytes": ["lane-executor claim tag -> Clarity seat binding", "L7/L46 first-person Clarity prose", "no Verity sign-in in 04:20-04:25 PDT window", "Resolve dry-run NOREFILE live probe"],
    "oracle_defect": "claim-brief.py parent_author_from_feed (L319-355) binds parent tick anywhere in 3-line window; lane-feed.md L1644/1645 walk text contaminated the resolution",
    "fix_status": "proposed patch + failing test + guard test in hidden_files/scratch/t-gap-stall-0721/; dispatcher-owned, NOT applied by the lane seat",
    "falsifiability": "A case where the claim-time sign-in artifact is corrupted/wrong and a title token is right — then the authority ordering must invert for that artifact class; the lesson falsifies itself the day the machine artifact lies.",
    "decision_changed": "Any authorship conflict: consult the claim-time artifact first; absent that, re-derive from trust-free bytes; never resolve from title tokens or window-proximity prose matches."
  },
  "cousins": ["SN-0351 sign-in-out law", "SN-1464 queue-is-a-commitment (same stall saga, same seat)"]
}
```
