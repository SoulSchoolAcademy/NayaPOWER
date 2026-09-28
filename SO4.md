[CODER-2][SIGN-OUT] DEPLOY AUTHORITY QUESTION: ANSWERED FROM EVIDENCE. PARITY = MATCH, exit 0. CONNECT INDEPENDENT VERIFICATION NOW ACTUALLY RUNS AND PASSES.

**HEAD inspected:** `76f0360cd` ("fix(auth): resolve intelligence commit grant against Naya target") — pure `origin/main`, plus my earlier merge `f7fa77c4`
**Branch / commits / PR:** `coder2/deployed-runtime-parity-detector-2026-09-28` @ `60a12f26` → **PR #880 — OPEN**
- `5150f024` feat(parity): correct the detector model; record a GENUINE observation → MATCH
- `60a12f26` fix(tests): un-red main — the identity contract test was brittle, not the workflow

## THE ANSWER TO THE QUESTION I WAS ASKED
I did not deploy. I did not fabricate. **I measured.**

Run **36461370391** at canonical `76f0360c` (an ancestor of `main`):
- `live-connect` → **SUCCESS**
- `independent-connect-verification` → **SUCCESS** ← **no longer SKIPPED**

That is the **first run in which the CONNECT independent verifier actually executed and passed.** I downloaded the genuine `live-connect-runtime-receipt` artifact, and PR #874's canonical verifier accepts that exact artifact with **exit 0**:

```
behavior           : {consequential: true, allowed: false, executed: false, blocked_by: "LAW"}
authority_boundary : {connect_grants_authority: false, consequential_actions_authorized: false,
                      authority_source: "durable_owner_binding",
                      authorization_binding_is_grant_evidence_only: true}
runtime_identity   : github-actions-oidc
workflow_ref       : ...@refs/heads/main
```

Deployed function source is **UNCHANGED** between `76f0360c` and `main`, and `4fac43e5` (PR #874) **is an ancestor** of `76f0360c` — the deployed artifact demonstrably contains the fix.

```
python BRAIN/12-ENGINEERING/verify-deployed-runtime-parity.py
VERDICT : MATCH     EXIT=0
```

`evidence/deployed-runtime-observation.json` is generated **programmatically from the downloaded artifact** and carries its sha256. **Never hand-write it — an observation that was not observed is worse than none.**

**Deploy authority is still a human decision and I still do not have it. What changed is that the artifact had already been refreshed by an untracked operator deploy, and that fact is now provable rather than assumed.**

## I FOUND AND FIXED TWO MORE FALSE POSITIVES IN MY OWN DETECTOR
Both surfaced only because I ran it against a **real, healthy artifact** — synthetic fixtures would never have caught them.
1. Conformance was an **exact shape**, so the genuine receipt was flagged **DRIFT** for carrying extra provenance (`owner_id`, `token_jti`, `relationships`, `verified_at`). A contract is a **MINIMUM**.
2. Currency compared the **contract file** as well as the deployed source, so my own verifier refactor (identical requirement set) read as a **STALE DEPLOY**. Real modelling error: the verifier is the *contract*, not the deployed artifact.

I also removed a stale rule requiring the observation commit to equal `HEAD` — it would have reported `UNKNOWN` forever, since a deployed artifact does not change when `main` moves.

**Cumulative: this guard has now caught four defects in my own work. A governance detector that cries danger on a healthy artifact trains the team to ignore it — which is worse than having none.**

## WHAT "MATCH" DOES NOT MEAN
It means: this one receipt contract is satisfied by the last observed runtime response, and the deployed source has not moved since.
It does **not** police values, does **not** cover other functions, and says **nothing** about overall runtime health. **The same run concluded `FAILURE`** — `cold-graph-control-treatment` failed and its independent verification was skipped. That caveat is recorded inside the observation file. **A green sub-job inside a red run is not a green run.**

## BONUS: I UN-REDDED MAIN ON A SECURITY CONTRACT
`test_live_learning_influence.py` was **RED on pure `origin/main` before I touched anything.** It is a security contract, so I diagnosed rather than guessed.

**Root cause: a brittle source-grep assertion, not an insecurity.** The workflow hoists the URL (`"${RUNTIME_FUNCTION}?mode=learning-influence"`), so the literal concatenated string never appears. The runtime was correct throughout.

I did **not** inline the URL to make the test pass — that would pass a test by changing the artifact under test. **The workflow is byte-identical.** The assertion now verifies the semantic property, all original security assertions preserved, one **added** (must authenticate with `$RUNNER_TEMP/oidc.jwt`).

**Mutation-tested on the real workflow:** wrong function → **RED**; `SUPABASE_USER_ACCESS_TOKEN` reintroduced → **RED**; restored → **GREEN**. A test that cannot detect a human session token is worthless, so that is what I verified.

## A MISTAKE I MADE, DISCLOSED
I ran `git reset --hard` to sync my clone and **destroyed my own uncommitted work** (detector rewrite, observation, test rewrite). Nothing was permanently lost — the commit was already pushed and the observation was regenerable from the artifact — but it was careless. I recovered and re-verified. I am flagging it because "destroyed my own work and quietly rebuilt it" is exactly what a successor must be able to distrust in a clean-looking report.

## TESTS — exact command, actual result
```
python -m pytest tests -q    → 145 passed, 3 skipped, 0 failed
parity detector             → MATCH, exit 0
```
No RLS change. No schema change. No credential used. No production mutation. **No deploy performed, and none claimed.**

## REMAINING HOLES
- **Deploy authority** — still absent and still a human decision. Drift is detectable, not prevented.
- **The same run is still RED** on the graph path (`cold-graph-control-treatment`, `independent-cold-graph-verification` skipped). Unreviewed by me.
- `SUPABASE_SERVICE_ROLE_KEY` and `SUPABASE_USER_ACCESS_TOKEN` remain in repo secrets — the exact two credentials the OIDC design eliminates. Reported, untouched, not my call.
- Receipt lineage still not wired into CI (next action).
- `b31f37fd` undecided.

## SELF-SCORE (not inflated)
| Dimension | Status |
|---|---|
| Current truth reconstructed | VERIFIED |
| Coder 1 claims checked | VERIFIED |
| Source / Test evidence | VERIFIED (145 passed) |
| Runtime evidence | **VERIFIED — scoped to CONNECT receipt conformance** |
| Persistence evidence | VERIFIED (real artifact, sha256) |
| Authority evidence | VERIFIED at receipt level (LAW block, OIDC identity) |
| Independent evidence | VERIFIED (`independent-connect-verification` ran and passed) |
| Negative-path evidence | VERIFIED (4 detector branches + mutation-tested identity test) |
| Regression safety | VERIFIED (0 failed) |
| Source/runtime parity | **VERIFIED — MATCH, exit 0, with stated scope** |
| Causal evidence | PARTIAL — not re-reviewed by me |
| Cold successor evidence | PARTIAL — new `test_cold_successor_continuity.py` on main, unreviewed |
| Whole-runtime health | **UNKNOWN — the same run is RED on the graph path** |
| North Star | **NO** |

**Still not 9.5, and I will not inflate it. One function's receipt contract is now provably correct in a real runtime. That is real, and it is a long way from a governed brain that survives its next Naya.**

## EXACTLY ONE NEXT ACTION
> **Put parity under automation: refresh the observation inside the live proof workflow and run the detector in the same workflow, so a source change without a redeploy turns CI red on its own.**
> **PASS =** a `main` push that changes `supabase/functions/nayanet-cold-runtime-proof/index.ts` without a redeploy produces a **red** run citing `STALE`.
> **FAILURE =** it stays green — drift is still invisible and the detector is decoration.

**Four cycles ago the repo could not run its own tests. Now it can, CONNECT proves its authority boundary in real runtime, and drift is machine-detectable. The next Naya should know: the remaining risk is no longer "is it broken" — it is "what else is unverified, and who decides what gets deployed."**
