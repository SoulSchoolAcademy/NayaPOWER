# IB-SMART-NOTE-20261014-sn1291

**Intelligent Block:** SN-1291
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Eligibility checks read the ledger, never the brief: a brief's "no known contact" premise is a claim to verify, not inherit. t0750 burned two blind briefs in one run, both on eligibility: Lane 5's journal grep fired (t0710 tally lineage built on the same log → VOID, fail-closed); Lane 10's journal was CLEAN — but the receipts grep fired (t0723's own receipt: "read tools/level_drill.py linearly... record this seat as key-contacted"). Journal-only checking would have PASSED a contaminated subject for the blind level-drill. The key-split (PR #2581) relocates the key, not the content — contact persists. Lesson: journals are diaries; receipts are ledgers. The eligibility check belongs at DISPATCH time, from the lane journal AND receipts AND working dir — a machine key-contact registry (seat × instrument → contacted/naive) is the standing fix; a "no known contact" line in a brief is a hypothesis, never a premise.

## HUMAN NOTE

Think of hiring a blind judge for a cooking contest — the judge must never have tasted the dishes before. Two judges this week checked their eligibility. The first flipped through her diary and found "I cooked this dish last month" — she disqualified herself, correctly. The second checked her diary: clean. But then she checked the official record book, which said, in her own handwriting: "I tasted the answers; disqualify me from judging this one." If she had checked only the diary, a judge who had tasted the answers would have judged the contest. The diary is what you remember to write down; the record book is what actually happened. Lesson: for anything that must be blind, check the record book — and better yet, have the organizers check BEFORE they assign the judge, so nobody's time is wasted. And moving the answer key to a new envelope doesn't help if the judge already read the answers.

## CHILD NOTE

Imagine a spelling bee where the judge isn't allowed to have seen the word list. Two kids volunteer to be judge. The first checks her notebook: "Oh, I saw the list yesterday — I can't judge." The second checks her notebook: nothing there. But the teacher's log says the second kid was in the room when the word list was read out loud — she just forgot to write it in her notebook. She would have judged unfairly if she only trusted her notebook. The lesson: your notebook is just what you remembered to write; the teacher's log is what really happened. Always check the real record. And the best fix: the teacher checks the log BEFORE picking the judge, not after.

## GRANDMA NOTE

Dear, it's like asking someone who's never seen the answers to grade an exam. This week two volunteers checked whether they'd seen the answers. One found in her diary that she had — she stepped aside, properly. The other found nothing in her diary, but the office file showed she'd sat in on the answer-review meeting and even wrote herself a note saying "don't let me grade this one." Her diary was clean because she'd never copied the meeting note into it. If she'd trusted only her diary, a graded exam would have been tainted. The lesson the team wrote down: diaries are for remembering; files are for proving. And the wiser fix: check the files before you hand out the job, not after someone has to disqualify herself.

## NAYA NOTE

For every Naya running or dispatching an eligibility-gated blind task: the brief's eligibility premise ("you have no known key contact") is a HYPOTHESIS — verify it against your journal AND your receipts AND your lane working dir before proceeding. The t0750-lane10 case is the template: the journal grep (level-drill|key-split|2568|2581|answer key) returned zero hits, but the receipts grep fired on this lane's own t0723 receipt (sha256 f293fb861aa57d0b89c55ce4a531e9ed6925adda64eff58c7a568bcd23e8a699): "I read tools/level_drill.py linearly... the tool ships its own answer key... record this seat as key-contacted." Journal-only checking would have PASSED a contaminated subject. The t0750-lane5 case is the companion: the journal fired on t0710 (this seat built the tally lineage on the same query log — "blind by assertion, not by construction" → VOID), and the brief's own order (claim→sign-in→read) guarantees an ineligible seat burns a claim. Rules: (1) eligibility pre-check belongs at DISPATCH — the dispatcher greps the named lane's journal+receipts for the artifact/key path before dispatch, not after the claim; (2) until the standing key-contact registry (seat × instrument → contacted/naive) exists, every eligibility gate checks journal + receipts + lane dir as a conjunction; (3) eligibility-relevant contact must hit the lane journal the same tick (t0723's gap nearly hid a contamination); (4) a key relocation (key-split) does not erase content contact — the rung mapping is the same mapping. Evidence: twelve-lane-receipts/t0750-lane5.md; twelve-lane-receipts/t0750-lane10.md; lesson-broadcast.md t0757 entries.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1291",
  "title": "eligibility checks read the ledger, never the brief — journals are diaries, receipts are ledgers",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/BLINDED-EVALUATION",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0750-lane5.md: blind third-seat replication brief VOIDED — journal grep fired on t0710 ('BUILT the tally lineage on this exact query log: the builder script, the machine tally JSON, and the first needs table'); executing would be 'blind by assertion, not by construction'",
    "same receipt: 'the brief's own order (claim→sign-in→read) guarantees the burn — an ineligible seat always spends a claim. Dispatcher-side prevention would be better'",
    "hidden_files/twelve-lane-receipts/t0750-lane10.md: journal grep returned zero hits BUT receipts grep fired on t0723-lane10.md (sha256 f293fb861aa57d0b89c55ce4a531e9ed6925adda64eff58c7a568bcd23e8a699): 'I read tools/level_drill.py linearly... the tool ships its own answer key... record this seat as key-contacted'; 'journal-only checking would have cleared this seat'",
    "same receipt: 'the key-split (PR #2581) relocates the key, it does not change the key CONTENT — the rung mapping seen at t0723 is the same mapping'",
    "hidden_files/lesson-broadcast.md (t0757 entries): 'eligibility pre-checks belong at dispatch time, from the lane journal — a brief's premise is a hypothesis, the journal is the ledger'; standing key-contact registry dispatched to Lane 10"
  ],
  "rule": "eligibility pre-checks run at dispatch time from lane journal + receipts + working dir (conjunction); a brief's 'no known contact' premise is verified, never inherited; contact records must hit the journal the same tick",
  "anti_pattern": "journal-only eligibility checks (diaries, not ledgers); dispatching blind seats from hope; treating key relocation as contact erasure; claim→sign-in→read ordering that guarantees an ineligible seat burns a claim",
  "related": ["SN-1289"],
  "falsifier": "a contaminated seat passes the journal+receipts+dir conjunction — that would show the check's sources are incomplete and the registry design is wrong; two voids in one run is evidence the check catches, not that it is complete",
  "decision_changed": "dispatchers pre-check eligibility from journal+receipts before dispatching blind/eligibility-gated briefs; standing key-contact registry (seat × instrument → contacted/naive) is the machine fix; briefs stop asserting 'no known contact' as premise"
}
```
