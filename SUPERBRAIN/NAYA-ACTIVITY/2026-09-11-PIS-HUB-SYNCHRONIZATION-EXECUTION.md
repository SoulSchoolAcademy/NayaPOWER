# Naya 16 Activity Record

## 2026-09-11 — PIS → Intelligent Hub synchronization execution

**STATUS:** CURRENT HUB DEPLOYED / DATABASE INDEX PATH REPAIRED / AUTHENTICATED END-TO-END RECEIPT BLOCKED ONLY BY REAL USER SESSION
**ACTION ID:** `PIS-HUB-SYNC-20260911`
**PROJECT:** NayaPOWER / Primary Intelligence System / Intelligent Hub
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**CANONICAL BRANCH:** `main`

### VERIFIED DEPLOYMENT
- Vercel project: `naya-power`
- Project ID: `prj_cHa9gwrtscCW8JuMDjcvw6DafaOK`
- Production deployment: `dpl_twhFhc3NNWP2iRpsnNjuu16jnRMX`
- Production URL: `https://naya-power.vercel.app`
- Production deployment status: READY
- Deployed source commit: `3cc9910b1dcaf6d0b6a8174e04ce8cbf0946b5d1`
- Vercel build logs show the current `main` commit and build of `NAYANET/HUB` via root `vercel.json`.
- Public artifact verification: HTTP 200; canonical marker `NAYANET-HUB-REACT-CANONICAL`; title `NayaNET — Intelligent Hub`; PIS artifact endpoint `/intelligence/pis-feed.json` returns `PIS-1.0`.

### V7 DISPOSITION
`nayanet-intelligent-hub-v7.vercel.app` was independently observed as a minimal `NayaNET` HTML shell, not the current Intelligent Hub runtime. It is obsolete deployment state. The linked `naya-power` project was previously production-linked to `v7-intelligent-hub-live`; that branch was deliberately fast-forwarded/force-aligned to the current `main` commit because functioning current architecture supersedes the obsolete V7 implementation. The root `vercel.json` now builds `NAYANET/HUB` directly, so the production project serves the current Hub rather than the old root shell.

### DATABASE REPAIR — SMART NOTE → INDEX
The database contained the canonical `nayanet_index_intelligence_row()` trigger function, but `smart_note_events` did not have the required trigger attached. This was a real runtime integrity defect.

Repaired in Supabase:
- trigger: `trg_smart_note_events_to_intelligence_index`
- table: `public.smart_note_events`
- timing: `AFTER INSERT OR UPDATE`
- function: `public.nayanet_index_intelligence_row()`

Known Smart Note used for deterministic index verification:
- event ID: `c1f15866-6493-41a3-8847-1a181f001c39`
- subject: `What Smart Notes Are and How They Work`
- event type: `SMART_NOTE`
- source status: `VERIFIED`
- persistent index ID: `526a9053-4dd1-49ad-b17e-1348abac103e`
- index source table: `smart_note_events`
- index source ID: same Smart Note event ID
- index title: same Smart Note subject

A no-op status update on the known event was used to exercise the newly attached trigger and confirm the persistent index row was created with the same source identity. This proves the database trigger/index path mechanically; it does **not** substitute for an authenticated browser write.

### CURRENT HUB AUTHENTICATION PATH
The current Hub now uses a centralized public Supabase configuration and a real Auth boundary:
- Supabase URL is client configuration.
- Supabase publishable key is client-safe; no service-role key is used.
- `IdentityProvider` listens to real Supabase Auth state.
- PIS uses `supabase.auth.getUser()` before persistent index retrieval.
- Persistent PIS queries `nayanet_intelligence_index` for the authenticated owner only.
- Preview/GitHub projection is not labeled as live persistence.
- Authentication UI exists at the Hub Settings route and uses real `signInWithPassword` / `signOut`.
- Access/refresh tokens are not placed in the application Identity object.

### WHAT IS VERIFIED
- current Hub source is on `main`
- current Hub production deployment is READY
- exact production HTML is the current React Hub, not the old V7 shell
- PIS build artifact is publicly served
- Vercel production build logs show current `main` source and `NAYANET/HUB` build
- real Supabase Auth code path exists in the deployed source
- known Smart Note exists in `smart_note_events`
- `smart_note_events → nayanet_intelligence_index` trigger path was repaired and exercised
- persistent index preserves exact Smart Note event identity
- PIS adapter source retrieves the persistent index through authenticated Supabase
- RLS policies exist on both Smart Note events and persistent index

### NOT YET VERIFIED
- a real browser session authenticated through the public Hub
- authenticated creation of a new Smart Note through the canonical Smart Note API
- RLS-authorized observation of that new event in the index from the browser session
- the same event being retrieved by the live PIS adapter for that session
- the same event identity being rendered by the live Hub during that authenticated session

### CURRENT BLOCKER
The remaining gate is not an architecture defect and must not be faked: Naya's tool environment cannot borrow Shawn's browser session or credentials. The Hub now has the real authentication entry point, but a human must authenticate through the deployed Hub before an authenticated runtime receipt can legitimately be recorded. No credentials are requested from chat and no RLS bypass will be used.

### END-TO-END TARGET
`REAL AUTHENTICATED HUB SESSION → SUPABASE AUTH USER → RLS-AUTHORIZED SMART NOTE → smart_note_events → nayanet_intelligence_index → PIS → HUB DISPLAY`

### NEXT HIGHEST-VALUE ACTION
Open `https://naya-power.vercel.app`, use the real Hub authentication entry point, and sign in with the existing NayaNET/Supabase member account. Then execute the first authenticated runtime receipt against the known/new Smart Note and capture the exact event ID at every hop. If any hop diverges, repair it and repeat before declaring completion.

### LEARNING
Functionality outranks appearance. The current deployment was therefore rebuilt around the actual Hub engine, the obsolete V7 shell was demoted to replaceable history, and a real database defect was repaired before further visual iteration. The remaining proof gate is intentionally external because authenticated identity must be genuine.

**16-PROTOCOL CHECK:** PASS
