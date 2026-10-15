# 09 — BLOCKERS: no orphan stalls — every stall names its blocker, its owner, and the unblock path

## ESSENCE
Every stall names three things — the blocker, its owner, the unblock path — or it is an orphan, and orphans get routed, never parked.

## WHAT IT IS
The blocker triad, named the moment the stall appears, in the receipt's BLOCKERS field, while the evidence is warm — never at sign-out, never in prose-only memory. One line: what's stopped, by what cause, who owns it, and the next physical step (the command, the file, the ask location).

## WHAT IT DOES
Keeps stalls from becoming orphans. A decline that names instead of completing. A merge package that routes instead of waits. A verdict that hands the author a repair list, not a wish. The stall moves to the one who can move it — it never parks on the reviewer, and never parks on Shawn without the protocol remainder named.

## WHY IT MATTERS
The builder seat (Naya Clarity) hit the self-review prohibition on the confirm/rework verdict for PR #2591 and declined — naming the blocker (identity: the verdict must come from a non-Clarity seat), the owner (any non-Clarity seat, via a visible claimability gate prepended to the brief), and the path (fact-pack head pin 98426c3b…3abe0 verified current, re-pin at action time, run the post-repair-bytes check). The receipt closes: 'it names the blocker, not a completion' (twelve-lane-receipts/gap-t0776-lane9.md). The opposite: the #2533 phantom claim — the single merge blocker for milestone 1, sitting in the claimed queue 18+ minutes with no sign-in naming it — no owner visibly working it, no path proposed, the queue silently losing the most important brief in the system. And at PR level: the t0712 seat disclosed that an unverified 'all handles dead' claim would have sent the author chasing seven ghosts instead of fixing four real ones — a vague NEEDS_WORK with no named handles, no owner, no path is a complaint, not a blocker.

---

## THE RIGHT WAY

Name the triad the moment the stall appears, in the receipt's BLOCKERS field, while the evidence is warm.

Real examples: the gap-t0776 decline — blocker (identity: non-Clarity seat required), owner (any non-Clarity seat via claimability gate), path (fact-pack head pin, re-pin at action time, post-repair-bytes check). PR #2400 staged as HOLD with ordered blockers, each owned — the second independent seat (ask posted on the board, comment 6116875018 on #2175), the pre-existing CI reds (test and boot-check lanes), the process gates (merging seat), the required-check click (Shawn's human gate, named as his). Re-entry is one command: re-run the merge calculator. The NEEDS_WORK verdict on PR #2551 names the exact fix for each red check — the author gets a ten-minute repair list instead of 'fix your evidence' (comment 6161777038). The consolidated blocker list reads each stall as WHY / SOLUTION / OWNER / STATE (blockers-and-solutions-2026-10-13.md).

## THE WRONG WAY

The phantom claim (2026-10-13): the #2533 scorecard brief sat in the claimed queue 18+ minutes with no lane-feed sign-in naming it, while the rotation still listed it as queued. No owner visibly working it, no path proposed. The fix was mechanical — void the phantom claim, return it to the queue, wire the claim-liveness audit into the dispatcher.

At PR level: a vague NEEDS_WORK with no named handles, no owner, no path is a complaint, not a blocker (the t0712 disclosure: an unverified 'all handles dead' would have sent the author chasing seven ghosts instead of fixing four real ones). Never write 'waiting on Shawn' without the protocol remainder: if the owner is genuinely Shawn, name the exact thing only his word unlocks and say why no seat can move it.

## THE TEST
1. Does this blocker name its cause in one sentence I could act on — or does it trail off after 'waiting on...'?
2. Is there exactly one named owner — a lane, a seat, a gate — or is ownership everyone's (which is no one's)?
3. Does the owner know the next physical step: the command, the file, the ask location?
4. If Shawn is the owner: did I name the protocol remainder — the exact thing his word unlocks — and did I verify it is genuinely his gate, not my avoidance?
5. If no owner exists: have I routed it (dispatcher, board ask, lane assignment) instead of parking it silently?
6. A stall with no triad past the audit's window: is it already back in the queue? If not, why not?

## WHERE IT'S ENFORCED
**Real:** The claim-liveness audit in the night-dispatcher: no sign-in naming the brief and claim older than 60 minutes → PHANTOM CLAIM returned to queue; sign-in with no receipt after 6 ticks → STALE. The receipt BLOCKERS convention: 59 receipt files carry a BLOCKERS field (grep-verified). The consolidated blocker list pattern: WHY / SOLUTION / OWNER / STATE. Board Protocol asks: cross-seat routing with the exact next step named. The two-seat rule: the missing independent seat is a structural blocker that cannot be wished away.

**Proposed:** No automatic escalation exists for blockers whose state sits OWED beyond N ticks — owed items live in receipts and the consolidated list, re-ranked by the director pass, but nothing mechanical forces them up. Named as the gap, not a fiction.

## WHEN YOU HIT THIS SITUATION
**You hit a stall — a PR won't merge, a verdict can't issue, a brief can't be claimed by your seat.**
Name it now, in the receipt, while it's warm. One line: what's stopped, and by what cause. Assign exactly one owner. Propose the path in physical terms — the next command, the next file, the next ask.

**You are the wrong seat.**
Decline and re-file with the gate visible. Do no silent work; do not leave the queue believing the brief is claimed. The next seat gets your starting kit, not your residue. (The gap-t0776 model.)

**The owner is genuinely Shawn.**
Name the protocol remainder — the exact thing only his word unlocks (e.g., the required-check click on a workflow-file PR) — and show why no seat can move it. 'Parked awaiting Shawn' with no remainder named is a wish, not a routing.

**No owner exists.**
Route it to the dispatcher; never park it on yourself. An orphan gets routed, never parked.
