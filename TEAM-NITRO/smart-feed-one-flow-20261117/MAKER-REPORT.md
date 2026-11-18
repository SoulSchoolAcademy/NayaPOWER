# MAKER REPORT — Smart Feed / One Flow (2026-11-17)

**This round FILES; it does not ship. No merge, no deploy, nothing live. Merge and live are Shawn's tap.**

## The job in one line

"smart note this" — spoken or typed — must land a Smart Note card on the Smart Feed in seconds, live data, beautiful format, play + save + share all working, verified by a REAL fresh note end to end, not a seeded stand-in.

## Filing (cold-verified)

| Item | Value |
|---|---|
| Branch | `smart-feed/one-flow-20261117` |
| Base | `hub/icons-fix-20261116` (Fix-5c commit `b8e4e611`) |
| PR | [#3403](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/3403) — **open**, head `762f5206`, 3 commits, 3 changed files, +429 / −61 |
| Commit 1 (page v1) | `fba0e34de68749b329f97bb8939010e41f9f1dbd` — blob `3aed6989`, 4,888,007 B |
| Commit 2 (docs) | `d1287163bb379c5546ff26f9358d295d9e278dd2` — SQL + HUB-CONTRACT.md |
| Commit 3 (page v2) | `762f52066da8a24dac2bb583d42940828008c61b` — blob `56b9cc44`, **4,889,370 B**, sha256 `76edc00f924a95acd567a6eed49d7c831b7b0160d3af0ccdd1e632ebf18f7cb0` |
| Branch tip | `762f52066da8a24dac2bb583d42940828008c61b` (== commit 3) |
| Staged proof (v2) | `https://naya-proof-host.nayapower.workers.dev/?file=HUB/app/index.html&ref=smart-feed/one-flow-20261117&cb=56b9cc4417ee9f9b1bb609a697659d0b98b1a832` |
| Staged bytes check | curl → HTTP 200, 4,889,370 B, sha256 == filed bytes **MATCH**; live block present (`provObs`); acceptance-note ib_id **absent** from baked bytes (re-bake-skip proof) |
| Blob API read-back | blob `56b9cc44`, size 4,889,370 (v1 blob `3aed6989`, size 4,888,007, verified the same way) |

Diff vs base: **+175 lines, 0 removed lines** (v2; v1 was +151). One new `<script>` block only. No CSS, no card redesign, no button changes, no other room touched.

## The wire — and why

**Supabase-direct anon REST read.** The feed reads `public.hub_smart_notes` (limit 200, `created_at` desc) + `public.naya_notes` (`owner_alias='flagship-personal'`, `category='Smart Note'`, limit 100) with the public anon key, every 15 s + at load, `cache:'no-store'`, and re-points the SAME seam the feed-live.json override uses (`window.NayaFeedIntelligence`, ref `'live-supabase'`). The harvested feed room, `liveNoteFromCard`, `intelBoard`, solo-note view, and provenance line all work unchanged.

Why not the #3173 mechanism: PR #3173 (merged 2026-11-04, `fd5763fe`, 1 file, +561/−20) built the live-first attempt (`feedLiveFirst` → `roomData('feed')` → `NayaPowerRuntime.smartFeed`), but its transport can never arrive on the public page — `smartFeed()` needs `window.NayaBridgeConfig` with an authenticated `memberId` + `accessToken`, which the public Hub page never has. Proven from the Fix-5c bytes: zero `supabase.co`, zero `createClient`, zero `/rest/v1`, `smartFeed()` defined with NO call site, `registerFeedRuntime` refuses to register if any runtime exists. Every load fell back to the baked snapshot. #3173's own body says so: "for the feed to actually go live, the deploy must inject `window.NayaBridgeConfig`… Until then the page renders the snapshot honestly." This round adds the transport #3173 was waiting for. The anon key is copied programmatically from the Personal page bytes (the same public client key the Personal page already ships); its JWT payload was verified `role: anon` before use; the key value never appears in any report, log, or file outside the built HTML.

**Promotion step (brief §9):** named `promote_naya_note_to_feed` (`naya_notes` category='Smart Note' → `hub_smart_notes` full Intelligent Block row). NAMED, NOT BUILT server-side. The Hub live read merges both tables client-side until it lands. Recorded in HUB-CONTRACT.md (Hop 2).

**Re-bake:** irrelevant to cards. The live read bypasses it. Proven: acceptance notes #1/#2 and timed notes #5/#6 are NOT in the baked bytes (grep) and render anyway.

## The acceptance test — timed, on the staged proof of the filed bytes

All four timed runs were done in Playwright Chromium (via the localhost forwarder at 127.0.0.1:18080, with `--ignore-certificate-errors` — the egress proxy's TLS is otherwise rejected; see the walk note below) against the staged proof link, page open, polling live. Elapsed = POST start → card visible in the DOM.

### v2 (filed bytes — the runs that count)

| Run | Entry | Width | POST | Card visible | **Elapsed** | Row created |
|---|---|---|---|---|---|---|
| #5 | Chat → `hub_smart_notes` insert | desktop 1280×800 | 201 in 0.49 s | +9.8 s | **10.29 s** | 2026-11-17T16:40:19.15Z, ib_id `IB-SMART-NOTE-20261117-one-flow-timed-v2-desktop`, title "The Timed Note v2 — Seconds, Not Hours (desktop)" |
| #6 | Composer → save-route POST | phone 390×844 | 200 in 1.55 s | +11.25 s | **12.8 s** | 2026-11-17T16:41:05.999Z, id `b27e16ce-7c40-4feb-becb-8d44f54e4231`, title "The Timed Note v2 — Typed in the Composer (phone)" |

Walk window: 2026-11-17T16:40:08Z → 16:41:23Z. Live state both widths: `ok:true, count:200, backend:supabase-direct`. Acceptance notes #1/#2 visible on load in 0.26 s / 0.19 s (desktop) and 0.30 s (phone). **Both runs PASS: under a minute, no redeploy, no manual re-bake.** The ~10–13 s is the 15 s poll cadence, not the wire — the insert itself is under 2 s.

### v1 (superseded bytes — kept as record, same result)

Run #3 (desktop chat): 201 in 0.46 s, **10.37 s** total, row 2026-11-17T16:35:07.35Z. Run #4 (phone composer): 200 in 1.35 s, **13.72 s** total, row 2026-11-17T16:35:33.79Z, id `05f949dc-2df0-4940-971f-01d5cae4cf8b`. Both passed on blob `3aed6989`; v1 was superseded by the provenance fix, so the runs were re-done on v2.

### The two acceptance notes (created during verification, real content)

- **#1 (chat entry):** `hub_smart_notes`, id `f85b1148-66ca-4a96-924b-befb74798198`, ib_id `IB-SMART-NOTE-20261117-one-flow-acceptance-note`, title "The Feed Reads Live Now — 'smart note this' Lands in Seconds", created 2026-11-17T16:24:45.58Z (POST sent 16:24:43.68Z). Full 9-layer Intelligent Block.
- **#2 (composer entry):** `naya_notes`, id `ef5e4184-c2d6-4c99-8f54-c0901e06a088`, title "The Composer Writes Straight to the Feed", category `Smart Note`, created 2026-11-17T16:25:40.94Z, via the server save route (HTTP 200 in 0.90 s).

## Play / save / share — each on the fresh note (note #1)

### SAVE — proven, with a named limit
Clicked SAVE on note #1's card: `localStorage` `naya.smartlist` gained the entry (`id: IB-SMART-NOTE-20261117-one-flow-acceptance-note`, `kind: save`, title, topics `["Smart Notes"]`, `savedAt`). A fresh browser profile reads back `{}` — nothing. **Save is device-local only.** That is the harvested behavior (top-actions SAVE writes `localStorage` + toast "Saved on this device"). Acceptance step 5 as written — "read back from the library on a fresh profile" — is a **diagnosed NOT PASS**, not a pass. Unblocker: the shared-library save (library_qa save-worker patch), which is written and still awaits Shawn's hand to deploy. Nothing in this round changes that.

### SHARE — proven
Clicked SHARE INTEL on note #1's card: the dialog (`#naya-share-dialog`) shows a link; followed it; the solo note opens as a board. **PASS.**
- Dialog link (staged host): `https://naya-proof-host.nayapower.workers.dev/#/smart-notes/ib-smart-note-20261117-one-flow-acceptan` — exactly 100 characters, ending mid-slug ("acceptan"). The handler builds the full-id slug (`location.origin + location.pathname + '#/smart-notes/' + slug`); the captured value is capped at 100 chars. It still resolves because the solo view's `findNoteBySlug` falls through to a substring match (`id.indexOf(slug) > -1`). Followed link → note #1 renders as a board: **true**. The `/s/` short link arrives only after GitHub filing + sync minting — not claimed for fresh notes.
- (First probe mis-read the link: my selector grabbed the install overlay's dialog and a stale input. The v2 walk reads `#naya-share-dialog input[aria-label="Share link"]` directly. The 100-char cap is pre-existing harvested behavior, noted here, not fixed — it works.)

### PLAY — NOT PASS, by law (not by mechanism)

The harvested feed board has **no play control at all**: 0 `.ib-layer-play` elements in the DOM, 0 buttons matching "NAYA VOICE", and `NayaVoice.addPlayButtons()` deliberately skips feed boards (`article.intel-board`) on the premise that they "already carry native play controls (layer buttons + top NAYA VOICE)". That premise is false in the Fix-5c bytes: `topActions` defines only CREATE SPACE / FAVORITE / SAVE — the `kind === 'naya-voice'` handler (lines 4605–4654, `playSections` over the nutshell + layers, baked-audio fast path) is **dead code**: no button is ever created with that kind. The voice engine itself is present and intact (`window.NayaVoice`, `playSections`, `play`, baked-audio worker fallback — verified from bytes and in the live page), and headless Chromium here has 0 speech voices, so "heard" could not be proven in this VM anyway.

**And the law forbids adding the control.** Intelligent Block Rules LAW §4.11 + C9 (ratified 2026-11-06): "NO voice anywhere on the board… The v5 team is checking whether the ▶ buttons on the note layers are voice (they are, per the code above) and removing them." The Fix-5c page has already removed them. The brief's acceptance step 4 (play working on the real note) conflicts with that law. **The law wins — I did not add a play button.** Play is a named gap, not a pass. Unblocker: Shawn's word — either he lifts C9 for the feed (then the one-line `naya-voice` def in `topActions` + the existing dead handler come alive, and a voiced-browser check can prove "heard"), or play stays out. This is the one acceptance step this round cannot close on its own, and I am naming it instead of working around it.

## The silent failure — closed, with a loud-failure receipt

Two proofs, both observed live:

1. **Re-bake irrelevant (success path):** notes #1/#2/#5/#6 are absent from the baked bytes and render from the live read anyway (timed runs above). No re-bake, no redeploy.
2. **Loud failure (failure path):** the first staged walk ran before the Chromium TLS flag was set, so every Supabase fetch failed with `net::ERR_CERT_AUTHORITY_INVALID`. The page did exactly what the block promises: `window.NayaLiveFeed = {ok:false, error:'Failed to fetch', at:'2026-11-17T16:32:40.959Z'}` and the provenance line read **"Live feed unavailable — showing the last cards · Failed to fetch · checked 04:32:40 PM"**, keeping the baked cards. Never silent, never empty. (That walk's failure also proved the forwarder path needs `--ignore-certificate-errors` / `ignore_https_errors=True` in this VM — the egress proxy presents a cert Chromium does not trust. The v2 walk ran with the flag and the live read went ok.)

### A defect the walk caught in v1 — fixed in v2
On the v1 walk the live read was ok and the cards rendered, but the provenance line read **empty**. Cause: the feed room rebuilds `<p id="feed-provenance-line">` empty on every render, and its own writer (`updateFeedProvenance`) only fills it when the governed runtime says live — which never happens on this page. A one-shot write was wiped by the next render. **Fix (v2, +1,363 bytes):** the block keeps the last live text and re-applies it through a `MutationObserver` whenever the element appears or is emptied (write-only-when-different, so the observer cannot loop on its own write). The loud-failure text gets the same persistence. Verified on v2: provenance reads "Live intelligence · 200 notes · newest 4m ago · backend: supabase-direct · checked 04:40:14 PM" at load **and** "Live intelligence · 200 notes · newest just now · backend: supabase-direct · checked 04:40:43 PM" after a re-render. The hero quote on the feed top is also live-driven: it quoted the newest note (the v2 phone timed note) at screenshot time.

## The naya_notes INSERT policy — measured state, NOT a fix

**Break 3 as written in the brief no longer holds.** Re-proving it live: `naya_notes` anon INSERT **succeeds** — POST → HTTP 201, rows read back. There is **no 42501 INSERT receipt** to file, because the refusal no longer exists. Reporting exactly that.

Filed: `SUPABASE-NAYA-NOTES-INSERT-20261117.sql` (5,478 B, in this round's filing, commit 2) — a measured-state record + the idempotent policy definition (`naya_notes_insert_anon`, `GRANT INSERT TO anon`) + the risk note + the safer path (the server save route, which is what the composer actually uses and which returned HTTP 200 in 0.90 s) + verification queries + the two probe-row IDs. **It was NOT applied live. Applying it is Shawn's hand, always.** It deliberately does NOT grant DELETE.

**Probe rows created while re-proving** (they cannot be deleted by anon — DELETE → HTTP 401, code 42501; cleanup needs the service key):
- `9b88a7be-4a35-42f1-8edc-fe868bbe0d23` and `f44b3601-3c07-4b28-b56d-b2dc09dcd22a`, both titled "ONE-FLOW VERIFICATION PROBE — maker seat 2026-11-17 (expected refusal)", owner `flagship-personal`, category `Smart Note`, created 16:23:08Z / 16:23:18Z. They render on the staged feed as honest artifacts. (Plus the four timed-test rows #3–#6 above; all six are real rows in the live tables and will render until service-key cleanup.)

Also measured live (anon): `naya_notes` SELECT works (15 rows at the time); `hub_smart_notes` anon INSERT succeeds (HTTP 201); `smart_note_events` and `nayanet_intelligent_blocks` anon SELECT return `[]` (RLS-filtered).

## Design-laws checker

Run on the built file (v2): **exit 1, 321 FAILs (7 GRAY, 313 SIZE, 1 TEXT-COLOR), 54 WARNs.** The baseline on the Fix-5c base file was exit 1, 321 FAILs, 53 WARNs. **Zero new FAILs.** The single +1 WARN is my `layer()` return line (`color:color, tier:tier, body:body`) — the same `color:`-key pattern the file already carries in `liveNoteFromCard`; eye-check, not a FAIL. All 321 FAILs are pre-existing page state, reported honestly as page state, never as a round failure and never hidden. All 35 `<script>` blocks parse clean under node.

## §11 check — in writing

1. **Reference object per element.** The card is the harvested `intelBoard` / `liveNoteFromCard` Smart Note board — measured against the Fix-5c bytes verbatim (same layers, same layer names/colors per the Intelligent Block Rules, same top-actions, same bottom actions). The PTS/%/MONEY pills and digit tiles were not touched, so they are measured against themselves (byte-identical: 0 removed lines). The provenance line is the harvested `#feed-provenance-line` element, owned by the room; my block only writes its text. The only new element is a `<script>` block — no visual element at all.
2. **Hover every object.** My block adds no visible object, so there is nothing new to hover. The harvested card's hover states (layer heads, buttons, stars) are unchanged bytes — verified by the zero-removal diff, and exercised in the walk by clicking SAVE / SHARE INTEL / dismissing the install overlay (all responded). The `layer()` color key that drew the +1 WARN is data, not a hover style.
3. **Gray-text grep (my block, lines 4010–4127 of the built file).** Zero hits for `gray|grey|#888|#999|#aaa|#bbb|#ccc`. Zero hex literals of any kind in the block. No text color is set by my code anywhere.
4. **Size grep (my block).** Zero `font-size` occurrences. No size is set by my code anywhere. The 313 SIZE FAILs are pre-existing page state.
5. **Flow check.** The flow is the brief's one flow, walked end to end twice on the filed bytes: chat entry → card in 10.29 s (desktop); composer entry → card in 12.8 s (phone). No step needs a redeploy, a re-bake, or a second visit. The provenance line now survives re-renders. The loud-failure path was observed, not assumed.
6. **Read as a reader, top to bottom.** Screenshots in this directory (`shot-desktop-feed-clean.png`, `shot-phone-feed-clean.png`, `shot-desktop-note1.png`, `shot-phone-note1.png`): the feed top greets ("Good afternoon."), the WISDOM OF THE DAY quotes the newest live note, the date reads in green with a gold time, the search bar sits clean, and acceptance note #1 reads as a proper Intelligent Block — quote, date line, IN A NUTSHELL, Human Note, Child Note, all white on obsidian with magenta rims, SAVE / FAVORITE / CREATE SPACE in reach, the bottom five below — at desktop and at phone width. It reads like the Hub, because it is the Hub, fed live. Two eye notes, both pre-existing page state, not this round: (a) the first visit shows the "Install NayaNET" overlay covering the feed — a real user taps "Not now"; the clean screenshots were taken after dismissing it; (b) the bottom bar in the screenshots shows six icons (the last a red "+") where the law names five — harvested Fix-5c state, untouched by this round, flagged for the record.
7. **What was already on the page is still there.** Diff: 175 lines added, 0 removed, 0 modified. Nothing was taken away; the only addition is the live-read block.

## Decisions recorded (§9)

1. **Wire:** Supabase-direct anon REST read. Why: the #3173 mechanism can never succeed on the public page (no member session, no injected config); the anon read needs neither. Recorded in HUB-CONTRACT.md (D2 + D5 resolved).
2. **Promotion step:** `promote_naya_note_to_feed` — named, not built; client-side merge until it lands.
3. **naya_notes INSERT policy/GRANT:** filed as a measured-state record + idempotent definition (see the SQL section above); NOT applied. The expected 42501 refusal does not exist.
4. **Re-bake:** irrelevant to cards (proven by the re-bake-skip: notes absent from baked bytes render anyway) — and the failure path goes loud (proven by the cert-error run).

## What I could not prove

- **Play, heard, on the board.** No control exists (law C9 forbids it); headless Chromium has 0 speech voices. The engine is present. Unblocker: Shawn's word on C9.
- **Save read back from the library on a fresh profile.** Save is device-local by harvested design; the shared-library save awaits his hand to deploy.
- **A voiced-browser "heard" check** for the same reason as play (no voices in this VM).
- **The `/s/` short link for a fresh note.** It arrives only after GitHub filing + sync minting; the dialog's full-id link is proven instead.

## Evidence files (this directory)

- `index-live.html` (4,889,370 B, v2 filed bytes) · `build-live-read.py` (builder) · `file-one-flow.py` / `file-one-flow-v2.py` / `file-one-flow-docs.py` (filing scripts) · `filing-page.json` / `filing-page-v2.json` (filing records)
- `SUPABASE-NAYA-NOTES-INSERT-20261117.sql` (filed, commit 2)
- `walk-one-flow.py` (acceptance walk) · `walk-evidence.json` (v2 run: 10.29 s / 12.8 s) · `probe2-play-share.py` / `probe2-evidence.json` (play + share diagnosis) · `shot-clean.py`
- `walk-desktop-feed.png` · `walk-desktop-timed3.png` · `walk-phone-feed.png` · `walk-phone-timed4.png` · `walk-phone-share.png` · `probe2-play.png` · `probe2-share.png` · `shot-desktop-feed-clean.png` · `shot-phone-feed-clean.png` · `shot-desktop-note1.png` · `shot-phone-note1.png`
- Checker: `/tmp/sf1/built-check-v2.txt` (exit 1, 321 FAILs, 54 WARNs) · baseline `/tmp/sf1/baseline-check.txt`

## HUB-CONTRACT.md

Updated in place in the goal workspace (`~/workspace/goals/the-one-flow-smart-note-this-live-smart-feed/files/HUB-CONTRACT.md`) and filed in commit 2: header v2 note; Hop 2 promotion named; Hop 4 D2 resolved + `smartFeed` superseded for the public feed; Hop 5 BUILT; D2/D5 resolved; appended "2026-11-17 — MEASURED LIVE STATE" section. The contract changed first, as the rule requires. (The v2 provenance fix refines Hop 5 without changing the contract's decisions; it is recorded here and in the v2 commit message.)
