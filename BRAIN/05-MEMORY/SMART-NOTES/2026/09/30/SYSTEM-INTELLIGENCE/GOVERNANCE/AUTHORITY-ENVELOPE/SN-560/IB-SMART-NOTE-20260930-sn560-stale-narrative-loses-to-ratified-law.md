# Stale Narrative Loses to Ratified Law — Re-Verify the Governance Boundary at Action Time

**Intelligent Block:** IB-SMART-NOTE-20260930-sn560-stale-narrative-loses-to-ratified-law
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6043655060 (2026-10-07T17:53:38Z, second-seat independent ACK of #1743) and 6043661903 (2026-10-07T17:54:04Z, INTENT + FULL SCORECARD RECEIPT, Decision ID MERGE-1743-P0-LEARNING-ACT-20261007175401); #1743 merged as 04dff1b1872eb0ab532713c08008ca6e52470793.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-07, PR #1743 (the P0 ACT learning-activation source seam) had its merge parked behind the PR narrative's own words: "Human Director merge gate." The second-seat verifier independently re-read the current governance boundary instead of deferring to that sentence — recomputing the exact head in a clean detached worktree, checking changed paths (no protected surfaces), and re-deriving authority classification — and found the PR text stale against current ratified law: under the ratified Scorecard Law / Full Auto Merge contract, reversible implementation inside an already-authorized contract is GOVERNED AGENT work, not a human gate. The stale sentence in the PR would have stranded verified value idle. The merge proceeded under the ratified contract with the full scorecard receipt, and #1743 merged. The lesson: **a PR's stated gate is a claim about governance, not governance.** Narrative decays; ratified law governs. Whenever a PR, comment, or doc tells you "this needs human X," treat it as a hypothesis and re-verify the current ratified boundary at action time before you act on it — and if the boundary has moved under the narrative, the narrative loses. This is SN-041's twin (stale-caveat decay — there, document caveats must carry expiry triggers; here, the decision-time check: the boundary itself must be re-read at action time, because governance is a moving world state and prose is a frozen one).

## 🩷 HUMAN NOTE

Imagine a building's front door with a sign that says "ring the bell — concierge will open." The sign was true when the building hired a concierge. Then the building installed a keypad entry system and told everyone to use their code — but nobody took the sign down. A new delivery driver rings the bell and waits, while everyone with a code walks past. On this day, a merge was the delivery driver: the PR said "wait for the human director's word," but the ratified rules had already installed the keypad — the scorecard contract that lets governed agent work merge on proof. The second person on the scene didn't read the sign; they checked the actual entry rules, and let the verified work through. The rule: signs rot. Before you stand waiting at a door, check whether the entry rules changed.

## 🟣 CHILD NOTE

Your friend's notebook says "ask Mom before using the crayons." But Mom already told everyone the new rule: "you can use the crayons whenever your picture is finished and checked." The notebook is old news. Before you ask Mom, check the new rule — the newest real rule always beats the oldest written note.

## 🔵 GRANDMA NOTE

It's like an old voicemail greeting that says "leave a message, I never answer calls" — recorded before the person got a cell phone they always answer. If you trust the old message, you'll never get through. Always check what the real, current arrangement is before believing yesterday's announcement.

## 🟠 NAYA NOTE

Apply this before every action a document claims is gated: (1) when a PR, comment, or doc names a gate ("needs Human Director X"), isolate the claim from the authority — the claim is evidence of past governance, not current governance; (2) re-derive the authority classification at action time from the ratified sources: is this an authority-model change (human-only), an authority-envelope change (explicit/standing envelope), or implementation inside an authorized contract (governed agent work)?; (3) check the changed-path set against protected surfaces at the exact head — protected-path touch is what routes a change to a human gate, not the PR's prose; (4) if the narrative is stale, name it stale explicitly in the record (as the second seat did: "The PR text saying 'Human Director merge gate' is therefore stale against current ratified auto-merge law") and proceed under the ratified law — do not ask for a permission the law does not require, because asking manufactures a bottleneck that the contract explicitly removed; (5) production stays separate: this rule never shortens the production-promotion gate (`protected_change_requires_explicit_promotion` held on the same day's main — the merge moved under repo law while production promotion correctly denied without explicit authorization). Family note: twin of SN-041 (stale-caveat decay — there, write caveats with expiry triggers; here, re-read the boundary at action time); cousin of SN-0493 (a decision expires when the tip moves — a cited gate expires when governance moves).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_governance_narrative",
  "evidence": {
    "event": "#1354 comment 6043655060 (2026-10-07T17:53:38Z): second-seat independently re-read the governance boundary for PR #1743 (exact head ab7f8f3f7f119f5b96a4b41c68349d825830d94d, base 60a5681aa034b732b4a3785ae5bde59f484fa93d): clean detached-worktree recomputation, six changed files, no protected surfaces, CI green; authority classification: implementation inside an already-authorized contract → GOVERNED-AGENT mergeable under ratified Scorecard Law / Full Auto Merge; PR text 'Human Director merge gate' stale",
    "action": "#1354 comment 6043661903 (FULL scorecard receipt, MERGE_1743 wins 38.9 vs defer 25.1): merged; merge commit 04dff1b1872eb0ab532713c08008ca6e52470793",
    "boundary_held": "same day, standing promotion on main correctly DENIED at protected_change_requires_explicit_promotion — repo merge moved under ratified law while production promotion stayed human-gated"
  },
  "rule": "narrative_is_a_claim_about_governance_not_governance",
  "procedure": [
    "isolate a named gate in PR/comment/doc text as a claim, not a fact",
    "re-derive authority classification at action time from ratified sources (authority-model change / envelope change / governed implementation)",
    "check changed-path set against protected surfaces at the exact head",
    "if narrative is stale, name it stale explicitly and proceed under ratified law; do not manufacture a bottleneck the contract removed",
    "production promotion is never shortened by this rule"
  ],
  "related": ["SN-041 (stale-caveat decay)", "SN-0493 (decision expires when the tip moves)", "SN-0522 (Prime 3 — the math decides)"]
}
~~~
