# NayaPOWER Cold-14 Scorecard, Hole Register, and Ranked Execution

STATUS: CANONICAL EVIDENCE RECEIPT
DATE: 2026-09-26
SOURCE HEAD: 2846a5e6032380e03bf47e7ee3b6e47ed3d09efa (live `origin/main`, zero divergence)
CANONICAL HUB BLOB: 0c2b9381deda6db5935afc55c508d97a965ae412
CANONICAL REPO: SoulSchoolAcademy/NayaPOWER
METHOD: Cold restoration from canonical sources only. No answer was supplied from conversation.

---

## 0. TRUTH RESTORATION — the first real defect found

The canonical checkout `C:\Users\Admin\NayaPOWER` was **detached HEAD at `9b6568f4`**, one commit
behind live `origin/main`, while local `main` was **55 commits behind**. Every prior surface
assessment in that tree described a stale commit.

- Local `main` had **0 unique commits** and was a verified ancestor of `origin/main`, so a pure
  fast-forward was safe.
- The one modified tracked file (`supabase/functions/nayanet-github-dispatch/index.ts`) is
  byte-identical across `9b6568f4` and `origin/main`, so convergence was non-destructive.
- **Repaired:** attached to `main` and fast-forwarded to `2846a5e6`. 259 untracked files preserved.
- **Live main advanced a second time during this session** (`86eadb34` -> `2846a5e6`), proving that
  other agents commit concurrently. Live resolution at execution time is mandatory, not advisory.

FINDING: A cold Naya landing in the default canonical checkout would have reasoned about a
**55-commit-stale** tree while believing it was on main. This is the single highest-leverage
defect repaired in this session.

---

## 1. THE 14 QUESTIONS — answered cold, with evidence

| # | Question | Status | Evidence |
|---|---|---|---|
| 1 | WHO are we? | PROVEN | `STATE.json` mission + `.naya/TEAM-NAYA/00-NAYANET-HUB-NORTH-STAR-MISSION-LOCK.md` |
| 2 | WHAT are we building? | PROVEN | `STATE.json` + `MAP.json`; Hub = `NAYANET/HUB/index.html` |
| 3 | WHY are we building it? | PROVEN | `STATE.json.north_star` — max verified human value per unit effort, with compounding intelligence and continuity |
| 4 | WHAT does success mean? | PROVEN | `BLOCKS.json` HUMAN-JOURNEY-P2 acceptance; cold takeover is the open gate |
| 5 | WHAT is true right now? | PROVEN (live-resolved this session) | HEAD `2846a5e6`, Hub blob `0c2b9381…`, control plane coherent |
| 6 | WHAT has already been proven? | PROVEN AT RECORDED SCOPES | `PROOF.json`; 8/8 receiver dimensions PROVEN; 9/9 adversarial dimensions PROVEN (run 35787965745) |
| 7 | WHAT is unknown? | UNKNOWN | Universal computation savings; model/provider learning quality; human-path usability (see §3 H2, H3) |
| 8 | WHAT authority exists? | GOVERNED | `.naya/codex/11-RUNTIME-CONSTITUTION.md`; release needs explicit approval + protected environment + session lease |
| 9 | WHAT happened previously? | PROVEN HISTORY | `PROOF.json` + `NAYA/ACTIVITY/`; failures converted to evidence and repaired at causal boundaries |
| 10 | WHAT did we learn? | VERIFIED | Repair the smallest causal boundary and rerun the same proof; evidence outranks assertion |
| 11 | WHAT should happen next? | ACTIVE | Close the human path: identity + capture + deep link (H2, H3) |
| 12 | HOW do I prove it? | CANONICAL | Live browser acceptance at exact source identity, not a harness-only pass |
| 13 | WHERE do I record it? | CANONICAL | `.naya/control-plane/{STATE,BLOCKS,PROOF,BATON}.json` + `NAYA/ACTIVITY/` + receipts |
| 14 | HOW does the next Naya continue? | CANONICAL | `README-FIRST.md` -> `BATON.json` -> single next action -> successor packet |

### 1a. Challenge to our own harness — status inflation (real defect)

`.naya/runtime/cold_successor_test.py` PASSES at `2846a5e6` and prints `Proven: 11`. That number
is **inflated**. It counts `GOVERNED`, `PROVEN_HISTORY`, `CANONICAL_PROOF_METHOD`,
`CANONICAL_RECORDING_CONTRACT`, and `CANONICAL_SUCCESSOR_CONTRACT` as "proven", and each answer is
a **pointer to a source path, not a verified content claim**.

The harness proves the 14 questions are **addressable**. It does **not** prove the answers are true.
Our own law says `UNKNOWN is not VERIFIED`; the same discipline must apply to our own scoreboard.
Recorded as hole **H7**.

---

## 2. SCORECARDS (evidence-based, not claimed)

Scale: 10 = AAA. Acceptance threshold for the mission is 9.5.

### 2.1 Superbrain engine (canonical runtime + compounding loop)

| Dimension | Score | Basis |
|---|---|---|
| Canonical object model (Smart Note = Intelligent Block, one identity) | 9.5 | Contract ratified 2026-09-24; registry + resolver live |
| Event/Block/Index/Lineage machinery | 9.5 | IB V1 lifecycle run 35906051544 PROVEN; Ledger integration 35460477460 PROVEN |
| Learning + evidence + retrieval | 9.0 | Dream->learning->later-decision PROVEN; policy improvement PROVEN (3 held-out cases, 0->3) |
| Conversation -> intelligence entry | **4.0** | **Orphaned — see H1** |
| Compounding measurement | 6.0 | Bounded avoided-work unit proven; universal savings still UNKNOWN |
| **ENGINE TOTAL** | **7.6** | Strong core; broken entry point |

### 2.2 Setup / operating continuity

| Dimension | Score | Basis |
|---|---|---|
| Control-plane coherence (STATE/BLOCKS/BATON) | 10.0 | **Verified MATCH this session** — historical `STATE_BLOCK_NEXT_ACTION_MISMATCH` absent |
| Cold-14 addressability | 9.0 | Harness passes; content-truth caveat H7 |
| Offline verification suite | 7.5 | **11/12 real gates PASS this session**; 1 blocked by H1; no aggregate command; `supabase`/`requests` not installed |
| Canonical checkout hygiene | **4.0** | Was detached/stale — repaired this session; 259 untracked scratch files remain |
| Repository hygiene (worktrees) | 4.5 | 58 registered worktrees, 10 prunable `.rehab-*` inside the repo |
| **SETUP TOTAL** | **7.0** | |

### 2.3 Hub (human-facing surface)

| Capability | Verdict | Evidence |
|---|---|---|
| Shell / single owner | 9.5 | One shell, one left rail, run 35773282882 |
| Deep link `/hub?ib=` | 9.5 | Resolver L993-1069; live Worker contains `NayaHubDeepLink` + `retrieveIntelligentBlock` |
| Smart Feed render | 8.0 | Live path via `smart-feed.js`; static fallback of 9 blocks; count label says "3" on first paint |
| Smart Note capture | 8.0 | **Reachable** via Room 01 `CAPTURE INTELLIGENCE` -> `open-notes` -> `render('notes')` -> `saveNote()` |
| Room 01 "Intelligence Today" | 9.0 | 8-section honest cockpit; declares NOT VERIFIED rather than fabricating |
| **Identity / sign-in** | **3.0** | **No sign-in UI in the Hub — see H2** |
| Library / Search | 6.0 | Filters static DOM only; never queries runtime `retrieveIntelligentBlocks` |
| Smart Share | 6.0 | Browser `navigator.share` only; canonical `publishSmartFeed` unreachable from Hub |
| Smart Mail / Spaces / Connections / Lists | 6.0 | Read-only projections; creation paths dead or unwired |
| Clarity / cognitive load | 5.0 | 11 nav items, 8 external ecosystem links duplicated in header, 3 legacy renderers — see H4 |
| **HUB TOTAL** | **7.0** | Beautiful shell; the front door does not open for a new human |

### 2.4 Sender readiness

| Door | Status |
|---|---|
| Smart Note | PROVEN |
| Smart Share | PROVEN (27/27 gates, run 35553013422) |
| Smart Mail | PROVEN with explicit `smart_mail_send` authority |
| **GitHub Webhook** | **BLOCKED_EXTERNAL_CREDENTIAL** — live probe 503 `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED` |
| MCP / REST / A2A / SDK | DOCUMENTED, live parity unproven at current HEAD |
| **SENDER TOTAL** | **7.5** |

### 2.5 Receiver readiness

| Boundary | Status |
|---|---|
| Accept events from any authorized sender | PROVEN |
| Authority boundary (`intelligence_commit` requires grant) | PROVEN (17/17, run 35898728927) |
| Persist cognition + receipts + Ledger | PROVEN (35460477460) |
| Project to intelligence index | PROVEN (35906051544) |
| Fresh owner retrieval | PROVEN (35898728927) |
| Exact replay / idempotency | PROVEN (migration 20260924222644) |
| Reject unauthorized / wrong-owner | PROVEN |
| Privacy boundary (private by default) | PROVEN (35462235010) |
| 9/9 adversarial dimensions | PROVEN (35787965745) |
| **RECEIVER TOTAL** | **9.5** |

**The decisive structural insight:** the receiver is the strongest component in the system
(9.5) and the human surface is the weakest link to it (Hub 7.0, identity 3.0). Value is being
produced by machinery that a human cannot yet reach. That inversion is the mission's real frontier.

---

## 3. HOLE REGISTER (ranked by value destroyed)

| ID | Hole | Severity | Evidence |
|---|---|---|---|
| **H1** | **Conversation -> intelligence entry is dead at runtime.** `conversation_continuity.py:206` reads `.naya/memory/projects/CURRENT-DAILY-PROJECT.json`, which does not exist. The file was **deliberately quarantined** by human commit `52452926` ("Quarantine legacy memory corpus behind fresh-start boundary", Shawn, 2026-09-25). The data was quarantined; **the code that reads it was not.** `test_conversation_continuity.py` crashes with `FileNotFoundError`. | **P0** | Verified by direct execution |
| **H2** | **No sign-in UI in the canonical Hub.** `name-first-auth-adapter.js` has 1 `createElement`, exposes only `establish({name,alias})`; auth is reachable only via `?name=&alias=` URL params. `hub-completeness.js:28` redirects unauthenticated users to `/identity.html`, which is **not in the 7-file release list** and SPA-falls back to the Hub. A new human is given no way in. | **P0** | Release copy list; adapter source |
| **H3** | **CI proves a path humans cannot reach.** `hub-completeness.js` `wireSidebar()` (L180-185) attaches **no click listener**; the only entry is `window.__nayaOpenSurface`, called **only from CI** (`wave-a-authenticated-browser-acceptance.yml`). 189 deployed lines are human-unreachable, and contain the H2 redirect. | **P1** | `addEventListener` audit of the file |
| **H4** | **Four competing navigation/render implementations.** (1) `index.html` v1 `labels`/`route()` — 6 of 9 route keys do not exist in markup; (2) `index.html` v2 `S`/`render()` — the real one; (3) `intelligence-surfaces-runtime.js` — also real, injected; (4) `hub-completeness.js` — dead. Plus a global `function render(){return true;}` no-op stub at L786. Violates the North Star directly. | **P1** | Direct read |
| **H5** | **Recorded state is stale, not wrong-but-safe.** `STATE.json.latest_hub_release.next_gap = CURRENT_CANONICAL_SOURCE_DEPLOYMENT_PARITY`, but the live Worker **does** contain the deep-link contract. Recorded gaps must be re-proven or marked resolved, else they permanently inflate the backlog. | **P2** | Live probe this session |
| **H6** | **Authority-drift pointer.** `HUB-PRESERVATION.json` names protected reference `"2026 09 17 NAYANET HUB.html"`, which does not exist. The artifact survives as `verification/visual/PROTECTED-HUB-REFERENCE-2026-09-17.html` — **nothing was lost; the pointer is wrong.** | **P2** | Filesystem search |
| **H7** | **Self-verification inflation.** The cold-14 harness reports `Proven: 11` by counting non-PROVEN statuses and emits pointers instead of verified content. | **P2** | This session's execution |
| **H8** | **No reproducible local environment.** No `requirements.txt`, `pyproject.toml`, `conftest.py`, or aggregate test command. `supabase` and `requests` are not installed. No skip markers exist, so a missing credential raises `KeyError` instead of skipping. | **P2** | Environment audit |
| **H9** | **Working-tree noise.** 259 untracked entries incl. ~150 scratch `_*` scripts and `.tmp-wave-browser/`. 58 worktrees, 10 prunable inside the repo. Every cold Naya re-pays this cost. | **P3** | `git status` |

---

## 4. RANKED EXECUTION LIST — highest value first

**P0-1 — Give a new human a front door (H2).** Add a minimal, honest sign-in surface to the Hub
that calls the existing `name-first-auth-adapter.establish()`. Reuse the adapter; invent nothing.
*Verify:* unauthenticated load -> sign in -> `snapshot().authenticated === true` -> capture succeeds.
*Contract:* additive; advance the Hub preservation checkpoint with a recorded reason.

**P0-2 — Restore the conversation -> intelligence entry (H1).** Point the runtime at the canonical
post-quarantine project state, or explicitly retire the orphaned reader. Do **not** fabricate
`CURRENT-DAILY-PROJECT.json`; derive it from control-plane truth or retire the code path.
*Verify:* `python .naya/runtime/test_conversation_continuity.py` exits 0, and the offline gate set
reaches 12/12.

**P1-3 — Collapse the four renderers to one (H4, H3).** Delete the v1 `labels`/`route()` layer and
`hub-completeness.js`; keep one canonical renderer. Re-point CI at the human-reachable path.
*Verify:* one nav handler; CI acceptance exercises a path a human can actually click.

**P1-4 — Make the Hub's own surfaces live.** Library/Search must query `retrieveIntelligentBlocks`;
Smart Share must reach canonical `publishSmartFeed`; Mail/Spaces/Lists must expose real creation.
*Verify:* each surface proves a runtime call, not a static card count.

**P2-5 — Correct the recorded state (H5, H6, H7).** Resolve the stale deployment gap; repoint
`HUB-PRESERVATION.json` to the surviving reference; stop counting non-PROVEN statuses as proven.
*Verify:* every recorded gap maps to a live re-observation.

**P2-6 — Make verification reproducible (H8).** Add a declared dependency set and one aggregate
offline gate command; add credential skip markers.
*Verify:* a cold machine runs `python -m pytest` equivalent and gets a truthful result.

**P2-7 — Unblock the GitHub Webhook door.** Requires an authorized operator to set
`GITHUB_WEBHOOK_SECRET` in Supabase project `dahisasgpfvziswqvmvm`. **Not agent-authorizable.**
*Verify:* live probe no longer returns 503 `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED`.

**P3-8 — Clean the working tree (H9).** Quarantine scratch artifacts to an ignored directory;
prune the 10 stale worktrees.
*Verify:* `git status --porcelain` count drops to zero without losing evidence.

**P3-9 — Close the human-path acceptance gap.** Run live browser acceptance at the exact release
identity proving sign-in -> capture -> feed -> deep link -> reload, on desktop and mobile.

**P3-10 — Re-measure compounding honestly.** Extend the bounded avoided-work benchmark toward a
real repeated-restoration measurement, keeping value and provenance intact.

---

## 5. ULTIMATE EXECUTION PROMPT FOR THE NEXT NAYA

> Read this receipt and `.naya/control-plane/BATON.json` before acting. Resolve live
> `origin/main` at execution time and confirm the canonical checkout is attached to `main`, not
> detached — a stale detached tree is the defect that already cost this project one session.
>
> Take exactly one item from §4. Stop at the first deterministic boundary. Repair only that
> boundary. Rerun the same proof. Record the receipt. Update STATE/BLOCKS/BATON so the single next
> action stays coherent. Then stop and pass the torch.
>
> Never: fabricate a missing artifact to make a test pass; treat BLOCKED as PASS; promote recorded
> evidence to current proof; bypass the Read-First gate; add a second brain, database, or renderer;
> edit the Hub without advancing the preservation checkpoint with a recorded reason; push to `main`
> without explicit authorization (a push fires ~62 workflows and the release gates).
>
> Success for your session = the human can do one more useful thing than before, and the next Naya
> inherits a strictly better starting state.

---

## 6. OPEN QUESTIONS — answered from canonical sources

1. **Should `CURRENT-DAILY-PROJECT.json` be restored or the reader retired?** The quarantine was a
   deliberate human act; restoring the file may violate its intent. -> *Needs director decision;
   both options recorded in P0-2.*
2. **Is `/identity.html` intended to be deployed?** It exists at `NAYANET/HUB/public/identity.html`
   but is outside the 7-file release contract. -> *Contract gap; P0-1.*
3. **Is `hub-completeness.js` retained deliberately?** It is deployed, CI-exercised, and
   human-unreachable. -> *P1-3.*
4. **Who is the authorized operator for `GITHUB_WEBHOOK_SECRET`?** -> *P2-7, human-only.*
5. **May I push to `main` and dispatch the release?** -> *Requires explicit authorization; not
   self-granted.*

---

## 7. RECEIPT INTEGRITY

- Executed at HEAD `2846a5e6`, zero divergence from `origin/main`.
- Offline gate suite: **11 PASS / 1 BLOCKED (H1)** — measured, not claimed.
- Cold-14 harness: **PASS** with the inflation caveat in §1a.
- Control-plane coherence: **STATE == BLOCKS == BATON** — measured this session.
- Live Worker probe: HTTP 200, contains deep-link contract — supersedes the recorded H5 gap.
- No production deployment was performed. No credential was exposed. No historical evidence was
  promoted to current proof.
