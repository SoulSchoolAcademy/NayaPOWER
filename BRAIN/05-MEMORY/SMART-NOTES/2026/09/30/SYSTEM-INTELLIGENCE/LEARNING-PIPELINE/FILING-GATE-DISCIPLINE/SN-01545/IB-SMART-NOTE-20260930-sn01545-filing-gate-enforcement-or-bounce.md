# The Filing Gate — A Lesson Isn't Learned Until It Names Its Enforcement

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01545-filing-gate-enforcement-or-bounce
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shawn's standing directive 2026-10-17 (Pillar 1, Phase A — "A lesson isn't learned until it names its enforcement"): a Smart Note candidate is INCOMPLETE unless its MACHINE NOTE json carries `applies_when` (mission-class / area / failure-signature tags) AND `enforcement` (the specific check that catches it if ignored — a script, a gate, a watch, a named verification step; "be careful" is not an enforcement). Missing either → BOUNCED, logged, never staged. Working implementation same day: hidden_files/lessons.jsonl (21 records, all carrying applies_when + enforcement); the distillation filing gate bounces notes missing them; the director's 04:10Z quarantine decision DROPPED 3 lessons.jsonl rows whose applies_when was a plain string with no enforcement (shared-state.json `director_decision_lessons_quarantine_2026_10_17`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A lesson file that says "be careful" is a wish with a timestamp. The filing gate makes capture mechanical: every candidate Smart Note must name (1) when it applies — `applies_when` tags by mission-class, area, and failure signature, so the dispatcher can inject it at decision time — and (2) what catches a violation — `enforcement`, a specific script, gate, watch, or named verification step. Missing either one, the note is bounced, not staged: logged as `BOUNCED {slug}: missing {applies_when|enforcement}`, never entering the store. The law was proven live the day it was spoken: three quarantined lesson-store rows violated it, and the director dropped them rather than file them.

## 🩷 HUMAN NOTE

Think of it like a smoke alarm rule for the fire department: every fire report must name the building AND the alarm that would go off if the fire restarted. A report that says "there was a fire somewhere, be careful" can't trigger anything — it sits in a drawer. Shawn's filing gate says: no building, no alarm, no report. Two hooks, always. The `applies_when` tags are the address — they tell the system when to surface the lesson (at decision time, to the right seat, in the right mission). The `enforcement` is the alarm — the exact check that fires if someone ignores it. A lesson without an enforcement isn't learned; it's noted. And noted lessons are where intelligence goes to die.

## 🟣 CHILD NOTE

Imagine you learn that touching a hot stove burns your hand. The lesson isn't "stoves are dangerous" — that's just a worry. The real lesson has two parts: (1) WHEN it matters — every time you walk into the kitchen and a stove is on (that's `applies_when`); (2) WHAT stops you — the rule that you must use the oven mitt, and mom checking that you did (that's `enforcement`). If a lesson can't tell you when it matters and what catches you forgetting it, it's not a lesson yet — it's just a story. Send it back until it can.

## 🔵 GRANDMA NOTE

Dear, this is the difference between a reminder and a system. A reminder says "don't forget" — and then everybody forgets. A system says WHEN the thing matters (which kitchen, which day) and WHAT checks that it was done (who looks, what machine beeps). The filing gate refuses to store a reminder that has no system attached. Every lesson the family keeps must carry its address and its alarm, or it doesn't get into the book. That's how the book stays honest: nothing in it can be ignored silently, because every page knows exactly how it would catch you.

## 🟠 NAYA NOTE

Apply this at every admission point where a lesson, note, or rule enters a persistent store: (1) demand `applies_when` as a list of tags — mission-class / area / failure-signature pairs like ["claim","lane-executor"], ["merge","receipt"], ["budget","governor"] — not prose, so a matcher can inject the lesson at decision time; (2) demand `enforcement` as a checkable hook — a script path, a gate name, a watch ID, a named verification step — with its trigger condition spelled out; "be careful" / "remember to" / "stay vigilant" are not enforcement, they are the bounce condition; (3) on missing either: BOUNCE — log `BOUNCED {slug}: missing {applies_when|enforcement}` in the run report, do not stage, do not "fix it later"; (4) for store invariants: an asserting pass on the store rejects rows violating the gate (the 2026-10-17 asserting pass: applies_when must be a dict with enforcement) — rows already inside get quarantined and either re-filed by their authors through the new pass or dropped; (5) track the bounce rate — a gate that never bounces is decorative. Cousin map: SN-0624 (quarantine snapshots are point-in-time — the filing gate is the admission twin); SN-1544 (a falsification must name its checks — same honesty family: a claim must name its tripwire).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1545,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "a_lesson_isnt_learned_until_it_names_its_enforcement__filing_gate_bounces_candidates_missing_applies_when_or_enforcement",
  "applies_when": [["distillation", "filing"], ["learning", "candidate-admission"], ["memory", "lesson-store"], ["fold", "asserting-pass"]],
  "enforcement": "The distillation loop's filing gate: a candidate whose MACHINE NOTE json lacks applies_when (list of mission-class/area/failure-signature tags) or enforcement (a specific script, gate, watch, or named verification step — 'be careful' is not an enforcement) is BOUNCED, logged as BOUNCED {slug} in the run report, and never staged. The lesson-store's asserting pass rejects rows violating the same rule (applies_when must be a dict with enforcement). Audit: every tick, grep staged/ingested notes for both fields; any admitted note missing either proves the gate decorative.",
  "evidence": {
    "directive": "Shawn's standing directive 2026-10-17 (Pillar 1, Phase A): 'A lesson isn't learned until it names its enforcement' — a candidate is INCOMPLETE without applies_when AND enforcement; missing either → do NOT stage; log BOUNCED {slug}",
    "implementation": "hidden_files/lessons.jsonl: 21 records, all carrying applies_when + enforcement (tag-matching verified at brief injection)",
    "live_proof": "shared-state.json director_decision_lessons_quarantine_2026_10_17 (2026-10-17T04:10:00Z): DROP the 3 quarantined rows that violated the BOUNCE law (applies_when as a plain string, no enforcement); store invariant restored at 278 rows; re-file only through the fold's NEW asserting pass"
  },
  "procedure": [
    "for each candidate, require applies_when as a list of [mission-class, area/failure-signature] tags — machine-matchable, not prose",
    "require enforcement as a checkable hook: script path, gate name, watch id, or named verification step, with the trigger condition spelled out; prose admonitions are the bounce condition",
    "on missing either field: BOUNCE — log BOUNCED {slug}: missing {applies_when|enforcement}, do not stage",
    "for stores: an asserting pass rejects violating rows; existing violators are quarantined, then re-filed by authors through the new pass or dropped",
    "measure the bounce rate; a gate that never bounces is decorative"
  ],
  "falsifier": "The gate is proven decorative if any staged/ingested note lacks applies_when or enforcement — a single missing-field note inside the store kills the claim. The rule is proven too weak if bounced candidates are later shown load-bearing AND unrecoverable by re-filing (then the gate should have repaired, not bounced).",
  "mechanism": "Tags route the lesson to decision time: the dispatcher injects the top-3 matching lessons by mission-class/area/failure-signature, so a lesson that can't be tagged can't be found when it matters. Enforcement is a tripwire: a lesson whose violation nothing catches is a wish, and wishes don't change behavior. The two fields together close the capture-to-behavior loop — routing without a hook is a poster, a hook without routing is an alarm nobody hears."
}
~~~
