# Proof Host Build — Cloudflare worker naya-proof-host

**Goal:** serve any file from the public repo SoulSchoolAcademy/NayaPOWER as a real web page
(content-type text/html) at a plain web address, so browser checks can open a page without
file grants, Muse file links, or third-party previewers.

**Account:** NayaPOWER `b5e2a51b3e883f7722287c5f51b1196b`
**Worker name:** `naya-proof-host`
**URL shape:** `https://naya-proof-host.<subdomain>.workers.dev/?file=<path>&ref=<branch, default main>`

## Worker code
File: `~/workspace/team-nitro/proof-host/worker.js`

```js
export default {
  async fetch(request) {
    const url = new URL(request.url);
    const file = url.searchParams.get("file");
    const ref = url.searchParams.get("ref") || "main";
    if (!file) {
      return new Response("Usage: ?file=<repo path>&ref=<branch, default main>", {
        status: 400, headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    if (file.includes("..") || file.startsWith("/") || file.includes("://")) {
      return new Response("bad path", {
        status: 400, headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    const enc = (p) => p.split("/").map(encodeURIComponent).join("/");
    const gh = `https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/${enc(ref)}/${enc(file)}`;
    const res = await fetch(gh, { headers: { "User-Agent": "naya-proof-host" } });
    if (!res.ok) {
      return new Response(`GitHub ${res.status} for ${file}@${ref}`, {
        status: res.status, headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    const body = await res.arrayBuffer();
    return new Response(body, {
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "no-store",
      },
    });
  },
};
```

## Deploy steps
1. PUT worker via `deploy.py` (multipart: metadata part first, then script part
   `Content-Type: application/javascript+module`). Credential via the same
   `dynamic_credentials.add_surrogate_to_request` mechanism as `cf-api.py` —
   no token in args/env/logs. Plain `application/javascript` on the script part
   400s with error 10021 (proven 2026-11-06).
2. Enable the workers.dev route: `POST /accounts/{id}/workers/scripts/naya-proof-host/subdomain`
   with `{"enabled": true}` (PATCH is 405 on that endpoint). New workers have the
   route DISABLED by default — deployed-bytes matching does NOT catch this.
3. Verify with curl (browser User-Agent; Python-urllib default UA gets 403 error 1010
   on *.workers.dev):
   - Dashboard: `?file=DASHBOARD/index-reporting-pass1-20261105.html&ref=dashboard/defectfix-v9`
     — expect 200, text/html, 1,581,065 bytes, sha256 `adfb70c1...`
   - Personal: `?file=PERSONAL/index-personal-candidate-2-20261107.html` (main)
     — expect 200, text/html, 1,181,009 bytes, sha256 `f6d6061e...`
   - Compare against a direct raw.githubusercontent.com fetch (same bytes).

## Progress log
- 19:26Z — checkpoint created; worker.js + deploy.py written.
- 19:26Z — PUT succeeded first try after one str/bytes bug fix in deploy.py:
  worker `naya-proof-host` created 2026-11-07T19:26:20Z, deployment_id
  `ccc973a2769a4b038b8d3d8cd0e4ebd6`, has_modules true, handler fetch.
- 19:26Z — workers.dev route enabled (POST subdomain): `{"enabled": true,
  "previews_enabled": true}`. Subdomain: `nayapower` →
  **https://naya-proof-host.nayapower.workers.dev/**
- 19:27Z — first curl verify FAILED on the test, not the worker: all four curls
  died with `curl: (23) Failure writing output to destination` — the EPERM
  flake hit /tmp writes. Reran with pipes (no disk writes) per SN-2215.
- 19:27Z — VERIFIED via pipes, both files byte-identical to raw.githubusercontent.com:
  - Dashboard `?file=DASHBOARD/index-reporting-pass1-20261105.html&ref=dashboard/defectfix-v9`:
    HTTP 200, `Content-Type: text/html; charset=utf-8`, `Cache-Control: no-store`,
    1,581,065 bytes, sha256 `adfb70c1f46bd9c58c9d519bb5a67540048aeb6bd980b5314f25a0e04fb15790`
    (direct GitHub fetch: identical size + identical sha256).
  - Personal `?file=PERSONAL/index-personal-candidate-2-20261107.html` (main):
    HTTP 200, `Content-Type: text/html; charset=utf-8`, `Cache-Control: no-store`,
    1,181,009 bytes, sha256 `f6d6061e2cff1c9021082fa458d465e8c37d08f846a94d38eb259379c21cecba`
    (direct GitHub fetch: identical size + identical sha256).
  - Error paths: no `?file` → 400 usage; `../` traversal → 400 bad path;
    missing file → 404 `GitHub 404 for ...@main`.
- 19:27Z — self-scorecard found two real gaps (no content-type by extension,
  no health endpoint). Fixed in worker.js, redeployed (deployment `0bd7bb79`,
  modified 19:27:50Z), re-verified: both files identical size + sha again,
  health `200 naya-proof-host ok`, AGENTS.md serves as `text/plain`.
  No caching added on purpose: proofs must serve the CURRENT file, not a cached one.

## Ready-to-use browser-task URLs (render proof still owed — parent's browser tasks)
- Dashboard: https://naya-proof-host.nayapower.workers.dev/?file=DASHBOARD/index-reporting-pass1-20261105.html&ref=dashboard/defectfix-v9
- Personal: https://naya-proof-host.nayapower.workers.dev/?file=PERSONAL/index-personal-candidate-2-20261107.html
- Health: https://naya-proof-host.nayapower.workers.dev/health

## Self-scorecard (written before reporting back, per the brief)
**Why it is not a 10 (every reason):**
1. No browser-render proof yet — curl proves bytes + content-type, but no one has
   SEEN either page render in a real browser through this host. That is the whole
   point of the host, and it is owed (parent's browser tasks, not mine — I cannot
   run a live browser).
2. No caching — every request fetches from GitHub fresh. (Deliberate: proofs must
   serve the current file. Still a cost at scale.)
3. No rate limiting or abuse guard — anyone who finds the URL can fetch any file
   from a public repo. Harmless (repo is public), but unbounded.
4. No monitoring/alerting — if the worker breaks, nothing tells anyone.
5. No custom domain — the URL is long. A short proof.nayanet.app-style link would
   be nicer (needs DNS + a decision, not mine to take).
6. No retry/fallback if raw.githubusercontent.com is slow or down.
7. The deploy script shipped with a first-run str/bytes bug — fixed, but it means
   the script was untested before first use.
8. Error messages name the repo path (`GitHub 404 for X@main`) — trivial, but
   more than the caller needs.
9. Only the two required files verified end-to-end; broader types spot-checked
   only (AGENTS.md as text/plain).
10. No usage log — no record of who used it or what was served.

**10 things I love:**
1. It works — both files byte-identical to GitHub, correct content-type, HTTP 200.
2. Deployed in ~4 minutes from first write to verified.
3. Public repo at runtime — no token needed, no credential surface at all.
4. Deploy reused the canonical credential mechanism — no token in args/env/logs.
5. Multipart shape right (after one trivial bug fix); subdomain enable first try.
6. Error paths clean and honest (400 usage, 400 bad path, 404 passthrough).
7. Checkpoint-first worked — the build file holds everything.
8. The flake didn't stop the work — pipes instead of /tmp writes routed around it.
9. One file, ~60 lines, no dependencies, no KV, no build step.
10. Extension typing + health endpoint added and re-verified in the same pass.

**10 things I don't love:**
1. No render proof in a real browser yet (the actual purpose).
2. No caching (deliberate, but a cost).
3. No rate limit.
4. Long URL, no custom domain.
5. Deploy script had a first-run bug.
6. No health monitoring.
7. No usage log.
8. No GitHub fallback.
9. Error messages leak the repo path.
10. Only two files verified end-to-end.

**10 things to make it 10x better:**
1. Browser-render proof through it (parent's browser tasks — Dashboard + Personal).
2. Custom domain for short proof links.
3. Retry GitHub fetch once on 5xx; fallback to the Contents API (public, no token).
4. Rate limit per IP (generous, e.g. 100/min) to bound abuse.
5. Logpush or a lightweight usage counter so breakage is visible.
6. A README in this dir with the URL shape + examples, so any seat can use it
   without asking.
7. Wire it into verifier briefs as THE proof route (previewer stays as fallback).
8. Add a `?type=` override for the rare file whose extension lies.
9. Pin the worker to a GitHub commit SHA option (`?sha=`) for frozen proofs.
10. Re-verify on a schedule (hourly health + byte check) so silent breakage is caught.

**10 solutions applied / to apply right now:**
1. Content-type by extension — APPLIED, redeployed, re-verified.
2. /health endpoint — APPLIED, returns 200.
3. Re-verified both files after the redeploy — APPLIED, identical sha.
4. Ready-to-use browser-task URLs written above — APPLIED.
5. Checkpoint file complete with code, steps, results — APPLIED.
6. No caching — DECIDED AGAINST on purpose (proofs must be current).
7. Custom domain — NOT APPLIED (needs DNS + a decision; flagged for parent).
8. GitHub retry/fallback — NOT APPLIED (small value, adds complexity; listed above).
9. README — NOT APPLIED in this pass (the checkpoint file serves as the record;
   a seat-facing README is a 5-minute follow-up).
10. Rate limit / monitoring / logging — NOT APPLIED (proof tool, not production;
    flagged for parent if the host becomes permanent infrastructure).

**My score: 9/10 for the task as defined.** Everything required is done and
proven with receipts. The one point off is the browser-render proof, which I
cannot do from here — it is the parent's next step, and the URLs are ready.

