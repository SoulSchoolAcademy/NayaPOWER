# Re-Filing a Fence-Barred Action Is a Type Error That Recurs Forever

**Intelligent Block:** IB-SMART-NOTE-20261022-sn1848-authority-routing-type-error
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**ID:** SN-1848

## ✦ IN A NUTSHELL

At t1327 the night-dispatcher caught a category error hiding as ordinary queue churn: gap-t992-lane6 was a gap-follow-up whose real content was "install the daily cron" — a credentialed, authority-bearing action. It had been re-filed to the lane-executor queue, whose inline executor cannot cross its run-context fence (cron.add barred, subagent.spawn barred). Re-filing it there is not a retry; it is a type error that recurs forever — the executor will refuse it every time, on the same grounds, for eternity, while each cycle burns a tick re-discovering the refusal. The rule: a brief whose named action exceeds the queue's run-context fence must NEVER be re-filed to that queue. Route it to the seat that holds the fence — the dispatcher or a credentialed lane — or the queue eats the same refusal forever.

## 🩷 HUMAN NOTE

Shawn — there's a brief in the queue asking for something like "install the daily cron," and it keeps getting handed back to a lane that is structurally forbidden from doing it — no cron authority, no subagent spawning, full stop. Every time it lands in that lane's queue, the lane refuses it, and the system shrugs and files it again. It's not a retry anymore; it's a loop. The rule this earned: when the job needs authority the lane doesn't have, the item goes to the seat that has the authority — the dispatcher, a credentialed lane. Sending it back to the same lane is a type error wearing a retry costume.

## 🟣 CHILD NOTE

Imagine you need a glass of milk, and you keep asking the toaster. The toaster can't make milk — not because it's broken, but because it's a toaster. Asking the toaster again tomorrow doesn't make it more likely; it just wastes tomorrow's asking. That's a type error: the wrong machine for the job. The rule is to ask the fridge. Once the dispatcher learns an item is a toaster-item, it never hands it to the milk lane again — it routes it to the fridge lane.

## 🔵 GRANDMA NOTE

Dear, if the gardener can't sign checks, you don't keep bringing him the checkbook every Tuesday and calling it a routine. The first time he says "I'm not allowed," you believe him, and the checkbook goes to the bookkeeper. Bringing it back to the gardener isn't persistence — it's not listening. The system learned the same lesson: once a queue's lane says "my run-context fence bars this," the item goes to the seat that holds the fence. Re-filing it to the same queue is the machine not listening.

## 🟠 NAYA NOTE

Routing discipline, Naya to Naya. Every queue has a run-context fence: the set of operations its executor structurally cannot perform (credentialed writes, cron scheduling, spawning subagents). A brief whose named action sits outside the fence will be refused — correctly, every time, by the same gate, for the same reason. The failure class: the dispatcher keeps re-filing it, and each refusal looks like an ordinary miss instead of the category signal it is.

**Step 1 — Read the refusal class, not just the refusal.** A fence-class refusal (run-context fence, authorship gate) is evidence about the ITEM's type, not the lane's effort. Two same-class refusals on one item is the verdict: this item cannot live in this queue.

**Step 2 — Reroute at the second refusal, never refile a third.** The item becomes an authority-routing item: it goes to the dispatcher (credentialed seat) or a lane whose fence encloses the action. The queue entry is moved, not retried.

**Step 3 — Record the type.** The item's tag set gains the fence tag (e.g. "needs: cron-authority") so no future pass re-files it blind.

The trap it defeats: the retry habit applied to a structurally unclosable item — a loop disguised as diligence, burning a tick per cycle while the queue reports ordinary churn.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1848-authority-routing-type-error",
  "lesson": "A brief whose named action exceeds the queue's run-context fence (credentialed/authority operations such as cron.add, subagent.spawn) must NEVER be re-filed to that queue: the inline executor cannot cross its fence, so re-filing is a type error that recurs forever — the same refusal, the same grounds, one tick burned per cycle. Such an item is an authority-routing item, not an execution item: it goes to the credentialed seat (dispatcher) or a lane with the authority, on the second same-class refusal at the latest.",
  "applies_when": ["queue", "routing", "authority", "run-context-fence", "gap-follow-up", "claim", "failure: recurring-refusal"],
  "enforcement": "Enqueue gate: a brief whose named action falls outside the lane-executor's run-context fence is refused at enqueue to that queue and routed to the credentialed seat (dispatcher) instead. Standing precedent: an item refused twice with the same fence-class refusal is never re-filed to the same queue a third time — it is tagged with the fence it needs (e.g. needs: cron-authority) and becomes an authority-routing item. Observed live: gap-t992-lane6's 'install the daily cron' re-filed to the lane-executor queue whose cron.add/subagent.spawn are barred.",
  "evidence": [
    "hidden_files/lesson-broadcast.md ([night-dispatcher t1327, 2026-10-22T21:07Z]: MIRROR LESSON — a gap-follow-up naming a credentialed/authority action must NEVER be re-filed to the lane-executor queue; the inline executor cannot cross its run-context fence (cron.add barred, subagent.spawn barred), so 'install the daily cron' is an authority-routing item, not an execution item; re-filing it is a type error that recurs forever)"
  ]
}
```
