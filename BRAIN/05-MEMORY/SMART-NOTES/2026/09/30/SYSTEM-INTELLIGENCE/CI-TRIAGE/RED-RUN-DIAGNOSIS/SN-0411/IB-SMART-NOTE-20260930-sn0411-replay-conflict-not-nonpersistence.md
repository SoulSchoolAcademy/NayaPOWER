# SN-0411 — A Replay Conflict Is Not Proof of Non-Persistence: Check the Canonical Store Before Classifying

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0411-replay-conflict-not-nonpersistence
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
The HTTP-400/409 replay failures on the NayaNET intelligence commit path were root-caused from live Supabase logs: PostgreSQL emitted EVENT_ID_REPLAY with SQLSTATE 23505 at the exact failing timestamps, from public.nayanet_intelligence_commit through the runtime bridge. The deeper finding overturned the working theory: the retried event had FULLY persisted — SUCCESS receipt, event, block, lineage, relationships, index, checkpoint. The workflow failed downstream and retried the same event key; the writer treated every repeated key as an unconditional conflict. So the replay error did not mean "nothing was saved" — it meant "everything was already saved and the writer refused to say so." Two lessons: (1) a replay conflict is not evidence of non-persistence — read the canonical store before classifying the failure; (2) the canonical repair is at the writer: same event key + same canonical payload + complete persisted lineage → reconcile to the already-persisted receipt/lineage with no duplicate writes; changed payload or incomplete lineage → fail closed. Rotating event IDs (the R2 workaround) recovered the instance but left the seam — fix the seam, not the caller.

## HUMAN NOTE
Imagine mailing a letter, the post office loses your receipt, so you mail it again — and the post office rejects the second letter saying "duplicate." You'd assume the first letter never arrived. But it did arrive; the post office just had no way to say "already delivered, here's your original receipt." The fix isn't to keep changing the envelope so it looks new (that just hides the problem) — it's to teach the post office to answer "already delivered" when the letter is identical. And the debugging rule: when the system says "duplicate," check the shelf before concluding the package never arrived.

## CHILD NOTE
You hand in your homework, the teacher's computer crashes before printing your receipt, so you hand it in again — and the computer says "already handed in, ERROR!" You might think your homework was lost. But it's sitting right there in the pile, graded and all. The computer just didn't know how to say "got it already, here's your first receipt." Always check the pile before panicking — and teach the computer to check the pile too.

## GRANDMA NOTE
Dear, it's like this: the machine shouted "duplicate!" and everyone assumed the work was lost. But the work was safe in the drawer — the machine simply couldn't say "I already have it." The lesson for anyone fixing such things: open the drawer before you declare a disaster. And the real fix isn't sending the letter with a different stamp each time — it's teaching the machine to recognize its own handwriting and hand back the original receipt.

## NAYA NOTE
This is a red-run diagnosis doctrine, not an idempotency-credit doctrine (see SN-0070 for the conjuncts; this is the field application). The classification error to avoid: treating the writer's conflict signal as a statement about what persisted. The writer's signal only says "I saw this key before" — persistence state lives in the store, and only the store answers it. The repair decision is the durable part: exact-replay reconciliation (key + canonical payload + complete lineage → original receipt, no duplicate writes) with fail-closed on any deviation. Note the scope discipline in the sign-in: the seat repaired the actual responsible seam (public.nayanet_intelligence_commit) rather than shipping another caller-side workaround, and staged source + regression proof only, leaving the production migration at its protected gate.

## MACHINE NOTE
```json
{
  "sn_id": "SN-0411",
  "slug": "replay-conflict-not-nonpersistence",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/RED-RUN-DIAGNOSIS",
  "rule": "a replay conflict asserts key-reuse, not non-persistence; read the canonical store before classifying; repair = exact-replay reconciliation at the writer (same key + same canonical payload + complete lineage -> original receipt, no duplicate writes; changed payload or incomplete lineage -> fail closed)",
  "evidence": {
    "root_cause": "#1354 comment 6005791972 (2026-10-05, Captain): HTTP-400 root cause proven from live Supabase logs for run 37388821051 — PostgreSQL EVENT_ID_REPLAY, SQLSTATE 23505, at exact failing timestamps, from public.nayanet_intelligence_commit through the runtime bridge",
    "reclassification": "#1354 comment 6006141293 (2026-10-05, Captain SIGN-IN): 'the old SN-0357 event did not partially persist — it fully persisted a SUCCESS receipt, event, block, lineage, relationships, index, and checkpoint. The workflow failed downstream, then retried the same event key.'",
    "scope_lesson": "'Changing event IDs (R2) recovered SN-0357, but it does not fix the underlying seam.'"
  },
  "pairs_with": ["SN-0070", "SN-0370", "SN-0352"],
  "captured": "2026-10-05"
}
```
