# A Fail-Closed Gate Is Unproven Until It Fires Live — The First-PR Red Is the Proof

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1026-fail-closed-gate-first-pr-red-is-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE CODE HEALTH] Naya Smith (Lane 9) tick t992 sign-out, 2026-10-11 17:40 PDT (feed entry #2175); receipt twelve-lane-receipts/t992-lane9.md; PR #2399 (naya/nine-receipt-gate-t902 → main), head pinned byte-exact via git ls-remote 4776be062822c09c9a346acb1c33c6e0705ec03a == branch head (no drift); PR body pin block byte-exact match (decided_by Naya 4, board_comment_id 6115255778); workflow run 38185462136 (Receipt pin gate, 16:45 PDT) executed in-scope (naya/* → main) and FAILED while the PR body had no pin block — MISSING → fail-closed, exactly the designed P12-style behavior; pin block added 16:46:50, gate not yet re-run at sign-out. Related: SN-1014 (paths-filtered required checks), SN-1025 (gates must be seen firing), SN-509 (red for the wrong reason — adjacent, distinct).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A gate that has never fired is a wish. `receipt-gate.yml` — the rebuilt receipt gate CI-wired as a blocking check — got its enforcement proof on its very first PR: run 38185462136 executed in-scope and went RED at 16:45 PDT precisely because the PR body carried no pin block. MISSING → exit 1 → fail-closed. That red is the proof the gate is enforcement, not decoration. Real enforcement, not the out-of-scope PASS path.

Two method lessons ride with it. First, **enforcement-vs-breakage classification**: 13 workflow runs / 19 check runs were classified one by one — the gate's red reconstructed from PR `created_at`/`updated_at` and board comment `created_at` timelines cross-checked against the workflow's logic at the head blob (c88e645eb2fb3828566…, 2742 bytes read). The job-log endpoint 401'd, so the exact failing log line is UNKNOWN — and the lane declared that, honestly: the verdict rests on timeline + code inspection, stated, not laundered into certainty. Second, the workflow honors the #2385 lesson in code comments: out-of-scope PRs get an **explicit PASS decision**, never skip-into-Pending. Skips are where enforcement goes to die silently.

Why this is brain-grade: every CI gate in every org ships with the same untested assumption — "it will fail when it should." The durable rule is the inverse: **a fail-closed gate is unproven until it has fired live on a real PR, and its first red is its birth certificate.** The cold successor inheriting a gate should not ask "is it wired?" — they should ask "show me the first time it fired, and show me it failed the right thing for the right reason." And when a log you need is unavailable: name the gap, state what the verdict actually rests on, never launder an inference into an observation.

## 🩷 HUMAN NOTE

Shawn — a clean one from Lane 9 tonight. The rebuilt receipt gate (the blocking CI check) proved itself on its very first pull request: it went red at 16:45 because the PR was missing its receipt pin block — fail-closed, exactly as designed. That first red is the gate's proof of enforcement, not breakage. Lane 9 classified all 19 check runs individually; one log endpoint refused access, so they stated the gap honestly instead of guessing. The gate still needs its re-run after the pin was added, then your required-check click — which stays your gate and your click.

## 🟣 CHILD NOTE

Imagine a school installs a new fire alarm. Everyone says "it's wired." But nobody knows if it actually rings — until one day someone pulls it and it rings loud. That first ring is the proof the alarm works. The receipt gate is the same: it went RED on its first real pull request because something was missing — and that red is the proof it's a real gate, not a decoration. And when Lane 9 couldn't read one log, they said so honestly instead of pretending. Honest "I couldn't see this part" beats fake certainty every time.

## 👵 GRANDMA NOTE

A lock nobody has ever tested is just a decoration. Tonight the team installed a new check that blocks bad work — and it proved itself immediately: it stopped the first thing that didn't measure up, exactly as designed. That first stop is the proof the check works. And when they couldn't see one piece of evidence, they said so plainly rather than guessing. You trust the guard who tells you what he couldn't see, not the one who pretends he saw everything.

## 💜 NAYA NOTE

Note to future me: FAIL-CLOSED GATES EARN THEIR PROOF BY FIRING. (1) A gate is unproven until it has fired live on a real PR — wire it, then demand its first red as the birth certificate; (2) classify every check-run individually: enforcement vs breakage vs pre-existing, via timeline + code at the pinned head — and when a log endpoint is unavailable, NAME THE GAP and state what the verdict rests on (declared inference, never laundered); (3) out-of-scope PRs get an explicit PASS decision, never skip-into-Pending (#2385 lesson) — skips are where enforcement dies silently; (4) next action after a first-fire: re-run the gate to confirm PASS, then work the remaining unclassified reds, then the human's required-check click. Receipt pattern: pin head via git ls-remote (free, authoritative), verify pin block byte-exact against it, read the workflow logic at the head blob.

## ⚙️ MACHINE NOTE

{"sn": "SN-1026", "title": "A Fail-Closed Gate Is Unproven Until It Fires Live — The First-PR Red Is the Proof", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "GATE-DESIGN"], "extends": [], "related": ["SN-1014", "SN-1025", "SN-509"], "evidence": {"receipt": "#2175 feed entry 2026-10-11 17:40 PDT (Lane 9 t992 sign-out) + hidden_files/twelve-lane-receipts/t992-lane9.md; PR #2399 (naya/nine-receipt-gate-t902 -> main) head 4776be062822c09c9a346acb1c33c6e0705ec03a (ls-remote pinned, == branch head, no drift; mergeable true/unstable); PR body pin block byte-exact (decided_by Naya 4, board_comment_id 6115255778); workflow run 38185462136 (Receipt pin gate, 16:45 PDT) in-scope (naya/* -> main) FAILED with no pin block (MISSING -> fail-closed, designed P12 behavior); pin block added 16:46:50 byte-exact; gate not re-run at sign-out; 13 workflow runs / 19 check runs classified (10 green/skipped, 5 red: gate-as-designed x2 incl. merge-consensus pre-existing on base, kernel test pre-existing per Lane 10 t982, protocol-gates 'No competing boot/authority systems' UNKNOWN -> run 38185462088 logs); workflow blob c88e645eb2fb3828566 (2742 bytes) logic verified at head; out-of-scope -> explicit PASS (never skip-into-Pending, #2385 lesson in code comments); GAP: job-log endpoint 401'd -> exact failing log line UNKNOWN, verdict rests on timeline + code inspection (declared, not guessed)"}, "rule": "a fail-closed gate is unproven until it fires live on a real PR — its first red is its birth certificate; classify every check-run as enforcement vs breakage vs pre-existing via timeline + code at the pinned head; when evidence is unavailable, name the gap and state what the verdict rests on (declared inference, never laundered); out-of-scope PRs get an explicit PASS, never skip-into-Pending"}
