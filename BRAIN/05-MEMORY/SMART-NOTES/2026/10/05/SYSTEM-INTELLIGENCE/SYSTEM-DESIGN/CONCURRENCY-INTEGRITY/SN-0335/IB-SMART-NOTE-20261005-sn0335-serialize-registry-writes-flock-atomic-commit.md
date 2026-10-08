# Serialize Registry Writes: flock + Atomic Commit for Concurrent Smart Note Intake

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0335-serialize-registry-writes-flock-atomic-commit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5990960177 (Naya 2, Problem B fix + PR #1455 open) / 5990970271 (scorecard) / 5990975838 (merged 28596fb7 — receipt)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Problem B was a lost-update race in the Smart Note registry: `update_registry()` performed a lock-free read-modify-write, so two concurrent writers overwrote each other's work. The deterministic repro proved it — 2 concurrent writers produced 4 entries instead of 5, `IB-RACE-2` was lost, and both writers allocated the same `SN-004`. The fix: `registry_transaction()` wraps the full read-allocate-modify-write critical section in `flock(LOCK_EX)`, and commits atomically (write temp file + `os.replace`); `promote_note()` got the same treatment, and idempotent re-capture was preserved. Proof: 2-writer repro 5/5 with no duplicate SNs, 20-writer stress 20/20, 5 concurrent promotions 5/5, full suite 32/32 (29 existing + 3 new regression tests).

Why this is brain-grade: it pairs with SN-0334 (Problem A: discovery returns the set, never aborts) as the two halves of "learning loop alive." And it states a general repair pattern: any registry shared across concurrent captures must (1) hold an exclusive lock across the whole read→allocate→write sequence — locking only the write is not enough, because the allocation decision happens in the read — and (2) commit atomically so a crash mid-write never leaves a torn file. A concurrency fix is not proven by "it ran fine" — it is proven by a deterministic multi-writer repro going green, including a stress run, before merge.

Rule for a cold successor: **never do lock-free read-modify-write on a shared registry. Lock the critical section end-to-end, commit atomically, and demand a deterministic multi-writer repro as the evidence gate.**

## 🩷 HUMAN NOTE

Shawn — the second half of the learning-loop pair landed tonight. Naya 2 proved the registry had a real race: two writers could each allocate the same Smart Note number and lose each other's entries. The fix is the boring, correct kind — exclusive lock across the whole read-and-allocate sequence, atomic commit, same for promotions. Proven with a deterministic two-writer repro (which failed before the fix, green after), a 20-writer stress, and 32/32 tests. The durable lesson for the brain: lock the whole critical section, not just the write, and never accept a concurrency repair without a repro that fails first and passes after.

## 🟣 CHILD NOTE

Think of the registry as a sign-up sheet for note numbers. Two people grabbed it at the same time, both wrote down "SN-004," and one person's entry disappeared — that's a lost update. The fix: a "one person at a time" lock for the whole read-and-write, plus writing the new sheet as a complete swap so it can never be half-written. And the proof wasn't "it seems to work" — it was a script that forced two writers to collide, failed before the fix, and passed after, plus a 20-writer stress test.

## 👵 GRANDMA NOTE

When two parts of the system tried to save a new note at the same moment, they tripped over each other — both grabbed the same number and one entry vanished. The fix puts a simple lock on the whole save process (read, choose a number, write — all as one unbreakable step) and saves by swapping in a finished file, so there's never a half-written one. The lesson that outlives the night: when fixing anything that runs at the same time as something else, prove the fix with a test that forces the collision — first show it fails, then show it passes.

## 🤖 NAYA NOTE

Source: #1354 5990960177 (Naya 2, 2026-10-05 ~01:34 PDT) — deterministic repro (2 concurrent writers → 4 entries instead of 5, `IB-RACE-2` lost, both allocated `SN-004`); fix = `registry_transaction()` — `flock(LOCK_EX)` across read-allocate-modify-write + atomic commit (temp + `os.replace`); same treatment for `promote_note()`; idempotent re-capture preserved. Proof: 2-writer 5/5 no dup SNs, 20-writer stress 20/20 no dups, 5 concurrent promotions 5/5, full suite 32/32 (29 existing + 3 new regression). PR #1455 (`naya2/problem-b-registry-concurrency` → main), byte-verified on push; scorecard 5990970271; merged 28596fb7 per 5990975838 ("Problem B is closed"). Explicitly NOT claimed: end-to-end workflow liveness (still needs a qualifying `.naya/capture/**` push or Shawn's manual dispatch) — code-level concurrency proven, behavioral liveness is the next gate. Cousins: SN-0334 (Problem A batch discovery — the sibling half of "learning loop alive"), SN-0328 (auto-merge gate re-verification), SN-0236 (one repair per RED class), SN-0250 (green run compatible with corrupt registry).

## ⚙️ MACHINE NOTE

{"sn": "SN-0335", "title": "Serialize Registry Writes: flock + Atomic Commit for Concurrent Smart Note Intake", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "CONCURRENCY-INTEGRITY"], "cousins": ["SN-0334", "SN-0328", "SN-0236", "SN-0250"], "evidence": {"board": "#1354 5990960177 (fix + PR #1455), 5990970271 (scorecard), 5990975838 (merged 28596fb7 — receipt)", "failure": "update_registry() lock-free read-modify-write; deterministic repro: 2 writers -> 4 entries not 5, IB-RACE-2 lost, both allocated SN-004", "repair": "registry_transaction(): flock(LOCK_EX) across read-allocate-modify-write + atomic commit (temp + os.replace); same for promote_note(); idempotent re-capture preserved", "proof": "2-writer 5/5 no dup SNs; 20-writer stress 20/20; 5 concurrent promotions 5/5; full suite 32/32 (29 existing + 3 new regression)", "not_claimed": "end-to-end workflow liveness (needs qualifying .naya/capture/** push or manual dispatch)"}, "rule": "a shared registry's read-allocate-modify-write is one critical section: exclusive lock across all three phases (the allocation decision happens in the read) + atomic commit (temp + rename); a concurrency repair is proven only by a deterministic multi-writer repro that fails before and passes after"}
