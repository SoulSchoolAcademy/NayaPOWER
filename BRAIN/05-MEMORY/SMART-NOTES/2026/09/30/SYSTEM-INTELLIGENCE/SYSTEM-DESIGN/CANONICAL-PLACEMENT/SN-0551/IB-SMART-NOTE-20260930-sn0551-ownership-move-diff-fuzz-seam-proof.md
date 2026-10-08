# An Ownership Move Earns Its Trust Mechanically: Diff-Fuzz the Seam, Don't Assert It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0551-ownership-move-diff-fuzz-seam-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6041923331 ([NAYA 4] [CONNECT-DRIVER] completion — CONNECT executable seam landed on main, 2026-10-07T16:12:52Z); main `75f6e225`; PR #1739

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The CONNECT executable seam landed on main (`75f6e225`): the Graph V2 selector is now a CONNECT-owned module (`supabase/functions/_shared/connect_selector.ts`) instead of inline code in KNOW's edge function. The move did not earn trust by assertion — it earned it mechanically: **6000-comparison diff-fuzz** proving zero behavior change, plus a **9/9 behavior matrix**, plus a full battery green except pre-existing base failures (CONNECT living 8.6 → 8.8). And the proof discipline caught what the move itself couldn't: relocating the module exposed a **test-gate seam** — the new `_shared/` directory trips the `edge_execution_coverage` gate — which got its own repair PR (#1739) instead of being merged through or self-repaired onto main.

Why this is brain-grade: an ownership move without behavior proof is a trust downgrade — the reviewers, the CI, and the cold successor all lose the thing the inline code's history gave them. The rule this establishes: moving code across an ownership boundary requires a mechanical no-delta proof at the seam (diff-fuzz with a named comparison count, behavior matrix with named coverage), AND the battery must cover the CI surface of the **new location**, not just the behavior of the old code. A moved module inherits new gates; the old location's greenness proves nothing about the new one. The honest move produced an honest second PR instead of a quiet merge.

## 🩷 HUMAN NOTE

Shawn — a process lesson worth banking from today's CONNECT work. When the Graph V2 selector moved from KNOW's edge function into its own CONNECT-owned module, the lane didn't just say "it works the same" — they ran 6000 comparisons proving the behavior is byte-identical, plus a full behavior matrix. And the move still surfaced something: the new folder trips a coverage gate, so a separate repair PR (#1739) is open for that instead of anyone merging through it. The rule now: moving code across an ownership boundary has to be proven mechanically, and the tests have to cover where the code lives *now*, not where it used to live.

## 🟣 CHILD NOTE

Imagine moving your desk to a new room and saying "everything is in the same place." Your friend shouldn't believe you — she should check every drawer. That's what the diff-fuzz did: checked 6000 things, drawer by drawer, and confirmed nothing changed. And then the move revealed something new: the new room has a different lock on the door (a new test rule). Instead of ignoring the lock, they opened a separate job to fix it properly.

## 👵 GRANDMA NOTE

When a family business moves the cash register to a new counter, the owner doesn't trust the move by memory — she counts the drawer before and after and reconciles every bill. That's the discipline here: count before, count after, 6000 comparisons, zero difference. And when the new counter turns out to sit under a different alarm sensor, you don't disable the alarm — you register the new counter with the alarm company. A second job, done properly, not a shortcut.

## 🧠 NAYA NOTE

Cold successor: whenever a PR moves code across an ownership boundary (inline → shared module, one node's file → another's), demand two things before treating it as a seam upgrade. (1) A mechanical no-delta proof at the seam: diff-fuzz with a named comparison count (here: 6000) plus a named behavior matrix (here: 9/9), proving zero behavior change — assertion is not proof. (2) A CI-surface check of the NEW location: the moved code inherits gates the old location never had (here: `edge_execution_coverage` on the new `_shared/` dir); run the full battery against the new location, and if it introduces a RED, open a separate repair PR (here: #1739) — never merge through it, never self-repair onto main. No merge by the builder; no deploys; nothing RATIFIED by this note.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0551",
  "title": "An Ownership Move Earns Its Trust Mechanically: Diff-Fuzz the Seam, Don't Assert It",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "CANONICAL-PLACEMENT"],
  "cousins": ["SN-0447", "SN-0236", "SN-0508"],
  "evidence": {
    "board": ["#1354 6041923331 ([NAYA 4] [CONNECT-DRIVER] completion — CONNECT executable seam landed on main, 2026-10-07T16:12:52Z)"],
    "landing": "main 75f6e225 — Graph V2 selector now CONNECT-owned supabase/functions/_shared/connect_selector.ts (was inline in KNOW's edge function)",
    "proof": "6000-comparison diff-fuzz (zero behavior change), 9/9 behavior matrix, full battery green except pre-existing base failures; CONNECT living 8.6 -> 8.8",
    "seam_found": "new _shared/ dir trips the edge_execution_coverage gate — the test RED that the #1735 merge introduced on main",
    "repair": "PR #1739 (fix(tests): exclude _shared/ from edge function coverage gate) — separate vehicle, node CI green on the branch; only pre-existing pytest drift remains; NOT merged by the builder"
  },
  "doctrine": {
    "no_delta_proof": "an ownership move without a mechanical zero-behavior-change proof (named comparison count + named behavior matrix) is a trust downgrade, not a seam upgrade",
    "new_location_new_gates": "a moved module inherits the CI surface of its new location; the old location's greenness proves nothing about the new one — battery the destination, not the origin",
    "separate_vehicle": "a gate seam exposed by the move gets its own repair PR (#1739), never merged through, never self-repaired onto main",
    "score_move": "CONNECT living 8.6 -> 8.8 on the evidence, not on the assertion"
  },
  "rule": "moving code across an ownership boundary is proven mechanically at the seam (diff-fuzz + behavior matrix) and battery-tested at the new location; anything the move exposes becomes its own repair PR"
}
```
