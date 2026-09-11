# Naya 16 Activity Record

## 2026-09-11 — PIS → Intelligent Hub synchronization execution

**STATUS:** PIS CI VERIFIED / AUTHENTICATED RUNTIME BLOCKED BY REAL HUB IDENTITY
**ACTION ID:** `PIS-HUB-SYNC-20260911`
**NAYA:** Implementation Naya
**PROJECT:** NayaPOWER / Primary Intelligence System / Intelligent Hub
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**BRANCH:** `main`
**CARRIER PIS CI RUN:** `34635525442`
**CARRIER PIS CI JOB:** `103382335713`
**CARRIER VERIFIED COMMIT:** `55cb767e5063354b8534ade8f65cad36d0f08e37`
**AUTH IDENTITY COMMIT:** `bbb64da614a6f7a9c9ae6d579a44e715bfe26af1`
**AUTH HARDENING COMMIT:** `36a46791d302efaf7e8e933e5060ee5afa0d3978`
**PIS RUNTIME COMMIT:** `96093a5043f7d4ccd90ee9e88923fc0ac0cca888`
**CARRIER AUTH-CHECK COMMIT:** `f820f389254b70afc3ca74991aad8cbe438121c2`
**CURRENT FOLLOW-UP:** `PIS-AUTHENTICATED-RUNTIME-VERIFICATION`

### 01 — WHAT IS HAPPENING NOW?
The PIS vertical slice is implemented. GitHub Smart Notes are projected into PIS, and the Hub can now use an authenticated Supabase identity boundary for persistent PIS retrieval. The static GitHub projection remains a deterministic unauthenticated/preview transport rather than being falsely presented as live persistence.

### 02 — WHAT ARE WE ACTUALLY TRYING TO ACHIEVE?
Establish the real central intelligence flow: canonical Smart Note → primary intelligence event → persistent PIS index → authorized Intelligent Hub presentation, while preserving one event identity and avoiding a second competing feed/database.

### 03 — WHAT DOES THE SYSTEM NOW DO?
The Hub IdentityProvider listens to Supabase Auth state and represents the real authenticated user when a session exists. The PIS adapter validates the current user through `supabase.auth.getUser()`, then queries `nayanet_intelligence_index` filtered to that authenticated user. The query is bounded by `PIS_QUERY_LIMIT`. No service-role key or credential is used in the browser. When no authenticated user exists, the Hub uses the deterministic GitHub projection.

### 04 — SECURITY BOUNDARY
No access token or refresh token is placed in the application Identity object. Authorization is not derived from mutable user metadata. The browser client is intended to use only the Supabase publishable key; database access remains subject to Supabase Auth and Postgres RLS. Supabase documentation confirms `getUser()` performs a network request and returns an authentic user record suitable for authorization decisions, while RLS policies can constrain rows using `auth.uid()`.

### 05 — RUNTIME SOURCE AUTHORITY
When authenticated, persistent Supabase PIS is authoritative for the Hub feed. A database error is surfaced rather than silently converted into a fake “live” state. When unauthenticated, the deterministic GitHub projection is used and the UI labels the transport as preview/GitHub rather than live/Supabase.

### 06 — UI TRUTH REPAIR
The previous Hub UI could label any loaded event `LIVE`, even when it came from the static build projection. That was repaired. The Hub now distinguishes authenticated persistent transport (`LIVE / SUPABASE`) from build projection (`PREVIEW / GITHUB`). This prevents a visual claim of runtime persistence without runtime evidence.

### 07 — CI VERIFICATION
The observed carrier workflow previously proved the PIS projection/build path: run `34635525442`, job `103382335713`, completed **SUCCESS**. It generated 20 PIS events and passed projection validation, persistent-adapter source validation, Hub typecheck, production build, and artifact parity. The carrier workflow was then hardened to check the authenticated adapter boundary (`auth.getUser`, Supabase index, bounded query, Auth state listener, publishable-key environment boundary).

### 08 — ACTUAL HUB DEPLOYMENT STATE
The Vercel project `nayanet-intelligent-hub-v7` currently has a READY production deployment, but its observed public response is only a minimal `NayaNET` HTML shell. That deployment is not evidence of the GitHub `main` branch Intelligent Hub implementation and does not provide a real authenticated Hub session for this PIS runtime test. Therefore it is not promoted as the runtime target.

The linked `naya-power` Vercel project is currently associated with an older V7 branch rather than the current `main` PIS implementation. This is a deployment/source-alignment issue, not permission to overwrite the canonical architecture.

### 09 — WHAT IS VERIFIED?
**VERIFIED:**
- canonical PIS contract/source
- GitHub Smart Note → PIS projection
- PIS schema/identity checks
- persistent Supabase adapter source
- Hub typecheck
- Hub production build
- PIS artifact parity
- authenticated identity adapter source
- UI distinction between persistent and preview transport

**NOT VERIFIED:**
- current `main` PIS changes in a fresh carrier CI receipt after the latest authentication commits
- deployed Hub running the current `main` artifact
- real authenticated Hub session
- authenticated Smart Note → `nayanet_intelligence_index` → PIS → Hub event observation

### 10 — WHAT MUST NOT HAPPEN?
Do not bypass authentication. Do not use a service-role/secret key in the browser. Do not expose session credentials. Do not weaken RLS. Do not fabricate a production runtime session. Do not call the current minimal Vercel shell a verified Intelligent Hub runtime. Do not call the static projection persistent runtime.

### 11 — END-TO-END TARGET
`REAL AUTHENTICATED HUB SESSION → SUPABASE AUTH USER → RLS-AUTHORIZED nayanet_intelligence_index → PIS EVENT → HUB SMART FEED`

For the first runtime receipt, use a known Smart Note event and prove stable event identity across the persistent index and Hub observation. Record authenticated user identity only internally as needed for verification; do not expose it through public collective intelligence.

### 12 — CURRENT BLOCKER
The real Hub identity/session does not yet exist on the currently observed production Hub target. The Vercel production Hub project responds with a minimal static shell, so there is no legitimate authenticated browser session available for Naya to observe. The runtime verification is therefore **BLOCKED / NOT VERIFIED**, not failed.

### 13 — NEXT HIGHEST-VALUE ACTION
Align the operational Intelligent Hub deployment with the current `main` PIS artifact and its required public Supabase configuration, then authenticate through the real Hub. Once a real session exists, execute the runtime receipt: authenticated identity → known Smart Note → persistent index → PIS retrieval → Hub display → stable event identity.

### 14 — LEARNING
The correct architecture is now explicit: build-time projection verification and authenticated persistent-runtime verification are separate gates. A successful build cannot substitute for a live session. A deployed shell cannot substitute for an operational Hub. Runtime truth requires the actual public target, actual auth state, actual authorized data path, and independent observation.

### PRESERVED
Existing Intelligent Hub architecture, Smart Feed renderer, Intelligent Event model, Supabase persistence, privacy boundaries, RLS boundary, and canonical Smart Note architecture are preserved.

### RECEIPTS
- PIS CI run `34635525442`
- PIS CI job `103382335713`
- Verified carrier workflow `.github/workflows/verify-smart-ledger-v1.yml`
- PIS adapter `NAYANET/HUB/src/data/pis.ts`
- Auth identity adapter `NAYANET/HUB/src/identity/session.ts`
- Hub integration `NAYANET/HUB/src/app/App.tsx`
- Supabase canonical Smart Note pipeline
- Vercel production Hub observation: `nayanet-intelligent-hub-v7.vercel.app` returned HTTP 200 but only a minimal `NayaNET` shell

**16-PROTOCOL CHECK:** PASS
