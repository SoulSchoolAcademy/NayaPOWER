# NayaPOWER Current-State Wiring Map — 2026-10-09

**Purpose:** Establish the actual repository/runtime wiring before additional end-to-end learning experiments.
**Evidence basis:** GitHub `main` at `527ebcfbc04896c3a6beee127757785597e0713a`; connected Supabase project `dahisasgpfvziswqvmvm`; live Edge Function metadata/source; read-only schema and row inspections.
**Status:** DIAGNOSTIC SNAPSHOT — not a ratified architecture change, not a deployment authorization, and not proof of learning.
**Human authority:** Shawn Vibert.

## Executive finding

Capture and persistence work on a real path. There are also multiple independent runtime pieces for identity, authority, memory, action, provenance, relationships, verification, and succession. However, the canonical nine-node contract and `BRAIN/03-KERNEL/MANIFEST.json` still declare universal runtime binding `NOT_PROVEN` and leave the runtime entrypoint null. The repository must not claim that nine implementations form one connected organism until the actual call/handoff chain is evidenced.

## Current path observed in source

```
GitHub .naya/capture/** change
  -> .github/workflows/live-intelligence-commit-proof.yml
  -> nayanet-intelligence-commit-runtime
  -> Supabase event + Intelligent Block + lineage + relationship + index + checkpoint + receipt
  -> independent reread
  -> GitHub Smart Note projection + registry update
  -> admission-promotion workflow job (capture lifecycle CANDIDATE -> ACTIVE)
  -> cold-successor-held-out
  -> independent-behavior-verification

Live Supabase Runtime Proof workflow:
  -> nayanet-learning-verify mode=candidate (creates/repairs learning_evidence row)
  -> nayanet-cold-runtime-proof?mode=learning-influence
  -> nayanet-causal-learning-experiment (causal verification / independent reread)
  -> learning-promotion
  -> graph/control-treatment and cold-successor follow-on jobs
```

Important boundary: a Supabase event row is a recorded event, not a trigger by itself. The workflows and function calls are the orchestration mechanism. Smart Link identifies a projection; receipt + persisted reread/hash bind capture evidence; neither alone proves behavioral learning.

## Nine-node binding status

| Node | Current implementation evidence | Current conclusion |
|---|---|---|
| SELF | `kernel/self_node.py`, identity binding/persona modules | Implementation exists; unified production binding not proven |
| LAW | `nayanet-law-runtime`, `kernel/protocol/authority_gate.py` | Implementation exists; parity/binding must be proven per runtime |
| ACT | `kernel/act_pipeline.py`, `nayanet-act-runtime` | Implementation exists; no claim that every learning path invokes it |
| KNOW | `nayanet-know-runtime`, registry/retrieval components | Implementation exists; must prove ranked retrieval and downstream consumer |
| PROVE | `nayanet-prove-runtime` and receipt/lineage paths | Implementation exists; verify exact evidence path per capture |
| CONNECT | shared selector / intelligence retrieval / graph runtimes | Distributed implementation; one end-to-end binding not proven |
| VERIFY | causal verification and verified-action runtimes | Distributed implementation; independent proof must be bound to the exact lesson |
| LEARN | `nayanet-learning-verify`, causal experiment/promotion path, Python admission gate | Partial; production gate placement and actual behavior-change loop not fully wired |
| EVOLVE | cold runtime/successor mechanics and handoff receipts | Partial; governed improvement/compounding not proven as one closed loop |

Canonical references:
- `BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.md`
- `BRAIN/03-KERNEL/MANIFEST.json`
- `BRAIN/00-ARCHITECTURE/MACHINE-INTELLIGENCE.json`
- `BRAIN/00-ARCHITECTURE/ACTIVATION-NAYA-PLAN.md`
- `BRAIN/07-LEARNING/learning-system-blueprint-v1.md`

## State and admission are distinct

Do not conflate these fields:
- Capture `lifecycle_state`: whether the capture version is current/active or superseded.
- Intelligent Block `understanding_state`: epistemic/learning state such as `CANDIDATE` or `LEARNED`.
- `learning_evidence.status`: status of an evidence/learning record.

The workflow now has an `admission-promotion` job between independent verification and cold retrieval. Its inline gate currently checks basic structure and relies on job ordering for verification; it does not itself validate a falsifiable experiment contract. Separately, PR #2049 merged `tools/learning_admission_gate.py` and `tools/learning_verification_queue.py`. Those are Python-side gate/queue components; repository search shows the choke point/queue calls in the Python modules/tests, but no proven production call from the Supabase learning path. Do not wire the gate indiscriminately to capture: its contract distinguishes a capture/provenance row from a learning-experiment claim. Reconcile the exact claim lifecycle and evidence schema before changing the write point.

## Live Supabase observations

- `nayanet_intelligence_commit_runtime`: deployed version 82; inspected deployed `index.ts` exactly matches current `main` source.
- `nayanet-learning-verify`: deployed version 98; inspected deployed source differs from current `main` source (deployed file length 38,539 characters; main file 39,822).
- `naya-decision-context`: deployed version 10; inspected deployed source differs from current `main` source (deployed file length 2,814 characters; main file 3,208).
- `nayanet-act-runtime`: deployed version 65; source parity was not established by the inspected response.
- Read-only row counts: 181 Intelligent Blocks; 195 cognition events; 143 learning_evidence rows (107 ACTIVE, 32 RETIRED, 4 NOT_SUPPORTED); Intelligent Block understanding_state counts: 95 CANDIDATE, 85 LEARNED, 1 VERIFIED. These counts are not a behavioral-learning score.
- T11 block `IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical`: Supabase row status DURABLE, understanding_state CANDIDATE, owner_scope PRIVATE; event `c80f6c27-e114-4513-8d92-e15fffa3bc4f`; receipt `7eface12-492c-4a9f-a40a-34d9a78a1866`. Registry projection is `SN-782`, truth_state CANDIDATE, lifecycle_state CANDIDATE, projection status GITHUB_BRAIN_PUBLISHED, Smart Link status ACTIVE_AUTH_GATED. This proves persisted candidate/projection metadata, not T11 behavioral learning. The reported SN-782 identity collision remains unresolved and must be reconciled before any conflicting write/merge.

## Security finding — requires human policy decision

Live schema inspection found Row Level Security disabled on:
- `public.smart_note_events`
- `public.smart_note_artifacts`
- `public.smart_note_receipts`

No policies were returned for those three tables. These tables may be exposed to client roles. Do not blindly enable RLS without policies because that can break legitimate access; define least-privilege policies for intended owner/runtime operations, review them, and obtain the required human decision before applying the database change. This is separate from learning acceptance and must not be silently ignored.

## Source/runtime parity and open work

- PR #2037 is still a draft and its base SHA is `1d73652231ac6127806640af5a31eb516c60738d`, behind the inspected current main `527ebcfbc04896c3a6beee127757785597e0713a`. Do not treat that draft as the current deployed truth without refreshing/reconciling it.
- PR #2012 (GitHub projection 403 diagnostic) is still draft and not deployed. Deployed `nayanet-github-dispatch` version 36 does not contain its diagnostic receipt change.
- The canonical activation plan marks production deployment of mismatched Edge Function bytes as a human gate. No production deployment is authorized by this diagnostic.

## Ordered closure queue — assemble before full end-to-end experiment

1. **Freeze the shared state/evidence contract.** Define distinct schemas for capture lifecycle, Intelligent Block understanding state, and learning-experiment admission/promotion.
2. **Close source/runtime parity.** Produce exact per-function source parity receipts for learning-verify, ACT, decision-context, and commit-runtime; resolve deployment gaps only through the documented human gate.
3. **Unify intake.** Reconcile the v2 capture path with the legacy `v7-smart-note-canonical` receiver. Choose one writer for each canonical record and for `learning_evidence`; define a deduplication key across retired paths. No second brain/store.
4. **Wire the proper learning admission point.** Route an actual pre-registered experiment claim through the admission contract at the correct stage. Log input hash + reason/verdict; prove reject/pass/fail-closed cases. Do not confuse capture receipts with learning claims.
5. **Wire and evidence all nine-node handoffs.** Resolve each contract binding to an executable implementation, input/output schema, authority boundary, produced/consumed event, and durable receipt. Missing binding must fail closed.
6. **Connect retrieved lesson to action.** Demonstrate the ranked selector supplies the exact applicable lesson to the authorized decision consumer; record the applied lesson ID and observed outcome.
7. **Close state back-sync and identity collisions.** DB and repository must agree on canonical state; resolve SN-782 collision and ensure only one authorized promotion writer.
8. **Address the RLS security finding.** Review least-privilege policies and obtain the required human decision before applying changes.
9. **Only after assembly:** run the preregistered CONTROL / TREATMENT / WRONG-LESSON, independent scorer, cold-successor, unrelated-refusal, and repeatability suite. Do not count fallback, exact-hash-only retrieval, or a Smart Link as learning proof.

## Acceptance boundary

A stage is complete only when its producer, consumer, state transition, authority check, failure path, and durable receipt are all evidenced against the exact source/runtime version. `UNKNOWN` and `BLOCKED` are not PASS. A stored note is not a learned lesson. A deployed source mismatch is not parity.
