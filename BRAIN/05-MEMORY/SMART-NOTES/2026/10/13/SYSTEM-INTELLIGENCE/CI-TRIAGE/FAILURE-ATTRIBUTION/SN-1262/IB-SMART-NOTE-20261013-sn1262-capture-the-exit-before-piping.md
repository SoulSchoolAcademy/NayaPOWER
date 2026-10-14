# Capture the Exit Before Piping — a Piped `$?` Measures the Last Command, Not the Instrument

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1262-capture-the-exit-before-piping
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0720] entry (Dispatcher mirror, t0712-lane8 tip index-freshness protect check, 9.5/10, 2026-10-13) — the synthetic-drift control nearly lied twice: `cmd | head; echo $?` measured `head`'s exit, not the instrument's. Pattern: `cmd > file 2>&1; echo "EXIT=$?"` — no pipes before the capture. Companion angle to SN-0988 (which covers `bash -e` killing the witness); this covers the pipeline element being measured.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The tip index-freshness check's synthetic-drift control nearly reported the wrong verdict — twice. The first near-lie was `cp` ownership noise; the second was pure shell mechanics: `cmd | head; echo $?` captures **head's** exit code, not the instrument's. The control instrument could have failed and the check would still have printed a green exit. The durable rule: **capture exits before piping, always** — `cmd > file 2>&1; echo "EXIT=$?"`, no pipes before the capture. A control that measures the wrong command's exit is worse than no control: it spends trust it didn't earn.

Why this is brain-grade: every lane writes instrument commands — verification harnesses, drift controls, reproduction scripts. The exit code is the thinnest, most-trusted signal in the system, and it silently measures the wrong thing the moment a pipe appears. Two near-lies in one tick means the pattern is waiting in every harness: audit your instrument commands for pipes between the command and the `$?`.

## 🩷 HUMAN NOTE

Shawn — a small shell lesson that almost cost a verification tick: when you pipe a command through `head` and then check `$?`, you're checking head's exit, not the command's. The drift control nearly reported "all good" while measuring the wrong program's success. The fix is a one-line discipline: run the command writing to a file, then read the exit code — no pipes in between. Tiny, mechanical, and it protects every automated check the lanes write from here on.

## 🟣 CHILD NOTE

Imagine you ask your friend "did you finish your homework?" but you actually asked their little brother, who says "yes!" — and you believed it. That's what happened: the check asked the computer "did the test pass?" but the pipe made the computer answer for the wrong program. The rule now: ask the right one directly, and check the answer before anything else touches it.

## 👵 GRANDMA NOTE

There's an old saying about shooting the messenger — this is the opposite: trusting the wrong messenger. The worker piped a command's output through a helper program, then asked "did it work?" — and the answer came from the helper, not the command. The command could have failed silently. The fix is plain common sense made into habit: check the result of the thing you actually ran, before anything else gets in the way.

## 🧠 NAYA NOTE

Note to future me: `$?` answers "how did the last thing go" — and in a pipeline, the last thing is the pipe's tail, not my instrument. Any verification I write must capture the exit in the same breath as the command: `cmd > file 2>&1; echo "EXIT=$?"`. If I ever see `| head` or `| tail` between a command and its `$?`, the verdict is suspect until re-run. And a synthetic control that can lie is worse than no control — controls get the same byte-discipline as the code they guard.

## ⚙️ MACHINE NOTE

{"sn": "SN-1262", "title": "Capture the Exit Before Piping", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "FAILURE-ATTRIBUTION"], "cousins": ["SN-0988"], "evidence": {"finding": "t0712-lane8 tip index-freshness protect check (2026-10-13, lesson-broadcast.md [t0720], dispatcher mirror 9.5/10): the synthetic-drift control nearly lied twice - cp-ownership noise, and piped $? measuring `head` instead of the instrument (cmd | head; echo $? captures head's exit). Rule adopted: cmd > file 2>&1; echo \"EXIT=$?\", no pipes before the capture"}, "decision_change": "every instrument/check command written by a lane is authored as cmd > file 2>&1; echo \"EXIT=$?\" with no pipe between the command and the exit capture; existing harnesses are audited for pipe-before-capture", "falsifier": "a case where the exit is captured before any pipe and still measures the wrong command, or a piped-$? verdict proven correct against the instrument's true exit - then the pipe is not the mechanism", "mechanism": "POSIX $? reflects the last element of a pipeline; cmd | head makes $? report head's exit, so the instrument's real exit is silently replaced by the tail command's", "rule": "capture exits before piping, always - no pipes between the instrument and the $?"}
