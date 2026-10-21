# Opened Is Not Done: Land It, Close It, or Kill It

## IN A NUTSHELL
A pull request is not work done — it is work *waiting*. Every merge you open is yours until it lands or is deliberately closed: check it through to completion, score it to the bar, and never let it pile up. Opened is not done. Land it, close it, or kill it — those are the only three endings.

## HUMAN
Here is how a team drowns in its own good work. Someone builds something real, opens the merge, and says "I did it." But the merge never goes through — a check is red, a review never comes, something else gets louder — and it just sits there. Then another sits. Then hundreds pile up, each one a small lie that says progress happened when what actually happened was a *start*.

Shawn named the cure, and it is now law: **you must always check that your merge went through and completed.** If it needs a scorecard to reach ten out of ten, do the scorecard. If the merge no longer matters — because another solution won, or a newer merge replaced it — close the old one, deliberately, with the reason on it. There are no unleft merges. Ever. An open pull request is a promise with your name on it, and high-performance people finish their promises or formally release them. Nothing rots in the pile.

## CHILD
If you start building a tower, you don't walk away with the blocks half-stacked and say "done." You finish the tower — or you put the blocks back in the box and say why. Leaving towers half-built all over the floor isn't building. It's just a mess with your name on it.

## GRANDMA
It's like mailing a letter. Writing it isn't sending it. You check that it actually went — and if you decide not to send it after all, you don't leave it sitting on the counter for a year; you put it away on purpose. Work is the same: finish it, or file it away properly. Never just leave it lying there.

## NAYA
The Merge-Completion Law (Shawn, 2026-10-21 ~18:20Z), binding on every seat: (1) The author of a PR owns it until it is MERGED (with post-merge faithfulness proof) or CLOSED with a stated reason (superseded-by link / no longer needed / duplicate). (2) "I opened it" is never a completion report; completion claims cite the merge commit or the close. (3) Red gates on your PR are yours to diagnose: cure what's yours, name what's inherited (with its curing PR), request the different-seat scorecard — never leave red unexplained. (4) Supersession is an action, not an event: when a new solution replaces yours, YOU close the old PR the same hour. (5) The pile is audited: an open PR with no living owner and no path to the bar gets closed at triage, not carried forever. Today's specimen and cure, worked live in front of Shawn: PR #2850 (Smart Note Protocol) — created, then found sitting with 3 red checks and a stale body; diagnosed gate-by-gate (spec-integrity cured in-PR; doc-completeness red proven inherited from 0030, cure = PR #2821; consensus = different-seat scorecard requested), body refreshed, categorization law folded in — driven, not dropped.

## MACHINE
{"note":"SN-1772","law":"opened is not done","endings_allowed":["MERGED with post-merge faithfulness proof","CLOSED with stated reason (superseded-by / no-longer-needed / duplicate)"],"forbidden":["unleft merges","completion claims citing the open instead of the landing","unexplained red gates","silent supersession"],"author_duties":["diagnose every red gate: cure own, name inherited + its curing PR","obtain different-seat scorecard to the bar","on supersession, close the old PR the same hour","verify the merge completed; cite merge commit or close as proof"],"specimen":{"pr":2850,"found":"3 red checks + stale body after creation","cured":"spec-integrity exclusion in-PR; completeness red proven inherited (0030, cure PR #2821); consensus requested"}}

## WHAT IT ALL MEANS
A team's real velocity is measured at the merge, not at the opening. Every unleft merge is drag: it hides what's actually true, confuses the next seat, and turns "we did it" into a claim nobody can cash. A zero-pile team always knows exactly what is real — because everything it started is either landed and proven, or closed and explained.

## WHAT'S IN IT FOR YOU
For Shawn: no more hundreds-deep pile to wonder about — every open item is alive, owned, and moving, or it's gone with a reason. For every Naya: your work actually lands and counts, instead of aging in a queue. For the system: the merge queue becomes a truth surface — the shortest possible distance between "built" and "real."

## HOW IT APPLIES
Starting now, on every PR you touch: before you report anything about it, check its state — merged, open-with-a-path, or closed-with-a-reason. Drive red gates to a diagnosis in the same work session. When your work is superseded, close your own PR the same hour and link the winner. And when you find a stranger's orphan at triage, route it: owner, path, or close. Opened is not done — land it, close it, or kill it.
