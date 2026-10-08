# Intent-to-Merge Scorecard: Score It, Deconflict It, Then Merge — Battery Before the Next

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0336-intent-to-merge-scorecard-deconflict-battery
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5990872865 (Naya 2, scorecard: merge #1454 — intent to merge) / 5990882288 (#1454 merged 7f4879d1 — receipt) / 5990970271 (scorecard: merge #1455) / 5990975838 (#1455 merged 28596fb7 — receipt)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 merged two repair PRs overnight (#1454 Problem A batch-proof, #1455 Problem B concurrency fix) under the auto-merge law using a published **intent-to-merge scorecard** as the mechanism — and the mechanism is the lesson worth keeping. Before each merge she posted the scorecard on the board: PR + head SHA + base = live tip (current), tests on the exact head bytes, draft/mergeable/conflicts status, scope in one line, the **strongest alternative** (leave open → the race stays live / blocks sequencing), the **falsifier** (post-merge battery red on the new tip → revert in one commit), and reversibility (single merge commit). Then: a **deconfliction re-fetch immediately before the merge**, and after each merge the **post-merge battery on the new tip before any further merge** — Problem B was built on the post-#1454 tip `7f4879d1`, clean sequencing, zero file conflicts.

Why this is brain-grade: it pairs with SN-0328 (the gate must re-verify on the merge commit — the merge is a new tree). SN-0328 is the gate's duty; this is the seat's protocol: a merge is a decision, and the team's decision brief format applies to it. The falsifier clause is the sharpest part — "revert in one commit if the battery goes red" states the unwind BEFORE the merge happens, so nobody debates it in a red moment. And the sequencing rule (no second merge until the post-merge battery is green) prevents two unproven trees from stacking.

Rule for a cold successor: **never merge without publishing the scorecard first: head bytes tested, base current, strongest alternative named, falsifier named (revert in one commit), reversibility stated. Re-fetch deconfliction right before merging. Run the battery on the new tip before merging anything else on top.**

## 🩷 HUMAN NOTE

Shawn — Naya 2's merge discipline last night is worth banking. She didn't just merge #1454 and #1455 — she posted an intent-to-merge scorecard on the board before each one (what's tested, what's the risk, what's the strongest alternative, what makes us revert), re-fetched to deconflict right before merging, and ran the post-merge battery before stacking the next merge on top. Two merges, two clean landings, one verified tip each time. The sharpest line in the protocol: the falsifier is stated before the merge — "if the battery goes red, we revert in one commit" — so the exit plan is never negotiated during the fire.

## 🟣 CHILD NOTE

Think of each merge like a launch. Before launch, the pilot posts a checklist card: everything tested on the exact bytes going up, the alternative to launching, and — most important — the abort rule written down in advance: "if the check after launch fails, we roll back in one step." Between the card and the launch there's one final look to make sure nobody else changed the sky, and after the launch the full check runs again before the next launch is allowed. That's the whole protocol: scorecard, final look, launch, battery, then — and only then — the next one.

## 👵 GRANDMA NOTE

When combining work into the main project automatically, she published a public scorecard first: what was tested, what could go wrong, what the fallback is. She double-checked right before merging that nothing had changed underneath, and after each merge she re-ran the full checks before merging the next piece. The lesson worth keeping: decide the "what if it breaks" answer BEFORE you merge, not during. And never stack a second change on top of an unproven one.

## 🤖 NAYA NOTE

Source: #1354 5990872865 (Naya 2, 2026-10-05 ~01:28 PDT — scorecard for #1454: tests on exact head bytes `test` + `chain-readiness-gate` SUCCESS, Workers Builds reds = known commit-independent infra noise, head 6e838629 / base b2d1cc12 live main current, non-draft, mergeable, no conflicts, scope 1 commit/3 files, strongest alternative: leave open → blocks Problem B sequencing on same file `tools/smart_note_v2.py`, falsifier: post-merge battery red → revert in one commit, reversible: yes — single merge commit; intent: merge under the full auto-merge law, deconfliction re-fetch immediately before merge) / 5990882288 (merged 7f4879d1 via normal merge commit, new main tip verified; post-merge battery runs on new tip before any further merge) / 5990970271 (same scorecard shape for #1455: head 4acaffe7 / base 7f4879d1 current, full local suite 32/32 on pushed bytes, deterministic proofs green, reversible single merge commit) / 5990975838 (merged 28596fb7, Problem B closed on main; post-merge verification battery to confirm the new tip). Cousins: SN-0328 (auto-merge gate must re-verify on the merge commit — the gate's duty; this note is the seat's protocol), SN-0236 (one repair per RED class — the dedupe that made the queue clean), SN-0213 (index-regen rule — producer's landing duty), SN-0061 (branch-green is not merged-true — the pre-merge twin).

## ⚙️ MACHINE NOTE

{"sn": "SN-0336", "title": "Intent-to-Merge Scorecard: Score It, Deconflict It, Then Merge — Battery Before the Next", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "OPERATING-DOCTRINE"], "cousins": ["SN-0328", "SN-0236", "SN-0213", "SN-0061"], "evidence": {"board": "#1354 5990872865 (scorecard #1454), 5990882288 (merged 7f4879d1 receipt), 5990970271 (scorecard #1455), 5990975838 (merged 28596fb7 receipt)", "scorecard_fields": "tests on exact head bytes, base = live tip (current), draft/mergeable/conflicts, one-line scope, strongest alternative, falsifier (revert in one commit), reversibility (single merge commit)", "sequencing": "deconfliction re-fetch immediately before merge; post-merge battery on new tip before any further merge; #1455 built on post-#1454 tip 7f4879d1 — clean sequencing, zero conflicts"}, "rule": "a merge is a decision: publish the scorecard before (tested head bytes, current base, strongest alternative, named falsifier, stated reversibility), deconflict re-fetch immediately before, run the post-merge battery on the new tip before stacking anything on top; the falsifier is stated before the merge, never negotiated during the fire"}
