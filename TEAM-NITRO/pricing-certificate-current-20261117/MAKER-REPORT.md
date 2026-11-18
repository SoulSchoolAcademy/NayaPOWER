# MAKER REPORT — Pricing Certificate Current (2026-11-17)

**Maker:** Naya Nitro Narzan (maker seat) · **Round:** pricing/certificate-current-20261117
**Status: STAGED WITH A FIX — live browser probe OWED, not claimed done.**
The current certificate is staged on the pricing-free staging worker and
verified byte-for-byte from served bytes, but the fresh-alias walk at 1920
and 390 was NOT run: every VM browser is dead (Chromium SIGTRAP, Firefox
SIGSEGV, 4 attempts, same signature as the 2026-11-12 event). The probe
script is filed and is the exact spec for the checker seat's cloud-browser
run. No alias was claimed — zero aliases burned.

## §0 Laws read first
`THE-NAYA-DESIGN-LAWS.md` (v2.1), `THE-PLAYBOOK.md`,
`DESIGN-INTELLIGENCE-REPORT.md`, the brief
`BRIEF-PRICING-CERTIFICATE-CURRENT-20261117.md` (§0–§6), plus
`team-nitro/AGENTS.md` (Checklist Law, Whole-Page Rule, Continuous Cycle
Law). Harvest verbatim, never rebuild; staging is the deliverable; live
is Shawn's hand.

## §1 Current-treatment source (named BEFORE touching anything)
- **File:** `~/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html`
- **Size:** 376,814 B · **sha256:**
  `8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d`
- **Live:** identical to staged
  `https://naya-walk-beginning-staging.nayapower.workers.dev/identity.html`
  (re-curled 2026-11-17).
- This is LATER than Certificate Round 5 (`1b8fd1d1`, 373,856 B,
  2026-11-16 03:44Z); it is the identity state bundled when the walk-end
  fix round landed 21:38Z 2026-11-16. It carries Round 4 H1 (trophy name)
  + Round 5 H3/H1/H2.
- **GitHub blob caveat (do not invent):** the Round 5 bytes `1b8fd1d1…`
  are blob `f760902f…` on branch `identity/certificate-round5-20261116`
  commit `6a139321…`. The staged/on-disk `8c641f96…` file's GitHub blob
  was NOT established in this round; none is claimed here.
- Round 2 record:
  `walk-v23-assembly-20261114/MAKER-RECORD-IDENTITY-CERTIFICATE-ROUND2-20261115.md`
  (Micheal row: alias `micheal`, cert_no 204, created 2026-11-13).
  Round 5 record: `MAKER-RECORD-IDENTITY-CERTIFICATE-ROUND5-20261116.md`.
- The walk bundle `/free/walk` derives from
  `walk-beginning-fix-20261111/walk-beginning-fixed.html` (sha `df17ac67…`,
  3,288,238 B) — but the certificate VIEW in the walk is `/identity.html`,
  so identity is the harvest source.

## §2 Base verified (before any work)
- Branch `pricing-f4-free-entry-20261116`, tip `eafbac16`
  (verified live: "Pricing Fix round: maker report with the filed commit
  SHA recorded (e6bf9a87). No code change." — on top of pricing-fix tip
  `e6bf9a87`, itself on top of taken-fix tip `fc6f70b0`). `/free` entry 315,878 B, sha256
  `06b08242c72e9d0b8f28037df3b93e74c5955e6702f358d0a07fff799edf58fd` —
  identical to `pricing-fix-20261117/fixed-entry.html` and to live staged
  `/free` (re-curled 18:48Z 2026-11-17).
- `/free/walk` 3,293,555 B, sha256
  `46bc52e54ac02e87cdad0ae2924ce35555671333ce3c7cd96676f17d86253fa1`.
- Staging worker 3,630,970 B, sha256
  `59e658353c079ca4ce3f8c7f8d37341efdd9bec92770bee22c1c77e48761fb90`.
- Pricing v78 untouched: 11,360,503 B, sha256
  `ca2eafeb896c763ae2459b4a10b8715e726765ced607c0aab3640d27e6c39ae2`.

## §3 Diff found — /free vs identity (measured from served bytes)
Seven deltas; the first four are the harvest (the brief's five diff
dimensions, H1–H4):
1. **Name:** `/free` plain white `color: var(--ink)`, no clone, no
   gradient, no chrome stroke, no hover, no settle; certified only a
   purple text-shadow. Identity: obsidian gradient body, 1px chrome
   stroke, `::before` clone (purple gradient, blur 12px, opacity 0.45
   rest / 0.9 hover), hover lift −2px + halo, `name-settle` 0.5s,
   certified `text-shadow: none`.
2. **Panels:** `/free` blue fill `#163a56 → #0a1c2e → #030609` (link)
   and brown-gold `#3a2a09 → #1c1204 → #060402` (mail), labels `#a8dcff` /
   `#ffd97a`, values painted instantly. Identity: obsidian fills
   `#101013 → #050505 → #070708` both, white labels, values typed
   letter-by-letter at 26ms/char with a caret in the panel's own color.
3. **Gray tokens:** `/free` `--silver`/`--muted` `#f2f2f6` (9 code
   occurrences), `--faint` `rgba(242,242,246,0.88)`, `--purple` `#a855f7`
   (second purple), `--hair` cream `rgba(245,241,232,0.16)`, plus
   cream/silver-white rgba tints. Identity: all `#ffffff` / white 0.88 /
   `#a06bff` (one purple) / white hairline; zero cut tokens.
4. **Agreement wording:** `/free` has ZERO mentions of "agreement".
   Identity carries the official sentence verbatim on the typed face
   only (10 mentions of "Collective Agreement"): "By entering your name,
   you make it official — you are signing the Collective Agreement, and
   you get the deed to your own world: high-level digital real estate —
   your personal page, your business, your space — free forever."
5. **Membership sentence** (`.cert-member`, Round 3 H1): present on
   identity (8 occurrences), ZERO on `/free`. **NOT harvested** — outside
   the five dimensions; needs its own geometry funding on `/free`'s
   certified face. Named follow-on.
6. **H6 green taken message** (`.hub-note.taken-note`, Round 5): 5
   occurrences on identity, ZERO on `/free`. **NOT harvested** — same
   reason. Named follow-on.
7. **`.cert-more` "Why this matters" unfold:** absent on `/free`.
   **NOT harvested** — the reader supersedes it as the full-agreement path.
- Already aligned, no work needed: `/free` is Marcellus (Newsreader 0);
  `.cert-plaque` / `.identity-pro-card` is `position: relative` on both;
  TAKEN STATE block and pricing-fix taken rules present on `/free`.
- Left verbatim, deliberately: the dead harvested `.enter` rule (live
  entrance, no element uses it) — its `#302054` / `rgba(168,85,247)` are
  purple-family glow in a dead rule, not gray text. Identity's `--serif`
  Newsreader NOT harvested — `/free` stays Marcellus per the 02:28Z
  2026-11-17 decision (one serif, Marcellus).
- Geometry kept: name size clamps byte-identical (desktop
  `clamp(2.4rem, 6.4vw, 4.1rem)`, phone `clamp(2.55rem, 13.5vw, 3.4rem)`,
  taken `clamp(1.65rem,6.2vw,2.5rem)`); only the paint was harvested.
- Name click: certified name click triggers the existing `startOverBtn`
  (identity Round 2 F8 equivalent); in composing it only hovers.
- Geometry funding: NOT pre-funded. The sentence adds ~40–50px to the
  typing-state foot at desktop; the v2.11.1 fit was already tight (~14px
  margin). The probe must measure foot bottom vs plaque bottom at
  1920/390/635 and fund only if overflow is proven, using Round 5's levers.

## §4 THE DEFECT FOUND AND FIXED (the round's real story)
The first staging (18:59Z 2026-11-17, entry 332,181 B, sha256
`72b18a32fd8d6bc0e876b1ae36a6f633fa32d453e224ff139b0a123c63797262`,
worker `16056fef…`) shipped a **JS syntax error in the main inline
script block**: the harvested reader IIFE closed `}();` instead of
`})();` — its grouping paren was dropped. In a browser, a syntax error
in a `<script>` block kills the WHOLE block: no availability check, no
claim, no paint. The staged page was broken, not just unproven.
- **Root cause (build line):** `extract_rule` returns through the
  function's closing `}` only; the build appended `"();"` where identity
  has `")();"` — a one-character harvest error.
- **Why it shipped:** two safety nets failed together. (1) The build's
  `js_syntax_check` used temp-file `node --check` and SILENTLY SKIPPED
  every block when the EPERM flake blocked the writes. (2) The live
  browser probe that was meant to be the fallback could not run (VM
  browsers dead). A check that can skip is not a check.
- **Caught by:** the maker's own static audit (`audit-static.py`,
  node `vm.Script` compile of every `<script>` block, no disk writes):
  block 2 failed `Unexpected token ';'` at line 188 `}();`, while the
  BASE block 2 compiled clean — proving a harvest regression, not a
  pre-existing fault. Bisection isolated it to the reader IIFE; identity
  closes `})();`.
- **Fix (build-certificate.py, three edits):**
  1. Reader IIFE append `"();"` → `")();"` + assert the harvested IIFE
     is byte-identical to identity's own segment (start marker through
     `})();`).
  2. `js_syntax_check` rewritten: `vm.Script` compile fed via stdin —
     no disk writes, NO skips; if it cannot run, the build FAILS.
  3. Step-0b live guard accepts the first (broken) staging sha
     `72b18a32…` as the expected live state for the fix re-run (the fix
     re-derives from the filed chain, never from live).
  4. Added main() assert: `new_entry.count("})();") >= 2` (reader +
     name-click IIFEs).
- **Re-staged 19:10Z 2026-11-17** (see §5). The audit now passes on all
  three script blocks (see §6).

## §5 Staging verification (fixed build, 19:10Z 2026-11-17)
- New entry: **332,182 B** (one byte more — the added `)`), sha256
  **`1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3`**.
- New worker sha256
  `f4cc645f218b8b2a81f4daff7fcbb0ef604d8ac82bd867c38875dab0e6f44e73`,
  Cloudflare read-back MATCH, `modified_on 2026-11-17T19:10:02Z`.
- Live HTTP verified (in-run + re-curled via stdout pipe):
  `/` 1,966 B · `/free` 332,182 B == source MATCH, sha `1e1bb489…` ·
  `/free/walk` 3,293,555 B unchanged MATCH · `/sw.js` 567 B (sha
  `abac2ab5…`) · `/manifest.webmanifest` 581 B (sha `b4abd81c…`) ·
  `/free/hub` 302 → `https://nayanet.app/`. Pricing v78 unchanged
  (`ca2eafeb…`). Walk unchanged (`46bc52e5…`).
- Node fetch-handler driver: PASS (new entry + walk + index + sw.js +
  manifest + hub).
- **EPERM flake (open, environmental):** the build's python disk write of
  `fixed-entry.html` failed (`[Errno 1] Operation not permitted`) and
  left a 0-byte file; removed after each run. The new bytes exist in
  memory (reproducible from the build script) and on the staged worker.
  The filing script re-derives the bytes in memory (import the build
  module, regenerate + apply, no staging) and files blobs from memory —
  never reads `fixed-entry.html` from disk. The same flake corrupted
  `curl -o /tmp/...` writes (HTTP 200 with a 0-byte file on disk) and
  `tee` writes; verification here used stdout pipes and in-memory fetches
  only.

## §6 Static audit of the staged bytes (all green)
Run against live staged `/free`, sha-verified `1e1bb489…`
(`audit-static.py`, `audit-static2.py`):
- Official sentence (exact): 1 · `cert-info-para` `<p>` elements: 9 ·
  CSS `.cert-info-para` selectors: 2 · `paintHeroName` / `paintValues` /
  `settleHeroName` defined: 1 each · obsidian `#101013` gradient starts:
  3 (link-line, mail-line, + one more obsidian fill) · `--silver:
  #ffffff`: 1 · `data-text`: 5 · clone `content: attr(data-text)`: 1 ·
  clone purple `#c9a5ff`: 2 (clone + hover halo gradient) · agree hidden
  on certified: 1 (`.cert-plaque.is-certified .cert-agree`) · agree hidden
  on taken: 1 (`.face-foot:has(.alias-status[data-state="taken"])`) ·
  taken `text-shadow: none`: 1 · Marcellus: 2 · name clamps kept: 1+1 ·
  `})();` IIFE closers in file: 6 (4 pre-existing + reader + name-click).
- Cut tokens, all ZERO: `#f2f2f6`, `#a8dcff`, `#ffd97a`, `#163a56`,
  `#3a2a09`, `#a855f7`, cream `245,241,232`, `Newsreader`,
  `rgba(242,242,246`.
- Named non-harvests, all ZERO as decided: membership sentence,
  H6 taken message, `.cert-more`.
- **JS syntax (node vm.Script, all blocks):** block 0 (415 chars) OK ·
  block 1 (223) OK · block 2 (37,720) OK. BASE block 2 (33,412) also OK.
  The syntax regression is fixed and proven fixed from served bytes.

## §7 Design-laws machine check (`check-design-laws.py` regexes, in memory)
- **BASE** (`06b08242…`): 10 FAILs, 0 WARNs. All 10 are checker false
  positives: 7 are comment prose containing "gray"/"grey" (the checker's
  `\bgray\b` matches comments), 3 are `border-color: rgba(..., 0.32/0.52)`
  hairlines (the `color:` regex matches `border-color:`, and purple
  `rgba(160,107,255,0.52)` is not gray text at all). The machine checker
  never caught the real gray (`#f2f2f6`) — the static audit in §6 is the
  real gray proof.
- **NEW** (`1e1bb489…`): 12 FAILs, 2 WARNs. Inherited: 8 (7 comment lines
  + the purple border line). The two cream border lines changed value
  (cream → white) and the checker still flags them (white 0.32 alpha
  matches its dim-rgba pattern) — same 2 lines, now white, counted as
  fixed+new by the differ. Genuinely new machine flags, adjudicated:
  - **SIZE 13px** (`.cert-info` "i" glyph) and **SIZE 15px**
    (`.cert-info-x` "×" glyph): icon glyphs inside real objects (the ⓘ
    circle, the × close button), harvested verbatim from the current
    treatment — not body text. §2.3 governs text; the §13 open question
    leaves sub-17px tile/icon furniture undecided ("His ruling owed").
    Judged non-violations; the eye (probe screenshots) is the final word.
  - **WARN `color: transparent` ×2**: the trophy name's transparent
    color (text shows via `background-clip`) + the clone's. Expected
    consequence of the harvest; the probe's computed-color audit will
    show the name renders.
- **Verdict: zero new REAL fails.** No new text-color, gray-text, or
  size violation on body text. (Two earlier "PASS" runs on a 0-byte
  file are DISCARDED — the EPERM flake had emptied the file; the
  in-memory check in `laws-check-new.py` is the real one.)

## §8 Fresh aliases used
**NONE.** The live probe never ran, so no alias was claimed and none was
burned. The probe script reserves `certcurrent` (hero "Certcurrent")
for the checker seat's run — it has NOT been claimed anywhere. Test
certs 737–746, 753, 755, 781/782 remain open awaiting Shawn's-hand cleanup
(as before).

## §9 Live probe — NOT RUN (owed, with the exact route)
`probe-certificate.py` is written and filed; it was never executed to
completion because **no VM browser launches**:
- 19:03Z: Playwright Chromium headless shell — SIGTRAP at launch (pid
  60243). Full Chromium build (`chromium-1248/chrome-linux64/chrome`) —
  same SIGTRAP (pid 60593). Firefox 1555 — SIGSEGV at launch (pid 61220).
- 19:11Z re-test: Chromium headless shell — SIGTRAP again (pid 66714).
- `--version` still prints fine (156.0.8078.4); the binaries are intact.
  This is the known recurring VM-browsers-dead condition (TOOLS.md,
  2026-11-12 event: Chromium 133, Firefox 139). The same probe shape ran
  fine at ~04:00Z 2026-11-17 (taken-fix round, `shots-after/`), so the
  breakage arrived between 04:15Z and 19:03Z.
- The forwarder `h1-proxy-forwarder.py` is running (PID 3522, since
  17:32Z); the failure is at browser launch, before any network.
- **Route (per TOOLS.md): the cloud browser task (`browser.browse`).**
  The checker seat runs `probe-certificate.py`'s flow there (or its
  equivalent): fresh alias `certcurrent`; 390 typed (trophy name computed
  style incl. `::before` clone, obsidian panels, agree line + exact
  sentence, ⓘ reader open → "2 of 9" → Close/Escape, console, overflow)
  + screenshot; resize 1920, ENTER → claim → redirect to `/free/walk` →
  back to `/free` → certified by own-restore (name in flow, clone,
  settle, values typed complete, agree hidden, hover lift) + screenshots;
  reload at 390 → certified restore + screenshot; 635×349 certified +
  wheel ENTER reachability (best-effort); second fresh profile, same
  alias → TAKEN (name `text-shadow` must be `none`, clone present) +
  screenshot. Record cert number issued, console errors, overflow at each
  width, and whether the typing-state foot fits at desktop.
- **Acceptance items NOT yet proven (the probe's job):** name judged
  against SN-2922 at 1920 AND 390; panels obsidian with a glow in their
  own color, mail ID first-class; NO gray text anywhere (grep + look —
  his eye overrules any audit); fresh-alias walk end-to-end; console
  clean, zero pageErrors, zero overflow at 1920 and 390; read as a
  reader — the certificate feels super special. **Do not claim done
  without this probe.**

## §10 Self-Check Law — three checks + seven questions (in writing)
**Check 1 — build invariants (run twice, 18:59Z and 19:10Z):** base SHAs
asserted at every chain link; tip worker reproduced byte-exact before
changing anything; harvest anchors asserted unique; geometry rules
asserted byte-identical; `vm.Script` syntax on all inline blocks (after
the fix); node driver PASS; worker read-back MATCH; live routes MATCH.
**Check 2 — independent static verification (after the fix):** §6 audit
from live served bytes (not from build memory) — sentence, 9 paras,
painters, obsidian, zero cut tokens, IIFE closers, all script blocks
compile; §7 laws diff — zero new real fails.
**Check 3 — live staged verification:** §5 — the exact bytes on the
staging worker, re-fetched and sha-matched through two independent
routes (build `_sim.http_get` + curl stdout pipe). What check 3 does
NOT include (honestly): the browser eye. That is §9, owed.

**The seven questions:**
1. **Most intelligent?** Yes — harvest the finished current treatment
   byte-for-byte instead of rebuilding; fix the one-character defect at
   its root (build + guard) instead of patching the staged bytes by hand;
   prove from served bytes instead of claiming from build memory.
2. **Most logical?** Yes — every step follows from evidence in order:
   source named first, diff measured, harvest applied, defect found by
   an independent audit, fixed in the build, re-staged, re-audited from
   live bytes. No leap: nothing is claimed that a tool result does not show.
3. **Most sensible?** Yes — a wise operator would rather hear "the page
   was broken, I found it, I fixed it, the eye still owes" than receive
   a clean report built on a skipped check. Stopping browser retries
   after four identical failures (per the standing TOOLS.md rule) instead
   of burning the seat is sensible.
4. **Full scope?** Yes — the whole page as he will see it: source,
   diff, harvest, defect, staging, laws, aliases, probe owed, follow-ons
   named (membership sentence, H6 taken message), test-cert cleanup
   untouched (his hand), live pricing untouched.
5. **Consequences?** First order: `/free` staging now serves the current
   certificate with working JS. Second order: the checker seat can run
   the real walk; Shawn's eye is the final gate before anything is shown
   to him. Who it touches: only the staging worker — no live page, no
   citizen data, no alias burned.
6. **Pros and cons?** Pros: current treatment staged + defect caught
   before any eye saw it; build hardened (no-skip syntax check,
   byte-identity IIFE assert); full static proof from served bytes.
   Cons (stated honestly): the live eye probe is owed — computed styles,
   overflow, console, and the "feels super special" judgment are
   unproven; the two SIZE machine flags and the transparent WARNs await
   the eye; geometry funding for the sentence is undecided until the
   probe measures the foot. Strongest case against my preference (ship
   the report as done): the static proof is strong, but Shawn's eye is
   the final gate by law — calling this done without it would repeat the
   exact failure the laws were written for.
7. **Best possible choice?** Yes — against the ultimate objective (the
   `/free` page shows the current certificate, proven, with nothing
   hidden): stage the fixed treatment, prove everything provable
   without a browser, name the unproven part plainly, and hand the
   checker seat a ready probe + a reserved alias. That is the best
   choice available in this VM state.

## §11 What passed / did not pass / is owed
**PASSED:** base verification · harvest diff-proven against the named
source · build + stage (fixed) · node driver · live staged bytes
sha-matched · static audit (sentence, reader, painters, obsidian, zero
gray tokens, all scripts compile) · design laws (zero new real fails) ·
pricing v78 untouched · walk unchanged · zero aliases burned.
**DID NOT PASS / FOUND AND FIXED:** the first staging shipped a JS
syntax error (reader IIFE `}();`); fixed in the build, re-staged,
re-proven from served bytes. The build's temp-file syntax check silently
skipped during the EPERM flake — replaced with a no-skip stdin check.
**OWED:** (1) the live browser probe at 1920 + 390 (+ 635 best-effort)
with fresh alias `certcurrent`, via the cloud browser route — the
acceptance items in §9; (2) the checker's cold verification of this
report; (3) geometry funding for the sentence, only if the probe proves
overflow; (4) membership sentence + H6 green taken message as named
follow-ons (own geometry funding); (5) Shawn's-hand test-cert cleanup
(737–746, 753, 755, 781/782); (6) Shawn's eye, phone-first, before
anything is shown to him as done.

## §12 Filing receipts
- Branch: `pricing/certificate-current-20261117` (NEW, from tip `eafbac16`)
- Commit: `52ae64d2c24b740be53530bc64895a6f053288a9`
  (tree `eef5c23c973a131e007fb20f5a71d7256d9c9dcd`, parent `eafbac16`)
- Files filed (8 blobs, all read-back MATCH by sha256):
  `MAKER-REPORT.md` (blob `1fbd6c0b…`, 21,606 B — this version, before
  receipts were added; the receipts update follows as a second commit) ·
  `build-certificate.py` (blob `c9ad618f…`) ·
  `probe-certificate.py` (blob `94c7246e…`) ·
  `laws-check-new.py` (blob `8d026c81…`) · `audit-static.py` (blob
  `34863e3f…`) · `audit-static2.py` (blob `4d9b491c…`) ·
  `fetch-new.py` (blob `cdb49c7f…`) · `fixed-entry.html` (blob
  `5cc7f40e…`, 332,182 B, sha256
  `1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3` —
  re-derived in memory, never read from disk).
- PR: **#3419**, https://github.com/SoulSchoolAcademy/NayaPOWER/pull/3419
  — open, UNMERGED (base `main`).
- Staged: `https://naya-pricing-free-staging.nayapower.workers.dev/free`
  (entry sha `1e1bb489…`, worker sha
  `f4cc645f218b8b2a81f4daff7fcbb0ef604d8ac82bd867c38875dab0e6f44e73`).
- Live `naya-model-pricing` untouched; nothing merged.
- Base-tip correction: the branch tip at filing time was `eafbac16`
  (a receipts-only commit on top of pricing-fix `e6bf9a87`), not
  `e6bf9a87` as an earlier note said. Verified live from the ref and
  the branch history before filing.
