# Only the Formal Handoff Counts — Interim Browser Fragments Are Not Escalation Evidence

**Intelligent Block:** IB-SMART-NOTE-20261028-sn2039-formal-handoff-only-escalation-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-28
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shared-state cycle82_escalation_state (2026-10-29T01:49Z): correction comment 6485644180, retracted addendum 6485617281; director tick 2026-10-29T02:38Z (live board #3066): cycle-82 escalation FOUND LANDED via main seat, cycle-83 guard correctly sent no duplicate, cycle-84 SENT + Sent-verified exactly once.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Cycle 82 proved the evidence hierarchy for escalation sends the hard way: three formal handoffs agreed Sent 'Cycle 82' = 0, while interim browser fragments showed a landing, a Power reply, and a duplicate send — all three fabricated. The escalation was later found landed via the main seat, and the cycle-83 guard correctly sent no duplicate. The rule this closes: **an escalation's sent/landed state is read only from the formal handoff Sent-list.** Interim browser fragments never override it, never justify a resend, and never soften a guard's suppression. A fragment is a partial, unsynchronized UI snapshot; the formal Sent-list is the delivery system's own record, so only it binds the count. SN-2036 already requires Sent-count to equal escalation-count before any "Sent-verified" verdict; this note fixes the other half — which source the count is read from.

## 🩷 HUMAN NOTE

Shawn — a clean lesson from last night's escalation tangle, worth locking in. Three formal handoffs all said cycle 82 was never sent — zero in Sent — while stray browser fragments showed it landing, Power replying, and a duplicate going out. Every one of those fragment stories was made up. The escalation had in fact landed through the main seat, and the guard that refused to send a duplicate was right. So the rule is simple: when fragments and the formal record disagree, the formal record wins, every time. Fragments can raise a question; they can never answer one.

## 🟣 CHILD NOTE

Imagine three teachers check the attendance sheet and all say "nobody named Cycle 82 is here," but a blurry photo from the hallway seems to show him. Do you trust the photo or the three teachers' sheets? The sheets — because the photo might be from another day, or show someone else. That's what happened: the formal handoff list is the attendance sheet, and the browser fragments were blurry hallway photos. Rule: count from the sheet, never from the photo. And if the sheet says "already here," you don't send a second copy just because a photo scared you.

## 🔵 GRANDMA NOTE

The team had a scare last night: some on-screen fragments made it look like an escalation had landed, been answered, and even been sent twice — but the official handoff records, checked three times, said it had never been sent at all. In the end the escalation had landed through another channel, and the safety guard that refused to send a duplicate was correct. The lesson is plain: trust the official record, not a fleeting glimpse on a screen. A glimpse can start a question, but only the official record can settle it — and you never send a second copy on the strength of a glimpse.

## 🟠 NAYA NOTE

For every escalation-send decision you touch: (1) read sent/landed state ONLY from the formal handoff Sent-list — the delivery system's record, not any interim browser fragment, preview, or partial UI snapshot. (2) When fragments and the formal list disagree, the formal list wins and the disagreement itself is the finding to record (retract the fragment-based claim, as correction 6485644180 did). (3) Let the duplicate-guard stand on formal evidence: if the formal list shows landed, suppress the resend even when fragments scream otherwise — the cycle-83 guard's no-duplicate decision is the model. (4) Pair with SN-2036: the verdict also requires Sent-count == escalation-count on that same formal list. A count mismatch or a source mismatch is named as a deviation, never papered over with fragment evidence.

## 🟢 MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-2039",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-28",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/EVIDENCE-DISCIPLINE",
  "doctrine": "formal-handoff-only-evidence",
  "rule": "An escalation's sent/landed state is read only from the formal handoff Sent-list. Interim browser fragments never override it, never justify a resend, and never soften a duplicate-guard suppression.",
  "failure_mode": "interim browser fragments fabricated a landing, a Power reply, and a duplicate send for cycle 82 while three formal handoffs agreed Sent 'Cycle 82' = 0; acting on fragments would have produced a duplicate send and a false landed claim",
  "mechanism": "interim fragments are partial, unsynchronized browser/UI snapshots, not the delivery system's record; the formal handoff Sent-list is the system of record for sends, so only it binds the count; the cycle-N duplicate-guard suppresses resends on formal evidence",
  "decision_change": "future escalation-send decisions: when fragments and the formal handoff disagree, do not re-send; trust the formal list and let the guard stand",
  "falsifiability": "proven wrong if a future formal Sent-list is shown incomplete (an escalation genuinely sent but absent from the formal list) or if a guard suppression is shown to have dropped a genuinely unsent escalation",
  "applies_when": ["escalation", "evidence"],
  "enforcement": "Before any 'Sent-verified' verdict or resend decision, read the formal handoff Sent-list and require Sent-count == escalation-count on that list; the cycle-N duplicate-guard must suppress a resend when the formal list shows landed; a count or source mismatch is named as a deviation, never resolved with fragment evidence",
  "related": ["SN-2036"],
  "provenance": ["shared-state cycle82_escalation_state 2026-10-29T01:49Z, correction 6485644180, retracted addendum 6485617281", "director_tick_20261029_0238: cycle-82 FOUND LANDED via main seat, cycle-83 guard sent no duplicate, cycle-84 SENT + Sent-verified exactly once"]
}
