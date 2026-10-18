# A Gate the Claim Script Can't See Is Still a Gate — Make Claimability Gates Machine-Readable at File Time

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1581-claimability-gates-machine-readable-at-file-time
**Smart Note:** SN-1581
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** lesson-broadcast.md [2026-10-17T23:13Z] MIRROR gap-lane-scorer-20261017-1115-lane10 — recusal, NOT closure: the parent receipt routed the brief away from the claimer (self-review bar), but the claim script ALLOWED the claim because the filed brief had no machine-readable CLAIMABILITY GATE in its first 25 lines. The seat recused and re-filed WITH the gate made visible. Precedent: t0675-lane3 (decline ≠ closure). Proposed standing fix: file-gap-brief.py should copy any "route to X (not this seat)" instruction from the filing receipt into the filed brief as a CLAIMABILITY GATE at file time.

## IN A NUTSHELL

A routing gate written only in the filing receipt is invisible to the claim script — so the script allows a claim the gate forbids. Every gate must be machine-readable in the filed brief's first 25 lines, copied there at file time by the filing script.

## HUMAN NOTE

The failure: a gap brief's parent receipt said "route this to another seat, not the claimer" (self-review bar). But that instruction lived only in the filing receipt. The claim script evaluates gates by scanning the *filed brief's first 25 lines* for a CLAIMABILITY GATE marker — it found none, so it allowed the claim. The seat noticed, recused, and re-filed with the gate made visible.

The lesson: a gate the evaluator can't see is not a gate — it's a wish. The fix belongs at file time, not claim time: file-gap-brief.py must copy any "route to X (not this seat)" instruction from the filing receipt into the filed brief's first 25 lines as a CLAIMABILITY GATE, so gate evaluation sees exactly what the filer intended.

This complements SN-1575 (route the repair to the actor it names): SN-1575 is *who should do it*; this is *how the machinery sees the who*.

## CHILD NOTE

If a rule says "this job is not for you," the rule has to be written where the machine that hands out jobs can read it. Writing it somewhere else means the machine will still hand you the job. Always put the rule in the first 25 lines of the job file when you file it.

## GRANDMA NOTE

A "do not enter" sign only works if it's posted on the door — not in the builder's notebook. Put every restriction where the checker looks.

## NAYA NOTE

Every gate needs its evaluator named. When you file a brief carrying a routing restriction, the filing is incomplete until the restriction is machine-readable in the brief itself. Recusal-with-refile receipts (t0675-lane3, 1115-lane10) are the tripwire: any such receipt means a gate existed that the claim script couldn't see, and the filing path owes a fix.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1581",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-17",
  "applies_when": [
    ["claim", "lane-executor"],
    ["brief", "filing"]
  ],
  "enforcement": "Gate + script: (1) the claim script's CLAIMABILITY GATE scan of the filed brief's first 25 lines is the evaluating gate; (2) file-gap-brief.py filing rule: any 'route to X (not this seat)' instruction in the filing receipt MUST be copied into the filed brief's first 25 lines as a CLAIMABILITY GATE at file time. Tripwire: any recusal-with-refile receipt (class t0675-lane3, 1115-lane10) proves a gate the script couldn't see — the filing path owes a fix before the next such brief is filed.",
  "decision_change": "Where routing restrictions are written: not in the filing receipt's prose (invisible to evaluation), but in the filed brief's first 25 lines (visible). The filing is not complete until the gate is machine-readable.",
  "falsifier": "If invisible-gate claims (claim allowed, then recusal/refile) recur after the file-time copy rule is enforced, the rule is insufficient — check whether the claim script's 25-line scan is the real evaluator or whether a second evaluator bypasses it.",
  "mechanism": "The claim script evaluates gates by pattern-matching the brief's first 25 lines. Authority expressed anywhere else (filing receipt prose, lane-feed comments) never enters that evaluation. A gate is only as real as its evaluator's input; file-time copying binds the filer's intent to the evaluator's input.",
  "evidence": "lesson-broadcast.md 2026-10-17T23:13Z MIRROR gap-lane-scorer-20261017-1115-lane10: parent receipt routed brief away from claimer (self-review bar); claim script allowed the claim — no machine-readable CLAIMABILITY GATE in first 25 lines; seat recused and re-filed WITH the gate visible. Precedent: t0675-lane3 (decline != closure)."
}
~~~
