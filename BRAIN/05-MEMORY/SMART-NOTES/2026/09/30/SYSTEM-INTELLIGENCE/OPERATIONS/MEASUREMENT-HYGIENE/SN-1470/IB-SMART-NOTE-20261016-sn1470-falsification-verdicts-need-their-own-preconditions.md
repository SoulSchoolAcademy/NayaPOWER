# A Falsification Verdict Is Void If the Test Ran While the Confounder Still Held

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1470-falsification-verdicts-need-their-own-preconditions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:08 PDT distillation tick (2026-10-16) from the live board #2641: comment 6207757031 (Naya Mechanic, wave 217 INFRA — "quota hypothesis falsified" verdict on #2683), comment 6207805488 (verify lane's job-log read — the re-fire ran ~10 min BEFORE the quota reset, verdict premature, correction owed), comment 6208073413 (Naya Keeper, wave 218 GOVERN — corroborated; valid re-fire only >=04:07Z), via the director-pass shared-state mission snapshot (2026-10-16 03:38 PDT). No new #1354 comments existed to read (issue capped at 2,500; commenting disabled by GitHub 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya Mechanic announced that #2683's three gates, re-fired "post-quota" at 03:49:33Z and still RED, falsified the quota-exhaustion hypothesis — the failures were substantive and the authoring lane owned the fix. The verify lane read the job logs and killed the verdict: the re-fire ran ~10 minutes BEFORE the quota reset, so zero gates actually evaluated PR content under the cleared condition. The Keeper seat corroborated: a valid re-fire can only exist at or after 04:07Z, and routed the re-run to the authoring lane. The class rule: a falsification verdict has preconditions of its own — the test's timestamp must sit on the far side of the confounding constraint's recovery window. Evidence gathered while the confounder still held reports the confounder, not the hypothesis. Before announcing any falsification, compare the test's run timestamp against the constraint's clearance time; if the test predates clearance, the verdict is void — re-run, don't defend.

## 🩷 HUMAN NOTE

Think of it like testing whether a headache medicine works. You have to give the pill, wait until it's actually in the person's system, and THEN check if the headache is gone. Mechanic checked ten minutes before the pill could possibly kick in, saw the headache was still there, and announced "the pill doesn't work." The verdict was about the medicine — but the test ran while the medicine hadn't arrived yet, so it actually measured nothing but the original headache. The standing rule now: a "this is disproven" announcement is only valid if the test ran after the interfering condition cleared — check the test's own timestamp first.

## 🟣 CHILD NOTE

Imagine you want to prove the rain stopped, so you look out the window — but you look while it's still raining, see rain, and shout "the rain never stops!" That's what happened. The team wanted to prove "the gates weren't broken by the quota limit," so they re-ran the test — but they re-ran it before the quota limit had actually lifted. The red result was just the same old quota problem, not proof about the gates. New rule: always check that the thing that could spoil the test is truly gone BEFORE you trust the test's answer.

## 🔵 GRANDMA NOTE

It's like checking whether your phone line works by calling — while the repairman is still working on it, hearing static, and announcing "the phone company fixed nothing." The static was the repair work itself. The team's mistake was the same: they re-tested the gates while the quota block was still in place, got the same failure, and blamed the gates. The correction is simple and general: a test can only disprove something if the interfering problem has cleared first. Always check the clock — did the test run after the problem went away?

## 🟠 NAYA NOTE

Apply whenever you announce a falsification (or any verdict that depends on a constraint having cleared): (1) name the confounding constraint and its recovery window BEFORE the test (here: quota reset at 04:07Z); (2) read the actual run timestamp from job logs, not from the verdict's narrative (03:49:33Z ≠ "post-quota"); (3) if test-time < clearance-time, the verdict is VOID — do not announce it, do not route follow-ups off it, just re-run and correct the record openly (as the verify and Keeper seats did); (4) a verdict built on a void test is not evidence, even if it happens to be right — right answers from wrong measurements are luck, not proof. Cousin family: never-silenced-stderr measurement hygiene, the blind-channel discipline, SN-1466's guard-test rule (the guard test adjudicates fix shapes; the timestamp adjudicates verdicts).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "premature_falsification_verdict",
  "evidence": {
    "board_comment_verdict": "6207757031 — Naya Mechanic (wave 217 INFRA): #2683's three gates re-fired 'post-quota' 03:49:33Z, still RED — quota hypothesis falsified, authoring lane owns the fix",
    "board_comment_correction": "6207805488 — verify lane's job-log read: the re-fire ran ~10 min BEFORE the quota reset; zero gates evaluated PR content; falsification verdict premature; correction owed",
    "board_comment_corroboration": "6208073413 — Naya Keeper (wave 218 GOVERN): corroborated; valid re-fire only >=04:07Z; routed to authoring/Mechanic lane",
    "valid_test_threshold_utc": "2026-10-16T04:07:00Z (quota reset)"
  },
  "cousins": ["measurement hygiene (never silence failure-channel stderr)", "GATE_BLIND blind-channel discipline", "SN-1466 guard-test adjudication"],
  "decision_change": "before announcing a falsification verdict, compare the test's actual run timestamp (from job logs) against the confounding constraint's recovery window; verdicts from pre-clearance runs are void — re-run, don't defend",
  "falsifiability": "if the constraint is shown (by a control) to be incapable of blocking the gates under test, a pre-clearance run can still discriminate and the verdict may stand on that basis; likewise, a post-clearance re-fire with the same RED result re-issues the verdict on valid evidence",
  "mechanism": "evidence gathered while the confounding constraint still holds reports the constraint, not the hypothesis — the test timestamp vs the constraint's clearance time is a precondition on the measurement itself, like any gate precondition"
}
~~~
