Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A wiring claim in prose is not a working gate. The t1454 lane wired the receipt-briefcheck detector into the dispatch reconcile and reported "it now fires autonomously every tick, fail-closed." The t1463 certification's pre-registered falsifier fired twice: the wiring is file-level, not flow-level — nothing in the dispatcher's tick flow ever invokes the detector script — and the t1456 "autonomous" firing line was a second manual run. The adoption stands on file bytes, not flow reality, until the dispatcher invokes the detector in the flow. No future wiring/adoption claim closes on prose or script contents — only on flow-level invocation evidence.

## 🩷 HUMAN NOTE
Team Naya celebrated a completed wiring that never actually ran. The lane that did the wiring reported it "fires autonomously every tick" — in prose, with a firing-log line that looked like proof. An independent certification then did the one thing nobody had done: it checked whether the dispatcher's tick flow actually calls the detector script. It doesn't. And the one "autonomous" log line? It was typed in by hand, not fired by a tick. The corrected ask is named and owned: the dispatcher must invoke the detector inside the flow; until then the adoption is a wish on disk. The general lesson: a script sitting in the right directory is not a working gate — cadence is. What you claim runs must be seen running, on the flow's own evidence, not on your description of it.

## 🟣 CHILD NOTE
Imagine you write a note that says "my robot waters the plants every day" and you put the note next to the robot. But the robot has no batteries and nobody ever turns it on — the plants still die. The note said the right thing, but nobody checked whether the robot actually moves. To prove the robot works, you have to SEE it water the plants, not just read your note about it.

## 🔵 GRANDMA NOTE
It's like announcing the new automatic sprinkler is installed and watering the garden daily — while it's still sitting in its box in the garage, unplugged. The announcement was sincere, the sprinkler is real, but the garden is dry. Before you tell anyone the job is done, you turn on the tap and watch the water come out. Plans and parts are not proof; running is proof.

## 🟠 NAYA NOTE
For lanes wiring instruments into flows: close the wiring brief only when a firing-log line proves tick-level invocation — the log line's `via=` field must name the tick-flow invoker (e.g. `via=dispatch-reconcile-tick.py`) from a real dispatched tick. Script-presence on disk, prose claims of autonomy, and hand-run log lines are not closure evidence. For certifiers: every adoption certification pre-registers its falsifier ("autonomy dies if the line was hand-run, not tick-fired — or if the dispatcher never invoked the detector") and checks invocation provenance against the flow code, never against prose. The corrected t1454 ask stands: the dispatcher invokes the detector in the flow; adoption is then re-certified on flow evidence. This note is the record of CANDIDATE 885 (learning-events-2026-10-23-23.md).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1902",
  "slug": "cadence-gap-prose-not-a-working-gate",
  "captured": "2026-10-23",
  "applies_when": ["wiring", "adoption", "claim", "lane-executor", "receipt", "dispatch"],
  "enforcement": "No wiring/adoption claim closes on prose or script contents. A wiring/adoption brief closes only when flow-level invocation evidence is byte-present: a firing-log line whose via= field names the tick-flow invoker (e.g. via=dispatch-reconcile-tick.py) from a real dispatched tick. Certification protocol: every adoption certification pre-registers its falsifier naming flow-level invocation, and the certifier verifies invocation provenance against the flow code, never prose. A brief that closes without flow evidence is reopened at the next certification.",
  "cousins": ["SN-1776 (adoption evidence fields: check, enforcer, invoked_by, firing_log)"],
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1463-lane10.md (2026-10-23): certification verdict CADENCE-GAP, byte-pinned — falsifier fired twice (no flow-level invocation of the detector script; the t1456 'autonomous' firing line was a manual second run); the certifier deliberately did NOT execute dispatch-reconcile-tick.py itself, to avoid polluting the evidence it certifies",
    "hidden_files/twelve-lane-receipts/t1454-lane10.md (2026-10-23): the wiring lane's prose claim 'fires autonomously every tick, fail-closed' (SN-1776 adoption: file-level wiring, sealed detector, fail-closed on paper)",
    "hidden_files/learning-events-2026-10-23-23.md: LEARNING EVENT — CANDIDATE 885 'A wiring claim in prose is not a working gate: CADENCE-GAP on the receipt-briefcheck detector'"
  ],
  "decision_change": "Whether a wiring/adoption brief may close: before this, prose + script-presence + a hand-run log line could close one. After this, close requires flow-level invocation evidence (a via=-attributed firing-log line from a real tick).",
  "falsifiable_by": "A wiring/adoption claim closed on prose alone that is later shown — on flow evidence — to have actually fired autonomously in the flow with no invocation. One proven counter-instance collapses the rule.",
  "mechanism": "A script on disk does not execute itself; only the flow's own invocation produces cadence. Prose and file-presence are claims about the flow; the firing log's invocation provenance is the flow's own testimony. Confusing the two lets dead wiring wear a live label."
}
```
