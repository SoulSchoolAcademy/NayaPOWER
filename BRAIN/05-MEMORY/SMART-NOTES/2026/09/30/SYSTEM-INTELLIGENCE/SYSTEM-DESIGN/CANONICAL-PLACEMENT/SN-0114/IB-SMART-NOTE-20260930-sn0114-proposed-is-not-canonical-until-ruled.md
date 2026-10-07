# SMART NOTE — Proposed Is Not Canonical — Until Ruled

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-114` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn114-proposed-is-not-canonical-until-ruled` |
| Human title | Proposed Is Not Canonical — Until Ruled |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | CANONICAL-PLACEMENT |
| Captured | 2026-10-01 23:15:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (canonical-set governance) |
| Capture type | Governance / Decision |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5942213324 (Naya 4: room-count reconciliation — 11 canonical rail rooms, notes/system recorded PROPOSED; PR #1283), #554 comment 5942413426 (NAYA seat: NOT-RIGHT FINDING — canonical 11-room Hub vs PR #1278 13-room rail; deliberate-promotion rule) |

---

## ✦ IN A NUTSHELL

**The app rail rendered 13 rooms; the canonical machine contract defines 11. The reconciliation did neither of the two lazy moves: it did not silently extend the canonical set to match the implementation, and it did not strip the implementation's extra rooms. Instead the room model records 11 canonical rail rooms (unchanged), welcome/identity classified as journey surfaces (not rail rooms), and the two additions — `notes` (Smart Notes capture) and `system` (scorecard/roadmap/registry) — recorded as PROPOSED, not canonical, until justified, scored, and ruled on. The standing rule, stated in the not-right finding: if product evidence later proves either deserves primary-room status, promote it deliberately and update the canonical contract.** The discipline: canonical sets grow by deliberate promotion, never by implementation drift. Record the proposed item IN the model as PROPOSED — visible, honest, ruled-on-later — rather than letting shipped code silently become product truth.

---

## 🩷 HUMAN NOTE

A library's catalog says it holds 11 sections, but the new branch library built 13 shelves. You don't secretly rewrite the catalog to say 13, and you don't tear down the two new shelves. You annotate the catalog: "11 canonical sections; shelves 12 and 13 are proposed — pending review." If readers later prove those two shelves belong in the official catalog, you promote them properly and print a new catalog. The rule protects both the builders (their work isn't deleted) and the truth (the catalog never silently changes).

---

## 🟣 CHILD NOTE

Your class list says there are 11 official teams. Two new groups showed up and play great games, but they're not on the list. You don't erase the list to add them quietly, and you don't kick them out either. You write on the list: "11 official teams + 2 try-out teams." If they prove they belong, the teacher makes them official. The list only changes when someone says so out loud.

---

## 🔵 GRANDMA NOTE

The official menu lists 11 dishes, but the kitchen started serving two more. The owner doesn't sneak them onto the printed menu overnight, nor does she ban them. She marks them "chef's specials — pending." If customers love them, they go on the menu properly. Printed truth changes by decision, never by drift.

---

## 🟠 NAYA NOTE

1. **Canonical sets grow by deliberate promotion, never by implementation drift.** The 11-room rail was canonical from the frozen concept; the implementation's 13 did not get to silently redefine it. The count stays 11 until justification, scoring, and a ruling say otherwise.
2. **Record the proposal IN the model, as PROPOSED.** The reconciliation put `notes` and `system` into `PROJECT-INTELLIGENCE.MACHINE.json`'s `room_model` with explicit PROPOSED status — visible, honest, ruled-on-later. Deleting the proposal would hide work; absorbing it silently would corrupt the contract. The third option is the right one: model it with its true epistemic state.
3. **Classify what is not in the set.** Welcome/identity were reclassified as journey surfaces, not rail rooms — the reconciliation resolved the count dispute by clarifying the taxonomy, not by arguing about the number. When a membership dispute arises, first check whether the items are even the same kind of thing.
4. **Write the promotion rule down.** "If product evidence later proves either deserves primary-room status, promote it deliberately and update the canonical contract." A canonical set without a stated promotion rule invites silent drift; with the rule stated, drift becomes a not-right finding anyone can file.
5. **The not-right finding is the enforcement arm.** The 11-vs-13 divergence was filed as a NOT-RIGHT finding with evidence (runtime source confirms the 13-entry rail), impact (navigation/IA divergence), and a recommended reconciliation — not a rewrite. Canonical discipline needs a finding format, not just a contract.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn114-proposed-is-not-canonical-until-ruled",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Governance decision",
  "rule": "canonical sets grow by deliberate promotion, never by implementation drift",
  "instance": {
    "canonical": "11 rail rooms (Smart Feed, Your Intelligence Today, Your Reports, Intelligent Library, Smart Connect, Smart Ledger, Your Connections, Smart Lists, Smart Mail, Smart Spaces, Settings)",
    "proposed": ["notes (Smart Notes capture — has concept lineage)", "system (scorecard/roadmap/registry — builder-facing scaffolding)"],
    "reclassified": "welcome/identity = journey surfaces, not rail rooms",
    "recorded_in": "HUB/PROJECT-INTELLIGENCE.MACHINE.json room_model (PR #1283)",
    "promotion_rule": "promote deliberately + update canonical contract IF product evidence proves primary-room status"
  },
  "discipline": {
    "never": "silently extend the canonical set to match the implementation; strip the implementation's proposed items",
    "always": "record proposed items IN the model as PROPOSED — visible, honest, ruled-on-later"
  },
  "evidence": ["#554 comment 5942213324", "#554 comment 5942413426", "PR #1283 (room reconciliation, candidate)", "PR #1278 (renders 13, runtime.js ROOMS[13])"],
  "family": ["SN-062 the count ledger is part of the change", "SN-078 merge adding BRAIN/ files must regen index", "SN-104 design-weight decisions not settled in the relay"],
  "open": ["Shawn's ruling on whether notes/system ever become primary rail rooms"]
}
```
