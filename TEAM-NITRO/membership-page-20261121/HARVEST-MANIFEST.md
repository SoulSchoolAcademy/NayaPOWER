# HARVEST MANIFEST — Membership page 2026-11-21

Every source: file + branch + blob + bytes + sha. Every adaptation: listed, no silent changes.

## Frame source (byte-for-byte — the One-Build Law)
| Piece | File | Branch | Blob | Bytes | sha256 |
|---|---|---|---|---|---|
| The frame (whole page skeleton: head styles, `.naya-frame` stage, `#deckBody` engine, `#deckControls`, all 7 frame scripts) | `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | `agreement/unfold-20261117` | `1f0b04747e3315be6f1b619c1411e5e14fbdc1bb` | 142,532 | `a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98` |
| Cover model (`.sa-cover` board: 11 rules + HTML pattern) | `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html` | `personal/complete-round4-20261120` | `65d2d31433df996fed784048d5c9218259d26744` | 10,503,077 | `0a7ae611f4ac867832f5fc095278db58d8848c7690cc8ed527ffb808b4c96f8c` |

Proof: `verify-byte-diff.js` — head styles identical (45,943 B, sha `cb4de85cbf83`), `.naya-frame` div identical (literal), main open tag identical (sha `c716ad0b3717`), `#deckControls` identical (sha `0379f45b6211`), frame scripts differ in exactly 5 lines (below). Lane copies: `frame-source-agreement.html`, `cover-model-personal.html`, `sa-cover-harvest.css`.

## Course data (DATA ONLY — no markup, layout, or behaviour taken)
| Piece | File | Branch | Blob | Bytes | sha256 |
|---|---|---|---|---|---|
| Course data (`SA_ACADEMY` / `SA_FAC` / `SA_MEMBERSHIPS`, `SA_COURSE_IMG`) | membership-complete source | `membership-complete-20261119` | `4e1e470a68d89b72d51f1ec6840d9e1e351233bf` | 1,490,394 | `00869bc6ec9027760489cd4f16dec890b869093b843d7fe9934e6b537f994f3d` |

Lane copies: `course-data-source.html`, `course-data.json`. Harvested fields per lesson: day/id/title/sub/saying/nutshell (Academy); full layers for FAC (headline/subheadline/saying/nutshellFull/human/child/grandma/naya/step). **Nothing invented:** Academy lessons have no plain/child/grandma/how beats (layers not on file); FAC has no video on file (honest "video on its way" board); Masterclass has no lessons on file (honest empty TOC room); audio beats are honest empty boards ("arrives with the owner's recording").

Cover art (all covers, verbatim): `SA_COURSE_IMG` = login-obsidian.jpg proof-host URL, `cb=7ba628ffb56a3e16721174aa98bd29ef42847953`.

## Colours (deepened per Design Laws §3.1/§13 — the frame file itself documents this adaptation)
Academy `#a06bff` → `#8e24aa` · Masterclass `#3fb8ff` → `#0f52ba` · Fast Action Club `#2fe89e` → `#07925f`.

## Documented word-only adaptations (5 — the ONLY differences from the frame source)
Recorded in `frame-adaptations.json`:
1. wirePlay tip: 'Naya will talk you through this page' → 'Naya will talk you through these courses'
2. wireFrame8 label: 'Listen to the agreement' → 'Listen to the memberships'
3. wireFrame8 button: 'Watch the anthem' → 'Watch the welcome'
4. anthem-note p1: the scattered-life paragraph → 'Three courses, one frame. Pick one — and begin.'
5. anthem-note p2: 'These are the anthem's opening words. The video is on its way.' → 'The welcome video is on its way.'
Header words also adapted (steplabel/title/sub/foot-links, play aria-labels). Internal ids/hooks kept verbatim (`fpAnthemVideoBtn`, `data-anthem-slot`). The 360 "agreement" hits in the built file are all inside harvested asset URLs (`agreement-unfold-20261117/face-1.jpg`, `deck-logo.jpg`) — not visible words. The 15-paragraph agreement speech script in wirePlay is carried verbatim as dead code (wireFrame8 clones `#playBtn`, severing its listener — the frame's own F4 comment proves it); a membership reading is NOT invented.

## New code (the only new code in the file)
- `fpMembership` CSS (beat content styles only; font sizes 17/19/24/20px — 24/20 are the ✦ jewel glyph, not text; no gray).
- `wireMembership` script (runs last; mirrors the frame engine's own patterns: clone-and-replace rewiring like wireFrame8, `stopPropagation` so the frame's delegated handler never double-handles a tap; `memShow` mirrors showFrame9's toggles verbatim because the frame's show functions are IIFE-scoped).

## NOT a source
- The old membership fix-8 page (blob `b13c17104a188e3b53bbbe77483fd4805afc29f2`, 2,373,535 B) — retired by Shawn's order; not built on, its link is not delivered.
- The local repo copy `~/workspace/nayapower-repo` — STALE, never used. All bytes came via the git blob API.
- Main tree searched (16,737 entries, main tip at search time `9ffd3805809f78b1e90779e967de3855492cb449`): zero `TEAM-NITRO/membership*` paths — no membership page home exists in the current system.

## Filed
- Branch `membership/page-20261121` (from main tip `b8bc93273c2413b1aca8f7be7f45a4167c418cb7`), commit `f85df46fae0d4452d39f61550f98187ebabf362d`.
- `TEAM-NITRO/membership-page-20261121/membership-page.html`, blob `46c44481c36d25b0a081833db7552c35cbacd2fa`, 238,066 B, sha256 `1e569e11bfbc98b8206e328ae25512dfe20ff76e54f0282fd6528f0c5e9cdf44` (blob read-back verified).
