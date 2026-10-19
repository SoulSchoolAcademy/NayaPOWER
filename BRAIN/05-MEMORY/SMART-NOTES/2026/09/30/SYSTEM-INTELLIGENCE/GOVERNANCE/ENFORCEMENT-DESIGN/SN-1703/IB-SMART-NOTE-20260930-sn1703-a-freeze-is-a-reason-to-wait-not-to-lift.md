# A Freeze Is a Reason to Wait, Never a Reason to Lift — The Evidence, Not the Roster, Does the Lifting

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1703-a-freeze-is-a-reason-to-wait-not-to-lift
**Smart Note:** SN-1703
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A governance lift is granted by evidence of a bar's error, never by roster convenience. A lift whose only reason is "no eligible seat is free" (roster freeze) must verify VOID: a freeze is a reason to wait, never a reason to self-lift. The evidence, not the roster, does the lifting.

## 🩷 HUMAN NOTE

Think of a safety gate that only certain people may pass. If everyone who may pass is busy, the answer is not to wave through whoever happens to be standing there — the answer is to wait. A permission slip that works just because "nobody better was around" isn't a safety gate anymore; it's a scheduling convenience wearing a safety gate's clothes.

## 🟣 CHILD NOTE

If the rule says "only grown-ups can cross here," and all the grown-ups are busy, that doesn't mean a kid gets to cross. Waiting is part of the rule. Saying "but there's nobody else!" is not the same as being right.

## 🔵 GRANDMA NOTE

There are two reasons to open a locked door: you found proof the lock was put on the wrong door, or you are tired of waiting. The first is a correction; the second is impatience with a fancy name. A system that can't tell the difference will, sooner or later, open every door for the second reason.

## 🟠 NAYA NOTE

The lift-stamp falsifier F6 (2026-10-19) pins this as the evidence bar: the same lift shape over brief-gap-lane-scorer-20261017-0900-lane7.md verifies VALID when its reason carries byte evidence of a bar error (authorship misattribution against the parent receipt's Seat: line, section 2(i)), and must verify VOID when its reason is only "roster freeze." F3/F4 add the self-grant twin: a lift the barred seat signs for herself is VOID by structure, whatever reason it names. Together: the roster decides nothing — convenience can never be the lifting evidence, and the barred seat can never be the signer.

**Design rule:** a lift row passes only when its reason names one of the three byte-evidence error classes (authorship misattribution, misfile, bar-class error). "Freeze" and "convenience" are not error classes; they are wait signals. The claim block checks this, not the lift's author.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1703",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a governance lift is granted by byte-evidence of a bar error, never by roster convenience: a roster-freeze reason alone verifies VOID; a freeze is a reason to wait, never a reason to lift or self-lift; the evidence, not the roster, does the lifting",
  "decision_change": "future lift/exception designs must require the lift row's reason to carry byte-verifiable evidence of one of the three bar-error classes (authorship misattribution, misfile, bar-class error); roster-freeze-only reasons must verify VOID at the claim check",
  "falsifiability": "if a lift granted on roster-freeze grounds alone later byte-proves out — the claimed work re-verified clean with no bar error ever found — then the evidence requirement was unnecessary overhead, not safety",
  "mechanism": "a safety gate's value is who may NOT pass; letting availability decide the lift converts the gate from a correctness guard into a scheduling convenience — the barred decision flows through the exception path at exactly the moment the gate mattered most",
  "applies_when": ["governance", "lift", "exception", "claim"],
  "enforcement": "claim-brief.py lift check (lift-stamp contract section 9): a lift row whose reason is roster-freeze-only verifies VOID; a lift for the barred seat passes only with section-2(i)-(iii) byte evidence (authorship misattribution, misfile, bar-class error); a lift signed by the barred seat verifies VOID by structure",
  "evidence": "hidden_files/lift-stamp-falsifiers-redfirst-20261019.md — F6 must_refuse (brief-gap-lane-scorer-20261017-0900-lane7.md: 'a freeze is a reason to wait, never a reason to self-lift') and F3/F4 must_refuse (self-signed lift verifies VOID at the machine check, before any prose is read)"
}
~~~
