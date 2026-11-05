# INTELLIGENT BLOCK — SN-2059

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02059-hourly-post-step-missed-generation-is-not-posting
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shared-state record hourly_post_missed_20261105 + live board #3066 comment 6656707408 (2026-11-05T11:21:41Z): the 10:53Z hourly report was generated on time but its posting step never ran; caught only by the director's 11:08Z pass and posted late at 11:21Z. Named failure mode HOURLY-POST-STEP-MISSED.

## ✦ IN A NUTSHELL

The 10:53Z hourly report was generated on time — and never posted. Its posting step never ran, and nothing in the job said so: generation success masqueraded as job success, and the miss was caught only by the director's 11:08Z pass reading the board tail, with the report posted late at 11:21Z. The durable rule: **generation is not posting, and a job is not green until its delivery is verified at its destination.** Cousins: SN-045 (lost-delivery recovery — the delivery *channel* swallowed a finished announcement in an approval queue; recovery is repost the verified receipt, never rerun the work) and SN-1057 (a gate step must never swallow its own failure — an early `exit 0` before evaluating). This failure is neither: no step exited green early and no channel held the post — the posting step simply never *ran*, producing no exit code, no error, and no signal at all. The check is therefore at the destination, not in the job: the board tail must show the hourly comment inside the hour it covers, or the hour is a named miss, not a quiet hour.

## 🩷 HUMAN NOTE

Shawn — the hourly report for 10:53 was written perfectly on time, and then it just… never went up. No error, no failure, nothing red — the job looked done because the writing part finished. The only reason anyone noticed is that the director went and looked at the board and saw nothing there. The fix is simple and it's now the rule: a report isn't done when it's written, it's done when it's *seen* on the board. From now on, every hourly job proves its post landed — the board has to show it inside the hour it covers — or the hour gets named as a miss, not written off as quiet.

## 🟣 CHILD NOTE

Imagine you write a letter, put it in an envelope, and feel proud — but you never walk it to the mailbox. The letter is finished, but nobody ever gets it. Nobody tells you, because writing the letter felt like the whole job. The new rule: the job isn't done when the letter is written. It's done when someone sees it in the mailbox. Every time, you go check the mailbox.

## 🔵 GRANDMA NOTE

Dear, it's like baking a cake for the neighbors and leaving it on your own counter — beautifully baked, never delivered. The oven timer dinged, so the kitchen thought the job was done. But the neighbors never got cake, and nobody knew until someone walked over and looked. From now on, the rule is: you don't just bake, you ring the doorbell and watch them take it. If the cake isn't on their table, the job isn't done — no matter how nicely the oven behaved.

## 🟠 NAYA NOTE

For every seat that runs a scheduled job with a delivery step: never report a job green on generation alone. Generate and post are separate steps with no confirmation handshake, so a posting step that never runs produces no error, no exit code, and no signal — silence is the default failure mode, and only a reader of the destination can see it. The verification check is at the destination: after every hourly run, read the board tail and confirm the comment for that hour is present inside the hour it covers. If it is absent, the hour is a named miss (HOURLY-POST-STEP-MISSED) to be reported in the next director pass — never a quiet hour, never assumed posted. When a miss is caught, repost the already-generated report; do not regenerate the work.

## 🟢 MACHINE NOTE

```json
{
  "slug": "hourly-post-step-missed-generation-is-not-posting",
  "sn": "SN-2059",
  "title": "The Hourly Post Step Missed: Generation Is Not Posting",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["schedule", "hourly-report", "posting", "delivery", "job-completion", "step-missed"],
  "enforcement": "Every scheduled report job verifies its delivery landed at its destination within the window it covers — the board tail must show the hourly comment inside the hour it covers; a job whose generation succeeds but whose post is absent from the destination is RED, not quiet, and the miss is named (HOURLY-POST-STEP-MISSED) in the next director pass.",
  "falsifier": "A later audit proving the 10:53Z post step did run and the comment was posted on time (a read error, not a missed step) would collapse the lesson; a pipeline change to atomic generate+post with a delivery confirmation would retire the prescription.",
  "decision_changed": "How a scheduled job reports success: generation success no longer counts as job success — the job is green only when the post is verified at its destination; a quiet hour is reported as 'posted, verified' or as a named miss.",
  "mechanism": "Generate and post are separate steps with no confirmation handshake; the scheduler records the job as complete when generation exits, so a never-invoked post step produces no error, no exit code, and no signal — silence is the default failure mode, and only an external reader of the destination can see it.",
  "provenance": "Shared-state hourly_post_missed_20261105 + live board #3066 comment 6656707408 (2026-11-05T11:21:41Z): 10:53Z hourly report generated on time, posting step never ran, caught by director 11:08Z pass, posted late 11:21Z. Cousins: SN-045 lost-delivery recovery (channel swallowed the announcement) and SN-1057 gate-step failure-masking (early exit 0) — this failure is a step that never ran at all."
}
```
