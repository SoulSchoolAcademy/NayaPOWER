## Coder 2 — deploy authority: the artifact was ALREADY refreshed. Parity is now provable → **MATCH**

**Base:** `main` `76f0360c` · **Branch:** `coder2/deployed-runtime-parity-detector-2026-09-28` @ `60a12f26`

### I did not deploy. I did not fabricate. I measured.

Run **36461370391** (canonical `76f0360c`, an ancestor of `main`):

| job | result |
|---|---|
| `live-connect` | **SUCCESS** |
| `independent-connect-verification` | **SUCCESS** ← no longer skipped |

That is the **first run where the CONNECT independent verifier actually ran and passed.** I downloaded the real `live-connect-runtime-receipt` artifact, and PR #874's canonical verifier accepts that exact artifact with **exit 0**:

```
behavior:           {consequential: true, allowed: false, executed: false, blocked_by: "LAW"}
authority_boundary: {connect_grants_authority: false, consequential_actions_authorized: false,
                     authority_source: "durable_owner_binding",
                     authorization_binding_is_grant_evidence_only: true}
runtime_identity:   github-actions-oidc
workflow_ref:       ...@refs/heads/main
```

Deployed function source is **UNCHANGED** between `76f0360c` and `main`, and `4fac43e5` (PR #874) **is an ancestor** of `76f0360c` — so the deployed artifact demonstrably contains the fix.

```
VERDICT : MATCH     EXIT=0
```

`evidence/deployed-runtime-observation.json` is generated **programmatically from the downloaded artifact** and carries its sha256. Not a transcription. **Never hand-write it — an observation that was not observed is worse than none.**

### I found and fixed two more false positives in my own detector

Both surfaced only because I ran it against a **real, healthy artifact** — synthetic fixtures would never have caught them.

1. Conformance was treated as an **exact shape**, so the genuine receipt was flagged **DRIFT** just for carrying extra provenance (`owner_id`, `token_jti`, `relationships`, `verified_at`). A contract is a **minimum**.
2. Currency compared the **contract file** as well as the deployed source — so my own refactor of the verifier (identical requirement set) was reported as a **STALE DEPLOY**. That was a real modelling error: the verifier is the *contract*, not the deployed artifact.

Fix 2 matters most. Currency is now judged only on the function source that actually gets deployed; conformance is always evaluated against the **current** contract. I also removed a stale requirement that the observation commit equal `HEAD` — it would have reported `UNKNOWN` forever, since the deployed artifact doesn't change when `main` moves.

### Scope — restated because a green is easy to over-read

**MATCH means:** this one receipt contract is satisfied by the last observed runtime response, and the deployed source hasn't moved since.

It does **not** police field values, does **not** cover other functions, and says **nothing** about overall runtime health. **The same run concluded `FAILURE`** because `cold-graph-control-treatment` failed and its independent verification was skipped. That caveat is recorded *inside* the observation file. **A green sub-job inside a red run is not a green run.**

### Second commit: un-redding `main` on a security contract

`test_live_learning_influence.py` was **RED on pure `origin/main`** before I touched anything — a security contract, so I diagnosed rather than guessed.

**Root cause: a brittle source-grep assertion, not an insecurity.** The workflow hoists the URL into a variable (`"${RUNTIME_FUNCTION}?mode=learning-influence"`) so the literal concatenated string never appears. The runtime was correct throughout.

I did **not** make the test pass by inlining the URL — that passes a test by changing the artifact under test. **The workflow is byte-identical in this commit.** The assertion now resolves the endpoint the workflow itself defines and verifies the semantic property, with all original security assertions preserved and one **added** (must authenticate with `$RUNNER_TEMP/oidc.jwt`).

**Mutation-tested against the real workflow:**
- wrong target function → **RED**
- `SUPABASE_USER_ACCESS_TOKEN` reintroduced → **RED**
- restored → **GREEN**

Same defect class as the brittle CONNECT assertion in #874. Treating those as governance failures is how real governance failures get missed.

### I also made a mistake, and I'm reporting it

I ran `git reset --hard` to sync my clone and **destroyed my own uncommitted work** (the detector rewrite, the new observation, the test rewrite). Nothing was lost permanently — the commit had already been pushed, and the observation was regenerable from the downloaded artifact — but it was careless. I recovered, re-derived, and re-verified. I'm flagging it because "I destroyed my own work and quietly rebuilt it" is exactly the kind of thing a successor needs to know to distrust a clean-looking report.

### Tests

```
python -m pytest tests -q                                  → 145 passed, 3 skipped, 0 failed
python BRAIN/12-ENGINEERING/verify-deployed-runtime-parity.py → MATCH, exit 0
```

No RLS change. No schema change. No credential used. No production mutation. **No deploy performed, and none claimed.**

### One next action

> **Bring parity under automation: refresh the observation inside the live proof workflow itself, so drift is detected on every run instead of on demand.**
> Concretely: have the successful `live-connect` job emit its receipt into the canonical evidence path, and have the parity detector run in the same workflow — so a source change without a redeploy turns CI red on its own.
> **PASS =** a `main` push that changes the function source without a redeploy produces a **red** run citing `STALE`.
> **FAILURE =** it stays green — that means drift is still invisible, and the detector is decoration.

**Deploy authority remains a human decision and I still don't have it. What changed is that the system can now tell the difference between "deployed and correct" and "we're guessing" — automatically, from real evidence.**
