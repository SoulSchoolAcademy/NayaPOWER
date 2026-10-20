# A Daily-Firing Alert on a Legitimate Mechanism Must Be Ratified or Rerouted

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1737-direct-push-alert-ratify-or-reroute
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Watch-4f fired DIRECT PUSH alerts on five direct-to-main pushes in about 90 minutes — four of them the projection pipeline's normal operation (canonical Smart Note projections IB-000039 through IB-000041) plus two Smart Note pushes (SN-0801, SN-0802). An alert that fires repeatedly on a legitimate mechanism without action is miscalibrated: ratify the path or reroute it. Unactioned alerts desensitize the watch and bury the genuine bypasses they exist to catch.

## 🩷 HUMAN NOTE

Hey Shawn — guess what I noticed: our direct-push alarm fired five times today on pushes that are actually the normal machinery doing its job (the projection pipeline filing Smart Notes to main). An alarm nobody acts on becomes wallpaper — and then the one real bypass hides in the noise. What I filed: when the same alarm fires three times on the same legitimate mechanism with no action, stop firing and open the real question instead — is this path approved as-is, or should it go through the normal merge lane? You decide once; the alarm learns. That's what the watch needs, and why.

## 🟣 CHILD NOTE

If a fire alarm goes off every day at lunchtime because someone is cooking, you don't keep running outside — you check whether the cooking is allowed, and if it is, you move the alarm. Same with our push alarm: it's firing on normal work, so we either approve the work or move the alarm.

## 🔵 GRANDMA NOTE

We have an alarm that watches for anyone putting changes straight into the main record. Lately it's been going off for our own normal machinery — the part that files Smart Notes. An alarm that cries wolf teaches everyone to ignore it, which is dangerous. The fix: either formally approve that machinery's path or route it through the usual checks — and quiet the alarm accordingly.

## 🟠 NAYA NOTE

Watch-4f counts consecutive unactioned DIRECT PUSH alerts per mechanism (author plus path pattern, e.g. nayanet[bot] projection pushes). At 3 or more on the same mechanism with zero action, the watch STOPS firing identical alerts and the director pass opens a ratify-or-reroute adjudication (main seat): either the mechanism's direct-to-main path is ratified (with its self-asserted Transaction, Authority-grant, and Idempotency fields validated) or it is rerouted through the merge lane. The watch's rule is updated within one tick of the adjudication. New mechanisms still alert fresh.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1737-direct-push-alert-ratify-or-reroute",
  "title": "A daily-firing alert on a legitimate mechanism must be ratified or rerouted",
  "lesson": "An alert that fires repeatedly on a legitimate mechanism without action is miscalibrated: ratify the path or reroute it. 2026-10-20: watch-4f fired DIRECT PUSH alerts on 5 direct-to-main pushes in ~90 min - nayanet[bot] projection pushes IB-000039/040/041 (the projection pipeline's normal operation) plus SN-0801/SN-0802 Smart Note pushes. The oath branch (naya4/oath-of-honor-20261020) shows the contrast: routed via branch, merge lane owns it. Main-seat adjudication is owed: ratify the projection pipeline's direct-to-main path (validating its self-asserted Transaction/Authority-grant/Idempotency fields) or route it via the merge lane like the oath branch.",
  "applies_when": [["watch", "4f"], ["push", "direct-to-main"]],
  "enforcement": "Watch-4f counts consecutive unactioned DIRECT PUSH alerts per mechanism (author+path pattern). At >=3 on the same mechanism with zero action, the watch stops firing identical alerts and the director pass opens a ratify-or-reroute adjudication request to the main seat; the watch's alert rule is updated within one tick of the adjudication. New mechanisms still alert fresh.",
  "evidence": ["shared-state.json:direct_push_20261020_1640 (2 direct pushes 2026-10-20T16:40:10Z: nayanet[bot] projection IB-000039, SN-0801)", "shared-state.json:director_tick_20261020_1008 tip chain (3 more direct pushes by 17:12Z: SN-0802, IB-000040, IB-000041)", "branch naya4/oath-of-honor-20261020 (contrast: routed via branch, merge lane owns - NOT merged to main)"],
  "decision_change": "The next projection-pipeline direct push: the director proposes standing ratification of the direct path (with self-asserted Transaction/Authority/Idempotency fields validated) vs rerouting through the merge lane - instead of firing another identical unactioned alert.",
  "falsifiability": "A direct projection push is later shown to carry unauthorized content or bypass a protected gate -> falsified: the path was not legitimate and the alerts were substantive. Shawn ratifies the path or it is rerouted -> corroborated.",
  "mechanism": "Alert fatigue: an alert that fires repeatedly on a legitimate mechanism without action desensitizes every watcher; the genuine-bypass signal the alert exists for gets buried in legitimate-path noise. Calibration (ratify the path or reroute the work) restores the alert's signal.",
  "captured_date": "2026-10-20",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/WATCHER-INTEGRITY"
}
```
