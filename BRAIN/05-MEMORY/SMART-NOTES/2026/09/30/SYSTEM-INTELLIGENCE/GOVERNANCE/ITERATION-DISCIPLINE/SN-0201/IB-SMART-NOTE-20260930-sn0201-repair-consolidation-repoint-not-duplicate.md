# Repair Consolidation: Re-Point the Stale Repair, Never Duplicate It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0201-repair-consolidation-repoint-not-duplicate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5955721777 (brain-build loop battery, 2026-10-02 15:32:07Z): `brain index --check` RED on main tip `5eaec742` (05-MEMORY git=29 vs ledger=23 — six non-report Smart Notes SN-018×2, SN-019, SN-020, SN-021, SN-022 landed 2026-10-01/02 via the governed publisher without the deliberate ledger bump); "No duplicate repair opened (repair-consolidation law: one open repair per RED class; #1251/#1301/#1314/#1315 already closed as superseded; verified no other open repair of this class)"; canonical repair PR #1312 re-pointed to current main — commit `0b3053c3` (parent `5eaec742`): deliberate 21→27 baseline + regenerated index artifacts; verification on exact bytes: `--check` OK (172 files), pytest 546 passed / 3 skipped / 0 failures, 4/4 files byte-verified; receipt at #1312 comment 5955707994; tip-move disclosure: main advanced `5eaec742` → `f4a24ef6` (docs-only, inert over BRAIN/tests/tools) during the re-point — evidence stands. Merge is Shawn's gate.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When the battery finds RED and an open repair of that RED class already exists, you do not open a second repair — you re-point the existing one to current main. The 05-MEMORY index battery went RED on `5eaec742`: six Smart Notes had landed through the governed publisher without the deliberate ledger bump (git=29 vs ledger=23). Instead of opening repair #5 for the same class, the loop verified the older repair PRs were closed-as-superseded, then re-pointed canonical PR #1312 to the current tip (`0b3053c3`, parent `5eaec742`) and re-ran the full verification on the exact new bytes — 172-file `--check` OK, 546 tests green, 4/4 files byte-verified. Because main advanced mid-repair, the loop disclosed the tip move and its materiality explicitly: `5eaec742` → `f4a24ef6`, docs-only, inert over BRAIN/tests/tools — evidence stands. That disclosure is the load-bearing part of the protocol: a re-point without a materiality statement asks the judge to trust a moving target.

Why this is brain-grade: the repair-consolidation law (one open repair per RED class) is the standing defense against repair-proliferation — five competing repairs of the same drift, each verified against a different base, each claiming the fix. Re-pointing also carries the root finding: the RED class was caused by the governed publisher landing content without performing the deliberate ledger bump — every governed writer that lands content owns its ledger step at land time; the battery is the catcher, not the fixer. And the tip-move disclosure rule generalizes: whenever you verify bytes and the base moves mid-verification, name the move and argue materiality, or the verification is void.

## 🩷 HUMAN NOTE

Shawn — a quiet win from the index battery: it caught the 05-MEMORY index RED (six published notes without the ledger bump) and, instead of opening yet another repair, re-pointed the existing repair PR #1312 to current main, re-verified the exact bytes, and disclosed that main moved mid-repair (docs-only, inert — evidence stands). The brain lesson: one open repair per RED class; when the base moves under your verification, you name the move and its materiality, or the proof doesn't count. And the root cause goes in the ledger at land time — the battery catches, it shouldn't have to fix.

## 🟣 CHILD NOTE

If you find a broken toy and someone is already fixing it, you don't start a second fixing station — you help them with theirs. And if you measured the broken piece but the toy wiggled while you measured, you say "it wiggled this much, and the wiggle doesn't change the measurement" — otherwise nobody knows if your measuring still counts.

## 👵 GRANDMA NOTE

When the checking tool found the index out of date, the builder didn't open a new repair ticket for a problem already being repaired — she moved the existing repair to the latest state and re-tested everything exactly. And when the ground shifted mid-repair, she wrote down exactly how it moved and why the tests still count. The lesson: one repair per problem; re-verify after every move; disclose every movement with an honest statement of whether it matters.

## 🤖 NAYA NOTE

Repair-consolidation law: one open repair per RED class — a stale repair PR is re-pointed to current main, never duplicated; superseded repairs close as superseded. Re-point verification runs on the exact new bytes (full battery + tests + byte-verified artifacts). If the base moves mid-verification, disclose the tip move and argue materiality explicitly — without that statement, the verification is void. Governed writers perform their ledger step at land time; the battery is the catcher, not the fixer.

## ⚙️ MACHINE NOTE

{"sn": "SN-0201", "title": "Repair Consolidation: Re-Point the Stale Repair, Never Duplicate It", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "ITERATION-DISCIPLINE"], "extends": ["SN-0079"], "evidence": {"red": "brain index --check RED on main tip 5eaec742: 05-MEMORY git=29 vs ledger=23; six non-report Smart Notes (SN-018x2, SN-019, SN-020, SN-021, SN-022) landed 2026-10-01/02 via governed publisher without deliberate ledger bump", "consolidation": "#554 5955721777: no duplicate repair opened; #1251/#1301/#1314/#1315 closed as superseded; canonical PR #1312 re-pointed (0b3053c3, parent 5eaec742): 21->27 baseline + regenerated index artifacts; --check OK (172 files), pytest 546/3/0, 4/4 byte-verified; receipt #1312 comment 5955707994", "tip_move_disclosure": "main advanced 5eaec742 -> f4a24ef6 (docs-only, inert over BRAIN/tests/tools) during re-point — evidence stands"}, "rule": "one open repair per RED class; re-point, never duplicate; re-verify exact new bytes; disclose tip moves with materiality argument; ledger step happens at land time"}
