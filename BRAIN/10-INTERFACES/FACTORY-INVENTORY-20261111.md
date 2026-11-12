# Factory inventory — categorized, with paths + grades

**Read stamp:** repo `SoulSchoolAcademy/NayaPOWER`, HEAD `2c4186582` (`Living Map state 2026-11-11T15:14Z`), fetched live from origin/main 2026-11-11 ~07:23 PST. Built by naya-power (decide-and-act) for PI item `14q-factory-push-wire-inventory`. Every count below is computed from the live tree and the live JSON files named — nothing typed from memory.

**Anchor rule:** `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.json` rules conflicts between inventories — its own rule: "THIS index is the canon. ... Conflicts between inventories resolve to this index, then to Shawn's word." The registry (`BRAIN/10-INTERFACES/PARTS-REGISTRY-V1.json`, v1.2, 2026-10-31) is the verified-source record. `interfaces/factory/pieces-inventory.json` (v2.0.0, 2026-10-20) is a dated working-store snapshot.

## Grade rule (stated, traceable per row — record + presence grades, NOT design AAA)

- **A** — usable now: canon status `canonical`, OR registry `source_status: verified` with its `source_repo_path` present at HEAD.
- **B** — verified source, present, but not canon-canonical (registry-only, or canon status `verified`).
- **C** — named in a registry but no file exists (e.g. templates listed under `missing`).
- **R** — canon status `retired` or `superseded`: listed for provenance, NOT usable.
- **U** — ungraded: the source record carries no status field (pieces-inventory.json rows carry model + name only).

These grades measure record status + tree presence. They do NOT claim a rendered design review: AAA (Aligned, Authenticated by a different seat live, Actionable) still needs a different-seat rendered check, and a cold generation run (T-Factory-2) has not been run from this inventory.

## §1. The six categories at a glance

| Category | Count (live) | Home in the repo |
|---|---|---|
| Pieces | 154 canonical of 571 union ids (retired 413, superseded 1, verified 3) | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.json` |
| Templates | 12 engine + 6 shelf + 1 flagship = 19 files; registry names 12, missing 2 | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/`, `.../templates/`, `interfaces/walk/flagship-template.html` |
| Elements | 48 registry rows (JWL 9, NAV 11, OVL 5, INP 8, MRK 7, ROW 4, HDR 3, HRO 1) | `BRAIN/10-INTERFACES/PARTS-REGISTRY-V1.json` |
| Icons | 26 registry rows (ICO) | `BRAIN/10-INTERFACES/PARTS-REGISTRY-V1.json` |
| Boards | 9 registry rows (BRD); 27 canon-canonical BRD | `BRAIN/10-INTERFACES/PARTS-REGISTRY-V1.json` |
| Buttons | 26 registry rows (BTN); 33 canon-canonical BTN | `BRAIN/10-INTERFACES/PARTS-REGISTRY-V1.json` |

Category mapping (this inventory's mapping, stated not assumed): the item's six words do not exist as literal directories. Pieces = the canon piece store. Templates = the engine template shelf + shelf + flagship template. Elements = registry categories other than BTN/ICO/BRD. Icons = ICO. Boards = BRD. Buttons = BTN.

## §2. Pieces — canon store

Canon: `CANONICAL-PIECE-INDEX`, v1.0.0, 2026-10-22. Counts: union 571; canonical 154; verified 3; retired 413; superseded 1.
Working store it describes: `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` (155 entries per the canon's own sources note).
Canonical by family: BRD 27, BTN 33, HDR 3, HRO 1, ICO 26, INP 8, JWL 21, MRK 7, NAV 11, ORB 8, OVL 5, ROW 4.

All 154 canonical pieces grade **A** (canon status canonical; canon file present at HEAD). Path for every canonical piece: `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.json` (row by model id) + working markup in `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json`.

Canonical models by family (grade A):

- **BRD** (27): NAYA-BRD-001, NAYA-BRD-012, NAYA-BRD-013, NAYA-BRD-015, NAYA-BRD-018, NAYA-BRD-019, NAYA-BRD-021, NAYA-BRD-022, NAYA-BRD-023, NAYA-BRD-024, NAYA-BRD-025, NAYA-BRD-026, NAYA-BRD-027, NAYA-BRD-028, NAYA-BRD-029, NAYA-BRD-030, NAYA-BRD-034, NAYA-BRD-035, NAYA-BRD-036, NAYA-BRD-037, NAYA-BRD-038, NAYA-BRD-039, NAYA-BRD-040, NAYA-BRD-041, NAYA-BRD-042, NAYA-BRD-043, NAYA-BRD-044
- **BTN** (33): NAYA-BTN-001, NAYA-BTN-002, NAYA-BTN-003, NAYA-BTN-004, NAYA-BTN-005, NAYA-BTN-006, NAYA-BTN-007, NAYA-BTN-008, NAYA-BTN-009, NAYA-BTN-010, NAYA-BTN-011, NAYA-BTN-012, NAYA-BTN-013, NAYA-BTN-014, NAYA-BTN-015, NAYA-BTN-016, NAYA-BTN-017, NAYA-BTN-018, NAYA-BTN-019, NAYA-BTN-020, NAYA-BTN-021, NAYA-BTN-022, NAYA-BTN-023, NAYA-BTN-024, NAYA-BTN-025, NAYA-BTN-026, NAYA-BTN-027, NAYA-BTN-028, NAYA-BTN-029, NAYA-BTN-030, NAYA-BTN-031, NAYA-BTN-032, NAYA-BTN-033
- **HDR** (3): NAYA-HDR-001, NAYA-HDR-002, NAYA-HDR-003
- **HRO** (1): NAYA-HRO-001
- **ICO** (26): NAYA-ICO-001, NAYA-ICO-002, NAYA-ICO-003, NAYA-ICO-004, NAYA-ICO-005, NAYA-ICO-006, NAYA-ICO-007, NAYA-ICO-008, NAYA-ICO-009, NAYA-ICO-010, NAYA-ICO-011, NAYA-ICO-012, NAYA-ICO-013, NAYA-ICO-014, NAYA-ICO-015, NAYA-ICO-016, NAYA-ICO-017, NAYA-ICO-018, NAYA-ICO-019, NAYA-ICO-020, NAYA-ICO-021, NAYA-ICO-022, NAYA-ICO-023, NAYA-ICO-024, NAYA-ICO-025, NAYA-ICO-026
- **INP** (8): NAYA-INP-002, NAYA-INP-003, NAYA-INP-004, NAYA-INP-005, NAYA-INP-006, NAYA-INP-007, NAYA-INP-008, NAYA-INP-009
- **JWL** (21): NAYA-JWL-001, NAYA-JWL-002, NAYA-JWL-003, NAYA-JWL-004, NAYA-JWL-005, NAYA-JWL-006, NAYA-JWL-007, NAYA-JWL-008, NAYA-JWL-009, NAYA-JWL-010, NAYA-JWL-011, NAYA-JWL-012, NAYA-JWL-013, NAYA-JWL-014, NAYA-JWL-015, NAYA-JWL-016, NAYA-JWL-017, NAYA-JWL-018, NAYA-JWL-019, NAYA-JWL-020, NAYA-JWL-021
- **MRK** (7): NAYA-MRK-001, NAYA-MRK-002, NAYA-MRK-003, NAYA-MRK-004, NAYA-MRK-005, NAYA-MRK-006, NAYA-MRK-007
- **NAV** (11): NAYA-NAV-001, NAYA-NAV-002, NAYA-NAV-003, NAYA-NAV-004, NAYA-NAV-005, NAYA-NAV-006, NAYA-NAV-007, NAYA-NAV-008, NAYA-NAV-009, NAYA-NAV-010, NAYA-NAV-011
- **ORB** (8): NAYA-ORB-001, NAYA-ORB-002, NAYA-ORB-003, NAYA-ORB-004, NAYA-ORB-005, NAYA-ORB-006, NAYA-ORB-007, NAYA-ORB-008
- **OVL** (5): NAYA-OVL-001, NAYA-OVL-002, NAYA-OVL-003, NAYA-OVL-004, NAYA-OVL-005
- **ROW** (4): NAYA-ROW-001, NAYA-ROW-002, NAYA-ROW-003, NAYA-ROW-004

Retired (413) and superseded (1) models are grade **R** — listed in the canon index for provenance, not usable. Full list: the canon index file itself.

## §3. Templates — 19 files

Registry: `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates-registry.json` (templates-registry-v1, built 2026-10-21). It names 12 templates; the 12 engine files match those 12 names exactly.

### Engine templates (12, grade A — file present + named in registry)

- `booking` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/booking.html`
- `business-hub` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/business-hub.html`
- `business` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/business.html`
- `community` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/community.html`
- `dashboard` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/dashboard.html`
- `event` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/event.html`
- `menu` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/menu.html`
- `personal-hub` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/personal-hub.html`
- `personal` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/personal.html`
- `portfolio` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/portfolio.html`
- `product` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/product.html`
- `signup` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/signup.html`

### Shelf templates (6, grade A — file present; NOT named in templates-registry.json)

- `business` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/templates/business.html`
- `dashboard` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/templates/dashboard.html`
- `hub` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/templates/hub.html`
- `membership` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/templates/membership.html`
- `personal` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/templates/personal.html`
- `space` — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/templates/space.html`

### Flagship template (1, grade A — file present, referenced by the walk)

- `flagship-template` — `interfaces/walk/flagship-template.html` (602,149B at Move 1; 602,684B at HEAD 2c4186582 — domain-move + nav fixes since)

### Missing templates (grade C — named, no file)

- `smart-list` — Intake template (templates2.py 'Smart List'). No contracts.json entry, no template worker, no base file exists.
- `today` — Intake template (templates2.py 'Today'). No contracts.json entry, no template worker, no base file exists.

## §4. Registry rows — elements, icons, boards, buttons (109 rows, all grade A)

Registry: `BRAIN/10-INTERFACES/PARTS-REGISTRY-V1.json`, v1.2, generated 2026-10-31T18:28:07Z. Counts: interface 109, functional 24, total 133. All 109 interface rows are canon-canonical (0 outside the canon) and all 6 distinct `source_repo_path` values are present at HEAD (0 missing). Functional parts: 24 (NAYA-FN-001..024) with action_binding/auth/data_contract — not interface pieces, listed here for completeness.

Source homes (all present at HEAD):

- `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json`
- `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html`
- `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html`
- `HUB/design-system/library/pages/Naya_Smart_Hub_Design.html`
- `HUB/design-system/library/showcase/Naya_Design_Elements_N2.html`
- `HUB/design-system/library/systems/Naya_Ultimate_Design_System_-_Naya_2.html`

### Buttons — 26 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-BTN-001 | 01 · Heroes — .living-btn — ◈ SEE IT WORKING | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-002 | 01 · Heroes — .living-btn — ✦ ENTER THE STANDARD | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-003 | 01 · Heroes — .living-btn — ＋ READ THE LAW | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-004 | 02 · Living System — .lv-btn | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-006 | 02 · Living System — .lv-btn — Blue | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-007 | 02 · Living System — .lv-btn — Coral | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-008 | 02 · Living System — .lv-btn — Disabled | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-009 | 02 · Living System — .lv-btn — Gold | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-010 | 02 · Living System — .lv-btn — Green | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-011 | 02 · Living System — .lv-btn — Indigo | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-012 | 02 · Living System — .lv-btn — Lime | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-013 | 02 · Living System — .lv-btn — Magenta | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-014 | 02 · Living System — .lv-btn — Purple | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-015 | 02 · Living System — .lv-btn — Teal | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-016 | 02 · Living System — .lv-btn — ◈ Purple Hero | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-017 | 02 · Living System — .lv-btn — ✦ Magenta Hero | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-018 | 02 · Living System — .lv-btn — ＋ Blue Hero | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-019 | 03 · Essential — .cx-btn — → CONTINUE | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-020 | 03 · Essential — .cx-btn — ◈ DETAILS | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-021 | 03 · Essential — .cx-btn — ＋ CREATE | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-022 | 04 · Naya 5 proximity · black restored | `HUB/design-system/library/systems/Naya_Ultimate_Design_System_-_Naya_2.html` | A |
| NAYA-BTN-023 | 04 · Standard — .primo | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-028 | 05 · Orbit — .orbit-btn — ◈ Launch | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-029 | 05 · Orbit — .orbit-btn — ✦ Create | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-030 | 05 · Orbit — .orbit-btn — ＋ Begin | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |
| NAYA-BTN-031 | 06 · Icon Buttons — .icon-btn —  | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` | A |

### Icons — 26 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-ICO-001 | Today · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-002 | Spaces · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-003 | Reports · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-004 | Mail · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-005 | Ask · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-006 | Doors · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-007 | People · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-008 | Ledger · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-009 | Grow · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-010 | Guard · dual | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-011 | Home · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-012 | Pulse · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-013 | People · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-014 | Calendar · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-015 | Docs · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-016 | Vision · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-017 | Saved · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-018 | Explore · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-019 | Favorite · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-020 | Reports · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-021 | Love · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-022 | Share · dock | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-023 | Icon socket | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-024 | App Tile · Mail | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-025 | App Tile · Pulse | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ICO-026 | App Tile · Hearth | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

### Boards — 9 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-BRD-001 | Feature board | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-025 | Orbital five | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-030 | Feature circle | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-034 | Bar chart | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-035 | Donut chart | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-041 | Product card | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-042 | Pricing tiers | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-043 | Countdown | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-BRD-044 | Post composer | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

### Elements (JWL) — 9 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-JWL-001 | 01 · Orbs — finished objects of light | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-003 | 01 · Orbs — finished objects of light —  | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-006 | 01 · Orbs — finished objects of light — ▶ | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-007 | 01 · Orbs — finished objects of light — ◈ | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-008 | 01 · Orbs — finished objects of light — ✦ | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-009 | 03 · Gem Bullets — for lists —  | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-014 | APP ICON Glyph at the core | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-015 | APP ICON Love, luminous | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` | A |
| NAYA-JWL-016 | Beautiful at sixteen pixels. —  | `HUB/design-system/library/systems/Naya_Ultimate_Design_System_-_Naya_2.html` | A |

### Elements (NAV) — 11 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-NAV-001 | [hub-rail] 11-room rail nav | `HUB/design-system/library/pages/Naya_Smart_Hub_Design.html` | A |
| NAYA-NAV-002 | Design Contract v2.0 — AI Law § | `HUB/design-system/library/showcase/Naya_Design_Elements_N2.html` | A |
| NAYA-NAV-003 | Design Contract v2.0 — Human Law § | `HUB/design-system/library/showcase/Naya_Design_Elements_N2.html` | A |
| NAYA-NAV-004 | Design Contract v2.0 — Machine Law § | `HUB/design-system/library/showcase/Naya_Design_Elements_N2.html` | A |
| NAYA-NAV-005 | Design Contract v2.0 — Pre-ship ✓ | `HUB/design-system/library/showcase/Naya_Design_Elements_N2.html` | A |
| NAYA-NAV-006 | Design Contract v2.0 — Self-Scorecard ✓ | `HUB/design-system/library/showcase/Naya_Design_Elements_N2.html` | A |
| NAYA-NAV-007 | Design Contract v2.0 — Try it ◆ | `HUB/design-system/library/showcase/Naya_Design_Elements_N2.html` | A |
| NAYA-NAV-008 | Four laws create one unmistakable world. — 01 | `HUB/design-system/library/systems/Naya_Ultimate_Design_System_-_Naya_2.html` | A |
| NAYA-NAV-009 | Four laws create one unmistakable world. — 02 | `HUB/design-system/library/systems/Naya_Ultimate_Design_System_-_Naya_2.html` | A |
| NAYA-NAV-010 | Four laws create one unmistakable world. — 03 | `HUB/design-system/library/systems/Naya_Ultimate_Design_System_-_Naya_2.html` | A |
| NAYA-NAV-011 | Four laws create one unmistakable world. — 04 | `HUB/design-system/library/systems/Naya_Ultimate_Design_System_-_Naya_2.html` | A |

### Elements (OVL) — 5 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-OVL-001 | Toast system | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-OVL-002 | Mini modal | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-OVL-003 | Share sheet | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-OVL-004 | Command palette | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-OVL-005 | Notification drawer | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

### Elements (INP) — 8 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-INP-002 | Alias field | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-INP-003 | Segmented control | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-INP-004 | Toggle switch | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-INP-005 | Recessed field | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-INP-006 | Jeweled checkbox | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-INP-007 | Settings row | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-INP-008 | Reference Well | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-INP-009 | Reference Select | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

### Elements (MRK) — 7 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-MRK-001 | Status pill | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-MRK-002 | Done mark | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-MRK-003 | Search highlight | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-MRK-004 | Divider bar | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-MRK-005 | Spectrum bar | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-MRK-006 | Count badge | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-MRK-007 | Skeleton loading | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

### Elements (ROW) — 4 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-ROW-001 | Meta row | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ROW-002 | Action row | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ROW-003 | Menu item | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-ROW-004 | Method row | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

### Elements (HDR) — 3 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-HDR-001 | Eyebrow | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-HDR-002 | Intelligence trio | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |
| NAYA-HDR-003 | Step number | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

### Elements (HRO) — 1 rows

| Model | Name | Source path | Grade |
|---|---|---|---|
| NAYA-HRO-001 | Reference Hero | `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json` | A |

Canon-canonical models NOT in the registry (45 — usable, unregistered): NAYA-BRD-012, NAYA-BRD-013, NAYA-BRD-015, NAYA-BRD-018, NAYA-BRD-019, NAYA-BRD-021, NAYA-BRD-022, NAYA-BRD-023, NAYA-BRD-024, NAYA-BRD-026, NAYA-BRD-027, NAYA-BRD-028, NAYA-BRD-029, NAYA-BRD-036, NAYA-BRD-037, NAYA-BRD-038, NAYA-BRD-039, NAYA-BRD-040, NAYA-BTN-005, NAYA-BTN-024, NAYA-BTN-025, NAYA-BTN-026, NAYA-BTN-027, NAYA-BTN-032, NAYA-BTN-033, NAYA-JWL-002, NAYA-JWL-004, NAYA-JWL-005, NAYA-JWL-010, NAYA-JWL-011, NAYA-JWL-012, NAYA-JWL-013, NAYA-JWL-017, NAYA-JWL-018, NAYA-JWL-019, NAYA-JWL-020, NAYA-JWL-021, NAYA-ORB-001, NAYA-ORB-002, NAYA-ORB-003, NAYA-ORB-004, NAYA-ORB-005, NAYA-ORB-006, NAYA-ORB-007, NAYA-ORB-008

## §5. Pieces-inventory snapshot — 155 rows, grade U

`interfaces/factory/pieces-inventory.json`, v2.0.0, 2026-10-20, source: Verity's smart-builder-v50-fixed.html (distilled from 478-piece index). Rows carry model + name only — no status, no path, so grade **U** (ungraded) until cross-checked against the canon. Cross-check vs canon: 4 inventory models are NOT canon-canonical (NAYA-BRD-031, NAYA-BRD-032, NAYA-BRD-033, NAYA-INP-001); 3 canon-canonical models are NOT in the inventory (NAYA-HRO-001, NAYA-INP-008, NAYA-INP-009). The canon rules the conflict.
By family: BRD 30, BTN 33, HDR 3, ICO 26, INP 7, JWL 21, MRK 7, NAV 11, ORB 8, OVL 5, ROW 4.

## §6. Push (c1) — what is on main

- Move 1, commit `c6d7e5872` (2026-10-26 00:47 UTC, nayapower-lane-agent[bot]): interfaces + Smart Factory into GitHub, Hub-app scope, PR-gated, declared scope **34 entries**. Files touched: 65 paths (64 new + `interfaces/README.md` edit). All six destination dirs populated on main at HEAD 2c4186582.
- `interfaces/` at HEAD: 70 files: hub 2, walk 9, front-door 2, factory 19, pipeline 31, design 1, demo 3, pi-face 2, README 1.
- `interfaces/hub/sw.js`: present at HEAD, **1,865 bytes**, LIVE v2 (`naya-hub-shell-v2`, CURE 2026-10-25) — byte count matches the Move 1 commit message exactly. No registration line (Shawn's call, per README).
- Count note, stated plainly: the move declares 34 entries but its commit names 64 new files; no push-list file exists in the repo tree (tree-name search for `push` finds only Smart Note captures). The entry-to-file grouping is NOT in the record, so `34` as a file count is UNVERIFIED — what is verified is that every file of the declared Hub-app scope is present on main, in the six dirs, plus sw.js v2. The 2026-10-30 draft's `UNIDENTIFIED` verdict is superseded by the Move 1 commit stat, which names every file.

## §7. Factory wiring (c2) — audit, not a pass

Wired (repo-relative, verified this pass):

- `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/generate-factory-page.py` — 0 box paths; reads the canon store + index by repo path (`BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json`, `.../CANONICAL-PIECE-INDEX.json`).
- `interfaces/factory/` pieces + cure + generators are all present in the tree (see §6 counts). Registry source paths 6/6 present.

Box-bound (NOT wired — a cold builder on another box cannot run these as landed):

| File (repo path) | Line | Current value | Verified repo equivalent |
|---|---|---|---|
| `interfaces/factory/generators/build-one-system.py` | 24–26 | `HERE=/home/hatch/workspace/factory-models`, `PIPE=/home/hatch/workspace/factory-pipeline` | `CURE` → `interfaces/factory/generators/cure/` (exists); `PIPE/deploy.py` → `interfaces/pipeline/deploy/deploy.py` (exists); `HERE/src` → `interfaces/factory/pieces/` (inferred, NOT verified same bytes); `PIPE/templates` → no verified equivalent |
| `interfaces/factory/generators/build-one-system.py` | 614 | writes `/home/hatch/workspace/personal-app/personal-v5.html` | output path — must become a parameter, not a repo path |
| `interfaces/factory/generators/build-dashboard.py` | 25–26, 237 | same HERE/PIPE; loads `PIPE/templates-registry.json` | registry → `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates-registry.json` (exists) |
| `interfaces/factory/deploy-smartfactory.py` | 14 | reads `~/workspace/team-nitro/smart-builder/factory/Smart_factory_smarttabs.html` | no such file in the repo tree (tree-name search: none) |
| `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/build-api.py` | 38 | `template_path=/home/hatch/workspace/personal-app/personal-v5.html` | none verified |
| `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/deploy.py` | 73–74 | `PWA_ASSETS=/home/hatch/workspace/factory-pipeline/pwa-assets`, `ICON_DIR=/home/hatch/workspace/user/files/icons` | `pwa-assets` → `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/pwa-assets/` (exists, incl. `hub/sw.js`); icons dir → no verified equivalent |
| `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/process-build-queue.py` | 59 | `REPO_CLONE=~/workspace/nayapower-repo` | a clone path — correct only on a box with that layout |
| `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates-registry.json` | 945 | source `local: ~/workspace/personal-app/personal-v5.html` | none verified |

Repair packet (for the owner seat, Nitro — constants only, no redesign): repoint the input constants above to repo-relative paths derived from each file's own location, leave the generated-page output path as a parameter, and re-run the read phase cold from a fresh clone. The repoint for `HERE/src` and `PIPE/templates` must NOT be guessed — their box contents have no verified repo twin. Verdict on c2: NOT in place yet; the wired core (generate-factory-page.py) is proven, the interfaces/factory generators are not.

## §8. Factory as a standard door

Definition (14 Questions report §11/§14, 2026-10-25): `Factory as a standard door in the personal app. A citizen can find the Factory, and the Hub can work, without a hunt.`

What the repo proves today:

- The Factory picker exists: `interfaces/factory/factory-app.html` — `Smart Factory — pick your pieces`.
- The door is linked from the walk: `interfaces/walk/flagship-template.html` links `https://nayanet.app/#/hub/factory` (`Smart Factory`) and `https://nayanet.app/smartfactory` (`Connect in the Smart Factory`).
- No factory file exists under `PERSONAL/` or `nayanet-app/` in the repo tree (tree-name search: none) — the door reaches the Factory by link, not by a file in the personal app.

What is NOT proven here: a rendered check that a citizen opening the live personal app can find the Factory door without a hunt. That needs a live-browser walk (desktop + phone) at the real address — owed, delegated to the parent, never claimed from a file read.

## §9. Disagreements — labeled, not smoothed

- **478 vs 109/154:** registry v1.0 claimed 478 interface parts; v1.2 (2026-10-31) counts 109 after a purge under Shawn's ratified order. The 152-vs-478 question is NOT ruled; the ruling pack is Shawn's decision (registry notes). This inventory uses the live v1.2 + canon counts and does not re-argue the purge.
- **155 vs 154:** pieces-inventory.json lists 155 models; the canon counts 154 canonical. Diff: +4 / −3 (§5). Canon rules.
- **109 vs 154:** the registry covers 109 of 154 canon-canonical models; 45 canonical models are unregistered (§4).
- **Templates:** 2 registry-named templates have no file (`today`, `smart-list`, grade C); 6 shelf templates exist but are not in the registry.
- **34:** see §6 count note.

## §10. What this inventory does NOT prove

- No rendered check: nothing here claims a page renders, a button works, or the live Hub/Factory opens. Rendered proof is a different seat's browser walk.
- No cold generation: no page was generated from this inventory this pass. T-Factory-2 (non-Nitro cold build, phone + laptop) is still open.
- No live deploy: landing this file in the repo is a record landing, not a deploy to the address citizens use. The Hub service worker bytes in the repo are v2; whether the live address serves them is a live check, not a repo read.

---
Built 2026-11-11 ~07:45 PST by naya-power for PI item `14q-factory-push-wire-inventory` (priority 9400, owner naya-nitro). Head read: `2c4186582`. Receipt: this file at `BRAIN/10-INTERFACES/FACTORY-INVENTORY-20261111.md` on main.
