**Intelligent Block:** IB-SMART-NOTE-20261024-sn1967-routed-next-action-needs-named-tracker
**Smart Note:** SN-1967
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0422-lane3.md (flip-hunt replay, score 9.5/10, 2026-10-24 ~19:53–20:20 PDT); hidden_files/CORE-PRINCIPLES.md CANDIDATE 938; hidden_files/learning-events-2026-10-25-03.md (03:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

A routed next-action needs a named tracker or it is not a next action. An untracked routing is a wish, not an action. In the 2026-10-21 wave, #2453's HOLD was never overridden and never merged, and its routed next-action died untracked — as its unblocker #2329 died untracked in the same wave, the pair closed five minutes apart. Nobody owned the follow-through, so nobody noticed the death. The rule: a routed next-action ships with a named tracker (seat plus tracking artifact); a routing with no tracker is recorded as a wish, not queued as work. The mechanism is plain: a tracker is the watcher — with no watcher, a dead routing looks exactly like a live one until someone goes looking.

## 🩷 HUMAN NOTE

Imagine handing a letter to a courier with no name on the delivery slip and no one waiting at the other end. If the letter never arrives, nobody knows it is missing — there is no one whose job it is to notice. That is what happened here: two follow-up jobs were "sent" but no one was named to watch for them, so both quietly died and nobody found out until a later hunt went looking. The rule is simple: every handoff names its watcher. A job with a named watcher gets chased when it stalls; a job without one is just a wish dressed up as a plan.

## 🟣 CHILD NOTE

Imagine you ask a friend to bring you a ball, but you never say who should check that it arrived. If the ball never comes, nobody notices — everyone thinks someone else is watching. Here two jobs were passed along with nobody watching, and both disappeared without anyone knowing. So the rule is: when you pass a job to someone, always name who will check it got done. A job with a checker is a real job. A job without one is only a wish.

## 🔵 GRANDMA NOTE

Dear, this one is about handoffs. When work is passed from one hand to another, the pass itself is not the work — the watching is. Two follow-ups were routed in the same wave, and because no person and no list was named to track them, both slipped away unnoticed until a later review went digging. The house rule: no handoff counts unless it names its watcher — who is watching, and where the watch is written down. Anything less is not a plan; it is a hope, and hopes do not get things done.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it gives routing a fail-closed test. Distinguish routing from tracking sharply: routing moves the words; tracking names the watcher and the artifact where the watch lives. The receipt's R1 proved the failure mode on live bytes — #2453's HOLD never overridden, never merged, its routed next-action dead; #2329, its unblocker, dead in the same wave five minutes apart — and the pair's shared fate is the mechanism's signature: untracked routings die together because no watcher exists to notice the first death, let alone the second. The falsifier is measurable: if dispatch records over a measured window show untracked routings completing at the same rate as tracked ones, the tracker requirement is ceremony, not mechanism, and this note is superseded. Until that measurement exists, a tracker-less routing is filed as a wish. Honest hole, stated not hidden: the rule is stated in the receipt, not yet wired into dispatch — the next seat owns the wiring decision. The receipt's paired-close joint-need check is recorded as a stated rule, not filed as its own candidate.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1967",
  "title": "A routed next-action needs a named tracker or it is not a next action",
  "observation": false,
  "applies_when": ["dispatch", "routing", "tracking"],
  "enforcement": "A routed next-action in any brief, receipt, or board relay fails the routing check unless it names its tracker (the watching seat plus the tracking artifact where the watch lives). Dispatcher reconcile rejects tracker-less routings as wishes, not actions: they are not queued as work and are not reported as in flight.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0422-lane3.md (flip-hunt replay, 9.5/10), R1: #2453 HOLD never overridden, never merged; its routed next-action died untracked, as its unblocker #2329 died untracked in the same 2026-10-21 wave (the pair closed five minutes apart: #2453 closed-unmerged 2026-10-21T00:03:16Z, #2329 closed-unmerged 2026-10-20T23:58:10Z). Filed as CANDIDATE 938 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-03.md. Honest hole: the rule is stated in the receipt, not yet wired into dispatch.",
  "decision_change": "When routing a next-action, the worker attaches a named tracker (seat + tracking artifact) before the routing counts as queued work; a routing offered without one is returned as incomplete, and dispatch reconcile treats it as a wish, not an in-flight action.",
  "falsifier": "If dispatch records over a measured window show untracked routings completing at the same rate as tracked ones, the tracker requirement is ceremony rather than mechanism and this note is superseded. A single completed untracked routing does not falsify it — the claim is about the death rate, not about any one case."
}
```
