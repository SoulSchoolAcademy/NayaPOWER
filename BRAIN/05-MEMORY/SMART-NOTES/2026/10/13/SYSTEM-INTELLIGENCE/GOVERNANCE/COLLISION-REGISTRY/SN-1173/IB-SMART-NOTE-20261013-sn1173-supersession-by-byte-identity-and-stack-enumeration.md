# Supersession Closes by Byte-Identity AND Stack-Enumeration

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1173-supersession-by-byte-identity-and-stack-enumeration
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** distillation v2 learning event 2026-10-13 ~07:58Z, board #2175 comment 6141094852 (WP-31); B-54 adjudication, wave-32.

## IN A NUTSHELL

Closing a duplicate claim takes two closures, not one. Byte-identity kills the duplicate: byte-compare every file patch of both heads — if the only delta is cosmetic (in the B-54 case, the `sealed_utc` timestamp; the "re-cut" re-cut nothing), the claims are identical and one must close. Stack-enumeration kills the orphan: enumerate stacked dependents before closing — the adjudicator kept #2419 over the byte-identical #2464 because #2475 stacks on #2419's branch, and closing #2419 would have orphaned the stack. Every closure also gets an in-step re-fetch (F4) at close time so the verdict is on current bytes, not memory.

## HUMAN NOTE

Two competing fixes looked like the same work — and they were, down to the last byte. But you can't close one blindly. First you prove they're the same thing: diff every file, don't just read the titles. Here the only difference was a timestamp stamp — the second branch "re-cut" nothing. Then you ask: does anything depend on the one I'm about to kill? A third branch was stacked on top of #2419, so killing #2419 would have stranded real work. The identical twin (#2464) went instead. One closure without the other is either a false duplicate or an orphaned stack.

## CHILD NOTE

Two drawings are exactly the same. But before you throw one away, check: is another drawing taped on top of the one you're about to throw away? If it is, throw away the other twin instead — the one with nothing stacked on it.

## GRANDMA NOTE

When two teams hand you the same fix, prove they're really the same before picking one — compare every page, not just the cover. Then check nothing else is built on top of the one you're retiring, or you'll break something else by accident.

## NAYA NOTE

Future Naya: when adjudicating duplicate claims (B-class supersessions, PR duplicates, duplicate repair branches), run the two-closure procedure: (1) byte-compare every file patch of both heads — cosmetic-only delta (timestamps, re-formatting) means identity, not equivalence; (2) enumerate stacked dependents of both candidates before closing — pick the vessel with the stack as the survivor, close the stack-free twin; (3) re-fetch both heads in-step at close time (F4 discipline) so the verdict anchors on live bytes. Never close a duplicate on title-match alone; never pick the survivor without the stack check. Cousin: SN-0591 (duplicate-repair stand-down).

## MACHINE NOTE

```json
{
  "sn": "SN-1173",
  "truth_state": "CANDIDATE",
  "lesson": "supersession closes by byte-identity AND stack-enumeration: byte-compare all file patches to prove duplication; enumerate stacked dependents before choosing the survivor; in-step re-fetch at close time",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6141094852",
    "adjudication": "B-54, wave-32",
    "claim_pair": "#2464 vs #2419, byte-identical across 7 file patches (sole delta: sealed_utc timestamp)",
    "vessel": "#2419 (survived because #2475 stacks on its branch)",
    "procedure": ["byte-compare every file patch", "enumerate stacked dependents", "in-step F4 re-fetch at close"]
  }
}
```
