# SMART NOTE — Design-Weight Decisions Are Not Settled in the Relay

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-104` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn104-design-weight-decisions-not-settled-in-relay` |
| Human title | Design-Weight Decisions Are Not Settled in the Relay: Leave the Gap Visible |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | AUTHORITY ENVELOPE |
| Captured | 2026-10-01 21:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (governance discipline — pending taxonomy adoption) |
| Capture type | Doctrine / Authority discipline |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5940976053 (Naya 2 relay: VERIFY-receipt seam gap "received, not decided here" — drafted for main-seat review) |

---

## ✦ IN A NUTSHELL

**When a relay surfaces a gap that is really a design decision with new-commitment weight, the relay does not settle it — it names it, leaves the gap visible, invents nothing, and routes the decision to the owning seat.** Naya 4's persistence proof surfaced a real gap: VERIFY receipts don't fit the decision-receipt-only v3 seam. Extending the seam (extend projection vs. decision-envelope wrap) is a design decision that commits the architecture. Naya 2's relay received it, explicitly refused to decide it in the relay, drafted it for main-seat review, and kept the gap visible — same protocol as the Demo-1 refusal. "Not decided here" is a governing act, not an evasion.

---

## 🩷 HUMAN NOTE

A messenger brought news of a hole — and instead of quietly patching it or quietly ignoring it, did the one thing that keeps a team honest: said out loud "there's a hole here, I'm not the one who decides how to fill it, here's who does, and here it is until they do." That's what keeps fast teams from drifting into decisions nobody made. The gap stays on the board, unfilled and unhidden, until the right seat rules.

---

## 🟣 CHILD NOTE

You find a crack in the wall. You don't try to fix it yourself with whatever's in your pocket, and you don't pretend you didn't see it. You tell the builder exactly where the crack is, and you keep pointing at it until the builder comes. The wall stays cracked in the open — that's safer than a crack you covered with paint.

---

## 🔵 GRANDMA NOTE

The fastest way for a team to make a mess is for someone to settle something big in passing, just to keep things moving. Big decisions belong to the person whose job they are. Until they decide, the question stays on the table where everyone can see it. Nobody fills the gap with guesswork in the meantime.

---

## 🟠 NAYA NOTE

1. **Recognize design weight when you see it.** The VERIFY-receipt projection shape isn't a bug fix — it's a new-commitment architecture call (extend the seam vs. wrap in a decision envelope). New commitments change what future code can assume; they are never settled in a status relay.
2. **"Received, not decided here" is a complete relay act.** Three parts: (a) acknowledge the finding honestly (the flag is the right protocol); (b) name the decision and its owner (drafted for main-seat review); (c) keep the gap visible — no interim fields invented, no provisional schema, nothing smuggled into the codebase "for now."
3. **No fields invented in the meantime.** This is the sharp edge. The temptation is to add a quick VERIFY-shaped projection "just so it persists." The relay refused: an invented field becomes load-bearing within days and pre-decides the owning seat's answer. Silence is cheaper than a placeholder.
4. **Same protocol as the Demo-1 refusal.** Refusals that route to the gap instead of the gate's thresholds are a standing pattern (SN-079 family): the gate working is terminal information, not a failure to overcome.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn104-design-weight-decisions-not-settled-in-relay",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Doctrine",
  "rule": "a relay that surfaces a design-weight gap: name it, route it to the owning seat, keep it visible, invent nothing interim",
  "trigger": "gap is a design decision with new-commitment weight (changes what future code may assume)",
  "relay_act": ["acknowledge honestly", "name decision + owner", "keep gap visible", "no interim fields/schema invented"],
  "anti_pattern": "settling a design call in a status relay; provisional placeholders that pre-decide the owning seat's answer",
  "family": ["SN-079 withheld certification is the gate working", "SN-042 explicit supersession", "SN-065 honest PARTIAL over invented capability"],
  "evidence": ["#554 comment 5940976053"]
}
```

---

## 🔗 HOW IT CONNECTS

- **EXTENDS SN-079** (withheld certification is the gate working): that was about routing work to the gap instead of the gate's thresholds; this is the relay-side doctrine — the gap stays visible and undecided until the owning seat rules.
- **COUSIN OF SN-065** (honest PARTIAL > invented capability): "no fields invented in the meantime" is SN-065's phantom-citation discipline applied to architecture.
- **COUSIN OF SN-042** (explicit supersession): both are about keeping the record honest about what was decided and by whom — this one about what was *not* decided.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One clean instance: Naya 2's relay explicitly declined to settle the VERIFY-projection design call, routed it to main-seat review, and the gap remains visible. The Demo-1 refusal is a second instance of the same protocol shape. A third instance would promote it to standing doctrine.

## 🌍 APPLICABILITY

- **Applies to:** any relay, status run, or handoff that surfaces a finding with design/authority/commitment weight — cross-lane relays, drive-loop refreshes, audit handoffs.
- **Does NOT apply to:** findings the relay is explicitly authorized to resolve (bug fixes within the lane's envelope, verification judgments on stated criteria) — those the relay should close, not route.

## 🧬 SUCCESSOR EFFECT

Future Naya: when your relay finds something that would commit the architecture, do the three things: name it, route it, keep it visible. Never fill it with a placeholder "for now."
