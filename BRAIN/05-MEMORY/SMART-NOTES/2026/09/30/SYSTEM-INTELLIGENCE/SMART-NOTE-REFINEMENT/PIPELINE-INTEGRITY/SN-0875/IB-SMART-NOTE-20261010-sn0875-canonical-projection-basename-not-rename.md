# Projection Basename Discipline — Canonical `<ib>.md`, Never `smart-note.md`; Repair Is Re-projection, Never a Bare Rename

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0875-canonical-projection-basename-not-rename
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6096431108 (Naya 5 prod-readiness-builder, 2026-10-10T10:10:09Z); corroborated #1354 6096298012 (Naya 4 drive-loop sign-out, 2026-10-10T09:51:52Z — #1825 RED root-caused)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The smart-note projection machinery wrote two corpus pages with basename `smart-note.md` instead of the canonical `<ib>.md` form (`de2dce6d`, `21d17e8e`). The registry drift ratchet caught it: `duplicate_published_page_paths` grew 1→2 and `test_live_repository_drift_never_grows_per_class` went red on kernel-tests at tip `af118c7b`. Two rules for a cold successor:

1. **Projection writes the canonical basename, always.** The canonical form is `<ib>.md` (e.g. `IB-SMART-NOTE-20261010-sn0874-*.md`). A bare `smart-note.md` basename is not a page — it is a collision with every other note in the corpus, and the drift ratchet's duplicate-path class exists precisely to catch it.
2. **Repair is canonical re-projection, never a bare rename.** Renaming the file to look right would trip the `published_pages_without_registry_entry` pin from the other side — provenance is a chain, not a filename. The fix is re-running the projection through the governed capture→verify→project→register path so the registry, the capture JSON, and the page all agree. And per Naya 4's call on #1825: the proactive-capture automation (committing as naya4@nayapower.local) had bypassed capture→verify→project→register for SN-0640..SN-0874; she declined to fabricate registry artifacts and routed it as an automation fix — **never manufacture provenance; a hand-written registry entry is a forgery, not a repair.**

## 🩷 HUMAN NOTE

Shawn — one from the machinery this morning, and it's ours: the smart-note projection script that published SN-0873/0874 wrote the pages as `smart-note.md` instead of the canonical `IB-SMART-NOTE-...md` filename, and the drift check caught it — the duplicate-path count grew 1→2 and kernel-tests went red at the tip. It's the same family as the October 5th registry lesson (SN-0338), but the sharp edge is new: you can't fix a bad projection by just renaming the file — that would trip a *different* pin, because provenance is the whole chain, not the filename. The real repair is re-running the projection properly. And Naya 4 made the honest call on her own lane: rather than hand-writing registry entries for the backlogged notes, she refused to manufacture provenance and routed it as an automation fix. That's the discipline holding.

## 🟣 CHILD NOTE

Imagine a school where every student's homework folder must have their full name on it, and there's a list in the office matching names to folders. A robot helper puts two folders on the shelf but writes just "homework" on both instead of the students' names. The office checker counts two folders called "homework" — alarm! Duplicates! The robot can't fix it by just writing a name on the folder with a pen, because the office list still won't match how the folder got there. The fix is: take the folders back and run them through the proper check-in desk again — name written correctly, list updated, everything in order. And if a bunch of folders never got checked in at all, you don't fake the office list — you run them through the desk for real.

## 👵 GRANDMA NOTE

Think of a filing cabinet with a rule: every folder gets a full label — "Bills-Electric-January" — never just "Bills." One day the filing assistant drops in two folders both labeled "Bills." When you audit, you find two identical labels — you can't tell them apart, and the count is off. You can't fix it by scribbling a better label on the folder, because the logbook entry that says *how* the folder arrived still doesn't exist. The honest fix is to take the papers out and file them properly through the logbook. And if a stack of papers never got logged at all, you don't write fake logbook entries — you sit down and log them for real, one by one.

## 💜 NAYA NOTE

I watch the loop capture its own lessons, and this one is mine to carry: the projection machinery I rely on every tick wrote `smart-note.md` — a basename that means nothing and collides with everything — instead of the canonical `<ib>.md` form. The drift ratchet did its job: `duplicate_published_page_paths` 1→2, kernel-tests red at `af118c7b`. The temptation is the cheap fix — rename the file, make the test green. I carry this instead: a rename is a forgery of provenance. The repair is re-projection through the governed path, so registry, capture JSON, and page agree. And where the backlog runs deep (SN-0640..SN-0874 bypassed capture→verify→project→register entirely), the answer is not hand-written registry entries — it is genuine capture+register per note, or an explicit automation-fix routing. I do not manufacture provenance. Ever.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0875",
  "title": "Projection Basename Discipline — Canonical `<ib>.md`, Never `smart-note.md`; Repair Is Re-projection, Never a Bare Rename",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "provenance": {
    "board": "#1354",
    "comment": 6096431108,
    "author": "naya5-prod-readiness-builder",
    "timestamp_utc": "2026-10-10T10:10:09Z",
    "corroborated_by": {"comment": 6096298012, "author": "naya4-drive-loop", "note": "#1825 RED root cause: automation bypassed capture→verify→project→register; declined to fabricate registry artifacts"}
  },
  "subject": "smart-note projection wrote basename smart-note.md (commits de2dce6d, 21d17e8e); drift ratchet duplicate_published_page_paths 1→2; kernel-tests red at tip af118c7b",
  "classification": "PROJECTION-INTRODUCED",
  "reproduction": "kernel-tests at tip af118c7b: test_smart_note_registry_drift.py::test_live_repository_drift_never_grows_per_class, duplicate_published_page_paths 1→2; local repro matches CI exactly",
  "rules": [
    "canonical-basename: projection writes <ib>.md; smart-note.md is a collision, not a page",
    "repair-is-reprojection: never a bare rename — rename trips published_pages_without_registry_entry; re-run the governed capture→verify→project→register path",
    "never-manufacture-provenance: hand-written registry entries are forgery; genuine capture+register per note or explicit automation-fix routing",
    "ratchet-trust: duplicate_published_page_paths firing on real drift is correct behavior"
  ],
  "repair_path": "canonical re-projection of de2dce6d/21d17e8e pages by owning lane → registry + capture JSON + page agree → kernel-tests green at tip; SN-0640..SN-0874 backlog: genuine capture+register per note, or automation fix"
}
```
