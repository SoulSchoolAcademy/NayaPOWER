# Classify Collisions Before Acting — GENUINE / FALSE / HISTORICAL, and Never Renumber What Design Explains

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0625-collision-triage-classify-before-acting
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6050063949 ([Naya 2][PRIORITY-7 SIGN-OUT] — 19 note-ID collisions quarantine triage, 2026-10-08T01:08:11Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Asked to triage 19 note-ID collisions, Naya 2 classified before acting and found **nothing to renumber** — and that was the correct, complete outcome. Her rubric, worth keeping verbatim: (1) enumerate from live bytes at pinned SHAs (main tree + open SN PR heads + date-partition scan, leading zeros normalized); (2) classify each by *artifact type* before calling it a collision. The 19 fell into three classes: **GENUINE** — real duplicates needing a disposition (SN-018's 10/01 vs 10/02 date-partition pair → already tombstoned, no action; SN-0522 cross-branch → genuinely colliding because Naya 5's claim was ratified and merged on main via #1726, so the #1229 branch voice note must renumber before merge, escalated to the lane that owns the branch); **FALSE** — pairs that look like collisions but are by design (SN-002: `.naya/capture/` JSON vs `BRAIN/` MD are pipeline input vs canonical note; SN-0522 on main: `.naya/laws/` JSON vs `BRAIN/` MD are a machine-law twin pair linked by `machine_twin_of`); **HISTORICAL** — resolved by prior renumbering before the snapshot (14 of the 19). Two standing rules fall out: a collision triage that ends with "nothing to renumber" is a *completed* triage, not a failed one; and **renumbering is the disposition of last resort** — tombstoned, by-design, and already-healed items are never re-touched. Action taken: zero. Destructive writes: zero. Correctness: preserved.

## 🩷 HUMAN NOTE

Shawn, Naya 2 was handed 19 ID collisions and handled them exactly right: she sorted them before touching anything, and the sorting showed almost none were real problems. Some were tombstones (already-dead markers pointing to the real note — fine to leave), some were deliberate pairs (the same note in two formats by design — fine to leave), and the rest had already been fixed by the dedup agents. The only genuinely live one is the SN-0522 cross-branch case, and she escalated it to the lane that owns that branch instead of renumbering it herself. Nothing was renamed, nothing was broken. That's the standard: classify first, act only on what's real, and the owner of the artifact does the renaming.

## 👶 CHILD NOTE

Imagine you find two kids with the same name tag in school. Before you make one change their name, you check: are they twins (same name on purpose)? Is one tag an old sticker that was already replaced? Was the mix-up already fixed by the teacher? Only if it's a *real* clash — two different kids, one name, right now — do you change anything. Naya 2 checked all 19 "clashes" and found most were twins, old stickers, or already fixed. She left them alone. Checking first means you never break what's already right.

## 👵 GRANDMA NOTE

Dear, this is about resisting the urge to fix. When you see a list of problems, the instinct is to start fixing immediately — but the first step is sorting. Some "problems" are just how things are supposed to look; some are already gone; only a few are real. Naya sorted all 19 and found only one that needed anyone to act, and she sent it to the right person rather than doing it herself. A fixer who never sorts is a wrecker with good intentions. Sort first; fix only what's real; leave the rest — including other people's property — alone.

## 🧠 NAYA NOTE

Cold successor: the collision-triage registry procedure, in order: (1) pin SHAs — main HEAD, #1229-branch HEAD, every open SN PR head — and say them in the same breath as the findings; (2) enumerate with normalization — `git ls-tree` / tree API recursive, normalize leading zeros (`SN-018` ≡ `SN-18`), scan date partitions (`2026/10/01` vs `2026/10/02`) since the same note restaged under a new date is the most common phantom collision; (3) classify by artifact type before calling it a collision — CAPTURE input vs canonical note (`.naya/capture/` JSON vs `BRAIN/` MD) and machine-law twin pairs (linked by `machine_twin_of`) are FALSE by design, tombstones marking supersession are RESOLVED by design; (4) for GENUINE cross-branch collisions, apply first-claim-stands — a ratified-and-merged note on main outranks a draft copy on a branch, and **the displaced lane renumbers its own artifact** (you never renumber another seat's branch; you escalate to them, as Naya 2 did for SN-0522 → the #1229 priority agent); (5) close with the exact disposition table — ID, location, class, action, evidence — so the next successor can re-derive it. "No live collisions remain; nothing renumbered; nothing touched" is a complete verdict. Do not let a zero-action outcome feel like an unfinished job — it is the triage succeeding.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0625",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/COLLISION-REGISTRY",
  "doctrine": "Classify collisions before acting — GENUINE (act or escalate), FALSE (by-design artifact pairs: capture input vs canonical note, machine-law twin pairs), HISTORICAL (already resolved); renumbering is the disposition of last resort, and the displaced lane renumbers its own artifact.",
  "family": "COLLISION-REGISTRY (SN-0033 first-claim, SN-0167 director-lock, SN-0480 registry, SN-0624 quarantine-staleness)",
  "evidence": [
    "#1354 comment 6050063949 (Naya 2 triage table: 19 items; SN-018 tombstoned→resolved; SN-002 capture-vs-canonical→FALSE by design; SN-0522 machine-twin→FALSE by design; SN-025 stale branch title→resolved; 14× 09/30 vs 10/04→HISTORICAL)",
    "#1354 comment 6050063949 (SN-0522 cross-branch: Naya 5 claimed 2026-10-07 14:27Z, ratified, merged #1726 on main → first-claim stands; #1229 branch voice note must renumber before merge; escalated, not touched)"
  ],
  "falsifiers": [
    "Renumbering a collision classified FALSE or HISTORICAL",
    "Renumbering another seat's branch artifact instead of escalating to its owner",
    "Calling a capture/canonical or machine-twin artifact pair a collision without checking artifact type",
    "A triage with zero actions reported as incomplete work"
  ],
  "applies_to": "all smart-note ID collision triage; registry reconstruction procedure: pinned SHAs, recursive enumeration, leading-zero normalization, date-partition scan"
}
```
