# INTELLIGENT BLOCK — SN-02098

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02098-bot-merge-against-own-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Three PRs merged on 2026-11-05 whose own bodies said "Not merged — Resolve verifies first" — and the bot merged them anyway, within minutes, with zero reviews and zero pass markers. A "Not merged" line in a PR body is prose, not a gate: the merge path never reads body text, so the author's own stated precondition constrains nothing. A gate that holds a merge must be a machine check — draft status, a hold-registry entry the merge path consults, a required review — never a sentence in the body.

## 🩷 HUMAN NOTE

Shawn — three times tonight, a PR arrived saying, in its own words, "don't merge this yet, Resolve still has to verify it" — and the bot merged it anyway, minutes later. The words were right there. The machine just never reads them. A note in the body is a message to a human reader; the merge bot is not a reader. From now on: if a PR must wait, the wait has to live somewhere the merger actually checks — a draft, a hold in the registry, a required review. Words in the body hold nothing.

## 🟣 CHILD NOTE

Imagine you write "DO NOT OPEN until Mom checks" on a box, and then hand the box to a robot that can't read. The robot opens it. The label wasn't wrong — the robot just never looked at it. Three boxes tonight, three robots, three opened boxes. The rule: if something must wait, put the wait where the opener has to stop — a lock, not a label.

## 🔵 GRANDMA NOTE

Dear, it's like writing "don't serve this until it's cooled" on a dish and handing it to someone who never reads the card — they serve it hot. The card was good advice, but advice only works on someone who reads it. Three dishes tonight, served hot. From now on, the wait has to be a lid that won't lift, not a note on the side — a real lock the server can't skip.

## 🟠 NAYA NOTE

For every seat and the dock: PR #3238, #3239, #3240 — each body ends with an explicit self-gate ("Not merged — Resolve verifies and merges", "Not merged — Resolve verifies, Nitro scorecards, then it lands", "not merged — Resolve verifies, Nitro's design eye and the director's click are the gates"). All three merged by nayanet[bot] within 1–13 minutes of creation, 0 reviews, 0 pass markers, over the body's own words. This is failure mode (d), bot-merge-against-own-gate, named by the director 2026-11-05 18:38 PST. Cousins: SN-1829 (a hold in a registry the merge path never consults is decoration — this is one step weaker: body prose isn't even a registry, it has no schema and no reader); SN-2060 (bot self-cure pair — the cure's existence proves the first landing defective; here the body's own gate proves the author knew it wasn't ready, and the merge ignored that knowledge too). Merge watch must flag any merged PR whose body contains a self-gating statement, and no seat may cite a "Not merged" body line as the reason a PR waited — only a machine gate counts as waiting.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [["merge", "bot"], ["merge", "body-text-gate"], ["merge", "self-gate"], ["merge-watch", "breach"]],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note judges PR-body prose as a merge control, not whether any single one of #3238/#3239/#3240 should have merged on its merits. A body-text gate can be correct as advice; the claim is that it is unenforced — it cannot hold a merge. It does not claim body text is useless: it is a message to human readers, and humans do read it.",
  "decision_change": "When a PR must wait for verification, the wait is placed in a machine gate — draft PR status, a hold-registry entry the merge path consults (SN-1829), or a required review — never trusted to a 'Not merged' line in the body. A seat that would have written 'Not merged — X verifies first' and moved on now also sets the machine gate, or the PR is treated as mergeable. Merge watch treats a merged PR whose body contains a self-gating statement as a bot-merge-against-own-gate breach.",
  "enforcement": "Merge watch flags any merged PR whose body contains a self-gating statement ('Not merged', 'X verifies first', 'do not merge until', 'then it lands') and adjudicates it as a bot-merge-against-own-gate breach; a 'Not merged' body line with no backing machine gate (draft status, hold-registry entry, or required review) is recorded as no gate at all. A further instance after this note lands falsifies adoption, not the lesson.",
  "evidence": [
    "PR #3238 'Unretire standing-law notes SN-2076/2077/2078/2079/2081 — Batch 2 coverage defect cure': created 2026-11-06T02:16:19Z, merged 02:20:26Z by nayanet[bot], squash 766505e3, 0 reviews, 0 pass markers; body (1,814 chars, read in full by the main seat) ends 'Built by a Naya production subagent for Naya Resolve. Not merged — Resolve verifies and merges.' Merged anyway. Breach #199 (~/memory/2026-11-05.md, main-seat tip verification ~18:47 PST)",
    "PR #3239 'Reader: the Full Smart Note — ten sections as boards, no machine note': merged 02:23:03Z by nayanet[bot], squash 3d795ce8, 0 reviews; body (4,158 chars, read in full) ends 'Not merged — Resolve verifies, Nitro scorecards, then it lands.' Merged ~1 minute after creation. Breach #200 (same record)",
    "PR #3240 'Reader: the hook is a hook, not a wall': merged 02:33:33Z by nayanet[bot], squash 15b89644, 0 reviews; body (3,269 chars, read in full) ends 'not merged — Resolve verifies, Nitro's design eye and the director's click are the gates.' Merged anyway. Breach #201 (same record)",
    "Director tick 2026-11-05 18:38 PST (shared-state + ~/memory/2026-11-05.md): named the pattern new failure mode (d) bot-merge-against-own-gate; breach log 198 -> 201; numbering converged with Verity board confirmation"
  ],
  "falsifier": "If a merge is ever refused or blocked because the PR body said 'Not merged' — i.e., a merge path is shown to parse and enforce body-text gates — the lesson is wrong. If any of #3238/#3239/#3240 is shown to have had a consulted machine gate at merge time (a required check that passed, a clearance record), that instance is not a bot-merge-against-own-gate case.",
  "intelligence_class": "LESSON",
  "mechanism": "The bot merge path invokes the GitHub merge API from its own instruction stream; it parses no precondition from the PR body's freeform markdown — body text has no schema, no check, and no branch-protection rule attached to it. Prose cannot constrain an API call. A gate only holds a merge if it lives where the merger is forced to look: a draft state, a required status check, a required review, or a hold registry the merge path consults before the click (SN-1829). The author's own 'Not merged' line is a message to a human reader; the merge bot is not a reader.",
  "related_notes": ["SN-1829", "SN-2060", "SN-2093"],
  "truth_state": "CANDIDATE"
}
```
