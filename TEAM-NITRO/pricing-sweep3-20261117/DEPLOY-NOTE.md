# DEPLOY NOTE — Free Entry (/free), Inspector Sweep #3 + Certificate Current

**For:** the deploy seat (or Shawn's hand) — **NOT this round's to take.**
**Live step (one-string swap of `FREE_ENTRY_URL` + button href) is Shawn's hand,
never this round's. Nothing here merges or goes live on this round's authority.**

## What this filing contains

Branch `pricing/sweep3-20261117` (from `pricing-f4-free-entry-20261116` head
`eafbac16`), PR open UNMERGED. The fixed entry file carries BOTH the 14
inspector fixes AND the certificate-current harvest:

| File | Size | sha256 |
|---|---|---|
| `fixed-entry.html` | 337,779 B | `9ac3b4f5f8189bf353af34f186ea9d14133e4024e1312be879a09a87d5f01ad3` |
| `manifest.webmanifest` | 585 B | `4e7958edfd722fbd8d3e842a7dd1076edf9e6bdfaef6a10f6be3dd6ad588a155` |
| `icons/icon-512.png` | 229,337 B | `770cfa135f5e5dd983d7c1d7cd0b1e3e397e3ff482adc0465d644c15c4d8acbd` |
| `icons/icon-192.png` | 48,626 B | `32903142c8e364e7ec01c32ced0bb47d2fe9bf4c3552b3ad751074d76005eb29` |
| `icons/apple-touch-icon.png` | 43,852 B | `0dfac98028743b9cdc398a6adde8efccdbd44acdcb3553980e01001e55fb2020` |

## Deploy steps (staging worker `naya-pricing-free-staging`)

1. **Swap the entry bytes** — the worker serves `fixed-entry.html` at `/free`.
   Verify by curl: `/free` returns 337,779 B and sha256 `9ac3b4f5…`.
2. **Swap the manifest bytes** — the worker serves `manifest.webmanifest`.
   Verify: `theme_color` is `#8e24aa`.
3. **Add icon routes to the worker** — the worker currently has NO icon routes
   (hence the 404s). Add `/icon-192.png`, `/icon-512.png`,
   `/apple-touch-icon.png` serving the filed PNGs (the manifest references
   `icon-192.png` / `icon-512.png` by relative name; the install card falls
   back to `icons/apple-touch-icon.png`). Verify each returns 200 with the
   filed bytes (sha match).
4. **Re-curl and re-open** — `/free` at 1920 AND 390, plus `/api/claim?alias=…`
   GET (read-only). Confirm the staged bytes are the filed bytes (sha match),
   the icons load, and the install card shows the crystal N.
5. **Do NOT touch** `naya-model-pricing` (live pricing) or any live URL. The
   live step (one-string `FREE_ENTRY_URL` swap + button href) is Shawn's tap.

## Before the captain's eye

- The independent checker (owed — see `CHECKER-VERDICT.md` §6) must run its
  own walk at 1920 + 390, its own checker run, its own live `/api/claim` GET
  (never the POST), and the certificate-harvest behavioural proofs (trophy
  render, reader open/Next/Close/Escape, typing values, fit WITH the
  agreement line in).
- The captain's eye walks the staged fix phone-first. Only then does it go
  to Shawn whole — done + not-done together.

## Known state at filing

- Privacy line: reachable by scrolling the face at all measured widths, but
  below the fold on phone in the typed state (pre-harvest numbers in the maker
  report §3; the agreement line adds height — re-measure after deploy).
- The harvest's behavioural proofs are owed (VM browsers died before they
  could run — see maker report §11).
- Fix 7 (alias reservation) awaits Shawn's decision; Fix 14's corrections are
  recorded in `RECORD-CORRECTIONS.md`.
