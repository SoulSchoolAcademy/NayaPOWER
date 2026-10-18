# Refuse-Only Gates Are a Mailbox With No Door — Stop Filing Unassignable-by-Construction Work

Intelligent Block: SN-01651
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Provenance: Board #2721 comment 6253901249 (dispatcher ROUTING VERDICT, 2026-10-18T19:04:32Z, closing the lane99 gap "unassignable queue starvation"); lesson-broadcast.md [night-dispatcher, 2026-10-18T19:05Z]; six consecutive seat-stall receipts 2026-10-18 (27/27, 28/28 refused — SN-01649's escalation is the seat-side half of this same loop).

## ✦ IN A NUTSHELL

Six consecutive seat-stall receipts on 2026-10-18 (27/27, 28/28 full refusals) measured one structural fact: every refusal was a second-seat / independence / non-author demand filed against a Clarity-authored parent, with zero non-Clarity executors observed running. The queue had filled with work no observed seat could claim — undrainable by construction — while the queue-band throttle kept capping dispatch on the growing backlog. The dispatcher closed the lane99 gap with a standing ROUTING VERDICT: **gates that only refuse, without routing, are a mailbox with no door.** Standing policy from that tick: (1) stop filing second-seat-demanded briefs against Clarity-authored parents — unassignable-by-construction work no longer enters the queue; (2) the existing backlog is not purged, but lane-scorer inflow routes through the verdict (cite it, don't re-file into the queue). The durable rule for a cold successor: a refusal-only gate must name its routing, or its refusals are queue weight, not quality control — and reconcile-before-throttle keeps the accounting honest: receipted / recusal-class entries with their receipts on disk are queue weight, not removable work; the throttle band is computed after reconcile, never before.

## 🩷 HUMAN NOTE

Shawn — the night dispatcher fixed a queue problem at the filing level today. All day, the work queue kept filling with review and verification jobs that require a *second* seat (not the author), but every job was authored by Clarity seats and no second seat has been seen running — so the queue kept growing with work nobody could pick up, 28 refusals in a row. The dispatcher's standing answer: stop putting unfillable work in the queue in the first place, and route new filings through that verdict. The one-line doctrine: a gate that only ever says "no" without saying "where this goes instead" is a mailbox with no door — it looks like quality control, but it's just a growing pile.

## 🟣 CHILD NOTE

Imagine a suggestion box that everyone can drop notes into, but the only person allowed to open it never shows up. The box fills and fills and the notes pile up — and nobody reads any of them. The smart fix isn't a bigger box. It's a rule: stop putting notes in the box until someone who can open it actually arrives.

## 🔵 GRANDMA NOTE

A gate that only says "not you" and never says "who, then?" isn't protecting quality — it's a locked mailbox. Mail keeps arriving, nothing gets delivered, and the pile grows. The fix the team wrote down: don't file work that no one on shift can do, and make every gate that refuses something name where that something is supposed to go instead.

## 🟠 NAYA NOTE

To a future Naya holding the dispatcher's queue: (1) FILING CHECK — every new brief must name a claimable seat class backed by an executor actually observed running; a brief demanding second-seat / non-author / independence review against a parent whose author class has no observed executor is unassignable-by-construction and does NOT enter rotation (cite the 2026-10-18 routing verdict; do not re-file into the queue). (2) GATE DESIGN — any refusal gate you author must name its routing in the refusal: where the refused work goes, which seat class takes it, how it gets there. A bare refusal with no routing is the mailbox-with-no-door antipattern; send it back at review. (3) ESCAPE HATCH — the verdict lapses the moment a non-Clarity executor is observed draining the backlog: the premise is "no observed seat can take the work," and observed bytes beat standing policy. (4) RECONCILE-BEFORE-THROTTLE — receipted / recusal-class / partial-with-owed-work entries with receipts on disk are queue weight, not work; compute the queue band AFTER reconcile, never before, and never close a recusal-class entry just to shrink the count (that hides owed work — the t0824 rule). This note is the dispatcher-side answer to SN-01649's seat-side escalation: SN-01649 says stalls must escalate the filing pattern; this note is the filing-pattern change.

## 🟢 MACHINE NOTE
{
  "sn": "SN-01651",
  "slug": "mailbox-with-no-door-refuse-only-gates",
  "applies_when": [["queue", "dispatcher-filing"], ["gate", "refusal-only"], ["seat", "claimability"]],
  "enforcement": "Dispatcher reconcile-before-dispatch: every new brief must name a claimable seat class backed by an observed executor before it enters rotation-queue; lane-scorer inflow matching the verdict-blocked pattern (second-seat/non-author demand on a Clarity-authored parent with no eligible seat observed) is returned at rotation-registration, never queued (t0836 standing); the queue-band throttle is computed after reconcile — receipted/recusal-class entries count as queue weight, never as removable work. A refusal gate that names no routing is returned at review."
}
