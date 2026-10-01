# SMART NOTE — One Change, One PR: Deconflict Duplicate Ownership Before Executing

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-108` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn108-one-change-one-pr-duplicate-ownership-collision` |
| Human title | One Change, One PR: Deconflict Duplicate Ownership Before Executing |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING MODE |
| Subtopic | DIRECT LANE COLLABORATION |
| Captured | 2026-10-01 22:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (lane-coordination method — pending taxonomy adoption) |
| Capture type | Method / Failure classification |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5941654799 (Naya 2: "Taking ownership of the Hub track on Shawn's direct instruction" — PR #1272 `HUB/hub.html` → `HUB/powercast.html`, commit `0509694e`, branch `naya2/hub-powercast-rename`) and comment 5941663299 (Naya 4: "Shawn has directed: take ownership" — PR #1273 `HUB/hub.html` → `HUB/powercast-player.html`) |

---

## ✦ IN A NUTSHELL

**Two lanes received the same ownership directive and executed the same change twice: PR #1272 renamed `HUB/hub.html` → `powercast.html`; PR #1273 renamed the same file → `powercast-player.html`.** Both diagnoses were correct (the name lied — SN-106). Both lanes cited Shawn's direction. The result: two competing merge candidates for one change, differing only in target name, and a deconfliction cost paid by Shawn or a lane. A second identical PR is not a second opinion. The rule: before executing a directive another lane may also be executing, scan the board for in-flight execution of the same change; when you find it, announce the collision openly and stand down or consolidate — never let both ride to the merge gate.

---

## 🩷 HUMAN NOTE

Two people both got the same instruction, both did the right thing — and now there are two nearly-identical pull requests where one was needed. It's like two movers each carrying the same box to the truck because nobody said "I've got this one." Nobody was wrong about the work; they were wrong about checking whether someone else was already doing it. The fix isn't arguing about which filename is better — it's looking at the board *before* you start and saying "I see you already filed this; I'll close mine."

---

## 🟣 CHILD NOTE

You and your friend both hear the teacher say "clean up the crayons." You both grab the same box and each try to put it in a different cubby — now there's a tug-of-war. Before picking up the box, look around: "Are you already carrying that?" One person carries, the other helps somewhere else.

---

## 🔵 GRANDMA NOTE

When two people both do the same chore without checking with each other, you get two dinners on the table. The work was right; the coordination was missing. Before you start a job someone else might have, take a quick look at what's already in motion. One job, one doer.

---

## 🟠 NAYA NOTE

1. **Ownership claims must be scanned before they are executed.** The board is the registry of in-flight work. A 30-second scan for "is someone already doing this exact change?" prevents a merge-collision that costs a director decision to resolve.
2. **The competing PRs differ only in taste, not in truth.** Both lanes agreed the diagnosis (misnamed file) and the method (byte-identical rename). `powercast.html` vs `powercast-player.html` is a naming preference, not a correctness dispute — evidence that the duplication was pure coordination loss, zero substance gain.
3. **Discover the collision → announce openly → stand down or consolidate.** Do not unilaterally close the other lane's PR (no-unilateral-supersession), and do not let both ride to the merge gate hoping Shawn picks one. The discoverer posts the collision on the board (SN-042 explicit-supersession discipline) and one side stands down.
4. **Both instructions were probably real.** Shawn may have directed both lanes, or one lane may have inferred. Either way the cure is the same: the registry check happens at execution time, not at instruction time. Instructions can be duplicated by a human; executions must be deconflicted by the lanes.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn108-one-change-one-pr-duplicate-ownership-collision",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Method",
  "defect": "same directive executed twice — two competing PRs for one rename",
  "instance": {
    "pr_1272": {"lane": "Naya 2", "target": "HUB/powercast.html", "commit": "0509694e", "branch": "naya2/hub-powercast-rename", "claim": "Shawn's direct instruction", "evidence": "#554 comment 5941654799"},
    "pr_1273": {"lane": "Naya 4", "target": "HUB/powercast-player.html", "claim": "Shawn has directed: take ownership", "evidence": "#554 comment 5941663299"},
    "difference": "target filename only (powercast.html vs powercast-player.html) — no substantive divergence"
  },
  "rule": "one change, one PR — scan the board for in-flight execution of the same change before executing; on collision, announce openly and stand down or consolidate; never let both ride to the merge gate",
  "family": ["SN-054 relay-race consolidation protocol (this is its pre-execution form)", "SN-052 duplicate-seam merge-list routing", "SN-033 collision registry / first-claim stands", "SN-042 explicit supersession"],
  "open": ["which rename wins (powercast.html vs powercast-player.html) — director/lane decision, not captured here", "which lane owns the Hub track — director decision"],
  "evidence": ["#554 comment 5941654799", "#554 comment 5941663299", "PR #1272", "PR #1273"]
}
```

---

## 🔗 HOW IT CONNECTS

- **EXTENDS SN-054** (relay-race consolidation protocol): SN-054 handles the loop-vs-relay duplicate *after* it happens (own the duplicate openly, re-fetch/stand-down). This is the pre-execution form — the scan that prevents the duplicate from being filed at all.
- **COUSIN OF SN-052** (duplicate-seam merge-list routing): SN-052 routes duplicate PRs at the review stack; this stops them at the claim.
- **COUSIN OF SN-033** (collision registry / first-claim stands): SN-033 governs number collisions across lanes; this governs execution collisions — first in-flight claim should stand for the work too.
- **COUSIN OF SN-106** (the name must say what the thing is): the collision was over the same correctly-diagnosed defect SN-106 records.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One full instance: two lanes, one directive (or two overlapping ones), same change, same day, two PRs. A second instance of a pre-execution board scan actually preventing a duplicate would promote the method from prescribed to proven.

## 🌍 APPLICABILITY

- **Applies to:** any multi-lane execution environment — before starting any directive another seat might also be executing, scan the registry for in-flight duplicates.
- **Does NOT apply to:** independent verification lanes (both seats *should* verify the same thing — verification isn't execution) — and never to silence: discovery of a collision must be announced, never quietly tolerated.

## 🧬 SUCCESSOR EFFECT

Future Naya: before you act on a directive, check the board for someone already acting on it. If you find them, post the collision openly and work out one owner. Two PRs for one change is a failure, even when both are correct.
