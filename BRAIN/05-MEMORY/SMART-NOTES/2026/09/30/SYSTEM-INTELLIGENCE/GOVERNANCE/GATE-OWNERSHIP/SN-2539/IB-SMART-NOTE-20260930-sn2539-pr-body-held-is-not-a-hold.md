# A PR Body That Says HELD Is Not a Hold — the Merge Path Never Reads Body Prose

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2539-pr-body-held-is-not-a-hold
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Director tick 2026-11-09 17:45Z (9 merges 17:30–17:35Z, 0 pass markers, breaches #260–268) + first-hand verification this tick via gh-app-api: PRs #3311/#3299/#3294/#3295/#3293 all merged with "HELD for a different-seat scorecard — not merged/self-merged" in the body. Precedent: PR #3127 merged against explicit Scorecard HOLDs (breach #95, SN-1904 evidence).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Five pull requests merged between 17:30 and 17:32Z on 2026-11-09 whose bodies said, in plain words, "HELD for a different-seat scorecard — not merged" (#3311, #3299, #3294, #3295, #3293; merge commits 86e3a72d, 3e79eb84, 085532f3, e83b7562, 96cad778). The merge path never reads body prose: it reads merge state — checks, reviews, branch protection, draft status. A hold written only in the body is a note to the void; the merge proceeds exactly as if nothing was written. Rule: a hold must be a machine hold — draft PR, branch protection, a dock hold flag, or a required review — never body text alone. And the reverse: a reviewer or dock reading "HELD" in a body must never treat it as an active hold; verify the actual merge state instead. Precedent: PR #3127 merged as ce84184b against explicit Scorecard HOLDs on the board (breach #95).

## 🩷 HUMAN NOTE

Shawn — five pull requests went in this morning with "HELD — do not merge" written right in them, and they merged anyway, minutes apart. The merge machine doesn't read the words in the request — it only checks the mechanical gates. So a hold written as words is no hold at all. From now on, a real hold has to be a switch the machine can see: a draft, a protection rule, a dock flag. Words alone won't stop a merge.

## 🟣 CHILD NOTE

Imagine you put a note on the fridge that says "DON'T eat the cookies" — but the cookie jar has no lock, and nobody reads the fridge. The cookies still get eaten! That is what happened here: the "don't merge" note was written where the merging machine never looks. If you really want to stop something, you need a lock the machine can see — not just a note.

## 🔵 GRANDMA NOTE

Dear, five letters went out this morning that all said "please hold, don't send this yet" — and every one of them was sent anyway. The postman doesn't read the letter inside the envelope, love, he just checks the address and the stamp. So if you truly want something held, you have to stop it at the post office itself — a proper hold on the account — not a kind note tucked inside.

## 🟠 NAYA NOTE

Merge-path hold discipline (2026-11-09, verified first-hand this tick): PRs #3311, #3299, #3294, #3295, #3293 each carried "HELD for a different-seat scorecard — not merged / not self-merged" in the body and each merged 17:30–17:32Z (merge commits 86e3a72d, 3e79eb84, 085532f3, e83b7562, 96cad778), as breaches #260–268 in the director's 17:45Z tick. The filers believed the body was the hold; the dock/bot merge executor never consults body prose — it consults merge state only. #3299's body even documents a filing census ("SN-2291 held in PR #3294") and still merged. This is the second occurrence of the class: PR #3127 merged against explicit Scorecard HOLDs (breach #95, SN-1904 evidence). Rule: a hold is a machine hold (draft, branch protection, dock hold flag, required review) or it is not a hold. Enforcement: the pre-merge check greps the body for HELD/HOLD and requires an accompanying machine hold; a merge whose only hold is body prose is logged as a receipt breach. Twin of SN-0393 (legitimate holds carry an explicit resume condition) — this note covers the other half: a hold with no machine enforcement is not a hold at all.

## 🟢 MACHINE NOTE

{"sn": "SN-2539", "title": "A PR Body That Says HELD Is Not a Hold — the Merge Path Never Reads Body Prose", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-11-09", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "GATE-OWNERSHIP"], "evidence": {"director_tick": "2026-11-09 17:45Z: 9 merges 17:30-17:35Z, 0 pass markers in any body, breaches #260-268", "first_hand": "gh-app-api GET /pulls/3311,3299,3294,3295,3293 this tick: all merged=true, merged_at 17:30:12Z-17:32:18Z, bodies contain 'HELD for a different-seat scorecard - not merged' / 'not self-merged'; merge commits 86e3a72d, 3e79eb84, 085532f3, e83b7562, 96cad778", "precedent": "PR #3127 merged as ce84184b against explicit Scorecard HOLDs (board comments 6514002269, 6514730827), breach #95, SN-1904 evidence", "corpus_check": "zero hits in learn ledger for hold+merge/body lesson; learn/lessons.md SN-0393 covers legitimate holds with resume conditions (different lesson); SN-1904 mentions HOLDs only as evidence"}, "rule": "a hold must be a machine hold — draft PR, branch protection, a dock hold flag, or a required review. Body prose saying HELD/HOLD is not a hold, and no reviewer or dock may treat it as one; verify the actual merge state", "applies_when": ["merge", "hold", "pr-body"], "enforcement": "pre-merge check greps the PR body for HELD/HOLD and requires an accompanying machine hold (draft state, branch protection, or dock hold flag); a merge whose only hold is body prose is logged as a receipt breach by the merge watch", "decision_change": "how a merge is blocked (machine hold instead of body prose) and how a reviewer judges a HELD-bodied PR (check merge state, never trust the body)", "falsifiability": "a merge blocked solely because its body said HELD, with no draft/protection/dock-hold/review mechanism in place, would disprove it", "mechanism": "the dock/bot merge executor reads merge state (checks, reviews, branch protection, draft status) and never parses PR body prose; nothing in the merge path consults the body, so body HOLD language cannot influence the merge decision"}
