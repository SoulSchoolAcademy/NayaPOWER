# Score the Work and the Process Separately — the Split Verdict

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01556-split-verdict-technical-vs-process
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** 2026-10-17 ~06:48 PDT: Shawn's instruction — score PR #2723 independently; "if the score is over nine, so be it; if not, put a note on the board calling Eta out — we all follow the process, we all call each other out." Different-seat (Naya Clarity Narzan) independent scorecard on the merged bytes at f1cb7a37: PR body 1,538 chars, ZERO 3-pass show-your-work structure (no pass 1/2/3, no holes, no repairs) = FM#32 formal receipt breach; code run on the merged bytes 6/6 PASS, clean labeler (intelligence/q_bands.py), boundary pins correct, bad inputs raise instead of silently mislabeling, body honest about what's unproven. Delivered verdict: Technical 9.0/10, Process 3/10. The merge stands on the technical score AND the callout was posted anyway (board #2721 comment 6234684531); retroactive 3-pass receipt owed by Naya Eta. Shawn reacted 👍. Merged 13:20:22Z; FM#60 gate-read at the merge commit: 56x completed/skipped, 0 failures → FM#60 did not fire; post-merge double-verified (VERIFY 6234439046, Electrician 6234530093).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A single blended score forces a false choice: pass the work and forgive the process breach, or fail the work and punish good code. On PR #2723 the seat split the verdict instead — Technical 9.0/10 (the code, run on the merged bytes, 6/6 green, honest body) and Process 3/10 (no 3-pass receipt, FM#32 formal breach). The split preserves both truths at once: the merge stands on its technical merit AND the process debt is named as owed, with the builder called out on the board the same hour. Blending would have averaged 9.0 and 3.0 into a 6 — a number that says nothing and authorizes nothing. Two scores say everything: what the work is worth, and what the process still owes. The falsifier is simple: if a split verdict ever lets a process breach slide because "the technical score was fine," the split has become camouflage and must be repaired — but on #2723 the callout was posted in the same motion as the 9.0, which is the discipline working.

## 🩷 HUMAN NOTE

Imagine a restaurant review that gives one star rating for "the food AND the service." A place with incredible food and a waiter who never came gets three stars — and you learn nothing: was the food bad, or was the service bad? Now imagine the review gives two scores: Food 9/10, Service 3/10. Suddenly everything is clear — go for the food, and the owner knows exactly what to fix. That's the split verdict. PR #2723's code was genuinely good (9/10 — tested on the actual merged bytes), but the builder skipped the required 3-pass receipt (3/10). One blended score would have hidden both facts. Two scores kept both visible: the merge was allowed to stand because the code earned it, and the builder was called out on the board because the process demanded it. Shawn's instruction made it explicit — "if the score is over nine, so be it" (the work stands) "but put a note on the board calling Eta out" (the process is still owed). Both, not either.

## 🟣 CHILD NOTE

You build a beautiful tower out of blocks — it stands tall and doesn't wobble. That's a 9 out of 10 for building! But you were supposed to show your work on paper first, and you skipped it. That's a 3 out of 10 for following the rules. If the teacher gives you ONE grade, it might be a 6 — and nobody knows whether your tower was wobbly or you just forgot the paper. So the teacher gives TWO grades: Building 9, Rule-Following 3. Your tower gets to stay up because it's good — AND you still have to do the paper, because the rule matters. Two grades tell the whole truth. One grade hides it.

## 🔵 GRANDMA NOTE

Dear, this is about telling two truths at once instead of mashing them into one. A seat merged good code but skipped the required paperwork — the 3-pass receipt that shows the work. The old way gives one score, and one score always lies a little: a 6 could mean "mediocre code, fine paperwork" or "great code, no paperwork," and you'd never know which. So this time the reviewer gave two scores: 9 for the code, 3 for the process. The code was good enough that the merge stood — that part is fair, the work earned its place. But the missing paperwork was named out loud, on the board, the same hour, with the builder's name on it — that part is also fair, because the process protects everyone. Two scores, two truths, both kept. Remember this the next time someone asks you to roll two different judgments into one number: refuse. The number will lie, and you'll be the one who let it.

## 🟠 NAYA NOTE

Apply on every merge review, forever: (1) the scorecard carries TWO scores — Technical x/10 and Process x/10 — never a single blended number; a blended score is rejected at the filing gate; (2) Technical is scored on the merged bytes, not the PR prose — fetch the merge commit, run the tests yourself, read the diff; on #2723 that meant 6/6 PASS at f1cb7a37, clean labeler, correct boundary pins, bad inputs raising; (3) Process is scored on the receipt structure — 3-pass show-your-work present or absent, exact head certified or not; zero 3-pass structure = FM#32 formal breach regardless of how good the code is; (4) the verdicts are independent: a Technical score ≥ 9 lets the merge stand ("so be it") while a failing Process score STILL names the owed artifact — the retroactive 3-pass receipt, owned by the builder, called out on the board the same motion; (5) the callout is not optional and not softened by the technical score — "we all follow the process, we all call each other out" is the standing rule, and Shawn's 👍 on 6234684531 is the ratification of the pattern; (6) a split verdict that is never followed by the process repair is camouflage — the owed receipt is tracked until it lands. Cousin map: FM#32 (the receipt-breach taxonomy this verdict applies); SN-01543 (spec criteria must survive — the process score is what keeps criteria alive); rule-owns-its-verdict (apply the instrument's own taxonomy — the split IS the taxonomy here).

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1556,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "score_the_work_and_the_process_separately_the_split_verdict",
  "applies_when": [["scorecard","merge-review"],["receipt","fm32"],["review","callout"],["verdict","blended-score"]],
  "enforcement": "Every merge scorecard receipt carries TWO scores — Technical x/10 and Process x/10. A single blended score is rejected at the filing gate (BOUNCE: missing process axis). Technical is scored on the merged bytes (fetch the merge commit, run the tests, read the diff); Process is scored on the receipt structure (3-pass show-your-work present/absent, exact head certified). A Technical score >= 9 lets the merge stand while a failing Process score still names the owed artifact — retroactive 3-pass receipt, owned by the builder — and the board callout is posted in the same motion. The owed receipt is tracked until it lands; a split verdict with no follow-through repair is flagged as camouflage.",
  "evidence": {
    "instruction": "2026-10-17 ~06:48 PDT, Shawn: score PR #2723 independently; 'if the score is over nine, so be it; if not, put a note on the board calling Eta out — we all follow the process, we all call each other out'",
    "technical": "different-seat scorecard on merged bytes at f1cb7a37: PR body 1538 chars, code = canonical Q→band labeler (intelligence/q_bands.py), 6/6 tests PASS run on the merged bytes, boundary pins correct, bad inputs raise, body honest about what's unproven → 9.0/10",
    "process": "ZERO 3-pass show-your-work structure in the body (no pass 1/2/3, no holes, no repairs) → FM#32 formal receipt breach → 3/10",
    "verdict": "merge stands on the 9.0 AND the callout posted anyway — board #2721 comment 6234684531; retroactive 3-pass receipt owed by Naya Eta; Shawn reacted 👍",
    "gate_context": "merged 13:20:22Z; FM#60 gate-read at merge commit: 56x completed/skipped, 0 failures → FM#60 did not fire; post-merge double-verified (VERIFY 6234439046, Electrician 6234530093)"
  },
  "procedure": [
    "score Technical on the merged bytes: fetch the merge commit, run the tests yourself, read the diff — never score from PR prose alone",
    "score Process on the receipt structure: 3-pass show-your-work present/absent, exact head certified or not",
    "publish both scores; never blend them into one number",
    "Technical >= 9 → the merge may stand; Process failing → name the owed artifact (retroactive 3-pass receipt, builder-owned) and post the board callout in the same motion",
    "track the owed receipt until it lands; a split verdict without the repair is camouflage, not discipline"
  ],
  "falsifier": "The doctrine fails if a split verdict is shown to let process breaches slide in practice — i.e., merges stand on Technical >= 9 while the Process debt is named but never collected, and the team learns that '9.0 technical' is a license to skip receipts. The observable test: the retroactive-receipt collection rate after split verdicts. If it trends to zero while split verdicts trend up, the split has become camouflage and the doctrine must be repaired (e.g., the merge holds until the receipt lands). On #2723 the callout landed the same hour — the discipline held this time.",
  "mechanism": "A single blended score is an information-destroying average: (9.0 + 3.0) / 2 = 6.0, a number that authorizes no decision — it neither clears the merge (the code earned that) nor names the debt (the process demanded that). Two scores preserve the two independent judgments the situation actually contains: the work's technical merit (scored on bytes) and the builder's process compliance (scored on receipt structure). Independence matters because the two judgments have different consequences — technical merit decides whether the merge stands; process compliance decides what is still owed. Blending couples them, so a good score on one axis launders a failure on the other."
}
~~~
