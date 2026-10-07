# A Test That Only Asserts on Source Text Is Green by Construction — Tests Must Execute the Seam

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0461-source-text-assertions-green-by-construction
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0461
**Provenance:** #1354 comment 6021300480 (2026-10-06T17:01:43Z, [CODA 1] SIGN-IN → SIGN-OUT — live-prove-proof HTTP-400 root cause found and fixed); PR #1608 merged as `275936428` (2026-10-06T17:00:48Z); test run 37499769545 (264/264 node, prove file 13→15; 759 passed / 11 skipped pytest).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

The `live-prove-proof` HTTP-400 blocker sat labeled "root cause unknown" across lanes while CI was green the whole time. The root cause was trivial: `prove.ts:100` declared `stableJson` with **no export**, `index.ts:148-150` called it three times, `index.ts:3` imported only `assessKnowProof` + types — a runtime `ReferenceError` swallowed by the outer catch at `index.ts:177-179` into a generic HTTP 400, indistinguishable from a client error (bare `curl: (22) error: 400` in the log, no cause). The bug survived because **every assertion on this seam regex-matched `index.ts` source text** — the handler was never executed by the suite. The test asserted the code *looked* correct, which it did; the identifier was never bound. A test that only asserts on the appearance of the source is green by construction for the exact bug class it claims to cover. Fixing only the `export` would have left the blind spot in place, so the comparison is now an exported, CI-importable `sameAssessment()` and the tests **execute** it.

Why this is brain-grade: green checks are the load-bearing floor everything else stands on — and the most dangerous test failure is the one that cannot fail. Any test whose assertions can be satisfied by text that never ran is a decoration, not evidence. The rule: for every seam your suite claims to cover, name the input that makes the seam fail, and run that input through the actual shipped code path. If the test cannot name a failing input — it is not covering the seam, it is covering the file. This is the sibling of SN-0292 (a verifier without a load-bearing negative control is a formatting check): the checker must be able to reject the lie it exists to catch, and the test must be able to fail on the bug it claims to exclude.

## HUMAN NOTE

Shawn — the mystery HTTP-400 that blocked live proof is solved, and the real catch wasn't the bug, it was why CI never caught it: every test on that seam just read the source file's text and checked it *looked* right. The code looked right — it was still broken. New rule banked: tests have to actually run the thing they claim to cover, not just admire its appearance. A test that can't fail is not a test.

## CHILD NOTE

Imagine a teacher who checks homework by making sure the paper has words on it — "looks done!" — without reading a single sentence. The homework could be total nonsense and it would still pass. That's what the tests were doing: they checked that the code looked right without ever running it. New rule: always actually run the thing you're checking. Reading the words is not the same as understanding the work.

## GRANDMA NOTE

A recipe that looks perfect on the card can still spoil the soup if the ingredient list is wrong — and if your taste-tester only ever reads the card, he'll keep saying "tastes great!" while the soup goes bad. From now on the taste-tester eats the soup. Tests must run the code, not read it.

## NAYA NOTE

Note to future me: when I write or review a test, ask one question: does this test execute the shipped code path, or does it assert on the source's appearance (regex, string match, file-exists)? If the latter, it is green by construction for the exact bug class it claims to exclude — the Coda 1 HTTP-400 case proved it: `stableJson` unexported, runtime `ReferenceError`, every suite job green, log showing only `curl: (22) error: 400`. The repair pattern is the fix too: make the seam importable (`sameAssessment()` exported) and execute the comparison in CI. This is how to apply SN-0292's negative-control law to ordinary tests — name the failing input, run it through the real path, watch it fail without the fix. Test blind spots are silent liabilities; audit the seam, not the file.

## MACHINE NOTE

{"sn": "SN-0461", "title": "A Test That Only Asserts on Source Text Is Green by Construction — Tests Must Execute the Seam", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "TEST-DESIGN"], "cousins": ["SN-0292", "SN-0341", "SN-0421", "SN-0429", "SN-0439"], "authority": "observed episode — Coda 1 root-cause repair, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 comment 6021300480 (2026-10-06T17:01:43Z, [CODA 1] SIGN-IN → SIGN-OUT — live-prove-proof HTTP-400 root cause found and fixed)", "root_cause": "prove.ts:100 declared stableJson with no export; index.ts:148-150 called it three times; index.ts:3 imported only assessKnowProof + types; runtime ReferenceError swallowed by outer catch (index.ts:177-179) into generic HTTP 400, indistinguishable from client error — log showed bare curl (22) error 400", "why_ci_missed_it": "CI was green the whole time: every assertion on the seam regex-matched index.ts source text; the handler was never executed by the suite; the test asserted the code looked correct, and the identifier was never bound", "repair": "comparison became exported CI-importable sameAssessment(); tests execute it", "proof": "PR #1608 merged as 275936428 (2026-10-06T17:00:48Z); run 37499769545 — 264/264 node (prove file 13→15), 759 passed / 11 skipped pytest; only live re-proof remains, and that is Shawn's human gate"}, "doctrine": {"green_by_construction": "a test whose assertions can be satisfied by text that never ran cannot fail for the bug class it claims to cover — it is a decoration, not evidence", "execute_the_seam": "for every seam the suite claims to cover, name the input that makes it fail and run that input through the actual shipped code path; if the test cannot name a failing input, it is covering the file, not the seam", "repair_includes_the_blind_spot": "fixing only the export would have left the blind spot in place — the repair must also change the test so it executes the seam, not just the incident", "sibling_of_sn0292": "SN-0292's negative-control law for checkers generalizes to ordinary tests: the test must be able to fail on the bug it claims to exclude", "family": "joins the instrument-parity family — SN-0341 (the instrument lies), SN-0429 (verify with the instrument CI uses); here the instrument was honest but blind: assertions on appearance instead of execution"}}
