# When Two Lanes Claim One Number: The Collision Arbitration Rule

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0372-sn-collision-arbitration-rule
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5999003422 ([ARBITRATION] SN-0355 collision resolved — Naya 4 ruling, 2026-10-05T16:49:56Z / 09:49 PDT). The collision: two unrelated notes both numbered SN-0355 — Naya 2's NONSTOP LOOP operating code (merged to main: `BRAIN/05-MEMORY/SMART-NOTES/2026/10/05/.../SN-0355/IB-SMART-NOTE-20261005-sn0355-nonstop-loop.md`) vs Naya 4's malformed-first-shelves-batch R8 boundary (staged on draft PR #1229 only, unmerged). Relay: #1354 5999007428 (Naya 2 received the ruling). Prior application of the same rule: SN-0343 (renumbered from SN-0341 per the distillation worker's first-claim).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Prevention (the AGENTS.md rule: pre-claim collision scan before taking a number) works until two lanes work fast enough that it doesn't. On 2026-10-05, SN-0355 was claimed twice for two unrelated lessons. The arbitration ruling:

**The merged note keeps the number. The draft renumbers. No exceptions.**

Rationale, in the ruling's own words: main is canonical. The merged note is CI-referenced (registry + brain-index) and director-pushed; a repair on that note was in flight on main at arbitration time. Renumbering a merged, referenced note mid-repair to accommodate a draft would be reckless — you would move the number under live machinery.

**Executed exactly:**

1. The draft note renumbered SN-0355 → SN-0366 on the staging branch (commits `00c2efac` new path, `a23c933a` old path removed). Content unchanged — a renumber is a move, never an edit.
2. Arbitration provenance recorded in the renumbered note's header — the number change is documented where the note lives, so a future reader tracing SN-0366 finds the full lineage instead of a mystery.
3. The learn system renamed every derived anchor: ledger entry renamed, `learn/lessons.md` anchor → SN-0366, receipt renamed. No double-ingest — the note's identity moved as one unit, not as fragments that could re-collide.
4. The counter advanced to 366.
5. The other lane was invited to flag disagreement on the board, with the old path restorable from `a23c933a^` — the ruling is reversible by design, and the dissent channel is explicit, not assumed.

Note what the ruling is NOT: it is not "first in time wins." If the earlier claimant were the draft and the later claimant the merge, the merged note would still win — canonicality decides, not timestamps. (SN-0343's earlier renumbering went by the first-claim variant because both claims were drafts; the rule generalizes: the strongest canonical holder wins.) And it is not an apology: renumbering is a routine, reversible operation; what matters is that it happens in the right direction and leaves a full paper trail.

Why this is brain-grade: a cold Naya will hit this again — parallel lanes, fast ticks, a shared counter that races. This note teaches the three-part doctrine: **prevent** (pre-claim scan on board + open Smart Note PRs, first claim stands), **arbitrate** (canonical/main-merged holder keeps the number, draft renumbers), **repair atomically** (move unchanged, record provenance in the header, rename every derived anchor, keep the revert pointer, invite dissent on the board). The collision itself is a coordination event; the doctrine turns it into five minutes of bookkeeping instead of a broken registry.

## 🩷 HUMAN NOTE

Shawn — a quick coordination note from the lanes: two notes both ended up numbered SN-0355 today (Naya 2's Nonstop Loop code, which is already merged to main, and one of mine that was only staged on the draft branch). Ruling: the merged one keeps the number — main is canonical, and it was mid-repair on main at the time, so moving its number would have been reckless. My draft renumbered to SN-0366, content untouched, provenance in the header, learn-system entries renamed so nothing double-ingests. Reversible by design, and she was invited to flag disagreement on the board. Prevention (the pre-claim scan) usually works; this is the rule for when it doesn't: canonical wins, draft renumbers, paper trail everywhere.

## 🟣 CHILD NOTE

Imagine two kids at school both get assigned locker number 355 — one already moved all her stuff in and has her name on the door, the other's locker is still empty and just written on a sign-up sheet. The rule is simple: the kid who already moved in keeps 355. The other kid takes a new locker, moves her sign-up sheet unchanged, writes on it "I used to be 355," and tells everyone who has a copy of the old sheet so nothing gets confused. And she can say "I disagree" out loud — nobody just takes someone's locker quietly. Keep the number with the one who's actually moved in; keep a paper trail for everyone else.

## 👵 GRANDMA NOTE

It's like two houses getting the same street address by clerical error. One family has already moved in, registered with the post office, and has deliveries arriving. The other is still just a plan on paper. You don't change the moved-in family's address — you'd break every delivery route. You give the paper one a new address, note the old one for the record, and notify everyone who had the old paperwork. The principle: the number belongs to whoever is actually living at it, and every change is recorded so nobody's confused later.

## 💜 NAYA NOTE

Note to future me: when a number collision lands, do not debate seniority or timestamps — check canonicality: merged-to-main (registry + brain-index referenced) always beats draft-staged. Then execute the move as a pure rename (new path commit, old path removed, content byte-identical), record arbitration provenance in the renumbered note's header, rename every derived anchor in the learn system (ledger, lessons.md, receipts) so nothing double-ingests, advance the counter past the renumbered number, and post the ruling on the board with the revert pointer (`<old-path-remove-commit>^`) and an explicit invitation to disagree. The dissent channel is part of the doctrine — a ruling with no appeal path is just power. Cross-reference: AGENTS.md pre-claim scan (prevention), SN-0343 (first-claim variant between two drafts).

## ⚙️ MACHINE NOTE

{"sn": "SN-0372", "title": "When Two Lanes Claim One Number: The Collision Arbitration Rule", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LANE-COORDINATION"], "extends": [], "related": ["SN-0343", "SN-0366"], "evidence": {"board": "#1354 5999003422 ([ARBITRATION] SN-0355 collision resolved, 2026-10-05T16:49:56Z): two unrelated notes both numbered SN-0355 — Naya 2's NONSTOP LOOP (merged to main BRAIN/05-MEMORY/SMART-NOTES/2026/10/05/.../SN-0355/..., CI-referenced, director-pushed) vs Naya 4's malformed-first-shelves-batch (draft PR #1229 only). Ruling: merged keeps SN-0355 (main is canonical; renumbering a merged note mid-repair reckless). Executed: draft -> SN-0366 (commits 00c2efac new path, a23c933a old path removed), content unchanged, arbitration provenance in header, learn ledger + lessons.md + receipt renamed, no double-ingest, counter -> 366; Naya 2 invited to flag disagreement (restorable from a23c933a^); relay 5999007428", "prior_application": "SN-0343 renumbered from SN-0341 per distillation worker's first-claim (both drafts)"}, "rule": "identity collisions resolve in favor of the strongest canonical holder (merged-to-main beats draft-staged; canonicality decides, not timestamps or seniority); renumber is a pure move with arbitration provenance in the header, every derived learn-system anchor renamed atomically, revert pointer posted, explicit dissent invitation on the board"}
