# The Count Ledger Is Part of the Change

**Intelligent Block:** IB-SMART-NOTE-20260930-sn062-count-ledger-is-part-of-the-change
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5933379398 (Naya-2, 2026-10-01T14:19:39Z) — #1239 stale-index CI failure diagnosed and repaired; commit aa06f6cd on brain-build/sn053-collective-chain-first-test.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The SN-053 Smart Note added one file under `BRAIN/05-MEMORY` (21 files on disk), but the reconciliation ledger in `tools/regenerate_brain_index.py` still pinned `EXPECTED_DOMAIN_COUNTS['05-MEMORY']` at 20. The `--check` gate therefore failed with exit 2 in CI's `test` job — and it looked like a regression, but it wasn't one: the ledger was stale relative to a real, deliberate BRAIN/ change. The diagnosis was reproduced locally on the exact bytes (`02d65636`); the repair was deliberate, not mechanical: update `EXPECTED_DOMAIN_COUNTS` per the tool's own guidance (05-MEMORY 20→21, comment updated), regenerate the index layers (`NAYAPOWER-BRAIN-INDEX.json`, `REAL-TREE.json`, `REAL-TREE.md`), then verify on the exact pushed bytes (`--check` PASS over 164 files, `node --test` 0 fail, pytest 545 passed / 3 skipped). The lesson: wherever a `--check`-style gate compares declared counts against actual content, the count declaration is not metadata — it is part of the change. Any commit that adds or removes files under a counted domain must update the count ledger in the same commit. A stale pin turns a deliberate content change into a CI failure that reads as a code regression, wasting a triage cycle and eroding trust in the gate.

## 🩷 HUMAN NOTE

You add a bedroom to your house and update the blueprints — but forget to update the insurance declaration that says "4 bedrooms." The inspector arrives, counts 5, and flags your property as non-compliant. Nothing is wrong with the new bedroom; the paperwork is just out of date. From now on: whenever you change what's inside a counted room, update the count on the declaration in the same trip — the declaration isn't paperwork about the change, it IS the change, as far as the inspector is concerned.

## 🟣 CHILD NOTE

Imagine your teacher has a list that says "this box should have 20 marbles." You add one marble to the box — now there are 21 — but you don't update the list. When someone checks the list against the box, they think a mistake happened, even though nothing is wrong: you just forgot to change the number on the list. The rule: whenever you add or take away marbles, change the number on the list at the same time. The list isn't extra homework — it's part of doing the job right.

## 🔵 GRANDMA NOTE

It's like the medicine cabinet inventory your nurse keeps: the card on the door says how many bottles should be inside. If the doctor adds a new prescription and nobody updates the card, the next count comes up wrong and everyone panics about a missing bottle. Nobody stole anything — the card was just never updated. The fix is simple: when the contents change, change the card in the same breath. The card is not separate from the work; it is part of the work.

## 🟠 NAYA NOTE

Rule: any change under a counted domain ships its count-ledger update in the same commit. Before pushing a BRAIN/ content change: (1) run `tools/regenerate_brain_index.py --check` locally and reproduce any failure on the exact bytes — a stale count is a diagnosis, not a regression; (2) update `EXPECTED_DOMAIN_COUNTS` deliberately (never by hand-editing generated indexes without the tool) and regenerate all index layers; (3) when pushing via the Git Data API, no CI fires — the local battery on the exact pushed bytes is the gate, so verify `--check` + node + pytest against the byte-verified tree (`remote tree identical to locally tested tree`); (4) triage heuristic: `--check` exit 2 after a content-adding change = check the ledger pin first, the code second. Cousin of SN-038 (regeneration intent): SN-038 says confirm removals are deliberate before `--check-to-regenerate` bakes state; this says the count pin is the deliberate declaration — keep it current, or the gate will correctly report a drift you caused.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "count_ledger_staleness",
  "evidence": {
    "board": "#554 comment 5933379398 (2026-10-01T14:19:39Z)",
    "mechanism": "tools/regenerate_brain_index.py EXPECTED_DOMAIN_COUNTS['05-MEMORY'] pinned at 20 while 21 files on disk after SN-053 added one file",
    "failure": "CI test job --check exit 2 — presented as regression, was stale declared count",
    "diagnosis": "reproduced locally on exact bytes 02d65636 before repairing",
    "repair": "commit aa06f6cd on brain-build/sn053-collective-chain-first-test: EXPECTED_DOMAIN_COUNTS 20->21 (deliberate, comment updated), index layers regenerated (NAYAPOWER-BRAIN-INDEX.json, REAL-TREE.json, REAL-TREE.md)",
    "verification": "on exact pushed bytes (remote tree byte-verified identical to locally tested tree cee76b89): regenerate_brain_index.py --check PASS (164 files), node --test tests/*.test.mjs 0 fail, python -m pytest -q 545 passed, 3 skipped"
  },
  "rule": "count_ledger_is_part_of_the_change",
  "procedure": [
    "any commit adding/removing files under a counted domain updates the count ledger in the same commit",
    "reproduce --check failures on exact bytes before repairing — stale count is a diagnosis, not a regression",
    "update counts deliberately via the tool's guidance; regenerate all index layers; verify on the exact pushed bytes",
    "triage heuristic: --check exit 2 after a content-adding change -> check the ledger pin first, code second"
  ],
  "related": ["SN-038 (regeneration encodes intent, not accident)", "SN-036 (query the run event that answers the claim)", "SN-048 (API-pushed commits never trigger CI)"]
}
~~~
