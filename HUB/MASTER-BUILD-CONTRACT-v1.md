# HUB MASTER BUILD CONTRACT v1

**Status:** DRAFT — for team review. Not merged. Not ratified. Never merge without the 3-pass receipt.
**Author seat:** Naya Clarity Narzan (Naya 4), 2026-10-16 ~00:30 PDT, at Shawn's word: *"write the contract for the hub… this is what you need to do, this is how you need to do it, this is why you need to do it that way, here's the specs, here's everything."*
**Deep-dive basis:** every claim in §3 was verified from live bytes on 2026-10-16 (Supabase management API, GitHub REST, git protocol, the shipped page files). Where an earlier claim was corrected, it says so plainly.

---

## 0. NUTSHELL

The Hub is twelve rooms. Today every room is a static island — baked data, on-device saves, nothing arrives from anywhere. This contract builds the one synchronized system: **capture → pump → Supabase → realtime → bridge → Hub room**, with **GitHub as the canonical archive leg** (reports, ledger, notes at rest) and the **GitHub App as the archive/event relay** (never the hot path). When it's built, saying *"smart note this"* puts a playable, savable, shareable Smart Note card on the live Hub within sixty seconds — and every other room follows the same contract pattern until all twelve breathe the same air.

---

## 1. WHAT — the target state

1. **Goal #1 works:** Shawn says "smart note this" about a lesson → it appears on the Hub Smart Feed as a Smart Note card → he can read it, play it, save it, share it. Sixty-second target, timestamped at capture, persistence, bridge receipt, and render.
2. **Every sync-data room is contract-fed:** Smart Feed, Reports, Today, Smart Ledger, and the main-page Activity Feed all load from the bridge, not from baked snapshots.
3. **Every remaining functional room gets the same plumbing:** receiver contract defined → page made bridge-ready → sender lands on a ready socket → no localStorage-only islands, no sender without a receiver, no page waiting on a future sender before its receiving side is prepared.
4. **One writer per path.** The pump writes notes. The report pipeline writes report events. The ledger sync writes ledger rows. Nobody else writes those paths.
5. **Honest states everywhere:** when the bridge is down or empty, the page says so — never a fake "live" shimmer over dead data.

---

## 2. WHY — why it must work this way

- **Humans experience this first.** The Hub is the first thing a human touches. A dead Hub teaches the human the system is a demo; a living Hub teaches her the system is real.
- **Supabase is the hot path because the Hub is a living page.** A human staring at a page needs data that *arrives*. GitHub is versioned truth at rest — perfect for archive, wrong for a 60-second render. So: Supabase carries the live pulse; GitHub carries the canonical record. Each does what it's built for.
- **The App is the relay, not the road.** The GitHub App moves archive material and emits events (report published, note archived). Putting the hot path through webhooks would add a hop, a failure mode, and a latency tax to the one flow humans feel first.
- **Contract-first because twelve rooms can't integrate by vibes.** Every room's receiver is frozen *before* its sender is built. The receiver contract is the law the sender obeys. This is how twelve rooms stay one system instead of twelve integrations.

---

## 3. DEEP-DIVE FINDINGS — verified from live bytes, 2026-10-16

### 3a. Supabase — the shelves are stocked, the bell is disconnected

- Project `supabase-red-cable` (`dahisasgpfvziswqvmvm`, ca-central-1): **ACTIVE_HEALTHY** — verified via management API.
- 22 tables in `public`, including `nayanet_smart_ledger`, `smart_note_events`, `smart_note_receipts`, `smart_note_artifacts`, `nayanet_intelligent_blocks`.
- **CORRECTION:** an earlier drive reported "tables exist, zero rows." Live count: **381 ledger rows, 27 note events, 27 receipts, 108 artifacts, 191 blocks.** The shelves are NOT empty — data was written, then the writing stopped.
- Freshest ledger write: **2026-10-15 18:41 UTC** (~12.5 hours stale at contract time). The write path is silent.
- The `supabase_realtime` publication **exists but contains ZERO tables**. Realtime broadcasts nothing. This is the single mechanical reason nothing live reaches any page.
- **Pump:** PR #2691 is a DRAFT titled "schedule plumbing for agent capture (review only, do not merge)." There is no real-payload pump. Capture inbox for "smart note this" does not exist.

**Supabase verdict:** storage works, history exists, the live wire is cut in two places — empty realtime publication + silent write path.

### 3b. GitHub — the archive leg flows, the event leg is missing

- The director's mission-snapshot + NAYANET ledger sync to `naya/mission-state` runs every tick — `LEDGER/activity-ledger.jsonl` lands on GitHub continuously. **The archive leg is alive.**
- Report canonical paths exist in the repo (daily/weekly/monthly/yearly). **Report-created event emission does not exist** — nothing announces a new report to the bridge.
- The GitHub App: installation could not be verified via API on this pass (the installation endpoint requires JWT auth this seat doesn't hold). **Open item:** verify installation + subscribed events. Its scoped role is archive/event relay (see §4.3) — it is NOT on the hot path, so this verification does not block Goal #1.

### 3c. Hub pages — all static, verified from their own bytes

- Main page (`index-8.html`, 521 KB): Smart Notes are a baked 2026-10-02 snapshot; saves go to `localStorage` (`naya.activity`); its own code says *"no backend."* Bridge seams exist as names only.
- Reports page (180 KB): reports are `RAW_MD` strings baked in; no bridge seam; localStorage only tracks visit badges.
- Today page (482 KB): baked intelligence; Smart List in `localStorage` (`nayanet.today.smartlist.v1`); no bridge seam.
- Ledger page (166 KB): `LedgerAdapter.demoStream()` + baked `PACKS.realReceipts` with `simLive:true` — its "live" is simulated. The real stream (`LEDGER/activity-ledger.jsonl`, syncing to GitHub every tick) is not connected to it.

**Pages verdict:** specified ≠ implemented. The two receiver-contract documents (Smart Feed v1, Symphony v1) are proposals on paper — no receiver code is installed in any page.

---

## 4. HOW — what to build, component by component

### 4.1 SUPABASE — reconnect the bell, restart the writing

**What:** make live data arrive.
**How:**
1. `ALTER PUBLICATION supabase_realtime ADD TABLE public.smart_note_events, public.smart_note_receipts, public.smart_note_artifacts, public.nayanet_smart_ledger, public.nayanet_intelligent_blocks;` — the tables that feed Hub rooms join the broadcast. (SQL change, reviewable in one PR. Protected: needs Shawn's word only if it touches credentials — it doesn't; it's schema config.)
2. Restart the write path: the pump writes real rows on capture. Until the pump exists, a manual insert is the smoke test — one row, then watch it arrive.
3. Row-shape → bridge mapping (§5): the bridge reads rows and emits receiver-contract blocks. The table schema is the sender's raw material; the receiver contract is the law — the bridge translates, never the page.
**Why this way:** the publication is the entire difference between "database" and "live database." One statement turns 381 silent rows into a stream. No new infrastructure, no new service, no new bill.

### 4.2 GITHUB — keep the archive leg, add the event leg

**What:** GitHub stays the canonical record and gains event emission.
**How:**
1. **Keep:** the `naya/mission-state` ledger sync (director-owned, runs every tick). Do not touch what flows.
2. **Build:** on every report publish, emit `INTELLIGENCE_REPORT_CREATED` (shape in §5) — a small emitter in the report pipeline that writes the event where the bridge listens (Supabase `smart_note_events` or a dedicated `report_events` table — bridge team decides, one writer).
3. **Build:** Smart Note archival — when a note is captured, its canonical markdown lands in the repo under the notes tree (the existing `SN-01458+` staging pattern), so GitHub holds the record even if Supabase is ever wiped.
**Why this way:** GitHub is where the team lives and where history is provable. Events are cheap rows; the bridge already watches tables. Archive and event are the same write, two readers.

### 4.3 GITHUB APP — the relay, scoped and boring

**What:** verify it, scope it, keep it off the hot path.
**How:**
1. Verify installation + subscribed events (open item, owner: Team Nitro — they hold the data-layer contract).
2. Its jobs: (a) relay `INTELLIGENCE_REPORT_CREATED` as a repository dispatch for archive-side consumers; (b) confirm note-archive commits landed; (c) expose the ledger stream to external consumers later.
3. It NEVER sits between capture and the Hub page. If the App is down, notes still reach the Hub. The hot path is capture → pump → Supabase → realtime → bridge → page. Full stop.
**Why this way:** every hop on the human-feeling path is a place the 60-second promise can die. The App does valuable work where latency doesn't matter.

### 4.4 THE PUMP — the missing machine

**What:** turn "smart note this" into a real payload, fast.
**How:**
1. Capture inbox: a single intake (chat command + API endpoint) that accepts the lesson text + speaker + timestamp. One writer.
2. Payload builder: emits the Smart Note block (shape in §5) — all six layers (essence, meaning, connections, for-you, apply, lesson), room routing (`smart-feed`, plus `today` nutshell projection).
3. Write: insert into Supabase (`smart_note_events` + `smart_note_receipts`), then archive to GitHub. Insert first (hot path), archive second (can lag).
4. First acceptance: a hand-written payload inserted manually must render on a bridge-ready test page before the pump is declared working.
**Why this way:** PR #2691 proved schedule plumbing is not a pump. The pump's only job is payload — everything else is ceremony.

### 4.5 THE BRIDGE — the translator

**What:** turn stored rows into receiver-contract blocks and serve the rooms.
**How:**
1. Implement to the two frozen receiver contracts (Smart Feed v1, Symphony v1 — linked in §5). The contract is the spec; no improvisation.
2. Subscribe to the Supabase tables (§4.1); on insert/update, translate the row to the contract block and push to subscribed rooms.
3. Room loaders: each page gets a loader that calls the bridge, renders blocks, and shows the honest empty/offline state. Smart Feed first.
4. Contract-amendment guardrail: once a receiver contract is frozen, changes need a version bump + a migration note — never a silent shape change under a running page.
**Why this way:** the bridge is the only component allowed to know both the database shape and the page shape. Pages stay dumb and honest; the database stays raw; the bridge owns the translation. One translator, twelve rooms.

### 4.6 HUB OUTPUT — the twelve rooms, made bridge-ready

**What:** pages that receive.
**How, per room:**
1. Receiver contract frozen (done for Smart Feed, Reports, Today, Ledger, Activity — §5).
2. Page modified: bridge-backed loader replaces baked data; localStorage becomes cache/fallback, never the source of truth; honest empty/offline state.
3. Sender lands on the ready socket (pump → Smart Feed; report emitter → Reports; note nutshell → Today; ledger sync → Ledger; local activity + opt-in sync → Activity Feed).
4. Room-by-room acceptance (§9), then the same pattern rolls to the remaining rooms (§6).
**Why this way:** a page that can't receive is a page the system can't talk to. Making every room bridge-ready first means no sender is ever built for a deaf room.

### 4.7 REDEPLOY — Shawn's word, then the lights come on

Production deploy/redeploy is a protected gate. The team preview host is down; restoring it needs his explicit word. Nothing in this contract routes around that. The contract builds everything up to the gate; he opens it.

---

## 5. THE SPECS — payload shapes (the law)

Frozen receiver contracts (proposals awaiting install — specified, not yet implemented):
- Smart Feed receiver contract v1 — the Smart Note block: `{id, title, subtitle, topics[], topic, tone, icon, kind:"smart-note", layers[{name,key,color,tier,body}]}` with deeper keys `meaning | connections | for-you | apply | lesson`.
- Symphony receiver contracts v1 — Reports (`INTELLIGENCE_REPORT_CREATED`: `{event, report_id, ib_id, period, period_date, title, nutshell, canonical_path, commit_sha, scope, created_at}`), Today (`{date, title, nutshell, truth:"CANDIDATE", kind, words}`), Ledger (GitHub `LEDGER/activity-ledger.jsonl` stream via bridge — replace `demoStream()`), Activity Feed (personal activity: loves/saves/plays; local by default, cross-device only with explicit consent).

**Amendment guardrail:** frozen means frozen. A change = version bump + migration note + both sides updated. Silent shape drift is a breach.

---

## 6. ROOM ROLLOUT MATRIX — the same concept, every room

| # | Room | Receiver contract | Sender | GitHub-send | State |
|---|------|-------------------|--------|-------------|-------|
| 1 | Smart Feed | v1 frozen (proposal) | Pump (§4.4) | Note archive | RECEIVER NOT INSTALLED — first build |
| 2 | Reports | v1 frozen (proposal) | Report emitter (§4.2.2) | Canonical report paths exist | EMITTER NOT BUILT |
| 3 | Today | v1 frozen (proposal) | Note nutshell projection (pump) | — | RECEIVER NOT INSTALLED |
| 4 | Smart Ledger | v1 frozen (proposal) | Ledger sync (flows) → bridge | `LEDGER/activity-ledger.jsonl` flows every tick | SENDER FLOWS; RECEIVER NOT INSTALLED |
| 5 | Activity Feed (main) | v1 frozen (proposal) | Local activity + opt-in sync | — | RECEIVER NOT INSTALLED; consent path owed |
| 6–12 | Remaining rooms | TO WRITE — same pattern | TBD per room | TBD | CONTRACTS OWED |

Rule, universal: **no sender without a receiver, no receiver without a contract, no contract without a version.**

---

## 7. WORKING TRACKER — the working file of the working system

This table is the live checklist. It moves only on evidence (commit SHA, PR link, observed timestamp) — never on claims.

- [ ] **T1.** Realtime publication carries the five tables (§4.1.1) — evidence: `pg_publication_tables` query output
- [ ] **T2.** Manual smoke row inserted → observed arriving via realtime — evidence: timestamps
- [ ] **T3.** Capture inbox accepts "smart note this" — evidence: endpoint + test capture
- [ ] **T4.** Pump emits full six-layer Smart Note block — evidence: sample payload
- [ ] **T5.** Pump writes Supabase rows (hot) + GitHub archive (leg) — evidence: row id + commit SHA
- [ ] **T6.** Bridge implements Smart Feed receiver contract — evidence: repo path + tests
- [ ] **T7.** Smart Feed page bridge-ready (loader replaces baked snapshot) — evidence: branch + observed render
- [ ] **T8.** 60-second test passes: capture → card on Hub — evidence: four timestamps
- [ ] **T9.** Report emitter emits `INTELLIGENCE_REPORT_CREATED` — evidence: event row + bridge receipt
- [ ] **T10.** Reports page bridge-ready — evidence: branch + observed render
- [ ] **T11.** Today page bridge-ready (nutshell projection) — evidence: branch + observed render
- [ ] **T12.** Ledger page bridge-ready (real stream replaces `demoStream()`) — evidence: branch + observed render
- [ ] **T13.** Activity Feed bridge-ready (local-first, consent-gated sync) — evidence: branch + consent flow
- [ ] **T14.** GitHub App installation verified + scoped to relay role — evidence: installation id + event list
- [ ] **T15.** Remaining rooms: contracts written, receivers installed — evidence: per-room PRs
- [ ] **T16.** Production redeploy — **PROTECTED: Shawn's word** — evidence: live URL + observed pass

---

## 8. ALIGNMENT — how this contract steers the whole team

1. **All teams see it here.** This file is the canonical contract, on a reviewable branch. The live board (#2641) carries the announcement + the build order. No seat works from a summary — the contract is the orders.
2. **The master directive carries it.** The director folds this contract's tracker into the live plan's TOP-10 on the next pass; the compiler (`master_directive.py`) carries those priorities into the master directive (#2601) — the one artifact every lane tunes into. (Note: #2601 currently shows HAND_EDIT_DETECTED — the lead reconciles the hand edit; the compiler never clobbers it.)
3. **The mission snapshot broadcasts it.** `BRAIN/CURRENT-MISSION-STATE.md` on `naya/mission-state` carries the contract link + tracker state every tick — every cold-starting Naya reads it first.
4. **One writer per path, always.** Pump, report emitter, ledger sync, bridge — each path has exactly one owning seat. Collisions are a breach of this contract.

---

## 9. ACCEPTANCE — how we prove it, not claim it

- **Per room:** the 60-second test (or room-equivalent): real input → observed on the live page → read/play/save/share verified → four timestamps recorded.
- **System-in-sync test:** one capture produces the Smart Feed card, the Today nutshell, the ledger entry, and the GitHub archive — four surfaces, one truth, no drift between them.
- **Honesty test:** with Supabase unreachable, every room shows its offline state — no fake live, no silent empty.
- **Done words:** specified ≠ implemented ≠ merged ≠ deployed ≠ observed ≠ verified. A tracker box checks only on the evidence named beside it.

---

## 10. OWNERSHIP & GATES

- Contract steward: Naya Clarity Narzan (Naya 4). Amendments come as PRs against this file — never drive-by edits.
- Data-layer contract: Team Nitro (per Shawn's 2026-10-15 assignment).
- Protected gates (Shawn's explicit word, never inferred): production deploy/redeploy, credentials/money, destructive actions, privacy/consent changes (Activity Feed cross-device sync), ratification.
- Budget: the whole team shares ~2,500 actions/month. The contract is sequenced so the cheapest mechanical steps (T1: one SQL statement) come first — value per action, always.
