# CHECKER REPORT — Agreement Distill Fix-3

**Round:** `walkthrough/agreement-distill-fix3-20261119` (checker)
**Date:** 2026-11-19, ~23:47–00:45 MST (over the one-hour max; the overrun was
three full harness runs — the maker's script twice, my own checker twice —
plus the stale-sha diagnosis, the causal fetch test, and the real laws-checker
pipe runs — see §8)
**Base:** branch `walkthrough/agreement-distill-fix-20261119`, tip `e0681545`
(repo `SoulSchoolAcademy/NayaPOWER`)
**New branch:** `walkthrough/agreement-distill-fix3-20261119` — **NOT FILED**
(EPERM, see §7; verified 404 by the checker, §7)
**Staged worker (base, unchanged):** https://naya-walk-beginning-staging.nayapower.workers.dev/
**Work files:** `~/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/checker/work/`
— `check-fix3.js` (checker's own transform + byte harness + laws + full state
machine, 721 lines), `dom-check3.js` (checker copy of the fix-1 DOM — diff vs
the fix-2 checker's copy shows ONLY the pending-fetch patch, §8),
`diff-maker.js` (evaluates the maker's own transform constants verbatim),
`mech-probe.js` (insertion sizes + claim-verdict handler + availability
function, base bytes), `variant-probe.js` (hunt for the claimed 25 bytes)
**Brief:** `AGREEMENT-DISTILL-FIX3-BRIEF.md` · **Maker report:** `maker/MAKER-REPORT.md`

## VERDICT: GOES BACK

One defect, and it is in the maker's **report**, not in the code: the claimed
fix-3 walk sha does not reproduce. Everything else in the round verified —
including the three F9 fixes themselves, the full state machine, the
fetch-verdict mechanism, the continue button, the laws delta, and the
no-regressions list. The code needs no change. The report's §2/§7 walk sha
must be corrected to the reproducible value before anyone lands this round,
because the landing steps verify against §2 — as written, they cannot succeed.

| # | Result |
|---|---|
| 1. Base + fix-2 reproduction | **PASS** — base matches exactly (fresh staging + git tree); all four fix-2 shas identical to the fix-2 checker report §1 |
| 2. Fix-3 shas (maker's §2 claims) | **FAIL on walk only** — unfold, welcome, identity all match; walk is 4,363,264 B sha `ef982267…`, not the claimed 4,363,239 B `b068d1da…` (25 B; see §6) |
| 3. State machine (checker's own, 152 assertions) | **152/2 PASS** — the 2 fails are the walk-sha claim, nothing behavioral |
| 4. Maker's script re-run by me | **139/139, exit 0** — but its own `FIXED3 walk` line prints `ef982267…`, contradicting maker §2 |
| 5. Fetch-verdict mechanism | **PROVEN** — the verdict (not the 4 s timer) advances the walk on fix-2 bytes; the `proceed()` guard holds both paths on fix-3 bytes |
| 6. Parallel-worker additions | **VERIFIED line by line** — all match the brief; no unsanctioned behavior |
| 7. Laws delta | **PASS** — 0/0 on all four files, with the REAL `check-design-laws.py` run on real bytes via pipe (not a replication) |
| 8. Landing | **BLOCKED** — EPERM re-proven by the checker; no filing, no rebuild, no deploy (correct: verdict is GOES BACK anyway) |

## 1. Base verification + fix-2 reproduction (independent, fresh)

Base fetched from staging by the checker, twice (once in my own script, once
inside the fix-2 re-run), and verified against the git tree via the git-data
API (`gh-direct.py GET .../git/trees/e0681545?recursive=1`, 12,272 entries):

| File | Base bytes / sha256 (first 16) | Git blob (path) |
|---|---|---|
| `agreement-unfold-fixed.html` | 141,781 / `5fe1a3ec2231c128` | `877afe659ba609e6…` (141,781 B) |
| `welcome-staged.html` | 1,913,241 / `c3c750b72a2b0330` | `8c4f9522bbb63129…` (1,913,241 B) |
| `walk-beginning-fixed.html` | 4,361,369 / `0f05b3f96ce8edd0` | `96d6899ba50345d1…` (4,361,369 B) |
| `identity-fixed.html` | 401,040 / `3279dc3572337e5e` | `7920438ed488869f…` (401,040 B) |
| worker `walk-beginning-staging-worker.js` | — (tree size 8,438,106 B) | `e2c840710bbf9e59…` (8,438,106 B) |
| build script `build-v23-staging-worker.py` | — | `0b6df24d60405388…` (92,883 B) |

All six match the fix-2 checker report §1 exactly. Paths (for the landing):
the four HTML files live under `team-nitro/agreement-unfold-fix-20261117/`
(unfold) and `team-nitro/walk-v23-assembly-20261114/` (welcome, walk,
identity, worker, build script). The maker report §7 names the build script
without a path — it is `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py`.

Fix-2 re-ran exactly (its own harness 33/33, laws delta 0/0 on unfold+welcome)
and all four fix-2 shas matched the fix-2 checker report §1 exactly:

| File | Fix-2 bytes / sha256 |
|---|---|
| agreement-unfold-fixed.html | 142,120 / `50876fff8caa79eeb3d6d75b4d2099db39ade2688edf6762e58ac9083eb0d26b` |
| welcome-staged.html | 1,929,575 / `3874b7ebcc6b95e2a7ef2d320ed95e13253083a954fe6c0efc36afe6d58fa747` |
| walk-beginning-fixed.html | 4,362,221 / `854a8f60328afca94e9856d660d02e897c4a777e0e5be4a9dcaaebc998283244` |
| identity-fixed.html | 402,166 / `d0f26529513ba25eb6614098f369583393345d5ee02ec4bc914c0d49085c0513` |

## 2. The fix-3 shas — what reproduces and what does not

The checker applied the brief's four remedies with its own transform
(`checker/work/check-fix3.js`, anchors located + context-printed in the
fix-2 bytes first). Result:

| File | Maker's §2 claim | Checker's own transform | Match? |
|---|---|---|---|
| agreement-unfold-fixed.html | 142,120 / `50876fff…` (unchanged) | 142,120 / `50876fff8caa79eeb3d6d75b4d2099db39ade2688edf6762e58ac9083eb0d26b` | **YES** |
| welcome-staged.html | 1,929,575 / `3874b7eb…` (unchanged) | 1,929,575 / `3874b7ebcc6b95e2a7ef2d320ed95e13253083a954fe6c0efc36afe6d58fa747` | **YES** |
| walk-beginning-fixed.html | 4,363,239 / `b068d1da…` (+1,018) | **4,363,264 / `ef98226767ddbb507b7e8282a64c72e4c741b3bf0b38413985484798dbc7464f`** (+1,043) | **NO — 25 B** |
| identity-fixed.html | 402,647 / `51776174…` (+481) | 402,647 / `51776174b59cee4a39f7a00eb7f7b874fc33103a0235308a876d4a94179307f5` | **YES** |

The mismatch was proven three independent ways, so it is not a transcription
error in the checker's transform:
1. **Checker's own transform** (`check-fix3.js`): walk 4,363,264 `ef982267…`.
2. **The maker's own constants, evaluated verbatim** (`diff-maker.js` slices
   the transform block out of `run-fix3.js` and executes it — no retyping):
   walk 4,363,264 `ef982267…`, byte-identical to the checker's transform;
   identity identical too.
3. **The maker's own script, re-run by the checker** (twice, exit 0,
   139/139 both times): its own `FIXED3 walk` line prints
   `4363264B sha256 ef98226767ddbb507b7e8282a64c72e4c741b3bf0b38413985484798dbc7464f`
   — contradicting maker §2 in the script's own stdout.

Insertion arithmetic (measured from the constants): identity +481 B (matches
the claim); walk P-GUARD +332, T-GUARD +98, continue button +119, wiring
+494 = **+1,043 B** (the claim says +1,018 B). The 25 B live somewhere inside
the walk insertions. A hunt over ten plausible earlier variants
(`variant-probe.js`: no button, no button style attr, no diamond, no wiring,
no wiring comment, no guard comment, no-space guards, no "never a timer",
em-dash→hyphen, no no-alias clause) matched **neither** the claimed size
**nor** the claimed sha — the closest was button-without-style-attr at
4,363,236 B (3 B short). **The claimed bytes survive nowhere**: no file, no
blob, no branch (both fix-2 and fix-3 branches 404 — §7), no constructible
variant. What the 25 bytes were is unknowable from surviving records; what is
known is that the current bytes are the ones the script deterministically
produces and the ones every behavioral check below was run against.

**Why this is GOES BACK, not a note:** the landing steps (maker §7) verify
each filed file "by size + sha256 against §2" and update the build script's
asserts to the §2 walk sha. Followed literally, the landing fails its own
verification (file `ef982267…` ≠ assert `b068d1da…`) — or, if someone
"fixes" the assert by recomputing from disk without noticing, the record
keeps a false sha permanently. The remedy is a one-line report correction
(§6), not a code change: the fix itself is fully verified below.

## 3. Fix-by-fix table (the checker's own evidence)

| # | Fix | Checker's evidence |
|---|---|---|
| F9(a) input | Name wiped after fill | **PASS.** Paired URL at runtime: input `="distill"` at boot AND after 5 s (S6a/C-IDENT). Byte order proven: FIX2-insert @347486 < FIX3-clear @348990 < load-paint @355605 < FIX3-paint @355635 — the paired paint sits after the clear and after the load-time paint, exactly as the brief's remedy orders. Name-only: input `""` (captain's reconciliation holds). Alias-only: input `="distill"` via the pre-existing FIX6 load check (base-proven — the same value on base bytes, so not a fix-3 change). No-params: `""`. |
| F9(a) echo | Certificate name never shows | **PASS.** Paired URL at runtime: hero text `="Distill Eye Walk"`, `data-text="Distill Eye Walk"`, `hidden=false` at boot AND after 5 s. Paint goes through `paintHeroName` (the one hero painter — 1 definition; text + data-text + hidden set together). Control: base paired bytes show hero `""`/hidden (the bug) with the same input value — so the fix, not FIX6, paints the hero. Later painters cannot clobber it at boot: `checkAliasAvailability`'s verdict only calls `setAliasState` (never `paintHeroName`); `stampCertificate` paints only on stamp; the `setAliasState` 'own' path paints `certRegalia.name \|\| rawName` — registry truth with the passed name as fallback. |
| F9(b) guard | Wrong timer advances the walk | **PASS — mechanism proven, not assumed (§4).** `proceed()` guarded at its top (spaced form 2×: guard + timer guard; fix-2 K3 no-space guards still 2×). Door visible at boot, still `["step-door"]` after 6 s with no user action, on both the default fetch and a never-resolving fetch. The 4 s timer fires inside that window and the guard holds it (pending-fetch run). |
| F9(b) dismiss | Door needs a user action | **PASS in all three scenarios.** Continue button: exactly 1×, `type="button"`, same `.p3-enter` pill as its sibling cert link, placed immediately after it in `#step-door`, outside any `<form>` (so it cannot submit anything). Wiring (boot IIFE, where `proceed()` is in scope): hides the door first, then `proceed()` — so the guard passes. Aliased: visible, tap → `["step-1"]`. No-alias: hidden, cert link present (the only way forward). Certified return trip (alias+name in localStorage): door holds 2 s, continue visible, tap → `["step-1"]`. Cert link still exactly 1× and still carries name+alias at runtime. It is one of the brief's two sanctioned dismiss actions (certificate link or explicit continue) — verified in implementation, not just in name. |
| CORE | Do not regress | **PASS.** Full state machine §4: deck 37/37 + letter 37/37 + unfold 37/37, jewel in sync every landing, holds firing, bridge URL exactly 1 replaceState on both routes, race retry+fallback fired at runtime, rail 67 articles, money board 51 clean, plain-welcome scenario 5 in full. |
| F1–F8, F9c, F10, (a)(b)(c) | Everything else | **PASS.** Unfold + welcome byte-identical to fix-2 (sha). Money-board cut live in the rail DOM (`hired!` 0×; board 51 has no Congratulations/hired). Board-22 title "How it all connects" present, old title 0×. `slide-*.jpg` multisets identical base→fixed on all four files (unfold 8, welcome 16, walk 0, identity 0 refs). `#letterAll` + `#fpLinkLetterAll` NOT restored (ids absent — captain's settled call followed). |
| Diff minimal | Only the claimed F9 changes | **PASS.** Reverse-application proof: fixed identity minus the one I-FIX3 block == fix-2 bytes exactly; fixed walk minus the four insertions (guard comment+line, guarded timer, button line, wiring block) == fix-2 bytes exactly. Nothing outside the claimed set. Insertions carry no `color:` and no `font-size`; no new CSS rules (no `<style>`; the only `style=` occurrences are the anchor's pre-existing `text-decoration` and the button's `font-family:inherit`). Syntax: all 15 script blocks parse (unfold 7, welcome 5, walk 2, identity 1). |

## 4. The fetch verdict — the key mechanism claim, proven causally

The maker claimed the FETCH VERDICT (not the 4 s timer) advances the walk in
1.5 s on fix-2 bytes, so guarding the timer alone would not have fixed it.
The checker proved this from the base bytes with its own runs — it did not
take it from the maker:

**In bytes (fix-2 walk, base mechanism).** The boot IIFE issues
`fetch('/api/claim?alias=' + …)` with two handlers, both funneling through
`proceed()`:
```js
.then(function(d){
  if (gateDone6) return; gateDone6 = true; if (gateTimer6) clearTimeout(gateTimer6);
  if (d && d.exists && !d.own) { window.location.href = '/identity.html?name=' + … + '&alias=' + …; return; }
  proceed();
})
.catch(function(){ if (gateDone6) return; gateDone6 = true; if (gateTimer6) clearTimeout(gateTimer6); proceed(); });
```
`proceed()` is the single funnel: it resumes at the first unanswered step
(`showStep(first)`), or shows the end slide on a saved reveal. The full
advance-path enumeration of the walk scripts (12 `setTimeout`, 0
`setInterval`, 2 `fetch`, 5 `proceed()` sites, all `showStep`/`showDoor`/
`.hidden = false` sites) shows exactly three boot-time advance legs — the
fetch verdict, the fetch catch, and the 4 s claim-gate timer — and all three
call `proceed()`. Every other timer is a status/copy/scroll/reveal timer
that never touches a step; every other `showStep` call sits inside a
user-action handler or inside `proceed()` itself. No path advances the walk
while the door is visible except through `proceed()` — so guarding
`proceed()` itself covers all three legs, and the timer guard additionally
keeps the 4 s gate unconsumed while the door is visible.

**At runtime (checker's causal test, 100 ms polling).** On fix-2 bytes,
aliased URL, default harness fetch (resolves 404 immediately; the one fetch
call at boot is `/api/claim?alias=distill`): the door advances to `step-1`
at **104 ms** — before the 4 s timer could possibly fire, so the timer is
NOT the advancer. Same bytes with the fetch stubbed to **never resolve**:
the door advances at **4,094 ms** — at the timer, not before. That pair is
the causal proof: verdict first (fast), timer second (4 s backstop). On
fix-3 bytes the door holds 6 s with the default fetch AND with the pending
fetch — the `proceed()` guard holds the verdict path and the timer path
together. The maker's control (`control-fix2.js`, re-run by the checker)
agrees: C1 input `""`, C2 hero `""`/hidden/`null`, C3 door → `step-1` in
1.5 s — **3/3 reproduced on fix-2 bytes**, so the harness can see the bugs
and its passes on fix-3 bytes are not vacuous.

## 5. State machine — checker's own harness (152 assertions)

`checker/work/check-fix3.js` drives the real HTML + real scripts in the
checker's DOM (`dom-check3.js`, the fix-2 checker's fixed copy + a
pending-fetch patch — diff proves the patch is the only change) and proves,
tap by tap. **TOTAL: 152 pass / 2 fail** — the 2 fails are the walk-sha
claim (§2), nothing behavioral. The maker's script, re-run by the checker
twice, reports **139/139, exit 0** — on the `ef982267…` bytes (§2).

| Scenario | What it proves | Result |
|---|---|---|
| C-IDENT paired | `?name=Distill Eye Walk&alias=Distill`: input `="distill"`, hero text + data-text `="Distill Eye Walk"`, unhidden — at boot AND after 5 s; seal present; no errors | pass |
| C-IDENT name-only | `?name=` only: input `""`, hero blank + hidden + data-text null (FIX3 stands) | pass |
| C-IDENT alias-only | `?alias=` only: input `="distill"` (pre-existing FIX6), hero hidden | pass |
| C-IDENT no-params | Input empty, hero hidden | pass |
| C-IDENT base paired | Same paired URL on BASE bytes: input `="distill"`, hero blank + hidden (the before-state) | pass |
| C-WALK aliased | Door visible at boot, seal, link carries name+alias, still `["step-door"]` after 6 s, continue visible → tap → `["step-1"]` | pass |
| C-WALK no-alias | Door visible, continue hidden, cert link present | pass |
| C-WALK return | Alias in localStorage: door holds 2 s, continue visible, tap → `["step-1"]` | pass |
| C-WALK pending-fetch | Fetch never resolves: door still visible after 6 s (timer fired, guard held) | pass |
| C-CAUSAL | Fix-2 advance at 104 ms (default fetch) vs 4,094 ms (pending fetch); fix-3 no advance in 6 s | pass |
| C-CORE deck | 37 boards one-at-a-time, jewel in sync, Enter → hold → bridge, exactly 1 replaceState to `/?stage=bridge` | pass |
| C-CORE letter | Same 37/37, I agree → hold → bridge, exactly 1 replaceState | pass |
| C-CORE unfold | /agreement 1→37, pill + cascade in sync, Back 37→36, board 37 keeps Congratulations — you're hired | pass |
| C-CORE race | Failed showcase → `&retry=1` + `data-fp-retried=1`; second failure → showcase hidden; failed face → `crystal-n.png` | pass |
| C-CORE rail | 67 rail articles, money board 51 clean, "read the whole page at once" link exists | pass |
| C-CORE plain | Hero Read → /agreement; agreed submit → hold → identity with the name; reload with fromBridge re-opens the name form | pass |
| C-CORE stage redirects | ?stage=deck/letter/bridge → /?stage=… (1 replace each) | pass |
| Byte harness + laws | Fix-3 insertions, minimality by reverse-application, no-regress spots, syntax 15/15, laws delta 0/0 ×4 | pass except the 2 walk-sha claim fails |

Observation (recorded, not scored): after boot on the paired page, dispatching
a manual `input` event on the alias field left the hero at "Distill Eye Walk"
(no degradation observed in the harness). The harness input-event path may
not faithfully model a real keystroke, and the page's designed live-echo
(v2.11.2 — the hero echoes typing) means a real keystroke legitimately
repaints the hero from the field; the eye should type in the field on staging
and confirm the echo reads sensibly. Not a fail.

## 6. The one fail — exact remedy

**FAIL — maker report §2 (and §7) walk sha is stale.** The reproducible
fix-3 walk is **4,363,264 B, sha256
`ef98226767ddbb507b7e8282a64c72e4c741b3bf0b38413985484798dbc7464f`**
(delta **+1,043 B** on fix-2), not the claimed 4,363,239 B /
`b068d1da38403878eb0b4a552ea92efec2fe77724d6a12fdef04f98fb8f8089b`
(+1,018 B). Proven three ways (§2). The claimed bytes survive nowhere
(§2, variant hunt).

**Remedy (report-only; no code change):** in the maker report, correct §2 to
walk **4,363,264 B / `ef982267…`** (+1,043 B) and correct §7 step 2 to
`walk 0f05b3f9→ef982267` (identity `3279dc35→51776174`, unfold
`5fe1a3ec→50876fff`, welcome `c3c750b7→3874b7eb` — all already correct).
Then re-run `node run-fix3.js` and confirm its `FIXED3 walk` line matches
the corrected §2, and land per §7 with the corrected asserts. The captain's
eye then walks the corrected bytes. The fix-3 code itself is verified and
needs no rework.

## 7. Laws — §11 design check in writing + machine delta (REAL checker)

**The real `check-design-laws.py` RAN this round** — no disk files needed:
the checker piped real bytes (base via staging fetch, fixed via the
checker's `--dump` mode) straight into `python3 check-design-laws.py
/dev/stdin`. Counts on real bytes, all eight states:

| File | Base | Fixed | Delta |
|---|---|---|---|
| agreement-unfold-fixed.html | 1 FAIL / 2 WARN | 1 FAIL / 2 WARN | **0 / 0** |
| welcome-staged.html | 83 FAIL / 4 WARN | 83 FAIL / 4 WARN | **0 / 0** |
| walk-beginning-fixed.html | 128 FAIL / 8 WARN | 128 FAIL / 8 WARN | **0 / 0** |
| identity-fixed.html | 11 FAIL / 2 WARN | 11 FAIL / 2 WARN | **0 / 0** |

The checker's JS replication (transcribed fresh from the script) agrees on
all four files, and the normalized fail sets are identical (unfold 1 unique
fail, welcome 20, walk 22, identity 11; 0 truly-new, 0 removed). All
pre-existing FAILs are the known ones (gray words inside comments, 12–12.5 px
foot text — pre-existing, not introduced by this round, and not in this
round's brief to re-typeset). The added code carries no `color:` and no
`font-size` below 17 px (the continue button inherits the existing
`.p3-enter` pill — same family, same styling, no new CSS at all).

**§11 check in writing (eye part):**
- **Reference object per changed element:** the continue button is measured
  against its own sibling — the door's existing "Get your certificate ◆"
  `.p3-enter` pill (same class, same pill, stacked vertically; nothing
  invented). The hero paint is measured against the page's own
  `paintHeroName` (the one hero painter — text + data-text + hidden set
  together, never apart). The door guard is measured against the door's own
  `hidden` attribute (the same flag `showDoor()` sets).
- **Hover every object:** the continue button is a `.p3-enter` pill — it
  inherits whatever hover the existing door link already carries (same
  class, same family). No new interactive control with new hover was
  introduced; the identity input and the cert link are unchanged controls
  with pre-existing hover/focus.
- **Gray-text grep:** the real gray regexes ran over base and fixed on all
  four files (delta 0, normalized sets identical). The added JS carries no
  `color:` declaration at all.
- **Size grep:** the added JS carries no `font-size` at all. The 12–12.5 px
  hits are pre-existing foot text, untouched.
- **Flow check:** the board flow is unchanged — one tap per board, pill in
  sync, re-proven by the state machine on the fixed bytes (37/37 deck +
  37/37 letter + 37/37 unfold). The only flow-adjacent changes are the
  three F9 remedies themselves, each re-proven at runtime (§§3–5): the
  certificate paints the passed name, the door holds until the user acts,
  and the certified citizen has exactly one tap (Continue) into the
  questionnaire.

**Five gates (before acting):** 1. Right — the certificate names the reader
and the door waits for the reader; nothing is taken from anyone. 2. Truly
needed — these are the eye's three exact F9 fails, worked to zero at
runtime. 3. Mine to do — the dispatched checker round; no protected gate
crossed (no money, no credentials, no destructive action, no live deploy,
no merge, no link to Shawn). 4. Now — the round ran inside the live
sequence; the overrun is documented, not absorbed silently. 5. Prove it —
§§1–7 above, all re-runnable by the captain from `checker/work/`.

## 8. Landing — BLOCKED by EPERM (re-proven by the checker; do not force it)

- `node` fetch from staging works (141,781 B), but `fs.writeFileSync` in the
  same network-touching process fails: `EPERM: operation not permitted, write`
  — and leaves a 0-byte file (deleted afterwards by the checker).
- A plain shell write failed the same way in the same window:
  `echo: write error: Operation not permitted` (the flake is currently
  blocking even non-network writes, per-path per-moment).
- Nothing is filed, nothing rebuilt, nothing deployed. The checker confirmed
  via the branches API that **neither** `walkthrough/agreement-distill-fix2-20261119`
  **nor** `walkthrough/agreement-distill-fix3-20261119` exists (both 404).

**Exact landing steps for the next round, when the window opens (with the
CORRECTED walk sha from §6):**
1. Correct maker §2/§7 to walk 4,363,264 B / `ef982267…` (+1,043 B).
   Re-run `node run-fix3.js` in `maker/work/` (expect FIX2 §1 shas + 139/139
   + the `FIXED3 walk` line matching the corrected §2), then write the four
   fixed files to disk (verify each by size + sha256 against the corrected §2).
2. Update `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py`
   sha asserts to the fixed shas (walk `0f05b3f9`→`ef982267`, identity
   `3279dc35`→`51776174`, unfold `5fe1a3ec`→`50876fff`, welcome
   `c3c750b7`→`3874b7eb`).
3. Run the build script to rebuild the worker; verify the rebuild is
   byte-identical to a second rebuild.
4. File branch `walkthrough/agreement-distill-fix3-20261119` from base
   `e0681545` via the git-data API (base blob shas verified in §1), then
   verify the filed bytes by FRESH blob-API reads (filed blob shas must
   equal the in-memory fixed shas).
5. Do not deploy staging from unfiled bytes.

**Open question (carried from fix-2, not a fail):** the worker blob decoded
via the blob API is 8,438,021 B vs the tree size 8,438,106 B (85 B short).
Re-check when the worker is rebuilt from disk inputs.

## 9. Harness notes + parallel-worker verification (for the next checker)

- The checker's DOM copy (`dom-check3.js`) differs from the fix-2 checker's
  fixed copy by exactly one patch (proven by `diff`): `preset.fetch ===
  'pending'` returns a never-settling promise, which is what makes the
  causal test in §4 possible. Everything else is byte-identical (sha
  `84bea701…` before the patch).
- `node ... > file` redirects from a network-touching process land 0 bytes
  in this VM; the checker piped through the tool output and through
  `| python3 … /dev/stdin` instead — pipes to another process work fine.
- **Parallel-worker additions — verified line by line against the brief and
  the base bytes (not assumed):** `control-fix2.js` (68 lines: C1/C2/C3 as
  in §4 — re-run by the checker, 3/3 reproduced); the continue button
  (W-FIX3c) + wiring (W-FIX3d) + byte checks W3f/g/h + scenarios S7/S7b/S7c
  + S6a +2 s stability checks in `run-fix3.js`. Every added line does
  something the brief sanctions: the button is the brief's explicit
  continue; the wiring is the only way to dismiss the door without
  navigating away; the scenarios are the brief's three door cases
  (aliased, no-alias, certified return trip). No added line does anything
  the brief did not sanction — no new navigation, no new timer, no new
  CSS, no change to the certificate-link path (still exactly 1×, still
  carrying name+alias). The stale W3a count the maker reports fixing is
  fixed in the file as run (W3a counts the full "— the door is the gate:"
  string, 1× — the checker's own count of the spaced guard is 2×, the
  guard + the timer guard, as designed).
- The checker's full run took ~150–170 s (harness parses of the 1.9 MB
  welcome file dominate); the maker's script ~150–270 s. Budget for it.

## 10. What the captain's eye must still prove (pixels — not claimed here)

VM browsers are dead (Chromium SIGTRAP, Firefox SIGSEGV) — no render was
seen in this round. The harness proves bytes, counts, geometry arithmetic,
syntax, and state transitions — not pixels. On the new staging, at phone
width first: the completed certificate names the reader (F9a — currently
FAILS on staging, which still serves fix-1 bytes); the door waits with both
its pills visible and tappable (F9b — "Get your certificate ◆" and
"Continue to the walk ◆" — the eye judges whether two pills stack well
there); the seal sits bottom-centre on home, deck, letter, identity, and
the welcome door (F7); the left edge is clear on every deck board (F1);
Naya's photo sits top-right, fully visible, on deck and letter (F2/F4); the
footer reads whole in the first view on every board (F3); board 37's
picture fills the void (F5a); images fit whole with no bottom crop (F5c);
the Ambassador button is visible in the first view on board 37's end card;
typing in the alias field echoes sensibly in the hero (see §5 observation).
Phone 390 was NOT tested (carried from the brief). The anthem wiring round
still queues behind this one (same file, one lane). No merge, no live
deploy, no link to Shawn — the maker corrects §2/§7 first (§6), then the
captain's eye.
