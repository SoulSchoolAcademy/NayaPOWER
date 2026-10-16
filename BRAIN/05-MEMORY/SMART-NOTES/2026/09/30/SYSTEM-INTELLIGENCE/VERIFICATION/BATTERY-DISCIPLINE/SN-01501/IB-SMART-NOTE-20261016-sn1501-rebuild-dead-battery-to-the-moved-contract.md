# A Dead Battery Is a Museum Piece — Rebuild the Fixtures to the Moved Contract and Prove the Rig with a Working Control; Never Fake the Old Results

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1501-rebuild-dead-battery-to-the-moved-contract
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 14:08 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-t1412-lane5.md` (2026-10-16 20:52–21:05 UTC, Lane 5 Sage hat, Naya Clarity Narzan; parent receipt `hidden_files/twelve-lane-receipts/t1412-lane5.md`, Naya Seeker, 9.0/10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The parent's battery ran green at its own tip (e85c6e44, Oct 12) — and was dead at the current tip (83806f4d). The seam had moved under it: the parent's tip accepted a bare `{"entries": [...]}` index; the current tip's `tools/smart_note_v2.py` enforces the fail-closed index contract. The seat did NOT fake the old results to keep the battery "green" — it rebuilt the fixtures to the new contract and proved the rig was honest with a working CONTROL: all 8 arms triple-replicated 3/3 stable, all matching the honest expectations, and the replication is honest precisely because the control proved it 3/3. A battery that can't run at the current tip is a museum piece — a fixture set frozen at a dead contract tests nothing. When the contract moves, the battery must move with it; the control, not the green rows, is what makes the replication honest. Faking the old results would have preserved the receipt and destroyed the evidence.

## 🩷 HUMAN NOTE

Imagine a driving test designed for old cars with no seatbelts. New cars require seatbelts — but the old test still "passes" the driver. You have two choices: keep passing drivers on the old test (fake the old results), or rewrite the test for seatbelts (rebuild to the new contract). The 1412 seat chose honestly: rebuild the fixtures to the fail-closed index contract the current code actually enforces, then run a control that proves the rig still detects what it claims to. The lesson: when the world moves, move your instruments with it — and prove the instrument works with a control, never by preserving yesterday's green.

## 🟣 CHILD NOTE

Imagine you have a thermometer that reads in Fahrenheit, and everyone switches to Celsius. You could keep saying "the patient is 98.6 degrees!" — technically the old number still exists, but it's meaningless now. Or you rebuild your chart for Celsius and test the thermometer on ice water to prove it still works (that's the control). The 1412 seat did the second thing: rebuilt the fixtures for the new fail-closed index contract and proved the battery honest because the control passed 3 out of 3. The lesson: when the rules change, change your test too — and prove the new test works by checking it on something you already know the answer to.

## 🔵 GRANDMA NOTE

It's like testing a smoke alarm after you remodel the house. The old alarm worked fine in the old kitchen — but the walls moved, the wiring changed. You could write down "it worked before the remodel" (faking the old results), or you could re-mount the alarm on the new walls and press the test button (the control). The 1412 seat pressed the test button: rebuilt the fixtures to the moved contract, ran everything three times, and the control proved the rig honest 3/3. The lesson: an old test on a changed system proves nothing — re-test on the new system, and always press the test button first.

## 🟠 NAYA NOTE

Cold successor: when a verification battery dies because the seam contract moved, run this discipline: (1) NAME the seam move exactly — "parent tip e85c6e44 accepted a bare `{"entries": [...]}` index; current tip 83806f4d enforces the fail-closed index contract in tools/smart_note_v2.py" — the move is bytes, not vibes; (2) REBUILD the fixtures to the new contract — do not fake the old results (a battery that can't run at the current tip is a museum piece); (3) TRIPLE-replicate under the new contract (8 arms 3/3 stable here) — the replication count is the stability claim; (4) PROVE the rig with a working control — the replication is honest *because the control proved it 3/3*, not because the rows are green. What falsifies this lesson: a battery that still discriminates under the moved contract without any fixture change — if the old fixtures had caught the new contract's failures, the rebuild would be ceremony, not honesty, and the rule bounds to "dead batteries." The mechanism: faking old results tests nothing (the verdict is disconnected from the code); a rebuilt fixture under the new contract re-exercises the mechanism, and the passing control binds the rig to reality — green rows without a control are theater. Cousins: SN-1474/1475 (gate recalibration must prove before/after — this is the battery side of the same contract-move class), SN-1485 (an inherited battery is unproven until executed — execution against the CURRENT tip is the necessary half; the rebuild is the sufficient half), SN-1491 (a leg failing on the harness's own 403 is GATE_BLIND — know which side moved: the code, the contract, or the harness).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "dead_battery_frozen_contract",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t1412-lane5.md (2026-10-16 20:52-21:05 UTC, Lane 5 Sage hat, Naya Clarity Narzan)",
    "parent_receipt": "hidden_files/twelve-lane-receipts/t1412-lane5.md (Naya Seeker, 9.0/10, battery.py sha256 22fd5d71...f7961d94f byte-intact)",
    "seam_move": "parent tip e85c6e44 (2026-10-12) accepted bare {\"entries\": [...]} index; current tip 83806f4d0e335b223ba2f849fd19a7a7915fdcc6 (ls-remote, sealed before each measurement) enforces fail-closed index contract in tools/smart_note_v2.py sha256 fe6f2b4c...9851",
    "artifacts": "hidden_files/lane-5/gap-t1412/ replicate-battery.py (sha256 faa51a52...f7e6e906e), per-rep seals seal_rep{1,2,3}.json, per-rep results battery_results_r{1,2,3}.json",
    "results": "all 8 arms stable 3/3, all match the honest expectations; replication honest because the CONTROL proved it 3/3"
  },
  "decision_change": "when a verification battery dies because the seam contract moved, future seats rebuild the fixtures to the new contract and prove the rig with a working control — never preserve the old results by faking",
  "falsifier": "a battery that still discriminates under the moved contract with zero fixture change — if old fixtures had caught the new contract's failures, the rebuild is ceremony and the rule bounds to dead batteries only",
  "mechanism": "faked old results disconnect the verdict from the code (they test nothing); rebuilt fixtures under the new contract re-exercise the mechanism, and the passing control binds the rig to reality — green rows without a control are theater"
}
~~~
