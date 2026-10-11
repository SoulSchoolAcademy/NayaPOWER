# The Door Nobody Walks Through — a Monitoring Gate That's Never Called Is an Open Door Wearing a Lock

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1004-door-nobody-walks-through
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 12:08 PDT distillation tick (2026-10-11) from #2175 comment 6112432337 ([NAYA 2 VERIFY sign-out — T-07 delayed-harm observation windows, PR #2356], 2026-10-11T18:47:29Z), read live. Full evidence: hidden_files/t07-verify-20261011.md. Live bytes: PR #2356 head a02ec577, main tip c510d743.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's independent verify of PR #2356 (T-07, delayed-harm observation windows) proved a real gap empirically: with the review date 1 hour overdue, zero reports filed, and `review()` never called, `execution_permitted` still returned `(True, "")` — execution proceeds with NO monitoring evidence at all. The door function is correctly written: `review()` would PAUSE on MONITORING_FAILURE. But `execute_plan` NEVER calls `review()` — zero `.review(` call sites in `act_pipeline.py`. The gate checks the door's *state* (due dates, filed reports), not its *invocation*: it never fires because nobody walks through it. Zero of the 32 passing tests cover this — every test knocked on the door, none watched whether the pipeline opened it. The lesson: when you build an enforcement mechanism, verify the CALL path, not just the mechanism. Existence of a gate function ≠ enforcement. Test the overdue-and-unreviewed path end to end: stale review date + no reports filed must yield PAUSE, on live pipeline bytes, or the lock is decorative.

## 🩷 HUMAN NOTE

It's like installing a perfect smoke detector — and then never putting batteries in it. Every inspection of the detector says "flawless circuitry, would alarm at any smoke." But nobody ever wired it to the alarm panel, so when the kitchen fills with smoke the house stays silent. The detector isn't broken; it's just never consulted. Same here: the monitoring function is perfect, all its own tests pass — but the main pipeline never calls it. The protection exists on paper only.

## 🟣 CHILD NOTE

Imagine the school makes a perfect hall pass — fancy stamp, hologram, impossible to forge. But nobody ever stands at the hallway door to check it. Every kid could walk the halls during class and the beautiful hall pass wouldn't stop anyone, because the checker is never at the door. The pass is perfect; the checking never happens. That's what happened: a perfect "stop" button that the machine never presses.

## 🔵 GRANDMA NOTE

It's like buying the finest deadbolt ever made and leaning it against the doorframe instead of installing it. If you test the lock itself, it clicks beautifully — strongest lock in the store. But a burglar walks right past it because nobody put it in the door. The work wasn't building the lock; it was screwing it into the door. When the team builds a safety check, the check has to be *used* by the system, not just *available* to it.

## 🟠 NAYA NOTE

Apply this every time you build or verify an enforcement/monitoring mechanism: (1) grep the pipeline for actual call sites of the enforcement function — a function with zero callers is a decoration; (2) test the invocation path, not the mechanism in isolation: drive the pipeline to the state where enforcement should bite (overdue review date + zero filed reports) and assert the pipeline actually refuses/pauses; (3) count test coverage of the *call*, not just the function — here 32/32 tests passed and 0 covered the missing call; (4) when a verify finds a door like this, name it plainly as a mechanism gap with a refinement TODO (as Naya 2 did: T-07-VERIFY refined in MASTER-TODO.md for the build lane), scored honestly (8.x, not green-washed); (5) never let "the function is correct" stand as the whole verdict — the verdict is "the function is correct AND the pipeline cannot pass without calling it."

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "enforcement_mechanism_never_invoked",
  "evidence": {
    "board_comment": "6112432337 — [NAYA 2 VERIFY sign-out — T-07 complete] (2026-10-11T18:47:29Z): 'review date 1h overdue + zero reports filed + review() never called → execution_permitted returns (True, \"\") — execution proceeds with NO monitoring evidence. The door is status-only (checks neither due dates nor filed reports); review() correctly PAUSEs on MONITORING_FAILURE but execute_plan NEVER calls review() (zero .review( calls in act_pipeline.py). 0 of 32 tests cover this.'",
    "verify_artifact": "hidden_files/t07-verify-20261011.md — full empirical evidence; verify lane's independent worktree wt-verify-t07-2356 at exact PR head a02ec577; 32/32 new tests + 108/108 no-regression slice PASS",
    "wire_location": "act_pipeline.py L678–757 (observation gate after Law 11), execute_plan door at L973 — fail-closed on missing/retroactive/unregistered/PAUSED/STOPPED, but review() call absent",
    "refinement": "T-07-VERIFY TODO refined in MASTER-TODO.md (build lane); scorecard 8.x — mechanism sound, invocation gap open"
  },
  "rule": "verify_the_call_path_not_just_the_mechanism",
  "procedure": [
    "for every enforcement/monitoring mechanism, grep the pipeline for its actual call sites — zero callers = decoration",
    "drive the pipeline to the enforcement-triggering state (overdue + unreviewed) and assert it refuses/pauses on live bytes",
    "count test coverage of the invocation, not just the function; a fully-tested function with zero call-path tests is unverified",
    "name invocation gaps as mechanism gaps with a refinement TODO — never let 'function is correct' be the whole verdict"
  ],
  "related": ["SN-0998 (novel vectors from a different seat — verify must falsify, not re-confirm)", "SN-0996 (fallback doctrine — enforcement machinery must exist, not be assumed)"]
}
~~~

---
*DRAFTED 2026-10-11 12:08 PDT — CANDIDATE, NOT RATIFIED. Only Shawn ratifies. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/10/11/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-1004/IB-SMART-NOTE-20261011-sn1004-door-nobody-walks-through.md. Rides draft PR #1825 (naya4/smart-notes-2026-09-30) — never merge.*
