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
| **MCP** | MCP transport/session authentication | Agent/client identity participates through the same governed runtime | Server-side authority grant; tools/call must not infer permission from connection | Tool + project + target scope; explicit consent where required | Canonical event/receipt + fresh retrieval | Session/token/grant revocation must block calls | Request/idempotency key must prevent duplicate durable effects | **PARTIAL** — architecture and release machinery exist; authenticated current-source production proof remains open |
| **REST/OpenAPI** | Authenticated API identity | API client participates through canonical API boundary | Same authority lifecycle as MCP; transport must not create a second authority model | Endpoint/action/target/project scope | Same canonical persistence and receipt chain as MCP | Credential/grant revocation must fail closed | Idempotency and replay behavior must match MCP semantics | **PARTIAL** — architecture exists; current deployed authenticated parity proof remains open |
| **Webhooks** | Signed/verified sender identity | External system becomes an event source, not an authority source | Inbound event authenticity does not authorize downstream execution | Event/source scope; consent and authority evaluated before side effects | Canonical inbound event + receipt/provenance | Signing secret/source registration revocation must reject future events | Delivery replay must converge on one canonical event/effect | **DOCUMENTED / UNPROVEN** — transport contract exists; full governed production door proof remains open |
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

`NAYANET/UNIVERSAL-AGENT-INTERFACE` is source-defined as the canonical REST/OpenAPI + MCP adapter over `nayanet-compound-intelligence`. The source contract requires Bearer authentication and MCP `initialize → tools/list → tools/call`; consequential retrieve/understand actions force `cold_restore` first. **Current truth: source-implemented; authenticated live transport-to-receipt proof remains OPEN.**

### Current next frontier

Execute the first authenticated live Universal Agent Interface proof across **MCP + REST/OpenAPI parity** using the existing bearer identity and canonical runtime. Required chain: authentication → initialize/tools → cold restore → action → authority decision → canonical persistence/retrieval → receipt/evidence → revoke/denied reuse → exact replay. No new authority model or backend.
