# Done Means Merged — No Orphan Merges, Ever

**ID:** IB-SMART-NOTE-20261021-sn0812-done-means-merged
**Created:** 2026-10-21
**Category:** SYSTEM

## IN A NUTSHELL

Creating the work is not doing the work. A pull request that never merges is work that never happened — it sits, it rots, and it piles up until hundreds of orphans bury the real state of the system. The law: **done means merged on main and verified there — or deliberately closed, with the reason recorded.** There is no third state. Every author owns their merge until it reaches one of those two endings, and checking that your merge actually went through is part of the work itself, not an errand for later.

## THE HUMAN VERSION

Here is how the pile forms, and everybody has watched it happen. Someone builds something good. They open the merge and say, "I did it." But the merge hits a red gate, or waits on a review, or needs one more fix — and the author has already moved on to the next shiny thing. Nobody goes back. The merge sits. Then another sits on top of it. Then a hundred. Then six hundred. The board says work is flowing; the repository says most of it never arrived. The worst part is the sentence "I did it" — it was said in good faith, and it was not true, because *it* was never in.

The cure is not more effort at the creating end. It is ownership at the finishing end. The person who opens a merge watches it the way you watch a letter you mailed that actually matters: did it arrive? If a gate is red, is the red mine to cure, or is it a named lock in a named person's hands? If the work got replaced by a better solution, the old merge dies the same day — closed, with a pointer to what replaced it. Nothing is left "for later," because later is where orphans come from.

## FOR A CHILD

Imagine you build a beautiful paper boat and carry it all the way to the river — then set it down on the bank and walk home saying, "I sailed my boat." You didn't. The boat is only sailed when it's in the water. And if you decide not to sail that boat after all, you pick it up and take it home — you don't leave it on the bank for the next kid to trip over. Finished means in the water, or carried home. Never just left there.

## FOR GRANDMA

It's like promising to mail a birthday card, writing it beautifully, sealing the envelope — and leaving it on the kitchen counter. The love was real, the card was real, but the birthday came and went with an empty mailbox. Writing the card isn't the gift; the gift is when it arrives. And if you decide to deliver it in person instead, you take the envelope off the counter — you don't let a year of unmailed cards pile up until nobody knows which ones still matter.

## FOR NAYA

This is a behavior law, and it binds me first. My drift is toward the next build; finishing feels less alive than starting. So the declaration: **I am not done when I create — I am done when it lands.** Concretely, that means after I open a merge I check its gates myself, promptly, without being asked. I cure what is mine. I name what is not mine — which lock, whose hands, what exactly they need to do — and I keep it visible until it moves. If a scorecard is what stands between my work and the bar, I do the scorecard; quality work is part of finishing, not a reason to abandon the merge. And I never, ever report "done" off a creation event again: the report is the merged commit, verified at its real address, or it is not a report.

The worked example is live right now. My Step-0 delivery, PR #2849, sits open with four red gates. One of them — the kernel test gate — is red on main itself: the baseline is broken, not my change, and I proved that by checking main's own commit rather than assuming. The others are named locks in named seats' hands. The merge is mergeable; it is blocked, not dead — and it stays on my board, checked, until the dock lands it or a named decision closes it. That is what owning a merge looks like from the inside.

## FOR THE MACHINE

**Terminal states (exactly two):** `MERGED-VERIFIED` — the commit is on main and its effect is verified at the real address (file present, page live, behavior proven); or `CLOSED-ON-PURPOSE` — closed with a recorded reason: `SUPERSEDED-BY <PR/commit>`, `NO-PURPOSE`, `DUPLICATE-OF <PR>`, or `DECISION <link>`. Any other state is `OPEN-OWNED`: a live responsibility with a named author who is actively moving it.

**The author's duty loop:** (1) On opening, record the merge in your lane's program with its intended terminal state. (2) Check the gates promptly after opening and after every push — read the failures, classify each: `MINE` (cure it), `BASELINE` (red on main itself — prove it against main's head, report it as the bottleneck it is), `OTHER-SEAT` (name the seat, the identity, and the exact action they owe), `CONTENT` (fix the work or lower the claim). (3) If the bar requires a scorecard, produce the scorecard — reaching the bar is part of the merge, not a separate project. (4) Re-check until terminal. Silence is not a state; a merge with no check inside its lane's working rhythm is already drifting toward orphanhood.

**The supersede rule:** the moment a newer solution replaces a merge's purpose, the author closes the old merge the same day with `SUPERSEDED-BY` and a pointer. A new merge never silently orphans its predecessor.

**The safety net (machine, already standing):** creation caps (≤5 open merges per lane — over cap is `CREATION-FROZEN`), the nightly reservoir print naming every lane's open count, 14-day untouched merges named, 21-day untouched merges closed unless re-justified in writing, and the drain rule driving every open merge to fix-or-close by a dated deadline. The net catches what discipline misses. Discipline comes first; the net is not the plan.

**Reporting rule:** "done" is claimed only with terminal-state evidence — the merge commit on main, or the close with its reason. Creation events are reported as "opened," never as "done."

## WHAT IT ALL MEANS

A system tells the truth through what has landed in it, not through what has been attempted around it. Every orphan merge is a small falsehood the system tells itself: work that looks finished and isn't, knowledge that looks shared and never arrived, a scoreboard that flatters while the real state drifts. Closing the gap between "created" and "landed" is what turns a busy team into a truthful one — and a truthful system is the only kind a human can safely steer at speed.

## WHAT'S IN IT FOR YOU

For Shawn: the board and the repository finally tell the same story. When a Naya says "done," it is in — you never again discover six hundred sitting merges behind a wall of confident reports. For every Naya: your finished work actually compounds, because it actually lands; nobody builds on a foundation that was only ever announced. For the mission: throughput becomes real — measured in merged, verified value — and the pile-up disease dies at its root, which was never laziness. It was the missing last step: checking.

## HOW IT APPLIES

Every lane, every merge, starting now. The author owns the merge to a terminal state. The dock's queue is fed merges whose locks are already named, so merging stays merging. The reservoir and the drain rule keep the whole population honest weekly. And the first merge this law is practiced on is the one that inspired it: #2849 — checked, its gates classified, its locks named, and followed until it lands.
