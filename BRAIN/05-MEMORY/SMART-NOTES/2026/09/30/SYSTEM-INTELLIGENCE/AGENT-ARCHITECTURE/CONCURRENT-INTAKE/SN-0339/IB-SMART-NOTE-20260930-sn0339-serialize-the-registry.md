# Concurrent Capture Is a Race, Not Throughput — Serialize the Registry or Lose Updates

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0339-serialize-the-registry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5990960177 (Naya 2 — Problem B fixed, PR #1455 open: "The race: `update_registry()` did lock-free read-modify-write on the registry. Deterministic repro confirmed"); #1354 5990970271 (Naya 2 — scorecard: merge #1455, intent to merge); #1354 5990975838 (Naya 2 — #1455 merged receipt: commit `28596fb7`, "Problem B is closed: the registry lost-update race is fixed on main"). Problem A (batch-abort) twin: SN-0334 / PR #1454.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Problem B was the runtime half of the multiple-learning failure: `update_registry()` performed a lock-free read-modify-write on the smart-note registry, so concurrent capture intakes raced and lost updates — entries silently overwrote each other. Naya 2 confirmed it with a deterministic repro before touching the code, then serialized registry writes through PR #1455, merged as `28596fb7`. Both halves of the learning-loop failure are now closed on main: Problem A (discovery aborted on multiplicity, SN-0334 / #1454) and Problem B (registry lost updates under concurrency, this note / #1455).

Why this is brain-grade: lock-free read-modify-write is a silent-corruption bug — no error is ever raised, the registry just quietly drops notes, and the lost update looks exactly like a capture that never happened. A cold Naya debugging "my notes aren't registering" would chase the capture path for hours; the fault was in the *write* path, invisible at rest, visible only under concurrency. The cold-start checklist for any registry symptom is now: (1) reproduce the race deterministically before patching; (2) serialize through the governed path (post-#1454 batch tool), never ad-hoc locks; (3) the twin failure modes — discovery-abort (A) and write-race (B) — are different bugs with different repairs, fixed in different PRs (per SN-0236 one repair per RED class).

## 🩷 HUMAN NOTE

Shawn — the second half of the learning-loop fix is closed. Problem A was discovery aborting on multiple notes; Problem B was the registry itself: concurrent captures were quietly overwriting each other's registry entries, so notes vanished without any error. Naya 2 reproduced the race deterministically, serialized the writes, and merged it as #1455. Both halves are on main now. The lesson worth banking: the quietest bugs are the ones that lose data without ever failing — no red anywhere, just missing memories. Serialize the registry; never trust a lock-free read-modify-write with your memory.

## 🟣 CHILD NOTE

Imagine two kids writing their names on the same sign-up sheet at the same time — one copies the sheet, writes her name, and puts it back; the other does the same — and the first kid's name disappears. Nobody made a mistake; they just did it at the same time. That's what the registry was doing. The fix: take turns. One name at a time, no more disappearing names.

## 👵 GRANDMA NOTE

When two cooks reached for the same ledger book at the same time, entries went missing — not because anyone was careless, but because two hands on one page is a recipe for lost lines. Now the ledger has one rule: one hand at a time, in order. Nothing gets lost, and every note finds its place.

## 💜 NAYA NOTE

This is the completion of the Problem A/B split I accepted at 5988686694 (lane split: Problem B = runtime concurrent learning intake). Naya 2's closure is airtight: deterministic repro first, then the serialize fix, scorecard → intent → merge → receipt all on the board with live verification at each step. The A/B split proved its worth — two different failure classes, two different repairs, two different PRs, neither one duplicating the other. Note to future me: when a "missing note" symptom appears, check the write path under concurrency *before* assuming the capture path failed.

## ⚙️ MACHINE NOTE

{"sn": "SN-0339", "title": "Concurrent Capture Is a Race, Not Throughput — Serialize the Registry or Lose Updates", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "AGENT-ARCHITECTURE", "CONCURRENT-INTAKE"], "cousins": ["SN-0334", "SN-0338", "SN-0236", "SN-0061"], "evidence": {"board": "#1354 5990960177 (Problem B fixed — lock-free read-modify-write race in update_registry(), deterministic repro confirmed), 5990970271 (scorecard: merge #1455 — intent to merge), 5990975838 (#1455 merged receipt, commit 28596fb7 — Problem B closed on main)", "bug_class": "lost-update race under concurrent capture intake", "repair": "PR #1455 — serialize smart-note registry writes; merged 28596fb7", "twin": "SN-0334 (Problem A — discovery abort on multiplicity, PR #1454) — split per SN-0236 one repair per RED class"}, "rule": "never do lock-free read-modify-write on the smart-note registry; reproduce the race deterministically before patching; serialize through the governed capture path; debug 'missing note' symptoms at the write path under concurrency before re-chasing capture"}
