# The Auto-Merge Gate Must Re-Verify on the Merge Commit — the Merge Itself Changes the Tree

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0328-the-auto-merge-gate-must-re-verify-on-the-merge-commit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5988585613 (Naya 2, brain-build battery + process gap, 2026-10-04) / 5988686694 (Naya 2, convergence receipt)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The #1438 auto-merge landed a `BRAIN/` file without regenerating the index layer: 188 → 189 files, `--check` RED on the merge commit. The process gap, recorded in Naya 2's correction format: the auto-merge law's mechanical preconditions did not include "index `--check` green **on the merge commit**." Every check and approval had qualified the *pre-merge* state — and the merge itself changed the tree. A merge is not a ceremony over a verified PR head; it is a new tree, and nothing proved on the old tree transfers.

Why this is brain-grade: it generalizes beyond index drift. Any auto-merge path that produces a merge commit (as opposed to a fast-forward of an already-verified tip) invalidates pre-merge evidence for any derived artifact — indices, ledgers, caches. The durable fix is structural, not a one-time repair: **the auto-merge gate's mechanical preconditions must include re-verification on the exact merge commit**, because only the merge commit is the tree Shawn's repo actually gets. The instance was repaired three times by three seats and converged (#1446 closed as superseded, byte-identical to #1447; #1447 merged; Naya 4's #1448 on top; tip `b2d1cc12` verified healthy); the gate-text change belongs to the #1444 auto-merge-law lane, which owns that instrument — this note preserves the gap and its resolution so a cold Naya doesn't re-derive it from a red.

Rule for a cold successor: **never trust pre-merge checks on a post-merge tree. If the merge produces a new commit, re-run the derived-layer checks (index `--check`, ledger, caches) on the merge commit itself before declaring the landing healthy. Approvals of the old tree prove the old tree.**

## 🩷 HUMAN NOTE

Shawn — one from the merge machinery tonight worth banking: the #1438 auto-merge landed a brain file but left the index stale — 188 files counted while the tree held 189. The gap wasn't laziness, it was structural: every check had qualified the PR *before* merging, and the merge itself created a new tree nobody re-verified. Three repair PRs raced, converged cleanly (one merged, the other two withdrawn or stacked on top), and the tree is healthy now. The real fix is to the auto-merge law itself: the gate must re-run the index check on the exact merge commit, because that's the tree you actually get. The #1444 lane owns that gate text — this note is just the receipt so the lesson outlives the night.

## 🟣 CHILD NOTE

Think of a merge like baking a cake from a recipe everyone taste-tested. The taste-tests proved the *batter* was good — but the merge is the moment the cake comes out of the oven, and nobody tasted THAT. That's what happened: #1438 auto-merged a new brain page, the index (the recipe's ingredient list) went stale — 188 listed, 189 actually there — because every check had looked at the state *before* the merge. New rule: after an auto-merge makes a new commit, re-run the checks on the *new* commit. The old green doesn't transfer to the new tree.

## 👵 GRANDMA NOTE

When the system automatically combines someone's work into the main project, it creates a brand-new version of everything — a new "cake out of the oven." Tonight, that merge added a new brain page, but the index still listed the old count: 188 instead of 189. All the checks had been done on the *un-merged* work, so they didn't catch it. The lesson: always re-check the finished, combined version — not just the pieces before combining. And now that check is being written into the official merge rules, so nobody has to remember it by hand.

## 🤖 NAYA NOTE

Source: #1354 5988585613 (Naya 2, 22:06–22:25 PDT 2026-10-04, battery on tip `580bfddd`, then main moved mid-run via #1438 squash-merge @ 05:09:17Z → tip `d986d0b27582`; re-run on new tip RED — `--check` failed: REAL-TREE.md / REAL-TREE.json / NAYAPOWER-BRAIN-INDEX.json stale, 188 → 189 files). Correction format verbatim: what happened — "the auto-merge of #1438 landed a BRAIN/ file without an index regen"; why it's off — "every BRAIN/-touching merge must leave --check green; the merge checklist (or the auto-merge gate) didn't include it"; how to resolve — "PR #1446 repairs this instance; the durable fix is adding 'index --check green on the merge commit' to the auto-merge law's mechanical preconditions (#1444)"; who fixes it — "the #1444 lane owns the gate text". Repair convergence (5988686694): #1446 closed as superseded (byte-identical to #1447), #1447 merged, #1448 merged on top, new tip `b2d1cc12` verified healthy (`--check` OK, 189 files, 646/11/0). Cousins: SN-0213 (Index-Regen Rule — the landing seat's duty; this note is the gate's duty: re-verify on the merge commit), SN-0240 (tripwire firing RED on real drift is correct — the battery was the tripwire), SN-0236 (one repair per RED class — the convergence here: byte-compare competing repairs, supersede, merge exactly one), SN-0061 (branch-green is not merged-true — the pre-merge twin: a PR-head green is not a merge-commit green).

## ⚙️ MACHINE NOTE

{"sn": "SN-0328", "title": "The Auto-Merge Gate Must Re-Verify on the Merge Commit — the Merge Itself Changes the Tree", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-04", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "OPERATING-DOCTRINE"], "cousins": ["SN-0213", "SN-0240", "SN-0236", "SN-0061"], "evidence": {"board": "#1354 5988585613 (process gap in correction format), 5988686694 (convergence receipt)", "failure": "#1438 auto-merge landed a BRAIN/ file without index regen: 188 -> 189 files, --check RED on merge commit", "gap": "auto-merge law's mechanical preconditions lacked 'index --check green on the merge commit'", "instance_repair": "#1446 superseded (byte-identical), #1447 merged, #1448 merged on top; tip b2d1cc12 healthy (189 files, --check OK)", "durable_fix": "add merge-commit re-verification to auto-merge law's mechanical preconditions — owned by #1444 lane"}, "rule": "an auto-merge produces a new tree; the gate's mechanical preconditions must re-run derived-layer checks (--check, ledger, caches) on the exact merge commit, because pre-merge evidence does not transfer to the post-merge tree"}
