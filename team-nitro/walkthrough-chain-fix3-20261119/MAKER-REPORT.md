# Walkthrough Chain Fix Round 3 — MAKER REPORT

**Maker seat, staged only. No PR, no merge, no live deploy, no message to Shawn.**
**Branch:** `walkthrough/chain-fix3-20261119` · **Parent:** fix2 tip `7181266f91c15315fa574f00eabcce6422e89b5a`
**Round version (captain's stop order, 2026-11-19 ~03:00 MST): fix3c** — built 03:00, live-probed 03:04.
**Branch tip:** commit `34a733823e24be10b2ae86588cbf4258d103789b` (commit 3 of 4; commit 4 files this report + the remaining work records).

## Verdicts first

| Item | Verdict | Proof |
|---|---|---|
| (1) BRIDGE | **DONE** | Live Firefox probe, fix3 staging (evidence/fix3-live.json) |
| (2) COPY | **DONE** | Live probe: pill tap → "Copied ◆", clipboard holds the key |
| (3) TAKEN ALIAS | **DONE** | Live probe: `jordantest` → note + key panel, ENTER dim |
| (4) PROOF-HOST CLAIM | **DONE** (one named caveat) | Cert Nº 000842 + Nº 000846 show the alias's own name; staging redirect lands on the real walk |
| (5) IMAGES | **PASS — untouched** | Per brief |
| (6) FOOTER, bridge strip only | **DONE** | Live probe: 55px, every link 38px one-line at 534 and 390 |
| (7) ADJUDICATE | **DONE** | Cert overlap fixed + proven (0 overlaps); crests fixed + proven; hero echo fixed + proven; Jump-back-in + heading/portal + audio adjudicated not-a-defect with evidence |

Nothing in this round is claimed from a report number. Every DONE above rests on bytes I read back myself (git blob API, curl sha) or on a live Firefox click-through in this VM against the staged bytes.

## Staged version — the shas

| File | Bytes | sha256 | Blob (filed) |
|---|---|---|---|
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,860,839 | `d79793c0d9b74121e83c0c65fed095e6d0dd278481b60c7a2b339bbe9231c934` | `c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f` |
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 397,308 | `88c19001f9e5738de867a43994955c79593fdbdb48c57a89a582398db4a57b88` | `ee6a99aeb4a56262f978ff7685b7b5d343a6fede` |
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 105,308 | `3252948ed7f80157d0fa86fd730dc2e535a749f00e80944f0274ded54eb6a0f8` | `8980e57786c9bb196fb1ac5252f483995228e337` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,339,176 | `33cbda41030651ee0dc359f9466086c688c44b2136050a31097e70d6d48849cd` | `290111b63b12f7f853dbc1ff06246323d24a2f7a` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | — | asserts welcome `d79793c0`, identity `88c19001`, unfold `3252948e` | `fbd11f5e2af13dbc0e8449452a93a98590e669e9` |

Worker embeds verified by sha after the build: WALK `4b5f9264` (4,359,016 B stored), IDENTITY `88c19001`, WELCOME `d79793c0`, UNFOLD `3252948e`, PERSONAL_TEMPLATE `61002d15`.

**Staged:** `https://naya-walk-beginning-staging.nayapower.workers.dev/` — all 7 routes curl-verified byte-identical by sha256 after the PUT (STAGE-RESULT3, 03:02 MST):
`/` = welcome `d79793c0…`; `/agreement` = unfold `3252948e…`; `/welcome` = walk `4b5f9264…`; `/identity.html` = identity `88c19001…`; `/?stage=bridge`, `/?stage=deck`, `/?stage=letter` = welcome `d79793c0…`.
Proof-host pages verified by full sha: welcome (`cb=c66e2fa2…`) = `d79793c0…`; identity (`cb=ee6a99ae…`) = `88c19001…`.

**Commits on the branch** (all read-back verified by full blob sha):
- Commit 1 `9a1109b32baff414b1b4b4fa7249665abcf18f47` — fix3 (welcome + identity `22a1ae61` + unfold + worker `7b058fde` + builder + drivers).
- Commit 2 `76614270c12f6a93081e5ca3e6da07f5ee391ac3` — fix3b (crest rotated-box 32px offsets; identity `6a4615b6`, worker `231e59a2`).
- Commit 3 `34a733823e24be10b2ae86588cbf4258d103789b` — fix3c (certified-534 fit; identity `88c19001`, worker `33cbda41`).
- Commit 4 (this report + remaining work records) — filed after this report; see branch tip in the coordinator handoff.

**Builder-sha correction (carried from the fix2 checker, do not rebuild on the wrong number):** the filed fix2 builder hashes to `0cd80c8532baf7de159cfdef6ff5108ed57242c0448a02ef58cdee1295ad7003`, NOT the `594044ee…` in the fix2 maker report. The fix2 maker report's number is wrong; the filed blob is the truth.

## Diagnosis — why the eye saw what it saw (reconciled with the fix2 checker trace)

Fix2's code was statically correct for the **in-page** paths, and the fix2 checker trace (§ code-path traces) said `goBridgeAfterAgree` / `render()` were correct — true for the in-page paths only. The eye walked the **cross-page** path, and that path was broken in three places fix2 never touched:

1. The `/agreement` page is a separate file (unfold). Its agree button **navigates** to `/?stage=bridge` on the staging origin — it cannot call the welcome page's `goBridgeAfterAgree()`. Fix2 explicitly left that arrival pre-agree (its own comment: "`/agreement` agree → bridge still land here with the agreed line and the onward button hidden").
2. On `/?stage=bridge`, the welcome boot hook calls `enterStage('bridge')`, which hides G2/G3/G4/Final, shows More1, and hides the AGREED line and the gold onward pill.
3. The boot restore is suppressed whenever `?stage=` is set (`_fpRestoreStage` forced null), and `render()`'s save branch **wipes the saved `bridge-agreed` key on that arrival**. The agreed state was actively destroyed by the arrival itself.

That is the whole of item 1: the state the eye's path needed was never set, and the arrival destroyed it. The fix carries the state with the navigation instead of relying on the in-page handler.

## Per-item record

### (1) BRIDGE — DONE

**Changes** (welcome-staged.html + agreement-unfold-fixed.html):
- Unfold sets `localStorage.setItem('nayanet_fp_stage','bridge-agreed')` and `localStorage.setItem('nayanet_fp_agreed','1')` **before** navigating to `/?stage=bridge`.
- Welcome keeps a durable agreed key `nayanet_fp_agreed`, set in `goBridgeAfterAgree()`, surviving `exitStage`, cleared only by the gold pill.
- `enterStage()` re-enters the post-agree bridge from the agreed key on `?stage=bridge` or plain re-entry; the boot restore also restores from the agreed key.
- New `goBridgeToName()`: the gold pill clears the agreed keys, exits the stage, then clicks `#newAccountLine` if the returning view is showing, so the name form opens directly — no extra "Create a new account" click — and focuses `#userName`.
- Boot-restore guard (my fix to the earlier unfiled attempt, which had no URL guard and would have hijacked `?stage=deck` / `?stage=letter` back to the bridge): `else if(!_fpStage && (_fpRestoreStage==='bridge-agreed' || _fpAgreedKey))`.

**Live proof** (`work/probe-fix3-live.py`, evidence/fix3-live.json, screenshots `fix3-live-A-*.png`):
- Agree on `/agreement` → `/?stage=bridge` at 534: view `bridge`, all five groups + Final visible, AGREED line + gold pill "Continue — enter your name" visible, `lsStage=bridge-agreed`, `lsAgreed=1`.
- Reload at 534: identical state — agreed state visibly persists.
- Gold pill click: entry form visible, `#userName` **focused** (`userNameFocused=true`), returning view hidden — name entry with no extra click.
- `?stage=deck` with the agreed key set: stays `deck`, bridge hidden — the guard holds, no hijack.
- Direct `?stage=bridge` with no agreed keys: correctly shows the pre-agree bridge (G1 only, More1, agreed/onward hidden) — that is the right state for a citizen who has not agreed.

### (2) COPY — DONE

**Root cause:** the handler WAS bound and the clipboard write SUCCEEDED (repro: pill tap set the Copy button text to "Copied ◆" and `navigator.clipboard.readText()` returned the key). The feedback was invisible because the Copy button carries class `cert-more` and `.cert-plaque.is-certified.cert-more { display:none }` hides it on every certificate. Also `doCopyKey` showed "Copied ◆" even on clipboard failure (`.then(done, done)`).

**Changes** (identity-fixed.html): the Copy button gets its own visible `.key-copy` style (obsidian pill, white word, sapphire `#0f52ba` rim + glow) and no longer carries `cert-more`; `doCopyKey` shows "Copied ◆" on the `#keyValue` pill itself AND the button, **only on real clipboard success**, with a `textarea`+`execCommand` fallback (failure shows nothing).

**Live proof** (fix3-live.json `E_copy_after_pill_tap`, `E_copy_clipboard`; screenshot `fix3-live-E-copy-1920.png`): pill tap on the certified certificate → `keyValueText="Copied ◆"`, `keyCopyText="Copied ◆"`, both visible; `navigator.clipboard.readText()` returned the actual key `nayanet_key_72vumj4m82e`.

### (3) TAKEN ALIAS — DONE

**Root cause:** the code path the fix2 checker traced (ENTER → note + unhide `#keyPanel`) only fires on ENTER, not on the availability result itself. Typing a taken alias showed only "already claimed".

**Changes** (identity-fixed.html): `setAliasState('taken')` now opens the note + `#keyPanel` on the availability result itself; ENTER stays dimmed (`activate-btn dim`), never armed as if the alias were free.

**Live proof** (fix3-live.json `E_taken_jordantest`; screenshot `fix3-live-E-taken-1920.png`): typing `jordantest` on the clean proof-host identity page → status "already claimed", note visible ("That alias is already claimed. If it is yours, use your device key below — a name alone never opens it."), `keyPanelVisible=true`, ENTER dim.

### (4) PROOF-HOST CLAIM — DONE (one named caveat)

**Root cause (name leak):** the claim POST already sent the paired `finalName`, but `activateAndRedirect` stored `localStorage.setItem('nayanet_smart_name', rawName || prettyName(finalAlias))` — the load-time `rawName` — and `stampCertificate` paints the hero from that stored name.

**Changes** (identity-fixed.html): `currentDisplayName(alias)` computes the claim name live at ENTER from the claimed alias and its paired name (passed name only with its own paired alias; saved name only with its own saved alias; otherwise the alias title-cased); `activateAndRedirect` uses `currentDisplayName(finalAlias)` for the POST, and the stored name line is now `finalName` (was `rawName || prettyName(finalAlias)`).

**Live proof — name:** fresh alias `fix3livecheck` claimed with a stale `?name=Jordan Test` in the URL → Certificate Nº **000842**, `lsName="Fix3livecheck"` (not "Jordan Test"). Re-proven on fix3c: `fix3certc` → Nº **000846**, hero "Fix3certc", `lsName="Fix3certc"`.

**Live proof — landing:** staging `/identity.html`, fresh alias `fix3redirect`, ENTER (no route abort) → landed on `https://naya-walk-beginning-staging.nayapower.workers.dev/welcome`, body "Tell me who you are, in your own words…" — the **real walk**, `lsName="Fix3redirect"` (`work/probe-staging-redirect.py`).

**Caveat (named, not hidden):** on the **proof-host origin itself**, `/welcome` still serves the proof host's white file-server page — the proof host serves files from GitHub, not the walk, so a relative `/welcome` redirect has no walk behind it there. That is a property of the proof-host worker, not of the identity page: the page's relative redirect is correct on any origin that serves the walk (staging proven above). Follow-on, not a page defect: either serve the walk at proof-host `/welcome`, or walk staging `/identity.html` for the claim path. I did not modify the proof host — it is outside this round's files.

### (5) IMAGES — PASS, untouched

Per brief. Nothing touched.

### (6) FOOTER, bridge strip only — DONE

**Root cause:** fix2 claimed both strips one-row (nowrap + sideways scroll). The probe proved the bridge strip was not: at 534/390 it was 91px tall vs 55px entrance, every multi-word label wrapping to two lines.

**Changes** (welcome-staged.html): the bridge strip links get `flex:0 0 auto;white-space:nowrap` under the bridge-only selector. Entrance strip untouched.

**Live proof** (fix3-live.json `A_after_agree_534`, `C_bridge_footer_390`, `C_bridge_footer_534`): bridge strip 55px at 534 and 390; every link 38px tall, one line ("Acceptable Use" 123px, "Community Guidelines" 171.8px, "Copyright / DMCA" 139.3px, "Ambassador Terms" 147.6px, "Membership & Billing" 163.6px — all single-line widths). The overlap is NOT chased: `#fpBridge` ends 51px above the strip — nothing touches, not a defect (per brief).

### (7) ADJUDICATE AND FIX WHERE REAL — DONE

**Identity certificate text overlaps at ~534 — REAL, FIXED, PROVEN (fix3c).**
The fix3b live probe (evidence/fix3b-live.json, screenshot `fix3b-live-C-cert-534.png`) measured the certified certificate at 534 and proved the eye right: the name tucked 9px under "This certifies that"; the stale "Available — it's yours to claim." status printed across the member sentence's second line (22px overlap); the Smart Link label caught its last 3px; and the "Pick a different alias" switch pill straddled the plaque's bottom edge. Root cause: the certified document is ~41px taller than its 706px face at 534×900, and the grid's `align-items:center` splits the foot's overflow equally up and down, so the foot spills UP into the center row.
Fix (certified + `max-width:640px` only; desktop and the composing state untouched): the card grows 36+8px (main `padding-bottom` + back-row padding released while certified via `:has()`); the head gives 20px (face + head padding); the stale status line is hidden while certified; the foot aligns to the top of its track (`align-self:start`); the foot trims 20px (Copy pill, ENTER, regalia, switch margins).
**Live proof** (`work/probe-fix3c-live.py`, evidence/fix3c-live.json, screenshot `fix3c-live-A-cert-534.png`): certified `fix3certc`, Nº 000846, at 534 — **overlaps: []** (zero). Name clears "This certifies that" by 19px; member sentence clears the Smart Link label by 16px; status hidden; plaque grew 708→752px; switch pill y=796–829, **inside the plaque** (plaque bottom 850). I read the screenshot as a reader: the certificate is clean, nothing crosses, nothing is cut.

**Top corner emblems clipped at 1920 — REAL, FIXED, PROVEN (fix3b).**
Cause: the crests used `translate(±50%, ±50%)`, centring each emblem ON the plaque corner so half hung outside the viewport (probe: x=-57 TL, right edge 1977 TR). The translate removal alone left 7px clipped at 1920 (x=-7, right 1927) — a 100×122 box rotated 59° has a 156×149 axis-aligned box, so its centre must sit ≥78px from the edge; at 20px the centre is 70px in. Fix: large-variant offsets 20px → 32px (centre 82px in, ~4px clearance). **Live proof** (fix3c-live.json `A_crests_1920`): all four crests inside at 1920 (x=5, right=1915, `clipped:false`); at 534 also all inside (x=5, right=529). Same emblem, same rotation, same corner.

**Name rendered twice on proof-host identity — REAL, FIXED, PROVEN.**
Cause: the composing hero echo painted `prettyName(currentAlias)` (sanitized, no spaces) while the field shows the typed words with spaces. Fix: the dead `titleName` helper is wired into the echo (`paintHeroName(titleName(aliasInput.value))`). **Live proof** (fix3-live.json `E_hero_echo_nova`): typing "nova eye test" → hero "Nova Eye Test" (was "Novaeyetest" + "Nova Eye Test").

**"Jump back in" buttons truncated at ~534 — NOT REPRODUCED, not a defect.**
Two earlier probe runs reported the returning view hidden; both used Playwright `add_init_script` to seed localStorage — and a direct diagnostic proved **`add_init_script` does not run in this VM's Playwright/Firefox setup** (`window.__initRan` stayed `None`, alias stayed `null`). That was a probe-harness failure, not a page failure. Re-probed the reliable way (set localStorage via `evaluate`, reload): the returning view shows, stage stays closed, and both buttons are whole — "Jump back in →" 214×41, `scrollW==clientW==212`, `truncated:false`; "Jump back in as Walker Test →" 227×31, `scrollW==clientW==225`, `truncated:false` (fix3c-live.json `B_returning_534`; screenshot `fix3c-live-B-returning-534.png`). No change made.

**Main heading clipped by portal circle at ~534 — NOT REPRODUCED, not a defect.**
Measured on the login view at 534 (fix3-live.json `D_login_returning_534`): the visible heading "The Collective Agreement" (x=30, y=201, 474×31) ends at y=232; the portal circle starts at y=232 (x=53–481, y=232–660). They touch exactly; they do not overlap. No change made.

**Talk/Play audio produced no audible output — NOT A DEFECT IN THIS ENVIRONMENT, not rebuilt.**
Measured live (fix3-live.json `D_audio`): after clicking Play, `speechSynthesis.getVoices()` returns **0** voices, `speaking=false`, `pending=true`. The page queues the utterance (the code works — `speak()` was called and is pending) but a headless/cloud browser has no speech voice to sound with, so nothing can be heard. There is nothing in the page to fix for that; rebuilding audio would not put a voice in the browser. Per the brief I did not rebuild audio. What remains is an ear-check on a real device — the captain's ear on Shawn's phone, not a maker item.

**A note on the earlier fix3b "failure" that was not one:** the direct `?stage=bridge` probe with pre-set agreed keys showed the pre-agree bridge — because the same context had first visited `?stage=deck`, and a deck/letter arrival wipes the agreed keys (see follow-on below). With no keys, the pre-agree bridge is the correct state. The probe design was at fault, not the page.

## Verification record (receipts)

- **node --check:** welcome 3 script blocks OK; identity 1 block (55,204 B) OK; unfold 2 blocks OK; built worker as ES module OK (re-run after every identity change; last run on the fix3c worker).
- **Design laws** (`work/law-fix3.py`, checker's own rules, base-vs-new, re-run after every change): welcome base **83 FAIL / 4 WARN → new 83 FAIL / 4 WARN**; identity base **11 FAIL / 2 WARN → new 11 FAIL / 2 WARN**. **Zero new violations, zero gone** — the same pre-existing round-1 baseline as fix2. CLI confirms the same counts (`check-design-laws.py`: welcome "83 violation(s), 4 warning(s)", identity "11 violation(s), 2 warning(s)").
- **Worker built deterministically** (builder run twice in the original fix3 build; fix3b/fix3c rebuilds assert the same embeds): fix3c worker 8,339,176 B, sha `33cbda41…`; embeds verified by sha (WALK `4b5f9264`, IDENTITY `88c19001`, WELCOME `d79793c0`, UNFOLD `3252948e`, TEMPLATE `61002d15`); FIX3 markers present (`nayanet_fp_agreed`, `goBridgeToName`, `flex:0 0 auto;white-space:nowrap`, `currentDisplayName`, `titleName`, `key-copy`, `bridge-agreed`, `align-self: start`, `padding-bottom: 0`).
- **Live Firefox probes** (the brief said browsers were dead in this VM — they are not; `playwright.firefox.launch` works here, which is why this round has live click-through evidence instead of static traces): `work/probe-fix3-live.py` (evidence/fix3-live.json + 12 screenshots), `work/probe-fix3b-live.py` (evidence/fix3b-live.json + 6 screenshots), `work/probe-fix3c-live.py` (evidence/fix3c-live.json + 2 screenshots), `work/probe-staging-redirect.py`. All JSON + PNGs are in `~/workspace/team-nitro/walkthrough-chain-fix3-20261119/evidence/` (PNGs kept in the workspace; JSONs filed on the branch).
- **EPERM flake, live:** the builder's file write reported success but the local worker file still held the old bytes (fix3b build) — recovered by `cp` + sha verification. Every write in this round was verified by size + sha after the write; no `python3 … > file` redirects were used.

## §11 design-laws check (in writing)

I read `THE-NAYA-DESIGN-LAWS.md` first, before touching code, and re-checked the work against it at the end. The laws base is the same pre-existing round-1 baseline (welcome 83 FAIL / 4 WARN, identity 11 FAIL / 2 WARN) — **zero new violations were introduced by this round, and none were removed**. The changes are behaviour and layout fixes inside the existing design language, not redesigns: no element was rebuilt from scratch; the bridge reuses the existing four-group + Final structure and the existing gold pill; the Copy button reuses the existing obsidian-pill language with a sapphire rim from the Smart Link family; the crest fix moves the existing emblems to fully-inside positions with the same artwork and rotation; the certified-534 fix funds space inside the existing grid (card growth, padding, alignment, trims) without changing the document's composition, copy, or colors. Nothing was removed that the brief did not instruct to remove; nothing the eye passed (images, desktop footer, entrance strip) was touched. The one genuine new §2.3-scale question the round surfaced — the 10px empty-orb invite caption from the Dashboard round — is not part of this round and is not re-litigated here.

## What is left unfinished (honest list — follow-ons, not silent iterations)

1. **Deck/letter arrival wipes the agreed keys.** A `?stage=deck` or `?stage=letter` arrival still clears `nayanet_fp_stage` / `nayanet_fp_agreed` (the `render()` save branch). The eye's path never hits it, and the chain path + reload persistence are proven — but a citizen who agreed and later visits the deck loses the agreed state. Follow-on if Shawn wants agreed state to survive a deck/letter visit.
2. **Proof-host `/welcome` routing.** See item (4) caveat: the proof host serves files, not the walk. Either serve the walk at proof-host `/welcome` or walk the claim path on staging `/identity.html`.
3. **Audio ear-check on a real device.** The page queues speech correctly; the headless browser has no voice. Whether Talk/Play sounds on Shawn's phone is for the captain's ear.
4. **Stale status text on desktop certified.** The "Available — it's yours to claim." line is hidden only at ≤640px (where it collided). On desktop certified it still shows — wrong words, but no collision and no layout effect. Cosmetic follow-on: hide it in the certified state at all widths.
5. **Registry cleanup (do NOT delete — owed later, per brief).** Test certificates created in this round, in addition to the eye's Nº 000839 (`nov19eyecheck`) and Nº 000840 (`proofeyecheck`): Nº 000841 (`fix3eyecheck`), Nº 000842 (`fix3livecheck`), Nº 000843 (`fix3cert534`), Nº 000844 (`fix3diag534`), Nº 000846 (`fix3certc`), plus `fix3redirect` (claimed on staging during the redirect probe; its certificate number was not captured in that probe). Nº 000845 sits in the sequence with no probe of mine to account for it — the registry owner should identify it before any cleanup. None of these rows were deleted by me.

## Files

- Report: `~/workspace/team-nitro/walkthrough-chain-fix3-20261119/MAKER-REPORT.md` (this file; filed on the branch in commit 4)
- Work records: `~/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/` (`fetch-bases.py`, `law-fix3.py`, `stage-fix3.py`, `resume-fix3.py`, `resume2-fix3.py`, `stage-fix3b.py`, `stage-fix3c.py`, `probe-fix3-live.py`, `probe-fix3b-live.py`, `probe-fix3c-live.py`, `probe-staging-redirect.py`, `worker-fix3.js`, `worker-fix3b.js`, `worker-fix3c.js`, `bases/`)
- Evidence: `~/workspace/team-nitro/walkthrough-chain-fix3-20261119/evidence/` (`fix3-live.json`, `fix3b-live.json`, `fix3c-live.json`, `fix3-repro-*.json`, 20 screenshots)
- Sources: `~/workspace/team-nitro/walk-v23-assembly-20261114/` (welcome-staged.html, identity-fixed.html, build-v23-staging-worker.py, walk-beginning-staging-worker.js), `~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html`
