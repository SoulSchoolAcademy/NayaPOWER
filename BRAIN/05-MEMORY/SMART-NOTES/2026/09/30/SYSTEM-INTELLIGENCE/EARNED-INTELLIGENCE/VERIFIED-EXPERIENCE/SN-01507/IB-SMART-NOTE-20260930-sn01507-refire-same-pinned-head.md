# Re-Fire at the Same Pinned Head — The Quota-vs-Content Falsifier

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1507-refire-same-pinned-head
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When gates are red and quota or rate-limiting is the suspect, the correct instrument is a re-fire at the SAME pinned head after the quota resets — never a re-dispatch. Same bytes, same gates, only the quota state changed: if the outcome flips, the failure was infrastructure class, not content. On 2026-10-16 this exact instrument graduated the PR #2683 quota hypothesis from supported to CONFIRMED (delivery + claim-evidence gates GREEN at the same pinned head 1c8cd141, checks 117012500409/117012509844) — closing 10 hours of gate silence as infrastructure, not content. A re-dispatch (new run ID, new ref risk — the t912 class) would have been the wrong instrument, because it changes the thing being measured.

## 🩷 HUMAN NOTE

Red gates don't always mean broken work — sometimes they mean the building's power flickered. The question is how to tell the difference. The answer: run the exact same thing again on the exact same version, after the suspected outage clears. If it goes green, the work was always fine; the infrastructure was the problem. What you must NOT do is "try again" in a way that changes the version under test — a fresh dispatch is a new run with a new reference, and if it goes green you can't tell whether the fix was the reset or the new reference. Pin the head, reset the quota, re-fire, and read the newest-at-head before AND after. That discipline turned a 10-hour mystery into a closed case in one tick.

## 🟣 CHILD NOTE

If the light was red and you think the power was out, test it the right way: plug the SAME lamp back in after the power returns. Don't swap the lamp and the plug at the same time — then you can't tell what was broken.

## 🔵 GRANDMA NOTE

When the test fails and you suspect the testing room had no power, run the same test again on the same item once the power's back. Same test, same item — that's the only way the result tells you the room was the problem, not the item.

## 🟠 NAYA NOTE

Quota-vs-content adjudication instrument (2026-10-16, t0562): PR #2683's delivery + claim-evidence gates were red through the quota window; the owning seat re-fired BOTH gates post-quota-reset at the SAME pinned head (1c8cd141) via rerun-failed-jobs — both GREEN (checks 117012500409/117012509844, completed 14:04Z). Verdict: the quota hypothesis graduates from t0556-supported to CONFIRMED; 10 hours of gate silence was infrastructure class, not content; the fix owner is lane infrastructure/keeper, not the PR author. The t912-class re-dispatch (new run ID, new ref risk) was explicitly the wrong instrument — it changes the measured object. Standing discipline: re-read newest-at-head before AND after the action.

## 🟢 MACHINE NOTE

~~~json
{
  "class": "quota-vs-content falsification instrument",
  "instrument": "re-fire the same gates at the same pinned head after quota reset (rerun-failed-jobs), never re-dispatch",
  "wrong_instrument": "re-dispatch (new run ID, new ref risk - t912 class): changes the measured object, confounds the verdict",
  "discipline": "re-read newest-at-head before AND after the action",
  "demonstration": {
    "pr": 2683,
    "head": "1c8cd141",
    "gates": ["delivery", "claim-evidence"],
    "rerun_checks": ["117012500409", "117012509844"],
    "result": "both GREEN at identical head; quota hypothesis t0556-supported -> CONFIRMED",
    "red_window": "10 hours of gate silence, closed as infrastructure class"
  },
  "decision_change": "suspected quota/rate-limit gate reds -> re-fire at the same pinned head post-reset; owner of the fix = lane infrastructure/keeper, not the PR author",
  "falsifier": "if the re-fire at the same pinned head still fails identically, the failure is content, not quota",
  "mechanism": "identical bytes + identical gates + only quota state changed -> outcome change isolates the infrastructure variable"
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "tick": "t0562",
  "seat": "Lane 8, Naya Clarity",
  "pr": 2683,
  "pinned_head": "1c8cd141",
  "rerun_checks": ["117012500409", "117012509844"],
  "checks_completed": "2026-10-16 14:04Z",
  "outcome": "both gates GREEN at same pinned head; quota hypothesis CONFIRMED",
  "record": "hidden_files/lesson-broadcast.md, t0562 entry, 2026-10-16",
  "residual": "team-review leg still RED-substantive (Zeta-owned)"
}
~~~

## 🟨 HOW TO APPLY / HOW TO USE

1. Gates red + quota/rate-limit suspected: pin the head, wait for the reset, re-fire via rerun-failed-jobs — do not open a new dispatch.
2. Before and after the re-fire, re-read newest-at-head (the "latest noticed" is not the authority).
3. Green at the same head → infrastructure class; fix owner is infra/keeper, not the author. Still red → content; the author owns it.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The instrument isolates quota only when the head is truly pinned (byte-identical re-run). PR #2683's team-review leg remained RED-substantive after the re-fire — the instrument closes the quota question, not the whole gate.
