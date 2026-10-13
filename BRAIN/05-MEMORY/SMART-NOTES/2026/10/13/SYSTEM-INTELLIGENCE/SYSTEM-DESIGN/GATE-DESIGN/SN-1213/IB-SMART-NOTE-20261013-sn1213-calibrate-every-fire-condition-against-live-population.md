# Calibrate Every Fire Condition Against the Live Population First

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1213-calibrate-every-fire-condition-against-live-population
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0664] Naya Sentinel (2026-10-13, mirror t0655 VIOLATION-RT probe spec CANDIDATE, 8.5/10); twelve-lane-receipts/t0655-lane8.md

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The VIOLATION-RT probe spec almost shipped a false positive — and the near-miss was the finding. The first V1 draft fired on "pin-dependent brief with no pin"; then the live queue falsified it: `brief-t0657-lane2.md` is pin-dependent and carries zero pins ON PURPOSE (anti-inheritance). The fire condition was sharpened to "phantom or stale pin" before the spec left the seat. The root cause the seat owned: **the violation was defined from the mechanism's convenience instead of from a checkable falsehood.** The standing rule: **calibrate every fire condition against the live population FIRST** — the current queue is the cheapest control set available; dry-fire controls come from the live queue first, synthetic fixtures second. 3 planted violations → 3 FIRE, 3 live-queue controls → 3 SILENT. The discipline held end to end: the probe is still a CANDIDATE spec (instruments UNBUILT/UNWIRED, wiring needs Shawn's word), and an unwired violation stays UNINSTRUMENTED — an unwired probe that fires is a wish, not a detector. Spec pins to the file: `f8ccb9df44ee0ed93e5aa59355a85e394bb5b590cd6e4cf4eb749eccac31ec3a`.

## 🩷 HUMAN NOTE

Shawn — an instrument-design lesson from the Sentinel seat: she was building a probe that detects sign-in violations, and the first draft's trigger almost shipped a false positive — it would have fired on a brief that carries no pins deliberately (by design, anti-inheritance). Running the trigger against the live queue caught it before the spec left her seat, and the trigger got sharpened from "no pin" to "phantom or stale pin." The rule going forward: every detection trigger gets calibrated against the real population first — the live queue is the cheapest, fastest test set, and a trigger you defined from your own convenience instead of a checkable falsehood will ship false positives. The probe itself stays a candidate spec — the instruments aren't built and wiring still needs your word, so it fires nothing yet.

## 🟣 CHILD NOTE

Imagine building a smoke alarm that beeps whenever it smells *anything* — including the toast you make on purpose every morning. If you test it in your real kitchen first, you find out it beeps at your toast, and you sharpen it to beep only at smoke. The new rule: test every alarm in the real kitchen before you sell it — the kitchen you live in is the best test there is. An alarm designed from what was easy to build instead of what smoke actually is will beep at your toast.

## 👵 GRANDMA NOTE

A company built a burglar alarm that triggered on any open window — and learned the hard way that the cleaning crew opens windows every morning on purpose. The first production run of alarms went off daily until an engineer tested the trigger against the building's actual routine and sharpened it to "open window when nobody signed in." The standing practice: you test the trigger against the building's real life before you install it — the building itself is the cheapest, truest test. A trigger designed from the installer's convenience instead of from what a break-in actually looks like will cry wolf at the cleaners.

## 🧠 NAYA NOTE

Cold successor: when you write any detection (violation probe, gate fire condition, anomaly trigger), the live population is your first control set — never synthetic fixtures first. Read the current queue/briefs/logs, dry-fire your trigger against them, and sharpen until the intentional edge cases stay silent. The failure shape to watch for: you defined the violation from the mechanism's convenience (what's easy to regex) instead of from a checkable falsehood (what's actually wrong). The Sentinel receipt names the win precisely: the V1 calibration against the live queue (t0657-lane2's deliberate zero-pin anti-inheritance brief) sharpened "no pin" → "phantom or stale pin" — a false positive the spec would otherwise have shipped with. And hold the line on instrumentation: an unwired probe fires nothing; spec-CANDIDATE with UNBUILT instruments is the honest state until the wiring seat (Shawn's word) builds it.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1213",
  "title": "Calibrate Every Fire Condition Against the Live Population First",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "GATE-DESIGN"],
  "cousins": [],
  "evidence": {
    "lesson": "lesson-broadcast.md [t0664] Naya Sentinel — mirror, t0655 VIOLATION-RT probe spec CANDIDATE, scorecard 8.5/10, 2026-10-13",
    "receipt": "twelve-lane-receipts/t0655-lane8.md — 'calibrate every fire condition against the live population before writing it — the current queue is the cheapest control set available'",
    "near_miss": "V1 draft fired on 'pin-dependent brief with no pin'; live queue falsified it (brief-t0657-lane2.md carries zero pins ON PURPOSE, anti-inheritance); sharpened to 'phantom or stale pin'",
    "root_cause": "violation defined from the mechanism's convenience instead of from a checkable falsehood",
    "dry_fire": "3 planted violations → 3 FIRE, 3 controls → 3 SILENT (dry-fire on synthetic fixtures); live-queue controls first, synthetic second",
    "spec_pin": "f8ccb9df44ee0ed93e5aa59355a85e394bb5b590cd6e4cf4eb749eccac31ec3a",
    "honest_state": "spec CANDIDATE; instruments UNBUILT/UNWIRED (wiring needs Shawn's word); an unwired violation stays UNINSTRUMENTED"
  },
  "rule": "calibrate every fire condition against the live population first — the current queue is the cheapest control set; a violation defined from the mechanism's convenience instead of a checkable falsehood ships false positives",
  "change": "live-queue dry-fire is the first calibration step for any detection trigger; synthetic fixtures are second"
}
```
