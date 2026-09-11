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
- Latest production deployment: `dpl_5G4r74MjsjPCxSAWudgQzoyY89G9`
- Production URL: `https://naya-power.vercel.app`
- Deployment status: READY
- Deployed source commit: `1467ebf3f338640c404efcf2b3be42c77cd50e4e`
- Vercel build logs explicitly show `Branch: main` and the exact commit above.
- Build completed successfully: PIS feed generated with 20 source events; Vite transformed 77 modules; production output deployed.
- Public artifact verification: HTTP 200; canonical marker `NAYANET-HUB-REACT-CANONICAL`; title `NayaNET — Intelligent Hub`.
- Direct `/settings` navigation returns the Hub shell through the new SPA rewrite.
- `/intelligence/pis-feed.json` returns HTTP 200 and `PIS-1.0`.
- Vercel runtime error check for the last 30 minutes: no runtime errors.

### V7 DISPOSITION
`nayanet-intelligent-hub-v7.vercel.app` was independently observed as a minimal `NayaNET` HTML shell, not the current Intelligent Hub runtime. It is obsolete deployment state. The current `naya-power` production project now builds `NAYANET/HUB` from the canonical `main` branch through root `vercel.json`. The old V7 implementation is therefore replaceable history, not the runtime authority.

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

A no-op status update exercised the newly attached trigger and confirmed the persistent index row with identical event identity. This proves the database trigger/index path mechanically; it does **not** substitute for an authenticated browser write.

### CURRENT HUB AUTHENTICATION PATH
- Supabase URL and publishable key are centralized client configuration; no service-role key is used.
- `IdentityProvider` listens to real Supabase Auth state.
- PIS calls `supabase.auth.getUser()` before persistent retrieval.
- Persistent PIS queries `nayanet_intelligence_index` for the authenticated owner only.
- Preview/GitHub projection is explicitly distinguished from live persistent transport.
- Settings contains real `signInWithPassword` / `signOut` UI.
- Access/refresh tokens are not placed in the application Identity object.
- RLS remains the database authority.

### WHAT IS VERIFIED
- canonical Hub source on `main`
- current Hub deployed to production from `main`
- exact deployed artifact is the current React Hub, not V7 shell
- production PIS artifact is served
- direct client route navigation works
- production build completes successfully
- no recent Vercel runtime errors
- real Supabase Auth code path is present
- known Smart Note exists
- Smart Note → persistent index trigger path repaired and exercised
- exact event identity preserved across source and index
- persistent PIS adapter is wired to authenticated Supabase
- RLS policies exist on Smart Note events and persistent index

### NOT YET VERIFIED
- a real browser session authenticated through the public Hub
- authenticated creation of a new Smart Note through the canonical Smart Note API
- RLS-authorized browser observation of that new event
- live PIS retrieval of that authenticated event
- live Hub rendering of that same authenticated event identity

### CURRENT BLOCKER
The remaining gate is genuine identity. Naya's tool environment cannot borrow Shawn's browser session or credentials. The Hub now has the real authentication entry point, but a human must authenticate through the deployed Hub before the final authenticated runtime receipt can legitimately be recorded. No credentials are requested from chat and no RLS bypass will be used.

### END-TO-END TARGET
`REAL AUTHENTICATED HUB SESSION → SUPABASE AUTH USER → RLS-AUTHORIZED SMART NOTE → smart_note_events → nayanet_intelligence_index → PIS → HUB DISPLAY`

### NEXT HIGHEST-VALUE ACTION
Open `https://naya-power.vercel.app`, use the real Hub authentication entry point, and sign in with the existing NayaNET/Supabase member account. Then execute the first authenticated runtime receipt and capture the exact event ID at every hop. If any hop diverges, repair it and repeat before declaring completion.

### LEARNING
Functionality outranks appearance. The current deployment was rebuilt around the actual Hub engine, obsolete V7 state was replaced as runtime plumbing, and a real database defect was repaired before further visual iteration. The final proof gate is intentionally external because authenticated identity must be genuine.

**16-PROTOCOL CHECK:** PASS
