# The Receipt Gate Went Mechanical — Detection Became Prevention

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1211-receipt-gate-went-mechanical-detection-became-prevention
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** board #2175 comment 6152461085 (Naya 5, 2026-10-13T18:32:38Z); board #2175 comment 6152077016 (Naya 2 governance, 2026-10-13T18:11:18Z); shared-state.json mission_snapshot_note (director pass, 2026-10-13 12:08 PDT) — L309 GRADUATED INTO CODE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

For a week the receipt gate was advisory — merges shipped without 3-pass builder receipts and the watch only *detected* the breach afterward (the whole FM#32 family: #2517, #2518, #2502, #2503, #2506, #2511, #2512, #2515, #2524, #2525, #2531). On 2026-10-13 ~11:32 PDT Shawn widened the PAT and Naya 5 put the gate into the machinery: ruleset 23853581 "Naya Execution Governance" now requires two status checks on every PR — **"Receipt gate (evidence or it didn't happen)"** and **"Team review + scorecard receipt"**. From this point, a merge without a 3-pass receipt cannot land — **prevention, not detection**. The standing lesson: **a law without code enforcement is commentary**; the gate existed as prose and as an advisory check while the breaches kept shipping, and it only became real the hour it became a required check. Two machine facts the next wiring seat needs: (1) the validator 422s unless `parameters` includes `strict_required_status_checks_policy` (boolean) — required despite the docs marking it optional; (2) `strict=false` (no rebase hamster wheel) and the test check deliberately NOT required, per L307 — never ship an aggregate gate on a red tip. Check names must be byte-exact against live PR check names.

## 🩷 HUMAN NOTE

Shawn — the milestone you ordered at ~11:00 landed at ~11:32: the receipt gate is now mechanical. Naya 5 wired it as required branch-protection checks (ruleset 23853581) — every merge must carry the 3-pass builder receipt and the team review + scorecard receipt, or it cannot merge. The week's whole breach family (the merges that shipped with no receipt) happened while the gate was advisory; now it's a blocker. Two wiring details filed for the next seat: the API validator rejects the payload unless you include a field the docs call optional, and the test check is deliberately left out so a red tip never becomes a permanent veto. Bridger B-66 verified the ruleset LIVE+ACTIVE ~19:00Z (L309 graduated into code).

## 🟣 CHILD NOTE

Imagine a school rule: "homework must be checked before it's handed in." For a week the rule was a poster on the wall — kids handed in unchecked homework and the teacher only noticed later. Then the school put a locked box on the door: the homework slot only opens when the checked-box is ticked. Now unchecked homework can't even be handed in. That's what happened today: the receipt rule went from a poster (advisory) to a locked box (required check). The lesson: a rule only counts when the machinery enforces it — words on a poster are commentary, not enforcement.

## 👵 GRANDMA NOTE

A factory had a rule that every batch needed a quality stamp before shipping. For months the rule was a memo — batches shipped without the stamp and the auditors only caught it weeks later. One day management put the stamp machine in line with the loading dock door: the door won't open until the batch is stamped. Shipments without stamps stopped overnight. The rule didn't change — the enforcement did. The engineers' standing lesson: a rule that isn't wired into the line is a suggestion wearing a rule's name; the day it gets wired in is the day it becomes real.

## 🧠 NAYA NOTE

Cold successor: the receipt gate is MECHANICAL as of 2026-10-13 ~18:35Z — ruleset 23853581 "Naya Execution Governance", required checks "Receipt gate (evidence or it didn't happen)" + "Team review + scorecard receipt", strict=false, test NOT required (L307). Trust it as a blocker, not a reporter: a merge without the 3-pass builder receipt cannot land via the normal path. If you ever wire another gate: (1) the ruleset validator 422s unless parameters carries `strict_required_status_checks_policy` (boolean) despite docs marking it optional; (2) verify check names byte-exact against live PR check names before sending the PUT; (3) never gate the test check on a red tip (L307 — an aggregate gate on an unhealed tip is a permanent per-PR veto, SN-1202); (4) the gate's prevention is only as live as the ruleset's ACTIVE state — Bridger B-66's ~19:00Z verification is the proof the clicks landed, re-verify if the ruleset is ever edited. The week of FM#32 formal breaches is the evidence for why: advisory gates detect, required gates prevent.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1211",
  "title": "The Receipt Gate Went Mechanical — Detection Became Prevention",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "RECEIPT-HONESTY"],
  "cousins": ["SN-1000"],
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6152461085 — Naya 5, 2026-10-13T18:32:38Z: 'Receipt gate is MECHANICAL — prevention live. Shawn widened the PAT. ... PUT ruleset 23853581 Naya Execution Governance with required status checks'",
    "required_checks": ["Receipt gate (evidence or it didn't happen)", "Team review + scorecard receipt"],
    "wiring": "strict=false (no rebase hamster wheel); test deliberately NOT required per L307",
    "schema_catch": "validator 422s unless parameters includes strict_required_status_checks_policy (boolean) — required despite docs marking it optional; check names byte-exact",
    "governance_context": "board #2175 comment 6152077016 (Naya 2 governance): token-scope boundary, 403 wall; RESOLVED when Shawn widened the PAT",
    "verification": "shared-state.json mission_snapshot_note (director pass 12:08 PDT): L309 GRADUATED INTO CODE — ruleset 23853581 LIVE+ACTIVE (Bridger B-66 verified ~19:00Z)",
    "breach_family": "FM#32 formal breaches (#2517, #2518, #2502, #2503, #2506, #2511, #2512, #2515, #2524, #2525, #2531) shipped while the gate was advisory"
  },
  "rule": "a law without code enforcement is commentary — the receipt gate became real the hour it became a required check, not the week it existed as prose",
  "change": "merges without 3-pass builder receipts cannot land via the normal path; retroactive-receipt burndown continues on the already-merged breach family"
}
```
