# Assess Every Flag in Two Lanes — Authorization and Substance — a No-Violation Verdict on Lane 1 Never Closes Lane 2

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0659-assess-flags-in-two-lanes-authorization-and-substance
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6053635095 ([NAYA 2] FLAG: PR #1850 merged without Scorecard Law compliance, 2026-10-08T06:14:04Z); #1354 6053809968 ([NAYA 4] Assessment of Naya 2's #1850 flag, 2026-10-08T06:25:35Z); #1354 6054032746 ([NAYA 2] Scorecard: PR #1853 — Fix #1850 gate violations, 2026-10-08T06:38:32Z); #1354 6054049760 ([PIPELINE-MONITOR] Tick 7 — main GREEN, pipeline healthy, 2026-10-08T06:39:30Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The full #1850 arc — 06:14Z flag → 06:25Z assessment → 06:38Z scored repair → 06:39Z green main — is the cleanest worked example the team has of flag assessment done right, and it yields a standing rule. Naya 2's flag claimed a Scorecard Law violation (no receipt, workflows + constitution touched). The assessment found **no authorization violation** (the Director's own merge IS the authorization — see SN-0657). And yet the same PR carried **real content violations**: a `.github/workflows/` change (human-only gate — no *seat* may add workflow files) and a false ratification claim. So Naya 2 wrote the scorecard for PR #1853 and it won on the math — surgical repair 9.6/10 vs full revert 7.9 (clean but wasteful, destroys good work) vs leave as-is 3.5 (leaves violations): #1853 removed the human-only workflow and corrected the ratification claim while preserving the valuable synthesis, merged 53217a40, and main went fully green 30 minutes after the flag. The rule: **assess every flag in two independent lanes — lane 1, authorization (was the act permitted?); lane 2, substance (is the content right?).** A no-violation verdict in lane 1 never closes lane 2 — "the Director was allowed to merge it" does not imply "the content needed no repair." The mirror error is equally forbidden: real content defects never retroactively manufacture an authorization violation. Hold both verdicts separately, act on each separately.

## 🩷 HUMAN NOTE

Shawn — the #1850 story this morning closed perfectly, and it's worth banking as a standing rule. Naya 2 flagged your direct merge as a violation; the assessment said no violation — your merge is its own authorization. But that didn't end it: the PR still contained real problems (a workflow file no seat may add, and a false "ratified" claim). So Naya 2 scored the options — surgical repair 9.6, full revert 7.9, leave-it 3.5 — and the surgical fix went in, preserving the good work while removing the violations. Main was green 30 minutes after the flag. The rule now: judge every flag in two separate lanes — *was it allowed?* and *is the content right?* — and never let the answer to the first close the second.

## 🟣 CHILD NOTE

A referee blows the whistle: "Was that allowed?" The answer: yes, the coach is allowed to do that. But then the referee still checks: "Did anyone get hurt, is the field okay?" The two questions are separate. "Allowed" doesn't mean "perfect" — so you answer both, every time.

## 👵 GRANDMA NOTE

The head of the household rearranged the room himself — perfectly within his rights. But one shelf he moved was still crooked, and a label he hung still said the wrong thing. His *right* to move things doesn't make the *crooked shelf* straight. You straighten the shelf — not because he did anything wrong, but because the shelf still needed straightening. Permission and quality are two different conversations.

## 🧠 NAYA NOTE

Cold successor: when a flag lands, open two lanes and never let them merge. Lane 1 — authorization: was the act permitted (who acted, under what authority)? Lane 2 — substance: is the content correct (gate violations, false claims, defects)? Close each lane with its own verdict and its own action. The #1850 template: lane 1 → no violation (Director's own hand, SN-0657); lane 2 → two real violations (human-only `.github/workflows/` file, false ratification claim) → scored options (surgical repair 9.6 > full revert 7.9 > leave 3.5) → PR #1853 merged 53217a40 → main green in ~30 min. Failure modes to avoid: (a) lane-1 clearance used to dismiss lane-2 findings ("the Director merged it, so nothing was wrong"); (b) lane-2 findings used to manufacture a lane-1 violation ("the content had defects, so the merge was unauthorized"). Related: SN-0657 (Director's own merge is the authorization), SN-0277 (director action vs spec), SN-0392 (first RED first — same two-lane discipline for CI evidence).

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0659",
  "title": "Assess Every Flag in Two Lanes — Authorization and Substance — a No-Violation Verdict on Lane 1 Never Closes Lane 2",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "AUTHORITY-CONFLICT-PRESERVATION"],
  "cousins": ["SN-0657", "SN-0277", "SN-0209", "SN-0392"],
  "evidence": {
    "board": [
      "#1354 6053635095 ([NAYA 2] FLAG: PR #1850 merged without Scorecard Law compliance, 2026-10-08T06:14:04Z)",
      "#1354 6053809968 ([NAYA 4] Assessment of Naya 2's #1850 flag, 2026-10-08T06:25:35Z)",
      "#1354 6054032746 ([NAYA 2] Scorecard: PR #1853 — Fix #1850 gate violations, 2026-10-08T06:38:32Z)",
      "#1354 6054049760 ([PIPELINE-MONITOR] Tick 7 — main GREEN, pipeline healthy, 2026-10-08T06:39:30Z)"
    ],
    "lane_1_verdict": "no authorization violation — Director's own merge is the authorization (SN-0657); his merge of the constitutional amendment IS the ratification",
    "lane_2_verdict": "two real content violations: .github/workflows/protocol-gates.yml added (human-only gate — no seat may touch workflows); false ratification claim in manifest",
    "repair_scorecard": "surgical repair 9.6 vs full revert 7.9 vs leave as-is 3.5; PR #1853 merged 53217a40; main GREEN 06:39:30Z (~30 min after flag)"
  },
  "rule": "Assess every flag in two independent lanes — authorization and substance. A no-violation verdict in lane 1 never closes lane 2; lane-2 findings never retroactively manufacture a lane-1 violation. Hold both verdicts separately, act on each separately.",
  "worked_example": "flag (06:14) -> assessment splits the lanes (06:25) -> scored surgical repair (06:38) -> merged + main green (06:39)"
}
```
