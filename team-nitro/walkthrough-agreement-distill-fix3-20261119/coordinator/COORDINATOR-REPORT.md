# COORDINATOR REPORT — Agreement Distill Fix-3

**Round:** `walkthrough/agreement-distill-fix3-20261119` (coordinator)
**Date:** 2026-11-20, ~00:24–01:10 MST
**Base:** branch `walkthrough/agreement-distill-fix-20261119`, tip `e0681545`
**Work files:** `~/workspace/team-nitro/walkthrough-agreement-distill-fix3-20261119/coordinator/work/`
— `coord-verify.js` (my own 34-assertion harness), `coord-control-fix2.js` +
`run-fix2-localbase.js` (fix-2 control against verified local base), base blobs
(`unfold/welcome/walk/identity-base.html`, fresh blob-API reads)

## Verdict: FILED, and verified cold — the three F9 fails are fixed

The maker filed the branch, the worker was rebuilt, and staging serves the
fix-3 bytes. I verified the filing identity, the tree diff, the filed bytes
by fresh blob-API reads, the laws with the REAL checker, and the three fixes
with my own harness cases (not the maker's). Two of my own assertions failed
and both are my mis-specifications, not page defects (§4). The independent
checker (parallel lane) returned GOES BACK on one report defect only — the
stale walk sha — and the maker corrected exactly that before filing; the
re-checker PASSED the correction. The code itself passed every independent
check.

## 1. Filing identity — verified cold by me

- **Branch:** `walkthrough/agreement-distill-fix3-20261119`
- **Tip:** `f3d4ab3a185c31fd28c8d392f761706309e632b5` (GET branch — tip == commit
  sha; commit message is the §12 correction; tree `65c1f008…`, parent
  `5d81171938c3ebff2f796df16935a8b35159f37a`)
- **Filing commit:** `5d81171938c3ebff2f796df16935a8b35159f37a` (parent `e0681545…`)

| File | Bytes | sha256 | Git blob sha |
|---|---|---|---|
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 142,120 | `50876fff8caa79ee…` | `f7f919db59dbaafb…` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,929,575 | `3874b7ebcc6b95e…` | `4830958834321ee…` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html` | 4,363,264 | `ef98226767ddbb50…` | `5f914291abb84d6e…` |
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 402,647 | `51776174b59cee4a…` | `2d1266553ecde92a…` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,459,261 | `cc46798578df4c9b…` | `da8f3cc8fe4784e8…` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 93,731 | `f6107678a0e9eef…` | `91ebfe7f4d46aac6…` |

How I verified (each step mine, not the maker's): disk files sha256-matched the
claims; `git hash-object` on the disk files matched the tree's blob shas
exactly; the tip tree (recursive, 12,289 entries) lists the same blob shas
and sizes; FRESH blob-API reads of the filed walk + identity blobs decoded
to 4,363,264 B `ef982267…` and 402,647 B `51776174…` exactly. The old 85 B
shortfall question is settled for the new worker: the fresh read decoded the
full 8,459,261 B (I did not re-read the 8.4 MB worker blob; the tree blob
sha + disk sha + size agree, and the staging curl below confirms the served
bytes).

**Diff replay (base tree `e0681545` → tip tree):** 0 removed; changed = exactly
the 6 files above (+ 3 directory tree pointers); added = the fix-3 round dir
only (brief + maker report + 12 work files). Nothing else touched.

**Staging serves fix-3 (curl, browser UA, my own read):** `/welcome`
4,363,264 B `ef982267…`, `/identity.html` 402,647 B `51776174…`,
`doorContinue` 2× in the served walk, `passedName && passedAlias` 1× in the
served identity. Deployed by the parallel worker from the filed bytes (not
from unfiled bytes); no live/production deploy.

## 2. What I verified myself vs what the maker claims

**Mine (cold, independent):**
- Filing identity, tree diff, fresh blob reads, staging curl — §1.
- Base blobs re-read fresh from the blob API: unfold 141,781 `5fe1a3ec…`,
  welcome 1,913,241 `c3c750b7…`, walk 4,361,369 `0f05b3f9…`, identity
  401,040 `3279dc35…` — all match the fix-2 checker §1 exactly.
- **Laws — REAL `check-design-laws.py` run by me on disk files, base vs
  fixed:** unfold 1/2 → 1/2, welcome 83/4 → 83/4, walk 128/8 → 128/8,
  identity 11/2 → 11/2 — **delta 0/0 on all four files**.
- **My own harness (`coord-verify.js`, 34 assertions, my own scenarios):**
  32 pass / 2 fail — both fails are my mis-specifications, §4.
  - C1 paired identity: input `="distill"`, hero text + data-text
    `="Distill Eye Walk"`, unhidden at boot AND after 2 s.
  - C2 name-only: input `""`, hero blank + hidden + data-text null.
  - C3 door paired: only `step-door` visible at boot, still only
    `step-door` after 5 s, continue visible, tap → `step-1`, door gone.
  - C4 no-alias: continue hidden, cert link present.
  - C6 control on BASE bytes: hero blank+hidden (the bug), walk
    auto-advances within 5 s (the bug) — the harness sees the bugs.
- **Fix-2 control (`coord-control-fix2.js`, local-base reproduction):**
  fix-2 bytes reproduced exactly (identity 402,166 B `d0f26529…`, walk
  4,362,221 B `854a8f60…`). Fix-2 paired: input `="distill"`, hero
  blank+hidden; fix-3 same harness: input `="distill"`, hero painted.
- **Byte checks (my own greps on the disk files):** I-FIX3 block at identity
  line 2229 (paired guard + `paintHeroName(passedName)`); `proceed()` guard
  is the first statement inside `var proceed = function(){…}` (walk line
  2586); claim-gate timer guarded (line 2607); `doorContinue` button 1× in
  markup (`.p3-enter`, after the cert link); cert link still 1×;
  `#letterAll`/`#fpLinkLetterAll` NOT restored (0× element, 1× pre-existing
  JS var) — captain's call followed.

**Taken from the maker (verified where I could, stated where I could not):**
- Maker's 139/139 state machine and 33/33 fix-2 repro — I did not re-run
  the full 139 (my 34 + the independent checker's 152 + re-checker's 139
  cover the same ground; see §3). Maker's §11 landing narrative (emit,
  rebuild byte-identical twice, backups) — the filed result matches it, and
  I verified the outcome, not each step.
- Render: NOT proven by any seat (VM browsers dead). The eye is the
  render proof — §5.

## 3. The independent checker + re-checker (parallel lane — read by me)

- **Checker** (`checker/CHECKER-REPORT.md`, 27,779 B): **GOES BACK on one
  report defect only** — the maker's claimed walk sha `b068d1da…` did not
  reproduce (reproducible: 4,363,264 B `ef982267…`, proven three ways).
  Everything behavioral PASSED: its own 152-assertion state machine
  (152/2 — the 2 fails are the sha claim), its own transform reproducing
  the same walk sha, the fetch-verdict causal proof (fix-2 advances at
  104 ms via verdict vs 4,094 ms via timer; fix-3 holds 6 s on both),
  parallel-worker additions verified line by line, laws 0/0 with the REAL
  checker run by pipe.
- **Re-checker** (`checker/CHECKER-REPORT-RECHECK.md`, 16,951 B): **PASS**
  — the correction (maker §10, walk 4,363,264 `ef982267…`) verified by its
  own fresh re-run (139/139), landing honestly blocked at that time.
- The maker corrected §2/§7 exactly as ordered BEFORE filing, so the filed
  branch carries the corrected values. The checker's GOES BACK item is
  closed by the correction + the filing — there is no open checker item.
- Both checker reports are filed in the PARALLEL commit `27689bf6`
  (tree `c200836e…`) but NOT in the tip tree: the force-update to
  `5d811719` dropped the `checker/` dir (the only file differing between
  the two trees is `MAKER-REPORT.md`; the parallel tree additionally
  carries `checker/` + 5 work files). The reports survive on disk and in
  `27689bf6` (reachable by sha). Flagged for the captain: if the branch
  should carry the checker reports, they need re-adding in a follow-on
  commit — the tip as it stands holds maker-only proof.

## 4. Two of my assertions failed — both mine, not the page

1. **C5 cert-link tap navigation:** tapping the door's certificate link
   produced no navigation in my harness. Cause: the DOM engine's `click()`
   only dispatches the click event — it never follows an anchor's `href`
   (engine code read: `click: function(){…dispatchEvent…}` and nothing
   more). The link's href is correct (carries name+alias, verified in bytes
   and by the fix-2 checker at runtime), and the door stays visible after
   the tap (no auto-advance). Engine limitation, not a page defect.
2. **C6 base-identity input control:** I asserted base paired input would
   read `""`; it reads `"distill"`. Cause: my control was mis-specified —
   the checker's Fail 1 was demonstrated with the NAME-ONLY url, and on
   base bytes the pre-existing FIX6 load check fills the field from
   `?alias=`. The real observable F9(a) bug is the HERO (blank+hidden on
   fix-2 paired — my control proves it), and fix-3 fixes exactly that.
   Note for the record: the checker's Fail 1 as literally written
   (name-only should pre-fill) is SUPERSEDED by the captain's confirmed
   reconciliation — name-only MUST stay empty, and it does (fix-2 name-only:
   input `""`, hero blank+hidden — correct per reconciliation, verified by
   me on fix-2 bytes).

## 5. What the captain's eye must still prove (pixels — not claimed here)

- The eye walk has RUN in the parallel lane: `eye/` holds desktop +
  phone-390 screenshots (07:50–08:02) and `eye-log2.json` (unfold 1→37,
  identity, door, bridge steps logged) — but NO eye verdict `.md` is filed
  yet. The captain's eye verdict is still owed.
- On staging (which now serves fix-3), phone width first: the completed
  certificate names the reader (F9a); the door waits with both pills
  visible and tappable ("Get your certificate ◆" and "Continue to the
  walk ◆" — the eye judges whether two pills stack well there); the seal
  sits bottom-centre on home, deck, letter, identity, and the welcome
  door (F7); the left edge is clear on every deck board (F1); Naya's
  photo sits top-right, fully visible, on deck and letter (F2/F4); the
  footer reads whole in the first view on every board (F3); board 37's
  picture fills the void (F5a); images fit whole with no bottom crop (F5c);
  the Ambassador button is visible in the first view on board 37's end
  card; typing in the alias field echoes sensibly in the hero (checker's
  §5 observation).
- Phone 390 was NOT tested by any byte seat — the eye's phone leg is the
  first 390 proof for this round. The anthem wiring round still queues
  behind this one (same file, one lane). No merge, no live deploy, no link
  to Shawn until the eye passes it.

## 6. Five gates (coordinator, before reporting)

1. Right — the certificate names the reader and the door waits for the
   reader; nothing is taken from anyone. 2. Truly needed — the eye's three
   F9 fails, worked to zero and verified cold three ways. 3. Mine to do —
   the dispatched coordinator round; no protected gate crossed (no money,
   no credentials, no destructive action, no live deploy, no merge, no
   link to Shawn). 4. Now — inside the live sequence; the maker overran
   the hour and documented why (EPERM landing fight, base-proven assertion
   corrections, concurrent-worker adoption). 5. Prove it — §§1–4 above,
   all re-runnable from `coordinator/work/`.

## 7. Scorecard (coordinator's own)

Why not a 10: the round overran the hour; part of the shipped code arrived
from a parallel worker (verified line by line, not originated by the maker);
the branch tip dropped the filed checker reports in the force-update; the
eye verdict is not yet written though the walk ran. What is a 10: the fix
itself — three fails, three remedies, each proven at runtime by three
independent harnesses (maker 139, checker 152, mine 34 + control), the
filing verified byte-for-byte from fresh reads, laws delta 0/0 with the
real checker, staging serving the fixed bytes.
