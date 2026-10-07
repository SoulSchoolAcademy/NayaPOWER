# Verify Sequential Merge Chains with Git's Real Merge Machinery — Merge-Bases Shift

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0542-sequential-merge-verification-real-merge-machinery
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07 ~06:45 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6040069735 (NAYA 4 self-build loop cycle sign-in/out — repair 955b1996 independently recomputed, 2026-10-07 14:26 UTC: sequential merge of #1702→#1701→#1700 re-anchored at tip ed82e8b3).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When Naya 4 independently verified the 955b1996 tree repair (the #1700/#1701/#1702 head-tree merge damage), a naive per-path 3-way merge simulation against the ORIGINAL base falsely reported 4 conflicts. The naive model is wrong because **merge-bases shift at each step of a sequential merge** — each PR's merge base is computed against the running result, not against the original base you started with. The correct verification method: rebuild the true merge locally with git's own machinery — partial clone, `merge-tree --write-tree` per step in order (#1702→#1701→#1700). That recomputed all three merges CLEAN, final tree `72f44ba2e4edfca51103f2d7568eacbe84f19238` — byte-identical to the repair commit's remote tree. The negative control corroborated: `tools/note_bridge.py` + `scripts/gate-learning-compounding.py` ABSENT at broken tip 46179105, PRESENT at repair tip; broken→repair = exactly 34 files (14 added / 20 modified / 0 removed). CI at repair tip: 19 check-runs, zero failures including the brain-index drift check. The doctrine for the cold successor: **never simulate a sequential merge by hand against a fixed base — re-execute it with the tool that performs it.** The same principle generalizes: any multi-step stateful transformation must be verified by replaying the actual machinery in order, never by a simplified single-step model against the starting state.

## 🩷 HUMAN NOTE

Shawn, one sharp methodology catch from this morning's repair verification: a hand-built simulation of the merge chain reported 4 conflicts that don't exist. The problem was the simulation, not the merge — git computes each merge against a shifting base, and the naive model froze the base at the start. When the merge was re-executed properly with git's own machinery, all three steps were clean and the final tree was byte-identical to the repair. Lesson banked: to verify a multi-step chain, replay the actual machinery in order — never simulate it with a simplified model.

## 👶 CHILD NOTE

Imagine stacking three building-block towers, each one on top of the last. Someone tries to check the stack by rebuilding each tower on the table separately, from the ground up — and says "this doesn't fit!" But that's wrong: each tower was built on top of the *previous* tower, not on the table. To check the stack properly, you have to rebuild it in the same order: tower one on the table, tower two on tower one, tower three on tower two. When they did it that way, everything fit perfectly. Check things the way they were actually built.

## 👵 GRANDMA NOTE

Dear, a clever check this morning failed for the wrong reason. Our engineer wanted to verify a repair that joined three pieces of work, one after another. She tried to test it by comparing each piece against the starting point — and got four false alarms. The trouble: each piece was joined onto the *running result*, so the reference point moved every step. When she re-did the check by actually replaying the joins in order, everything was clean — a perfect match. The rule going forward: to verify a chain, replay the chain itself. Never test steps against the starting line when the ground moves under each step.

## 🧠 NAYA NOTE

Cold successor: whenever you must verify a sequential git-data merge (or any multi-step stateful transformation), replay the real machinery in order — partial clone, then `merge-tree --write-tree` per step, comparing the final tree byte-for-byte against the artifact's remote tree. A naive per-path 3-way merge against the ORIGINAL base is inadmissible evidence: merge-bases shift at each step, and the naive sim will fabricate conflicts (it falsely reported 4 here). Pair the positive recompute with a negative control (files absent at broken tip, present at repair tip; exact add/modify/remove counts) and CI at the tip. This lesson is the verification-methodology cousin of the 2026-10-07 AGENTS.md correction (tree=head-tree silently drops base changes — the failure mode); SN-0128 covers merge-base drift in repair basing. Keep all three in the family but do not merge them: failure mode ≠ verification method ≠ basing discipline.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0542",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "doctrine": "Verify a sequential merge chain by re-executing git's own merge machinery in order (merge-tree --write-tree per step); never simulate it with a naive per-path 3-way merge against the original base — merge-bases shift at each step and the naive model fabricates conflicts.",
  "evidence": [
    "#1354 comment 6040069735 (NAYA 4 self-build loop cycle, 2026-10-07 14:26 UTC: independent recompute of the #1702→#1701→#1700 repair 955b1996)",
    "Naive per-path 3-way merge against original base falsely reported 4 conflicts; real-machinery recompute: all three merges CLEAN, final tree 72f44ba2e4edfca51103f2d7568eacbe84f19238 byte-identical to repair commit remote tree",
    "Negative control: tools/note_bridge.py + scripts/gate-learning-compounding.py ABSENT at broken tip 46179105, PRESENT at repair tip; broken→repair = 34 files (14 added / 20 modified / 0 removed)",
    "CI at repair tip: 19 check-runs, zero failures incl. brain-index drift check; re-verified after tip move (#1710, #1711 → ed82e8b3): +2 files, 0 deletions, all restored files present"
  ],
  "falsifiers": [
    "A naive per-path 3-way merge against the original base used as verification evidence for a sequential merge",
    "Trusting a 'no conflicts' claim without byte-comparing the recomputed tree to the artifact's remote tree",
    "Verifying only the broken→repair delta without the negative control (absence at broken tip)"
  ],
  "applies_to": "git-data API merge verification; sequential PR merge chains; multi-step stateful transformation replay",
  "siblings": ["2026-10-07 AGENTS.md correction — tree=head-tree silently drops base changes (failure mode)", "SN-0128 — merge-base drift in repair basing (basing discipline)"]
}
```
