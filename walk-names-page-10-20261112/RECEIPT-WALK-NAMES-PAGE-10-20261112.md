# RECEIPT — WALK NAMES PAGE 10/10 (presentation round)

**Round:** walk/names-page-10-20261112
**Maker:** Walk Names Page maker seat. **Captain:** Naya Nitro Narzan (coordinator).
**Status:** BUILT + LOCALLY PROVEN 99/99 — **DEPLOY STOPPED** (Q10 probe not run).
Honest score: **7/10 round, 10/10 build locally** — below 9, no checker dispatched.

- Brief: `~/workspace/team-nitro/BRIEF-WALK-NAMES-PAGE-10-20261112.md`
- Branch: `walk/names-page-10-20261112` (from main tip `091961ba4149628191d143c5eccd2c0e5251109c`)
- Branch head at filing (before this receipt's own commit): `20730b3f72738ac28221b72135b16df03eed109f`
  (this receipt was filed as the next commit; the final head is in the
  coordinator handoff, not in this file — the head above is the last commit
  whose blobs are all verified below.)
- Base file: `walk-questions-10-20261112/walk-beginning-fixed.html` — v22 base
  sha `227a667e…` (3,363,931 B, re-measured + served-bytes verified 02:36Z)
- New walk file: **3,365,275 B, sha256 `a3510446170380e48a99803e6b6617a01eee99b263ce1d34fd0cf0d313c83d94`**
- Build script: `build-beginning-staging-worker.py` — 32,582 B, walk-sha assert `a3510446`
- Generated worker (NOT DEPLOYED): **4,344,625 B, sha256 `1b2ff1e27846ab2a7d7f524a2f77066c8cefeb409af26d6ce43df2b2bcd21b60`**,
  embedded walk byte-identical to the filed walk, `recordJoin` 3×
- Staged link: https://naya-walk-beginning-staging.nayapower.workers.dev/
  — **still serves v22** (deployment `2dcc6ecbf9fa4b93974ff8d635b6508c`,
  `/welcome` 3,363,931 B sha `227a667e…`, curl-verified 02:36Z). **No deployment
  id exists for this build — no Cloudflare PUT was made.** Deploy waits for
  the captain to coordinate v23 with the Q10 maker after the Q10 probe runs.
- Record: `RECORD-WALK-NAMES-PAGE-10-20261112.md` in this dir (25,334 B)
- Scorecard: `SCORECARD-WALK-NAMES-PAGE-10-20261112.md` in this dir (7,522 B)
- Probe: `names-probe.py` (15,762 B) + `names-results.json` (17,316 B) —
  **99/99 PASS, 0 FAIL** on the final bytes (Playwright Firefox, 1440/390/360)
- Screenshots: `names-probe-shots/` (15 PNGs) in this dir, not filed to the branch

## Filed blobs (branch `walk/names-page-10-20261112`, all read-back match=True)

- `walk-questions-10-20261112/walk-beginning-fixed.html` — blob `b1eae0802596f11d2dbfae537d86b92fee246162`, 3,365,275 B
- `walk-questions-10-20261112/build-beginning-staging-worker.py` — blob `387593ff5faeaccbb471f08d01a15f34a34d7fe6`, 32,582 B
- `walk-questions-10-20261112/walk-beginning-staging-worker.js` — blob `8ef445fdbd9802469db0c05f6a7f3f237b1ff0c6`, 4,344,625 B
- `walk-names-page-10-20261112/RECORD-WALK-NAMES-PAGE-10-20261112.md` — blob `3a5dd02ef9c0179325a91437757bb9129160a414`, 25,334 B
- `walk-names-page-10-20261112/SCORECARD-WALK-NAMES-PAGE-10-20261112.md` — blob `695e9ea95a109e2e11dc5dea2d939dafce063c8d`, 7,522 B
- `walk-names-page-10-20261112/names-probe.py` — blob `d2b28d9cd90e002686e769bcacc5cc34a36439f0`, 15,762 B
- `walk-names-page-10-20261112/names-results.json` — blob `875f6f12340ac4a988d9ff8e0f47dd6a57bad5ad`, 17,316 B

## The five 19:59Z rulings (short)

1. Hover light — PROVEN rendered, 3/3 cards, all widths. 2. URL inputs live —
   PROVEN by typing. 3. No gray — PROVEN by getComputedStyle sweep, 0 bad
   nodes. 4. Eye modals — PROVEN by clicking, 3/3. 5. Building links click
   through — **UNRUN on this build** (needs the staged worker; deploy stopped).

## Test aliases

None — the probe ran locally with a throwaway context; no claim, no completion,
no Box/project/page created anywhere. Nothing to clean up.

## Bounds kept

- Staged walk only (and not even staged — deploy stopped). No live deploy, no merge, no PR, no mail sends. Nothing deleted by this round.
