# 🔱 HUB 10/10 — PROJECT INTELLIGENCE & BUILD LAW (CANONICAL v2)

**Version:** 2.0 — 2026-10-01
**Authority:** Shawn Vibert, Human Director
**Reconciled from:** Naya 2's `HUB-10-10-PROJECT-INTELLIGENCE-V1` (8 dimensions, scorecard instrument, phases 0–8) + Naya 4's elite design contract (12 frozen laws, Smart Doors spec, 22-element criteria)
**Companion:** `HUB/DESIGN-CONTRACT.md` (the visual law — this document is the build law)
**Frozen visual baseline:** `HUB/NAYANET INTERFACE CONCEPT.html` @ main `ffedda20`

> Reconciliation notes: the 8-dimension scorecard and its instrument are adopted as the measurement law (cleaner governance). The 22 granular element criteria fold in as measurement detail under their parent dimension. The Phase 0–8 plan is adopted (more actionable than the 4-phase version). The Smart Doors spec and Door Law are baked into Phase 4. Where the two sources disagreed, the disagreement is named below — never silently resolved.

---

## 1. THE MISSION IN ONE PARAGRAPH

Turn the Hub concept into a real, working, intelligent application that scores 10/10 on every dimension that matters — visual, functional, intelligent, honest, fast, reliable, accessible, crafted — without ever regressing the visual quality Shawn already loves. We measure with the scorecard in §3, in the open, every phase. Nothing is "done" until it scores.

---

## 2. WHAT 10/10 MEANS — THE EIGHT DIMENSIONS

### D1 · Visual Excellence — "the most elite interface anyone has ever experienced"
**10 looks like:** Every pixel obeys the Design Contract. Living depth on every interactive object. The full 12-color spectrum used semantically. One jewel icon family, zero emoji-as-icon. Boards feel like distinct intelligent objects. Motion is physical and purposeful.
**9.0 (the bar):** Contract obeyed everywhere; at most minor polish items remain.
**Current: 8.7** — the concept is here; icons (6.5) and token discipline are the gap. The job is to not lose it while building.

### D2 · Functional Completeness — "every control does something real"
**10 looks like:** Every button, tab, search, filter, and action has a real causal path. Zero dead controls. If a capability is unavailable, the control honestly shows it.
**9.0:** All primary paths work; minor secondary actions pending only with honest states.
**Current: 3.9** — the controls exist; the causal paths don't yet.

### D3 · Intelligence — "it actually thinks with NayaPOWER"
**10 looks like:** The Hub retrieves real intelligence from the canonical substrate. Search returns real results with provenance. "Your Intelligence Today" answers from real data. Smart Note capture flows through the real pipeline. Relevance improves with use. It feels alive because it IS connected to something alive.
**9.0:** Core retrieval + capture paths live; learning loop demonstrably improving.
**Current: 2.7** — the nine-node kernel took its first breath; the Hub is not yet connected to it.

### D4 · Honesty — "it never lies about what it knows"
**10 looks like:** Every state is truthful. Loading means loading. Empty means empty. Unverified is marked unverified. No sample data, no fake mailboxes, no animated "activity" that isn't real.
**9.0:** All states honest; no known fake-data paths.
**Current: 7.0** — the concept already marks NOT VERIFIED honestly; the risk is future builders faking liveness.

### D5 · Performance — "it feels instant"
**10 looks like:** First paint fast, interactions at 60fps, search responsive. The 843KB concept becomes a properly code-split app.
**9.0:** All core interactions smooth on a mid-range device.
**Current: 5.0** — single 843KB file, 27 script tags, 11 MutationObservers; unmeasured.

### D6 · Reliability & Continuity — "it remembers"
**10 looks like:** Sessions survive. Intelligence persists. Close it, come back tomorrow — state, lists, learning are there. Errors readable and recoverable, never silent.
**9.0:** Persistence proven on the production path; graceful degradation everywhere.
**Current: 6.0** — persistence proven on disposable DB; production path (PR #1243) awaits Shawn's merge.

### D7 · Accessibility — "everyone can use it"
**10 looks like:** Full keyboard navigation, screen-reader semantics, visible focus, reduced-motion respected, contrast AA+. The elite aesthetic survives all of it.
**9.0:** No blocking a11y failures; continuous improvement tracked.
**Current: 4.0** — some ARIA/focus in the concept; never audited.

### D8 · Craft — "the last 10%"
**10 looks like:** Typography exact. Spacing rhythmic. Micro-interactions considered. Mobile preserves identity. Empty states beautiful. Error states kind.
**9.0:** No craft defect visible in normal use.
**Current: 6.5** — strong bones; never given a unified craft pass.

**Current overall: ~5.6/10.** The path to 10 is D2, D3, D5, D7 — the application dimensions. D1 is near the bar; the entire game is preserving it while the rest climbs.

---

## 3. THE SCORECARD INSTRUMENT (MEASUREMENT LAW)

1. The builder self-scores with evidence links (screenshots, recordings, test output).
2. An **independent seat re-scores** from the evidence — builder self-score never closes a gate.
3. Disagreements are resolved by re-reading the artifact, not by debate.
4. The scorecard is re-run every phase. **Scores can go DOWN** — a regression is a finding, not a failure.
5. **Below 9.0 = not ready, no exceptions.** Target 10, happy with 9.5 (Shawn's standing bar).

---

## 4. THE PHASED BUILD PLAN

### Phase 0 · Hygiene (NOW)
- ✅ Rename completed on main: `HUB/hub.html` → `HUB/powercast-player.html` via merged PR #1273
- Fix `NAYANET INDENITY PAGE.html` filename typo (→ `NAYANET IDENTITY PAGE.html`)
- Snapshot the frozen baseline (visual reference capture per Design Contract)
- Resolve Smart Share → Smart Connect naming in the concept file

### Phase 1 · App Shell + Router
Componentize the baseline WITHOUT redesigning it: `NayaAppShell`, `NayaLeftRail`, `NayaTopBar`, `NayaSearch`, `NayaBoard`, `NayaIcon`, room router (`/feed`, `/today`, `/reports`, `/library`, `/connect`, `/ledger`, `/connections`, `/lists`, `/mail`, `/spaces`, `/settings`). Visual output must be indistinguishable from the baseline.
**Gate:** side-by-side visual diff passes.

### Phase 2 · Design Token System
Spectrum as real tokens (`--naya-purple` … `--naya-magenta`), room accent inheritance, button/board/icon grammar as shared components. Eliminate inline one-off styles.
**Gate:** zero emoji-as-icon in production paths; token coverage 100%.

### Phase 3 · Runtime Adapter
Hub → Runtime Adapter → Governed Runtime → Canonical Intelligence. The Hub never queries storage directly. Depends on PR #1243 (persistence) + nine-node kernel on main.
**Gate:** one real retrieval round-trip through the adapter with receipt.

### Phase 4 · Room-by-Room Activation
Each room gets real data + the honest state model (LOADING / EMPTY / READY / BLOCKED / NOT_VERIFIED / VERIFIED / ERROR). Rooms parallelize across builders. Each room scores D2+D4 independently before moving on.

**Smart Connect gets special attention — it is the "new internet" room.** One brain. Many doors:

| # | Door | Who connects |
|---|---|---|
| 1 | **MCP** | AI agents → NayaPOWER tools/context (priority 1) |
| 2 | **REST / OpenAPI** | Apps, agents |
| 3 | **GitHub App** | Coding/repository agents (works with our current GitHub setup + the app we create) |
| 4 | **Webhooks** | System → NayaPOWER events |
| 5 | **SDK** | Developers embed NayaPOWER |
| 6 | **A2A** | Agent ↔ agent collaboration |
| 7 | **Browser / Web Hub** | Humans — the Hub itself is a door |
| 8 | **Email / messaging adapters** | Human & network communication |
| 9 | **Enterprise identity** | Organization-level authorization (later) |
| 10 | **Private MCP tunnel** | Private / on-prem agents (specialized) |

**Door Law:** every door is its own themed, elevated object showing what it is, who it's for, live connection status, and the connect action with a real causal path — never a dead button. **Connection ≠ permission to act.** That distinction is architectural law.
**Gate per room:** every control has a causal path or an honest state; zero fake data.

### Phase 5 · Identity Rebuild
The bridge page: jewel identity emblem, obsidian board, live alias preview, privacy statement, fail-closed states, ENTER NAYANET → Hub. Flow contract: **welcome → identity → hub**. Remove the workers.dev redirect.
**Gate:** end-to-end flow works; identity page scores ≥9.0 on D1.

### Phase 6 · Intelligence Layer
Smart Note capture → real pipeline. Search → real substrate with provenance. "Your Intelligence Today" from real retrieval. Learning loop: relevance measurably improves.
**Gate:** D3 ≥ 9.0 with behavioral evidence (not just wiring).

### Phase 7 · Hardening
Accessibility audit + fixes. Performance pass (code-split, 60fps). Mobile responsive preserving identity. Error/empty/offline states crafted.
**Gate:** D5, D7, D8 ≥ 9.0.

### Phase 8 · The 10/10 Gate
Full scorecard, independent re-score, Shawn experiences it end-to-end: welcome → identity → hub → search → capture → ledger → close → return tomorrow → it remembers.
**Gate:** all eight dimensions ≥ 9.0, D1 = 10. Then we keep measuring — 10/10 is a floor, not a ceiling.

---

## 5. TEAM LANES

| Lane | Work | Needs |
|---|---|---|
| Shell + tokens (Phases 1–2) | Componentize baseline, token system | Design Contract; frozen baseline |
| Runtime adapter (Phase 3) | Hub↔substrate seam | PR #1243 merged; kernel on main |
| Room builders (Phase 4) | 11 rooms, parallelizable | Adapter; room contracts (Design Contract Part 4) |
| Identity (Phase 5) | Bridge page rebuild | Design Contract; flow contract |
| Intelligence (Phase 6) | Capture pipeline, search, learning | Nine-node kernel; Smart Note pipeline |
| **Scorecard keeper** | **Independent re-score every phase** | **Must NOT be the builder of the phase being scored** |

All lanes coordinate on issue #554. No lane rewrites another lane's in-flight work.

### Team Naya standing finding law

**ANY MATERIAL NOT-RIGHT FINDING → ISSUE #554 + EVIDENCE.**

Broken, stale, contradictory, misleading, unsafe, missing-proof, below-standard, architecturally divergent or regression-risk findings must not disappear inside one agent's context. Record the surface, evidence/truth state, remaining hole and highest-value next action. Posting is coordination, not execution authority.

 **All lanes are invited to bring a wiser, more powerful, more extraordinary approach to the table** — the spec is the floor, not the ceiling. If you can beat the concept's look, do it — but the scorecard decides, not taste.

---

## 6. LAWS THAT GOVERN ALL PHASES

1. **The baseline is the law.** Improve, never replace. (Design Contract §0.)
2. **No fake anything.** Honest states over simulated liveness. (D4.)
3. **Producer self-check ≠ qualification.** The scorecard keeper is independent.
4. **Scores can go down.** A regression found is progress.
5. **Smallest effective change.** Componentize the code; don't redesign the visual language.
6. **One shell, many rooms, one substrate.** No second brains, no second databases.
7. **When in doubt, preserve and ask.** Escalate with options + recommendation, not bare questions.

---

## 7. OPEN DECISIONS (SHAWN'S)

1. **Tech approach:** framework app vs disciplined vanilla componentization. Recommendation: framework/component architecture — the 843KB laboratory proves the current monolith does not self-organize at this scale.
2. **Merge/order and implementation ownership** for Phase 0/1 work should be reconciled against current live main before execution.

---

*Canonical v2 — reconciled 2026-10-01. This is the build law. The design contract is the visual law. Together they are how we get to 10/10 without going backward.*
