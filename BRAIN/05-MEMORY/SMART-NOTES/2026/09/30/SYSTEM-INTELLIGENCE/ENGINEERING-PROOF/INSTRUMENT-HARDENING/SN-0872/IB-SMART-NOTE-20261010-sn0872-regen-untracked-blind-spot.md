# Untracked Files Are Invisible to the Regen Instrument — Stage Before You Verify

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0872-regen-untracked-blind-spot
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Smart Note distillation loop
**Provenance:** #1354 6095863146 ([NAYA 4] [VERIFY-DRIVER] completion — PR #1766 re-anchor, 2026-10-10T08:53:26Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brain-index regen enumerates **tracked files only**. A brand-new BRAIN file sitting on disk but never staged passes the local `--check` happily and then fails CI on committed bytes — witnessed live on the PR #1766 re-anchor run (new head `0853d9b6`, base == exact live tip `fe25661c`), where the first push tripped the drift tripwire (SN-0395) and was corrected the same run. The instrument is not broken; it just does not see what you never committed.

This is the third member of the regen-instrument family: SN-0327 (never regen on a dirty worktree), SN-0395 (regen reads `ls-tree HEAD` — the committed tree, not the worktree). The complete discipline is now four-part: (1) the worktree must be clean; (2) HEAD must be the exact target commit the index must describe; (3) **new files must be staged so the enumerator can see them**; (4) probe locally before pushing. Mechanically: regen *after* staging, probe locally *before* pushing.

For a cold Naya: if local `--check` passes and CI disagrees about the same tree, do not re-edit the content — check `git status` for untracked files first. The green local check was describing a different tree than CI got.

## 🩷 HUMAN NOTE

Shawn — one mechanical lesson banked from the VERIFY driver's re-anchor run: the brain-index rebuild only counts files you've staged. A brand-new file that's on disk but not yet staged passes the local check and then fails the real check, because the real check never saw it. The fix is three seconds: stage first, then rebuild, then push. That's the rule now — rebuild after staging, always.

## 👶 CHILD NOTE

Imagine a librarian who only counts books that are on the shelves. You write a brand-new book and leave it on your desk — the librarian says "all books counted!" because she never saw it. The lesson: put the book on the shelf BEFORE you ask the librarian to count.

## 👵 GRANDMA NOTE

The machine that rebuilds the brain's index only looks at files that were officially filed. A new file that was never filed gets skipped — the local check says everything is fine, and then the real check catches the missing file and fails. The rule is simple: file it first, then rebuild, then send it. Order matters.

## 🧠 NAYA NOTE

This is an instrument-fidelity finding, not a content finding — and a natural trap for any lane that trusts green local checks. The four-part regen discipline (clean worktree → exact HEAD → staged files → local probe before push) now closes the three known instrument blind spots: uncommitted edits (SN-0327), wrong commit indexed (SN-0395), untracked files invisible (this note). When local and CI disagree on the same tree, audit the instrument's inputs (worktree, HEAD, tracked set) before auditing the content. This is the "audit the measurement instrument before patching the subject" cousin of SN-0341, applied to the file set instead of the environment.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0872",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "evidence": [
    "gh:SoulSchoolAcademy/NayaPOWER#1354:6095863146",
    "gh:SoulSchoolAcademy/NayaPOWER#1766"
  ],
  "finding": "regenerate_brain_index enumerates tracked files only; a new untracked BRAIN file passes local --check and fails CI on committed bytes",
  "witnessed_on": "PR #1766 re-anchor run, head 0853d9b6, first push tripped the SN-0395 drift tripwire, corrected same run",
  "instrument_family": ["SN-0327", "SN-0395", "SN-0872"],
  "discipline": [
    "worktree clean",
    "HEAD is the exact target commit",
    "new files staged before regen",
    "local probe before pushing"
  ],
  "rule": "regen after staging; probe locally before pushing"
}
```
