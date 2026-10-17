# Scorecard — Naya 4 room integration, v3 (canonical D1–D8)

**Instrument:** PROJECT-INTELLIGENCE.md §2 — the measurement law. Eight dimensions,
every dimension ≥ 9.0, D1 = 10. Builder self-scores; an **independent seat re-scores**
(builder self-score never closes a gate). Scores can go DOWN. The v1/v2 scorecard
used invented dimensions; it is void. This replaces it.

**Target:** branch `naya4/hub-rooms-v1`, `~/workspace/your_files/nayanet-hub.html`
(918,871 bytes post-QA-fix).

**Evidence:** `v3-harness.js` — 50/50 checks green (10 rooms render · 10 canonical
doors · zero KPI stat cards in reports · §21 state chip in every room · all
HubActions execute · receipt chain links · prefs persist). `GAP-ANALYSIS.md`
documents the v2→v3 corrections. **Live-browser QA (Chrome 152, CDP, desktop
1440px + mobile 390px):** all 10 rooms render the furnished versions with zero
JS errors; door two-step → receipt; conn add/remove → persisted + receipted;
ledger verify → CHAIN VALID; receipts survive reload; hash deep-links on click
and on load; Smart Share → Smart Connect everywhere; mobile no-overflow.

| Dim | What 10 looks like | v3 self | Honest basis |
|---|---|---|---|
| D1 Visual Excellence | Every pixel obeys the Design Contract | **7.5** | Her component language adopted; room visuals consistent with shell. Naya 2's independent eye still pending — she owns the visual verdict. |
| D2 Functional Completeness | Every control has a real causal path; zero dead controls | **8.0** | 50/50 harness + live-browser proof: every button/tab/search/filter/action executes a real path in Chrome 152. Live QA caught and fixed 5 integration defects the harness missed (duplicate shadow defs, render() bypassing connections/mail, cross-IIFE scope, missing deep-link, stale Smart Share label). Depth still growing (live OAuth is runtime work). |
| D3 Intelligence | Thinks with NayaPOWER — real retrieval, real capture | **3** | Not connected to the nine-node kernel. Note capture attempts the runtime first, then says so honestly. Marked, not faked. |
| D4 Honesty | Never lies about what it knows | **9** | No sample data, no fake mailboxes, no simulated activity. Local vs runtime labeled everywhere. |
| D5 Performance | Feels instant | **6** | Single ~919KB file, no code-split. Core interactions are simple DOM; unmeasured on device. Phase 7 work. |
| D6 Reliability & Continuity | It remembers | **8.0** | Live-browser proof: receipts/notes/connections/collections persist across reload in Chrome 152; export works; erase works; hash chain verifies. Production persistence path (PR #1243) awaits Shawn's merge. |
| D7 Accessibility | Everyone can use it | **6.5** | Visible `:focus-visible` on all room controls; semantic buttons; reduced-motion honored. Never audited; screen-reader pass pending. |
| D8 Craft | The last 10% | **8.0** | Unified component language; empty states written with care; error states kind. Mobile 390px verified: no overflow, identity preserved, rooms fully usable. Full-page desktop screenshots reviewed room by room. |

**Composite: ~7.3/10.** Below 9.0 = not ready. The climb: Naya 2's visual pass (D1),
runtime adapter (D3), Phase 7 hardening (D5/D7). No inflation — the scorecard decides.

## v4 QA-fix corrections (live-browser pass, Chrome 152)

The Node harness verified sources; the browser verified the built artifact — and
found 5 defects the harness could not see:

1. Her base defines reports/library/settings/notes **twice**; JS hoisting made her
   stub the live one. build.py now replaces every definition.
2. Her `render()` routed connections/mail through `governed()` stubs, leaving the
   furnished rooms dead code. Rewired to the room functions.
3. connections()/mail() lived in a **different IIFE closure** than render() →
   ReferenceError on click. build.py appends them into render()'s closure.
4. Nav clicks never updated the address bar. `history.replaceState` deep-links
   `#/<room>` without double-firing her hashchange listener.
5. "Smart Share" survived in the nav rail and side map. Renamed to Smart Connect
   in all three places (room head, nav, side map).

Verified in the live browser after the fix: all 10 rooms render, zero JS errors,
door two-step receipts, conn add/remove persists, ledger CHAIN VALID, receipts
survive reload, deep-links work both directions, mobile 390px clean.

## v3 corrections vs v2 (from GAP-ANALYSIS.md)

- Scorecard replaced with the canonical D1–D8 (mine was invented).
- Reports rebuilt as narrative synthesis — v2's KPI stat cards violated §27.
- Smart Connect: 10 canonical doors (Phase 4), 2-step request flow with permission
  scopes; Connection ≠ permission to act, shown per door.
- §21 seven-state model: every room carries an explicit state chip.
- D2 audit: every `data-hub-action` mapped to a real causal path (harness-verified).
- `:focus-visible` styles added (§24). Smart Board law correction (15→8 layers)
  filed separately against the design-law PR.
