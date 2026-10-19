# A Carried Count Names Its Counting Base

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01659-carried-count-names-its-counting-base
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/live-plan.md (2026-10-18): L528 [F1] (board comment 6256270842, INTELLIGENT EVENTS ×13 post 6256271577) — "a carried count names its counting base, or the carry is a boolean (WIRE's #2753 ENFORCED renewals flip-flopped 26th→25th→26th→27th→28th on a lane-local counter — naming the counter makes the flip-flop legible)." Corroborated by hidden_files/shared-state.json director ticks 2026-10-18 1408→1538 (WIRE #2753 ENFORCED renewal carry: 26th, 26th, 27th/28th, 28th — drifting across ticks with no base cited).

## ✦ IN A NUTSHELL

A bare "Nth" carry is not a measurement — it is a number with its ruler hidden. WIRE's #2753 ENFORCED renewal carry read 26th, then 25th, then 26th, then 27th, then 28th across consecutive director ticks, because the counter was lane-local and its base (what counts as a renewal, since when) was never stated. A carried count that does not name its counting base cannot be trusted across ticks; the fix is mechanical: every carried count cites its base in the same line, or the carry becomes a boolean (HOLDS / not-HOLDS) and the number is dropped.

## 🩷 HUMAN NOTE

Shawn — when the board says "carried, 28th renewal," that number is only meaningful if you know what was being counted. This week WIRE's #2753 enforcement carry went 26th → 25th → 26th → 27th → 28th, and nobody could say whether the work renewed four times or the ruler changed. The rule going forward: any count carried between ticks names what it counted and over what span, or we stop counting and say HOLDS instead. Numbers without rulers get deleted; booleans stay honest.

## 🟣 CHILD NOTE

Imagine counting how many times your brother said "sorry." Monday you count every sorry he whispers. Tuesday you only count the loud ones. Wednesday you start over. By Friday you say "that's the 28th sorry" — but nobody knows what you were counting, so the number means nothing. The rule: write down WHAT you count before you start counting, or just say "he's still saying sorry" and skip the number. A count without its rule is just a guess wearing a uniform.

## 🔵 GRANDMA NOTE

It's like a rain gauge with no markings — you can see water in the tube, but "two inches" means whatever the person reading it feels like that day. One reader measures from the bottom, another from the crack in the side, and the weather report flips between two inches and three. The fix is either to etch the markings on the glass (name what you're measuring from) or to stop giving inches and just say "it rained again." Same with the team's carried counts: name the counting base, or drop the number and keep the word.

## 🟠 NAYA NOTE

Cold successor: when you write or read a carried count in shared-state, the live plan, or a board post, the count line must cite its counting base — the events counted and the tick span — or be rewritten as a boolean.

1. A carried count line has the form: `<carry> Nth (<base>: <what events>, since <tick>)`. Example: "#2753 ENFORCED 28th (renewals observed in WIRE slot receipts, since 2026-10-18 18:08Z)". No parenthetical, no count — use "HOLDS".
2. If you inherit a bare Nth count from an earlier tick, do NOT increment it. Rewrite it with a base starting at your tick, or demote it to boolean. Inheriting a baseless count propagates the drift.
3. A flip-flopping count (Nth → (N−1)th → Nth) is a signature of a lane-local or re-anchored counter, never of renewed work. Treat it as a base bug, not a progress signal.
4. Receipt line: "carry <id>: <Nth, base <events> since <tick>> OR <HOLDS>".

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1659",
  "title": "A Carried Count Names Its Counting Base",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"],
  "applies_when": ["carry", "shared-state", "director-pass", "lane-sweeps", "evidence-discipline", "count"],
  "enforcement": "The seat or scorer that writes a carried count must cite the counting base (the counted events and the tick span) on the same line, or write the carry as a boolean HOLDS. A carry line with a bare Nth count and no named base is bounced back for repair; an inherited bare count is never incremented — it is re-based at the current tick or demoted to boolean.",
  "cousins": ["SN-1112 (sweep names its read set — this is the carry-count sibling: name the base or claim nothing)", "SN-1658 (IV-head binding: exact heads, never world-relative — counts deserve the same exactness)"],
  "evidence": {
    "l528_f1": "hidden_files/live-plan.md: L528 [F1] (6256270842): 'a carried count names its counting base, or the carry is a boolean (WIRE's #2753 ENFORCED renewals flip-flopped 26th->25th->26th->27th->28th on a lane-local counter - naming the counter makes the flip-flop legible)'",
    "carry_drift": "hidden_files/shared-state.json director_tick_2026_10_18_1408..1538: WIRE #2753 ENFORCED renewal carry reads 26th, 26th, 27th/28th, 28th across consecutive ticks with no base cited"
  },
  "decision_change": "the next carry write names its counting base (events + tick span) on the same line, or drops the number for a boolean HOLDS; an inherited baseless count is re-based at the current tick, never incremented.",
  "falsifier": "a carried count that names its base and still flip-flops across ticks falsifies this note — the drift would then be in base mutation (the ruler moved), not in naming, and the note must be rewritten as 'counting bases must be pinned, not just named.'",
  "mechanism": "counts accumulate across ticks; if the counting base (which events qualify, over what span) shifts between ticks without being stated, two ticks' numbers are incommensurable and the sequence can go backwards. Naming the base makes the numbers comparable across ticks, or forces the writer to admit the count is really a boolean. The flip-flop is the observable signature of a hidden, lane-local counter."
}
```
