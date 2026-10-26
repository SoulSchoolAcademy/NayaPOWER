# DAILY INTELLIGENCE — 2026-10-26 (learning event)

**Filed:** 2026-10-26 ~03:37Z by the daily learning event (scheduled run, Naya Resolve seat) · **Main tip at filing:** `b4891b8ad4932aa64059b984b853837fddd0a3ef` (live ref via gh-api)
**Live board:** #3066 (successor to #2793, archived 2026-10-25; #2793/#2765/#2721/#2641/#2537/#2175 retired, #1354/#554 unpostable/archived).
**Sources:** `~/memory/2026-10-26.md` (643 lines at run start, plus the 2026-10-25 evening flush recorded in it), MEMORY.md standing entries dated 2026-10-26, board #3066 tail (162 comments; newest 6407452689, 2026-10-26T03:18:56Z), and merged PRs via gh-api: #3075 (02:24Z) and #3076–#3081 (03:01–03:03Z), plus direct commits for the Design Toolkit, SN-1869, and the brain-index regen cure `78d9c9d0`.
**The arc in one line:** Shawn reviewed the pages himself and turned the findings into law — show nothing that isn't done right, one page per job, fix the page that exists, score your work and land it yourselves — while the team's own audit falsified itself once, corrected itself in public, and learned that bytes prove a page exists but only eyes prove what it says.

---

## THE DAILY INTELLIGENCE (max 7)

### 1. THE SHOWING GATE IS LAW — done right, or not shown (Shawn ~00:20Z; SN-1869; L675)
- **What it is:** Before anything is shown to Shawn: (1) the approved/best work was studied first and its elements reused, (2) it is the most intelligent thing the seat could do, not the fastest, (3) it would stand as the only thing he sees of the work. A seat that cannot do a thing at standard routes it to the seat who can.
- **What it means:** Resolve's cover chooser (PR #3074) was rejected in full — flat, generic, invented instead of harvested — and closed by its own author the same hour; the redesign went to Nitro, the interface lead.
- **Why it matters:** It names the exact failure (excitement + speed shown as progress) and makes routing to the right seat the intelligent move, not an admission.
- **What's in it for me:** Every seat stops paying Shawn's attention for its homework; what he sees is finished, proven work.
- **How it connects:** It is the enforcement face of the Elevated Standard (2026-10-24) and produced the Naya Design Toolkit (`BRAIN/10-INTERFACES/`, landed at `1b0b584c`) the same night.
- **What changes tomorrow:** No interface face is authored outside its lane; any interface touched is cold-checked against the approved pages' actual elements before it is shown.

### 2. MERGE DOCTRINE CORRECTED BY THE DIRECTOR (Shawn ~03:18Z; board 6407452689)
- **What it is:** Shawn sweeps the PR queue himself (he cleared ~600 parked PRs to under 10); his click is trust, not a scorecard, and authorizes/proves nothing. Standing instruction: never put a PR forward that isn't right; scorecard it before; then agents merge their own scored work — the queue must never depend on his sweep.
- **What it means:** Breaches #46 (PR #3073), #47 (PR #3075) and #48–#53 (PRs #3076–#3081, merged 03:01:58–03:03:12Z with no scorecard on record) stand factually as "merged with no scorecard," but responsibility sits with the proposing seats who left unscored work merge-ready in his path — not with his click.
- **Why it matters:** The old "HOLD for scorecard" parking posture is retired: unscored work must not sit in a mergeable state at all.
- **What's in it for me:** A proposing seat owns its merge end-to-end; a clean queue is the team's job, not the director's chore.
- **How it connects:** Substance is still proven by scorecards + post-merge faithfulness (tonight's four reports/specs were byte-verified at tip); the T0 ruleset remains the mechanical cure in the production packet.
- **What changes tomorrow:** This report's own PR opens as a draft with its maker scorecard below, and does not become merge-ready until a different-seat scorecard at its exact head exists.

### 3. THE FOUR LAWS + ONE AREA — the director's page review (Shawn with Nitro ~01:00–01:50Z; filed in PI same pass)
- **What it is:** (1) Every order lands in Project Intelligence the same pass — chat alone doesn't count. (2) NO HOLDING — decide the most intelligent thing, build it, prove it, show it done. (3) ONE AREA — one page per job; related views live inside it behind buttons. (4) FIX THE PAGE THAT EXISTS — edit-only; a new page instead of a repair is the defect.
- **What it means:** Seven doubled pairs were named and filed as merges (all in_progress in PI): Intel Today, Growth, Connections, Mail (personal#inbox is garbage; /rooms/mail is the right one), Lists (overhaul to Shawn's Smart Lists definition), Reports (stats becomes a view inside the real library), Settings — plus Library overhaul, PI face World View, Smart Tabs (Business + Spaces apps were missing), Spaces directory format, Smart Factory templates, and FINAL FORMAT v1 for the dashboard/smart-app format.
- **Why it matters:** Doubling was the named waste: surfaces that look like something but are nothing burn time, money, and trust.
- **What's in it for me:** Citizens get one obvious place per job; seats get one record per job to fix, prove, and close.
- **How it connects:** The three-lead split carries it — Resolve: study/harvest briefs (PR #3078, seven Toolkit-format briefs) + rendered verification; Power: wiring; Nitro: craft + scorecards on the others' builds.
- **What changes tomorrow:** No page passes alone when a twin exists; fixes are edit-only diffs on the live page at nayanet.live/projects and its siblings, never replacements.

### 4. L676 — ABSENCE OF MATCH IS NOT ABSENCE OF FACT (audit correction, ~02:00Z; board 6406524772)
- **What it is:** Resolve's 32-page design audit (filed in PI 33/33, receipt 6405895588) claimed the flagship template had NO viewport meta; the bytes carry it single-quoted and the analyzer matched double quotes only. The claim was withdrawn in public, the flagship score revised 4→6, the whole set re-verified quote-agnostically, and the analyzer fixed.
- **What it means:** A mechanical audit is a floor, not a verdict; a regex is not a reading.
- **Why it matters:** The false claim had already spawned four fix items — the pre-build byte re-read caught the checker before a fix was built on it (WP-247).
- **What's in it for me:** Every absence verdict now names its match assumptions and is re-read format-agnostically against raw bytes before filing or acting.
- **How it connects:** The findings that survived re-verification stand and are queued: Today room genuinely has no viewport, the Mission room has no page at all, `/projects/questions.json` is a dead 404 still registry-listed, canonical flagship URLs render sample citizens, Life with Naya weighs 24,842KB.
- **What changes tomorrow:** Audit scores stay capped until rendered review; mechanical signals never file a fix alone again.

### 5. PR #3075 RETRO-SCORE 5.5/10 — A SECOND FACTORY AUTHORITY WAS THE REAL FINDING (board 6407042406)
- **What it is:** The evidence pack (65 files, all `interfaces/**`) falsified the PR's "404 unified pieces" claim: it contains 155 pieces, all pre-existing in canon (571 union declared), and it created `interfaces/factory/` parallel to the pre-existing `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/` — twin share-card generators, ~254KB of byte-identical internal duplication, four walk-server generations, three `sw.js` variants (v2 narrows the never-cache doctrine and must not be registered as-is).
- **What it means:** The merge's form breach (#47) is separate from its substance; on substance it is not a pass at the 9.0 bar.
- **Why it matters:** Two inventories for one factory is the duplicate-mechanism defect in its purest form — every later builder would have had to guess which authority is real.
- **What's in it for me:** One canonical home wins by prior existence; `factory-single-authority-reconcile-20261026` is filed in PI (Nitro owns, Resolve verifies byte-level), including carrying NAYA-BRD-031/032/033 into canon.
- **How it connects:** Same root as item 3's doubled pages — duplication is today's recurring defect, in pages and in factories alike.
- **What changes tomorrow:** New mechanisms are checked against canonical seams before they are built, not reconciled after they land.

### 6. BYTES PROVE IT EXISTS; EYES PROVE WHAT IT SAYS (flagship rendered cold-check, ~02:30–02:36Z)
- **What it is:** Rendered, guest-view checks of personal/business/space/dashboard + the Connections room: all render, but canonical URLs still wear sample citizens (Nova Reyes / Acme Corp / Our Community), no library cover is wired (gradient only), the dashboard shows NO points total with several integrations "NOT CONNECTED", and Connections carries two contradictory lines on one screen ("live on this device only — nothing is sent or synced" vs "saved in your NayaNET store"). Phone-width was untestable from the harness and was NOT claimed.
- **What it means:** The flagship's real gaps are birth/wiring gaps (page-birth mission, points layer), not template gaps — the opposite of what the mechanical audit first said.
- **Why it matters:** It is item 4's lesson from the other side: existence and even correctness of bytes say nothing about what a citizen actually sees.
- **What's in it for me:** Verification budgets go to rendered proof (phone + laptop, different seat scoring), which is now the acceptance shape for every page-audit item.
- **How it connects:** Shawn's own review set this standard — his audit was rendered, functional, and pair-hunting; the team's rises to match. Shawn's standing charge the same hour: when there is a lesson, Smart-Note it proactively, without being told.
- **What changes tomorrow:** Covers reconciled as the canonical count until the next dated re-count: 89 carded · 85 ready · 86 files on main.

### 7. NOT 10 YET — AND THE LOOP THAT GETS THERE WAS PROVEN (Ten-by-Ten convergence; kernel cure)
- **What it is:** Resolve's Ten-by-Ten (PR #3077) and Power's 10/10 report (PR #3076) converge independently: ~6.5/10, "No, not yet," same sequence, PI first. Power's measured census: 262 work_items (done 20 · in_progress 52 · queued 164 · verifying 19 · needs_shawn 6 · blocked 1 = 7.6% done), 203 of 262 uncategorized by area; Smart Match live tables empty; the ledger's 30 rows frozen since 2026-10-22. The same night, the kernel brain-index red was root-caused (BRAIN landings without regen), cured in one commit (`78d9c9d0`, 3 index files), and CI-verified green at that head.
- **What it means:** The distance to 10 is measured, categorized work — an area mapping filled once and maintained on insert — not unknown unknowns.
- **Why it matters:** Two seats reaching the same verdict from different evidence is the scorecard system working; the kernel cure is the loop (detect → root-cause → fix → CI verify) completing inside one hour.
- **What's in it for me:** The execution order is already filed as the top PI item (`ten-by-ten-execution-2026-10-26`, pri 10000); nobody needs to re-plan, only to execute and prove.
- **How it connects:** Items 1–6 are all instances of this loop succeeding or failing; the standing blockers it cannot move remain human-gated (behavioral proof, production stamp, 19 pending migrations).
- **What changes tomorrow:** Execution runs nonstop under the director's release; reporting is finished, proven things only.

---

## What compounded today
- **The Showing Gate changed a decision in the same pass it was named:** PR #3074 was closed by its author, the face rerouted to Nitro, the Design Toolkit landed, and the gate itself was Smart-Noted (SN-1869) and promoted to standing law (L675) — a lesson that changed routing, tooling, and law within one hour.
- **The pre-build byte re-read (WP-247)** stopped a false viewport fix from being built and triggered a whole-set re-verification, not a one-line patch.
- **The merge-doctrine correction** changed breach accounting (#46–#53) and the team's forward behavior in the same post that recorded it.

## What was let go
- **PR #3074** (Resolve's cover chooser) — closed, superseded by Nitro's `cover-library-interface-nitro` item.
- **PR #3072** (cover-library v1 branch) — closed unmerged; the library is whole on main via #3071/#3073 (no-duplicate-mechanisms).
- **The "HOLD for scorecard" parking posture** — retired by the corrected merge doctrine (item 2).
- **The flagship viewport claim and the "404 pieces" claim** — both falsified on live bytes and corrected in place (PR #3077 carries CORRECTIONS blocks in all three tongues).
- **Power's receipts on retired board #2793** — superseded as a venue; pointers mirrored to live board #3066 (6407019197). #2793 itself stays retired/archived.

## Trash candidates — FLAG ONLY (deletion is the Human Director's call; nothing deleted by this run)
1. `personal#inbox` — the doubled Mail page Shawn named "garbage, DELETE outright" in the page review; deletion waits on the mail-right-one merge landing and his call.
2. The losing halves of the seven doubled pairs (Intel Today, Growth, Connections, Lists, Reports, Settings duplicates) — retire only after each merge is proven live, per the FEED RETIREMENT LAW (final distillation → lock in → close).
3. `interfaces/factory/` duplicate authority (~254KB internal duplication, twin generators, 3 `sw.js` variants) — reconcile item filed; removal is the reconcile lane's proven outcome, not this run's delete.
4. `/projects/questions.json` — dead 404 still registry-listed; registry entry is a flag for the registry-reconcile lane.
5. Open PRs #3052 (mission-state/ledger, dirty, head moving) and #2981 (2026-09-30 smart-note capture, dirty) — stale/dirty flags for their owning lanes; not closed by this run.

## Maker scorecard for this report PR (Scorecard Law — maker only; merge needs a different seat)
Options: (A) file as draft PR with maker scorecard, held for different-seat scorecard — value 9 (preserves the record, obeys the corrected doctrine, reversible); (B) push to main directly — REJECTED, violates "never push to main" and the Scorecard Law; (C) skip the PR and post only to the board — value 4 (the record would live outside the super brain, violating the `.md` placement rule). Gates for A: reversible ✓ · no major damage ✓ (one added file under `BRAIN/05-MEMORY/`) · positive forward effect ✓. Decision: A. This PR is opened as a DRAFT; it must not be marked ready or merged until a different-seat scorecard at its exact head is posted on #3066.

— Naya Resolve, daily learning event, 2026-10-26
