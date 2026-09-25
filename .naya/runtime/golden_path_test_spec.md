# Human Golden Path Test Specification

**Status:** CANONICAL TEST SPECIFICATION  
**Target:** OPEN → UNDERSTAND → NAVIGATE → SEARCH → CREATE → SAVE → SEE RESULT → RELOAD → FIND → EVIDENCE → CONTINUE  
**Canonical Hub:** `NAYANET/HUB/index.html`  
**Protected Visual Reference:** `2026 09 17 NAYANET HUB.html`  
**Prerequisite:** Authenticated user session (2 test accounts: owner + non-owner)

---

## TEST PHILOSOPHY

> **The goal is not to test features. The goal is to test the human journey.**
> 
> A feature exists in service of distilled intelligence. The test proves a human can accomplish a real outcome without becoming a project manager.

---

## TEST ACCOUNTS REQUIRED

| Account | Purpose |
|---------|---------|
| `owner@test.nayanet` | Full journey: create, save, share, continue |
| `nonowner@test.nayanet` | Isolation verification: cannot see owner's private intelligence |

---

## GOLDEN PATH STEPS

### Phase 1: ENTRY & UNDERSTAND
| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 1.1 | Navigate to `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev` | Name-first auth screen loads | Screenshot |
| 1.2 | Enter name "Test Owner" | Redirects to Hub, session established | Network: 200 OK, localStorage `nayanet.supabase.auth` |
| 1.3 | Observe Hub shell | AppShellV3 loads, left nav visible, no right rail | Screenshot + DOM check |
| 1.4 | Read Smart Feed (Personal) | Empty state or existing intelligence | Screenshot |
| 1.5 | Read Activity lens | Activity events visible | Screenshot |
| 1.6 | Read Collective lens | Published intelligence (if any) | Screenshot |

**Pass Criteria:** All 3 lenses render without console errors. One shell (AppShellV3). One left nav. No right rail.

---

### Phase 2: NAVIGATE & SEARCH
| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 2.1 | Click "Intelligence" in left nav | Library view loads | Screenshot |
| 2.2 | Use search bar: "test" | Results filter in real-time | Screenshot |
| 2.3 | Click "Reports" in left nav | Reports view loads | Screenshot |
| 2.4 | Click "Settings" in left nav | Settings view loads | Screenshot |
| 2.5 | Click "Smart Spaces" in left nav | Spaces view loads | Screenshot |
| 2.6 | Click "Smart Lists" in left nav | Lists view loads | Screenshot |

**Pass Criteria:** All 7 nav items (Intelligence, Activity, Reports, Settings, Smart Spaces, Smart Lists, Smart Mail) accessible. Search works across all views.

---

### Phase 3: CREATE → SAVE → SEE RESULT
| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 3.1 | Click "New Smart Note" (FAB or nav) | Capture modal opens | Screenshot |
| 3.2 | Fill Human Note: "Test golden path capture" | Text accepted | - |
| 3.3 | Fill Naya Note: "This verifies the human journey" | Text accepted | - |
| 3.4 | Fill Machine Note: "Automated test artifact" | Text accepted | - |
| 3.5 | Fill Intelligence Feed: "Golden path verified" | Text accepted | - |
| 3.6 | Fill Intelligent Block: "Human journey works end-to-end" | Text accepted | - |
| 3.7 | Fill Evidence: `{}` | Accepted | - |
| 3.8 | Fill Hub State: `{}` | Accepted | - |
| 3.9 | Click "Save" | POST to v7-smart-note-canonical | Network: 200 OK |
| 3.10 | Observe receipt toast | Event ID + Receipt ID displayed | Screenshot + copy IDs |
| 3.11 | Navigate to Personal Feed | New Smart Note at top | Screenshot |
| 3.12 | Click Smart Note card | Opens detail view | Screenshot |
| 3.13 | Verify 4 artifacts visible | Human/Naya/Machine/Feed tabs | Screenshot |
| 3.14 | Verify Intelligent Block visible | Block card with truth/authority/provenance | Screenshot |
| 3.15 | Verify Smart Ledger verification | Badge: VERIFIED, confidence: 1 | Screenshot |

**Pass Criteria:** Single Smart Note creates canonical event → cognition → PIS → Smart Ledger → Feed projection. All 4 artifacts + Block + Ledger verification visible. IDs match receipt toast.

---

### Phase 4: RELOAD → FIND → EVIDENCE
| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 4.1 | Hard reload (Ctrl+Shift+R) | Hub reloads, session persists | - |
| 4.2 | Navigate to Personal Feed | Same Smart Note at top | Screenshot |
| 4.3 | Click Smart Note | Same detail view | Screenshot |
| 4.4 | Verify Event ID matches receipt | ID identical | Compare screenshots |
| 4.5 | Verify Receipt ID matches receipt | ID identical | Compare screenshots |
| 4.6 | Verify Intelligent Block ID stable | Block ID unchanged | Screenshot |
| 4.7 | Verify Ledger verification still active | Badge: VERIFIED, confidence: 1 | Screenshot |
| 4.8 | Open Evidence panel (if available) | Lineage: Event → Cognition → PIS → Ledger → Block | Screenshot |

**Pass Criteria:** Complete identity stability across reload. All IDs match. Ledger verification persists. Lineage traceable.

---

### Phase 5: SHARE → COLLECTIVE → REVOKE
| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 5.1 | Click "Share" on Smart Note | Authority grant modal | Screenshot |
| 5.2 | Issue grant (smart_share) | Grant issued | Network: 200 OK, grant ID |
| 5.3 | Confirm explicit consent | Consent modal → confirm | Screenshot |
| 5.4 | Observe Collective Feed | Smart Note appears in Collective | Screenshot |
| 5.5 | Verify publisher identity hidden | "Private by default" badge | Screenshot |
| 5.6 | Click "Revoke" | Publication status = revoked | Network: 200 OK |
| 5.6 | Verify Collective Feed | Smart Note removed | Screenshot |
| 5.7 | Verify Personal Feed | Smart Note still there (private) | Screenshot |

**Pass Criteria:** Share requires grant + explicit consent. Revocation immediate. Private by default enforced.

---

### Phase 6: ISOLATION VERIFICATION (Non-Owner)
| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 6.1 | Logout owner, login non-owner | Name-first auth → Hub | - |
| 6.2 | Navigate to Personal Feed | Empty (no owner's intelligence) | Screenshot |
| 6.3 | Navigate to Collective Feed | Owner's shared note NOT visible (revoked) | Screenshot |
| 6.4 | Navigate to Library | Owner's intelligence NOT visible | Screenshot |
| 6.5 | Attempt direct URL to owner's Smart Note | 404 or 403 | Network: 403/404 |
| 6.7 | Attempt direct URL to owner's Intelligent Block | 404 or 403 | Network: 403/404 |

**Pass Criteria:** Private by default enforced. Non-owner sees zero owner intelligence. Collective only shows explicitly published + consented.

---

### Phase 7: CONTINUE → AUTHORIZED NEXT ACTION
| Step | Action | Expected | Evidence |
|------|--------|----------|----------|
| 7.1 | Login as owner | Session restored | - |
| 7.2 | Open Smart Note detail | "Continue" or next action available | Screenshot |
| 7.3 | Click "Continue" (if available) | Authorized continuation flow | - |
| 7.4 | Verify authority grant required | Modal: grant required | Screenshot |
| 7.5 | Issue minimum intelligence_commit grant | Grant issued | Network: 200 OK |
| 7.6 | Execute continuation | New Intelligent Block or decision | Receipt + event ID |
| 7.7 | Verify successor context | New event + receipt + baton update | Screenshot |

**Pass Criteria:** Continuation requires explicit authority grant. Successor context created with full lineage.

---

## NEGATIVE TESTS (Must Fail Closed)

| Test | Action | Expected Failure |
|------|--------|------------------|
| N1 | Non-owner accesses owner's private Smart Note | 403/404 |
| N2 | Non-owner accesses owner's private Intelligent Block | 403/404 |
| N3 | Share without authority grant | 403 AUTH_REQUIRED |
| N4 | Share without explicit consent | 403 CONSENT_REQUIRED |
| N5 | Revoke non-existent publication | 404 NOT_FOUND |
| N6 | Duplicate Smart Note (same idempotency key) | REPLAY status, same IDs |
| N7 | Malformed Smart Note payload | 400 INVALID_JSON |
| N8 | Unauthorized Smart Note capture (no auth) | 401 UNAUTHORIZED |

---

## EVIDENCE COLLECTION CHECKLIST

| Artifact | Location | Required |
|----------|----------|----------|
| Screenshots (all phases) | Test run artifact | YES |
| Network logs (HAR) | Test run artifact | YES |
| Console logs | Test run artifact | YES |
| Event IDs (all) | Test notes | YES |
| Receipt IDs (all) | Test notes | YES |
| Grant IDs (all) | Test notes | YES |
| Event IDs from DB | Supabase query | YES |
| Receipt IDs from DB | Supabase query | YES |
| Ledger events from DB | Supabase query | YES |
| PLAYBACK_LINEAGE.json | `.naya/control-plane/` | YES |
| BATON.json | `.naya/control-plane/` | YES |
| Activity board update | `NAYA/ACTIVITY/2026/09/` | YES |

---

## PASS/FAIL CRITERIA

| Category | Requirement |
|----------|-------------|
| **All 7 phases** | PASS |
| **All 8 negative tests** | FAIL CLOSED (as expected) |
| **Zero console errors** | PASS |
| **Zero network 5xx** | PASS |
| **Identity stability** | All IDs match across reload |
| **Privacy isolation** | Non-owner sees zero owner intelligence |
| **Evidence completeness** | All checklist items collected |

**Overall: GOLDEN PATH = PASS only if ALL above = PASS**

---

## EXECUTION COMMANDS

```bash
# 1. Deploy canonical Hub (if not current)
gh workflow run assistant-cloudflare-hub-release.yml \
  -f approval=EXPLICIT_APPROVAL_GRANTED \
  -f reason="Golden path test deployment" \
  -f source_ref=main

# 2. Wait for deployment, verify URL
# https://sparkling-shape-7ae5.smartnetpodcast.workers.dev

# 3. Run Playwright test
cd tests/
python golden_path_test.py --owner=owner@test.nayanet --nonowner=nonowner@test.nayanet

# 4. Collect evidence artifacts
# Artifacts uploaded automatically by test runner

# 5. Verify Supabase state
psql "postgresql://..." -c "SELECT * FROM nayanet_cognition_events WHERE user_id='owner-id' ORDER BY created_at DESC LIMIT 5;"
psql "postgresql://..." -c "SELECT * FROM nayanet_execution_receipts WHERE user_id='owner-id' ORDER BY created_at DESC LIMIT 5;"
psql "postgresql://..." -c "SELECT * FROM nayanet_smart_ledger WHERE owner_id='owner-id' ORDER BY created_at DESC LIMIT 5;"
psql "postgresql://..." -c "SELECT * FROM nayanet_intelligence_index WHERE owner_id='owner-id' ORDER BY created_at DESC LIMIT 5;"
```

---

## EVIDENCE RECEIPT TEMPLATE

```markdown
# GOLDEN PATH TEST RECEIPT — YYYY-MM-DD

**Test Run ID:** <GitHub Actions run ID>
**Source HEAD:** <git rev-parse HEAD>
**Owner:** <owner@test.nayanet>
**Non-Owner:** <nonowner@test.nayanet>

## PHASE RESULTS
| Phase | Status | Event ID | Receipt ID | Notes |
|-------|--------|----------|------------|-------|
| 1 Entry | PASS/FAIL | - | - | |
| 2 Navigate | PASS/FAIL | - | - | |
| 3 Create | PASS/FAIL | <event_id> | <receipt_id> | |
| 4 Reload | PASS/FAIL | <event_id> | <receipt_id> | Identity match: YES/NO |
| 5 Share | PASS/FAIL | <pub_id> | <grant_id> | Revoke: PASS/FAIL |
| 6 Isolation | PASS/FAIL | - | - | Non-owner count: 0 |
| 7 Continue | PASS/FAIL | <event_id> | <receipt_id> | Grant: <grant_id> |

## NEGATIVE TESTS
| Test | Status | Expected Failure |
|------|--------|------------------|
| N1 | PASS/FAIL | 403/404 |
| N2 | PASS/FAIL | 403/404 |
| ... | | |

## EVIDENCE ARTIFACTS
- Screenshots: <artifact URL>
- HAR file: <artifact URL>
- DB queries: <output>
- PLAYBACK_LINEAGE.json: <content>
- BATON.json: <content>

## VERDICT
**GOLDEN PATH: PASS / FAIL**

**If FAIL:** First failure: <phase.step> - <error>
**Repair:** <causal boundary>
```