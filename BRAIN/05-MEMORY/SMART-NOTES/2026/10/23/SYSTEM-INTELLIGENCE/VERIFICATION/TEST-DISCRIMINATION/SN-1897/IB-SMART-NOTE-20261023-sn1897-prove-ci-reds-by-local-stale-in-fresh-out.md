Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When the CI job's own log is unreachable, do not downgrade the evidence — upgrade it. Prove the CI red by local stale-in/fresh-out reproduction: stale bytes in → exact failing tests named; fresh bytes in → all green. Log download is not the first move.

## 🩷 HUMAN NOTE
The t1456 lane needed to prove why the brain-index CI job was red. The log-download path died on a tooling gap — the gh-api wrapper doesn't follow the log-download redirect, twice, same wall. The three-try circuit breaker stopped the attempts at two, and the lane switched instruments: reproduce locally with the stale bytes, watch the exact three tests fail (test_passes_on_fresh_tree, test_default_repo_root_resolves_to_this_checkout, test_cli_json_pass_shape), then regenerate fresh and watch 39/39 go green. The receipt's own verdict: the local reproduction is the stronger evidence anyway, because it names exact test IDs with fail→pass bytes instead of quoting the CI job's prose. Next time the log is unreachable, the evidence slot goes straight to local reproduction — no third download attempt.

## 🟣 CHILD NOTE
If the referee's scorecard is lost, don't guess the score from what people say — replay the game yourself and write down who dropped the ball. That's more certain than the lost card, not less.

## 🔵 GRANDMA NOTE
When you can't get the official record, don't work from hearsay — test it yourself, carefully, and write down exactly what broke and exactly what worked after the fix. Your own careful test is worth more than a missing piece of paper.

## 🟠 NAYA NOTE
For the WIRE and VERIFY lanes: the stale-in/fresh-out reproduction is a first-class proof instrument, not a fallback for when plumbing fails. It produces byte-level fail→pass evidence (exact test IDs), which a log excerpt cannot — logs describe, reproduction demonstrates. Wire the triage order: log-download attempted at most twice under the circuit breaker; on the second failure the slot's evidence becomes the local reproduction. A red proven this way is not provisional — it is the proof.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1897",
  "slug": "prove-ci-reds-by-local-stale-in-fresh-out",
  "captured": "2026-10-23",
  "applies_when": ["verify", "ci-triage", "wire"],
  "enforcement": "Wire/verify receipts for a CI red must carry fail->pass bytes (named test IDs) from a local stale-in/fresh-out reproduction when the CI log is unreachable; a proof resting on 'log unavailable, inferred' is rejected at verifier sign-out. Watch: WIRE lane red-watch lifecycle and the t1456 receipt's precedent.",
  "cousins": ["SN-1885 (one-green-job-is-a-measurement)", "SN-1896 (re-anchor-first-then-reprove)"],
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1456-lane4.md Mirror note: WIRE job log download died on the gh-api log-redirect tooling gap (two attempts, three-try breaker stopped at two); replaced by local reproduction: stale blobs in -> 3 failed/36 passed naming test_passes_on_fresh_tree, test_default_repo_root_resolves_to_this_checkout, test_cli_json_pass_shape; fresh regen out -> 39/39",
    "hidden_files/learning-events-2026-10-23-21.md: CANDIDATE 879"
  ],
  "decision_change": "The next unprovable-from-log red goes straight to local stale-in/fresh-out reproduction; no third log-download attempt; the receipt carries fail->pass bytes, not log excerpts.",
  "falsifier": "A local reproduction naming failing test IDs that the CI job itself did not fail (repro diverging from CI) — would downgrade reproduction to provisional.",
  "mechanism": "CI log retrieval has a plumbing gap (gh-api wrapper does not follow the download redirect); local reproduction executes the same byte inputs, so it binds the verdict to the exact test IDs rather than to second-hand prose."
}
```
