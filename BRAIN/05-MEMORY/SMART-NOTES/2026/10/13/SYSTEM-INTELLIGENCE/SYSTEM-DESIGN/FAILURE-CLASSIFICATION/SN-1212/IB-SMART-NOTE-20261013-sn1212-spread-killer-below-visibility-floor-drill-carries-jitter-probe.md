# Spread-Killer Below the Visibility Floor — Every Drill Carries a Jitter Probe

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1212-spread-killer-below-visibility-floor-drill-carries-jitter-probe
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0666] Naya Verity (2026-10-13, mirror t0657 SURGE slice (d) cold-retrieve drill re-run → HOLD, 8.5/10); twelve-lane-receipts/t0657-lane1.md

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A new failure class was named today: **spread-killer (b)** — host-level disk/CPU jitter that lives BELOW the lane-visibility floor. The signature is unmistakable once you know it: quiet 1-minute load (≤2.66) + wide cold spreads (14.7–58.3%) + a stable warm arm (0.349/0.350s) + mincore COLD on 100% of trials. The load gate cannot see this; it is not lane contention — the instrument is being shaken by something the lane can't observe. The standing rule: **every drill carries a per-run jitter probe** (one sequential 607-file read per run) so the signature becomes a measurement, not a hypothesis. And the decision rule that follows: if spread >10% persists with probe-quiet reads, the bar itself — not the environment — is the load-bearing question; that is the lanes-2/5 seat decision (dispatched t0666), not the executor's. The same tick showed the discipline in its fail-closed form: an in-bar 1.094s median was left unquoted because its 58.3% spread said the measurement was untrustworthy — a good number from a bad measurement is not a good number. Premise-rot was caught pre-measurement (the brief's 4f0c9aa8 → live 582e5e5f), so the drill re-ran on live bytes rather than producing a verdict about a dead tip.

## 🩷 HUMAN NOTE

Shawn — a new measurement failure class from the SURGE drill lane: host-level jitter the load gate can't see. The drill's cold times were swinging wildly (15–58% spread) while the machine looked quiet and the warm runs were rock-steady — the verdict went to HOLD, and the lane named the class "spread-killer (b)": disk/CPU jitter below the visibility floor. The standing fix: every drill now carries a small jitter probe (one quick sequential file read per run) so the signature becomes evidence instead of an excuse. And if the spread stays wide while the probe is quiet, the bar itself gets questioned — that's a seat decision, not an executor's call. The lane also refused to quote a good-looking median (1.094s, inside the bar) because its spread said the measurement was untrustworthy — fail closed under pressure.

## 🟣 CHILD NOTE

Imagine timing how fast you can run around the block — but sometimes a hidden headwind blows and you don't feel it, you just run slower. Your stopwatch times swing wildly while the day looks calm. A friend watching with a little wind-meter would see the gusts your body can't feel. The new rule: every timing run carries a wind-meter (a quick probe read before the real run), so wild swings become "the wind did it" — evidence, not an excuse. And if the meter says calm and the swings persist, maybe the stopwatch itself is the problem, and that's the grown-ups' decision. One more: a fast time on a shaky run doesn't count — a good number from a bad measurement is not a good number.

## 👵 GRANDMA NOTE

A kitchen tested a new oven's preheat time and the readings swung wildly — some mornings fast, some slow — while the kitchen seemed calm and the thermometer looked fine. An engineer eventually named the culprit: the building's old wiring sagged under load the kitchen couldn't see. The new procedure: every test run starts with a quick probe of the wiring, so the wild readings get a cause instead of a shrug. And if the probe says the wiring is fine and the readings still swing, the engineers stop blaming the building and question the thermometer itself. The standing lesson: when you can't trust the measurement, you don't get to keep the number.

## 🧠 NAYA NOTE

Cold successor: when a cold-retrieve (or any timing) drill shows wide cold spreads with a quiet load gate and a stable warm arm, reach for the spread-killer (b) signature first: mincore COLD on ~100% of trials + spread 15–58% + warm stable = host-level disk/CPU jitter below the lane-visibility floor, not lane contention. Do not tune the drill to average it away on your own authority — the drill must carry the jitter probe (sequential 607-file read per run); if spread >10% persists probe-quiet, route to the owning seats (lane 2/5): the bar itself is then the load-bearing question. Fail closed under pressure: never quote an in-bar median whose spread says untrustworthy (the 1.094s median at 58.3% spread was left unquoted — correct). And always premise-check the brief's tip pin before measuring: the brief's 4f0c9aa8 was dead; the live tip was 582e5e5f — a verdict measured on a dead tip is a verdict about nothing.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1212",
  "title": "Spread-Killer Below the Visibility Floor — Every Drill Carries a Jitter Probe",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "FAILURE-CLASSIFICATION"],
  "cousins": [],
  "evidence": {
    "lesson": "lesson-broadcast.md [t0666] Naya Verity — mirror, t0657 SURGE slice (d) cold-retrieve drill re-run → HOLD, scorecard 8.5/10, 2026-10-13",
    "receipt": "twelve-lane-receipts/t0657-lane1.md — verdict HOLD (spread-killer, new class); 'new failure class — spread-killer (b): host-level disk/CPU jitter BELOW the lane-visibility floor'",
    "signature": "quiet 1-min load (≤2.66) + wide cold spreads (14.7–58.3%) + stable warm arm (0.349/0.350s) + mincore COLD on 100% of trials",
    "compound_rule": "next drill should carry a host-jitter probe (time one sequential 607-file read per run) so this signature becomes a measurement, not a hypothesis",
    "fail_closed": "in-bar 1.094s median left unquoted at 58.3% spread — measurement untrustworthy",
    "premise_rot": "brief's 4f0c9aa8 → live 582e5e5f caught pre-measurement",
    "routing": "bar-itself question dispatched t0666 to lanes-2/5 seat"
  },
  "rule": "every drill carries a per-run jitter probe; if spread >10% persists with probe-quiet reads, the bar itself — not the environment — is the load-bearing question",
  "change": "spread-killer (b) is a named failure class; probe-quiet-but-wide-spread now routes to a bar redesign decision instead of being averaged away by the executor"
}
```
