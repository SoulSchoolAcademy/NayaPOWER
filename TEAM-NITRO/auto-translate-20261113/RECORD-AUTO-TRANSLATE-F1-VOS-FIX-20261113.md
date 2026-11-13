# RECORD — AUTO-TRANSLATE F1 MICRO-FIX: TES → VOS (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Owner seat: Wrena (BUILD) · Maker: Wrena (BUILD), one scorecard cycle

Base: branch `personal/auto-translate-card-labels-fix-20261113`, tip
`2e348bb19e89ce6d4b1a3bc20130c00159d252e0` (tree
`a3524fedc627ef4a8c726d392d5794fa09558467`) — 1,652,796 B, sha256
`93f4302a5866a007b290ac3b144bda62c373ee16a7bfe63222e485ffc29a7b3b`.
Fix bytes (worktree):
`/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`
— 1,652,796 B, sha256
`9ee0d0f72b4f33a06d79b5dd5444ab3c0ed7c030b05fa86e23c2d4d811dfa334`.
Work dir: `~/workspace/team-nitro/auto-translate-20261113/`.

Bullseye (one line): the French voice is vous everywhere — one wrong
word fixed, so a French citizen reading a naya feed card sees
"VOS MOTS", never "TES MOTS".

## §0 — The five gates (applied to this fix)

1. **Is it right?** Yes. A French citizen who picks French should read
   vous everywhere; one tu-form word is a visible inconsistency inside
   the card-labels round's own new keys (the sibling key reads
   `VOS MOTS, MOT POUR MOT`).
2. **Is it what they truly need?** Yes — the page's own words, in the
   voice the round itself settled (record §3: fr vous).
3. **Is it mine to do?** Yes. Staged only, on a new branch from the
   card-labels tip, one commit. No live touch, no merge, no PR. No
   change to any other dictionary value, no change to the Spanish or
   German values, no marking, layout, or code change.
4. **Is now the time?** Yes — the corrections round is held behind
   auto-translate landing, and this one word is the only thing standing
   between the card-labels fix and its double-check. The base did not
   move mid-round (card-labels tip still `2e348bb1`; staged base
   re-fetched live at verify time, sha `93f4302a…`).
5. **Can I prove it?** Yes — §3: grep zero for `TES MOTS` in the
   dictionary and in the staged bytes, a tu-form scan of all 56 new
   French keys at zero, and a diff of exactly one line against the
   card-labels staged bytes. The one exception is named in §3, not
   hidden: the rendered French card was not browser-proven by this
   seat (VM browsers dead); re-proof is owed by the captain's
   cloud-browser eye check on the staged link.

## §1 — The gap, first-hand (what the checker found)

The checker's audit (`CHECKER-VERDICT-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md`
§7, finding F1) proved the new card key
`YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA` carries the French value
`TES MOTS — MIS EN FORME AVEC SOIN PAR NAYA`, and proved it is the
only tu-form among the 56 new keys — which also disproves the
card-labels record §4 claim that its tu-form scan found "the only one"
(it found the sibling key `YOUR WORDS, WORD FOR WORD`, not this one).
The render site is confirmed in the staged bytes: ibFeedCard naya
branch, `<span class="ib-naya-fidelity" data-mw-tr="set"
data-mw-en="YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA">` + `mwTr(...)`
— it renders on naya-type feed cards in French.

I re-proved the gap first-hand before editing: `TES MOTS` occurs
exactly once in the built file (line 20413, the `MW_I18N` line) and
exactly once in `dict-final.json` (line 515). Spanish
(`TUS PALABRAS`, tú voice) and German (`DEINE WORTE`, du voice) are
correct and do not change.

## §2 — The fix (one value, two places, plus the record correction)

- **`dict-final.json` line 515:** `TES MOTS — MIS EN FORME AVEC SOIN
  PAR NAYA` → `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA`.
  sha `68d6d3cd…` → `5e3c395c29cf9921f0227bed61220ddb0097a2d7432192b27621e647459628bd`.
- **Built file, embedded `MW_I18N`, line 20413:** the same one value.
  sha `93f4302a…` → `9ee0d0f7…`, size unchanged at 1,652,796 B
  (TES→VOS is three characters for three).
- **Card-labels record §4 corrected** (this round's second deliverable):
  the claim "a tu-form scan of all fr values found this as the only
  one" now reads what actually happened — the scan found the sibling
  key and was read as the only one; it missed this key, which the
  checker's audit found as F1. The corrected record is filed on this
  round's branch alongside the fix, so the filed record tells the
  truth. No other line of that record was touched.

No rebuild: the file was edited in place, one dictionary value, never
a fresh build — per the brief. No other dictionary value changed; no
marking, layout, or code changed.

**EPERM flake, this round (named, with the workaround):** python and
shell writes were blocked per-path per-moment while the edits were
attempted — `sed -i` failed on its temp file, `cp` to /tmp failed, the
python edit script failed 10 consecutive write attempts over ~27 s,
and a shell redirect left a 0-byte temp file (removed, never trusted).
The original files stayed intact through every failure (shas
re-checked after each). Both edits were applied through the runtime
file tool, which bypasses the flake — `dict-final.json` first, then
the built file — and verified by sha + grep immediately after. No
evidence was faked: every number in §3 was re-measured after the
edits landed.

## §3 — Proof (all first-hand, on the fix bytes; `verify-f1-vos-fix.py` → `verify-f1-vos-fix.json`)

### 3.1 Grep — zero left
- `TES MOTS` in the built file: **0** (was 1). In `dict-final.json`:
  **0** (was 1). In the embedded `MW_I18N`: **0**.
- `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA`: **1** in the file,
  **1** in the dictionary.
- Spanish untouched: `TUS PALABRAS` still **2** occurrences in the
  file. German untouched: `DEINE WORTE` still **2**.
- Fidelity render site still present (the `ib-naya-fidelity` span +
  `mwTr(...)`), so the fixed value has somewhere to render.

### 3.2 Tu-form scan — zero across the 56 new French keys
Re-run over all 56 new keys, in `dict-final.json` **and** in the
embedded `MW_I18N`, with the checker's exact regex
(`\b(tu|tes|ton|ta|tes mots)\b`) and a wider net
(`\b(tu|tes|ton|ta|toi|t'es|t'as)\b`): **0 tu-forms in both**.
Dictionary still 266 keys/language, all values strings, embedded ==
`dict-final.json` exactly.

Full-French scan for context (not charged here): the only tu-form left
in any French value is the pre-existing base-210 `YOUR WORLD` →
`TON MONDE` — prior-round debt, named by the checker, not this round.
(`YOU · STANDING` → `TOI · LISTÉ` and `Post my Naya note` →
`Publie ma Note Naya` are likewise base-210 and outside the 56.)

### 3.3 Diff vs card-labels staged bytes — exactly one line
Live fetch of the card-labels staged bytes (re-verified sha
`93f4302a…`, 1,652,796 B) against the local fix bytes: **exactly 1
hunk, 2 changed lines (1 removed + 1 added)** — line 20413, the
`MW_I18N` line. The two lines are 58,349 characters each and differ
at exactly 2 character positions: `TE` → `VO`. Nothing else in the
1.6 MB file moved. This is the whole no-regression battery at byte
level: the Settings panel, tabs, rail, + menu, bottom bar, Translate
tap, pill, and persistence code are byte-identical to the
checker-verified card-labels bytes, which passed the full browser
regression in that round.

Markers unchanged: `data-mw-tr` **196**, `data-mw-ph` **7**,
`data-mw-aria` **6** — the card-labels counts exactly.

### 3.4 Syntax — 36/36 blocks parse
Node parse check on all 36 script blocks of the edited file: **0 bad**.
(Checked in-memory via `new Function` parse because /tmp file writes
were EPERM-blocked at that moment; the change is 2 characters inside
a double-quoted string literal, and the embedded `MW_I18N` also
parses as JSON — §3.2.)

### 3.5 The one gap — rendered French card NOT browser-proven by this seat (named, not hidden)
One Playwright Firefox launch attempt, first-hand: `Failed to launch
the browser process` (pid 381836, process died on launch) — the
documented TOOLS.md flake (browsers dead since ~17:32Z 2026-11-12;
the checker hit the same failures ×3 Firefox SIGSEGV, Chromium
SIGTRAP, at 20:05Z). I did **not** run a browser proof and I claim
none. What stands instead: the grep zero (§3.1), the tu-form scan
(§3.2), the one-line diff (§3.3), and the fact that the render site
and mechanism are live-proven from the card-labels round (the French
ibFeedCard render was browser-proven there; this round changes one
dictionary value inside it). **Re-proof owed by the captain's
cloud-browser eye check on the staged link:** switch the picker to
French, open the feed, find a naya-type feed card — the fidelity
microcopy must read `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA`
(screenshot at 390). The checker/captain should close it before
calling the round done-done.

Also still open from the card-labels round, unchanged by this round:
§5.4 rendered noteCard browser proof (needs a live browser on the
staged link, Supabase live). Named, not charged here.

### 3.6 Self-check catch — the verify script's own assertion was wrong
The first verify run reported `changed_line_tes_to_vos_only: false`.
The file was right; my assertion was wrong: it required
`VOS MOTS` to occur once on the changed line, but the line carries
`VOS MOTS` twice — the sibling key `VOS MOTS, MOT POUR MOT` (fixed
in the card-labels round) plus this fix. Corrected the assertion
(sibling 1 + fix 1 = 2) and re-ran: all green. Lesson filed in the
scorecard: count the siblings before asserting a count.

## §4 — DONE definition (fix brief §Done first, checked)

- Grep count of `TES MOTS` in French dictionary values = 0. **Done**
  (§3.1 — dict and embedded both 0).
- Grep count of `TES MOTS` in the staged bytes = 0. **Done on local
  bytes; staged re-verification in §5.**
- Rendered French naya-type feed card reads
  `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA` (screenshot at 390).
  **Open — §3.5** (captain's cloud-browser eye check).
- Tu-form scan of all 56 new French keys = 0 tu-forms. **Done**
  (§3.2, two regexes, dict + embedded).
- Zero overflow at 390/1440/360, zero console errors. **Inherited by
  byte identity** — the only changed bytes are 2 characters inside a
  dictionary string (§3.3); overflow and console behaviour were
  proven on the identical card-labels bytes and nothing that renders
  them moved. **Re-measured by the checker/captain on the staged
  link with the French render (§3.5).**
- Record §4 claim corrected to what actually happened. **Done** (§2).
- Stage via proof-host (new ref for the new branch), verify staged ==
  local by sha, report staged link + sha + branch + commit. **§5.**

## §5 — Staging + filing

- **Branch:** `personal/auto-translate-f1-vos-fix-20261113` (new,
  from the card-labels tip).
- **Parent:** `2e348bb19e89ce6d4b1a3bc20130c00159d252e0` (card-labels
  tip), parent tree
  `a3524fedc627ef4a8c726d392d5794fa09558467` (fetched live via
  `gh-direct.py` GET on the commit).
- **One commit** via `file-f1-vos-fix.py` (adapted from
  `file-card-labels-fix.py`: one blob per file, base64 generated in
  memory via process substitution — never staged to disk — then one
  tree, one commit, one ref-create). Contents: the built page + this
  round's brief + the card-labels checker verdict (the evidence) +
  the corrected card-labels record + this record + the scorecard +
  `dict-final.json` (fixed) + `verify-f1-vos-fix.py` +
  `verify-f1-vos-fix.json` + `file-f1-vos-fix.py` +
  the file/manifest/commit-message files.
- **Staged link:**
  https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-f1-vos-fix-20261113&cb=<FINAL COMMIT SHA — see the maker's final report>
- **Staged == local by sha:** verified with the proof-host curl
  pattern after filing; the staged sha must equal
  `9ee0d0f72b4f33a06d79b5dd5444ab3c0ed7c030b05fa86e23c2d4d811dfa334`
  (1,652,796 B). Staged only. No live touch, no merge, no PR.

## §6 — Three self-checks (each found NEW things)

1. **The edit itself** — NEW findings: the EPERM flake blocked every
   python/shell write route (sed, cp, redirect, 10 python retries)
   and left 0-byte temp files that had to be removed, never trusted;
   the runtime file tool bypassed it. The original files survived
   every failed attempt (shas re-checked). The fix is 2 characters,
   not 3 — `TE` → `VO`, the `S MOTS` shared.
2. **The byte proof** — NEW findings: the verify script's own
   `VOS MOTS` count assertion was wrong (sibling key on the same
   line, §3.6); the full-French scan leaves exactly one pre-existing
   tu-form (`YOUR WORLD` → `TON MONDE`, base-210 debt); the diff is
   exactly one 58,349-character line.
3. **The proof itself** — re-read the diff character by character
   (2 differing positions), re-ran the verify after fixing the
   assertion, confirmed the base did not move mid-round (staged base
   re-fetched live, sha `93f4302a…`). NEW finding: a one-line diff
   is the strongest no-regression proof this round can give without
   a browser — it says every surface the card-labels round proved
   is byte-identical.

## §7 — Seven pre-merge answers (in writing)

1. **Three self-checks done?** Yes — §6, each finding new things.
2. **Honest 9+?** Score 9 — see
   `SCORECARD-AUTO-TRANSLATE-F1-VOS-FIX-20261113.md`.
   Deduction: one point, for the rendered French card not being
   browser-proven by this seat (§3.5). Everything else the bullseye
   names is measured true.
3. **Blast radius named?** Staged Personal page only, on a new branch
   from the card-labels tip. The Hub shell, the walk worker and live
   are untouched. No main change. No mail.
4. **Checks green?** Grep zero + tu-form scan zero + one-line diff +
   markers unchanged + syntax 36/36, all green on the final file;
   every exception named (§3.5, §4).
5. **Five gates?** Yes, with evidence (§0).
6. **Real proof?** Live bytes, shas, line numbers, counts, and a
   live-fetched staged-base diff, all read first-hand in this round
   (§1–§3, §5).
7. **No silent known defects?** None silent — every gap is named in
   this record (§3.5 rendered French card, §4 overflow/console
   inherited-by-identity, §3.2 the one pre-existing base-210 tu-form).

## §8 — Follow-ons (named, not silent)

- **Rendered French card re-proof on the staged link** (the §3.5
  open item): switch to French, open the feed, read a naya-type
  card's fidelity microcopy at 390. Captain's cloud-browser eye
  check to close before done-done.
- **Rendered noteCard re-proof on the staged link** (card-labels
  §5.4, still open): open Notes in es, read the three sample cards.
- **Base-210 French tu-forms** (checker F1 addendum, not this round):
  `YOUR WORLD` → `TON MONDE`, `YOU · STANDING` → `TOI · LISTÉ`,
  `Post my Naya note` → `Publie ma Note Naya` — prior-round debt,
  a follow-on round if the captain wants the whole dictionary vous.
- **The EPERM lesson for the hive:** when python/shell writes fail
  per-path per-moment, the runtime file tool still lands edits —
  and a 0-byte file left by a failed write is flake damage, never an
  empty file to trust. The verify-assertion lesson (§3.6): count the
  siblings before asserting a count.
