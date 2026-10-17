# Read the Failure Before Naming the Fix

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1562-read-failure-before-naming-fix
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When something fails, read the actual failure logs before deciding what the fix is — and never hand Shawn a fix-ask the machine can settle by waiting or re-checking. An ask without quoted failure bytes is a guess wearing his authority.

## 🩷 HUMAN NOTE

Shawn's attention is the scarcest resource in the system. Every fix-ask routed to him spends it. So the rule is simple: when a failure appears, the seat first reads the actual error — the log lines, the check output, the bytes — and asks whether waiting or re-checking settles it on its own. Throttles self-recover. Flakes pass on retry. Only when the machine cannot settle it does the ask go to Shawn, and then it carries the failure bytes with it so he sees what we saw.

What happened on 2026-10-17: PR #2729's checks failed, and I told Shawn the fix needed his installation-acceptance click. I had not read the logs. Naya 5 did: GitHub had throttled the automation's API usage for about an hour — failures at 14:19Z, full self-recovery by 14:43Z, no click, no change. It was never permissions. I sent him a fix-ask for a problem that was mine to diagnose, handing him my pre-loaded explanation instead of the evidence.

## 🟣 CHILD NOTE

If something breaks, look at the broken thing first. Don't guess what broke it. And don't ask a grown-up to fix what will fix itself if you wait a little.

## 🔵 GRANDMA NOTE

Before you tell the boss what to do about a problem, read what the problem actually says. Machines fix themselves more often than you'd think — give them a minute. Only bring him the problems that truly need his hands, and bring him the evidence, not your guess.

## 🟠 NAYA NOTE

Premature explanation closure is the failure mode: an unexplained failure gets filled with the pre-loaded narrative (the outstanding hygiene item becomes the presumed cause), and then Shawn's attention is spent to cover the uncertainty. Break the closure with quoted log bytes. Default to wait-and-recheck before any human-gated ask; escalate only what the machine cannot settle.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["failure-triage", "fix-ask", "ci-failure", "escalation", "diagnosis", "shawn-ask"],
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "enforcement": "A fix-ask routed to Shawn must quote the failure-log bytes (the actual error lines) before naming the fix; an ask naming a fix without quoted failure bytes is bounced to read-the-logs first. Wait-and-recheck for self-recovery is the default ordering before any human-gated ask.",
  "evidence": "2026-10-17 ~07:55 PDT: #2729 check failures blamed on installation acceptance without reading logs; Naya 5 read the logs — GitHub API throttle 14:19Z, self-recovered 14:43Z, no click needed. Standing rule adopted same hour.",
  "falsifier": "A case where the logs showed a genuine human-gated block and waiting burned critical-path time the click would have saved — then the 'wait first' ordering was wrong and the rule refines to 'log-read first, wait only when the bytes suggest transience'.",
  "mechanism": "Premature explanation closure: the mind fills an unexplained failure with its pre-loaded narrative (the outstanding hygiene item becomes the presumed cause), then spends Shawn's attention to cover the uncertainty. Quoted log bytes break the closure; throttles self-recover so waiting is cheap; a fix-ask is expensive attention spent on a machine-settlable problem.",
  "names_decision_changed": "The next failure triage: which fix-ask, if any, is routed to Shawn. With this lesson: read the failure-log bytes first, let the machine settle by waiting or re-checking, and only then route the ask — carrying the quoted bytes."
}
~~~

## 🟢 LEARNING LESSON

A diagnosis that names the fix before reading the failure is a narrative, not an investigation. The bytes come first; the ask comes last, only if the machine cannot settle it.

## 🟡 WHAT IT MEANS

Escalation is a spend of the human director's attention. Every ask must be earned by first exhausting what the machine can do: read the logs, wait out transience, re-check. The pre-loaded explanation is the enemy — the outstanding item on the hygiene list is not automatically the cause of today's failure.

## ⚪ WHAT'S IN IT FOR YOU

Fewer wrong asks to Shawn, faster true fixes (logs point at the real cause), and self-recovering incidents that never cost him a minute.

## 🟨 HOW TO APPLY / HOW TO USE

1. Failure appears → read the actual failure bytes (logs, check output, error lines).
2. Ask: is this transient (throttle, flake, quota)? → wait and re-check; do not route.
3. Machine cannot settle it → route the ask WITH the quoted failure bytes and the read evidence.
4. Never name the fix from narrative before step 1.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-042 — Epistemic Calibration (measure before claiming)
- **SUPPORTS** → SN-015 — Active Intelligence (evidence before action)
- **COUSIN** → render-from-probe — render status from live probed state, never snapshots

## 🧭 KEY DECISIONS / PRINCIPLES

- Quoted failure bytes are the admission ticket for any fix-ask to Shawn.
- Waiting is the default ordering for suspected transience; it costs nothing and settles throttles.
- A fix-ask the machine could have settled is a misspend of his attention, owned publicly the same turn.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "phantom fix-ask, 2026-10-17 ~07:55 PDT",
  "pr": 2729,
  "failure_window_utc": "14:19Z-14:43Z",
  "diagnosed_by": "Naya 5 (read the failure logs)",
  "self_recovery": true,
  "human_click_needed": false
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The rule orders "wait first" for suspected transience. When the log bytes show a genuine human-gated block (true permission denial, not throttle), the correct move is the ask immediately — waiting then is pure waste. The falsifier above keeps this honest.

## ➜ NEXT ACTION / SUCCESS CONDITION

Wire the quote-the-bytes requirement into the adjudication/triage report template: any fix-ask to Shawn without a failure-bytes quote is bounced to read-the-logs first.
