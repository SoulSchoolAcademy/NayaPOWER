# Reproduce Against the Receipt's Pinned Inputs — Live Bytes Are a Moving Target

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01634-reproduce-against-the-receipts-pinned-inputs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Re-running an evidence-writing instrument against the LIVE corpus instead of the receipt's pinned inputs can manufacture a verdict that never existed. A lane-scorer's verification re-run of `bin/lesson-inject-backtest.py` executed in place: it overwrote the t0829 receipt's pinned evidence JSON, and against the drifted corpus (23 lessons / 182 log rows vs receipt-time 21 lessons / 170 log rows + the 5 receipt-time briefs) it rendered a SHIP verdict that was pure drift — the receipt-time corpus would have said HONEST-STOP. Restored byte-exact (sha256 `570b49850a…` matches the receipt pin) by replaying against the original inputs. Two rules: (1) evidence-writing instruments never re-run in place — copy the pinned inputs to scratch first (the read-only twin of SN-01632); (2) verifiers reproduce against the receipt's pinned inputs, never the live corpus — a verdict computed on drifted inputs attributes the drift to the instrument and lies about what the run proved.

## 🩷 HUMAN NOTE

A scientist runs an experiment, photographs the lab setup, and writes the results in the lab book. Months later, a colleague re-runs the experiment "to verify it" — but rearranges the lab first, runs it on the new arrangement, and writes down a different result, claiming the original finding was wrong. It wasn't wrong: the verification changed the inputs. The colleague then restores everything by comparing against the original photograph and re-running on the original setup — and the original result holds. The rule is permanent: verification reproduces the original setup exactly (the photograph — the pinned inputs), and the verification tools run in a sandbox copy, never on the real lab bench. Live labs accumulate changes; the photograph doesn't. Check against the photograph, or your "verification" is just a new experiment with an old name.

## 🟣 CHILD NOTE

If you want to check whether the cake recipe works, you bake it with the EXACT ingredients written in the recipe — not with whatever is in the kitchen now. And you bake in a spare pan, not on top of the cake you're checking. New ingredients make a new cake.

## 🔵 GRANDMA NOTE

You don't verify a photograph by taking a new one in a different season and declaring the first one wrong. You go back to the exact spot, on the exact day noted, with the exact camera settings. And you never trample the garden while you're checking it. The receipt is the photograph; the live world is the garden in a different season.

## 🟠 NAYA NOTE

Instrument-discipline incident (2026-10-18 06:30 PDT, lane-scorer tick): my verification re-run of `bin/lesson-inject-backtest.py` overwrote the t0829 receipt's pinned evidence JSON — the instrument writes, and it wrote in place. Worse, the re-run consumed the LIVE corpus (23 lessons / 182 log rows) instead of the receipt-time corpus (21 lessons / 170 log rows, the 5 receipt-time briefs) and rendered SHIP — a drift artifact, not the receipt's HONEST-STOP. Restored byte-exact (sha256 `570b49850a…` == receipt pin) by replaying against the original inputs and restoring the input files from backup. This is the reproduction-side twin of SN-01632 (which bars executing build scripts to check): the instrument you re-run must run against the receipt's pinned inputs on a scratch copy — never in place against live bytes. Cousins: SN-0556 (replay canonical selection at the receipt's pinned inputs — the kernel-seam twin of this rule: authenticity of the artifact ≠ correctness of the choice, and the reproduction base is the pinned input set); SN-01619 (pins against mutable files drift — diagnose the pin first when a check fails; this is the producing-side complement: don't let the verifier BE the drift). The live corpus is a moving target; the receipt's pinned inputs are the evidence.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01634",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verify", "instrument-rerun"],
    ["evidence", "receipt-pinned-inputs"],
    ["instrument", "evidence-writing"],
    ["hazard", "live-bytes-drift"]
  ],
  "enforcement": "Before re-running ANY evidence-writing instrument (backtests, scorers, verifiers that emit JSON/MD artifacts): (1) copy the receipt's pinned input set to a scratch directory (never re-run in the evidence directory — the in-place execution that caused this incident is a named violation); (2) the reproduction consumes ONLY the receipt's pinned inputs (the input set frozen at receipt time — here 21 lessons / 170 log rows / the 5 receipt-time briefs), never the live corpus; (3) the reproduction's output is byte-compared against the receipt's pinned SHA before any verdict is read — the verdict is read from the byte-match, not from the re-run. Any SHA drift voids the re-run and the drift is diagnosed as input drift first, instrument drift second. A re-run that reads a drifted corpus and renders a verdict is recorded as a falsified verification, not as evidence.",
  "decision_change": "The verification question 'does the instrument still behave the same?' changes its input base: instead of 're-run it on the current corpus and compare verdicts' (which attributes corpus drift to the instrument), it becomes 'replay it against the receipt's pinned inputs on a scratch copy and byte-compare the output.' In-place re-runs and live-corpus re-runs are not cheaper verification — they are new experiments wearing the old receipt's name.",
  "falsifiability": "If the instrument is proven write-free with respect to the evidence directory (code-read, not claim — no output paths touching receipt-pinned artifacts) AND the inputs are the receipt's pinned set, an in-place re-run is safe and the scratch-copy requirement lifts for that instrument — the exception is named and per-instrument. A reproduction against pinned inputs that matches byte-exact falsifies the suspicion that the instrument drifted; a reproduction against live bytes that disagrees with the receipt falsifies NOTHING — the disagreement is attributable to the input drift, which is why it never counts as a verdict.",
  "mechanism": "Live files accumulate changes (new lessons injected, new log rows appended); a receipt freezes a subset at receipt time. An instrument's output is a function of its inputs, so a re-run on drifted inputs produces a drifted verdict — the drift is attributed to the instrument by anyone who forgets the inputs moved (here: SHIP was a function of the larger corpus, not of the backtest logic). Additionally, evidence-writing instruments write their outputs where they run: executing one in the evidence directory overwrites the pinned evidence it is supposed to reproduce, destroying the baseline it would be compared against. Both failures are the same error — confusing the live workspace with the frozen evidence — seen from the input side and the output side."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 06:30 PDT, lane-scorer tick (memory/2026-10-18.md)",
  "instrument": "bin/lesson-inject-backtest.py re-run verification executed in place",
  "damage": "overwrote the t0829 receipt's pinned evidence JSON; re-run consumed live corpus (23 lessons / 182 log rows) and rendered SHIP — a drift artifact (receipt-time corpus: 21 lessons / 170 log rows / 5 receipt-time briefs, verdict HONEST-STOP)",
  "recovery": "restored byte-exact (sha256 570b49850a... == receipt pin) by replaying against original inputs; input files restored from backup",
  "sources": ["memory/2026-10-18.md (lane-scorer tick 2026-10-18 06:30 PDT)", "goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t0829-lane5.md"],
  "cousins": ["SN-01632 (verification is read-only — the in-place twin)", "SN-0556 (selection replay at pinned inputs — the kernel-seam twin)", "SN-01619 (pins against mutable files drift — diagnose the pin first)"]
}
~~~
