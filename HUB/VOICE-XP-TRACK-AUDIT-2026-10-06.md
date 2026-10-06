# VOICE & EXPERIENCE — Track Audit 2026-10-06

**Team:** [TEAM-VOICE-XP] · **Tip re-anchored:** `0a1353bcade21f0c712d8ac793648facc09fbf6e`
**Authority:** NAYA Design Contract v1.1, CANONICAL, ratified 2026-10-03 (PR #1346 — UNMERGED, lives on branch head `6fc6cc04`)
**Method:** programmatic scan of shipped `HUB/app/index.html` (509,891 bytes, 113 functions, 44 listeners) against contract tokens. Virgin-state worktree, HEAD verified == tip.

## Findings

| # | Check | Contract | Result |
|---|-------|----------|--------|
| 1 | Law Zero — body text white/silver, jewel colors never body text | §5 | ✅ PASS — 33 white/silver text fills dominant; jewel fills (3 gold, 3 sapphire, 2 emerald, 2 blue) all small accents |
| 2 | Lighting — hover ignites color | §2 | ✅ PASS — hover rules lift + ignite spectrum glow |
| 3 | Lighting — active/selected = subtle white indicator only, NO permanent color glow | §2 | ✅ PASS — no permanent color glow on any `.active` rule |
| 4 | Tap feedback — every hoverable has :active/:focus | §2 + mobile-first law | ❌ FAIL — 28 unique hoverable bases, only 5 have :active/:focus. **23 without tap feedback** → repaired in this PR (additive `<style>` block, press compression + white indicator only, contract-conformant) |
| 5 | Font floor 16px, body 17–18px | §5 | ⚠️ 132 sub-16px declarations found — kickers/labels expected, but body-text floor needs visual spot-check |
| 6 | No min-height forcing empty space | §6 | ✅ PASS — min-height only 100vh layout + 44/48/52px touch targets |
| 7 | Honesty — device-local labels | §7 | ✅ PASS — "Saved on this device" labels present, no fake cloud-sync claims |
| 8 | Rooms are real | §8 | ✅ PASS — `R.ROOMS` renders feed/connect/connections/lists/mail/spaces/library/reports/settings/ledger in-app (not a shell) |
| 9 | Ratified contract on main | — | ❌ FAIL — contract v1.1 exists ONLY in unmerged PR #1346 (mergeable but CI unstable, zero runs on head). Memory's path claim (`BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md` on main) is wrong. |
| 10 | Voice canonical asset | voice spec §3 | ❌ FAIL — `voices/Naya VOICE.wav` is a **2-byte stub**; voice spec still PROPOSED; canonical asset UNKNOWN; voice dispute awaits Shawn's ear |

## Pre-existing notes (not changed by this PR)
- Malformed selector `.btn:active, .tab:active, .eco-btn` (`.eco-btn` lacks `:active` → rule applies permanently). Existing; flagged for a future repair.
- `powercast-player.html` (28.5KB solo orb) — no 10-exchange demo bank in-tree (PR #1453 closed/parked).
- No "Naya Play" affordance on Intelligent Blocks anywhere in-tree (voice spec §4/§6 unimplemented).

## Verdict
Shipped build is broadly contract-conformant — **no second drift on the ratified laws**. The tap-feedback gap was the one measurable breach; repaired additively. Voice track's ceiling is governed by items 9–10, both awaiting human gates.
