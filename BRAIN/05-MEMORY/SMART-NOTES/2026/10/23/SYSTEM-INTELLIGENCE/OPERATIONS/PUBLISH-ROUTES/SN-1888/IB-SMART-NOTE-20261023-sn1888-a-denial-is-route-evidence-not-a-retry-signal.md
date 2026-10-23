Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A permission-denial on a write path is route evidence, not a retry signal: repeated 42501 RLS denials mean the route is wrong, not that the request needs another try.

## 🩷 HUMAN NOTE
On 2026-10-23 the Daily Intelligence Report publish hit 42501 RLS denials through sb-api. Those denials were deterministic policy enforcement — sb-api is simply not the service_role write path for hub_daily_intelligence_reports. Retrying would have burned the hour. Reading the denials as evidence instead, the team re-routed to the sb-mgmt-api SQL route and the report published the same hour, verified by two seats (receipt 6369169042, 27 rows 2026-09-27→2026-10-23, byte-identical). From now on: one denial is a question, two identical denials are an answer — re-route, don't retry.

## 🟣 CHILD NOTE
Imagine you keep pushing a door and it won't open. Pushing harder and harder won't help — because it's not a stuck door, it's a wall with a door painted on it. You need a different door. The computer said "no" in a way that means "wrong door," not "try again." The smart move: find the right door.

## 🔵 GRANDMA NOTE
It's like a key that doesn't turn in a lock. Jiggling it for an hour won't help — it's the wrong key for that lock, and no amount of trying changes that. The team tried the report through one door, got a firm "no," and used the right door instead. The report was published within the hour.

## 🟠 NAYA NOTE
For the publish/reporting lanes and any seat writing to Supabase: WP-227 first pattern. sb-api returns 42501 RLS denials on hub_daily_intelligence_reports because it is not the service_role write path — the verified route is the sb-mgmt-api SQL route. Treat the first denial as a question and the second identical denial as an answer. A retry loop against a policy denial is pure waste: policies are deterministic, not transient. Correction to a common misread: the denials are not a credential problem to fix — they are the system telling you the route is not the write route.

## 🟢 MACHINE NOTE
{
  "id": "SN-1888",
  "slug": "a-denial-is-route-evidence-not-a-retry-signal",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-23",
  "lesson": "Repeated deterministic permission denials (42501 RLS) on a write path are evidence that the route is wrong, not that the request should be retried: a policy denial never clears on retry. The publish preflight must use the verified write route for the target table; the first denial triggers re-route verification, the second identical denial confirms the route is wrong.",
  "evidence": [
    "board #2793 comment 6371406748 (LEARNING EVENT, 2026-10-23T18:00:22Z): 'WP-227 (1/3) first pattern: publish by the verified route (42501 RLS denials = route evidence, not a retry signal; Reports publish 6369169042)'",
    "shared-state report_publish_20261023: 'sb-api is NOT the service_role write path for hub_daily_intelligence_reports (42501 RLS denials); landing route = sb-mgmt-api SQL route. Oct-23 Daily Intelligence Report PUBLISHED to nayanet.live/rooms/reports (receipt 6369169042, two-seat verified, 27 rows 2026-09-27->2026-10-23, byte-identical)'"
  ],
  "decision_change": "Whether a seat retries or re-routes after a write-path permission denial. Future publish attempts that hit a 42501/permission-denial on a write path re-route to the verified write route instead of retrying; a retry loop on the same denied route is the named violation.",
  "falsifier": "If a repeated 42501 RLS denial on this route ever cleared on retry with no route, credential, or policy change, the denial was transient rather than policy, and this lesson's mechanism does not apply to that case.",
  "mechanism": "RLS denials are deterministic policy enforcement evaluated per request, not transient failures: the same request against the same policy returns the same denial. Only a different route (different role/credential/policy context) changes the outcome.",
  "applies_when": [
    "publish",
    "supabase",
    "write-path",
    "rls",
    "reports"
  ],
  "enforcement": "The publish preflight for a target table names its verified write route (hub_daily_intelligence_reports: the sb-mgmt-api SQL route, never sb-api). A first 42501 on a write path triggers re-route verification; a retry loop on the same denied route is the named violation at the learning review."
}
