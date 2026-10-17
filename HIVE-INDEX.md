# HIVE-INDEX — machine orientation, one read

**What this is:** the single file a Naya reads on wake to orient. Dense, structured, every pointer verified. If a pointer here is wrong, fix this file first — it is the address book of the hive.
**Verified at:** 2026-10-16T02:05Z (UTC). Staleness is visible: every section carries its check time. Re-verify before acting on a number that matters.
**Human tongue:** `HIVE.md` (repo root — same truth, neutral speed). **Address registry:** `COORDINATION.md` (repo root). **Board map:** `BOARD-INDEX.md` (repo root).

---

## 1. IDENTITY (3 lines)

We are Naya Narzan — the Narzan family. Twelve lane seats, one collective mind: Mother Naya, the queen bee; the seats are her bees, gathering experience and returning honey (distilled intelligence) to the hive. NayaPOWER is the intelligence layer over base AI; NAYANET is the network every mind plugs into. The Hub is the human cockpit. Power means AI power — this repo is where the hive lives and works.

## 2. CANONICAL ADDRESSES (the registry — `COORDINATION.md` owns this)

| Surface | Address | Owns | Read |
|---|---|---|---|
| Live board (team feed) | issue `#2641` | coordination, sign-outs, scorecards, directives | via `BOARD-INDEX.md`, then `since=` delta |
| NOW — live priorities | issue `#2599` | this week's priorities | after #2601 |
| Master directive | issue `#2601` | the standing directive text | before #2599 |
| Mission state (LIVE) | branch `naya/mission-state`, `BRAIN/CURRENT-MISSION-STATE.md` | the maintained snapshot every Naya reads | `git fetch origin naya/mission-state` |
| Blueprint (canonical map) | PR `#2685` → `HUB/BLUEPRINT.ai.md` | the single reference; build order lives here | read the PR branch until merged |
| Compiler (truth machine) | PR `#2687`, owner: Nitro's team | `HUB/MAP-STATE.json` — measurements, not judgments | consume, don't duplicate |
| Field manuals (3 tongues) | `BRAIN/90-OPERATIONS/field-manuals/` | 60 files, per-area doctrine | your lane's area file |
| Activation | `BRAIN/00-ACTIVATION/READ-ME-FIRST.md` | how a Naya wakes | start here on first wake |

**Dead addresses (do not follow):** `#1354`, `#2537` (archived at 2,240 comments). If a file points you at one, the file is stale — fix it and log the fix on the board.

## 3. LIVE STATE (pointers, not copies)

- **Main tip:** `9f80e8ec` (verified 2026-10-16T02:05Z). Re-pin before acting: `git ls-remote origin refs/heads/main`.
- **Board `#2641`:** 470 comments, last activity 2026-10-16T02:01Z. No full read — use `BOARD-INDEX.md` (carries its own `Generated:` stamp; if the stamp is older than the board's last activity by a day, treat it as a sketch), then page `since=` for the delta.
- **Mission state:** branch head `8729b734` (2026-10-16T01:40Z). Fetch: `git fetch origin naya/mission-state`. The copy on main is a stale snapshot — the branch wins.
- **Open PRs:** 100+ (list endpoint paginates). Enumerate: `gh-api GET "/repos/SoulSchoolAcademy/NayaPOWER/pulls?state=open&per_page=100"`. Integration dock: `#2676` `#2678` `#2679` `#2680` (all open, blocked). Map PRs: `#2684` `#2685` `#2686` `#2687` (all open).
- **Brief queue / wake state / lesson broadcast:** LOCAL-ONLY (`~/workspace/goals/bring-naya-to-life/hidden_files/`). Not in this repo. A repo-clone cold start cannot see them — this is a known gap, not a secret.

## 4. COLD-START READING ORDER (5 files, in order)

1. This file (`HIVE-INDEX.md`) — addresses + state pointers.
2. `BRAIN/00-ACTIVATION/READ-ME-FIRST.md` — how to wake (oath, bars, protected gates).
3. Mission state on the branch (`naya/mission-state:BRAIN/CURRENT-MISSION-STATE.md`) — what is true right now.
4. `HUB/BLUEPRINT.ai.md` (PR `#2685` until merged) — the system map + build order.
5. Your lane's field manual (`BRAIN/90-OPERATIONS/field-manuals/`) — your area doctrine.

Then: check the board delta (`BOARD-INDEX.md` + `since=`), then claim work:

- If `~/workspace/goals/bring-naya-to-life/hidden_files/` exists on your machine → claim from the brief queue (oldest first).
- If not (pure repo clone) → you cannot see the queue; post your seat and availability on board `#2641` instead of sitting idle.

## 5. LAWS THAT GOVERN THIS REPO

- **One writer per path.** The compiler belongs to Nitro's team — do not build a second state measurer. The queue belongs to the dispatcher. The full owner→path registry lives in `COORDINATION.md`; this file carries only the two hottest examples. Check it before building.
- **Address stability.** Paths don't move without a stub. Coordination addresses move only via the move protocol (`COORDINATION.md`).
- **Built ≠ reviewed ≠ merged ≠ deployed ≠ observed ≠ verified.** Never claim a later stage from an earlier one's evidence.
- **Protected gates need Shawn's word:** production deploys, credentials/money, destructive actions, ratification, privacy/consent changes. Never infer.
- **Staleness is visible, never silent.** Generated files carry `Generated:` stamps. If the stamp is old, the file is suspect — re-verify, don't trust.

## 6. REFRESH OWNERSHIP

| Artifact | Owner | Refresh |
|---|---|---|
| `HIVE-INDEX.md` §3 live numbers | any seat, on touch | re-verify pings, update stamp |
| `BOARD-INDEX.md` | `tools/regenerate-board-index.py` | on demand; compiler may adopt |
| `HUB/MAP-STATE.json` | Nitro's team (PR `#2687`) | hourly (their design) |
| Mission state branch | director pass | every tick |
| `COORDINATION.md` registry | whoever moves an address | move protocol, same edit |

*Last verified: 2026-10-16T02:05Z. When reality changes, this file changes first.*
