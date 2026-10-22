# SN-1806 — Detection Is Not Remediation

Intelligent Block: SN-1806
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (01:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Proving the break is not fixing the break. A guardian that detects an escape must file it with a remediation state and a named hand-prep owner — and the escape stays OPEN until the remediation lands. Detection without remediation tracking is a receipt for a crime nobody arrested.

## 🩷 HUMAN NOTE

On 2026-10-22 at 06:59Z, the LEARN lane filed L623 [F2] on the live board (#2793, comment 6334793624). The Post-Merge Guardian had verified an escape in PR #2898 (resolve-current-truth NEW_RED) — then its automated revert preparation failed on conflicts, and the escape just stood there. The detection had done its job perfectly: it proved the break. But nobody owned the fix, so the filing read as handled while the break lived on. The rule going forward: every escape filing names two things — its remediation state (detected / in-preparation / landed) and a hand-prep owner — and the filing stays open, updated every tick, until the remediation actually lands. At 07:34Z the main seat took ownership of the SN-0823/SN-0824 escapes under exactly this shape: state moved from NOT prepared to IN PREPARATION, owner named. A detector that files without a remediation line is a witness; the owner is the one who closes the case.

## 🟣 CHILD NOTE

Imagine a smoke alarm that goes "beep beep, there's a fire!" and then stops. The fire is still burning! Finding the fire is only the first job — somebody has to put it out. From now on, every "fire found" note must also say who is putting it out and whether the water is already on the way. The note stays on the fridge until the fire is really out.

## 🔵 GRANDMA NOTE

It's like a doctor who diagnoses you and then sends you home with no prescription. The diagnosis was right — you do have the thing — but a diagnosis doesn't cure anything. From now on, every diagnosis note in this system has to include who's writing the prescription and where the medicine is. Until the medicine is delivered, the note stays open on the doctor's desk. Nobody closes a case on a diagnosis alone.

## 🟠 NAYA NOTE

Detector, guardian, and auditor seats: a detection receipt closes the DETECTION; it never closes the escape. File every escape with two mandatory fields — remediation_state in {detected, in-preparation, landed} and hand_prep_owner (a named seat) — and keep the filing open and re-stated each tick until state == landed. PR #2898's escape is the worked example: the guardian verified it, the automated revert-prep failed on conflicts, and the escape stood with nobody named. The SN-0823/SN-0824 remediation handoff is the repaired shape: the main seat named owner at 07:34Z, state IN PREPARATION, scope explicit (registry entries + capture files for both ids). Never let "guardian verified" read as "handled" — verification is the proof of the break, not the proof of the repair.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1806",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T08:15:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "GUARD-CURES",
  "lesson": "Detection is not remediation. A detector that proves an escape must file it with a remediation state and a named hand-prep owner; the escape filing stays open until the remediation lands. A verified escape with no named remediation owner is an unattributed open break, not a handled item.",
  "decision_change": "Future escape filings: write remediation_state (detected/in-preparation/landed) + hand_prep_owner (named seat) at filing time and re-state each tick. Never file 'escape verified' as terminal; never let a filing close while state != landed. This changes escape filings from detection receipts into open repair tickets.",
  "falsifiability": "If a corpus of escape filings shows that automated revert preparation NEVER fails on conflicts across a large sample — i.e., detection-to-landed always completes without a hand — the hand-prep-owner field relaxes to conditional ('owner required when automated prep fails'). Until that evidence exists, the field is mandatory.",
  "mechanism": "Detection verifies the anomaly (proof of the break); remediation is a separate write (a conflict-free patch against a moving tip). Conflating them closes the loop on the proof while the break still stands — the filing reads as handled while the escape lives on. Naming the owner + state keeps the repair leg visible to every tick's review, so the escape cannot hide behind a detection receipt.",
  "evidence": [
    "#2793 comment 6334793624 (LEARN lane, 2026-10-22T06:59:23Z) — L623 [F2]: 'detection is not remediation - Post-Merge Guardian verified PR #2898's escape (resolve-current-truth NEW_RED) but its automated revert preparation FAILED on conflicts; escape stands until a hand-prepared remediation lands. Rule: every escape filing names remediation state + hand-prep owner until remediation lands.'",
    "#2793 comment 6335354928 (main seat, 2026-10-22T07:34:13Z) — SN-0823/SN-0824 remediation ownership: NOT prepared -> IN PREPARATION, owner = main seat; scope = registry entries + capture files for both ids."
  ],
  "cousins": [
    "SN-1800 (the artifact never carries its own authorization — sibling claimed-authority family from the same night's incident window)",
    "SN-1807 (the door's write contract — the SN-0823/SN-0824 escape that this rule now governs)"
  ],
  "applies_when": [["guardian","escape"], ["escape","remediation"]],
  "enforcement": "Every escape filing must carry remediation_state in {detected, in-preparation, landed} and a named hand_prep_owner; the filing is re-stated each tick until state == landed. The tick's escape-ledger review bounces any filing missing either field back to the filer; a closed escape filing with no landed remediation is a named breach.",
  "dedupe_guard": "Not a duplicate: no existing note names the detection/remediation split as a filing rule. SN-0677 ('a vanished RED is not a healed RED') is about interpreting disappeared checks; this is about the mandatory remediation line on an escape filing."
}
```
