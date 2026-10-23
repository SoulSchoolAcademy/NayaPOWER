Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The hub-sync liveness alarm failed with a JSON parse error ("Expecting value: line 1 column 1 char 0") and the first reading blamed the writer. The Nitro sync lane's independent receipt (board #2793, comment 6370911469, 2026-10-23 17:34Z) proved verdict BOTH: writer-down AND endpoint-wrong. GET https://nayanet.live/sync-heartbeat.json returned HTTP 200 — as text/html, a 5.17MB copy of the Hub monolith, not heartbeat JSON. That 200 is exactly what produced the parse failure in the scheduled deploy runs (39990909081 at 16:56Z, 39949936268 at 11:59Z). Meanwhile the actual writer was alive: watcher heartbeat 2026-10-23T17:30:58Z, errors 0. An HTTP 200 is not a content contract. A liveness probe answers three different questions — did the server respond (status), did it serve the right artifact (content-type), did the writer produce valid bytes (parse) — and collapsing all three into one parse error mis-routes a serving/routing failure to the writer's owner. The decision-change: when a probe fails on parse, triage reads the endpoint's status and content-type before declaring the writer dead; the repair routes to the hub/deploy lane first, not the sync lane. Falsifier: if a future probe failure's root cause lies in none of the three legs, the three-leg model is incomplete and must be extended. Companion to SN-1883 (which fixed the oracle's authorship): this fixes the alarm's reading of the endpoint.

## 🩷 HUMAN NOTE

Shawn — the deploy gate kept failing and every alarm pointed at the thing that writes the heartbeat. Turns out the writer was fine and on time. The problem was the website itself: the heartbeat address was handing out the Hub's front page — five megabytes of it — stamped "success." The checker tried to read it as a heartbeat, choked, and blamed the writer. The rule from here: "the server answered" is not "the server answered correctly." When a health check fails, we now check three things separately — did it answer, did it hand over the right kind of file, and is the file valid — because those are three different people who need to fix it.

## 🟣 CHILD NOTE

Imagine you ask your friend "are you okay?" and a stranger answers "yes" — in a different language you don't speak. You'd think your friend is in trouble, but really your friend is fine; the wrong person answered. That's what happened here: the health check asked the heartbeat address "are you alive?", the website's front page answered "200 OK" in the wrong language (a whole webpage instead of a tiny heartbeat file), and the checker blamed the heartbeat writer. The fix: check WHO answered (the right address?), WHAT language they spoke (the right kind of file?), and only then whether the message makes sense.

## 🔵 GRANDMA NOTE

Think of a doctor's office that faxes your test results every morning. One day the fax machine starts sending the clinic's brochure instead of your results — with a perfectly clear "transmission successful" stamp. The nurse sees a failed delivery, blames the lab, and the lab insists the results were ready on time. Both are right about their part. The real fault is the fax machine sending the wrong document. From now on the nurse checks three things: did the fax arrive, is it the results form (not a brochure), and are the numbers readable. Each check points to a different person to call.

## 🟠 NAYA NOTE

For the lanes: this is the endpoint-wrong half of the verdict-BOTH receipt (6370911469); SN-1883 already covers the oracle-authorship half (the 1970 seed). The liveness preflight (tools/hub_sync_heartbeat.py) must surface three separate legs — HTTP status, content-type, parse result — each with its owner: status failure goes to the hub/deploy lane (route down); content-type mismatch (expected application/json, got text/html) goes to the hub/deploy lane (route serving the monolith instead of the artifact — a production route surface, which needs Shawn's word per the receipt); parse failure on a correct content-type goes to the sync/writer lane. Until the three-leg report exists, any "no heartbeat readable" whose body is more than 1KB of HTML is presumed endpoint-wrong, not writer-down, and routes to the deploy lane first. Do not weaken the --max-age 600 fail-closed posture (the receipt's standing classification: P1 observability/liveness blocker, NOT a proven Hub-sync outage).

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1884-a-200-with-wrong-content-is-not-a-green",
  "lesson": "An HTTP 200 is not a content contract: a liveness probe answers three different questions — did the server respond (status), did it serve the right artifact (content-type), did the writer produce valid bytes (parse) — and collapsing all three into one parse error mis-routes a serving/routing failure to the writer's owner. Evidence: board #2793 comment 6370911469 (Nitro sync lane owner receipt, 2026-10-23T17:34:38Z, verdict BOTH): GET https://nayanet.live/sync-heartbeat.json -> HTTP 200 text/html 5.17MB (the Hub monolith, not heartbeat JSON) — explains the 'Expecting value: line 1 column 1 char 0' parse failure in scheduled deploy runs 39990909081 (16:56Z) and 39949936268 (11:59Z); no beat writer in repo; sync cycles RUNNING (watcher heartbeat 2026-10-23T17:30:58Z, errors 0). The writer was alive; the endpoint served the wrong artifact with a success stamp. Decision-change: when a probe fails on parse, triage reads status + content-type before declaring the writer dead; repair routes to the hub/deploy lane first. Falsifier: a future probe failure whose root cause lies in none of the three legs makes the model incomplete and extends it. Companion to SN-1883 (oracle authorship).",
  "applies_when": ["liveness", "probe-design", "alarm-triage", "hub", "sync", "deploy-gate", "http", "content-contract"],
  "enforcement": "The liveness check (tools/hub_sync_heartbeat.py) must report HTTP status, content-type, and parse result as three separate fields with three separate owners (status -> hub/deploy lane; content-type mismatch -> hub/deploy lane; parse failure on correct content-type -> sync/writer lane). A failure surfaced as a bare parse error without the content-type leg is re-triaged per this note: any 'no heartbeat readable' whose body is more than 1KB of HTML is presumed endpoint-wrong and routes to the deploy lane first. The hub/deploy lane asserts /sync-heartbeat.json serves application/json, not text/html. The --max-age 600 fail-closed posture is not weakened.",
  "evidence": ["board #2793 comment 6370911469 (Nitro sync lane owner receipt, 2026-10-23T17:34:38Z): verdict BOTH — writer-down AND endpoint-wrong; GET https://nayanet.live/sync-heartbeat.json -> HTTP 200 text/html 5.17MB (Hub monolith); explains parse failure in runs 39990909081 / 39949936268; watcher heartbeat 2026-10-23T17:30:58Z errors 0", "board #2793 comment 6370281593 (independent continuity audit, 2026-10-23T17:00:54Z): P1 observability/liveness blocker; repo HUB/sync-heartbeat.json is the 1970 seed"],
  "falsifier": "A future probe failure whose root cause lies in none of the three legs (status, content-type, parse) — then the three-leg model is incomplete and must be extended.",
  "related": ["SN-1883 (oracle authorship: heartbeat must be written by the living process)"]
}
```
