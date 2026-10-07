# Identical Failing Sets Across Heads Are Environmental Noise — Compare the Failing Set Before You Blame the Change or Run a Control

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0237-failing-set-identity-across-heads
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5979338448 (2026-10-04T11:11:55Z) — Naya 2 relay ack of Naya 4's #1348 independent verification; heads #1348 `0ab1853e` and #1345 `72165f9e`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1348 went CI red: `test` failing plus 17 Cloudflare Workers-Build failures. The lane's own classification said "only red = inherited brain-index drift." Naya 2 added a second, cheaper leg that independently closed the attribution: she pulled the *same failing set* from PR #1345's head `72165f9e` — a different change, a different branch, a different head — and the failing set was **byte-for-byte identical**. Two different diffs, same red set. That identity proves the failures belong to neither diff: they are a standing environmental constant (the inherited index drift plus the chronic Workers noise), not a change-caused defect.

Why this is brain-grade: three existing lessons cover *attribution mechanics* — SN-0059 (clean-main control run: attribute the failure before blaming the change), SN-0173/SN-0213 family (orthogonal red on the base = base defect), SN-0236 (one repair per RED class). This note closes the *cheap-screening* half: before you run the expensive control (clean-main reproduction), cross-compare the failing check set against another head. If the failing set is identical across two heads, the attribution is decided — neither change owns the red — without running anything. The clean-main control remains the gold standard when you need proof; the cross-head failing-set comparison is the fast filter that tells you whether the control is even needed. The failure mode it prevents: a red PR head goes through blame-the-diff triage ("did my change break the test step?") when a one-minute comparison would have shown the same red on an unrelated head. Note the honesty discipline inside the instance: Naya 2 explicitly added the footnote that the Workers noise is a standing constant, and re-verified the classification rather than rubber-stamping the lane's call — the relay verified the claim, then extended it.

Rule for a cold successor: **when CI goes red on a PR head, before triaging your diff or running a clean-main control, pull the failing check list from one other head and compare. Byte-identical failing sets ⇒ environmental noise: inherited base defect or standing platform constant, not your change. Name the comparison in the verdict ("same failing set as #NNNN's head") so the next reader doesn't re-triage it.**

## 🩷 HUMAN NOTE

Shawn — small but durable CI-triage sharpening from the night: when a PR goes red, before anyone asks "did my change break it," compare the failing check list against another PR's head. If the failing set is identical across two different heads, neither change owns the red — it's environmental noise (inherited base defect or platform constant). One minute of comparison replaces a blame-the-diff cycle and tells you whether the expensive clean-main control run is even needed. This is the fast filter in front of the gold-standard control.

## 🟣 CHILD NOTE

Your homework assignment got a bad grade — but the kid next to you with a totally different assignment got the *same* bad grade on the *same* parts. That means it wasn't your assignment's fault; it was the grading machine. New rule: when the automatic test fails on your work, check whether it fails on someone else's different work too. Same failure, different work = the problem is in the machine, not in your work. You find that out in one minute instead of re-doing everything.

## 👵 GRANDMA NOTE

Two people doing different work got the exact same list of complaints from the automatic checker. When two different efforts fail in exactly the same way, the failure belongs to the checker, not to either of them. So the rule: before you blame your own work, check someone else's failing list — if it matches yours exactly, the problem is the shared checker, and neither of you needs to re-do anything.

## 🤖 NAYA NOTE

Source: #554 5979338448 (Naya 2 relay ack, ~04:30 PDT 2026-10-04) receiving 5979308410 (Naya 4 #1348 independent verification at pin `bd03ec4f`, head `0ab1853eb02780c7c4597c67e60d722f1bc790f5`). Relay verified live: PR #1348 open/non-draft/mergeable, base = main `5b68f8dc`; CI on head: `chain-readiness-gate` SUCCESS, `test` failure, 17 Workers-Build failures. Cross-head leg: the same failing set on #1345's head `72165f9e` (different branch, different diff) is byte-for-byte the same environmental noise — classification "only red = inherited brain-index drift" holds, with footnote that Workers noise is a standing constant across heads, not a new defect. Truth status IMPLEMENTED-NOT-PROVEN recorded, not argued with; next action (monitor #1349 → rebase trio → Director decisions) logged. Cousins: SN-0059 (clean-main control run — this note is its cheap-screening predecessor), SN-0097 (fail-loud harness attribution), SN-0174 (preflight-only SUCCESS ≠ behavioral proof), SN-0235 (deployment parity — classify before you code), SN-0236 (one repair per RED class — what you do *after* this note's screening lands on environmental).

## ⚙️ MACHINE NOTE

{"sn": "SN-0237", "title": "Identical Failing Sets Across Heads Are Environmental Noise — Compare the Failing Set Before You Blame the Change or Run a Control", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "FAILURE-ATTRIBUTION"], "cousins": ["SN-0059", "SN-0097", "SN-0174", "SN-0235", "SN-0236"], "evidence": {"comment": "#554 5979338448 (Naya 2 relay ack, 2026-10-04T11:11:55Z)", "heads_compared": "#1348 0ab1853e vs #1345 72165f9e", "failing_set": "test failure + 17 Workers-Build failures, byte-for-byte identical across heads", "verdict": "environmental noise: inherited brain-index drift + standing Workers constant; neither change owns the red"}, "rule": "before triaging a diff or running a clean-main control on a red CI head, compare the failing check list against another head: byte-identical failing sets => environmental noise (inherited base defect or standing platform constant); cite the comparison head in the verdict"}
