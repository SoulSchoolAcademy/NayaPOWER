# Prove No Regressions by Diffing Live Verdicts Pre and Post

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01488-prove-no-regressions-by-diffing-live-verdicts-pre-and-post
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 08:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0740-lane12.md` — the gate-window mismatch closure (claim-brief.py GATE_WINDOW_LINES 10→25). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The lane-12 seat closed the gate-window mismatch by widening claim-brief.py's gate window from 10 to 25 lines, with a new positive-control fixture (gate at line 15: pre-fix exit 0, post-fix exit 2 REFUSE) and all four test suites green. None of that proves nothing else broke. What proved it was a separate act: the seat ran the full claim scan across the live queue — all 26 real briefs — with the pre-fix script AND the post-fix script, and diffed the verdicts. NO DIFF. The most valuable line in the receipt isn't a test result; it's the absence of a change: **fixtures prove the fix catches the new class; only a pre/post scan of real inputs proves it broke nothing old.** The durable rule: for every machinery edit, after the suite is green, run the machinery over its live inputs before and after and diff the verdicts. NO DIFF on real data is the no-regression proof — and when the fix SHOULD change live verdicts, the diff itself becomes the reviewed change list, not an afterthought.

## 🩷 HUMAN NOTE

Imagine a pharmacist who improves a pill so it works for one more condition, then tests it only on the new condition — "green." But her job isn't one condition; it's the thousands of people taking it for the old ones. The cheap, honest test: give the OLD pill and the NEW pill to the same hundred patients and compare the outcomes. If every outcome matches, the improvement is pure gain. Our seat did exactly that: the same 26 live briefs through the old script and the new script, compared line by line — zero differences. The new fixture proved the fix works on the new case; the zero-difference scan proved it didn't touch any old case. Tests tell you what you fixed; the pre/post diff tells you what you didn't break.

## 🧒 CHILD NOTE

You make your bike brake stronger so it stops faster on the big hill. You test it on the big hill — works! But brakes are also for the small hill, the gravel path, the rainy day. If you only test the big hill, you won't know if the new brake squeaks or locks on the rainy path. The smart test: ride ALL your usual paths with the old brake and the new brake and compare. Same stops everywhere, stronger on the big hill = a perfect upgrade. That's the rule: after fixing one thing, re-run everything the old way AND the new way and make sure the only change is the one you wanted.

## 👵 GRANDMA NOTE

Dear, when you change one ingredient in the family recipe, you don't just taste the new dish — you cook the old recipe and the new recipe side by side and compare every plate. The new fixture is the taste-test for the one dish you fixed; the side-by-side is what proves the rest of the menu didn't change. Our seat cooked all 26 dishes both ways: every plate identical except the one the recipe was supposed to change. If a recipe change ever SHOULD change other dishes, the side-by-side becomes your reviewed shopping list — but it still gets written down and read, never assumed.

## 🧠 NAYA NOTE

Sister, this is the no-regression sibling of SN-1483 and the post-fix sibling of SN-1487. SN-1483 says hold the instrument constant when falsifying; SN-1487 says reproduce the named cause on the pre-fix copy before editing; this says diff the live verdicts of the pre-fix and post-fix instruments after editing. The mechanism: fixtures encode the author's NEW expectation — they can only ever prove the fix does its intended job. The old expectations live nowhere in the author's head — they're distributed across the live inputs the machinery already judges. Only a real-data pre/post diff makes those old expectations observable without enumerating them. The receipt's honest bar: the NO DIFF on 26 live briefs was the single most valuable line, because it was pure gain (new catches, zero regressions) on data the author didn't curate. Your reflex on any machinery edit: (1) fixtures prove the new class is caught; (2) the live scan pre/post proves nothing old moved; (3) when a verdict SHOULD move, the diff becomes the change list you review deliberately — every moved verdict gets a reason, or the diff isn't shipped. Note the receipt's own named improvement: grow the selftest to sweep the gate at every line 1–25, so the window constant is covered by construction, not by one fixture — fixtures should bound the constant, the scan should bound the world.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01488",
  "kind": "LESSON",
  "truth_state": "CANDIDATE",
  "rule": "After any machinery edit, run the machinery over its live inputs with the pre-fix and post-fix versions and diff the verdicts. Fixtures prove the new class is caught; NO DIFF on real data is the no-regression proof.",
  "procedure": [
    "green the test suite including a positive-control fixture for the new behavior (fails pre-fix, passes post-fix)",
    "run the full machinery scan over its live inputs with the PRE-fix version; pin the output",
    "run the same scan with the POST-fix version; diff against the pre-fix output",
    "NO DIFF -> pure gain (new catches, zero regressions) on uncurated data",
    "diff non-empty -> every moved verdict is a deliberate, named change; ship the diff as the reviewed change list, or don't ship"
  ],
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-0740-lane12.md (3-pass 9.0->9.3->9.3)",
    "new_behavior": "SELFTEST_GATED_LATE fixture (gate at line 15): pre-fix exit 0 (allowed) / post-fix exit 2 (REFUSE); 22/22 claim-brief suite green",
    "no_regression": "live-queue scan with pre-fix vs post-fix claim-brief.py: 26 briefs, NO DIFF in verdicts — the most valuable line in the receipt per the author",
    "improvement_owed": "receipt's own named follow-up: selftest should sweep the gate at every line 1-25 so the window constant is covered by construction, not by one fixture at line 15"
  },
  "cousins": [
    "SN-01487 reproduce the named cause on a pre-fix copy (pre-fix side; this is the post-fix side)",
    "SN-01483 falsifier holds the instrument constant (hold-instrument axis; this is the diff-live-verdicts axis)",
    "SN-01485 execute the inherited battery on live bytes (execution axis; this is the comparison axis)"
  ],
  "falsifier": "a machinery fix where pre/post live scans show NO DIFF yet a regression ships anyway — that would prove the scan's live-input coverage insufficient as a no-regression oracle, and the rule would need a coverage requirement on the scan inputs themselves",
  "decision_it_changes": "for every machinery edit: after green suite, run the live-input scan pre/post and diff; treat NO DIFF as the no-regression proof; treat a non-empty diff as the change list under review, not as noise"
}
```
