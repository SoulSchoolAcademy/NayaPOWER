# Block Catalog — Coverage Report (t0907)

**457 canonical blocks** · model numbers `NAYA-<CAT>-<NNN>` · 19 of 49 interface-inventory items HAVE · **30 GAPs = the build list for the next wave**

Source: `block-catalog.json` (this folder). Models referenced below are checkable there.

## HAVE / GAP table

| # | Item | Status | Evidence / build note |
|---|------|--------|----------------------|
| 1 | nav bar | ✅ HAVE | NAYA-NAV-001 (11-room rail nav), NAYA-NAV-012 (nav) |
| 2 | hero | ❌ GAP | HRO category is empty. Build: full-width hero section block (headline + CTA + visual) |
| 3 | primary button | ✅ HAVE | NAYA-CRD-095 ("The one action · Primary"), NAYA-BTN-001..003 ("01 · Heroes") |
| 4 | secondary button | ✅ HAVE | NAYA-CRD-097 ("The supporting action · Secondary") |
| 5 | danger button | ✅ HAVE | NAYA-CRD-084 ("The irreversible action · Danger", red edge fire) |
| 6 | icon buttons | ✅ HAVE | NAYA-BTN-031..035 ("06 · Icon Buttons — .icon-btn") |
| 7 | cards | ✅ HAVE | 114 CRD records: NAYA-CRD-002/003/004 (board shell, door card, intel board), NAYA-CRD-091 (content card) |
| 8 | badges | ✅ HAVE | NAYA-JWL-080 (VERIFIED jewel — status badge; jewel form, not a text-label badge) |
| 9 | avatars | ❌ GAP | App icons exist; no user-avatar block. Build: avatar with presence states |
| 10 | input | ✅ HAVE | NAYA-CRD-085 (INPUT/FORM specimen — labeled input with recessed well) |
| 11 | textarea | ❌ GAP | Build: multiline variant of the input block |
| 12 | select | ❌ GAP | Build: dropdown select block |
| 13 | checkbox | ✅ HAVE | NAYA-FRM-001..006 (Pre-ship checklist checkbox rows) |
| 14 | radio | ❌ GAP | Build: radio group block |
| 15 | toggle | ✅ HAVE | NAYA-CRD-090 (TOGGLE/SETTINGS specimen) |
| 16 | slider | ❌ GAP | Build: range slider block |
| 17 | search bar | ✅ HAVE | NAYA-CRD-089 (SEARCH INTERFACE specimen) |
| 18 | tabs | ❌ GAP | Build: tab bar block |
| 19 | accordion | ❌ GAP | Build: expandable section block |
| 20 | modal | ✅ HAVE | NAYA-CRD-086 (MODAL/DIALOG specimen — "Keep this private?") |
| 21 | toast | ✅ HAVE | NAYA-CRD-087 (TOAST/NOTIFICATION specimen — "Copied to clipboard") |
| 22 | tooltip | ❌ GAP | Build: hover tooltip block |
| 23 | dropdown menu | ❌ GAP | Build: menu/popup block |
| 24 | pagination | ❌ GAP | Build: page-control block |
| 25 | table | ✅ HAVE | NAYA-CRD-088 (DATA TABLE specimen — Block/State/Proof columns) |
| 26 | list row | ✅ HAVE | NAYA-LST-002 (list specimen, "Every bullet a jewel") |
| 27 | feed card | ✅ HAVE | NAYA-CRD-091 (content card), NAYA-CRD-004 (intelligence board) |
| 28 | comment | ❌ GAP | Build: comment thread block |
| 29 | chat bubble | ❌ GAP | Build: chat message bubble block |
| 30 | gallery grid | ❌ GAP | Build: image grid block |
| 31 | lightbox | ❌ GAP | Build: media overlay block |
| 32 | audio player | ✅ HAVE | NAYA-CRD-092 (MEDIA PLAYER — voice-audio specimen) |
| 33 | video player | ❌ GAP | Build: video player block |
| 34 | progress bar | ❌ GAP | Build: progress indicator block |
| 35 | spinner | ❌ GAP | Build: loading spinner block |
| 36 | skeleton loader | ❌ GAP | Build: skeleton shimmer block |
| 37 | empty state | ❌ GAP | Build: empty-state illustration + copy block |
| 38 | error state | ❌ GAP | Build: error-state block |
| 39 | 404 | ❌ GAP | Build: 404 page block |
| 40 | breadcrumbs | ❌ GAP | Build: breadcrumb trail block |
| 41 | footer | ❌ GAP | Build: footer block |
| 42 | sidebar | ❌ GAP | hub-rail (NAYA-NAV-001) is adjacent vertical nav, not a sidebar panel. Build: sidebar panel block |
| 43 | stat card | ❌ GAP | Build: metric/stat card (number + label + delta) |
| 44 | chart container | ✅ HAVE | NAYA-CRD-093 (CHART/DATA-VIZ anatomy specimen) |
| 45 | timeline | ❌ GAP | Build: timeline block |
| 46 | pricing card | ❌ GAP | Build: pricing tier card |
| 47 | testimonial | ❌ GAP | Build: testimonial/quote card |
| 48 | CTA band | ❌ GAP | CTA *button* exists (NAYA-BTN-158 "✦ ENTER THE STANDARD"); no full-width band section. Build: CTA band section |
| 49 | login form | ❌ GAP | Build: login form block |
| 50 | signup form | ❌ GAP | Build: signup form block |
| 51 | settings row | ✅ HAVE | NAYA-CRD-090 (TOGGLE/SETTINGS pairs label + state — the settings-row pattern) |

Note: items 10, 15–17, 20, 21, 25, 32, 44 rest on the "missing ten" **anatomy specimens** (do/don't cards demonstrating the block). They are the design reference for building production versions — marked HAVE as designed, and the next wave should promote them to tested blocks.

## The GAP build list (30, next wave)

hero, avatars, textarea, select, radio, slider, tabs, accordion, tooltip, dropdown menu, pagination, comment, chat bubble, gallery grid, lightbox, video player, progress bar, spinner, skeleton loader, empty state, error state, 404, breadcrumbs, footer, sidebar, stat card, timeline, pricing card, testimonial, CTA band, login form, signup form

## Exclusions from the catalog (justified)

28 extracted records were excluded as non-blocks: 27 color-token demos (`<div class="swatch">`, `<div class="spec">`, role-labeled spectrum swatches) belong in the design-token contract, not a block catalog; 1 logo `<img>` asset (showcase1-065). Full list in the t0907 receipt. UNCAT count in the final catalog: **0**.
