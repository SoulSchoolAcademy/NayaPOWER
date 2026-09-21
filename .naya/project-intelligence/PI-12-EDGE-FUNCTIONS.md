# Project Intelligence — 12 Edge Functions

**Deployment target:** Supabase project `dahisasgpfvziswqvmvm`  
**Status:** 12/12 ACTIVE  
**Authentication:** JWT required on all 12  
**Core implementation:** `nayanet-compound-intelligence` v6  
**Rule:** A PI may act without asking a human only inside the explicitly bounded operation named by the endpoint, with the authenticated user's authority and existing project policies. Capability never creates authority.

| # | Edge Function | Fixed operation | Boundary |
|---|---|---|---|
| 1 | `nayanet-pi-restore` | RESTORE | Read/restore current governed context; no state mutation |
| 2 | `nayanet-pi-retrieve` | RETRIEVE | Read user-scoped project intelligence matching a query |
| 3 | `nayanet-pi-reconcile` | RECONCILE | Compare durable operation/bridge evidence; no authority escalation |
| 4 | `nayanet-pi-understand` | UNDERSTAND | Persist an interpretation as an understanding event; explicitly not verified fact |
| 5 | `nayanet-pi-learning-candidate` | LEARNING CANDIDATE | Create candidate learning from a user-owned source event; candidate is not active learning |
| 6 | `nayanet-pi-learning-verify` | LEARNING VERIFY | Promote only an existing candidate/active learning item when verification evidence is supplied |
| 7 | `nayanet-pi-successor-handoff` | SUCCESSOR HANDOFF | Persist successor context and continuity evidence |
| 8 | `nayanet-pi-share` | SHARE | Publish only with explicit consent in the operation payload; no implicit public sharing |
| 9 | `nayanet-pi-supersede` | SUPERSEDE | Create a new user-owned intelligence revision with explicit supersession lineage |
| 10 | `nayanet-pi-health` | HEALTH | Read-only operational counts/laws |
| 11 | `nayanet-pi-dream` | DREAM | Delegate to governed Dream Replay; preserve existing authorization/idempotency boundary |
| 12 | `nayanet-pi-compound` | COMPOUND | Produce the governed compounding cycle/context; does not silently mutate authority |

## Non-negotiable governance

- **Capability does not create authority.**
- **Unknown ≠ verified.**
- **Blocked ≠ pass.**
- **Unverified learning is never silently promoted.**
- **Share is explicit-consent only.**
- **Secrets/tokens are never returned to the human surface.**
- **The PI does not bypass the existing authenticated runtime.**
- **State mutation requiring director authority remains fail-closed in the underlying orchestrator.**
- **The 12 endpoints are thin fixed-action boundaries over the already deployed governed orchestrator; they do not create a second source of truth.**

## Proof standard

Deployment existence is proven by the Supabase Edge Function registry: each endpoint is ACTIVE, version 1, and JWT protected. Behavioral proof still requires an authenticated invocation of each endpoint and verification of its durable result.