# MAKER REPORT — Walkthrough Chain Fix Round 2 (fix2)

**Seat:** maker. **Branch:** `walkthrough/chain-fix2-20261118` (from `walkthrough/chain-20261118` tip `e4e1caa7`).
**Commit:** `a89e10aedd35fb5e065d45db4fc11396b9b03b09` (tree `59680fea0740c9c349f18c33ccaa025f67c1a996`).
**Staged:** `https://naya-walk-beginning-staging.nayapower.workers.dev/` — PUT HTTP 200, `success: true`,
modified `2026-11-18T23:50:04Z`, deployment `225eb19c2e264a61b8051d513532af62`.
**Status: STAGED AND BYTE-VERIFIED. LIVE CLICK-THROUGH NOT PROVEN — both VM browsers are dead
(Chromium SIGTRAP, Firefox killed at launch, re-tested 2026-11-18 ~23:55Z). Do not call this
verified until the cloud-browser eye walks it.**

No PR, no merge, no live deploy, no message to Shawn. Report to the coordinator only.

## 1. Diagnosis of the bridge cause (item 1 — the decisive failure)

Three findings, in order of weight. The eye's verdict (22:43–22:55Z) was: after "I agree" the page
lands on `?stage=bridge` showing the agreement deck again; no "Continue — enter your name" pill
anywhere (text search, both widths); deck-end Enter shows "AGREED ◆ WELCOME HOME." but reopening
shows only the two buttons.

**(a) REAL UX defect — the onward pill was unreachable (the likely eye hit).** The bridge code is
statically correct throughout (traced by hand: `goBridgeAfterAgree()` sets `S.view='bridge'`,
unhides the agreed line + onward pill, calls `render()`; all four end paths route to it — deck-end
Enter `deckJoin`, beat-9 anchor, "I agree" hold, 10s fallback; `render()` toggles `fp-view-bridge`;
CSS shows `#fpBridge` only in bridge view; bridge More1–4 wiring G2→G3→G4→Final is correct; boot
`?stage=bridge` hook, restore block, plain-load auto-enter all correctly guarded). BUT the onward
pill lives in `#fpBridgeFinal` and only appears after **four** bridge Continue clicks
(More1→More2→More3→More4). After agreeing, the bridge opens at group 1; the eye's text search
found nothing because the pill was never reached. The fix makes the post-agree bridge open with
all four groups + Final already shown.

**(b) Agreed state did not persist across reopen/refresh.** Round 1 named this a deliberate limit
under the F1 rule (only `agree` persists); the eye read the loss as the bridge never having
happened. The fix persists `bridge-agreed` in localStorage and restores the post-agree bridge
from it, same shape as the existing `agree` restore.

**(c) Served bytes during the eye window were wrong/flipping (co-cause, not proven sole cause).**
The coordinator's curl of the staging root at ~22:57Z returned HTTP 200, 3,466 bytes, but sha256 of
the saved file was the empty-file hash. My own first curl reported HTTP 200 size 3460 while the
piped body hashed to the full 1.8 MB welcome; `curl -o` and `tee` to files failed with EPERM /
wrote 0-byte files. Same pattern as the pricing wire-flip precedent the same night (captain's curls
showed three different contents in quick succession, including a 3.4 KB "Welcome to Naya World"
page). The staging wire was re-verified as the tip bytes on all routes before this build
(`/` = welcome `1a48347f…`, `/agreement` = unfold `984d87af…`, `/welcome` = walk `4b5f9264…`,
`/identity.html` = identity `d8c0d583…`, `/?stage=bridge` = welcome `1a48347f…`), and again after
this build (see §4). The eye may have loaded during a flip window.

## 2. What changed, file by file

### Welcome — `team-nitro/walk-v23-assembly-20261114/welcome-staged.html`
- Base: 1,854,672 B, sha256 `1a48347f9f7907c1404f3086302c6e7554a3e74ea6f898574da2dca90f3936ae`, blob `5ac2054d…`
- New: **1,857,688 B, sha256 `c8581fca0a697204a94d64b17b28e5ae67ef70d887fd95dd2cdd5b8ba1815d03`**, blob `868c746d1219…`
- **W1 (item 1):** `goBridgeAfterAgree()` now opens the post-agree bridge with ALL FOUR groups +
  Final shown (G2/G3/G4/Final `hidden=false`, More1–4 `hidden=true`), agreed line + onward pill
  visible on arrival; persists `bridge-agreed` in localStorage after `render()`. Pre-agree bridge
  via `enterStage()` still opens at group 1, untouched.
- Render save branch: `S.view==='bridge' && window.__fpAgreed` now saves `bridge-agreed` (a render
  on any in-stage click previously would have wiped it); plain bridge visits still clear the key.
- `exitStage()` now also clears `window.__fpAgreed=false` (leaving the stage resets to pre-agree).
- Boot restore: `_fpRestoreStage==='bridge-agreed'` restores the post-agree bridge (all groups +
  final shown, agreed line + onward visible), same shape as the existing `agree` restore.
  Plain-load auto-enter guard now also excludes `bridge-agreed` so it cannot clobber the restore.
- **W3 (item 6):** intro strip and bridge strip changed `flex-wrap:wrap` →
  `flex-wrap:nowrap;overflow-x:auto` (one row, sideways scroll). The D4 comment's claim that the
  bridge strip "already sets flex-wrap:nowrap + overflow-x:auto" is NOT in the base bytes — both
  strips wrapped to 2–3 rows at 534 wide, growing to ~100–150px tall and covering the in-flow
  choices. Added `body.fp-stage-on #fpAgreement.fp-view-bridge #fpBridge{padding-bottom:72px}`
  inside the existing `@media(max-width:640px)` block (72px clears the one-row strip ~53px).

### Identity — `team-nitro/walk-v23-assembly-20261114/identity-fixed.html`
- Base: 387,458 B, sha256 `d8c0d583e16f70194227b017db42980c2d4507283292475c5a8fde9c0fc46219`, blob `98b0efc0…`
- New: **388,608 B, sha256 `803e7ea8a7822f8f1e5942913615ca62bfec81e54b28bb4a05924134322bd617`**, blob `c0a351221d48…`
- **I2 (item 4):** added `__chainApiBase` at the top of the script (ENTRY-FLOW CONFIG area): `''`
  on the staging worker hostname, else absolute
  `https://naya-walk-beginning-staging.nayapower.workers.dev`. All FIVE `/api/claim` fetches now
  use `__chainApiBase + '/api/claim'` (live check, stamp read-back, POST claim, verifyKey, taken
  read-back). Verified: 0 remaining relative `fetch('/api/claim`, 6 `__chainApiBase` refs.
  Root cause of the proof-host claim failure: identity fetched relative `/api/claim` — on the
  proof-host origin that 404s — and the staging worker had ZERO `Access-Control` headers, so even
  an absolute cross-origin claim would have been blocked by the browser (JSON POST preflights,
  and no OPTIONS handler existed).
- **I1 (item 2):** `__chainShowKey` now defines one shared `doCopyKey` routine; the `#keyValue`
  pill is clickable (`cursor:pointer`, title "Tap to copy your device key", wired once via
  `dataset.chainWired`) and the existing "Copy key" button reuses the same routine; the button's
  "Copied ◆" (2s) is the visible feedback for both. Root cause: the Copy button EXISTS in the
  identity file (`#keyCopyBtn`, wired by `__chainShowKey`) but only shows once the certificate is
  certified — on the proof-host page the claim failed (item 4), so the certificate never stamped
  and the button never appeared. Separately the device-key pill itself had no click handler.

### Worker — `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js`
- Base: 8,321,721 B, sha256 `9a993d2d70cdf7d565fd30656d121ebb1184850840e8d58c75d2629df7545473`, blob `b3001cfe…`
- New: **8,326,561 B, sha256 `2a348c2d6354646142202ce3709f28417a8276c847decca70f4dcfdefaf599d0`**, blob `95191dfde4b9…`
- Built twice from the patched builder, byte-identical both runs. Embeds verified by sha256:
  WALK `4b5f9264` (4,359,566 B), IDENTITY `803e7ea8` (388,608 B), WELCOME `c8581fca`
  (1,857,688 B), UNFOLD `984d87af` (104,853 B), PERSONAL_TEMPLATE `61002d15` (1,486,773 B).
  FIX2 markers present in the worker: `bridge-agreed`, `__chainApiBase`, `doCopyKey`,
  `access-control-allow-origin`, `OPTIONS`, `flex-wrap:nowrap;overflow-x:auto`, plus all round-1
  chain markers (`goBridgeAfterAgree`, `fpBridgeToName`, `fpBridgeAgreed`, `__chainShowKey`,
  `keyPanel`, `Use my key`).

### Builder — `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py`
- Base: 90,333 B, sha256 `1cf5500c…`, blob (round-1 filed).
- New: **90,917 B, sha256 `594044eeb0a64dcbe2e96b50cd91532f2e67aa3aec51ed522eafc2b858e11b3f`**, blob `582b2804a4ef…`
- **CORS (item 4):** `JSONH` now includes `"access-control-allow-origin": "*"`,
  `"access-control-allow-methods": "GET, POST, OPTIONS"`,
  `"access-control-allow-headers": "content-type"`.
- **OPTIONS preflight (item 4):** branch at the top of the worker's `fetch` handler:
  `if (req.method === "OPTIONS" && p.startsWith("/api/")) { return new Response(null, { status: 204, headers: JSONH}); }`
- Assert shas updated to the new welcome (`c8581fca`) and identity (`803e7ea8`) shas.

### Image branches — item 5 (no page bytes changed)
Root cause: the image files were never attached to any repo tree at the referenced paths. Welcome
deck images (19) under `team-nitro/deck-royal-unfolding-20261115/` with ref
`deck/royal-unfolding-20261115`; unfold images (17) under `team-nitro/agreement-unfold-20261117/`
with ref `agreement/unfold-20261117`. BOTH branches did not exist (GitHub 404 on both branch
lookups); the directories 404ed on proof-host and on the GitHub contents API. Only the blobs
existed as orphans (the `cb=` values in the URLs ARE the blob shas). Staging `/agmt-*` assets serve
fine (200, from worker KV `WELCOME_ASSETS`) — those were never the problem.
- Created branch **`agreement/unfold-20261117`**: tree `1c136133b8bf`, commit `1505b49c46f8`
  (17 files, root commit).
- Created branch **`deck/royal-unfolding-20261115`**: tree `fc4f3d092393`, commit `eeff27852811`
  (19 files, root commit).
- Both trees hold exactly the referenced image files at the referenced paths, built from the
  pre-existing orphan blobs (e.g. face-1.jpg blob `8743e1868400…`, 484,837 B; deck-logo.jpg blob
  `c7d274c3ba51…`, 387,675 B). All 36 blob verifications passed.
- Proof-host verification after branch creation (fresh `t=` cache-buster, 2026-11-18): all five
  sampled URLs **200 with exact blob sizes** — deck face-1.jpg 484,837 B; deck slide-1.jpg
  287,005 B; deck deck-logo.jpg 387,675 B; unfold face-1.jpg 484,837 B; unfold welcome-0.jpg
  310,452 B. The remaining 31 share the same branches/trees, verified by blob existence + tree
  attachment.

### Item 3 — taken alias (no code change)
Verified statically — code is CORRECT. `checkAliasAvailability` (identity line 2291) sends this
browser's `nayanet_vault_key` and grants `own` ONLY on registry `d.own`; otherwise
`taken`/`neutral`. The silent restore calls it with the stored alias + this browser's key. The
eye's same-device grant is the designed same-device recognition. **Live clean-profile proof is
still owed** — a taken alias on an unknown device must ask for the device key and must NOT grant
on name alone. That proof needs a working browser; see §6.

### Drivers filed in the same commit
`walkthrough-chain-fix2-20261118/work/stage-fix2.py` (blob `b2767166ab7d…`),
`fix-images.py` (`da69e010016e…`), `patch-builder-cors.py` (`2fdc7965b05c…`),
`fetch-bases.py` (`b5df44dfb5ec…`). `verify-fix2.py` + `law-fix2.py` + this report to follow in
a second commit on the same branch.

## 3. Syntax checks (all passed)
- `node --check` (stdin, no temp files — EPERM blocks temp writes): welcome 3 script blocks
  (26,467 B / 11,686 B / 74,822 B) OK; identity 1 script block (50,056 B) OK; built worker as ES
  module (`--input-type=module`, 8,326,561 B) OK.
- Builder compiles (`compile()` in-process; `py_compile` writes `__pycache__` and EPERMs).

## 4. Staged links — served bytes verified by full sha after staging
Staging worker: `https://naya-walk-beginning-staging.nayapower.workers.dev/`

| Route | Served | sha256 (first 12) | Match |
|---|---|---|---|
| `/` | 1,857,688 B | `c8581fca0a69` | new welcome ✓ |
| `/agreement` | 104,853 B | `984d87aff1a0` | unfold unchanged ✓ |
| `/welcome` | 4,359,566 B | `4b5f926423d7` | walk unchanged ✓ |
| `/identity.html` | 388,608 B | `803e7ea8a782` | new identity ✓ |
| `/?stage=bridge` | 1,857,688 B | `c8581fca0a69` | new welcome ✓ |
| `/?stage=deck` | 1,857,688 B | `c8581fca0a69` | new welcome ✓ |
| `/?stage=letter` | 1,857,688 B | `c8581fca0a69` | new welcome ✓ |

All 7 routes byte-identical on attempt 1 (verified twice, 2026-11-18 ~23:52Z and ~23:53Z).

Proof-host links (byte-identical, full sha verified):
- Welcome: `https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/walk-v23-assembly-20261114/welcome-staged.html&ref=walkthrough/chain-fix2-20261118&cb=868c746d1219b376419e8d49631dcd920256b45f&t=1795045874`
  — 1,857,688 B, sha `c8581fca…` ✓
- Identity: `https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/walk-v23-assembly-20261114/identity-fixed.html&ref=walkthrough/chain-fix2-20261118&cb=c0a351221d48948d950dba0146e393709790e435&t=1795045876`
  — 388,608 B, sha `803e7ea8…` ✓

## 5. §11 design-laws check (in writing)
`check-design-laws.py` run on base blobs (fetched from the parent tree by sha, checked in memory)
vs the new files, plus the checker CLI on the new files:
- Welcome: base **83 FAIL / 4 WARN** → new **83 FAIL / 4 WARN**. Zero new failures, zero new
  warnings, zero gone.
- Identity: base **11 FAIL / 2 WARN** → new **11 FAIL / 2 WARN**. Zero new failures, zero new
  warnings, zero gone.
- The 83/11 failures are the pre-existing round-1 baseline (gray-text / sub-17px / text-color
  literals the checker flags across the whole file); my diff adds none and removes none. The
  checker CLI on the new files confirms the same counts. The eye still owes the non-machine
  checks (flat/dead, flow, harvest, read-as-a-reader) — which is exactly what the live
  click-through below is for, and it could not run.
- My changes stay inside the laws: the onward pill keeps its gold `#d4a017`; the footer strips
  keep their existing colors, only their wrapping changes; the Copy wiring reuses the existing
  button style; no new text below 17px, no new gray, no redesign, nothing moved or removed that
  was not instructed.

## 6. Live click-through evidence — NOT PROVEN, stated plainly
**No live browser works in this VM right now, so no item below is proven live. Nothing in this
section is claimed verified.**

- VM browsers re-tested 2026-11-18 ~23:55Z: Playwright Chromium SIGTRAP at launch (same as
  ~23:05–23:10Z); Playwright Firefox killed at launch (same as before). The launch crash happens
  before any network, so the localhost forwarding proxy cannot fix it.
- `probe1.py` (Playwright Firefox probe) never produced a result. jsdom install failed (npm
  EPERM on cache write).
- What IS proven without a browser: all 7 staging routes serve the new bytes (full sha, §4);
  both proof-host pages serve the new bytes (full sha, §4); 5 sampled images 200 with exact blob
  sizes (§2); all script blocks + the worker pass `node --check` (§3); the bridge wiring, the
  CORS branch, the absolute API base, and the Copy routine are present in the served bytes
  (marker checks in the stage driver: `bridge-agreed`, `__chainApiBase`, `doCopyKey`,
  `access-control-allow-origin`, `OPTIONS`, `flex-wrap:nowrap;overflow-x:auto` all found in the
  built worker; the worker embeds verified by sha).
- What is NOT proven live and must be walked by the cloud-browser eye before this goes anywhere
  near Shawn: (1) agree→bridge→name-entry on all four end paths, at 1920 / 635 / 390 / 534, with
  the onward pill gold and the post-agree column purple / emerald / gold / purple; (2) Copy
  clicked with "Copied" feedback; (3) taken-alias key prompt on a CLEAN profile; (4) proof-host
  identity claim completing with certificate number + device key + Copy; (5) images rendering
  (not just 200ing); (6) footer clear at 635 AND 390 with measured widths. The bridge/key
  presentation 10/10 scorecard cannot be honestly given from bytes — the eye must judge the
  render.

## 7. EPERM flake — what it cost this round (recorded for the next seat)
The flake is at its worst tonight: python `open()` creates 0-byte files and `write()` EPERMs or
silently lands 0 bytes; shell `cp` and redirects EPERM; `python3 script.py > file` exits 120 with
a 0-byte file (reproduced twice); `py_compile` EPERMs on `__pycache__`. Workarounds used and
proven: `node --check -` via stdin; `compile()` instead of `py_compile`; builder output captured
via `subprocess` pipes (never stdout redirect); all GitHub operations via the blob/tree APIs
(no local writes); the Cloudflare PUT done in-process by loading `cf-worker.py` as a module and
calling its own `authed_req`/`run` — the token stays inside the registered connector helper
(dynamic_credentials surrogate) and was never seen, logged, or stored. The local worker copy
(`walk-beginning-staging-worker.js`) could NOT be written — restore it from the filed blob
(`95191dfde4b9…`, 8,326,561 B, sha `2a348c2d…`) once the flake clears.

## 8. DONE and NOT-DONE, plainly

**DONE (staged + byte-verified):**
1. Bridge opens post-agree with all four choices + onward pill visible on arrival; `bridge-agreed`
   persists across refresh/reopen; pre-agree bridge untouched. (Bytes only — live proof owed.)
2. Copy: device-key pill clickable + existing Copy button shares one routine with "Copied ◆"
   feedback. (Bytes only — click proof owed.)
3. Taken alias: verified the code already grants only on registry `d.own`; no code change needed.
   (Clean-profile live proof owed.)
4. Proof-host claim: absolute API base + worker CORS (JSONH + OPTIONS preflight). (Live claim
   proof owed.)
5. Images: both branches created with all 36 files at the referenced paths; 5 sampled proof-host
   URLs 200 with exact sizes. (Render proof owed.)
6. Footer: both legal strips one-row at 534, bridge scroll area +72px clearance at ≤640px.
   (Measured-width proof owed at 635/390.)
7. Filed: branch `walkthrough/chain-fix2-20261118`, commit `a89e10aedd35…`, all 8 blobs read-back
   verified; worker PUT HTTP 200; all 7 routes + 2 proof-host links sha-verified.
8. Laws: zero new violations, zero new warnings (welcome 83/4, identity 11/2, identical to base).

**NOT DONE (do not claim):**
- Live click-through proof for ANY of the six items — VM browsers dead; the cloud-browser eye
  must walk it. This is the whole gap between this report and "verified".
- Item 4 sub-items from the eye verdict, not yet diagnosed or fixed: name rendered twice on the
  proof-host identity page ("Novaeyetest" + a separate "Nova Eye Test" textbox pill); top corner
  emblems clipped at 1920; text overlaps at 534 on the identity page.
- "Create a new account goes straight to name entry" — no code change made; that is the plain
  login flow as designed. Note it as designed-or-owed, not fixed.
- Local worker copy not written (EPERM) — restore from the filed blob when the flake clears.
- Bridge/key presentation 10/10 scorecard — cannot be given from bytes; the eye must judge it.
