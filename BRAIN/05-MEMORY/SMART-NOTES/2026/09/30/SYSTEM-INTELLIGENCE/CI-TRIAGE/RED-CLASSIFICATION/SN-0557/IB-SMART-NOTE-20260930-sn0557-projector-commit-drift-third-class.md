# Projector Commits Are a Third Brain-Index Drift Class — CI-Masked Until the Next Push

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0557-projector-commit-drift-third-class
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6043039900 ([DRIVE-LOOP] Latent brain-index drift on `d53d7547` — classified, repair PR #1747 offered, 2026-10-07T17:18:57Z); repair PR #1747 (branch `naya4/drive-loop/regen-brain-index-d53d7547`); independent second-seat ack #1354 6043164150

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The smart-note projection commit `d53d7547` added the SN-0525 note file without regenerating the brain index layer — `BRAIN/NAYAPOWER-BRAIN-INDEX.json`, `BRAIN/REAL-TREE.json`, `BRAIN/REAL-TREE.md` enumerated 234 files against a 235-file tree. No push CI ran on that commit, so the drift is **CI-masked**: the next push CI would go RED on the drift step. SN-0240 taught us to classify every CI red as PR-introduced or base-inherited. This note adds the **third class: projector-commit-introduced** — a projection/landing commit that adds content files without running the index regen (the SN-0213 rule: the regen lives in the producer's landing step), silently taking the index out of sync with the tree.

Why this is brain-grade and genuinely new: the drive loop reproduced it on virgin state, not inference — `tools/regenerate_brain_index.py --check` on a clean virgin worktree at exact `d53d7547` reports DRIFT on all three files; base control on `7aabf0d4` with the same instrument reports OK (234 files), matching CI's earlier green verdict — so the drift was introduced by the projector commit itself. The regen diff is minimal and exact: 234→235 files, basis `d53d7547`, SN-0525 entry added with blob SHA verified against `git hash-object` (`1d74b1e0df9a46e2bd1bb5727832a6eaff58164f`, 6563 bytes), CRLF endings preserved to match the committed files; post-regen `--check` OK (235 files). The heal is mechanical, not semantic: PR #1747 touches only the three generated files (16+/10−), mergeable True — and the drive loop did *not* merge it; the merge decision is the director's / owning lane's under the Scorecard Law.

## 🩷 HUMAN NOTE

Shawn — a new defect class for the board, caught before it ever broke a build. A projection commit quietly added a Smart Note without regenerating the brain index, so the index said 234 files while the tree had 235. Because no CI ran on that commit, nothing flagged it — it was invisible until a drive-loop check ran the exact same instrument on the exact tip against a clean base control. The fix is a pure mechanical regeneration (three generated files, no meaning changes). The standing rule: any commit that adds content files without regenerating the index is a drift source of its own class — neither "the PR broke it" nor "it was already broken" — and it gets classified on virgin-state evidence before anyone heals it.

## 🟣 CHILD NOTE

Imagine you have a toy chest and a list of everything inside. You drop in a new toy but forget to write it on the list — the list is wrong now, but nobody noticed because nobody re-counted the chest. The lesson: there's a difference between "the list was already wrong" and "the list was right until *you* added a toy without updating it." Both look the same at the end — but fixing them needs different care, so you have to name which one happened.

## 👵 GRANDMA NOTE

A library's card catalog says 234 books, but the shelves hold 235 — because someone shelved a new book and skipped filing its card. The catalog wasn't wrong before, and the book isn't a bad book; it's a filing step that got skipped. The fix is simple: file the missing card, exactly as the shelf shows. But you can only say it was a filing step — and not a catalog problem — after you've gone to the shelf yourself and counted.

## 🧠 NAYA NOTE

Cold successor: extend the SN-0240 classification triage with the third class. (1) On any brain-index drift, classify BEFORE healing: PR-introduced (the PR's own diff broke the index) / base-inherited (the drift predates the PR, base control shows the same DRIFT) / **projector-commit-introduced** (a projection/landing commit added content files without the regen; base control OK, commit shows DRIFT). (2) Reproduce on virgin state with the same instrument CI uses (`regenerate_brain_index.py --check` on a clean worktree at the exact SHA — SN-0233 phantom-green discipline); the base control must be the parent of the suspect commit. (3) Projector-commit drift heals by mechanical regen only: verify the regen's basis, blob SHA via `git hash-object`, byte count, and line-ending preservation before landing it — no semantic edits are allowed in a regen. (4) Never merge the repair yourself on a drive-loop discovery — offer it (here: PR #1747) and name the merge decision's owner; the tripwire firing RED on real drift is the design working (SN-0240), not an incident. (5) Template: drive-loop comment 6043039900 — virgin-state finding, base control, minimal exact regen diff, repair PR offered with scorecard-ready falsifiers.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0557",
  "title": "Projector Commits Are a Third Brain-Index Drift Class — CI-Masked Until the Next Push",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "RED-CLASSIFICATION"],
  "cousins": ["SN-0213", "SN-0240", "SN-0233"],
  "evidence": {
    "board": ["#1354 6043039900 ([DRIVE-LOOP] Latent brain-index drift on d53d7547 — classified, repair PR #1747 offered, 2026-10-07T17:18:57Z)"],
    "virgin_read": "tools/regenerate_brain_index.py --check on clean virgin worktree at exact d53d7547: DRIFT (all three files); base control 7aabf0d4 same instrument: OK (234 files) — drift introduced by the projector commit itself",
    "regen_diff": "234->235 files, basis d53d7547; SN-0525 entry blob SHA 1d74b1e0df9a46e2bd1bb5727832a6eaff58164f verified against git hash-object (6563 bytes); CRLF endings preserved; post-regen --check OK (235 files)",
    "masking": "no push CI ran on d53d7547 — the drift is CI-masked; the next push CI would go RED on the drift step",
    "repair": "PR #1747 (branch naya4/drive-loop/regen-brain-index-d53d7547, 3 files, 16+/10-, mergeable True) — mechanical regen only; independently acked at #1354 6043164150; merge decision owned by director / owning lane, not merged by the drive loop"
  },
  "doctrine": {
    "three_classes": "PR-introduced / base-inherited (SN-0240) / projector-commit-introduced — classify every drift on virgin-state evidence before healing",
    "masking": "a commit with no push CI can carry CI-masked drift; the tripwire only fires on the next CI run — probe projector commits directly",
    "heal": "projector-commit drift heals by mechanical regen only, with basis + blob-SHA + byte-count + line-ending verification — never semantic repair",
    "ownership": "the discoverer offers the repair and names the merge owner; never merges a drive-loop discovery unilaterally"
  },
  "rule": "whenever a projection/landing commit adds content files, classify any resulting index drift as projector-commit-introduced on virgin-state evidence (base control OK + commit DRIFT) and heal it by verified mechanical regen — the regen lives in the producer's landing step (SN-0213), and the tripwire firing on real drift is correct behavior (SN-0240)"
}
```
