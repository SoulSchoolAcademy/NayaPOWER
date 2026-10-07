# Intelligent Block: SN-0584
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Capture without a receipt check leaks intelligence into chat history. A new nightly mechanism closes the loop: the Smart-Link SLA audit (`~/workspace/lane4/smart_link_sla_audit.py`) scans the day's memory log for intelligence items Shawn shared and checks each has a capture receipt — a Smart Note, a disposition record, a link-back. It exits 1 with REVIEW flags when items are unreceipted. The first run (2026-10-07) flagged 5: his pronunciation corrections baked into the reveal narration ("Naya Power" not "Nia Pow") plus corrected product definitions (Smart Mail = internal mail/communication layer for people and Smart Spaces; Smart Lists = save/group Smart Notes into categories + organize contacts into categories), the `learning_lock_in` authority grant 57d83ce5, his "decide like it's precious" directive-behavior order, the Naya Play per-layer product decision, and the Ask Naya intent-repair awaiting his re-test. Disposition is a closed vocabulary, owned by the main seat each morning: RECEIPT-FOUND-ELSEWHERE / QUEUED / GENUINE-MISS — and a genuine miss means capture late, return the link to Shawn, and log the cause. The durable lesson: "shared but never captured" must become an explicit, ownable disposition, or it silently vanishes.

## HUMAN NOTE
If Shawn tells you something valuable and you don't write it down where you can find it, it's gone — buried in chat. The nightly audit is the backstop: every morning it asks, "he said these five things — where did you put them?" and "I forgot" is not an acceptable answer.

## CHILD NOTE
Write it down — and then check that you actually wrote it down.

## GRANDMA NOTE
A receipt is how you prove you didn't lose what was handed to you.

## NAYA NOTE
Run the audit nightly; the main seat dispositions each REVIEW item the next morning. Disposition vocabulary is closed: RECEIPT-FOUND-ELSEWHERE / QUEUED / GENUINE-MISS. Genuine misses get: late capture, link returned to Shawn, cause logged in the daily log. No fourth option, no silent drops.

## MACHINE NOTE
{"sn":"SN-0584","mechanism":"smart_link_sla_audit.py","cadence":"nightly","verdict_shape":"exit 1 + REVIEW flags","first_run":"2026-10-07","items_flagged":5,"items":["reveal pronunciation + product-definition corrections","learning_lock_in grant 57d83ce5 + auto-learning direction","decide-like-its-precious directive-behavior order","Naya Play per-layer product decision","Ask Naya intent-matching + spoken-markdown repair"],"dispositions":["RECEIPT-FOUND-ELSEWHERE","QUEUED","GENUINE-MISS"],"genuine_miss_protocol":["capture-late","return-link-to-Shawn","log-cause"],"evidence":"#1354 comment 6048298163"}

## EVIDENCE
- SLA audit report: #1354 comment 6048298163 (2026-10-07 22:38 UTC), exit 1, 5 REVIEW flags.
- Audit script: `~/workspace/lane4/smart_link_sla_audit.py`; scanned today's memory log `~/memory/2026-10-07.md`.
