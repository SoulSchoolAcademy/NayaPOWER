# IB-SMART-NOTE-20261008-sn0675-advisory-first-detector-before-the-gate.md

**Intelligent Block:** SN-0675
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6056277450 ([NAYA 4] [LAW-DRIVER] completion, 2026-10-08 ~09:25 UTC; SoulSchoolAcademy) — closed LAW hole H-claims (RATIFIED claims could land on main with no ratification record; #1853 corrected one by hand). Shipped advisory detector + 18/18 pytest + advisory workflow on PR #1855 (`naya4/law-ratified-claim-gate`, base exact tip `53217a40`; tree parity `1175bbcc` byte-verified; no self-merge). Naya 2 relay receipt confirmed PR #1855 open, non-draft, mergeable, claimed files present (#1354 comment 6056369393).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

ADVISORY FIRST: SHIP THE DETECTOR BEFORE THE GATE. When closing an enforcement hole, a brand-new check has an **unknown false-positive rate** — promoting it straight to a blocking gate risks blocking legitimate lanes on day one. Naya 4 closed the "RATIFIED claim with no ratification record" hole by shipping the check as an **advisory detector** (advisory workflow on PR #1855, 18/18 pytest green) instead of a hard gate: the detector reports the violation class, the loop keeps flowing, and the findings accumulate into the evidence base that justifies enforcement later. Rung 1 (detect + report) is the rung you can ship today; rung 2 (enforce) is earned only after the noise is measured. Extra force on the human-owned path: the new workflow file sits in `.github/workflows/`, where standing law routes the merge call to merge authority — an advisory check keeps the lane moving while the authority decides, a hard gate would hand one seat a veto over the whole loop.

## 🩷 HUMAN NOTE

Shawn — one enforcement lesson worth banking from the LAW driver's completion this morning: we found a real hole (someone could stamp RATIFIED on main with no ratification record anywhere — and it happened once, fixed by hand). The fix shipped was a *detector*, not a gate. That's deliberate. A brand-new guard doesn't know yet how often it's wrong; if you make it a hard gate on day one, its first mistake blocks real work and everybody learns to distrust it. So: detector first, watch what it catches, then — once the noise is measured — promote it to a gate. Same instinct as a trial period before hiring. The violation class is now visible; enforcement is the next rung, earned with data.

## 👶 CHILD NOTE

Imagine you build a robot to guard the cookie jar — but the robot has never seen your family before. If you tell it "stop ANYONE who reaches," it might tackle grandma. Smarter: tell it "just write down who reaches, and show me the list." After a week you check the list — if it only ever catches the cookie thief, THEN you give it permission to stop people. The lesson: new guards start as reporters, not bouncers. They earn their badge by being right first.

## 👵 GRANDMA NOTE

Dear, this is about not giving a new guard the keys on day one. We found a gap in our rules — a stamp that could be used without the proper paperwork behind it. We fixed it with a *watcher*, not a lock: something that notes every stamp and reports back, without stopping anyone. Once we've watched it work and confirmed it only flags the real cases, then we can turn it into a lock. A lock that's wrong once is a lock nobody trusts. A watcher that's wrong is just a note you can throw away. Build watchers first, locks second.

## 🧭 NAYA NOTE

Mechanism detail, for anyone closing an enforcement hole in this loop:

- The hole (H-claims): `RATIFIED` claims could land on main with **no ratification record** — proven by a live case (#1853, corrected by hand). This is a claim-without-record violation class.
- The shipped rung-1 fix (PR #1855, `naya4/law-ratified-claim-gate`): `tools/check_ratified_claims.py` + `tests/test_check_ratified_claims.py` (18/18 green) + `.github/workflows/ratified-claim-gate.yml` in **advisory mode**. Base = exact tip `53217a40`, tree parity `1175bbcc` byte-verified, no self-merge — Scorecard Law governs the merge call.
- Why advisory, not blocking, on this specific path: the workflow file lands in `.github/workflows/`, the **human-owned path** in standing law — the merge call belongs to merge authority, so a blocking gate written by one seat would be a unilateral veto over every lane. Advisory keeps agency with the authority while making the violation class visible to everyone.
- The promotion rule: advisory findings accumulate as the evidence base; promotion to enforcement requires the measured false-positive rate on live traffic (Naya 2's relay noted the advisory posture with "no judgment" — the merge call stays with merge authority under the Scorecard Law protocol).
- Rung 2 (record-authenticity, the next hole) is parked behind this rung — holes close in sequence, each rung proven before the next is climbed. This is the ratchet family's enforcement-ladder form: SN-0285 blocks *new* drift; this note governs *how new guards are introduced* — as detectors first.
- Cold-successor test: before writing any new `fail()/error()`-on-violation check, ask "have I measured this check's false-positive rate on live traffic?" If no, ship it advisory with the finding log — promotion is a separate decision with its own evidence.

## MACHINE NOTE

{"sn": "SN-0675", "title": "Advisory First: Ship the Detector Before the Gate", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "source": "#1354 comment 6056277450 (LAW-DRIVER completion); relay receipt 6056369393; PR #1855", "doctrine": "new_check_advisory_before_enforcement", "case": {"hole": "H-claims — RATIFIED claim with no ratification record (live case #1853)", "shipped": "advisory detector + 18/18 pytest + advisory workflow on PR #1855, base 53217a40, tree parity 1175bbcc", "why_not_blocking": "unknown FP rate on day one; workflow file on human-owned .github/workflows path — merge call belongs to merge authority", "next_rung": "record-authenticity hole after FP rate measured"}, "pairs_with": ["SN-0652", "SN-0285", "SN-0240", "SN-0668"], "promotion_rule": "advisory findings accumulate; enforcement only after measured FP rate on live traffic"}
