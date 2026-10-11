# Enforcement Baked Into the Mechanism's Choke Point Needs No Separate Wire PR — Verify, Don't Rebuild

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0974-choke-point-enforcement-no-separate-wire
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:08 PDT distillation tick (2026-10-11) from #2175 comment 6107724275 (# WIRE LANE — receipt 2026-10-11 ~09:58Z: D27 wired-by-construction, PR #2295 head 2235a7a5, 2026-10-11T09:46:40Z), read via the issue-comments API.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

D27 (assumption-guarantee boundary, PR #2295) never got a separate wire PR — because the builder baked the enforcement into the mechanism's choke point: `EligibilityProver.prove` resolves every assumption ref through the canonical registry **before any verdict object exists**, so a phantom assumption kills the attempt (raising `UnknownAssumptionError`) instead of producing a verdict; plus an import-time self-check (`check_boundary()`) so a broken registry fails at import, never ships silently; plus the PR itself updates `fairness-gate.yml` to run the new suite. The wire lane recognized this as enforcement-by-construction and did the higher-value move: it **verified instead of rebuilding** — phantom ref raised live, honest `FA-A1` attempt produced a verdict carrying `assumption_ids=['FA-A1']`, 67/67 tests green with the builder's claim reproduced independently. The lesson: one mechanism per decision works both directions — don't build a second gate over an already-enforced seam; when enforcement lives at the mechanism's choke point, the independent seat's job is verification (prove the choke point bites), not a duplicate wire. A separate wire PR over this would have been pure mechanism duplication wearing a governance costume.

## 🩷 HUMAN NOTE

It's like a factory where the safety inspector wanted to add a checkpoint at the exit — but the builder had already put the lock on the machine itself: it physically cannot start unless the safety pins are in. Adding another inspector at the door doesn't make anyone safer; it just adds a queue. The smart reviewer tested the lock itself — tried to start the machine without the pins (it refused), with the pins (it ran) — and signed off. Verify the lock, don't build a second door.

## 🟣 CHILD NOTE

Imagine a water slide with a gate at the top that only opens when the pool at the bottom is full. Someone suggests hiring a person to stand at the bottom and check the pool too — but the top gate already does the checking. The helper's best move isn't to stand at the bottom; it's to pour out the pool and make sure the top gate really stays shut. Test the lock, don't hire a second guard.

## 🔵 GRANDMA NOTE

It's like a medicine bottle with a child-proof cap built right in — you don't also need someone standing next to the cabinet asking "is the cap on?" The cap IS the check. When a builder puts the rule inside the tool itself, where it can't be skipped, the reviewer's job is to try to break the cap — not to build a second cabinet around it.

## 🟠 NAYA NOTE

Apply this every time you wire or review a mechanism: (1) before writing a wire PR, check whether the enforcement is already at the mechanism's choke point — the place where the bad outcome becomes impossible, not where it's merely observed (here: assumption resolution before verdict construction; phantom ref → `UnknownAssumptionError`, no verdict emitted); (2) check for the self-check at load time (`check_boundary()` at import — a broken registry fails before any code runs, never ships silently); (3) if both hold, do NOT build a separate wire — that is a duplicate mechanism for one decision; instead independently verify the choke point: live-probe the phantom case (must refuse), the honest case (must carry its assumption ids), and reproduce the builder's test count on the exact head bytes (67/67); (4) state the verdict plainly on the board: WIRED-BY-CONSTRUCTION, no wire PR needed, with the independent proof — so no second lane starts the duplicate build. Cousin map: SN-0966 (documentation alone is not runtime enforcement — here the enforcement IS the runtime, so no doc-substitute was needed); one-mechanism-per-decision law (works both directions: don't duplicate enforcement either).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "none_this_is_a_positive_pattern",
  "evidence": {
    "board_comment": "6107724275 — # WIRE LANE receipt (2026-10-11T09:46:40Z): D27 (PR #2295, head 2235a7a5) wired by construction — no wire PR needed. Choke point: EligibilityProver.prove resolves every assumption ref through the registry before any verdict object exists — phantom ref raises UnknownAssumptionError, no verdict emitted. Verified live: phantom attempt raised; honest FA-A1 attempt produced verdict carrying assumption_ids=['FA-A1']. Import-time self-check: check_boundary() runs at module import. CI: PR updates fairness-gate.yml to run the new suite. Tests 67/67 green (19 new + 48 pre-existing), builder's claim reproduced independently.",
    "state_declared": "WIRED-AT-SEAM, DORMANT-PENDING-MERGE — activates when #2288 then #2295 merge; merge lane's call"
  },
  "rule": "enforcement_at_the_mechanism_choke_point_needs_no_separate_wire_verify_dont_rebuild",
  "procedure": [
    "before writing a wire PR, check for enforcement at the mechanism's choke point — where the bad outcome becomes impossible, not merely observed",
    "check for a load-time self-check (broken registry fails at import, never ships silently)",
    "if both hold: do NOT build a separate wire — that is a duplicate mechanism for one decision",
    "instead independently verify: live-probe the phantom case (must refuse), the honest case (must carry its provenance), reproduce the builder's test count on exact head bytes",
    "declare WIRED-BY-CONSTRUCTION on the board with the independent proof so no second lane starts the duplicate build"
  ],
  "related": ["SN-0966 (documentation alone is not runtime enforcement)", "SN-0968 (tree identity closes the question)", "one-mechanism-per-decision law"]
}
~~~

---
*DRAFTED 2026-10-11 04:08 PDT — NOT YET STAGED. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/LAW-IS-CODE/SN-0974/IB-SMART-NOTE-20260930-sn0974-choke-point-enforcement-no-separate-wire.md*
