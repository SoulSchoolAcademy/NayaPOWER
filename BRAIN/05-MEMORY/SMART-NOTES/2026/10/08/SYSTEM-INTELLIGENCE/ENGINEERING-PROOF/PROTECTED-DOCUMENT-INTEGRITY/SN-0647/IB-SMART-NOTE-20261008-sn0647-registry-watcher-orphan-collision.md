# The Registry Watcher Seam — Orphan Entries Without Projection Paths Claim Real SN IDs

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0647-registry-watcher-orphan-collision
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6052661311 ([REGISTRY-WATCHER] Cycle 1 report — main @ `aca944b5`, 2026-10-08T05:01:42Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The first cycle of the new REGISTRY-WATCHER agent found the seam it was built to find: **18 duplicate SN IDs in the registry** — two registry entries claiming the same SN number. The pattern: one entry has a `projection_path` (real, backed by an on-disk IB), the other has none (orphan). The orphan is the invisible one: it claims the identity of a real note while pointing at nothing, so canonical intelligence can silently resolve to the wrong object. The doctrine: **a registry entry is claimed by its projection, not its number** — entries without projection paths are orphans and must be removed or renamed, never left to collide. The watcher pattern that caught it (count entries → count unique SN IDs → list on-disk directories → compare → report gaps and collisions, every 30 minutes, read-only) is now the mechanical guard. Complements SN-0643's duplicate-ID reader rule: SN-0643 resolves collisions at read time; this one removes them at the source.

## 🩷 HUMAN NOTE

Shawn — one registry bug worth banking from this morning's first watcher cycle: it found 18 Smart Note IDs claimed by *two* registry entries each. The pattern is always the same — one entry points at a real file on disk, the other points at nothing at all (an orphan left behind by some earlier staging step). The orphan is dangerous because it's invisible: same number, no file, and it can make the real note's identity resolve wrong. The fix rule is simple — a registry entry only owns its number if it points at a real file; orphan entries get removed or renamed, never left colliding. The watcher agent now checks this every 30 minutes, so the registry can't silently rot again. Same lesson as everywhere else: verify the real thing, don't trust the list.

## 👶 CHILD NOTE

Imagine a school where every student gets a locker number. One day someone finds 18 locker numbers assigned to *two* kids each — and the second kid on each locker doesn't actually exist; they're just names left on the list. The real kids can't be sure their locker is really theirs. The rule: a locker number only belongs to you if you're actually standing in front of a locker. Names on the list without a locker get erased. And now a helper walks the hallway every half hour counting lockers and lists, so it can never happen again.

## 👵 GRANDMA NOTE

Dear, this is about keeping a ledger honest. A registry is like a guest book: every entry should point to a real guest. The watcher found eighteen names in the book that each shared a number with a real guest — phantom entries with no person behind them. Phantoms are worse than missing entries, because they wear a real guest's number. The rule written down: an entry owns its number only if there's a real thing behind it; phantoms get struck from the book. And now someone walks through and reconciles the book against the actual guests every half hour, so phantoms can't pile up in the dark again.

## 🧠 NAYA NOTE

Cold successor: the Smart Note registry is load-bearing canonical infrastructure — an ID collision can make intelligence resolve to the wrong object or vanish. The seam: **staging can leave registry entries without `projection_path` (orphans), and orphans collide with real entries on the same SN number.** Mechanical guard, the REGISTRY-WATCHER pattern: every 30 minutes, read-only — (1) count registry entries; (2) count unique SN IDs; (3) list on-disk SN directories; (4) diff all three. Report four classes: duplicates (same ID, ≥2 entries — the orphans are the entries *without* projection_path), on-disk-not-in-registry, in-registry-not-on-disk (may be legitimate projection-less entries — do not auto-flag), and total counts. Repair is lead-owned: remove the orphan or reassign its ID; never regen the index to absorb it (SN-0420). Cycle 1 baseline (main @ `aca944b5`): 617 entries, 599 unique IDs → 18 collisions (SN-018, SN-019, SN-020, SN-022, SN-032, SN-034, SN-035, SN-041, SN-042, SN-0356, SN-0357, SN-0359, SN-0361, SN-0362, SN-0501, SN-0523, SN-0524, SN-0525), spot-confirmed as real collisions with distinct content hashes. Reader-side resolution is SN-0643; this note is source-side removal.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0647",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/PROTECTED-DOCUMENT-INTEGRITY",
  "doctrine": "A Smart Note registry entry is claimed by its projection_path, not its SN number: entries without projection_path are orphans that silently collide with real entries; the read-only watcher pattern (count entries, count unique IDs, list on-disk dirs, diff — 30min cycles) detects the drift; lead removes orphans, never regens the index to absorb them.",
  "family": "SN-0643 (duplicate-ID reader rule — read-time resolution; this is source-side removal) + SN-0420 (never absorb the anomaly to silence the tripwire) + SN-0408 (deletion discipline)",
  "evidence": [
    "#1354 comment 6052661311 ([REGISTRY-WATCHER] Cycle 1 report, 2026-10-08T05:01:42Z): 18 duplicate SN IDs in registry — one entry with projection_path (real), one without (orphan); spot-checked SN-018, SN-0356, SN-0501, SN-0359 confirmed real collisions with distinct content hashes",
    "Cycle 1 counts: 617 registry entries, 599 unique SN IDs; 597 on-disk SN directories; 8 on-disk-not-in-registry (covered by PR #1838); 8 in-registry-not-on-disk (legitimate projection-less entries, not flagged)",
    "SN-0359 collision noted as separate from PR #1837's capture-file fix — registry still needs the orphan entry removed/renamed after merge"
  ],
  "falsifiers": [
    "Leaving a projection-less registry entry on an SN number already claimed by a real entry",
    "Fixing a duplicate-ID report by regenerating the index instead of removing the orphan entry",
    "Auto-flagging projection-less entries that are legitimately unprojected (conflates two distinct classes)"
  ],
  "applies_to": "smart-note registry maintenance, any ID-claiming registry with projection-backed entries, canonical intelligence infrastructure"
}
```
