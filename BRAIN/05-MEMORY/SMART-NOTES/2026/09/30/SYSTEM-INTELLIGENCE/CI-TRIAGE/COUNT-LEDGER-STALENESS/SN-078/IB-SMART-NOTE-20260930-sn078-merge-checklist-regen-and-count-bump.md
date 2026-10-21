# Merge Adding BRAIN/ Files Must Regen the Index AND Deliberately Bump the Count Ledger — Bake It into Merge Checklists

**Intelligent Block:** IB-SMART-NOTE-20260930-sn078-merge-checklist-regen-and-count-bump
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5936359525 (Naya 2 brain-build loop — battery on new main tip, RED found + repaired, PR #1251, 2026-10-01T17:00:26Z). Extends SN-062 (count ledger is part of the change).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Main moved `a726a837` → `42c8f594` (4 commits landing the AutoResearch harness Smart-Note lessons). Naya 2's brain-build loop ran its battery on the exact new tip: pytest green (545 passed / 3 skipped) — but `tools/regenerate_brain_index.py --check` was **RED on main itself**. The merge had added a `BRAIN/` file without the two deliberate companion actions: (1) regenerating the index artifacts (`BRAIN/NAYAPOWER-BRAIN-INDEX.json`, `REAL-TREE.json`, `REAL-TREE.md` were all stale vs regenerated output), and (2) deliberately bumping `EXPECTED_DOMAIN_COUNTS` for the touched domain (`05-MEMORY` git=21 vs ledger=20). Repaired, not merged: PR #1251 (commits `e94b1d57` deliberate 20→21 bump + `66ba0843` regenerated 3 index artifacts; `--check` OK on 164 files, pytest 545/545; no self-merge — Shawn's gate). The durable lesson, and the reason this is a new note rather than a footnote on SN-062: SN-062 diagnosed the count-ledger discipline on a draft branch; this is the **recurrence on main itself through the merge path** — a merge can carry the red onto the canonical branch while every test stays green, because `--check` is not part of the test suite. Two standing rules fall out: **(a) any merge adding a `BRAIN/` file must regen the index AND deliberately bump `EXPECTED_DOMAIN_COUNTS`** — the tool's own `--check` failure message prescribes the repair, so the repair is never a judgment call; **(b) bake it into merge checklists** — Naya 2's explicit ask — because a rule that lives only in one lane's memory will be re-broken by the next lane's merge. The green-test/red-check split is the signature: when the test suite and the index check disagree, the check is telling you the merge was incomplete, not that the check is wrong.

## 🩷 HUMAN NOTE

It's like a library that adds a new wing of books: the books are all there (every test passes — the books exist and are fine), but nobody updated the card catalog or the "we now have 21 sections" sign on the door. Visitors using the catalog can't find the new wing. The merge added the books and skipped the catalog — twice now: once on a branch (SN-062), once on main itself. The fix isn't clever: update the catalog and the sign every time you add a wing, and put "update the catalog and the sign" on the moving-day checklist so no crew can forget it. The tool even tells you what's wrong when you run its check — the repair instructions are printed on the failure itself.

## 🟣 CHILD NOTE

Imagine your classroom gets a new bookshelf full of books. The books are great! But the shelf list on the wall still says "20 shelves" and the library map doesn't show the new one. Your friends can't find the new books even though they're right there. The rule is simple: every time you add a shelf, you MUST update the map AND change the number on the wall — no exceptions, and it's written on the moving-day checklist so nobody forgets. The checker tool even tells you exactly what to fix when you forget. Books without a map are almost the same as no books at all.

## 🔵 GRANDMA NOTE

It's like adding a new room to the house but never updating the address list or the house number plaque. The room exists, it's lovely — but the mail carrier and the guests can't find it. You wouldn't call the house "complete" with guests wandering the yard. So the family rule: any renovation updates the directory and the count, and it's on the contractor's checklist, not left to memory. The second time it happened — on the main house itself, not just the garden shed — is what turned a reminder into a rule.

## 🟠 NAYA NOTE

Apply this to every merge touching indexed content: (1) treat the count ledger (`EXPECTED_DOMAIN_COUNTS`) and the regenerated index artifacts as **part of the change**, not follow-up chores — a merge that adds indexed files without them is an incomplete merge, even with a green suite; (2) the signature to watch for is green-tests/red-check: `pytest` green plus `regenerate_brain_index.py --check` red means the merge was incomplete — trust the check, not the suite, for index completeness; (3) the repair is prescribed by the tool's own message (deliberate bump + regen) — never improvise a different fix; (4) bake the regen+bump step into the merge checklist as a named item so every lane's merge crew executes it — a rule in one lane's memory will be re-broken by the next lane; (5) Naya 2's PR #1251 is the model repair: deliberate bump commit separate from regen commit, byte-verified 4/4, exact-branch-head `--check` OK, pytest full suite green, no self-merge — repair and merge authorization stay separated (Shawn's gate).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "incomplete_indexed_merge",
  "evidence": {
    "board": "#554 comment 5936359525 (2026-10-01T17:00:26Z) — Naya 2 brain-build loop, battery on new main tip 42c8f594",
    "red_on_main": "tools/regenerate_brain_index.py --check RED on main itself: deliberate ledger mismatch (05-MEMORY git=21 vs ledger=20); BRAIN/NAYAPOWER-BRAIN-INDEX.json, REAL-TREE.json, REAL-TREE.md all stale vs regenerated output",
    "green_suite": "pytest 545 passed / 3 skipped on exact tip — the test suite does not cover index completeness",
    "repair": "PR #1251 (draft, no self-merge): e94b1d57 deliberate 05-MEMORY 20->21 bump + 66ba0843 regenerated 3 index artifacts; --check OK (164 files); pytest 545/545 on exact branch head; byte-verified 4/4",
    "extends": "SN-062 (count ledger is part of the change — draft-branch instance); this is the recurrence through the merge path onto main itself"
  },
  "rule": [
    "any merge adding a BRAIN/ file must regen the index AND deliberately bump EXPECTED_DOMAIN_COUNTS — both are part of the change",
    "green-tests/red-check means the merge was incomplete — trust the check for index completeness",
    "the tool's own --check failure message prescribes the repair — never improvise a different fix",
    "bake regen+bump into the merge checklist as a named item — a rule in one lane's memory will be re-broken by the next lane",
    "repair and merge authorization stay separated — the repair PR does not self-merge"
  ],
  "lesson_line": "A merge that adds indexed files without regenerating the index and deliberately bumping the count ledger is an incomplete merge — green tests don't cover the catalog, so bake regen+bump into the merge checklist."
}
~~~
