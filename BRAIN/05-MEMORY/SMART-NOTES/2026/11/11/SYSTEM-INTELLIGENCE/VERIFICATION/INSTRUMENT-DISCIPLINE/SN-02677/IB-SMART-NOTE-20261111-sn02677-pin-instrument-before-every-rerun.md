**Intelligent Block:** IB-SMART-NOTE-20261111-sn02677-pin-instrument-before-every-rerun
**Smart Note:** SN-2677
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 21:38 PST. Evidence: receipt hidden_files/twelve-lane-receipts/gap-gap-lane-scorer-20261018-1610-lane12.md (Lane 12, 9.4/10, filed 2026-11-12T05:17Z) + runner sha/mtime verified first-hand + CORE-PRINCIPLES.md CANDIDATE 1024 (same lesson as a principle, no SN yet). Pre-number check: counter last line 2675; learn/lessons.md max SN-2675 ingested; no SN-2676/2677/2678 in lessons.md or ingestion-log.md; open PRs checked via App route (2 open, none Smart Note); #1354 capped at 2500 comments-disabled, no GitHub comment fetch per cheap check; branch claim check by stage_smart_note.py.

## ✦ IN A NUTSHELL

Verify the instrument first, every time: pin the instrument's sha before every re-run; the re-run proves the world, the pin proves the instrument. The Lane 12 seat sha-pinned run_pilot12_battery.py before two consecutive re-runs because the parent had — and the pin caught the runner changed after the parent's verification (dc228b5f → d5835794, mtime 2026-10-18 23:40:55 UTC, 12 minutes after the parent run ended). The F6 bytes are intact and byte-identical to the parent's quotes; the rest of the diff is unrecoverable — no second copy exists on disk. The seat did not edit the runner and did not restore bytes it could not verify; the drift answer is owed by the battery owner. A drifted instrument is named as a hole, never run past silently. Without the pin, the seat would have filed "F6 clear, all shas match" on bytes never actually compared.

## 🩷 HUMAN NOTE

Shawn — before re-running a test to prove the world is fine, the seat checked the test itself — and caught that the test program had changed twelve minutes after the last verified run. The check's own answer was still right, but the tool that produced it was no longer the tool that was verified. The rule from now on: pin the instrument before you run it, check it again after, and if it drifted, say so out loud instead of filing a clean verdict over it. A true measurement on a drifted instrument is still unverified.

## 🟣 CHILD NOTE

Imagine you use a ruler to prove your tower is exactly as tall as yesterday. But someone swapped your ruler for a slightly different one while you weren't looking. Your tower might be fine — but your ruler can't prove it anymore, because it's not the ruler you measured with yesterday. So now the rule is: before you measure, write down your ruler's secret code, and check the code again after. If the code changed, you say so — you don't just write down "tower is fine."

## 🔵 GRANDMA NOTE

Dear, a seat went to double-check some work, and before running the test she wrote down the test program's fingerprint — just as the last seat had done. Good thing she did: the program had changed twelve minutes after the last check, and nobody knew what had changed in it. The part that mattered was untouched, but she refused to pretend the rest was verified when she couldn't see it. So the rule is: check the tool before you trust its answer, and if the tool moved, name it plainly. A good answer from a changed tool is still an unverified answer.

## 🟠 NAYA NOTE

The verified facts: (1) The Lane 12 seat pinned hidden_files/run_pilot12_battery.py before two consecutive re-runs (full --arm semantic-t0426, both exit 0) because the parent did — and the pin caught drift nobody had named: runner sha dc228b5f → d5835794, mtime 2026-10-18 23:40:55 UTC, 12 minutes after the parent run ended (23:28). (2) The F6-relevant bytes are intact and byte-identical to the parent's quotes (L168 print, L201 comment, F6 assignment — verified by read); the rest of the diff is unrecoverable from available bytes — no prior copy exists on disk (find over /tmp + ~/workspace found no second copy; the parent's /tmp evidence is gone). (3) The seat did not edit the runner and did not restore bytes it could not verify. What changed in the rest of the file, and who changed it, is UNKNOWN — owed by the battery owner / second seat. (4) The re-runs themselves are clean: logs byte-identical, both print `F6: clear (byte-identical=True)`, cold shas match the parent's 2365ff4e, sealed verdict untouched — the verdict stands, the instrument does not. (5) Distinction from the pin family: SN-0429 pins the tool version against CI's ratchet floor; SN-1352 pins every free parameter in a battery manifest; SN-0586 verifies the instrument rather than the receipt. This note is the re-run instance: pin the runner itself, before the run and after it, and a drift found by the pin is a filed hole, not a silent pass. (6) Honest scope: the pin caught one drift; it does not prove no other instrument drifted unnoticed. Recorded as CORE-PRINCIPLES.md CANDIDATE 1024 (learning event, 2026-11-11-21); this note is its Smart Note form — no SN existed for it before this staging.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2677",
  "slug": "pin-instrument-before-every-rerun",
  "title": "Verify the instrument first, every time: pin the instrument's sha before every re-run; the re-run proves the world, the pin proves the instrument",
  "observation": false,
  "applies_when": [["rerun", "instrument-pin"], ["battery", "runner"], ["verification", "reproduction"]],
  "enforcement": "No re-run verdict is filed without a pre-run instrument pin (sha + mtime) and a post-run re-check; a drifted instrument is filed as a named hole, and a clean verdict filed over a known drift fails this note's check. Bytes that cannot be verified are not edited or restored.",
  "evidence": "Receipt hidden_files/twelve-lane-receipts/gap-gap-lane-scorer-20261018-1610-lane12.md (Lane 12, 9.4/10, filed 2026-11-12T05:17Z): the seat pinned run_pilot12_battery.py before two consecutive re-runs (full --arm semantic-t0426, both exit 0) and the pin caught the runner changed after the parent's verification — dc228b5f -> d5835794, mtime 2026-10-18 23:40:55 UTC, 12 minutes after the parent run ended; F6 bytes intact and byte-identical to the parent's quotes, the rest of the diff unrecoverable (no second copy on disk). The seat did not edit the runner and did not restore bytes it could not verify; the drift answer is owed by the battery owner. Also CORE-PRINCIPLES.md CANDIDATE 1024.",
  "decision_change": "Every future re-run starts with an instrument pin (sha + mtime) and ends with a re-check; a verdict on a drifted instrument is filed as a named hole, never as a clean pass. Without this note, seats file 'all shas match' on bytes they never actually compared.",
  "falsifier": "A future re-run that pins the instrument, finds it drifted, and files a clean verdict anyway — or a drift that the pin fails to catch — shows the rule as stated does not hold; if the battery owner proves the 23:40 change was a no-op on the measured path, the drift hole closes but the pin rule stands.",
  "cousins": ["SN-0429 (a branch's exact-pinned tool can lag the ratchet-floor version — tool-version pin, different seam)", "SN-0586 (verify the instrument, not the receipt)", "SN-1352 (pin every free parameter in the battery manifest — manifest parameters; this note pins the runner itself before the run)", "SN-2676 (falsifier line verbatim or unverified — same receipt, sibling rule: 2676 governs the report wording, this note governs the instrument)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
