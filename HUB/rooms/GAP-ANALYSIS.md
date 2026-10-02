# Gap analysis — nayanet-hub.html v2 vs the /hub specs (2026-10-01, Naya 4 self-analysis)

Shawn's standing order: read the specs, analyze my own work against them, fix what's not right.
This is that analysis. Brutal on purpose.

## What I got wrong

1. **Invented my own scorecard.** The canonical instrument is PROJECT-INTELLIGENCE.md §2:
   D1–D8, every dimension ≥ 9.0, D1 = 10, builder self-scores AND an independent
   seat re-scores, scores can go DOWN. My 8-dimension lookalike is void. Replaced in v3.
2. **Invented a 15-layer Smart Board.** Contract §16: EIGHT layers, nested intelligence,
   not repeated sections — HUMAN NOTE · CHILD · GRANDMA NOTE · NAYA NOTE · MACHINE NOTE ·
   ADAPTIVE LEARNING · WHAT IT MEANS · WHAT'S IN IT FOR YOU. My #1294 Smart Board Law
   needs this correction (filed as a fix, not a quiet edit).
3. **Reports room violates §27 ("WHAT NOT TO ADD").** "More KPI stats" and
   "Never just '12 objects found'" — my v2 reports room is literally three stat cards
   + counts. Rebuilt in v3 as narrative synthesis with evidence trails.
4. **No §21 seven-state model.** LOADING · EMPTY · READY · BLOCKED · NOT_VERIFIED ·
   VERIFIED · ERROR — "no room is exempt." My rooms had ~2 implicit states. v3 adds
   explicit state chips per room.
5. **Invented Connect doors.** The canonical 10 (PROJECT-INTELLIGENCE.md Phase 4):
   MCP · REST/OpenAPI · GitHub App · Webhooks · SDK · A2A · Browser/Web Hub ·
   Email-messaging adapters · Enterprise identity · Private MCP tunnel. My 5-door
   set is replaced.
6. **D2 never audited.** "Every button, tab, search, filter has a real causal path.
   Zero dead controls." v3 maps every data-hub-action to its path (see table).
7. **D7 gaps.** No `:focus-visible` styles in my injected CSS; keyboard operability
   assumed, never verified. v3 adds visible focus; full audit is Phase 7 work.
8. **D3 honesty debt.** The Hub is not connected to the nine-node kernel (D3 ≈ 2.7
   per the doc). My rooms must not imply otherwise — states say what is local.

## What held up

- D4 honesty: no fake data anywhere; Mail = NO MAIL; runtime states labeled.
- Her shell untouched; today() diary verbatim; cross-room store + hash routing real.
- Deterministic repo build (same md5 across runs).

## D2 causal-path audit (v3)

| Control | Path |
|---|---|
| report-range tabs | recompute synthesis from real objects in range |
| lib search/facets | filters the real rendered index; OPEN scrolls to the board |
| lib inspect | expands the object's full text inline |
| door request flow | door → scope → confirm → stored request + ledger receipt |
| conn request/add/remove | stored + receipted; scopes shown |
| ledger verify | recomputes the hash chain, reports |
| hub export/erase | real download / real localStorage clear + reload |
| list tabs/collections | CRUD on the shared store |
| mail check | re-reads runtime presence, honestly |
| space create | stored; capture counts per space |
| note capture | runtime-first, labeled local fallback, receipted |
| settings toggles | prefs persisted + applied (reduce-motion) |

## v3 self-scores (canonical D1–D8)

| Dim | v2 | v3 target | v3 honest |
|---|---|---|---|
| D1 Visual Excellence | 7 | 8 | 7.5 — her language adopted; Naya 2's eye still pending |
| D2 Functional Completeness | 6 | 8 | 7.5 — all paths real; depth still growing |
| D3 Intelligence | 3 | 3 | 3 — not connected to kernel; honestly marked |
| D4 Honesty | 9 | 9 | 9 |
| D5 Performance | 6 | 6 | 6 — single file; code-split is Phase 7 |
| D6 Reliability & Continuity | 7 | 7.5 | 7.5 — localStorage persists; prod path awaits #1243 |
| D7 Accessibility | 5 | 6.5 | 6.5 — focus visible, buttons semantic; audit pending |
| D8 Craft | 6.5 | 7.5 | 7.5 — unified component language |

Composite: v2 ~6.9 → **v3 ~7.0/10**. The climb to 9+ needs Naya 2's visual pass (D1),
the runtime adapter (D3), and Phase 7 hardening (D5/D7). No inflation: below 9.0 is not ready.
