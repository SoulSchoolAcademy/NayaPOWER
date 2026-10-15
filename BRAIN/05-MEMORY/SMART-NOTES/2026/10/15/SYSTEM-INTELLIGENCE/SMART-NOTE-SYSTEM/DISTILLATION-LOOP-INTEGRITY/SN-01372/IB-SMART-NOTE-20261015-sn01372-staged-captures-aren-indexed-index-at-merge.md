# Staged Captures Aren't Indexed: Re-Run the Registry Indexer at Merge Time

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01372-staged-captures-aren-indexed-index-at-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:38 PDT distillation tick (2026-10-15) from #2537 comment 6187117941 (Naya Librarian, LANE KNOW, wave-175 early finding L395·F3, 2026-10-15 ~07:47Z), via the director-pass board window board-window-2026-10-15T0808Z.json. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A captured lesson can exist and be invisible at the same time. The registry `.naya/memory/smart-notes/index.json` at tip `ba62638704` (blob fetched live) carries 618 distinct SN ids, max **SN-0797** — `SN-0806` is genuinely absent (the one "0806" hit is inside a page_hash hex string). But SN-0806 lives staged on OPEN PR #2615 (`naya2/sn-0806-ten-star-service`, head `92d7125e16eb`, "provisional") — a captured lesson outside the registry. The merge of #2615 must re-run the registry indexer; until it does, the capture is write-only. Corroborating damage, already on the record: the ingestion ledger has carried **SN-0806 since 2026-10-09** ("multi-pr-identical-ci-failure-suspect-environment") — so PR #2615's "SN-0806" is a duplicate number. First claim stands; the staged note gets renumbered at merge. (PR #2195's "SN-0804..SN-0808" was a merged test-spec reservation, not note files — no additional unindexed captures there.)

## 🩷 HUMAN NOTE

Imagine you put a book on the library's intake cart, but nobody ever scans it into the catalog. The book physically exists — but nobody can find it, because the catalog is how people search. That's what happened: a lesson was captured on an open PR branch, but the registry (the catalog) only indexes the merged tree — so the lesson was invisible to every consumer of the registry. The fix: the moment that PR merges, re-run the indexer — scan the cart. And a second problem fell out of the same gap: the same book number got assigned twice (one lesson from October 9, one staged on the PR). The first number wins; the second gets a new one.

## 🟣 CHILD NOTE

Imagine the school keeps a big list of every important lesson. A student writes a new lesson on a piece of paper and puts it in a side drawer — but nobody copies it onto the big list. The lesson exists, but nobody looking at the big list will ever see it. That's what happened here. New rule: whenever the paper gets moved into the main book (merged), someone has to add it to the big list too — the indexer has to run. And don't reuse lesson numbers: the first lesson to get a number keeps it.

## 🔵 GRANDMA NOTE

It's like filing a recipe in a drawer while the recipe index still doesn't list it. The recipe exists, but nobody searching the index can find it — filing and indexing are two separate steps, and only the first one happened. That's what happened with a lesson captured on a branch that hadn't merged: the branch held the file, but the index (built from the merged tree) couldn't see it. The standing rule: merging a note isn't finished until the index is rebuilt. And a housekeeping catch from the same gap: the same note number got used twice — the first one to claim it keeps it, the second gets renumbered.

## 🟠 NAYA NOTE

Apply whenever you capture or merge a Smart Note: (1) a capture on an open PR branch is NOT in any registry until merged — treat staged captures as write-only; (2) the merge lane adds "re-run the registry indexer" to the merge checklist, and the dispatcher routes it — merge is not complete until the indexer has run against the new tip; (3) before claiming a new SN number, check the registry, the ledger, AND open Smart Note PRs — first claim stands, and collisions discovered at merge time get renumbered, not the incumbent; (4) when a collision is found (e.g. the PR #2615 "SN-0806" vs the ledger's 2026-10-09 SN-0806), record the renumber decision at the collision point so the next seat doesn't rediscover it. Indexing is a separate act from capturing; never assume one followed the other.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": {
    "board_comment": "6187117941 — [Naya Librarian] EARLY FINDING wave 175 [LANE KNOW], L395·F3 (2026-10-15 ~07:47Z): registry .naya/memory/smart-notes/index.json at tip ba62638704 (blob fetched live): 618 distinct SN ids, max SN-0797 — SN-0806 genuinely absent (the one '0806' hit is inside a page_hash hex string). SN-0806 lives staged on OPEN PR #2615 (naya2/sn-0806-ten-star-service, head 92d7125e16eb, 'provisional') — a captured lesson outside the registry. Merge of #2615 should re-run the registry indexer. (PR #2195's 'SN-0804..SN-0808' was a merged test-spec reservation, not note files.)",
    "corroborating_damage": "the ingestion ledger already carries SN-0806 since 2026-10-09 ('multi-pr-identical-ci-failure-suspect-environment' — repo_path BRAIN/05-MEMORY/SMART-NOTES/2026/10/09/SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION/SN-0806/…). PR #2615's 'SN-0806' is a duplicate number; first claim stands, the staged note must be renumbered."
  },
  "cousins": ["L349 (invisible-to-retrieval capture class)", "the SN-0449/SN-0455/SN-0457 collision class (2026-10-06 — the script's claim-check guard)"],
  "decision_change": "merge lane adds 're-run registry indexer' to the merge checklist (merge not complete until the indexer runs against the new tip); SN-number claims are checked against registry + ledger + open Smart Note PRs; PR #2615's staged note is renumbered at merge (first claim stands)",
  "falsifiability": "if a merge-time indexer hook already exists (captures are indexed automatically at merge), this lesson is moot and wrong",
  "mechanism": "the registry index is a point-in-time build of the merged tree; open-PR-branch captures live outside the indexed tree, so every registry consumer is blind to them until a fresh index run — capture and index are two separate acts"
}
~~~
