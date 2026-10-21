# MACHINE CONTRACT — COMPANION NOTES
## How to read and use GENERAL-DESIGN-CONTRACT.machine.json

*Companion to `GENERAL-DESIGN-CONTRACT.machine.json` (v1.0.0, 2026-10-21), which is generated from `GENERAL-DESIGN-CONTRACT.human.md`. The human version is the source of truth; this file explains the machine version, it does not amend it.*

---

## 1. What the machine version is

Every one of the 16 laws is carried as a structured rule: `id`, `name`, `statement`, `why`, `human_check`, `scope`, and `checks`. The `statement`, `why`, and `human_check` fields are **extracted verbatim** from the human contract's Rule / Why / Check text (markdown emphasis stripped, whitespace normalized) — `validate-machine-contract.py` re-derives them from the human file and fails if they differ, so the machine version cannot silently lose or paraphrase law. Law 2 additionally carries the SN-0808 canonical paragraph as `canonical_quote`, exactly as the human contract quotes it. The director-override rule (human §5) is carried at top level as `override_rule`. The spectrum, the five-piece `exemplar_map`, the severity vocabulary, and the `brief_schema` are data, not prose.

Drift is detectable: the JSON records the human file's sha256 and byte count. If the human contract changes, the hash check in the validator fails and the machine version must be regenerated (statements re-extract; the hand-authored `checks` re-reviewed against any changed wording) before a gate trusts it.

## 2. Machine-checked vs judgment

Of **52 checks, 43 are machine-testable and 9 are marked `judgment: true`**, each judgment check carrying the human criterion quoted as its `criterion` field. No judgment law was given a fake testable check.

**Machine-testable families:**
- **Computed-style assertions** — shadow-stack contents and direction (Laws 2, 3), border/glow presence at rest (Law 2), text color whitelist and opacity = 1 (Law 6), text sizes by role (Law 6), hero gloss-fall stops (Law 13), name-field counts (Law 9).
- **Named motion specs** — animation names, durations, easings read from CSS and piece records: the well's focus travel (2.8s), the button's breathe/sweep/lift/sink (4.2s / 5.5s / .28s / .08s), the select's open/chevron/press (.22s / .24s / .08s), the hero's sheen/breathe (5s / 5.6s), plus the reduced-motion lit-static rule (Law 4).
- **Document/DOM assertions** — spectrum adjacency in DOM order (Law 1), duplicate visible strings (Law 7), install once-at-bottom and no first-view interruption (Law 12), Smart Tabs presence (Law 14), scorecard record fields and the ≥ 9.5 ship threshold (Law 16).
- **Brief/gate assertions** — citation completeness against `brief_schema`, and every shipped element tracing to a canonical NAYA-* ID or a named harvest source (Laws 1, 10).
- **Behavioral tests** — the Function Law's click-everything test is a live harness test, not a style assertion (Law 11).

**Judgment-only (9 checks):** Law 1's color-as-identity read, Law 3's cover-the-labels drill, Law 4's wow test, Law 5's squint test, Law 8's per-line job test, Law 11's empty-state honesty, Law 13's inspector's-eye test, Law 15's fix-don't-report conduct test, Law 16's his-eye-supersedes clause. A gate records these as *reviewer attestation required*; it never auto-passes them.

## 3. How the gate consumes the JSON

**At brief time (dispatch gate):** parse the brief against `brief_schema` — `contract_id` and `contract_version` must match this contract, `exemplar_ids_cited` must be non-empty with every ID resolving in `CANONICAL-PIECE-INDEX.json` at status `canonical` with a reference role, and `harvest_sources` must name file + section (+ piece ID) for every element planned. Any miss → the brief does not dispatch. First verify the contract itself: recompute the human file's sha256 against `source.human_file_sha256`; on mismatch, stop — the contract drifted.

**At build review (ship gate):** run the testable checks against the rendered page (headless browser computed styles + DOM scans) and the piece records in `pieces.json`; each check's `trace` field says which source document its expected values come from, so a failure can be adjudicated against the scorecard or the human text. `blocker` failures stop the ship; `major` failures must be fixed before the work is presented as done. Judgment checks are surfaced to the reviewing designer as quoted criteria for attestation. The verdict is recorded in the deliverable's scorecard (Law 16), which the gate also validates for shape: three passes, gaps named, final score present.

## 4. What resisted faithful translation — named honestly

- **Law 8 (Text Earns Its Place) resisted entirely.** "Necessary or raises conversion" is an editorial judgment about each line; there is no mechanical proxy that is not a fake. Its single check is judgment-only, quoting the human check verbatim.
- **Law 13 (The Obsidian North Star)** — the law's core is a perception ("polished stone with light in it"). The machine checks assert its testable correlates (the harvested gloss-fall stops, the certificate palette discipline) and keep the inspector's-eye test as judgment. The correlates passing does not prove the law; the notes say so so nobody mistakes them for it.
- **Law 15 (The Inspector Rule)** is a conduct law. It governs the inspectors, not the page; no page property can express it. Its check is judgment over the work record (fix-then-report, verified), marked as such.
- **Law 5's squint test and Law 3's cover-the-labels drill** are human perception drills by design. The machine versions assert their structural correlates (own-color light present in every content area; shadow-direction classification per element role) and keep the drills as judgment checks beside them.
- **Law 4's wow test** is judgment by definition — a named reviewer finding nothing to add cannot be computed. It is carried as a blocker-severity judgment check so the gate still stops for it.
- **One value-level gap:** Law 2's well stack includes an "inner bottom light" layer. The exemplar scorecard names the layer but not its alpha (the factory CSS carries `inset 0 -2px 3px rgba(255,255,255,.10)`), so the machine check asserts the layer's *presence and kind* rather than inventing a threshold. Every other numeric value in the checks is asserted exactly as the scorecard or the human contract states it — the validator traces all of them (73 values traced, 0 untraced).
- **A representation note:** in the canon index a crowned piece carries its reference *role* as a string (`"reference": "Reference Well"`), while `pieces.json` carries boolean `reference: true`. The validator checks both forms so neither store can quietly lose a crown.

*Regeneration: statements/why/human_check are extracted from the human file by script; the `checks` arrays are hand-authored against the exemplar scorecard's values. On any human-contract change: re-extract, re-review checks, re-run `validate-machine-contract.py` until green.*
