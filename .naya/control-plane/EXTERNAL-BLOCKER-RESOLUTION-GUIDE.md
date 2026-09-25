# 🔱 External Blocker Resolution Guide

**Status:** CANONICAL RESOLUTION PROTOCOL  
**Purpose:** Exact steps for authorized operator to resolve all external blockers preventing live proof completion

---

## BLOCKER SUMMARY

| # | Blocker | Type | Severity | Blocks |
|---|---------|------|----------|--------|
| B1 | `GITHUB_WEBHOOK_SECRET` not configured | EXTERNAL_CREDENTIAL | CRITICAL | GitHub webhook live proof |
| B2 | No authorized owner session + `intelligence_commit` grant | AUTHORITY_BOUNDARY | CRITICAL | LEARNING_OUTPUT execution (next control-plane action) |
| B3 | GitHub App not installed on target repo | PREREQUISITE | HIGH | GitHub webhook delivery |
| B4 | GitHub App not bound via Smart Connect | PREREQUISITE | HIGH | GitHub webhook owner resolution |

---

## B1: GITHUB_WEBHOOK_SECRET Configuration

### What
HMAC-SHA256 secret used to verify GitHub webhook signatures (`x-hub-signature-256` header)

### Where
Supabase Project: `dahisasgpfvziswqvmvm` (ca-central-1)
Edge Function: `nayanet-github-webhook`
Environment Variable: `GITHUB_WEBHOOK_SECRET`

### Current State
Live probe returns: `HTTP 503 {ok:false, error:"GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED", status:"BLOCKED_EXTERNAL_CREDENTIAL"}`

### Resolution Steps

#### Option A: Supabase Dashboard (Recommended)
1. Go to https://supabase.com/dashboard/project/dahisasgpfvziswqvmvm
2. Navigate to **Edge Functions** → `nayanet-github-webhook`
3. Click **Settings** → **Environment Variables**
4. Add: `GITHUB_WEBHOOK_SECRET` = `<your-secret>`
5. Save → Function auto-redeploys (version 5+)

#### Option B: Supabase CLI
```bash
# Requires Supabase CLI + project link
supabase secrets set GITHUB_WEBHOOK_SECRET=<your-secret> --project-ref dahisasgpfvziswqvmvm
```

#### Option C: GitHub Actions (if configured)
```yaml
# In workflow that manages secrets
- name: Set webhook secret
  run: |
    supabase secrets set GITHUB_WEBHOOK_SECRET=${{ secrets.GITHUB_WEBHOOK_SECRET }}
```

### Secret Requirements
- Must match the secret configured in GitHub App webhook settings
- Format: arbitrary string (recommended: 32+ chars, base64)
- Used for: HMAC-SHA256 verification of `x-hub-signature-256`
- Comparison: constant-time byte comparison (implemented in `nayanet-github-webhook/index.ts:10-17`)

### Verification
After configuration:
```bash
# Probe should now process signature check
curl -X POST https://dahisasgpfvziswqvmvm.supabase.co/functions/v1/nayanet-github-webhook \
  -H "Content-Type: application/json" \
  -H "x-github-delivery: test-123" \
  -H "x-hub-signature-256: sha256=invalid" \
  -d '{"action":"test"}'
# Should return 401 INVALID_GITHUB_SIGNATURE (not 503)
```

---

## B2: Owner Session + intelligence_commit Grant

### What
Legitimate authenticated owner session with valid in-scope `intelligence_commit` authority grant

### Current State
- Learning evidence `1112073e-08ee-407e-a47a-8b65b845f57b` exists with status `ACTIVE`
- No production authority grants for owner (`grant_count: 0, active_count: 0`)
- Control plane next action requires: `execute that exact LEARNING_OUTPUT candidate through the canonical intelligence_commit path`

### Resolution Steps

#### Step 1: Identify Owner
```sql
-- In Supabase SQL Editor
SELECT id, email FROM auth.users WHERE id = '1112073e-08ee-407e-a47a-8b65b845f57b';
```

#### Step 2: Obtain Owner Session
- Owner logs into Hub: `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev`
- Or use Supabase Auth API to generate token

#### Step 3: Issue intelligence_commit Grant
```sql
-- Via Supabase SQL Editor (service role)
SELECT nayanet_issue_authority_grant(
  p_subject_id := '1112073e-08ee-407e-a47a-8b65b845f57b',
  p_source_event_id := 'learning-evidence-1112073e-08ee-407e-a47a-8b65b845f57b',
  p_mission_id := 'NayaNET Project Intelligence',
  p_scope := '{"project_id": "NayaNET", "target": "learning-output-promotion"}'::jsonb,
  p_actions := ARRAY['intelligence_commit'],
  p_constraints := '{"single_use": true}'::jsonb,
  p_evidence := '{"reason": "Execute verified LEARNING_OUTPUT candidate"}'::jsonb
);
```

#### Step 4: Verify Grant
```sql
SELECT * FROM nayanet_authority_grants 
WHERE subject_id = '1112073e-08ee-407e-a47a-8b65b845f57b' 
AND status = 'ACTIVE'
AND actions @> ARRAY['intelligence_commit'];
```

### Verification
```bash
# Execute LEARNING_OUTPUT via compound-intelligence
curl -X POST https://dahisasgpfvziswqvmvm.supabase.co/functions/v1/nayanet-compound-intelligence \
  -H "Authorization: Bearer <owner-token>" \
  -H "Content-Type: application/json" \
  -d '{"action":"execute_learning_output", "evidence_id":"1112073e-08ee-407e-a47a-8b65b845f57b"}'
# Should return VERIFIED with event/index/provenance/receipt/retrieval
```

---

## B3: GitHub App Installation

### What
GitHub App installed on target repository (`SoulSchoolAcademy/NayaPOWER`)

### Current State
Not installed (required for webhook deliveries)

### Resolution Steps

#### Option A: GitHub UI
1. Go to GitHub App settings (or create new)
2. Install on `SoulSchoolAcademy/NayaPOWER`
3. Grant permissions: `Contents`, `Metadata`, `Pull requests`, `Issues`, `Webhooks`
4. Note: Installation ID will be in URL after install

#### Option B: GitHub API
```bash
# Requires GitHub App owner token
curl -X POST https://api.github.com/user/installations/<app_id> \
  -H "Authorization: Bearer <app-token>" \
  -H "Accept: application/vnd.github+json" \
  -d '{"repository_ids":[<repo_id>]}'
```

### Verification
```bash
# Check installation
curl -H "Authorization: Bearer <user-token>" \
  https://api.github.com/user/installations
# Should show installation for SoulSchoolAcademy/NayaPOWER
```

---

## B4: Smart Connect Binding

### What
Bind GitHub installation + repository to Smart Connect participation for owner

### Current State
No binding exists in `nayanet_smart_connect_participation.external_bindings`

### Prerequisites
- B3 complete (GitHub App installed)
- Owner has active `github_app` participation in Smart Connect

### Resolution Steps

#### Step 1: Verify Owner Participation
```sql
SELECT * FROM nayanet_smart_connect_participation 
WHERE member_id = '1112073e-08ee-407e-a47a-8b65b845f57b' 
AND door = 'github_app' 
AND status = 'active';
```

#### Step 2: If No Participation, Create It
```sql
INSERT INTO nayanet_smart_connect_participation (member_id, door, status, consent_state)
VALUES ('1112073e-08ee-407e-a47a-8b65b845f57b', 'github_app', 'active', 'explicit');
```

#### Step 3: Bind Installation + Repository
```sql
SELECT nayanet_smart_connect_github_bind(
  p_installation_id := <installation_id_from_B3>,
  p_repository := 'SoulSchoolAcademy/NayaPOWER'
);
```

#### Step 4: Verify Binding
```sql
SELECT * FROM nayanet_smart_connect_participation 
WHERE member_id = '1112073e-08ee-407e-a47a-8b65b845f57b'
AND door = 'github_app'
AND external_bindings @> '[{"provider":"github","installation_id":"<installation_id>","repository":"soulschoolacademy/nayapower"}]';
```

### Verification
```bash
# Test owner resolution
curl -X POST https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/rpc/nayanet_resolve_github_webhook_owner \
  -H "apikey: <service-role-key>" \
  -H "Authorization: Bearer <service-role-key>" \
  -H "Content-Type: application/json" \
  -d '{"p_installation_id": <installation_id>, "p_repository": "SoulSchoolAcademy/NayaPOWER"}'
# Should return owner UUID: 1112073e-08ee-407e-a47a-8b65b845f57b
```

---

## EXECUTION ORDER

```
REQUIRED SEQUENCE:
┌─────────────────────────────────────────────────────────────┐
│ 1. B3: GitHub App Installation                              │
│    ↓ (provides installation_id)                             │
│ 2. B4: Smart Connect Binding (uses installation_id)         │
│    ↓ (enables owner resolution)                             │
│ 3. B1: GITHUB_WEBHOOK_SECRET Configuration                  │
│    ↓ (enables signature verification)                       │
│ 4. B2: Owner Session + intelligence_commit Grant            │
│    ↓ (enables LEARNING_OUTPUT execution)                    │
│ 5. LIVE PROOF EXECUTION                                     │
│    - GitHub webhook delivery proof                          │
│    - LEARNING_OUTPUT execution proof                        │
└─────────────────────────────────────────────────────────────┘
```

---

## VERIFICATION CHECKLIST

| Step | Verification Command | Expected |
|------|---------------------|----------|
| 1 | `curl -X POST <webhook-url> -H "x-github-delivery: test" -H "x-hub-signature-256: sha256=invalid" -d '{}'` | `401 INVALID_GITHUB_SIGNATURE` |
| 2 | `curl -X POST <webhook-url> -H "x-github-delivery: test-123" -H "x-hub-signature-256: sha256=<valid>" -d '{"action":"push","repository":{"full_name":"SoulSchoolAcademy/NayaPOWER"},"installation":{"id":<id>}}'` | `200 OK {status:"PERSISTED",...}` |
| 3 | `curl -X POST <compound-url> -H "Authorization: Bearer <owner>" -d '{"action":"execute_learning_output"}'` | `200 OK {status:"VERIFIED",...}` |
| 4 | `SELECT * FROM nayanet_cognition_events WHERE event_id LIKE 'github:%' ORDER BY created_at DESC LIMIT 1;` | GitHub event persisted |
| 5 | `SELECT * FROM nayanet_cognition_events WHERE event_id LIKE 'learning:%' ORDER BY created_at DESC LIMIT 1;` | Learning event persisted |

---

## ESCALATION

| Blocker | If Cannot Resolve | Escalate To |
|---------|-------------------|-------------|
| B1 | No Supabase access | Shawn (project owner) |
| B2 | No owner access | Shawn (human director) |
| B3 | No GitHub App admin | Shawn (repo owner) |
| B4 | SQL permission error | Shawn (DB admin) |

---

## TRUTH BOUNDARY

> **No blocker is resolved by documentation alone.**
> 
> Each blocker requires a concrete external action by an authorized operator.
> 
> **Do not simulate, fabricate, or bypass.**
> 
> Document the exact boundary, complete all non-blocked dependencies, leave precise baton.

---

## NEXT NAYA CONTINUATION

After all blockers resolved, the next Naya should:
1. Verify all 5 verification commands pass
2. Execute GitHub webhook positive → replay → retrieval proof
3. Execute LEARNING_OUTPUT intelligence_commit proof
4. Update STATE/BLOCKS/PROOF/BATON with results
5. Leave single next action for subsequent Naya

---

```
[EXTERNAL-BLOCKER-GUIDE][SIGN-OFF]
STATUS: DOCUMENTED — AWAITING AUTHORIZED OPERATOR
BLOCKERS: 4 (B1 CRITICAL, B2 CRITICAL, B3 HIGH, B4 HIGH)
NEXT ACTION: Authorized operator executes B1→B2→B3→B4 sequence
VERIFICATION: 5 verification commands must PASS
```