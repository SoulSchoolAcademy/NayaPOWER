# The Loop Checks the Board Before It Executes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0194-loop-checks-the-board-before-it-executes
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5954468079 (Naya 4, 2026-10-02 14:17:21Z) — the dedupe post: self-build loop's 07:03 cycle rebuilt Room 01 in parallel with Naya 4's director-assigned rebuild; `#1327` closed, `#1328` stands as the single Room 01 vehicle; and `#554` 5954617393 (Naya 2 relay, 2026-10-02 14:26:37Z) — relay verification of the clean close plus: "Your loop's new no-duplicates guard (check `#554` for in-flight builder claims before Execute) — good law, matches the standing rule. Logged."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two Room 01 rebuilds flew at once: the self-build loop's 07:03 cycle (PR `#1327`, branch `naya4/room-01-feed-v2`) and Naya 4's director-assigned rebuild (PR `#1328`, branch `naya4/room-01-main-stage-v2`). Both were legitimate work launched in good faith; together they were duplicate in-flight work, against the team law (SN-0108: one change, one PR; SN-0117: converge by scored selection). The dedupe was clean and public: `#1327` closed with rationale on the PR, `#1328` kept as the single vehicle, the superseded branch preserved intact, its quality-bar ideas logged as fold-in candidates for after the verdict — rehomed, not destroyed.

The structural fix is the real capture: the loop spec now carries a no-duplicates guard — **check `#554` for in-flight builder claims before Execute**. An autonomous loop cannot rely on memory of what was assigned; the board is the single place where in-flight work is announced (SN-0109: everything on 554), so the pre-execute step reads the board like a registry. Naya 2's relay confirmed it as standing law, not new law: "good law, matches the standing rule."

Why it belongs in the brain: every future loop, lane, or cold successor that executes builds will face the same race — scheduled work colliding with director-assigned work, both invisible to each other except through the board. The guard is cheap (one board scan per cycle), and the cost of skipping it is two reviewed builds instead of one, doubled director attention, and a public dedupe. Four corollaries: (1) the dedupe itself must be explicit and public — closed PR with rationale, single vehicle named on the board; (2) nothing gets destroyed in a dedupe — losing work is rehomed as fold-in candidates, per the owner-canon discipline (SN-0116); (3) the board scan must cover in-flight *claims*, not just merged state — the race window is the open PR; (4) the relay seat can verify the close independently (open state, branch head intact), which is what makes the dedupe trustworthy rather than asserted.

## 🩷 HUMAN NOTE

Shawn — the loop and I both rebuilt Room 01 at once, because the loop couldn't see your director-assigned work. Caught openly, deduped publicly: `#1327` closed with its rationale, `#1328` is the single vehicle, nothing destroyed. The loop spec now has a guard: it reads the board for in-flight builder claims before it executes anything. An autonomous system must check the registry before it acts, not after it collides.

## 🟣 CHILD NOTE

Imagine two cooks in the same kitchen both starting to make dinner — because neither asked "is anyone already cooking?" Now before cooking, the loop always checks the big board on the wall where everyone writes what they're making. Two cooks, one dinner, no wasted food — and the board always tells the truth about who's doing what.

## 👵 GRANDMA NOTE

Two people started the same job at the same time because neither looked at the shared list first. The fix is simple and permanent: before starting any job, check the shared list for who's already working on it. Cheap to do, expensive to skip. The duplicate job was closed politely, with a note explaining why, and its good ideas were saved for later instead of thrown away.

## 🤖 NAYA NOTE

Before any loop Execute step: scan `#554` for in-flight builder claims (open PRs and announced sign-ins), then act. If a collision is found, dedupe openly: close the duplicate vehicle with rationale on its PR, name the single surviving vehicle on the board, preserve the closed branch intact, and log its salvageable ideas as fold-in candidates. Have the relay seat independently verify the close (PR state unmerged, branch head unmoved) — the dedupe is evidence-backed or it doesn't count. This is the standing one-change-one-PR law (SN-0054/0108/0117) operationalized as a pre-execute read, and the audit lane has already confirmed it matches the rule.

## ⚙️ MACHINE NOTE

{"sn": "SN-0194", "title": "The Loop Checks the Board Before It Executes", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATING-MODE", "DIRECT-LANE-COLLABORATION"], "extends": ["SN-0054", "SN-0108", "SN-0109", "SN-0116", "SN-0117"], "evidence": {"collision": "#554 5954468079 — self-build loop 07:03 cycle rebuilt Room 01 in parallel with the director-assigned rebuild (#1327 vs #1328)", "dedupe": "#1327 closed with rationale on the PR; #1328 named the single Room 01 vehicle; branch naya4/room-01-feed-v2 preserved; quality-bar ideas logged as fold-in candidates", "guard": "loop spec now carries no-duplicates guard: check #554 for in-flight builder claims before Execute", "relay": "#554 5954617393 — Naya 2 independently verified the clean close (head e71a4c5f intact) and confirmed the guard matches standing rule"}, "rule": "autonomous execution begins with a board read: no Execute step fires without a #554 scan for in-flight builder claims; collisions are deduped openly, nothing destroyed"}
