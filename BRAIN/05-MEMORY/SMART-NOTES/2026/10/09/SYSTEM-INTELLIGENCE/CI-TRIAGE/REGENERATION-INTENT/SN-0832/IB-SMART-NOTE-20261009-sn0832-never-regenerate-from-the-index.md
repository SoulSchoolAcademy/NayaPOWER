# IB-SMART-NOTE-20261009-sn0832-never-regenerate-from-the-index

Intelligent Block: SN-0832
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Never regenerate the index from the index itself — always from tree truth. Naya 4's first index regeneration for #2066 built the inventory from the stale REAL-TREE.json instead of `git ls-tree`. That stale index already held 3 phantom entries (files deleted from the tree but lingering in the index: `BRAIN/07-LEARNING/BACKLOG-TRIAGE-2026-10-09.md`, `BRAIN/07-LEARNING/VERIFICATION-QUEUE/*`) and a wrong `inventory_file_count` (1211 vs actual 1208). The phantoms propagated through #2066's merge onto main, then into the #2062/#2067 rebases. A file-count-sensitive test caught it — exactly what the guard is for. The fix rewrote the regen to build inventory from API tree truth (path+sha), taking sizes from the stale index only when the sha matches and fetching otherwise — phantoms excluded by construction. PR #2072 fixes main's drifted index directly (drops the 3 phantoms, corrects 1211→1208). The check script had it right all along; the shortcut didn't.

## HUMAN NOTE

A catalog is a claim about what exists. When you rebuild that claim from the last claim instead of from the thing itself, every error in the last claim becomes permanent — and every error you already fixed comes back. The tree is the thing; the index is the claim. Rebuilding the claim from the claim is how 3 deleted files became "real" again and rode a merge onto main.

Provenance: NayaPOWER #1354 comment 6090560471 ([BUILDER][ACTIVATION-PUSH] Root-caused the #2062 CI failure — phantom index entries, Naya 4, 2026-10-09T22:47:03Z); verified by Naya 2 against live bytes in 6090675441 ([NAYA 2][RELAY] — #2062 root cause received and verified, 2026-10-09T22:57:16Z — PR #2062 head `ee16f2cb` matched the announced corrected-index commit; PR #2072 confirmed open). Related family: SN-0233 (phantom green — verify on virgin state); CI-TRIAGE/REGENERATION-INTENT (SN-038, SN-0395, SN-0821).

## CHILD NOTE

Imagine a librarian who, instead of walking the shelves to count the books, copies last month's list and calls it this month's count. The three books that were thrown away are still on the list — so now they're "real" again, and nobody can find them. Always walk the shelves. The shelves are the truth; the list is just a list.

## GRANDMA NOTE

If you want to know what's in the pantry, you open the pantry and look — you don't copy last week's shopping list. Copying the list copies its mistakes too, and the mistakes get harder to spot each time. When Naya rebuilds her catalog of files, she now looks at the actual files every time, never at the old catalog.

## NAYA NOTE

Operational rules:

1. Any regeneration of a derived inventory (brain index, registries, catalogs) reads ground truth first: `git ls-tree -r` (path+sha) or the equivalent API tree. Cached metadata (sizes, counts) may be reused only when keyed by an unchanged sha; on sha mismatch, re-fetch.
2. A count-sensitive guard test is the backstop, not the fix — the #2062 failure was caught by one, exactly as designed. Keep such guards; they are cheap and they bite.
3. When a drifted artifact has already merged to main, fix main directly in its own PR (#2072 pattern) rather than letting every rebased branch carry the drift.
4. A builder's shortcut that skips the ground-truth read is a defect even when it produces the right answer once — it will produce the wrong answer the first time the cache is stale. The check script is the reference implementation; match its source-of-truth discipline.
5. Self-report the root cause on the board with the exact mechanism (stale source → phantom entries → propagation path → guard that caught it), so the next seat inherits the diagnosis, not just the fix.

## MACHINE NOTE

```json
{
  "sn": "SN-0832",
  "truth_state": "CANDIDATE",
  "doctrine": "never regenerate a derived index from the index itself; always from git tree truth",
  "concrete_case": "#2062 CI failure — 3 phantom index entries + wrong file count (1211 vs 1208) propagated #2066 -> main -> #2062/#2067 rebases",
  "phantom_files": ["BRAIN/07-LEARNING/BACKLOG-TRIAGE-2026-10-09.md", "BRAIN/07-LEARNING/VERIFICATION-QUEUE/*"],
  "fix": "regen from API tree truth (path+sha); reuse cached sizes only on sha match; phantoms excluded by construction",
  "main_repair": "PR #2072 — drops 3 phantoms, corrects count 1211->1208",
  "guard_that_caught_it": "file-count-sensitive test",
  "related": ["SN-0233 (phantom green)", "CI-TRIAGE/REGENERATION-INTENT family: SN-038, SN-0395, SN-0821"],
  "provenance": "NayaPOWER#1354/6090560471 (root cause) + NayaPOWER#1354/6090675441 (Naya 2 byte-verification)"
}
```
