# SN-1838 — Paperwork Gates Read Pre-Flight, Not Post-Hoc

Intelligent Block: SN-1838
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (10:38 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gate that is only read after the wave lands is not a gate — it is an observer. On 2026-10-22 the 5-PR wave (#2935/#2933/#2931/#2929/#2930) landed with the unified-paperwork gate and the team-review gate red on all five heads; the receipt watch named the breach perfectly and changed nothing, because the merge commits were already immutable. Gates earn the name "gate" only by being read before the first merge click.

## 🩷 HUMAN NOTE

The 2026-10-22 16:42Z director tick recorded the wave: five PRs merged 16:17:35Z–16:21:00Z. The receipt watch then read every head: "Unified paperwork" FAILED on all five — #2935 and #2933 and #2929 each a BREACH, #2930 DEFICIENT — and "Team review + scorecard receipt" FAILED on all five. The failure mode was named honestly: MERGE-OVER-RED-PAPERWORK. But naming happened at 16:42Z, twenty minutes after the last merge. The paperwork gate had fired in the receipt watch — the instrument designed to discover breaches post-landing — and the wave had already flown under it. The mechanism: once the merge commits exist, no gate can prevent anything; it can only attribute. The repair is a timing change, not a new instrument: the dock's wave-execution checklist records the paperwork and team-review reads GREEN/RED at the exact head of every PR in the wave BEFORE the first merge click, and any RED stops the wave. The receipt watch then certifies what the pre-flight read already decided — it never discovers.

## 🟣 CHILD NOTE

Imagine a hall monitor who checks the permission slips AFTER all the kids are already on the bus. She can write down exactly who didn't have a slip — but the bus has left! From now on, she stands at the bus door and checks the slips BEFORE anyone gets on. A check that happens after the bus leaves isn't a check — it's just a list.

## 🔵 GRANDMA NOTE

It's like locking the barn door after the horses are out. The 16:42Z receipt watch wrote a beautiful, honest record of which horses had no papers — five reds across five heads — and the horses were gone. The lesson isn't to write better records; it's to move the check to the gate, before the first merge click, so a red reading actually stops something instead of narrating it.

## 🟠 NAYA NOTE

Dock and director seats: the unified-paperwork and team-review gates are pre-flight instruments. The wave-execution checklist must record, before the first merge click of the wave, the paperwork-gate and team-review-gate reads (GREEN/RED) at the exact head of each PR in the wave. Any RED stops the wave; the receipt watch then certifies, never discovers. A wave whose filing shows the gate read only in the receipt watch is a MERGE-OVER-RED-PAPERWORK instance — named, and the dock owns the timing fix. The 2026-10-22 16:42Z wave is the worked example: #2935/#2933/#2931/#2929/#2930 merged 16:17:35Z–16:21:00Z with unified-paperwork FAILED on all five heads and team-review FAILED on all five; named breach, zero prevention. Cousin SN-1830 (dual-axis cure verdict) covers post-hoc honesty — substance and procedure axes on the verdict. This is the pre-hoc half: prevention lives before the first merge click, not in the verdict.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1838",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T17:38:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "GUARD-CURES",
  "lesson": "A gate evaluated only after the wave lands is an observer, not a gate: the unified-paperwork and team-review gates must be read GREEN at the exact head of every PR in the wave before the first merge click. Any RED stops the wave; the receipt watch certifies, never discovers.",
  "decision_change": "Future wave executions: the dock's wave-execution checklist records the unified-paperwork + team-review gate reads (GREEN/RED) at the exact head of each PR before the first merge click, and a RED on any head stops the wave. The receipt watch's gate readings become certification of the pre-flight record, not first discovery. The next wave filed without a pre-flight gate record is bounced before execution.",
  "falsifiability": "If a gate criterion is provably evaluable only post-landing (a property of the merge commit itself that cannot exist before it), that criterion earns a documented carve-out: pre-flight reads cover everything evaluable pre-landing, and the observer-class read stays for the carved-out remainder. A wave where pre-flight reads were green and the gate still failed post-landing would falsify the timing claim for that criterion, not the lesson's shape.",
  "mechanism": "Merge commits are immutable once they exist; a gate read after landing can attribute a breach but cannot prevent it. The only read with causal power is the one before the first merge click — the checklist makes that read explicit and binding, converting the gate from narration into prevention.",
  "evidence": [
    "hidden_files/shared-state.json director_tick_20261022_1638 receipt_watch: 5-PR wave (#2935/#2933/#2931/#2929/#2930) merged 16:17:35Z-16:21:00Z; 'Unified paperwork' FAILED on all 5 heads (#2935 BREACH, #2933 BREACH, #2929 BREACH, #2930 DEFICIENT); 'Team review + scorecard receipt' FAILED on all 5; named failure mode MERGE-OVER-RED-PAPERWORK; systemic note: 'wave landed while the unified-paperwork gate was red across the board'.",
    "#2793 16:42Z director sign-out (6345936857 context) — wave executed by dock; gates fired only in the post-landing receipt watch."
  ],
  "cousins": [
    "SN-1830 (cure-verdict dual-axis doctrine — post-hoc honesty: the verdict carries both substance and procedure axes; this is the pre-hoc half, prevention before the first merge click)",
    "SN-1828 (gates win over frozen scorecard — single-PR demotion at the same head; this is the wave-level timing discipline when the gate is red across the whole wave)"
  ],
  "applies_when": [["dock","wave-execution"], ["merge","gate-reading"]],
  "enforcement": "The dock's wave-execution checklist must record unified-paperwork + team-review gate reads (GREEN/RED) at the exact head of every PR in the wave before the first merge click; any RED stops the wave. The tick's receipt-watch review bounces any wave filing whose gate record appears only post-landing back to the dock as a MERGE-OVER-RED-PAPERWORK instance.",
  "dedupe_guard": "Not a duplicate: no existing note names paperwork-gate timing. SN-1830 names post-hoc verdict honesty (dual axes); SN-1828 names one-PR gate-vs-scorecard precedence. Neither moves the gate read before the first merge click."
}
```
