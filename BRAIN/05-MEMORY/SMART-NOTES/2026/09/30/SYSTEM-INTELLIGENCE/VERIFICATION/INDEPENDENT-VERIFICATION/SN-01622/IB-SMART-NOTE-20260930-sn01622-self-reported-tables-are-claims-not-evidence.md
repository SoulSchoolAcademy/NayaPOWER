# Self-Reported Tables Are Claims, Not Evidence — Re-Derive Claimability Live at Action Time

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1622-self-reported-tables-are-claims-not-evidence
**Smart Note:** SN-1622
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher t0834 (2026-10-18T10:26Z): "MIRROR gate-stall-20261018-1014 (child of gate-stall-1000): 21 per-brief claimability evaluations re-run on LIVE bytes, not self-reported — parent's self-reported blocker table was premise, not proof. Claimability tables must be re-derived live at action time; a parent's own evaluation is input, never evidence."

## IN A NUTSHELL

When the gate-stall investigation re-ran the 21 per-brief claimability evaluations on live bytes instead of accepting the parent seat's self-reported blocker table, the table turned out to be premise, not proof. A seat's evaluation of its own situation is a claim about the work — useful input, never evidence for the verdict. The rule: claimability tables must be re-derived live at action time. Copying a parent's evaluation into your own decision treats the author's word as the bytes' state; re-deriving treats the bytes as the state. When the two disagree, the bytes win — the same evidence hierarchy that governs specs, pins, and counts, applied to evaluator-authored artifacts.

## HUMAN NOTE

A manager reports "my team is blocked on 21 items." You could plan around the 21 — or you could check each one yourself and discover the real picture is different. The manager wasn't lying; they were reporting their view, and views embed assumptions and staleness. The discipline we locked in: when a team reports its own status, treat the report as the *starting question*, never the answer. The answer comes from checking the actual items. We re-checked all 21 on the real data, and the parent's table was a hypothesis — a useful one, but a hypothesis. "They said so" is not verification.

## CHILD NOTE

Your brother tells you "the fridge is empty, there's nothing to eat." You could just believe him and stay hungry — or you could open the fridge and look. Maybe he's right! But maybe he's wrong, or maybe he looked yesterday, or maybe he only checked the top shelf. Opening the fridge takes ten seconds and ends the argument. The rule: when someone reports what's true, that's a great hint about where to look — but the looking is what makes it true. Believe the fridge, not the brother.

## GRANDMA NOTE

It's the difference between asking the fox how many hens are in the henhouse and counting the hens yourself. The fox may be perfectly honest — but he counts from memory, and his memory has yesterday's numbers and today's interests mixed together. Nobody's blaming the fox; you just count the hens. Teach the house this: a report from the interested party is where the counting *starts*, never where it ends.

## NAYA NOTE

**The evidence hierarchy extends to evaluator-authored artifacts.** A spec sentence is a claim about code; a pin is a claim about bytes at a timestamp; a self-reported evaluation is a claim about work-state by the seat whose work it is. All three are input; the verdict comes from live bytes at action time. The t0834 run is the canonical instance: 21 evaluations re-derived live, not inherited — and the inheritance would have laundered the parent's premises into the child's verdict. This is sharper than "re-verify everything" — it names the exact failure: the consumer of a report is the party at risk, because the report's author already decided what it means. Distinguish from SN-01617 (corroboration is not independence — that note decides *who may* evaluate; this note decides *what an evaluation is worth when it arrives*). Cousin family: SN-01188 (spec-true is not code-true — the hierarchy, spec flavor); SN-0950 (merge-commit SHA is a hypothetical preview — the hierarchy, CI flavor); SN-1442 (every dialect of no — the claimability gate this re-derivation feeds). Status: standing pattern; stamp-claimability-gate.py --gate-check is the mechanized form — the gate window runs the evaluations, not the parent.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1622",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verification", "claimability"],
    ["gate", "self-report"],
    ["evaluation", "parent-report"]
  ],
  "enforcement": "stamp-claimability-gate.py --gate-check runs the per-brief claimability evaluations against LIVE bytes at action time — the t0834 pattern (2026-10-18T10:26Z: 21 evaluations re-run on live bytes, not self-reported). Any claimability verdict consumed from a parent's blocker table without a live re-derivation is premise-labeled-as-proof and is rejected at the gate window: the evaluator's table is logged as input, the verdict is logged only from the re-derivation, and the two are never allowed to share a cell. The mirror log records each re-derivation's byte-anchored source so a cold successor can re-run it.",
  "decision_change": "Future claimability decisions change from 'the parent says brief X is blocked, so it is' to 'the parent says brief X is blocked — re-derive from live bytes, then decide.' Future gate-window decisions gain a standing filter: 'was this verdict re-derived at action time, or inherited from a reporter's table?' — inherited verdicts are inadmissible as evidence.",
  "falsifier": "A parent's self-reported table that matches the live re-derivation exactly on all 21 items doesn't falsify the rule — it falsifies its necessity for that case (the re-derivation was cheap insurance). The rule is falsified only by a case where the re-derivation is impossible (no live bytes accessible) AND the inherited verdict proves correct by later independent check — then the note is revised to name the access boundary as the exception.",
  "mechanism": "Self-reports embed three things the consumer can't see: staleness (the evaluation was true at some earlier instant), framing (the author already decided what counts as a blocker), and interest (the author's situation colors the reading). Inheriting the table launders all three into the consumer's verdict with no trace. Re-deriving at action time severs the laundering: the consumer's verdict rests on bytes the author didn't choose, sampled now, under the consumer's own criteria. The check is cheap; the inherited error is silent.",
  "evidence": "hidden_files/lesson-broadcast.md, t0834 (2026-10-18T10:26Z): 'MIRROR gate-stall-20261018-1014 (child of gate-stall-1000): 21 per-brief claimability evaluations re-run on LIVE bytes, not self-reported — parent's self-reported blocker table was premise, not proof. Claimability tables must be re-derived live at action time; a parent's own evaluation is input, never evidence.'",
  "cousins": ["SN-01188 (spec-true-is-not-code-true — the evidence hierarchy, spec flavor)", "SN-01617 (corroboration-is-not-independence — decides who may evaluate; this note decides what an evaluation is worth when it arrives)", "SN-1442 (every-dialect-of-no — the claimability gate this re-derivation feeds)", "SN-0950 (merge-commit-sha-is-a-hypothetical-preview — the hierarchy, CI flavor)"]
}
~~~
