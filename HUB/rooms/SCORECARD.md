# Scorecard — Naya 4 room integration, v3 (canonical D1–D8)

**Instrument:** PROJECT-INTELLIGENCE.md §2 — the measurement law. Eight dimensions,
every dimension ≥ 9.0, D1 = 10. Builder self-scores; an **independent seat re-scores**
(builder self-score never closes a gate). Scores can go DOWN. The v1/v2 scorecard
used invented dimensions; it is void. This replaces it.

**Target:** branch `naya4/hub-rooms-v1`, `~/workspace/your_files/nayanet-hub.html`
(905,145 bytes, deterministic md5 `52c289480187df39f5aff6a918f38d7c`).

**Evidence:** `v3-harness.js` — 50/50 checks green (10 rooms render · 10 canonical
doors · zero KPI stat cards in reports · §21 state chip in every room · all
HubActions execute · receipt chain links · prefs persist). `GAP-ANALYSIS.md`
documents the v2→v3 corrections.

| Dim | What 10 looks like | v3 self | Honest basis |
|---|---|---|---|
| D1 Visual Excellence | Every pixel obeys the Design Contract | **7.5** | Her component language adopted; room visuals consistent with shell. Naya 2's independent eye still pending — she owns the visual verdict. |
| D2 Functional Completeness | Every control has a real causal path; zero dead controls | **7.5** | 50/50 harness: every button/tab/search/filter/action executes a real path. Depth still growing (e.g., Connect doors record requests; live OAuth is runtime work). |
| D3 Intelligence | Thinks with NayaPOWER — real retrieval, real capture | **3** | Not connected to the nine-node kernel. Note capture attempts the runtime first, then says so honestly. Marked, not faked. |
| D4 Honesty | Never lies about what it knows | **9** | No sample data, no fake mailboxes, no simulated activity. Local vs runtime labeled everywhere. |
| D5 Performance | Feels instant | **6** | Single 905KB file, no code-split. Core interactions are simple DOM; unmeasured on device. Phase 7 work. |
| D6 Reliability & Continuity | It remembers | **7.5** | localStorage persists across sessions; export works; erase works. Production persistence path (PR #1243) awaits Shawn's merge. |
| D7 Accessibility | Everyone can use it | **6.5** | Visible `:focus-visible` on all room controls; semantic buttons; reduced-motion honored. Never audited; screen-reader pass pending. |
| D8 Craft | The last 10% | **7.5** | Unified component language; empty states written with care; error states kind. Mobile identity-preservation untested. |

**Composite: ~7.0/10.** Below 9.0 = not ready. The climb: Naya 2's visual pass (D1),
runtime adapter (D3), Phase 7 hardening (D5/D7). No inflation — the scorecard decides.

## v3 corrections vs v2 (from GAP-ANALYSIS.md)

- Scorecard replaced with the canonical D1–D8 (mine was invented).
- Reports rebuilt as narrative synthesis — v2's KPI stat cards violated §27.
- Smart Connect: 10 canonical doors (Phase 4), 2-step request flow with permission
  scopes; Connection ≠ permission to act, shown per door.
- §21 seven-state model: every room carries an explicit state chip.
- D2 audit: every `data-hub-action` mapped to a real causal path (harness-verified).
- `:focus-visible` styles added (§24). Smart Board law correction (15→8 layers)
  filed separately against the design-law PR.
