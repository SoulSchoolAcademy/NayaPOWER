# Propose-then-Build — Touching Another Lane's In-Flight Work

**Intelligent Block:** IB-SMART-NOTE-20261001-sn105-propose-then-build
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn's standing directive (2026-10-01, #554 `5942150726`): everything on #554 — **starting** something → one line (what, why, branch/PR); **finishing** something → what landed, exact artifact, what it means; **finding** something not-right → finding law, surface + evidence, no burying; **touching another lane's in-flight work** → propose on #554 first, get agreement, then build. Born live the same day: 8 commits landed on `naya4/hub-intelligence-projections-v1` from another lane without a heads-up. The content was benign and verified (full diff reviewed), so the seat merged and moved forward — with one light process note: next time, a one-line #554 proposal before pushing keeps everyone's trust intact.

## 🩷 HUMAN NOTE

Someone walked into your workshop and improved your project while you were out — the improvements were good, but you only found out when you saw the new paint. You kept the improvements (they were solid), said "nice work, but knock next time," and the boss made "knock first" an official rule. That's the whole note: **knock before you touch someone else's work.** One sentence on the board — "I'm going to add X to your branch because Y, okay?" — costs ten seconds and saves every drop of trust. The review still happens: the owner reads the whole diff before merging, every time.

## 🟣 CHILD NOTE

Two friends are building a tower. One friend wants to add blocks to the other's side. The rule is: say "can I add these blocks to your side?" and wait for "yes" before touching. Even if the blocks are perfect, you ask first — because the tower is theirs, and asking is how friends stay friends.

## 🔵 GRANDMA NOTE

There's an old courtesy: you don't rearrange someone's kitchen without asking, however good your intentions. If you must — say what you'd change and why, get the nod, then do it. And when someone rearranges yours unasked but well, you accept the gift, say thank you, and gently restate the rule. That is exactly what happened here: the work was kept, the rule was named, and nobody's feelings were hurt because the note was light and the trust was real.

## 🟠 NAYA NOTE

Cross-lane branch writes are a trust operation, not a code operation. The protocol, four event types, all on #554:

1. **STARTING** — one line: what, why, which branch/PR. Before the work, not after.
2. **FINISHING** — what landed, the exact artifact (branch/commit/PR/test counts), what it means. A receipt, not an announcement.
3. **FINDING** — the finding law: surface + evidence on #554, no burying. Findings are board events.
4. **TOUCHING another lane's in-flight work** — propose on #554 first, get agreement, then build. The proposal is one line: what you'd change, why, which branch. The owner reviews the FULL diff before merging (Naya 4 reviewed all 8 commits), however benign it looks.

The failure mode this fixes: silent cross-lane commits that the owner discovers at merge time. The repair when it happens anyway: keep the benign work, verify it fully, post the light process note naming the rule — no punishment, norm stated. Note the asymmetry with SN-104's flag-don't-override: flagging is for *findings about* a lane; proposing is for *writes into* a lane. Both protect the same thing — lane ownership — at different depths.

## 🟢 MACHINE NOTE

~~~json
{
  "adoption_decision": "ADOPT_AS_COORDINATION_PROTOCOL",
  "authority": "Shawn Vibert (Human Director), standing directive, issue #554 comment 5942150726, 2026-10-01",
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "Observed once, 2026-10-01. The triggering friction was benign (verified sound, merged). Unproven: a hostile or sloppy cross-lane push, whether 'agreement' requires an explicit board reply vs silence-as-consent, and the timeout after which silence counts. Treat silence as NOT consent until the team rules otherwise.",
  "event_types": {
    "FINISHING": "what landed + exact artifact (branch/commit/PR/test counts) + what it means",
    "FINDING": "finding law: surface + evidence on #554, no burying",
    "STARTING": "one line: what, why, which branch/PR",
    "TOUCHING_ANOTHER_LANES_WORK": "propose on #554 first, get agreement, then build"
  },
  "intelligence_class": "SEAT_COORDINATION_PROTOCOL",
  "owner_reviews_full_diff_before_merge": true,
  "verdict_projection": "PREFER_EXPLICIT_PROPOSAL_OVER_SILENT_WRITE"
}
~~~

## 🟢 LEARNING LESSON

"Benign and verified" is the luckiest possible outcome of a silent cross-lane write — and it was still worth one process note. The lesson: protocol is not punishment for bad intent; it is the thing that lets good intent be *seen* as good intent. The one-line proposal costs nothing and converts "who touched my branch?" into "thanks for the help." Also: when the friction is benign, the note stays light — heavy process for a verified-sound contribution would teach seats to hide their help instead of proposing it.

## 🟡 WHAT IT MEANS

Every seat now has a four-line board ritual for the whole lifecycle of work: start, finish, find, touch. The next time a seat wants to improve another lane's in-flight branch, it posts the one-line proposal first and waits for agreement. It pairs with SN-103 (same-path collisions — the mechanical case) and SN-104 (same-purpose duplication — the canonicality case) as the third coordination primitive: **same-branch writes**. Between the three, the seats have a named protocol for every way two lanes can step on each other.

## ⚪ WHAT'S IN IT FOR YOU

No more discovering someone else's commits on your branch at merge time. No more trust erosion from well-meaning silent help. The board trail (5941810483 → 5941910955 → 5941960535 → 5942117122 → 5942139930 → 5942150726) becomes a complete, auditable lifecycle of the Hub intelligence lane — any future seat can replay exactly what happened, who decided what, and under which rule.

## 🟨 HOW TO APPLY / HOW TO USE

Before pushing to (or opening a PR against) another seat's in-flight branch: post one line on #554 — the change, the reason, the branch — and get the owner's agreement. Then build. When you finish anything: post what landed with exact artifacts. When you find something not-right: post the finding with evidence. When you start something: post the one-liner. If someone skips the proposal and the work is sound: verify the full diff, merge, post the light process note, move on.

## 🔗 HOW IT CONNECTS

- **EXECUTES** → Shawn's standing directive, issue #554 comment 5942150726 (this note is its retrievable projection, not a second source)
- **PAIRS WITH** → SN-103 — Rename-Race Collision Protocol (same-path collisions)
- **PAIRS WITH** → SN-104 — Converge by Withdrawal (same-purpose duplication; flag-don't-override is the finding-side twin of propose-then-build's write-side)
- **REFINES** → SN-057 — Cross-Seat Handoff Protocol
- **SUPPORTS** → SN-017 — Seat Coordination Protocol

## 🧭 KEY DECISIONS / PRINCIPLES

- Proposing is cheaper than unpicking — one line before, not one incident after.
- The lane owner reviews the full diff before merging cross-lane commits, however benign they look; trust is verified, not assumed.
- Benign intent gets a light note, not a penalty — heavy process for sound contributions teaches seats to hide help.
- Silence is NOT consent: agreement must be an explicit board reply until the team rules otherwise.
- Flagging (findings about a lane) and proposing (writes into a lane) protect the same ownership at different depths — know which one you're doing.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "8 unverified cross-lane commits on naya4/hub-intelligence-projections-v1, 2026-10-01",
  "observed_by": "Naya 2 relay seat",
  "receipts": {
    "naya4_merges_note": "issue #554 comment 5942139930 — '#1276 + #1279 MERGED (Shawn's word)', main 5885459af8; 8 commits from another lane reviewed (full diff), verified sound: rename decision ✅, stale decision removed, #554 finding law added, NAYA/PROOF/FEATURES projections + design intelligence standard added, door-honesty structure preserved, JSON valid; light process note posted",
    "director_standing_directive": "issue #554 comment 5942150726 — 'SHAWN'S DIRECTIVE — EVERYTHING ON 554 (standing)': starting/finishing/finding/touching protocol",
    "main_head_after_merges": "5885459af85bcbaede4480557413ae9c681028a1 (merge of c45db9450c + cbaf6a40b6)"
  },
  "resolution_note": "Work kept, rule named, trust intact — no director tie-break needed.",
  "truth_ceiling": "CANDIDATE — single observed instance; silence-as-consent rule unresolved"
}
~~~

## ⚠️ NON-CLAIMS

- Not proven against a sloppy or hostile cross-lane push — only the benign case was observed.
- "Get agreement" is unresolved on mechanics: explicit board reply vs silence-as-consent, and any timeout. Until ruled, silence is NOT consent.
- The light-note repair assumes the lane owner actually reviews the full diff — if review is skipped, the protocol degrades to notification.
- This note projects Shawn's directive for retrieval; the directive itself (5942150726) remains the authority, not this file.
