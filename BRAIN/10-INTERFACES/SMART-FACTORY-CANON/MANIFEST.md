# STEP-0 FACTORY DELIVERY — Manifest

Assembled: 2026-10-21 · By: Nu (BUILD), Team Nitro
Purpose: the artifacts Resolve's Elite Parts Plan (2026-10-21) found unreachable from her lane — her STEP 0 names Nitro to commit these nine-artifact sources; this package is the local assembly of exactly those sources, byte-for-byte, so the landing route can be named against real files.
Assembly only: copies, no edits. No git operations were performed. The `backup/` subdirectory of the source contract folder was excluded per brief.

## Verification (from evidence, 2026-10-21)

- **Byte-identity:** sha256 computed on source and copy for all 21 artifacts — **21/21 MATCH**. Every copy below is byte-identical to its source.
- **pieces.json:** parses as JSON. 155 records, keyed by piece ID. All five crowned exemplar records are **present**, each carrying `reference: true`:
  - `NAYA-BTN-009` — "Hero · Enter the Standard" (fields: name, html, reference, motion)
  - `NAYA-BRD-001` — "Feature board" (fields: name, html, reference)
  - `NAYA-INP-008` — "Reference Well" (fields: name, html, reference, motion)
  - `NAYA-INP-009` — "Reference Select" (fields: name, html, reference, motion)
  - `NAYA-HRO-001` — "Reference Hero" (fields: name, html, reference, motion)
- **smart_factory_final-2.html:** `data-model` attributes counted in the file — **157 occurrences, 153 distinct piece IDs** referenced (the room audit's "153 data-model pieces" = the distinct count).
- **CANONICAL-PIECE-INDEX.json:** parses as JSON. Headline counts from its own records: **571 unique IDs in the union; 154 canonical; 1 superseded; 416 unverified.**

## Artifacts

Gap key — **§0 (B)**: §0 evidence base, the unreachable canonical index. **§0.1**: the unreachable INP-008 / INP-009 / HRO-001 exemplar sources. **(L)**: the absent live intake source. Contract files are listed under §0 (B) as the contract half of the same evidence base.

| File | Source path | Size (B) | sha256 | What it is / gap it closes |
|---|---|---:|---|---|
| CANONICAL-PIECE-INDEX.md | ~/workspace/smart-factory-contract/CANONICAL-PIECE-INDEX.md | 34310 | d5d31ef70dee0ba206aa26f11db1ae9f5c5b4509cc1290d3e103df399504f874 | The canonical piece index, human-readable: 571 IDs reconciled to 154 canonical / 1 superseded / 416 unverified. Closes **§0 (B)**. |
| CANONICAL-PIECE-INDEX.json | ~/workspace/smart-factory-contract/CANONICAL-PIECE-INDEX.json | 198488 | a56020be98b8bbb9c941b776179995d3c7e6c8eebed56f5e8f3e74cdb7a0ed8b | The same index in machine form — the distillation's working input. Closes **§0 (B)**. |
| GENERAL-DESIGN-CONTRACT.human.md | ~/workspace/smart-factory-contract/GENERAL-DESIGN-CONTRACT.human.md | 18295 | a818917c07f38e3f55d02a680bce0cf43110e52969d77ae60942f63cffbf4352 | The 16 design laws in human form — the standard every elite part is scored against. **§0 (B)** evidence base. |
| GENERAL-DESIGN-CONTRACT.machine.json | ~/workspace/smart-factory-contract/GENERAL-DESIGN-CONTRACT.machine.json | 50671 | e5f6ad08a0121824f3f4955afb3602ee60944390e3925a876e8fb95ae7b4abfa | The same contract in machine form — what builder gates check against. **§0 (B)** evidence base. |
| validate-machine-contract.py | ~/workspace/smart-factory-contract/validate-machine-contract.py | 9295 | 01ced3e69887e180911f3f6ea7173b27f67b1068a5dedf012a2a1f0821b5108e | The contract validator (last run: PASS, 86 traced / 0 untraced). **§0 (B)** evidence base. |
| MACHINE-CONTRACT-NOTES.md | ~/workspace/smart-factory-contract/MACHINE-CONTRACT-NOTES.md | 7003 | 86fbb6bf7d24fc0653102329999d5d76f100257416e57146a839cfa3574887c4 | Working notes behind the machine contract — decisions and rationale. **§0 (B)** evidence base. |
| EXEMPLAR-BUILD-SCORECARD.md | ~/workspace/smart-factory-contract/EXEMPLAR-BUILD-SCORECARD.md | 13288 | 5a6752efee950652aee12ad9ce5f1bc56e9c5042ca5d1495ce21c2c59982d0c3 | Scorecard for the exemplar builds (BTN-009, BRD-001, INP-008, INP-009, HRO-001) — how the crowns earned reference status. Closes **§0.1**. |
| INP008-REBASE-SCORECARD.md | ~/workspace/smart-factory-contract/INP008-REBASE-SCORECARD.md | 17346 | cc1426cc36c4e37901eb70e6456e95a8f91bbbabcbaa2ad796a2c5ef32e43ce4 | The INP-008 re-base record: the retired depth stack replaced by the factory recipe, with the LAW-02 wording tension flagged for Shawn's ruling. Closes **§0.1**. |
| EXEMPLAR-GAP-REPORT.md | ~/workspace/smart-factory-contract/EXEMPLAR-GAP-REPORT.md | 12983 | ff162b22135f27da19e3a3c0384806121db5f0672f0ffbf78c4be5c2466eee9a | The gap analysis behind the exemplar set — which classes lacked a crowned reference and why. Closes **§0.1**. |
| pieces.json | ~/workspace/personal-app/pieces.json | 60300 | 1e0186bb1aab664aa58337f30b313ad42dffe3b5303844c6179ce3c8866977c7 | The working store: 155 live piece records, including all five crowned exemplars (`reference: true`). Closes **§0.1**. |
| factory.css | ~/workspace/personal-app/factory.css | 171405 | e4542d31ad3ba3a5388a2231f2dafb242b92ab78f92e76363be3e25d5f037ea1 | The store's live CSS — carries the re-based `.ref-well-box` recipe (silver-white rim at rest, accent on focus). Closes **§0.1**. |
| smart_factory_final-2.html | ~/workspace/user/files/smart_factory_final-2.html | 454033 | 8912059628b63e07652f7d9bff0d75a29df5cc4ed4b45c01f015565549dd06b9 | The live Smart Factory intake page source — 157 `data-model` attributes, 153 distinct pieces. Closes **(L)**. |
| showcase/index.html | ~/workspace/smart-factory-contract/showcase/index.html | 6940 | 3578c6613cf0eaf83e375fc7c766db5d86a25aa0364c93fa0e57b690510007ab | The showcase page: all five crowned exemplars working in one place. Closes **§0.1**. |
| showcase/verify.mjs | ~/workspace/smart-factory-contract/showcase/verify.mjs | 7710 | 04f1f129e30337ed0d9252db3629ca6fd958c08d1b41e42fd66ee60a0db7a054 | Showcase verification script (part of the showcase directory, copied whole). |
| showcase/verify2.mjs | ~/workspace/smart-factory-contract/showcase/verify2.mjs | 2575 | 40a28c836a21b0000767cbe9d9bfbf532178099c5eeae9411385b93fe5542a0a | Showcase verification script, second pass (copied whole with the directory). |
| showcase/probe.mjs | ~/workspace/smart-factory-contract/showcase/probe.mjs | 2491 | 51c84637d72493498123584ab24263c2fbd86d99de2457c02fa2ec136c9a4612 | Showcase probe script (copied whole with the directory). |
| showcase/shot-phone.mjs | ~/workspace/smart-factory-contract/showcase/shot-phone.mjs | 1660 | b1f16899566b009fe1a02148935c0b22278546e1e952671bd4742c6538743d33 | Showcase phone-screenshot script (copied whole with the directory). |
| showcase/verify-out.json | ~/workspace/smart-factory-contract/showcase/verify-out.json | 1316 | fa86abafa1fe2f88c823668a779e3ba37d1970241c3aaf5f238082889379813f | Recorded output of the showcase verification run (copied whole with the directory). |
| showcase/shot-desktop.png | ~/workspace/smart-factory-contract/showcase/shot-desktop.png | 431836 | d1c9cc15f74b77746a1562c5e118c5b368f140119ea6f9f7d23be634a0cada02 | Showcase screenshot, desktop (copied whole with the directory). |
| showcase/shot-phone.png | ~/workspace/smart-factory-contract/showcase/shot-phone.png | 907897 | 55b7e079f7ecfe213d5f2e4bddcd0f44aee1e45fcaf67dd9bc4df41aae92fddf | Showcase screenshot, phone (copied whole with the directory). |
| showcase/shot-select-open-desktop.png | ~/workspace/smart-factory-contract/showcase/shot-select-open-desktop.png | 449196 | 46a6e0bb358585b636c82ce6903eadfda04fbd34c0b14472ab15aef989fa2299 | Showcase screenshot, INP-009 select open, desktop (copied whole with the directory). |

**Totals:** 21 artifacts copied (+ this manifest = 22 files in the package). Artifact bytes: 2,859,038.

**Proposed repo home (proposed only — nothing created in any repo checkout; the landing route gets named with Resolve's lane):** `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/`
