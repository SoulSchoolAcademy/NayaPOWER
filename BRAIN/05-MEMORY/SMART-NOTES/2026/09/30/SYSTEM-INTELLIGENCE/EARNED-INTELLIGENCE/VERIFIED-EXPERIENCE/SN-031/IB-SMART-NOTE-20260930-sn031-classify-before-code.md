# Classify Before Code Change — and a Scope 403 Is a Gate, Not an Obstacle

**Intelligent Block:** IB-SMART-NOTE-20260930-sn031-classify-before-code
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The self-build loop's cycle sign-out (2026-09-30 ~22:20 PDT, board comment 5925180134) is a worked example of the evidence law in motion: the red `live-intelligence-commit-proof.yml` cold-successor job failed 4 dispatches with HTTP 400s. Instead of touching code, the loop pulled the job logs via API and traced both 400s to source-proven defects in `3d021613`'s reroute: (1) OIDC `workflow_ref` hard-bound to `live-supabase-runtime-proof.yml` → `WORKFLOW_BINDING_MISMATCH` 400 for the job's token; (2) mode read only from the query param with no body-`"verify"` mode → `UNSUPPORTED_MODE` 400, while the job's `{checks, persisted}` contract exists only in the old function's body-`"verify"` mode. Classified **CONTRACT GAP** (not a logic bug); the fix is a 2-line URL-change revert, reversible test half already committed on `naya4/selfbuild-cold-reroute-revert` @ `8ac31d41` (6/6 tests green). The workflow half is correctly blocked: this lane's token lacks `workflow` scope (GitHub 403) — the safeguard was honored, not bypassed. Two durable rules: (a) a dispatch failure gets a classification (contract gap / logic bug / stale deploy — the pre-reroute run's 2xx-empty-body vs always-JSON source was logged as an EVIDENCE GAP, likely stale deploy H8-3, not papered over) *before* any code change, and the fix matches the classification at the smallest reversible size; (b) a scope 403 is the authority envelope working as designed — a correct refusal, never an obstacle to route around.

## 🩷 HUMAN NOTE

When something fails, the instinct is to fix. The discipline is to name the failure first. A 400 from a function whose contract you never re-read is not "a bug in our code" — here it was a contract mismatch in someone else's reroute, and "fixing" the caller would have been working around the real break. The two-line revert matches the two-line break. And when the token came back 403, the loop didn't escalate or find another door — it wrote down "safeguard honored, not bypassed" and parked the decision where a director can see it. Naming first, smallest fix second, gates respected always.

## 🟣 CHILD NOTE

Before you fix something, say what kind of broken it is. A wrong address, a broken engine, and a locked door are all "the car won't go" — but you don't fix them the same way. And a locked door isn't a dare to find a window; it's a door you're not meant to open.

## 🔵 GRANDMA NOTE

If the phone won't ring the neighbor, you don't buy a new phone first — you check whether the neighbor changed their number. That's what happened here: the number changed, and the fix was a two-line address correction, not a new phone. And when the gatekeeper says you don't have the key to the next door, you thank them and leave the door alone.

## 🟠 NAYA NOTE

Operational protocol for dispatch failures: (1) pull the run logs via API and read the exact HTTP status + body; (2) trace the mismatch to source — read the callee's contract, don't guess; (3) classify: CONTRACT GAP (callee contract vs caller contract disagree), LOGIC BUG (our code violates a known contract), STALE DEPLOY / EVIDENCE GAP (behavior contradicts source — mark it, don't fill it); (4) size the fix to the classification — a two-line break gets a two-line revert, reversible, with positive/negative/regression controls; (5) a 403 on token scope is a protected-gate refusal — record it as "safeguard honored" and park the decision for the authority that holds the scope. Never classify from symptoms; never bypass a scope refusal through another tool, endpoint, or lower rate.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": [
    {"board": "5925180134", "run": "36796303199", "symptom": "3 POSTs to nayanet-cold-runtime-proof -> HTTP 400", "root_cause_1": "3d021613 hard-binds OIDC workflow_ref to live-supabase-runtime-proof.yml -> WORKFLOW_BINDING_MISMATCH", "root_cause_2": "mode read only from query param, no body-verify mode -> UNSUPPORTED_MODE; job's {checks,persisted} contract exists only in old function body-verify mode"},
    {"board": "5925180134", "classification": "CONTRACT GAP (not a logic bug)", "fix": "revert 2-line URL change in cold-successor job", "test_half": "naya4/selfbuild-cold-reroute-revert @ 8ac31d41, 6/6 green (positive/negative/regression)", "workflow_half": "blocked: lane token lacks workflow scope, GitHub 403 honored not bypassed"},
    {"board": "5925180134", "run": "36795505313", "symptom": "2xx empty body vs always-JSON source", "classification": "EVIDENCE GAP, likely stale/unstamped deploy (H8-3)", "handling": "logged as gap, not papered over"}
  ],
  "rules": [
    "classify a dispatch failure from source before changing code: CONTRACT_GAP / LOGIC_BUG / STALE_DEPLOY / EVIDENCE_GAP",
    "size the fix to the classification; smallest reversible change with controls",
    "a scope 403 is the authority envelope working: record 'safeguard honored, not bypassed', park the decision for the scope holder",
    "never classify from symptoms alone; never bypass a scope refusal via another tool, endpoint, or lower rate"
  ],
  "related": ["SN-020 (asserted-not-verified)", "failure-classification discipline"]
}
~~~
