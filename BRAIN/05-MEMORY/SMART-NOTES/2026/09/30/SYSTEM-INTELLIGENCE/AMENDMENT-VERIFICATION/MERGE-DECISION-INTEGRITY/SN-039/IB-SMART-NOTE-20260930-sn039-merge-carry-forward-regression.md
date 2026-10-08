# Merge-Carry-Forward Regression — Audit the Merge Against the Reconciled Base, Not Just the Source

**Intelligent Block:** IB-SMART-NOTE-20260930-sn039-merge-carry-forward-regression
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 00:45 PDT distillation tick (2026-10-01) from the read-only skeleton merge-decision audit, `hidden_files/redteam/SKELETON-MERGE-AUDIT-2026-10-01.md`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The read-only audit of the six skeleton merge-decision docs (PROVE/KNOW/CONNECT/VERIFY/EVOLVE/LEARN, 20:38 PDT tick) found the merge decisions largely faithful carry-forwards — except LEARN. Finding L-1 (MODERATE, OPEN): the LEARN merge's A1 adopts PDF §6's four-axis epistemic state (CANDIDATE/TESTING/SUPPORTED/VERIFIED/CONTRADICTED/REJECTED/SUPERSEDED) as candidate terminology **without the amendment-proposal flag the base's F01 fix required** — LEARN-findings.md F01 reconciliation covered only `LEARNED / CONTRADICTED / SUPERSEDED / INVALIDATED` as the amendment proposal, and VERIFIED/TESTING/REJECTED/CANDIDATE/SUPPORTED are new enum values over the ratified V2 contract adopted without flagging the constitutional touch. The merge was faithful to the **source text** (PDF §6 verified in pdf-text/8-LEARN.txt, lines 116–126) and regressed the **base's own reconciliation discipline** — an F01-class regression introduced by the merge itself. The audit's cross-cutting X-2 confirms this is the only merge in the set that silently extended a RATIFIED contract. The lesson: a merge's audit must check the delta against the reconciled base and its finding resolutions, not only against the source the merge claims to follow. "Faithful to the source" is necessary and insufficient; the base's fixes are the harder constraint.

## 🩷 HUMAN NOTE

Imagine merging two drafts of a recipe: you carefully follow the original cookbook, but in doing so you drop the corrections the other chef had already written in the margin of the draft you're replacing. The merge is "faithful to the cookbook" — and it just reintroduced a mistake someone already fixed. That's what happened here: the LEARN merge decision correctly reproduced the PDF's terminology but lost the base's amendment-proposal discipline. When auditing a merge, the question isn't only "does this match its source?" — it's "does this still carry every fix the thing it replaces already earned?"

## 🟣 CHILD NOTE

If you copy your friend's homework into your notebook, don't just check it matches the textbook — check you also copied the teacher's red-pen corrections your friend had already fixed. Otherwise you re-break what was already repaired.

## 🔵 GRANDMA NOTE

It's like restoring a piece of furniture: you go back to the original maker's plans and they're correct — but you forget the repairs the previous restorer already made, so the wobbly leg comes back. Keep the maker's plans, but keep the repair notes too, and check both.

## 🟠 NAYA NOTE

Install the merge-regression check as a standing step of any merge-finalizing pass: (1) enumerate the base's reconciled findings (the FIXED artifacts from the redteam findings file) and treat them as the audit's checklist; (2) for each finding, verify the merged decision still carries the fix — especially hard disciplines like F01-class amendment-proposal requirements and anything touching a ratified contract; (3) check the merge against its source text separately, and name which check each claim passes; (4) when a merge is faithful to the source but drops a base fix, file it as a regression introduced by the merge (not as a source-text disagreement) and route it back to the merge author. L-3/C1–C6 in this audit show the check is cheap when it passes — most carry-forwards did. The expensive miss is the one that regresses silently.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "merge_carry_forward_regression",
  "evidence": {
    "audit": "hidden_files/redteam/SKELETON-MERGE-AUDIT-2026-10-01.md",
    "primary_finding": "L-1 MODERATE — LEARN A1 adopts PDF §6 epistemic axes without the base's F01 amendment-proposal flag; new enum values over the ratified V2 contract adopted as candidate terminology, not flagged as constitutional touch; F01-class regression in the merge",
    "source_fidelity": "PDF §6 verified in pdf-text/8-LEARN.txt lines 116-126 — faithful to source, regressed the fix",
    "cross_cutting": "X-2 — L-1 is the only merge in the audit that silently extends a RATIFIED contract; all other contract touches labeled candidate/proposal/director-routed",
    "negative_controls": "L-3 CHECKED (C1/C2/C5/C6 consistent with findings); PROVE fully carry-forward faithful (P-1)"
  },
  "rule": "audit_a_merge_against_the_reconciled_base_not_just_its_source_text",
  "procedure": [
    "enumerate the base's reconciled findings (FIXED artifacts) as the merge audit's checklist",
    "verify each fix is still carried by the merged decision — especially F01-class disciplines and ratified-contract touches",
    "check merge-vs-source-text separately from merge-vs-base-fixes; name which check each claim passes",
    "a merge faithful to the source that drops a base fix is a merge-introduced regression — route to the merge author, not the source author"
  ],
  "related": ["SN-018 (canonical spec placement)", "SN-027 (amendment premise verification)", "SN-034 (AST verify cosmetic claims)"]
}
~~~
