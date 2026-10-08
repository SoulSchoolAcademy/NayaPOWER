# Declare the Repair Owner at Detection Time — Parallel Lanes Duplicate Before the Law Fires

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0711-declare-repair-owner-at-detection-time
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6067526879 ([NAYA 4 → NAYA 2], 2026-10-08T19:32:10Z, "Deeper find"); sibling commits 924fd6558, ec7b45df1, da4a5920c, eaca9f6cb, 17e9d620b; SN-0236 (one repair per RED class)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 4's deeper find while trimming #1858: the node_order fix existed as **five sibling commits** — `924fd6558`, `ec7b45df1`, `da4a5920c`, `eaca9f6cb`, `17e9d620b` — the same repair built independently on multiple branches. Four are now dead history; only main's `17e9d620b` owns the class. She called it a pre-law SN-0236 violation: SN-0236 says that when a CI red classifies BASE-DEFECT via bare-pin reproduction, exactly one repair PR owns the class.

The new lesson is the **timing gap**. SN-0236 triggers at *classification* — but all five siblings were built *before* any classification finished. In a parallel-lane team, detection-to-build is shorter than detection-to-classification: each lane sees the red, builds the obvious fix, and by the time someone declares an owner, the duplicates already exist. "Declare at classification" is too late. The declaration must happen at **detection time**, before anyone builds — and it costs one sentence on the feed: "RED class X detected, provisional owner = lane Y, pending classification." Provisional ownership is still ownership; five independent builders are the failure.

The cost isn't just bytes. Dead siblings are forensic landmines: the very next comment in the thread shows Naya 2 citing a dead sibling (`924fd6558`) as the landed heal — see SN-0710. Every unowned duplicate is a future miscitation waiting to happen, plus merge conflicts if two siblings ever converge on the same base.

Why this is brain-grade: this is the *temporal* half of the repair-governance family. SN-0236 closed the governance half (one owner per RED class, declared after attribution lands on BASE-DEFECT). This note closes the timing half: attribution arrives too late to prevent duplication, so the ownership sentence moves to the earliest possible moment — the first post that names the RED class. A cold successor running the Nonstop Loop hits this weekly; the loop moves too fast for post-hoc ownership.

Rule for a cold successor: **the first post that detects a RED class names its provisional repair owner in the same breath.** Format: "RED class `<name>` detected at tip `<sha>` — provisional repair owner: `<lane/PR>`, pending classification." If classification later reattributes the red, the owner changes openly. If two lanes already built, the detector's job is to declare the survivor and strand the rest *by name* before citing anything — never let a dead sibling live unmarked in the thread.

## 🩷 HUMAN NOTE

Shawn — one more from the #1858 thread, and it's about team speed creating its own waste. The node_order fix was built five separate times on five branches before anyone declared an owner; only the one on main matters now, and the four dead copies already caused a miscitation (Naya 2 cited a dead one as the landed fix — Naya 4 corrected it). The existing law (SN-0236, one repair per RED class) fires at classification, which is too late — parallel lanes build faster than classification finishes. The repair: the first post that names a RED class also names its provisional repair owner, in the same breath. One sentence, zero delay, five duplicate builds avoided.

## 🟣 CHILD NOTE

Five people all see the same broken toy and all fix it at the same time — now there are five fixed toys, but only one is needed. The four extras aren't just clutter: someone later points at an extra one and says "this is the fix that got used," and they're wrong. The rule: the first person who spots the break says "I'm fixing this" right away — before anyone else starts. One fixer, no confusion, no wrong pointers later.

## 👵 GRANDMA NOTE

Five different people independently repaired the same software bug, each in their own copy. Only one repair made it into the final version. The other four weren't just wasted effort — one of them later got mistaken for the real fix in an official report. The lesson: when a problem is spotted, the spotter should immediately say who's fixing it, before anyone starts work. That one sentence prevents five people from doing the same job and prevents the unused copies from causing confusion later.

## 🟣 NAYA NOTE

Speed without a declared owner is just duplication at velocity. The moment I detect a RED class and post about it, the owner sentence rides in the same post — provisional is fine, pending is fine, silence is not. Parallel by default means five lanes can build the same fix in parallel; the one-sentence declaration is what keeps parallel from becoming redundant. And when duplicates already exist, I strand them by name — four dead commits listed, one survivor crowned — so no future seat cites a corpse. SN-0710 is the proof that unmarked duplicates become miscitations.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0711",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE",
  "doctrine": "declare-repair-owner-at-detection-time",
  "rule": "The first post that detects a RED class names its provisional repair owner in the same post, before any lane builds. Format: 'RED class <name> detected at tip <sha> — provisional repair owner: <lane/PR>, pending classification.' If duplicates already exist, declare the survivor and strand the rest by name.",
  "timing_gap": "SN-0236 declares ownership at BASE-DEFECT classification; parallel lanes build before classification finishes, so ownership must move to detection time",
  "cost_of_duplicates": ["merge conflicts if siblings converge on one base", "forensic miscitation (dead sibling cited as landed heal — see SN-0710)", "board noise: green-looking PRs that own nothing"],
  "cousins": ["SN-0236", "SN-0710", "SN-0351"],
  "evidence": [
    "#1354 comment 6067526879 (Naya 4, 2026-10-08T19:32:10Z, 'Deeper find') — node_order fix as five sibling commits: 924fd6558, ec7b45df1, da4a5920c, eaca9f6cb, 17e9d620b; main's 17e9d620b owns the class; other four are dead branches",
    "Same comment: #1858 trimmed to weights-only (ref 13b1ad03 → 39e88a6b, force rebase onto 78661f59), node_order half dropped as superseded",
    "SN-0236 text: 'when a CI red classifies BASE-DEFECT by bare-pin reproduction, exactly one repair PR owns the class' — the classification-time trigger this note amends"
  ]
}
