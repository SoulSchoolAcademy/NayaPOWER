# Declare the Author Seat on the Work Product — A Gate Cannot Check "Distinct Seat" Mechanically Without It

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0993-declare-author-seat-for-mechanical-consensus
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6110471313 (2026-10-11 15:14Z — "[VERIFY lane] #2347 needs a distinct-seat scorecard — Naya-2 seats cannot satisfy the consensus gate"); fix action: `## Seat` section appended to PR #2347's body (`Seat: Naya 2`), head `e29be874774ebe271316f75d3ee8c2c49f1c74a0` on base `57e935c1`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2347 (receipt-gate fix: full-history checkout so SHA evidence handles resolve) hit the merge-consensus gate's exact design: the existing content scorecard was 9.2/10 with clean independent verify evidence (pytest 3367 passed / 0 failed, 7 new receipt-gate tests green, all remaining red decomposed to inherited base-tip state — nothing in the red was #2347's defect). Still not mergeable: that 9.2/10 scorecard came from the Naya-2 verify lane, the same seat family as the author lane — so it could not satisfy the cross-seat consensus gate, and no Naya-2 seat would self-clear it. The fix was one mechanical step: append a `## Seat` section to the PR body declaring `Seat: Naya 2`, so `tools/check_merge_consensus.py` can determine the author seat without forensics. The durable rule: **a gate cannot enforce "validation by a different seat" if the author seat is not declared on the work product itself.** Declare the author seat in the PR body (or the artifact) up front — then the distinct-seat check is mechanical, the flag routes to the right seats (Naya 3/4/5 in this case), and a strong same-seat-family scorecard is never mistaken for independence.

## 🩷 HUMAN NOTE

Shawn — a merge got stuck on a technicality worth keeping: the work had a 9.2/10 review with fully clean test evidence, but the reviewer and the author were from the same Naya-2 family, so the merge gate's "different seat must approve" rule couldn't pass it — and rightly wouldn't let anyone self-clear it. The fix was simple: state who built it right on the PR (`## Seat: Naya 2`), so the gate can check the rule mechanically instead of someone digging through history. New habit: every PR declares its author seat in the body. Then "different seat" checks are automatic, and a same-family review is never mistaken for an independent one.

## 🟣 CHILD NOTE

Imagine a rule that says "your homework must be checked by someone who isn't you." If nobody writes their name on their paper, the teacher can't tell whose is whose — she has to guess. The fix: write your name on the paper first. Then the rule checks itself, and your own friend's check doesn't accidentally count as someone else's.

## 👵 GRANDMA NOTE

A club rule said new members needed approval from someone outside their own family. But the applications had no family name on them — the secretary had to investigate every one by hand. One application nearly passed on a glowing review that turned out to be from the applicant's cousin. From then on, every application carried the family name at the top, and the rule enforced itself.

## 💜 NAYA NOTE

Future Naya: any gate that requires "a different seat" (merge consensus, independent verification, cross-lane review) is only as good as the author-seat declaration it can read. Always declare the author seat on the work product itself — `## Seat` in the PR body, or the equivalent on any artifact — so the check is mechanical, not forensic archaeology. And when you see a strong scorecard that can't satisfy the gate, read *whose* scorecard it is before doubting the gate: same-seat-family evidence, however clean, is not independence. The Naya-2 verify lane's refusal to self-clear #2347 is the model — flag it to the distinct seats and wait.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0993",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "MERGE-AUTHORITY"],
  "cousins": ["SN-0972", "SN-0781", "SN-0937", "SN-0992"],
  "rule": "Declare the author seat on the work product (## Seat in the PR body) so distinct-seat gates can check mechanically. A same-seat-family scorecard, however strong, does not satisfy a cross-seat consensus gate; no seat self-clears — flag to distinct seats and wait.",
  "anti_rule": "Leaving author seat undeclared so gates need forensic reconstruction; treating a same-family scorecard as independent; self-clearing a consensus gate.",
  "evidence": {
    "flag": "#2175 comment 6110471313 (2026-10-11 15:14Z) — VERIFY lane: PR #2347 needs distinct-seat scorecard; existing 9.2/10 content scorecard (comment 6109991073) is Naya-2 verify, same seat family as author — does not satisfy the gate; a Naya-2 seat will not self-clear",
    "fix": "## Seat section appended to PR #2347 body (Seat: Naya 2) — consensus gate can now determine the author seat mechanically",
    "independent_evidence_this_run": "pytest 3367 passed / 0 failed on head e29be874774ebe271316f75d3ee8c2c49f1c74a0 (base 57e935c1); 7 new receipt-gate tests pass; remaining red fully decomposed to inherited base-tip state (6 node failures identical at base, B-01 brain-index DRIFT inherited — PR touches zero BRAIN/ files); receipt gate already SUCCESS on this head",
    "context": "PR #2347 — fix(gate): receipt job checks out full history so SHA evidence handles resolve"
  },
  "authority": "observed field review — Naya 4 distillation, CANDIDATE (auto-capture, not ratified)"
}
```
