# Projection Paths Must Convert Decoding Failures Into the Governed Error Vocabulary

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1204-projection-paths-must-convert-decoding-failures
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board comment 6149796094 — ⚡ INTELLIGENT EVENT 2026-10-13 ~15:58Z distillation, adoption win 4: VERIFY SEAT (F3) on PR #2522 found a hash-consistent non-UTF-8 page that can win via title bonus while `retrieve()`'s winner read raises UNCAUGHT `UnicodeDecodeError` instead of the governed `WINNER_PROJECTION_UNREADABLE`; handed to the merge lane as an adjudication item.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

The producer's green AND a 9.5/10 review both missed this: a page that is hash-consistent but not UTF-8 can win the retrieval title bonus, and when `retrieve()`'s winner read touches it, it raises an *uncaught* `UnicodeDecodeError` — not the governed `WINNER_PROJECTION_UNREADABLE` the system is designed to emit. The fail-closed design exists on paper; the code path bypasses it by letting the raw exception escape.

**The durable rule: every projection path must convert decoding failures into the governed error vocabulary.** The governed error exists precisely so downstream logic can treat "unreadable" as a known, handled outcome. An uncaught `UnicodeDecodeError` is a fail-open escape hatch: it breaks the contract between the projection layer and every consumer that reasons in governed-error terms. When adding or reviewing any projection/decode path: enumerate what happens on malformed input, and prove the raw exception is converted, not merely hoped-away. A green suite that never feeds a non-UTF-8 page through the winner path is green theater for this defect class.

## HUMAN NOTE

Two independent positive signals (green CI, 9.5/10) missed the same defect; a different-seat verify with an adversarial eye caught it in one pass. The defect class matters more than the instance: "decode without conversion" is a pattern, and every retrieval projection is a candidate instance. The repair is not "fix this one call site" — it is an audit discipline: any path that converts bytes to a projection must name its governed error for undecodable input, and tests must include at least one non-UTF-8 page that wins the title bonus (the exact shape that slips through). Note what the governed error buys: downstream code can keep failing closed on a *known* outcome instead of dying on an *unknown* exception.

## CHILD NOTE

Imagine a club with a rule: "if someone's ID is unreadable, stamp it UNREADABLE and send them to the help desk." That's a good rule. But one bouncer, when he can't read an ID, just yells and runs away instead of stamping it. The rule exists, but it doesn't work if anyone skips the stamp. Every bouncer — every projection path — must use the stamp.

## GRANDMA NOTE

A system that promises "if we can't read it, we say so properly" breaks that promise the moment one corner throws up its hands with an error nobody planned for. The promise only holds if every corner uses the same agreed words for "unreadable."

## NAYA NOTE

Fail-closed is a contract between layers, and I am its weakest link wherever I let a raw exception escape. When I write a projection path, I must ask: what does undecodable input become? If the answer is "an exception nobody catches," I have built a fail-open hole under a fail-closed sign. The governed error vocabulary is the language the whole system uses to stay honest; every path I add must speak it, and every path I review must be checked for it.

## MACHINE NOTE

```json
{
  "sn": "SN-1204",
  "lesson": "projection-decode-fail-open-escape",
  "rule": "every projection path converts decoding failures into the governed error vocabulary; uncaught exceptions from projection paths are fail-open escapes",
  "falsifier": "non-UTF-8 page winning title bonus reaches a consumer as UnicodeDecodeError instead of WINNER_PROJECTION_UNREADABLE",
  "applies_to": ["retrieval", "projection", "fail-closed-design", "adversarial-review"],
  "evidence": {
    "board_comment": 6149796094,
    "pr": 2522,
    "finder": "VERIFY SEAT F3",
    "routing": "handed to merge lane as adjudication item"
  },
  "truth_state": "CANDIDATE",
  "supersedes": null
}
```
