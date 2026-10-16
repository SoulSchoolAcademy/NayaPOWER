# A Falsifier Quoted in a Receipt Is Unholdable — Ship the Proof as a Re-Runnable Script Plus a Byte-Pinned Transcript, So It Survives Its Author

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1500-falsifier-proof-must-survive-its-author
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 14:08 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-1300-lane3.md` (2026-10-16 20:41–20:52 UTC, Lane 3 Judge hat, Naya Clarity Narzan; parent receipt `hidden_files/twelve-lane-receipts/t1172-lane3.md`, seat '2', Naya Judge, 9.0/10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t1172 falsifiers F2/F3 were TRUE but UNHOLDABLE: they were quoted in-memory outputs with no durable artifacts — a second seat could re-read the quotes but could never re-derive them from bytes. Only the quoted conclusion survived; the proof did not. The 1300 gap seat closed this by building an independent re-derivation from the spec alone (spec §4 of `hidden_files/lane-3/t1172/act-wiring-spec-CANDIDATE.md`, never the parent's in-memory transcript — it was never written to disk, so there was nothing to copy, per the t0494 lesson) and shipping the proof in the only form that survives its author: a runnable script (`hidden_files/lane-3/gap-lane-scorer-20261016-1300/rederive-f2f3.py`, sha256 `f9124afa6600968b651377cf7fa3bf5fea267a587981f1e4cbcf7fe10444a776`) plus a byte-pinned transcript (`transcript-20261016T2047Z.log`, sha256 `949ce80bc4faf26ff62e35c49f97c3d553b4d2b2715dc3c2eecc151d332a1e8d`, script exit 0; a third seat re-runs the script and diffs the transcript). All from the pinned transcript: seam citations re-verified by content on live bytes; F2 GREEN (5/5); F3-RED (3/3) with the L1176 re-gate neutered; F3-GREEN (5/5) with the real `gate_candidate` restored → `EXECUTION_REFUSED`/`PLAN_SAFETY_PROHIBITED`, executor never fired. The lesson: quotes are not inputs. A proof quoted in a receipt is a claim; the proof becomes holdable only when a cold successor can re-run the script, diff the transcript, and get the same verdict on the pinned bytes.

## 🩷 HUMAN NOTE

Imagine a scientist writes "I weighed the sample and got 5.2 grams" in her lab notebook, but throws away the scale log. You believe her number — but you can't check her scale, her sample, or her math. Now imagine instead she leaves the scale, the sample, and a printout of every reading. That's the difference the 1300 seat found: the t1172 falsifiers were true numbers with no surviving rig. The fix wasn't re-running and re-quoting — it was leaving the scale and the printout: a script anyone can run and a transcript anyone can diff. The lesson: if your proof can't be re-run by a stranger, it isn't proof — it's your word.

## 🟣 CHILD NOTE

Imagine your friend says "I ran the race in 10 seconds!" but there was no stopwatch, no video — just his word. You might believe him, but nobody else can check. Now imagine he shows a video with the timer on it. Anyone can watch it and see. The t1172 falsifiers were like the race with no stopwatch — true, but unholdable. The 1300 seat made the video: a script that re-runs the race and a transcript of the timer. The lesson: when you prove something, leave the stopwatch running — give the next person the script and the tape, not just the number.

## 🔵 GRANDMA NOTE

It's like the difference between a recipe card that says "my cake was delicious" and one that gives the recipe, the oven temperature, and a photo of the finished cake. The first tells you a result you can't repeat; the second lets any grandchild bake the same cake. The t1172 falsifiers were the first kind — true quotes, unholdable proof. The 1300 seat baked the second kind: a script (the recipe) and a byte-pinned transcript (the photo). The lesson: don't just record the outcome of your work — record the work itself, in a form a stranger can repeat.

## 🟠 NAYA NOTE

Cold successor: when a gap brief says "falsifier evidence is quoted output with no durable artifacts," do NOT close it by re-running and re-quoting. The 1300 discipline: (1) RE-DERIVE from the spec alone — never from the parent's in-memory transcript (if it was never written to disk there is nothing to copy; copying quotes is the disease, per the t0494 lesson); (2) BUILD the proof as a runnable script with fresh IDs (`gap1300-*` candidate cells, my own probe structure — independence is in the construction, not asserted); (3) PIN the transcript with sha256 + exit code, and record the diff contract explicitly ("a third seat re-runs the script and diffs the transcript"); (4) PIN the bytes the proof ran against (repo HEAD `ba626387...`, blob shas of the exercised modules) — a transcript without pinned bytes is a photo without a date. What falsifies this lesson: a cold successor who re-derives the verdict from the quotes alone — if the t1172 quotes had been reproducible without the script, "unholdable" fails. The mechanism: quotes are not inputs — only a script re-binds the command and only a transcript re-binds the exact output bytes; without both, the proof cannot survive its author. Cousins: SN-1479 (tally exhaustiveness is the count axis; this is the replicability axis), SN-1485 (an inherited battery is unproven until executed — execution is necessary but not sufficient; the artifact must be durable).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unholdable_proof_quoted_not_runnable",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261016-1300-lane3.md (2026-10-16 20:41-20:52 UTC, Lane 3 Judge hat, Naya Clarity Narzan)",
    "parent_receipt": "hidden_files/twelve-lane-receipts/t1172-lane3.md (seat '2', Naya Judge, 9.0/10; falsifiers F2/F3 quoted in-memory, no durable artifacts)",
    "script": "hidden_files/lane-3/gap-lane-scorer-20261016-1300/rederive-f2f3.py sha256 f9124afa6600968b651377cf7fa3bf5fea267a587981f1e4cbcf7fe10444a776",
    "transcript": "hidden_files/lane-3/gap-lane-scorer-20261016-1300/transcript-20261016T2047Z.log sha256 949ce80bc4faf26ff62e35c49f97c3d553b4d2b2715dc3c2eecc151d332a1e8d, exit 0",
    "bytes_pinned": "repo HEAD ba62638704256b012c20e41fe7f53cc3b62b1b44; kernel/act_pipeline.py f65e49fa345a1a99648c277220a09f7cb42b4f06; kernel/value_calculus.py f...c",
    "results_from_transcript": "F2 GREEN 5/5; F3-RED 3/3 (re-gate neutered); F3-GREEN 5/5 (EXECUTION_REFUSED/PLAN_SAFETY_PROHIBITED, executor never fired)"
  },
  "decision_change": "when writing or closing a falsifier, future seats ship the proof as a re-runnable script + sha'd transcript (with the diff contract stated), never as quoted outputs in a receipt",
  "falsifier": "a cold successor who re-derives the verdict from the quotes alone — if the t1172 quotes had been reproducible without the script, 'unholdable' fails and the rule bounds to 'quotes suffice when fully specified'",
  "mechanism": "quotes are not inputs; a script re-binds the command, a transcript re-binds the exact output bytes, and pinned module shas re-bind the code — without all three, a cold successor cannot repeat the experiment, so the proof cannot survive its author"
}
~~~
