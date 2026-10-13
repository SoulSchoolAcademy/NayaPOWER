# The Observer Must Not Move the Subject — Telemetry Seams Stay Verdict-Neutral

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0979-telemetry-stays-verdict-neutral
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6109084227 (2026-10-11T12:36:03Z, [NAYA 2 · BUILD LANE] sign-out ~12:45Z, night shift). PR #2342 (`naya2/worker-lifecycle-events-2244d`), head `07ed8c27813c25503cbfb9ac4bd4b1229676d96e`, stacked on #2296 @ `6546cdca`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The worker gates used to die silently: when a shift stood down on the rate-limit flag or a worker exited blocked, that material fact lived only in a run log. The #2244-D wire (PR #2342) fixed the silence by issuing DETECTED learning events through the #2296 canonical envelope from two guarded call-sites in `worker_entry.py` (STAND_DOWN → NOTICE) and `worker_exit.py` (blocked → WARNING) — **without changing any gate verdict or exit code**. The construction makes verdict-neutrality structural, not promised: best-effort and never-raises, kill switch `NAYA_LIFECYCLE_EVENTS=0`, no network, no API, ledger under `.naya/` (drift-free). Proof: 17/17 tests green including absent/broken-envelope subprocess proofs (gates exit 20/0 unchanged) and unpatched-main-bytes negative controls proving no emission without the call-sites; the envelope's own suites still green (34/34).

The durable rule: **instrumentation added to a gate must be physically incapable of changing the gate's verdict.** Telemetry is a passenger, never a driver. The moment an observability seam can alter an outcome — a raise that flips an exit code, a network call that times out a check, a write that fails closed — the instrument becomes a second, unreviewed gate, and every future debugging session must suspect the observer along with the subject. Structural guarantees beat promises: kill switch, never-raises, negative controls on unpatched bytes, subprocess proofs that the verdict survives a dead envelope.

## 🩷 HUMAN NOTE

Shawn — the worker gates used to stand down or exit blocked with no record anywhere but a run log. The #2244-D wire now emits a learning event when that happens — but the build was done so the event can *never* change a gate's verdict or exit code (kill switch, never-raises, proven by tests that kill the envelope mid-flight and watch the gate exit unchanged). Lesson banked: when we add observability to a gate, the instrument must be physically incapable of moving the subject — telemetry rides along, it never drives.

## 🟣 CHILD NOTE

You put a camera on a referee to record the game. But the camera is so heavy it bumps the referee, and the referee makes a different call. Now nobody knows if the call was real or caused by the camera. Rule: when you add a watcher to something important, build it so the watcher *cannot* change what it's watching — a camera that floats and never touches. Then you trust both the game and the recording.

## 🔵 GRANDMA NOTE

It's like putting a thermometer in a pot of soup. If the thermometer is cold enough to cool the soup, the reading lies — you're no longer measuring the soup, you're measuring your own instrument. Build the thermometer so it can never change the temperature: then the reading is honest and the soup is untouched. Same rule for anything we add to watch our gates: it may observe, it may never alter.

## 🟠 NAYA NOTE

Whenever I add observability to a decision path — event emission, logging, metrics — I ask one question before anything else: *can this seam change the verdict?* If the answer is not a structural no, I rebuild it until it is: guarded call-sites, never-raises, a kill switch, and negative controls proving the verdict is identical on unpatched bytes and under a dead/absent envelope. A promise of "it won't affect anything" is not evidence; a subprocess proof that the exit code survives a broken envelope is. The observer must not move the subject — because the day a gate misfires, the first suspect must be the gate, never my camera.

## 🟢 MACHINE NOTE

~~~json
{
  "sn": "SN-0979",
  "title": "The Observer Must Not Move the Subject — Telemetry Seams Stay Verdict-Neutral",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "MEASUREMENT-BOUNDARY"],
  "authority": "distillation tick 2026-10-11 05:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board_comment": "#2175 comment 6109084227 (2026-10-11T12:36:03Z — [NAYA 2 · BUILD LANE] sign-out ~12:45Z, night shift)",
    "pr": "PR #2342 (naya2/worker-lifecycle-events-2244d), head 07ed8c27813c25503cbfb9ac4bd4b1229676d96e, stacked on #2296 @ 6546cdca",
    "mechanism": "worker_entry.py STAND_DOWN → DETECTED blocker (NOTICE); worker_exit.py blocked → DETECTED blocker (WARNING); two guarded call-sites; kill switch NAYA_LIFECYCLE_EVENTS=0; no network, no API; ledger under .naya/",
    "proof": "17/17 tests green incl. absent/broken-envelope subprocess proofs (gates exit 20/0 unchanged) and unpatched-main-bytes negative controls (no emission without the call-sites); envelope suites 34/34 green"
  },
  "rule": "telemetry_seam_is_structurally_verdict_neutral",
  "procedure": [
    "before adding observability to a decision path, ask: can this seam change the verdict? — require a structural no, not a promise",
    "guarantee it with: guarded call-sites, never-raises, a kill switch, no network/API on the seam",
    "prove it with: subprocess proofs that verdicts/exit codes survive a dead or absent envelope, negative controls on unpatched bytes",
    "an observability seam that can alter an outcome is a second, unreviewed gate — every future debug session must then suspect the observer"
  ],
  "related": ["SN-0976 (empty parse fails loud — the fail-closed family; this note is its complement: loud instruments must not steer)", "SN-0528 (never attest with a literal)"]
}
~~~
