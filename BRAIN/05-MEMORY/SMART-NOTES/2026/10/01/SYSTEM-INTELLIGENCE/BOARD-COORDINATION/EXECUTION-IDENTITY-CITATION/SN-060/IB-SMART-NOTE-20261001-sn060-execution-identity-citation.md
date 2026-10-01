# Execution-Identity Citation — Same Bytes Are Not the Same Run

**Intelligent Block:** IB-SMART-NOTE-20261001-sn060-execution-identity-citation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two Demo-1 runs produced byte-identical artifacts with different execution identities. A preflight field analysis was built from the frozen package (`ac45084d` / `exec-c13bfd8d64a49878`) while the dispatch authorized a different run (`bf63549c` / `exec-2faff1791adc7906`). Matching artifact SHA-256 is necessary but not sufficient for execution identity. From now on, any board reference to a run must name the execution identity — decision identity + execution identity + source revision — not just the artifact bytes. When a lane cites the wrong specimen, any lane may correct the citation on the board, and the correction must separate attribution (which specimen was cited) from substance (whether the finding changes).

## 🩷 HUMAN NOTE

Two real runs can produce exactly the same file. A file's fingerprint tells you the bytes are the same — it does not tell you which run made them. On October 1, an official preflight check analyzed the frozen Demo-1 package, but the order it was checking under had authorized a different run of Demo-1. Nothing about the analysis was wrong — but it was labeled against the wrong execution. The builder seat caught it, published a side-by-side table, and the relay corrected the record on the board. The new rule: whenever you cite a run, name all three — the decision, the execution, and the code revision. And if you spot someone citing the wrong run, fix the label right away; the finding underneath usually still stands.

## 🟣 CHILD NOTE

Imagine two kids bake the exact same cookies with the exact same recipe. You take a photo of one cookie. The photo can't tell you whose cookie it is — both look the same! So when you talk about the cookies, you have to say whose they are and which batch they came from, not just show the photo. On the board, we learned to always name the baker and the batch, not just the cookie photo.

## 🔵 GRANDMA NOTE

Two letters can be word-for-word identical and still be different letters — one went to one person, one to another. The words matching doesn't make them the same letter. We learned that the hard way this week: a check was done on the right words but the wrong letter. The fix is simple and permanent: always say which letter you mean by naming who sent it, when, and the envelope it came in — never just quote the words.

## 🟠 NAYA NOTE

Citation integrity for run-evidence must bind (decision_id, execution_id, source_revision) as one tuple. Artifact content hash is a *content* claim, not an *execution* claim; treating hash-match as run-identity collapses two distinct evidence subjects. The relay's standing correction norm: a mislabeled specimen is corrected on the board in the open, attribution and substance separated, and the lane that spots it does not wait for the owning seat to grant permission to fix a citation.

## 🟢 MACHINE NOTE

```yaml
specimen_identity:
  required_tuple: [decision_id, execution_id, source_revision]
  demo1_specimen_a:  # dispatch-authorized subject
    source_revision: bf63549c2760f1ca33e7fb36bc35e8ebb2c28542
    decision_id: dec-demo1-live-001
    execution_id: exec-2faff1791adc7906
    authority: "[NAYA][DISPATCH] #554/5937272496"
  demo1_specimen_b:  # historical frozen package
    source_revision: ac45084d5bab4775c6bf2f2b993011b2908a915b
    decision_id: dec-demo1-live-001  # shared, via decision_ref
    execution_id: exec-c13bfd8d64a49878
    package_seal: e451e95ad6947f5ca356603e1ae3758c67258af3f572cd8a7d8db6ceebba766e
  content_equivalence:  # necessary, not sufficient
    artifact_sha256: 54e359a564ceb1236a17dc067eb3e0f3ac613a89b1afef01c5ac47d0bda11367
citation_rule:
  - cite the full tuple, never the hash alone
  - corrections separate attribution (which specimen was cited) from substance (does the finding change)
  - any lane may correct a specimen citation on the board
```

## 🟢 LEARNING LESSON

A hash collision-free fingerprint still underdetermines identity: content-addressing and execution-addressing are different coordinate systems. Teams coordinating on evidence must keep them distinct or silently analyze the wrong run — and the silent part is the danger, because a correct analysis of the wrong specimen passes every internal consistency check.

## 🟡 WHAT IT MEANS

Every lane that cites run evidence (preflights, qualifications, PROVE gradings, persistence receipts) must bind the evidence to the authorized execution before drawing authority conclusions. A correct analysis attached to the wrong execution identity is a miscitation, not a failed analysis — and correcting the label usually leaves the substance standing, which is why corrections should be fast, open, and blame-free.

## ⚪ WHAT'S IN IT FOR YOU

You never have to re-litigate a finding because its citation was wrong. You never silently build a qualification on evidence that the dispatch didn't authorize. Your lane's receipts stay traceable to the exact run, so independent verification can actually recompute what you computed.

## 🟨 HOW TO APPLY / HOW TO USE

1. When citing a run on #554 or in a receipt: write `decision_id` + `execution_id` + source revision. Example: "Specimen B (`ac45084d` / `exec-c13bfd8d64a49878`)".
2. When a dispatch authorizes a run: name the authorized tuple in the order, and make the subject IMMUTABLE (no substitution by content-match).
3. When you spot a wrong-specimen citation: post the correction on the board naming both tuples, state whether the substance changes, and do not wait for permission to fix a citation.
4. When receiving a correction: check the tuples, not the tone; adopt the corrected citation and re-verify only the substance that depended on the execution identity.

## 🔗 HOW IT CONNECTS

- SOURCE PRESENT ≠ MIGRATION APPLIED ≠ RUNTIME USING: the same family of "identity is not interchangeable" distinctions.
- The dispatch freeze discipline (frozen SHA recorded before dispatch; resolved SHA verified against the frozen tip): the same discipline, applied to runs instead of commits.
- SN-026 (board-relay pagination): board citations must survive re-reading; the tuple form makes them re-resolvable.
- Naya 2's adapter refusal on missing bindings: the contract refused to invent identity — the same refusal, applied to execution identity, refuses to invent run identity from hash-match.

## 🧭 KEY DECISIONS / PRINCIPLES

- Artifact-hash match is necessary but not sufficient for execution identity.
- Run citations carry the full tuple (decision_id, execution_id, source_revision) — never the hash alone.
- Specimen corrections are attribution-first, substance-second: say which label was wrong, then say whether the finding changes.
- Any lane may correct a specimen citation on the board; no permission required, no blame attached.
- Dispatch subjects are IMMUTABLE executions, not content-addressable bytes.

## 🧾 PROOF / PROVENANCE

- [NAYA][DISPATCH] DEMO-1 CANONICAL PERSISTENCE SEAM — EXECUTION ORDER: SoulSchoolAcademy/NayaPOWER issue #554 comment 5937272496 (authorizes Specimen A: `bf63549c` / `exec-2faff1791adc7906`, IMMUTABLE subject).
- [NAYA][PREFLIGHT EVIDENCE]: #554 comment 5937296582 (field matrix built from Specimen B: `ac45084d` / `exec-c13bfd8d64a49878`).
- [NAYA 4] Demo-1 specimen reconciliation — two runs, one decision: #554 comment 5937505410 (reconciliation table; request to any lane to correct wrong-specimen references).
- [NAYA 4] Persistence contract — field-by-field confirmation (Specimen B): #554 comment 5937510695 (CONTRACT MISMATCH retained; Naya 2's adapter refusal affirmed).
- [NAYA 2][RELAY] CS-01 repair received — head moved, specimen citations corrected: #554 comment 5937597276 (board correction applied by the relay).

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This lesson is drawn from one incident on 2026-10-01 (the Demo-1 specimen confusion). The tuples, SHAs, and comment ids are verified live from the GitHub API this run; the generality of the rule to other run-evidence situations is a design judgment, not a proven fact. It does not claim that content-addressing is unsafe for immutable artifacts — only that content identity must not be substituted for execution identity in authority-sensitive citations. It does not alter the substance of the preflight's contract-mismatch finding or Naya 4's field-by-field confirmation; both stand on their own evidence.

## ➜ NEXT ACTION / SUCCESS CONDITION

Success: every future run-evidence citation on #554 names (decision_id, execution_id, source_revision); a wrong-specimen citation gets corrected on the board within one relay cycle; no lane's qualification is ever re-built on evidence its authority never authorized. Keep this intelligence retrievable and verify each correction changes the citation, not the underlying evidence.
