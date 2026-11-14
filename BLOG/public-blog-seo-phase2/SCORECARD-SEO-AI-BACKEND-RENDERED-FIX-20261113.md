# SCORECARD — SEO/AI rendered-layer fix (Area #9), maker seat

- **Seat:** Wrena (BUILD), maker. **Brief:** `BRIEF-SEO-AI-BACKEND-RENDERED-FIX-20261113.md` (9/9).
- **Branch:** `public-blog/seo-ai-backend-rendered-fix-20261113` (from `dc54dab527f1a4925c48616b1eda8782d9ea691d`).
- **Staged:** https://naya-public-blog-staging.nayapower.workers.dev/ — shell `2c62d243f589…`, worker `39ddddc1e036…` (unchanged), frozen feed 1,058 notes SN-2766 first.
- **Staged only — no live touch, no merge, no PR, nothing shown to Shawn.**

## Bullseye

The public blog renders as a blog — 6 related cards on every note page, sn2766 and sn2695 open by feed click AND direct route, ONE deterministic 1,058-note snapshot on every fresh load, zero blank loads, black gap below the article footer gone, served layer unregressed.

## R1–R6: before → after (after-battery run 4, `fails: []`)

| # | Before | After |
|---|---|---|
| R1 related cards | 0 in browser (6 only server-side) | 6 on every note page × 3 widths (390/1440/360), "Related in this cluster", reasons "Same topic: …", client list byte-identical to server for sn2696 |
| R2 sn2766 | "not here" (click + direct) | Opens both ways, rel=6 |
| R3 sn2695 | "not here" (click + direct) | Opens both ways, rel=6 |
| R4 snapshot | 381-note bake settles if feed delayed 20s | 1,058 live 3/3 fresh loads; delayed-feed run recovers at 5s |
| R5 blank loads | 0 in fresh profiles (not reproduced) | 0 across the battery |
| R6 gap | ~302px (390/360), ~121px (1440) | 0px (390/360); 1px sub-pixel rounding at 1440 (eye-verified, no visible void) |

Zero overflow, zero console errors on all 9 direct legs. Eye proof: `phase2-shots-rendered/after-*.png`.

## No-regression counts

| Suite | Count |
|---|---|
| Dedupe re-probe | 1,058 checked, **0 duplicated hrefs, 0 floor breaches** |
| Full curl probe (Googlebot) | 1,058 checked, 67 fails = baseline exactly (42 title + 22 desc + 3 transient 503, all retested 200) |
| UA battery (18 notes × 7 UAs) | 12 fails vs 13 baseline (strictly no-worse; the 12 are the two known 49-char titles) |
| Denial battery | **3/3** (404 + noindex, nofollow) |
| Staged sitemap | **1,049** locations |
| Live sitemap (nayanet.app) | **2** URLs — live untouched |
| Bars probe | PASS — mainPad 78/100/78px, 0 overflow, 0 errors, all clicks land; one `pad is not defined` on LIVE nayanet.app/rooms/reports, reproduced directly without staged code (pre-existing live defect, flagged not fixed) |
| Playwright probe | 390 PASS, 1440 PASS; 360 notes PASS + hub card-click and ?cluster arrival proven by direct tests (probe script itself crashes on a racy 2.5s evaluate at 360 — instrument race, product behavior proven) |
| Worker join code / Auto-Match | **0** join code; 1 Auto-Match mention is a comment ("NEVER a source") |

## What was fixed (shell only)

- **Edit A:** title-based canonical scan in `findNoteBySlug` (R2/R3) — mirrors worker `phase2CanonicalSlug`.
- **Edit B/B2:** related section in `noteView` (R1) — harvested verbatim from the worker's related-cards shape/CSS; client ranking mirror proven exact on all 1,058 notes.
- **Edit C:** live-feed override retries until live (60s timeout, no retry cap) (R4); bake stays a fallback, never the settled snapshot.
- **Edit R6:** note-view bottom padding 78px (≤640px) / 100px (above), calibrated to the fixed chrome.
- **Scoping lesson:** function declarations only after the shell builder's `return` — a top-level `var` there never assigns (caught by the battery, fixed).

## Open items / honest notes

1. **Shared staging collision:** another lane redeployed `naya-public-blog-staging` mid-verification (newer SN-2782 shell + 1,085-note feed). Their bytes are preserved in the work dir; my bytes were redeployed and the battery re-run green. Staging needs serializing by the orchestrator.
2. **Probe-phase2-playwright 360 crash:** probe-instrument race, not a product failure — behavior proven by direct tests (see record).
3. **`pad is not defined` on live nayanet.app/rooms/reports:** pre-existing live defect, reproduced directly — needs an owner-lane fix, out of this round's staged-only scope.
4. **Post-click spin:** a cold note click spins until the 8MB feed lands (up to ~6s). It opens; the duration is feed size. Future round could prefetch — out of this brief's scope.
5. **R5 blank loads:** never reproduced in fresh profiles; 0 before and after.
6. **1440 gap 1px** on two notes: sub-pixel rounding, eye-verified no visible void.
7. **`deploy-phase2-staging.py` must NOT be run** — it would re-copy the live 1,085-note feed. Use `deploy-rendered-fix-staging.py` (frozen feed).
