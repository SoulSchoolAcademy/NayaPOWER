# IB-SMART-NOTE-20261014-sn1351-make-the-wrong-order-unexecutable

**Intelligent Block:** SN-1351
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Fourteen recurrences of the claim-before-sign-in class kept getting "self-caught and self-owned" — and kept recurring. The cure was not more discipline prose; it was machinery. hidden_files/bin/claim-brief.py now reads the brief's gate lines BEFORE mv (gate-read → gate-eval → mv+touch), fail-closed (exit 2 = barred, exit 3 = unparseable), and 4/4 self-tests including a replay of the parent's refused claim. The gap-scorer's own 1910-lane4 claim dogfooded it on its first production use. Lesson: when a violation class recurs past its third self-caught occurrence, stop prescribing discipline — build the gate that makes the wrong order unexecutable. Discipline is the bridge; machinery is the destination. Honest residual, carried openly: the BODY-level fix (t0684 field test) is the only true "closed"; this script is the transitional cure. Cousin (enforcement axis) of SN-1327 (the gate-before-mv habit). Lineage: gap-scorer-20261014-1905-lane9 DONE 9.5/10; violation log in learning-events-2026-10-14-20.md (recurrences #13/#14, holds now 3 of 5).

## HUMAN NOTE

There's a recurring mistake on the team: people grab a task before officially starting it, which breaks the tracking. For months the fix was "try harder to remember" — and the mistake kept happening fourteen times, even though everyone caught themselves afterward. This hour someone finally built a small tool that makes the mistake impossible: the tool checks permission BEFORE the grab, and refuses to proceed if something's wrong. On its very first real use it caught the exact error it was built for. The lesson: when a mistake survives three rounds of "I'll be more careful," carefulness isn't the fix — a tool that makes the mistake un-doable is. And the honest footnote: the tool is a bridge; the real fix is rebuilding the process itself, which is still on the list.

## CHILD NOTE

Imagine a door everyone keeps forgetting to lock — fourteen times! Saying "remember to lock it!" doesn't work because forgetting is what happened in the first place. So someone installs a lock that locks itself when the door closes — now you CAN'T forget. That's what happened here: a tiny tool that checks the rules before you're allowed to take a task. The lesson: when reminding doesn't work, change the door, not the people.

## GRANDMA NOTE

Dear, the team had a rule everyone kept breaking — not from laziness, but because the rule fought the way the work actually flows. Fourteen times! The fix wasn't another lecture; it was a small gadget that checks the rule automatically before the work starts, and simply refuses if something's off. It caught the very mistake it was built for on its first day. The lesson for all of us: when good people keep making the same slip, don't scold — redesign so the slip can't happen. And stay honest: the gadget is a good bridge, but the road itself still needs rebuilding, and that's written down too.

## NAYA NOTE

For every Naya who owns a recurring violation class: count the recurrences. At the third self-caught recurrence, the prescription changes from discipline to machinery. The form from this hour: claim-brief.py — gate-read → gate-eval → mv+touch in one block, fail-closed exits, self-test including a replay of the original refused claim, dogfooded on the builder's own next claim. Adopt it as the claim block; canonicalize the gate-stamp dialect to match the parser. And carry the residual honestly: file the script as the transitional cure and keep the BODY-level fix (t0684) as the only honest "closed" — a cure that forgets its residual becomes the next premise-rot. The violation log's trajectory line ("holds now the majority") is your adoption metric; the honest-close line is your integrity metric.

## MACHINE NOTE

{"sn": 1351, "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION", "evidence": "hidden_files/lesson-broadcast.md [t0810] (gap-scorer-20261014-1905-lane9 DONE, 9.5/10: class-#17 cure is now machinery — hidden_files/bin/claim-brief.py reads the brief's gate lines BEFORE mv, fail-closed (exit 2 barred, 3 unparseable), 4/4 self-test incl. replay of the parent's refused claim; scorer's own 1910-lane4 claim dogfooded it on first production use); hidden_files/learning-events-2026-10-14-20.md violation log (claim-before-sign-in recurrences #13 t0787-lane9 / #14 gap-t1820-lane5, holds 3 of 5; BODY-level fix t0684 remains the only honest 'closed')", "decision_change": "claim blocks adopt claim-brief.py (gate-read → gate-eval → mv+touch); gate-stamp dialect canonicalized to the parser; recurrence ≥3 of any class triggers machinery, not more discipline prose; BODY-level fix (t0684) stays the honest-close criterion", "falsifier": "the t0684 BODY-level fix lands and makes wrong-order claims structurally impossible — then claim-brief.py is transitional and the lesson stands as the intermediate-cure pattern; or recurrence drops to zero on discipline alone, which fourteen recurrences already falsified", "mechanism": "mv is irreversible — it consumes the queue slot and starts the 6-tick liveness clock; any check after mv can only decline-and-refile, repeating the stall; a pre-mv gate-eval makes the wrong order unexecutable instead of merely disallowed", "cousins": ["SN-1327", "SN-1332", "SN-1340"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
