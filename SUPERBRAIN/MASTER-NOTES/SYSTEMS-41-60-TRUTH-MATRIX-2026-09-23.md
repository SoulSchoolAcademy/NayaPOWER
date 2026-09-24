# Systems 41–60 — Truth & Dependency Matrix

**Owner:** NAYA 3 / CODA 3
**Baseline main:** `ad2d2ba466fe60a3443611fb18dead428a57d800`
**Rule:** IMPLEMENTED/EXISTS is not VERIFIED; BLOCKED is not PASS; UNKNOWN is not success.

| # | System | Current classification | Evidence / current substrate | Gap / proof needed | Dependency |
|---|---|---|---|---|---|
| 41 | Human Intelligence Dashboard | PARTIAL | `.naya/NAYAPOWER-INTELLIGENT-HUB-READ-FIRST.md`; Hub contract lists Your Intelligence Today, Report, Library; browser surface evidence exists | Prove the complete human intelligence summary: know/learned/changed/believe/verify/unknown/decisions/outcomes/recommendations/what Naya learned | 54, 57, 58, 59 |
| 42 | Human Recognition Layer | PARTIAL | Hub/intelligence architecture preserves source/person/project/context and contribution concepts; recognition is strongly documented | Prove human-visible recognition of created/discovered/experienced/learned/contributed/changed outcomes without exposing private data | 41, 43, 59 |
| 43 | Collective Intelligence | PARTIAL | Smart Share is a governed publication surface; Hub contract maps Smart Share → publishSmartFeed; existing publication/retrieval proof exists | Prove complete owner-consent → sharing policy → identity/privacy policy → collective projection → provenance/revocation lineage | 44, 57, 58 |
| 44 | Consent Revocation | PARTIAL | Revocation denial is proven in controlled policy evidence; authority/revocation machinery exists | Prove semantic effects across original, derived intelligence, summaries, caches/embeddings and downstream conclusions | 43, 45, 46 |
| 45 | Derived Intelligence | PARTIAL | Intelligent Block schema contains relationships/evidence references; derived intelligence is part of the canonical architecture | Prove dependency identity A+B+C → D and expose dependencies to revalidation | 46, 47 |
| 46 | Intelligence Invalidation | UNKNOWN/PARTIAL | Supersession/stale concepts exist in control plane and intelligence lifecycle | Need one executable dependency invalidation → recheck → recalculate → supersede proof | 45, 54 |
| 47 | Causal Model | PARTIAL | Controlled paired policy experiment proves observed outcome/benefit lineage; experiment infrastructure exists | Explicitly distinguish correlation/association/causal claim and prove one bounded causal-strengthening path | 45, 46, 56 |
| 48 | Capability Registry | PARTIAL | Smart Door architecture exists in PR #522 and Hub capability contracts enumerate governed capabilities | Need canonical machine-readable registry with authority/scope/risk/reversibility/receipt/verification contract and runtime discovery | 49 |
| 49 | Universal Smart Door | PARTIAL | Smart Door architecture is defined; Hub capability contracts already express governed action boundaries | Need one proven universal lifecycle DISCOVER → REQUEST → AUTHORIZE → EXECUTE → RECEIVE → VERIFY → PERSIST → INDEX → LEARN | 48, 60 |
| 50 | Distributed Naya | PARTIAL/FUTURE | Provider-independence and one-network governance principles exist | No evidence yet of multi-surface/node continuity preserving identity, authority, memory, provenance and governance across real distributed execution | 48, 49, 55 |
| 51 | Backup / Disaster Recovery | PARTIAL | Rebuild/recovery are named in repository operating standard and 10-star plan | Need actual EXPORT → RESTORE → VERIFY → REPLAY/REBUILD → LIVE CONTINUATION evidence | 52 |
| 52 | Rebuildability | PARTIAL | PIS builder and canonical event/control-plane architecture provide reconstruction machinery | Need bounded destructive/rebuild test proving derived indexes/projections/Hub views can be rebuilt from canonical events without using derived state as truth | 51, 54, 57 |
| 53 | Architectural Garbage Collection | MISSING/PARTIAL | Source map classifies canonical/active/derived/evidence/historical/archived; history-preservation rules exist | Need detection → classification → proposal → authorization → archive workflow; no silent deletion | 54 |
| 54 | Current-Truth Compiler | IMPLEMENTED — NOT VERIFIED | PR #563: generator, smoke test, CI workflow, contract doc; live HEAD is resolved at generation time | Workflow run 35952598828 passed smoke test, generation, artifact-shape validation, deterministic freshness check, and artifact upload; local run also reported live HEAD and STALE runtime parity without guessing. | 55 |
| 55 | Cold-Naya Benchmark | VERIFIED (bounded boot reconstruction) | Canonical boot chain and cold-Naya acceptance rules already exist | Workflow run 35952804157 passed smoke test, cold boot reconstruction, artifact validation, and upload. Machine benchmark proves 8 canonical reads, 0 conversation reads, one current next action, and explicit NOT_MEASURED boundaries for model reasoning/human task success. | 54, 60 |
| 56 | Human Task Benchmark | PARTIAL | 10-star plan defines representative human tasks and human usefulness as a core measure | Need executable task suite with real human outcomes and measurable success, not architecture claims | 41, 58, 60 |
| 57 | Hub as Projection | VERIFIED (source-architecture bounded) | Hub Read-First + visual/structural contract explicitly state one brain / many projections; canonical Hub path is protected | Need source→intelligence→projection→action proof showing Hub does not become a second store/brain | 41, 43, 45, 58 |
| 58 | One Experience / Multiple Surfaces | PARTIAL | Hub contract defines multiple surfaces and golden human journey; desktop/mobile evidence exists in prior proof lanes | Need release-blocking parity proof across desktop/mobile for OPEN → UNDERSTAND → NAVIGATE → SEARCH → CREATE → SAVE → SEE → RELOAD → FIND → VERIFY → ACT → LEARN → CONTINUE | 55, 56, 57 |
| 59 | Why Naya Explanation Layer | VERIFIED (implementation/build bounded) | Retrieval explanation is explicitly absent in Coda 1's 1–20 truth map; current Hub contracts describe evidence/provenance but not a verified explanation surface | Implemented `whyNaya.ts` and rendered WHY NAYA in SmartFeedBoard using recorded source/context/interpretation/meaning/action/verification/authority/uncertainty fields; workflow 35953146350 passed npm ci, TypeScript, and Vite production build. No chain-of-thought is exposed. | 11, 41, 57 |
| 60 | Ultimate NayaPOWER Loop | PARTIAL | Core loop is documented across constitution, control plane, learning/action/outcome proofs, and Hub contracts | Need one bounded end-to-end proof joining intent → understand → retrieve → truth → authority → value → decide → act → observe → verify → result → reconcile → intelligence → index → learn → successor | 54, 55, 57–59 |

## Dependency order

**54 → 55 → 57 → 59 → 41/42 → 43/44 → 45/46 → 47 → 48/49 → 51/52 → 53 → 56 → 58 → 60**

### Immediate execution rule

System 54 must be independently verified before System 55 is started. After 54 is green, 55 becomes the cold-Naya gate for the remaining 41–60 chain.

### Protected boundaries

- Do not touch Systems 1–20 or 21–40.
- Do not modify Hub visuals merely to satisfy 57/58.
- Do not bypass Cloudflare authorization.
- Do not alter the learning boundary merely to advance 41–60.
- Do not create a second intelligence store, capability layer, collective store, or Hub.

### Current first causal gap

**System 54 verification** is the only active 41–60 front until its generated artifact and workflow evidence are independently observed.

