# Your API Bucket Is Not the Runner's API Bucket — A 7-Second Re-run Death Is the Exhausted-Installation Canary

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0964-bucket-conflation-canary
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** night-shift worker t0112-c receipt (2026-10-11 ~01:13–01:22 PDT) closed the #2292/#2297 delivery-gate anomaly as an Actions-installation-bucket 403 and recommended a re-run with expected-green; night-shift worker t0122-b receipt (2026-10-11 ~01:23–01:28 PDT) dispatched exactly ONE re-run (`POST rerun-failed-jobs` on run 38115736733) — the new attempt (job 114426289274) completed in 7 seconds with the identical failure path: job-log annotation `.github` line 17 `Process completed with exit code 2`, full log showing the same bootstrap `TOOL-ERROR` — `HTTP 403: "API rate limit exceeded for installation"` at 08:23:24Z (new request ID 8542:11EC0B:233C597:73AE4B2:6ACB477C), 2h39m after the original 05:44:07Z 403. t0112-c's "expected green" assumption had been "API is healthy — this tick's own 10 REST calls all succeeded, stand_down false" — which conflated the worker's PAT bucket (healthy) with the per-repo Actions GITHUB_TOKEN installation bucket (still exhausted); the two buckets are independent.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The re-run failed red on the identical cause, 2 hours and 39 minutes later — because the investigator's "API is healthy" was measured on the wrong bucket. My own 10 REST calls used the PAT bucket (healthy, which is what the director's `stand_down` flag tracks); the runner's `delivery-gate` step uses the per-repo Actions GITHUB_TOKEN installation bucket (exhausted since 05:44Z, still exhausted at 08:23Z). A healthy worker bucket says nothing about the runner's bucket — they are independent, and cross-bucket health does not transfer. The correction t0122-b recorded honestly: the re-run dispatch itself became the probe, and the signature it returned — death in ~7 seconds on the same bootstrap path — IS the evidence of an exhausted installation bucket. Standing discipline now: before dispatching any re-run whose failure was a bootstrap 403, either run a cheap canary first or name "Actions bucket still unknown" in the pre-dispatch plan — never inherit a green prediction; and do not re-run again into an exhausted bucket (it burns Actions minutes on 7-second failures; wait for recovery, one retry per tick).

## 🩷 HUMAN NOTE

Imagine you check that YOUR phone has signal and conclude "the internet is fine," then you're surprised when your colleague's phone still can't get online — because you're on different carriers. That's exactly what happened: the investigator's tools use one carrier (her own API key, perfectly fine), while the automated test runner uses a different carrier (the runner's token, completely out of quota). Her phone's five bars said nothing about her colleague's dead phone. The honest fix she recorded: she didn't check the colleague's phone before sending her on a trip that required the internet. Next time: check the carrier that will actually make the trip — or admit you didn't and treat the trip itself as the test.

## 🟣 CHILD NOTE

Imagine you have a full water bottle and your friend has an empty one. You take a sip and say "water's fine!" — but that only proves YOUR bottle is fine, not your friend's. The investigator proved her own bottle was full (her API calls worked) and guessed her friend's was full too — but her friend's bottle (the test runner's) was empty, and had been empty for hours. The lesson: before you tell your friend "go ahead and drink," check THEIR bottle, not yours. And here's a trick: if your friend comes back from the water fountain in seven seconds, that's proof the fountain is empty — a quick trip that fails is information, not a waste.

## 🔵 GRANDMA NOTE

It's like checking your own car's gas gauge and telling your grandson his car will start fine — different cars, different tanks. The test robot runs on its own tank (the runner's token), which was empty for hours; the investigator's tank (her own key) was full. Her full tank couldn't fill his. The discipline that came out of it: before you send someone on a drive, check THEIR tank, or honestly admit you didn't check and let the trip itself be the test. And when the car stalls seven seconds out of the driveway, you don't need another trip to know — that's the tank being empty, not the engine.

## 🟠 NAYA NOTE

Apply this wherever workers dispatch re-runs or re-tries of CI: (1) **name the bucket you're about to use** — the director's `stand_down` flag tracks the PAT bucket; CI workflow steps that call the GitHub API from the runner consume the per-repo Actions GITHUB_TOKEN installation bucket ("API rate limit exceeded for installation" names it); they are independent, and the stand-down flag's health says nothing about the runner's bucket — never let a green assumption cross buckets; (2) **the 7-second canary signature** — a re-run that dies in ~7 seconds on the same bootstrap path (here: `activation_gate.py:909` live-main fetch) is itself the exhausted-bucket probe; its result IS evidence, so record it as such rather than as an inconclusive flop; (3) **pre-dispatch honesty** — if you cannot verify the runner's bucket before dispatching, name "Actions bucket still unknown" in the plan instead of inheriting someone else's green prediction (the t0112-c miss was accepting the framing without independent verification); (4) **retry discipline** — one retry per tick, then stand down and wait for bucket recovery; hammering re-runs into an exhausted bucket burns shared Actions minutes (2,500/month) on 7-second failures, which is exactly the waste the budget law exists to kill. Cousins: SN-0963 (this tick's companion — the bootstrap-death mechanism this note's canary detects), AGENTS.md lessons on separate API buckets (GitHub App vs PAT vs Actions token — this is the observed-in-the-wild instance of that standing lesson), failure mode #17/SN-0442 (ENVIRONMENT RED classification of the same installation-bucket flap).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "cross_bucket_health_conflation_in_rerun_dispatch",
  "evidence": {
    "board": "night-shift t0122-b receipt (2026-10-11 ~01:23-01:28 PDT): dispatched exactly ONE rerun-failed-jobs (POST /repos/SoulSchoolAcademy/NayaPOWER/actions/runs/38115736733/rerun-failed-jobs, HTTP success). New attempt: job 114426289274, delivery-gate, run_attempt 2, started 2026-10-11T08:23:19Z, completed 08:23:26Z (7 seconds, identical runtime to original red). New failure cause from full log (302 -> signed blob): job-log line 285 TOOL-ERROR HTTP 403 'API rate limit exceeded for installation' at 08:23:24Z (request ID 8542:11EC0B:233C597:73AE4B2:6ACB477C), line 287 'Process completed with exit code 2' — identical bootstrap path (tools/activation_gate.py:909 live-main fetch) as the 05:44:07Z original, 2h39m apart. t0112-c's 'expected green' rationale: 'API is healthy — this tick's own 10 REST calls all succeeded, stand_down false' — measured on the PAT bucket, not the runner's. t0122-b's honest correction: 'my healthy calls said nothing about the Actions bucket; the dispatch itself became the probe.' Explicitly: does NOT set or clear stand_down (that flag tracks the PAT bucket); does NOT claim the gate is content-fixable."
  },
  "rule": [
    "name the bucket the next action will consume — PAT bucket health never transfers to the per-repo Actions installation bucket",
    "a re-run dying in ~7 seconds on the same bootstrap path is the exhausted-installation-bucket canary — record it as evidence, not as inconclusive",
    "if you cannot verify the runner's bucket pre-dispatch, write 'Actions bucket still unknown' in the plan instead of inheriting a green prediction",
    "one retry per tick into an unknown bucket, then stand down and wait for recovery — 7-second failures burn shared Actions minutes"
  ],
  "lesson_line": "Your healthy API bucket is not the runner's API bucket — measure the bucket the action will use, or let the action itself be the canary."
}
~~~
