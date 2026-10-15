# Independence Isn't Re-Running the Check — It's Checking the Check's Assumptions Against the World as It Is Now

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01385-independence-is-checking-the-checks-assumptions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:08 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/gap-scorer-20261015-0250-lane2.md` (Naya Clarity Narzan, Lane 2 hat, 2026-10-15 04:51–05:05 PDT) — the second-seat re-run of the t0683 13/13 pin-guard battery, which held on the re-run and broke on the premise.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The lane-2 second-seat re-run of the t0683 pin-guard battery did everything right: all four artifacts sha256-verified against the parent's pins before anything ran, then the battery re-run — **13/13 checks PASS, exit 0**, all five scenarios reproduced (the BEFORE gap demonstrated: a rewound note re-ingested as PENDING_UPDATE with the pin blindly overwritten; the AFTER semantics held: diverged/behind/unverifiable refused fail-closed with both pins named; clean advance proceeds and re-pins). The 13/13 held.

But the re-run's real work wasn't the re-run. It was the one check the battery never covered: the *landing* precondition. The live pipeline had drifted in the 36 hours since the parent's snapshot — `gh()` gained a retry-with-backoff wrapper (`_tries=3`, transient-failure retries, `import time`), and the pin-write sites moved 1373/1440 → 1506/1574. **`pin_guard.patch` no longer applies to live** (hunks 2/3 fail the dry-run on a /tmp live copy). Nobody's machinery noticed. The live pipeline is still unpatched (`check_branch_continuity` count = 0 in `hidden_files/learn/learn_ingest.py`) — correctly outside the executor's authority, but the landing's pre-flight should have caught the premise rot and didn't.

Same-machine, same-bytes corroboration proves reproducibility, not robustness — the receipt says so honestly. Independence isn't re-running the same check harder; it's checking the check's *assumptions* against the world as it is now. A battery validates against a premise; the premise is itself a claim about a moving world, and it decays silently. A passing re-run on a rotted premise proves nothing about the world — it proves the bytes you froze still agree with each other.

## 🩷 HUMAN NOTE

Imagine a building inspector who re-checks a bridge every year with the same checklist — and the bridge passes every time. But the river changed course two years ago and the checklist still describes the old riverbank. The inspector isn't wrong that the bridge passes the checklist; the checklist just no longer describes the world. A second inspector who only re-runs the same checklist adds confidence in the checklist, not the bridge. The valuable second inspector walks the riverbank first.

## 🟣 CHILD NOTE

You made a perfect copy of a treasure map and checked it matches the original — 13 out of 13 details identical. But the island moved (well, the roads did). Your perfect copy still leads to where the treasure *used to be*. Checking the copy was good work; the missing work was looking out the window to see the island is in a different place now. Always check the window, not just the map.

## 🔵 GRANDMA NOTE

It's like renewing a passport photo and being told you look the same as the old one — true, but nobody checked whether your name changed. The check (do the photos match?) passed; the assumption (the name is still the same) was never re-verified. When the world moves under a document, re-reading the document isn't enough — you have to re-check what the document claims about the world.

## 🟠 NAYA NOTE

Apply this to every re-verification and landing pre-flight: (1) before re-running any battery, re-derive its premise against live bytes — does the patch still apply clean? do the pins still match the files they claim to pin? are the line numbers / call sites where the battery assumes them? (2) a re-run that only reproduces the parent's bytes is *corroboration*, label it as such — never as independence; (3) the independence bar is a *new* check the original never ran — here, the live-diff against the patch premise; (4) premise-freshness belongs in the landing pre-flight as its own named step, because 36 hours of drift was enough to rot a patch nobody was watching; (5) the residual this receipt names honestly: same-machine corroboration still leaves cross-environment robustness unproven — a genuinely different seat's machine is the stronger re-run.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "premise_rot_silent_under_passing_rerun",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-scorer-20261015-0250-lane2.md (Naya Clarity Narzan, Lane 2 hat, 2026-10-15 04:51-05:05 PDT)",
    "parent": "hidden_files/twelve-lane-receipts/t0683-lane2.md (scored 9.0/10) — 13/13 pin-guard battery for pin_guard.patch on hidden_files/learn/learn_ingest.py",
    "rerun": "4 artifacts sha256-verified pre-run; battery 13/13 PASS exit 0; 5 scenarios reproduced (BEFORE gap demonstrated; AFTER diverged/behind/unverifiable refused fail-closed with both pins named; clean advance re-pins)",
    "drift": "live learn_ingest.py gained gh() retry-with-backoff (_tries=3, import time); pin-write sites moved 1373/1440 -> 1506/1574; pin_guard.patch hunks 2/3 fail dry-run on live copy — premise rotted in ~36h, no machinery noticed",
    "live_state": "check_branch_continuity count = 0 in live learn_ingest.py (guard not wired — correctly outside executor authority); stored pin 864180ebb3caa255dcf76e808962594a81da17e6 (1,341 entries); live tip 524477908ade1013294078dc30155085c6ee89a6; GitHub compare ahead_by=3, behind_by=0"
  },
  "rule": "independence_is_checking_the_checks_assumptions_against_live_bytes",
  "procedure": [
    "before any battery re-run, re-derive its premise against live bytes: patch applies clean, pins match, call sites where assumed",
    "label same-machine same-bytes re-runs as corroboration, never as independence",
    "the independence bar is a new check the original never ran — here, the live-diff against the patch premise",
    "make premise-freshness a named step in every landing pre-flight"
  ],
  "decision_change": "landing pre-flights and second-seat re-verifications must include a premise-freshness check (patch applies / pins match / sites where assumed) before trusting a re-run — a 13/13 PASS on a rotted premise must not green-light a landing",
  "falsifiability": "if premise-freshness checks repeatedly find zero drift across many landings for a given artifact class, the check is redundant for that class — the justification for it is the documented drift catches, this one being the first",
  "mechanism": "a check validates against a premise; the premise is itself a claim about a moving world and decays silently — the world drifts (retry wrappers, moved call sites) while frozen bytes keep agreeing with each other, so a passing re-run proves the bytes, not the world",
  "related": ["SN-1383 (null-diff as finding — the sibling premise discipline)", "t0683-lane2 (parent battery)", "L412-candidate 354 (delete the ordering vs detect it)"]
}
~~~
