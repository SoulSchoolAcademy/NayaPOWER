# 🔱 NayaNET Intelligent Hub — AAA Visual/Interaction Pass Checklist

**Status:** CANONICAL RELEASE GATE  
**Target:** 10/10 AAA — Zero Critical Unknowns  
**Protected Visual Reference:** `2026 09 17 NAYANET HUB.html`  
**Canonical Hub Source:** `NAYANET/HUB/index.html`  
**Canonical Hub Source SHA:** `eb825f34caecdb925bd3d7fe6a4390ce072025d7`  

---

## 📋 EXECUTION RULE

**No feature is AAA until every checklist item has independent browser/runtime evidence.**  
**Visual regression = FAIL.**  
**Competing surface = FAIL.**  
**Missing evidence = BLOCKED.**

---

## 1. SHELL ARCHITECTURE (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 1.1 | **Single canonical shell** — AppShellV3 only; HubBaselineApp is iframe baseline only | Browser DOM inspection: exactly one `app-shell` root | ⏳ |
| 1.2 | **No right sidebar** — Permanent right rail MUST NOT EXIST | Visual inspection + DOM: no persistent right panel | ⏳ |
| 1.3 | **Left navigation only** — Single left rail with canonical nav items | DOM: one `nav` element in left position | ⏳ |
| 1.4 | **Shell owns all routes** — No competing top-level layouts | Route map: all paths render within AppShellV3 | ⏳ |
| 1.5 | **Responsive breakpoints** — Desktop (≥1024), Tablet (768-1023), Mobile (<768) | Browser devtools device toolbar: all 3 breakpoints render correctly | ⏳ |

---

## 2. NAVIGATION (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 2.1 | **Canonical nav items** — Intelligence, Activity, Library, Reports, Settings, Smart Spaces, Smart Lists | Visual: all 7 items present in left nav | ⏳ |
| 2.2 | **Active state indication** — Current route highlighted | Visual: active nav item distinct styling | ⏳ |
| 2.3 | **No duplicate navigation** — No breadcrumbs, tabs, or secondary nav competing | Visual: single nav authority | ⏳ |
| 2.4 | **Mobile nav drawer** — Hamburger → drawer with same items | Mobile viewport: drawer opens/closes, same 7 items | ⏳ |
| 2.5 | **Keyboard navigation** — Tab/Shift+Tab/Enter works on all nav | Keyboard-only test: full nav traversable | ⏳ |

---

## 3. SMART FEED — CORE INTELLIGENCE SURFACE (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 3.1 | **Feed central** — Smart Feed is primary content area | Visual: Feed occupies main content, not sidebar | ⏳ |
| 3.2 | **Three streams** — Personal / Activity / Collective tabs | Visual: three tabs, switchable | ⏳ |
| 3.3 | **Personal stream** — Shows owner's cognition events | Authenticated: events where user_id=auth.uid() | ⏳ |
| 3.4 | **Activity stream** — Shows owner's activity events | Authenticated: activity events for owner | ⏳ |
| 3.5 | **Collective stream** — Shows published intelligence | Published events with consent_state=explicit | ⏳ |
| 3.6 | **Intelligent Block cards** — Each item renders as canonical Block card | Visual: card with title, truth, authority, provenance, evidence | ⏳ |
| 3.7 | **Block card fields** — All required fields visible | Title, truth state, authority badge, provenance chain, evidence links | ⏳ |
| 3.8 | **Smart Ledger verification** — Verification state + confidence displayed | Visual: badge (VERIFIED/SUPPORTED/etc), confidence score | ⏳ |
| 3.9 | **Actions per item** — Save / Favorite / Like / Love / Share | Visual: action icons, hover states, click handlers | ⏳ |
| 3.10 | **Action persistence** — Actions survive reload | Reload: actions remain applied | ⏳ |
| 3.11 | **Infinite scroll / pagination** — Load more works | Scroll: new items load, no duplicates | ⏳ |
| 3.12 | **Empty state** — Helpful empty message when no items | Visual: "No intelligence yet. Create a Smart Note..." | ⏳ |
| 3.13 | **Loading state** — Skeleton/skeleton while fetching | Visual: skeleton cards during fetch | ⏳ |
| 3.14 | **Error state** — Graceful error display | Network error: toast + retry button | ⏳ |

---

## 4. SMART NOTE CAPTURE — PRIMARY SENDER (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 4.1 | **Capture entry point** — Accessible from main nav / FAB | Visual: "New Smart Note" button prominent | ⏳ |
| 4.2 | **Four artifacts** — Human / Naya / Machine / Intelligence Feed | Form: four text areas, all required | ⏳ |
| 4.3 | **Idempotency key** — Auto-generated, editable | Field: pre-filled UUID, user can override | ⏳ |
| 4.4 | **Evidence attachment** — URLs for artifacts | Field: evidence URLs array | ⏳ |
| 4.5 | **Subject auto-derivation** — From human note | Auto: subject from first line of human note | ⏳ |
| 4.6 | **Submit → canonical event** — Single event created | Network: POST to v7-smart-note-canonical, 200 OK | ⏳ |
| 4.7 | **Receipt displayed** — Event ID + receipt ID shown | Visual: toast/modal with IDs | ⏳ |
| 4.8 | **Feed projection** — New note appears in Personal stream | Navigate to Feed: new item at top | ⏳ |
| 4.9 | **Reload identity** — Same event ID after reload | Reload: item still there, same IDs | ⏳ |
| 4.10 | **Evidence visible** — Ledger verification on new item | Visual: verification badge on new card | ⏳ |

---

## 5. INTELLIGENT BLOCK LIFECYCLE (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 5.1 | **Block creation** — Smart Note → Block automatic | Feed: Block card appears with canonical fields | ⏳ |
| 5.2 | **Block identity** — Stable block_id across projections | Visual: block_id displayed, matches index | ⏳ |
| 5.3 | **Block truth** — Understanding state badge | Visual: CANDIDATE/VERIFIED/SUPERSEDED badge | ⏳ |
| 5.4 | **Block authority** — Authority scope visible | Visual: owner_scope badge | ⏳ |
| 5.5 | **Block provenance** — Source event lineage traceable | Click: lineage modal shows source events | ⏳ |
| 5.6 | **Supersede flow** — Block → Supersede → New Block | UI: supersede button, creates new block, lineage preserved | ⏳ |
| 5.7 | **Replay identity** — Supersede replay returns same block | Repeat supersede: same new block_id | ⏳ |
| 5.8 | **Continue authorization** — Authority grant for continuation | UI: continue button requires grant | ⏳ |
| 5.9 | **Successor handoff** — Successor context created | Feed: successor event visible | ⏳ |

---

## 6. SMART SHARE — PROVEN DOOR (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 6.1 | **Share action** — Available on owned intelligence | Personal stream: share button on own items | ⏳ |
| 6.2 | **Authority grant** — Explicit grant required | Modal: grant issuance before share | ⏳ |
| 6.3 | **Explicit consent** — Consent state = explicit | Visual: consent confirmation | ⏳ |
| 6.4 | **Publication created** — Collective stream entry | Collective stream: new published item | ⏳ |
| 6.5 | **Publisher identity private** — "Private by default" badge | Visual: publisher identity hidden | ⏳ |
| 6.6 | **Collective actions** — Save/Favorite/Like/Love on collective | Collective stream: action icons | ⏳ |
| 6.7 | **Revocation** — Owner can revoke publication | Publication: revoke button, status=revoked | ⏳ |
| 6.8 | **Revoked = invisible** — Revoked removed from collective | Collective stream: revoked item gone | ⏳ |
| 6.9 | **Replay identity** — Share replay returns same publication | Repeat share: same publication_id | ⏳ |

---

## 7. SMART MAIL — NEXT DOOR (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 7.1 | **Compose UI** — Recipient picker (Connections only) | Visual: connection selector | ⏳ |
| 7.2 | **Thread view** — Messages grouped by thread | Visual: thread list + message detail | ⏳ |
| 7.3 | **Authority grant** — smart_mail_send required | Modal: grant before send | ⏳ |
| 7.4 | **Send → receipt** — Message + thread + receipt created | Network: 200 OK, receipt displayed | ⏳ |
| 7.5 | **Receiver retrieval** — Recipient sees in Feed/mail | Recipient login: message visible | ⏳ |
| 7.6 | **Reply flow** — Reply in same thread | UI: reply button, same thread_id | ⏳ |
| 7.7 | **Verification** — Receiver verifies message | UI: verify button, verification state | ⏳ |
| 7.8 | **Learning bridge** — Message → learning evidence | Learning: evidence created from mail | ⏳ |

---

## 8. SMART SPACES / CONNECTIONS / LISTS (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 8.1 | **Spaces list** — Owned + joined spaces | Visual: space cards with status | ⏳ |
| 8.2 | **Create space** — Private by default | Modal: create, defaults private | ⏳ |
| 8.3 | **Invite/join** — Connection-based invites | UI: invite from connections | ⏳ |
| 8.4 | **Connections list** — Owner's connections | Visual: connection cards | ⏳ |
| 8.5 | **Connect/revoke** — Owner-only actions | Buttons: connect (non-owner), revoke (owner) | ⏳ |
| 8.6 | **Non-owner blocked** — 403 on wrong actions | Network: 403 RECEIVER_MISMATCH | ⏳ |
| 8.7 | **Lists CRUD** — Create/add/remove | UI: full list lifecycle | ⏳ |
| 8.8 | **List membership** — Connections only | Add: connection picker | ⏳ |

---

## 9. SEARCH / LIBRARY / REPORTS / SETTINGS (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 9.1 | **Global search** — Finds across intelligence | Search: results from cognition events | ⏳ |
| 9.2 | **Library** — Browse all intelligence | Route: /library, paginated | ⏳ |
| 9.3 | **Reports** — Generated insights | Route: /reports, view/download | ⏳ |
| 9.4 | **Settings** — Profile, preferences, auth | Route: /settings, functional | ⏳ |
| 9.5 | **Evidence surface** — Provenance viewer | Route: /evidence/:eventId, full lineage | ⏳ |

---

## 10. IDENTITY / NAME-FIRST SESSION (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 10.1 | **Name-first auth** — Email → name → Hub | Flow: name entry before Hub access | ⏳ |
| 10.2 | **Session persistence** — Survives reload | Reload: still authenticated | ⏳ |
| 10.3 | **Logout** — Clears session, returns to name | Click logout: name entry screen | ⏳ |
| 10.4 | **Private by default** — No public exposure | Network: no public data without consent | ⏳ |

---

## 11. VISUAL FIDELITY (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 11.1 | **Protected reference match** — Pixel-perfect vs `2026 09 17 NAYANET HUB.html` | Visual diff tool: 0 critical differences | ⏳ |
| 11.2 | **Typography scale** — Consistent heading/body/caption | Visual: design system tokens applied | ⏳ |
| 11.3 | **Color system** — Semantic colors (primary, success, warning, error) | Visual: color tokens, dark/light mode | ⏳ |
| 11.4 | **Spacing system** — Consistent 4px grid | Visual: spacing tokens | ⏳ |
| 11.5 | **Border radius** — Consistent rounded corners | Visual: radius tokens | ⏳ |
| 11.6 | **Shadows/elevation** — Consistent depth | Visual: elevation tokens | ⏳ |
| 11.7 | **Icons** — Consistent icon set (Lucide/Phosphor) | Visual: single icon library | ⏳ |
| 11.8 | **Animations** — Meaningful, not decorative | Interaction: transitions on state change | ⏳ |
| 11.9 | **Focus states** — Visible keyboard focus | Keyboard: visible focus rings | ⏳ |
| 11.10 | **Reduced motion** — Respects prefers-reduced-motion | OS setting: animations disabled | ⏳ |

---

## 12. INTERACTION QUALITY (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 12.1 | **Click/touch targets** — ≥44px minimum | Visual: all interactive elements meet size | ⏳ |
| 12.2 | **Hover states** — All interactive elements | Mouse: hover feedback | ⏳ |
| 12.3 | **Active/pressed states** — Feedback on press | Touch/click: pressed feedback | ⏳ |
| 12.4 | **Disabled states** — Clear disabled styling | Visual: disabled = muted + not clickable | ⏳ |
| 12.5 | **Toast notifications** — Non-blocking, auto-dismiss | Action: toast appears, dismisses | ⏳ |
| 12.5 | **Modal dialogs** — Focus trap, ESC to close | Keyboard: trap + ESC | ⏳ |
| 12.6 | **Form validation** — Inline, real-time | Input: validation messages | ⏳ |
| 12.7 | **Drag/drop** — Where applicable (lists, spaces) | Interaction: drag works | ⏳ |

---

## 13. ACCESSIBILITY (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 13.1 | **Semantic HTML** — Proper landmarks, headings | axe-core: 0 violations | ⏳ |
| 13.2 | **ARIA labels** — All interactive elements | Screen reader: all labeled | ⏳ |
| 13.3 | **Color contrast** — WCAG AA minimum | axe-core: contrast PASS | ⏳ |
| 13.4 | **Keyboard navigation** — Full app traversable | Keyboard-only: complete journey | ⏳ |
| 13.5 | **Screen reader** — NVDA/VoiceOver compatible | Screen reader: all content announced | ⏳ |
| 13.6 | **Language declaration** — html lang attribute | HTML: lang="en" | ⏳ |

---

## 14. PERFORMANCE (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 14.1 | **First Contentful Paint** — <1.5s | Lighthouse: FCP < 1.5s | ⏳ |
| 14.2 | **Largest Contentful Paint** — <2.5s | Lighthouse: LCP < 2.5s | ⏳ |
| 14.3 | **Cumulative Layout Shift** — <0.1 | Lighthouse: CLS < 0.1 | ⏳ |
| 14.4 | **Total Blocking Time** — <200ms | Lighthouse: TBT < 200ms | ⏳ |
| 14.5 | **Bundle size** — <500KB gzipped | Build: main bundle < 500KB | ⏳ |

---

## 15. EVIDENCE / PROVENANCE DISPLAY (Must Score 10/10)

| # | Check | Evidence Required | Status |
|---|-------|-------------------|--------|
| 15.1 | **Event ID visible** — On every intelligence item | Visual: event_id displayed | ⏳ |
| 15.2 | **Receipt ID visible** — On every intelligence item | Visual: receipt_id displayed | ⏳ |
| 15.3 | **Ledger hash** — Verification evidence link | Visual: ledger_event_id link | ⏳ |
| 15.4 | **Source lineage** — Traceable to origin | Click: lineage modal | ⏳ |
| 15.5 | **Authority lineage** — Grant traceable | Click: grant lineage | ⏳ |
| 15.6 | **Timestamp** — occurred_at displayed | Visual: relative + absolute time | ⏳ |

---

## 🎯 EXECUTION PROTOCOL

### Pre-Checklist (Before Starting)
- [ ] Resolve live main HEAD: `git rev-parse HEAD`
- [ ] Deploy canonical Hub: `gh workflow run assistant-cloudflare-hub-release.yml`
- [ ] Verify exact source parity: deployed SHA = canonical Hub source SHA
- [ ] Open Chrome DevTools + Lighthouse + axe-core
- [ ] Have two authenticated test accounts ready

### Per-Category Execution
1. **Navigate** to each surface
2. **Interact** with every control
3. **Verify** against checklist
4. **Screenshot** evidence (before/after/reload)
5. **Record** PASS/FAIL/BLOCKED
6. **Stop at first FAIL** → repair causal boundary → rerun category

### Post-Checklist
- [ ] All 15 categories = PASS
- [ ] Zero critical unknowns
- [ ] Zero visual regressions vs protected reference
- [ ] Evidence artifacts uploaded
- [ ] Scorecard updated to 10/10
- [ ] Release gate = GREEN

---

## 📊 SCORECARD TEMPLATE

| Category | Target | Actual | Evidence | Blocker |
|----------|--------|--------|----------|---------|
| Shell Architecture | 10/10 | — | — | — |
| Navigation | 10/10 | — | — | — |
| Smart Feed | 10/10 | — | — | — |
| Smart Note Capture | 10/10 | — | — | — |
| Intelligent Block Lifecycle | 10/10 | — | — | — |
| Smart Share | 10/10 | — | — | — |
| Smart Mail | 10/10 | — | — | — |
| Spaces/Connections/Lists | 10/10 | — | — | — |
| Search/Library/Reports/Settings | 10/10 | — | — | — |
| Identity/Name-First | 10/10 | — | — | — |
| Visual Fidelity | 10/10 | — | — | — |
| Interaction Quality | 10/10 | — | — | — |
| Accessibility | 10/10 | — | — | — |
| Performance | 10/10 | — | — | — |
| Evidence/Provenance Display | 10/10 | — | — | — |
| **OVERALL** | **10/10** | **—** | **—** | **—** |

---

## 🚀 RELEASE GATE

```
AAA RELEASE CRITERIA:
☐ All 15 categories = 10/10
☐ Zero critical unknowns
☐ Zero visual regressions
☐ Evidence artifacts for every PASS
☐ Source parity verified (deployed = canonical)
☐ Cold successor can continue without human reconstruction
☐ Scorecard ≥ 9.5 on all critical subsystems
☐ Single next action for post-release

IF ALL ☐ → RELEASE GATE = GREEN
ELSE → RELEASE GATE = RED (block, repair, rerun)
```

---

## 📝 SIGN-OFF

```
[AAA][CHECKLIST]
STATUS: PENDING_EXECUTION
CANONICAL_HUB: NAYANET/HUB/index.html
PROTECTED_REFERENCE: 2026 09 17 NAYANET HUB.html
NEXT_ACTION: Execute checklist against live deployed Hub
EVIDENCE_REQUIRED: Screenshots + Lighthouse + axe-core + network logs per category
```