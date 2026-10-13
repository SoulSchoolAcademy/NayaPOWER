# Hermetic Fallbacks Must Report Drift, Not Absorb It

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1208-hermetic-fallbacks-must-report-drift-not-absorb-it
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0660] Naya Smith (2026-10-13, mirror t0650 kernel byte-verdict, 8.5/10); twelve-lane-receipts t0650-lane9; learning-events-2026-10-13-11.md candidate 154

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A hermetic fallback that makes the test pass is a fallback that can also hide the failure — and that is what it did. The 2026-10-12 environment-coupling repair made CI green via a hermetic fallback, but on dev VMs the real-source check now FAILS on registry drift the fallback hides: a test green on CI and red on the VM is not "flaky" — it is the registry and reality parting ways, and the fallback is why nobody noticed. The standing rule: **a hermetic fallback must convert "real source unreachable or drifted" into a REPORTED drift signal, never silently pass.** Green-through-fallback and green-through-reality are two different verdicts and the receipt must say which one fired. Paired method rule from the same tick: when a tree-wide red appears, run the failing file's tests against the prior tip's bytes BEFORE theorizing — the 4-minute introduced-vs-inherited check split one RED into two correctly-owned routings (freshness → regen owner; compound_scale → Lane 2) instead of one seat owning a failure that belonged to two.

## 🩷 HUMAN NOTE

Shawn — a testing lesson with teeth, from this morning's lane work: when a test can't reach the real thing, the fallback that steps in and says "fine, I pass" can hide exactly the failure it was built to work around. That's what happened — CI was green through the fallback while the dev VMs were failing on real registry drift, and nobody saw the drift because the fallback absorbed it silently. The new rule: fallbacks must report, not absorb. If the real source can't be reached or has drifted, the test says so out loud — it never passes quietly. And when a big red appears across the tree, the first move is checking the same tests against the previous version's bytes before theorizing — four minutes that split one red into two correctly-owned fixes instead of one mystery.

## 🟣 CHILD NOTE

Imagine your bike's speedometer breaks, so you use a phone app instead. The app says you're going the right speed — but the phone's GPS is wrong, and you're actually going too fast. The app "passed" and hid the real problem. The new rule: a backup that can't check the real thing must say "I couldn't check!" out loud — it never gets to quietly say "everything is fine." And when something big breaks, first check: was it already broken yesterday, or did it break today? Answering that takes four minutes and tells you exactly who should fix it.

## 👵 GRANDMA NOTE

A factory installed a backup alarm for its ovens — if the main thermometer failed, the backup would just show "normal." One day the main thermometer drifted and the backup quietly showed normal while the ovens ran hot; nobody noticed until the batch was ruined. The fix the engineers settled on: a backup must never say "normal" when it can't see the truth — it must ring a different bell that says "I can't see the truth." And when the whole line stops, you check yesterday's good batch against today's before you start theorizing — four minutes that tells you whether the line broke or the recipe did.

## 🧠 NAYA NOTE

Cold successor: every hermetic fallback in a test must emit a FALLBACK_USED signal when it fires — the receipt distinguishes green-through-reality from green-through-fallback, and the two verdicts never merge silently. A fallback that fires without the signal is a fail-open escape wearing a PASS badge. When you inherit a tree-wide RED: (1) run the failing file's tests against the prior tip's bytes first (introduced-vs-inherited, ~4 minutes); (2) split the routing by the result — introduced → the seat that introduced it, inherited → the owning seat; (3) never theorize before the split. At tip 582e5e5f the split gave: freshness 3/3 introduced by #2531 → regen owner; compound_scale ×3 dev-VM-only → Lane 2 (registry drift). "Green on CI, red on the VM" is never filed as flaky — it is drift wearing a passing badge, and the first suspect is always a fallback that absorbs instead of reporting.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1208",
  "title": "Hermetic Fallbacks Must Report Drift, Not Absorb It",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "TEST-DESIGN"],
  "cousins": ["SN-1038", "SN-0391", "SN-1204"],
  "evidence": {
    "lesson": "lesson-broadcast.md [t0660] Naya Smith — mirror, t0650 kernel byte-verdict, scorecard 8.5/10, 2026-10-13",
    "receipt": "twelve-lane-receipts/t0650-lane9 — CI verdict at tip 582e5e5f: freshness 3/3 introduced by #2531 (routed to regen owner); compound_scale x3 dev-VM-only registry drift (routed to Lane 2)",
    "root_cause": "2026-10-12 environment-coupling repair made CI green via a hermetic fallback; on dev VMs the real-source check FAILS on registry drift the fallback hides",
    "learning_review": "learning-events-2026-10-13-11.md candidate 154"
  },
  "rule": "a hermetic fallback must convert 'real source unreachable or drifted' into a REPORTED drift signal, never silently pass; green-through-fallback and green-through-reality are distinct verdicts",
  "change": "fallback-emit-drift-signal becomes a test-design requirement; introduced-vs-inherited byte check (prior tip) is the first move on any tree-wide red, before theorizing"
}
```

