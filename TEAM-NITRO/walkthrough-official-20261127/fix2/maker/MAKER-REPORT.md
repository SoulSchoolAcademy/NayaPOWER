# MAKER REPORT — Official Walkthrough FIX2 (fix-back pass)

**Staged only. Nothing live. Nothing to Shawn directly.**
**Lane:** `~/workspace/team-nitro/walkthrough-official-20261127/fix2/maker/`
**Staged:** https://official-walkthrough-staging.nayapower.workers.dev/
**Branch:** `walkthrough-official-20261127`
**Parent head (fix1):** `4fc628cac5cfa4861b3d543bace1a578b29adf15`
**Commit 1 (files):** `bbc31afb707647efeaf66f635eec4fe3ab1f2d49`
**Commit 2 (this report):** filed after commit 1; sha recorded in the lane file after filing — see the branch log, not this line.
**Deployed:** 2026-11-28 ~03:40 UTC, deployment `9da60c33e978454693402594ed1dc2f5` (HTTP 200).

## Sizes + shas (staged bytes == local bytes, verified by curl + cmp)

| File | Size | sha256 |
|---|---|---|
| Portal (`portal.html`, staged `/`) | 47,432,462 B | `3301fa0550432c1a33927bb714d3fb9993130247aa7a80e9da3b5390f19f7817` |
| Certificate (`identity.html` / `identity-consolidated.html`, identical) | 306,117 B on disk | `58574945f837c9e21c4d9767dce62911d0733ff588452924ad7e2b8242c594e1` |
| Worker (`worker-consolidated.js`) | 47,764,626 B | `2919797fb50c328ce568294495dfd6f789a2e9cceae57af9d333d3d16241bf9c` |
| Portal rebuild input (`portal-v1.html`, NEW blob this round) | 13,901,029 B | `88346f9d25906f0c70419057458e9a2f1890d52e736be9585dc0ec4c6158b863` |

Base verified by sha256 before editing (portal `eb6a2f7e…`, cert `86536d53…`, branch head `4fc628ca…`). Rebuild run twice, byte-identical both times; build assertions **35/35 PASS, 0 FAIL** (fix1's report said "36/36" — the script contains 35 `assert(` calls in both fix1 and fix2; a miscount in the fix1 report, not a regression). Portal delta +633 B (exactly the portal-v1 delta); worker −11,799 B (cert −12,547 B + portal +633 B, plus rounding).

## What changed per item

### 1. F1 — certificate paragraph "ur alias" (390, already-claimed state) — FIXED, re-proved
Cause: D3 tiles pushed ENTER + paragraph down ~90px into the bottom corner crests; the D4 margin fix covered `#hubNote` only, not this paragraph (`.cert-benefit`). Fix (`fix2-cert.mjs`, applied to both identity files, still byte-identical to each other): `.cert-benefit { margin-left: 24px; margin-right: 24px; }` with a FIX2 F1 comment, after the `.cert-plaque.is-certified.cert-benefit` rule. Re-proved at 390 in the taken state (alias shawn, already claimed, reads only — no new row in the shared `nayanet_identities` table): paragraph x=43, 24px margins, "Yo" point-test lands on the paragraph, not a crest. Seen with my own eyes in `evidence/fix2-390-cert-para.png`: "Your alias is your Smart Link route — alias.nayanet.app — Smart Mail, and your identity in NayaNET." — "Yo" clear of the left crest, right end clear of the right crest.

### 2. Install veil — DELETED, not guarded — FIXED
The veil element and ALL its show-code are gone from both identity files: the whole install CSS block (3,963 B cut), corner-button strays, the veil HTML element (3,206 B cut), the whole PWA install JS IIFE (5,625 B cut) — replaced with a minimal service-worker-registration-only block. Removed tokens: `installVeil`, `openModal`, `installGo`, `installX`, `installLater`, `installManual`, `beforeinstallprompt`, `install-veil`, `install-card`. Grep over the shipped bytes: **0 hits**. JS still valid (inline `<script>` blocks syntax-checked via `new Function`; 0 page errors in every probe session). Kept: manifest link (browser-native affordance, not a veil) and SW registration (not install UI). **Named consequence:** removing the IIFE also removes the `beforeinstallprompt` suppression, so the browser's own native install affordance is no longer suppressed. That is the browser's own prompt, not a replacement prompt — none was built — but it is a behaviour change to be aware of.

### 3. Remove-account confirm (`#fpRemoveModal`) — converted to full-screen in-frame — FORM FIXED AND PROVED; TRIGGER NOT REACHABLE BY TAPS (named gap, see below)
Modeled on the agreement story (`#fpStory`) pattern (`fix2-portal.mjs`, applied to `portal-v1.html`): modal background `rgba(0,0,0,.72)` → opaque `#02030a`; the floating card rule replaced with full-frame content styling (`width:100%; max-width:640px; background:transparent; border:0; border-radius:0; box-shadow:none; padding:24px 20px; text-align:center`); added a 44px round × close button top-right (`.fp-remove-close`, mirroring `.fp-story-close`) wired to the existing `closeRemoveAccount`; Esc + Keep + backdrop-click already closed it. Remove behaviour itself untouched.
**Proved live at 390** (`evidence/probe-fix2c.log`, `evidence/fix2-390-remove.png` — seen with my own eyes): modal opens naming the account ("Remove Friend (friend)? You will lose this account for good — it cannot be brought back."), fullscreen **[0,0,390,844]**, `position:fixed`, opaque `rgb(2, 3, 10)`, card transparent / borderless / full-width, × in view top-right, closes on × tap with the account NOT removed, closes on Esc, 0 page errors in the portal session.

**THE TRIGGER GAP (new finding this round — corrects fix1's static reading):** the fix1 verdict described the trigger as "reachable on the portal only for returning users with multiple saved accounts". Live, it is NOT reachable by taps, in two layers:
1. **The list is hidden by a deliberate v1 ruling.** With two saved accounts the row renders in the DOM (1 row, aria-label "Remove account Friend"), but `body.fp-returning #returningOthers{display:none!important}` hides the whole "Also on this device" list in the returning view — the portal CSS comment says so explicitly: *"This is me — it's my name" and the "Also on this device" list STAY hidden in this view (v1 ruling, others-list question still awaits a ruling).* In fresh mode the list's ancestor `#returningView` is hidden. So no tap reaches the × as shipped.
2. **Even revealed, the × is not pointer-reachable.** Lifting the ruling class (probe-only) makes the × visible — but it renders 70px BELOW its view's box (view bottom 504, × at y 574) under the positioned `.stage` layer, so every sampled point inside the × hit-tests to `.stage` (5/5). A pointer tap lands on `.stage`, never on the ×. (The "Jump back in" button, inside the view's box, hit-tests fine.)
**What the proof actually was:** the modal was opened with a DOM click on the × (`element.click()` — fires the real handler with the real row/alias); every close after that (× tap, Esc) was a real pointer tap / key press. The probe log's check name said "real x tap" for the opener — that wording is wrong and is corrected here and in the probe file; the log line itself predates the correction. **The modal form is fixed and proven. The trigger routing is a product decision, not a fix2 change:** the others-list visibility awaits Shawn's ruling, and the ×'s position under `.stage` rides with it. Do not claim the remove flow is reachable by taps until that ruling lands.

### 4. Live re-proof — complete() POST, Choose plan, #dealPlain, #fpZoom — PROVED LIVE
- `complete()` POST 200, `/me` POST 200, end screen READY ("6 of 23 questions answered. Your world is ready"), 44 answer keys saved, end screen whole at both widths.
- "Choose plan →" click lands on https://naya-model-pricing.nayapower.workers.dev/.
- `#dealPlain` opens fullscreen [0,0,390,844] on a real mirror-link tap, carries the whole letter as plain text ("THE COLLECTIVE AGREEMENT\nBetween NayaNET"), closes on Esc.
- `#fpZoom` opens fullscreen [0,0,390,844] on a real showcase-image tap, closes on × tap.
- **Probe totals: part A 59 PASS / 0 FAIL** (`probe-fix2.py`); **part B 10 PASS** (zoom + plain re-proved in a fresh portal session, then the remove trigger's row found in the DOM); **part C 19 PASS / 0 FAIL** (`probe-fix2c.py` — remove form + 1440 keepers). Two probe crashes along the way were probe bugs, not product defects (eye `#dealEyeMain` not visible in part A; top-bar `#fpStageExit` not visible in letterPage view in part B; both fixed by using the page's own `__fpStage.exit()` API).

**THE DEAL-VIEW ROUTE (documented, as briefed — the fix1 checker could not find it):** the deal view (the stage, `#fpAgreement` layer) has **NO tap entry in the shipped build**. The story never enters it (all story entries call `openStory(0)`; story close/agree return to the name box); `?stage=` deep links are deliberately disabled (PORTAL-ROOT-FIRST, 2026-11-22); nothing in the page calls `enterStage()` from any UI control — its only entry is the page's own exposed API `window.__fpStage.enter()` (exposed at `window.__fpStage={state:S,enter:enterStage,exit:exitStage,render:render}`). The intro's "Read the agreement" choice navigates to `/agreement` (302 to live nayanet.app/agreement), not the staged deal view. `#dealEyeMain` is hidden in EVERY reachable state (section `display:none` under `html.fp-locked` out of stage; `display:none` in the stage CSS group) — it is NOT a live opener. `#dealPlain`'s only live opener is the stage-bar mirror link `#fpLinkLetterAll` ("or read the whole letter at once"), visible only in letter/letterPage views. The letter view itself is unreachable by taps from a fresh load: `resumeTarget()` never returns `'letter'`, returns letterPage only when a letter beat beyond 0 is already shown, and no tap can show one (wireLetter's Next/rail controls live inside the fp-locked section; deck end exits to login by design — the `a.deck-next[href="#dealUnfold"]` anchor is intercepted to `exitStage()`; `enterLetterPage()` has no caller). Empirically: walking the whole deck by taps (deck 0→8) leaves `letterShown == 1` and the mirror hidden at deck end. `#fpZoom` opens only from a tap on an image inside `.lb-showcase` while `body.fp-stage-on` — reachable by taps once in the stage (deck beat 0 showcase image, proven live twice). **Qualification:** `#dealPlain` and `#fpZoom` are proven live, but the deal view itself has no citizen tap route — a follow-on could wire a real entry. Do not claim a tap route exists.

## Keepers re-proven (do not regress — all PASS)
Veil dead by removal (grep 0); 1440 trio **360/360/360px** unclipped in all 8 groups with slide header on every phone (`evidence/fix2-1440-g1.png`, `evidence/fix2-1440-end.png`); certificate digit tiles ticking in Tuesday gold (`TUESDAY20OCT2026 · 03:43:47`, `rgb(212, 160, 23)`); `#hubNote` margins 24/24 clear of jewels; 23 steps in exact order; no Skip; gender no default; no church/Spotify; picture map byte-exact; video direct file only (plays/pauses); end screen whole at 390 and 1440, no video at end; answers save (44 keys); **0 page errors** at 390 and 1440.

## Named gaps / corrections
1. **47 MB product files NOT filed** (`portal.html` + `worker-consolidated.js` 422 on the blobs API, "input too large", proven in fix1). Every rebuild input IS filed (commit 1), including the NEW `portal-v1.html` blob this round, and the rebuild was proven byte-identical twice locally. Rebuild needs the pictures copied from `workspace/user/media_library` to `media/` first.
2. **No citizen tap route to the deal view** (see item 4). `#dealPlain` / `#fpZoom` proven live via the state API + real taps inside the stage.
3. **Remove-account trigger not tap-reachable as shipped** (see item 3): v1 ruling hides the list; the × sits under `.stage` even when revealed. Modal form proven; trigger awaits Shawn's ruling.
4. **`beforeinstallprompt` suppression removed with the veil** (see item 2): the browser's native install affordance is no longer suppressed.
5. **"6 of 23 questions answered" on the ready line vs 44 saved keys** — fills map to 6 question keys; the count is questions, not keys. Not a defect.
6. **fix1's "36/36" build assertions was a miscount** — the script has 35 `assert(` calls; fix2 is 35/35 PASS.
7. **Probe log wording correction:** `probe-fix2c.log` says the remove modal "opens on a real x tap" — the opener was a DOM click (pointer tap impossible as shipped, see item 3); the closes were real taps. The probe file's check name was corrected after the run; the log line predates it.

## Files in this lane
- `fix2-cert.mjs`, `fix2-portal.mjs` (the fixes), `build-official.mjs` (pin only), `commit-fix2.py`, `commit-fix2.log`
- `portal-v1.html`, `identity.html`, `identity-consolidated.html`, `portal.html`, `worker-consolidated.js`
- `evidence/`: `probe-fix2.py`, `probe-fix2.log` (59 PASS / 0 FAIL), `probe-fix2b.py`, `probe-fix2b.log` (10 PASS), `probe-fix2c.py`, `probe-fix2c.log` (19 PASS / 0 FAIL), `debug-deal.py`, `debug-deal.log`, `debug-remove.py`, `forwarder.log`, screenshots `fix2-390-cert.png`, `fix2-390-cert-para.png`, `fix2-390-g1.png`, `fix2-390-end.png`, `fix2-390-dealplain.png`, `fix2-390-zoom.png`, `fix2-390-remove.png`, `fix2-1440-g1.png`, `fix2-1440-end.png`
- Forwarder (Chromium via localhost proxy) left running, PID 2926, `~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py` on 127.0.0.1:18080, for the checker.
