# Mergeable Is Blind to Stacked Conflicts — Simulate the Wave with merge-tree on Exact SHAs

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0740-mergeable-blind-to-stacked-conflicts
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6072910747 ([NAYA 4][SELF-BUILD LOOP — SIGN-OUT, 2026-10-08 19:45 PDT / 2026-10-09 02:45 UTC] — SoulSchoolAcademy; wave merge-readiness scan #1840 → #1858 → #1838 → #1837 → #1900 → #1854 ↔ #1844; main pin `58bb427ddfc1551899258cd55ef98439cf7219ea`).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

GitHub's `mergeable=True` is computed per-PR against main — **it cannot see conflicts between two open PRs that both target main.** Every PR in the RED-fix wave read clean individually, yet a pairwise `git merge-tree` simulation on the exact head SHAs found two real stacked conflicts: **#1838 ↔ #1837** (both orders) and **#1854 ↔ #1844** (both orders), all on `.naya/memory/smart-notes/index.json`.

The simulation is only half the lesson — the other half is **characterizing each conflict at entry level** before anyone merges, because the characterization prescribes the resolution:

- **#1838 ↔ #1837: positional-only.** #1837 renames the SN-0359→SN-0642 entry while #1838 adds 8 new entries — zero entry overlap. Resolution: apply both (624 entries).
- **#1854 ↔ #1844: field-disjoint.** 16 shared entry IDs, but the lanes change disjoint fields (#1854: `smart_link*` fields; #1844: `smart_note_id` + provenance). Resolution: field-level merge resolves cleanly.
- All other pairs: CLEAN. #1900 (base == tip) conflicts with nothing.

Rule for a cold successor: **before sequencing any merge wave, simulate every adjacent pair with `git merge-tree` on the exact SHAs, then characterize each conflict as positional-only / entry-overlap / field-disjoint.** The characterization — not the merger's gut — prescribes the resolution recipe (apply-both / field-merge / rebase by wave owner). `mergeable=True` answers "can this one PR merge into main right now"; it never answers "can these PRs merge in sequence" — and a wave merged on that confusion lands a conflict at the worst possible moment. All merges still re-validate mergeability at action instant (SN-0493); the simulation feeds the order, the instant check gates the merge.

## 🩷 HUMAN NOTE

Shawn — a merge-safety fix from tonight's wave work. GitHub said every PR in the RED-fix wave was mergeable, but "mergeable" only checks one PR against main — it can't see two PRs fighting each other. A pairwise simulation on the exact branch heads caught two real conflicts the dashboard missed, both in the Smart Notes index. Each one was characterized precisely (one is a positional clash, the other two lanes editing different fields of the same entries), so the resolutions are mechanical, not judgment calls. Standing rule: no merge wave is sequenced without the simulation first; the wave order is computed from the simulation, and the actual merge still re-checks freshness at the instant it runs.

## 🟣 CHILD NOTE

Imagine two kids each ask the teacher "can I sit in that empty chair?" and the teacher says yes to both — because she checked each kid against the chair, not against each other. That's what GitHub's "mergeable" check does. The fix: before seating day, check every pair of kids against each other. When two want the same chair, figure out exactly what kind of clash it is — do they want the chair at the same time, or do they just want to decorate different parts of it? The kind of clash tells you how to fix it.

## 👵 GRANDMA NOTE

When several changes are lined up to be added to the project, the website said "all clear" on every single one. But the website only checks each change against what's already there — it doesn't check whether the changes fight each other. Running a test merge of each pair on the exact current versions revealed two fights the website missed, both in the same index file. The fix: before lining changes up, always test-merge the pairs, describe each fight precisely (positional, overlapping, or editing different parts), and let that description decide the order and the fix — not guesswork.

## 🟠 NAYA NOTE

Make wave sequencing mechanical: (1) list the wave in proposed order; (2) for every pair that will land adjacently, run `git merge-tree` on the two exact head SHAs (not branch names — SHAs, per SN-0493's currency rule); (3) for each conflict found, characterize at the finest grain the file format allows — positional-only, entry-overlap, or field-disjoint — and write the resolution recipe into the wave receipt; (4) mergeable=True remains only a per-PR hygiene signal, never a wave-safety verdict; (5) re-validate at action instant, because the tip moves. If a wave's conflict list is empty, say so explicitly — "all pairs clean" is a claim with the simulation as its evidence.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0740",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/MERGE-BOUNDARY",
  "doctrine": "mergeable-blind-to-stacked-conflicts",
  "rule": "GitHub mergeable=True is per-PR against main and cannot see stacked conflicts between open PRs. Before sequencing a merge wave, simulate every adjacent pair with git merge-tree on exact head SHAs, characterize each conflict as positional-only / entry-overlap / field-disjoint, and let the characterization prescribe the resolution recipe.",
  "failure_mode": "a wave ordered on mergeable=True lands a stacked conflict at merge time — the dashboard was green for every PR individually",
  "checks": [
    "enumerate the wave's adjacent pairs",
    "run git merge-tree on exact head SHAs for each pair (record SHAs in the receipt)",
    "characterize each conflict at entry/field level; write the resolution recipe before merging",
    "re-validate mergeability at action instant (SN-0493) — the simulation feeds the order, the instant check gates the merge"
  ],
  "cousins": ["SN-0676", "SN-0681", "SN-0236", "SN-0508", "SN-0493"],
  "evidence": [
    "#1354 comment 6072910747 (Naya 4 self-build loop sign-out, 2026-10-08 19:45 PDT / 2026-10-09 02:45 UTC): stacked-merge simulation (git merge-tree on exact SHAs) — GitHub mergeable=True does NOT see stacked conflicts; #1838<->#1837 CONFLICT and #1854<->#1844 CONFLICT (both orders) on .naya/memory/smart-notes/index.json, characterized at entry level (positional-only: #1837 renames SN-0359->SN-0642 entry, #1838 adds 8 new entries, zero overlap; field-disjoint: 16 shared entry IDs, disjoint fields); all other pairs CLEAN; #1900 conflicts with nothing"
  ]
}
