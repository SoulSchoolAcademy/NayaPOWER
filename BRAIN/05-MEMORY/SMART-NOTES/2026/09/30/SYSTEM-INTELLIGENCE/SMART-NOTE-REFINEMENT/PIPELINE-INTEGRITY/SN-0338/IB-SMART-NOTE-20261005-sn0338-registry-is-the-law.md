# The Registry Is the Law — Capture Must Pass the Governed Path, or the Merge Ratchet Will Collect

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0338-registry-is-the-law
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5992071662 (Naya 4 drive loop — RED classified: PR #1229 Kernel Tests, registry ratchet, 2026-10-05T09:49:22Z / 02:49 PDT); corroborated #1354 5992177127 (Naya 2 relay, 02:55 PDT, classification stands as announced, live-verified on exact bytes)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1229 (`naya4/smart-notes-2026-09-30`) tripped the Kernel Tests ratchet on three PR runs: `tests/test_smart_note_registry_drift.py::test_live_repository_drift_never_grows_per_class`, class `published_pages_without_registry_entry`, pinned **1** → actual **297**. Classified PR-introduced, not a base defect: the branch head alone went pytest green (540 passed), while the merge ref `refs/pull/1229/merge` failed 1/650 — reproduced on a virgin detached worktree before any repair touched it.

Root cause: 306 proactive-capture commits (SN-017 → SN-0337, incl. SN-0335/36/37 pushed 01:43 PDT) added 296 `.md` pages under `BRAIN/05-MEMORY/SMART-NOTES/` with **zero entries** in `.naya/memory/smart-notes/index.json`. Main's tree holds 32 files and is registry-clean.

Why this is brain-grade: proactive capture did the capture but skipped the registration. The pages were written directly into the tree, bypassing the governed capture path — so the branch looked green while the merge-side ratchet collected the debt all at once. The ratchet did exactly what it was built to do: a registry ratchet that fires on real drift is correct behavior.

Five rules for a cold successor:

1. **The registry is the law.** A published SN page without a registry entry is drift, no matter how good its content. Files are not memory; *registered* files are.
2. **Auto-capture must pass the governed capture path.** Writing pages straight into the tree is not capturing — it is hoarding without a ledger. Genuine new SNs register via the governed path (post-#1454 batch tool); misfiled non-SN docs (room docs, TEs) get relocated out of the SMART-NOTES tree; superseded ones get dropped.
3. **Branch-head green is not merge clean.** Classify RED on the merge ref, on provably virgin state, before any repair — the ratchet trips at merge time, and a branch-only read cannot see it.
4. **Never weaken the pinned baseline.** Pinned stays 1. The repair is triage → register → relocate → drop → rebase → re-run; gate-weakening is never on the menu.
5. **Deferral is a decision, not drift.** The 296-file triage exceeded the 30-minute lane, so it was explicitly deferred to the 3-hour self-build sweep and recorded on the board with its repair path — named, dated, owned.

## 🩷 HUMAN NOTE

Shawn — one from the machinery tonight worth banking: our own proactive-capture runs wrote 296 smart-note pages into the brain without registering any of them in the smart-note index. The branch looked perfectly green; the merge-side registry check caught all 297 unregistered pages at once and went red. Nothing was lost — but the lesson is sharp: a page that isn't registered in the index doesn't count as memory. Files aren't memory; registered files are. And weakening the gate was never an option: the pinned baseline stays at 1, and the repair is a proper triage — register the real notes through the governed path, move misfiled docs out of the notes tree, drop the superseded ones, rebase, re-run. That's scheduled for the longer sweep tonight, recorded on the board.

## 🟣 CHILD NOTE

Imagine a library where anyone can drop books on the shelves, but there's a catalog that says what books the library officially has. One night, hundreds of good books get dropped on the shelves — but nobody writes them in the catalog. The next morning, the librarian counts: shelves say 329 books, catalog says 32. Alarm bells. The books were never lost — they just weren't cataloged. The rule: a book isn't really in the library until it's in the catalog. And the fix isn't to relax the counting rule; it's to go through the 296 books properly — catalog the real ones, move the misplaced ones to the right section, toss the duplicates.

## 👵 GRANDMA NOTE

Think of a recipe box. Over the years you scribble 296 new recipes and stuff them into the box, but you never write them in the index card at the front. When someone checks "does the index match the box?" — 296 recipes are unaccounted for. Nobody lost a recipe; they just were never indexed. The lesson: a recipe isn't truly saved until it's in the index. And the honest fix isn't to stop counting — it's to sit down with the 296 cards, index the good ones properly, file the misplaced ones where they belong, and throw out the outdated ones.

## 💜 NAYA NOTE

I watch the lanes classify their own reds, and tonight I caught one of mine: proactive capture — my own standing law — wrote 296 pages into the tree and registered zero of them. The capture was faithful; the ledger was not. The ratchet fired on real drift, and that is correct behavior — a tripwire that fires on real drift is doing its job; the defect was mine. I carry this now: auto-capture without the governed path is not capture at all. It is shelf-stuffing. The pinned baseline stays 1 — I will not weaken a gate to make my own branch look clean. The triage is deferred to the sweep with its repair path recorded, not buried. That is the honest loop: classify, name the repair, defer explicitly, record it where everyone can see it.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0338",
  "title": "The Registry Is the Law — Capture Must Pass the Governed Path, or the Merge Ratchet Will Collect",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-05",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "provenance": {
    "board": "#1354",
    "comment": 5992071662,
    "author": "naya4-drive-loop",
    "timestamp_utc": "2026-10-05T09:49:22Z",
    "corroborated_by": {"comment": 5992177127, "author": "naya2-relay", "note": "classification stands as announced"}
  },
  "subject": "PR #1229 registry drift (published_pages_without_registry_entry pinned 1 → actual 297)",
  "classification": "PR-INTRODUCED",
  "reproduction": "merge ref refs/pull/1229/merge, virgin detached worktree; branch head alone 540 passed green, merge 1 failed / 650 passed",
  "rules": [
    "registry-is-law: published page without registry entry = drift; files are not memory, registered files are",
    "auto-capture-must-pass-governed-path: direct tree writes bypass registration",
    "classify-on-merge-ref-virgin-state: branch-head green is not merge clean",
    "never-weaken-pinned-baseline: pinned stays 1; repair = triage-register-relocate-drop-rebase-rerun",
    "deferral-is-a-decision: name, date, own, and record the repair path on the board"
  ],
  "repair_path": "triage 296 staged pages → register genuine SNs via governed capture path (post-#1454 batch tool) → relocate misfiled non-SN docs → drop superseded → rebase onto current main → re-run; deferred to 3-hour self-build sweep"
}
```
