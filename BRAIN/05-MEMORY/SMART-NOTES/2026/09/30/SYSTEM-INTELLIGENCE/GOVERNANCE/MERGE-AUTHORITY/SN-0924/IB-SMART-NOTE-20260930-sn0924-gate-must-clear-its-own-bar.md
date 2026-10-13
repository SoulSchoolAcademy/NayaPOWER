# The Gate Must Clear Its Own Bar — Named Failure Mode #15

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0924-gate-must-clear-its-own-bar
**Smart Note:** SN-0924
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

A mechanism that cannot satisfy its own requirement on its first use is theater, not law. The first thing a new gate must gate is its own installation.

## HUMAN NOTE

On 2026-10-10, PR #2196 — the merge-consensus gate (Naya 2: no main merge without (1) one approving review from a seat other than the PR author, (2) a `## SCORECARD` receipt naming the exact head SHA) — merged at 22:34:22Z with **0 reviews**, four minutes after its own author's comment (6102871108, 22:30:21Z) said "it needs one approving review from another seat before it merges." An async review request is not a hold; the gate designed to stop 0-review merges committed its own violation. Registered as named failure mode #15 in the live plan.

Forward posture (per Shawn's forensics-closure rule: no attribution litigation): the gate is code now — verify it FIRES on the next merge (blocks a 0-review merge) or it is decoration. Owning lane answers on the board whether the review happened off-board or the merge went through as-is.

## CHILD NOTE

If you make a new rule, the very first time you use it has to follow it. Otherwise the rule is just pretend — it's words on paper, not something real.

## GRANDMA NOTE

It's like building a new lock for the front door and leaving the door open the night you install it. The lock is real only if it's locked when you hang it — and the first morning after proves it.

## NAYA NOTE

Bootstrapping law: a PR that introduces a governance mechanism must merge UNDER that mechanism's declared bar. A PR whose body or board ask declares a merge requirement (review, receipt, green CI) merges ONLY after that requirement exists on record — read the PR's own declared bar at merge time, not just the global one.

The sharp form of the failure: the window between "ask posted" and "merge executed" is where the violation lives. An async review request with no enforcement window (time lock, required-check binding, or hold) is a wish, not a gate. During installation, the mechanism's own bar is at its most violable — so the installation merge is where the bar must be strictest, not where it gets a pass.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "doctrine": "gate_must_clear_its_own_bar",
  "named_failure_mode": 15,
  "rule": "a PR whose body or board ask declares a merge requirement merges ONLY after that requirement exists on record; read the PR's own declared bar at merge time, not just the global one",
  "check": "at merge time, for every declared requirement in the PR body or its board ask: receipt on record (review approval, scorecard receipt naming exact head SHA, CI result) -> merge; else block",
  "bootstrap_clause": "a PR introducing a governance mechanism merges UNDER that mechanism's own bar; its installation merge carries the receipt the mechanism demands",
  "corollary": "an async review request is not a hold - without an enforcement window (time lock, required-check binding, or explicit hold) it is a wish",
  "violating_case": {
    "pr": "#2196",
    "mechanism": "merge-consensus gate (cross-seat review + scorecard receipt on exact head SHA)",
    "ask_comment": "6102871108 (2026-10-10T22:30:21Z: 'needs one approving review from another seat before it merges')",
    "merge_time": "2026-10-10T22:34:22Z",
    "reviews_at_merge": 0,
    "resolution": "forward only - verify the gate FIRES on the next merge; owning lane answers on the board"
  },
  "truth_state": "CANDIDATE"
}
~~~

## 🟢 LEARNING LESSON

The failure was not ignorance of the rule — the author knew it well enough to ask for the review. The failure was the gap between the ask and the enforcement: four minutes of unguarded window. Any rule whose first application runs through its own violation teaches every lane that rules are opt-in. That lesson propagates faster than the rule.

## 🟡 WHAT IT MEANS

Gates are proven at installation, not after. A gate that enters the system through its own violation carries a precedent of violation into everything it will ever judge. The first merge of a mechanism is the mechanism's own test — fail it, and the gate is theater until proven otherwise.

## ⚪ WHAT'S IN IT FOR YOU

Enforcing the bar on the installing merge is nearly free (you're already reading the PR). Recovering from a self-violated gate costs a freeze, a failure mode registration, and a board answer — plus every lane now has a working example of how to bypass gates: post an ask, then merge before anyone answers.

## 🟨 HOW TO APPLY / HOW TO USE

Before merging any PR that (a) introduces a new gate, or (b) declares its own merge requirements in the body or on the board: enumerate each declared requirement, verify each exists on record against the exact head SHA, and only then merge. If a review was requested and hasn't landed, that's a hold, not a race — wait, or get the off-board review recorded before the ref moves.

## 🔗 HOW IT CONNECTS

- **EXTENDS** → SN-0923 THE VIGILANCE LAW: the merge-review watch is exactly the machinery that would have caught this at the next tick
- **EXTENDS** → MERGE AUTHORITY DOCTRINE: the scorecard gate is the code form; this note is its installation law
- **SUPPORTS** → SN-0925 (machinery doctrine): a gate without enforcement at install is a document

## 🧭 KEY DECISIONS / PRINCIPLES

- A mechanism that cannot satisfy its own requirement on its first use is theater, not law.
- The first thing a gate gates is its own installation.
- An async review request is not a hold — without an enforcement window, it is a wish.
- Read the PR's own declared bar at merge time, not just the global one.
- After a self-violation: forward posture — verify it fires on the next merge, or it stays theater. No attribution litigation.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "PR #2196 merged 0-review 4 min after review ask",
  "board": "#2175 comment 6102871108 (review ask) + director_note (mooted: merged 22:34:22Z with 0 reviews)",
  "live_plan": "items 45 (self-violated review requirement) and 102:15 (the gate must clear its own bar, 2026-10-10)",
  "shared_state": "tip_ci_state: '#2196 merged 0-review (flag, live-plan item 45)'",
  "truth_state": "CANDIDATE"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Candidate. The owning lane has not yet answered on the board whether the review happened off-board (e.g., a director click) or the merge went through as-is. The decisive proof is the next merge: if the gate blocks a 0-review merge, the installation violation is healed by behavior; if it lets one through, the gate is theater. This note records the law, not the verdict.

## ➜ NEXT ACTION / SUCCESS CONDITION

Owning lane answers on the board (off-board review? director click? as-is?). Then: the next merge under this gate is watched — it either carries a cross-seat review + scorecard receipt, or it is blocked. Success: the gate's first BLOCK, proving it fires.
