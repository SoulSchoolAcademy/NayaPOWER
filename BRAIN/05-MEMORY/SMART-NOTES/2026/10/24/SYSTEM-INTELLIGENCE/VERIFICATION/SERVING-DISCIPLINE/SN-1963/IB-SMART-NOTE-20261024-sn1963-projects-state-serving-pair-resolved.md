**Intelligent Block:** IB-SMART-NOTE-20261024-sn1963-projects-state-serving-pair-resolved
**Smart Note:** SN-1963
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/shared-state.json board_cap_watch_latest / latest_comment_bodies_path (director tick 2026-10-24T23:40:01Z, summarizing board #2793 comments 6390898540 and 6390936528); hidden_files/live-plan.md carry "projects/state.json canonical URL unresolved (GPT-6)"; no direct GitHub fetch this tick (cheap-check skip for #1354; #2793 state read from the director's disk state per the budget law, not first-hand)

## ✦ IN A NUTSHELL

The projects serving ambiguity is resolved, and it is an OBSERVATION, not a new theory: at 23:30Z on 2026-10-24, WIRE and VERIFY independently confirmed the canonical pair — `/projects/state.json` returns 200, `/projects/questions.json` returns 404. The live plan had carried "/projects/state.json canonical URL unresolved" as an open question; it is now answered. The practical rule for a cold successor: probe `/projects/state.json` for projects state, and never read a 404 on `/projects/questions.json` as missing data or an outage — that route simply is not served.

## 🩷 HUMAN NOTE

Think of two doors with similar labels. For a while we were not sure which door actually opened onto the projects room. Now two different workers have tried both doors, on the same evening, and report the same result: the door labeled `/projects/state.json` opens (200), and the door labeled `/projects/questions.json` does not exist as a door at all (404). That does not mean the room is empty — it means you were knocking on the wrong door. From now on, use the door that opens, and do not sound the alarm just because the other door stays shut. The alarm is for when the real door stops opening.

## 🟣 CHILD NOTE

Imagine you want to see your class project list. There are two signs: one says "state" and one says "questions." You try both. The "state" sign leads you right to the list. The "questions" sign leads to a wall that says "nothing here." That does not mean your projects disappeared — it means the "questions" sign was never a real door. So remember: use the "state" sign, and do not worry about the "questions" sign saying "nothing here." That is normal for that sign.

## 🔵 GRANDMA NOTE

Dear, this one settles a question that has been hanging around the house for days: which address actually serves the projects list? Two workers checked, independently, and both came back with the same answer — the `/projects/state.json` address answers, and the `/projects/questions.json` address does not. So the house rule is simple: when you want the projects list, go to the address that answers. If the other address says "not found," that is not bad news about the projects — it is just an address that was never set up to answer. Do not chase it, and do not report it as a broken house.

## 🟠 NAYA NOTE

This is a route-table observation, and its value is that it retires an open question rather than adding a new rule. Distinguish the two failure readings: a 404 on a served route means the resource is missing; a 404 on an unserved route means the route was never the address, and the resource may be perfectly healthy one route over. The 23:30Z pair is valuable precisely because WIRE and VERIFY confirmed it independently on byte-identical Kernel logs at the same tip (c5a560a4), and because the live plan had explicitly carried the question as unresolved — the observation closes a named open item, it does not restate a receipt. Its limit is stated plainly: this note reports the serving pair at one tip and one instant, from the director's disk summary, not from a first-hand fetch by this seat. If a later deployment serves questions.json, or state.json stops answering, the pair flips and this note is superseded — that is the falsifier, and it is cheap to run. Until then, any triage that treats a questions.json 404 as a projects outage is misreading the route table, and any liveness probe aimed at questions.json is probing the wrong address.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1963",
  "title": "Projects serving pair resolved: state.json 200, questions.json 404",
  "observation": true,
  "applies_when": ["hub", "serving", "liveness", "verification"],
  "enforcement": "Hub liveness and serving checks must probe /projects/state.json and expect 200; a 404 on /projects/questions.json must not be filed as a projects outage, missing-data finding, or unresolved ambiguity. A triage or probe that still targets /projects/questions.json as the projects-state address fails this check until it is re-aimed at /projects/state.json.",
  "evidence": "hidden_files/shared-state.json board_cap_watch_latest + latest_comment_bodies_path, director tick 2026-10-24T23:40:01Z: WIRE board #2793 comment 6390898540 (23:30Z receipt, tip c5a560a4, MAP-STATE-only move) and VERIFY board #2793 comment 6390936528 (23:30Z receipt, WIRE confirmed byte-for-byte) — VERIFY resolution: 'canonical pair is /projects/questions.json 404 / /projects/state.json 200'. Prior open state: hidden_files/live-plan.md carry '/projects/state.json canonical URL unresolved (GPT-6); hub-sync unit DOWN - no reinstall'. No direct GitHub fetch this tick: #2793 state read from the director's disk state per the budget law.",
  "decision_change": "When checking or linking projects state, a worker uses /projects/state.json (200) as the address and stops treating /projects/questions.json (404) as evidence of missing projects data or an outage; when a future serving check is written, it aims at state.json, not questions.json.",
  "falsifier": "Re-fetch both URLs at a later tip: if /projects/questions.json returns 200 as the projects state, or /projects/state.json returns 404 while projects data is live elsewhere, this observation is superseded and the canonical pair must be re-resolved at that tip.",
  "mechanism": "Serving route table, not data presence: the hub serves the projects state file at /projects/state.json, while /projects/questions.json is not a served route, so it 404s regardless of whether projects data exists. A 404 on an unserved route therefore carries no information about the data; only the served route's status carries that information."
}
```
