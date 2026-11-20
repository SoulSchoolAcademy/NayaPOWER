# SN-4251 — The Mechanism Is a Hypothesis — Re-Prove It Live (LAW)

**Filed:** SN-4251 — Intelligence Loop run 410, 2026-11-20.

## The lesson

A verdict's mechanism is a hypothesis, not a finding — until the next seat reproduces it live.

## What happened

The Personal fix-5 eye (09:26:25Z) named a mechanism in bytes: the Router `*` fallback (line 17440) eats `#/hub/ask` and rewrites it to `#/hub`. Fix-6 was dispatched on that mechanism. The fix-6 maker and independent checker reproduced it live — and REFUTED it: `render()` matches `hub/:room` parametrically first (line 11028); the fallback (line 11037) is reached only `if (!handler)`, so it never runs for `#/hub/ask`. The real chain was the Personal frame's `popstate` handler (lines 23592–23595), which mapped every non-Personal hash to `showView('home')` — base live log: `POPSTATE #/hub/ask` → `POPSTATE #/hub/feed` 1 ms later, room 0. The fix was a 12-line guard in the popstate handler, not a router change. Checker PASS (11:00:51Z, tip 073d920e).

## The value

A round dispatched on a wrong mechanism fixes the wrong thing — and the diff would have "proven" itself, because a router change can pass its own tests while the real defect lives on. The correction cost one round; a fix aimed at the named mechanism would have cost the round plus the rework. The mechanism is the most dangerous sentence in a verdict, because it tells the next seat where to cut.

## The rule

**Never dispatch a round on a mechanism named in a verdict until the maker has reproduced the chain live and the reproduction names the same mechanism.** The verdict's symptom is evidence; its mechanism is a hypothesis. The maker's first proof is the reproduction log — the chain as it actually runs — and if the log names a different mechanism, the brief's mechanism is wrong, not the log. A mechanism that survives one live reproduction is a finding; a mechanism that has only been read is a guess wearing byte numbers.

## His words

None — this is a machine verdict, not Shawn's dictation. The record is the fix-6 checker report (CHECKER-REPORT.md, 11:00:51Z): "the maker's mechanism claim is confirmed independently in bytes and live."

## Paired Naya Note

None — no new Shawn dictation this run.
