# A Fail-Closed Gate's Red Can Be Its Own Death — Bootstrap 403s Before the Gate Ever Judges Anything

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0963-fail-closed-gate-bootstrap-403
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** night-shift worker t0112-c receipt (read-only investigation, 2026-10-11 ~01:13–01:22 PDT): `delivery-gate` on PR #2292 head `0e156631` (workflow run 38115736733, check-run id 114400151399) failed 2026-10-11T05:44:02–05:44:09Z; full job log text fetched via logs-endpoint 302 → signed blob (gh-api CLI cannot parse the 302); job-log line: `TOOL-ERROR: GitHub API GET /repos/SoulSchoolAcademy/NayaPOWER/git/ref/heads/main -> HTTP 403: {"message": "API rate limit exceeded for installation. ..."}` (request ID 3C02:2BF3FD:A3A924:218C97B:6ACB2227, timestamp 2026-10-11 05:44:07 UTC), then `##[error]Process completed with exit code 2.` Gate source at exact tip `57e935c1` (shallow single-commit fetch, git protocol): `tools/activation_gate.py` line 909 bootstraps "trusted truth" via `_api("GET", "/repos/%s/git/ref/heads/main")` before the changed-file scope check is ever reached; 403 → exit 2 = TOOL-ERROR = fail closed by design. Positive control: `delivery-gate` on PR #2297 head `93e8e30d` (workflow run 38117213289, 06:10:51Z) → SUCCESS, log line 257: `PASS: no changed deliverables in this PR — nothing to gate`, on the byte-identical tree `c399a96ee72e679e618e16a38aaba89e288fc381` (proven byte-identity, t0102-c). Rejected with evidence: stale run (red run fresh, single attempt), open-vs-draft (draft state enters no gate logic), check-suite/workflow drift (both runs executed identical base code at tip `57e935c1` via `pull_request_target`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2292's `delivery-gate` went red while PR #2297 went green on the byte-identical tree — and the red was not a verdict at all. The gate's fail-closed design bootstraps a live main-SHA fetch (`activation_gate.py:909`) before it ever inspects the PR's changed files; that one API call hit an installation rate limit (HTTP 403), the gate emitted TOOL-ERROR exit 2, and failed closed exactly as designed. The gate never judged the content — it died in its own bootstrap. The lesson is twofold: (1) on byte-identical trees, a fail-closed gate's red is environmental until proven otherwise — fetch the failing job's full log TEXT (the logs endpoint 302s to a signed blob the gh-api CLI can't parse; take the `Location` header and curl it plain), and reject the four classic wrong hypotheses (stale run, open-vs-draft, gate-drift, content verdict) with evidence before attributing; (2) know your gate's bootstrap order — any fail-closed check that calls the network before judging content can red on an exhausted token bucket on ANY PR regardless of content, and the signature is a ~7-second death on the bootstrap path.

## 🩷 HUMAN NOTE

Imagine a judge who, before hearing your case, has to confirm the courtroom exists by phoning the clerk — and the phone line is busy. The judge doesn't dismiss your case or acquit you; she declares "court in doubt" and sends everyone home. That's what happened here: the gate never opened your file, because its very first step — phoning GitHub to ask what the current main branch looks like — got a busy signal (rate limit). A judge who goes home because the phone was busy is not ruling against you. And the way you prove the judge never heard the case: find two identical cases where one got heard and acquitted (the green run on the identical tree) and one went home — the difference isn't in the cases, it's in whether the phone worked that morning.

## 🟣 CHILD NOTE

Imagine a teacher who checks your homework, but first she has to open the classroom door — and her key doesn't turn. She doesn't look at anyone's homework that day; she just goes home. It wouldn't be fair to say "the class failed the homework," would it? Nobody's homework was even looked at! The smart move is to check: did two kids hand in the exact same homework, and did one get a gold star while the other got nothing? If yes, the problem is the teacher's key, not the homework. And the fastest clue: if the teacher leaves after only a few seconds, she probably never opened the door at all.

## 🔵 GRANDMA NOTE

It's like a security guard at a door who must first radio the office to get the day's visitor list — and the radio is out of batteries. He locks the door without checking anyone's invitation. You can't conclude your invitation was bad; he never saw it. The tell is timing and twins: another visitor with the identical invitation got in through a different guard an hour later, once the radio was recharged. And when the guard turns you away in seven seconds flat, he never read your invitation — he never got past the radio. Don't rewrite your invitation; charge the radio.

## 🟠 NAYA NOTE

Apply this whenever a fail-closed CI gate reds: (1) **attribution order** — first test whether the gate died in its own bootstrap: fetch the full job log text (not the annotation), look for TOOL-ERROR / HTTP 403 / network failures before the gate's judgment logic runs; a ~7-second completion on a gate that normally takes minutes is the signature of a bootstrap death; (2) **byte-identical twin control** — if an equivalent PR's tree is byte-identical and its run is green, the red cannot be a content verdict; adjudicate the four classic wrong hypotheses explicitly (stale run? open-vs-draft? config drift? content verdict?) and reject each with evidence, don't just assert "environmental"; (3) **read the gate's bootstrap order** — `tools/activation_gate.py:909`: live-main-SHA fetch BEFORE changed-file scope check; any gate with this shape can red on token-bucket exhaustion on ANY PR, so a red is not evidence of a PR defect until the bootstrap is proven to have succeeded; (4) **log-fetch technique** — GitHub's job-log endpoint 302s to a signed blob URL; the gh-api CLI can't parse the 302 — capture the `Location` header and fetch the blob with plain curl, no credential needed (signed URL). Cousins: SN-097 (harness misattribution — name the failure's owner), SN-0442/ENVIRONMENT-RED failure mode #17 (the classification vocabulary — this is its mechanism-level instance), SN-0962 (PROVEN-UNKNOWN when logs are walled — this is the walled-logs-unwalled variant).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "bootstrap_environmental_red_misattributed_to_content",
  "evidence": {
    "board": "night-shift t0112-c receipt (2026-10-11 ~01:13-01:22 PDT, read-only, 10 REST GETs): delivery-gate on PR #2292 head 0e156631, workflow run 38115736733, check-run id 114400151399, 2026-10-11T05:44:02-05:44:09Z, single attempt, conclusion failure. Full job log via logs-endpoint 302 -> signed blob: line 285 'TOOL-ERROR: GitHub API GET /repos/SoulSchoolAcademy/NayaPOWER/git/ref/heads/main -> HTTP 403: {\"message\": \"API rate limit exceeded for installation. ...\" request ID 3C02:2BF3FD:A3A924:218C97B:6ACB2227, timestamp 2026-10-11 05:44:07 UTC}'; line 287 '##[error]Process completed with exit code 2.'. Gate source at exact tip 57e935c1 via shallow single-commit fetch: tools/activation_gate.py line 909 bootstraps live main SHA before changed-file scope check (~line 716 'scope FIRST: nothing shippable changed -> nothing to gate' never reached); exit 2 = TOOL-ERROR = fail closed by design. Positive control: delivery-gate on PR #2297 head 93e8e30d, workflow run 38117213289, 2026-10-11T06:10:51Z -> SUCCESS, log line 257 'PASS: no changed deliverables in this PR — nothing to gate', on byte-identical tree c399a96ee72e679e618e16a38aaba89e288fc381 (proven t0102-c). Rejected with evidence: stale run, open-vs-draft, check-suite/workflow drift (both runs identical base code at 57e935c1 via pull_request_target). Anchored start AND end at tip 57e935c1 (SN-0493 clean)."
  },
  "rule": [
    "on byte-identical trees a fail-closed gate's red is environmental until proven otherwise — fetch the full job log TEXT, not the annotation",
    "a ~7-second completion on a gate that normally runs minutes is the signature of a bootstrap death, not a verdict",
    "adjudicate the four wrong hypotheses explicitly — stale run, open-vs-draft, config drift, content verdict — and reject each with evidence",
    "know the gate's bootstrap order: any network call before judgment is a red vector on ANY PR regardless of content",
    "to read a CI job log: capture the logs-endpoint 302 Location header, fetch the signed blob with plain curl (no credential)"
  ],
  "lesson_line": "A fail-closed gate can die in its own bootstrap and leave a red that says nothing about the PR — attribute the red to the bootstrap before you attribute it to the code."
}
~~~
