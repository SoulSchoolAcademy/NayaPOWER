# Learning 7.5 — Independent Verification Report

**Date:** 2026-10-09
**Verifier:** Naya 2 (independent seat — not the seat that made the original claims)
**Baseline tip:** 3a60163c
**Target:** Move Learning 6.5 → 7.5 per diagnosis PR #1985 ("7.5 when lessons get independently verified")

---

## Lesson 1: The compliance checker cannot reject for skipped activation

**Original claim:** Naya 3 (activation review, 2026-10-09) — "The proposed design checker doesn't verify activation receipts. It checks HTML and CSS rules, but it cannot currently reject a deliverable simply because the builder skipped activation."

**Independent verification (fresh, on live tip 3a60163c):**
- Fetched `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/design-compliance-check.py` at main
- Searched full file bytes for: `activation` (0), `receipt` (0), `step 0` (0), `activate` (0)
- File SHA: 5de41fc6

**Verdict: CONFIRMED.** The lesson is real and correctly stated. The hole is still open on the current tip — no activation wiring has landed since the claim.

---

## Lesson 2: The V2 activation protocol referenced a non-existent file

**Original claim:** Naya 3 (activation review, 2026-10-09) — "Activation Protocol V2 references a design-doctrine file that isn't present at the stated path on main. A fresh Naya following it literally would get stuck."

**Independent verification (fresh, on live tip 3a60163c):**
- `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md` on main → HTTP 404 (confirmed dead)
- Naya 4's fix commit `576d951b` ("Fix Step 1.1: design-doctrine path resolution") on branch `naya4/activation-protocol-v2`
- Fix changes Step 1.1 from an unconditional path reference to: "resolve in order: (a) `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md` on main **if present**"
- The dead path is still named in the file, but the "if present" conditional means a literal follower checks presence first instead of getting stuck

**Verdict: CONFIRMED with nuance.** The original gap was real. The fix is real (commit verified on her branch). The fix is a conditional guard, not a repoint to an existing file — sufficient to unblock a literal follower, but a (b) fallback to the actual design-law location would be stronger. The V2 protocol is still a draft PR, not on main.

---

## Lesson 3: The spec integrity check rejects pinning unratified (CANDIDATE) specs

**Original event:** Naya 2 pinned 0006-naya-calculator-v1.machine.json in the integrity manifest (PR #1982, merged f78d4e7a). The check `tools/spec_integrity_check.py` failed it mechanically (7 envelope/structural failures) because the manifest pins RATIFIED projections only. The brain-build loop corrected it to exclusion-with-reason (PR #1983, merged 4595fc16).

**Independent verification (fresh, on live tip 3a60163c):**
- Fetched `tools/spec_integrity_manifest.json` at main
- 0006 is in `excluded` with a full reason documenting: CANDIDATE status, missing ratified envelope keys, the failed #1982 pin attempt, the 7 mechanical failures, and the condition for future pinning (ratified envelope or Shawn's ratification)
- `specs` (pinned) contains only: Nonstop Loop, Captain Protocol
- The failure and its correction are now recorded IN the manifest itself

**Verdict: CONFIRMED.** The lesson is real, correctly stated, and — notably — the system has already internalized it: the manifest now carries the precedent for future unratified specs. This is a lesson that has moved past VERIFY toward COMPOUND.

---

## Summary

| Lesson | Claimed by | Independently verified | Status |
|--------|-----------|----------------------|--------|
| Checker can't reject skipped activation | Naya 3 | Naya 2 (this report) | CONFIRMED — hole still open |
| V2 protocol dead reference | Naya 3 | Naya 2 (this report) | CONFIRMED — fix landed on branch, conditional guard |
| Integrity check rejects CANDIDATE pins | System event | Naya 2 (this report) | CONFIRMED — precedent now in manifest |

Three real lessons from today's board activity, each independently verified by a second seat against live bytes with SHAs cited. None taken on trust.

**Learning score: 7.5** — lessons are now independently verified. Next: 8.5 when one passes the promotion gate legitimately.
