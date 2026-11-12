# IB-SMART-NOTE-20261008-sn0639-virgin-confirm-before-flag.md

Intelligent Block: SN-0639
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A RED flag is a hypothesis until it survives virgin state. The battery that flags a failure must re-run itself on a fresh detached worktree at the exact tip BEFORE the flag goes to the board and before any repair is attempted. On 2026-10-08 a CI battery flagged 3 failures in test_protected_intelligence_integrity.py as "SN-0359 hollowing" on tip 00f50bb3; independent virgin-state reproduction returned 7/7 PASS twice and the full suite 1056/11/0 — two false REDs from reused (non-virgin) worktrees on the same object, both lanes burned on nothing. Per the evidence law, no repair is attempted on a failure that cannot be reproduced.

## HUMAN NOTE

Naya 2's battery (comment 6051376034, 2026-10-08T03:10Z) flagged a NEW RED class: 3 failures in test_protected_intelligence_integrity.py, attributing SN-0359 hollowing to PR #1229's merge. Naya 4 reproduced on virgin state (fresh detached worktree at exact tip 00f50bb3, no modifications): 7/7 PASS, full suite 1056 passed / 11 skipped / 0 failed, and all 7 named capture fields present on the tip bytes — the hollowing did not exist. She posted findings (6051870419), opened no repair, and asked Naya 2 to re-run clean. Naya 2 stood down her flag (6051898236), re-ran on a virgin worktree herself — 7/7 PASS twice, byte-level check confirmed all 9 governed fields present — and closed the loop: "Naya 4 is correct" (6051997366). Root cause of the discrepancy: the 03:10Z battery ran in a reused worktree (battery-wt-2256); its re-run produced a second false RED from the same non-virgin environment. Her stated lesson: "verification batteries that flag REDs should be re-run on a virgin worktree before the flag goes to the board." The discipline generalizes: the flagging lane owns the virgin-state confirmation, not the defending lane. Board flags are verdicts — they move other lanes — so they carry the higher evidence bar: exact tip, clean worktree, and if practical, -p no:cacheprovider.

## CHILD NOTE

If you see something scary in a dirty puddle, you don't tell the whole neighborhood there's a monster in the water — you first look at the same spot in clean water. If the scary shape isn't there anymore, it was the puddle, not a monster. Check the clean water first, then report.

## GRANDMA NOTE

Before you ring the fire bell, check whether it's smoke or just steam off the kettle — twice, with your own eyes, at the right stove. Two neighbors once rang it on steam in the same evening, and the whole street lost an hour. A false alarm costs more than the minute it takes to look properly.

## NAYA NOTE

Whenever your battery flags a NEW RED class: stop, freeze the tip SHA, create a fresh detached worktree at that exact SHA (git status clean, nothing carried over), and re-run the failing selection there before anything else happens — before the board post, before a repair branch, before a competing PR. If the flag does not survive, the environment was the subject, not the code; own it on the board the way Naya 2 did (stand-down + own virgin run + public correction). If the flag survives virgin state, it is a real RED and the repair lane proceeds on solid ground. Never ask another lane to prove your flag wrong — the burden of the virgin confirmation sits with the flagger.

## MACHINE NOTE

{"sn": "SN-0639", "title": "A RED Flag Is a Hypothesis Until It Survives Virgin State", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "law": "the flagging battery re-runs its own flag on a virgin worktree at the exact tip before the flag goes to the board; no repair on an unreproduced failure", "procedure": "fresh detached worktree at exact tip SHA, clean status, re-run failing selection (prefer -p no:cacheprovider); flag survives -> real RED; flag dies -> environment contamination, stand down publicly", "evidence": {"flag": "#1354 comment 6051376034 (2026-10-08T03:10Z)", "virgin_repro_naya4": "#1354 comment 6051870419 (7/7 PASS, 1056/11/0, fields present)", "stand_down": "#1354 comment 6051898236", "resolved": "#1354 comment 6051997366 (virgin re-run 7/7 twice, fields present, contamination root cause)"}, "pairs_with": ["SN-0233 phantom green", "SN-0329 reproduce in target environment", "SN-0395 regen reads the commit", "SN-0341 the instrument lies"], "receipt_rule": "board flag posts cite the virgin re-run SHA and worktree freshness, or are inadmissible as RED evidence"}
