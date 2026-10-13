# A Repair CI Never Runs Is Unverified, Not Proven — Sequence Repairs in Gate Order

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0764-repair-invisible-behind-fail-fast-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6077062126 (Naya 4 [SELF-BUILD LOOP] sign-in/sign-out, 2026-10-09T08:10:04Z); virgin tip `925e4c34` (codeload tarball, index.json marker byte-verified); repairs #1840 (collection), #1838 (registry drift), #1825 (drive-loop ingestion)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On tip `925e4c34`, CI's visible verdict on the kernel suite was a single FAIL — the pytest collection abort in `tests/test_engineering_gates.py` (`ModuleNotFoundError: No module named 'engineering_gates'`, owned by repair #1840). Because collection aborted, **the whole suite never ran**. Behind the fail-fast gate, a second independent RED waited invisible: `test_live_repository_drift_never_grows_per_class` would have failed (`published_pages_without_registry_entry` 1 → 11, owned by #1838).

The consequence is sharper than "audit what skipped" (SN-0552): the queued merge order (#1840 → #1858 → #1837/#1838) is **load-bearing for verification, not just safety**. #1838's registry-drift heal cannot even be CI-visible until #1840 unbreaks collection — the repair exists, the evidence exists (head index.json + 8 captures applied to the tip tree took the class 11 → 3, exactly the SN-0632..SN-0639 scope, no collateral on any other class, non-vacuous because the test still fails on the residual — #1838 scored 8.0/10) — but CI will never run it until the gate clears. **A repair that CI never runs is unverified, not proven.**

The discipline for a cold successor:
1. When the tip is RED at a fail-fast gate, enumerate what the gate withholds — the visible FAIL names only the first defect.
2. Sequence collection-blocking repairs first; document the order where merge authority reads it (SN-0676).
3. Re-run the verification battery after each gate clears — never call a queued repair "proven" until CI actually ran it.
4. Verify the heal non-vacuously: apply it to the exact tip tree and confirm the residual still fails for exactly the right reasons (no anomaly absorbed).

## 🩷 HUMAN NOTE

Shawn — one verification discipline worth banking from this morning's self-build loop: a repair sitting in the queue behind a broken CI gate is NOT proven, even if the repair itself is perfect. The loop found a real second defect hiding behind the first — the test suite was crashing on a collection error, so it never even ran the test that would have shown the registry drift. Lesson: fix the gate-blocking repair first, and don't call anything "verified" until CI actually ran it. The order isn't arbitrary — it's load-bearing.

## 🟣 CHILD NOTE

Imagine two fixes waiting in line at a broken door. The first fix repairs the door itself; the second fix repairs the thing behind the door. Nobody can check the second fix until the door opens — so the order matters: door first. A fix that hasn't been checked isn't proven, no matter how good it looks.

## 👵 GRANDMA NOTE

Grandma, the team had two repairs ready, but the testing machine was broken in a way that stopped it before it could check the second one. The rule they wrote down: the repair that unbreaks the testing machine goes first, and nothing counts as "verified" until the machine actually ran the check. Being ready is not the same as being proven.

## 🟣 NAYA NOTE

For future merge-queue work: when a tip is RED at a fail-fast gate, (1) run the suite on virgin tip bytes past the abort to enumerate concealed REDs (codeload tarball + byte-verified markers, as #1354/6077062126 did); (2) treat collection-blocking repairs as first in line, document the order on the PR (SN-0676); (3) verify each heal by applying it to the exact tip tree and confirming the failure count moves exactly in its owned scope with no collateral — a still-failing residual on exactly the right pages is non-vacuous evidence (the SN-0420 anti-absorption test). Never promote a queued repair on the strength of its diff alone.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0764",
  "slug": "repair-invisible-behind-fail-fast-gate",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6077062126 (Naya 4, 2026-10-09T08:10:04Z)"},
    {"type": "virgin_tip", "ref": "tip 925e4c34, codeload tarball, index.json marker byte-verified"},
    {"type": "repair", "ref": "#1840 owns the collection abort; #1838 verified 11 -> 3 on the tip tree, non-vacuous, 8.0/10; #1825 owns the SN-0742/43/44 residual"}
  ],
  "lesson": "A repair queued behind a fail-fast collection abort is unverified, not proven: CI never runs it, so sequence collection-blocking repairs first, document the order, and re-verify after each gate clears. Verify non-vacuously: apply the heal to the exact tip tree and confirm the residual fails for exactly the right reasons.",
  "related": ["SN-0236", "SN-0552", "SN-0676", "SN-0420"]
}
```
