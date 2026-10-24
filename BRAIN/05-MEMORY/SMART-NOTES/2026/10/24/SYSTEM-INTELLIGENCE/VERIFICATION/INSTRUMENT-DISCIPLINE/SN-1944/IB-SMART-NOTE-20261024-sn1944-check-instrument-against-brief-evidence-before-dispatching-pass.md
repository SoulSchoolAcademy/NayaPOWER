**Intelligent Block:** IB-SMART-NOTE-20261024-sn1944-check-instrument-against-brief-evidence-before-dispatching-pass
**Smart Note:** SN-1944
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/gap-gap-t1530-lane12.md (Mirror lesson + ten-thing accounting item 10 FAILED + next action: "A page-text pass must NOT be re-filed for this gap")

## ✦ IN A NUTSHELL

Check the instrument against the brief's evidence list before dispatching the pass — a page-text browser view cannot supply network-layer evidence, and re-running it only re-observes the same unknown. gap-gap-t1530-lane12 was filed to deliver instrumented browser evidence (loaded asset URLs, response statuses, cache headers, service-worker state, storage contents, from a fresh profile with a cache-bypassing hard reload) for the live sidebar's source. The browser views used expose rendered page text only, so that leg failed — the third page-text pass to reproduce the same unidentified sidebar source and the same no-navigation Your Connections click. The receipt's verdict line, not its footnotes, names the failure, and its next action narrows from "another browser pass" to "a network-instrumented pass." The rule going forward: every future browser brief gets its DoD evidence list checked against what the browser views actually expose before the pass starts — a DoD item no view exposes is re-scoped to a network-instrumented pass or struck, never filed as a page-text pass. A measurement names its instrument, and an instrument that cannot see the subject reports its blindness, not the subject's absence.

## 🩷 HUMAN NOTE

A team needed to know where a website's sidebar really came from — was it the deployed code, a stale saved copy, or something else? They sent a worker to look, but the only tool she had showed her the words on the page, not the behind-the-scenes details (which files loaded, whether they came from cache, what the browser remembered). She came back with the same answer as the two workers before her: the sidebar looks the same, the button still does nothing visible, and where it comes from is still unknown. Three trips, same unknown — because the tool was never able to answer the question. The lesson: before you send someone on a job, check that their tool can actually produce the evidence the job demands. If the job needs network details and the tool only shows page words, don't send that worker — send the one with the network tools, or change the job. A tool that can't see the thing should say "I can't see it," not pretend the thing isn't there.

## 🟣 CHILD NOTE

Imagine asking a friend to tell you what color socks someone is wearing — but your friend can only see the person from the shoulders up! No matter how many times you ask, your friend will never see the socks. That is what happened here: three workers in a row were asked to find out where a website's sidebar came from, but their tool could only show the words on the page — not the hidden details like which files loaded or whether they came from saved copies. Each time, the answer was the same "we still don't know!" The lesson: before you start a job, check whether your tool can even see what you are asking about. If it can't, pick a different tool — don't just ask again and again hoping the answer appears!

## 🔵 GRANDMA NOTE

Dear, imagine sending someone to check whether the oven is hot, but only giving them a thermometer that measures the room, not the oven. They will come back three times saying "the room feels fine" — and you will still not know about the oven. That is exactly what happened: the job needed network details (which files loaded, cache headers, what the browser stored), but the tool only showed page words. Three passes, same unknown. The lesson is simple and saves real work: before dispatching any checking pass, match the job's evidence list against what the tool can actually show. If the tool cannot show it, say so up front and send the right instrument — a network-instrumented pass — instead of burning another trip that can only re-observe the same unknown. And when a tool's limits are the finding, put that in the verdict line where the next person will see it, not buried in the footnotes.

## 🟠 NAYA NOTE

The instrument here is the pre-dispatch evidence-capability check, and the failure it prevents is instrument-blind re-filing: spending passes on a DoD the dispatched tool cannot satisfy by construction. Page-text browser views expose rendered text only — no asset URLs, no response statuses, no cache headers, no service-worker state, no storage contents — so a brief whose DoD names network-layer evidence and whose instrument is a page-text pass is unsatisfiable before it starts. gap-gap-t1530 proved it three times over: same 14-room sidebar, same no-navigation click, same UNDETERMINED source, with the only new information being the limitation list itself. The discipline is cheap and mechanical: DoD evidence list vs. instrument's exposed evidence, checked before dispatch. Any future browser brief that files a page-text pass for network-layer evidence should be returned as unfileable, and any receipt that hides an unmet DoD item in its footnotes instead of its verdict line should be returned as incomplete — because the next seat reads the verdict line and re-files the doomed pass. Cousin: SN-1942 (check deploy currency before grading code) — both gate a verdict on its prerequisite evidence; this one gates the pass itself on the instrument's capability.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1944",
  "title": "Check the instrument against the brief's evidence list before dispatching the pass — a page-text view cannot supply network-layer evidence.",
  "applies_when": ["browser", "verification", "measurement", "lane-executor", "dispatch"],
  "enforcement": "Before a browser pass is dispatched, the brief's DoD evidence list is checked against the evidence the browser views actually expose; a DoD item no view exposes is re-scoped to a network-instrumented pass (fresh profile, cache cleared, hard reload with cache disabled, asset URLs, response statuses, cache headers, service-worker state, storage contents, console log) or struck — a page-text pass is never filed for network-layer evidence, and a receipt that meets no DoD item states the instrument limit in its verdict line, not its footnotes.",
  "decision_change": "Future browser briefs do not file page-text passes for network-layer evidence — after gap-gap-t1530-lane12, a DoD naming asset URLs, cache headers, or service-worker state routes to a network-instrumented pass first, instead of burning a tick re-observing the same unknown a third time.",
  "falsifiability": "Falsified if the browser views are proven to expose network-layer evidence (asset URLs, response statuses, cache headers, service-worker registration/control state) — then the pre-dispatch check adds nothing and page-text passes can satisfy such DoDs. Weakened if pre-dispatch checks repeatedly confirm the views expose every DoD item asked.",
  "mechanism": "Page-text browser views expose rendered page text only; they have no channel to network-layer facts (loaded document/script asset URLs, response statuses, cache age/ETag, from-cache vs network status, service-worker state, storage contents). A DoD demanding those facts from that instrument is unsatisfiable by construction, so re-running the pass cannot change the verdict — it can only re-observe the same unknown while consuming a tick. Checking capability before dispatch converts an unsatisfiable pass into a correctly-instrumented one.",
  "evidence": ["twelve-lane-receipts/gap-gap-t1530-lane12.md (Mirror: 'a measurement names its instrument, and an instrument that cannot see the subject reports its blindness, not the subject's absence'; ten-thing accounting item 10 FAILED; verdict 'gap NOT fully closed'; next action: 'A page-text pass must NOT be re-filed for this gap')"]
}
```
