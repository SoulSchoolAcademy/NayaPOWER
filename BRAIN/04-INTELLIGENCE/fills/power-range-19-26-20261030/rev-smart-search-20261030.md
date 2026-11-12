# Capability fill — Smart Search — POWER RANGE REVISION 20261030 (staging only, NOT landed, NOT complete)

**Revision status:** Three-seat update pass, Shawn 2026-10-30. Power range 19–26, this file #26.
Maker only, never verifier. Scorer: Resolve (maker never verifies own work).
**Kind: CAPABILITY, not an app build.** Shawn's ruling 2026-10-30: Smart Search is NOT
a separate app. Search lives on EVERY app as quick tabs + search in the Smart Bar,
searching the whole network. There is no standalone face, no separate app verdict,
and no 26th app build. This revision specifies the weave; it does not specify a page.
**Base carried:** merged packet `~/workspace/user/files/fill-packet-smart-search-merged-20261029.md`
(Power, 2026-10-29; Registry = 1028's card/face/brief read; Workspace = 1029's
spec + harness). Packet grounding (15 F-fields, conflicts, measured truth, chain)
rides that packet by reference, never claimed as in this file. The canonical
app-fill file `app-fill-smart-search-20261029.md` (batch-1, wave-3 mirror 9.0) is a
SEPARATE record of the old app framing — this capability revision does NOT overwrite
it and does NOT inherit its app verdict; Resolve scores THIS capability spec.
**Fill-doc version (this revision): 4.0-20261030-power-range.** Ranker version: OWED
(workspace ranker file `rank-v3.js` exists; no version number on file — never
conflated with the fill-doc version).

## §A. Ultimate function + bullseye moment (master §6 #26, quoted, never rewritten)

- **Bullseye moment:** type anything and the right thing in NayaNET answers first —
  the exact note, person, space, or page — and the click lands where it promised.
- **Ultimate function:** search across the whole system, with exact-phrase tiers and
  /s/ deep links that resolve to the note, not the feed root.
- **Packet bullseye (carried, distinct):** takes a plain question or phrase and returns
  the matching Smart Notes, ranked title → nutshell → block, with the matching
  Intelligent Block itself rendered at the top — not a scroll jump, not a list of
  matching words. How it is connected: reads the notes corpus (the original records)
  and returns blocks from those records. Connects to the feed (a found note opens as
  its block), to the network ranking (notes + blocks first, then network in the same
  ranking), and to every page that needs finding (the one search, not a search per
  page). How it looks: one top result as the full block (title, nutshell,
  matched-tier badge, matched words, present sections, "Open the block"), ranked list
  beneath. Phone-first, one-handed, readable phone-size text.
- **How it functions (locked spec + decision A, carried):** whole-word,
  plural-insensitive matching; stopwords excluded from content scoring but counted
  for phrase checks; exact contiguous full-query phrase in nutshell/block OUTRANKS
  scattered higher-tier word matches (within exact matches: title > nutshell >
  block); partial, stemmed, fuzzy, synonym matches stay in their tiers; notes-only,
  mail never read, ranked, or rendered; deterministic tiebreaks (identical scores
  order by id); SN-id lookup (explicit SN ranks that note first, tier 'id');
  all-stopword query → 'too-general' state, never an empty lie; empty query → no
  results, never noise; panel shape 1 + 7 = 8, feed never scrolled.
- **NOT this capability:** the command palette (`naya-search.js`, network types) is
  NOT this packet. Smart Search is Notes + Blocks first, then the network in the same
  ranking — never a second search system, never private mail content. The
  palette-vs-capability reconciliation is OWED (see §H) — one search entry, ranked
  unified, never two searches.

## §B. THE WEAVE — how search lives in every app's Smart Bar (this pass's specification)

**Weave rule:** every app's Smart Bar carries a search entry (search field + quick
tabs) that runs the SAME ranker over the WHOLE network. The entry lives in the bar
chrome — it is not a page, not a tab to a search app, and not a per-app search.
Power owns the capability (ranker, corpus, ranking, /s/ resolution); Nitro renders
the bars (one hand, one language — the search entry looks and behaves identically
on every app).

**Per-bar placement (spec §4 decided rules applied):**
- The search entry sits in the bar chrome, outside the scrolling tab row, so drift
  (top right, bottom left) never carries it away. Exact chrome position + phone
  layout: OWED (Nitro lane — the entry must stay reachable one-handed at phone
  width; a position that fails that is a defect, not a layout choice).
- Top bar: the entry searches from inside the current app AND the network (one
  search, notes + blocks first, then network in the same ranking). The current app's
  own sections stay the top bar's tabs; search does not become a tab.
- Bottom bar: the entry is the same capability, same ranker, same ranking — never a
  second search with different results. Bottom-bar tabs stay APPS ONLY; search is
  chrome, not a tab.
- Quick tabs: the search entry offers quick tabs (recent / saved / per-app shortcuts
  as the record provides them — tab lists come from the record, never invented).
  A quick tab with no destination says so — never a dead link.
- Results render: one top result as the FULL BLOCK (title, nutshell, matched-tier
  badge, matched words, present sections, "Open the block"), ranked list beneath,
  panel shape 1 + 7 = 8, feed never scrolled. A result that opens as a scroll jump
  or a word list FAILS the bullseye.
- /s/ resolution: every result's click lands on the NOTE (the block itself), never
  on the feed root. SN-1897's redirect to the Smart Feed root is the standing
  counterexample — the standalone block view it needs is still OWED (see §H).
- Privacy: notes-only by construction everywhere. Live mail exclusion = G4, still
  OPEN — delivery of mail-adjacent search behavior WAITS on G4. No mail content is
  read, ranked, or rendered by this capability, in workspace or live, ever.

**Weave order (as each app lands):** the search entry lands WITH each app's bars, in
the grouped build order (pilot → door+identity → Trinity → communication →
knowledge → system/money/engine). An app that lands without the search entry is
missing its bar — not aligned, no exceptions. Power's GO/NO-GO on the capability
comes AFTER the first three apps carry it live (see §F) — not before, not on the
workspace harness alone.

## §C. Alignment v2 — Shawn's 4-part method, adapted to a capability (this pass)

1. **Aligned how?** Design: one search, not a search per page — the network's memory
   with one entry everywhere. Laws: notes-only (mail never read); original records
   only (results open the record's block, never a copy); exact-phrase tiers locked
   (decision A); deterministic ranking (identical scores order by id); no second
   search system (palette reconciliation owed, never duplicated). Rules: fill bar
   honestly graded (see §G). System: the capability plugs into every app's bars;
   it owns no surface and no tab.
2. **Missing the mark where?** (1) NO live route exists for Smart Search — the
   workspace harness is the only place the ranker runs. (2) Live chassis stale:
   old per-term substring scoring on a stale baked corpus (381 notes; SN-1880
   absent) vs workspace corpus 394. (3) G4 (live mail exclusion) + G5 open; G4/G5 +
   exact-phrase-tier decisions await the chain record. (4) SN-1897 standalone block
   view owed (redirect to feed root ≠ bullseye). (5) C2-06 stays rank 11 — a SPEC
   question (the phrase "nobody reads my mail" appears NOWHERE in SN-1888; the
   nutshell reads "Nobody reads it"), NOT a ranker bug — the tier is NEVER widened
   unilaterally to promote it. (6) Shawn's live try still word-hunts (his own
   report: a query about inputting a smart note went to the bottom of the feed
   among matching words instead of returning the actual block at the top) — the
   workspace improvement is NOT live, so the live friction stands. (7) Palette
   reconciliation owed (see §A). (8) Corpus refresh mechanism owed (workspace 394
   vs live 381 — the refresh path, not just a one-time refresh).
3. **Fastest effective fix (card order, unchanged from the packet chain).**
   Different-seat scorecard + verification of THIS capability spec → Nitro rendered
   review (desktop + phone, real address, /s/ click-test, cold-page wait) → G4/G5 +
   exact-phrase-tier decisions from the chain record → Power's GO/NO-GO in writing
   → gates → post-landing live proof (Q1–Q7, phone + laptop) → Shawn's eye test as
   the final gate. No step skipped, no step self-awarded. What it is NOT: not
   sending a link before clicking it open (SN-1897 miss → author-click rule); not
   word-hunting (locked spec, not a new idea); not claiming an exact phrase not in
   the note bytes (verify phrase presence in the note bytes, every time); not
   presenting workspace as live; not widening a tier unilaterally.
4. **Connections map v2 (per-link states; TARGET = proposed, never built):**
   - Every app's Smart Bar: the search entry lives in the chrome. TARGET (weave
     order §B).
   - Notes corpus (original records): the ranker reads originals, returns blocks.
     TARGET (corpus refresh owed — workspace 394 vs live 381).
   - Feed: a found note opens as its block in the feed. TARGET (/s/ resolution,
     SN-1897 owed).
   - Network ranking: notes + blocks first, then network in the same ranking.
     TARGET (network leg is its own packet after the notes leg lands — not
     smuggled into this one).
   - Connections / Library / every app's content: searchable through the one entry.
     TARGET (content coverage follows the corpus refresh).
   - Ask Naya (answers resolve to records): Ask answers and Search results both
     resolve to original records, never copies. TARGET (shared resolution rule).
   - Command palette (`naya-search.js`): NOT this capability — reconciliation OWED
     (one entry, ranked unified).
   - Mail: NEVER read, ranked, or rendered. NOT-A-CONNECTION (stated so no reader
     mistakes notes-only for a mail search).
   - Place in the tree: the network's memory — without it, the network's memory is
     write-only.

## §D. Measured truth — carried, neither inflated (packet, re-stated this pass)

- Power re-test (workspace, exit 0): 37/39 #1-with-block (was 34/39), top-3 38/39
  (was 35/39), mean rank 1.31 (was 2.23), original 9 9/9 with zero regressions.
  Promoted to #1: C1-04 (was 15), C1-05 (was 17), C2-03 (was 14). C2-01 stays rank 3
  (paraphrase, correctly NOT promoted). C2-06 stays rank 11 (phrase absent — see
  §C.2.5). No previously-passing term dropped. Corpus: 394 workspace notes, mail 0.
  Re-run rule (packet, carried): `node test-final.cjs` re-runs after ANY ranker
  touch; a re-run that is not run is not proof.
- Resolve cold verification (live-served run, 2026-10-28 16:12–16:52Z): top-1 4/4 —
  ONE run, counted once. The definition example's own verdict is PARTIAL (block form
  NOT met; phone leg owed); a passed accuracy measure flips no facet by itself.
- Live chassis today (both packets agree): old per-term substring scoring on a stale
  baked corpus (381 notes; SN-1880 absent). The workspace ranker is NOT the live
  search, and this revision never claims otherwise. NO live route exists. No link
  to a live search is sent with this revision, and none may be sent until the author
  has clicked a live result open in a real browser.

## §E. F9 trio — DRAFTED this pass (bar clarification, PI n=180)

The packet carries 1029's purpose/mission/goal/vision; CARD lines were OWED. This
pass DRAFTS the card lines from the packet lines (derivations stated, judgment owed
to the scorecard — never presented as sourced):

- **Vision — DRAFTED:** "Search so good it disappears — a citizen types anything and
  the right thing answers, and the search itself is forgotten." Derivation: 1029's
  vision line, promoted from packet line to draft card line.
- **Goal — DRAFTED (measurable, via the harness + the live bar, not via a %):**
  "39/39 terms #1-with-block on the harness with zero regressions on the original 9
  — and then the same standard proven live (top-1 on a fresh cold set, block form
  rendered, phone leg proven, /s/ click-test passed)." Derivation: 1029's measurable
  goal + 1028's five success defaults. No % is typed: % stays OWED until Search's
  own jobs land in the record with criteria + evidence (packet % rule, carried).
- **Mission — DRAFTED:** "End word-hunting: one search that finds the original
  record — notes and blocks first, then the network in the same ranking — and opens
  the block itself, never a list of matching words." Derivation: 1029's mission +
  purpose lines, composed into a mission sentence.
- **Success bar (carried, 1028's five defaults + 1029's chain):** (1) top-1 accuracy
  holds on a fresh cold set (not just the 4/4 seed); (2) results render in block form
  per the definition; (3) phone leg proven (renders and completes at phone width);
  (4) /s/ click-test passes; (5) G4/G5 + exact-phrase-tier decisions settled. Only
  (1)'s seed measure exists today (Resolve 4/4, one run); none of the five is proven
  complete.

## §F. F12 — carried + weave tests (0 passed live)

Registry evidence bar (carried, specified not met): (1) serve vehicle renders a
search surface, phone + laptop; (2) results render in block form per the definition;
(3) top-1 accuracy holds on a fresh cold set (not the seed set); (4) /s/ click-test
passes — the click lands on the note, not the feed root; (5) G4/G5 + exact-phrase-tier
decisions settled on the record; (6) a citizen searches and lands on the right thing,
unaided, phone + laptop, cold; (7) rendered review: 0px overflow at 390 + 1280, zero
errors, different seat. Tests passed (live bar): NONE. Workspace harness checks
(`node test-final.cjs`: original 9 9/9 + Cycle 1/2/3 sets, 37/39 now + panel shape +
SN-id + stopword checks) are HARNESS evidence, never live passes — the two are never
blended.
Proposed verifier chain (packet, carried): Nitro rendered review → different-seat
full-coverage scorer → Power GO/NO-GO in writing. Verifier ≠ maker at every step.
Verdicts OWED.
New in this pass: T-Search-Weave-1 — first-three-apps weave test: after the first
three apps carry the search entry live, a citizen searches from EACH app's bar and
lands on the right block, unaided, phone + laptop, cold — same ranker, same ranking,
no per-app divergence. Evidence: three cold walks + rendered reviews. Failure/
recovery: any app diverging (different ranking, word-list results, feed-root click)
= fail; recovery is fixing the weave in that app's bar, never forking the ranker.
T-Search-Weave-2 — palette reconciliation test: one search entry exists per surface
(palette + capability reconciled, not duplicated); a search from the palette entry
and from the bar entry return the same ranked blocks. Evidence: side-by-side cold
walks. Failure/recovery: two different searches = fail; recovery is the
reconciliation decision on the record, never a second system shipped quietly.

## §G. Bar checklist (updated this pass — adapted to a capability)

1. Seven-part content — CLOSED AS SPEC (bullseye + function + connects carried from
   the packet; weave spec §B written; F9 trio DRAFTED §E; front/back lists: the
   capability's "front" is the bar entry + results render, its "back" is the ranker
   + corpus + /s/ resolution — TARGET lists, explicitly NOT record jobs, since no
   Search jobs exist in the record).
2. Alignment diagnosis + remedy + connections map — CLOSED (v2 above, with the
   live-friction + C2-06 + palette items named, not smoothed).
3. Sourced F9 trio — DRAFTED, not sourced (§E); awaits scorecard judgment.
4. Real F12 test lists + NAMED verifier ≠ maker — CLOSED AS LIST + PROPOSAL
   (registry 7 + harness checks + T-Search-Weave-1/2; verifier chain proposed =
   Nitro rendered leg + different-seat scorer + Power GO/NO-GO; verdicts OWED;
   live passes: NONE).
5. Owner + version + data/API contract — PARTIAL, honestly (fill-doc version
   4.0-20261030-power-range set; OWNER NAMED: Power owns the capability (plan) —
   the capability owner, not an app owner; ranker version OWED; contract: ranker
   interface draft — matching tiers + corpus read + /s/ resolution + notes-only
   rule, implementation OWED on the live chassis).
6. Tree's four fields — PARTIAL (implementation source: workspace ranker + harness,
   live chassis stale; acceptance tests listed, 0 live passes; owner Power
   (capability); contract interface draft).
7. Per-batch shared-parts harvest note — CLOSED (§I).
8. Different-seat scorecard on the exact final version — OWED (Resolve scores this
   range; this mirror is the maker's, never the scorecard). NOTE: the packet's own
   chain (scorecard of the merged packet) is ALSO owed — the two scorecards are
   distinct (packet scorecard + capability-spec scorecard) and neither substitutes
   for the other.
9. Shawn's verdict — N/A (not one of the original four). Shawn's EYE TEST is the
   final gate of the chain (§C.3) — a gate, not a verdict on this spec.

## §H. Gaps still open (counted, 16 — owner + exit each)

Different-seat scorecard on this capability spec (exit: Resolve's score) · merged
packet scorecard, chain step 1 (exit: packet scorecard on the record) · Nitro
rendered review, desktop + phone, real address, /s/ click-test, cold-page wait
(exit: rendered review) · G4 live mail exclusion + G5 decisions, chain record
(exit: decisions on the record) · exact-phrase-tier decisions from the chain
record (exit: decisions on the record) · Power GO/NO-GO in writing (exit: written
GO/NO-GO, after the first three apps carry the weave live — never before) · gates
(exit: gate records) · post-landing live proof Q1–Q7, phone + laptop (exit: proof
record) · Shawn eye test, final gate (exit: his eye on the live capability) ·
live route for the capability (exit: a live search entry clicked open by its
author in a real browser) · live chassis refresh, 381 → current corpus incl.
SN-1880 + ranker replacement (exit: live corpus + live ranker proven by the
harness standard) · corpus refresh MECHANISM, not just a one-time refresh (exit:
mechanism on file + proven) · SN-1897 standalone block view, /s/ resolves to the
note, not the feed root (exit: block view + click-test) · C2-06 spec question,
phrase presence in SN-1888 bytes (exit: spec decision on the record — never a
unilateral tier widening) · palette reconciliation, one entry, ranked unified
(exit: reconciliation decision + T-Search-Weave-2) · ranker version number (exit:
version on file) · % + Search jobs in the record with criteria + evidence +
prover ≠ maker (exit: jobs in the record — % computed only then, never typed).
Fill stays NOT COMPLETE (no live leg, no scorecard) until the chain runs.

## §I. Shared-parts harvest note (this pass)

Contributions: the weave pattern (a capability lives in every app's chrome, never
as its own destination — reused by every future capability: search today, and any
capability Shawn rules non-app tomorrow); the notes-only rule (mail never read,
ranked, or rendered — reused by every memory surface); the harness-≠-live
discipline (37/39 workspace is harness evidence, never a live pass — reused by
every workspace measurement); the phrase-presence rule (verify phrase presence in
the note bytes, every time — reused by every exact-phrase claim); the
author-click rule (no link sent before its author clicks it open — reused by every
/s/ link). NOT harvested: any live search claim; any per-app search divergence;
the palette as a second system.

## §J. Sources read this pass + NOT verified

Read: this pass's plan; alignment master (§6 #26, §2, §3, §5, §8 — corrected file);
alignment spec (§4, §6); merged packet (bullseye, F9, F12, measured truth, % rule,
chain, kit extras — decisive sections, read in full this pass).
NOT verified from this seat: any live route, render, or cited workspace path inside
the carried packet (no live browser in this lane) — cited paths are UNVERIFIED, not
passes. The harness was NOT re-run from this seat (workspace ranker files exist on
the parent seat's box; the 37/39 measure is carried from the packet + Power's
re-test record, NOT re-proven here — a fresh harness run is owed before any build
touches the ranker, per the packet's re-run rule). The master §6 #26 heading ("no
face entry yet (to build)") is STALE against its own corrected fix line (capability
weave) — flagged for the record lane; this revision follows the fix line + Shawn's
ruling, never the stale heading. No mail sent or read this pass. No canonical file
overwritten. No PI note, no board comment, no build, no deploy, no schema, no
money, no credentials, no deletions, no history rewrites.
