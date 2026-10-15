# Corpus Resolution: Distill the Spine, Archive the Rest — the Cold Path Must Contain Zero Ambiguity

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01400-corpus-resolution-distill-the-spine-archive-the-rest
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 07:38 PDT distillation tick (2026-10-15) from #2537 comment 6194027547 (main seat, 2026-10-15T14:06:28Z — "CORPUS RESOLUTION — FULL PLAN, THOUGHT THROUGH BEFORE ACTING"), via the director-pass board window board-window-2026-10-15T1414Z.json. Decision: Shawn's directive, deliberated with a scored decision matrix before acting.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The repo's doc corpus (~880 docs) had grown into a cold-start hazard: a new Naya activating from the working tree alone met confusion, duplication, and rot. The main seat's resolution, scored before acting: (1) TRIAGE — ranked list with per-doc verdicts; (2) DISTILL THE SPINE — the top docs distilled to ESSENCE in three tongues, machine tongue FIRST (exact values, procedures, dependencies as structured data), AI tongue second, human tongue last, linked in dependency order, load-bearing first — this becomes the cold-start path; (3) CLEAR THE WORKING TREE — everything not in the spine moves to archive branch `archive/corpus-2026-10-15`, leaving working BRAIN/ as spine + manifest; (4) COLD-START MANIFEST — one file, the single entry point: names the spine in reading order, documents the archive branch and the one-command on-demand fetch, carries machine-readable status per spine doc (last-verified, supersedes/superseded-by). Destruction was rejected as irreversible and human-gated; the archive branch preserves the full audit trail reversibly. The decision's own falsifier: the cold trial — a cold Naya activates from the manifest alone; if she can't, the spine is wrong, re-distill, don't re-argue. Known consequence, named up front: the retrieval batteries (B-48/B-51) measure against the corpus, so their baselines move with it — re-baseline after the move; a RED against the old corpus is not a RED on the new tree.

## 🩷 HUMAN NOTE

Think of the repo like a workshop that accumulated 880 manuals over months — some current, some outdated, some saying opposite things. A newcomer walking in can't tell which manual to trust. The decision: pick the essential manuals, rewrite each one three ways (first as exact data a machine can use, then as working instructions, then as plain human explanation), put them in reading order with one master index — and move everything else into a labeled storage room (not the trash; nothing destroyed). The workshop itself then holds only the essentials plus the index. And there's a built-in test: hand the index to someone who's never been here — if they can't get working from it alone, the essentials list is wrong.

## 🟣 CHILD NOTE

Imagine your backpack is stuffed with 880 papers — old homework, new homework, notes that disagree with each other. You can never find what you need! The grown-ups decided: keep only the most important papers, rewrite them super clearly three ways (first with exact facts, then with instructions, then in simple words), put them in order with one list on top — and move all the other papers into a special labeled box (not thrown away, just stored). Now the backpack has only what you need plus the list. The test: give the backpack to a friend who's never seen it — if they can do the homework from the list alone, you packed it right!

## 👵 GRANDMA NOTE

Sweetheart, picture a recipe box with 880 cards collected over the years — some updated, some crossed out, some contradicting each other. Nobody starting fresh could cook from that box. So the family decided: choose the best recipes, rewrite each one neatly three ways (first the exact measurements, then the steps, then a friendly explanation), arrange them in order with one master card on top listing everything — and move the rest into a labeled keepsake box in the attic, nothing thrown away. The kitchen box now holds only the best plus the master card. And the proof it worked: hand the box to someone who's never cooked here — if they can make dinner from the master card alone, the box is right.

## 🤖 NAYA NOTE

This is the standing shape of the corpus going forward, and it binds your cold-start behavior. When you wake into this repo: read the cold-start manifest first, then the spine in its listed order — that is the whole cold path. Do NOT go digging through the archive branch for cold-start answers; the archive is audit trail, not authority. If a spine doc you need is missing or stale, that is a spine defect — route it, don't work around it by pulling from the archive. When you write or file a doc: ask whether it belongs in the spine (load-bearing, cold-path) or the archive (history, superseded, duplicate). And remember the falsifier discipline this decision models: the decision named its own test (the cold trial), its known consequence (B-48/B-51 re-baseline), and its rejected options (in-tree archive dir = mechanical fragility across every glob; deletion = irreversible) BEFORE acting. Score the options, name the falsifier, then act — never the reverse.

## 🔧 MACHINE NOTE

```json
{
  "sn": "SN-1400",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-15",
  "lesson_class": "DECISION",
  "decision": {
    "spine": "ranked top docs distilled to ESSENCE, three tongues, machine-first, dependency order, load-bearing first; = the cold-start path",
    "archive": "branch archive/corpus-2026-10-15; everything not in the spine leaves the working tree; reversible; audit trail preserved",
    "working_tree": "BRAIN/ spine + cold-start manifest only",
    "manifest": "one file; spine in reading order; archive branch + one-command on-demand fetch documented; per-doc machine-readable status (last-verified, supersedes/superseded-by)"
  },
  "rejected_options": {
    "in_tree_archive_dir": "880 docs remain in every glob/sparse-checkout; confusion persists unless excluded everywhere = mechanical fragility",
    "delete_outright": "irreversible; human-gated; not this seat's to do"
  },
  "falsifier": "the cold trial: a cold Naya activates from the manifest alone; failure => the spine is wrong => re-distill, don't re-argue",
  "known_consequence": "retrieval batteries B-48/B-51 measure against the corpus; re-baseline after the move; RED vs old corpus != RED on new tree",
  "future_decision_changed": "where any doc lives (spine vs archive); how cold-start is designed; whether to delete vs archive; how to score corpus-shape options",
  "evidence": ["https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6194027547"]
}
```
