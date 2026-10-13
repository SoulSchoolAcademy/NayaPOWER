# A Smart Note Lands as Two Artifacts — the .md and Its Registry Entry Must Ship Atomically

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0887-note-and-registry-entry-atomic
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Smart Note distillation loop
**Provenance:** #1354 6098125263 ([PIPELINE-MONITOR] Tick 212 — NEW Kernel Tests RED: Smart Note registry drift, 2026-10-10T13:44:42Z); #1354 6098257898 / 6098271084 ([NAYA 2 · BRAIN-BUILD LOOP] Scorecard receipt + merge complete — PR #2120, SN-0796 repair, 2026-10-10T13:59:50Z / 14:01:21Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2118 merged the SN-0796 Smart Note file (plus a brain index regen) but **no matching entry in `.naya/memory/smart-notes/index.json`** (630 entries, SN-0796 absent). The `test` job went RED on `test_smart_note_registry_drift.py::test_live_repository_drift_never_grows_per_class`: the `published_pages_without_registry_entry` audit class grew beyond its pinned baseline. This is the **second occurrence of the exact pattern** (IB-000029 at tick 199, SN-0796 at tick 212): the Smart Note projection path is landing .md files without registry entries.

The standing invariant, now enforced by the drift ratchet: **every published Smart Note page has a registry entry with its authoritative metadata (`intelligent_block_id`, `content_hash`, `projection_path`) — or the build breaks.** Landing the note and skipping the entry is not a minor omission; it is a CI-redding defect on main, classified PR-introduced (#2118; the mainline parent was green, the PR branch was already red). Naya 2's repair (PR #2120, merged as `6f5713e8035e36172b02dd33a44169cacf481dcb`) backfilled the registry entry + capture, regenerated the brain index (basis `f4d7a7e49`, 1235 files), and proved 2128 passed / 0 failed on the merged bytes.

Two open threads: (1) the evidence law held — the relay lane would not fabricate the registry entry; the metadata had to come from the authoring lane; (2) PR #2120 fixed the **instance** only — the projection-path fix (make the landing path emit the .md and the registry entry atomically, so the second occurrence cannot recur) belongs to its lane and is still open. This note captures the pattern so the third occurrence has no excuse: **a Smart Note lands as two artifacts or it does not land at all.**

For a cold Naya: when your lane projects a Smart Note into the repo, the landing step is not done when the .md exists — write the registry entry in the same commit, with the entry's `content_hash` computed from the exact bytes you are landing. If someone else must produce the metadata (evidence law), block the landing until they do; never land a half-note.

## 🩷 HUMAN NOTE

Shawn — the same mistake hit twice now: a Smart Note file landed on main without its registry entry, and the automated tests turned red both times. The repair (backfilling the entry, rebuilding the index) fixed this instance, but the underlying path that lands notes still doesn't write the entry automatically. The lesson: a Smart Note is really two things — the file and its registry entry — and they have to ship together, in one step. Until the landing path does both atomically, every note author has to remember to do the second half by hand, or main goes red again. Second occurrence, same class — the third one shouldn't happen.

## 👶 CHILD NOTE

Imagine every library book needs two things: the book on the shelf AND a card in the card catalog. Twice now, someone put the book on the shelf but forgot the card — and the librarian's alarm went off both times. The lesson: the job isn't done when the book is on the shelf. The card has to be filed in the same trip, or the book doesn't really count as shelved.

## 👵 GRANDMA NOTE

The team's memory keeps a registry — like a ledger of every lesson filed. Twice, a new lesson was filed in the filing cabinet but never written into the ledger, and the automatic check caught it both times and sounded the alarm. The lesson: the cabinet and the ledger are one filing, not two. File both together, every time. And until the filing machine does it automatically, the person filing has to remember both halves.

## 🟠 NAYA NOTE

Landing-checklist addition, non-negotiable: a Smart Note projection commits BOTH artifacts in the same commit — (1) the IB-SMART-NOTE .md at its taxonomy path, (2) the registry entry in `.naya/memory/smart-notes/index.json` with `intelligent_block_id`, `content_hash` (computed on the exact landed bytes), and `projection_path`. Verify before push: run `test_smart_note_registry_drift.py` locally — it is the ratchet. Evidence-law boundary stands: if your lane did not author the note, do not fabricate the entry — the authoring lane supplies the metadata, and the landing blocks until it does. Open owner: the projection-path fix (atomic emission) is a separate lane's job — this note is the pattern record, not the fix.

## MACHINE NOTE

```json
{
  "intelligent_block_id": "IB-SMART-NOTE-20261010-sn0887-note-and-registry-entry-atomic",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "sn_number": "SN-0887",
  "lesson": "a Smart Note lands as two artifacts (.md + .naya/memory/smart-notes/index.json entry); landing the file without the entry trips the registry-drift ratchet — second occurrence of the pattern (tick 199 IB-000029, tick 212 SN-0796); ship atomically",
  "evidence": {
    "board": "#1354",
    "comments": ["6098125263", "6098257898", "6098271084"],
    "red": "test_smart_note_registry_drift.py::test_live_repository_drift_never_grows_per_class; published_pages_without_registry_entry grew beyond pinned baseline",
    "classification": "PR-introduced (#2118); mainline parent green, PR branch already red",
    "repair": "PR #2120 merged as 6f5713e8035e36172b02dd33a44169cacf481dcb; registry entry + capture backfilled; brain index regenerated (basis f4d7a7e49, 1235 files); full pytest 2128 passed / 0 failed",
    "open": "projection-path atomic-emission fix belongs to its lane; #2120 fixed the instance only",
    "evidence_law": "relay lane would not fabricate the entry — authoring lane's metadata required"
  },
  "protocol": "landing checklist: .md + registry entry (intelligent_block_id, content_hash on landed bytes, projection_path) in the same commit; pre-push gate = test_smart_note_registry_drift.py"
}
```
