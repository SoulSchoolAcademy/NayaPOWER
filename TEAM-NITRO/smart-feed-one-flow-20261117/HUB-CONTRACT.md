# THE HUB CONTRACT v1 — updated 2026-11-17 (One Flow round, maker seat)

**Status:** VERIFIED SPECS + OPEN DECISIONS. Every spec below was measured from the code, the live API, or the PR diff — cited. Anything unverifiable is marked UNKNOWN, never invented.
**2026-11-17 update (Smart Feed / One Flow round, branch `smart-feed/one-flow-20261117`):** D2 RESOLVED — the wire is named and built (Supabase-direct anon REST read, §Hop 4 below). D5 RESOLVED — the transport is the 15s poll, measured in seconds (not realtime broadcast). Hop 2's link is NAMED (`promote_naya_note_to_feed`) but NOT BUILT server-side; the Hub live read merges both tables client-side until it lands. Hop 5 RENDER is BUILT this round. The `naya_notes` anon INSERT refusal the old Break 3 assumed NO LONGER HOLDS live (measured 2026-11-17 16:23Z: HTTP 201) — see the 2026-11-17 section at the end.
**Purpose:** the complete specification for the Hub's full loop — what each piece does, how it connects, why it's built that way, and the exact specs. One contract, no gaps.
**Alignment:** implements the master directive's mission (prove the brain learns: capture → persist → receipt → retrieve → apply → verify → learn). The compiler measures this contract's done-states; where they disagree, the compiler wins.
**Working file:** this document IS the queue — each hop carries its status. Claim a missing piece, build it, scorecard it.

---

## THE LOOP (7 hops)

```
"smart note this"
  → [1 CAPTURE] v7_create_smart_note RPC
  → [2 PERSIST] v7_smart_note_transactions → (UNNAMED LINK) → nayanet_intelligent_blocks
  → [3 EMIT] emitter → HUB/FEEDS/*.json → raw.githubusercontent.com
  → [4 BRIDGE] window.NayaPowerRuntime → envelope {ok, state, data}
  → [5 RENDER] page loader → Smart Note cards
  → [6 ARCHIVE] GitHub filing (async)
  → [7 MEASURE] compiler probes → HUB/MAP-STATE.json
```

---

## HOP 1 — CAPTURE

**What:** turns "smart note this: [lesson]" into a canonical Smart Note row.
**How:** `POST /rpc/v7_create_smart_note` (authenticated `naya-runtime` user).
**Why this way:** the v7 RPC pipeline is the one capture path that has ever run in production (27 transactions Oct 7–10). Idempotency key prevents doubles.
**Spec (verified via PostgREST OpenAPI):**
- Required: `p_idempotency_key` (text), `p_user_id` (uuid), `p_human_note`, `p_naya_note`, `p_machine_note`, `p_intelligent_feed`, `p_intelligent_block`, `p_evidence`, `p_hub_state` (all jsonb).
- Optional: `p_subject` (text). Note: no `subject` column exists on the target table — where it lands is UNKNOWN.
**Status:** RPC exists. The pump (#2680, hourly schedule + heartbeat, re-validated 9.6) fires the workflow. ⚠️ The Blueprint mandates a `capture_inbox` table as the single entry — **it does not exist in the live schema** (see Decision D3).

## HOP 2 — PERSIST

**What:** durable home of the note + lineage.
**How:** RPC writes `v7_smart_note_transactions` (`id, idempotency_key, user_id, created_at, status, human/naya/machine_note, intelligent_feed, intelligent_block, evidence, hub_state, failure_stage, failure_message`) — params map 1:1 to columns. Lineage in `smart_note_artifacts` / `smart_note_events` / `smart_note_receipts`.
**Why this way:** transactions give idempotency + failure staging; artifacts/events/receipts give the audit trail.
**Spec — feed reads:** `nayanet_intelligent_blocks` (`block_id, title, content(jsonb), subject_id, block_type, version, status, understanding_state, owner_id, owner_scope, source_event_ids(uuid[]), evidence_refs, provenance, value_context, applicable_scope, connections(jsonb), search_vector, schema_version, created_at, updated_at, supersedes/superseded_by_block_id, intelligent_block_id`).
**Status:** tables exist. The link `v7_smart_note_transactions` → `nayanet_intelligent_blocks` is UNNAMED in schema and spec — **this is the exact gap blocking the feed loader.** Someone must name and build the promotion step.
**2026-11-17 (One Flow round):** the promotion step for the COMPOSER path is NAMED — **`promote_naya_note_to_feed`** (`naya_notes` with `category='Smart Note'` → `hub_smart_notes` full Intelligent Block row). Status: NAMED, NOT BUILT server-side. Until it lands, the Hub live read merges both tables client-side (see Hop 4), so no card waits on it. The v7 → blocks link remains unnamed.
**RLS (measured, anon):** transactions/artifacts/events/receipts/blocks/members → 200 with `[]` (SELECT grant present, rows RLS-filtered — zero anon policies, authenticated-only by design). `nayanet_smart_ledger` → **42501, anon has no SELECT grant at all.**

## HOP 3 — EMIT (GitHub, public lane)

**What:** turns Supabase rows into zero-auth feed files the pages can fetch.
**How:** `.github/workflows/hub-feeds-emit.yml` (hourly UTC + dispatch) runs `HUB/FEEDS/emit_hub_feeds.py`, which queries via the Management API **server-side only** (bypasses RLS by design — must never run client-side) and commits `HUB/FEEDS/today.json`, `lists.json`, `spaces.json` on real content diffs only (idempotent).
**Why this way:** zero-auth CDN serving with a full audit trail in git; the emitter holds the only RLS-bypass and stays server-side.
**Spec — feed envelope (room-feed/v1, verified from the diff):** `contract`, `room`, `emitted_at` (America/Los_Angeles = last *content* change, not last run), `source_ref`, `items[]`. Per-item required: `id`, `title`, `topics[]`, `kind`. today adds `priority, blocker, next_action, layers[]`; lists adds `list_id, members[], membership_rule`; spaces adds `space_id, pins[], posts[]`.
**Fetch:** `https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/HUB/FEEDS/<room>.json` with `{cache:'no-store'}` (until #2678 merges, these 404).
**Status:** PR #2678 open (re-validated 9.6). Fail-closed until `SB_API` repo variable + `SUPABASE_MANAGEMENT_TOKEN` secret are configured. 🛑 **BLOCKED on D4 (privacy) — see below.**

## HOP 4 — BRIDGE

**What:** the one pipe the page holds — lane-abstracted, so the page never cares which lane supplied the data.
**How:** `window.NayaPowerRuntime` (browser; `global.NayaPowerRuntime` in node) — verified character-for-character in `HUB/naya-power-runtime.js`. `NayaRuntime` exists only as the hub adapter's resolution fallback.
**Why this way:** one global, per-room named methods matching the page's METHOD_MAP; the adapter resolves and calls, the page never assumes a method exists.
**Spec — methods (verified from #2679's diff):** `intelligenceToday()` (+ aliases `dailyIntelligence()`, `today()`), signature `function(payload)` — payload accepted but ignored — returns a Promise of the envelope. ⚠️ **`smartFeed()` deliberately returns `{ok:false, state:'not_verified', message:'Smart Feed reads the canonical markdown wire; this bridge does not own it.'}` — there is NO Smart Feed accessor.**
**Spec — envelope:** `{ok, state, data}` where `state ∈ {ready (L0 live), cached (L1 localStorage fallback), empty (L2 empty-but-valid)}`; `data = {contract:'room-feed/v1', room, emitted_at, source_ref, items[], _feed_meta:{source, age_seconds, emitted_at, bridge_version}}`. No `method` field, no `runtime_connected` on success; accessors never return `'error'` (only the adapter's catch synthesizes it). `'not_verified'` appears only on stubs.
**Status:** PR #2679 open (re-validated 9.3). Graded fallback L0→L1→L2 genuinely coded, 23/23 harness tests.
**2026-11-17 (One Flow round) — D2 RESOLVED, and `smartFeed()` superseded for the PUBLIC feed:** PR #3173 (merged 2026-11-04, `fd5763fe`) did build the live-first attempt — `feedLiveFirst` → `roomData('feed')` → `NayaPowerRuntime.smartFeed` with fallback to the baked snapshot — and it is present in the Fix-5c Hub bytes (lines ~6642–6662). But `smartFeed()` can never succeed on the public page: the bundled `supabase-bridge.js` only registers `window.NayaPowerRuntime` when no runtime exists, and its `smartFeed()` needs `window.NayaBridgeConfig.supabaseRest` with an authenticated `memberId` + `accessToken`, which the public Hub page never injects (0 occurrences of `NayaBridgeConfig` set in the page; 0 `supabase.co`, 0 `createClient`, 0 `/rest/v1` in the Hub bytes). Every load therefore falls back to the baked snapshot — proven from the current bytes. **The wire, named and built this round:** Supabase-direct anon REST read of `public.hub_smart_notes` (order `created_at` desc, limit 200) + `public.naya_notes` (`owner_alias='flagship-personal'`, `category='Smart Note'`, limit 100), merged newest-first, polled every 15s, re-pointing the SAME seam the feed-live.json override uses (`window.NayaFeedIntelligence`, ref `'live-supabase'`). The anon key is the public client key the Personal page already ships. No member session, no deploy injection, no re-bake. `smartFeed()` remains the accessor for authenticated rooms; the public feed no longer waits on it.

## HOP 5 — RENDER

**What:** the page loader — takes the bridge's envelope and renders Smart Note cards in the page's format.
**How:** against the bridge contract above; never assumes a method exists, never upgrades missing data into READY (in-file law).
**Status:** ❌ NOT BUILT. Receiver-ready workstream launched (board). Blocked on D1 (seam name — now resolved: `NayaPowerRuntime`, verified) and D2 (the Smart Feed wire — see below).
**2026-11-17 (One Flow round):** BUILT. The live-read block (one new `<script>` in `HUB/app/index.html`, +10,296 bytes, branch `smart-feed/one-flow-20261117`) re-points `window.NayaFeedIntelligence` from the live tables; the harvested feed room, `liveNoteFromCard`, `intelBoard`, solo-note view, and provenance line work unchanged. The provenance banner flips to live truth (`Live intelligence · N notes · newest Xm ago · backend: supabase-direct · checked HH:MM:SS`); a failed read goes LOUD on the same line and in `window.NayaLiveFeed` (`{ok, error, at}`), and the baked snapshot stays as the honest fallback only.

## HOP 6 — ARCHIVE

**What:** every note filed to GitHub under date partitions, async, non-blocking.
**How:** writer TBD — the async GitHub file-filing writer is specified in the Blueprint as missing.
**Status:** ❌ NOT BUILT.

## HOP 7 — MEASURE

**What:** the compiler watches the loop and reports.
**How:** hourly probes → `HUB/MAP-STATE.json` → schematics + Hub Home health strip. Loud `unknown`, never fake green.
**Status:** PR #2687 open (fixes pushed, re-validated). The contract's done-states are what the probes check: capture ran? rows persisted? feeds fresh? bridge present? rooms live or seeds?

---

## OPEN DECISIONS (must resolve — flagged, not buried)

**D1 — Seam name: RESOLVED.** `window.NayaPowerRuntime` — verified in code. The Blueprint's `window.NayaRuntime.roomData(roomId)` and the nonexistent `roomData` method are superseded; Blueprint needs the correction.

**D2 — The Smart Feed wire: NO OWNER.** The bridge refuses it, the emitter doesn't emit it, and "the canonical markdown wire" is unspecified. **This is Goal #1's missing piece.** Recommendation: emitter adds the feed-room file from `nayanet_intelligent_blocks` + bridge adds the feed accessor (GitHub lane + Hub lane). Needs a decision, then an owner.
**2026-11-17 — RESOLVED by the One Flow round (maker's decision, per brief §9):** the wire is the Supabase-direct anon REST read (see Hop 4). The emitter + bridge-accessor path was NOT chosen: it needs an authenticated session the public page never has. The decision was decided by the acceptance test — the card lands in seconds on the staged proof with no redeploy and no re-bake.

**D3 — Capture canonical: inbox vs v7.** Blueprint mandates `capture_inbox`; reality runs the v7 RPC pipeline. Recommendation: bless v7 as the capture transport (it works), build the inbox as the unified front door that writes *through* v7 (one entry for humans/rooms/systems, no second pipeline). Engine/team to confirm.

**D4 — PRIVACY: RESOLVED by doctrine (2026-10-16).** Shawn: "I didn't make a privacy decision — just make the smartest choice." The answer: there was never a decision to publish private rows, so the default holds — `owner_scope=PRIVATE` rows are excluded from ALL public emitter output ("personal rows never touch git"). Not a new rule; doctrine enforced. Patch drafted + posted to #2678 (comment 6210481464): `WHERE owner_scope != 'PRIVATE'` on emit_lists, validator relaxed for legitimately-empty feeds. Residual gap flagged honestly: `nayanet_intelligence_index` + `smart_note_artifacts` (today/spaces feeds) have NO scope column — team must confirm public-by-purpose or add one before the emitter is fully D4-clean.

**D5 — Transport liveness: UNKNOWN.** Real-time could not be verified (admin endpoints reject the available key). The "lands in seconds" acceptance currently has no verified transport — hourly CDN polling is not seconds. Verify Supabase real-time or name the actual live path.
**2026-11-17 — RESOLVED (measured, not realtime):** the transport is HTTPS polling every 15s against the live tables. No Supabase realtime broadcast is used or claimed. "In seconds" = poll interval (15s) + REST round-trip (~1s) + render (<1s); the timed browser runs in the maker report measure the real elapsed times.

**Minor:** spaces.json pre-empts build-order step 7 (design-first) — reconcile; today-source (index+artifacts) vs "v7 reports area" naming — reconcile; `p_subject` landing — clarify.

---

## SENDER → RECEIVER MAP (the plumbing, hop by hop)

| Sender | Sends | Via | Receiver | Receives | Status |
|---|---|---|---|---|---|
| Shawn ("smart note this") | lesson text | chat → inbox (to build) | capture inbox | a row to drain | ❌ inbox missing |
| pump (#2680) | payload_json | workflow dispatch | capture workflow | a run | 🟡 PR open, 9.6 |
| capture workflow | canonical note | v7 RPC | Supabase | persisted rows | 🟢 RPC live |
| promotion (UNNAMED) | intelligent block | — | nayanet_intelligent_blocks | feed-ready rows | ❌ unbuilt |
| emitter (#2678) | feed JSON | git commit → raw CDN | HUB/FEEDS/*.json | fetchable files | 🟡 PR open, D4 resolved (PRIVATE rows excluded) |
| bridge (#2679) | envelope | window.NayaPowerRuntime | page loader | {ok,state,data} | 🟡 PR open |
| page loader | cards | DOM | the Hub page | rendered notes | ❌ unbuilt (D2) |
| compiler (#2687) | MAP-STATE.json | hourly commit | health strip | live status | 🟡 PR open |

**The critical path to Goal #1:** D2 (feed wire owner) → promotion step → loader → D4 resolved → merges → deploy (Shawn's gate).
**2026-11-17 (One Flow round):** D2 is resolved (wire built, this round). The promotion step is named (`promote_naya_note_to_feed`) and bridged client-side; building it server-side is the follow-on. Merge/deploy remain Shawn's tap.

---

## 2026-11-17 — MEASURED LIVE STATE (One Flow round, maker seat)

All of this was measured live on 2026-11-17 ~16:23–16:28Z with the anon role (PostgREST), not taken from files:

- **`naya_notes` anon INSERT SUCCEEDS.** `POST /rest/v1/naya_notes` → HTTP 201, rows read back by id. The 42501 refusal Break 3 records no longer holds. Probe rows created while re-proving it (cannot be deleted by anon — DELETE is refused 42501, see below): `9b88a7be-4a35-42f1-8edc-fe868bbe0d23` (16:23:08Z) and `f44b3601-3c07-4b28-b56d-b2dc09dcd22a` (16:23:18Z), both titled "ONE-FLOW VERIFICATION PROBE — maker seat 2026-11-17 (expected refusal)". The filed SQL (`SUPABASE-NAYA-NOTES-INSERT-20261117.sql`) records the policy definition idempotently + the risk; it is NOT applied by this round.
- **`naya_notes` anon DELETE is refused** — HTTP 401, code 42501, "permission denied for table naya_notes". That refusal is load-bearing (it is why the probe rows need the service key to clean up).
- **`hub_smart_notes` anon INSERT SUCCEEDS** (HTTP 201) and anon SELECT returns rows. Acceptance note #1 (chat entry) landed there 2026-11-17T16:24:45Z, id `f85b1148-66ca-4a96-924b-befb74798198`.
- **The composer save route WORKS.** `POST https://naya-save-staging.nayapower.workers.dev/api/personal/save` with the exact composer payload → HTTP 200 in 0.90s, `naya_note` id `ef5e4184-c2d6-4c99-8f54-c0901e06a088` (acceptance note #2, 2026-11-17T16:25:40Z). The composer never used the direct insert — it POSTs to this server route ("PERSONAL SAVE ONE-ROUTE").
- **Save on a Hub card is device-local.** Top-actions SAVE/FAVORITE write `localStorage` (`naya.smartlist`, canonical id/title/topics) + toast "Saved on this device." A fresh profile reads back nothing. The shared-library save (library_qa save-worker patch) is written and still awaiting Shawn's hand to deploy — that is the unblocker for acceptance step 5, not this round.
- **Play exists on Hub cards** (`NayaVoice`: `speechSynthesis` + baked-audio worker fallback; layer play buttons call `NayaVoice.playSections`/`play`). "Heard" needs a live browser ear — the maker proves the mechanism, the checker hears it.
- **Share mints a working link at share time** for a live note: the Hub share dialog shows `#/smart-notes/<full-ib-id>` when no `snNNNN` key exists (the solo-note view resolves the full id from the live-fed `NayaFeedIntelligence`). The `/s/` short link arrives only after GitHub filing + sync minting — not claimed for fresh notes.
- **D4 note:** `naya_notes` carries no `owner_scope` column. The live read surfaces ONLY `category='Smart Note'` rows for `owner_alias='flagship-personal'` — the explicit share act (filing a note AS a Smart Note). Adding `owner_scope` to `naya_notes` is the follow-on hardening; until then the category gate is the filter, recorded here.
- **Re-bake status:** IRRELEVANT to cards now (the live read bypasses it), proven by the staged proof: the acceptance notes are NOT in the baked bytes and render anyway. The re-bake still feeds `feed-live.json` (the fallback) and the sync still archives to GitHub — neither is in the card path anymore.

---

*Aligned with the master directive (mission: prove the brain learns) and measured by the compiler. When reality changes, this file changes first.*
*Research sources: PR #2679 diff (naya4/nayapower-runtime-t0480), PR #2678 diff (naya4/hub-feeds-emitter-t0479), Supabase PostgREST OpenAPI (22 definitions), GitHub App API (ID 5198315), index-2.html. Every spec above was read from these; unknowns are marked.*
