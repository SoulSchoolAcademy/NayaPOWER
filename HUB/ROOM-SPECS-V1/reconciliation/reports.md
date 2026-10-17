# REPORTS Room — Independent Reconciliation (Naya 4 lane vs Naya 3 lane)

**Reviewer:** Naya 4 (independent execution lane) · **Date:** 2026-10-01
**A** = `reports/SPEC.md` + `reports/wireframe.html` (my lane, SPEC-FIRST)
**B** = `grounding/blueprints/03-your-reports.md` (Naya 3 lane blueprint, claims ROOM-BLUEPRINT-STANDARD-V1)
**Grounding cited:** `INTELLIGENCE-PROJECTION-CONTRACT-V1.md` (projection contract), `ROOM-FUNCTIONAL-CONTRACT-V1.md` (room contract), `1278-tokens.css` (tokens, visual law).

SHAWN'S LAW applied: "No blueprint, no building"; taste belongs at blueprint stage. No-Hub-Capture law checked against both sides. Neither spec silently violates it (see §1), with one wording risk noted in §2.

---

## 1. AGREEMENTS — locked identically on both sides

1. **No "Generate report" button / no Hub-side report authorship.** A field 1 + field 9 + predicate 6 + wireframe legend ("No 'Generate report' / no client-local synthesis anywhere"). B Controls + Do-not ("No Generate Report button", "do not author canonical reports client-side"). Both obey the No-Hub-Capture law (projection contract §3, §10).
2. **Projection-source data model.** A field 2–4: reports created upstream by the governed intelligence-report pipeline, mirrored via the projection/event adapter; the room owns nothing canonical. B Data: "Consumes canonical Daily/Weekly/Monthly/Yearly report artifacts." Both match projection contract §8 (automatic mirroring) and §0 (Hub = output, not input).
3. **Period distinction law.** A field 2 + predicate 1–2: DAY/WEEK/MONTH/YEAR are materially different experiences (verifiable by section headings; Weekly = story, not seven pasted dailies). B Distinction: "DAY, WEEK, MONTH, YEAR must differ in synthesis depth, not just date filter." Same rule, both sides.
4. **No fabricated fill for missing periods.** A EMPTY state: honest no-report panel + real explanation (predicate 9); R-STATE wireframe: "No fabricated reports to fill space." B Do-not: "do not fill missing periods with sample reports." Matches projection contract §11 (fixtures excluded from production paths) and A predicate 13.
5. **Compare mode exists.** A: "Compare periods" secondary button → R-CMP overlay with dual panes, period pickers ("Choose period A/B"), criteria line (Changed · Improved · Declined · Newly learned · Unresolved · Contradictory), "Close compare" footer. B: top-bar [Compare] + "compare mode" control. Same control, same behavior; placement adjacency differs only (§2, minor).
6. **Previous / Next period navigation.** A R-PERIOD: "Previous period" and "Next period" buttons. B Controls: "previous/next period." Agreed.
7. **Ask Naya present.** A: R-HDR + R-COVER (duplicated — see §2). B: listed under Controls. Agreed as an allowed projection-safe action (projection contract §3: Ask Naya may explain/compare/summarize; it is not a client-side intelligence store).
8. **Save / Add-to-List, Export, Share (governed only).** A field 5 allowed actions + predicate 7: Export rendered only where actually supported, Share only where governance authorizes — both absent otherwise, never disabled ghosts. B Controls: "save/list; export/share only where governed." Identical governance treatment.
9. **Freshness/truth honesty.** A: freshness + verification line ("verified · updated 2 h ago" / "not verified" / "runtime offline" — "always honest"); R-COVER verification badge; OFFLINE/ERROR banners with last-verified time (R-STATE, wireframe). B first-3-seconds: "confidence/freshness" visible on entry. Agreed on freshness visibility; wording differs ("confidence" vs verification — see §2).
10. **Evidence/source trail.** A: per-conclusion "Evidence" links → canonical objects (`IB-…`, events); R-APPX collapsible evidence appendix ("a conclusion with no evidence link is a spec violation"); predicate 3. B: [Evidence / source trail] composition block + "open source/evidence" control. Same commitment; A is the more testable specification.
11. **Cross-room identity preservation.** A field 8: handoffs to Library/Feed/Ledger/Connections/Mail/Space/List "by canonical ID"; predicate 8 ("identity matches character-for-character"). B Proof: "Opening a report from Feed and Reports resolves to the same report identity." Both satisfy room contract §4 and projection contract §4 (one object → many projections).
12. **Mobile = single reading column.** A Mobile: "Report cover → sections → evidence in a single reading column; ... R-CMP becomes stacked panes." B Mobile: "Single-column report narrative." Agreed.

---

## 2. CONTRADICTIONS — A says / B says / recommended resolution

**C1 — Report-type dimension: time-only vs six-type dropdown.**
- A says: R-PERIOD includes a "Report type" dropdown — Time-based (locked default) · Project / Space · Decision · Learning · Relationship · Thematic; field 3 canonical data includes those purpose types. A's own taste question asks whether all five ship in V1 or V1 locks to time-based.
- B says: "Consumes canonical Daily/Weekly/Monthly/Yearly report artifacts" — periodic only; no type dimension anywhere.
- Resolution: **V1 locks to time-based only.** Stronger grounding: the projection contract §1C names only DAILY/WEEKLY/MONTHLY/YEARLY as canonical report classes; A's purpose types appear in neither the projection contract nor B. A's own taste question #5 already concedes the point. Purpose types need upstream pipeline evidence before they enter V1 scope. [V1 = time-based only; purpose types return with pipeline evidence]

**C2 — Header composition: one bar vs two bands.**
- A says: R-HDR (title + report identity + freshness + Ask Naya + Compare) with R-PERIOD as a separate band below (segmented Day/Week/Month/Year + prev/next + type dropdown).
- B says: single top bar "[Your Reports] [ DAY | WEEK | MONTH | YEAR ] [Compare]" — selector and Compare grouped with the title.
- Resolution: **Keep A's two-band split.** Rationale: R-PERIOD also carries prev/next + (C1 aside) type controls, which is too much control weight for one header row; room contract §3 (overflow: low-frequency operations) favors the orientation band staying slim. Minor, non-blocking.

**C3 — "Confidence" vs verification vocabulary.**
- A says: freshness + verification line; VERIFIED / NOT VERIFIED truth badges; per-conclusion truth badges.
- B says: first-3-seconds lists "confidence/freshness" — "confidence" appears nowhere in the grounding.
- Resolution: **Drop "confidence."** Stronger grounding: the projection contract's receiver contract (§12) exposes `truth_state` (CANDIDATE | VERIFIED | …), and room contract §6 defines the VERIFIED / NOT_VERIFIED state model. "Confidence" is an invented metric with no canonical source. Use verification + freshness only. [NEEDS DIRECTOR TASTE only if a separate confidence number is actually desired as product — it would need an upstream source]

**C4 — Highlight-card strip: B-only composition element.**
- A says: R-COVER (featured report) → R-BODY sections directly; no card strip.
- B says: "[ Biggest changes ] [ Decisions ] [ Learning ] [ Open loops ]" — a highlight-card row between PERIOD THESIS and the story sections.
- Resolution: **Do not add B's strip as a separate row.** Rationale: it duplicates A's DAY body sections (Discoveries / Decisions / Learning — A's field 2 already locks those sections) and collides with B's own primary-instrument claim ("Time Synthesis Reader, not a grid of report cards"). Fold the four card contents into R-BODY DAY sections per A's period law. Neither side has director grounding for the strip; fold-in is the non-duplicative reading. Director may override.

**C5 — B's body composition is generic; A's period law forbids one template.**
- A says: body structure changes by period (DAY 8 sections; WEEK story sections; MONTH patterns; YEAR reflective), predicate 1 testable by section headings.
- B says: one fixed section list in desktop composition ("What changed / Why it matters / Patterns / Risks/opportunities / Carry-forward") — while its own Distinction clause demands periods differ "in synthesis depth, not just date filter."
- Resolution: **Adopt A's per-period bodies; B's generic list is withdrawn.** Stronger grounding: A's period law is explicit and testable (predicate 1–2); B's composition contradicts its own Distinction clause. B's fixed section list does not satisfy its own requirement.

**C6 — Naya synthesis panel vs no Naya layer in B.**
- A says: R-SYN "Naya's synthesis" panel with the locked marker "Naya's interpretation — not source truth" (predicate 11).
- B says: no synthesis panel; no Naya-behavior section at all (only "Ask Naya" under controls).
- Resolution: **Adopt A's R-SYN with the interpretation marker.** Stronger grounding: room contract §8 — "Naya must distinguish suggestion from fact"; room contract's five-layer law requires a NAYA layer in every room. B's omission is a gap against the room contract, not a legitimate alternative.

**C7 — Compare dimensions/criteria: specified vs absent.**
- A says: R-CMP shows explicit criteria per dimension (Changed · Improved · Declined · Newly learned · Unresolved · Contradictory); locked rule — no automatic "good/bad" judgment without declared criteria (predicate 5).
- B says: "compare mode" only; no dimensions, no criteria.
- Resolution: **Adopt A's R-CMP with criteria line.** Stronger grounding: A's field 6 (authority boundary: "no automatic 'good/bad' judgment without declared criteria") is a room-contract §7-quality requirement; silent compare invites unsupported judgment. B's compare is underspecified, not contradictory.

**C8 — Search-in-reports: authorized by A, placed by nobody.**
- A says: field 5 allowed actions include "search within reports" — but the visual blueprint (§b) places no search control, the wireframe shows none, and the component inventory has no search component. Internal inconsistency in A.
- B says: silent (composition shows [GLOBAL SEARCH] in the shell, not the room).
- Resolution: **[NEEDS DIRECTOR TASTE].** Grounding favors omission: room contract §3 — "Search/filter controls appear only where they materially reduce burden." A must either place the control (R-PERIOD adjacent, per wireframe revision) or remove the action from field 5. No side's grounding wins the placement decision; director calls it.

**C9 — "Open report" primary action semantics.**
- A says: R-COVER action row includes "Open report" (primary) which "scrolls to / expands R-BODY; on small screens opens the reading view."
- B says: silent.
- Resolution: **Define or remove.** Adversarial finding: the wireframe shows R-BODY rendered inline below the cover — if the body is always visible, a primary button that merely scrolls is a near-dead control (room contract §3: "No dead button"). If R-BODY starts collapsed, SPEC never says so. Recommended: either lock R-BODY collapsed-by-default with "Open report" expanding it, or demote the action. [NEEDS DIRECTOR TASTE on the reading-flow decision]

**C10 — "Ask Naya" appears twice in A.**
- A says: "Ask Naya" in R-HDR (secondary) AND in the R-COVER action row. B lists it once under controls.
- Resolution: **Keep one.** Rationale: room contract §3 calls for a small number of real primary/secondary actions; duplicating the same control in adjacent regions adds no capability and dilutes the action deck. Recommend R-HDR keeps it (persistent context action), R-COVER drops it. Reversible, non-blocking.

**C11 — EMPTY-state wording risks implying Hub generation.**
- A says: EMPTY panel reads "No report can be generated from the available verified intelligence yet."
- B says: silent; its Do-not only forbids filling gaps with samples.
- Resolution: **Reword to "No report has been produced yet from the available verified intelligence."** Rationale: "can be generated" in passive voice risks implying the Hub is the generator — the exact claim the No-Hub-Capture law forbids (projection contract §3). Upstream produces; the Hub projects. Small, non-blocking, recommended.

**C12 — Refresh / upstream re-request: permitted-but-undecided in A, silent in B.**
- A says: field 9 allows a runtime refresh that re-requests upstream projection if honestly labeled; the taste question says "I locked 'no refresh button' pending your call." (Internal tension: permitted-in-principle, absent-in-practice.)
- B says: silent.
- Resolution: **Director call per A's taste question** (see §4). Non-blocking: either resolution keeps projection law intact, because the locked wording forbids anything labeled as generation.

---

## 3. GAPS — present in one side, missing in the other

**B lacks (and A has):**
1. **First-3-seconds** — A implies it through R-HDR/R-COVER but has no explicit entry statement; B *has* this section. (Genuine asymmetry: B wins this one; A should add a 3-seconds line.)
2. **Truth states** — A has the full state table (field 7) + R-STATE treatments (LOADING/EMPTY/OFFLINE/ERROR). B has no truthful-states section at all, despite claiming the ROOM-BLUEPRINT-STANDARD-V1 (which requires one).
3. **Cross-room handoffs** — A field 8 (Library / Feed / Ledger / Connections / Mail / Space / List by canonical ID). B lists none beyond "open source/evidence."
4. **Naya behavior / synthesis layer** — A R-SYN + interpretation marker. B has no Naya-behavior section (standard requires it).
5. **Evidence appendix** — A R-APPX (collapsible, "a conclusion with no evidence link is a spec violation"). B's [Evidence/source trail] block has no appendix concept.
6. **Anti-patterns / forbidden substitutes** — A field 9 ("Forbidden local substitutes": no Generate/Refresh fabrication, no ornamental charts, no record-count reports, no unsupported causal conclusions, no seven-dailies-pasted-into-a-week). B's "Do not" covers only two items.
7. **Visual law / tokens** — A pins `--accent-reports` = `var(--indigo)` `#6675ff` (verified in `1278-tokens.css` lines 24, 41) and token-per-component notes. B is silent on visual law entirely.
8. **Acceptance predicates** — A has 13 numbered, mostly testable predicates + fixture exclusion (predicate 13). B has only a "Proof" line.
9. **URL routing** — A: `/reports/week/2026-W40` updates on period/type change; predicate 10–12 (back/forward, reload persistence). B silent.
10. **Generation provenance on the cover** — A R-COVER: "generated upstream · time · pipeline vX · N source objects"; predicate 4 ("the Hub never claims authorship"). B has no provenance requirement.
11. **Current Space context** — A R-HDR shows current Space (room contract §7: spatial/context law). B silent.

**A lacks (and B has):**
1. **Explicit first-3-seconds entry statement** — B's is crisp ("report period selector; latest report thesis; confidence/freshness; period summary"). A's R-HDR/R-COVER imply it but never state it. (B wins this section; A should adopt it minus "confidence" per C3.)
2. **Signature instrument naming** — B names "Time Synthesis Reader, not a grid of report cards." A names the metaphor (THE FILM ROOM) but not the instrument. (Naming only — not blocking.)

**Both lack:**
- **Accessibility section** — neither spec has one. The blueprint standard requires it; room contract quality gate #8 requires it. Must be authored before freeze.

---

## 4. TASTE QUESTIONS STILL OPEN — union, deduplicated

B contributes no explicit taste questions (its blueprint is compressed). All five come from A, plus one arising from C8:

1. [NEEDS DIRECTOR TASTE] **Runtime refresh:** "Check for updated report" button (honestly labeled upstream re-request) vs silent projection-event updates only? (A Q1; see C12)
2. [NEEDS DIRECTOR TASTE] **Truth-badge colors:** semantic color mapping for VERIFIED / NOT VERIFIED uninvented; should be one mapping across rooms — decide once. (A Q2)
3. [NEEDS DIRECTOR TASTE] **Compare depth:** period-vs-period only, or also report-vs-report within one period (e.g., Decision vs Weekly)? (A Q3)
4. [NEEDS DIRECTOR TASTE] **Charts:** explicit allow-list of chart types vs builder judgment under the "no ornamental charts" law? (A Q4)
5. [NEEDS DIRECTOR TASTE] **Thematic/custom report types:** ship all five purpose types in V1 or lock V1 to time-based only? (A Q5; note C1's grounding-based recommendation for time-based-only V1 — this question decides whether that recommendation holds)
6. [NEEDS DIRECTOR TASTE] **Search-in-reports:** place a room-level search control or defer to shell global search? (from C8)

---

## 5. FREEZE RECOMMENDATION — **NEEDS RESOLUTION**

Not ready to freeze. The blocking items, by name:

1. **Report-type dimension** (C1) — resolve V1 scope: time-based only vs five purpose types. (A's Q5; grounding leans time-based-only V1.)
2. **Highlight-card strip** (C4) — B-only element with no grounding; adopt fold-in or director overrides.
3. **Search-in-reports** (C8) — place the control or strike it from allowed actions; internal inconsistency in A today.
4. **"Open report" primary semantics** (C9) — define collapsed/expanded reading flow or remove the control.
5. **Runtime refresh** (C12 / taste Q1) — director's call on the re-request button.
6. **Accessibility section** — missing from both specs; required by the blueprint standard and room contract gate #8.

**Non-blocking (resolve inline, no director call):** C2 header split (keep A), C3 drop "confidence", C5 adopt A's per-period bodies, C6 adopt R-SYN + interpretation marker, C7 adopt A's criteria-line compare, C10 single Ask Naya (R-HDR), C11 EMPTY rewording, fold B's first-3-seconds statement into A, name A's signature instrument ("Time Synthesis Reader").

**Standing note:** both specs pass the No-Hub-Capture check — neither authorizes Hub-side report creation, local synthesis, manual upload, or a Generate/Refresh-fabricating control. The frozen spec must keep that lock intact.
