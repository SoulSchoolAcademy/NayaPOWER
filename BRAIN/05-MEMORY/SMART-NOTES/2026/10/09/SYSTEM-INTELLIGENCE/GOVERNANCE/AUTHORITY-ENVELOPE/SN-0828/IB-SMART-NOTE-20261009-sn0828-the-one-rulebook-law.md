# The One-Rulebook Law — Plan and Execute Share One Risk Policy; a Mid-Flight Swap Is Refused

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0828-the-one-rulebook-law
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 6089857525 (2026-10-09).
**Provenance:** #1354 comment 6089857525 ([NAYA 5][ACHIEVEMENT] Safety — closed the ACT re-gate risk-policy threading hole, 2026-10-09T21:51:19Z). Branch `naya5/safety-risk-policy-threading` @ 63ed5d06; proven with 9 falsifier tests (red before, green after); full suite 1940 passed, 0 failed. Full scorecard on #1606 (comment 6089854060). Cousins: RiCo — authority must travel with the message, legitimacy is continuous; SN-0706 (grant-system rebuild on authority-travels-with-receipts); SN-0575 (proactive fix authority).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A plan phase and an execute phase were each allowed to judge "how much risk is too much" under a different rulebook — and nothing forced them to agree. The hole: a risk policy could be swapped between planning and doing, and the doer would fire anyway. The repair, closed 2026-10-09: **the plan carries its rulebook; the execute phase re-checks under the same rulebook by default; if anyone tries to swap the rulebook mid-flight, the action is refused — the doer never fires.** The durable law: there is ONE risk rulebook per action, and it is bound to the plan like a seal. Any phase that would judge risk must inherit it, not substitute its own. This is RiCo's "authority must travel with the message" applied to safety: the rulebook IS the message's authority, and legitimacy (here: permission to act) is only continuous if the rulebook is continuous. For a cold successor building any plan→act pipeline: thread the policy object through the seam, re-verify identity at the seam, and refuse on mismatch — default to refusal, not to the newest rulebook.

## 🩷 HUMAN NOTE

Shawn — we found and closed a real safety hole: the planning side and the doing side of ACT could each follow a different set of risk rules, and if the rulebook changed between plan and action, the action would just go ahead anyway. Now the plan carries its rulebook with it, the executor re-checks against that same rulebook, and if anyone tries to swap it mid-flight, the action is refused outright — the doer never fires. Nine falsifier tests proved it was broken before and sealed after, and the full suite stayed green. One rulebook per action, always.

## 🟣 CHILD NOTE

Imagine a kid gets a hall pass for the bathroom, but then scribbles "plus the playground" on it. The teacher can't tell, so the kid wanders off. The fix: the pass is stamped in a way that can't be changed — the hallway teacher checks the stamp matches, and if it's different, the kid goes back to class. Same idea: the plan's risk rules travel with it like a stamp, and the executor checks the stamp. Different stamp? No action.

## 👵 GRANDMA NOTE

There's a two-step job in the system: one part makes a plan, another part carries it out. Both parts are supposed to follow the same safety rules — but they weren't checking that the rules matched. It was like approving a recipe and then swapping the ingredients halfway through cooking without telling the cook. We fixed it so the safety rules are sealed to the plan, and the second part refuses to cook if the seal is broken. Simple, and now it can't slip through.

## 🤖 NAYA NOTE

A cold Naya building any plan→execute seam: make the risk policy an explicit object bound to the plan (not ambient configuration each phase reads independently). At the seam: (1) the executor receives the plan's policy object, (2) re-verifies it is the same object (identity, not just shape), (3) refuses to fire on any mismatch — default-deny. Test with falsifiers: mutate the policy between phases and assert refusal (the 9 falsifier tests here were red before the fix, green after — the test that fails before you build the fix is the proof the hole was real). Never default to the "newest" policy; default to the plan's policy.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0828",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "directive": "#1354 6089857525: close the ACT re-gate risk-policy threading hole",
  "law": "one risk rulebook per action: the plan carries its rulebook, the execute phase re-checks under the same rulebook by default, and a mid-flight rulebook swap is refused — the doer never fires",
  "rule": "thread the policy object through the plan→execute seam; re-verify identity at the seam; default-deny on mismatch",
  "rationale": "plan and execute phases judging risk under different rulebooks lets a mid-flight policy swap authorize what the plan forbade",
  "completion_criterion": "falsifier tests mutate the policy between phases and assert refusal; full suite stays green",
  "disagreement_protocol": "on policy mismatch at the seam, refuse the action and surface the mismatch; never silently substitute the newest policy",
  "generalizes_to": "RiCo instantiated in the safety domain — authority (permission to act) travels with the message (plan + its rulebook); legitimacy is continuous only if the rulebook is continuous",
  "cousins": ["RiCo", "SN-0706", "SN-0575"]
}
```
