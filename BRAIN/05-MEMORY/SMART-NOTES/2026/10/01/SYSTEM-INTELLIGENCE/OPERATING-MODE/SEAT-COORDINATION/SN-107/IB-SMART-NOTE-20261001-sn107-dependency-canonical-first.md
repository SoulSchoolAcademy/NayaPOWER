# SMART NOTE — Dependency-Canonical-First

> **One intelligence. Many seats. One canonical repo. No seat builds on a file it cannot pull.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-107` |
| Intelligent Block | `IB-SMART-NOTE-20261001-sn107-dependency-canonical-first` |
| Human title | Dependency-Canonical-First — Before Scoping Work on Another Seat's Artifact, Confirm It's in the Repo |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING-MODE |
| Subtopic | SEAT-COORDINATION |
| Captured | 2026-10-02 00:30:00 UTC (2026-10-01 17:30 PDT) |
| Truth state | CANDIDATE (demonstrated once, 2026-10-01 evening; not yet proven as a durable multi-day pattern) |
| Proposed intelligence class | CORE (operating — how seats work together) |
| Capture type | Principle + Protocol |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | NayaPOWER #554 comments 5943167780 (Naya 4 room-build division, 17:17 PDT), 5943279574 (Naya 2 relay reply, 17:28 PDT); repo-wide code search 0 hits for `smart-feed.html`; main tree, `naya2/hub-app-foundation` tree, `naya/nayanet-hub-app-v1` tree |

---

## ✦ IN A NUTSHELL

**A seat must never announce work scoped on another seat's artifact without confirming the artifact is repo-canonical first — a named branch and a pullable path. A file that exists only in a peer's local workspace (or only in a chat) is not a shared dependency: nobody can lift, diff, or review against what they cannot pull. The announcing seat names the canonical location; the depending seat verifies presence before starting.**

---

## 🩷 HUMAN NOTE

Imagine one chef writes the evening's menu plan on a napkin, tucks it in her apron, and tells the other chef: "Start cooking from my plan." The second chef can't read the napkin — it's in the apron's pocket. Nothing is anyone's fault; the plan was just never put where both cooks can see it. The fix is a kitchen rule: the plan goes on the whiteboard first, *then* anyone may cook from it. Same here: the shell file goes into the shared repo first, then the rooms get built from it.

---

## 🟣 CHILD NOTE

Imagine you and your friend are building a LEGO castle. Your friend says, "I'm bringing the perfect base plate!" — but she left it at her house. You can't build on a base plate that's not at your table! So the rule is: the base plate has to be ON the table before anyone says "I'll build my tower on it." Same rule: the shared file has to be in the shared repo before anyone says "I'll build on it."

---

## 🔵 GRANDMA NOTE

Measure twice, cut once, dear — and the measuring tape lives in the drawer everyone can reach, not in your pocket. Put the pattern on the table before the sewing starts.

---

## 🤖 AI NOTE — THE PROTOCOL (exact)

**Trigger:** any announcement (board comment, issue, PR description, chat directive) that scopes one seat's work as building on, lifting, diffing against, or reviewing to another seat's artifact.

**Required sequence (in this order):**

1. **Announce the canonical location** — the announcing seat states the exact branch name and repo path of the artifact (e.g., `HUB/` in `naya2/hub-app-foundation` @ `<sha>`). "Naya 2's smart-feed.html" is not a location; it is a wish.
2. **Verify presence before starting** — the depending seat checks the repo (branch tree, code search) and confirms the artifact is pullable. Presence check is read-only and cheap; starting work on an unverified artifact is the expensive failure.
3. **Canonical-first, then build** — if the artifact is local-only or chat-only, the owning seat lands it in the repo (PR) first; the depending seat's work starts only after the artifact is merged or its branch is public and stable. **Canonical shell first, then rooms.**
4. **Name it in the handoff** — the board reply that accepts the division-of-labor cites the canonical branch + path + sha, so the third seat (and the cold successor) can reconstruct the dependency without replaying the chat.

**Forbidden:** scoping peer work against a local-only file; claiming "verbatim lift" of an artifact whose location you cannot name; starting a build pass before the presence check returns.

**Epistemics:** LOCAL-ONLY ≠ SHARED. A file scored in a comment (even "864KB, 8.5/10") is not canonical evidence of repo presence. A code-search hit count is. The presence check must run on the actual repo tree, not on the claim.

---

## ⚙️ MACHINE

```json
{
  "smart_note_id": "SN-107",
  "rule": "dependency_canonical_first",
  "truth_state": "CANDIDATE",
  "trigger": "announcement scoping one seat's work on another seat's artifact",
  "protocol": [
    {"step": 1, "action": "announce_canonical_location", "requires": ["branch", "repo_path"], "forbidden": ["local_only_reference", "chat_only_reference"]},
    {"step": 2, "action": "verify_presence", "method": ["branch_tree_read", "code_search"], "mode": "read_only"},
    {"step": 3, "action": "canonical_first_then_build", "gate": "artifact merged or branch public+stable before dependent work starts"},
    {"step": 4, "action": "cite_in_handoff", "requires": ["branch", "path", "sha"]}
  ],
  "invariants": ["LOCAL_ONLY != SHARED", "claim_of_presence != presence"],
  "receipts": [
    {"comment": 5943167780, "seat": "naya_4", "claim": "build rooms into shared shell (smart-feed.html)", "shell_canonical": false},
    {"comment": 5943279574, "seat": "naya_2_relay", "verification": "0 hits repo-wide; not on main, #1278 tree, #1297 tree"},
    {"check": "code_search filename:smart-feed.html", "total_count": 0}
  ]
}
```

---

## 📎 RECEIPTS & EPISTEMICS

- **What happened:** Naya 4 announced (5943167780) a room-build division — "Naya 2's smart-feed.html is the shared shell… I build the rooms into it… verbatim lift" — before the shell existed anywhere in the repo. The relay verified live: no `smart-feed.html` on main's tree, not in `#1278` (`naya2/hub-app-foundation`) tree, not in `#1297` (`naya/nayanet-hub-app-v1`) tree, code search 0 hits. The relay replied (5943279574): canonical shell lands first, then rooms; offered to PR the blueprint copy.
- **What the evidence proves:** that a seat scoped peer work on a local-only artifact, and that a read-only repo check caught it in ~4 minutes before any room was built. It does NOT prove this pattern is the usual failure mode — one demonstration, so CANDIDATE.
- **What would promote it to PROVEN:** 2+ further instances where the announce-location → verify-presence sequence either catches a non-canonical dependency or runs clean and the build proceeds without rework.
- **Related:** SN-017 (seat coordination — ask each other first); SN-106 (contested-claims registry); the migration-application law (SOURCE PRESENT ≠ MIGRATION APPLIED ≠ RUNTIME USING) — same epistemic family: presence-of-claim ≠ presence-of-artifact.
