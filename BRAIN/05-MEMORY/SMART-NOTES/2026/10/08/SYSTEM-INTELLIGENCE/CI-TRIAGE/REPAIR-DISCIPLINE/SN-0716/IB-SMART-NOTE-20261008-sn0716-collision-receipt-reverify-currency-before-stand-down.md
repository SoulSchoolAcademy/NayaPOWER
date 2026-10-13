# A Colliding Claim Earns the Stand-Down Only After Currency Re-Verification

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0716-collision-receipt-reverify-currency-before-stand-down
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6068504158 ([NAYA 2][BRAIN-BUILD] Collision receipt — `engineering-gates-import-red` stood down, 2026-10-08T20:31:36Z); queued by #1354 comment 6068378264 (BRAIN-BUILD BATTERY, 2026-10-08T20:23:55Z); same RED classified as base defect owned by #1840 in #1354 comment 6068194195 ([NAYA 4] SIGN OUT, 2026-10-08T20:12:47Z) — all SoulSchoolAcademy

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brain-build loop's 20:22Z battery queued `engineering-gates-import-red`: `tests/test_engineering_gates.py` fails at collection with `ModuleNotFoundError: No module named 'engineering_gates'` — the test inserts `~/workspace` into `sys.path` and imports a module that exists nowhere importable there, neither in CI (the workflow has zero setup for it) nor locally. Reproduced on the bare base tip, so this is a **NEW RED on main, pre-existing** (not PR-caused). The next run's claim scan returned **COLLISION**: Naya 4's PR #1840 ("Fix test_engineering_gates import") is OPEN and claims this exact RED class.

The lane did not blindly defer — and did not duplicate. It ran the **currency receipt on exact tip bytes** `78661f59`:
1. **RED still red on the tip** — `pytest --collect-only` on the tip reproduces the `ModuleNotFoundError`.
2. **The claim's head actually fixes it** — #1840 @ `7fd4942c`: collection error gone on its head, 1340 passed, live CI evidence (run 37749848048 @ 08:26Z, per Naya 4's wave-unblock classification).
3. **The claim is not stale** — the repaired files (`tests/test_engineering_gates.py`, `tests/test_ci_declares_test_dependencies.py`) are byte-identical between #1840's base `53217a40` and the current tip `78661f59`.

Only then: the item was marked `blocked` ("claimed by Naya 4's PR #1840 — valid + current; stand down per no-duplicate-repair law"), no second PR was opened, Naya 4's branch was left untouched, and the merge path was recorded as #1840 under the Scorecard Law (with the #1840↔#1838 stacked path per the wave-unblock classification).

Why this is brain-grade: SN-0236 says one repair per RED class, and SN-0508 says stand down your own unpushed repair when another lane heals the seam. Both assume the colliding claim is good. This note closes the trust-but-verify half: **an open claim is not automatically a current claim.** A repair PR opened two tips ago against a moved base can be open, green on its own head, and stale on the current tip. Blindly deferring to it converts the no-duplicate rule into a permanent blocker for a real RED — the class stays broken because everyone is "standing down" for a repair that no longer applies. The collision receipt is the handshake: collision → verify currency on exact tip bytes → then and only then stand down. A claim that fails currency doesn't earn the stand-down; it earns a currency flag on the board.

Rule for a cold successor: **when your claim scan collides with an open repair, re-verify the claim before standing down:** (1) the RED reproduces on the exact current tip; (2) the claim's head fixes it, with live CI evidence; (3) the claim's repaired files are byte-identical between its base and the current tip. Open ≠ current. Only a claim that passes all three owns the class.

## 🩷 HUMAN NOTE

Shawn — a lane-coordination lesson from tonight's build loop. The loop queued a repair for a broken test import, then found Naya 4's PR #1840 already open for the same red. Instead of blindly deferring or building a duplicate, it re-verified her claim on the exact current tip: the red is still red, her branch still fixes it (with live CI proof), and her fixed files match the current tip byte-for-byte. Only then did it stand down. The standing rule: an open claim doesn't automatically win — it has to prove it's still current on today's exact bytes, or it doesn't earn the stand-down. That's how parallel lanes avoid both duplicate repairs and permanent blockers.

## 🟣 CHILD NOTE

Imagine you and a friend both notice the same broken swing, and your friend says "I'll fix it." You don't just walk away forever — you check: is the swing still broken today? Did your friend's fix actually work? And does their fix still fit *this* swing, or was it made for the old one before it got replaced? Only if all three answers are yes do you stand down. If the fix was made for an old swing, it doesn't count — the swing is still broken and someone has to fix the real one.

## 👵 GRANDMA NOTE

Two workers both spotted the same defect and one already had a repair in progress. Before stepping aside, the other verified three things: the defect is still present in the current version, the in-progress repair actually fixes it (with test evidence), and the repair was made against the current version — not an older one it no longer matches. Only then did they stand down. The lesson: "someone's already on it" is only a reason to step aside if their fix is still valid today. An old fix for a changed situation doesn't count.

## 🟣 NAYA NOTE

The no-duplicate-repair law is a governance instrument, not a sleep aid. When my claim scan collides, I run the currency receipt before I stand down: RED-on-exact-tip, claim-head-fixes-it with live CI evidence, repaired-files byte-identical between claim base and current tip. Three passes and the claim owns the class — I mark my item blocked and touch nothing of theirs. Any failure and the claim doesn't earn the stand-down; it earns a currency flag on the board, publicly, because a stale claim silently blocking a live RED is worse than a duplicate repair — it's an invisible one.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0716",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE",
  "doctrine": "collision-receipt-currency-verification",
  "rule": "A colliding claim earns the stand-down only after currency re-verification on exact tip bytes: (1) RED reproduces on the current tip; (2) claim head fixes it, with live CI evidence; (3) claim's repaired files byte-identical between its base and the current tip. Open != current.",
  "failure_mode": "blind deference to a stale open claim converts the no-duplicate rule into a permanent blocker for a live RED",
  "receipt": [
    "pytest --collect-only on tip 78661f59 reproduces ModuleNotFoundError: No module named 'engineering_gates'",
    "#1840 @ 7fd4942c: collection error gone on its head, 1340 passed (CI run 37749848048 @ 08:26Z)",
    "repaired files (tests/test_engineering_gates.py, tests/test_ci_declares_test_dependencies.py) byte-identical between #1840 base 53217a40 and tip 78661f59"
  ],
  "cousins": ["SN-0236", "SN-0508", "SN-0710", "SN-0711", "SN-0625"],
  "evidence": [
    "#1354 comment 6068504158 (Naya 2, 2026-10-08T20:31:36Z) — collision receipt: claim scan COLLISION with Naya 4's open PR #1840; currency re-verified on exact tip 78661f59; item marked blocked; no second PR opened; Naya 4's branch untouched; merge path #1840 under Scorecard Law",
    "#1354 comment 6068378264 (battery, 2026-10-08T20:23:55Z) — item queued: NEW RED on main, pre-existing; test inserts ~/workspace into sys.path and imports a module importable nowhere; reproduced on bare base tip",
    "#1354 comment 6068194195 (Naya 4 sign-out, 2026-10-08T20:12:47Z) — same RED classified as BASE-DEFECT/TEST DEFECT owned by #1840; no duplicate repair opened per one-repair-per-RED-class"
  ]
}
