# ðŸ”± Smart Connect â€” Seven-Door Authority Matrix
**Date:** 2026-09-24
**Repository:** SoulSchoolAcademy/NayaPOWER
**Canonical room contract:** `NAYANET/HUB-ROOM-SYSTEM/04-SMART-CONNECT.md`
**Evidence anchor:** Universal Envelope production bridge run `36054810899` + focused relationship proof `NAYANET_SMART_CONNECT_RELATIONSHIP_SECURITY_PROOF_V1`

## Governing rule

Smart Connect is participation, not authority.

**Connection â‰  Permission. Authentication â‰  Authorization. Participation â‰  Execution authority.**

Every door must converge on the existing governed core:

**DOOR â†’ AUTHENTICATION â†’ IDENTITY â†’ PARTICIPATION â†’ AUTHORITY â†’ SCOPE â†’ CONSENT â†’ PERSISTENCE â†’ REVOCATION â†’ ACTIVITY/EVIDENCE â†’ REPLAY/IDEMPOTENCY â†’ FRESH RETRIEVAL**

No door may create a second connection store, authentication model, authority model, or intelligence source of truth.

## Common participation boundary â€” independently verified

The canonical relationship substrate is `public.nayanet_connections`, reached through the existing authenticated runtime/RPC boundary.

Fresh adversarial proof verified:

- owner creates A â†’ B Connection;
- owner retrieves the canonical row;
- non-owner B cannot retrieve A's row;
- non-owner B cannot revoke A's row;
- replayed connect is idempotent and returns the same Connection;
- owner revocation succeeds;
- replayed revoke is idempotent;
- owner sees the canonical row as `revoked`;
- non-owner remains unable to retrieve the row after revocation.

Proof schema: `NAYANET_SMART_CONNECT_RELATIONSHIP_SECURITY_PROOF_V1`.

This proves the **relationship/participation seam**, not the seven external technical doors themselves.

## Seven-door matrix

| Door | Authentication | Participation / identity | Authority | Scope / consent | Persistence / evidence | Revocation | Replay / idempotency | Current truth |
|---|---|---|---|---|---|---|---|---|
| **GitHub App** | GitHub installation / app identity; exact mechanism must remain external to source | Repository/user installation participation; installation identity must remain distinct from human identity | Separate Naya authority grant + least-privilege GitHub installation/repository scope | Repository, installation, action scope; human consent must be explicit | GitHub observation + canonical Naya event/receipt; no GitHub source-of-truth substitution | App installation/token/repository permission revocation must block subsequent actions | Webhook/action replay must be idempotent by canonical event/idempotency identity | **PARTIAL** â€” repository authority exists; independent end-to-end production agent proof remains open |
| **MCP** | MCP transport/session authentication | Agent/client identity participates through the same governed runtime | Server-side authority grant; tools/call must not infer permission from connection | Tool + project + target scope; explicit consent where required | Canonical event/receipt + fresh retrieval | Session/token/grant revocation must block calls | Request/idempotency key must prevent duplicate durable effects | **LIVE VERIFIED** â€” UAI run `36061300293` authenticated initialize â†’ tools/list â†’ cold restore â†’ understand â†’ retrieve â†’ restore with canonical receipt/evidence; governed execution boundary additionally verified in Attack 4 run `36062784233` |
| **REST/OpenAPI** | Authenticated API identity | API client participates through canonical API boundary | Same authority lifecycle as MCP; transport must not create a second authority model | Endpoint/action/target/project scope | Same canonical persistence and receipt chain as MCP | Credential/grant revocation must fail closed | Idempotency and replay behavior must match MCP semantics | **LIVE VERIFIED** â€” UAI run `36061300293` authenticated cold restore â†’ understand â†’ retrieve; run `36064087479` additionally proved governed intelligence_commit authority parity through the same canonical UAI adapter/runtime |
| **Webhooks** | Signed/verified sender identity | External system becomes an event source, not an authority source; current receiver does not persist an explicit GitHub installation ID or resolve repository → participation/member owner | Inbound event authenticity does not authorize downstream execution; receiver uses github_webhook_received, not intelligence.capture | Event/source scope; repository binding currently comes from repository.full_name, but no governed installation/repository → member resolution seam exists in the receiver | Canonical nayanet_record_cognition_event â†’ cognition event/project state/execution receipt; downstream projection is not invoked by the receiver | Secret/source registration revocation remains external and unverified | Cognition event has unique (user_id,project_id,event_id); the six-argument replay path is now hardened to return the original event/state/receipt without creating a second receipt or advancing project state. Live webhook replay remains NOT VERIFIED until the external secret is configured | **BLOCKED_EXTERNAL_CREDENTIAL** â€” deployed fail-closed receiver; positive signed delivery and exact replay remain unverified |
| **SDK** | Application/client authentication | Embedded client participates through canonical SDK adapter | SDK delegates authority to governed runtime; local SDK capability must not become authority | App/project/user scope plus explicit action consent | Same canonical event/persistence/evidence path | App credential/grant revocation must block governed actions | SDK retries must be idempotent at canonical boundary | **DOCUMENTED / UNPROVEN** â€” adapter concept exists; independent production door proof remains open |
| **A2A** | Agent identity/authentication | Agent participates as an external actor through governed adapter | Authority must be independently evaluated; agent relationship never implies execution permission | Agent/task/project/target scope | Canonical agent event + execution receipt + fresh retrieval | Agent credential/grant/task revocation must block subsequent actions | Message/task replay must preserve idempotent canonical outcome | **DOCUMENTED** â€” future channel; no broad-use production proof established |
| **MCP Apps** | MCP app/session authentication | App participates through MCP capability boundary | Same server-side governed authority as MCP; app UI cannot grant itself permission | Tool/app/session/project scope + consent | Canonical MCP event/receipt path | Session/app/grant revocation must fail closed | UI retries and tool-call replay must converge on canonical idempotent effect | **DOCUMENTED / UNPROVEN** â€” defined door; independent production proof remains open |

## Required proof sequence

The seven doors are **not** seven separate brains or seven separate authorization systems.

### Phase A â€” common relationship seam
**VERIFIED**

Owner/non-owner/revocation/replay proof is complete for the canonical relationship substrate.

### Phase B â€” door convergence
For each door, prove:

1. unauthenticated request is rejected;
2. authenticated participation is established;
3. connection/participation does not create execution authority;
4. authorized action requires the existing authority boundary;
5. scope is enforced server-side;
6. persistence lands in the canonical event/receipt path;
7. fresh retrieval reconstructs the same result;
8. revocation blocks subsequent use;
9. replay is idempotent;
10. non-owner / wrong-scope access is denied;
11. evidence records actor, authority, decision, execution, persistence and receipt lineage.

### Phase C â€” parity
For MCP and REST/OpenAPI specifically, prove semantic parity:

**same identity â†’ same authority rules â†’ same canonical object â†’ same persistence â†’ same receipt semantics â†’ same fresh retrieval truth.**

## Evidence boundary

The production Universal Envelope bridge proof is independently **VERIFIED** at run `36054810899` on main commit `943192584c8829225d7ff4841e2140d5be004d9c`.

The first Universal Agent Interface production transport proof is independently **VERIFIED** at run `36061300293` on main commit `e316ac9311230bf2f4f182971c440c3ef0c81559`; UAI version `3318bb4b-a31c-4efb-a872-888b10b87810` passed authenticated MCP + REST persistence/retrieval parity.

The governed execution/authority proof is independently **VERIFIED** at run `36062784233` on main commit `dcdc299349a9e14c2a39fc4f627e08e140863c6b`: MCP participation connected without changing authority; one live `intelligence_commit` was authorized and independently reconstructed with actor, authority, decision, execution, scope, governance and binding hash; exact replay returned the same event/checkpoint identity; MCP participation revocation left authority unchanged; authority-grant revocation then denied a fresh commit with `AUTHORITY_REQUIRED:GRANT_REVOKED`.

It proves:

**fresh owner â†’ existing envelope adapter â†’ production bridge â†’ persisted receiver transaction/event/receipt/index â†’ independent retrieval â†’ independent reconstruction â†’ exact replay**

It does **not** by itself prove any of the seven Smart Connect doors.

The focused relationship proof proves the shared participation substrate and adversarial relationship lifecycle. It does **not** promote any external door to production-ready.

## Single next frontier

**Execute the first door-specific adversarial proof against the existing authority seam, beginning with the Universal Agent Interface pair: MCP + REST/OpenAPI.**

Required chain:

**authenticated initialize â†’ tools/call â†’ authority decision â†’ canonical persistence â†’ fresh retrieval â†’ verified outcome â†’ revoke â†’ denied reuse â†’ exact replay semantics â†’ REST parity**

No new authority model. No second backend. No direct Hub-to-Supabase bypass.


## 2026-09-24 live evidence â€” continuation after production bridge verification

### Production bridge boundary

Run `36054810899` is **VERIFIED** on `main` commit `943192584c8829225d7ff4841e2140d5be004d9c`. The proof job independently verified fresh owner bootstrap, existing envelope adapter validation, production receiver transaction/event/receipt/index persistence, independent retrieval, lineage reconstruction, and exact replay with the same receiver transaction/event/receipt lineage.

### Common relationship seam â€” live adversarial proof

The canonical `nayanet_connections` boundary was exercised with two authenticated identities in a rollback-scoped production database transaction:

- Owner A â†’ B connection: `CONNECTED`.
- Owner replay: `ALREADY_CONNECTED`.
- Non-owner B revoke attempt: `CONNECTION_NOT_FOUND` / **BLOCKED**.
- Owner A revoke: `REVOKED`.
- Owner replay revoke: `ALREADY_REVOKED`.
- `nayanet_connections` RLS: owner retrieval visible; non-owner retrieval count `0`.
- The canonical connection uniqueness constraint remains `(owner_member_id, connected_member_id)`.

This proves the common relationship authority seam without creating a second relationship store.

### Seven-door participation proof

All seven canonical doors were exercised against the same `nayanet_smart_connect_participation` RPC/table boundary:

| Door | First connect | Replay connect | Authority | Publication | Non-owner disconnect | First disconnect | Replay disconnect |
|---|---|---|---|---|---|---|---|
| GitHub App | CONNECTED | ALREADY_CONNECTED | UNCHANGED | NOT_GRANTED | BLOCKED | DISCONNECTED | ALREADY_DISCONNECTED |
| MCP | CONNECTED | ALREADY_CONNECTED | UNCHANGED | NOT_GRANTED | BLOCKED | DISCONNECTED | ALREADY_DISCONNECTED |
| REST/OpenAPI | CONNECTED | ALREADY_CONNECTED | UNCHANGED | NOT_GRANTED | BLOCKED | DISCONNECTED | ALREADY_DISCONNECTED |
| Webhooks | CONNECTED | ALREADY_CONNECTED | UNCHANGED | NOT_GRANTED | BLOCKED | DISCONNECTED | ALREADY_DISCONNECTED |
| SDK | CONNECTED | ALREADY_CONNECTED | UNCHANGED | NOT_GRANTED | BLOCKED | DISCONNECTED | ALREADY_DISCONNECTED |
| A2A | CONNECTED | ALREADY_CONNECTED | UNCHANGED | NOT_GRANTED | BLOCKED | DISCONNECTED | ALREADY_DISCONNECTED |
| MCP Apps | CONNECTED | ALREADY_CONNECTED | UNCHANGED | NOT_GRANTED | BLOCKED | DISCONNECTED | ALREADY_DISCONNECTED |

The replay semantics above were the fail-first gap discovered during this continuation: before the bounded repair, connect replay returned `CONNECTED` and disconnect replay returned `DISCONNECTED`. Migration `20260924143000_harden_smart_connect_participation_idempotency_v1.sql` changed only those replay semantics to explicit no-op results. It did not create a new authority model, table, backend, or connection store.

### Transport frontier

`NAYANET/UNIVERSAL-AGENT-INTERFACE` is now **LIVE VERIFIED** at the authenticated transport/persistence/retrieval boundary by run `36061300293`. The existing release harness proved fail-closed unauthenticated REST/MCP, authenticated MCP initialization/tools, mandatory 14-question cold restore, MCP understand â†’ receipt â†’ retrieve, REST understand â†’ receipt â†’ retrieve, and same-canonical-path parity.

### Current next frontier

**Attack external-door authority parity, not the already-proven core.** The governed core now proves owner-bound authority, non-owner/wrong-scope denial, participation/replay/revocation semantics, and receipt reconstruction. MCP + REST transport/persistence/retrieval are live verified, but the UAI public surface currently exposes safe intelligence actions rather than `intelligence_commit`. The next bounded frontier is to prove the same authority grant/deny/revoke/replay semantics through an existing external door without creating a second authority model or backend.


## 2026-09-24 execution frontier â€” top 10 highest-value remaining items

1. **Unblock GitHub App/Webhook credential boundary.** Configure production `GITHUB_WEBHOOK_SECRET` through the external secret-management/admin surface; never place the secret in source or chat.
2. **Live-prove GitHub webhook ingress.** Positive HMAC verification â†’ canonical event persistence â†’ exact delivery replay â†’ one logical event â†’ independent retrieval.
3. **Prove webhook-to-authority separation.** A valid GitHub event must remain an event source, never implicit `intelligence_commit` authority; privileged execution must require an existing grant.
4. **Prove webhook disable/revocation.** Disable/revoke the source registration and demonstrate subsequent signed deliveries are rejected or quarantined.
5. **Prove GitHub App repository-scope isolation.** Authorized repository accepted; unauthorized repository rejected before private projection.
6. **Prove GitHub App/Hub two-way mutation boundary.** Hub action â†’ existing authority â†’ canonical event â†’ authorized GitHub mutation â†’ GitHub observation â†’ verification â†’ Hub projection.
7. **Audit SDK door.** Resolve whether an actual SDK adapter exists in production source; if absent, keep it DOCUMENTED/UNPROVEN rather than inventing an adapter.
8. **Audit A2A door.** Resolve whether an actual A2A adapter exists; if absent, keep it DOCUMENTED/FUTURE and define the smallest production seam.
9. **Audit MCP Apps door.** Determine whether the existing MCP surface is app-capable and prove that UI/session capability cannot grant authority.
10. **Run final seven-door cross-door invariance.** Same actor/authority/scope/revocation/idempotency semantics across every actually implemented door, with explicit NOT VERIFIED for doors lacking production infrastructure.

### Current live boundary

- Universal Envelope production bridge: **VERIFIED** â€” run `36054810899`.
- UAI MCP + REST transport/persistence/retrieval: **LIVE VERIFIED** â€” run `36061300293`.
- UAI privileged authority parity: **LIVE VERIFIED** â€” run `36064087479`.
- GitHub webhook function: **ACTIVE / BLOCKED_EXTERNAL_CREDENTIAL** â€” positive production proof cannot run because `GITHUB_WEBHOOK_SECRET` is not configured.
- No evidence was found in the repository tree for a separate SDK, A2A, or MCP Apps implementation beyond the documented contracts; these remain **NOT VERIFIED**.

### Job holes identified

- The first UAI proof targeted the PI continuation helper for an `intelligence_commit` grant; fail-first evidence showed it intentionally issues `pi.continue`, not `intelligence_commit`. Repaired by using the canonical `nayanet_issue_authority_grant` RPC.
- The first replay assertion used the wrong UAI JSON path and could compare null to null. Repaired by requiring exact source-event/checkpoint identity plus `replayed=true`.
- The privileged UAI commit path was initially absent from the external door. The bounded implementation now delegates directly to the existing governed runtime; no second authority or backend was introduced.
- GitHub webhook infrastructure is deployed but not operationally provable because its required external credential is absent.
- The remaining doors must not be promoted from documented contracts to production truth without actual adapter execution evidence.

### Evidence for this continuation

- `36054810899` â€” production Universal Envelope bridge.
- `36061300293` â€” UAI MCP/REST production transport/persistence/retrieval.
- `36064087479` â€” UAI privileged authority owner/replay/retrieval/non-owner/revocation proof.
- Direct production probe of `nayanet-github-webhook` â€” `503 GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED / BLOCKED_EXTERNAL_CREDENTIAL`.

### Single next action

**Configure `GITHUB_WEBHOOK_SECRET` in the production secret-management/admin boundary, then run the signed GitHub webhook positive â†’ replay â†’ persistence â†’ retrieval â†’ authority-separation proof.**


## 2026-09-24 P1 â€” GitHub Webhook credential boundary and safe preflight

**Status: BLOCKED_EXTERNAL_CREDENTIAL**

### Production credential boundary

The production Edge Function nayanet-github-webhook is ACTIVE, version 3, and its deployed digest is 081cc239fb9f6c662044ea13d3a56d4015baf0741d720b29bfbfa01bafa6349c. The repository source is NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts (blob cf00cb52b424783f37d25a2a89f031724b19543a).

A fresh production probe at 2026-09-24T22:11:01Z returned HTTP 503 with GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED and BLOCKED_EXTERNAL_CREDENTIAL, before delivery/signature processing or persistence. The secret value was not requested or handled. The current permitted Supabase tool surface exposes deployment/source metadata but no secret-management read/write operation.

### Safe call-graph findings

GitHub POST â†’ webhook Edge Function â†’ method check â†’ delivery/signature headers â†’ GITHUB_WEBHOOK_SECRET check â†’ HMAC-SHA256(raw body) â†’ JSON parse â†’ normalization â†’ service-role canonical cognition RPC â†’ cognition event + project state + execution receipt â†’ response.

No second inbound webhook implementation was found in repository source. The separate nayanet-github-dispatch function is outbound GitHub workflow dispatch, not an inbound webhook caller.

The receiver normalizes repository, actor, ref, commit SHA, delivery ID, source system, correlation ID, and idempotency key. It does not currently persist an explicit GitHub installation ID. The authority object in the normalized event is source/scope metadata, not execution authority.

### Critical preflight replay finding

The receiver uses the six-argument nayanet_record_cognition_event overload with action github_webhook_received. That overload now has canonical event-id replay protection. Production currently retains both six- and seven-argument overloads. The six-argument path de-duplicates the cognition row by (user_id, project_id, event_id) but still creates a new execution receipt and increments project cognition state on each replay. Therefore the required exact replay/idempotency property is NOT VERIFIED and has a concrete causal repair target. No repair is made in P1.

### Authority separation

Source inspection shows the webhook does not call the intelligence.capture authority-required action and supplies no execution authorization object. This is source-level evidence for WEBHOOK EVENT â‰  EXECUTION AUTHORITY. Live authority-separation proof remains unverified until a signed production event can be accepted.

### Adversarial preparation

Prepared, but not run in production: missing signature, wrong signature, altered payload, wrong repository, wrong installation/source, revoked/disabled source, duplicate delivery, and authority-separation checks. No production mutation was executed for this preparation.

### Durable evidence

- P1 artifact: .naya/project-intelligence/GITHUB-WEBHOOK-P1-CREDENTIAL-BOUNDARY-2026-09-24.md
- Main after evidence artifact: 1f4825405527f3e1a67b0a82aa7ec7ea14d0cde8
- UAI privileged authority proof: 36064087479
- UAI deployment: 36063359510

### Single next action

**Run the controlled signed production GitHub webhook proof after the authorized operator has configured the real production secret.**


## 2026-09-24 P2 â€” Canonical webhook replay/idempotency repair

### What changed

The highest-value unblocked causal hole identified during P1 was repaired in the existing canonical cognition persistence seam. Migration `20260924222644_harden_cognition_event_replay_idempotency_v1` changes the existing six-argument `nayanet_record_cognition_event` path so an existing `(user_id, project_id, event_id)` with its canonical receipt is treated as an exact replay: it returns the original event/state/receipt with `replayed=true`, without creating a second execution receipt or incrementing project cognition state.

No second backend, event store, authority model, or webhook ingress was introduced.

### Evidence

- Repository commit: `7451968c14f9285a43b6a61dfe971e5630d3e564`
- Production migration version: `20260924222644` / `harden_cognition_event_replay_idempotency_v1`
- Production function definition independently read back after migration and contains the replay branch.
- Existing cognition uniqueness remains `(user_id, project_id, event_id)`.

### Truth status

- Replay/idempotency implementation: **VERIFIED**
- Production schema application: **VERIFIED**
- Live signed GitHub replay proof: **NOT VERIFIED / BLOCKED_EXTERNAL_CREDENTIAL**
- Current direct webhook probe still returns HTTP 503 `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED` before signature processing.

### Remaining causal hole

The positive signed-production proof cannot yet cross the external `GITHUB_WEBHOOK_SECRET` boundary. The receiver also still does not persist an explicit GitHub installation ID, so installation-level isolation remains NOT VERIFIED.

### Single next action

**Configure `GITHUB_WEBHOOK_SECRET` in the authorized production secret-management/admin boundary, then execute the controlled signed webhook positive â†’ exact replay â†’ independent persistence/retrieval â†’ authority-separation proof.**


## 2026-09-24 P3 — GitHub owner identity boundary

The signed-webhook frontier has a second material blocker beyond the missing production secret. The inbound receiver creates its Supabase client with the service-role key and calls the owner-bound canonical cognition RPC. That RPC requires `auth.uid()` and persists `user_id=auth.uid()`. The service-role JWT shape does not provide a human user `sub`, so the receiver currently has no legitimate owner identity for private cognition persistence.

The existing `nayanet_smart_connect_participation` seam contains `member_id` and `door` plus consent/status fields, but no GitHub installation or repository identity. The receiver therefore cannot safely resolve a signed GitHub delivery to exactly one participating member.

This must not be solved by selecting a default/system owner, bypassing the canonical persistence boundary, or creating a second connection/authority store.

### Required bounded repair

Extend the existing Smart Connect participation seam with the minimum GitHub installation/repository binding required to resolve:

`GitHub installation + repository → active GitHub App participation → canonical member owner`

Then fail closed on missing, ambiguous, or revoked bindings and invoke the existing canonical cognition persistence path under the resolved owner context.

### Truth status

- Owner identity binding: **NOT IMPLEMENTED / NOT VERIFIED**
- Installation/repository isolation: **NOT VERIFIED**
- Replay/idempotency repair: **VERIFIED / PRODUCTION APPLIED**
- Signed production webhook proof: **BLOCKED_EXTERNAL_CREDENTIAL**
- Webhook → execution authority separation: **SOURCE-LEVEL PASS / LIVE NOT VERIFIED**

### Single next action

**Implement the smallest governed GitHub installation + repository → existing Smart Connect participation/member binding on the existing participation seam, with fail-closed missing/ambiguous/revoked resolution.**


## 2026-09-24 P4 — GitHub owner-bound canonical persistence seam

### Source/runtime change

The inbound receiver at NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts now:

1. verifies the existing GitHub HMAC signature before parsing/normalizing;
2. extracts installation.id and repository.full_name;
3. fails closed with BLOCKED_OWNER_BINDING when either binding key is missing/invalid;
4. resolves the human owner through service-only nayanet_resolve_github_webhook_owner(installation_id, repository);
5. fails closed when the binding is missing, ambiguous, inactive/revoked, or unresolved;
6. passes the resolved owner into the existing seven-argument nayanet_record_cognition_event canonical persistence seam;
7. the canonical seven-argument function independently re-resolves the same installation/repository binding and rejects an owner mismatch before persistence;
8. replay protection remains in the canonical seven-argument path, returning the original event/state/receipt with replayed=true instead of creating a second receipt or advancing state.

No second persistence store, connection store, authority model, or webhook backend was introduced.

### Production deployment

The updated Edge Function is ACTIVE, version 4 with deployment digest 36f89f5c9beadcf77298ee0ccf8705a8e836cbdd4813ef1c70282d40bd366072.

The deployed source was independently read back and matches the repository source.

The canonical seven-argument function was independently read back after the production migration and contains both owner-bound service-role handling and exact replay protection.

### Independent live runtime verification

A fresh POST probe reached production version 4 and returned:

HTTP 503 — GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED — BLOCKED_EXTERNAL_CREDENTIAL

This is the expected fail-closed boundary while the real production GitHub secret remains absent. The response proves the deployed runtime is active and still refuses to process an unsigned/unconfigured webhook before owner resolution or persistence.

### Current truth

- Owner binding implementation: PRODUCTION APPLIED / SOURCE + RUNTIME VERIFIED
- Canonical owner-aware persistence seam: PRODUCTION APPLIED / READ-BACK VERIFIED
- Missing/ambiguous/revoked binding fail-closed path: SOURCE + FUNCTION LOGIC VERIFIED; LIVE POSITIVE/NEGATIVE DELIVERY TEST NOT VERIFIED
- Signed webhook positive ingress: BLOCKED_EXTERNAL_CREDENTIAL
- Exact signed replay: NOT VERIFIED until the external secret is configured
- Installation/repository isolation under live GitHub delivery: NOT VERIFIED
- Webhook → execution authority separation: SOURCE-LEVEL PASS; LIVE NOT VERIFIED
- No default/system owner fallback: VERIFIED BY SOURCE
- No second authority/persistence model: VERIFIED BY SOURCE

### Correction to earlier P1/P3 notes

The earlier statements that the receiver had no installation binding and no owner-resolution seam are superseded by this P4 repair. The missing production secret remains an independent external credential boundary. The live signed delivery proof remains open.

### Evidence

- Webhook source commit: da74234e2a44bd0d3a3710ac4f06b84de4569644
- Canonical owner-aware persistence migration commits: e61e1ff2c0d77f5af7386607459cfa91caf75114, f02038a6c32bf02d70785e88a798146872e8ca29
- Production Edge Function: nayanet-github-webhook, version 4
- Production deployment digest: 36f89f5c9beadcf77298ee0ccf8705a8e836cbdd4813ef1c70282d40bd366072
- Independent runtime probe: HTTP 503 GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED
- Production canonical function read-back: owner-aware service-role path + resolver revalidation + replay branch

### Single next action

Configure GITHUB_WEBHOOK_SECRET through the authorized production secret-management boundary, then execute the live signed GitHub proof: bound owner positive → exact persistence → exact replay → fresh retrieval → non-owner/wrong-repository denial → source revocation denial → authority-separation proof.
