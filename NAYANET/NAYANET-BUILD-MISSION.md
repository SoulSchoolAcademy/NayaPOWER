# 🔱☀️ NAYANET — DEFINITIVE BUILD MISSION

**STATUS:** CANONICAL TASK-LOCAL BUILD MISSION
**PRODUCT:** NayaNET
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**BRANCH:** `main`
**PARENT DIRECTIVE:** `.naya/NAYANET-10-RELEASE-EXECUTION-DIRECTIVE.md`
**MISSION:** Build, repair, verify, and release the actual NayaNET experience from repository truth.

> **This mission begins with archaeology, not invention.**

---

# 0. EXECUTION COMMAND

**NAYA: EXECUTE THIS MISSION END-TO-END.**

Opening sequence is mandatory:

**CURRENT-HEAD → RUNTIME/STATE → AUTHORITATIVE SOURCE → IMPLEMENTATION ARCHAEOLOGY → BASELINE → SOURCE-LOCK → PROTECT → BUILD → TEST → RUNTIME VERIFY → ASK WHY NOT 10 → REPAIR → VERIFY AGAIN → RELEASE-CERTIFY → DEPLOY → LIVE VERIFY → REPORT → LEAVE CONTINUITY**

Never substitute:

**PROMPT → DESIGN PROPOSAL → CODE → DONE**

Do not ask the human to answer questions that the repository can answer. Discover the answers first.

---

# 1. REPOSITORY-TRUTH ANSWERS

These are the answers established from the current repository archaeology. They are the starting facts for the mission, not assumptions to be silently replaced.

## 1. What is the actual current HEAD?

**Answer:** `facbc69fd2a4fe6f75fc272f9b476294951a747e`

The commit message is:

`Define airtight NayaNET Power Player Smart App Network build mission`

It is on the repository's canonical `main` branch.

The mission must re-check HEAD at execution time because HEAD may have advanced. If it has changed, the new HEAD becomes the execution baseline and the mission must repeat the archaeology against it.

---

## 2. What actually runs?

**Answer:** The canonical NayaNET implementation is the static-first application at:

`NAYANET/E02-INTELLIGENT-HUB-CLOUDFLARE/`

Its current runtime shell is:

- `index.html`
- `nayanet-10-experience.css`
- `nayanet-10.js`
- `naya-data.js`
- `powercasts.json`
- `_headers`
- `404.html`

`index.html` loads the canonical CSS and the `naya-data.js` + `nayanet-10.js` runtime. The page contains the Front Door, Intelligent Hub, Living Sun/Naya, Power Player, world map/cards, story/cast grid, world destination view, persistent mini-player, toast/status surface, and native `<audio>` element. fileciteturn357file0L2-L5

The Cloudflare build workflow validates this exact shell, validates the 18-Powercast registry, syntax-checks the runtime, verifies canonical assets/headers, and packages the seven runtime files into the standalone Cloudflare artifact. fileciteturn364file0L2-L2

**Execution rule:** verify the current runtime references at the actual HEAD before modifying anything.

---

## 3. What is the real runtime/state model?

**Answer:** The current E02 runtime is browser-native, static-first JavaScript with a single-page experience controller and HTML/CSS presentation. It uses the native browser `<audio>` element for media.

The current runtime keeps:

- selected Powercast index in `localStorage` under `nayanet_cast`;
- user name under `nayanetName` and `nayanet_name`;
- intelligence/challenge/notes/spaces state under `nayanet:intelligence:v1`;
- a `lastSeen` timestamp in that local state object;
- in-memory playback state such as `playing`.

The runtime initializes state from browser storage and writes state back through its `save()` path. The current code therefore establishes **browser-local continuity**, not proof of authenticated cloud persistence. fileciteturn360file0L2-L2

The engineering blueprint confirms that the product is intentionally static-first and says baseline presentation/interactions must not require Node, Wrangler, SSR, API availability, or database availability. It also says local persistence is appropriate only for permitted non-sensitive temporary state and that future APIs should sit behind a provider-neutral client abstraction. fileciteturn368file0L2-L2

**Truth boundary:** do not describe browser-local storage as private account persistence, Supabase persistence, or network intelligence unless actual authenticated/backend evidence proves it.

---

## 4. Which Power Player implementation is authoritative?

**Answer:** The authoritative current implementation is the Power Player inside:

`NAYANET/E02-INTELLIGENT-HUB-CLOUDFLARE/`

using the current `index.html` player surface and `nayanet-10.js` controller, together with the canonical Powercast data/configuration.

The current shell has a primary Power Player plus a persistent mini-player and native audio element. The controller's canonical Powercast registry contains 18 records with real artwork and audio identifiers. fileciteturn357file0L2-L5 fileciteturn360file0L2-L2

The repository's Media + Powercast Blueprint defines Powercast as a core Naya Power experience and requires explicit playback controls, progress, volume/mute, captions/transcript where available, responsive/mobile-safe behavior, keyboard controls where supported, and honest unavailable-media states. fileciteturn366file0L2-L2

**Rule:** no parallel replacement player unless archaeology proves the current implementation is not authoritative.

---

## 5. Which previous implementations matter?

**Answer:** The relevant implementation lineage is directly visible in the history of `nayanet-10.js`.

Most important recent ancestors include:

- `1583a7512ba7d8b02fa7068359d6504710fabfe0` — **NayaNET 10: replace patch runtime with single experience controller**;
- `c72d2a02b5ab005cec199a3153a7ff9ed9cc5370` — **Complete living portal runtime — real Powercasts, spatial worlds, responsive interaction and clean state flow**;
- `c5f8a24e7737a88bd0d9fa434621afbb1d722b51` — **NayaNET 10: add single coherent experience runtime with real interactions**.

These commits matter because they show the evolution from patch-oriented runtime work toward a single coherent controller and the explicit preservation of real Powercasts, spatial worlds, responsive interaction, and clean state flow. fileciteturn370file0L2-L2

Earlier NayaNET architecture remains important at the specification level: the master directive defines E01–E09 as the original construction sequence and explicitly says that sequence is a construction plan, not permission to invent the destination one block at a time. fileciteturn369file0L2-L2

**Archaeology rule:** preserve useful intent and solved problems from these ancestors; do not blindly resurrect their code.

---

## 6. What is live vs legacy?

**Answer:**

### Current/canonical

- `main` branch;
- current E02 static runtime;
- `nayanet-10.js` single experience controller;
- `index.html` canonical shell;
- `nayanet-10-experience.css`;
- `naya-data.js`;
- `powercasts.json`;
- current Cloudflare packaging workflow;
- canonical Vercel release workflow and governance contract.

### Legacy/history

Earlier patched runtimes represented by the ancestor commits are historical implementation lineage, not permission to run competing runtimes. The repository history itself records the move to a single experience controller. fileciteturn370file0L2-L2

### Deployment truth

The Cloudflare workflow is currently a **packaging/proof workflow**, not proof of a live deployment. It creates and verifies a standalone Cloudflare ZIP and uploads it as an Actions artifact. fileciteturn364file0L2-L2

The current canonical deployment governance explicitly says Vercel is the authorized deployment surface, while deployment defaults to DENY. It binds releases to the canonical Vercel project and requires explicit authorization, exact commit SHA, target environment, verification evidence, and approval. fileciteturn361file0L2-L2

**Rule:** committed is not deployed; packaged is not live; old URLs are not proof of current production.

---

## 7. What state is genuinely persistent?

**Answer:** In the current E02 implementation, the proven persistence mechanism is **browser `localStorage`**.

It currently persists at least:

- name/Smart ID input;
- selected Powercast;
- the `nayanet:intelligence:v1` object containing local notes/challenge/spaces state;
- a last-seen timestamp.

The runtime itself demonstrates these writes and reads. fileciteturn360file0L2-L2

This is **not proof of durable authenticated cloud persistence**.

The master architecture does envision an Intelligent Hub, personal Superbrain, Smart Notes, reports, account/security, and sovereign/private intelligence, but the build mission must distinguish specified architecture from implemented and verified capability. fileciteturn369file0L2-L2

The intelligence blueprint further establishes the canonical Note Event lifecycle and says provenance, permissions, and privacy classification must be preserved. fileciteturn367file0L2-L2

**Rule:** never claim cloud persistence, private account memory, or CIS continuity until backend/auth/database evidence proves it.

---

## 8. Which APIs/services are real?

**Answer:** The current E02 baseline is deliberately static-first and does not require an API/backend to render its baseline experience. The current Powercast runtime uses browser-native media and external Google Drive media URLs. fileciteturn360file0L2-L2

The repository architecture defines future/provider-neutral API seams for Naya, notes, reports, Superbrain, Collective Intelligence, and Network capabilities, but those interfaces must not be represented as live services merely because they are specified. fileciteturn368file0L2-L2

The current deployment control plane has a real authorized Vercel release workflow. That workflow checks the exact requested commit, runs repository governance verification, requires a Vercel credential, binds the canonical project, and deploys the exact verified commit. fileciteturn362file0L2-L2

The canonical Vercel project is:

- project name: `naya-power`;
- project ID: `prj_cHa9gwrtscCW8JuMDjcvw6DafaOK`;
- organization ID: `team_RQnhoOb3bAXxMlcr67GFTu3Q`.

fileciteturn361file0L2-L2

**External media is real configuration, not yet universal proof of successful playback.** Media must be runtime-tested.

---

## 9. Which visual behaviors were intentional?

**Answer:** The visual system is intentional and architectural, not decoration.

The current NayaNET shell intentionally implements:

- an **INTELLIGENT INTERNET BEGINS HERE** Front Door;
- NayaNET identity and tagline;
- Smart ID/name entry;
- five introductory doors;
- an Intelligent Hub rather than a conventional dashboard;
- Living Sun/Naya as the focal intelligence interface;
- orbit/energy geometry;
- nine worlds;
- Power Player as the central media heartbeat;
- a persistent mini-player;
- world destinations that preserve orientation;
- premium black/obsidian spatial composition.

The master directive establishes the governing principle: **complexity belongs in the system; simplicity belongs with the human**, with Naya as the guide. fileciteturn369file0L2-L2

The current implementation visibly encodes the Front Door, Living Sun, worlds, player, and continuity-oriented return structure. fileciteturn357file0L2-L2

**Rule:** do not replace these with a generic dashboard, conventional SaaS cards, or meaningless animation. Improve the living system while preserving the intentional spatial language.

---

## 10. What previous fixes must not regress?

**Answer:** At minimum, protect the work represented by the recent runtime lineage:

- move from patch runtime to a single experience controller;
- real 18-Powercast registry and mappings;
- spatial nine-world experience;
- responsive interaction and clean state flow;
- canonical shell/assets;
- Smart ID/name continuity;
- local intelligence/notes/challenge state where currently implemented;
- persistent mini-player behavior;
- native media state handling;
- accessibility semantics and labels already present;
- static-first deployability;
- canonical deployment governance and fail-closed release rules.

The repository's Cloudflare workflow explicitly protects the canonical shell, rejects stale runtime asset references, requires exactly 18 Powercasts, syntax-checks JavaScript, and proves the packaged artifact contents. fileciteturn364file0L2-L2

The engineering blueprint also requires no giant framework for a simple block, browser-native media where practical, no assumed autoplay, graceful unavailable-media state, and a complete testing matrix. fileciteturn368file0L2-L2

**Law:** preserve what works; improve what matters; remove nothing without evidence.

---

## 11. What deployment target is actually intended?

**Answer:** The repository's **current canonical deployment governance says Vercel**.

Deployment is fail-closed by default. Vercel remains connected infrastructure, but publication requires an explicit release authorization contract and the canonical authorized release workflow. fileciteturn361file0L2-L2

The canonical release workflow is:

`.github/workflows/authorized-vercel-release.yml`

and it deploys the exact authorized commit to the canonical Vercel project. fileciteturn362file0L2-L2

The Cloudflare workflow remains a real **artifact-generation/proof path**, and the engineering blueprint says the static artifact must be compatible with Cloudflare static deployment when that is the chosen product, while distinguishing static upload from Worker deployment. fileciteturn364file0L2-L2 fileciteturn368file0L2-L2

Therefore:

**CURRENT GOVERNED RELEASE TARGET = VERCEL.**

**CLOUDFLARE = CURRENTLY VERIFIED AS A PACKAGING/ARTIFACT PATH, NOT THE GOVERNED PRODUCTION TARGET.**

If product authority later deliberately changes this, the deployment governance must be changed explicitly before release. Never silently bypass the governance.

---

## 12. What production evidence exists?

**Answer:** There is **repository/build evidence**, but the evidence available here does not establish current NayaNET production proof.

There is a successful GitHub Actions run for the newest build-mission commit, proving repository automation ran successfully for that commit. fileciteturn371file0L2-L2

There is also a real Cloudflare packaging workflow that creates, validates, hashes, and uploads a standalone release artifact. fileciteturn364file0L2-L2

There is a governed Vercel production mechanism, but the repository's authorization file is only a template until a specific release is explicitly authorized and evidence-backed. fileciteturn363file0L2-L2

Therefore the current production status must be classified:

**LIVE PRODUCTION: NOT YET PROVEN BY CURRENT EVIDENCE.**

**PRODUCTION-PROVEN: NO.**

The mission must not manufacture a live URL, deployment success, playback proof, or production claim.

---

# 2. BUILD TARGET

Now build the actual NayaNET experience described by the canonical repository authorities.

NayaNET is:

> **A living intelligent network where humans and AI connect, create, and grow together.**

Primary tagline:

> **Create. Connect. Grow with US.**

Supporting positioning:

> **Master AI and Be Your MAX!**

Core thesis:

> **The internet connected information. NayaNET connects intelligence.**

The human experience is:

**ARRIVE → IDENTIFY → ENTER → MEET NAYA → EXPLORE → CREATE → CONNECT → LEARN → CAPTURE → GROW → BECOME WISER**

The system may be sophisticated underneath.
The human experience must remain radically simple.

---

# 3. THE ACTUAL BUILD PRIORITIES

After baseline archaeology, rank and repair in this order:

1. broken primary journey;
2. false or fake capability;
3. broken real media;
4. state/continuity failures;
5. security/privacy failures;
6. accessibility failures;
7. mobile/responsive failures;
8. comprehension/cognitive-load failures;
9. weak Naya/Living Sun relationship;
10. weak Power Player experience;
11. weak Hub/world integration;
12. visual craft and emotional impact;
13. performance and micro-optimization.

Do not polish a broken capability.

---

# 4. NAYANET EXPERIENCE CONTRACT

The Front Door must immediately communicate:

**INTELLIGENT INTERNET BEGINS HERE**

**NayaNET**

**Create. Connect. Grow with US.**

The user should understand the first action without a manual.

The Hub must feel like:

**ONE LIVING ENVIRONMENT → MANY CAPABILITIES**

not a dashboard or collection of disconnected widgets.

Naya/Living Sun must communicate meaningful state.

The Power Player must be a heartbeat of the environment.

The nine worlds must have spatial meaning and preserve orientation.

Smart Notes, identity, continuity, intelligence, Challenge, MAXESS, Intelligent Spaces, and Network capabilities must be truthful about their actual implementation state.

---

# 5. POWER PLAYER CONTRACT

All 18 canonical Powercasts must remain intact.

The player must prove:

- artwork;
- metadata;
- media source;
- loading;
- play;
- pause;
- progress;
- seeking where supported;
- ended state;
- unavailable state;
- network/media error;
- retry;
- mobile controls;
- keyboard controls;
- continuity;
- Naya relationship.

The Media Blueprint explicitly defines Powercast as a learning interface and establishes the future intelligence chain:

**media → transcript → timestamp → insight → note → report → optional contribution**. fileciteturn366file0L2-L2

Do not turn this into a decorative waveform with fake playback.

---

# 6. INTELLIGENCE CONTRACT

The canonical intelligence primitive is the **Note Event**.

The system distinguishes:

- Human Note;
- Naya Note;
- Machine Note.

The lifecycle is:

**INPUT → NOTE EVENT → VALIDATE → CLASSIFY → CANONICAL STORE → INDEX/RETRIEVAL → CIS → SYNTHESIS → ACTION/REPORT/LEARNING**. fileciteturn367file0L2-L2

Personal intelligence may remain private.
Collective intelligence must be deliberately contributed.

Never publish private Note Events by default.

Never fabricate continuity.

---

# 7. STATE-TRUTH CONTRACT

Every major capability must be classified explicitly:

**CONCEPT / SPECIFIED / IMPLEMENTED / TESTED / VERIFIED / DEPLOYED / LIVE VERIFIED / HUMAN-VERIFIED / PRODUCTION-PROVEN / HUMAN REVIEW REQUIRED / BLOCKED / UNKNOWN**

Never collapse these states.

If a capability exists only in a blueprint, call it specified.

If it exists only in browser-local storage, call it local.

If an external media URL exists but playback was not tested, do not call it verified.

If a release artifact exists but the target was not deployed, do not call it deployed.

---

# 8. TEST MATRIX

Verify at minimum:

### Runtime
- clean load;
- first visit;
- returning visit;
- navigation;
- reload;
- browser back/forward where relevant;
- no runtime console errors;
- no broken asset references.

### Power Player
- all 18 records;
- artwork;
- audio;
- play/pause;
- progress;
- seeking;
- next/previous;
- mini-player;
- error/retry;
- persistence boundary.

### Hub
- Front Door;
- Smart ID;
- Living Sun;
- nine worlds;
- world entry/exit;
- Ask Naya surfaces;
- player integration.

### Intelligence
- Smart Note creation;
- local state boundary;
- challenge state;
- context continuity;
- truthful failure when backend capability is absent.

### Responsive
- 320px;
- 375px;
- 430px;
- tablet;
- desktop;
- wide desktop;
- iframe/Groove dimensions where applicable.

### Accessibility
- keyboard;
- focus;
- labels;
- tab order;
- live regions;
- contrast;
- reduced motion;
- text scaling;
- non-pointer interaction;
- media alternatives.

### Failure states
- network failure;
- unavailable media;
- invalid state;
- persistence failure;
- unsupported browser media;
- slow loading;
- stale state;
- duplicate action;
- cancellation.

---

# 9. 10/10 MIRROR

After implementation, score the actual experience:

| Dimension | Weight |
|---|---:|
| Immediate understanding | 12% |
| Push-button simplicity | 12% |
| Interaction/state responsiveness | 12% |
| Visual excellence/craft | 11% |
| Power Player / real media | 10% |
| Hub/spatial architecture | 9% |
| Mobile/responsive | 9% |
| Emotional impact / wow | 8% |
| Accessibility | 6% |
| Performance/technical quality | 6% |
| Consistency/design system | 5% |

Ask:

> **Why is this not a 10?**

Then repair the answer.

Repeat until no machine-verifiable deficiency remains and every subjective dimension that cannot be established by tooling is explicitly marked **HUMAN REVIEW REQUIRED**.

---

# 10. RELEASE LAW

A release is blocked by:

- broken primary journey;
- runtime/build failure;
- fake capability;
- material persistence/data failure;
- security/privacy failure;
- material accessibility failure;
- major mobile failure;
- critical media failure;
- contradictory deployment governance;
- unknown release target;
- artifact not tied to tested commit;
- missing required evidence;
- material regression.

Never send the human a release command because the code merely exists.

The release sequence is:

**BUILD → TEST → VERIFY → 10/10 REVIEW → REPAIR → VERIFY AGAIN → EXACT ARTIFACT → AUTHORIZATION → DEPLOY → LIVE VERIFY → RELEASE REPORT**

Only then may Naya provide the final release instruction.

---

# 11. FINAL BUILDER COMMAND

> **Naya, build NayaNET from truth.**
>
> Start at the actual current HEAD.
> Discover the actual runtime and state.
> Read the authoritative sources.
> Perform implementation archaeology.
> Establish the verified baseline.
> Protect everything that works.
> Do not invent what the repository already answers.
> Do not replace working systems because a new implementation is easier.
> Build the human experience, not a code demonstration.
>
> Make NayaNET calm on the surface and extraordinary underneath.
> Make the first action obvious.
> Make Naya feel present without becoming a gimmick.
> Make the Living Sun meaningful.
> Make the Power Player a heartbeat.
> Make the nine worlds feel like one intelligent environment.
> Make Smart Notes and continuity truthful and useful.
> Preserve sovereignty and consent.
> Make mobile and accessibility first-class.
> Use real content and real capabilities.
> Never fake a service, persistence layer, playback state, or deployment.
>
> Test the whole journey.
> Ask why it is not a 10.
> Repair what you find.
> Verify again.
> Resolve deployment truth through the canonical control plane.
> Tie every release artifact to an exact tested commit.
> Deploy only through authorized release mechanisms.
> Verify the actual target.
>
> **Do not declare victory because code was written.**
>
> **Execute. Verify. Prove. Release. Leave continuity.**
