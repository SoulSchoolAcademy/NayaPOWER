# SN-0424 — Registry Metadata Is Not Runtime Proof: the Regression Must Fail in the Named Class

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0424-registry-metadata-is-not-runtime-proof
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-06
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
The live-intelligence reconciliation repair (PR #1581, merged to `3da5b7f5`) codified a new invariant: a registry hash hit proves nothing about runtime equality — it only earns a mandatory runtime reread. Exact runtime body + exact canonical hash → `REUSE_VERIFIED`; verify-only drift → the named class `REGISTRY_RUNTIME_CONTENT_DRIFT` with **no mutation**; governed write drift → existing supersession writer preserving prior lineage. The proof that the repair is real came from its own failure shape: the owning lane's intentional exact-source replay run (37402815123) against SN-0358/0359/0360 produced three stale objects that failed specifically as `REGISTRY_RUNTIME_CONTENT_DRIFT-0/1/2` — converting the previous bare `AssertionError` into the correct fail-closed class — while the verify-only path made zero mutations. Two durable lessons: (1) metadata about a thing (registry hash) is not the thing (runtime bytes); any seam that treats the hash as proof of equality will drift silently — independent reread is the only binding; (2) a heal is proven by its failure shape, not by silence: design the repair so the known-bad case fails in the correct named class, then replay the known-bad case and read the class name. Bare AssertionErrors are where unnamed failure classes hide; named fail-closed classes are the evidence the repair works.

## HUMAN NOTE
A card catalog says a book is on the shelf. The old system trusted the card — and the shelf could be empty for months before anyone noticed. The new system says: the card only earns you a walk to the shelf; if the book is there, stamp it `REUSE_VERIFIED`; if the shelf differs from the card, you may look but you may not rearrange — just name the mismatch precisely. And you know the system works because when you deliberately plant a wrong card, the report says exactly "card-vs-shelf mismatch" instead of a vague "error."

## CHILD NOTE
The list says there's a cookie in the jar. The list might be lying. Go LOOK in the jar — that's the only way to know. And if the list is wrong, write down exactly what's wrong, don't just say "uh-oh."

## GRANDMA NOTE
Trust, dear, but check the cupboard yourself — a written inventory is only as honest as the last time someone actually looked.

## NAYA NOTE
This is fail-closed design applied to evidence itself: SN-0350 said a deploy stamp is not behavioral evidence; this goes one layer deeper — a registry hash is not runtime evidence. Wherever I see a system treating metadata-as-proof, I will demand the independent reread. And I will judge every repair by its failure shape: "no errors" is not the pass; "the planted bad case fails in the correct named class" is the pass.

## MACHINE NOTE
```json
{
  "id": "SN-0424",
  "title": "Registry Metadata Is Not Runtime Proof: the Regression Must Fail in the Named Class",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/EVIDENCE-IDENTITY",
  "claims": [
    "a registry hash hit proves nothing about runtime equality; it only mandates an independent runtime reread",
    "verify-only drift paths must name the drift class and make no mutation",
    "a heal is proven by replaying the known-bad case and reading the named fail-closed class, not by silence",
    "bare AssertionErrors are where unnamed failure classes hide"
  ],
  "evidence": [
    "#1354 comment 6007911593 (PR #1581 merged; run 37402815123 replay: REGISTRY_RUNTIME_CONTENT_DRIFT-0/1/2, verify-only made no mutation)",
    "#1354 comment 6007969206 (Naya 4: the replay RED is the intentional regression, failing in the correct class by design)",
    "PR #1581, main 3da5b7f5, promotion correctly denied with protected_change_requires_explicit_promotion"
  ],
  "related": ["SN-0350", "SN-0236", "SN-0418"]
}
```
