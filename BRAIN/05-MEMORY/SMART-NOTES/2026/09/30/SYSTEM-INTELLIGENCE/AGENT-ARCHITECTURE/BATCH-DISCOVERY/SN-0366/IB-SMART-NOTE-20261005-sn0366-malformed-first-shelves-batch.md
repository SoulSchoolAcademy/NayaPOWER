# One Malformed Capture Shelves the Whole Batch — the R8 Boundary on Per-Capture Isolation

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0366-malformed-first-shelves-batch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5997303283 ([NAYA 4][SUBAGENT SIGN-OUT], 2026-10-05T15:11:40Z / 08:11 PDT): 8-rung multiple-learning reproduction on pinned main@bf4c8e9b, rungs 1-7 PASS, R8 FAIL. RED test: ~/workspace/multi-learn-repro/harness/test_batch_isolation_red.py — test_malformed_first_does_not_shelve_valid_capture FAILS on the pin; 2 companions pass; no fix implemented (per brief, separate work item). Related: SN-0334 (discovery abort on multiplicity — different seam).
**Renumbered SN-0355 → SN-0366 on 2026-10-05 by lane arbitration (Naya 4):** a second, unrelated note (Naya 2's NONSTOP LOOP operating code) was merged to main as SN-0355. The merged note keeps SN-0355 (canonical main, CI-referenced, director-pushed); this draft-branch note renumbers. First staged claim is relinquished to the merged note; content unchanged.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The multiple-learning experiment climbed the 8-rung ladder with a full lifecycle per rung (capture → batch discovery → registry → KNOW retrieval → behavior vs control → independent recomputation), plus an adversarial retrieval-interference probe — rungs 1–7 PASS. Rung 8 found a real boundary: **a malformed capture sorting before valid captures aborts the ENTIRE batch.** The workflow batch loop (`live-intelligence-commit-proof.yml` ~L100–110) runs under `set -euo pipefail`; one malformed capture's JSONDecodeError kills the step, so the valid captures are never processed. Proven empirically: batch [malformed, valid] → exit 1, valid never processed; control [valid] alone → processed, exit 0.

The defect contradicts `changed_capture`'s own docstring promise — "fail-fast instead on any *individual* capture that is malformed" — because the implementation is fail-fast-*batch*, not fail-fast-individual. One bad capture shelves good intelligence, the exact failure the docstring says will not happen. The repair principle (not implemented): per-capture error isolation in the batch loop (try/catch per capture, record the failure loudly, continue the batch) — or extract the loop into a tested Python function. Owner: whoever owns `live-intelligence-commit-proof.yml`. The RED test is the acceptance gate. No action needed from Shawn.

Why this is brain-grade: "shelved intelligence" is the original sin the capture pipeline was built to prevent, and here it reproduces through a two-character mechanism (`set -e` + an unguarded loop). A cold Naya reading the docstring would trust the promise; this note teaches her to distrust the promise until the loop is proven. The boundary was found by the falsifier discipline — per-rung controls in fresh processes, no fix until the RED test exists — and the fix was deliberately NOT implemented (brief: finding the boundary and writing the RED test was the work item), which is the correct separation: a RED test without a premature fix stays an honest instrument.

## 🩷 HUMAN NOTE

Shawn — the learning-loop stress test found a real boundary: if a malformed capture file sorts before good ones, the pipeline's batch step dies on it and *none* of the good captures get processed — good intelligence gets shelved by one bad file. That's the opposite of what the code promises. There's a failing test that pins it exactly (test_malformed_first_does_not_shelve_valid_capture), and deliberately no fix yet — the fix is a separate work item with its own owner. Finding the boundary cleanly was the job; fixing it is the next one.

## 🟣 CHILD NOTE

Imagine a teacher collecting homework from a line of kids. The rule is supposed to be: "if one kid's paper is scribbled, keep collecting everyone else's." But the teacher actually stops the whole line at the first scribbled paper and sends everyone home — the kids with perfect homework never get theirs collected. The rule written on the wall was right; the teacher just didn't follow it. The fix is simple: when you hit a bad paper, write the kid's name down and keep moving down the line.

## 👵 GRANDMA NOTE

Think of a sorting machine at the post office that's supposed to set aside torn envelopes and keep delivering the good mail. Instead, one torn envelope jams the whole machine and *all* the mail piles up behind it — nobody's letters get delivered. The instruction manual promised it would set bad envelopes aside and keep going, but the machine was never taught how. The fix: teach it to set the bad ones aside loudly (a note on each one) and keep sorting the rest.

## 💜 NAYA NOTE

Note to future me: docstring promises about error behavior are folklore until the loop is proven. When you see a batch loop under `set -euo pipefail` touching untrusted inputs, the first question is always "what happens when item N is malformed — does item N+1 still process?" The answer here was no, proven empirically with a control. Related but different: SN-0334 is the discovery-seam abort (return the set, never abort on multiplicity); this note is the batch-seam abort (isolate per capture, never abort the batch on one malformed item). Also note the discipline: the worker ran the full 8 rungs with per-rung falsifiers, found the boundary, wrote the RED test, and did NOT implement the fix — "fix is a separate work item" is the honest separation between boundary-finding and repair. Don't collapse them.

## ⚙️ MACHINE NOTE

{"sn": "SN-0366", "title": "One Malformed Capture Shelves the Whole Batch — the R8 Boundary on Per-Capture Isolation", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "AGENT-ARCHITECTURE", "BATCH-DISCOVERY"], "extends": [], "related": ["SN-0334"], "evidence": {"board": "#1354 5997303283 ([NAYA 4][SUBAGENT SIGN-OUT], 2026-10-05T15:11:40Z): rung 8 FAIL — batch [malformed, valid] -> exit 1, valid never processed; control [valid] -> processed, exit 0; seam: live-intelligence-commit-proof.yml ~L100-110 under set -euo pipefail; contradicts changed_capture docstring 'fail-fast instead on any individual capture that is malformed'", "pin": "bf4c8e9b", "red_test": "~/workspace/multi-learn-repro/harness/test_batch_isolation_red.py::test_malformed_first_does_not_shelve_valid_capture FAILS on pin, 2 companions pass; fix NOT implemented (separate work item)", "owner": "owner of live-intelligence-commit-proof.yml; no action from Shawn"}, "rule": "a batch loop under set -e is fail-fast-batch, not fail-fast-individual — never trust a docstring promise of per-item isolation until the loop is empirically proven; per-capture isolation (try/catch per capture, record loudly, continue) or extract to a tested Python function; the RED test is the acceptance gate"}
