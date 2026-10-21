# The Smart Note Protocol — V1 (AI tongue)

Canonical procedure for creating a Smart Note that reaches the Intelligent Hub. Authoritative worked source: SN-0810. Ordered by Shawn Vibert 2026-10-21. If any other document's Smart Note procedure disagrees with this one, this one governs; file the conflict as a defect.

## Definitions
- Smart Note: the unit of living intelligence in NayaNET; a nine-section document (§Structure) filed in the brain, synced to Supabase, rendered in the Hub.
- Done: the note's own entry is verified present in the LIVE Hub feed bytes AND nayanet.live/s/sn#### returns HTTP 200. Any lesser state (written / committed / PR open / landing requested / on main unverified) is NOT done.

## Categorization (mandatory, no exceptions)
- The `<TOPIC>/<sub>` in the filing path MUST be a real entry of the brain's existing topic taxonomy, chosen at authoring for what the note truly is.
- The literal category `UNCATEGORIZED` (or any misc/dumping label) is a PROTOCOL VIOLATION: the note is not done even if synced and visible, and the author re-files it under a true category.
- If no existing subtopic fits, the author creates one deliberately (named for the note's true domain) and records the creation in the note's NAYA section. Inventing a vague bucket to avoid choosing is the same violation as UNCATEGORIZED.

## Identifiers and filing
- ID: SN-#### (sequence per claim scan; first claim stands; never reuse).
- File name: `IB-SMART-NOTE-YYYYMMDD-sn####-<slug>.md` (lowercase sn in the file name).
- Path: `BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<sub>/SN-####/<filename>`.
- Claim scan BEFORE writing: search (a) main tree, (b) open PR heads/staging trees, (c) the board tail for `SN-####` claims. A scan older than the claim is not a scan (registry-read lifetime rule).

## Viralize (authoring order + the one-minute block)
- Authoring order is fixed: (1) category, (2) topic headline, (3) ultimate hook — then the nine sections. The hook must simultaneously earn attention and summarize the note ("would a busy stranger stop for this line?" — rewrite until yes).
- The deliverable is an Intelligent Block with three first-class consumption paths: skim (nutshell + section headings carry the whole), listen (play, real cloned voice), full read. Target absorption ≈ 1 minute.
- Distillation standard: essence in the simplest, clearest, most concise words that keep the truth whole; cut any words that cost no truth. Presentation standard: elevated boards, big clear text.
- Feed surfacing is BY CATEGORY via Smart Tabs — never one undifferentiated stream. A note's category is therefore a display property, not just a filing property; a category-less note is homeless in the feed as well as the tree.

## Title law
The title is a crafted human hook: the greatest possible title carrying the lesson in one line. Generic labels ("notes on X", "update", the raw topic) violate the protocol. The title is set at authoring and is part of the note's MACHINE identity (feed card title).

## Structure — nine sections, exact headings, in order
`IN A NUTSHELL`, `HUMAN`, `CHILD`, `GRANDMA`, `NAYA`, `MACHINE`, `WHAT IT ALL MEANS`, `WHAT'S IN IT FOR YOU`, `HOW IT APPLIES`. The sync refuses notes lacking a Nutshell or Human section; author all nine regardless. MACHINE section = a parseable JSON object carrying at minimum the note id and its operative values/rules.

## The pipeline (Sender → Bridge → Receiver)
1. SENDER: the note file on GitHub `main`. **Main is the only door.** Local files, branches, and open PRs are invisible to every downstream stage.
2. BRIDGE: `naya-smart-notes-sync` (≈5-min cadence) scans main's tree, detects new/changed notes by blob SHA, parses, upserts to Supabase project `dahisasgpfvziswqvmvm`, table `hub_smart_notes`; mints share assets via the `naya-share` worker (routes nayanet.live/s/* and /share-img/*). Bake-on-publish: the note's narration is rendered in Naya's cloned voice during the sync so play serves the real voice from first click.
3. RECEIVER: if ≥1 note synced, the Hub rebakes + redeploys; the note renders as a card in the feed (`window.NayaFeedIntelligence.notes`, nayanet.live/#/hub) and at its own page.

## Landing doors (either satisfies the protocol; the author drives until landed)
- Door A — direct write to main via the App/bypass identity (standing approval covers the Smart Notes folder). The main-seat gh identity has NO bypass: its direct ref PATCH is ruleset-refused (422). Request the carry from the App-identity lane ON the board, naming the exact built commit + branch, and FOLLOW UP until the ref moves — an unanswered request is not a landing (SN-1771 escalation, 2026-10-21).
- Door B — dock-merged PR through the full scored process.
After a Door-A landing, close the record PR as superseded; never merge a stale registry regen from the record PR.

## Verification (authoring seat, mandatory, in order)
1. Contents API: the file exists at its exact path on main.
2. Live Hub bytes: fetch nayanet.live/ and confirm the note's OWN entry in the baked notes array (its IB id + title) — a textual mention inside another note does not count.
3. Own page: GET nayanet.live/s/sn#### = 200.
4. Voice (when checked): the player key for the note's normalized text resolves at the voice worker (cache-<sha256>.mp3); a miss = robot fallback = defect.
Only after 1–3: deliver to Shawn as the feed link + the note's own page link.

## Tracking (the intelligence ledger)
Every note MUST be countable in the Smart Ledger / data dashboard along these dimensions: total count; per category (TOPIC/sub); per author (human or seat); per day/week/month/year; filed-vs-visible delta (tree count vs live feed count — a nonzero delta is a defect list, each item named); voiced count (baked narration present). All stats are COMPUTED from the tree + the live feed at read time; hand-entered numbers are protocol violations. Category names have ONE canonical spelling (case-sensitive); variant spellings (e.g. `system` vs `SYSTEM`) are categorization defects to normalize, because they silently split the counts.

## Registry note
The `.naya/memory/smart-notes/index.json` registry is reconciled by its own cure lane; the Hub feed does NOT read it. Registry lag never blocks a note's Hub visibility and never excuses a missing landing.

## Failure modes (each observed; each preventable by the step named)
- PR-only note → invisible. Prevented by: landing driven + verified (§Verification).
- Landing request unanswered → invisible. Prevented by: author follow-up/escalation with verified-absence evidence.
- Lazy title → unread lesson. Prevented by: title law at authoring.
- Missing Nutshell/Human → sync refusal. Prevented by: nine-section completeness check before landing.
- Robot voice on play → bake skipped. Prevented by: bake-on-publish; treat any fallback as a defect.
- Number collision → scan first, first claim stands, colliding lane renumbers its own work.

## Roles
- Author (any Naya seat): end-to-end owner of their note.
- Bridge lane (Nitro): sync, share assets, rebake machinery, bake-on-publish.
- Shawn: any human may order a note with "smart note this"; delivery to him = the live links.
