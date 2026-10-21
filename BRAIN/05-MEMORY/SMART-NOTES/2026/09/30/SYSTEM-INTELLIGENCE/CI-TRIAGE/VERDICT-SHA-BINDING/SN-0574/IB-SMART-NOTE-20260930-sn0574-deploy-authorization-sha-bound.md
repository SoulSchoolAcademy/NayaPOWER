# A Deploy Authorization Is Bound to an Exact SHA — and a Failed Dispatch Means Production Is Stale, Not Almost Live

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0574-deploy-authorization-sha-bound
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6046831916 ([NAYA 5], 2026-10-07T21:04:55Z) + PR #1665 merged (cold-retrieve v1, main @ `5e629d3`)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The evening of 2026-10-07 taught us what an authorization actually is. Shawn gave two manual deploy authorizations (18:49 and 19:49 UTC); both FAILED. The 19:49 run cleared authorization and then died at step 10, "Dispatch canonical end-to-end runtime proof after producer." Meanwhile PR #1665 merged — main moved to `5e629d3` — and the production branch is still on the old build.

Two durable facts for a cold successor: **(1) An authorization is a verdict, and every verdict binds to the SHA it was computed on.** The 18:49/19:49 authorizations were for the main that existed then; main has moved to `5e629d3`, so any new authorization must name the fresh SHA — re-running the old authorization is inadmissible (this is SN-0493's "a decision expires when the tip moves," applied to human authority). **(2) A failed dispatch is not "almost deployed" — it is stale production plus an unresolved failure.** Nothing reaches production until the pipeline is repaired; Naya 1 owns diagnosing the runtime-proof dispatch (the #1 blocker); the re-authorization request must wait for the repair and must carry the new SHA.

Why this is brain-grade: this converts an evening's confusion into a standing protocol. The failure mode it closes is the plausible-sounding one: "Shawn already authorized the deploy, so just re-run it" — wrong, because the bytes being authorized no longer exist at the tip. It also closes the optimism failure: treating a failed run as partial progress toward production. A failed authorization-gated run leaves exactly two things behind — a stale production branch and a diagnosis job. The re-auth request is a new request, on new bytes, after the repair. Any lane that reaches Shawn for a deploy authorization must present: the failing step's diagnosis, the repair, the fresh tip SHA, and the verdict binding the authorization to that SHA — never a re-run of yesterday's authorization.

## 🩷 HUMAN NOTE

Shawn — banking the hard-won deploy lesson from tonight, in plain words: an authorization belongs to the exact code it was given for. When the code moves forward (PR #1665 put main on 5e629d3 after your two authorizations), the old authorization no longer applies — a new authorization has to name the new code. And a failed deploy run isn't "almost live" — production is still on the old build, and the pipeline needs repair (Naya 1 owns diagnosing step 10, the runtime-proof dispatch) before any new authorization is requested. The standing protocol from here: diagnose, repair, then re-authorize on the fresh SHA — never re-run an old authorization.

## 🟣 CHILD NOTE

Imagine your mom signs a permission slip for a field trip on Tuesday. If the trip gets moved to Thursday with a different bus and a different plan, does Tuesday's slip still work? No — she has to sign a new one for the new trip. And if the bus broke down on Tuesday, the trip didn't "almost happen" — everyone is still at school, and the bus needs fixing first. Same here: the signed permission was for Tuesday's code, the code changed, and the bus broke — so fix the bus, then get a new slip for the new trip.

## 👵 GRANDMA NOTE

It's like a building permit: the city approves *these blueprints*. If the architect revises the plans and the foundation crew hits a problem, the old permit doesn't cover the new building — you fix the problem, submit the new plans, and get a new permit. Waving the old permit around changes nothing. Authority travels with the exact thing it authorized.

## 🧠 NAYA NOTE

Cold successor: production deployment protocol after any failed authorized run. (1) **Diagnose before re-auth.** Find the exact failing step (here: step 10 "Dispatch canonical end-to-end runtime proof after producer," owned by Naya 1 on 2026-10-07) and repair the pipeline first — a failed dispatch means production is stale, not almost live. (2) **Re-anchor the tip.** If main moved since the authorization (here: PR #1665 merged → `5e629d3`), the old authorization is expired — SN-0493. (3) **Request a new authorization** that names the fresh SHA, the failing-step diagnosis, and the repair — never ask Shawn to "re-run the old one." Checklist before approaching him: pipeline green on the new tip? diagnosis written? new SHA named? If any answer is no, you are not ready to ask. Two authorizations spent without a deploy is the cost of skipping this protocol — do not pay it twice.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0574",
  "title": "A Deploy Authorization Is Bound to an Exact SHA — and a Failed Dispatch Means Production Is Stale, Not Almost Live",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "VERDICT-SHA-BINDING"],
  "cousins": ["SN-0493", "SN-0350", "SN-0438"],
  "evidence": {
    "board": ["#1354 6046831916 ([NAYA 5], 2026-10-07T21:04:55Z)"],
    "authorizations": "Shawn's two manual deploy authorizations (2026-10-07 18:49 UTC, 19:49 UTC) both FAILED; 19:49 run cleared authorization, died at step 10 'Dispatch canonical end-to-end runtime proof after producer'",
    "state": "PR #1665 MERGED (cold-retrieve v1); main moved to 5e629d3; production branch still on old build; deploy = Shawn's gate",
    "diagnosis_owner": "Naya 1 — proof-chain dispatch diagnosis is the #1 blocker"
  },
  "rule": "an authorization is a verdict bound to the exact SHA it was computed on — when the tip moves, the authorization expires (SN-0493); a failed authorized run leaves stale production + a diagnosis job, never partial deployment; re-authorization requires: failing-step diagnosis, repair, fresh tip SHA",
  "failure_mode_closed": "re-running a stale authorization against new bytes; treating a failed dispatch as 'almost deployed'"
}
```
