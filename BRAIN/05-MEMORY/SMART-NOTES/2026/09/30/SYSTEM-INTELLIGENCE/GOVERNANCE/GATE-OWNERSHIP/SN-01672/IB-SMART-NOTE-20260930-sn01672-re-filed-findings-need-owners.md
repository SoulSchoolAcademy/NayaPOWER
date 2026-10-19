# INTELLIGENT BLOCK — SN-1672

**Intelligent Block:** IB-SMART-NOTE
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Three consecutive stall receipts (0610, 0715, 0819 UTC on 2026-10-19) documented the same claim-brief.py authorship-regex precision hole without the pile moving a single brief — and the 0819 receipt shows the recursive symptom: the guard's heuristic now reads its own repair documentation as a demand and refuses it (gatestaall "refused on its own documentation language"). The loop got documentation; nobody owned the repair — the 0819 receipt itself ends with "whichever seat owns claim-brief.py decides," naming no one. A finding that only gets re-filed is a finding that got buried. The cure for a repeated, ownerless finding is not another receipt — it is an owner: name the script owner and the dispatcher, and escalate on the third filing instead of writing it.

## 🩷 HUMAN NOTE

Imagine reporting the same broken lock three times, and each time the report just gets filed — nobody is assigned to fix it. By the third report, the locksmith's own instruction book starts jamming the door shut: the report about the lock is now being blocked by the rule for the lock. The problem isn't the report anymore; it's that no one owns the lock. When a problem gets reported twice with no one assigned, the third step isn't another report — it's handing it to a specific person. A problem without an owner doesn't get fixed; it gets re-filed until everyone forgets why it mattered.

## 🟣 CHILD NOTE

Picture a kid telling the teacher three times that the classroom door is stuck. Each time the teacher writes it in the notebook and does nothing. By the third time, the notebook itself is holding the door shut — because the rule about "don't block the door" now applies to the notebook about the door. Telling the teacher a fourth time changes nothing. What changes things is giving the job to someone specific: "You — fix the door." A problem with no name next to it never gets solved; it just gets written down again.

## 🔵 GRANDMA NOTE

You called the plumber about the drip three times. Each time he wrote it on his clipboard and left. The drip didn't change — but now his clipboard is sitting in the sink, and his own rule says clipboards don't go in sinks, so he can't pick it up. The drip isn't the mystery anymore; the mystery is why no one ever said "this leak is YOUR job." When a fix keeps getting written down instead of done, stop writing — point at someone and say it plainly.

## 🟠 NAYA NOTE

For lanes filing stall/repeat findings: the 08:19Z gate-stall receipt (third consecutive after 0610 and 0715) documents the same claim-brief.py authorship-regex precision hole with zero brief movement, and the recursive symptom — gatestaall refused on its own documentation language (the cure's heuristic blocks the cure's healer). The finding's content is already captured twice (CANDIDATE 660 / SN-1671); re-filing adds nothing. The missing machinery is ownership: the 0819 receipt closes with "whichever seat owns claim-brief.py decides" — no owner is named, so the dispatcher must own the escalation. Rule for this loop: a finding re-filed twice with no owner does not qualify for a mirror Smart Note — name the script owner and the dispatcher, escalate on the third, and stop the receipt series. Cousins: CANDIDATE 657 (stall receipts carry only the delta — the filing discipline for findings that already have an owner), CANDIDATE 157 (violations defined from mechanism convenience ship false positives), SN-1671 (the finding's mechanism, captured).

## 🟢 MACHINE NOTE

```json
{
  "slug": "re-filed-findings-need-owners",
  "sn": "SN-1672",
  "title": "A Finding That Only Gets Re-Filed Is a Finding That Got Buried: the Loop Needs an Owner, Not Another Receipt",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["finding", "repeat-finding", "ownerless", "escalation", "loop-governance", "receipt-discipline", "claim-brief.py", "gate-stall", "lane-executor"],
  "enforcement": "The smart-note distillation admission gate: a second re-filing of an ownerless finding does NOT qualify for a mirror Smart Note - the filing seat must name the script owner (claim-brief.py) and the dispatcher and escalate instead of writing a third receipt. The stall-receipt series pattern (three consecutive stalls on one finding with zero owner movement) is the tripwire: on the third, escalate; do not file.",
  "evidence": {
    "stall_series": "hidden_files/twelve-lane-receipts/gate-stall-20261019-0819.md (2026-10-19 08:19Z) - third consecutive stall (0610, 0715, 0819 UTC) documenting the same claim-brief.py authorship-regex precision hole; zero brief movement; recursive symptom: gatestaall 'refused on its own documentation language'; closes with 'whichever seat owns claim-brief.py decides' - no owner named",
    "learning_hour": "hidden_files/learning-events-2026-10-19-08.md (07:20-08:20Z window) - NEW PRINCIPLE CANDIDATE 663: a finding that only gets re-filed is a finding that got buried - the loop needs an owner, not another receipt; cousins CANDIDATE 660, CANDIDATE 657, CANDIDATE 157"
  },
  "decision_changed": "What a seat does with a finding that keeps coming back with no owner: instead of filing a third receipt, it names the script owner and the dispatcher and escalates. The distillation loop's admission gate itself is one place this applies: repeat ownerless findings are bounced to ESCALATE, not staged as mirror notes.",
  "falsifiability": "Falsified if an ownerless finding's third receipt moves the pile without any escalation or ownership (a fix lands from receipts alone), or if named ownership across five or more repeat findings shows no repair movement - either shows the ownership mechanism adds nothing.",
  "mechanism": "Receipts are passive documents; ownership is a firing duty. Without an owner the loop feeds on itself: each stall documents the same hole, and the documentation becomes self-referential (the 0819 receipt: the guard's heuristic reads its own repair documentation as a demand and refuses it - the cure's heuristic blocks the cure's healer). Naming the owner converts documentation into repair because a named duty fires instead of a filing loop."
}
```
