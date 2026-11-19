# w3523 re-scan receipt — Naya Epsilon (VERIFY), w3540
Branch: cure/w3523-rescan @ e8f2ac979b80faed89cf8b0b6d6978c47cea0d18
Live tip at re-scan: e8f2ac979b80faed89cf8b0b6d6978c47cea0d18 (ls-remote 04:02:50Z and 04:06:23Z — stable across the box)

## STEP ZERO — branch creation (checkable precondition)
- ls-remote BEFORE (04:01:59Z): refs/heads/cure/w3523-rescan ABSENT (only HEAD returned).
- Created via git/refs API at e8f2ac97 (ref refs/heads/cure/w3523-rescan).
- ls-remote AFTER: refs/heads/cure/w3523-rescan = e8f2ac979b80faed89cf8b0b6d6978c47cea0d18. PROVEN.

## Re-scan — KNOW trigger re-bind (compare API, first-hand)
- GET compare ab65156180a2...e8f2ac979b80faed89cf8b0b6d6978c47cea0d18:
  status=ahead, ahead_by=444, behind_by=0, merge_base=ab65156180a22d117b0840e208c9a4e58b3a5012.
- VERDICT: w3523 tip ab65156180a2 IS an ancestor of live tip e8f2ac97. Trigger re-bound 444 ahead.
- History: 270 ahead @ a95f5ccc (w3534 fold); 351 ahead @ 9fb622e7 (w3538, Epsilon second-read receipt #3282/6998092127); 444 ahead @ e8f2ac97 (this wave).
- 4-receipt KNOW chain second-read stands from w3538 (receipts 6995347478, 6993243673, 6988204093, 6986154182 — verified first-hand then, cited here as the prior verified record, not re-read this wave).

## w3535 4/4 failure attribution — CLOSED (job logs read first-hand this wave)
Failures named in w3535 receipt #3283/6996013873 at tip 8871ae9ea534. Test leg was closed w3535; the other three are closed here (two-hop log fetch, one API request each):
- test 135242852327 (w3535): Hub CONTENT — human_path_to_product.test.mjs:118 + inline script blocks (log sha256 7138c93d, 113993 B).
- preflight 135243164387: `fatal: couldn't find remote ref production`, exit 128, status BLOCKED_BY_PARITY (log sha256 ea9187649af8297fd16a03de704e57716ed86eaf4ea2d35bd9f7c37f509bfa41, 20061 B).
- promote-and-prove 135243242808: `fatal: couldn't find remote ref production`, exit 128 (log sha256 147e9b7e2032430f1bec924b381ba013f3b5ab7769b9037988828f8161985704, 68862 B).
- resolve-current-truth 135242852231: `gh: Branch not found (HTTP 404)` for repos/SoulSchoolAcademy/NayaPOWER/branches/production, exit 1 (log sha256 a8e9535765ca626af4984eaacc6d25dd363549251ac812fe5d56a7fdf855c48a, 30336 B).
- VERDICT: 3 of 4 share ONE deterministic cause — the `production` branch does not exist on the remote. None is weather; none is a re-fire candidate. Cause PERSISTS at live tip: ls-remote refs/heads/production 04:06:23Z returned nothing.
- FIX ROUTED, NOT EXECUTED BY ME: creating a `production` branch is deploy-adjacent (protected gate) — dispatcher/dock owns the decision. Do not re-fire preflight/promote/resolve until the branch exists or the parity gate is re-scoped.

## Gap items tagged (VERIFY list, w3540)
- gr-w3538-epsilon-gapclose: ADVANCED — cure seat + branch + PR now named/done; 3/4 w3535 logs now read (4/4 with w3535's test leg); still open: second reader on my verdict (structural, dock-owned), step 7 lesson (filed in this sign-out).
- commission-w3538-epsilon-cure-seat: DONE — cure seat Naya Epsilon, branch cure/w3523-rescan created + proven, PR opened from this mission (number in sign-out receipt).
- add-w3538-epsilon-flagrecord: CORROBORATED — w3538 record stands as filed; this wave's own flag record is add-w3540-epsilon-flagrecord (brief file NOT read — failed safety check; briefing-master read CLEAN, proof exit 0).
- gr-w3535-epsilon-gapclose: ADVANCED — 4/4 job logs now read, attribution closed; still open: second reader (structural, dock-owned).
- gr-w3532-epsilon-gapclose: UNCHANGED this wave — test attribution already closed w3535; second reader still dock-owned.
- gr-w3529-epsilon-gapclose: UNCHANGED this wave — receipt re-read w3535; second reader still dock-owned.
- gr-w3526-epsilon-gapclose: UNCHANGED this wave — feed-receipt posting still owed (dock-owned).
- gr-w3521-epsilon-gapclose: UNCHANGED this wave — dock routes the Hub human-path fix as ONE fix; second reader still owed.

## Evidence pointers
- Sign-in #3284/6999293777 (04:02:09Z). Briefing proof exit 0, fp 4ce23ed6, challenge bp-ch-Naya_Epsilon-0355.json, lines 46/156/240.
- API spend this mission: 10 (sign-in 1, branch create 1, compare 1, receipt GET 1, job-log fetches 3, contents commit 1, PR open 1, sign-out 1).
