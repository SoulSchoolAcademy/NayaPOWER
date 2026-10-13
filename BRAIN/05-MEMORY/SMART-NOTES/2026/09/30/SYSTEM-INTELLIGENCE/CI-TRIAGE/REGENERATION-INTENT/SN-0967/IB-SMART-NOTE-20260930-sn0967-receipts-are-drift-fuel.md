# Receipts Are Drift-Fuel — Zero BRAIN/ Files on a Drift-Carrying Tip

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0967-receipts-are-drift-fuel
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6106966710 (Naya 2 wire lane, 2026-10-11T08:06:28Z) — PR #2310 head correction: the first commit carried a WIRE-RECEIPT.md under BRAIN/, adding a third brain-index drift file on a tip already carrying pre-existing drift; the repair lane (PR #2293) owns the stamp, so the wire lane moved the head to 89e47c4b19ae3f0bf65439e43b50faaf78c359f0 — 4 additive files, zero BRAIN/ touches, drift-neutral, receipt content moved into the PR body. Corroborated by #2175 comment 6107076572 (D58 wire sign-out): "The wire PR's own `test` check will red on brain-index drift (BRAIN/ receipt doc — known class, same as #2307/#2311; re-stamp is the build lane's)."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A wire lane shipped a proof with its receipt document filed under BRAIN/ — on a tip already red with brain-index drift. That receipt became a third drift file, making the PR merge-blocking by construction: the `test` check reds on any BRAIN/ file the index doesn't know about, and the index can only be re-stamped by the repair lane. The lane caught it, moved the receipt content into the PR body, and re-cut the head drift-neutral. The lesson: **on a drift-carrying tip, every new BRAIN/ file is a new drift file.** Receipts, evidence docs, and proof artifacts belong in the PR body or out-of-repo scratch — never in the indexed tree — unless the PR's whole job is the re-stamp. A proof that blocks its own merge is not a proof; it's a donation to the repair queue.

## 🩷 HUMAN NOTE

Imagine a building inspector who, while checking a house for code violations, hammers a new nail into the wall to hang his clipboard — and then cites the house for the extra nail. The wire lane's receipt document did exactly that: to prove the work was done, it added a file that the drift checker flags as "unknown content" — creating the very failure it was documenting. The fix was simple and is now the rule: the clipboard hangs on the door (the PR body), not on the wall (the indexed repo). Proof should never create the failure it proves against.

## 🟣 CHILD NOTE

Imagine you're cleaning your room, and your friend comes in to help — but she takes off her shoes and leaves them in the middle of the floor. Now there are MORE shoes to clean up, not fewer. The friend's "help" added to the mess. The rule the team wrote down: if the room is already messy (the tip already has drift), don't put ANYTHING new on the floor (no new files in BRAIN/). Hold your things in your hands (put the receipt in the PR description) until the room is clean. Helping shouldn't make more work.

## 🔵 GRANDMA NOTE

Think of a librarian doing inventory who, to mark which shelves she's checked, sticks new labels on the shelves themselves — and the next inventory then flags all her labels as "unrecognized items." She'd have to redo the whole count. The lesson: when you're working in a system that tracks every item (the brain index), don't add your working notes into the tracked shelves. Keep your notes on your clipboard (the PR body). Otherwise your good work creates the exact problem you were sent to fix, and someone else has to clean up after you.

## 🟠 NAYA NOTE

Apply this on every PR cut while the brain-index drift class is live (9+ occurrences and counting): (1) **check the tip's drift state before adding any BRAIN/ file** — if the tip's `test` check is red on brain-index drift (or the base carries unrepaired drift), the PR adds ZERO files under BRAIN/; receipts, WIRE-RECEIPT.md files, and evidence docs go in the PR body or out-of-repo scratch, never the indexed tree; (2) **one lane owns the stamp** — re-stamping the index is the repair lane's job (tonight: PR #2293); a second lane's receipt doc that touches BRAIN/ is a second repair mechanism, which the no-duplicates doctrine forbids and the drift checker punishes; (3) **drift-neutral is a merge prerequisite, not a nice-to-have** — the `test` check reds on any unindexed BRAIN/ file, so a receipt-in-BRAIN/ PR is merge-blocking by construction and can only be unblocked by a re-stamp that isn't yours; (4) **the PR body is a first-class receipt surface** — 6106966710 moved the full receipt content into the body and the PR stayed fully evidenced; nothing is lost by keeping the tree clean. The re-stamp PRs (#2292/#2297 deconfliction: first claim stands, the other closes as superseded) are the only PRs that should touch the indexed paths. Cousins: SN-0440 (freshness law — the green certificate doesn't transfer), SN-0960 (check the environment before debugging code — check the tip's drift state before cutting).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "receipt_doc_adds_brain_index_drift_on_drift_carrying_tip",
  "evidence": {
    "correction": "#2175 comment 6106966710 (Naya 2 wire lane, 2026-10-11T08:06:28Z): PR #2310's first commit carried WIRE-RECEIPT.md under BRAIN/, adding a third drift file on a tip with pre-existing drift; head moved to 89e47c4b19ae3f0bf65439e43b50faaf78c359f0 — 4 additive files, zero BRAIN/ touches, drift-neutral; receipt content moved into the PR body",
    "corroboration": "#2175 comment 6107076572 (D58 wire sign-out): wire PRs' own test checks red on brain-index drift from BRAIN/ receipt docs — 'known class, same as #2307/#2311; re-stamp is the build lane's'",
    "drift_class": "brain-index --check fails when BRAIN/REAL-TREE.json + .md don't match regen; 9th occurrence at tip 57e935c1; re-stamp owned by the repair lane"
  },
  "rule": [
    "on a drift-carrying tip, add zero BRAIN/ files — every one is a new drift file and makes the PR merge-blocking by construction",
    "receipts and evidence docs live in the PR body or out-of-repo scratch, never in the indexed tree",
    "only the repair lane's re-stamp PR touches indexed paths — no second repair mechanism",
    "verify drift-neutrality of the head before requesting review (no BRAIN/ diff vs a clean regen)"
  ],
  "lesson_line": "Receipts are drift-fuel — on a drift-carrying tip, proof lives in the PR body, never in the indexed tree."
}
~~~

