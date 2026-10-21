# Verify with the Instrument CI Uses — a Branch's Exact-Pinned Tool Can Lag the Ratchet-Floor Version

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0429-instrument-ci-uses
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6009020612 ([NAYA 4][SIGN-OUT] drive loop 20:43 PDT tick, 2026-10-06T03:56:59Z); PR #1229 branch `naya4/smart-notes-2026-09-30`.

## ✦ IN A NUTSHELL

Diagnosing PR #1229's red with the branch's own exact-pinned tool was a phantom measurement: the branch's stale tool version could not regen the backlog at all, while CI validates with main's ratchet-floor tool version (from #1576). The repair only worked once Naya 4 regenerated REAL-TREE.json/md and NAYAPOWER-BRAIN-INDEX.json with main's ratchet tool (`--check` exit 0, committed `b2ad1c92`). Rule: when you reproduce or repair a CI red, pin to the tool version the CI gate itself uses — a pass (or failure) produced by an older pinned tool is not evidence about what CI sees. Same tick, second discipline applied: the first red was pytest (job dies at step 7 `python -m pytest -q`), not the drift check — the drift-check failure was downstream, classified per SN-0392 and not patched.

## HUMAN NOTE

Shawn — a measurement discipline from tonight's #1229 work: the Smart Note seed branch pins its tools to old exact versions, but CI checks the branch with the newest ratchet-floor tool from main. Naya 4 proved the branch's own tool couldn't even regenerate the registry backlog — the repair only landed when she used main's tool, which is what CI actually runs. Cold lesson for every seat: always reproduce a CI red with CI's tooling, never the branch's. And the same tick applied your First-RED law cleanly — she first attributed the red to the drift check, then corrected to pytest dying at step 7 and left the drift check alone. pytest stays red (expected): the capture worker keeps pushing unregistered seeds, which is the capture lane's repair, not this branch's.

## CHILD NOTE

Imagine your teacher grades homework with a new answer key, but you check your own work against last year's answer key and say "I'm fine." You're not fine — you used the wrong key. When CI is the teacher, always borrow CI's answer key: use exactly the tool version the gate uses, or your "it passes" means nothing. And when two things fail, fix the first failure first — the second one might just be complaining about the first.

## GRANDMA NOTE

If the inspector uses a modern tape measure and you check your work with your grandfather's old wooden ruler, you'll swear the shelf fits — and the inspector will fail it anyway. Always measure with the inspector's ruler. And when several things break at once, start with the first thing that broke; the rest often fix themselves once the first is repaired.

## NAYA NOTE

Note to future me: this is the INSTRUMENT-PARITY family's newest member — SN-0341 taught us the harness lies about disk, SN-0428 taught us the CI checkout lies about the tree, and now SN-0429 teaches us the branch's exact-pin lies about the tool. The exact trap: a branch pins `tools/*` to old versions for reproducibility; CI (and main's ratchet tool) moved on. Two concrete checks before any regen or repair on a CI-gated branch: (1) diff the branch's pinned tool version against the version the CI workflow invokes — if they differ, use CI's; (2) confirm the tool even CAN do the job — the stale pin here could not regen a 386-entry backlog at all, so any conclusion drawn from its output would have been fiction. Pairs with SN-0392: Naya 4's in-tick correction (drift check → pytest step 7) is the First-RED discipline executed correctly — name it as the pattern to copy. A cold Naya inheriting a red CI-gated branch should check tool parity before reading a single failure line.

## MACHINE NOTE

{"sn": "SN-0429", "title": "Verify with the Instrument CI Uses — a Branch's Exact-Pinned Tool Can Lag the Ratchet-Floor Version", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "INSTRUMENT-PARITY"], "cousins": ["SN-0341", "SN-0329", "SN-0428", "SN-0392"], "authority": "observed finding — Naya 4 drive-loop sign-out, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 comment 6009020612 ([NAYA 4][SIGN-OUT] drive loop 20:43 PDT tick, 2026-10-06T03:56:59Z)", "red": "PR #1229 (naya4/smart-notes-2026-09-30): Kernel Tests failing on 4 capture pushes 19:45–20:43 PDT (SN-0425..SN-0428)", "first_red": "pytest, not the drift check — CI step data: job dies at step 7 `python -m pytest -q`; drift step never runs (initial drift-check attribution corrected per SN-0392)", "tool_gap": "branch's stale exact-pin tool version cannot regen the 386-entry backlog; main's ratchet-floor version (#1576) is what CI uses", "repair": "merged main into branch (00ee7a31, server tree verified identical to local), regenerated REAL-TREE.json/md + NAYAPOWER-BRAIN-INDEX.json with main's ratchet tool (--check exit 0), committed b2ad1c92; pytest still red (expected)"}, "doctrine": {"instrument_parity": "reproduce and repair a CI red with the exact tool version the CI gate uses — a branch's older exact-pin is a different instrument and its verdict is inadmissible", "capability_check": "confirm the pinned tool can even perform the operation before drawing conclusions from its output", "first_red_discipline": "name the first red (pytest step 7) and leave downstream steps (drift check) unpatched per SN-0392"}}
