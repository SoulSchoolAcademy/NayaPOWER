# Fail-First CI Topology Converts Secondary REDs into Invisible Skips — Audit What Skipped Behind the RED

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0552-fail-first-topology-conceals-secondary-reds
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6042026672 ([DRIVE LOOP] Tip moved — #1737 index heal verified, one latent RED left standing, 2026-10-07T16:18:55Z); virgin tip `aea25885`; PRs #1737/#1738

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The drive-loop re-verification of tip `aea25885` (virgin, depth-1, rev-parse confirmed) closed the #1737 index heal but exposed a **latent RED that CI never showed**: `tests/test_smart_note_registry_drift.py::test_live_repository_drift_never_grows_per_class` still fails (`published_pages_without_registry_entry`: 2 vs pinned 1 — the unregistered page is a duplicate SN-0522 copy sitting under `GOVERNANCE/OPERATING-DOCTRINE/` while the registered copy lives under `GOVERNANCE/PRIME-JUDGMENT/`). The latent RED was CI-masked because the pytest step **skips behind the node failure** — the visible RED (the `_shared` edge-coverage failure from #1735) gates the job that would have reported the second one. So on a RED tip, the job you most need to see is exactly the one CI withholds.

Why this is brain-grade and genuinely new: SN-0421 says a run-level SUCCESS with skipped behavioral jobs is vacuous (don't treat skips as proof). SN-0442 says a skip is neither proof nor failure — read its cause (don't treat skips as failure). This note completes the triad from the other side: **on a RED tip, a skip behind the failing job can conceal an independent RED** (treat the skip as a hiding place, not as either verdict). The fail-first topology converts secondary failures into invisible skips. The discipline: when the tip is RED, never assume the visible RED is the only RED — enumerate what skipped behind it and run the most diagnostic skipped jobs locally (as the drive loop did on virgin `aea25885`). The heal path it produced is itself governed: SN-0522 adjudication (owning lane: name the canonical copy, register it) → #1738 rebases onto `aea25885` → merges green → main goes green → the fail-closed promotion gate (SN-0438, working as designed) unblocks.

## 🩷 HUMAN NOTE

Shawn — one more CI lesson from this tick's drive loop, and it completes a family. We know skips aren't proof of anything (SN-0421) and aren't failure either (SN-0442). Now the third one: on a red build, the tests that *didn't run* can be hiding a second red. That's what happened this morning — the visible red (a Node coverage failure) blocked the Python test step, and that step was hiding its own independent failure: an unregistered duplicate of Smart Note SN-0522 sitting on main. A local re-run on the exact tip caught it; CI never showed it. The rule: when the build is red, don't just fix the red you see — go look at what didn't run behind it.

## 🟣 CHILD NOTE

Imagine a fire alarm goes off and the teacher says "everyone out" — but one classroom's door never opened, so nobody knows if there's smoke in there too. You wouldn't say that classroom is safe just because you can't see smoke; you also wouldn't say it's on fire. You'd go open the door. That's this lesson: when one test fails and the rest don't run, go open the doors that stayed shut — one of them had a second fire.

## 👵 GRANDMA NOTE

A hospital's first test comes back bad, so the doctor cancels the rest of the tests — and the canceled one was the one that would have found a second problem. You don't assume the canceled test was fine, and you don't panic about it either. You reschedule it. Our new rule: on a failing build, the skipped tests get rescheduled and run by hand — because the one that didn't run is exactly the one that could be hiding something.

## 🧠 NAYA NOTE

Cold successor: when the tip is RED, add one step before you declare the RED's class (SN-0236/SN-0240). (1) Enumerate every job that skipped **behind** the failing job. (2) Run the most diagnostic skipped ones locally on the virgin tip (or prove their skip is by design per SN-0442 — parity/authorization gates are correct no-ops; fail-fast topology is NOT by design for diagnostic jobs). (3) Any secondary RED found gets its own classification and its own heal path — never folded into the first RED's repair (here: the registry-drift RED belongs to the SN-0522 owning lane's adjudication, not to #1738's coverage-gate fix; #1738 was correctly NOT a content problem, just blocked upstream). (4) The promotion gate firing closed on a knowingly-RED tip is the design working (SN-0438) — name the RED it is reacting to, don't treat the gate as the incident. Template: the drive-loop comment 6042026672 — virgin-tip re-verification, explicit heal ordering (adjudicate → rebase → merge green → unblock).

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0552",
  "title": "Fail-First CI Topology Converts Secondary REDs into Invisible Skips — Audit What Skipped Behind the RED",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "SKIP-DISCIPLINE"],
  "cousins": ["SN-0421", "SN-0442", "SN-0438", "SN-0236", "SN-0240"],
  "evidence": {
    "board": ["#1354 6042026672 ([DRIVE LOOP] Tip moved — #1737 index heal verified, one latent RED left standing, 2026-10-07T16:18:55Z)"],
    "virgin_read": "depth-1 clone at aea25885, rev-parse confirmed; tools/regenerate_brain_index.py --check PASS (233 files); #1737 touched exactly 3 files (BRAIN/NAYAPOWER-BRAIN-INDEX.json, REAL-TREE.json, REAL-TREE.md)",
    "latent_red": "tests/test_smart_note_registry_drift.py::test_live_repository_drift_never_grows_per_class STILL FAILS: published_pages_without_registry_entry 2 vs pinned 1; unregistered page = duplicate SN-0522 copy at BRAIN/05-MEMORY/SMART-NOTES/2026/10/07/SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-DOCTRINE/SN-0522/; registered copy at .../GOVERNANCE/PRIME-JUDGMENT/SN-0522/",
    "masking": "pytest step skips behind the node failure (the _shared edge-coverage RED from #1735) — CI never surfaced the secondary RED",
    "heal_path": "SN-0522 owning-lane adjudication (name canonical copy + register) -> #1738 rebases onto aea25885 -> merges green -> main goes green -> fail-closed promotion gate unblocks; #1738's node --test already PASSING on the branch (fix works; pytest failure is base-inherited, not a content problem)"
  },
  "doctrine": {
    "triad": "SN-0421: skips are not proof. SN-0442: skips are not failure — read the cause. This: on a RED tip, skips behind the failing job can conceal independent REDs — audit the hiding place.",
    "fail_first_concealment": "fail-first CI topology converts secondary failures into invisible skips; the job you most need to see is the one the topology withholds",
    "discipline": "on a RED tip, enumerate what skipped behind the failing job and run the most diagnostic ones on the virgin tip; never assume the visible RED is the only RED",
    "own_lane_owns_adjudication": "the duplicate SN-0522 is adjudicated by its owning lane (SN-0522 lane), not folded into #1738's repair — one repair per RED class (SN-0236)",
    "gate_working": "the Governed Production Promotion gate firing closed on the knowingly-RED tip is SN-0438 design working — name the RED it reacts to, never treat the gate as the incident"
  },
  "rule": "a RED tip gets its skips audited: enumerate what skipped behind the failing job, run the diagnostic ones on the virgin tip, and classify each secondary RED on its own — the visible RED is never assumed to be the only RED"
}
```
