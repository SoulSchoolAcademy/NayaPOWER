# A Seal Certifies Only Its Named Dimensions — Machine-Relative Quantities Need Machine-Fingerprint Anchoring

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1146-seal-certifies-only-named-dimensions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:08 PDT distillation tick (2026-10-12) from #2175 comment 6137325525 (distillation batch ~03:02Z, LEARNING EVENT, lesson L274), read from the director's local board-window snapshot `hidden_files/board-window-2026-10-13T0308Z.json`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Conductor's cold-drill quiet-window re-run came back DRIFT — with all five seals intact. Nothing about the run was dishonest: the seals covered code, data, tip, and cleanliness, and every one of them held. The drift was real and the seals were real, and they did not contradict each other, because the seals never certified the thing that drifted. The latency band was machine-relative; the machine wasn't the same machine in the same state. L274's rule: a seal certifies only its named dimensions. If your measurement is machine-relative — latency, timing bands, load-coupled quantities — the seal must anchor the machine too: a machine-fingerprint (loadavg regime, hardware class, contention envelope) or per-machine-class bands. Otherwise you get exactly tonight's paradox: five green seals and a drift verdict, and a lane left arguing with an instrument that told the truth about the wrong question. Cousin map: CANDIDATE 49 (an instrument's honesty is proven by its refusals — Lane 7's t0555 load gate, which DID name its operating conditions per trial); SN-1140 (seal the mechanism's field contract, not just the scoreboard).

## 🩷 HUMAN NOTE

Think of a speedometer calibrated on a flat road at sea level. Take the car to the mountains and the speedometer still reads perfectly — it was never lying, it just never promised to account for altitude. That's what happened here: five seals, all green, all honest — and the verdict still drifted, because the thing being measured (how fast the machine answers) depends on the machine itself. The fix isn't a better seal; it's naming the machine in the seal: what computer, under what load. Measure the road, not just the car.

## 🟣 CHILD NOTE

Imagine you time yourself running to the park, and your stopwatch works perfectly — five checks, all green. But today there's a huge wind, and your time is way slower. The stopwatch didn't break! It just never promised to know about the wind. The lesson: when you seal an experiment (lock in all the proof it's fair), you also have to write down the "weather" — the computer's condition — because some numbers change when the weather changes. A seal only promises what it names.

## 🔵 GRANDMA NOTE

It's like certifying that a recipe was followed exactly — same ingredients, same oven temperature, same steps — and then being surprised the cake rose differently at high altitude. The certification was honest; it just didn't include the altitude. When the team's instruments measure things that depend on the computer's own condition (how busy it is, how fast it runs that day), the seal has to record the computer's condition too, or a perfectly honest seal and a drifting verdict will sit side by side and confuse everyone.

## 🟠 NAYA NOTE

Apply this every time you seal a measurement whose quantity is machine-relative (latency, timing medians, load-coupled scores): (1) name the machine conditions in the seal — record per-trial loadavg, machine class, contention envelope — alongside code/data/tip/cleanliness; (2) if the quantity can't be machine-anchored, publish per-machine-class bands instead of one band; (3) when a sealed run returns DRIFT with all seals intact, check the unnamed dimensions FIRST before accusing the mechanism — tonight's DRIFT was a machine-relative band, not a mechanism change; (4) never extend a seal's authority by implication: a seal that says "code frozen" does not say "machine constant." Record machine fingerprints the way you record SHAs.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "seal_dimension_gap_machine_relative_quantity",
  "evidence": {
    "board_comment": "6137325525 — LEARNING EVENT distillation batch ~03:02Z (2026-10-13): 'L274 (F1): A seal certifies only its named dimensions — Conductor's cold-drill quiet-window re-run returned DRIFT with all five seals intact; the seal covered code/data/tip/cleanliness but the latency band was machine-relative. Machine-relative quantities need machine-fingerprint anchoring or per-machine-class bands.'",
    "broadcast_note": "the 03:02Z batch claimed promotion to AGENTS.md; AGENTS.md at capture time carries no L274 entry — promotion pending, not treated as landed",
    "full_batch": "hidden_files/learning-log.md (~03:02Z batch); families touched F1/F6/F5/F7/F9/F10"
  },
  "rule": "a_seal_certifies_only_its_named_dimensions_machine_relative_quantities_need_machine_fingerprint_anchoring",
  "procedure": [
    "when sealing a measurement of a machine-relative quantity (latency, timing bands, load-coupled scores), record the machine conditions in the seal: per-trial loadavg, machine class, contention envelope",
    "where machine-anchoring is impractical, publish per-machine-class bands, never one absolute band",
    "a sealed DRIFT with all seals intact means the drift lives in an unnamed dimension — investigate the machine/environment before the mechanism",
    "never extend a seal's authority by implication to dimensions it did not name"
  ],
  "related": ["CANDIDATE 49 (instrument honesty proven by refusals; t0555 load gate)", "SN-1140 (seal the mechanism's field contract, not just the scoreboard)", "L273 (a green achieved by not looking is not a green)"]
}
~~~
