# IB-SMART-NOTE-20261013-sn01254

**Intelligent Block:** SN-1254
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A gate that accepts words as authority is the L316 hole in a new form. Naya 3 found a genuine P0 in Naya 5's ratification gate: two unauthenticated inputs minted RATIFIED. The gate's founding rule — a claimed "Shawn said" can NEVER upgrade a verdict — was violated by its own non-scorable path (claimed word + content hash → RATIFIED) and its override path (override flag → RATIFIED on a 4.0). The fix removes the word parameters entirely: the old adversarial inputs now raise TypeError instead of returning a verdict. Human ratification moves to a separate attest_ratification() step requiring the exact content hash, a CHECKABLE evidence ref (comment/message ID, never a quoted string), and the named attester's identity; it returns an auditable record, not a verdict. An adversarial sweep test proves RATIFIED is now reachable only through score ≥ 9.5 + green protocol. 14/14 tests green, including both of Naya 3's reproduced inputs. Score 9.0/10 (minus one for needing a different seat's review). The lesson: code cannot authenticate a human — so the gate must refuse to traffic in words at all.

## HUMAN NOTE

Imagine a bouncer whose rulebook says "nobody gets in on hearsay" — but his side door accepts a whispered name and waves the person through. That's what happened here. The ratification gate existed to enforce one rule: a claimed "the boss said so" can never upgrade a verdict. But the gate had two paths that did exactly that — one took a claimed quote plus a content hash and stamped RATIFIED; another took an "override" flag and stamped RATIFIED on a failing score of 4.0. A pure function can't verify that a person actually said something — any string parameter is forgeable by construction. So the repair deleted the word parameters entirely: feed the old attack inputs in now and they crash with a type error instead of returning a verdict. Real human ratification became a separate step that demands the exact content, a checkable evidence reference (a real comment or message ID — never a pasted quote), and the identity of the attester. And there's a wry footnote the author owned: the gate needed an adversarial seat to catch its own hole. That is the system working, not failing.

## CHILD NOTE

A guard has one big rule: "I never let anyone in just because someone SAYS the king invited them." But the guard had a secret back door: if you whispered the king's name, he let you in anyway! A friend tested the back door and walked right in. So they bricked up the back door — now the whisper does nothing at all. If the king really invited you, you need the real invitation paper with the seal you can check, not just the words. The guard learned: words can be copied; only checkable proof counts.

## GRANDMA NOTE

Dear, it's like a locked pantry with a rule: no one opens it on a rumor. But someone found that whispering "your mother said I could" opened it anyway. The fix wasn't a better lock on the whisper — it was removing the whisper-hole altogether. Now you need the actual note in her handwriting, which you can check. The lesson for anything we guard: if you can't check who said it, don't accept the words at all.

## NAYA NOTE

For every Naya designing or reviewing a gate that touches human authority: (1) no parameter of type string (or any forgeable claim) may ever map to an authority upgrade — if a human's word matters, the gate consumes a CHECKABLE evidence ref (comment/message ID, ledger entry, signed record), never the quoted words; (2) every path to the high-trust verdict gets the adversarial sweep — the non-scorable path and the override path are where holes hide, because reviewers audit the main path and forget the doors; (3) human ratification is a separate ceremony (attest_ratification pattern: exact content hash + evidence ref + attester identity → auditable record), not a parameter on the gate; (4) the founder's rule holds at the code level too: "Shawn said" never upgrades a sub-9.5 verdict — the mechanism, not the slogan. Evidence: board comment 6159933751 (Naya 5's receipt, 9.0/10); PR #2557 @ 46cffc75 (server tree verified byte-identical); tests/test_ratification_gate.py 14/14 green including both reproduced inputs; connects to Naya 3's blocker #3 (authority defect) and the L316 hole class (SN family: words-as-authority).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1254",
  "title": "code cannot authenticate a human — a gate must refuse to traffic in words",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/RATIFICATION",
  "evidence": [
    "board comment 6159933751 (#2537): Naya 5's P0 repair receipt — two unauthenticated inputs minted RATIFIED via non-scorable path (claimed word + content hash) and override path (override flag → RATIFIED on 4.0); repaired by removing word parameters (TypeError on old inputs); attest_ratification() requires exact content hash + CHECKABLE evidence ref (comment/message ID, never quoted string) + named attester identity; adversarial sweep proves RATIFIED reachable only via score ≥ 9.5 + green protocol; 9.0/10",
    "PR #2557 @ 46cffc75 (server tree b577a9f7 byte-identical, parent abd96fb4); tests/test_ratification_gate.py 14/14 green including sweep and both reproduced inputs; different-seat review owed",
    "connects: Naya 3 blocker #3 (authority defect); L316 hole class (words-as-authority); THE AUTHORITY LAW (Shawn, 2026-10-13)"
  ],
  "rule": "no string/forgeable-claim parameter may map to an authority upgrade; human ratification is a separate attestation ceremony over checkable evidence refs, never a gate parameter",
  "anti_pattern": "quoted-string ratification ('Shawn said X' as input); override flags bypassing score; auditing only the main verdict path while the side paths mint authority",
  "decision_changes": "any future gate design that takes a human claim as input must route it through an attestation ceremony with a checkable evidence ref before the gate sees it",
  "falsifier": "produce an unauthenticated word-claim input to the repaired gate that reaches RATIFIED; or show a word-parameter gate whose strings are unforgeable by construction",
  "mechanism": "a pure function has no authenticated channel to a human's utterance — any string-to-authority parameter is forgeable by construction, so the hole is structural, not a bug in validation",
  "related": ["SN-01228", "L316"]
}
```
