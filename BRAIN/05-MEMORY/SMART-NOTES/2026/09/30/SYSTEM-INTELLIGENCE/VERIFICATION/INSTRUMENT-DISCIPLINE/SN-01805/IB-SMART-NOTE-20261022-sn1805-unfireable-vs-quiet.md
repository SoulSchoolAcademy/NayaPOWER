# SN-1805 — A Gate That Never Landed Cannot Fail Quietly

Intelligent Block: SN-1805
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (00:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

"The gate never fired" is not a verdict about the corpus until you prove the instrument's code existed at the evaluated pin. PR #2509's smart-note-completeness-gate workflow lives only on the closed PR branch head 59832ba — it is absent from main — so the gate is structurally unfireable, not merely untriggered. Unfired is not quiet until you prove the instrument could have fired at all.

## 🩷 HUMAN NOTE

On the 2026-10-22T05:26Z night-dispatcher tick (t1238), a Lane 4 receipt scored 9.0/10 with a finding the dispatcher named explicitly: "when a gate 'never fired,' check whether it ever LANDED before assuming the corpus was quiet." The smart-note-completeness-gate's workflow (PR #2509) lives only on the closed PR branch head 59832ba — it never landed on main. So every "the gate never fired on main" verdict was measuring the code's absence, not the corpus's calm: the gate is structurally unfireable at that pin, not untriggered by a quiet corpus. The dispatcher dispatched a live-fire exercise (brief-t1238-lane3.md: branch from 59832ba, touch a SMART-NOTES file, open the PR, record the check-run verdict, close unmerged) precisely because the only way to learn whether the gate fires is to put its code where it can fire. Absence of a check-run at a pin without the code proves nothing; the verdict splits into two: QUIET (code present at pin, no trigger) or UNFIREABLE (code absent at pin).

## 🟣 CHILD NOTE

Imagine a fire alarm that's never in the building — and the building manager says "no fires this year, the alarm works great!" The alarm didn't work. It wasn't there. Before you say "the alarm never went off," you have to check the alarm was actually installed. A gate that never landed on main can't tell you main is calm.

## 🔵 GRANDMA NOTE

It's like a security camera that was never mounted. "The footage shows nothing suspicious" — well, there's no footage, because there's no camera. The dispatcher learned this the expensive way: a gate lived only on a closed side branch, and "it never fired" sounded like good news when it was really no news. Now the rule is: check the camera is on the wall before you read the tape.

## 🟠 NAYA NOTE

Verification and gate seats: any "gate never fired" verdict must first pass the code-presence check — pin the instrument's code (blob SHA, read-only, at the evaluated tip), confirm it exists in the evaluated tree, and THEN read the corpus. If the code is absent at the pin, the verdict is UNFIREABLE (structural), never QUIET. The live-fire exercise is the positive proof: branch from the pin that HAS the code, run the instrument, record the check-run verdict — that is how you learn whether a gate fires. Write the verdict as one of the two, with the code pin cited, or don't write it.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1805",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T07:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "VERIFICATION",
  "sub": "INSTRUMENT-DISCIPLINE",
  "lesson": "A 'gate never fired' verdict is valid only after the code-presence check: the instrument's code must exist at the evaluated pin. PR #2509's smart-note-completeness-gate workflow lives only on the closed PR branch head 59832ba and is absent from main — structurally unfireable at the main pin, not untriggered by a quiet corpus. Verdicts fork: QUIET (code present, no trigger) vs UNFIREABLE (code absent at pin).",
  "decision_change": "Future gate verdicts: before writing 'never fired,' run the code-presence check at the evaluated pin (blob SHA pinned, read-only) and cite the code pin in the verdict. If the code is absent at the pin, the verdict is UNFIREABLE — the next action becomes a live-fire exercise at a pin that has the code (branch from the code pin, exercise the instrument, record the verdict), not a claim about the corpus.",
  "falsifiability": "If the code-presence check shows the instrument IS present at the evaluated pin and the corpus shows no trigger, the verdict flips to QUIET — the rule is a fork, not a presumption of absence. The rule breaks only if code-presence at the pin fails to distinguish firing-capable from non-firing states (e.g., code present but structurally disabled by configuration) — that would add a third verdict: DISARMED.",
  "mechanism": "A gate can only fire if its code is present in the evaluated tree. A behavioral claim ('never fired') measured at a pin where the code is absent measures absence, not behavior — the corpus is unobserved by that instrument, so 'no trigger' is the output of a missing sensor, not a calm corpus. Presence-at-pin is the precondition of any firing claim; the live-fire exercise supplies the positive proof the corpus verdict cannot.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1238, 2026-10-22T05:26:42Z]: MIRROR receipt gap-lane-scorer-20261021-1920-lane4.md (Lane 4 Mason 9.0/10): 'when a gate never fired, check whether it ever LANDED before assuming the corpus was quiet — PR #2509's workflow lives only on the closed PR branch head 59832ba, absent from main, so the gate is structurally unfireable, not merely untriggered.'",
    "Exact next action dispatched as brief-t1238-lane3.md: branch FROM 59832ba, touch one SMART-NOTES file, open the PR, record the check-run URL/ID + verdict, close unmerged"
  ],
  "cousins": [
    "t1132 trigger-list lesson (derive the coverage predicate from the instrument's CODE bytes, blob SHA pinned — the presence-check sibling)",
    "SN-1802 (silent-arrival audit cadence — the gate's non-firing was discovered by a different audit)"
  ],
  "applies_when": [["verification", "gate-verdict"], ["gate", "never-fired"], ["instrument", "code-presence"]],
  "enforcement": "Gate verdicts must carry the instrument code's pin/SHA as a named field (blob SHA, read-only check at the evaluated tip); a 'never fired' verdict without the presence check is rejected at review. The UNFIREABLE/QUIET fork is the verdict format — a verdict naming neither is incomplete.",
  "dedupe_guard": "Not a duplicate: t1132 governs deriving predicates from instrument code bytes; no existing note names the QUIET-vs-UNFIREABLE fork or the PR #2509 landing evidence (grep: zero 'unfireable' hits in learn/lessons.md)."
}
```
