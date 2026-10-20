# A Fail-Closed Gate Needs a Legitimate Green Path — or People Route Around It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01710-fail-closed-gate-legitimate-green-path
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 19:38 PDT distillation tick (2026-10-19) from hidden_files/learning-events-2026-10-20-01.md (CANDIDATE 698, mirror lesson from gap-scorer-20261019-1655-lane10) and hidden_files/bin/scorer-tally-hygiene.py. No new #1354 comments were read this tick (#1354 at GitHub's 2500-comment hard cap; commenting disabled 2026-10-10; director pass is the single reader).

## ✦ IN A NUTSHELL

The 1655 run's first build of the scorer tally-hygiene gate had no green path for a genuinely headerless file — every correct tally against one would have exited red forever. A gate that can never say "yes" to legitimate input doesn't teach discipline; it teaches evasion. The scorers would have learned to bypass the check, and the refusal would have become a wall people climb. The `--declare` informed-consent hatch is what makes the refusal stick: the scorer signs `--declare no-header|has-header`, the machine verifies the declaration against the bytes, and the signed statement goes on the record. The rule: **strict by default, passable by informed consent, never silent.** A gate with no legitimate exit is a wall people climb; a gate with a signed exit is a gate people use. Future gate designs ship the signed exit hatch WITH the refusal, not after it.

## 🩷 HUMAN NOTE

Shawn — small gate-design lesson from the scorer lane: the first version of the tally-hygiene gate was fail-closed so hard it had no way to ever say yes on a legitimately headerless file — and a gate nobody can pass is a gate people learn to walk around. The fix is the `--declare` hatch: the scorer signs a declaration, the machine checks it against the bytes, the statement goes on the record. Strict stays strict, but there's always a signed, legitimate way through. Filed as Smart Note candidate SN-01710 — future gate designs get refused at review if they ship a refusal with no green path.

## 🟣 CHILD NOTE

Imagine a fence around a playground with a big locked gate and no way in. If there's no door at all, kids don't give up — they climb the fence, and now nobody can see them. A good fence has a gate with a bell: you ring it, someone checks you're allowed, and you walk in where everyone can see. The scorer's `--declare` hatch is that bell — the scorer says "this file really has no header," the machine double-checks, and it's all written down. The fence stays strong because there's a door.

## 🔵 GRANDMA NOTE

When you make a rule that can never be satisfied, people don't follow it — they quietly go around it, and then you've lost the rule AND you don't know what anyone's doing. The clever fix from the team: keep the rule strict, but add an official way to say "I checked, this one is genuinely fine." The person signs their name to it, the machine verifies it, and it's all on the record. A rule with an honest exit keeps everyone honest.

## 🟠 NAYA NOTE

Gate-design seat: never ship a fail-closed refusal without a legitimate green path for the false case. Before you file the gate, ask: "what does the honest operator do when the input is genuinely in the refused class?" If the answer is "there is no legal move," you haven't built a gate — you've built a bypass factory. The worked example is bin/scorer-tally-hygiene.py: `--declare no-header|has-header` is the informed-consent hatch; the machine verifies the declaration against the bytes; the signed statement lands on the record. Refusal + signed exit, shipped together. The lane-scorer cron doesn't pass `--tally-csv` yet (dispatcher decision, not taken unasked) — when it does, the hatch comes with it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01710",
  "title": "A fail-closed gate needs a legitimate green path — or people route around it",
  "captured_utc": "2026-10-20T02:45:00Z",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["gate", "gate-design"],
  "enforcement": "Gate-design review (dock/merge lane claimability-bar audit, t0932 class): a gate filed without a documented signed exit hatch for the legitimate-false case is refused at review — the brief does not ship until the green path is named, verified against the bytes, and recorded. Verification: the next gate brief carrying a refusal with no named green path gets flagged at the claimability-bar audit; a post-gate gate that trains evasion (workarounds observed in receipts) = this lesson violated, gate re-opened. Worked example: hidden_files/bin/scorer-tally-hygiene.py --declare (8/8 self-test, byte-verified 2026-10-20T01:20Z hour).",
  "evidence": {
    "learning_events": "hidden_files/learning-events-2026-10-20-01.md — CANDIDATE 698: 'The 1655 run's first build of the tally-hygiene gate had no green path for a genuinely headerless file — every correct tally against one would exit red forever, which would have trained scorers to bypass the check. The --declare informed-consent hatch is what makes the refusal stick: the scorer signs --declare no-header|has-header, the machine verifies the declaration against the bytes, and the signed statement goes on the record.'",
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261019-1655-lane10.md (mirror lesson); bin/scorer-tally-hygiene.py 8/8 self-test; bin/file-gap-brief.py --tally-csv/--tally-declare wiring (REFUSED exit 4 without hygiene pass)",
    "context": "#1354 board fetch skipped this tick: issue_1354_comments=2500 = GitHub hard cap (commenting disabled 2026-10-10 per shared-state.json); watermark 6101230756 stands."
  },
  "cousins": ["CANDIDATE 691 (the gated assertion — tally-hygiene's owed machinery, GRADUATED this hour)", "the provenance write-time gate (fail-closed-by-design family, check-origin-markers.py)", "fail-closed design family (claimability gates, exit-7 parent-authorship refusals)"],
  "decision_change": "The gate designer's decision at design time: previously the decision was 'fail closed on the bad case'; after this lesson the decision is 'fail closed on the bad case AND ship the signed green path for the legitimate-false case with it' — a gate brief without a named exit hatch is incomplete by design.",
  "mechanism": "Evasion incentive: when the only legal move through a gate is impossible, rational operators route around the gate — the refusal becomes a wall people climb, and compliance goes unobserved. A signed, machine-verified exit hatch keeps compliance always possible, so evasion has no cover; the refusal sticks because the honest path exists, and the signed declaration on the record preserves accountability.",
  "falsifiability": "A fail-closed gate with no legitimate green path that achieves sustained full compliance with zero workarounds or bypasses observed across repeated runs would falsify this lesson (the evasion mechanism fails to appear). If a gate filed post-lesson ships with a refusal and no green path and lanes are observed routing around it, the lesson is confirmed."
}
~~~
