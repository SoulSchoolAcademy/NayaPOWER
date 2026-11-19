# Walkthrough Chain Fix Round 6 — MAKER REPORT

**Maker seat, staged only. No PR, no merge, no live deploy, no message to Shawn.**
**Branch:** `walkthrough/chain-fix6-20261119` · **Parent:** fix5 tip `f79a03eb9c749f4b0eea2cf57ec8e91231371a84` (confirmed by ref lookup before filing)
**Staged:** `https://naya-walk-beginning-staging.nayapower.workers.dev/`
**Round version: fix6** — one defect (the fresh-device hole via the walk URL), both legs.

## Verdicts first — read this box before anything else

| Item | Verdict | Proof |
|---|---|---|
| THE FIX, SERVER LEG (completion refuses a non-owner key) | **FILED + STAGED + LIVE-PROVEN by API** | Three completion POSTs as `jordantest` (fresh key, missing key, fresh key again) all returned **409 `{"ok":false,"error":"taken"}`** on the staged worker; two full GET reads of the stored completion after the refusals agree byte-identical (2,227 B, sha `7f2465aa…`); claim row intact (cert Nº 000837, `own:false`). See § "Live API probes" and `evidence/fix6-api.json`. |
| THE FIX, CLIENT LEGS (walk load check + identity URL-arrival check) | **FILED + STAGED, NOT presented as render-proven** | Both gates are in the filed and staged bytes (shas below), traced line by line, node-checked. The browser probe that would prove the bounce + flag on a render **could not run — both VM browsers are dead** (see § "What was NOT live-proven"). Per the brief, the client legs are **not** presented as render-proven until `probe-fix6-live.py` runs. |
| THE DIAGNOSIS (fix-5 checker §2) | **CONFIRMED from the filed bytes, with one correction** | The walk URL path was real exactly as the checker proved it. One correction: the completion POST **already carried `device_key`** — `cred()` (WALK line 1660) puts `ID.device_key` (from `nayanet_vault_key`) in every completion payload, so no walk change was needed for the POST's key; only the server refused to check it. See § "Diagnosis". |

Nothing in this round is claimed from a live render I did not see. Every DONE above rests on bytes I read back myself (git blob API, curl piped to sha) or on a code trace from the filed blobs, or on live API probes I ran and quote verbatim.

## Diagnosis — the hole, and the one correction

**The defect as briefed (checker §2, re-proved, not re-litigated):** fix-5 closed the identity ENTER path, but a fresh device could open `/welcome?name=…&alias=jordantest` directly: walk `ingest()` (WALK 1635–1648) stored the pair into localStorage unchecked; the walk made no load-time ownership check (`api(` once in 2,589 lines, line 1883, the completion POST); and `/api/welcome/complete` wrote the project, Box, and pages keyed by alias alone with no `device_key` reference and no row lookup.

**What I traced before touching code (from the fix-5 filed blobs):**
1. **The walk URL path was real.** `ingest()` stores any `?alias=`; `ID` (1649–1653) reads straight from localStorage; boot (the `(function boot(){…})()` at the end of the walk script) resumes at the first unanswered step or shows the door — no ownership verdict anywhere before `showStep`/`showDoor`.
2. **The completion POST already carried the key — the brief's item (c) was half right.** `cred(extra)` (line 1660) builds `{ alias, device_key: ID.device_key, name }`, and `completeWalk` (1880–1883) posts `cred({answers, topics, pageNames})`. `ID.device_key` is `lsGet('nayanet_vault_key')` — a fresh device sends `''`. So the client half of leg 2 was already done; the missing piece was purely server-side: the worker's complete handler never read `b.device_key` and never called `sbGetRow`. **No walk edit was made to the completion POST** — there was nothing to add.
3. **The bounce target needed a real change, not just a redirect.** Identity on load only ever checked the *saved* alias, silent (`if (restoreAlias) checkAliasAvailability(restoreAlias, true)`), and `passedAlias` (captured at load) was never fed to a check — a plain redirect to `/identity.html?name=…&alias=jordantest` would have landed composing with an empty field and no flag. The silent restore deliberately paints `neutral` for taken rows (v2.6/v2.7), so the redirect alone could NOT show the flag + key panel. That is why leg 1 carries a small identity change alongside the walk gate.
4. **The server lookup to harvest already existed.** `sbGetRow(alias)` (worker template, in the builder) selects `alias,name,device_key,cert_no,created_at` and is exactly what GET `/api/claim` uses for its `own` verdict. No new lookup was invented.

## The fix — both legs, three small edits, all additive

**1. Walk load check (walk-beginning-fixed.html, +26/−0 lines, two hunks).** Boot wraps its resume in `proceed()` and gates it on a verdict GET — the same endpoint the identity typing check uses, read with this browser's key if it has one, 4 s timeout, mirroring the fix-5 gate's shape:
- Taken + not-own → `window.location.href = '/identity.html?name=…&alias=…'` **before** `showStep`/`showDoor` runs — the questionnaire never renders for a non-owner.
- Own / available → `proceed()` (the existing resume/door, untouched inside).
- Failed or timed-out verdict → `proceed()` — the walk never hangs on this read; the server leg is the backstop.
- No alias at all → `proceed()` immediately (the door, as before).

**2. Identity URL-arrival check (identity-fixed.html, +13/−0 lines, one hunk).** After the silent saved-alias restore:
```js
if (passedAlias) {
  var pa6 = passedAlias.toLowerCase().replace(/[^a-z0-9]/g, '');
  if (pa6) { aliasInput.value = pa6; checkAliasAvailability(pa6); }
}
```
The LIVE (non-silent) check: taken → `setAliasState('taken')`, which unhides `#hubNote` (taken text) + `#keyPanel` (fix-3 code, unchanged); own → certifies; available → arms ENTER. It runs after the silent restore, so its higher `aliasSeq` wins the race. The fix-5 ENTER gate is untouched (`verdictChecked` ×2, gate comment at line 2689, verified); fix-4's hide rule is untouched (lines 1338/1380, `display: none`, count 2).

**3. Server completion gate (build-v23-staging-worker.py, in the `/api/welcome/complete` POST handler, before any write).** Harvests `sbGetRow`:
```js
const dk6 = String(b.device_key || "").slice(0, 64);
const claimRow6 = await sbGetRow(alias);
if (claimRow6 && claimRow6.device_key && (!dk6 || dk6 !== claimRow6.device_key))
  return j({ ok: false, error: "taken" }, 409);
```
- A row whose `device_key` is set refuses a missing or mismatched key with 409, **before** the project PATCH/insert, the Box write, the page writes, and the KV mirrors — no writes on the refused path.
- A row with **no** `device_key` set is NOT refused — the same rule POST `/api/claim` uses for its own 409 (`if (row.device_key && row.device_key !== device_key)`). A legacy pre-key row's owner is not bricked by a completion they cannot key.
- **No claim row exists → proceed as today.** That is a carried observation, not a redesign of the claim flow: a completion for a never-claimed alias still writes, exactly as before this round. The claim flow itself is untouched.

**Diff vs the fix-5 filed bytes (my own unified diff of the filed blobs):**
- Walk +26/−0, 4,359,566 → 4,361,146 B (+1,580 B), hunks at boot only.
- Identity +13/−0, 400,253 → 401,040 B (+787 B), one hunk at the load check.
- Builder +24/−9, 91,680 → 92,708 B (+1,028 B), three hunks: walk assert, identity assert (+comment), server gate. The −9 are the old assert/comment lines replaced, not behaviour removed.
- Worker 8,342,190 → 8,345,689 B (+3,499 B); embeds verified by sha (below). Welcome, unfold, template byte-identical to fix-5.

## Staged version — the shas

| File | Bytes | sha256 | Blob (filed, commit 1) |
|---|---|---|---|
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html` | 4,361,146 | `b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773` | `7b8fe1bfbfe7d821c6e268890c682080421ff920` |
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 401,040 | `3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c` | `7920438ed488869f29d520fd8dcd590061cb6586` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,345,689 | `ca77517805448215af523f3c2a68ed2cba4da519220ecc8c56af2e04ae185ab7` | `9d15c3090eaec3a0288b4ea6df25daf80ecc63b2` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 92,708 | (asserts moved walk `4b5f9264` → `b6befc33`, identity `6f805eba` → `3279dc35`) | `f3ca4bb3bc9b58a4602147a390418915054a0887` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,860,839 | `d79793c0d9b74121e83c0c65fed095e6d0dd278481b60c7a2b339bbe9231c934` (unchanged, fix-3) | `c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f` |
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 105,308 | `3252948ed7f80157d0fa86fd730dc2e535a749f00e80944f0274ded54eb6a0f8` (unchanged, fix-3) | `8980e57786c9bb196fb1ac5252f483995228e337` |

Worker embeds verified by sha after the build (builder run twice, identical sha `ca775178`): WALK `b6befc33` (4,361,146 B), IDENTITY `3279dc35` (401,040 B), WELCOME `d79793c0`, UNFOLD `3252948e`, PERSONAL_TEMPLATE `61002d15`. The FIX6 markers (`FIX6 (2026-11-19`, `gateDone6`, `claimRow6`, `dk6`) and the FIX5 markers (`verdictChecked`, `FIX5 (2026-11-19`) are present in the built worker bytes. `node --check`: identity script block (58,256 B) OK; walk main script (4,132,492 B) OK; built worker as ES module OK.

**Staged — all 7 routes curl-verified byte-identical by sha256 after the PUT** (curl piped to sha, never a file write — EPERM flake live):
`/` = welcome `d79793c0…`; `/agreement` = unfold `3252948e…`; `/welcome` = walk `b6befc33…`; `/identity.html` = identity `3279dc35…`; `/?stage=bridge`, `/?stage=deck`, `/?stage=letter` = welcome `d79793c0…`.
**Proof-host pages verified by full sha** (`work/verify-proof-fix6.py`, run standalone — walk included this round because the walk changed): welcome (`cb=c66e2fa2…`, ref fix6) = `d79793c0…`; identity (`cb=7920438e…`, ref fix6) = `3279dc35…`; walk (`cb=7b8fe1bf…`, ref fix6) = `b6befc33…`.

**Commits on the branch:**
- Commit 1 `d426f96b9ca2a6807409ea3436dc2e59850cc006` — fix6 (walk + identity + worker + builder + drivers). Parent `f79a03eb` (fix5 tip) confirmed.
- Commit 2 (this report + `evidence/fix6-api.json`) — filed after this report; see branch tip in the coordinator handoff.

**EPERM flake, live in this round:** both local worker writes failed (the V23 worker file still holds the fix-3 bytes `33cbda41…`; no `work/worker-fix6.js` copy landed — `write_resilient` 40-attempt writes refused; a `/tmp` write also landed 0 bytes). The worker bytes were built and filed from memory (deterministic sha `ca775178` across two builder runs, rebuilt identically inside the stage script), so the filed blob + staged PUT are the truth; the local copies are to be restored from the filed blob when the flake clears. Every write was verified by size + sha after the write; no `python3 … > file` redirects were used. One residue: `work/worker-fix6.js.tmp-stage-fix3` (0-byte tmp from the refused writes) sits in the work dir, unfiled.

## Live API probes — the server leg, proven (verbatim)

Staged worker, `jordantest` (cert Nº 000837, claimed 2026-11-18T20:18:43Z). Full record in `evidence/fix6-api.json`.
- GET `/api/claim?alias=jordantest` → `{"exists":true,"alias":"jordantest","name":"Jordan Test","cert_no":837,"created_at":"2026-11-18T20:18:43.276014+00:00","own":false}` (no key sent).
- POST `/api/welcome/complete` as `jordantest`, fresh key `nayanet_key_fix6probe_freshdevice` → `{"ok":false,"error":"taken"}`, **HTTP 409**.
- POST again, key missing entirely → `{"ok":false,"error":"taken"}`, **HTTP 409**.
- POST again, fresh key `nayanet_key_fix6probe_freshdevice2` → `{"ok":false,"error":"taken"}`, **HTTP 409**.
- GET `/api/welcome/complete?alias=jordantest` after the refusals: 2,227 B, sha `7f2465aa…` — two full reads agree byte-identical; the claim row is intact (`exists:true`, `own:false`, cert 837).
- **No registry rows created or deleted by this round.** Nº 000845 still unaccounted — carried, no owner invented.

**One honest limit on the no-write proof:** my first GET of the stored completion was piped through `head -c 300`, so its sha (`4e9a418f…`) is of a truncated prefix, not the full record — no full before-hash exists, so a byte-identical before/after comparison is NOT established. What is established: all three completion attempts returned 409, the two full after-reads agree, the size is unchanged (2,227 B), the claim row is intact, and the code returns 409 before the first write in the handler (the project PATCH/insert, Box, pages, and KV mirrors all sit below the gate). The probe script's section C does the before/after comparison correctly (full bytes both times) and rides with the browser probe.

## Design laws — zero new

`work/law-fix6.py` (check-design-laws.py's own rules; base = fix-5 filed blobs fetched via the blob API, walk base extracted from the fix-5 worker embed, checked in memory):
- Welcome: base **83 FAIL / 4 WARN → new 83 FAIL / 4 WARN**. Added: none. Removed: none.
- Identity: base **11 FAIL / 2 WARN → new 11 FAIL / 2 WARN**. Added: none. Removed: none.
- Walk: base **128 FAIL / 8 WARN → new 128 FAIL / 8 WARN**. Added: none. Removed: none.
- CLI confirms the same counts (welcome "83 violation(s), 4 warning(s)", identity "11 violation(s), 2 warning(s)", walk "128 violation(s), 8 warning(s)"). The 83/11/128 are the pre-existing round-1 baselines; the delta is zero new, as briefed.

## The live probe — NOT run (plainly)

The brief requires the fresh-device probes (walk URL arrival as a taken alias; identity URL arrival; fresh-device completion attempt) before the fix is presented as render-proven. **The browser halves did not run in this seat:**

- VM browsers are DEAD in this window, re-tested this round: Chromium (Playwright headless shell) fails at launch with `TargetClosedError: ... browser has been closed`; Firefox fails at launch (`Failed to launch the browser process`). No binaries on PATH. This is the known flap; nothing in this seat revives it, and as a subagent I have no live-browser task to route it through.
- `work/probe-fix6-live.py` is filed (commit 1) and ready: section A opens `/welcome?name=Jordan%20Test&alias=jordantest` on a fresh context and records the bounce + identity flag/panel; section B opens the proof-host identity with the pair in the URL and records the flag/panel on load; section C is the API refusal (already run by hand above — the script's version does the full before/after comparison correctly). **No test certificates were claimed in this round** — no new registry rows; the refusal probes create none by design (the gate returns before any write).
- What stands in place of the browser probe, and what it does and does not prove: the byte + trace + live-API proof above proves both gates are in the filed and staged bytes, use the same endpoint and verdict the typing check already proved live in fix-3, and that the server refuses a non-owner completion with 409 and no writes. That proves the mechanism and the server leg live. It does **not** prove the rendered bounce + taken flag + key panel on a fresh device — only the probe (or the captain's eye on the staged link) proves that. **The fix is therefore NOT presented as render-proven.** The next gate is the checker/captain's eye running `probe-fix6-live.py` (identity blob `7920438ed488869f29d520fd8dcd590061cb6586`, walk blob `7b8fe1bfbfe7d821c6e268890c682080421ff920` as the `cb` arguments) against the staged link.

## Untouched, as briefed

- The identity ENTER gate (fix-5, proven correct) — untouched; the fix-4 certified-status hide (identity lines 1338/1380) — untouched; agreed-state persistence; Copy feedback; deck/letter stages; the questionnaire; the walk beyond the load check (the completion POST needed no change — see Diagnosis item 2).
- Follow-ons #2, #3, #5 ride separately; #1 stays closed. No registry rows created or deleted; Nº 000845 still unaccounted.
- No images touched; no `cb=` or image URL changed (welcome/unfold byte-identical to fix-3).

## §11 design-laws check (in writing)

I read `THE-NAYA-DESIGN-LAWS.md` first, before touching code, then the Playbook, the Intelligence Report, the Orientation, the Anatomy, the team-nitro house rules, then the fix-5 checker verdict and maker report. The laws base is the same pre-existing round-1 baseline (welcome 83/4, identity 11/2, walk 128/8) — **zero new violations were introduced by this round, and none were removed**.

**Five gates:** (1) Right — a taken alias must never silently open as someone else, and a fresh device must never overwrite another citizen's stored world; the server refusal + the load bounce both serve exactly that; yes. (2) Truly needed — the fix-5 checker proved the hole open in the filed bytes, one URL away from the closed gate, to the same end state including overwriting the owner's world; yes. (3) Mine to do — maker seat, staged only; the three files the brief named (walk, identity, builder), worker rebuilt through the proven path, builder asserts moved with it; no money, credentials, destructive, privacy, or live action; no registry rows touched or deleted (three refusal POSTs that returned 409 before any write); yes. (4) Now — staged only, within the round, nothing sits: the branch, the staged worker, the live API probes, and this report land in the same round; yes. (5) Prove it — every claim above carries its own measurement (blob shas, wire shas, node runs, law counts, diff hunks, code traces, live API responses quoted verbatim); the live gaps and the one honest limit in the no-write proof are stated as gaps, never claimed; yes.

**Design check (per element, against its reference object):** the changed elements are two JS gates + one server guard, not new objects — they add no element, no text, no color, no motion to any page; the taken note + key panel the bounce lands on are the existing fix-3 elements, measured against the certificate itself and the Smart Note board (the reference board): nothing is added, so no new volume, light, shadow, or color is introduced; the certificate's composition, copy, and colors are untouched; no text is added at any size (the note text is the existing fix-3 wording, shown on a path where it already existed); no gray, no new color, no flow change; the fix-4 hide rule is untouched at lines 1338/1380. Hover/dead checks do not apply to gates that show existing elements; nothing was moved or removed that was not instructed — the one behavioural change in each file is the brief's fix, and the builder's removed lines are its own replaced asserts. Read-as-a-reader: I read the fix-3 live taken screenshot record (green note visible, key panel below, ENTER dim) — the taken state as the citizen sees it is the state the bounce now also reaches from the walk URL.

**Three-round scorecard (honest):** Round 1 (the diagnosis): the walk URL path, the completion POST's key, the bounce target's load behaviour, and the server lookup were each traced from the filed bytes before any edit — including the correction that the POST already carried the key, which saved an unneeded walk edit; score 9/10, the missing point is that only the eye's own device state would settle the render. Round 2 (the fix + filing): both legs in the smallest correct changes — a load verdict before the questionnaire, a URL-arrival check where the redirect lands, a server refusal before any write, no new server surface, no new lookup — branch, commit, blobs, worker, staging PUT, 7 routes + 3 proof-host pages all verified by sha, plus the server leg live-proven by API; score 9/10. Round 3 (the live browser proof): did not run — no browser in this seat; score 0/10, owed. Overall the round is 8/10: everything provable without a browser is proven, including the server leg live; the render proof is honestly outstanding. What would make it 10: the fresh-device walk-URL probe at 1920 clean (bounce lands, flag + panel show, questionnaire never renders) plus the identity URL-arrival probe — both ride to the checker/captain's eye, both are ready to run (`probe-fix6-live.py`).

**Seven questions (Self-Evaluation Checklist):**
1. Most intelligent? Yes — verify ownership at the walk's own front door and at the server's own write, instead of trusting the handoff URL or the ENTER gate to cover a path neither guards.
2. Most logical? Yes — it follows from the evidence in order: the walk is reached by URL as well as by ENTER, the URL path had no guard, the completion had no key check, therefore both need one, and the bounce must land where the flag actually shows.
3. Most sensible? Yes — a wise operator would call one verdict GET before the questionnaire and one row lookup before the write sensible; rebuilding the claim flow or the certificate would be clever in a way that breaks something else.
4. Full scope? Yes — the whole walk entry path was checked (ingest, ID, boot, resume, completion payload), the identity load path (passedAlias, silent restore, setAliasState, ENTER gate), the worker claim + completion handlers, the live API (GET claim + POST complete ×3 + GET read-back), the registry, the laws on all three files, and the untouched follow-ons.
5. Consequences? First order: a fresh device can no longer enter the walk as a taken alias (it bounces to identity with the flag + panel), and can no longer complete as one (409, no writes). Second order: every /welcome load with an alias costs one availability GET (~one round-trip, the same endpoint already called while typing); owner re-entry and fresh claims are unchanged; completions for unclaimed aliases are unchanged. Nobody else is touched: no other page, no live deploy, no registry rows.
6. Pros and cons? Pro: smallest fix on both legs, same endpoint/verdict/lookup already proved live, zero law delta, server leg live-proven by API in this seat. Con: no live render from this seat — the client legs are not presented as render-proven, and the round openly carries that gap to the next gate; and the no-write proof carries the truncated first-hash limit, named, not settled. The strongest case against: that a byte-only client leg should have waited for a live browser — answered: the bytes are filed and staged now, the server leg is proven live now, the probe runs the moment a browser lives, and nothing reaches Shawn before the eye.
7. Best possible choice? Yes — trace first (and correct the diagnosis where the bytes corrected it), file the smallest gates on both legs, stage it, prove everything provable without a browser including the server leg live, and hand the render probe to the next gate with the script ready, rather than sit on the fix waiting for a browser that flaps.

## What is left unfinished (honest list)

1. **Fresh-device browser probes (sections A + B).** Owed to the checker/captain's eye: run `work/probe-fix6-live.py` (identity blob `7920438ed488869f29d520fd8dcd590061cb6586`, walk blob `7b8fe1bfbfe7d821c6e268890c682080421ff920`) against the staged link when a browser lives. Until then the client legs are NOT presented as render-proven.
2. **Follow-on #1 live re-probe.** Still owed from fix-4/fix-5 (probe section D in fix-5); byte evidence says no wipe is possible; the live run settles it.
3. **Local worker copies.** The V23 worker file still holds fix-3 bytes (`33cbda41…`); restore from the filed fix-6 blob (`9d15c309…`, 8,345,689 B) when the EPERM flake clears.
4. **Carried observations (not redesigns):** a completion for a never-claimed alias still writes as today; a claim row with no `device_key` set is not refused by the completion gate (same rule as POST `/api/claim`'s 409). Both ride as follow-on design questions, not this round's scope.
5. **Follow-ons #2, #3, #5** ride separately, as briefed.

## Files

- Report: `~/workspace/team-nitro/walkthrough-chain-fix6-20261119/MAKER-REPORT.md` (this file; filed on the branch in commit 2)
- Work records: `~/workspace/team-nitro/walkthrough-chain-fix6-20261119/work/` (`build-fix6.py`, `law-fix6.py`, `probe-fix6-live.py`, `stage-fix6.py`, `verify-proof-fix6.py`)
- Evidence: `~/workspace/team-nitro/walkthrough-chain-fix6-20261119/evidence/fix6-api.json` (live API probes, verbatim; no browser probe ran, so no `fix6-live.json` + screenshots yet — they land here when the probe runs)
- Sources: `~/workspace/team-nitro/walk-v23-assembly-20261114/` (walk-beginning-fixed.html, identity-fixed.html, build-v23-staging-worker.py), `~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` (unchanged)
