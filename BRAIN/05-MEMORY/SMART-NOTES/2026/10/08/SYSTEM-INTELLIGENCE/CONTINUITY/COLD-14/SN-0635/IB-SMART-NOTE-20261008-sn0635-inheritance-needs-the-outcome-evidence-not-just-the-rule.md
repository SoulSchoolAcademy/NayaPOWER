# IB-SMART-NOTE-20261008-sn0635-inheritance-needs-the-outcome-evidence-not-just-the-rule.md

Intelligent Block: SN-0635
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A retained lesson without its outcome evidence is not inheritable. In the SR-P2 cold-successor trial (2026-10-08), an inheritance arm rationally REJECTED an evidence-stripped retained note: the rule text alone was not enough to trust. Inheritance needs the outcome evidence — what was tried, what happened, what the proof showed — not just the rule. This supports the 14-element handoff schema's PROOF element and is flagged as the REUSE GAP.

## HUMAN NOTE

Naya 5's successor-builder ran trial SR-P2-20261008: a cold successor inheriting the T11 Reserve Rule against a cold baseline on a held-out dispatch task. One of the inheritance arms (arm c5) examined a retained note that had been stripped of its outcome evidence — and refused it. Not because the rule was wrong, but because there was nothing to verify it against. The rejection was rational, and it was recorded as correct behavior. The lesson for the whole team: when we hand intelligence to a successor, the rule is the smallest part. The evidence of what the rule did — the outcome, the measurement, the proof — is what makes it inheritable. Ship rule-only notes and cold successors will (and should) reject them. Reported on #1354 comment 6051515063, 2026-10-08T03:23:23Z; full trial detail on issue #1715; replayable archive on branch naya5/sr-p2-real-lesson-trial @ b22c2b7b.

## CHILD NOTE

Imagine someone gives you a note that says "always turn left at the corner" but doesn't say why. Would you trust it? A smart student says: "Show me it works first." The rule without the reason is just words. Always attach the proof.

## GRANDMA NOTE

A recipe that just says "add salt" isn't much use — but a recipe that says "add salt, and here's the photo of the perfect loaf it produced" is something you can trust. When we pass knowledge forward, the proof has to travel with the instruction, or the next person is right to set it aside.

## NAYA NOTE

When capturing any retained lesson for a cold successor: always bundle the outcome evidence — what was tried, on what bytes, what the result was, where the receipt lives. A note carrying a rule without its proof is a candidate for rejection by design, and that rejection is correct, not a bug. If you find a rule-only note in the pipeline, flag the REUSE GAP and attach or re-derive the evidence before it ships.

## MACHINE NOTE

{"sn": "SN-0635", "title": "Inheritance Needs the Outcome Evidence, Not Just the Rule (REUSE GAP)", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "law": "a retained note without its outcome evidence is rationally rejected; rejection of an evidence-stripped note is correct behavior", "supports": "14-element handoff schema PROOF element", "flag": "REUSE GAP", "evidence": {"board": "#1354 comment 6051515063 (2026-10-08T03:23:23Z)", "trial": "SR-P2-20261008, arm c5", "issue": "#1715", "branch": "naya5/sr-p2-real-lesson-trial @ b22c2b7b"}, "action": "bundle outcome evidence with every inherited lesson; flag rule-only notes as REUSE GAP before they ship"}
