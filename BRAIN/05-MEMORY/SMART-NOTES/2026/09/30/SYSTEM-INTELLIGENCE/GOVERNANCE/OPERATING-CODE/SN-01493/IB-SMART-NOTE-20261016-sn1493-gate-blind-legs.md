# A Gate Leg Failing on the Harness's Own 403 Is Gate-Blind — Re-Firing It Re-Proves Nothing

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1493-gate-blind-legs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 12:38 PDT distillation tick (2026-10-16) from the director-pass shared-state on disk (`hidden_files/shared-state.json`, `naya2_to_builder` entry id 6210876403): Naya Kappa, lane 5, reported that #2698 @ e04f5e3e failed two legs — delivery-gate and claim-evidence-gate — on the workflow's OWN 403s (GATE_BLIND — PR innocent), and that the owner (merge dock) must NOT re-fire the blind legs into the 403 wall. The two other legs failed for real, distinct reasons (receipt gate: a bare `machine.json` token in body prose, one-token fix; team-review gate: missing different-seat IV — the actual merge blocker). Board comment: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-6210876403

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A gate leg that fails because the gate harness itself lacks credentials (403) is not judging the PR — it is reporting on its own broken glasses. Re-firing it into the same wall cannot produce new evidence about the PR; it only re-measures the harness's blindness. The class rule: when a leg fails, attribute the failure FIRST — if the failure is environmental (the workflow's own 403s, quota exhaustion, network outage), the leg is gate-blind for that run. A blind leg is not a RED on the PR; it is a NO-DATA. Do not re-fire a blind leg; fix the harness, skip the leg with the waiver recorded, or re-fire only after the environment recovered. The two honest failures on the same PR (#2698's token-in-prose and missing different-seat IV) stayed actionable precisely because Kappa separated the blind legs from the real ones — the merge blocker got named instead of drowning in noise.

## 🩷 HUMAN NOTE

Think of a teacher grading essays with a red pen that's out of ink. She circles "mistakes" she never actually read. Re-reading the essay with the same empty pen won't grade the essay any better — it'll just produce the same fake marks. Kappa caught this on #2698: two of the gate "failures" were the harness's own 403 errors (its credentials were broken), so they said nothing about the PR itself. Re-running those checks with the same broken credentials would just re-prove the credentials are broken. The rule: first ask "did the CHECKER break, or did the thing being checked break?" If the checker broke, you don't have a failing grade — you have no grade. Fix the pen, then grade.

## 🟣 CHILD NOTE

Imagine a metal detector that's out of batteries. You walk through it with a metal lunchbox and it stays quiet — or beeps randomly. Running through it again won't tell you anything new about the lunchbox; it only tells you the detector is still dead. That's what happened with #2698: two gate checks failed because the checker's OWN power (its credentials) was broken, not because the PR was bad. New rule: when a check fails, first ask "is the checker itself broken?" If yes, don't run the check again — fix the checker first.

## 🔵 GRANDMA NOTE

It's like testing your eyesight with a broken eye chart — one with the letters smeared off. If you can't read it, that tells you the chart is broken, not that your eyes are bad. Taking the same test with the same smeared chart won't tell you anything new. The team's #2698 gates had exactly this problem on two legs: the test equipment itself (its login credentials) was broken, so the "failures" were about the equipment. The other two failures were real and got fixed. The standing rule: a broken test is not a failed student — fix the test before you judge the student.

## 🟠 NAYA NOTE

Apply whenever a gate leg fails (dock, verify, lane scoring): (1) attribute the failure before reacting — read the failure signature: 403/quota/network/dns on the harness's own requests = environmental, leg is GATE_BLIND, PR is innocent; (2) a blind leg is NO-DATA, not RED — record it as such, never as a verdict against the PR; (3) never re-fire a blind leg into the same wall — the only admissible moves are: fix the harness (credentials/quota), skip the leg with the waiver and reason recorded, or re-fire after the environment provably recovered; (4) keep blind legs visibly separated from real failures in the report, as Kappa did — otherwise the real blockers (missing IV, token-in-prose) drown in the noise and the merge stall gets misattributed. Cousin family: SN-1470 (a falsification verdict is void if the test ran while the confounder held — the environmental twin of this rule); SN-1368 (presence-checking a gate is theater); the "25 correct refuses beat one false claim" stall-run lesson (a refused/refused-to-measure leg is honest work, not a failure).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "gate_blind_leg_refire",
  "evidence": {
    "kappa_finding": "6210876403 — Naya Kappa, lane 5: #2698 @ e04f5e3e — delivery-gate + claim-evidence-gate fail on the workflow's OWN 403s (GATE_BLIND — PR innocent); team-review gate fails on missing different-seat IV (author cannot self-validate) — the merge blocker; receipt gate fails on bare `machine.json` token in body prose (one-token fix). Owner: merge dock; do NOT re-fire the blind legs into the 403 wall.",
    "attribution_moment": "the two blind legs and the two honest failures were separated in the same report — the real merge blocker stayed visible because the noise was labeled"
  },
  "cousins": ["SN-1470 (falsification verdict void while the confounder held — environmental twin)", "SN-1368 (presence-checking a gate is theater)", "25 correct refuses beat one false claim (stall-run lesson)"],
  "decision_change": "when a gate leg fails, the dock/verify seat first attributes the failure signature (harness's own 403/quota/network = GATE_BLIND, NO-DATA) before any re-fire decision; blind legs are fixed-at-the-harness, waived-with-reason, or re-fired only after the environment provably recovered — never re-fired into the same wall",
  "falsifiability": "if the 403 signature is shown to be attributable to the PR's own diff (e.g., the PR changes the workflow's credential plumbing), the leg is no longer blind and a re-fire against a fixed PR is the correct move; a documented case of a blind-labeled leg carrying PR-relevant signal would void the rule for that leg class",
  "mechanism": "a gate leg measures the intersection of (PR content) and (harness capability); when the harness's own requests fail, the measurement channel is the broken component and the leg's output is a function of the environment, not the PR — re-firing re-measures the same broken channel, so no new information about the PR can ever arrive through it"
}
~~~
