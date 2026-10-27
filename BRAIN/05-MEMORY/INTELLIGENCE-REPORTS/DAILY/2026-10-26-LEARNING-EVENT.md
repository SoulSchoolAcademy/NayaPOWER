# Daily Intelligence — 2026-10-26 (America/Vancouver)

*End-of-day edition. Supersedes the morning edition of this file merged in PR #3082 (that run distilled the day at 03:37Z, before most of it happened). Sources: the 2026-10-26 and early 2026-10-27 memory logs (Vancouver day = 2026-10-26T07:00Z → 2026-10-27T07:00Z), live board #3066 (450 comments at open), and 17 PRs merged in the window (#3082, #3085–#3087, #3090, #3091, #3093, #3095–#3100, #3102–#3105). Main tip at open: `9ab30aded487792fa52df7cf86bcc5e0dab1610c`.*

## The day in one line

The team stopped governing by announcement: behavior was written as a constitution and then correctly demoted into the Naya Code, communication became addressed mail on a 15-minute clock instead of published waiting, and the day's three biggest disputes — the Hub overwrites, the PI counts, and the PI face — were all closed or narrowed by ordered, byte-level reads rather than by whoever spoke last.

## THE DAILY INTELLIGENCE — 7 items

### 1. The constitution is not a new document — it is completing the Naya Code
- **What:** Resolve built `BRAIN/01-GOVERNANCE/0036-NAYA-CONSTITUTION-V1` in three tongues with an executable gate (`tools/naya-constitution/check.py`, 8/8 tests; PR #3091). Convergence then proved Zara's point from issue #2245: the Naya Code already owns this job as an entry point that *resolves to* ratified law (Constitution Act · Law of One 0016 · Operating Code 0008 · 0017) and never competes with it. Both standalone texts (0036 and `GOVERNANCE/NIA-PROTOCOL-V1`) stand down as sources; the work is completing #2246's entry point, wiring enforcement, and adversarially testing it. Ratification stays Shawn's gate.
- **What it means:** 0036's recon missed the repo's own `CONSTITUTION/` directory — a scope error, owned on the record.
- **Why it matters:** One governing identity, resolved to law — no competing constitutions for a cold Naya to choose between.
- **What's in it for me:** A seat reads one entry point and knows how to behave; she does not have to adjudicate documents.
- **How it connects:** Feeds the gate in item 6 (behavior rules are only real when a checker or a call site enforces them) and the Endgame Sequence (item 5).

### 2. Communication became law — address, don't publish; mail is proven
- **What:** Shawn's suite landed in one day: the Asking Law (a feed post is not a message *to* someone — name the seat, the need, the unblock condition), the Escalation Ladder (Project Intelligence → board #3066 → Shawn as relay, last), the 15-Minute Clock (cycle ≤15 min; silent waiting is the defect), the Tap-Inflation Correction (decide by scorecard; never re-seek a tap already given; his reserved gates stay narrow and named), score-movement reporting instead of questions, and the Sharing Practice (board post *with link* + PI entry + mail to the seats + Smart Note when it fits). That night Smart Mail was proven end to end: Resolve claimed ID `resolve`, Power is `naya-power`, Nitro is `nitro`, Tree is `nayacodex`, Shawn is `shawnlife`; seats mailed each other and the director and everybody received it (Shawn confirmed ~00:56Z). The mail habit is standing: check every 15–20 minutes, 30 max.
- **What it means:** The alias table is not the authority — live addressing is (Nitro has no table row, yet `nitro` works).
- **Why it matters:** Every cross-seat input that day had arrived carried by Shawn personally; that single-relay failure mode is now named, lawful to escape, and mechanically replaced.
- **What's in it for me:** Ask a sister directly and get an answer in one cycle; never wait hours on a feed nobody was addressed in.
- **How it connects:** This is the transport the PI pulse (item 4) and the family charge run on; its first uses — addressed asks 6426497285, the concession mail in item 4, the fold in item 3 — all closed the same night.

### 3. The Hub deployer war ended at the mechanism — restores are not stability
- **What:** Two overwrite mechanisms were proven in sequence. (a) The frozen copy: repo `HUB/app/` carried a weeks-old home (523,177 B, sha `4aa796e0`) that the whole-folder auto-deploy shipped unchecked over the true home (5,463,030 B); Resolve landed the true home into `HUB/app/index.html` at source (commit `32ef40b4`), disarming that class. (b) The second writer: the lane-local Smart Note sync bake (`sync-smart-notes.py`, 5-minute cron) PUT its own build directly to the same Cloudflare worker `hub`, so every note landing replaced the repo build and erased /pi — proven by byte correlation (restores held until the next note landed; zero deploy-workflow runs in between), and named in the docstring of `HUB/deploy/deploy-hub-code.py` (`fdc5679e`). Power's `hub-deploy.yml` was exonerated (53/53 runs failed; it never deployed). Power then landed the fold: the second deployer is removed/folded, serving is stable, /pi still serves home bytes until the face landing (item 5).
- **What it means:** A freeze announced in prose is not a mechanism, and a successful restore proves only that a re-assert works — intermittence *is* the defect.
- **Why it matters:** Seven recurrences in one day, each burning a restore, because the cause was watched (sentinel) instead of removed.
- **What's in it for me:** The next canonical landing will stick; the cure's final proof is explicit — a subsequent note landing leaves /pi alive.
- **How it connects:** Unblocks the PI face landing (items 4–5) and is the concrete case behind item 6's lesson: name the stage you're actually at.

### 4. PI truth was reconciled — one record, one source, ordered reads
- **What:** Tree's parity audit, Resolve-verified: canonical `work_items` vs the legacy `project_intel_items` projection diverged (scoped join: 184 canonical records missing from the legacy display · 8 stale extras · 13 conflicting states). /pi reads canonical; /projects reads the legacy projection. The count dispute then closed by method, not authority: complete *ordered* reads (`order=item_key.asc`, limit 25/page — limit 50 truncates at the ~4,000-char sb-api cap) give **PI scope = 314 rows · 314 unique · 23 done_proven** — Power's numbers stand in full. Resolve's 330/349/374 figures were a prepared dataset and artifacts of unordered offset pagination racing a mutating table; he conceded all three by mail and put the dataset itself in the open as draft PR #3103. Cure roles: Power owns the one governed publisher + data boundary; Resolve owns reconciliation verification.
- **What it means:** A number without its scope and read method is not a number (L692: the filter is part of the number; L697: one record, one canonical source table).
- **Why it matters:** PI is the team's one place of accountability; if its counts move with the reader, nothing built on it can be trusted.
- **What's in it for me:** Quote 314/23 with the method attached and it will survive any other seat's re-read.
- **How it connects:** The publisher cure is the data half of the face in item 5; the privacy finding rides along (RLS enabled but anonymous read policies not owner-restricted = verified configuration, *not* proven exposure; the fix stays behind Shawn's authority gate).

### 5. The PI face was measured, not described — and the Endgame was sequenced
- **What:** Against the 42-check contract, the only shared artifacts scored: Power's draft PR #3089 = **6/42 NOT LIVE-READY**; Nitro's shared v2 = **11/42**; Resolve's v3 (built on Nitro's branch, dots replaced by Factory jewels, weakest point named on the face) self-checked **29/42**, then its anchor fix was different-seat verified 9.5 *at fix scope only* after Nitro caught three fake deep links minted on retired board #2793 (L698: a venue re-point must verify preserved anchors resolve on the target board). The check target now sits at head `9a4f3963` (items.json regenerated from the ordered read in item 4); Nitro's 9+ whole-face cold check at that exact head is the gate before landing. Zara's 8-dimension contract (D1–D8) is the scorecard form: no dimension below 9.0, a critical failure can never be averaged away. Shawn sequenced the endgame: (1) PI to 10/10 first, (2) rip apart every page vs the doctrine, (3) align, (4) sync the seams.
- **What it means:** A claimed "finished practice copy" with no bytes on any shared surface does not exist as work (full tree + ~1,078 branches scanned). Shared work, not handoff-and-wait (Shawn's correction): join the build on the shared surface.
- **Why it matters:** This is the 9+ Completion Protocol in practice — nothing is shown mid-build; a page arrives complete, scorecarded, or not at all.
- **What's in it for me:** Score movement (6 → 11 → 29/42) is the report; nobody has to take a seat's adjective for a face again.
- **How it connects:** Consumes item 3's stable serving and item 4's true record; produces the pattern every other page's rip-apart will reuse.

### 6. The merge doctrine was corrected — and its enforcement gap was root-caused
- **What:** Shawn corrected the doctrine in his own words (~03:18Z): he merges as a sweeper trusting the team; his clicks authorize and prove nothing; scorecard *before* putting a PR forward, then agents merge their own scored work; a merge-ready PR without its scorecard is the defect, and HOLD-parking is retired (SN-1873 carries the delta). The same day, sweep merges kept landing unscored — breaches reached **68** (incl. #3091/#3093/#3095 and #3097–#3100) — and Naya 5 root-caused it mechanically: the main ruleset requires **0 reviews and no required checks**. The cure is a ruleset change, which is Shawn-gated; the interim cure is post-merge different-seat scorecards at the exact merged heads, owned by the proposing seats.
- **What it means:** Announcement ≠ implementation ≠ verification ≠ value — the law was announced and recorded while the machine still permitted its violation on every merge.
- **Why it matters:** Sixty-eight repetitions of one lesson is the system's most expensive sentence: a gate that exists only in prose will be swept.
- **What's in it for me:** Never cite a director click as approval; bring the exact-head scorecard or the merge is a breach with your name on it.
- **How it connects:** Same shape as item 3's prose freeze and item 1's unwired constitution — the day's meta-lesson.

### 7. Smart Note collisions were cured by adjudication, not force
- **What:** The SN-1878 reconciliation door pass found **7 defects, not the recorded 3** (hash mismatches, stale page hashes, missing entries/captures across SN-1878/1879/1880), cured all in one pass — door checker at tip `4316bc72`: **ok:true, 0 defects, 0 tombstones**; registry 739 entries; corpus seal recomputed and independently matched. The deviation was reasoned on the record: the approval note was renumbered to **SN-1881, not SN-1879**, because Power had claimed 1879 in the interim with a complete filing — forcing 1879 would have manufactured a second collision (first claim stands, SN-033). Different-seat cold proof then closed serving: /s/sn1878 and /s/sn1881 each serve their own note. SN-1884 (design-mastery doctrine) filed full-form and serving the same night, completing the Sharing Practice's fourth channel for PR #3101.
- **What it means:** Collision repair that respects in-flight claims beats repair that wins the number and breaks the registry again.
- **Why it matters:** The registry is the collective's memory index; every doubled number is a lesson a future Naya retrieves wrong.
- **What's in it for me:** When numbers collide, adjudicate by first claim and document the deviation in the note itself — the next seat inherits the reasoning, not just the result.
- **How it connects:** Notes are the sharing unit in item 2 and the bake whose sync caused item 3 — the same system, cured at both ends in one day.

## What compounded today
- **Ordered, complete reads closed a live dispute in one pass** (item 4): the PI count argument ended when the method changed — this changes tomorrow's default for every number reported.
- **Addressed mail replaced published waiting** (item 2): the first addressed asks, the concession mail, and the deployer fold all moved seat-to-seat the same night they were sent — the ladder and clock are now exercised, not just written.
- **Cold checks stopped two landings and improved both** (item 5): 6/42 and 11/42 verdicts, delivered to named owners with named fixes, produced v3 — scoring as a build input, not a postmortem.

## What was let go
- **Standalone constitutions** (0036, NIA-PROTOCOL-V1) as governing documents — kept as sources to the Naya Code, retired as authorities.
- **HOLD-parking and tap-seeking** — retired by the corrected merge doctrine and the Tap-Inflation Correction.
- **"Second deployer = the lane pipeline"** — superseded by the proven note-sync-bake mechanism; Power's `hub-deploy.yml` exonerated on the record.
- **330 / 364 / 374 as PI truth** — superseded by the ordered-read 314/23 (PI scope) with the method attached.
- **Restores as stability claims** — Restore #5/#6 receipts stand as re-assert proofs only.
- **The morning edition of this report** — superseded by this edition.

## Trash candidates — FLAG ONLY (deletion is the Human Director's call)
1. **Retired boards still receiving real posts** — Zara's acceptance contract and Power's playbook post + invitation both landed on archived #2793 today and had to be re-homed to #3066 (6430463709, 6430464616, 6428332322). *Feed Retirement Law candidate: the retired boards' final distillation is locked in; their continued postability is the leak.*
2. **The legacy PI projection** — `project_intel_items` / /projects as a second display of the record (184 missing · 8 stale · 13 conflicting vs canonical `work_items`). Retire after Power's one governed publisher lands; until then it is a stale second truth, not a backup.
3. **Duplicate repo surface `interfaces/factory/`** — the twin of `BRAIN/10-INTERFACES/SMART-FACTORY-CANON` found by PR #3075's retro-score (5.5/10, L677); reconcile to the canonical home, do not keep both.
4. **NOW board #2599** — 256,105 chars vs the proven 256,088 PATCH ceiling: a record surface at its ceiling silently freezes (L699). Trim/distill is owed before any further entry; flagging as a feed-hygiene candidate.
5. **Stale / dirty / superseded PRs** — #3052 (dirty, purpose-gate deadline 2026-10-27), #2981 (stale), #3088 (review owed), #3089 (DO NOT MERGE draft; its checks are harvested into the v3 contract) — owning lanes to close or land; flagged, not touched.
6. **Duplicate live share-table rows for SN-1878/SN-1881** — registry on main is unambiguous and serving is cured; the DB-row delete is grant-gated.
7. **The prepared PI dataset's goal-file copies** — the dataset now lives in the open as PR #3103; the goal-file originals are a second copy that will drift. Keep one source once #3103 lands.

## Maker scorecard (this report's PR — held, not merged)
Options: (A) merge on maker score alone — 2/10, violates the different-seat rule Shawn restated today; (B) open as DRAFT, byte-verify, post the lock-in on #3066, and hold for a different-seat exact-head scorecard — 9.5/10, reversible, gates pass; (C) skip the PR and post only — 4/10, the day's intelligence would live only in a board comment. **Decision: B.** No receipt from another seat, no merge — per SCORECARD-LAW-V1 and item 6 above.
PI routing note: the learning-event item's PI entry routes through the writer seat (Power, S1 door); it is named here, not claimed synced from this seat.

— Naya Resolve, daily learning event run, 2026-10-27T03:37Z (2026-10-26 Vancouver)
