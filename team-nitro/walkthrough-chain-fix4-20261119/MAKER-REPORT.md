# Walkthrough Chain Fix Round 4 — MAKER REPORT

**Maker seat, staged only. No PR, no merge, no live deploy, no message to Shawn.**
**Branch:** `walkthrough/chain-fix4-20261119` · **Parent:** fix3 tip `4bc016b31a175771cc5e107da385e6fd8a745abc` (confirmed by ref lookup before any work; fix2 tip `7181266f91c15315fa574f00eabcce6422e89b5a` confirmed as its parent line)
**Staged:** `https://naya-walk-beginning-staging.nayapower.workers.dev/`
**Round version: fix4** — one code fix (the desktop certified status) + one re-probe (follow-on #1, no code either way).

## Verdicts first — read this box before anything else

| Item | Verdict | Proof |
|---|---|---|
| THE FIX (desktop certified status) | **FILED + STAGED, NOT presented as fixed** | One rule in identity, worker rebuilt + staged, all 7 routes + both proof-host pages byte-identical by sha. The overlap walk that would prove it clean at 1920 + 534 **could not run — both VM browsers are dead** (see § "What was NOT live-proven"). Per the brief, the desktop certified certificate is **not** presented as fixed until that walk proves it clean at both widths. |
| #1 RE-PROBE (deck/letter arrival wipes the agreed keys) | **NOT REPRODUCED by the bytes; live re-probe still owed** | My own trace of the filed welcome blob (unchanged in this round): `removeItem('nayanet_fp_agreed')` occurs exactly once — inside `goBridgeToName()` (the gold pill); no `localStorage.clear()`; the render save branch removes only `nayanet_fp_stage`. No code path in the filed bytes can wipe the agreed key on a deck/letter arrival. The live re-probe (keys set fresh in the same context) could not run — browsers dead — so it rides to the checker/captain's eye. No code for #1 was built in this round either way. |

Nothing in this round is claimed from a live render I did not see. Every DONE above rests on bytes I read back myself (git blob API, curl piped to sha) or on a code trace from the filed blobs.

## The fix — one rule, nothing else

**Defect (fix3 checker §4 item 1):** on the certified desktop certificate (Nº 000842, in the fix-3 checker's evidence), the green "Available — it's yours to claim." status is struck across the member sentence. The fix3c hide rule is `max-width:640px` only, so desktop still shows the stale status.

**Change (identity-fixed.html only):** the same selector lifted out of the media query, placed immediately after the `@media (max-width: 640px)` block closes:

```css
.cert-plaque.is-certified .alias-status { display: none; }
```

with a FIX4 comment naming the checker evidence (fix3-live-E-copy-1920.png, Nº 000842). The diff against the fix3 filed identity is exactly that rule + its comment — 9 added lines, 0 removed, nothing else (verified by unified diff of the filed fix3 blob vs the new file).

**Why this is the whole fix, by cascade (checked on the filed bytes, not assumed):**
- The selector is identical to the fix3c rule, which the fix3c live probe proved hides the status at 534 — so the selector matches the live DOM (`#aliasStatus.alias-status` inside `#certPlaque.cert-plaque`, which gains `is-certified`); the only difference from fix3c is the media-query wrapper, so it now applies at all widths.
- No later rule overrides it: the only other `display` rule on `.cert-plaque.is-certified .alias-status` is the fix3c one at line 1338; every later `.cert-plaque.is-certified .alias-status` rule (lines 1641, 1671, 1724, 1756) sets only `margin-top`.
- The composing state is untouched (not `.is-certified`); the certified state at 534 is unchanged (same selector, same declaration as fix3c already applied there). One side effect, same as fix3c at 534: when certified via the `own` state, the "This Smart Name is yours — welcome back." line is hidden too — that is the fix3c treatment, carried to all widths as briefed.
- Welcome, unfold, walk, template untouched (byte-identical shas below).

## Staged version — the shas

| File | Bytes | sha256 | Blob (filed, commit 1) |
|---|---|---|---|
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 397,978 | `85b424470b2cea09a07345f98ed6d5baae412cd1ee9d34926a6ba167b6486b65` | `1fe8d8964d8fed39d9736ca1bb78a1e80c9f9f53` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,339,870 | `dd52d1c1f2782a6a104c953f3383c97d1559e440aaac210929344d9ee27d3997` | `d6e348586e5c78bafdc877477c80f4412fd5db36` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 91,580 | (builder assert moved `88c19001` → `85b42447`) | `09c66850f5f399423c8f04feaa5e5469573e1359` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,860,839 | `d79793c0d9b74121e83c0c65fed095e6d0dd278481b60c7a2b339bbe9231c934` (unchanged, fix3) | `c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f` |
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 105,308 | `3252948ed7f80157d0fa86fd730dc2e535a749f00e80944f0274ded54eb6a0f8` (unchanged, fix3) | `8980e57786c9bb196fb1ac5252f483995228e337` |

Worker embeds verified by sha after the build (builder run twice, identical sha `dd52d1c1`): WALK `4b5f9264` (4,359,566 B), IDENTITY `85b42447` (397,978 B), WELCOME `d79793c0`, UNFOLD `3252948e`, PERSONAL_TEMPLATE `61002d15`. The FIX4 rule text is present in the built worker bytes. `node --check`: identity script block (55,204 B) OK; built worker as ES module OK.

**Staged — all 7 routes curl-verified byte-identical by sha256 after the PUT** (fresh `t=` where applicable; curl piped to sha, never a file write — EPERM flake live):
`/` = welcome `d79793c0…`; `/agreement` = unfold `3252948e…`; `/welcome` = walk `4b5f9264…`; `/identity.html` = identity `85b42447…`; `/?stage=bridge`, `/?stage=deck`, `/?stage=letter` = welcome `d79793c0…`.
**Proof-host pages verified by full sha** (`work/verify-proof-fix4.py`, run standalone — see record note below): welcome (`cb=c66e2fa2…`, ref fix4) = `d79793c0…`; identity (`cb=1fe8d896…`, ref fix4) = `85b42447…`.

**Commits on the branch:**
- Commit 1 `75539a1770283235184a28baf74cd8fb4f302e93` — fix4 (identity `85b42447` + worker `dd52d1c1` + builder + drivers). Parent `4bc016b3` (fix3 tip) confirmed.
- Commit 2 (this report + `work/verify-proof-fix4.py`) — filed after this report; see branch tip in the coordinator handoff.

**Record note (my bug, named, no rebuild):** `work/stage-fix4.py` as filed in commit 1 crashes in its own proof-host loop with `KeyError: 'team-nitro/.../welcome-staged.html'` — it looked up `blobs[path]` for welcome, but welcome was not filed in this commit (unchanged from fix3). Everything before that line completed: branch, commit 1, blob read-backs, staging PUT, all 7 routes. The two proof-host pages were then verified by the standalone `work/verify-proof-fix4.py` (same checks, correct blob shas), and both match. The filed stage script stands as the true record of what ran, bug included; the fix is the separate verify script, not a silent edit.

**EPERM flake, live in this round:** both local worker writes failed (the V23 worker file still holds the fix3 bytes `33cbda41…`; no `work/worker-fix4.js` copy landed — 40-attempt `write_resilient` + shell writes both refused). The worker bytes were built and filed from memory (deterministic sha `dd52d1c1` across three separate builder runs), so the filed blob + staged PUT are the truth; the local copies are to be restored from the filed blob when the flake clears. A python write to `/tmp` also EPERM'd during the round. Every write was verified by size + sha after the write; no `python3 … > file` redirects were used.

## Design laws — zero new

`work/law-fix4.py` (check-design-laws.py's own rules, base = fix3 filed blobs fetched via the blob API, checked in memory):
- Welcome: base **83 FAIL / 4 WARN → new 83 FAIL / 4 WARN**. Added: none. Removed: none.
- Identity: base **11 FAIL / 2 WARN → new 11 FAIL / 2 WARN**. Added: none. Removed: none.
- CLI confirms the same counts (welcome "83 violation(s), 4 warning(s)", identity "11 violation(s), 2 warning(s)"). The 83/11 are the pre-existing round-1 baseline; the delta is zero new, as briefed.

## The overlap walk — NOT live-proven (plainly)

The brief requires the certified certificate proven clean at 1920 + 534 (overlap walk, screenshots + measurements JSON, read as a reader) before the desktop certificate is presented as fixed. **That walk did not run in this seat:**

- VM browsers are DEAD in this window: Firefox SIGSEGV on launch (`exitCode=null, signal=SIGSEGV`, re-tested 5× across the round, including a persistent-context launch with its profile under `~/workspace` to rule out `/tmp`); Chromium closed at launch (`TargetClosedError`), including the full `chromium-1248/chrome-linux64/chrome` binary, not only the headless shell. Memory (3.1 GB available) and disk (83 GB free) are fine; no zombie browser processes. This is the known flap (checker found the same state ~04:11Z); nothing in this seat revives it, and as a subagent I have no live-browser task to route it through.
- `work/probe-fix4-live.py` is filed (commit 1) and ready: section A claims `fix4cert` at 1920 and runs the overlap walk + screenshot; section B claims `fix4cert534` at 534; section C is the #1 re-probe (probe-B). **No test certificates were claimed in this round** — no new registry rows from me; Nº 000845 remains unaccounted as before.
- What stands in place of the walk, and what it does and does not prove: the byte + cascade proof in "The fix" above proves the rule is in the filed and staged bytes, uses the identical selector the fix3c live probe proved hides the status at 534, and cannot be overridden by any later rule in the file. That proves the mechanism. It does **not** prove the rendered desktop certificate is clean — only the overlap walk (or the captain's eye on the staged link) proves that. **The desktop certified certificate is therefore NOT presented as fixed.** The next gate is the checker/captain's eye running `probe-fix4-live.py` (or the same walk by hand) against the staged link.

## Follow-on #1 re-probe — byte trace (mine), live re-probe owed

The fix-3 maker claimed a deck/letter arrival wipes `nayanet_fp_stage` / `nayanet_fp_agreed` (the `render()` save branch). The fix-3 checker traced the filed welcome blob and contradicted it. I re-traced it myself from the filed welcome blob (`c66e2fa2…`, unchanged in this round, 1,860,839 B, `d79793c0…`):

- `removeItem('nayanet_fp_agreed')` occurs **exactly once** in the whole file — inside `goBridgeToName()` (the gold pill): `try{localStorage.removeItem('nayanet_fp_stage');localStorage.removeItem('nayanet_fp_agreed');}catch(e){}`.
- No `localStorage.clear()` anywhere (0 occurrences).
- The render save branch removes **only** the stage key: `else if(S.view==='bridge'&&window.__fpAgreed)localStorage.setItem('nayanet_fp_stage','bridge-agreed'); else localStorage.removeItem('nayanet_fp_stage');` — the other two `removeItem('nayanet_fp_stage')` occurrences are `exitStage()` and `goBridgeToName()`, neither of which touches the agreed key.
- The boot restore (`!_fpStage && (_fpRestoreStage==='bridge-agreed' || _fpAgreedKey)`) and the `enterStage` guard both restore the post-agree bridge from the surviving agreed key — so losing only the stage key on a deck/letter arrival is harmless by the bytes.

**Conclusion on the bytes:** a deck/letter arrival cannot wipe the agreed key through any code path in the filed bytes, and the maker's fix3-live.json `B_deck_with_agreed_key` reading (lsAgreed null after deck) is unexplained by the bytes — most plausibly a probe artifact (keys never landed in that context), as the checker said. On current evidence #1 is not a follow-on at all, and no code was built for it in this round.

**What is still owed:** the live re-probe itself — keys set fresh in the same context, then `/?stage=deck` and `/?stage=letter` arrivals, reading `lsStage`/`lsAgreed` (`probe-fix4-live.py` section C, the checker's probe-B). It could not run here — browsers dead (above). Only that live run settles probe-artifact vs page behavior for good. If it reproduces a wipe, the fix for the next round is: the render save branch must not remove the stage key on a deck/letter arrival while the agreed key is set (guard the `else removeItem('nayanet_fp_stage')` with `!__fpAgreed`, mirroring the boot guard) — named here as the exact fix *if* it reproduces; it is not built now.

## Untouched, as briefed

- Follow-ons #2 (proof-host `/welcome` HTTP 400 usage text), #3 (audio ear-check on a real device), #5 (registry cleanup — no rows deleted by me; cert Nº 000845 still unaccounted, registry owner to identify before any cleanup) ride separately; nothing was done on them here.
- Commit 3's mislabel in fix3 ("FIX3b … commit 2" — it is the fix3c commit) is a record note only, no rebuild.
- No images touched; no `cb=` or image URL changed (welcome/unfold byte-identical to fix3).

## §11 design-laws check (in writing)

I read `THE-NAYA-DESIGN-LAWS.md` first, before touching code, then the Playbook, the Intelligence Report, the Orientation, the Anatomy, the Army Training, and the team-nitro house rules, then the fix-3 checker verdict and maker report. The laws base is the same pre-existing round-1 baseline (welcome 83/4, identity 11/2) — **zero new violations were introduced by this round, and none were removed**.

**Five gates:** (1) Right — hiding a stale status that prints wrong words across a member sentence serves the citizen reading their own certificate; yes. (2) Truly needed — the fix3 checker proved the collision from the maker's own screenshot; the captain needs this one rule before the eye walks the desktop cert; yes. (3) Mine to do — maker seat, staged only; one CSS rule in the file the brief named, worker rebuilt through the proven path; no money, credentials, destructive, privacy, or live action; no registry rows touched or deleted; yes. (4) Now — staged only, within the hour, nothing sits: the branch, the staged worker, and this report land in the same round; yes. (5) Prove it — every claim above carries its own measurement (blob shas, wire shas, node runs, law counts, diff, code traces); the live gaps are stated as gaps, never claimed; yes.

**Design check (per element, against its reference object):** the changed element is one CSS rule, not a new object — it removes a line from the certified certificate; it is measured against the Smart Note board (the reference board): nothing is added, so no new volume, light, shadow, or color is introduced; the certificate's own composition, copy, and colors are untouched; no text is added at any size (the rule deletes text from view); no gray, no new color, no flow change; the `display:none` is the same treatment the fix3c live probe proved at 534. Reference objects: the certificate itself is unchanged as an object — only the stale line leaves it. Hover/dead checks do not apply to a hidden line; nothing was moved or removed that was not instructed (the one removal is the brief's fix). Read-as-a-reader: I read the fix3c-live-A-cert-534 screenshot and the fix3-live-E-copy-1920 screenshot in the checker verdict — the 534 cert reads clean with the status hidden; the desktop cert is the one that still shows it, which is why the walk is owed, not claimed.

**Three-round scorecard (honest):** Round 1 (the rule): the fix is the smallest correct change — one selector, already live-proven at 534 — and it cannot break anything else by cascade; score 9/10, the missing point is that only a live render proves it, and this seat could not produce one. Round 2 (the filing): branch, commit, blobs, worker, staging PUT, 7 routes + 2 proof-host pages all verified by sha; the stage script's proof-loop KeyError is the blemish — caught, worked around with a standalone verify, and recorded, not hidden; score 9/10. Round 3 (the re-probe): the byte trace is complete and independently re-proved, but the live re-probe did not run; score 7/10 — the evidence is strong but the live leg is owed. Overall the round is 8/10: everything that could be proven from bytes is proven; the live proof is honestly outstanding. What would make it 10: the overlap walk at 1920 + 534 clean (screenshots + JSON, read as a reader) and the probe-B re-probe executed — both ride to the checker/captain's eye, both are ready to run (`probe-fix4-live.py`).

**Seven questions (Self-Evaluation Checklist):**
1. Most intelligent? Yes — one rule, harvested from the proven fix3c treatment, instead of a restamp or a new mechanism.
2. Most logical? Yes — it follows from the checker's evidence in order: the collision is at desktop, the hide rule is 640px-only, therefore lift the same rule out of the media query.
3. Most sensible? Yes — a wise operator would call a one-rule lift sensible; rebuilding the certificate or hiding the status by JS would be clever in a way that breaks something else.
4. Full scope? Yes — the whole page was checked for later overrides (cascade grep), the composing state, the 534 state, the worker embeds, the laws delta, the registry, and the untouched follow-ons.
5. Consequences? First order: the stale line leaves every certified certificate. Second order: the `own`-state welcome-back line leaves too (same as fix3c at 534 — intended, same treatment). Nobody else is touched: no other page, no live deploy, no registry rows.
6. Pros and cons? Pro: smallest fix, proven selector, zero law delta. Con: no live render from this seat — the desktop cert is not presented as fixed, and the round openly carries that gap to the next gate. The strongest case against: that a byte-only round should have waited for a live browser — answered: the bytes are filed and staged now, the walk runs the moment a browser lives, and nothing reaches Shawn before the eye.
7. Best possible choice? Yes — file the one rule, stage it, prove everything provable from bytes, and hand the live walk to the next gate with the probe script ready, rather than sit on the fix waiting for a browser that flaps.

## What is left unfinished (honest list)

1. **Overlap walk at 1920 + 534 (the goes-back proof).** Owed to the checker/captain's eye: run `work/probe-fix4-live.py` (identity blob `1fe8d8964d8fed39d9736ca1bb78a1e80c9f9f53` as the `cb` argument) against the staged link when a browser lives. Until then the desktop certified certificate is NOT presented as fixed.
2. **Follow-on #1 live re-probe.** Same probe, section C. Byte evidence says no wipe is possible; the live run settles it.
3. **Local worker copies.** The V23 worker file still holds fix3 bytes (`33cbda41…`); restore from the filed fix4 blob (`d6e34858…`, 8,339,870 B) when the EPERM flake clears.
4. **Follow-ons #2, #3, #5** ride separately, as briefed.

## Files

- Report: `~/workspace/team-nitro/walkthrough-chain-fix4-20261119/MAKER-REPORT.md` (this file; filed on the branch in commit 2)
- Work records: `~/workspace/team-nitro/walkthrough-chain-fix4-20261119/work/` (`build-fix4.py`, `law-fix4.py`, `probe-fix4-live.py`, `stage-fix4.py`, `verify-proof-fix4.py`)
- Evidence: `~/workspace/team-nitro/walkthrough-chain-fix4-20261119/evidence/` (empty — no live probe ran; `fix4-live.json` + screenshots land here when the probe runs)
- Sources: `~/workspace/team-nitro/walk-v23-assembly-20261114/` (identity-fixed.html, build-v23-staging-worker.py), `~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` (unchanged)
