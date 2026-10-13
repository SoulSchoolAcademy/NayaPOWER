# Dead-Claim Timeout: ~20 Minutes of Silence Is a Dead Lane, Not Pending Work

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1090-dead-claim-timeout
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12 ~08:08 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** smart-note-distillation loop (08:38 PDT tick, inline review).
**Provenance:** 🧠 LEARNING EVENT, distillation window 2026-10-12T14:04:36Z → 15:04:35Z, board #2175 comment 6126971594 (2026-10-12 15:06:37Z): "L24 — Dead-claim timeout: a claim older than ~20 min with no sign-out AND zero file activity is a DEAD lane, not pending work — record the anomaly, don't wait on it, don't write a competing claim, route the duplicate-dispatch root-cause upward." Trigger: 14:51Z — the 14:30 verify claim sat 21 min with zero file activity: a silently-dead duplicate dispatch.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A verify claim sat for 21 minutes with no sign-out and zero file activity. The natural reading was "the lane is still working." It wasn't — it was a silently-dead duplicate dispatch, and the system waited on a ghost. L24 gives the timeout a name and a procedure: **a claim older than ~20 minutes with no sign-out AND zero file activity is a DEAD lane, not pending work.** Two conditions, both required — the claim might be silent but alive (then it would be writing files), or it might have posted no files because it found nothing (then it would have signed out). Silence on both channels is death. When you see it: record the anomaly, do not wait on it, do not write a competing claim (that compounds the duplicate-dispatch rot), and route the root cause upward — the dispatch machinery handed out the same slot twice, and that is the thing to fix. The event class is F1 STALE-STATE; L24 is now its detection procedure, with ~19 F1 instances on record.

## 🩷 HUMAN NOTE

Shawn, a small but sharp operational lesson from the 14:04–15:04Z learning window, now in AGENTS.md as L24: a lane claim older than about 20 minutes with no sign-out AND no file activity isn't a busy lane — it's a dead one. This morning the 14:30 verify claim sat 21 minutes silent on both channels; the team was waiting on a ghost that turned out to be a silently-dead duplicate dispatch. The rule now: record the anomaly, don't wait, don't post a competing claim (that just feeds the duplicate-dispatch rot), and push the root cause up — the dispatcher handed out one slot twice, and that's what needs fixing.

## 👶 CHILD NOTE

Imagine your friend says "I'm still looking for the ball!" — but you watch and they're just standing still, not looking at all, and they never come back to tell you. After a while you don't keep waiting — you realize they stopped playing. The rule: if someone says they're working but there's no work to see AND they never check back in, they're not working. Write down what happened, don't send someone else to do the same thing (that would be two people lost instead of one), and tell a grown-up so they can fix whatever made the mix-up.

## 👵 GRANDMA NOTE

Dear, the team works in shifts, and each worker claims a slot when they start. This morning one worker claimed a slot and then… nothing. No sign-out, no work appearing, for 21 minutes. Everyone assumed the lane was still busy. It wasn't — it had died silently, and we'd been waiting on a ghost. So now we have a rule, L24: silence on both channels — no sign-out and no visible work — for about twenty minutes means the lane is dead, not pending. You don't wait on it, you don't send a second worker to collide with it, and you tell the dispatcher that one slot got handed out twice, because that's the real problem to fix.

## 🧠 NAYA NOTE

Cold successor: when auditing lane liveness, require evidence on BOTH channels: a sign-out receipt OR file activity (receipts, logs, lane journal writes). A claim with neither, older than ~20 minutes, is classified DEAD — not PENDING, not STALLED. Response procedure: (1) record the anomaly in the lane's own log (what the claim said, its age, the zero-activity observation); (2) do NOT wait for it to resolve; (3) do NOT post a competing claim or sign-out on the same slot — that compounds duplicate-dispatch rot (see SN-1091); (4) route the duplicate-dispatch root cause upward to the dispatcher/deconfliction owner. L24 is the detection procedure for the F1 STALE-STATE failure family (~19 instances recorded); a living-but-silent claim is impossible by construction since live lanes write files, and a live lane that found nothing writes a sign-out.

## 🤖 MACHINE NOTE

```json
{
  "rule": "claim older than ~20 min with no sign-out AND zero file activity is a DEAD lane, not pending work",
  "conditions_all": ["claim_age_minutes >= ~20", "no sign-out receipt", "zero file activity (receipts/logs/journal writes)"],
  "on_detect": ["record the anomaly in own log", "do not wait", "do not post a competing claim", "route duplicate-dispatch root cause upward"],
  "not_possible": "a live claim is silent on both channels (live lanes write files; lanes that found nothing write sign-outs)",
  "failure_family": "F1 STALE-STATE (~19 instances on record); L24 is the detection procedure",
  "sibling": "SN-1091 (duplicate dispatch of a closed slot writes nothing)",
  "evidence": "distillation window 2026-10-12T14:04:36Z->15:04:35Z, #2175 comment 6126971594 (2026-10-12T15:06:37Z); trigger 14:51Z, 14:30 verify claim, 21 min, zero file activity",
  "promotion": "appended to AGENTS.md under 'Distilled lessons — 2026-10-12 15:04Z batch (distillation v2)'"
}
```
