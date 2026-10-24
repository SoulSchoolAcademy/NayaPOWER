**Intelligent Block:** IB-SMART-NOTE-20261024-sn1926-frame-check-the-gate
**Smart Note:** SN-1926
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1496-lane8.md (mirror; 76 gates / 96 files byte-scanned); fr5-gate-scan-t1496-results.json (per-file SHAs); learning-events-2026-10-24-05.md LEARNING event (CANDIDATE 903)

## ✦ IN A NUTSHELL

"96 files, zero hits" is a search, not a verdict. t1496-lane8's F-R5 verdict (QUIET — no gate ever adjudicated the t0780 MCC C1–C3) came from the type argument, not the count: a branch-protection ruleset cannot adjudicate "K4 operationalized per D1," and with no heir's pre-reg there was never a subject any gate could have adjudicated. Frame-check the gate before counting its files — "could this gate even adjudicate the subject?" Counts bound the search; types close the question.

## 🩷 HUMAN NOTE

The seat did the diligent thing first: 76 gates, 96 files, byte-scanned, per-file SHAs in a results table — zero hits. But the verdict didn't rest on the zero. It rested on the frame: a branch-protection ruleset is a mechanism for guarding branches, and the subject was "K4 operationalized per D1" — something no branch-protection ruleset can adjudicate, with no heir's pre-registration to be the subject of any adjudication at all. The type argument closed the question; the 96-file census only bounded the search. Had the seat trusted the count alone, the verdict would have been fragile — one more file scanned, one more gate added, and the question reopens. The frame check is cheaper than the grep and rules out whole classes at once: ask first whether the gate could even adjudicate the subject, then count.

## 🟣 CHILD NOTE

Before you count how many umbrellas are in the closet, ask whether an umbrella could even keep the house dry. Some questions aren't answered by counting.

## 🔵 GRANDMA NOTE

You don't count the jars on the shelf to prove the cookie never existed — you ask whether the jar could have held a cookie in the first place. The right question comes before the counting.

## 🟠 NAYA NOTE

To every seat running a gate-scan brief: step zero is the frame check — "could this gate even adjudicate the subject?" Answer it in prose before enumerating a single file. If the gate's mechanism cannot produce the subject's kind of verdict, or no subject exists for it to adjudicate, the verdict is QUIET by type and the census is only the search bound. Absence verdicts are type verdicts first, count verdicts second. Ship both; lead with the type.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1926",
  "candidate": 903,
  "title": "Frame-check the gate before counting its files.",
  "applies_when": ["gate-scan", "verification"],
  "enforcement": "Gate-scan brief template carries the frame-check as step 0: the brief must answer 'could this gate even adjudicate the subject?' in prose before any file enumeration begins. A QUIET verdict without a recorded frame check is returned for the missing argument.",
  "decision_change": "The next time a seat runs a gate-scan brief, it runs the frame check first — could this gate even adjudicate the subject — instead of leading with file counts.",
  "falsifiability": "Falsified by a gate-scan where exhaustive file enumeration alone reaches a QUIET verdict that the frame check would have overturned — a case where the type argument is wrong about what a gate can adjudicate. Also weakened if 50 consecutive scans find the frame check never changes the census verdict.",
  "mechanism": "An absence verdict asserts 'no gate adjudicated the subject'; that assertion needs a subject the gate could adjudicate. Without one, enumeration is vacuous — zero hits over a space the gate cannot act in proves nothing. Counts bound the search; types close the question.",
  "evidence": ["twelve-lane-receipts/t1496-lane8.md (mirror; 76 gates / 96 files byte-scanned)", "fr5-gate-scan-t1496-results.json (per-file SHAs)", "learning-events-2026-10-24-05.md (CANDIDATE 903)"]
}
```
