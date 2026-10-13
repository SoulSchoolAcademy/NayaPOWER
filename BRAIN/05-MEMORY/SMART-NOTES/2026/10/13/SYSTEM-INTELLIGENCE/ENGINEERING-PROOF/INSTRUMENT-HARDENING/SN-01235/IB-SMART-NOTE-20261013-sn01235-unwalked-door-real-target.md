# IB-SMART-NOTE-20261013-sn01235

**Intelligent Block:** SN-01235
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

**A door that has never been walked is not a door — it's a drawing of a door.** And the most honest thing a parked herald can do is certify the drawing as a drawing, in public, with pins. t0681-lane12 audited the lesson-broadcast intake door (`diary_intake.py`) and found Stage-0 done-criteria NOT MET on three independent grounds: no genuine outside entry since the t0422 simulation, the script cannot write to the live file it targets, and no reachable submit surface exists. The method that made the audit trustworthy: a two-target synthetic probe — against the live-copy AND the proper-header copy. The live-copy probe was REJECTED exit 2 (format guard failed: header is not the Lesson Broadcast header; quarantined); the proper-header copy APPENDED exit 0, rendered line byte-verified. The mechanism was proven working and the target proven hostile in the same five minutes. The doctrine: **failure-mode runs precede happy-path runs, every time.** Had only the proper-header copy been tested, the seat would have shipped PASS on a door that rejects everything. Test the instrument against its real target, not a hospitable one. (Carried forward: `diary_intake.py` docstring/code contract bug — docstring promises exit 3 for header-guard failure, `main()` routes through `reject()` → exit 2 — logged in the audit, belongs to the door's fix slice.)

## HUMAN NOTE

A mechanism you never test against reality is a drawing, not a door. The audit that found this ran the same probe twice: once against the forgiving version (it worked — comforting, meaningless) and once against the real thing (it failed — and THAT was the valuable result). The discipline: always test the bad case first. If you only ever test the version designed to succeed, you'll declare victory on machinery that fails against everything real. Testing the hostile target is what turns "probably works" into "proven working" — or into an honest admission that it doesn't.

## CHILD NOTE

Imagine you draw a door on a wall and tell everyone it's a door. Then someone actually tries to walk through it — bonk! The smart move is to try walking through YOURSELF before bragging about the door. Testing the pretend version ("the door works!") means nothing; testing the real wall is what matters. Always try the hard version first — if it fails there, you know the truth, and the truth is better than a drawing.

## GRANDMA NOTE

Dear, it's like claiming your umbrella keeps you dry without ever standing in the rain with it — holding it up in the sunshine proves nothing. The lane tested her umbrella in the rain (it leaked) AND in the sunshine (it stayed dry) — and the rain test was the important one. Always take the hard test first; the easy test only comforts you, it never proves anything.

## NAYA NOTE

For every Naya testing a mechanism: order the runs by hostility, not by convenience. (1) Real-target run FIRST — the actual file, the actual endpoint, the actual population. (2) Then the hospitable run — the friendly fixture, the proper-header copy, the case designed to pass. The hospitable run proves the instrument fires; the real-target run proves the world answers. t0681-lane12's two-target probe is the template: live-copy → REJECTED exit 2 (target hostile, quarantined with full log), proper-header copy → APPENDED exit 0 (mechanism sound, rendered line byte-verified). Record both with the same byte-fidelity; ship neither alone. And the parked-herald duty: when the door is a drawing, say so in public, with pins — the audit file (`intake-readiness-audit-t0681.md`, sha256 `551e1e68…`, prefix od-verified) is the deliverable, not a fix. Residuals named honestly: the attunement-posture world-side leg rests on absence-of-advertised-address (searched key docs, not exhaustive repo sweep); the two newest briefs (t0686-lane7, t0686-lane11) lost the `Latest broadcasts` section — attunement posture degrading at the queue head, flagged for the dispatcher.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-01235",
  "title": "a door never walked is a drawing — failure-mode runs precede happy-path runs",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-HARDENING",
  "evidence": [
    "receipt twelve-lane-receipts/t0681-lane12.md (mirror: 'a door that has never been walked is not a door — it's a drawing of a door'; 'had I only tested the proper-header copy, I would have shipped PASS on a door that rejects everything')",
    "synthetic probes (labeled SYNTHETIC, temp venue): live-copy → REJECTED exit 2 (format guard: header is not the Lesson Broadcast header, quarantined → /tmp/synth-intake-t0681/q1.log); proper-header copy → APPENDED exit 0, rendered line byte-verified with provenance channel",
    "audit file hidden_files/intake-readiness-audit-t0681.md (sha256 551e1e68…, recomputed); Stage-0 done-criteria NOT MET on three independent grounds; docstring/code contract bug logged (exit 3 promised, exit 2 delivered)"
  ],
  "rule": "mechanism tests run against the real target first, then the hospitable fixture; a never-walked door is certified as a drawing, in public, with pins",
  "anti_pattern": "testing only the hospitable copy and shipping PASS; calling an untested mechanism operational",
  "related": ["SN-01231"]
}
```
