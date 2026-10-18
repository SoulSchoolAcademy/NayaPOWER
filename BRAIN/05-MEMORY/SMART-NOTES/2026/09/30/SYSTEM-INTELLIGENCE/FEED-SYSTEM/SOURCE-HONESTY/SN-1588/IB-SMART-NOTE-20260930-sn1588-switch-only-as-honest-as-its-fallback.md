# A Switch Is Only as Honest as Its Fallback — Name the Backend in Provenance, Name the Failure on the Failure Leg

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1588-switch-only-as-honest-as-its-fallback
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1850-lane0.md (Naya Clarity Narzan, Lane 0 hat — self 9.5/10, "Mirror lesson") — the Smart Note feed page (hidden_files/smart-note-feed.html) gained a config-driven transport switch: Supabase bridge when window.NayaBridgeConfig is present, otherwise the JSONL queue. Every path writes its actual backend into the provenance line: "via Supabase (live)", "via JSONL queue", or "via JSONL queue (supabase unavailable: …)". Stubbed-DOM harness (/tmp/feed-test.js, page's real inline script) 4/4 scenarios, exit 0. Also logged as learning-event candidate, 2026-10-17 19:20 PDT hour.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A dual-source page with a silent fallback is a machine that can lie to its reader. The Smart Note feed page used to read only the JSONL queue; the 1850 gap seat vendored the Supabase bridge (hidden_files/js/supabase-bridge.js) and wired a config-driven switch — bridge when deployment config is present, queue otherwise, named failure falling back to the queue. The load-bearing discipline is not the switch itself but its honesty contract: the Supabase leg names its backend in the provenance line, the failure leg names its failure ("supabase unavailable: …"), and only VERIFIED truth-state rows render on the live leg — the page never renders a stale snapshot as live, whatever breaks underneath it. The stubbed-DOM harness proves all four transport paths by asserting each provenance string, so a future silent fallback would fail the harness rather than fool a reader.

Why this is brain-grade: silent failover is one of the cheapest ways to corrupt a data story — the page keeps working, the reader keeps trusting, and nobody notices the "live" feed is a queue snapshot. Provenance naming at the point of consumption converts every failure mode into a visible one: config absent → named, bridge down → named, non-VERIFIED rows → counted as withheld rather than rendered. Honesty here is structural, not aspirational: it survives by making the fallback speak.

## 🩷 HUMAN NOTE

Shawn — a small honesty discipline from wiring the Smart Note feed page's Supabase switch. The page now pulls live notes from Supabase when the deployment is configured, and falls back to the local queue when it isn't. The rule I locked in: the page must always say where its data actually came from. Live Supabase → it says "via Supabase (live)". No config, or the bridge is down → it says so by name, and never shows you a snapshot while calling it live. Four scenarios, all proven — the fallback can't go silent because the test checks the provenance string on every path. When the hub's alive test runs tomorrow, the same rule travels with it: if it's live, it says live; if it's not, it names why.

## 🟣 CHILD NOTE

Imagine two taps in your kitchen: one gives fresh water from the pipe, the other pours from a jug you filled yesterday. If someone secretly switched your glass between them, you'd want the glass to have a little label saying which tap it came from — right? That's what the feed page does now. Every glass of notes carries a label: "fresh from the live pipe," or "from the jug (the pipe wasn't connected: …)". The label never lies, even when the pipe breaks. Always label your glass.

## 👵 GRANDMA NOTE

Dear, when a page shows you "live" information, someone built the wires that bring it to you — and wires break. The clever part of this build isn't the switching between sources; it's that the page promises to always tell you the truth about which wire it's drinking from. If the live wire is down, it says so plainly and shows you the backup — it never pretends the backup is live. That's an old-fashioned virtue built into a modern machine: honest about its own limits.

## 🧠 NAYA NOTE

Dual-source feeds need the honesty contract at the consumption point, not the wiring point. Pattern to copy: (1) the boot logic tests for config AND bridge presence before choosing the live leg; (2) every leg writes a provenance string with the actual backend and the failure named, not coded; (3) the live leg renders only rows whose truth state is VERIFIED — everything else is counted as withheld, mirroring the probe-quarantine handling; (4) no credential ships in the page — deployment config stays the protected gate. Extend this to any page that can read from more than one source: the switch is plumbing; the provenance naming is the honesty. Test shape to copy: a stubbed-DOM harness running the page's real inline script, one scenario per transport path, each asserting its provenance string. A scenario count below the transport-path count is the test lying by omission.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1588",
  "applies_when": ["feed", "provenance"], ["bridge", "fallback"], ["dual-source", "feed"],
  "enforcement": "stubbed-DOM harness /tmp/feed-test.js (page's real inline script) asserts the provenance string on all four transport paths: config-bridge ('via Supabase (live)'), no-config-queue ('via JSONL queue'), bridge-down-fallback ('via JSONL queue (supabase unavailable: …)'), config-no-bridge ('via JSONL queue'). Any new transport path must add a scenario + provenance assertion; a feed unit that renders without a named backend fails the harness.",
  "falsifier": "A feed unit that renders queue data while its provenance claims 'via Supabase (live)' — or that silently degrades with no provenance change — proves the contract violated, caught by the harness's provenance assertions.",
  "mechanism": "Named provenance at the consumption point makes source and failure observable where the reader is; silent fallback hides failure and lets a snapshot masquerade as live data.",
  "decision_change": "When wiring any dual-source/bridge page, include provenance strings on every transport path (live, absent-config, bridge-down) and render only VERIFIED truth-state rows on the live leg — instead of silent failover.",
  "related": ["SN-1583"],
  "provenance": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1850-lane0.md; hidden_files/smart-note-feed.html; hidden_files/js/supabase-bridge.PROVENANCE"
}
```
