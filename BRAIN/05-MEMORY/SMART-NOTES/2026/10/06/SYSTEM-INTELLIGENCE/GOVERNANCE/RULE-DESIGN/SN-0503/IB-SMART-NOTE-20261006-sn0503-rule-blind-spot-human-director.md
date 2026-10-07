# IB-SMART-NOTE-20261006-sn0503-rule-blind-spot-human-director

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0503-rule-blind-spot-human-director |
| Smart Note | SN-0503 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

SN-0213 (the Index-Regen Rule) says any seat landing BRAIN/ content on main must regen the brain index in the same action. On 2026-10-06, main went RED anyway — because the violation didn't come from a seat. Shawn, the human director, made a direct docs commit (8df3565c4, +90 lines to BRAIN/12-ENGINEERING/NEXT-NAYA-EXECUTION-PROMPT-V2.md) without the regen. The rule had a blind spot: it covered seats landing via PR, direct push, and standing loops — but not the director's own hands. CI caught it (tripwire correct), #1668 fixed it (index refresh, main green). The lesson: a rule that doesn't cover every path by which the violation can arrive is a rule with a hole. Don't patch the human's memory — close the path. Either the regen becomes automatic on any BRAIN/ change, or the check moves pre-merge so no path lands un-regen'd.

## HUMAN NOTE

Shawn — here's the why behind today's RED, straight: at 17:03 you made a direct commit re-anchoring the Next-Naya execution prompt — 90 lines into a BRAIN/ file, no index regen. That's not a mistake, it's a blind spot in SN-0213. The rule says "any seat landing BRAIN/ content" — but you're not a seat, you're the director, and your direct commits don't run the seat landing checklist. CI caught it (the tripwire did its job), #1668 fixed it six minutes later, main's green. But the pattern is what matters: every rule needs to cover every path, including yours. The fix isn't "remember to regen" — it's making the regen inescapable. Either it happens automatically whenever BRAIN/ changes, or the check runs before merge instead of after. No human memory required, including yours.

## CHILD NOTE

The class rule says "everyone must wash their hands before lunch." But the teacher comes in from the playground and sits down to eat without washing. Nobody did anything wrong — the rule just didn't say "including the teacher." Good rules cover everybody, even the person who wrote them. Better yet: put the soap dispenser right at the cafeteria door so nobody can walk past it.

## GRANDMA NOTE

The farm had a rule: "close the gate behind you." Every hand knew it. But the farmer himself drove through one morning thinking about the weather and left it open — the cows got out. He wasn't careless; the rule lived in everyone else's checklist but not in his routine. The fix wasn't scolding the farmer — it was hanging a bell on the gate that rings until it's closed. Make the right thing automatic and nobody has to remember, not even the boss.

## NAYA NOTE

Note to future me: when a rule fails, don't ask "who forgot" — ask "which path did the rule not cover." (1) SN-0213's enumeration (PR merge, direct push, standing-loop consolidation) described seat behaviors, not landing paths — the human director's direct commit is a fourth path the rule never named. (2) Enumerate PATHS, not actors: "any BRAIN/ content landing on main, by any hand, human or agent" — actor-based rules always miss someone. (3) Prefer mechanism over memory: the durable fix is automatic regen on BRAIN/ change or a pre-merge gate, not a longer checklist. A rule that relies on anyone remembering — director included — will fail exactly when they're thinking about something else. (4) The tripwire firing correctly (CI RED on drift) is the system working — the gap was prevention, not detection. Close the path, keep the tripwire. Family: SN-0213 (the rule with the hole), SN-0240 (tripwire correct), SN-0390 (harden the whole family, not the one path), SN-0493 (re-verify at action time).

## MACHINE NOTE

```json
{
  "rule": "rules_must_cover_every_path",
  "violation": "SN-0213 covered seat landing paths; human-director direct commit 8df3565c4 (+90 lines BRAIN/12-ENGINEERING/NEXT-NAYA-EXECUTION-PROMPT-V2.md, no index regen) was an uncovered fourth path",
  "detection": "CI 'Verify generated Brain index has no drift' fired correctly (tripwire per SN-0240); main RED at 8df3565c4",
  "repair": "PR #1668 (merge 3f1e6d787) refreshed BRAIN-INDEX.json, REAL-TREE.json, REAL-TREE.md; main GREEN, all 15 checks success",
  "prescription": "enumerate landing PATHS not actors ('any BRAIN/ content by any hand'); prefer automatic regen or pre-merge gate over checklist memory",
  "family": ["SN-0213", "SN-0240", "SN-0390", "SN-0493"],
  "evidence_class": "rule_failure",
  "falsifier": "a BRAIN/ landing by an uncovered path that the index check passes without regen"
}
```

## EVIDENCE

- Commit 8df3565c4 (Shawn Vibert, 2026-10-06 17:03 PDT): "docs(continuity): re-anchor Next-Naya execution prompt to current main" — direct commit, single parent, +90 lines to BRAIN/12-ENGINEERING/NEXT-NAYA-EXECUTION-PROMPT-V2.md, no index regen
- CI RED: "Verify generated Brain index has no drift" failed on 8df3565c4
- Repair: PR #1668, merge commit 3f1e6d787 (2026-10-06 17:09 PDT): "fix(brain): refresh generated projections after main docs change" — BRAIN-INDEX.json, REAL-TREE.json, REAL-TREE.md refreshed
- Post-repair: all 15 check runs SUCCESS on 3f1e6d787 (test, promote-and-prove, guard, spec-integrity, chain-readiness-gate all green)
- SN-0213 text: "any seat landing BRAIN/ content on main (PR merge, direct push, standing-loop consolidation) regenerates the brain index artifacts..."
