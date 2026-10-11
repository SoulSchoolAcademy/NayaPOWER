# The Shallow-Clone Landmine: Check `.git/shallow` Before Trusting Range Math

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0718-shallow-clone-range-math-landmine
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6068954760 (Naya 5 hourly report, 2026-10-08T21:00:04Z; src: `learn-builder-20261008-2045`) — SoulSchoolAcademy

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During a 2026-10-08 learning-lane rebase, the builder discovered that `~/workspace/nayapower-work` was a **shallow clone** — `.git/shallow` boundary markers sitting right at the tip. The first rebase attempt generated a **169-commit garbage todo** and, for a brief alarming window, it looked like **main's history had been rewritten**. The cause was not a force-push war, not a corrupted remote, not another lane's `git gc` — it was the clone itself: shallow boundaries silently corrupt merge-base/rebase range math. Nothing announced the problem; the todo list just looked insane.

Why this is brain-grade: the failure mode is *silent*, not loud. Shallow clones don't refuse range operations — they *answer* them with wrong history boundaries, and the wrong answer looks like a repository disaster (rewritten main history), which triggers the expensive misdiagnosis path (chasing force-pushes, auditing other lanes) instead of the cheap one (checking the clone's depth). Every range-based operation — `git rebase`, `git merge-base`, cherry-pick ranges, `git log A..B`, any mechanical verifier with local-object preconditions — inherits the corruption. A cold successor who inherits a worktree or a loop-local clone cannot know from the working tree whether history is whole. The check is one line and must come first.

Rule for a cold successor: **before any range-based git operation in a worktree you did not create yourself, check for `.git/shallow`** (or `git rev-parse --is-shallow-repository`). If it's shallow, either deepen it or move the operation to a full clone. Never diagnose "main's history was rewritten" from a todo list generated in a shallow clone — the shallow clone fabricates exactly that appearance. This is the quietest member of the instrument-lies family: SN-0341 (harness lies about disk), SN-0429 (branch pin lies about the tool), and now SN-0718 — the clone lies about history.

## 🩷 HUMAN NOTE

Shawn — a sharp little landmine from the learning lane tonight, worth keeping. A builder ran a rebase in a shallow clone (`~/workspace/nayapower-work`) and got a 169-commit garbage todo that briefly looked like main's history had been rewritten. It wasn't another lane and it wasn't a force-push — the shallow clone silently corrupts merge-base and rebase range math. New standing rule: before any rebase/merge-base/range operation in a worktree you didn't create, check `.git/shallow` first. One line, and it saves chasing a phantom rewrite.

## 🟣 CHILD NOTE

Imagine you have a history book, but someone secretly tore out the middle pages and stapled the cover to the last chapter. Now you try to read "everything between page 10 and page 50" — and the book just makes things up, because the pages don't exist. That's a shallow clone: it looks like it has all the history, but it doesn't, and git happily gives you wrong answers instead of saying "I don't know." The lesson: always peek inside the book first — check for `.git/shallow` — before you trust what git tells you about history.

## 👵 GRANDMA NOTE

The team nearly thought someone had rewritten the project's history tonight — the computer produced a list of 169 changes that made no sense. Turns out the computer wasn't lying exactly; it was working from an incomplete copy of the files that *looked* complete. The new rule is simple: before trusting anything about the project's history, first verify you have the full copy, not a shortcut one. A shortcut copy gives confident wrong answers, which is worse than saying "I don't know."

## 🟣 NAYA NOTE

I treat every worktree as suspect until proven full. Range math (rebase, merge-base, `A..B`) only runs where `git rev-parse --is-shallow-repository` says false. If a rebase todo looks impossible — hundreds of commits that don't belong — I check `.git/shallow` before I check the network, other lanes, or the remote. A shallow clone fabricates the exact appearance of rewritten history; the misdiagnosis costs an hour, the check costs a second. The instrument family keeps growing: the harness, the checkout, the pinned tool — and now the clone itself.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0718",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/INSTRUMENT-PARITY",
  "doctrine": "shallow-clone-range-math-landmine",
  "rule": "Before any range-based git operation (rebase, merge-base, cherry-pick range, A..B log) in a worktree you did not create, check .git/shallow (or git rev-parse --is-shallow-repository). Shallow boundaries silently corrupt range math and fabricate the appearance of rewritten history.",
  "failure_mode": "169-commit garbage rebase todo; phantom 'main history rewritten' scare; expensive misdiagnosis of other lanes instead of the one-line depth check",
  "cousins": ["SN-0341", "SN-0429", "SN-0327"],
  "evidence": [
    "#1354 comment 6068954760 (Naya 5 hourly report, 2026-10-08T21:00:04Z) — 'SN-0575 fix: shallow-clone landmine. ~/workspace/nayapower-work was shallow (.git/shallow boundaries at tip) → silently corrupts merge-base/rebase range math (first rebase attempt generated a 169-commit garbage todo; briefly looked like main's history had been rewritten…' (src: learn-builder-20261008-2045)",
    "No existing Smart Note on shallow-clone depth checks (grep of staged notes tree, 2026-10-08)"
  ]
}
