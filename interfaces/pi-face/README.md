# PI Face — review draft (NOT the live page, NOT shipped)

## What this is, plainly

A complete, self-contained Project Intelligence face (`pi-face.html`) built
to the Wave 6 live-face build packet
(`workspace/system/pi-hub-live-face-build-packet-2026-10-26.md`), folded
with Shawn's human-first refinement (2026-10-26, binding): the surface is
in human words — plain labels, no hashes, no IDs, no machine strings —
and machine proof lives ONE TAP behind each item's Details door. Every
number carries a read time. Nothing is invented. Nothing staged is
presented as live.

**This PR does not change the live page.** It cannot — see Provenance
below. It is a DRAFT for Nitro's rendered review and for the provenance
ruling. It must NOT be merged until the gates in "Owed before landing"
land. Merge to main auto-deploys the Hub worker
(`.github/workflows/deploy-hub-cloudflare.yml`), which does NOT serve
`/projects` — so even a merge would not land this face. The wiring step
to the real `/projects` route is named, not assumed.

## Human-first rules applied (Shawn's refinement)

- Surface labels in human words. State mapping used when rows arrive:
  done_proven → "Done · proven", in_progress → "In motion",
  queued → "To do", verifying → "Being checked",
  needs_shawn → "Needs a decision", blocked → "Blocked".
  Raw state codes, item keys, hashes, SHAs, and entry IDs never appear
  on the surface; they live behind the item's Details door.
- % done prominent (largest orb, computed live from the read, never typed).
- Done vs to-do unmistakable: done means finished AND proven; anything
  less stays in to-do until its proof lands.
- Movement visible: verified finishes today + effort per verified finish,
  from the live state read, with read time. No movement number is shown
  without its read.
- Every item visible, nothing hidden behind a filter by default: the
  to-do section shows the whole list structure with no filter applied.
  The ROWS are withheld (see Items read below) — showing invented rows
  would break "the numbers don't lie". If it is not there, it is not
  done, and this face says what is not there.
- Buttons elevated (three-layered shadows), every control labelled
  (no icon-only controls), icons are labelled text companions only.

## Live read path (the only data path in the face)

1. `fetch("/projects/state.json", {cache: "no-store"})` on every load
   and on Refresh. Proven live: served from production, refreshes
   (verified 2026-10-26: derived minutes before each read).
2. Hub numbers computed client-side from that payload's counts
   (done_proven / total = % done). Read time shown from the payload's
   `derived_at` plus fetch time.
3. Failure mode (packet §2.7): on failed/timeout/partial read, the face
   shows "Live read failed at <time> — showing structure only, no
   numbers invented." Never a spinner hiding failure, never a carried
   % presented as current.
4. NO other data source: no workspace JSON, no staged file, no seed,
   no derivation presented as live. `/projects/todos.json` is NOT read
   (staged-1 seed, not live-updating). The ledger is NOT claimed live
   or frozen by the face at render time (no ledger endpoint is wired);
   the ledger section says so.

## Items read — the endpoint contract (NOT yet existing)

The full item rows (names, owners, next steps, notes, receipts,
updated times) need a live items read on the production worker. Until
it exists, the face shows the honest notice and no rows. The endpoint
must return, per item: human name, state, owner, next step, latest
note text, receipt link (where done is claimed), updated time, and
the machine fields for the Details door (item key, state code,
evidence URL, prover). The row format in this face is built for that
payload; wiring the endpoint lights the list up with no other change.
Per-area counts and per-area % stay withheld until backfill
acceptance (Uncategorized under 5%, zero done uncategorized, zero
needs-decision uncategorized — none met; latest verified derivation:
Uncategorized 186/280, 66.4%, 28 of 30 done uncategorized).

## Provenance finding (proven, not assumed)

The live `/projects` page source is NOT in SoulSchoolAcademy/NayaPOWER
at the main tip:
- Full recursive tree (6,772 entries, not truncated): no projects app,
  no todos app, no state.json generator.
- Code search for four exact live strings ("Reading your projects",
  "Shared with you", "The ones you started", "Projects are kept in
  NayaNET's shared records"): no code hits.
- `HUB/app/index.html` (the Hub SPA) contains none of the live
  `/projects` strings and carries a different title and byte size.
- The only deploy workflow serves `HUB/app/**` to the Hub worker,
  which serves static assets only — it does not serve `/projects`.
- Registry entry for `/projects` carries `source_sha: null` and
  `deployed_sha: null`.
Ruling requested (in the system, board + PI): where is `/projects`
deployed from, and who owns that deploy? Until that lands, no PR can
edit the live page in-repo, and no claim otherwise is made.

## Packet sections satisfied

- §2 live read path: state.json path, read-time labels, failure mode.
- §3.1 hub top: Project Intelligence first, 5 numbers (parts at 9+
  DARK, today's pace NOT_MEASURED, sync health via ledger section
  honestly unwired, gates count live), 3 lists in structure (weakest
  point / priorities / packets load with the items read — counts
  live, names withheld, never invented).
- §3.2 area views: breadcrumb + return top and bottom, header block,
  % gate block, to-dos by state (structure), bottlenecks/enhancements
  (honest), done-with-receipt rule, decisions separate, links
  (only working or labelled ones), feed (honest), team notes
  (honest), pages DARK/NULL, bottom switch + search + back.
- §3.3 areas: 12 rooms in seed order, seed colours on chrome only;
  areas 11–12 shown NEUTRAL (distinct colour pending Shawn's contract
  amendment or Nitro's non-adjacent-reuse ruling — provisional reuse
  NOT presented as distinct).
- §4 hold table: per-area % withheld, per-page scores DARK/NULL,
  parts at 9+ DARK, today's ratio NOT_MEASURED, no live ledger header,
  signed-in view NOT claimed, owner columns NOT claimed trustworthy,
  questions.json NOT linked (404), shell pages NOT presented as live,
  every control works or is absent.
- §5 ledger: no live header, no productivity number from a frozen
  table; ledger section honest about its unwired read.
- §7 signed-in test: NOT run, NOT claimed — owed via live-browser
  delegation (guest view is not a substitute).
- §9 harvest: see Inventory below. §10 "done" look: structure only
  until the owed gates land.

## Gate homework (shown, in order)

1. Lane: builder is Power (engine lead), building under Shawn's
   explicit correction that every seat learns design and does
   interfaces, with Nitro reviewing and teaching. This draft is NOT
   presented to Shawn before Nitro's rendered review.
2. Contract read, in full, 2026-10-26:
   - `workspace/user/files/naya-design-laws-official-2026-10-17.md`,
     SHA-256 `0a3ae81bfb540fcf4404f552d2cb019522edac5e4c6d6fd8319cb57a6c58bbac`
   - `workspace/interfaces-build/README.md`,
     SHA-256 `704c81b16eef0f08e13124502a1d33eaafa0904ce3cb960c59eac43577ba209d`
   - `workspace/user/files/DESIGN-LANGUAGE__1.pdf` (contract v1.1
     canonical, ratified 2026-10-03; contract wins on disagreement),
     SHA-256 `44facb53605483920f815e4b8fb2b9a8534dd7b5d1627a53f07c0c8220dda01e`
   - `workspace/system/pi-hub-live-face-build-packet-2026-10-26.md`
     (build packet), `workspace/system/project-intelligence-hub-10star-spec.md`
3. Inventory, composed verbatim, no new Lego piece:
   - N5 tokens (laws file Law 9; machine-check allowed set in
     `workspace/design-gate/design-gate.json`)
   - Pill buttons, 999px, black center, white text, white rim at rest
     (DESIGN-LANGUAGE §5.1 button DNA; flagship Projects Start card)
   - Board grammar: horizontal rectangles, layered elevation
     (DESIGN-LANGUAGE §1.2/§4; `.ph-card` flagship form — gradient
     rendered here in machine-check-allowed obsidian/deep tokens,
     since the flagship `#14141c`/`#0a0a10` are outside the allowed
     set; Nitro may rule otherwise at review)
   - Orb circles carrying numbers (NAYA-ORB-002; DESIGN-LANGUAGE §7.1)
   - Smart Note card pattern as the row format reference (packet §9.3)
   - Hub top bar pattern: "← Hub" pill + wordmark, reworded to
     Project Intelligence (packet §9.3)
   - Section heads with breathing dot (DESIGN-LANGUAGE §6.4)
   - Diamond bullets as chrome (packet §9.3)
   - Repo pieces cited: `naya-library/tokens.css` (token library),
     `components/01-hero-buttons.html` (hero buttons)
4. Machine check: `python3 workspace/design-gate/check-design-gate.py`
   on `pi-face.html` → PASS on all four checks (private_hex,
   colored_button_at_rest, flat_surface, dead_control), exit 0.
   Floor only, not a review.
5. Same-Language Check (DESIGN-LANGUAGE §10, 24 items), self-assessed
   in source — rendered items OWED to Nitro, never claimed:
   1 field PASS (source) · 2 full width PASS (source) · 3 rectangles/
   circles PASS (source) · 4 no voids PASS (source) · 5 twin pluses
   N/A (Hub chrome, not this module; no second chrome added) ·
   6 Smart Tabs N/A (same reason) · 7 drift N/A (no tab bar) ·
   8 walk PARTIAL (packet seed order governs; adjacent hues all
   distinct; walk order differs from DESIGN-LANGUAGE start — seed
   table is the packet's colour authority) · 9 colour jobs PASS
   (source) · 10 rest-white PASS (source; rendered confirmation
   owed) · 11 hover-edge-only PASS (source; pointer measurement
   owed) · 12 jewel tones PASS (source) · 13 elevation PASS
   (source; computed-style confirmation owed) · 14 wells/buttons
   PASS (source) · 15 button DNA PASS (source; keyboard
   confirmation owed) · 16 jewel icons PARTIAL (no standalone
   icons; every control text-labelled; Nitro to rule) · 17 type
   PASS (source) · 18 orbs PASS for numbers (source); people orbs
   N/A until item rows · 19 living data PARTIAL (shape + human
   sentence present; per-stat trend needs history the read does
   not carry; movement shown as counts) · 20 timestamps OWED
   (no feed rows yet; when feed lands, stamps must follow §7.5) ·
   21 calm switch PASS (source; emulation confirmation owed) ·
   22 no dead buttons PASS (source) · 23 nothing recreated PASS
   (pieces named above) · 24 edit-only FAIL (honest — provenance
   finding above; this is a new module awaiting wiring, not an
   edit to the existing page).
6. Nitro rendered review: OWED (requested in the system with this PR).

## Fresh verification reads (build time, 2026-10-26T15:24:35Z)

- NayaPOWER work_items: total 280 — done_proven 30, in_progress 52,
  queued 178, verifying 13, needs_shawn 6, blocked 1.
- All projects work_items: total 340 — done_proven 46, in_progress 65,
  queued 202, verifying 15, needs_shawn 8, blocked 4.
- ledger_entries: 30 rows, max seq 31, latest 2026-10-22 23:01:21Z
  (frozen — stated in the build record, never as face data).
- Live `/projects/state.json`: derived minutes before each read;
  counts track the all-projects aggregate within small filing drift.
  These numbers are verification reads for this PR, never face data
  baked into the file.

## Owed before landing (in order)

1. Provenance ruling: where `/projects` deploys from + who owns it.
2. Items read endpoint on the production worker (contract above).
3. Backfill acceptance (schema tap + lane-owner review + acceptance
   re-read) before any per-area %.
4. Nitro rendered review, desktop + phone, at a real address.
5. Different-login scorecard at the exact final head, 9+ to land.
6. Signed-in acceptance test (§7) + cold citizen walk, desktop +
   phone, at a real address.
7. Separate deploy tap (Shawn) — distinct from any schema tap.
8. Ledger writer gates (§5) before any live ledger header.
Until 1–7 land, this PR stays DRAFT and the live page is unchanged.
