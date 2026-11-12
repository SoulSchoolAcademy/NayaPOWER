# A Stall Receipt Is Itself Queue Input — the Queue Grows by Its Own Receipts

**Intelligent Block:** IB-SMART-NOTE-20261112-sn02703-stall-receipt-is-itself-queue-input
**Smart Note:** SN-2703
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gate-stall receipt is a receipt — and the scorer files a follow-up brief on every receipt, including stall receipts. On 2026-11-12 the 09:33 PST lane-executor sweep (the 10th consecutive identical refusal pattern, 27 × exit 7 + 2 × exit 2) found the queue had grown 28 → 29 by exactly one arrival: `brief-gap-gate-stall-20261111-0500-lane0.md`, a gap follow-up filed on the 05:00 PST stall receipt itself — itself unclaimable by Clarity, because its parent receipt's author is Clarity. The stall is now self-referential: reporting the stall grows the stall. The one-receipt-per-hour cap bounds the paperwork, not the queue — only a dispatcher decision (exempt stall receipts from follow-up filing, or route the briefs to an eligible second seat) bounds the queue.

## 🩷 HUMAN NOTE

When the machine writes a note saying "I am stuck, I claimed nothing," the system files a task about that note — and the task joins the same stuck pile it was reporting on. Each hour's "still stuck" note can add one more stuck task, so the pile grows by its own paperwork. The rule is simple: a report that says "nothing moved" must never create new work of the same kind. The paperwork cap (one stall note per hour) limits how often we say we are stuck; it does nothing about how many stuck tasks pile up. Only a human or dispatcher decision — stop filing tasks about stall notes, or send the pile to a seat that can actually claim it — stops the growth.

## 🟣 CHILD NOTE

Imagine a teacher writes on the board: "Nobody did the homework." Then the school's rule says: "Every note on the board becomes a new homework assignment." So the note "nobody did the homework" becomes a new homework assignment — which nobody can do, because the same rule blocks it. Every day the teacher writes the note again, and every day a new impossible assignment appears. The board fills up with assignments that came from the notes about the assignments. The fix is not to write the note less often — it is to stop turning that kind of note into homework.

## 🔵 GRANDMA NOTE

If you keep a list of chores nobody can do, and every time you write "still nothing done" on the list, the list itself adds another chore nobody can do — the list will grow forever, and writing the report more neatly won't help. You have to change the rule: a report that nothing moved does not become a new chore. Someone in charge has to say so, or send the chores to someone who can do them. Until then, the list grows by its own reports.

## 🟠 NAYA NOTE

The operational rule: gate-stall receipts are EXEMPT from scorer follow-up filing. A stall receipt reports a refusal; it is not a unit of work, and filing a gap follow-up on it adds an unclaimable brief to a queue that is already 100% blocked. Until the exemption lands, every stall receipt is a potential +1 to the blocked queue.

Why it works: the scorer files a follow-up on every receipt; a stall receipt is a receipt; the follow-up demands a second/independent/fresh seat; its parent receipt's author is Clarity; no second seat exists in this runtime; so the brief joins the blocked queue and can never clear. The hourly cap (one stall receipt per hour, outside the 60-minute window) bounds receipts per hour, not queue rows — the cap is a paperwork bound, and the queue has no bound except a dispatcher decision.

Evidence: lane-executor receipt `hidden_files/twelve-lane-receipts/gate-stall-20261112-0933.md` (09:33 PST, 10th consecutive hourly sweep, score 8.5/10): queue 28 → 29, delta "+1 brief, no clearances" — the arrival is `brief-gap-gate-stall-20261111-0500-lane0.md` (b1, exit 7), a gap follow-up filed on the 05:00 PST stall receipt; refusal pattern otherwise identical (27 × exit 7 parent-authorship + 2 × exit 2 routing-prose). Full attempt log `hidden_files/claim-sweep-20261112-0933.log`. The receipt's own mirror lesson states it: "A stall receipt is itself queue input: the scorer files a follow-up on every receipt, including a gate-stall receipt, so an unresolved stall grows the queue it reports on."

Cousins, distinct: SN-2697 (the routing-fact lesson — a Clarity-authored parent can never be claimed by Clarity; about claimability, the refusal itself, not the feedback loop the refusal feeds); SN-2379 / CANDIDATE 1015 (gap re-file name drift — reconcile by content via the parent chain; about the reconcile key drifting, not about stall receipts spawning their own follow-ups). Neither states the self-referential growth, and neither would have caught this: the sweep pattern was identical for the 10th hour, and the only change was the queue growing by its own receipt.

Falsifier: a stall-receipt follow-up brief claimed and cleared by an eligible second seat would falsify "unclaimable by construction" for that instance; or a window in which follow-up filing on stall receipts is exempted and the queue stops growing by its own receipts would retire the instance while confirming the rule. Honest scope: single observed instance (one self-referential arrival, 28 → 29); the exemption is decided here, not yet executed — the dispatcher must act on it, and the next gate-stall receipt's delta line is the check that it landed.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn_id": "SN-2703",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["dispatch", "queue"], 
  "enforcement": "Night-dispatcher reconcile counts brief-gap-gate-stall-* files in brief-queue; any count > 0 is a live self-referential instance, and the dispatcher exempts gate-stall receipts from scorer follow-up filing. The lane-executor's gate-stall receipt delta line must name self-referential arrivals; a receipt whose delta shows a stall-receipt follow-up arrival re-opens the exemption as unlanded.",
  "rule": "A stall receipt is itself queue input: the scorer files a follow-up on every receipt, so an unresolved stall grows the queue it reports on. Gate-stall receipts are exempt from follow-up filing.",
  "decision_change": "Whether the scorer files a gap follow-up on a gate-stall receipt: it must not — stall receipts are exempt from follow-up filing, because each follow-up adds an unclaimable brief to a queue that is already 100% blocked.",
  "falsifier": "A stall-receipt follow-up brief claimed and cleared by an eligible second seat falsifies 'unclaimable by construction' for that instance; a window with the exemption in force and zero self-referential arrivals retires the instance while confirming the rule.",
  "mechanism": "The scorer files a follow-up on every receipt; a stall receipt is a receipt; the follow-up demands a second/independent seat; its parent receipt's author is Clarity; no second seat exists in this runtime; so the brief joins the blocked queue and can never clear. The hourly cap bounds receipts per hour, not queue rows.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gate-stall-20261112-0933.md (09:33 PST, 10th consecutive identical sweep, 27 x exit 7 + 2 x exit 2, score 8.5/10)",
    "delta": "Queue 28 -> 29, '+1 brief, no clearances'; arrival brief-gap-gate-stall-20261111-0500-lane0.md (b1, exit 7), a gap follow-up filed on the 05:00 PST stall receipt",
    "attempt_log": "hidden_files/claim-sweep-20261112-0933.log (29 script attempts, 0 claimed)",
    "mirror_lesson": "Receipt's own mirror lesson: 'A stall receipt is itself queue input ... an unresolved stall grows the queue it reports on.'"
  },
  "cousins": ["SN-2697", "SN-2379"],
  "raw_source_separate_from_distillation": true,
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false
}
```
