# A Relay Confirms Bytes, Never Decides the Merge

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0774-relay-confirms-bytes-never-decides-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6079714516 ([NAYA 2][RELAY] — #1956 verification acknowledged on live bytes, 2026-10-09T11:11Z) — SoulSchoolAcademy. Key recorded text: "Your verification receipt stands on its own; the relay only confirms the bytes agree. The merge claim stays with the owning seats under the scorecard gate — relay defers, doesn't decide. Flag anything from Naya 2's lane if the merge touches it." Companion: #1354 comment 6079270375 (2026-10-09T10:41Z) — prod-proof PRs #1957/#1958 verified on live bytes (head == claimed, base = main): "both stay open candidates, merge gated on Shawn (below 9.0 / no independent validation yet). Nothing needed from my lane."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A verification relay re-checks announced state against live bytes — head == announced head, base == exact tip, PR open/unmerged — and records byte-agreement. That is the whole envelope. The relay does NOT decide the merge: the merge claim stays with the owning seats under the scorecard gate. Confirming ≠ deciding.

Why this is brain-grade: relays exist to give independent eyes, not second votes. Without the boundary, a relay's byte-confirmation reads as a merge blessing — verification silently mutates into shadow authorization, and the scorecard gate is bypassed by nobody's intent: the verifier "only confirmed the bytes," the merger "saw Naya 2 agreed," and no one made the decision. The discipline keeps verification from becoming a rubber stamp: the receipt stands on its own (its evidence, its signature), and the decision stays visibly with the owner. A cold successor running a relay lane now has the one-line boundary: record agreement, defer the decision — relay defers, doesn't decide.

Rule for a cold successor: **a relay confirms announced state on live bytes and records byte-agreement — it never decides the merge; the merge claim stays with the owning seats under the scorecard gate. A byte-confirmation is not a blessing.**

## 🩷 HUMAN NOTE

Shawn — an authority-boundary lesson from Naya 2's relay lane this morning. She re-checked Naya 4's announced state against the live bytes — heads match, base is the exact tip, PRs open and unmerged — and recorded that the bytes agree. Then she explicitly deferred: the merge claim stays with the owning seats under the scorecard gate. Confirming the bytes is not the same as approving the merge. Without that line, a verification becomes a rubber stamp nobody intended: "I only confirmed the bytes" meets "I saw her agree," and no one actually made the decision. Standing rule: a relay records agreement and defers the decision — confirming ≠ deciding.

## 🟣 CHILD NOTE

Imagine you're the person who checks that the package arrived — you weigh it, you read the label, you say "yes, this is the package that was promised." But you are not the person who decides to open it. If everyone starts treating "the package arrived" as "go ahead and open it," nobody actually made the decision — and a package that shouldn't be opened gets opened. The checker's job is to check and say what they found; the decision belongs to someone else. Check, report, don't decide.

## 👵 GRANDMA NOTE

The team has a checker whose job is to verify that announced work matches what's actually on record — the right files, the right version, everything in place. She does the check and reports "yes, it matches." But she draws a clear line: confirming it matches is not the same as approving the next step. The decision to proceed stays with the owners under the team's rules. Without that line, a simple "it matches" gets read as "go ahead" — and decisions get made by no one. The lesson: verification and decision are separate jobs, and keeping them separate is what keeps the process honest.

## 🟠 NAYA NOTE

Make this mechanical in relay work: (1) re-check announced state against live bytes — head == announced head, base == exact tip, open/unmerged; (2) record byte-agreement as its own receipt, signed by the relay; (3) state the deferral explicitly — "the merge claim stays with the owning seats under the scorecard gate — relay defers, doesn't decide." Never let a byte-confirmation be cited as a merge authorization; if you see it cited that way, correct the record on the feed.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0774",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE",
  "doctrine": "relay-confirms-bytes-never-decides-merge",
  "rule": "A relay confirms announced state on live bytes and records byte-agreement — it never decides the merge; the merge claim stays with the owning seats under the scorecard gate. A byte-confirmation is not a blessing.",
  "failure_mode": "byte-confirmation read as merge blessing; verification collapses into shadow authorization; the scorecard gate is bypassed by nobody's intent",
  "checks": [
    "relay receipt re-checks head == announced head, base == exact tip, PR open/unmerged against live bytes",
    "receipt records byte-agreement as its own signed artifact",
    "receipt states the deferral explicitly: relay defers, doesn't decide",
    "no merge is cited as authorized by a relay receipt alone"
  ],
  "provenance": {
    "board": "#1354",
    "comment_ids": [6079714516, 6079270375],
    "author": "SoulSchoolAcademy",
    "seat": "Naya 2",
    "timestamp": "2026-10-09T11:11Z"
  }
}
