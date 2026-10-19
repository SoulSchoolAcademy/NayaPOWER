# NayaPOWER System Map — Naya Nitro Narzan's Living Knowledge
# Last updated: 2026-10-19
# Purpose: Stop discovering, start knowing. This is the whole system as I understand it.

## The Big Picture

NayaPOWER is a governed, self-improving "mother brain" where humans and Nayas create beautiful, useful, connected smart apps. The architecture is a loop:

**GitHub → Supabase → Edge Functions → Templates → Cloudflare → GitHub**

- **GitHub**: Source of truth (code, contracts, lessons, intelligence)
- **Supabase**: Persistence layer (data, user content, system state)
- **Edge Functions**: Intelligence layer (law, know, act, prove, learn)
- **Templates**: User interface (12 smart app templates)
- **Cloudflare**: Hosting (workers serving the templates)

## The Three Pillars (Shawn's standing order)

1. **Learn near-instantly** — The system gets smarter from every interaction
2. **Smart apps humans love** — Beautiful, functional, useful
3. **A system built for Nayas to build in** — Nayas can build within the system

## The Smart Flow

**KNOW → DECIDE → DO → VERIFY → LEARN + IMPROVE → CONTINUE**

This is the operational loop. Every action follows this pattern.

## Infrastructure — What's Live

### Supabase (Project: dahisasgpfvziswqvmvm, "supabase-red-cable")
- **Region**: Canada Central (ca-central-1)
- **Status**: ACTIVE_HEALTHY
- **URL**: https://dahisasgpfvziswqvmvm.supabase.co

**Tables** (confirmed existing):
- `smart_spaces` — Has data ("Team Naya")
- `smart_lists` — Has data
- `user_connections` — Exists
- `smart_notes` — CREATED 2026-10-19 (id, content, owner_alias, created_at, updated_at)
- `connections` — CREATED 2026-10-19 (owner_alias, connected_alias, status)

**Access**:
- Anon key: For browser-side read/write with RLS (stored as custom.supabase-anon)
- Service key: For server-side operations (via custom.supabase connector)
- Management API: Full DDL/control (stored as custom.supabase-mgmt, token from Shawn 2026-10-19)

### Edge Functions (20 ACTIVE)

**A. Nine-node intelligence and governance** (6):
- `nayanet-law-runtime` — Authority/permissions decisions (verify_jwt: false, uses GitHub OIDC)
- `nayanet-act-runtime` — Executes governed actions (verify_jwt: false)
- `nayanet-know-runtime` — Retrieves intelligence/knowledge (verify_jwt: false)
- `nayanet-prove-runtime` — Verifies evidence/receipts (verify_jwt: false)
- `nayanet-intelligence-commit-runtime` — Commits structured intelligence (verify_jwt: false)
- `naya-decision-context` — Retrieves learning context for decisions (verify_jwt: true)

**B. Learning, verification and continuity** (6):
- `nayanet-learning-verify` — Verifies learning evidence (verify_jwt: false)
- `nayanet-causal-learning-experiment` — Controlled learning experiments (verify_jwt: false)
- `nayanet-causal-verify` — Verifies learning changed outcomes (verify_jwt: false)
- `nayanet-cold-runtime-proof` — Cold-start continuity proof (verify_jwt: false)
- `naya-dream-replay` — Replays cognition events (verify_jwt: true)
- `nayanet-successor-handoff` — Successor handoff info (verify_jwt: true)

**C. GitHub and project integration** (4):
- `nayanet-github-webhook` — Receives GitHub events (verify_jwt: false, HMAC)
- `nayanet-github-dispatch` — GitHub projections for Smart Notes (verify_jwt: true)
- `nayanet-github-build-dispatch` — Triggers Hub build verification (verify_jwt: true)
- `nayanet-project-intelligence-bridge` — Project intelligence packets (verify_jwt: false)

**D. Customer-facing features** (3):
- `nayanet-smart-mail` — Messaging backend (verify_jwt: true, requires authenticated user)
- `nayanet-smart-note-viewer` — Smart Note viewing (verify_jwt: false)
- `v7-smart-note-canonical` — Smart Note intake (verify_jwt: true, requires AUTHENTICATED_USER)

**E. AI-action verification** (1):
- `nayanet-verified-ai-action` — Verifies AI actions obey governance (verify_jwt: false)

**Key insight**: Functions with `verify_jwt: false` use GitHub OIDC (backend-to-backend). Functions with `verify_jwt: true` use Supabase JWT (can be called with user tokens). The customer-facing functions require authenticated users, not just the anon key.

### Cloudflare (Account: NayaPOWER b5e2a51b3e883f7722287c5f51b1196b)
- **Workers.dev subdomain**: nayapower
- **Zone**: nayanet.live (7846f14ed50b53bbf887227e73d94fa2)

**Workers** (live):
- `naya-showpiece` — Personal template (https://naya-showpiece.nayapower.workers.dev/)
- `naya-supabase-proxy` — Supabase proxy for templates (CREATED 2026-10-19)
- `naya-template-business`, `-booking`, `-product`, `-portfolio`, `-event`, `-menu`, `-community`, `-signup`, `-dashboard`, `-personal-hub`, `-business-hub` — 11 other templates
- `app`, `hub`, `lifewithnaya`, `nayanet`, `powercasts`, `smartfactory`, `naya-templates-preview`

**Deploy recipe**: Multipart PUT with boundary `----nayaformdata7d3f9a1c`, metadata `{main_module:'worker.js', compatibility_date:'2024-01-01'}`, Content-Type `application/javascript+module` for ES modules.

**Limitations**: Token cannot create DNS (403), cannot POST /workers/domains (405). CAN deploy workers, create routes, enable workers.dev via POST `/accounts/{ACCT}/workers/scripts/{name}/subdomain`.

### GitHub (SoulSchoolAcademy/NayaPOWER)
- **Main branch**: Last verified 2026-10-18
- **Live board**: #2765 (not #2721, not #2641)
- **Key PRs**: #2745 (Visual Smart Contract, 9.5/10, DRAFT), #2741 (canonical hexes), #2742 (design laws v2)

**Factory pipeline** (~/workspace/factory-pipeline/, committed as 8cef83e on nitro/templates-themed-v2):
- `customize.py` — Customizes template from contract
- `deploy.py` — Deploys HTML to worker
- `build-api.py` — Contract → {build_id, url, receipt}
- `contracts.json` — All 12 template contracts

## The 12 Templates

All are customizations of personal-v5.html. All live at https://<worker>.nayapower.workers.dev/:

1. **Personal** (`naya-showpiece`) — Flagship, WIRED TO SUPABASE 2026-10-19
2. **Business** (`naya-template-business`)
3. **Booking** (`naya-template-booking`)
4. **Product** (`naya-template-product`)
5. **Portfolio** (`naya-template-portfolio`)
6. **Event** (`naya-template-event`)
7. **Menu** (`naya-template-menu`)
8. **Community** (`naya-template-community`)
9. **Signup** (`naya-template-signup`)
10. **Dashboard** (`naya-template-dashboard`)
11. **Personal Hub** (`naya-template-personal-hub`)
12. **Business Hub** (`naya-template-business-hub`)

**Template architecture** (personal-v5.html, ~212KB):
- Cover (uploadable) → Avatar (uploadable) → Name/motto (editable, localStorage)
- Points badge (gold, Smart Ledger: note +10, connect +15, save +5, like +2)
- Connect button → Message button
- Plus button → Hub menu (12 destinations)
- Sticky spectrum nav (7 tabs: About, Intelligence Today, Smart Notes, Connections, Smart Mail, Smart Lists, Settings)
- Sections per tab
- Bottom Smart Tabs bar (F-01, spectrum, marquee)
- **Supabase integration** (2026-10-19): Quick Capture saves to proxy + localStorage; loads from both on page start

## The Design Language (LOCKED)

1. **SPECTRUM WALK**: Purple #a06bff → blue #3fb8ff → green #2fe89e → gold #ffbf3d → orange #ff9a5a → red #ff5e6c → magenta #e84fff → purple. Never same twice.
2. **WHITE AT REST, COLOR IGNITES**: Clean at rest, ignites in own color on hover.
3. **ELEVATION EVERYWHERE**: Multi-layer depth on every element. Nothing flat.
4. **RECTANGLES, NOT SQUARES**: Horizontal 16:9. Never squares/vertical.
5. **FULL WIDTH**: No max-width. Fill the screen.
6. **REAL PIECES ONLY**: Every element traces to Smart Factory (152 pieces).
7. **COLOR = IDENTITY**: Each section owns its spectrum color.

**Nav tabs** (Shawn's spec): About=purple, Intelligence Today=indigo #6675ff, Smart Notes=canyon blue #3fb8ff, Connections=green, Smart Mail=gold, Smart Lists=orange, Settings=red.

## Key Laws

- **DONE**: Committed to repo + announced on board + independently verified by different seat
- **FUNCTION**: Pretty + useless = not done. Every button must work.
- **HARVEST-FIRST**: Use existing pieces, never invent. Builder briefs name exact sources.
- **EDIT-ONLY**: Polish existing builds, never rebuild from scratch.
- **ALL-LAWS**: Partial compliance is not compliance.
- **Image A vs B**: A=complete/populated/functional (9/10). B=placeholders/coming soon (4/10). Never show B.
- **Scorecard everything**: Score, why not 10, fix, re-score. Merge bar: 9.5+different seat+no objection.

## The Heartbeat (2026-10-19)

**What**: Templates remember across devices via Supabase.

**How**:
1. User writes note in template
2. Template POSTs to `naya-supabase-proxy.nayapower.workers.dev/notes`
3. Proxy forwards to Supabase `smart_notes` table with anon key
4. On load, template GETs from proxy, merges with localStorage
5. Note appears on all devices

**Status**: Personal template wired and deployed. Other 11 need the same pattern.

## The Intelligence Layer (Next)

The 20 Edge Functions are ready but require authenticated users. To activate:
1. Implement Supabase Auth in templates (sign-in/sign-up)
2. Templates call `v7-smart-note-canonical` with user JWT (for governed note intake)
3. Templates call `nayanet-smart-mail` with user JWT (for messaging)
4. Backend services call law/know/act/prove runtimes with GitHub OIDC (for intelligence)

## What I Learned (2026-10-19)

1. **Wisdom > Intelligence**: Don't ask "what do you want?" Understand the system, then figure out where you fit.
2. **Heartbeat before brain**: Persistence first, intelligence second. She can't learn if she can't remember.
3. **Connect, don't rebuild**: The 20 Edge Functions exist. Use them, don't duplicate them.
4. **The system is almost ready**: All major parts done. We're connecting dots, not building from scratch.
5. **Document to know**: Write it down or you'll discover it again tomorrow.

## Open Threads

- Wire remaining 11 templates to Supabase (same pattern as personal)
- Connect factory Build button to pipeline (build-api.py + HTTP endpoint)
- Implement user auth for Edge Function intelligence layer
- Verity's full-system scorecard (requested 2026-10-19, awaiting response)
- Fix customize.py to replace demo identity ("Alex Morgan") with contract values
- Push pipeline commit 8cef83e per DONE law
