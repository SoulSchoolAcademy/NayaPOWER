# INTELLIGENT BLOCK — SN-2068

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02068-skip-on-gates-never-on-flags
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Weekly distillation 2026-11-01 (weekly-distill-20261101-librarian-heir.md, Workstream C, mirror lesson); lessons.jsonl record 39, id `reconcile-gate-skip-vs-flag-advisory-20261101`; surfaced by the daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1010).

## ✦ IN A NUTSHELL

Skip on gates, never on flags — and prove which one you obeyed. A skip trigger is a failed precondition evaluated by the claim gate; a flag trigger is an advisory classifier mark with no precondition failure. The run is the live instance: 31 briefs skipped on exit-7/exit-2 claim-gate bars (real preconditions) while one runtime-flagged intermediate result was set aside as data and skipped no required work. The durable rule: **a gate decides whether work proceeds; a flag only classifies — a skip must name its gate code, and a flagged result decides nothing.**

## 🩷 HUMAN NOTE

Shawn — when a sweep skips work, the reason has to be a real gate: a precondition that actually failed, with its code on the record. A flag is different — it's just a note saying "this looks odd," with no pass or fail behind it. This week a run skipped 31 briefs for genuine gate failures and set one flagged result aside as data, skipping nothing because of it. That's the standard now: every skip names its gate code in the same line as the brief, and a flag never gets to stop work on its own.

## 🟣 CHILD NOTE

Imagine two kinds of stop signs. One is a real gate: the bridge is closed, you cannot cross, and the sign says why. The other is a sticky note someone left saying "this bridge looks funny" — it doesn't close anything, it just marks something to look at later. The new rule: you only turn back for the real gate, and when you do, you write down which gate stopped you. A sticky note never turns you around by itself.

## 🔵 GRANDMA NOTE

Dear, it's like the difference between a locked door and a little yellow note on the fridge. The locked door means you truly can't go in — the key didn't turn, and that's a fact. The yellow note just says "have a look at this when you can" — it locks nothing. From now on, whenever we skip a job we write down which locked door stopped us, right next to the job's name. A yellow note is never, ever the reason a job doesn't get done.

## 🟠 NAYA NOTE

For every seat that runs a sweep or a claim pass: a skip is a gate verdict, never a flag verdict. A skip trigger is a failed precondition evaluated by the claim gate (exit-7/exit-2 bars and their kin) — name the gate code in the same line as the brief. A flag trigger is an advisory classifier mark with no precondition failure — record it as data, set the flagged result aside, and let it skip no required work. If a skip line cites a flag as its reason, the claim review rejects it. If a flagged result ever blocks a required step, it is not a flag — it is a gate in disguise, and the split has collapsed for that flag: reclassify it as a gate or remove the block.

## 🟢 MACHINE NOTE

```json
{
  "slug": "skip-on-gates-never-on-flags",
  "sn": "SN-2068",
  "title": "Skip on Gates, Never on Flags — Prove Which One You Obeyed",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["sweep", "claim-gate"],
  "enforcement": "Every sweep skip line names its claim-gate exit code in the same line as the brief (claim-brief.py / sweep-claims.py verdict); the claim review rejects a skip whose stated reason is a runtime flag, and a flagged result is recorded as data only — it decides no skip.",
  "falsifier": "Proven wrong if a flag trigger is shown to encode a failed precondition — a classifier mark that blocks a required step — in which case the flag is a gate in disguise and the split collapses for that flag.",
  "decision_changed": "How sweeps record skips: each skip names its gate code beside the brief, and a flagged intermediate result is set aside as data instead of silently deciding a skip.",
  "mechanism": "A gate evaluates a precondition — pass/fail decides whether the work proceeds; a flag classifies — an advisory mark with no precondition evaluated. Different machinery, different authority: conflating them lets an advisory mark borrow a gate's power to stop work, or lets a failed precondition hide behind an advisory label.",
  "provenance": "Weekly distillation 2026-11-01 (weekly-distill-20261101-librarian-heir.md, Workstream C, mirror lesson): 31 briefs skipped on exit-7/exit-2 claim-gate bars (real preconditions) while one runtime-flagged intermediate result was set aside as data and skipped no required work. Filed as lessons.jsonl record 39, id reconcile-gate-skip-vs-flag-advisory-20261101. Surfaced by daily learning review 2026-11-05 13:20 PST (learning-events-2026-11-05-13.md, CANDIDATE 1010)."
}
```
