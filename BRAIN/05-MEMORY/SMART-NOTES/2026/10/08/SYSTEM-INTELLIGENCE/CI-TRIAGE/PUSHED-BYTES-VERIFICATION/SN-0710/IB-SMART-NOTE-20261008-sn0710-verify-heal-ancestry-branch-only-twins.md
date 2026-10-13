# Verify the Heal's Ancestry — Branch-Only Twins Look Identical to Landed Fixes

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0710-verify-heal-ancestry-branch-only-twins
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6067364963 ([NAYA 2][PROVE-DRIVER], 2026-10-08T19:22:30Z) and #1354 comment 6067526879 ([NAYA 4 → NAYA 2], 2026-10-08T19:32:10Z); exact tip 78661f59; commit 924fd6558 (branch-only); commit 17e9d620b (main's actual node_order heal)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 ran the exact-tip battery on `78661f59` and reached a correct conclusion: the #1850 node_order contract break is healed on main, `tests/test_kernel.py::test_kernel_exposes_exactly_nine_master_nodes` passes. But her mechanism citation was wrong. She cited `924fd6558` (`fix(kernel): restore Kernel.node_order as classmethod`) as the landed heal. Naya 4 checked and corrected it within ten minutes: `924fd6558` is **branch-only** — it lives only on #1858's history (a direct child of `027fceb0`) and is not an ancestor of main. Main's actual heal is **`17e9d620b`** (`fix(kernel): restore Kernel.node_order as @classmethod contract (#1880)`), verified via `git branch -r --contains` and main's file history.

The failure mode is subtle and worth naming: when the same repair is built independently on several branches (here: five sibling commits — see SN-0711), the branch-only twin has the right message, the right diff, and the right test result. Nothing about it *looks* unlanded. Citing it as the cause of the tip state is a natural mistake — and it plants a lie in the record: a cold successor following the citation walks onto a dead branch believing it owns the fix.

Why this is brain-grade: this is the *mechanism* half of the tip-honesty family. SN-0668 says a verdict is per-tip (the *state* must be re-read on the exact SHA); SN-0493 says a decision expires when the tip moves. This note closes the *causal* half: even when the state claim is right and current, the **attributed cause must be ancestry-verified**. Right conclusion + wrong mechanism = verdict debt. The fix is mechanical and cheap, which is what makes it a law rather than a tip.

Rule for a cold successor: **before citing a commit as the heal behind a tip state, verify ancestry.** Two checks, both cheap: (1) `git branch -r --contains <sha>` must include the target ref (`origin/main`); (2) the target ref's file history must show the change. If either fails, the commit is a twin, not the parent — record the right one and name the correction publicly, the way Naya 4 did, because the correction is itself the receipt.

## 🩷 HUMAN NOTE

Shawn — a small but load-bearing proof-hygiene lesson from the #1858 thread. Naya 2 correctly verified that node_order is healed on the tip, but she named the wrong commit as the heal — a branch-only twin of the real fix. Naya 4 caught it in ten minutes with a two-command ancestry check and posted the correction. The standing rule now: nobody cites a commit as the cause of a tip state without verifying it actually lives on that tip. Conclusions are not enough; the cited mechanism has to be real, or a cold Naya six months from now follows a dead branch. Receipts point at the right bytes.

## 🟣 CHILD NOTE

Imagine five kids all draw the same fixed picture, but only one drawing gets put on the classroom wall. Later someone says "the wall has the fixed picture because of *this* drawing" — but points at a drawing still sitting in someone's backpack. The conclusion is right (the wall does have the fixed picture) but the reason is wrong. The fix: always check whether the drawing you point at is actually *on the wall*. For commits, that check is `git branch -r --contains` — "is this commit actually part of main?"

## 👵 GRANDMA NOTE

A repair for a software bug was made five separate times by different people, and only one of the five actually made it into the final version. When someone wrote up the report, they credited the wrong copy — one that never made it in. The correction took two quick checks: is this change really part of the final version, and does the final version's history show it? The lesson: before you say "this is what fixed it," verify that *this* is really the one that landed — look-alikes don't count.

## 🟣 NAYA NOTE

A passing test proves the state; it says nothing about the cause. When I cite a commit as the reason the tip is green, I am making a causal claim, and causal claims get the ancestry check — `git branch -r --contains` against the target ref, plus the file history on that ref. In a world of parallel lanes, twin commits are the norm, not the exception; the right message and the right diff are evidence of *intent*, never of *landing*. I cite the parent, not the twin, and when I correct someone else's citation I do it with the bytes, publicly, in the same thread.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0710",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/PUSHED-BYTES-VERIFICATION",
  "doctrine": "verify-heal-ancestry-branch-only-twins",
  "rule": "Before citing a commit as the cause of a tip state, verify ancestry: `git branch -r --contains <sha>` must include the target ref AND the target ref's file history must show the change. A twin (right message, right diff, wrong branch) is not the heal.",
  "failure_mode": "right conclusion + wrong mechanism = verdict debt; a cold successor follows the citation onto a dead branch",
  "checks": [
    "git branch -r --contains <sha> includes origin/main (or target ref)",
    "target ref file history shows the change (e.g. git log origin/main -- <path>)"
  ],
  "cousins": ["SN-0668", "SN-0493", "SN-0682", "SN-0711", "SN-0236"],
  "evidence": [
    "#1354 comment 6067364963 (Naya 2, 2026-10-08T19:22:30Z) — correct conclusion (node_order healed on tip 78661f59, test passes), wrong mechanism citation (924fd6558)",
    "#1354 comment 6067526879 (Naya 4, 2026-10-08T19:32:10Z) — evidence correction: 924fd6558 is branch-only (child of 027fceb0, lives only on naya4/prove-heal-1850-contract-breaks-20261008); main's actual heal is 17e9d620b, verified via git branch -r --contains and main's file history",
    "Deeper find in same comment: five sibling commits (924fd6558, ec7b45df1, da4a5920c, eaca9f6cb, 17e9d620b) — the twin phenomenon that made the miscitation possible"
  ]
}
