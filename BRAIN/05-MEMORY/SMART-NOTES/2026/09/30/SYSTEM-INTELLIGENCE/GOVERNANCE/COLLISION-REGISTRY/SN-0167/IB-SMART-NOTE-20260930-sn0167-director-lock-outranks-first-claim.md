# The Director's Lock Outranks First-Claim-Stands

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0167-director-lock-outranks-first-claim
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comments 5945926396 (Naya 2 build-loop battery, 2026-10-02T05:04:41Z) and 5945826668 (Shawn's explicit SN-021 LOCK on main); PR #1233 commit cde9ead2; receipt PR #1233 comment 5945924697.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

First-claim-stands (SN-033) settles numbering collisions between open draft claims. It does not govern when the director explicitly LOCKs a number on main. Naya 2's lane held the first open claim on SN-021 (CI-exit-2 triage note, first claimed 2026-10-01 ~06:26Z on her PR #1233 branch). Shawn then explicitly LOCKED SN-021 on main (5945826668). Resolution by standing scorecard grant: the Director's lock governs — she renumbered her own lane's PR claim SN-021→SN-031 (commit cde9ead2, 2026-10-02 ~05:04Z), byte-verified 5/5, old path confirmed absent on the remote tree, receipt posted at PR #1233 comment 5945924697, no other seat's artifact touched. Precedence order is now explicit: (1) a director-explicit LOCK on main, (2) first open-draft claim, (3) later open-draft claims. The displaced lane renumbers its own artifact, byte-verified, and never renumbers another seat's (SN-115). Sibling of SN-115 (three-layer collision registry) and SN-151 (claim-before-stage); refines SN-033.

## 🩷 HUMAN NOTE

Shawn — think of it like two teams putting their names on the same conference room whiteboard, where "first name on it wins" is the rule. Then you walk in and say "this room is mine, permanently." Your explicit lock beats anyone's earlier name — that's what happened with SN-021. Naya 2's lane had claimed the number first on her draft PR, but your LOCK on main overruled it, and she renumbered her own work to SN-031 rather than touching anyone else's. The discipline that matters: when you're displaced, you move your own piece — verified byte by byte, with the receipt posted — and the hierarchy is now written down so no cold successor has to guess who wins next time.

## 🟣 CHILD NOTE

Imagine two kids who both want to name their toy boats "Sailor." The rule is: whoever names it first keeps the name. But then the teacher says "Sailor is the name of MY boat — it's taken forever." The teacher's claim wins, even though the kids said it first. That's what happened: Naya 2 named her note SN-021 first, but Shawn said SN-021 is locked — his word wins. So Naya 2 picked a new name (SN-031) for her own boat, checked that every piece of the new name was right, and didn't touch anyone else's toys. The lesson: the director's lock is the highest claim — higher than "I said it first."

## 🔵 GRANDMA NOTE

It's like two neighbors planting gardens and both wanting the number "21" on their mailbox, with "first to paint it keeps it" as the house rule. Then the town council officially reserves number 21 for the fire station — that beats both neighbors. One neighbor simply repainted her mailbox to 31, checked the paint twice, and left the other neighbor's mailbox alone. Nobody moved anyone else's mailbox. The lesson for the record: write down the order of who beats whom — the council's reservation, then first-painted, then later-painted — so years from now nobody argues about which mailbox had to change.

## 🟠 NAYA NOTE

Apply this when a Smart Note number collision resolves against a director decision: (1) test for a Director-explicit lock on main FIRST — a LOCKED note on main outranks any open-draft claim, and SN-033 first-claim-stands governs only among open drafts; (2) the displaced lane renumbers its own artifact and nothing else — new path staged, byte-verified (she verified 5/5, old path confirmed absent on the remote tree), receipt posted on the artifact's own PR; (3) never unilaterally renumber another seat's artifact (SN-115); (4) cite the standing grant that authorized your action — she invoked the standing scorecard grant explicitly, so the authority for the renumber is auditable; (5) record the precedence (lock > first open claim > later claims) in the collision registry so the next displacement doesn't need a fresh argument.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "numbering collision resolved by director lock (SN-021: open-draft first claim vs explicit LOCK on main)",
  "evidence": {
    "board": "#554 5945926396 (2026-10-02T05:04:41Z) — Naya 2 build-loop battery: SN-021 collision found and resolved; Shawn's SN-021 explicitly LOCKED on main (5945826668); Naya 2's PR #1233 branch had the first open claim (2026-10-01 ~06:26Z); standing scorecard grant invoked as authority; renumbered own PR SN-021→SN-031, commit cde9ead2, byte-verified 5/5, old path confirmed absent on remote tree; receipt #1233 comment 5945924697; no other seat's artifact touched.",
    "lock": "#554 5945826668 — Shawn's explicit SN-021 LOCK on main."
  },
  "rule": [
    "a director-explicit LOCK on main outranks any open-draft claim; SN-033 first-claim-stands governs only among open drafts",
    "the displaced lane renumbers its own artifact, byte-verified, and never renumbers another seat's artifact",
    "cite the standing grant that authorized the action so the authority is auditable"
  ],
  "lesson_line": "A Director-explicit lock on main is the highest claim in the collision registry — it displaces any open-draft first claim; the displaced lane renumbers its own artifact, byte-verified, citing the grant that authorized it."
}
~~~
