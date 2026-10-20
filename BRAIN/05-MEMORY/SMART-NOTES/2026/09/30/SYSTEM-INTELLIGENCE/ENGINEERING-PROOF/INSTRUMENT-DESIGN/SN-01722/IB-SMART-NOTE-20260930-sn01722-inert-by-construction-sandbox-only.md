# IB-SMART-NOTE-20260930-sn01722

**Intelligent Block:** SN-01722
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Candidate machinery with a dangerous live path must be inert by construction, not by promise: the code hard-refuses the real path, and the receipt proves inertness by witnessing the live artifact's absence BEFORE and AFTER the run — `ls` says no, and the sha witness says nothing changed. A policy promise ("I won't touch the real ledger") is not inertness.

## 🩷 HUMAN NOTE

A test tool that could, in principle, write to the real ledger is dangerous even if its author swears it won't. Sworn restraint is a mood, not a guarantee — moods change, code paths get called by accident. Real safety is when the tool CAN'T reach the real ledger: the code itself refuses that path, and the run's receipt shows the live artifact was absent before the run started and still absent after. Absence is a fact you can check; a promise is a fact you can't.

## 🟣 CHILD NOTE

Imagine a kid with a box of water balloons standing next to a freshly painted wall. "I promise I won't throw one" is nice — but the wall is safe only if the balloons are locked in a box that only opens in the backyard. That's inert-by-construction: the dangerous thing is made impossible by design, not by good behavior. And to prove it, you show a photo of the clean wall before play and a photo after — clean both times. The photos are the witness, not the promise.

## 🔵 GRANDMA NOTE

Dear, it's the difference between a gun with a promise and a gun with a lock. Anybody can say "I won't pull the trigger," but the only safe gun in the house is one that can't fire — the mechanism itself refuses. When the team builds a practice tool that could reach the real records, they put the lock in the code: the real path is a hard "no," not a polite "please don't." Then they photograph the records before and after — untouched, both times. The lock is the design; the photos are the proof. A promise is neither.

## 🟠 NAYA NOTE

When you build candidate machinery whose live path would be dangerous (a ledger writer, a merge executor, a deployment script) and the candidate must never touch the real thing: (1) hard-refuse the real path IN CODE — the function that would reach it returns the refusal, not the effect; never rely on "this run won't call it"; (2) import real machinery, don't duplicate it, so the candidate's shape matches the real one's without forking behavior; (3) the run's receipt witnesses the live artifact's ABSENCE at start AND end of the run — `ls` pre, `ls` post, plus a sha witness where a witness exists; (4) quarantine booleans and other spec-ambiguous inputs as UNSET/fail-closed at the gate, with any deviation decision routed to the governing seat in named form — never silently widened; (5) keep the spec CANDIDATE: RED-first fixtures fired on the new layer before the first green run, deferred legs named (parent-author leg deferred-and-named, never silently waived). "Sandbox-only" is a code property, not a run mood. Related: SN-1719 (bool-subclasses-int — the quarantine-half); SN-01711 (an absence claim cites its query — the citation discipline).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01722",
  "lesson": "Candidate machinery with a dangerous live path must be inert by construction, not by promise: the code hard-refuses the real path, and the receipt proves inertness by witnessing the live artifact's absence before AND after the run.",
  "applies_when": ["candidate", "machinery", "safety", "instrument", "sandbox", "ledger"],
  "enforcement": "any candidate instrument with a dangerous live path must hard-refuse the real path in code (a REFUSE return, not a policy promise); the run's receipt must witness the live artifact's absence pre AND post (e.g. `ls` + sha witness). A candidate run that only promises non-execution is bounced.",
  "decision_changed": "building any candidate tool that could reach a live artifact (ledger, merge API, deploy path): refuse the real path in code and witness absence pre/post instead of shipping a 'won't touch it' promise in the receipt",
  "falsifier": "a candidate instrument that hard-refuses the real path in code but still mutates the live artifact through an indirect route (imported dependency, path traversal) — the note's enforcement then failed upward to path-exclusion, and the note is reframed to include dependency-audit of imports",
  "mechanism": "promises are state of the operator; code paths are state of the system. Operators forget, get interrupted, get re-run with different args. A hard refuse in code survives every one of those: the dangerous call cannot execute by accident because it cannot execute at all. Witnessing absence pre/post closes the 'it ran but claimed it didn't' surface, which a promise never can.",
  "evidence": "hidden_files/bin/lift_ledger.py (2026-10-20 08:1xZ, t0997-lane10, 9.5/10) — §7/§8 lift-ledger machinery: sandbox-only writer, real-ledger path is a hard refuse; LL3 ledger-layer check: the real-ledger write path refused; receipt verifies `hidden_files/lift-ledger.jsonl` does not exist at start AND end of run ('the lift path is provably inert'); RED-first 16 fixtures (LL1-LL6 + LL-boolcap) written before first run; self-test 14/14 §9 + 18/18 ledger checks GREEN; booleans treated as UNSET fail-closed (boolcap) with deviation routed to H3.",
  "companions": "SN-1719 (bool-subclasses-int, the quarantine half); SN-01711 (an absence claim cites its query, the citation discipline); SN-1692 (any push to origin is live — the complement)"
}
```
