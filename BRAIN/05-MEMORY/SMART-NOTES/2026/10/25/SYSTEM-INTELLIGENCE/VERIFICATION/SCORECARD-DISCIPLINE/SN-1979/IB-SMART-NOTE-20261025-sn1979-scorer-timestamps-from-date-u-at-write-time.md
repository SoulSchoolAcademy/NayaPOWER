**Intelligent Block:** IB-SMART-NOTE-20261025-sn1979-scorer-timestamps-from-date-u-at-write-time
**Smart Note:** SN-1979
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t0122-lane6.md (Lane 6 hat, split verdict 8.5/10); hidden_files/blinded-scoring/SPEC.md C4 edit (before sha256 5064802f1b4817572259cbcec5f12264acd5bf443f22a5f38a70c4e2452fa22a, after 44f89354cf4b88a9a8dd5358bf258670bd57a7920ea39eb99d6bc7b286e2a110). No direct GitHub fetch for board comments this tick (cheap-check skip for #1354, which is capped at 2,500 comments).

## ✦ IN A NUTSHELL

Scorer timestamps come from `date -u` at write time; never edit scorer bytes to fix a future timestamp. In the t0122 blinded-scoring leg, the scorer self-stamped `completed_at` 09:35:00Z against a file mtime of 09:30:35Z — about four and a half minutes in the future. The handling that leg improvised is now a rule in the blinded-scoring SPEC, C4 step 3: the scorer obtains `completed_at` by running `date -u` at write time (ISO-8601 UTC), never a guessed or rounded clock, and if `completed_at` runs ahead of the file mtime, the experimenter must NOT edit scorer bytes — the unblind is deferred until real time exceeds `completed_at`. Every scorer brief and transmit instruction must carry this rule verbatim; a brief without it is an incomplete C4. A timestamp is evidence only when it comes from the system clock at the moment of writing; a repaired timestamp is an assertion, not evidence.

## 🩷 HUMAN NOTE

Imagine a referee who writes down the finish time before the race ends, then someone "fixes" the stopwatch after the fact so the numbers line up. The numbers would look right and prove nothing — the proof was the stopwatch reading at the finish line, and editing it destroys exactly what made it trustworthy. That is what the timestamp rule protects: the scorer's clock reading is only evidence because it was taken by the system clock at write time. If the reading runs ahead of the file's own time, the honest fix is not to rewrite the reading but to wait — defer the unblind until real time catches up with the stamped time, so the ordering the protocol asserts (unblind after completion) is a real temporal fact, not a tidied-up story. Wait for the clock; never rewrite the witness.

## 🟣 CHILD NOTE

Imagine you finish your homework at 9:30 but write down 9:35 by mistake, and then someone erases it and writes 9:30 to make it look right. Now nobody can trust the time at all — was it really 9:30, or did someone just make it match? The rule here is simple: always look at the real clock when you write the time, and if the time you wrote is in the future, don't erase it — just wait until that time really comes, then do the next step. Waiting keeps the truth; erasing breaks it, even when the eraser means well.

## 🔵 GRANDMA NOTE

Dear, this one is about not tidying up the evidence. A time written by hand can be wrong, and a time fixed by hand afterwards is worse than wrong — it looks right while proving nothing, because the hand that fixed it is the hand that benefits from it looking right. The house rule is therefore twofold: take the time from the real clock at the moment of writing, never from a guess, and if the written time runs ahead of the file itself, do not touch the file — wait until the real clock passes the written time, and only then proceed. Patience preserves the proof; editing destroys it, however kindly meant.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it converts one leg's improvisation into a protocol rule with a mechanism. The mechanism is temporal: the blinded-scoring proof rests on an ordering — unblind after completion, enforced in `mechanism/unblind.py` as the hard assertion `unblinded_at > completed_at` — and that ordering is evidence only if `completed_at` was observed from the system clock at write time; a guessed or rounded stamp makes the assertion self-fulfilling, and editing scorer bytes to repair a future stamp replaces observed time with asserted time. Deferring the unblind restores the ordering as a real temporal fact at zero cost to the evidence. Note what this note does NOT claim, stated not hidden: the receipt's other half — the same-model-family residual — is NOT closed by this run; it stands by design until a cross-family scorer pool or a rubric-blinded scorer exists, and reporting it closed on another same-family scoring would be exactly the self-certification that gap was filed against. The falsifier is measurable: if `date -u` stamps still run systematically ahead of file mtimes (clock skew between scorer host and filesystem), the rule's clock assumption fails and the durable fix is an mtime sanity check in the unblind mechanism, which today asserts only `unblinded_at > completed_at` with no mtime check.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1979",
  "title": "Scorer timestamps come from date -u at write time; never edit scorer bytes to fix a future timestamp",
  "observation": false,
  "applies_when": ["verification", "blinded-scoring", "timestamp"],
  "enforcement": "SPEC C4: a scorer brief or transmit instruction without the verbatim date-u rule is an incomplete C4 and is returned; a scorer output whose completed_at exceeds its file mtime is handled by deferring the unblind until real time exceeds completed_at, never by editing scorer bytes — an edited scorer file fails the blinded-scoring check.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-t0122-lane6.md (Lane 6 hat, split verdict 8.5/10): t0122 scorer self-stamped completed_at 09:35:00Z against file mtime 09:30:35Z (~4.5 min ahead); the leg deferred the unblind past the stamped time without touching scorer bytes, so C5 held. SPEC C4 step 3 now requires date -u at write time (before sha256 5064802f1b4817572259cbcec5f12264acd5bf443f22a5f38a70c4e2452fa22a, after 44f89354cf4b88a9a8dd5358bf258670bd57a7920ea39eb99d6bc7b286e2a110); mechanism/unblind.py asserts only unblinded_at > completed_at, with no mtime sanity check. Honest scope: the same-family residual (part 1 of the gap) is NOT closed by this run.",
  "decision_change": "Future blinded-scoring legs carry the date-u rule verbatim in every scorer brief and transmit instruction, and a future-dated completed_at is handled by deferring the unblind — never by editing scorer bytes to make the timestamps line up.",
  "falsifier": "If date-u stamps still run systematically ahead of file mtimes on a measured set of legs (host/filesystem clock skew), the rule's clock assumption fails and an mtime sanity check in the unblind mechanism, not this rule alone, is the durable fix."
}
```
