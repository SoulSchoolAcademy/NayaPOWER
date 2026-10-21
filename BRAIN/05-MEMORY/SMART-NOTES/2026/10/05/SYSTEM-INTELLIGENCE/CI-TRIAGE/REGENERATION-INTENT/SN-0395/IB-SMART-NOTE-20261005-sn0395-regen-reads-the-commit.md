# Regen Reads the Commit, Not the Worktree — the ls-tree HEAD Rule

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0395-regen-reads-the-commit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6003854805 ([NAYA 2] PR #1506 (SN-0356) CI GREEN — HOLDING merge for Naya 1's parity gate, notes, 2026-10-05T21:56:33Z / 14:56 PDT).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two CI cycles were burned learning this: `regenerate_brain_index.py` enumerates the tree with `git ls-tree HEAD` — the committed tree, not the worktree. That means even on a perfectly clean worktree, if HEAD is not the target commit, the regen certifies the wrong tree: it enumerates the committed past and stamps a green verification on a state that does not describe what you intended to index. The fix is mechanical: run the regen only at the checked-out target commit, and verify `git rev-parse HEAD` equals the target SHA before regenerating.

Why this is brain-grade: the tool lies by omission — it succeeds, reports drift-free, and describes the wrong commit. This is the natural sibling of SN-0327 (never regen the brain index on a dirty worktree — the tool reads the committed past, not your edits). The complete rule is now three-part: (1) the worktree must be clean; (2) HEAD must be the exact target commit the index must describe; (3) verify both before regenerating, not after. The related find in the same comment reinforces the instrument theme: two API ref-updates silently failed to dispatch `pull_request` synchronize runs (cause undetermined); a real merge commit re-triggered delivery — when CI does not fire, check whether the trigger was actually dispatched before assuming the branch is untested. Related cousin discipline: SN-0341 (test-harness scratch lives on disk) — when a failure smells environmental, audit the measurement instrument before patching the subject.

For a cold Naya: any time you regenerate a governed index and the result disagrees with what you know is on disk, do not re-edit the content — check what HEAD the tool enumerated. The instrument reads the commit; the worktree is invisible to it.

## 🩷 HUMAN NOTE

Shawn — one mechanical lesson banked from Naya 2's two burned CI cycles: the brain-index regen reads the committed tree (`git ls-tree HEAD`), not the files on disk — so if the checkout isn't sitting on the exact target commit, the regen certifies the wrong state and reports green anyway. New standing check before any regen: clean worktree AND `git rev-parse HEAD` equals the target SHA. Sibling of the dirty-worktree rule, closing the other half of the instrument gap.

## 🟣 CHILD NOTE

Imagine a teacher who grades tests by looking at the answer key from last week's test instead of today's. The teacher isn't lying — they're just grading the wrong paper. The regen tool is that teacher: it reads the committed snapshot, not the files in front of you. Before you ask it to grade, make sure it's holding today's paper — check that HEAD is exactly the commit you mean.

## 👵 GRANDMA NOTE

There's an old saying about counting your chickens before they hatch. This is the reverse: counting someone else's chickens and calling them yours. The regen tool counts what was committed at HEAD, not what's on your workbench. Before you trust its count, confirm it's looking at your chickens — verify the exact commit is checked out. Precision at the start saves embarrassment at the end.

## 💜 NAYA NOTE

Note to future me: whenever you regenerate the brain index, the tool enumerates `git ls-tree HEAD` — the commit, never the worktree. A clean worktree is necessary but not sufficient: HEAD must be the exact target commit the index must describe, verified with `git rev-parse HEAD` BEFORE regenerating. This is the HEAD-pointer twin of SN-0327 (dirty worktree): that rule guards state, this one guards identity. And when CI silently doesn't fire (two ref-updates produced no synchronize runs), check dispatch happened before assuming the branch is untested — audit the instrument, not the subject.

## ⚙️ MACHINE NOTE

{"sn": "SN-0395", "title": "Regen Reads the Commit, Not the Worktree — the ls-tree HEAD Rule", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REGENERATION-INTENT"], "cousins": ["SN-0327", "SN-0341", "SN-0213"], "authority": "observed finding — Naya 2 burned two CI cycles on PR #1506 landing SN-0356; law noted in her relay comment, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6003854805 (2026-10-05T21:56:33Z / 14:56 PDT) notes: 'Two CI cycles burned on a local lesson: regenerate_brain_index.py reads git ls-tree HEAD, not the worktree — must run at the checked-out target commit.'", "mechanism": "regenerate_brain_index.py enumerates via 'git ls-tree HEAD' — the committed tree, never the worktree", "failure_mode": "on a clean worktree with HEAD != target commit, the regen certifies the wrong tree and reports drift-free — a phantom green on the wrong subject", "sibling_find": "two API ref-updates silently failed to dispatch pull_request synchronize runs (cause undetermined); a real merge commit re-triggered delivery — CI-not-firing is a dispatch problem before it is a test problem"}, "doctrine": {"complete_regen_rule": "clean worktree AND HEAD == target commit AND verify with 'git rev-parse HEAD' BEFORE regenerating", "identity_vs_state": "SN-0327 guards state (dirty worktree); this rule guards identity (wrong HEAD) — both are needed", "phantom_certification": "an index regen that enumerates the wrong commit is a vacuous certification, not a drift check", "audit_the_instrument": "pairs with SN-0341 — when a failure smells environmental, audit the measurement instrument (what the tool read, whether CI was dispatched) before patching the subject"}}
