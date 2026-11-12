**Intelligent Block:** IB-SMART-NOTE-20261111-sn02674-expired-policy-denies-every-push
**Smart Note:** SN-2674
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 16:08 PST. Evidence: self-build cycle W46-TIPVERIFY-34 record (~/workspace/goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261111-1538-w46-tipverify34.md, PROVE section): promote-and-prove classified GATE-BLOCKED / POLICY EXPIRED (expected fail-closed, not a bug), step 4 "Enforce ratified standing policy" failing at both pins ea4806dc and 918caf3a, reproduced locally with the pin-exact evaluator as DENY policy_expired, controls non-vacuous. Standing policy STANDING-PRODUCTION-PROMOTION-V1, expires_at 2026-10-29T00:00:00-07:00, automatic_renewal false.

## ✦ IN A NUTSHELL

The standing production promotion policy expired on 2026-10-29, and from that moment promote-and-prove fails on every push — by design, not by defect. The gate's step 4, "Enforce ratified standing policy," returns DENY policy_expired before reaching any other gate, because evaluate_policy() re-reads expiry from the ratified document itself and automatic_renewal is false. The self-build cycle W46-TIPVERIFY-34 reproduced the denial locally with the pin-exact evaluator at two pins (ea4806dc and 918caf3a) with non-vacuous controls, and classified it GATE-BLOCKED / POLICY EXPIRED — expected fail-closed, not a bug. The diagnostic rule this leaves behind: when promote-and-prove fails at step 4, check the policy's expires_at first and debug nothing; the only cure is renewal, and renewal is a ratification — Shawn's word, not a code fix. Until then, red promote-and-prove on every push is the gate working, and treating it as a regression wastes the investigation.

## 🩷 HUMAN NOTE

Shawn — the automatic promotion check has gone red on every push since your standing promotion policy expired on October 29th, and it will stay red until the policy is renewed. This is the gate working exactly as designed, not something broken: the policy can't extend itself, renewal is deliberately off, so the gate refuses everything automatic until you renew it. Nobody should spend time debugging the gate code — the check to run first is the policy's expiry date, and the fix is your word renewing it. Until then, expect the red on every push and don't chase it.

## 🟣 CHILD NOTE

Imagine a permission slip that lets the robot move toys to the big shelf by itself. The slip says it works until October 29 — and after that day, it stops working. The robot isn't broken; the slip just ran out. Every time it tries, it checks the slip first, sees the date has passed, and says no. The only way to make it work again is for the principal to sign a new slip. If you try to fix the robot, you'll waste the whole afternoon — the robot is fine, the slip is just old.

## 🔵 GRANDMA NOTE

Dear, the automatic promotion check has been failing on every push lately, and everyone assumed something broke. Nothing broke. The permission that lets it run on its own expired on October 29th — it was written to end on that date, and it can't renew itself. So the gate does the safe thing and says no to everything automatic until a new permission is signed. The lesson is simple: when that check fails, look at the permission's date first, before touching any of the machinery. And only Shawn can sign the new permission — it's his decision, not a repair job.

## 🟠 NAYA NOTE

The verified facts: (1) Cycle W46-TIPVERIFY-34 (pin 918caf3a, window exactly 1 commit, DP-705) classified promote-and-prove (completed 22:52:01Z) as GATE-BLOCKED / POLICY EXPIRED — expected fail-closed, not a bug. The failing step is step 4, "Enforce ratified standing policy before automatic promotion." (2) The denial was reproduced locally with the pin-exact evaluator at both pins, ea4806dc and 918caf3a, as DENY policy_expired, with non-vacuous controls (the explicit-human path promoted on the Human Director's D3 runs, so the automatic denial is a real verdict, not a broken pipe). (3) The policy terms: STANDING-PRODUCTION-PROMOTION-V1, RATIFIED, expires_at 2026-10-29T00:00:00-07:00, automatic_renewal false — by design, so the policy cannot self-extend on the automatic path (SN-0215's mechanism). (4) Consequence, stated in the cycle record: every push to main will keep failing promote-and-prove until the policy is renewed; renewal is a ratification (protected gate, Shawn's word). The cycle's crisp decision routes renewal to Shawn via the dock; until renewed, promote-and-prove red on every push is expected and is not a regression. (5) Honest scope: the classification is about step 4 only — the separate `test` red at the same pin is classified BASE-DEFECT (carried suite red), a different cause. This note does not claim the whole CI is healthy; it claims the promote-and-prove leg is explained. (6) This is not SN-0215 (the policy cannot self-extend — the mechanism, written 2026-10-02 while the policy was still in force); this note is the first observed expired-state behavior: the permanent DENY on every push, the diagnostic order (expiry first, code never), and the renewal routing. SN-0215 says the door cannot open itself; this note says the door is now shut, by the calendar, and here is how you tell.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2674",
  "slug": "expired-policy-denies-every-push",
  "title": "An expired promotion policy fails closed on every push — DENY policy_expired is the gate working, not a regression",
  "observation": false,
  "applies_when": [["promote-and-prove", "policy-expired"], ["gate", "policy-expiry"], ["promotion", "standing-policy"]],
  "enforcement": "The W46-TIPVERIFY cycle re-runs the pin-exact evaluator at the next tip and classifies any promote-and-prove step-4 failure with the standing policy's expires_at cited before any code debugging; a classification that debugs the gate before citing expiry fails the cycle's own check. The workflow itself emits DENY policy_expired — that string is the diagnosis, not a symptom to investigate.",
  "evidence": "Self-build cycle W46-TIPVERIFY-34 record (~/workspace/goals/nayapower-self-build-loop/hidden_files/selfbuild-cycle-20261111-1538-w46-tipverify34.md, PROVE section): promote-and-prove classified GATE-BLOCKED / POLICY EXPIRED (expected fail-closed, not a bug); step 4 'Enforce ratified standing policy' fails at both pins ea4806dc and 918caf3a, reproduced locally with the pin-exact evaluator as DENY policy_expired, controls non-vacuous (explicit-human path promoted on D3 runs). Standing policy STANDING-PRODUCTION-PROMOTION-V1, RATIFIED, expires_at 2026-10-29T00:00:00-07:00, automatic_renewal false. Consequence recorded: every push fails promote-and-prove until renewed; renewal is a ratification (Shawn's word).",
  "decision_change": "When promote-and-prove fails at step 4, check the policy's expires_at first — do not debug the gate code. The next decision this changes is the renewal call: it routes to Shawn as a ratification, and until renewed, promote-and-prove red on every push is expected and needs no investigation.",
  "falsifier": "Renew the standing policy — if promote-and-prove clears on the next push (rest green), the diagnosis holds; if it still DENYs policy_expired after renewal, the diagnosis is wrong.",
  "cousins": ["SN-0215 (the policy cannot self-extend — the mechanism this note applies to the expired state; written while the policy was in force)", "SN-0079 (withheld certification is the gate working)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
