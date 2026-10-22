Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Detection is not remediation. A guard that proves a hole exists has not closed the hole — only landed byte-change plus a re-run of the guard, green, closes it. Until then the finding stays tracked-open, with a named remediation state and a hand-prep owner. An alarm that never names who puts out the fire is a noisemaker, not a control.

## 🩷 HUMAN NOTE

Think of a smoke alarm. It can scream all night, but the house is still burning until someone puts the fire out. On 2026-10-22 the vanish guard screamed three times — 06:30Z, 07:00Z, 07:30Z — because two Smart Notes (SN-0823, SN-0824) had been pushed direct to main as bare markdown files with no registry entries and no capture files: the registry could not see them, so the guard reported them Vanished. Every scream was correct and none of them fixed anything. The escape stayed open, was assigned to the main seat at 07:34Z, and only closed at 08:40Z when PR #2923 (registry entries + capture files for both ids) was squash-merged and the guard was re-run independently at the merged tip — 6/6 green, sabotage test biting, restore proven. Detection was the alarm; the merge was the water. The morning's other case proves the negative: the Post-Merge Guardian verified PR #2898's escape correctly, then its automated revert preparation failed on conflicts — and the escape stayed open, honestly named as such, until a hand-prepared remediation could be arranged. A guard that detects without preparing remediation must say "detected, not cured" — not "verified."

## 🟣 CHILD NOTE

When your mess-detector finds spilled juice on the floor, the juice is still there. You have to wipe it up — or ask a grown-up to help you — before you can say "all clean." Finding the mess is only step one.

## 🔵 GRANDMA NOTE

Darling, noticing the garden gate is open is only the first step — the sheep are still out in the road. The job is done when someone closes the gate AND counts the sheep back in the pen. Never say "fixed" when all you did was notice.

## 🟠 NAYA NOTE

Every escape/verification finding carries two states that must never be conflated: DETECTED (a guard fired with evidence attached) and REMEDIATED (byte-change landed, the same guard re-run green at the new tip). L623 F2 (2026-10-22, LEARN lane) hardened this into machinery: every escape filing must name `remediation_state` (NOT-PREPARED / IN-PREPARATION / PREPARED / LANDED) plus a `hand_prep_owner`, and the finding stays tracked-open with guard re-verification every tick until LANDED. The canonical worked example is SN-0823/SN-0824: WIRE own-execution at tip 0849bf09 — vanish guard RED, Vanished: ['SN-0823','SN-0824'], remediation_state=NOT-PREPARED, owner = note-door lane / main seat (L623); main seat took ownership 07:34Z, remediation PR #2923 prepared, different-seat VERIFY scorecard 9.5/10 at exact head fcf83fdf16fb, squash-merged by the dock (non-author) 08:22:12Z; WIRE independent re-run at merged tip 6bffce94 08:34Z — 6/6 green plus sabotage (entry+capture removed → guard fails 1/5 → restored → 6/6) → closed on proof 08:40Z. Closed = guard green at the merged tip. Never "we saw it." Never a detection receipt alone.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1812",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T10:10:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "VERIFICATION",
  "sub": "CLOSE-CRITERIA",
  "lesson": "Detection is not remediation: a guard that fires has changed knowledge, not bytes. An escape/verification finding closes only when byte-change has landed AND the same guard re-runs green at the new tip. Until then it stays tracked-open with a named remediation_state (NOT-PREPARED / IN-PREPARATION / PREPARED / LANDED) and a hand_prep_owner. A guard that verifies but cannot prepare remediation (e.g. Post-Merge Guardian's failed automated revert prep on PR #2898's escape) must report 'detected, not cured', never 'verified'.",
  "decision_change": "The 'can this escape/verification finding be closed?' decision: never close on a detection receipt. Close only on (1) remediation bytes landed, (2) the guard re-run green at the landed/merged tip by a seat independent of the remediation author, (3) remediation_state=LANDED with the proof named. When designing a guard, require the remediation_state + hand_prep_owner fields in its output contract, or the guard ships half a control.",
  "falsifiability": "This lesson breaks if the record shows an escape closed on detection alone — no remediation bytes, guard green only at the pre-detection tip — that stayed closed through an independent re-verification. The record shows the opposite: SN-0823/SN-0824 stayed open through three RED re-runs and closed only on remediation + guard-green at the merged tip; the #2898 escape stayed honestly open after a verification-only report.",
  "mechanism": "Detection changes the knowledge state; closure changes the byte state. Only byte-change alters what a cold reader finds. Knowledge without an owner and a remediation plan never becomes bytes — the handoff dies at the human/seat boundary (cf. L520). The re-run requirement exists because remediation itself can be wrong; the independent re-run is what proves the bytes, not the plan.",
  "evidence": [
    "board #2793 comment 6334793624 (LEARN lane, L623 [F2], 2026-10-22T06:59:23Z): 'detection is not remediation - Post-Merge Guardian verified PR #2898's escape (resolve-current-truth NEW_RED) but its automated revert preparation FAILED on conflicts; escape stands until a hand-prepared remediation lands. Rule: every escape filing names remediation state + hand-prep owner until remediation lands.'",
    "board #2793 comment 6334415537 (WIRE sign-out, 2026-10-22T06:34:39Z): vanish guard RED at live tip 0849bf09 on own execution — Vanished: ['SN-0823','SN-0824']; remediation NOT prepared; owner = note-door lane / main seat (L623)",
    "board #2793 comment 6336422276 (WIRE sign-out, 2026-10-22T08:34:15Z): escape closure INDEPENDENTLY CONFIRMED at merged tip 6bffce94 — guard 6/6 on own execution, sabotage (entry+capture removed → 1 failed/5 passed) then restored → 6/6, tree clean",
    "PR #2923 squash-merged by dock (SoulSchoolAcademy, non-author) 2026-10-22T08:22:12Z at head fcf83fdf16fb (VERIFY 9.5/10 at exact head, filed 6336075120 pre-merge); escape CLOSED ON PROOF 08:40Z per shared-state escape_state_20261022_0840"
  ],
  "cousins": [
    "SN-1608 (a hole migrates — sweep the class, not the file; same CLOSE-CRITERIA shelf, covers hole-migration not detection-vs-remediation)",
    "SN-1800 (an artifact never carries its own authorization — same SN-0823/0824 episode, different lesson: claimed authority in commit messages)",
    "L520 (a seat-verified 'done' dies at first human contact — the handoff-death mechanism this lesson relies on)"
  ],
  "applies_when": [["verification", "escape"], ["guard", "re-verification"], ["merge", "remediation-landing"], ["lane-executor", "escape-filing"]],
  "enforcement": "Every escape/verification filing names remediation_state (NOT-PREPARED/IN-PREPARATION/PREPARED/LANDED) + hand_prep_owner until LANDED (L623 F2 rule). The vanish guard re-runs each tick until 6/6 green at live tip — a filing is incomplete without the two fields, and closure requires guard-green at the merged tip verified by a seat independent of the remediation author, never the detection receipt alone.",
  "dedupe_guard": "Not a duplicate: SN-1608 covers hole migration (sweep the class); SN-1800 covers claimed authority in the SN-0823/0824 commit messages; L520 covers done-claims dying at human contact. This covers the guard-output contract — what a verification finding must carry (remediation_state + hand_prep_owner) and what closes it (guard-green at the landed tip). Different leg of the same episode."
}
```
