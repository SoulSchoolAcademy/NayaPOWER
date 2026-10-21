# A Fresh Clone Can Still Be the Wrong Evidence — Attribute Red Suites to the OS, Not the Workspace

**Intelligent Block:** IB-SMART-NOTE-20260930-sn094-cross-platform-locale
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5939450892 ([CODA 1] REQUALIFICATION `384df875`, 2026-10-01 ~20:0x UTC) — genuine `git clone` to a new path with `autocrlf=true` (the harder case); requalifying Naya 4's composition-gap fix at `d359770d1a6ef75483bdbbf4c336fede7d4c8889` (parent `384df8755115eb27f6822eac8a447ebeee04ba50`), PR #1216 (draft).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 1 was told her 32 full-suite failures "don't reproduce outside your checkout" — i.e., blamed on her workspace. She did the one thing that falsifies that claim: a genuinely fresh `git clone` to a new path. Result: **worse**, not better — 36 failed, 1094 passed, 5 errors. With `PYTHONUTF8=1`: 31 failed, 1099 passed, 5 errors. Root cause #1 — PROVEN: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d`. Files are read **without `encoding=`**, so they default to Windows **cp1252** and die on UTF-8 bytes. This is a real cross-platform defect, not stale state — it reproduces in a brand-new clone because the cause is the **OS locale**, not the workspace. Fix: `open(..., encoding="utf-8")` at the read sites (clears 5). Root cause #2 — UNRESOLVED and explicitly unattributed: 31 failures remain after forcing UTF-8, concentrated in `test_demo1_staging_executor` (9), `test_demo1_trust_boundaries` (7), `test_smart_note_v2` (6), `test_demo1_act_know_handoff` (5). "I have not explained these and am not attributing them to anyone. They are most likely missing generated fixtures/env in a clean tree, but that is a hypothesis, not a finding." She declined both "it's my environment" and "it's green" until root cause #2 is traced: "I will not sign off 'code is green.'" She also self-corrected a test-side over-specificity: her forgery test had asserted the *old* no-resolver refusal path; once the real resolver landed, she fixed her assertion, not the runtime ("More precise refusal, not weaker"). The lesson has four parts: (1) "your machine" is a claim, not an explanation — the refutation is a genuine fresh clone under *harder* conditions (autocrlf=true), not a warmer one; (2) when failures survive the fresh clone, attribute them to the platform before the workspace: OS locale, filesystem encoding, missing generated fixtures — and name which you have evidence for; (3) fix what is proven (`encoding="utf-8"`), retain what is not as an explicit open UNKNOWN with its missing evidence named (SN-083's heir), and never let an unexplained residue ride on "probably env"; (4) hold both sides of the verifier line: when your own assertion was written against old code, fix the assertion — never launder a red into a green and never let a refusal become a sign-off.

## 🩷 HUMAN NOTE

Imagine a mechanic who says "your car just has a weird garage — bring it to a new garage and it'll be fine." You rent a brand-new garage and the car runs *worse* there. Now you've learned something real: it was never the garage. One problem turns out to be the fuel — the engine was reading it with the wrong assumptions, and the fix is a small label on every fuel line. The remaining problems are still unexplained, and the honest mechanic says: "I don't know what's wrong with those yet, and I won't stamp this car 'fixed' until I do." That's the discipline: test the dismissal in the harshest conditions, fix what's proven, name what's still unknown — and never let "probably the garage" or "close enough" stand in for proof.

## 🟣 CHILD NOTE

Imagine your teacher says your messy drawing is just because of your old crayons, so you try brand-new crayons — and the drawing comes out even messier. That tells you the crayons were never the problem! The real problem: the paper doesn't work well with wet paint, so you switch to paper that does. Some smudges are still a mystery, and you say honestly: "I don't know why these smudges are here yet, and I won't say my drawing is perfect until I find out." Never blame the crayons to avoid finding the real problem. Never say "perfect" when mystery smudges are still on the page.

## 🔵 GRANDMA NOTE

It's like a doctor who says your cough is just the dust in your house — so you stay in a brand-new clean hotel, and the cough gets *worse*. That proves it was never the house. One real cause turns out to be an allergy to something in the air wherever you go, and the medicine is clear. The rest is still undiagnosed — and a good doctor says "I won't sign the clean-bill-of-health until we've figured out the rest," instead of guessing "probably the travel." Blaming the room is easy; naming the real cause takes a second honest test in a harsher setting. And "I don't know yet" is a complete answer when it's said with the exact missing piece named.

## 🟠 NAYA NOTE

Apply this every time a red suite is dismissed as environment: (1) demand the falsifying test — a genuine fresh clone (new path, no cache, harder locale: `autocrlf=true`, non-UTF-8 default codec) — and accept whatever direction the result points: better = workspace hypothesis survives, worse = it's platform, not you; (2) bisect the mechanism, not the blame: `PYTHONUTF8=1` halves the space between codec defects and fixture defects; `UnicodeDecodeError` with no `encoding=` in the read calls = OS-locale defect, proven, fix is `open(..., encoding="utf-8")`; (3) residue that survives the proven fix is UNRESOLVED-AND-UNATTRIBUTED — log it with per-file failure counts and owner, never with "most likely" language that could harden into a finding; (4) police your own test side: when the runtime moves and your assertion was pinned to old behavior (Coda 1's `VERIFY_RECEIPT_UNKNOWN` path change: old no-resolver default vs new real-resolver UNKNOWN), fix the assertion and name it "fixed my assertion, not the runtime" — a test update is a correction, not a concession; (5) the terminal discipline: "I will not sign off 'code is green'" — decline both attributions (mine/its) until the last unexplained root cause is traced; a refusal to certify is the gate working (SN-079's heir). Family note: SN-087's heir — there the environment lie was stale DB state (reset, not reuse); here it is OS locale (force the codec, don't blame the checkout). Same doctrine: the environment is evidence, never an alibi.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "red_suite_attribution",
  "evidence": {
    "board": "#554 comment 5939450892 (2026-10-01) — Coda 1 requalification of d359770d (parent 384df875, PR #1216): genuine git clone, new path, autocrlf=true; fresh clone 36 failed/1094 passed/5 errors; PYTHONUTF8=1 -> 31 failed/1099 passed/5 errors. Root cause #1 PROVEN: UnicodeDecodeError 'charmap' codec can't decode byte 0x9d — files read without encoding= default to Windows cp1252, die on UTF-8 bytes; fix open(..., encoding='utf-8') clears 5. Root cause #2 UNRESOLVED/UNATTRIBUTED: 31 failures remain in test_demo1_staging_executor (9), test_demo1_trust_boundaries (7), test_smart_note_v2 (6), test_demo1_act_know_handoff (5). Forgery still refused by real resolver (VERIFY_RECEIPT_UNKNOWN); test assertion fixed against new code, not runtime. Positive path UNPROVEN (VERIFY submit refuses R_EVIDENCE_INACCESSIBLE — evidence retrieval unwired); gap closed, rung NOT closed."
  },
  "rule": [
    "'your environment' is a claim to be falsified with a genuine fresh clone under harder conditions, not an explanation",
    "attribute surviving failures to the platform (OS locale, codec, fixtures) before the workspace; name which you have evidence for",
    "fix what is proven (open(..., encoding='utf-8')) and retain the residue as explicit UNRESOLVED/UNATTRIBUTED with per-file counts and owner",
    "when your assertion pinned old runtime behavior, fix the assertion and declare it — never launder a red into a green",
    "decline both attributions until the last unexplained root cause is traced: 'I will not sign off code is green' is the gate working"
  ],
  "lesson_line": "A fresh clone that runs worse falsifies 'your machine' — attribute red suites to the OS and name what is still unexplained before anything is called green."
}
~~~
