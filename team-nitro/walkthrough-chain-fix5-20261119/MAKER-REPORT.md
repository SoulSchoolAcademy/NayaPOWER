# Walkthrough Chain Fix Round 5 — MAKER REPORT

**Maker seat, staged only. No PR, no merge, no live deploy, no message to Shawn.**
**Branch:** `walkthrough/chain-fix5-20261119` · **Parent:** fix4 tip `0c436d580256b2be0d2b05131d5c0e7234b24c86` (confirmed by ref lookup before any work)
**Staged:** `https://naya-walk-beginning-staging.nayapower.workers.dev/`
**Round version: fix5** — one code fix (ENTER resolves the availability verdict first) on the fix-4 filing.

## Verdicts first — read this box before anything else

| Item | Verdict | Proof |
|---|---|---|
| THE FIX (taken alias flagged + key prompt on ENTER) | **FILED + STAGED, NOT presented as render-proven** | One gate in identity, worker rebuilt + staged, all 7 routes + both proof-host pages byte-identical by sha. The live taken-ENTER probe that would prove it on a render **could not run — both VM browsers are dead** (see § "What was NOT live-proven"). Per the brief, the fix is **not** presented as render-proven until that probe runs. |
| THE DIAGNOSIS (why the eye's path skipped the taken flag) | **PROVEN from the filed bytes + live API probes — with one honest limit** | The typing path, the server, and the ENTER-taken path are each proven correct for a fresh device; the only fresh-device hole is the race the gate closes. The eye's `/welcome` is reproducible on the filed bytes ONLY as owner re-entry (the device already holding the row's key) — see § "Diagnosis" for the full chain and the limit. |

Nothing in this round is claimed from a live render I did not see. Every DONE above rests on bytes I read back myself (git blob API, curl piped to sha) or on a code trace from the filed blobs, or on live read-only API probes I ran and quote verbatim.

## Diagnosis — why the eye's path skipped the taken flag

**The defect as briefed:** the captain's cloud eye (desktop 1920×999, 04:53–05:02Z, test alias walkeye9187, "fresh device") claimed taken alias `jordantest`: no "already claimed" message, no device-key prompt — ENTER went straight to `/welcome` exactly as a fresh claim does, and Back showed the pre-existing CERTIFIED certificate for "Jordan Test" (Nº 000837, Nov 18 20:18).

**What I traced, in order, from the fix-4 filed identity blob (`1fe8d896…`, 397,978 B, sha `85b42447…`) and the fix-3 worker bytes:**

1. **The taken path EXISTS and is live-proven on the typing side.** `checkAliasAvailability` (identity ~char 364685): GET `/api/claim?alias=…` (+ `device_key` if the browser has one); `d.exists && !d.own` → `setAliasState('taken')` (non-silent), which sets status text `already claimed` AND (fix3) unhides `#hubNote` (taken text) + `#keyPanel`. The fix-3 live probe `E_taken_jordantest` (proof host, 1920×999) proves it on a render: typing `jordantest` → status "already claimed", state `taken`, note visible, `keyPanelVisible=true`, ENTER dim. The fix-2 eye's "already claimed text but no prompt" is fully explained by the fix-2 bytes: in fix-2 the taken state set the status text only — the note+panel unhide on the taken state was added in fix3 (`fix3-repro-identity.json`: fix-2 `taken_jordantest` has `noteHidden:true`, `keyPanelHidden:true`).
2. **The server is correct for a fresh key (live probes, this round).** Staging GET `/api/claim?alias=jordantest` → `{"exists":true,"alias":"jordantest","name":"Jordan Test","cert_no":837,"created_at":"2026-11-18T20:18:43.276014+00:00","own":false}` — with and without a bogus device key. POST `/api/claim` with a fresh random device key → `{"ok":false,"error":"taken"}` (409 path in the worker: the row exists and its key differs). So the server does NOT grant a fresh device the alias, and the row's `device_key` is non-empty. The "server steals the alias" hypothesis is dead for `jordantest`.
3. **The ENTER-taken path fires on every non-own outcome.** In `activateAndRedirect`, a 409 `taken` POST does a read-back GET with this browser's key; `own:false` → `showTaken()` (note + panel + scroll), and even a fetch failure falls through to `.catch(showTaken)`. The only route from ENTER to `/welcome` with a taken alias is `ok:true` from the POST — which the worker returns only when the row's key matches this browser's key (201 insert, or 409 re-claim by the same device) — or the no-alias owner branch (not applicable: an alias was typed).
4. **The fresh-device hole is the RACE — and it is real.** The typing check is debounced 300 ms (`scheduleAliasCheck(false)` on every input event) and **ENTER never consulted `aliasState` at all**: `activateAndRedirect` went straight to minting a key, writing localStorage, and POSTing. So at the moment of a fast ENTER, the taken flag and the key prompt depend on a check that may still be pending or may never have run — exactly the question the brief told me to answer ("what happens when the lookup fails or is still pending when ENTER is pressed?"). Answer: ENTER claimed blind; the POST was the only guard, and it resolves only after its round-trip.
5. **The honest limit.** On the filed bytes there is NO path by which a genuinely fresh device silently re-enters `jordantest`: the GET says `own:false`, the POST says `taken`, the ENTER-taken path shows the flag. The eye's `/welcome` + Back-to-cert-000837 is reproducible ONLY if the eye's browser already held `jordantest`'s device key — i.e. the eye was the owner device, not fresh (owner re-entry is the designed behaviour: only the owning device re-enters silently). The row was claimed Nov 18 20:18:43Z, before this round; which seat claimed it is not in the fix-2/fix-3 records I searched, and I cannot see the eye's localStorage from here — so I cannot prove the eye's device was or was not fresh. **What the fix does about that:** it makes ENTER deterministic on every path regardless of device history — the verdict is resolved before any claim is attempted, so the flag + prompt fire on ENTER itself, with zero reliance on debounce timing or on what the typing check did. What it does NOT do: it does not change owner re-entry (correct by design), and it does not retroactively prove the eye was fresh.

## The fix — one gate in identity, nothing else

**Change (identity-fixed.html only, +2,275 B):** `activateAndRedirect` now takes an optional `verdictChecked` flag, and before any key mint, localStorage write, or claim POST it resolves the availability verdict first:

```js
window.activateAndRedirect = function(verdictChecked) {
  /* ... finalAlias / finalName computed as before ... */
  /* FIX5 — ENTER resolves the availability verdict FIRST ... */
  if (!verdictChecked) {
    var gateKey = null; try { gateKey = localStorage.getItem('nayanet_vault_key'); } catch(e){}
    var gateDone = false;
    var gateTimer = null;
    var gateGo = function(){ /* once */ window.activateAndRedirect(true); };
    gateTimer = setTimeout(gateGo, 4000);
    fetch(__chainApiBase + '/api/claim?alias=' + encodeURIComponent(finalAlias)
      + (gateKey ? '&device_key=' + encodeURIComponent(gateKey) : ''), { cache: 'no-store' })
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(d){
        if (gateDone) return;
        if (d && d.exists && !d.own) {
          /* taken: flag + key panel, return — no write, no POST */
          setAliasState('taken', finalAlias);
          /* ... note text + taken-note class + unhide + scroll, keyPanel unhide ... */
          return;
        }
        gateGo();
      })
      .catch(function(){ gateGo(); });
    return;
  }
  /* ... the existing claim flow, unchanged ... */
}
```

**Why this is the whole fix, by trace (checked on the filed bytes, not assumed):**
- The verdict GET is the same endpoint the typing check uses, read with this browser's key if it has one — so its `taken` verdict means exactly what the typing check's `taken` means, with no new server surface and no worker change (the claim handler is untouched).
- Taken on ENTER now shows the flag + the key panel and returns BEFORE the key mint, the `nayanet_smart_alias` / `nayanet_smart_name` writes, and the claim POST — so there is no stored profile to restore afterwards (the old ENTER-taken path's restore step is never needed on this path) and no claim attempt that could attribute a join.
- Own or available falls through to the existing claim below — the POST stays the authority, the own re-claim path is unchanged, and a fresh claim still stamps + redirects exactly as before.
- A failed or timed-out verdict (4 s) falls through too, so ENTER can never hang on this read; the POST's own error path still shows on failure.
- The load-time silent restore is untouched (v2.6/v2.7): a saved alias claimed under a different key still paints nothing beneath an empty input — the gate only runs on ENTER with a typed alias.
- The fix-4 certified-status hide (identity line 1380), the agreed-state persistence, Copy feedback, deck/letter keys, the walk, and the questionnaire are untouched. Follow-on #1 is closed (see fix-4 verdict) — no code for it in this round. The `/deck` and `/letter` PATHS redirect off-site; the arrivals are query stages on the staging root — routing, not a defect, untouched.

**Diff vs the fix-4 filed identity (my own unified diff of the filed blobs): exactly two hunks** — the signature `function()` → `function(verdictChecked)` and the gate insert after the no-alias branch. +2,275 B, 0 removed, nothing else. Welcome, unfold, walk, template byte-identical to fix4 (see embeds + staging below).

## Staged version — the shas

| File | Bytes | sha256 | Blob (filed, commit 1) |
|---|---|---|---|
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 400,253 | `6f805eba00fa7ccbf89103c46878c352e73db5b26792010dc2de535c706418f0` | `9e0ed79da9057d878aed198bfa8e971b07e50e92` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,342,190 | `a58a48ba3ac486af0e8937b5132d21d11072ddaedab435ab718978caa4ec7f4e` | `ea0b7a92fa78dff3dbe53de0b41bb1d916562735` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 91,672 | (builder assert moved `85b42447` → `6f805eba`) | `bb98b490a29a1c7f3d7587ff445a8df241a6ac11` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,860,839 | `d79793c0d9b74121e83c0c65fed095e6d0dd278481b60c7a2b339bbe9231c934` (unchanged, fix3) | `c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f` |
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 105,308 | `3252948ed7f80157d0fa86fd730dc2e535a749f00e80944f0274ded54eb6a0f8` (unchanged, fix3) | `8980e57786c9bb196fb1ac5252f483995228e337` |

Worker embeds verified by sha after the build (builder run twice, identical sha `a58a48ba`): WALK `4b5f9264` (4,359,566 B), IDENTITY `6f805eba` (400,253 B), WELCOME `d79793c0`, UNFOLD `3252948e`, PERSONAL_TEMPLATE `61002d15`. The FIX5 gate text (`verdictChecked`, `FIX5 (2026-11-19`) is present in the built worker bytes. `node --check`: identity script block (57,677 B) OK; built worker as ES module OK.

**Staged — all 7 routes curl-verified byte-identical by sha256 after the PUT** (fresh `t=` where applicable; curl piped to sha, never a file write — EPERM flake live):
`/` = welcome `d79793c0…`; `/agreement` = unfold `3252948e…`; `/welcome` = walk `4b5f9264…`; `/identity.html` = identity `6f805eba…`; `/?stage=bridge`, `/?stage=deck`, `/?stage=letter` = welcome `d79793c0…`.
**Proof-host pages verified by full sha** (`work/verify-proof-fix5.py`, run standalone — the fix-4 KeyError trap avoided: welcome is not looked up in this commit's blobs; its fix-3 blob sha is used explicitly): welcome (`cb=c66e2fa2…`, ref fix5) = `d79793c0…`; identity (`cb=9e0ed79d…`, ref fix5) = `6f805eba…`.

**Commits on the branch:**
- Commit 1 `b1084f5686e04a588fb85531c5e496b2c28e68a4` — fix5 (identity `6f805eba` + worker `a58a48ba` + builder + drivers). Parent `0c436d58` (fix4 tip) confirmed.
- Commit 2 (this report) — filed after this report; see branch tip in the coordinator handoff.

**EPERM flake, live in this round:** both local worker writes failed (the V23 worker file still holds the fix3 bytes `33cbda41…`; no `work/worker-fix5.js` copy landed — `write_resilient` 40-attempt + shell writes both refused, and a `/tmp` write EPERM'd during the round). The worker bytes were built and filed from memory (deterministic sha `a58a48ba` across two builder runs), so the filed blob + staged PUT are the truth; the local copies are to be restored from the filed blob when the flake clears. Every write was verified by size + sha after the write; no `python3 … > file` redirects were used.

## Design laws — zero new

`work/law-fix5.py` (check-design-laws.py's own rules, base = fix4 filed blobs fetched via the blob API, checked in memory):
- Welcome: base **83 FAIL / 4 WARN → new 83 FAIL / 4 WARN**. Added: none. Removed: none.
- Identity: base **11 FAIL / 2 WARN → new 11 FAIL / 2 WARN**. Added: none. Removed: none.
- CLI confirms the same counts (welcome "83 violation(s), 4 warning(s)", identity "11 violation(s), 2 warning(s)"). The 83/11 are the pre-existing round-1 baseline; the delta is zero new, as briefed.

## The live probe — NOT run (plainly)

The brief requires the taken-alias ENTER probe on a fresh profile (type `jordantest`, ENTER, observe) before the fix is presented as render-proven. **That probe did not run in this seat:**

- VM browsers are DEAD in this window: Chromium exits with SIGTRAP on launch (re-tested twice this round, headless shell via Playwright); Firefox is not on PATH in this VM (`firefox: No such file or directory`). This is the known flap; nothing in this seat revives it, and as a subagent I have no live-browser task to route it through.
- `work/probe-fix5-live.py` is filed (commit 1) and ready: section A types `jordantest` and clicks ENTER immediately (the race — no wait); section B types, waits 2.5 s for the typing check, then ENTER; section C is the available-alias control (claims `fix5avail` — one new registry row, joins the cleanup list); section D is the #1 re-probe (keys set fresh in the same context). **No test certificates were claimed in this round** — no new registry rows from me; the taken probes create none by design (the gate returns before the claim POST). Nº 000845 remains unaccounted as before; `jordantest` Nº 000837 / `walkertest` Nº 000836 are pre-existing test aliases, untouched by me except the read-only GETs and one POST probe that returned 409 `taken` (no row written).
- What stands in place of the probe, and what it does and does not prove: the byte + trace + live-API proof in "Diagnosis" above proves the gate is in the filed and staged bytes, uses the same endpoint and verdict the typing check already proved live in fix3, writes nothing and POSTs nothing on the taken path, and cannot be bypassed by debounce timing. That proves the mechanism. It does **not** prove the rendered taken flag + key panel on ENTER — only the probe (or the captain's eye on the staged link) proves that. **The fix is therefore NOT presented as render-proven.** The next gate is the checker/captain's eye running `probe-fix5-live.py` (identity blob `9e0ed79da9057d878aed198bfa8e971b07e50e92` as the `cb` argument) against the staged link.

## Untouched, as briefed

- The fix-4 certified-status hide (identity line 1380), agreed-state persistence, Copy feedback ("Copied ◆"), deck/letter keys, the walk, the questionnaire — untouched.
- Follow-on #1 is CLOSED — no code for it in this round.
- Follow-ons #2 (proof-host `/welcome` HTTP 400 usage text), #3 (audio ear-check on a real device), #5 (registry cleanup — no rows deleted by me; cert Nº 000845 still unaccounted, registry owner to identify before any cleanup) ride separately; nothing was done on them here.
- No images touched; no `cb=` or image URL changed (welcome/unfold byte-identical to fix3).

## §11 design-laws check (in writing)

I read `THE-NAYA-DESIGN-LAWS.md` first, before touching code, then the Playbook, the Intelligence Report, the Orientation, the Anatomy, the team-nitro house rules, then the fix-4 checker verdict and maker report. The laws base is the same pre-existing round-1 baseline (welcome 83/4, identity 11/2) — **zero new violations were introduced by this round, and none were removed**.

**Five gates:** (1) Right — a taken alias must never silently open as someone else, and the flag + key prompt must fire on every taken path; yes. (2) Truly needed — the captain's eye saw the silent re-entry on the fix-4 filing, and the race that lets ENTER claim blind is proven in the filed bytes; yes. (3) Mine to do — maker seat, staged only; one gate in the file the brief named, worker rebuilt through the proven path, builder assert moved with it; no money, credentials, destructive, privacy, or live action; no registry rows touched or deleted (one read-only POST probe that returned 409 taken); yes. (4) Now — staged only, within the round, nothing sits: the branch, the staged worker, and this report land in the same round; yes. (5) Prove it — every claim above carries its own measurement (blob shas, wire shas, node runs, law counts, diff hunks, code traces, live API responses quoted verbatim); the live gaps and the one honest limit in the diagnosis are stated as gaps, never claimed; yes.

**Design check (per element, against its reference object):** the changed element is one JS gate, not a new object — it adds no element, no text, no color, no motion to the page; the taken note + key panel it shows are the existing fix-3 elements, measured against the certificate itself and the Smart Note board (the reference board): nothing is added, so no new volume, light, shadow, or color is introduced; the certificate's composition, copy, and colors are untouched; no text is added at any size (the note text is the existing fix-3 wording, shown on a path where it already existed); no gray, no new color, no flow change. Hover/dead checks do not apply to a gate that shows existing elements; nothing was moved or removed that was not instructed — the one behavioural change is the brief's fix. Read-as-a-reader: I read the fix-3 live taken screenshot record (`fix3-live-E-taken-1920.png` via the fix-3 checker verdict: green note visible, key panel below, ENTER dim) — the taken state as the citizen sees it is the state this gate now also reaches from ENTER.

**Three-round scorecard (honest):** Round 1 (the diagnosis): the server, the typing path, and the ENTER-taken path were each traced and live-probed, the fix-2 discrepancy explained from its own bytes, and the one limit (eye freshness unprovable from here) named instead of papered over; score 9/10, the missing point is that only the eye's own device state would settle fresh-vs-owner for good. Round 2 (the fix + filing): the gate is the smallest correct change — one verdict GET before the claim, no new server surface, no worker change — branch, commit, blobs, worker, staging PUT, 7 routes + 2 proof-host pages all verified by sha; the stage script's proof loop was fixed before running (the fix-4 KeyError named and avoided, not repeated); score 9/10. Round 3 (the live proof): did not run — no browser in this seat; score 0/10, owed. Overall the round is 8/10: everything provable from bytes is proven; the live proof is honestly outstanding. What would make it 10: the taken-ENTER probe at 1920 clean on both the fast and slow variants (screenshots + JSON, read as a reader) plus the #1 re-probe — both ride to the checker/captain's eye, both are ready to run (`probe-fix5-live.py`).

**Seven questions (Self-Evaluation Checklist):**
1. Most intelligent? Yes — resolve the verdict before the claim instead of racing the debounce, and let the existing taken UI do the showing.
2. Most logical? Yes — it follows from the evidence in order: the flag depends on a check ENTER never consulted, therefore ENTER must consult the verdict first.
3. Most sensible? Yes — a wise operator would call one verdict GET before a claim sensible; rebuilding the claim endpoint or the certificate would be clever in a way that breaks something else.
4. Full scope? Yes — the whole ENTER path was checked (typing check, debounce, gate, POST, read-back, verify-key, no-alias branch, silent restore), the worker claim handler, the live API (GET + POST), the fix-2 discrepancy, the registry, and the untouched follow-ons.
5. Consequences? First order: a taken alias can no longer reach the claim POST from ENTER, so the flag + key panel fire on every taken ENTER. Second order: every ENTER costs one extra availability GET (~one round-trip, the same endpoint already called while typing); owner re-entry and fresh claims are unchanged. Nobody else is touched: no other page, no live deploy, no registry rows.
6. Pros and cons? Pro: smallest fix, same endpoint and verdict the typing check already proved live, zero law delta, no server change. Con: no live render from this seat — the fix is not presented as render-proven, and the round openly carries that gap to the next gate; and the diagnosis limit (eye freshness) is named, not settled. The strongest case against: that a byte-only round should have waited for a live browser — answered: the bytes are filed and staged now, the probe runs the moment a browser lives, and nothing reaches Shawn before the eye.
7. Best possible choice? Yes — diagnose first (and say plainly where the diagnosis stops), file the one gate, stage it, prove everything provable from bytes, and hand the live probe to the next gate with the script ready, rather than sit on the fix waiting for a browser that flaps.

## What is left unfinished (honest list)

1. **Taken-ENTER live probe at 1920 (fast + slow variants).** Owed to the checker/captain's eye: run `work/probe-fix5-live.py` (identity blob `9e0ed79da9057d878aed198bfa8e971b07e50e92` as the `cb` argument) against the staged link when a browser lives. Until then the fix is NOT presented as render-proven.
2. **Follow-on #1 live re-probe.** Same probe, section D. Byte evidence says no wipe is possible; the live run settles it.
3. **Local worker copies.** The V23 worker file still holds fix3 bytes (`33cbda41…`); restore from the filed fix5 blob (`ea0b7a92…`, 8,342,190 B) when the EPERM flake clears.
4. **The eye-freshness question.** If the captain's eye re-walks the taken path on the staged link and still sees silent re-entry, the eye's device state (stored `nayanet_vault_key` / `nayanet_smart_alias`) must be inspected first — on the filed bytes, only an owner key reaches `/welcome` with a taken alias.
5. **Follow-ons #2, #3, #5** ride separately, as briefed.

## Files

- Report: `~/workspace/team-nitro/walkthrough-chain-fix5-20261119/MAKER-REPORT.md` (this file; filed on the branch in commit 2)
- Work records: `~/workspace/team-nitro/walkthrough-chain-fix5-20261119/work/` (`build-fix5.py`, `law-fix5.py`, `probe-fix5-live.py`, `stage-fix5.py`, `verify-proof-fix5.py`)
- Evidence: `~/workspace/team-nitro/walkthrough-chain-fix5-20261119/evidence/` (empty — no live probe ran; `fix5-live.json` + screenshots land here when the probe runs)
- Sources: `~/workspace/team-nitro/walk-v23-assembly-20261114/` (identity-fixed.html, build-v23-staging-worker.py), `~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` (unchanged)
