# 🔱 Smart Connect — Seven-Door Authority Matrix
**Date:** 2026-09-24
**Repository:** SoulSchoolAcademy/NayaPOWER
**Canonical room contract:** `NAYANET/HUB-ROOM-SYSTEM/04-SMART-CONNECT.md`
**Evidence anchor:** Universal Envelope production bridge run `36054810899` + focused relationship proof `NAYANET_SMART_CONNECT_RELATIONSHIP_SECURITY_PROOF_V1`

## Governing rule

Smart Connect is participation, not authority.

**Connection ≠ Permission. Authentication ≠ Authorization. Participation ≠ Execution authority.**

Every door must converge on the existing governed core:

**DOOR → AUTHENTICATION → IDENTITY → PARTICIPATION → AUTHORITY → SCOPE → CONSENT → PERSISTENCE → REVOCATION → ACTIVITY/EVIDENCE → REPLAY/IDEMPOTENCY → FRESH RETRIEVAL**

No door may create a second connection store, authentication model, authority model, or intelligence source of truth.

## Common participation boundary — independently verified

The canonical relationship substrate is `public.nayanet_connections`, reached through the existing authenticated runtime/RPC boundary.

Fresh adversarial proof verified:

- owner creates A → B Connection;
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
| **GitHub App** | GitHub installation / app identity; exact mechanism must remain external to source | Repository/user installation participation; installation identity must remain distinct from human identity | Separate Naya authority grant + least-privilege GitHub installation/repository scope | Repository, installation, action scope; human consent must be explicit | GitHub observation + canonical Naya event/receipt; no GitHub source-of-truth substitution | App installation/token/repository permission revocation must block subsequent actions | Webhook/action replay must be idempotent by canonical event/idempotency identity | **PARTIAL** — repository authority exists; independent end-to-end production agent proof remains open |
| **MCP** | MCP transport/session authentication | Agent/client identity participates through the same governed runtime | Server-side authority grant; tools/call must not infer permission from connection | Tool + project + target scope; explicit consent where required | Canonical event/receipt + fresh retrieval | Session/token/grant revocation must block calls | Request/idempotency key must prevent duplicate durable effects | **LIVE VERIFIED** — UAI run `36061300293` authenticated initialize → tools/list → cold restore → understand → retrieve → restore with canonical receipt/evidence; governed execution boundary additionally verified in Attack 4 run `36062784233` |
| **REST/OpenAPI** | Authenticated API identity | API client participates through canonical API boundary | Same authority lifecycle as MCP; transport must not create a second authority model | Endpoint/action/target/project scope | Same canonical persistence and receipt chain as MCP | Credential/grant revocation must fail closed | Idempotency and replay behavior must match MCP semantics | **LIVE VERIFIED** — UAI run `36061300293` authenticated cold restore → understand → retrieve; run `36064087479` additionally proved governed intelligence_commit authority parity through the same canonical UAI adapter/runtime |
| **Webhooks** | Signed/verified sender identity | External system becomes an event source, not an authority source; current receiver does not persist an explicit GitHub installation ID | Inbound event authenticity does not authorize downstream execution; receiver uses github_webhook_received, not intelligence.capture | Event/source scope; repository binding currently comes from repository.full_name and is not yet independently adversarially proven | Canonical nayanet_record_cognition_event → cognition event/project state/execution receipt; downstream projection is not invoked by the receiver | Secret/source registration revocation remains external and unverified | Cognition event has unique (user_id,project_id,event_id), but webhook's current six-argument RPC path still creates a fresh receipt/state update on replay; exact idempotency is NOT VERIFIED | **BLOCKED_EXTERNAL_CREDENTIAL** — deployed fail-closed receiver; positive signed delivery and exact replay remain unverified |
| **SDK** | Application/client authentication | Embedded client participates through canonical SDK adapter | SDK delegates authority to governed runtime; local SDK capability must not become authority | App/project/user scope plus explicit action consent | Same canonical event/persistence/evidence path | App credential/grant revocation must block governed actions | SDK retries must be idempotent at canonical boundary | **DOCUMENTED / UNPROVEN** — adapter concept exists; independent production door proof remains open |
| **A2A** | Agent identity/authentication | Agent participates as an external actor through governed adapter | Authority must be independently evaluated; agent relationship never implies execution permission | Agent/task/project/target scope | Canonical agent event + execution receipt + fresh retrieval | Agent credential/grant/task revocation must block subsequent actions | Message/task replay must preserve idempotent canonical outcome | **DOCUMENTED** — future channel; no broad-use production proof established |
| **MCP Apps** | MCP app/session authentication | App participates through MCP capability boundary | Same server-side governed authority as MCP; app UI cannot grant itself permission | Tool/app/session/project scope + consent | Canonical MCP event/receipt path | Session/app/grant revocation must fail closed | UI retries and tool-call replay must converge on canonical idempotent effect | **DOCUMENTED / UNPROVEN** — defined door; independent production proof remains open |

## Required proof sequence

The seven doors are **not** seven separate brains or seven separate authorization systems.

### Phase A — common relationship seam
**VERIFIED**

Owner/non-owner/revocation/replay proof is complete for the canonical relationship substrate.

### Phase B — door convergence
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

### Phase C — parity
For MCP and REST/OpenAPI specifically, prove semantic parity:

**same identity → same authority rules → same canonical object → same persistence → same receipt semantics → same fresh retrieval truth.**

## Evidence boundary

The production Universal Envelope bridge proof is independently **VERIFIED** at run `36054810899` on main commit `943192584c8829225d7ff4841e2140d5be004d9c`.

The first Universal Agent Interface production transport proof is independently **VERIFIED** at run `36061300293` on main commit `e316ac9311230bf2f4f182971c440c3ef0c81559`; UAI version `3318bb4b-a31c-4efb-a872-888b10b87810` passed authenticated MCP + REST persistence/retrieval parity.

The governed execution/authority proof is independently **VERIFIED** at run `36062784233` on main commit `dcdc299349a9e14c2a39fc4f627e08e140863c6b`: MCP participation connected without changing authority; one live `intelligence_commit` was authorized and independently reconstructed with actor, authority, decision, execution, scope, governance and binding hash; exact replay returned the same event/checkpoint identity; MCP participation revocation left authority unchanged; authority-grant revocation then denied a fresh commit with `AUTHORITY_REQUIRED:GRANT_REVOKED`.

It proves:

**fresh owner → existing envelope adapter → production bridge → persisted receiver transaction/event/receipt/index → independent retrieval → independent reconstruction → exact replay**

It does **not** by itself prove any of the seven Smart Connect doors.

The focused relationship proof proves the shared participation substrate and adversarial relationship lifecycle. It does **not** promote any external door to production-ready.

## Single next frontier

**Execute the first door-specific adversarial proof against the existing authority seam, beginning with the Universal Agent Interface pair: MCP + REST/OpenAPI.**

Required chain:

**authenticated initialize → tools/call → authority decision → canonical persistence → fresh retrieval → verified outcome → revoke → denied reuse → exact replay semantics → REST parity**

No new authority model. No second backend. No direct Hub-to-Supabase bypass.


## 2026-09-24 live evidence — continuation after production bridge verification

### Production bridge boundary

Run `36054810899` is **VERIFIED** on `main` commit `943192584c8829225d7ff4841e2140d5be004d9c`. The proof job independently verified fresh owner bootstrap, existing envelope adapter validation, production receiver transaction/event/receipt/index persistence, independent retrieval, lineage reconstruction, and exact replay with the same receiver transaction/event/receipt lineage.

### Common relationship seam — live adversarial proof

The canonical `nayanet_connections` boundary was exercised with two authenticated identities in a rollback-scoped production database transaction:

- Owner A → B connection: `CONNECTED`.
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

`NAYANET/UNIVERSAL-AGENT-INTERFACE` is now **LIVE VERIFIED** at the authenticated transport/persistence/retrieval boundary by run `36061300293`. The existing release harness proved fail-closed unauthenticated REST/MCP, authenticated MCP initialization/tools, mandatory 14-question cold restore, MCP understand → receipt → retrieve, REST understand → receipt → retrieve, and same-canonical-path parity.

### Current next frontier

**Attack external-door authority parity, not the already-proven core.** The governed core now proves owner-bound authority, non-owner/wrong-scope denial, participation/replay/revocation semantics, and receipt reconstruction. MCP + REST transport/persistence/retrieval are live verified, but the UAI public surface currently exposes safe intelligence actions rather than `intelligence_commit`. The next bounded frontier is to prove the same authority grant/deny/revoke/replay semantics through an existing external door without creating a second authority model or backend.


## 2026-09-24 execution frontier — top 10 highest-value remaining items

1. **Unblock GitHub App/Webhook credential boundary.** Configure production `GITHUB_WEBHOOK_SECRET` through the external secret-management/admin surface; never place the secret in source or chat.
2. **Live-prove GitHub webhook ingress.** Positive HMAC verification → canonical event persistence → exact delivery replay → one logical event → independent retrieval.
3. **Prove webhook-to-authority separation.** A valid GitHub event must remain an event source, never implicit `intelligence_commit` authority; privileged execution must require an existing grant.
4. **Prove webhook disable/revocation.** Disable/revoke the source registration and demonstrate subsequent signed deliveries are rejected or quarantined.
5. **Prove GitHub App repository-scope isolation.** Authorized repository accepted; unauthorized repository rejected before private projection.
6. **Prove GitHub App/Hub two-way mutation boundary.** Hub action → existing authority → canonical event → authorized GitHub mutation → GitHub observation → verification → Hub projection.
7. **Audit SDK door.** Resolve whether an actual SDK adapter exists in production source; if absent, keep it DOCUMENTED/UNPROVEN rather than inventing an adapter.
8. **Audit A2A door.** Resolve whether an actual A2A adapter exists; if absent, keep it DOCUMENTED/FUTURE and define the smallest production seam.
9. **Audit MCP Apps door.** Determine whether the existing MCP surface is app-capable and prove that UI/session capability cannot grant authority.
10. **Run final seven-door cross-door invariance.** Same actor/authority/scope/revocation/idempotency semantics across every actually implemented door, with explicit NOT VERIFIED for doors lacking production infrastructure.

### Current live boundary

- Universal Envelope production bridge: **VERIFIED** — run `36054810899`.
- UAI MCP + REST transport/persistence/retrieval: **LIVE VERIFIED** — run `36061300293`.
- UAI privileged authority parity: **LIVE VERIFIED** — run `36064087479`.
- GitHub webhook function: **ACTIVE / BLOCKED_EXTERNAL_CREDENTIAL** — positive production proof cannot run because `GITHUB_WEBHOOK_SECRET` is not configured.
- No evidence was found in the repository tree for a separate SDK, A2A, or MCP Apps implementation beyond the documented contracts; these remain **NOT VERIFIED**.

### Job holes identified

- The first UAI proof targeted the PI continuation helper for an `intelligence_commit` grant; fail-first evidence showed it intentionally issues `pi.continue`, not `intelligence_commit`. Repaired by using the canonical `nayanet_issue_authority_grant` RPC.
- The first replay assertion used the wrong UAI JSON path and could compare null to null. Repaired by requiring exact source-event/checkpoint identity plus `replayed=true`.
- The privileged UAI commit path was initially absent from the external door. The bounded implementation now delegates directly to the existing governed runtime; no second authority or backend was introduced.
- GitHub webhook infrastructure is deployed but not operationally provable because its required external credential is absent.
- The remaining doors must not be promoted from documented contracts to production truth without actual adapter execution evidence.

### Evidence for this continuation

- `36054810899` — production Universal Envelope bridge.
- `36061300293` — UAI MCP/REST production transport/persistence/retrieval.
- `36064087479` — UAI privileged authority owner/replay/retrieval/non-owner/revocation proof.
- Direct production probe of `nayanet-github-webhook` — `503 GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED / BLOCKED_EXTERNAL_CREDENTIAL`.

### Single next action

**Configure `GITHUB_WEBHOOK_SECRET` in the production secret-management/admin boundary, then run the signed GitHub webhook positive → replay → persistence → retrieval → authority-separation proof.**


## 2026-09-24 P1 — GitHub Webhook credential boundary and safe preflight

**Status: BLOCKED_EXTERNAL_CREDENTIAL**

### Production credential boundary

The production Edge Function nayanet-github-webhook is ACTIVE, version 3, and its deployed digest is 081cc239fb9f6c662044ea13d3a56d4015baf0741d720b29bfbfa01bafa6349c. The repository source is NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts (blob cf00cb52b424783f37d25a2a89f031724b19543a).

A fresh production probe at 2026-09-24T22:11:01Z returned HTTP 503 with GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED and BLOCKED_EXTERNAL_CREDENTIAL, before delivery/signature processing or persistence. The secret value was not requested or handled. The current permitted Supabase tool surface exposes deployment/source metadata but no secret-management read/write operation.

### Safe call-graph findings

GitHub POST → webhook Edge Function → method check → delivery/signature headers → GITHUB_WEBHOOK_SECRET check → HMAC-SHA256(raw body) → JSON parse → normalization → service-role canonical cognition RPC → cognition event + project state + execution receipt → response.

No second inbound webhook implementation was found in repository source. The separate nayanet-github-dispatch function is outbound GitHub workflow dispatch, not an inbound webhook caller.

The receiver normalizes repository, actor, ref, commit SHA, delivery ID, source system, correlation ID, and idempotency key. It does not currently persist an explicit GitHub installation ID. The authority object in the normalized event is source/scope metadata, not execution authority.

### Critical preflight replay finding

The receiver uses the six-argument nayanet_record_cognition_event overload with action github_webhook_received. Production currently retains both six- and seven-argument overloads. The six-argument path de-duplicates the cognition row by (user_id, project_id, event_id) but still creates a new execution receipt and increments project cognition state on each replay. Therefore the required exact replay/idempotency property is NOT VERIFIED and has a concrete causal repair target. No repair is made in P1.

### Authority separation

Source inspection shows the webhook does not call the intelligence.capture authority-required action and supplies no execution authorization object. This is source-level evidence for WEBHOOK EVENT ≠ EXECUTION AUTHORITY. Live authority-separation proof remains unverified until a signed production event can be accepted.

### Adversarial preparation

Prepared, but not run in production: missing signature, wrong signature, altered payload, wrong repository, wrong installation/source, revoked/disabled source, duplicate delivery, and authority-separation checks. No production mutation was executed for this preparation.

### Durable evidence

- P1 artifact: .naya/project-intelligence/GITHUB-WEBHOOK-P1-CREDENTIAL-BOUNDARY-2026-09-24.md
- Main after evidence artifact: 1f4825405527f3e1a67b0a82aa7ec7ea14d0cde8
- UAI privileged authority proof: 36064087479
- UAI deployment: 36063359510

### Single next action

**Run the controlled signed production GitHub webhook proof after the authorized operator has configured the real production secret.**
