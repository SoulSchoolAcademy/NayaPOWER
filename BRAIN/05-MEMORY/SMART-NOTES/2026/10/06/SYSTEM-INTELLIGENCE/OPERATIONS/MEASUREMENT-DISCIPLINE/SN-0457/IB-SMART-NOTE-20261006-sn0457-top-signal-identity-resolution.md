# An Instrument That Can't Resolve Its Top Signal's Identity Is Theater

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0457-top-signal-identity-resolution
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Wiring the Human Value instrument (Team 2 track, Learning 10/10, 2026-10-06). The instrument's highest-weight event is w10 "Shawn merged it himself" — but both Shawn's clicks and lane API merges run under the shared SoulSchoolAcademy GitHub account, so `merged_by` is byte-identical and the API cannot distinguish them. Design decision recorded in `~/workspace/goals/learning-10-10/hidden_files/human-value/README.md` ("Known instrument limitation").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When designing any measurement, check identity resolution for your highest-weight signal first. The Human Value instrument weights "Shawn merged it himself" at 10 — its top signal — but the GitHub API cannot tell Shawn's merge clicks apart from lane merges because both authenticate as the same shared account. An instrument that silently scores its top event from an unresolvable signal is theater, not measurement. The honest repair: the instrument openly declares the limitation and requires independent second-source evidence (board confirmation, transcript, lead verification) for every weight-10 event — never the API alone.

## HUMAN NOTE

Shawn's highest trust signal is him personally staking his tip on a merge — that's worth more than any lane receipt. But our tooling can't see the difference between his click and our API call; we share one GitHub account. So instead of pretending the data says something it doesn't, the instrument demands a second witness for every top-weight event. The principle: never let your most important metric rest on data that can't actually identify what it claims to measure.

## CHILD NOTE

Imagine a scoreboard that gives 10 points when the coach scores a goal — but the camera can't tell the coach apart from the players. If you just trust the camera, the score is made up. The fix: only count the coach's goals when a second person saw it happen. Always check: can my measuring tool actually see the thing I'm giving the most points for?

## GRANDMA NOTE

We built a scoreboard for how much good the team does. The biggest points go to times Shawn himself approves something. But our records can't tell his approval apart from ours — we all sign the same name. So we made a rule: the biggest points only count when someone else confirms they saw it. Don't award the biggest prize on blurry evidence.

## NAYA NOTE

Future Naya: whenever you build or inherit a measurement instrument, audit identity resolution before trusting any score it produces. Ask: for the highest-weighted event type, can the data source distinguish the actor it claims? Shared accounts, shared tokens, and proxy identities all break naive attribution. If the answer is no, either find a second source or downgrade the weight — never silently score it. This note exists because the HV instrument's w10 event had exactly this flaw and we chose to declare it rather than hide it. Apply the same check to value-calculus inputs, authorship claims, and any "verified by" signal.

## MACHINE NOTE

```json
{
  "sn": "SN-0457",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Check identity resolution for the highest-weighted signal before trusting any instrument; shared-account environments break naive API attribution.",
  "instance": {
    "instrument": "human-value HV/moment",
    "top_signal": "w10: Shawn merged a lane PR himself",
    "flaw": "merged_by identical for Shawn UI clicks and lane API merges (shared SoulSchoolAcademy account)",
    "repair": "w10 events require independent second-source evidence (board/transcript/lead verification); documented in human-value/README.md"
  },
  "evidence": ["~/workspace/goals/learning-10-10/hidden_files/human-value/README.md", "value-events.jsonl w10 entries with evidence fields"]
}
```
