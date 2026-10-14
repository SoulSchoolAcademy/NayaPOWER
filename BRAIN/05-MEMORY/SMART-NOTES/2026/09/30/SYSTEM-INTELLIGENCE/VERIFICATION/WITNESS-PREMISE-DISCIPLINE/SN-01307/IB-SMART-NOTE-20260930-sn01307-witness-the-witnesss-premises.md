# IB-SMART-NOTE-20261014-sn1307

**Intelligent Block:** SN-1307
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Witness the witness's own premises, not just its outputs. At t0770 an independent seat ran the witness check for lane-2/pin_rederive_check_t0759.py — 9/9 pins MATCH at live tip 0cc7c9f2 — but before trusting the checker's object-addressed P-mech derivation, the seat ran the premise check on the mirror itself: `git cat-file -t` on the tip object, proving the addressed object actually exists in the store being run against. Shared-state was treated as a cache (re-pinned via git ls-remote at action time), and stale mirror refs (e8b4868ce4) couldn't bite because addressing is by object, not by ref. The lesson: an object-addressed derivation is only as trustworthy as the object's presence in the store you are running against — outputs matching tells you the checker agreed with itself; the premise check tells you it agreed with the world.

## HUMAN NOTE

Shawn — this is the one extra step that turns "an independent seat confirmed it" into proof you can actually rely on. This morning a second seat re-ran a witness check and got 9/9 matching pins — good. But before accepting that result, she verified the premise the checker depended on: that the exact git object the checker derived from actually exists in the repository copy she was running against. She didn't trust the shared-state file (it's a cache, refreshed only twice an hour), and she didn't trust the mirror's branch pointers (one of them was stale). She went one level deeper — asked the object store directly whether the thing exists. It did. That's the standard now: don't just witness the outputs; witness the premises. An agreement between a checker and itself is worth exactly what its foundation is worth.

## CHILD NOTE

Imagine a kid who checks whether a puzzle answer is right by comparing it to the answer key. Another kid checks the checker — she makes sure the answer key is the real one for THIS puzzle, not last week's. Because if the key is wrong, the checker can match it perfectly and still be wrong. The second kid's extra step is the lesson: always check the checker's key, not just the checker's answers.

## GRANDMA NOTE

Dear, it's like this: two bookkeepers agree the accounts balance. That's nice — but before you trust them, you make sure they're looking at the real ledger and not an old photocopy. This morning the second bookkeeper did exactly that extra step: she went to the vault and confirmed the ledger pages the first one used are really there, right now, not an old copy. The lesson the girls wrote down: an independent check is only as good as what it stands on. Check what it stands on.

## NAYA NOTE

For every seat consuming or producing an independent witness run: (1) the witness run must name its premises — what object/commit/state it derived from, resolved at action time, never from a cache; (2) before accepting the outputs, run the premise check in the same environment: for git-object derivations, `git cat-file -t <object>` on the store you're running against — shared-state.json is a cache, never a pin; branch refs can be stale (t0770's e8b4868ce4); the object store is the ground; (3) addressing by object is the defense: stale refs can't poison an object-addressed derivation, because the derivation never consults the ref namespace — but the defense only holds if the object is present in that store; (4) record the premise check in the receipt alongside the outputs. Evidence: hidden_files/lesson-broadcast.md [t0770] Dispatcher mirror — "witness the witness's own premises, not just its outputs; an object-addressed derivation is only as trustworthy as the object's presence" (9/9 pins MATCH at live tip 0cc7c9f2; re-pinned via git ls-remote at action time; stale mirror refs don't bite when addressing is by object). Standing principle applied: live bytes; independent eyes.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1307",
  "title": "Witness the witness's own premises, not just its outputs — object-addressed trust chains to the object store",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/VERIFICATION/WITNESS-PREMISE-DISCIPLINE",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0770] Dispatcher (reconcile, t0763-lane6 DONE 9.5/10): independent-seat witness run of lane-2/pin_rederive_check_t0759.py — 9/9 pins MATCH at live tip 0cc7c9f2 (re-pinned via git ls-remote at action time; shared-state treated as cache); the seat ran the premise check on the mirror itself (git cat-file -t on the tip object) before trusting the checker's object-addressed P-mech derivation — stale mirror refs (e8b4868ce4) don't bite when addressing is by object; 'witness the witness's own premises, not just its outputs; an object-addressed derivation is only as trustworthy as the object's presence'"
  ],
  "rule": "an independent witness run names its premises resolved at action time (never from shared-state cache); the consuming seat re-verifies the premise in the run's own environment (git cat-file -t for object derivations) before accepting the outputs; addressing by object is the structural defense against stale refs",
  "anti_pattern": "accepting a witness run because 'outputs match' without checking what the outputs were derived from; pinning the derivation base to shared-state.json (a cache) instead of git ls-remote at action time; trusting mirror branch refs that may lag the live store",
  "related": ["SN-1306", "SN-0724"],
  "falsifier": "an object-addressed derivation that produces correct-looking outputs while git cat-file shows the addressed object missing from the store it ran against — that would mean object-addressed trust does NOT chain to object presence and the mechanism is wrong; or a stale ref shown to corrupt an addressing-by-object derivation",
  "decision_changed": "what a consuming seat must do before accepting an independent witness run (premise check in the same environment, outputs second); how witness receipts are written (premises + outputs, both named); the live dispatch rule: re-run discover+verify per dispatch, re-pin via git ls-remote at action time, unknown != clean",
  "mechanism": "an object-addressed derivation's trust chains to the object store (git object DB), not the ref namespace — the ref namespace is a mutable, laggy pointer layer (stale e8b4868ce4 proves it); git cat-file -t on the addressed object closes the chain at the ground; outputs matching alone only proves the checker agreed with itself"
}
```
