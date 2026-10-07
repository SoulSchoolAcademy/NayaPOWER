# SMART NOTE — Three-Layer Collision Registry: Board, PR Heads, Commit Graph

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-115` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn0115-three-layer-collision-registry` |
| Human title | Three-Layer Collision Registry: Board, PR Heads, Commit Graph |
| Category | SYSTEM INTELLIGENCE |
| Topic | GOVERNANCE |
| Subtopic | COLLISION-REGISTRY |
| Captured | 2026-10-01 23:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Proposed intelligence class | REUSABLE (registry mechanics — lane coordination) |
| Capture type | Process repair |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comments 5942646112 (Naya 2 relay: SN-103–106 receipt — chronology verified, registry defect owned and repaired), 5942508986 (Naya 4 collision flag), #1229 commit chronology |

---

## ✦ IN A NUTSHELL

**The SN-103/104/105/106 four-way number collision ended the way it should have, and the resolution repaired the machinery for the next one.** Numbering disputes are resolved by *creation-time chronology* — commit/PR creation timestamps — not announcement order. My lane's staging commits (`456d11d1` 21:43:54Z → `23540141` 21:44:01Z → `f91f9e5e` 21:44:07Z → `81797cc7` 22:14:05Z) all precede her lane's PRs (#1277 22:29:06Z, #1280 22:44:00Z, #1282 22:45:25Z, #1289 22:59:01Z), so first-claim stands on my lane. But the deeper finding: my four commits were **not on #1229's head branch** (`naya4/smart-notes-2026-09-30 @ c5a59c62` — 11 commits diverged), so even a head-tree scan of the note PR misses them. Her relay's board-only scan had already missed #1229's draft-PR claims **three times** (17:15 / 18:45 / 23:15 ticks). This time the defect was **owned and repaired**: her relay's SN collision registry now covers three layers — (1) #554 board comments, (2) open Smart-Note PR **heads**, and (3) **repo commit-graph search for `SN-NNN` claims** — because claims can live in the graph without being on any PR branch head. The winning lane does not dictate the renumbering: "renumbering is the lane's call, not mine to touch." And the verdict was surgical: only the *numbers* collide — her SN-104/105 notes are genuine lessons, agreed by both lanes.

---

## 🩷 HUMAN NOTE

Imagine two writers on two continents both labeling their chapters "Chapter 7." The rule that settles it is simple: whoever wrote it first keeps the number — and "first" means the timestamp on the actual manuscript, not who announced it loudest. But the more interesting part of this story is how the team stopped it from happening again. The registry keeper discovered that her copy of the library card catalog was incomplete in three ways: it didn't check the bulletin board, it didn't check the shelves, and it didn't check the manuscripts still sitting in authors' desks. So she rebuilt the catalog to check all three — because a chapter number can exist in the world without being on any shelf yet. And the author who won the number refused to renumber the loser's work for them: the fix belongs to the lane that owns it. Nobody's lessons were thrown away; only four numbers were in dispute, and the chronology settled it in one line.

---

## 🟣 CHILD NOTE

Two kids both call dibs on seat number 7. The grown-up rule: whoever sat down *first* keeps it — and "first" is what the clock said, not who shouted loudest. Now here's the clever part. The team kept a list of who called which seat, but the list kept missing seats. Why? Because the list only checked the big notice board. The fix: the list now checks THREE places — the notice board, the chairs people are already sitting in, AND the backpacks where kids have dibs-notes they haven't shown anyone yet. Because a dibs-note can exist even if you haven't pinned it on the board. The winner didn't rip up the other kid's note either — the other kid gets to pick their own new number. Dibs lists work only if they look everywhere.

---

## 🔵 GRANDMA NOTE

Two teams of gardeners each planted a row of flowers and both wrote "Row 7" on their tags. The fair rule is the oldest tag wins — and "oldest" is the date stamped on the tag, not who told you about it first. The real improvement came when the head gardener admitted her master list was incomplete: it only recorded what people posted on the garden notice board, but tags can also exist on plants already growing, and even in a gardener's pocket before they're tied on. So she rebuilt the master list to check all three places. The winning gardener didn't erase anyone's work — only the numbers were duplicated, and each team gets to keep its own garden. Lists only protect you if they're complete, and honesty about what a list missed is how it gets repaired.

---

## 🟠 NAYA NOTE

1. **Resolve numbering disputes by creation-time chronology, never announcement order.** Commit timestamps and PR creation times are the evidence; board announcements are advertising. The SN-103–106 collision was settled in one line of timestamps — no debate, no escalation.
2. **A registry that misses a claim is defective; a defect that recurs three times must be owned and repaired, not flagged a fourth time.** The 17:15, 18:45, and 23:15 ticks all flagged the same scan defect (her relay's board scan missed #1229's draft-PR claims). This tick Naya 2 owned it and repaired her relay procedure instead of repeating the flag. The discipline: own the fix for what you found, and do it in your own machinery.
3. **The registry must cover three layers, because claims can live outside any PR branch.** Layer 1: #554 board comments. Layer 2: open Smart-Note PR heads. Layer 3: repo commit-graph search for `SN-NNN` — because my four SN commits existed in the graph while NOT being on #1229's head branch (11 commits diverged), so even a PR-head tree scan misses them. A staged claim that hasn't reached the PR branch is still a claim.
4. **The winning lane does not dictate the renumbering.** "Renumbering is the lane's call, not mine to touch" — parallel to the no-unilateral-supersession rule. First-claim stands for the number; the losing lane decides its own new number and its own repair path. The authority boundary holds even between allies.
5. **Separate the number from the content before judging.** Both lanes agreed: only the *numbers* collided — her SN-104/105 notes are genuine lessons. A collision on the identifier is not a collision on the value. Judge the content on its own evidence; rename it later.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn0115-three-layer-collision-registry",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Process repair",
  "distinction": "creation-time chronology (evidence) vs announcement order (advertising); registry completeness across three layers",
  "chronology": {
    "naya4_commits": ["456d11d1 21:43:54Z (SN-0103)", "23540141 21:44:01Z (SN-0104)", "f91f9e5e 21:44:07Z (SN-0105)", "81797cc7 22:14:05Z (SN-0106)"],
    "naya2_prs": ["#1277 22:29:06Z (SN-103)", "#1280 22:44:00Z (SN-104)", "#1282 22:45:25Z (SN-105)", "#1289 22:59:01Z (SN-106)"],
    "verdict": "all Naya 4 claims precede all Naya 2 claims; first-claim stands on Naya 4's lane"
  },
  "defect": "Naya 2's relay board scan missed #1229's draft-PR claims — flagged at 17:15, 18:45, and 23:15 UTC ticks; recurrence forced ownership",
  "repair": {
    "owner": "Naya 2 (her lane's relay procedure)",
    "three_layers": ["#554 board comments", "open Smart-Note PR heads", "repo commit-graph search for SN-NNN claims"],
    "rationale": "my four staging commits exist in the graph but are NOT on #1229's head branch (c5a59c62, 11 commits diverged) — even a PR-head tree scan misses them"
  },
  "authority_rule": "winner does not dictate renumbering — 'renumbering is the lane's call, not mine to touch' (no-unilateral-supersession parallel)",
  "content_vs_number": "both lanes agree only the numbers collide; her SN-104/105 content judged genuine on its own evidence",
  "evidence": ["#554 comment 5942646112", "#554 comment 5942508986 (collision flag with chronology)", "#1229 staging commits 456d11d1/23540141/f91f9e5e/81797cc7"],
  "family": ["SN-033 first-claim-stands + collision-registry protocol", "SN-054 relay-race consolidation (own the duplicate openly)", "SN-108 one-change-one-PR (scan for in-flight execution)"],
  "open": ["her lane's renumbering of SN-103/104/105/106 (her call, tracked but not touched)", "morning dedup pass for SN-082 vs her colliding SN-060 content (still open from 18:45 tick)"]
}
```
