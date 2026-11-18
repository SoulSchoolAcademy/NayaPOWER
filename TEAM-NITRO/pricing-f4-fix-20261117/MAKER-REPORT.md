# MAKER REPORT — Pricing Free-Entry Fix (F4-FIX, 2026-11-17)

Maker: pricing free-entry fix round. Brief: `~/workspace/team-nitro/BRIEF-PRICING-F4-FIX-20261117.md`
(follows on from `BRIEF-PRICING-FREE-ENTRY-20261116.md`). Required reads done first:
Playbook, Design Intelligence Report (read), Naya Design Language, Naya Code.
Built 2026-11-17 ~01:28–01:45Z. **Stage only. Do NOT merge. Nothing went live.**

## Staged URLs

- Pricing v78 (unchanged): https://naya-pricing-f4-staging.nayapower.workers.dev/
- Free route: https://naya-pricing-free-staging.nayapower.workers.dev/free
- Free walk (fixed): https://naya-pricing-free-staging.nayapower.workers.dev/free/walk
- Hub: https://naya-pricing-free-staging.nayapower.workers.dev/free/hub (302 → https://nayanet.app/)

## 1. ROOT-CAUSE DIAGNOSIS — the stall was client-side, not the backend

**The backend was never the problem.** Before touching anything I re-proved it live:
`POST /api/welcome/complete` with a walk-shaped payload → **200 in 0.94 s**, reveal with
`pages.personal/business/space/dashboard` all present. The F4 maker had proven the same.

**The stall is four bugs in the walk's own script** (harvested verbatim from
`walk-beginning-fixed.html`, sha `df17ac67…` — the bugs live in that source too):

1. **Naming Enter goes nowhere visible.** The names-step Enter handler calls
   `showStep(14)` — the NAMES step itself — then `completeWalk()` in the background.
   The click changes nothing on screen (the eye's "silent Enter", three clicks, nothing).
   On success `showBuildDone()` unhides `#buildDone` *inside* `#step-building`, which is
   still hidden — so success is invisible. On failure `showBuildError()` is equally invisible.
2. **Reload lands on "Building it" forever.** `boot()` sees the saved `S.reveal` and calls
   `showStep(15)` — the BUILDING step with `#buildWorking` visible and `#buildDone` hidden.
   Nothing on that load ever calls `showBuildDone()`. That is the eye's ~6-minute stall
   across two page loads, exactly: the reveal was already saved, the screen still said
   "Building it — wait a minute…", with no progress, no error, no timeout.
3. **No timeout.** `api()` is a bare `fetch()` with no `AbortController`, no deadline — a
   hanging POST hangs forever.
4. **"See your pages" loops.** It calls `showStep(15)` (building again), not `showStep(16)`
   (the end slide) — it would loop even after a good build.

**The `/api/welcome/me` 404 was a red herring with a real edge.** The endpoint exists but is
POST-only; a GET falls through to `{"ok":false,"error":"unknown api"}` — and the walk never
calls `/api/welcome/me` at all. I wired the GET branch anyway (W1 below), so the endpoint
answers as the eye probed it. **Fix chosen: fix the walk client-side (the real root) + add
the GET branch (the probed edge).** Pointing the walk at another backend was not the fix —
its own backend answers in under a second.

## 2. THE FIX — free copy only (F1–F8 + W1)

Applied on top of F4's patches P1–P4, in `build-fix.py` (`replace_once` anchors, asserted):

- **F1 CSS:** build progress bar (`.p3-buildbar`, `min(320px,80%)`, green `#2fe89e` — the
  free colour) + `.p3-enter.is-busy` pressed state + error-message spacing.
- **F2 HTML:** progress bar + live status line `#buildStatus` in `#buildWorking`; error
  message line `#buildErrorMsg` + **"Back to your names"** button in `#buildError`.
- **F3 `api()`:** 25 s `AbortController` timeout → `{ok:false, timedOut:true}`. A hanging
  POST now fails, never hangs.
- **F4 `completeWalk()`:** in-flight guard (no double POST); starts visible progress
  (status cycles every 2.5 s through *Saving your answers… / Building your pages from your
  own words… / Wiring up your Hub, Dashboard and pages… / Almost there…*, bar 8% → 92%);
  on failure calls `showBuildError()` with the reason (timeout names the 25 seconds).
- **F5 `showBuildDone()` / `showBuildError(reason)`:** stop the progress (bar to 100% on
  done), reset the naming Enter, error shows its readable message.
- **F6 naming Enter:** immediate pressed feedback on every click — disabled, `is-busy`,
  label becomes **"Building…"** — then `showStep(15)` (**the BUILDING step, visible**) +
  `completeWalk()`. Double-clicks are ignored while building.
- **F7 "See your pages" → `showStep(16)`** (the end slide, five doors). "Back to your
  names" → `showStep(14)`.
- **F8 boot resume with a saved reveal → the end slide directly** (five doors), never the
  building screen.
- **W1 worker:** `GET /api/welcome/me` (alias from the query) mirrors the POST read.

**What did NOT move:** pricing v78 (untouched, sha below), `/free` entry (byte-identical),
`/free/hub` (302), the nine paid chooser tiles, chooser/finale free options, the play button
beside Naya's portrait (glow-only, no audio wired — as ordered). The diff old→new walk is
125 lines, all F1–F8; the worker diff is 25 lines (the `WALK_FREE` line + the 7-line GET
branch). Nothing else differs.

**Follow-on, NOT this round:** the same four bugs exist in the live walk source
`walk-beginning-fix-20261111/walk-beginning-fixed.html` (sha `df17ac67…`) and therefore in
the walk staging worker. Fixing the live walk source is a walk-round job — this round
touched only the free copy, as briefed.

## 3. FILES / WORKERS CHANGED — before → after

| Thing | Before | After |
|---|---|---|
| Pricing v78, worker `naya-pricing-f4-staging` | 11,360,503 B, sha `ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2` | **UNCHANGED** (re-verified live over HTTP) |
| Free entry `/free` | 307,918 B, sha `e0534a61441dd6f4f643b79a74a9d1a8479c8c41cb2d6abf126d3b7fd87eb1ab` | **UNCHANGED** (re-verified live over HTTP) |
| Free index `/` | 1,966 B, sha `085939f6f1a8bc0106f54434f5dc27ef12e7a17c8733ca792d8ad61e8521c47e` | **UNCHANGED** |
| Free walk `/free/walk` | 3,288,471 B, sha `ea1e77a67cbdc34d5829d8a4f09bceba0338ca3efac8483d84703d69521191cc` | **3,291,949 B (+3,478), sha `04ec6218783e949690cb832c57e5d02e38ed304e7f2f164ddea8b67167c6ba78`** |
| Free worker `naya-pricing-free-staging` | 3,615,644 B, sha `7a6a90959ced7d104b7e0781de023396412cea2eadfc504db309e964fc66a41c` | **3,619,556 B (+3,912), sha `83aa4090852cb3fd58dfaaaccb337d428662a2b88ff9314caf803d1ec1678cbc`** (gzip under the 10 MB limit, assert passed in the build run) |
| `GET /api/welcome/me?alias=f4captaincheck` | 404 `{"ok":false,"error":"unknown api"}` | **200 `{"alias":"f4captaincheck","name":"F4captaincheck"}`** (before cleanup) |

Round files (this dir `~/workspace/team-nitro/pricing-f4-fix-20261117/`):
`build-fix.py` (build + stage, in-memory), `check-walk-flow.mjs` (DOM harness),
`cleanup-test-alias.py` (KV + Supabase cleanup), this report.
**Big files are NOT on disk** — the EPERM flake is still up (python/curl writes fail with
`[Errno 1] Operation not permitted`, leaving 0-byte files; small shell/file-tool writes work).
The fixed walk + worker are recoverable byte-exact from the staged workers at the shas above,
exactly as the F4 round left them. Filed to GitHub (see §6).

## 4. SELF-CHECK — per brief item (three passes)

**Pass 1 — build + stage (`build-fix.py`):** fix markers all present, old code all gone
(`showStep(14); completeWalk()` 350 ms, boot `showStep(15)`, go-button `showStep(15)`).
Node driver (the workers' real fetch handlers): fixed walk + unchanged entry + index + hub
redirect all **PASS**. PUT read-back sha **MATCH**. Live HTTP: `/`, `/free`, `/free/walk`
byte-equal to source; `/free/hub` 302 → `https://nayanet.app/`; `GET /api/welcome/me`
200; `POST /api/welcome/complete` (test alias `f4fixvoeityel`) 200 with reveal pages;
GET complete read-back MATCH; `GET /f4fixvoeityel` 302 → live personal page.

**Pass 2 — DOM harness (`check-walk-flow.mjs`, executes the real served script):**
the harness runs the walk's actual inline script in a minimal DOM facade (no browser exists
in this VM; jsdom could not be installed — npm registry blocked — so the facade is
hand-rolled; it executes the real bytes, it does not re-implement the logic).
- **Old-code baseline first (proves the harness catches the bugs): 11 failures** on the
  main run (old call present, no timeout, no Enter feedback, building never visible, build
  never completes into doors, resume lands on Building it) and **7 failures** on the
  timeout run (no loud error, no way back).
- **Fixed staged bytes, main run: ALL PASS 16/16** (×3 runs) — boot → step-14 → names Enter
  (disabled + "Building…" + `is-busy`) → building visible with live status → bar moves
  8% → 22% while building → buildDone → "See your pages" → end slide, five doors
  Hub/Dashboard/Personal/Business/Space in order + free line; reload with a saved reveal
  lands on the end slide directly.
- **Fixed staged bytes, timeout run: ALL PASS 11/11** (×2 runs) — hanging POST fails loudly
  (buildError visible, message names the 25-second timeout), Try again + Back to your names
  present, Enter re-enabled, Back returns to names. Note: the timeout run overrides `25000`
  → `150` ms in a harness copy only and simulates the aborted fetch (a real `AbortController`
  passed into the vm context aborts the Node process, and a `curl | node` pipe aborts it too
  — both are harness-environment quirks, not page bugs; the runs use a python-fed stdin
  instead. `AbortController` itself was proven separately in Node: `new AbortController()` +
  `abort()` fires abort, `signal.aborted === true`.)
- **Item 1 (build stall): PASS.** Build shows visible progress, completes into the five
  doors, and fails loudly on timeout with a readable error + a way back.
- **Item 2 (silent Enter): PASS.** Immediate pressed feedback on every click, proven in
  the harness (T1) and by the code (disabled + `is-busy` + "Building…" before the 150 ms
  step change).
- **Item 3 (test-alias cleanup): PARTIAL — see §5.** KV side complete; Supabase row remains.
- **Item 4 (390px): NOT PROVEN LIVE — see §5.** Static + state-machine proof only.

**Pass 3 — untouched surfaces re-verified after staging:** staged pricing still serves v78
byte-exact (`ca2eafeb…` over HTTP); `/free` still `e0534a61…`; `/free/hub` still 302;
play button present and untouched; the walk diff touches only F1–F8 (125 lines) and the
worker diff only the `WALK_FREE` line + GET `/me` (25 lines).

## 5. HONESTLY NOT DONE

1. **Supabase row for `f4captaincheck` still exists.** All six KV completion records were
   deleted and verified 404 (`complete_f4captaincheck`, `complete_f4fixvoeityel`,
   `complete_f4diag1`, `complete_f4testekcpgpnv`, `complete_f4testmhxphhky`,
   `complete_f4probeex`). The Supabase `nayanet_identities` DELETE with the public anon key
   returned **200 with `[]` — zero rows deleted (RLS filters it)** — and `GET /api/claim?
   alias=f4captaincheck` still returns `exists:true, cert_no:737, created 2026-11-17T01:10:32Z`.
   What this means in practice: the alias no longer resolves to any test pages (the
   `/<alias>` redirect reads the KV record, which is gone; `GET /api/welcome/complete?
   alias=f4captaincheck` is 404), but the identity row itself is still in the table and the
   alias still shows as claimed. Deleting it needs a key the anon key cannot supply; I did
   not go hunting for one. **Needs a follow-on with the right key, or Shawn's hand.**
2. **No live browser proof (desktop or 390px).** I am a subagent with no live browser; the VM
   browsers are dead (Firefox exit 139, Chromium exit 133 per the house notes) and jsdom
   could not be installed. What I prove instead: the state machine, executed from the real
   served bytes at any width (the code path is width-independent), plus the static 390px
   picture — viewport meta present; every fixed width over 390px in the walk CSS is a
   `max-width` cap (520/560/680px, with `width:100%`) or inside a `@media (max-width:480px)`
   rule; the walk carries explicit "MOBILE FIT — whole page fits one viewport at 390px/
   360px" rules; my progress bar is `min(320px,80%)`. **The checker/eye must still walk
   pricing → /free → /free/walk → five doors at 390px in a real browser.**
3. **The fine-print sentence is not in the served bytes.** The brief says to keep
   "No PayPal, no Stripe, no wallet." on the `/free` entry page — I checked the served
   `/free` bytes: **zero mentions of PayPal, Stripe, or wallet**, and the sentence is not in
   staged pricing v78 either. Nothing was removed (the entry is byte-identical to F4, sha
   `e0534a61…`), so the "keep" holds vacuously — but the sentence itself is not there to
   keep. Flagging the discrepancy rather than adding a sentence I was not asked to add.
4. **Big files not on disk** (EPERM flake, §3) and **no GitHub filing of the 3.2 MB walk /
   3.6 MB worker sources** (same as F4: the staged workers are the byte-exact record).
   Small files (this report + 3 scripts) are filed — see §6.
5. **Live walk source still carries the same four bugs** (follow-on, §2).

## 6. GITHUB FILING

Branch `pricing-f4-free-entry-20261116` (repo `SoulSchoolAcademy/NayaPOWER`, TEAM-NITRO is a
folder inside it). New commit on top of the branch tip — **NOT merged**.
Files: `pricing-f4-fix-20261117/MAKER-REPORT.md`, `pricing-f4-fix-20261117/build-fix.py`,
`pricing-f4-fix-20261117/check-walk-flow.mjs`, `pricing-f4-fix-20261117/cleanup-test-alias.py`.
**Filed: branch `pricing-f4-free-entry-20261116`, commit
`57a6d9e3847a41322c1028c983d65d2c4f986fa7`** (parent = branch tip `f5fc9b53…` as briefed),
tree `6730faea8035010b5fb4e8820beb14ec59045d79`, 4 blobs (report `4a8b78b2…`,
build-fix `52d7be07…`, harness `b022dfae…`, cleanup `4fa28615…`); ref verified pointing at
the new commit; maker-report blob read-back MATCH (sha256
`22a39f09f975fe02b7aa9aa4b7962ad2b63095b08544a8f12ad522375f518f53`). **NOT merged.**

## 7. FOR THE CHECKER

Cold, from the staged bytes: claim a fresh test alias at `/free`, answer the 14 steps, name
the pages, click Enter — watch the button press, the building screen with the moving bar +
stage text, then "Done — here are your pages" → "See your pages" → the five doors + the
end line "You're in on Naya Free — zero cost, zero risk", at desktop AND 390px. Reload
mid-build and after completion (must never sit on "Building it"). Point the build at a dead
backend if you can (the 25 s timeout + error + Back path); my harness proves that path with
a simulated abort only. Then clean up your own test alias the same way (KV DELETE +
Supabase row — the row will need the key this round could not supply).
