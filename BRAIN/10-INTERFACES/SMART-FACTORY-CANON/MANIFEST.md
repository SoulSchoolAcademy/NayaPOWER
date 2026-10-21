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
| validate-machine-contract.py | ~/workspace/smart-factory-contract/validate-machine-contract.py | 9257 | b87e74c3fe224f69899f11bcfcc70ae151bd871ad62940b056a45320d6c4e5f9 | The contract validator. **CURED 2026-10-21 (engine cure below):** line 43 previously read `~/workspace/personal-app/pieces.json` (author-machine absolute path — Resolve §6(b): clean checkout exited 1); it now resolves `pieces.json` relative to BASE, like every other input in the script. PASS re-proven from the package itself, incl. with HOME pointed at a nonexistent directory (86 traced / 0 untraced, exit 0). This row's hash is the cured in-package file; the workspace source still carries the hardcode. **§0 (B)** evidence base. |
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

**Totals (Step-0a):** 21 artifacts copied (+ this manifest = 22 files in the package). Artifact bytes: 2,859,038.

**Proposed repo home (proposed only — nothing created in any repo checkout; the landing route gets named with Resolve's lane):** `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/`

---

## Step-0 ENGINE CURE — 2026-10-21 (PR #2849, second head)

By: Nu (BUILD), Team Nitro — DOER stage of the relay, answering Resolve's scorecard on the first head (7.0/10 NOT APPROVED: contents integrity 9.8, Step-0 coverage **2/9** — the canon evidence half landed, the engine half did not). This section lands the 7 absent engine items under `engine/`, cures her §6(b) validator caveat, and maps the package onto the Factory Setup Map §6 nine-item list (her §7 item 5). Every copied file below is byte-identical to its source (sha256 computed on both, asserted equal at copy time). Two items have **no file source anywhere** — they were harvested from the live systems of record instead, and their rows say so plainly.

| File (in package) | Source | Size (B) | sha256 | What it is / item it closes |
|---|---|---:|---|---|
| engine/process-build-queue.py | ~/workspace/factory-pipeline/process-build-queue.py — the LIVE processor, post-R1-swap bytes (sha256 identical to the factory-r1 cured candidate; the pre-swap original is preserved at factory-pipeline/rollback-2026-10-21-r1-swap/) | 8891 | f71a7a5540bfd66a95eb5a5c274a052266aaa207755b495cd1c378b6c9c4900d | The queue processor that actually runs (cron, 2 min): selects the contract's chosen template via templates-registry.json, applies every contract field with an applied/not-applied ledger, deploys via deploy.py. **Item 1.** Honest note: the file's internal header + `PROCESSOR_TAG` still carry their pre-swap "R1 proposal — not the live file" wording — a stale self-description inside the live bytes, recorded here rather than edited (harvest is verbatim). |
| engine/customize_contract.py | ~/workspace/factory-pipeline/customize_contract.py | 8817 | f323f3fe443eb658a212172519d9e47a35959a6404bd37ff2cfe759b96670c24 | The customizer the queue processor actually imports (`from customize_contract import apply_contract`) — branding/pieces/functions applied per contract, every field ledgered. **Item 2 (the running customizer, under its true name).** |
| engine/customize.py | ~/workspace/factory-pipeline/customize.py | 2602 | d40b4d3b96ce790f7ef80d38fe3ebefee817df7d7aa2d8e5501126603047d910 | The LEGACY customizer — still present and still imported by build-api.py (below). Landed under its true name so the record is complete; see the two-door note. **Item 2 (legacy half).** |
| engine/build-api.py | ~/workspace/factory-pipeline/build-api.py | 3117 | 4db98b3e3b0ce2caa885d786088f44843970a35c62f7cc8c70a6badaecd56151 | The factory page's direct-build door. Evidence for the two-door truth: it imports the LEGACY `customize` and still hardcodes the personal base — the queue door is cured (R1), this door is not; its equivalent cure is the named R1b follow-up, NOT claimed here. |
| engine/deploy.py | ~/workspace/factory-pipeline/deploy.py | 7165 | b165fdef71bff28de04b6f68079d13a1c4a0cb31e538b869a27ba2c1709db080 | The deploy path for both build doors and the Hub: CSS brace gate, then a direct Cloudflare API PUT. The worker template is EMBEDDED in this file (`build_worker_js`) — **no wrangler configuration and no separate template file exist for this deploy path** (searched); claiming otherwise would be inventing one. **Item 3.** |
| engine/pwa-assets/hub/manifest.json | ~/workspace/factory-pipeline/pwa-assets/hub/manifest.json | 1317 | a70edc27e5b7484248db4baa4242a46a0e6ccbceeb8d852a24c898a2c08f540d | The exact manifest deploy.py's embedded PWA template reads at deploy time. **Item 3 (template inputs).** |
| engine/pwa-assets/hub/sw.js | ~/workspace/factory-pipeline/pwa-assets/hub/sw.js | 1454 | f1eef96d2b50e49e0497ec94300b0da28b6c986ab41c05282d247dd1f8dd2caf | The exact service worker deploy.py's embedded PWA template reads at deploy time. **Item 3 (template inputs).** |
| engine/templates-registry.json | ~/workspace/factory-pipeline/templates-registry.json | 7430 | 5a6c2cf66399dae5c6c2c5c69bce357ea8cdcda993f6f48e7f8569a917b70fb6 | The registry the cured processor selects template bases from: 12 templates pinned by md5. Its own `missing` map records honestly that **Today** and **Smart List** have no base file, no contracts.json entry, and no worker — not hidden, on the record. **Item 7 (selection half).** |
| engine/contracts.json | ~/workspace/factory-pipeline/contracts.json | 2135 | ea30ffd89e456a680bef5fae4d6e5dc2e4a978fe78ebb1dec8361bbfc58dbb26 | The intake's 12-template contract map. **Item 7.** |
| engine/templates/booking.html | ~/workspace/factory-pipeline/templates/booking.html | 229469 | d90caada52617868bf4d04b6b1e6f327a2ee5f82e2df2cdbd7c4ef0198c23fb7 | Template base file (one of the 12). **Item 7.** |
| engine/templates/business-hub.html | ~/workspace/factory-pipeline/templates/business-hub.html | 229479 | 5e525c6f0d7878266905262ef46e5eb76598b9e1d6f75941c97a433175ed8f9b | Template base file. **Item 7.** |
| engine/templates/business.html | ~/workspace/factory-pipeline/templates/business.html | 229489 | 63129efdb9ceee0709c151b0c1e7a8312e9553de84ddbd980362d603f6caa644 | Template base file. **Item 7.** |
| engine/templates/community.html | ~/workspace/factory-pipeline/templates/community.html | 229475 | a7e369003977ee67ef7c79678dd6259965248181248600dc25ac47ceaa01e917 | Template base file. **Item 7.** |
| engine/templates/dashboard.html | ~/workspace/factory-pipeline/templates/dashboard.html | 229476 | 204cce92e74505d3336ab36df003d08e6faa763fb8cd56ef5d099bb41d7e14cc | Template base file. **Item 7.** |
| engine/templates/event.html | ~/workspace/factory-pipeline/templates/event.html | 229481 | dd4a4696cba079786db2a67f5cd6a1d32d6ad7478c160ea9b601e073568e1006 | Template base file. **Item 7.** |
| engine/templates/menu.html | ~/workspace/factory-pipeline/templates/menu.html | 229476 | 57dd52cb917a363c09976d1d2ad1364a28fe58e0d34287e6a3dd47e27754e2df | Template base file. **Item 7.** |
| engine/templates/personal-hub.html | ~/workspace/factory-pipeline/templates/personal-hub.html | 229486 | 3f68280f553197e2c873bb12132dcdf72406710cb226d240587072fc9867eddb | Template base file. **Item 7.** |
| engine/templates/personal.html | ~/workspace/factory-pipeline/templates/personal.html | 229830 | fa3f90d46e00b4ff39b55dbe60eaf333c0b33189eebf0ff66876fc3a9a55c5c4 | Template base file (the personal template). **Item 7.** |
| engine/templates/portfolio.html | ~/workspace/factory-pipeline/templates/portfolio.html | 229486 | b1603f04b85295bd91544a5d4638b2412468a0e1c5a36f3c73494365d76f8abc | Template base file. **Item 7.** |
| engine/templates/product.html | ~/workspace/factory-pipeline/templates/product.html | 229496 | 984629f6b1ed136c8e067a456a12d5a0821554de7b037331842a566ca73cd8b4 | Template base file. **Item 7.** |
| engine/templates/signup.html | ~/workspace/factory-pipeline/templates/signup.html | 229469 | 09d615c58bb34b1ed45883d437e0f3410bc1d524fe521772d870847b479ba460 | Template base file. **Item 7.** |
| engine/build_queue-schema.sql | LIVE DATABASE (Supabase project dahisasgpfvziswqvmvm) — information_schema + pg_constraint read via the Management API, 2026-10-21 | 1772 | 86d2b6016e4cb0bb34f25814a9fd9c5d4c43b8753924bafe176b22da359e3dc4 | The build_queue schema. **No migration/DDL file for this table exists in the repo or the pipeline (searched)** — the table was created outside any tracked migration. This is a live-schema snapshot with full provenance in its own header, not a migration that was run. **Item 6 (landed as snapshot — the honest form of what exists).** |
| engine/naya-supabase-proxy.worker.js | PRODUCTION — Cloudflare account b5e2a51b… worker script `naya-supabase-proxy`, retrieved via the Workers API, 2026-10-21 | 3272 | 9fc71ddaf8a24d0384cc24b65ff7e1a5c73317861b03fc8b3a0ab9e2b132e6aa | The proxy worker source (v3 — its own first line). **No local source file exists anywhere in the workspace (searched — only URL references in HTML)**; these are the deployed production bytes, extracted from the API's multipart response and syntax-checked (`node --check` clean). It embeds the Supabase ANON key (JWT role `anon` — the public client key the browser pages ship with). **Item 5 (landed from production — the only source that exists).** |
| engine/sync-smart-notes.py | ~/workspace/factory-pipeline/sync-smart-notes.py | 37549 | 3b3349aff73d5e9f849fd92696754956069e27aaa9563dca172c837e6ac12ae4 | The intake sync: scans main's git tree for Smart Notes → upserts Supabase `hub_smart_notes` → mints share assets (via generate-share-card.py) → enqueues voice at publish → rebakes + redeploys the Hub via deploy.py. **Item 9.** |
| engine/generate-share-card.py | ~/workspace/factory-pipeline/generate-share-card.py | 4557 | b05cc458f1bbd4b00865727a73117e547fa7fdf733b95f3498d42695f34a19cb | The share-card minter the sync invokes per note. **Item 9 (deploy-path companion).** |

**Cure totals:** 25 engine artifacts added (+2,844,190 B). Package totals now: **46 artifacts (+ this manifest = 47 files), 5,703,228 artifact bytes.**

## Coverage vs Factory Setup Map §6 — the nine-item list (Resolve §7.5)

| # | Step-0 item | State at first head | State at this head |
|---|---|---|---|
| 1 | `process-build-queue.py` (processor) | ABSENT | **LANDED** — engine/process-build-queue.py (live post-swap bytes) |
| 2 | `customize.py` | ABSENT | **LANDED, reconciled** — engine/customize_contract.py (what the queue processor runs) + engine/customize.py (legacy, still used by the build-api door) + engine/build-api.py (the door itself, as evidence) |
| 3 | `deploy.py` + worker-template/wrangler config | ABSENT | **LANDED** — engine/deploy.py; the worker template is embedded in it and no wrangler config exists for this path (recorded, not invented) + its PWA template inputs under engine/pwa-assets/hub/ |
| 4 | `smart_factory_final-2.html` (live intake source) | PRESENT ✓ | PRESENT ✓ (package root, Step-0a) |
| 5 | Proxy worker source (`naya-supabase-proxy`) | ABSENT | **LANDED from production** — engine/naya-supabase-proxy.worker.js (no local source exists; deployed bytes harvested via the Workers API) |
| 6 | `build_queue` schema as a migration | ABSENT | **LANDED as live-schema snapshot** — engine/build_queue-schema.sql (no migration file exists; schema read from the live DB, provenance in the file header) |
| 7 | All 12 template app files + `contracts.json` | ABSENT | **LANDED** — engine/templates/ (12 files) + engine/contracts.json + engine/templates-registry.json |
| 8 | Canonical piece index artifact | PRESENT ✓ | PRESENT ✓ (package root, Step-0a) |
| 9 | Intake sync/deploy scripts | ABSENT | **LANDED** — engine/sync-smart-notes.py + engine/generate-share-card.py (deploy leg = engine/deploy.py, item 3) |

**Coverage: 9/9 items landed** — items 5 and 6 in the only form that exists (production harvest / live-schema snapshot), stated on their rows and in their files, not dressed as file copies.
