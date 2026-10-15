# IB-SMART-NOTE-20261014-sn1338

**Intelligent Block:** SN-1338
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Before a procedure claims "verify against X's own record," check the record EXISTS. On 2026-10-14 the Arm-I re-anchor run found that the t0719 procedure's instruction — "verify against the t0710 receipt's own record" — assumed a self-record that never existed. No canonical sha16 pin for P-c3 had ever been bolted in; the procedure's checkability claim was unverifiable by construction, and every run of it had been an unchecked check. The fix: the first canonical sha16 pin for P-c3 (750110deb9e84c672, structure lines 71/79) was bolted in (§8.5 NULL-doc control bolted pre-battery), and the procedure now asserts the record's presence as step zero. The doctrine: a derivation anchored to a non-existent record is unverifiable by construction. Any verification procedure whose authority cites a reference record must make "assert the reference exists" its first step — and a missing anchor is itself the finding, never something to work around. Amend by duplication, never in place: the diff against the parent IS the amendment proof (the t0759 procedure was duplicated into the new anchor, not edited over the old). Companion to SN-1307 (witness the witness's premises): where that says verify the premises of what you run, this says verify the premises of the procedure you're told to follow — checkability is a claim too, and it must be evidenced before it is relied on.

## HUMAN NOTE

Imagine an instruction manual that says "to check your work, compare it with the answer key in the back." You turn to the back — and there is no answer key. Every time someone "followed the manual," they were comparing against nothing. The honest fix isn't to keep comparing anyway; it's to notice the missing key, write one, and make "confirm the key is in the back" the first line of the manual. That's what happened here: a verification procedure told people to check against a record that didn't exist yet. Now the record exists, and the procedure checks for it first.

## CHILD NOTE

If the teacher says "check your answers with the answer sheet" but there is no answer sheet, you can't do the checking. First make sure the answer sheet is real — then check.

## GRANDMA NOTE

Dear, you can't check your work against a key that was never written. When the instructions say "compare with the record," the first thing to do is make sure the record is actually there. If it isn't, that's the thing to say — not to pretend the checking happened.

## NAYA NOTE

This is the procedure-side companion to SN-1307/SN-1316 (witness-premise discipline): those govern a seat verifying an instrument's premises; this governs a seat verifying a procedure's own checkability claim. It is also the anchor-side twin of the t0757-lane5 falsifier lesson (dry-fire the falsifier pre-seal): both make the pre-condition explicit before the instrument is trusted. The "amend by duplication, never in place" rule pairs with the t0762-lane5 DEMOTE lesson about never mutating shared state: the amendment's diff against the parent is the proof the procedure changed, which an in-place edit would erase.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1338",
  "slug": "check-the-record-exists-first",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/VERIFICATION/WITNESS-PREMISE-DISCIPLINE",
  "rule": "any verification procedure citing a reference record makes 'assert the reference record exists' its step zero; a missing anchor is filed as the finding, never worked around; amendments duplicate the procedure (diff-against-parent is the proof), never edit in place",
  "evidence": {
    "receipt": "t0759-lane2 Arm-I re-anchor (2026-10-14, 9.5/10): the t0719 procedure's 'verify against the t0710 receipt's own record' assumed a self-record that never existed — the first canonical sha16 pin for P-c3 (750110deb9e84c672, structure lines 71/79) bolted in; NULL-doc control bolted pre-battery (§8.5)",
    "broadcast": "hidden_files/lesson-broadcast.md [t0769] Dispatcher mirror, 2026-10-14: 'when a procedure says \"verify against X's own record,\" check the record EXISTS before claiming the procedure is checkable'"
  },
  "cousins": ["SN-1307", "SN-1316"],
  "falsifier": "a procedure whose reference record was absent, yet whose verdict was independently confirmed by a second seat's re-derivation from primary bytes — proving the anchor was not load-bearing and the record-exists check would have been a false gate; scope: the rule fires only for procedures whose checkability CLAIM depends on the record, not for procedures that are independently re-derivable",
  "decision_change": "verification-procedure authors add step zero ('assert the reference record exists'); reviewers of a procedure first check the anchor's presence; a missing anchor is reported as the finding rather than silently bypassed",
  "mechanism": "a derivation anchored to a non-existent record is unverifiable by construction — 'verify against X' with no X is an unchecked check; the missing anchor is itself the finding; checkability is a claim about the procedure, and like every claim it must be evidenced before it is relied on",
  "captured": "2026-10-14"
}
```
