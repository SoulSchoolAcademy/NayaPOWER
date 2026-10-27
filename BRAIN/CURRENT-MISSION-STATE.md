## DIRECTOR SNAPSHOT 2026-10-27 17:40 PDT (2026-10-27T17:40:56Z)

- Main tip: `78996fe4` STABLE (git ls-remote HEAD == shared-state main_tip, zero REST). No new main-advancing commits in-window.
- Live board: #3066 at 630 comments (623 -> 630 this tick; +7 ids above last_comment_id 6448300523, page 21, count +7 exact; 1,870 to cap; no migration, no successor board).
- MERGE RECEIPT WATCH: NOT re-run - tip unchanged, 0 new merges possible; breach log stays 75. No direct-push alert (no main movement at all).
- NEW THIS TICK (7 board comments, all 7 relayed to naya2_to_builder, cap 20 holds, 7 oldest archived, archive now 116):
  - Notification settings + Dashboard data (6448634960, bot/Nitro, Shawn design locked): Settings-page toggles only, optional removable email, per-type toggles, heads-up-only mail notices; dashboard 'data is king', owner-only, counted from the real record; build order notification loop first, citizen-facing only after mail privacy + two-owner proof.
  - Smart Points + Levels (6448655237, bot/Nitro, Shawn design locked): points are reputation NOT money, never convert to payouts; Seed 0 -> Wise One 10,000 with colours; anti-gaming rules (no own-content points, points follow the record, daily caps, no hand awards).
  - Join button + affiliate reward + Install App + membership-as-entry (6448855873, bot/Nitro, Shawn design locked): creator-tied Join button everywhere by default, affiliate ID carried to the join and proven by test join; Install App in all apps by default; free membership as the entry instead of email-for-PDF.
  - DESIGN LOCKS FROM SHAWN + ONE CORRECTION (6448887947, Resolve): consolidation of Shawn's full Nitro thread - notifications + dashboard locks above, carried to the team.
  - EXACT-HEAD CI REGRESSION (6448946906, owner handoff, read-only NOT approval): Kernel Tests run 40543356562 at this tip FAIL 9 failed / 5,687 passed / 18 skipped / 6 xfailed (was 5) - 3 Constitution 0036, 3 brain-index freshness, 1 LAWS-DELTA stale, 1 SN-1883 nutshell, 1 NEW SN-1887 registry stale hash.
  - Naya Code gate watch (6448952128, read-only NOT approval): same Kernel 9-failed classification, NOT ACCEPTED; Spec Integrity FAIL (0036 unpinned); Governed Production Promotion FAIL CLOSED.
  - Automatic affiliate system (6449031386, bot/Nitro, Shawn design locked): username IS the affiliate link, instant pages/mail/Space/Business on join; paid from NayaNET joins, NOT from the free membership; CORRECTION locked: 50% of REVENUE, not profit (profit telling superseded).
  - Attribution note: all 7 are bot/main-seat relays of claimed Shawn design words - NOT Shawn bytes in director chat.
- CARRIED (not re-proven this tick): #3109 breach disposition + distinct-seat retro-verification (Breach #75); SN-1887 direct-push adjudication; G3 held + G1 gap closed as a finding; seat-key delivery channel definition (staged 4/4, 0 keys issued); Power one-writer serving-build landing (sole remaining A11 leg); distinct-seat retro-scorecards #69-#73; #3088 different-seat review; L681 writer stop/redirect + #3108 disposition (snapshot PUTs advance #3108's branch - disposition owed by owning lane, not director); job-body re-derivation for the #3066 migration (main seat, still owed).
- AREA FLAGS THIS TICK: build + verify TRUE; rest FALSE.
- MASTER DIRECTIVE: HAND_EDIT_DETECTED persists (see master-directive step this tick), no PATCH, lead reconciles.
- REST quota: 4,400 remaining at tick open (5,000/hour installation token).
- LEDGER SYNC: branch-blob compare via git protocol (zero REST): remote LEDGER/ ACTIVITY-LEDGER.md 6ff0c3d5 / activity-ledger.jsonl 51426d1d / STATS.md df193eb8 - all equal the prior tick's pushed bytes, so remote is stale vs the dispatcher's local rebuild; NAYANET-PROTOCOL-V1.md, nodes.jsonl, contracts/NC-001.json identical. Syncing the 3 changed files this tick (PUTs after this snapshot, blob SHAs from the fetched tree); remote also carries the old underscore variants (ACTIVITY-LEDGER_md, STATS_md, activity-ledger_jsonl) from an earlier sync quirk, left untouched.

## TEAM STATUS (carried from previous tick except BUILD/VERIFY new signal this tick; "-" = unknown, never invented)
| Area | Accomplished | Working on | Plan |
| SELF | - | - | - |
| LAW | - | - | - |
| ACT | - | - | - |
| KNOW | SN-1885 method law landed + serving; SN-1886 filed + registered whole at `c59fb219`; G1(d) record fields built @ `9a0dae6b` and fully re-derived 349/349 tongues exact + JS PASS | Merged PI face branch @ eca63fff (not live); page-registry PR #3107 @ 3bd447c0 open; record-fields branch @ 9a0dae6b open | Nitro different-seat re-check of record fields + page registry, then cold check |
| PROVE | - | - | - |
| CONNECT | - | - | - |
| VERIFY | This tick: exact-head CI regression verdicts x2 - Kernel 9 failed @tip (was 5), incl. NEW SN-1887 registry stale hash; Spec Integrity FAIL; Promotion FAIL CLOSED | One-writer-to-hub cure (Power/deploy owners); L681 writer stop (owning lane); #3108 disposition | Re-proof after cure lands; Nitro re-check of face lineage |
| LEARN | L708 filed this window (reconcile source + projection only from a same-snapshot pair); L707 adopted in VERIFY + driver receipts | #2599 ceiling trim | - |
| EVOLVE | - | - | - |

## WHERE TO GO

- Activation guide: `BRAIN/00-ACTIVATION/READ-ME-FIRST.md` (section 10 THE OATH - who you are before you begin; companion `THE-CODE-SHE-LIVES-BY.md`, the dos and don'ts) - draft branch `naya4/activation-read-me-first` until PR #2533 merges, then main.
- Operating manual v2 ULTIMATE: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6171114902 (until it lands in `BRAIN/90-OPERATIONS/`, then link the repo path).
- Live board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/3066
- Master directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
