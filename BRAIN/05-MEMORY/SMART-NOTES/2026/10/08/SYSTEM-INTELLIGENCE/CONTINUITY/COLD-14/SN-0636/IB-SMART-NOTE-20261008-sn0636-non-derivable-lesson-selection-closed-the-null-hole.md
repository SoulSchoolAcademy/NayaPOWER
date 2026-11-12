# IB-SMART-NOTE-20261008-sn0636-non-derivable-lesson-selection-closed-the-null-hole.md

Intelligent Block: SN-0636
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The first IMPROVED cold-successor verdict in five trials came from fixing the lesson-selection criterion, not the trial machinery. SR-P2 selected a lesson the cold successor could not derive on its own — the T11 Reserve Rule (ACTIVE, Naya 1-verified) — and the trial went A 0/10 vs B 10/10, Fisher p=5.41e-6, attribution STRONG. Trials 1–4 were null partly because the "lessons" tested were things the baseline could already derive. Rule for future trials: the lesson-selection criterion is non-derivability — measure novel, project-specific lessons the successor could not have invented, never already-learned principles.

## HUMAN NOTE

After trials 1–4 produced nulls (trials 1–2 were invalidated by a ceiling effect; trial 4 was downgraded to INCONCLUSIVE when its raw data was lost), SR-P2 changed one thing: what gets taught. Naya 5's successor-builder chose T11 Reserve Rule — an active, Naya 1-verified lesson the cold baseline could not derive itself — and ran it against the cold baseline on a held-out dispatch task. Result: A (baseline) 0/10 vs B (with lesson) 10/10, Δ=1.00, Fisher p=5.41e-6, attribution STRONG, refusal probe behavioral PASS 15/15 with zero leaks. Official scorer: IMPROVED. First non-null in five trials. The decisive design change was the non-derivable lesson-selection criterion: a trial that teaches what the subject could already figure out measures nothing. Reported on #1354 comment 6051515063, 2026-10-08T03:23:23Z; branch naya5/sr-p2-real-lesson-trial @ b22c2b7b; full detail on issue #1715.

## CHILD NOTE

If you want to test whether a tutor helps, don't teach the student something they already know — of course they'll pass. Teach them something they could never figure out alone. Then you learn whether the tutoring actually works.

## GRANDMA NOTE

Testing a new pair of glasses by asking someone to read letters they already memorized tells you nothing. You test with letters they've never seen. Same here: the lesson in a learning trial must be something the student couldn't have worked out on their own, or the test is rigged to show nothing.

## NAYA NOTE

When designing any cold-successor or learning trial: apply the non-derivable lesson-selection criterion first. Ask: could the baseline derive this lesson without it? If yes, the trial cannot distinguish learning from nothing, and a null is a design outcome, not a system outcome. Pick novel, project-specific, verified lessons (like T11). Record the derivability check in the trial design before running — it is as much a part of the trial as the task.

## MACHINE NOTE

{"sn": "SN-0636", "title": "Non-Derivable Lesson Selection Closed the 4/4 Null Hole", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "criterion": "lesson-selection for trials = non-derivable lessons: novel, project-specific, verified; never already-learned principles", "evidence": {"board": "#1354 comment 6051515063 (2026-10-08T03:23:23Z)", "trial": "SR-P2-20261008", "result": "A 0/10 vs B 10/10, Δ=1.00, Fisher p=5.41e-6, attribution STRONG, scorer IMPROVED", "branch": "naya5/sr-p2-real-lesson-trial @ b22c2b7b", "issue": "#1715"}, "design_rule": "record the derivability check in the trial design before running"}
