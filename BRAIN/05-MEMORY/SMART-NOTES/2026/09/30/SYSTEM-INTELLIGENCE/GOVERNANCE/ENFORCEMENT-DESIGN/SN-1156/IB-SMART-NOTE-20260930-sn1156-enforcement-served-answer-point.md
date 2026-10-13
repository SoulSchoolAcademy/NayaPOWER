# SMART NOTE — Enforcement Sits at the Served-Answer Point

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1156` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1156-enforcement-served-answer-point` |
| Human title | Enforcement Sits at the Served-Answer Point — Two Refusal Paths, Flags Are Not Enforcement |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | ENFORCEMENT DESIGN |
| Captured | 2026-10-13 04:40:00 UTC |
| Truth state | CANDIDATE (one measured study; wiring not yet built — protected gate) |
| Proposed intelligence class | CORE (governance machinery — pending taxonomy adoption) |
| Capture type | Design law |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Lane 8 — Naya Sentinel, t0575 verdict-application study, #2175 board comment 6138023401; hidden_files/lane8-t0575-verdict-application.md (goal workspace); receipt twelve-lane-receipts/t0575-lane8.md |

---

## ✦ IN A NUTSHELL

**A score with no verdict rule picks the wrong winner.** On the t1412 fixture pool, the ungoverned score crowned SN-X5 at 103.86 — a FALSIFIED note, the t1282 hole. With verdict rules R1–R4 applied, SN-X6 (45.44, VERIFIED) wins and SN-X5 is demoted and named. Two design laws settle this measurement: (1) wiring needs **two distinct refusal paths** — a falsified-only pool must refuse as `REFUSED_FALSIFIED_ONLY`, a below-floor unknown must refuse as `UNKNOWN_TRUTH_STATE`, never collapsed; (2) the enforcement leg sits **at the served-answer point** — a flag-only wiring would reproduce the t1282 hole with better labels.

---

## 🩷 HUMAN NOTE

Think of a judge who scores diving but has no rulebook. The flashiest dive wins — even if it was a belly flop, because the flop was *spectacular*. Add the rulebook (falsified dives are disqualified, unknowns are marked unknown), and the real winner surfaces. The study proved this with numbers: without the rules, the falsified note "won" at 103.86. With the rules, the verified note won at 45.44. And one more law: labels don't enforce. A flag that says "this is falsified" but still serves it is a warning nobody reads — enforcement has to happen where the answer leaves the building.

---

## 🟣 CHILD NOTE

In a race, the stopwatch says who was fastest — but the rules say who actually wins. One runner cheated. Without the rules, the cheater wins. With the rules, the cheater is disqualified and the honest runner wins. The study ran the race both ways and wrote down the lesson: rules decide the winner, not the stopwatch. And the rule has to be enforced at the finish line — a sign that says "no cheating" doesn't stop anyone by itself.

---

## 🔵 GRANDMA NOTE

Dear, numbers without rules are just louder opinions. The test showed that a wrong answer with a big score beats a right answer with a smaller one — unless the rules step in. So the rules matter more than the scores. And a rule that only *labels* the wrong answer but still hands it over isn't a rule at all. It has to stop the handover. That's where enforcement lives: at the door, not on the label.

---

## 🟠 NAYA NOTE

1. **Re-assert the fixture pin PASS before measuring.** All 8 SHAs matched, base pin 3eeddc8f — stale fixtures poison the whole study. Measure nothing on an unpinned fixture.
2. Score first, apply the verdict rules, then compare the winners. **Publish both** — the ungoverned winner and the governed winner. The delta is the evidence.
3. If the winner changes under the rules, the rules are the instrument, not decoration. Wire them **at the served-answer point** — the enforcement leg is where the answer exits, not where it is computed.
4. Refusal paths must be **distinct signals**: falsified-only → `REFUSED_FALSIFIED_ONLY`; below-floor unknown → `UNKNOWN_TRUTH_STATE` flag. Collapsing them hides which failure happened, and the repair differs.
5. A flag-only wiring is rejected by design: it would reproduce the t1282 hole with better labels. Labels inform; enforcement stops.
6. **No wiring was done in this study.** Wiring is a protected gate — it needs Shawn's word. This note captures the measured design; it does not authorize the build.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1156-enforcement-served-answer-point",
  "epistemic_state": "CANDIDATE",
  "capture_type": "Design law",
  "study": {
    "lane": "Lane 8 — Naya Sentinel",
    "fixture_pool": "t1412",
    "fixture_pin": "3eeddc8f, 8/8 SHAs PASS before measuring",
    "ungoverned_winner": "SN-X5 FALSIFIED @ 103.86 (the t1282 hole)",
    "governed_winner": "SN-X6 VERIFIED @ 45.44",
    "verdict_rules": ["R1", "R2", "R3", "R4"],
    "measurement_score": "9.0/10 (same-seat; Lane 1 four-way still owed)"
  },
  "design_laws": {
    "refusal_paths": {
      "falsified_only_pool": "REFUSED_FALSIFIED_ONLY",
      "below_floor_unknown": "UNKNOWN_TRUTH_STATE",
      "collapse_forbidden": true
    },
    "enforcement_leg": "served-answer point",
    "flag_only_wiring": "rejected — reproduces the t1282 hole with better labels"
  },
  "protected_gate": "no wiring built; wiring needs Shawn's word",
  "board_evidence": ["#2175 comment 6138023401"]
}
```

---

## 🟢 LEARNING LESSON

**The instrument is the verdict rule, not the score.** Teams obsess over scoring fidelity (103.86 vs 45.44) and under-invest in the rules that decide what a score may do. This study inverts the priority: the R1–R4 rules flipped the winner. The scores were fine all along — the governance was missing. Build the rules first; calibrate the scores second.

---

## 🔗 HOW IT CONNECTS

- **ENABLES** the verdict-application program — the study is the first R1–R4 application against a real pool; the design laws are now named for the wiring lane.
- **COMPOUNDS** the F-family honesty discipline (L277/L278, same window): the machinery must be as honest as the measurement, and honest measurement must be enforced where it is served.
- **REQUIRES** the t1412 fixture pin discipline — unpinned fixtures would make the governed-vs-ungoverned comparison meaningless.
- **REFINES** the falsified-note lifecycle: `FALSIFIED_DEMOTED` is now a named, published disposition, not a silent drop.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One measured study, same-seat scored 9.0/10, independent four-way (Lane 1) still owed. The design laws are named but the wiring is unbuilt — deliberately, behind Shawn's protected gate. Do not claim this as deployed enforcement.

## ❓ UNCERTAINTY

- Does the two-refusal-path design hold under mixed pools (falsified + below-floor in one batch)?
- What is the served-answer point for non-chat surfaces (Hub projections, API consumers)?

## 🌍 APPLICABILITY

- **Applies to:** any scoring/selection wiring that serves answers to users; any verdict-rule design; falsified-note lifecycle handling.
- **Does NOT apply to:** exploratory measurements with no served answer; protected-gate wiring decisions (human authority).

## 🧬 SUCCESSOR EFFECT

Future Naya: never ship a score without its verdict rules, and never ship verdict rules that only label. When you design enforcement, put the leg where the answer leaves — and give falsified and unknown their own distinct refusals. A wrong answer with a big number is the oldest hole in the book; the t1282 hole is its name here. Don't re-dig it.
