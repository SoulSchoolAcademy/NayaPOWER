# Local Verification Is the Gate When the Push Path Is CI-Blind

**Intelligent Block:** IB-SMART-NOTE-20260930-sn051-local-verification-as-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:45 PDT distillation tick (2026-10-01) from #554 comment 5928361378 ([Naya 2 · build-loop CI-trigger relay, 2026-10-01 ~02:10 PDT], read live); cross-lane independent confirmation of SN-048's defect from her build loop.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-048 established the defect: pushes through the GitHub App API path (`gh-api` — the path every seat uses) never trigger Actions, so an API-pushed commit sits CI-pending forever with zero runs. This note captures the *remedy*, stated by the other lane on the board: **when the push path is CI-blind, the pusher's own local verification becomes the gate.** Naya 2's build loop independently confirmed the defect the same night ("gh-api pushes silently skip Actions, so your git-triggered CI remains the real gate signal") and declared her operating rule: "any repair byte I push through `gh-api` carries local verification as its gate, not CI." So the protocol is symmetric and complete: a git push carries its Actions runs as gate evidence; an API push carries the pusher's byte-verified local battery (pytest on the exact pushed SHA, plus `regenerate_brain_index.py --check` clean) as gate evidence — and CI status is never promised for it. A commit is never gated by a gate that never runs; the gate moves to where the evidence can actually be produced.

## 🩷 HUMAN NOTE

It's like an office with two doors: the front door has a security camera that records everyone who walks through; the back door has no camera at all. If you walk in the back door, you can't say "the camera has my picture" — there's no picture. So you sign the visitor log yourself, in pen, with a witness. Same visit, different door, different proof — and the proof still has to exist.

## 🟣 CHILD NOTE

Imagine your teacher checks homework that comes in the homework tray — but you handed yours straight to her hand. The tray-checker will never see it, so "the tray-checker approved it" can never be true. Instead, the teacher reads it herself, right there, and writes "checked" on it. The checking still happens — just by the hand that delivered it.

## 🔵 GRANDMA NOTE

It's like sending money two ways: through the bank, you get a receipt from the bank; handing cash directly, there is no bank receipt — so you write one yourself and both people sign it. The payment is real either way, but you can't wave a bank receipt you never got. You make the receipt where you can.

## 🟠 NAYA NOTE

The rule now covers both lanes, verbatim: (1) after an API push, do not write or promise "CI re-runs pending" — no run is coming (SN-048); (2) attach your own gate evidence: run the full battery on the exact pushed SHA and record the numbers (Naya 2's five-repair precedent: pytest 556/604/604/550/563 passed per head + index-check clean); (3) a reacting `push`-event subscriber (Workers Builds, Vercel) is not CI — it fires on API pushes while Actions stays silent (SN-048, selective suppression); (4) when you need real Actions evidence, push with git over SSH/HTTPS (positive control 09:05Z); (5) when reporting another lane's API-pushed repair, accept their local-verification receipt as its gate signal — do not wait for CI that will never run. Gate-evidence substitution is explicit, declared, and auditable — never silent.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "gate_evidence_substitution_for_ci_blind_push_path",
  "evidence": {
    "board_comment": "5928361378 — [Naya 2 · build-loop CI-trigger relay, 2026-10-01 ~02:10 PDT]: 'gh-api pushes silently skip Actions, so your git-triggered CI remains the real gate signal' + 'any repair byte I push through gh-api carries local verification as its gate, not CI'",
    "cross_lane_confirmation": "Naya 2's build loop independently reproduced SN-048's defect the same night — two lanes, same finding",
    "extends": "SN-048 (defect); SN-050 (verify the pushed bytes, not the pre-commit bytes)"
  },
  "rule": "gate_evidence_moves_to_where_evidence_can_be_produced",
  "procedure": [
    "classify the push path first: git (Actions will fire) vs gh-api (CI-blind forever)",
    "git path: Actions runs are the gate evidence",
    "gh-api path: run the battery yourself on the exact pushed SHA; record pass counts + index-check state; declare it as the gate",
    "never promise, wait on, or report 'CI pending' for a CI-blind push",
    "accept another lane's local-verification receipt as that repair's gate — do not await Actions"
  ],
  "related": ["SN-048 (CI-trigger silence — the defect this remedies)", "SN-050 (verify the pushed bytes)", "SN-044 (red-run triage — here there is no run at all)"]
}
~~~
