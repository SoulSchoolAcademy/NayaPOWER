# A Single Gate Run Is Motion — Re-Run and Byte-Compare Before the Verdict

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1681-single-run-is-motion-rerun-and-byte-compare-before-the-verdict
**Smart Note:** SN-1681
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

One run of a gate check is motion, not a verdict: a single exit-1 could be a flake, and a single exit-0 could be a race that silently passed. Before claiming a gate verdict, re-run the check and byte-compare the outputs. t0905 (2026-10-19) ran `tools/regenerate_brain_index.py --check` at pinned tip `1a1c22d3` three times: stdout md5 `a22e4a4c3277b8dd317b3c3227490f37` identical across all three runs, exit 1 every time — only then was DRIFT=STALE claimed. It also byte-pinned the generator (`41daba756288530a00f2542bff525c2d6438a35c`, matching the brief's shipped blob) to close the second confound: the tool moved, not the tree. The scorecard passed at 9.3 → 9.5 → 9.6 on exactly this ladder: single run, determinism closed, confound closed. Cheap re-runs with compared bytes turn an exit status from an anecdote into evidence.

## 🩷 HUMAN NOTE

One coin flip landing heads doesn't make the coin two-headed. Flip it three times, write down each result, and only then say what you know. The third identical result is what buys you the right to the verdict.

## 🟣 CHILD NOTE

If your friend says they beat the video game once, you might believe them. But if they beat it three times in a row and the score is exactly the same each time, now you really know. Same here: run the check more than once and compare, before you say it's true.

## 🔵 GRANDMA NOTE

Dear, a thermometer that blinks once might just be catching the light. Read it three times and make sure the numbers match — then you know what the temperature actually is. A single reading is a guess dressed up as a fact; three matching readings are a measurement.

## 🟠 NAYA NOTE

The concrete instance (2026-10-19, Naya Clarity Narzan, Lane 10 Librarian hat):
- twelve-lane-receipts/t0905-lane10.md: `tools/regenerate_brain_index.py --check` at action-time-pinned tip `1a1c22d32191b8e6ae90db1be58118ad0e33b7b0` (post-fetch re-pin, clean working tree verified first). Run 1: exit 1, DRIFT (3 files: BRAIN/REAL-TREE.json, BRAIN/REAL-TREE.md, BRAIN/NAYAPOWER-BRAIN-INDEX.json). Runs 2–3: exit 1, stdout md5 `a22e4a4c3277b8dd317b3c3227490f37` identical all three — determinism closed, flake confound dead. Generator blob `git hash-object tools/regenerate_brain_index.py` = `41daba756288530a00f2542bff525c2d6438a35c` — byte-identical to the blob the brief shipped: the tool did not move, so the drift is in the tree or the generator's inputs.
- The verdict was reported in the gate's own taxonomy (DRIFT = STALE on the read surface) — not as a re-worded claim about "the brain index being unhealthy."
The ordering matters: run → compare bytes → pin the tool → then verdict. A receipt that shows one run and one exit status is a claim with a confound still alive in it.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1681",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a single run of a gate check is motion, not a verdict; before claiming the verdict, re-run the check and byte-compare the outputs (identical stdout hashes across N independent runs close the flake confound), and byte-pin the tool itself (blob hash vs the shipped value) to close the tool-moved confound — only then does the exit status become evidence",
  "decision_change": "any lane reporting a gate verdict will (1) run the check at least twice and quote the byte-comparison (md5/SHA) of the outputs, (2) pin the instrument's blob hash against the brief's shipped value, (3) state the verdict in the gate's own taxonomy — instead of quoting one exit status as a verdict",
  "falsifiability": "a gate verdict derived from N byte-identical runs that is then proven wrong by the measurement's own design (a deterministic false-negative in the instrument) bounds this rule: re-runs close the flake confound, not the instrument-design confound; a case where re-running is impossible (destructive/one-shot check) names its own exception, not the rule's failure",
  "mechanism": "flake errors are per-run environmental noise; N independent runs producing byte-identical outputs makes identical wrong bytes from independent noise vanishingly unlikely, so agreement across runs isolates verdict truth from run luck; pinning the tool's blob separates tree-drift from tool-drift, which output bytes alone cannot distinguish",
  "applies_when": [["measurement","gate-verdict"], ["verification","determinism"], ["red","flake-confound"]],
  "enforcement": "measurement-receipt review REJECTs any gate-verdict claim whose receipt shows only one run of a check that is cheap to re-run; the receipt must quote >=2 runs with byte-compared outputs (md5/SHA) or name the specific reason re-running is impossible. Check runs on every measurement receipt before sign-out.",
  "evidence": "hidden_files/twelve-lane-receipts/t0905-lane10.md (2026-10-19, 9.6/10): --check at pinned tip 1a1c22d3 run 3x, stdout md5 a22e4a4c3277b8dd317b3c3227490f37 identical, exit 1 x3, DRIFT=STALE claimed only after determinism closed; generator blob 41daba756288530a00f2542bff525c2d6438a35c byte-matched the brief's shipped value, closing the tool-moved confound"
}
~~~
