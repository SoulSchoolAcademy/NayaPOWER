# No Reconciliation Artifact, No Reconciliation Claim — the Merge-Claim Evidence Rule

**Intelligent Block:** IB-SMART-NOTE-20260930-sn040-merge-claim-evidence-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 00:45 PDT distillation tick (2026-10-01) from the read-only skeleton merge-decision audit, `hidden_files/redteam/SKELETON-MERGE-AUDIT-2026-10-01.md`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two of the six skeleton merge-decision docs make status claims about the base they carry forward that the audit could not verify from artifacts. E-1 (MODERATE, OPEN): the EVOLVE merge claims the base was "red-teamed and fully reconciled (6 findings FIXED, 8.5/10)" — **no EVOLVE-findings.md exists on disk**, so the reconciliation is UNVERIFIABLE from the findings artifact. K-1 (MODERATE, OPEN): the KNOW merge claims the base was "red-teamed + reconciled" 8.5/10 — **no KNOW-findings.md exists**; the record shows only LEARN/PROVE findings files. The claims may be true, but a merge decision's job is to make its authority checkable: evidence law says a claim about prior reconciliation must point at the per-finding reconciliation artifact, and where no artifact exists the claim is an assertion, not evidence. The audit's X-1 notes this defect family ("unverifiable carry-forward claims") recurs across the merged ACT/LAW reviews too (M01/M02/M-LAW-01/02/03/05). The mechanical rule: **a merge decision must cite the base's reconciliation artifact for every status claim it inherits**; a status claim with no artifact on disk is downgraded to assertion and sent back to the author to either produce the file or retract the claim.

## 🩷 HUMAN NOTE

A builder handing you a house doesn't get to say "the foundation was inspected, all good" and expect you to take it on faith — you ask for the inspection report. These merge decisions did the equivalent of handing over the house without the report: they claimed the base document was fully reconciled, but the reconciliation paperwork (the findings file) doesn't exist where it should. The claim might be perfectly true — and the audit treats it that way, finding no contradiction, only absence. But "true and uncheckable" is not what a merge decision is for. A merge decision is the receipt. If the receipt has no attachments, it's just a story. Ask for the file, or treat the claim as a story.

## 🟣 CHILD NOTE

If your friend says "the teacher already graded my homework, I got an A," you don't argue — you ask to see the graded paper. If the paper doesn't exist, the A might be real, but you can't check. A merge decision is the graded paper of a document: it has to show its proof.

## 🔵 GRANDMA NOTE

It's like a seller telling you the car "just passed inspection" with no inspection paperwork in the glove box. Maybe it did — but a wise buyer doesn't pay the premium for a claim without the certificate. In a merge, the reconciliation findings file is the certificate. No certificate, no claim.

## 🟠 NAYA NOTE

Apply this before accepting any merge decision in the merge-finalizing pass: (1) list every status claim the merge makes about its base ("red-teamed", "fully reconciled", "N findings FIXED", any score like 8.5/10); (2) for each claim, locate the base's reconciliation artifact — the redteam findings file with per-finding FIXED marks; (3) no artifact on disk → downgrade the claim to assertion and return it to the author with exactly two options: produce the artifact or retract the claim to its checkable wording ("base carry-forward; reconciliation not on record"); (4) when the artifact exists, spot-check two findings against their FIXED evidence — the audit already did this for PROVE (all 16 FIXED with Appendix-A evidence) and it is the model. This is SN-020 (asserted ≠ verified) applied at the merge layer: a merge decision is not prose about a document, it is the document's evidence envelope.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unverifiable_carry_forward_claims",
  "evidence": {
    "audit": "hidden_files/redteam/SKELETON-MERGE-AUDIT-2026-10-01.md",
    "E-1": "EVOLVE merge claims base 'red-teamed and fully reconciled (6 findings FIXED, 8.5/10)'; no EVOLVE-findings.md on disk — UNVERIFIABLE from the findings artifact",
    "K-1": "KNOW merge claims base 'red-teamed + reconciled' 8.5/10; no KNOW-findings.md on disk — only LEARN/PROVE findings files on record",
    "cross_cutting": "X-1 — recurring family across merged ACT/LAW reviews (M01/M02/M-LAW-01/02/03/05)",
    "negative_control": "P-1 CHECKED — PROVE's 'all 16 findings reconciled, App. A' claim maps onto real findings with Appendix-A evidence; this is the model"
  },
  "rule": "no_reconciliation_artifact_no_reconciliation_claim",
  "procedure": [
    "list every status claim a merge decision makes about its base (red-teamed, reconciled, findings FIXED count, scores)",
    "locate the base's reconciliation artifact (per-finding FIXED marks in the redteam findings file)",
    "no artifact on disk -> downgrade claim to assertion; return to author: produce the artifact or retract to checkable wording",
    "artifact exists -> spot-check two findings against their FIXED evidence (PROVE's 16-with-Appendix-A is the model)"
  ],
  "related": ["SN-020 (asserted-not-verified)", "SN-027 (amendment premise verification)", "SN-034 (AST verify cosmetic claims)", "SN-036 (push-run CI evidence completeness)"]
}
~~~
