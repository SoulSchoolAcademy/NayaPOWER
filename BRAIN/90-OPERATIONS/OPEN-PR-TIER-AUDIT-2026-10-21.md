# Open PR Tier Audit — provisional title/body triage

**Captured:** 2026-10-21; **observed main SHA:** `576b67aafd7f7eea2bf393c7f15f334fbca4950f`; **open PR results:** 50.

**Important limitation:** this is a first-pass classification from live PR titles and descriptions. Changed-file paths and per-head check runs were not retrieved for every PR in this pass, so these tiers are provisional and blocker states are deliberately NOT guessed. The tier gate must use the full changed-file set and highest-risk match. Before migration, re-run the audit against current live PR files, reviews, workflow runs, mergeability, and dependencies.

| Tier | Count |
|---|---:|
| A — high consequence | 33 |
| B — ordinary work | 12 |
| C — mechanical content | 5 |
| Total | 50 |

## Queue

| PR | Tier | Provisional reason | Title | Current blocker state |
|---:|:---:|---|---|---|
| [#2855](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2855) | A | security/authority | DESIGN: Standdown blast-radius redesign (API-STANDDOWN v2) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2841](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2841) | A | security/authority | [NAYA 5] Safety: fail-closed VERIFY verdicts (revives #1944) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2854](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2854) | B | ordinary code, docs, or bounded feature; path audit required | Naya4/smart notes 2026 09 30 | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2742](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2742) | B | ordinary code, docs, or bounded feature; path audit required | Design laws v2 — 3-pass scored 9+ for ratification | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2397](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2397) | B | ordinary code, docs, or bounded feature; path audit required | feat(dashboard): live Team Naya activity dashboard — markdown + machine JSON | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2831](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2831) | C | mechanical note/index/content candidate | fix(brain): register SN-0800/SN-0805/SN-0806/SN-0807/SN-0808 — cure the SN direct-push registry debt | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2850](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2850) | A | governance/law/ratification | 0025 — The Smart Note Protocol V1 (three tongues): the canonical Smart Note protocol | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2526](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2526) | B | ordinary code, docs, or bounded feature; path audit required | P0-F5: source-bound mission section — no silent 2000-char truncation | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2808](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2808) | A | governance/law/ratification | Protocol operationalization: machine spec, pins, and enforcement for the ratified protocol | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2816](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2816) | A | security/authority | fix(brain): preserve Windows long-path projection existence in drift audit | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2741](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2741) | B | ordinary code, docs, or bounded feature; path audit required | Canonical hex set — 3-pass scored 9.25/10 for stamp | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2851](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2851) | C | mechanical note/index/content candidate | SN-1772 — Opened Is Not Done: Land It, Close It, or Kill It | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2848](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2848) | C | mechanical note/index/content candidate | SN-1771 — Already Built: Pick Your Model, Drive Away in Minutes | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2746](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2746) | A | governance/law/ratification | docs: establish Smart Builder human contract | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2846](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2846) | B | ordinary code, docs, or bounded feature; path audit required | fix(activation): pin Operating Code V2 LF in Windows checkouts (reland of #2732) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2754](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2754) | A | workflow/CI/deploy | Hub↔Supabase persistence bridge (Smart Note flow leg 3) — t0800 | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2842](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2842) | A | governance/law/ratification | boot-pointer fix: indirect live-board references in BRAIN/00-ACTIVATION (distill-daily-20261021) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2835](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2835) | A | governance/law/ratification | Clean home R1: remove the 10 byte-proven duplicate files (Shawn-approved) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2834](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2834) | A | governance/law/ratification | fix(readiness): C3 classifier no longer cries wolf on a healthy gate | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2838](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2838) | A | security/authority | fix(feeds): land hub-feeds-emit via deploy key with scoped ruleset bypass | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2836](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2836) | C | mechanical note/index/content candidate | cure(brain-index): regen index layer for SN-0808 landing (1-file drift at 895d7361) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2833](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2833) | C | mechanical note/index/content candidate | docs(brain): learning event 2026-10-20 | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2829](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2829) | B | ordinary code, docs, or bounded feature; path audit required | [W2 judge] L577 write-path guard: no score renders or writes without measured_at | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2830](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2830) | A | security/authority | fix(reporting): heuristic evidence never displaces authoritative score value/source (4th poison path) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2804](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2804) | A | workflow/CI/deploy | Mark IB-000042 SUPERSEDED by IB-000043 (Shawn ruling 2026-10-20) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2685](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2685) | A | workflow/CI/deploy | HUB/BLUEPRINT.ai.md — canonical team reference: the complete system map | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#1130](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1130) | A | governance/law/ratification | ratify(governance): Governance Contract V1 — awaiting Human Director decision | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2738](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2738) | A | security/authority | Hub deploy pipeline: GitHub → Cloudflare Workers | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2745](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2745) | B | ordinary code, docs, or bounded feature; path audit required | Visual Smart Contract v1 — the official machine contract for the smart builder (DRAFT, NOT RATIFIED) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2825](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2825) | A | security/authority | The GitHub webhook receiving door — nayanet-github-intake (verify + accept, fail-closed) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2824](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2824) | A | governance/law/ratification | governance(0032): THE HOUSE STANDARD — take care of the house | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2822](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2822) | A | governance/law/ratification | governance: 0031 NEVER AGAIN — The Reservoir Laws (Shawn, 2026-10-21) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2818](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2818) | A | governance/law/ratification | fix(know): make live Windows Smart Note bridge read all long-path notes | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2815](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2815) | A | workflow/CI/deploy | Viral Law — the headline standard (§22 of the Smart Note / IB Protocol) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2776](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2776) | A | security/authority | fix(smart-note): verify actual projection commit SHA | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2812](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2812) | A | governance/law/ratification | fix(activation): refuse undeclared cold starts at real admission gate | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2810](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2810) | A | security/authority | fix(protocol): reject false independent approvals (case, dismissal, comments) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2809](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2809) | A | governance/law/ratification | docs(activation): reconcile oath guide with ratified protocol and live board | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2803](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2803) | B | ordinary code, docs, or bounded feature; path audit required | [Team Verity] ops: THE NAYA TOOL DIRECTORY V1 — the catalog every Naya reads at activation | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2802](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2802) | A | security/authority | fix(protocol): tighten Honor activation, Hive venue and value truth boundaries | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2716](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2716) | B | ordinary code, docs, or bounded feature; path audit required | Composer v1 + gap closure (43->39 mapping, feed specimen) — item 15b | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2797](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2797) | A | governance/law/ratification | Governance: NAYA OATH OF HONOR (0023) — Shawn's 2026-10-20 law, three tongues | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2385](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2385) | A | workflow/CI/deploy | feat(ci): dedicated brain-index-freshness required gate workflow (Shawn 2026-10-11) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2739](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2739) | B | ordinary code, docs, or bounded feature; path audit required | Design library: canonical piece library on main (37 files, categorized, INDEX.md) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2747](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2747) | A | security/authority | feat: make Smart Builder library searchable and machine-accessible | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2736](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2736) | A | security/authority | fix(brain-index): make regeneration line-ending deterministic on every platform | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2589](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2589) | A | governance/law/ratification | Add decision CLI front door to value_calculus (tools/decision_cli.py) | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2735](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2735) | A | workflow/CI/deploy | Fix Living Map probes that mask latest failure or partial schema | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2680](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2680) | A | workflow/CI/deploy | t0483: hourly schedule pump for NayaNET Agent Capture | UNKNOWN — fetch current head checks/reviews/mergeability |
| [#2552](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2552) | B | ordinary code, docs, or bounded feature; path audit required | Intelligence intake triage: the hive's ingestion gate | UNKNOWN — fetch current head checks/reviews/mergeability |

## Audit completion required before settings migration

- Fetch changed paths and deletion counts for every open PR.
- Fetch exact head SHA, mergeability, review state, required check runs, and current failure annotations.
- Detect duplicate/superseded branches and dependency cycles.
- Reclassify any mixed-risk PR upward; only pure mechanical data/content may remain Tier C.
- Identify note filings that should be re-routed to the canonical Smart Note door instead of being merged as mega-PRs.
- Count blockers by cause: substantive test/spec failure, scorecard/seat shape, stale SHA, evidence section/link, conflict, permissions, dependency, or unknown.
- Do not change Required-check settings until the unified gate is independently verified and the shadow comparison proves no bypass.