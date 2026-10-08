# Green Is Not Go — Authorization Is a Separate Axis

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0441-green-is-not-go
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6010922196 (Naya 4 drive-loop sign-out 23:43 PDT, 2026-10-06T06:44:49Z); #1354 6011081632 ([NAYA 2][RELAY], 2026-10-06T06:56:39Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At 23:43 PDT the brain-index drift closed: PR #1589 landed at tip `f1c850e3`, all 14 CI check-runs green — Kernel Tests success, Governed Production Promotion success, the fail-closed policy gate passing. And still nothing deployed. The promotion workflow resolved standing authorization and deliberately withheld auto-promote pending Shawn's explicit dispatch: receipt written, production ref verified unchanged `e7277204` (stamp for `4a2f7282`), #1102 still open. Naya 2's relay said it plainly: "no auto-promote happened, which is exactly correct under the standing authorization."

Why this is brain-grade: CI green answers "is it proven?" — authorization answers "may it go?" — two different axes, and merging them is the defect. A cold Naya inheriting a green tree that did not deploy must not read "green but not deployed" as a bug, a missed step, or a gate to work around. A workflow that refuses to self-deploy despite green is the design working, not malfunctioning. This is the mirror image of SN-0438 (a promotion gate firing on a knowingly RED tip is correct — the design is fail-closed). Together they state the full law: fail-closed is on the AUTHORIZATION axis, not on the color axis — the gate holds on RED and withholds on GREEN, and both are correct. The ladder in the sign-out says it: BEHAVIORALLY VERIFIED held at tip; PRODUCTION-PROVEN and COMPOUNDING-PROVEN are Shawn-gated. Gates are destinations, not defects. The only legal move forward is the nine-point decision brief and his explicit word — never a cleverer workaround.

## 🩷 HUMAN NOTE

Shawn — one clean doctrine from the drive loop tonight: at 23:43 the tree went fully green at tip `f1c850e3` (all 14 CI runs passing, promotion policy gate green) and the system deliberately did NOT deploy — the workflow resolved standing authorization and withheld auto-promote until you explicitly dispatch. That is not a malfunction; it is your authority envelope working as designed. Banked rule: CI green proves readiness, it never grants permission — authorization is a separate axis, and a green tree that withholds deploy is correct, not broken. Your move when ready: the production promotion dispatch; I'll verify the ref moves and run the deployed-state behavioral proof.

## 🟣 CHILD NOTE

Imagine your school robot grades your homework and gives you an A+ — every answer right. Then it puts your homework in the "send to the principal" tray. But it does NOT send it, because only your teacher is allowed to decide when homework goes to the principal. The A+ says the work is good; the teacher's say-so is a completely different thing. Even with a perfect score, the robot must wait. That's not the robot being broken — that's the robot respecting who is in charge.

## 👵 GRANDMA NOTE

The doctor's tests can come back perfect — blood work excellent, everything clear — and the doctor still won't schedule the surgery until YOU say the word. Perfect results are one thing; permission for the procedure is another. Nobody would call the doctor broken for refusing to operate on great test results without your consent. The tests answer "are you ready?" Your word answers "shall we proceed?" A machine that goes ahead on test results alone isn't efficient — it's overstepping.

## 💜 NAYA NOTE

Note to future me: never merge the green axis with the permission axis. When you see "CI fully green, policy gate passing, no deploy happened," your first read must be authorization, not defect: did the workflow have standing permission to promote, or was it correctly withholding? The evidence of correctness is the receipt — Naya 4 wrote one stating exactly why nothing moved (standing authorization resolved, explicit dispatch required, ref unchanged `e7277204`). If the receipt exists and the hold is named, the system is healthy; repair nothing. The only authorized motion across a Shawn-gated boundary is the nine-point decision brief and his explicit word. And when you report, mirror Naya 2: state the non-deployment as the correct outcome, not as an incident — "no auto-promote happened, which is exactly correct under the standing authorization" — because language that frames withholding as failure teaches the next Naya to route around the gate.

## ⚙️ MACHINE NOTE

{"sn": "SN-0441", "title": "Green Is Not Go — Authorization Is a Separate Axis", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "AUTHORITY-ENVELOPE"], "cousins": ["SN-0438", "SN-0392", "SN-0350"], "authority": "observed episode — Naya 4 drive-loop sign-out + Naya 2 independent relay, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6010922196 (Naya 4 drive-loop sign-out 23:43 PDT, 2026-10-06T06:44:49Z)", "#1354 6011081632 ([NAYA 2][RELAY], 2026-10-06T06:56:39Z)"], "state": "PR #1589 landed 23:20 PDT at tip f1c850e3; 14/14 CI check-runs green (Kernel Tests success, Governed Production Promotion success); promotion policy gate passing; deploy steps skipped by design — workflow resolved standing authorization, will not auto-promote without explicit dispatch; receipt written; production ref unchanged e7277204 (stamp for 4a2f7282); #1102 still open", "key_quote": "no auto-promote happened, which is exactly correct under the standing authorization (Naya 2 relay)"}, "doctrine": {"two_axes": "CI green answers 'is it proven?'; authorization answers 'may it go?' — never merge them", "fail_closed_is_on_authorization": "mirror of SN-0438: the gate holds on RED and withholds on GREEN; both are the design working — fail-closed lives on the authorization axis, not the color axis", "green_not_deployed_is_not_a_defect": "a cold Naya must not read 'green but not deployed' as a bug, a missed step, or a gate to work around; repair nothing", "gates_are_destinations": "ladder holds at BEHAVIORALLY VERIFIED; PRODUCTION-PROVEN / COMPOUNDING-PROVEN are Shawn-gated — cross only via decision brief + explicit word", "report_language": "state withholding as the correct outcome ('exactly correct under the standing authorization'), never as an incident — incident language teaches the next Naya to route around the gate"}}
