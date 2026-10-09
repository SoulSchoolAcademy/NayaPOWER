# IB-SMART-NOTE-20261009-sn0835-diagnostic-document-status-claims-expire

Intelligent Block: SN-0835
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A Naya seat read `BRAIN/07-LEARNING/learning-system-blueprint-v1.md` at main SHA `527ebcfbc04896c3a6beee127757785597e0713a` and found the diagnostic document embeds an older verified baseline (`1d736522…`) and describes the admission gate as branch-only/no-PR — flatly contradicting later verified receipts (#2049 merged, #2048 merged). The seat issued a source-reconciliation correction: the document's architecture/gap analysis stays useful, but its historical implementation-status claims must NOT be treated as current without a fresh exact-head check. Rule: no old diagnostic snapshot may overrule newer verified code; each prior finding gets marked CONFIRMED / FIXED / STALE / UNKNOWN with source and SHA.

Provenance: NayaPOWER #1354 comment 6090875248 ([ACTIVATION-PUSH] Source reconciliation correction — blueprint snapshot is stale, 2026-10-09T23:15:48Z, SoulSchoolAcademy). Canonical assembly authority named in the comment: the Learning Engine Assembly Blueprint (PR #2037).

## HUMAN NOTE

Diagnostic documents are old maps: the terrain analysis still reads true, but the "here be dragons" labels expire the moment newer expeditions return. The seat that noticed didn't throw the map away — it split the map into two layers: how the territory works (durable) and who explored what when (stale). The discipline is tiny and saves you from the worst failure in evidence work: letting a confident old document outrank living code.

## CHILD NOTE

Your school's old handbook says lunch is at 11:30, but this year lunch moved to 12. Read the handbook to learn how lunch works — never to learn what time lunch is. What time lunch is lives on the clock on the wall, checked right now.

## GRANDMA NOTE

Keep grandmother's recipe book for the recipes — never plan this year's holiday dinner from her 1987 note about who was coming. Use old documents for how things work; check living sources for how things are.

## NAYA NOTE

Operational rules:

1. Two-layer reading: separate ARCHITECTURE (how the system works — survives) from STATUS CLAIMS (what's done, what's merged — expires at write time). Quote and rely on the first; quarantine the second.
2. Any diagnostic document that cites a baseline SHA names its own expiry. Treat every implementation-status claim as STALE until re-verified at the current live head.
3. Reconcile, don't erase: mark each prior finding CONFIRMED / FIXED / STALE / UNKNOWN with source and SHA before retiring it. The marker, not deletion, is what stops the next reader from re-litigating it.
4. Precedence: canonical assembly authority outranks diagnostic documents when they conflict (here: the Learning Engine Assembly Blueprint, PR #2037, per the document's own header).
5. Never infer full integration from module presence: node modules and unit tests existing does not prove runtime binding (the nine-node manifest's NOT_PROVEN on universal binding stands until a wiring manifest says otherwise).

## MACHINE NOTE

```json
{
  "sn": "SN-0835",
  "truth_state": "CANDIDATE",
  "doctrine": "Diagnostic documents carry a two-layer truth: architecture survives, status claims expire at write time. Re-verify every status claim at the current live head; mark each prior finding CONFIRMED/FIXED/STALE/UNKNOWN with source+SHA. No old diagnostic snapshot may overrule newer verified code.",
  "falsifiers": [
    "Acting on a diagnostic document's implementation-status claim without a fresh exact-head check",
    "Letting a diagnostic document's embedded baseline SHA outrank later verified merge receipts",
    "Deleting a stale finding instead of marking it STALE with source and SHA"
  ],
  "applies_to": "all blueprint, diagnostic, and gap-analysis documents whose status claims age against main"
}
```
